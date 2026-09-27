# Super Gears Motors — Zoho setup kit (Phase 1)

A build kit to move Super Gears Motors off notebooks and Excel and onto Zoho, covering three things:

| # | Capability | Zoho app | Extra licence cost |
|---|---|---|---|
| 1 | Customers, vehicles, job cards, service history | Zoho CRM (Professional) — custom modules **Vehicles** and **Job Cards** | none (uses your CRM) |
| 2 | Quote → invoice → payment | Zoho Books + native CRM ↔ Books sync + Stripe | Books plan only |
| 3 | Supplier invoices | Zoho Books document inbox + Autoscan → Bills | none |

No Zoho FSM, Flow or Inventory is needed at this stage.

## Build order

Follow these in order. Each step depends on the one before it.

1. **[CRM data model](docs/01-crm-setup.md)**: create the Vehicles and Job Cards modules, fields, layouts and related lists.
2. **[Job workflow (Blueprint)](docs/02-job-blueprint.md)**: Booked → In Workshop → Waiting Parts → Ready → Collected.
3. **[Zoho Books + CRM sync](docs/03-books-integration.md)**: Irish VAT, items, sync, the "Create Quote" button and payments.
4. **[Supplier bill capture](docs/04-supplier-bills.md)**: forward supplier emails to Books and let Autoscan turn them into bills.
5. **[Paper records → Zoho](docs/05-data-migration.md)**: capture on next visit, enter regulars first, keep the notebooks as the archive.
6. **[Go-live checklist](docs/06-go-live-checklist.md)**.
7. **[Automated setup with GitHub Actions](docs/07-github-actions.md)**: creates the CRM fields, Books VAT rates, price list and suppliers for you.

## Build with Claude + Zoho MCP

The Zoho CRM and Zoho Books connectors let Claude do the setup and data entry directly.
[`claude-project/project-instructions.md`](claude-project/project-instructions.md) sets up a Claude.ai Project for
this, and [`docs/BUILD_LOG.md`](docs/BUILD_LOG.md) tracks what's been built and what's next.

## Automation at a glance

- **Validate** workflow: runs on every push and checks the config, templates and Deluge scripts. No credentials needed.
- **Zoho setup** workflow: run it from the Actions tab. It's a dry run unless you tick *apply*, and it targets the CRM Sandbox unless you pick production.
- Credentials live only in GitHub environment secrets. Customer data never goes in this repo.

## What's in the repo

```
docs/               step-by-step setup guides
config/             what the automation creates: CRM fields, VAT rates, price list, suppliers
templates/          CSV templates for typing up paper records (customers, vehicles, job history)
deluge/             Deluge scripts to paste into CRM (Setup → Developer Hub → Functions)
zoho_setup/         the Python tool behind the workflows (python -m zoho_setup --help)
tests/              tests for the tool
.github/workflows/  Validate (every push) and Zoho setup (manual)
```

## How the pieces fit

```
Customer (Contact) ──< Vehicle ──< Job Card ──► Books Estimate ──► Books Invoice ──► Stripe payment
                                     │                                   │
                                     └── Blueprint stages                └── synced back to CRM (Zoho Finance tab)

Supplier email ──► Books document inbox ──► Autoscan ──► Bill ──► paid / reconciled
```

- A **Contact** is the customer. One customer can own many vehicles.
- A **Vehicle** is keyed on its Irish registration (e.g. `191-D-12345`). Its **Job Cards** related list *is* the service history.
- A **Job Card** is one visit to the workshop. It holds labour and parts lines, mileage in, the work done, and a link to the Books quote/invoice.

## Assumptions to confirm

- CRM edition is **Professional** or higher (Blueprint, custom functions and more custom modules). If you are on Standard, see the notes in `docs/02-job-blueprint.md`.
- The Books organisation is created with **Ireland** as the country. Confirm VAT rates with your accountant before going live (see `docs/03-books-integration.md`).
- Deluge scripts are written against the CRM v2+ and Books v3 APIs. **Test them in the CRM Sandbox first.**
