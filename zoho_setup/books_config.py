"""Creates Books VAT rates, the item price list and suppliers. Safe to re-run (matches by name)."""
import csv

from . import normalize

BOOKS = "/books/v3"


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return [r for r in csv.DictReader(f) if not normalize.is_example(r)]


def _list_all(client, org_id, path, key, params=None):
    out, page = [], 1
    while True:
        body = client.get(path, params={"organization_id": org_id, "page": page,
                                        "per_page": 200, **(params or {})}) or {}
        out += body.get(key, [])
        if not body.get("page_context", {}).get("has_more_page"):
            return out
        page += 1


def _created(report, name, resp, key):
    if resp is None:
        report.add("Books", name, "would create")
        return None
    if resp.get("code") == 0:
        report.add("Books", name, "created")
        return resp.get(key)
    report.add("Books", name, "failed", resp.get("message", ""))
    return None


def sync_taxes(client, org_id, taxes, report):
    existing = {t["tax_name"]: t["tax_id"] for t in
                (client.get(f"{BOOKS}/settings/taxes", params={"organization_id": org_id}) or {})
                .get("taxes", [])}
    ids = dict(existing)
    for tax in taxes:
        name = tax["tax_name"]
        if name in existing:
            report.add("Books", f"tax {name}", "exists")
            continue
        resp = client.post(f"{BOOKS}/settings/taxes", params={"organization_id": org_id}, json={
            "tax_name": name, "tax_percentage": tax["tax_percentage"], "tax_type": "tax",
        })
        created = _created(report, f"tax {name}", resp, "tax")
        ids[name] = created["tax_id"] if created else f"<new {name}>"
    return ids


def sync_items(client, org_id, rows, tax_ids, report):
    existing = {i["name"] for i in _list_all(client, org_id, f"{BOOKS}/items", "items")}
    for row in rows:
        name = row["Name"].strip()
        if name in existing:
            report.add("Books", f"item {name}", "exists")
            continue
        tax_id = tax_ids.get(row["Tax"].strip())
        if not tax_id:
            report.add("Books", f"item {name}", "failed", f"unknown tax {row['Tax']!r}")
            continue
        item = {"name": name, "rate": float(row["Rate"]), "product_type": row["Type"].strip()}
        if not tax_id.startswith("<new"):
            item["tax_id"] = tax_id
        for col, key in (("Unit", "unit"), ("SKU", "sku"), ("Description", "description")):
            if row.get(col, "").strip():
                item[key] = row[col].strip()
        resp = client.post(f"{BOOKS}/items", params={"organization_id": org_id}, json=item)
        _created(report, f"item {name}", resp, "item")


def sync_vendors(client, org_id, rows, report):
    existing = {c["contact_name"] for c in _list_all(
        client, org_id, f"{BOOKS}/contacts", "contacts", {"contact_type": "vendor"})}
    for row in rows:
        name = row["Company Name"].strip()
        if name in existing:
            report.add("Books", f"supplier {name}", "exists")
            continue
        notes = row.get("Notes", "").strip()
        if row.get("Tax Registration Number", "").strip():
            notes = f"VAT no: {row['Tax Registration Number'].strip()}\n{notes}".strip()
        vendor = {
            "contact_name": name,
            "company_name": name,
            "contact_type": "vendor",
            "notes": notes,
            "contact_persons": [{
                "first_name": row.get("Contact Name", "").strip() or "Accounts",
                "email": row.get("EmailID", "").strip(),
                "phone": row.get("Phone", "").strip(),
                "is_primary_contact": True,
            }],
        }
        if row.get("Payment Terms", "").strip():
            vendor["payment_terms"] = int(row["Payment Terms"])
            vendor["payment_terms_label"] = row.get("Payment Terms Label", "").strip() or f"Net {row['Payment Terms']}"
        resp = client.post(f"{BOOKS}/contacts", params={"organization_id": org_id}, json=vendor)
        _created(report, f"supplier {name}", resp, "contact")


def sync(client, org_id, config, report):
    tax_ids = sync_taxes(client, org_id, config["taxes"], report)
    sync_items(client, org_id, read_csv(config["items_file"]), tax_ids, report)
    sync_vendors(client, org_id, read_csv(config["suppliers_file"]), report)
