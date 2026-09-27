"""Creates the CRM list views (custom views) in config/crm_views.yaml. Safe to re-run.

Uses CRM API v8 POST /settings/custom_views (scope ZohoCRM.settings.custom_views.ALL),
as described in Zoho's own OpenAPI files: https://github.com/zoho/crm-oas (v8.0/custom_views).
"""
CRM = "/crm/v8"


def _field_ids(client, module):
    body = client.get(f"{CRM}/settings/fields", params={"module": module}) or {}
    return {f["api_name"]: f["id"] for f in body.get("fields", [])}


def _existing_views(client, module):
    body = client.get(f"{CRM}/settings/custom_views", params={"module": module}) or {}
    return {v["name"] for v in body.get("custom_views", [])}


def _criteria(node, ids):
    """Adds field ids to a criteria tree written with api_names. Raises KeyError on unknown fields."""
    if "group" in node:
        return {"group_operator": node["group_operator"],
                "group": [_criteria(n, ids) for n in node["group"]]}
    api, value = node["field"], node["value"]
    kind = "pre_defined" if str(value).startswith("${") else "value"
    return {"field": {"api_name": api, "id": ids[api]}, "comparator": node["comparator"],
            "value": value, "type": kind}


def _used_fields(spec):
    names = list(spec["fields"]) + ([spec["sort_by"]] if spec.get("sort_by") else [])
    stack = [spec.get("criteria") or {}]
    while stack:
        node = stack.pop()
        stack += node.get("group", [])
        if "field" in node:
            names.append(node["field"])
    return names


def view_payload(spec, ids):
    view = {
        "name": spec["name"],
        "access_type": "public",
        "fields": [{"api_name": f, "id": ids[f]} for f in spec["fields"]],
    }
    if spec.get("criteria"):
        view["criteria"] = _criteria(spec["criteria"], ids)
    if spec.get("sort_by"):
        view["sort_by"] = {"api_name": spec["sort_by"], "id": ids[spec["sort_by"]]}
        view["sort_order"] = spec.get("sort_order", "asc")
    return {"custom_views": [view]}


def sync(client, config, report):
    for module, views in config["views"].items():
        ids = _field_ids(client, module)
        if not ids:
            report.add("CRM views", module, "blocked", "module or its fields not found; run crm-schema first")
            continue
        existing = _existing_views(client, module)
        for spec in views:
            name = f"{module}: {spec['name']}"
            if spec["name"] in existing:
                report.add("CRM views", name, "exists")
                continue
            missing = sorted({f for f in _used_fields(spec) if f not in ids})
            if missing:
                report.add("CRM views", name, "blocked", "fields not in CRM: " + ", ".join(missing))
                continue
            resp = client.post(f"{CRM}/settings/custom_views", params={"module": module},
                               json=view_payload(spec, ids))
            if resp is None:
                report.add("CRM views", name, "would create")
                continue
            result = (resp.get("custom_views") or [{}])[0]
            if str(result.get("status", "")).lower() == "success":
                report.add("CRM views", name, "created")
            else:
                report.add("CRM views", name, "failed", result.get("message") or str(resp)[:200])
