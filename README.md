# SuperGear Motors Ltd. — Zoho CRM + Books setup kit

A build kit to move SuperGear Motors Ltd. (Maynooth, Co. Kildare) off notebooks and Excel and onto Zoho, covering three things:

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
7. **[Automated setup with GitHub Actions](docs/07-github-actions.md)**: creates the CRM fields, list views, reminder rules, Books VAT rates, price list and suppliers for you.
8. **[What Zoho's API can automate](docs/08-zoho-api-integrations.md)**: research from github.com/zoho/crm-oas, reminder workflows, email templates to paste.

**➡ Master plan: [ROADMAP](docs/ROADMAP.md)** (mirrored as numbered Tasks P1.0–P5.1 in Zoho CRM → Tasks)
**➡ What's live right now: [BUILD_LOG](docs/BUILD_LOG.md)** (start at "RESUME HERE")

## Build with Claude + Zoho MCP

The Zoho CRM and Zoho Books connectors let Claude do the setup and data entry directly.
[`claude-project/project-instructions.md`](claude-project/project-instructions.md) sets up a Claude.ai Project for
this, and [`docs/BUILD_LOG.md`](docs/BUILD_LOG.md) tracks what's been built and what's next.

## Automation at a glance

- **Validate** workflow: runs on every push and pull request and checks the config, templates and Deluge scripts. No credentials needed.
- **SuperGear Motors Ltd** workflow (job `deployment`): keeps live Zoho in line with `config/`.
  - **Pull request** that touches `config/`, `zoho_setup/` or the workflow → **dry run** against the live org; the run summary lists what would change.
  - **Merge** into the default branch → **apply**. Anything that already exists is reported as `exists` and left alone.
  - Every run waits for approval on the `production` environment (Actions → the run → Review deployments → Approve).
  - Can also be run by hand from the Actions tab (pick target, step and *apply*).
- Credentials live only in the `production` environment's secrets (`ZOHO_CLIENT_ID`, `ZOHO_CLIENT_SECRET`, `ZOHO_REFRESH_TOKEN`). The refresh token needs the full scope list in [doc 07](docs/07-github-actions.md). Customer data never goes in this repo.
- Zoho allows only about 10 token refreshes per 10 minutes. If a run fails with `Access Denied` at login, wait 10 minutes and use *Re-run failed jobs*.

| Step (`python -m zoho_setup <step>`) | Creates | Config |
|---|---|---|
| `crm-schema` | CRM custom fields (Customers, Vehicles, Job Cards, Services) | `config/crm_schema.yaml` |
| `crm-views` | CRM list views: Today in the workshop, Waiting parts, Not paid, Service/NCT due… | `config/crm_views.yaml` |
| `crm-workflows` | CRM reminder rules + task templates (service/NCT due, not collected, chase payment) | `config/crm_workflows.yaml` |
| `books-config` | Books VAT rates, items (price list), suppliers | `config/books.yaml`, `items.csv`, `suppliers.csv` |
| `all` | all of the above, in that order | |

Still manual (Zoho has no API): Blueprint, pasting Deluge functions, the Create Quote button, the Books ↔ CRM sync settings, hiding modules. Each run prints these as a checklist.

## What's in the repo

```
docs/               step-by-step setup guides
config/             what the automation creates: CRM fields, list views, reminder rules, VAT rates,
                    price list (items.csv), CRM services (services.csv), suppliers
templates/          CSV templates for typing up paper records (customers, vehicles, job history)
deluge/             Deluge scripts to paste into CRM (Setup → Developer Hub → Functions)
zoho_setup/         the Python tool behind the workflows (python -m zoho_setup --help)
tests/              tests for the tool
.github/workflows/  Validate (every push/PR) and SuperGear Motors Ltd (PR dry run, deploy on merge)
claude-project/     instructions for a Claude.ai Project that builds through the Zoho connectors
```

## How the pieces fit

```
Customer (Contact) ──< Vehicle ──< Job Card ──► Books Estimate ──► Books Invoice ──► Stripe payment
                                     │                                   │
                                     └── Blueprint stages                └── synced back to CRM (Zoho Finance tab)

Supplier email ──► Books document inbox ──► Autoscan ──► Bill ──► paid / reconciled
```

- A **Contact** is the customer (module relabelled **Customers**; business customers go under **Fleet Accounts**). One customer can own many vehicles. CRM Contacts sync to Books Customers.
- A **Vehicle** is keyed on its Irish registration (e.g. `191-D-12345`). Its **Job Cards** related list *is* the service history.
- A **Job Card** is one visit to the workshop. It holds labour and parts lines, mileage in, the work done, and a link to the Books quote/invoice.

## Assumptions to confirm

- CRM edition is **Professional** or higher (Blueprint, custom functions and more custom modules). The org is on an Enterprise **trial that ends 12 Oct 2026**; buy a plan before then (roadmap P1.9). If you are on Standard, see the notes in `docs/02-job-blueprint.md`.
- Both apps are in Zoho's **EU** data centre (`zohoapis.eu`, `accounts.zoho.eu`). Email is Zoho Mail on `info@supergearmotors.ie`.
- The Books organisation is created with **Ireland** as the country. Confirm VAT rates with your accountant before going live (see `docs/03-books-integration.md`).
- Deluge scripts are written against the CRM v2+ and Books v3 APIs. **Test them in the CRM Sandbox first.**
