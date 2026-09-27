# 1. CRM data model

> **Shortcut:** create the two modules by hand, then let the *Zoho setup* GitHub workflow create every field in the tables below (doc 07). Field labels must match exactly, because Zoho builds the API name from the label.

Setup → Customization → Modules and Fields.

## 1.1 Contacts (existing module, used for customers)

Rename the module label to **Customers** if you like; the API name stays `Contacts`.

Add these fields:

| Field label | Type | API name (suggested) | Notes |
|---|---|---|---|
| Mobile | Phone (existing) | `Mobile` | Primary field for WhatsApp later. Store in `+353…` format. |
| Eircode | Single line | `Eircode` | |
| Customer Type | Picklist | `Customer_Type` | Private, Business, Fleet, Trade |
| Preferred Contact | Picklist | `Preferred_Contact` | WhatsApp, SMS, Call, Email |
| WhatsApp Consent | Checkbox | `WhatsApp_Consent` | GDPR: tick only with explicit consent |
| Marketing Consent | Checkbox | `Marketing_Consent` | GDPR |
| Consent Date | Date | `Consent_Date` | |

Business and fleet customers: use **Accounts** for the company and Contacts for the people, as normal.

## 1.2 Vehicles (new custom module)

Setup → Modules and Fields → **+ New Module** → name `Vehicles` (API name `Vehicles`).

| Field label | Type | API name | Notes |
|---|---|---|---|
| Registration | Single line (**record name**, unique) | `Name` | Rename the default "Vehicle Name" field. Mark it **Do not allow duplicate values**. Format `191-D-12345`. |
| Customer | Lookup → Contacts | `Customer` | Creates a "Vehicles" related list on the customer |
| Company | Lookup → Accounts | `Company` | Optional, for fleet vehicles |
| Make | Picklist | `Make` | Toyota, Volkswagen, Ford, Hyundai, Skoda, Nissan, Kia, BMW, Audi, Renault, Peugeot, Opel, Mercedes-Benz, Other |
| Model | Single line | `Model` | |
| Year | Number | `Year` | |
| Fuel Type | Picklist | `Fuel_Type` | Petrol, Diesel, Hybrid, Plug-in Hybrid, Electric |
| Engine Size | Single line | `Engine_Size` | e.g. 1.6 |
| Colour | Single line | `Colour` | |
| VIN | Single line | `VIN` | 17 characters |
| Current Mileage | Number | `Current_Mileage` | Updated automatically when a job is collected |
| Last Service Date | Date | `Last_Service_Date` | Automatic |
| Next Service Due | Date | `Next_Service_Due` | Automatic: last service + 12 months (editable) |
| NCT Due | Date | `NCT_Due` | Entered from the NCT cert/disc. Used for reminders later. |
| Tax Due | Date | `Tax_Due` | Optional |
| Vehicle Status | Picklist | `Vehicle_Status` | Active, Sold, Scrapped |
| Vehicle Notes | Multi-line | `Vehicle_Notes` |
| Reg Check | Picklist | `Reg_Check` | OK, Check format. Set by `normalize_registration` | e.g. "locking wheel nut in glovebox" |

**Registration format:** don't add a save-time validation rule, because it would reject quick entries like `191d12345`
before they can be fixed. Instead, the `deluge/normalize_registration.dg` workflow function converts
`191d12345` / `191 D 12345` into `191-D-12345` after save. If it can't recognise the format, it sets
`Reg_Check` = *Check format*. Add that field as a picklist (`OK`, `Check format`) and a custom view to catch mistakes.

## 1.3 Job Cards (new custom module)

New Module → `Job Cards` (API name `Job_Cards`).

### Header fields

| Field label | Type | API name | Notes |
|---|---|---|---|
| Job Card Name | Single line (record name) | `Name` | Short title typed by staff, e.g. "Service – 191-D-12345" |
| Job Number | Auto-number | `Job_Number` | Prefix `JC-`, start `1001`. Fills itself in |
| Vehicle | Lookup → Vehicles | `Vehicle` | Required. Creates the service history list on the Vehicle. |
| Customer | Lookup → Contacts | `Customer` | Auto-filled from Vehicle by `deluge/job_card_on_create.dg` |
| Stage | Picklist | `Stage` | Booked, In Workshop, Waiting Parts, Ready, Collected, Cancelled. **Driven by the Blueprint** (see doc 02). |
| Job Type | Picklist | `Job_Type` | Full Service, Interim Service, Repair, Diagnostic, NCT Prep, Tyres, Brakes, Clutch, Timing Belt, Other |
| Booked For | Date/Time | `Booked_For` | |
| Mechanic | Single line | `Mechanic` | Mechanic's name (mechanics don't need a CRM licence) |
| Customer Complaint | Multi-line | `Customer_Complaint` | What the customer says is wrong |
| Mileage In | Number | `Mileage_In` | Required when moving to In Workshop |
| Work Done | Multi-line | `Work_Done` | Required when moving to Ready |
| Advisories | Multi-line | `Advisories` | Recommended future work (sell next visit) |
| Parts Awaited | Multi-line | `Parts_Awaited` | Required when moving to Waiting Parts |
| Promised By | Date/Time | `Promised_By` | |
| Books Estimate ID | Single line (read-only) | `Books_Estimate_ID` | Set by the "Create Quote" button |
| Books Estimate No | Single line (read-only) | `Books_Estimate_No` | |
| Books Invoice No | Single line | `Books_Invoice_No` | |
| Payment Status | Picklist | `Payment_Status` | Not Invoiced, Invoiced, Paid, Account Customer |
| Job Total (ex VAT) | Currency (formula or rollup) | `Job_Total` | Sum of line totals |
| Cancel Reason | Single line | `Cancel_Reason` | Required on the Cancel transition |
| Import Key | Single line | `Import_Key` | Used by the data import; hide from layouts |

### Subform: Job Lines (`Job_Lines`)

| Field | Type | API name |
|---|---|---|
| Line Type | Picklist: Labour, Part, Sundry | `Line_Type` |
| Description | Single line | `Description` |
| Part No. | Single line | `Part_No` |
| Qty / Hours | Decimal | `Qty` |
| Unit Price (ex VAT) | Currency | `Unit_Price` |
| Line Total | Formula: `Qty * Unit_Price` | `Line_Total` |

Subform **aggregate field**: Job Total = SUM(`Line_Total`).

## 1.4 Related lists and layouts

- **Contact page:** Vehicles, Job Cards and Zoho Finance (added automatically by the Books sync).
- **Vehicle page:** Job Cards, **sorted by Booked For descending**. This is the vehicle's service history.
- **Job Card page:** put Stage, Vehicle, Customer and Mileage In at the top, then Job Lines, then the Books section.

## 1.5 Custom views (save time at the desk)

| View | Module | Filter |
|---|---|---|
| Today's workshop | Job Cards | Booked For = today AND Stage not in (Collected, Cancelled) |
| On the ramp | Job Cards | Stage = In Workshop |
| Waiting parts | Job Cards | Stage = Waiting Parts |
| Ready – call customer | Job Cards | Stage = Ready |
| Not paid | Job Cards | Stage = Collected AND Payment Status != Paid |
| Service due next 30 days | Vehicles | Next Service Due in next 30 days AND Status = Active |
| NCT due next 60 days | Vehicles | NCT Due in next 60 days AND Status = Active |

## 1.6 Users and licences (cost control)

Only people who log in need a CRM licence. A typical setup:

- Owner: CRM + Books
- Front desk / service advisor: CRM + Books
- Mechanics: **no licence.** The advisor updates the Blueprint from the mechanic's paper or whiteboard, or you add a Zoho Forms "job update" form later.

Profiles: create an **Advisor** profile without delete permission on Vehicles and Job Cards.
