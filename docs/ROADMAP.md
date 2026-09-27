# Super Gears Motors — CRM roadmap

The same roadmap lives in **Zoho CRM → Tasks**. Every task is numbered `P<phase>.<step>`, so sorting by
subject gives the right order, and each task's description has step-by-step instructions.
Tick a task **Completed** in CRM when it's done, then ask Claude to check it.

Legend: ✅ done · 👤 owner clicks in Zoho · 🤖 Claude does it through the Zoho connector · 🤝 owner clicks, Claude guides and checks

## Phase 0 — Foundation (done 27 Sep 2026)
| # | Step | Who | Status |
|---|---|---|---|
| 0.1 | CRM org + Books org (Ireland, EUR) | 👤 | ✅ |
| 0.2 | Vehicles + Job Cards modules | 👤 | ✅ |
| 0.3 | 6 Customer fields, 17 Vehicle fields, 19 Job Card fields (incl. auto Job Number JC-…) | 🤖 | ✅ |
| 0.4 | Job Lines table (Labour / Part / Sundry, QTY, Unit Price, Line Total) + Job Total | 🤝 | ✅ |
| 0.5 | Zoho sample data removed (63 records) | 🤖 | ✅ |
| 0.6 | Staff (Standard profile) can see Vehicles + Job Cards | 🤝 | ✅ |
| 0.7 | Contacts → **Customers**, Accounts → **Fleet Accounts** | 🤝 | ✅ |
| 0.8 | Books VAT rates 13.5% / 23% / 0%; IDs wired into the Create Quote script | 🤖 | ✅ |
| 0.9 | Owner roadmap created as CRM Tasks | 🤖 | ✅ |

## Phase 1 — CRM ready for daily use (target: 9 Oct)
| # | Step | Who | Due |
|---|---|---|---|
| P1.0 | "Operations" menu group | 🤝 | ✅ |
| P1.1 | Hide unused modules (Leads, Deals, Inventory group, etc.) | 👤 | 29 Sep |
| P1.2 | Connect info@supergearmotors.ie (Zoho Mail) to CRM | 👤 | 30 Sep |
| P1.2c | Finish the domain switch to Hosting Ireland (email + website) | 👤 | 1 Oct |
| P1.2b | Rename "Vehicle/Job Card Owner" → "Handled By"; remove Email fields from Vehicles/Job Cards | 🤝 | 30 Sep |
| P1.3 | Job workflow (Blueprint): Booked → In Workshop → Waiting Parts → Ready → Collected | 🤝 | 2 Oct |
| P1.4 | Block duplicate registrations and mobiles | 👤 | 2 Oct |
| P1.5 | Paste the 4 automation scripts | 🤝 | 5 Oct |
| P1.6 | Saved lists: Today's workshop, Waiting parts, Ready, Not paid, Service/NCT due | 🤝 | 6 Oct |
| P1.7 | Workshop board (Kanban by Stage) | 👤 | 6 Oct |
| P1.8 | Phone app + front-desk user | 👤 | 8 Oct |
| **P1.9** | **Buy the paid CRM plan (Professional) — trial ends 12 Oct** | 👤 | **9 Oct** |

## Phase 2 — Money: quotes, invoices, payments (target: 10 Oct)
| # | Step | Who | Due |
|---|---|---|---|
| P2.1 | Send labour rate, prices, suppliers → Claude loads them into Books | 👤 → 🤖 | 1 Oct |
| P2.1c | Service catalog in CRM (16 services, SKU-matched to Books) | 🤖 | ✅ |
| P2.2 | Accountant confirms VAT rates | 👤 | 3 Oct |
| P2.3 | Books: VAT registration on (VAT number) | 👤 | 3 Oct |
| P2.4 | Link Books ↔ CRM | 🤝 | 6 Oct |
| P2.5 | "Create Quote in Books" button on Job Cards | 🤝 | 8 Oct |
| P2.6 | Stripe card payments | 👤 | 10 Oct |
| P2.7 | Supplier invoices: auto-scan + email forwarding | 👤 | 10 Oct |
| P2.8 | Logo, bank details, T&Cs on quotes/invoices | 👤 | 10 Oct |
| P2.9 | Books sends quotes/invoices from info@supergearmotors.ie | 👤 | 3 Oct |

## Phase 3 — Go live (target: 20 Oct)
| # | Step | Who | Due |
|---|---|---|---|
| P3.1 | Test run: one pretend job end to end, Claude checks each step and cleans up | 🤝 | 12 Oct |
| P3.2 | Front-desk daily routine (printed at the desk) | 👤 | 13 Oct |
| P3.3 | 3 real jobs in CRM alongside paper | 👤 | 15 Oct |
| P3.4 | Enter regulars / fleet / anyone due soon from notebooks (photos → Claude) | 👤 + 🤖 | 17 Oct |
| P3.5 | Paper stops; notebooks become the archive | 👤 | 20 Oct |
| P3.6 | GDPR consent collected at each visit | 👤 | ongoing |

## Phase 4 — Grow: automation and customers (Nov–Dec)
| # | Step | Who | Due |
|---|---|---|---|
| P4.1 | WhatsApp: "your car is ready" | 🤝 | 6 Nov |
| P4.2 | Automatic service + NCT reminders | 🤝 | 13 Nov |
| P4.3 | Google review request after collection | 🤝 | 20 Nov |
| P4.4 | Online booking (web form or Zoho Bookings) | 🤝 | 27 Nov |
| P4.5 | Owner dashboard | 🤝 | 4 Dec |

## Phase 5 — AI reception (2027)
| # | Step | Who | Due |
|---|---|---|---|
| P5.1 | AI phone receptionist that books jobs into CRM | 🤝 | Jan 2027 |

## Known limits of the Zoho connector
Claude **can**: create and verify fields, records, tasks, Books taxes, items, suppliers, estimates and invoices; clean data; read everything.
Claude **cannot**: create modules, layouts, Blueprint, workflow rules, functions, buttons, custom views, menu groups, or change settings. Those are 🤝 steps.
