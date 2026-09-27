"""Imports customers, vehicles and job history into CRM. Run locally: customer data is never committed.

Re-running is safe: customers match on Mobile, vehicles on Registration, jobs on Import_Key.
Blank cells never overwrite existing CRM values.
"""
import csv
import os
import re

from . import normalize

CRM = "/crm/v6"

CUSTOMER_HEADERS = ["First Name", "Last Name", "Mobile", "Email", "Mailing Street", "Mailing City",
                    "Eircode", "Customer Type", "Preferred Contact", "WhatsApp Consent",
                    "Marketing Consent", "Consent Date", "Description"]
VEHICLE_HEADERS = ["Registration", "Customer Mobile", "Make", "Model", "Year", "Fuel Type",
                   "Engine Size", "Colour", "VIN", "Current Mileage (km)", "Last Service Date",
                   "Next Service Due", "NCT Due", "Vehicle Status", "Notes"]
JOB_HEADERS = ["Registration", "Booked For", "Job Type", "Stage", "Mileage In (km)",
               "Customer Complaint", "Work Done", "Advisories", "Payment Status", "Books Invoice No."]

FILES = {
    "customers.csv": CUSTOMER_HEADERS,
    "vehicles.csv": VEHICLE_HEADERS,
    "job_history.csv": JOB_HEADERS,
}


def read_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return [r for r in csv.DictReader(f) if not normalize.is_example(r)]


def _int(value):
    value = re.sub(r"[^0-9]", "", value or "")
    return int(value) if value else None


def _clean(record):
    return {k: v for k, v in record.items() if v is not None and v != ""}


def _is_real(record_id):
    return bool(record_id) and not str(record_id).startswith("<")


def _escape(value):
    return re.sub(r"([(),\\])", r"\\\1", value)


def find(client, module, field, value):
    body = client.get(f"{CRM}/{module}/search",
                      params={"criteria": f"({field}:equals:{_escape(value)})"}) or {}
    data = body.get("data") or []
    return data[0]["id"] if data else None


def upsert(client, module, record_id, record, report, label):
    if _is_real(record_id):
        resp = client.put(f"{CRM}/{module}", json={"data": [{**record, "id": record_id}]})
        verb = "update"
    else:
        resp = client.post(f"{CRM}/{module}", json={"data": [record]})
        verb = "create"
    if resp is None:
        report.add("Import", label, f"would {verb}")
        return record_id or f"<new {label}>"
    result = (resp.get("data") or [{}])[0]
    if str(result.get("status", "")).lower() == "success":
        report.add("Import", label, f"{verb}d")
        return result.get("details", {}).get("id", record_id)
    report.add("Import", label, "failed", result.get("message") or str(resp)[:200])
    return None


def import_customers(client, rows, report):
    ids = {}
    for row in rows:
        mob = normalize.mobile(row["Mobile"])
        label = f"customer {row['First Name']} {row['Last Name']}".strip()
        if not mob:
            report.add("Import", label, "failed", f"bad mobile {row['Mobile']!r}")
            continue
        record = _clean({
            "First_Name": row["First Name"].strip(),
            "Last_Name": row["Last Name"].strip() or "(unknown)",
            "Mobile": mob,
            "Email": row["Email"].strip(),
            "Mailing_Street": row["Mailing Street"].strip(),
            "Mailing_City": row["Mailing City"].strip(),
            "Eircode": row["Eircode"].strip().upper(),
            "Customer_Type": row["Customer Type"].strip(),
            "Preferred_Contact": row["Preferred Contact"].strip(),
            "WhatsApp_Consent": normalize.boolean(row["WhatsApp Consent"]),
            "Marketing_Consent": normalize.boolean(row["Marketing Consent"]),
            "Consent_Date": normalize.date(row["Consent Date"]),
            "Description": row["Description"].strip(),
        })
        ids[mob] = upsert(client, "Contacts", find(client, "Contacts", "Mobile", mob),
                          record, report, label)
    return ids


def import_vehicles(client, rows, customer_ids, report):
    ids, owners = {}, {}
    for row in rows:
        reg = normalize.registration(row["Registration"])
        if not reg:
            report.add("Import", f"vehicle {row['Registration']}", "failed", "bad registration")
            continue
        mob = normalize.mobile(row["Customer Mobile"])
        customer_id = customer_ids.get(mob) if mob else None
        if mob and not customer_id:
            customer_id = find(client, "Contacts", "Mobile", mob)
        record = _clean({
            "Name": reg,
            "Customer": customer_id if _is_real(customer_id) else None,
            "Make": row["Make"].strip(),
            "Model": row["Model"].strip(),
            "Year": _int(row["Year"]),
            "Fuel_Type": row["Fuel Type"].strip(),
            "Engine_Size": row["Engine Size"].strip(),
            "Colour": row["Colour"].strip(),
            "VIN": row["VIN"].strip().upper(),
            "Current_Mileage": _int(row["Current Mileage (km)"]),
            "Last_Service_Date": normalize.date(row["Last Service Date"]),
            "Next_Service_Due": normalize.date(row["Next Service Due"]),
            "NCT_Due": normalize.date(row["NCT Due"]),
            "Vehicle_Status": row["Vehicle Status"].strip() or "Active",
            "Vehicle_Notes": row["Notes"].strip(),
            "Reg_Check": "OK",
        })
        ids[reg] = upsert(client, "Vehicles", find(client, "Vehicles", "Name", reg),
                          record, report, f"vehicle {reg}")
        owners[reg] = customer_id
    return ids, owners


def import_jobs(client, rows, vehicle_ids, owners, report):
    for row in rows:
        reg = normalize.registration(row["Registration"])
        if not reg:
            report.add("Import", f"job {row['Registration']}", "failed", "bad registration")
            continue
        vehicle_id = vehicle_ids.get(reg) or find(client, "Vehicles", "Name", reg)
        if not vehicle_id:
            report.add("Import", f"job {reg}", "failed", "vehicle not found; import vehicles first")
            continue
        customer_id = owners.get(reg)
        if customer_id is None and _is_real(vehicle_id):
            data = ((client.get(f"{CRM}/Vehicles/{vehicle_id}") or {}).get("data") or [{}])[0]
            customer_id = (data.get("Customer") or {}).get("id")
        booked = normalize.local_datetime(row["Booked For"])
        key = f"{reg}|{row['Booked For'].strip()}"
        record = _clean({
            "Vehicle": vehicle_id if _is_real(vehicle_id) else None,
            "Customer": customer_id if _is_real(customer_id) else None,
            "Booked_For": booked,
            "Job_Type": row["Job Type"].strip(),
            "Stage": row["Stage"].strip() or "Collected",
            "Mileage_In": _int(row["Mileage In (km)"]),
            "Customer_Complaint": row["Customer Complaint"].strip(),
            "Work_Done": row["Work Done"].strip(),
            "Advisories": row["Advisories"].strip(),
            "Payment_Status": row["Payment Status"].strip(),
            "Books_Invoice_No": row["Books Invoice No."].strip(),
            "Import_Key": key,
        })
        upsert(client, "Job_Cards", find(client, "Job_Cards", "Import_Key", key),
               record, report, f"job {key}")


def run(client, data_dir, report):
    customers = read_rows(os.path.join(data_dir, "customers.csv"))
    vehicles = read_rows(os.path.join(data_dir, "vehicles.csv"))
    jobs = read_rows(os.path.join(data_dir, "job_history.csv"))
    customer_ids = import_customers(client, customers, report)
    vehicle_ids, owners = import_vehicles(client, vehicles, customer_ids, report)
    import_jobs(client, jobs, vehicle_ids, owners, report)
