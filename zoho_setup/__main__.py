"""Command line: python -m zoho_setup <command> [--apply]

  validate      offline checks of config, templates and Deluge scripts (no credentials needed)
  crm-schema    create CRM custom fields from config/crm_schema.yaml
  books-config  create Books VAT rates, items and suppliers from config/books.yaml
  all           crm-schema + books-config
  import-data   import customers/vehicles/job history from --data-dir (run locally, not in CI)

Without --apply every command is a dry run: it reads from Zoho and prints what it would change.
"""
import argparse
import logging
import os
import sys

import yaml

from . import books_config, crm_schema, importer, validate
from .client import ZohoClient, ZohoError
from .report import Report

EU_API = "https://www.zohoapis.eu"


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="zoho_setup", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["validate", "crm-schema", "books-config", "all", "import-data"])
    parser.add_argument("--apply", action="store_true", help="make changes (default is a dry run)")
    parser.add_argument("--data-dir", help="folder with customers.csv, vehicles.csv, job_history.csv")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    schema = load_yaml("config/crm_schema.yaml")
    books = load_yaml("config/books.yaml")

    errors = validate.run(schema, books, args.data_dir)
    if errors:
        print("Validation failed:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("Validation passed.")
    if args.command == "validate":
        return 0

    if args.command == "import-data" and not args.data_dir:
        parser.error("import-data needs --data-dir")
    if args.command == "import-data" and os.environ.get("CI"):
        print("Refusing to import customer data from CI. Run import-data on your own computer.")
        return 1

    report = Report(dry_run=not args.apply)
    print(f"\nMode: {'APPLY' if args.apply else 'DRY RUN (no changes)'}\n")
    try:
        if args.command in ("crm-schema", "all"):
            crm = ZohoClient.from_env("ZOHO_CRM_API_DOMAIN", EU_API, dry_run=not args.apply)
            crm_schema.sync(crm, schema, report)
        if args.command in ("books-config", "all"):
            org_id = os.environ.get("ZOHO_BOOKS_ORG_ID")
            if not org_id:
                raise ZohoError("Missing environment variable: ZOHO_BOOKS_ORG_ID")
            bk = ZohoClient.from_env("ZOHO_BOOKS_API_DOMAIN", EU_API, dry_run=not args.apply)
            books_config.sync(bk, org_id, books, report)
        if args.command == "import-data":
            crm = ZohoClient.from_env("ZOHO_CRM_API_DOMAIN", EU_API, dry_run=not args.apply)
            importer.run(crm, args.data_dir, report)
    except ZohoError as e:
        print(f"\nZoho error: {e}")
        report.finish()
        return 2
    return report.finish()


if __name__ == "__main__":
    sys.exit(main())
