"""Offline checks: config files, CSV templates/data and Deluge field names. No Zoho access needed."""
import csv
import glob
import os
import re

from . import books_config, crm_schema, importer, normalize

# Fields the Deluge scripts use that are system fields or set up by hand (subform).
DELUGE_KNOWN_FIELDS = {
    "Name", "First_Name", "Last_Name", "Email", "Mobile",
    "Job_Lines", "Line_Type", "Description", "Part_No", "Qty", "Unit_Price",
}


def check_schema(schema):
    errors = []
    for module, mspec in schema["modules"].items():
        for spec in mspec["fields"]:
            where = f"crm_schema.yaml {module}.{spec.get('api_name')}"
            if normalize.api_name_from_label(spec["label"]) != spec["api_name"]:
                errors.append(f"{where}: label {spec['label']!r} would produce API name "
                              f"{normalize.api_name_from_label(spec['label'])!r}")
            if spec["type"] not in crm_schema.TYPE_MAP:
                errors.append(f"{where}: unknown type {spec['type']!r}")
            if spec["type"] == "picklist" and not spec.get("values"):
                errors.append(f"{where}: picklist needs values")
            if spec["type"] == "lookup" and not spec.get("module"):
                errors.append(f"{where}: lookup needs module")
    return errors


def check_deluge(schema, deluge_dir="deluge"):
    known = set(DELUGE_KNOWN_FIELDS)
    for mspec in schema["modules"].values():
        known |= {f["api_name"] for f in mspec["fields"]}
    errors = []
    for path in sorted(glob.glob(os.path.join(deluge_dir, "*.dg"))):
        text = open(path, encoding="utf-8").read()
        for field in sorted(set(re.findall(r'\.(?:get|put)\("([A-Z][A-Za-z_]*)"', text))):
            if field not in known:
                errors.append(f"{path}: uses field {field!r}, which is not in crm_schema.yaml")
    return errors


def check_books(config):
    errors = []
    tax_names = {t["tax_name"] for t in config["taxes"]}
    for i, row in enumerate(books_config.read_csv(config["items_file"]), start=2):
        where = f"{config['items_file']} line {i}"
        if not row.get("Name", "").strip():
            errors.append(f"{where}: Name is blank")
        if row.get("Type", "").strip() not in ("service", "goods"):
            errors.append(f"{where}: Type must be service or goods")
        try:
            if float(row.get("Rate", "")) <= 0:
                errors.append(f"{where}: Rate must be above 0")
        except ValueError:
            errors.append(f"{where}: Rate {row.get('Rate')!r} is not a number")
        if row.get("Tax", "").strip() not in tax_names:
            errors.append(f"{where}: Tax {row.get('Tax')!r} is not in books.yaml")
    for i, row in enumerate(books_config.read_csv(config["suppliers_file"]), start=2):
        where = f"{config['suppliers_file']} line {i}"
        if not row.get("Company Name", "").strip():
            errors.append(f"{where}: Company Name is blank")
        terms = row.get("Payment Terms", "").strip()
        if terms and not terms.isdigit():
            errors.append(f"{where}: Payment Terms must be a number of days")
    return errors


def check_data_dir(data_dir):
    """Headers always; row contents too (example rows are checked so the templates stay valid)."""
    errors = []
    for name, headers in importer.FILES.items():
        path = os.path.join(data_dir, name)
        if not os.path.exists(path):
            errors.append(f"{path}: missing")
            continue
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            missing = [h for h in headers if h not in (reader.fieldnames or [])]
            if missing:
                errors.append(f"{path}: missing columns {missing}")
                continue
            for i, row in enumerate(reader, start=2):
                errors += [f"{path} line {i}: {e}" for e in _row_errors(name, row)]
    return errors


def _row_errors(name, row):
    errors = []
    if "Registration" in row and not normalize.registration(row["Registration"]):
        errors.append(f"registration {row['Registration']!r} not recognised")
    for col in ("Mobile", "Customer Mobile"):
        if row.get(col, "").strip() and not normalize.mobile(row[col]):
            errors.append(f"{col} {row[col]!r} not recognised")
    for col in ("Consent Date", "Last Service Date", "Next Service Due", "NCT Due"):
        try:
            normalize.date(row.get(col))
        except ValueError as e:
            errors.append(f"{col}: {e}")
    try:
        normalize.local_datetime(row.get("Booked For"))
    except ValueError as e:
        errors.append(f"Booked For: {e}")
    return errors


def run(schema, books, data_dir=None):
    errors = check_schema(schema) + check_deluge(schema) + check_books(books)
    errors += check_data_dir("templates")
    if data_dir:
        errors += check_data_dir(data_dir)
    return errors
