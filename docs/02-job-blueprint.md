# 2. Job workflow (Blueprint)

Setup → Process Management → **Blueprint** → New Blueprint

- Module: **Job Cards**
- Layout: Standard
- Field: **Stage**
- Criteria: none (all job cards)

## 2.1 States and transitions

```
            ┌──────────────► Cancelled ◄──────────────┐
            │                                         │
Booked ──► In Workshop ──► Ready ──► Collected        │
                │   ▲                                 │
                ▼   │                                 │
           Waiting Parts ─────────────────────────────┘
```

| Transition | From → To | Who | Required during transition | After-transition action |
|---|---|---|---|---|
| **Check In** | Booked → In Workshop | Advisor | Mileage In, Mechanic | Update vehicle mileage (`deluge/job_card_check_in.dg`) |
| **Parts Needed** | In Workshop → Waiting Parts | Advisor | Parts Awaited | none |
| **Parts Arrived** | Waiting Parts → In Workshop | Advisor | none | none |
| **Work Complete** | In Workshop → Ready | Advisor | Work Done, at least one Job Line, Advisories (can be "None") | Optional: email/SMS "your car is ready" |
| **Collected** | Ready → Collected | Advisor | Payment Status, Books Invoice No. (unless Account Customer) | `deluge/job_card_on_collected.dg`: sets Last Service Date, Next Service Due, Current Mileage on the Vehicle |
| **Cancel** | Booked / Waiting Parts → Cancelled | Advisor | Cancel Reason | none |

Tips:
- Add a **checklist** to *Work Complete*: road-tested, service light reset, stamped service book, wheel nuts torqued.
- Set an **SLA** on *Ready*: if still Ready after 2 days, alert the owner ("car waiting for collection").
- Tick **"Allow the record owner to edit Stage outside Blueprint"** = off, so stages can't be skipped.

## 2.2 Workflow rules (Setup → Automation → Workflow Rules)

| Rule | Module | When | Action |
|---|---|---|---|
| Fill customer from vehicle | Job Cards | On create | Function `job_card_on_create` |
| Normalize registration | Vehicles | On create or edit (Registration modified) | Function `normalize_registration` |
| Overdue payment alert | Job Cards | Date-based: 7 days after Stage = Collected, if Payment Status != Paid | Email the owner |

## 2.3 If you are on CRM Standard

Blueprint needs Professional. On Standard, keep **Stage** as a plain picklist, use the
custom views in doc 01 as your workshop board (Kanban view grouped by Stage works well), and
use workflow rules with field-update criteria to run the same functions.
