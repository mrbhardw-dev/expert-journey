import os

import pytest
import yaml

from zoho_setup import books_config, crm_schema, crm_views, crm_workflows, importer, normalize, validate
from zoho_setup.__main__ import main
from zoho_setup.report import Report

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(autouse=True)
def repo_root(monkeypatch):
    monkeypatch.chdir(ROOT)


def load(name):
    with open(os.path.join(ROOT, "config", name), encoding="utf-8") as f:
        return yaml.safe_load(f)


class FakeClient:
    """Answers GETs from a dict keyed by path; records writes. dry_run mimics ZohoClient."""

    def __init__(self, gets, dry_run=True, write_response=None):
        self.gets, self.dry_run, self.writes = gets, dry_run, []
        self.write_response = write_response or {"fields": [{"status": "success"}]}

    def get(self, path, params=None):
        value = self.gets.get(path, {})
        return value(params) if callable(value) else value

    def _write(self, method, path, params, json):
        self.writes.append((method, path, params, json))
        return None if self.dry_run else self.write_response

    def post(self, path, params=None, json=None):
        return self._write("POST", path, params, json)

    def put(self, path, params=None, json=None):
        return self._write("PUT", path, params, json)


# ---- normalize ----

@pytest.mark.parametrize("raw, expected", [
    ("191d12345", "191-D-12345"),
    ("191 D 12345", "191-D-12345"),
    ("12-ky-123", "12-KY-123"),
    ("ABC 123", None),
    ("", None),
])
def test_registration(raw, expected):
    assert normalize.registration(raw) == expected


@pytest.mark.parametrize("raw, expected", [
    ("087 123 4567", "+353871234567"),
    ("+353 87 123 4567", "+353871234567"),
    ("00353871234567", "+353871234567"),
    ("353871234567", "+353871234567"),
    ("12", None),
])
def test_mobile(raw, expected):
    assert normalize.mobile(raw) == expected


def test_local_datetime_uses_irish_time():
    assert normalize.local_datetime("2026-07-01 09:00") == "2026-07-01T09:00:00+01:00"
    assert normalize.local_datetime("2026-01-05 09:00") == "2026-01-05T09:00:00+00:00"


def test_api_name_from_label():
    assert normalize.api_name_from_label("Current Mileage (km)") == "Current_Mileage_km"
    assert normalize.api_name_from_label("NCT Due") == "NCT_Due"


# ---- validation ----

def test_repo_config_is_valid():
    assert validate.run(load("crm_schema.yaml"), load("books.yaml")) == []


def test_schema_label_mismatch_is_caught():
    schema = {"modules": {"Vehicles": {"fields": [
        {"label": "Mileage (km)", "api_name": "Mileage", "type": "integer"}]}}}
    assert "would produce API name" in validate.check_schema(schema)[0]


def test_deluge_unknown_field_is_caught(tmp_path):
    (tmp_path / "x.dg").write_text('rec.get("Not_A_Field");')
    errors = validate.check_deluge({"modules": {}}, str(tmp_path))
    assert "Not_A_Field" in errors[0]


def test_cli_validate():
    assert main(["validate"]) == 0


# ---- CRM schema ----

def test_field_payloads():
    assert crm_schema.field_payload({"label": "Make", "type": "picklist", "values": ["Ford"]}) == {
        "field_label": "Make", "data_type": "picklist",
        "pick_list_values": [{"display_value": "Ford", "actual_value": "Ford"}]}
    assert crm_schema.field_payload({"label": "Vehicle", "type": "lookup", "module": "Vehicles"})[
        "lookup"] == {"module": {"api_name": "Vehicles"}}


def test_crm_schema_dry_run_blocks_missing_modules_and_skips_existing():
    schema = load("crm_schema.yaml")
    client = FakeClient({
        "/crm/v6/settings/modules": {"modules": [{"api_name": "Contacts"}, {"api_name": "Accounts"}]},
        "/crm/v6/settings/fields": {"fields": [{"api_name": "Eircode"}]},
    })
    report = Report(dry_run=True)
    crm_schema.sync(client, schema, report)
    outcomes = {name: outcome for _, name, outcome, _ in report.rows}
    assert outcomes["Contacts.Eircode"] == "exists"
    assert outcomes["Contacts.Customer_Type"] == "would create"
    assert outcomes["module Vehicles"] == "blocked"
    assert outcomes["module Job_Cards"] == "blocked"
    assert all(w[1] == "/crm/v6/settings/fields" for w in client.writes)
    assert report.manual_steps


def test_crm_schema_apply_flags_renamed_field():
    schema = {"modules": {"Contacts": {"fields": [{"label": "Eircode", "api_name": "Eircode", "type": "text"}]}}}
    client = FakeClient({
        "/crm/v6/settings/modules": {"modules": [{"api_name": "Contacts"}]},
        "/crm/v6/settings/fields": {"fields": []},  # still missing after "create"
    }, dry_run=False)
    report = Report(dry_run=False)
    crm_schema.sync(client, schema, report)
    assert [r[2] for r in report.rows] == ["created", "failed"]


# ---- Books ----

def test_books_dry_run_creates_only_missing():
    client = FakeClient({
        "/books/v3/settings/taxes": {"taxes": [{"tax_name": "VAT 23%", "tax_id": "t23"}]},
        "/books/v3/items": {"items": [{"name": "Oil filter"}], "page_context": {"has_more_page": False}},
        "/books/v3/contacts": {"contacts": []},
    })
    report = Report(dry_run=True)
    books_config.sync(client, "org1", load("books.yaml"), report)
    outcomes = {name: outcome for _, name, outcome, _ in report.rows}
    assert outcomes["tax VAT 23%"] == "exists"
    assert outcomes["tax VAT 13.5%"] == "would create"
    assert outcomes["item Oil filter"] == "exists"
    assert outcomes["item Engine oil (per litre)"] == "would create"
    # The example supplier row is skipped.
    assert not any("Example Motor Factors" in name for name in outcomes)
    item_posts = [w for w in client.writes if w[1] == "/books/v3/items"]
    assert {"name": "Engine oil (per litre)", "rate": 12.0, "product_type": "goods",
            "tax_id": "t23", "sku": "PRT-OIL-L"} in [w[3] for w in item_posts]


# ---- import ----

def write_csv(path, headers, rows):
    import csv
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        for r in rows:
            w.writerow({h: r.get(h, "") for h in headers})


def test_import_dry_run(tmp_path):
    write_csv(tmp_path / "customers.csv", importer.CUSTOMER_HEADERS,
              [{"First Name": "Sean", "Last Name": "Byrne", "Mobile": "087 555 1234"}])
    write_csv(tmp_path / "vehicles.csv", importer.VEHICLE_HEADERS,
              [{"Registration": "201d999", "Customer Mobile": "0875551234", "Make": "Ford"}])
    write_csv(tmp_path / "job_history.csv", importer.JOB_HEADERS,
              [{"Registration": "201-D-999", "Booked For": "2026-02-01 10:00", "Job Type": "Repair"}])
    assert validate.check_data_dir(str(tmp_path)) == []

    client = FakeClient({})  # nothing exists in CRM yet
    report = Report(dry_run=True)
    importer.run(client, str(tmp_path), report)
    assert [r[2] for r in report.rows] == ["would create"] * 3
    contact = client.writes[0][3]["data"][0]
    assert contact["Mobile"] == "+353875551234"
    assert "Consent_Date" not in contact  # blanks are not sent
    vehicle = client.writes[1][3]["data"][0]
    assert vehicle["Name"] == "201-D-999" and "Customer" not in vehicle
    job = client.writes[2][3]["data"][0]
    assert job["Import_Key"] == "201-D-999|2026-02-01 10:00"
    assert job["Booked_For"] == "2026-02-01T10:00:00+00:00"


def test_import_updates_existing_vehicle():
    client = FakeClient({"/crm/v6/Vehicles/search": {"data": [{"id": "v1"}]}}, dry_run=False,
                        write_response={"data": [{"status": "success", "details": {"id": "v1"}}]})
    report = Report(dry_run=False)
    row = {h: "" for h in importer.VEHICLE_HEADERS} | {"Registration": "191-D-1"}
    importer.import_vehicles(client, [row], {}, report)
    assert client.writes[0][0] == "PUT" and client.writes[0][3]["data"][0]["id"] == "v1"
    assert report.rows[0][2] == "updated"


def test_import_refuses_in_ci(monkeypatch, tmp_path):
    for name, headers in importer.FILES.items():
        write_csv(tmp_path / name, headers, [])
    monkeypatch.setenv("CI", "true")
    assert main(["import-data", "--data-dir", str(tmp_path)]) == 1


def test_search_criteria_escaping():
    assert importer._escape("a(b),c") == r"a\(b\)\,c"


# ---- crm views ----

def test_crm_views_dry_run_skips_existing_blocks_missing_and_adds_ids():
    config = load("crm_views.yaml")
    job_fields = [a for v in config["views"]["Job_Cards"] for a in crm_views._used_fields(v)]
    fields = {"Job_Cards": {"fields": [{"api_name": a, "id": f"id-{a}"} for a in set(job_fields)]},
              "Vehicles": {"fields": [{"api_name": "Name", "id": "id-Name"}]}}
    views = {"Job_Cards": {"custom_views": [{"name": "On the ramp"}]}}
    client = FakeClient({
        "/crm/v8/settings/fields": lambda p: fields[p["module"]],
        "/crm/v8/settings/custom_views": lambda p: views.get(p["module"], {}),
    })
    report = Report(dry_run=True)
    crm_views.sync(client, config, report)

    outcome = {name: out for _, name, out, _ in report.rows}
    assert outcome["Job_Cards: On the ramp"] == "exists"
    assert outcome["Job_Cards: Not paid"] == "would create"
    assert outcome["Vehicles: Service due next 30 days"] == "blocked"
    posted = [w[3]["custom_views"][0] for w in client.writes]
    assert "On the ramp" not in [v["name"] for v in posted]
    today = next(v for v in posted if v["name"] == "Today in the workshop")
    booked, stage = today["criteria"]["group"]
    assert booked == {"field": {"api_name": "Booked_For", "id": "id-Booked_For"},
                      "comparator": "equal", "value": "${TODAY}", "type": "pre_defined"}
    assert stage["type"] == "value" and stage["value"] == ["Collected", "Cancelled"]
    assert today["access_type"] == "public" and today["sort_by"]["id"] == "id-Booked_For"


# ---- crm workflows ----

def _workflow_client(existing_rules=None, existing_tasks=None, dry_run=True, write_response=None):
    ids = lambda names: {"fields": [{"api_name": a, "id": f"id-{a}"} for a in names]}
    fields = {
        "Tasks": ids(["Subject", "Due_Date", "Status", "Priority", "Description"]),
        "Vehicles": ids(["Name", "Next_Service_Due", "NCT_Due", "Vehicle_Status"]),
        "Job_Cards": ids(["Name", "Stage", "Payment_Status"]),
    }
    return FakeClient({
        "/crm/v8/settings/modules": {"modules": [{"api_name": m, "id": f"mod-{m}"}
                                                 for m in ("Vehicles", "Job_Cards", "Tasks")]},
        "/crm/v8/settings/fields": lambda p: fields[p["module"]],
        "/crm/v8/settings/automation/workflow_rules":
            lambda p: {"workflow_rules": [{"name": n, "id": "r1"} for n in (existing_rules or {}).get(p["module"], [])]},
        "/crm/v8/settings/automation/tasks":
            lambda p: {"tasks": [{"name": n, "id": i} for n, i in (existing_tasks or {}).get(p["module"], {}).items()]},
    }, dry_run=dry_run, write_response=write_response)


def test_crm_workflows_dry_run():
    client = _workflow_client(existing_rules={"Vehicles": ["NCT due in 30 days"]})
    report = Report(dry_run=True)
    crm_workflows.sync(client, load("crm_workflows.yaml"), report)
    outcome = {name: out for _, name, out, _ in report.rows}
    assert outcome["Vehicles: NCT due in 30 days"] == "exists"
    assert outcome["Vehicles: Service due in 14 days"] == "would create"
    assert outcome["Job_Cards: Collected but not paid"] == "would create"
    assert not report.failed

    task = next(w[3]["tasks"][0] for w in client.writes if w[1].endswith("/automation/tasks"))
    assert task["name"] == "Service due: ${!Vehicles.Name}" and task["module"]["id"] == "mod-Vehicles"
    subject = next(m for m in task["field_mappings"] if m["field"]["api_name"] == "Subject")
    assert subject == {"field": {"api_name": "Subject", "id": "id-Subject"}, "type": "merge_field",
                       "value": "Service due: ${!Vehicles.Name}"}

    rules = {w[3]["workflow_rules"][0]["name"]: w[3]["workflow_rules"][0]
             for w in client.writes if w[1].endswith("/workflow_rules")}
    service = rules["Service due in 14 days"]
    assert service["execute_when"]["type"] == "date_or_datetime"
    assert service["execute_when"]["details"]["unit"] == -14
    assert service["conditions"][0]["criteria_details"]["criteria"]["value"] == "Active"
    unpaid = rules["Collected but not paid"]["conditions"][0]
    assert unpaid["scheduled_actions"][0]["execute_after"] == {"period": "days", "unit": 3}
    assert unpaid["criteria_details"]["criteria"]["value"] == ["Paid", "Account Customer"]


def test_crm_workflows_apply_reuses_existing_task_template():
    client = _workflow_client(
        existing_tasks={"Job_Cards": {"Not collected yet: ${!Job_Cards.Name}": "t-existing"}},
        dry_run=False,
        write_response={"tasks": [{"status": "success", "details": {"id": "t-new"}}],
                        "workflow_rules": [{"status": "success", "details": {"id": "r-new"}}]})
    config = load("crm_workflows.yaml")
    config["rules"] = [r for r in config["rules"] if r["name"] == "Ready but not collected"]
    report = Report(dry_run=False)
    crm_workflows.sync(client, config, report)
    assert [w[1] for w in client.writes] == ["/crm/v8/settings/automation/workflow_rules"]
    actions = client.writes[0][3]["workflow_rules"][0]["conditions"][0]["scheduled_actions"][0]["actions"]
    assert actions == [{"type": "tasks", "id": "t-existing"}]
    assert report.rows[-1][2] == "created"


def test_crm_workflows_config_references_known_tasks():
    config = load("crm_workflows.yaml")
    keys = {t["key"] for t in config["tasks"]}
    for rule in config["rules"]:
        assert set(rule["tasks"]) <= keys
        for key in rule["tasks"]:
            assert next(t for t in config["tasks"] if t["key"] == key)["module"] == rule["module"]


def test_crm_views_one_rejected_view_does_not_stop_the_rest():
    from zoho_setup.client import ZohoError
    config = {"views": {"Vehicles": [
        {"name": "A", "fields": ["Name"]}, {"name": "B", "fields": ["Name"]}]}}

    class Rejecting(FakeClient):
        def post(self, path, params=None, json=None):
            if json["custom_views"][0]["name"] == "A":
                raise ZohoError("HTTP 400")
            return {"custom_views": [{"status": "success"}]}

    client = Rejecting({"/crm/v8/settings/fields": {"fields": [{"api_name": "Name", "id": "1"}]}}, dry_run=False)
    report = Report(dry_run=False)
    crm_views.sync(client, config, report)
    assert [(n, o) for _, n, o, _ in report.rows] == [("Vehicles: A", "failed"), ("Vehicles: B", "created")]
