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
5. **[Data migration](docs/05-data-migration.md)**: import customers, vehicles and past jobs from Excel using the CSV templates in `templates/`.
6. **[Go-live checklist](docs/06-go-live-checklist.md)**.

## What's in the repo

```
docs/        step-by-step setup guides
templates/   CSV import templates (customers, vehicles, job history, suppliers)
deluge/      Deluge scripts to paste into CRM (Setup → Developer Hub → Functions)
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
