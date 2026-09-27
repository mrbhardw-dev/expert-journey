"""Creates the CRM workflow rules (and their task templates) in config/crm_workflows.yaml. Safe to re-run.

Uses CRM API v8 as described in Zoho's own OpenAPI files (https://github.com/zoho/crm-oas, v8.0):
POST /settings/automation/tasks and POST /settings/automation/workflow_rules
(scopes ZohoCRM.settings.automation_actions.ALL, ZohoCRM.settings.workflow_rules.ALL).
"""
CRM = "/crm/v8"
SECTION = "CRM workflows"


def _module_ids(client):
    body = client.get(f"{CRM}/settings/modules") or {}
    return {m["api_name"]: m["id"] for m in body.get("modules", [])}


def _field_ids(client, module):
    body = client.get(f"{CRM}/settings/fields", params={"module": module}) or {}
    return {f["api_name"]: f["id"] for f in body.get("fields", [])}


def _existing(client, path, key, module):
    body = client.get(f"{CRM}{path}", params={"module": module}) or {}
    return {item["name"]: item.get("id") for item in body.get(key, [])}


def _ref(ids, api_name):
    return {"api_name": api_name, "id": ids[api_name]}


def task_payload(spec, module_ids, task_fields):
    def mapping(field, kind, value):
        return {"field": _ref(task_fields, field), "type": kind, "value": value}

    maps = [
        mapping("Subject", "merge_field" if "${" in spec["subject"] else "static", spec["subject"]),
        mapping("Due_Date", "execution_time", {"period": "days", "unit": str(spec.get("due_in_days", 0)),
                                               "trigger_field": "${CURRENTTIME}", "sign": "plus"}),
        mapping("Status", "static", "Not Started"),
        mapping("Priority", "static", spec.get("priority", "Normal")),
    ]
    if spec.get("description"):
        maps.append(mapping("Description", "merge_field" if "${" in spec["description"] else "static",
                            spec["description"]))
    return {"tasks": [{"name": spec["subject"], "module": _ref(module_ids, spec["module"]),
                       "feature_type": "workflow", "notify": True, "field_mappings": maps}]}


def _criterion(node, ids):
    if "group" in node:
        return {"group_operator": node["group_operator"].upper(),
                "group": [_criterion(n, ids) for n in node["group"]]}
    return {"field": _ref(ids, node["field"]), "comparator": node["comparator"], "value": node["value"]}


def rule_payload(spec, module_ids, fields, task_ids):
    module = _ref(module_ids, spec["module"])
    trig = spec["trigger"]
    if trig["type"] == "date":
        execute_when = {"type": "date_or_datetime", "details": {
            "trigger_module": module, "field": _ref(fields, trig["field"]),
            "period": "days", "unit": trig["days"], "recur_cycle": "once"}}
    elif trig["type"] == "field_update":
        execute_when = {"type": "field_update", "details": {
            "trigger_module": module, "repeat": True,
            "criteria": {"field": _ref(fields, trig["field"]), "comparator": "equal", "value": trig["value"]}}}
    else:
        raise ValueError(f"unknown trigger type {trig['type']!r} in rule {spec['name']!r}")

    actions = [{"type": "tasks", "id": task_ids[key]} for key in spec["tasks"]]
    condition = {"sequence_number": 1}
    if spec.get("criteria"):
        condition["criteria_details"] = {"criteria": _criterion(spec["criteria"], fields)}
    if spec.get("after_days"):
        condition["scheduled_actions"] = [{"execute_after": {"period": "days", "unit": spec["after_days"]},
                                           "actions": actions}]
    else:
        condition["instant_actions"] = {"actions": actions}
    return {"workflow_rules": [{"name": spec["name"], "description": spec.get("description"),
                                "module": module, "execute_when": execute_when, "conditions": [condition]}]}


def used_fields(spec):
    names = [spec["trigger"]["field"]]
    stack = [spec.get("criteria") or {}]
    while stack:
        node = stack.pop()
        stack += node.get("group", [])
        if "field" in node:
            names.append(node["field"])
    return names


def _created_id(resp, key):
    result = (resp.get(key) or [{}])[0]
    if str(result.get("status", "")).lower() == "success":
        return (result.get("details") or {}).get("id"), None
    return None, result.get("message") or str(resp)[:200]


def sync(client, config, report):
    tasks = {t["key"]: t for t in config.get("tasks", [])}
    module_ids = _module_ids(client)
    task_fields = _field_ids(client, "Tasks")
    fields, rules_done, tasks_done = {}, {}, {}

    for spec in config.get("rules", []):
        module, name = spec["module"], f"{spec['module']}: {spec['name']}"
        if module not in module_ids:
            report.add(SECTION, name, "blocked", "module not found")
            continue
        if module not in fields:
            fields[module] = _field_ids(client, module)
            rules_done[module] = _existing(client, "/settings/automation/workflow_rules", "workflow_rules", module)
            tasks_done[module] = _existing(client, "/settings/automation/tasks", "tasks", module)
        if spec["name"] in rules_done[module]:
            report.add(SECTION, name, "exists")
            continue
        missing = sorted({f for f in used_fields(spec) if f not in fields[module]})
        if missing:
            report.add(SECTION, name, "blocked", "fields not in CRM: " + ", ".join(missing))
            continue

        task_ids, failed = {}, None
        for key in spec["tasks"]:
            task = tasks[key]
            if task["subject"] in tasks_done[module]:
                task_ids[key] = tasks_done[module][task["subject"]]
                continue
            resp = client.post(f"{CRM}/settings/automation/tasks", json=task_payload(task, module_ids, task_fields))
            if resp is None:
                report.add(SECTION, f"{module}: task {task['subject']}", "would create")
                task_ids[key] = f"<new {key}>"
                continue
            task_id, error = _created_id(resp, "tasks")
            if error:
                failed = f"task {task['subject']}: {error}"
                break
            tasks_done[module][task["subject"]] = task_ids[key] = task_id
            report.add(SECTION, f"{module}: task {task['subject']}", "created")
        if failed:
            report.add(SECTION, name, "failed", failed)
            continue

        resp = client.post(f"{CRM}/settings/automation/workflow_rules",
                           json=rule_payload(spec, module_ids, fields[module], task_ids))
        if resp is None:
            report.add(SECTION, name, "would create")
            continue
        _, error = _created_id(resp, "workflow_rules")
        report.add(SECTION, name, "failed" if error else "created", error or "")
