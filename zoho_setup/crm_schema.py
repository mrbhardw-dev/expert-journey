"""Creates the CRM custom fields listed in config/crm_schema.yaml. Safe to re-run."""
CRM = "/crm/v6"

TYPE_MAP = {
    "text": "text",
    "textarea": "textarea",
    "picklist": "picklist",
    "checkbox": "boolean",
    "date": "date",
    "datetime": "datetime",
    "integer": "integer",
    "decimal": "double",
    "currency": "currency",
    "phone": "phone",
    "email": "email",
    "lookup": "lookup",
}


def field_payload(spec):
    kind = spec["type"]
    if kind not in TYPE_MAP:
        raise ValueError(f"unknown field type {kind!r} for {spec['label']}")
    payload = {"field_label": spec["label"], "data_type": TYPE_MAP[kind]}
    if kind == "text":
        payload["length"] = spec.get("length", 255)
    if kind == "picklist":
        payload["pick_list_values"] = [
            {"display_value": v, "actual_value": v} for v in spec["values"]
        ]
    if kind == "lookup":
        payload["lookup"] = {"module": {"api_name": spec["module"]}}
    return payload


def _first_result(resp):
    for key in ("fields", "data"):
        if resp and resp.get(key):
            return resp[key][0]
    return {}


def _existing_fields(client, module):
    body = client.get(f"{CRM}/settings/fields", params={"module": module}) or {}
    return {f["api_name"] for f in body.get("fields", [])}


def sync(client, schema, report):
    report.manual_steps += schema.get("manual_steps", [])
    body = client.get(f"{CRM}/settings/modules") or {}
    modules = {m["api_name"] for m in body.get("modules", [])}

    for module, mspec in schema["modules"].items():
        if module not in modules:
            report.add("CRM", f"module {module}", "blocked",
                       "create it in the CRM UI first (docs/01-crm-setup.md), then re-run")
            continue
        existing = _existing_fields(client, module)
        created = []
        for spec in mspec["fields"]:
            name = f"{module}.{spec['api_name']}"
            if spec["api_name"] in existing:
                report.add("CRM", name, "exists")
                continue
            if spec["type"] == "lookup" and spec["module"] not in modules:
                report.add("CRM", name, "blocked", f"lookup target {spec['module']} missing")
                continue
            resp = client.post(f"{CRM}/settings/fields", params={"module": module},
                               json={"fields": [field_payload(spec)]})
            if resp is None:
                report.add("CRM", name, "would create")
                continue
            result = _first_result(resp)
            if str(result.get("status", "")).lower() == "success":
                report.add("CRM", name, "created")
                created.append(spec["api_name"])
            else:
                report.add("CRM", name, "failed", result.get("message") or str(resp)[:200])

        if created:
            # Zoho picks the API name. Make sure it matches what the Deluge scripts use.
            now = _existing_fields(client, module)
            for api in created:
                if api not in now:
                    report.add("CRM", f"{module}.{api}", "failed",
                               "created under a different API name; rename it in Setup > Fields")
