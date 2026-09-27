# Build log

What has actually been built in the live Zoho account. Update this after each session.

**CRM org:** Supergear Motors Ltd. (org id 1042240000000023712), EU data centre, Europe/Dublin, EUR.
**Edition:** Enterprise **trial, ends 12 Oct 2026**. After that it drops to the Free edition unless a plan is bought.
**Books:** SuperGear Motors Ltd. (org id 20119876326), Ireland, EUR, Premium trial. **Company:** CRO 782596, VAT IE4393123CH. **VAT registration not switched on yet.** Connected to CRM (sync scope needs fixing).

## ▶ RESUME HERE (last session: 27 Sep 2026, ~10:15)

**Live data in CRM:** 1 customer (Mritunjay Bhardwaj, id 1042240000000643985: email set, **mobile missing**),
1 vehicle (181-KE-6745, BMW 530e 2018, 16,800 km, id 1042240000000643987), 0 job cards (first real = JC-1002),
33 roadmap Tasks (P1.0–P5.1; only P1.0 Completed, P2.4 In Progress). Fleet Accounts: none.
**Live data in Books:** 3 VAT rates, 28 items (labour €80 confirmed; rest ESTIMATED; items now also syncing to CRM Products), 2 vendors (Clane Motor Factors, Fergal Allen Motor Factors), 0 customers.

**Waiting on the owner (check these first, in this order):**
1. **Books sync set to Contacts** (currently syncs Accounts) → then verify Mritunjay appears in Books (task P2.4).
2. **CRM Services module**: "Enable Services" clicked but module not present via API; owner to finish the setup wizard / send screenshot. Then Claude creates 16 services matching Books SKUs (SVC-*, LAB-HR).
3. P1.2b: rename "Vehicle Owner"/"Job Card Owner" → "Handled By"; remove Email/Secondary Email from Vehicles + Job Cards (still pending when checked).
4. P1.1: hide unused modules (Leads, Deals, Inventory group, etc.): still all visible.
5. **VAT registration in Books (P2.3): number received (IE4393123CH, CRO 782596); owner must enter it in Books → Taxes → VAT Settings (no API) plus VAT registration date.** Also: accountant VAT confirmation (P2.2), owner price review (P2.1b), suppliers list (P2.1).
6. **P1.9 buy paid CRM plan before 12 Oct 2026.**

**Next build steps with Claude guiding:** P1.3 Blueprint → P1.5 Deluge scripts → P1.6 saved lists → P2.5 Create Quote button.

**Gotchas learned:**
- Clicking "customize layout" and being asked for a *layout name* = creating a NEW layout. Cancel; edit "Standard".
- Line_Type picklist stored values are "Option 1" (Labour) / "Option 2" (Part) / "Sundry"; scripts handle both.
- Job Lines qty field API name is `QTY` (not `Qty`).
- Zoho CRM MCP: `deleteRecords` (bulk) fails with parse error; use `deleteRecord` one at a time.
- Books `create_tax` rejects `country_code`; omit it.
- Connector cannot create modules/layouts/Blueprint/workflows/functions/buttons/custom views/menu groups, or change settings/icons: owner clicks, Claude guides and verifies.

## Done
| Date | What | How |
|---|---|---|
| 2026-09-27 | Contacts fields: Eircode, Customer_Type, Preferred_Contact, WhatsApp_Consent, Marketing_Consent, Consent_Date (API names verified) | Claude via Zoho CRM MCP |
| 2026-09-27 | Vehicles module created; record name relabelled *Registration* | Owner in CRM UI |
| 2026-09-27 | Vehicles fields (17): Customer, Company, Make, Model, Year, Fuel_Type, Engine_Size, Colour, VIN, Current_Mileage, Last_Service_Date, Next_Service_Due, NCT_Due, Tax_Due, Vehicle_Status, Vehicle_Notes, Reg_Check (API names verified) | Claude via Zoho CRM MCP |
| 2026-09-27 | Removed Zoho's 63 sample records (10 Leads, 10 Contacts, 10 Accounts, 10 Deals, 12 Tasks, 9 Meetings, 2 Calls). All modules verified empty; Books had none | Claude via Zoho CRM MCP |
| 2026-09-27 | Job Cards module created | Owner in CRM UI |
| 2026-09-27 | Job Cards fields (19): Job_Number (auto-number JC-1001), Vehicle, Customer, Stage, Job_Type, Booked_For, Mechanic, Customer_Complaint, Mileage_In, Work_Done, Advisories, Parts_Awaited, Promised_By, Books_Estimate_ID, Books_Estimate_No, Books_Invoice_No, Payment_Status, Cancel_Reason, Import_Key (API names verified) | Claude via Zoho CRM MCP |
| 2026-09-27 | End-to-end link check: throwaway Customer → Vehicle → Job Card created, Job_Number auto-filled (JC-1001), lookups OK; all three deleted. First real job will be JC-1002 | Claude via Zoho CRM MCP |
| 2026-09-27 | Job Lines subform (Line_Type, Description, Part_No, QTY, Unit_Price, Line_Total formula) + Job_Total on Job Cards; Standard profile given access to Vehicles and Job Cards | Owner in CRM UI, verified by Claude |
| 2026-09-27 | Books VAT rates: VAT 13.5% (1426684000000064001), VAT 23% (1426684000000065001), VAT 0% (1426684000000063002); IDs filled into create_books_estimate.dg | Claude via Zoho Books MCP |
| 2026-09-27 | Contacts renamed Customers, Accounts renamed Fleet Accounts (API names unchanged) | Owner in CRM UI, verified by Claude |
| 2026-09-27 | 16 owner Tasks created in CRM with step-by-step instructions: paid plan (due 9 Oct), VAT registration, accountant VAT check, hide modules, Operations group, Blueprint, scripts, saved lists, Books↔CRM link, Create Quote button, Stripe, supplier auto-scan, send prices, branding, enter regulars, GDPR consent | Claude via Zoho CRM MCP |
| 2026-09-27 | Operations menu group done by owner (task marked Completed). Unused modules still visible org-wide. Task added: connect Gmail to CRM | Owner / Claude via MCP |
| 2026-09-27 | Full roadmap: 31 CRM Tasks numbered P1.0–P5.1 (see docs/ROADMAP.md). First real vehicle 181KE6745 re-formatted to 181-KE-6745 | Claude via Zoho CRM MCP |
| 2026-09-27 | Books price list: 28 items with ESTIMATED prices (16 labour/services @13.5%, 12 parts @23%, SKUs LAB-/SVC-/PRT-); config/items.csv updated to match; task P2.1b for owner to confirm prices. CRM Services module not yet enabled (owner) | Claude via Zoho Books MCP |
| 2026-09-27 | Books↔CRM integration connected by owner, but syncing Accounts not Contacts (P2.4 In Progress). Placeholder Fleet Account 'SuperGear Customers' deleted from CRM + Books (owner approved); vehicle 181-KE-6745 unlinked from it first, still linked to customer | Owner / Claude via MCP |
| 2026-09-27 | Owner confirmed: labour €80/hr + VAT (Books item LAB-HR updated); suppliers Clane Motor Factors + Fergal Allen Motor Factors created in Books (contact details TBC); company CRO 782596 / VAT IE4393123CH recorded. Owner says 'normal VAT is 13.5%': pending decision whether parts on repair jobs should also be 13.5% | Claude via Zoho Books MCP |
| 2026-09-27 | Sync re-test: edited Mritunjay (Customer_Type=Private) to trigger sync → still 0 customers in Books; confirms sync scope must be changed to Contacts in Books UI. Did NOT hand-create him in Books (would duplicate once sync fixed). Books org profile/VAT fields still blank at 14:10 | Claude via MCP |

## Waiting on the owner
- [ ] **Choose a paid CRM plan before 12 Oct 2026.** Professional is the minimum for custom modules + Blueprint.
- [x] Vehicles module created
- [x] Job Cards module created
- [ ] Optional: tick *Do not allow duplicate values* on Vehicles → Registration
- [x] Sign up for Zoho Books (done 2026-09-27)
- [ ] (waiting on VAT number) Books → Settings → Taxes → tick *registered for VAT* and enter the VAT number (rates already exist; this is needed for VAT returns and to show the VAT no. on invoices)
- [ ] Send real prices (`config/items.csv`) and supplier names (`config/suppliers.csv`)
- [ ] Accountant confirms VAT 13.5% labour / 23% parts

## Next for Claude (once the above is done)
- [x] Create the Vehicles fields (17)
- [x] Create the Job Cards fields (19, incl. Job Number auto-number)
- [x] Job Lines subform added
- [ ] Create the Books VAT rates, items and suppliers
- [ ] Walk through the Job Lines subform, Blueprint, Deluge functions and Books sync (docs 01–03)
- [ ] Enter the first regular customers from notebook photos

## Remaining CRM setup (Zoho UI only: the connector has no API for these)
Order matters. Do them top to bottom.
1. [ ] Organise menu: ~~rename~~ done; hide unused modules; Operations group
2. [x] Job Cards → add **Job Lines** subform (Line Type, Description, Part No, Qty, Unit Price, Line Total) + **Job Total** aggregate (doc 01 §1.3). Line Type options renamed to Labour / Part / Sundry (stored values stay Option 1 / Option 2; script handles both). Accidental extra layout **M** deleted (verified: only Standard remains)
3. [ ] Custom views: Today's workshop, Waiting parts, Ready, Not paid, Service due 30 days, NCT due 60 days (doc 01 §1.5)
4. [ ] Blueprint on Job Cards → Stage (doc 02)
5. [ ] Functions + workflow rules: normalize_registration, job_card_on_create, job_card_check_in, job_card_on_collected (doc 02 §2.2)
6. [ ] Books: switch on VAT → Claude creates VAT rates, items, suppliers → CRM sync → `zbooks` connection → Create Quote button (doc 03)
