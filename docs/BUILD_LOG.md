# Build log

What has actually been built in the live Zoho account. Update this after each session.

**CRM org:** Supergear Motors Ltd. (org id 1042240000000023712), EU data centre, Europe/Dublin, EUR.
**Edition:** Enterprise **trial, ends 12 Oct 2026**. After that it drops to the Free edition unless a plan is bought.
**Books:** SuperGear Motors Ltd. (org id 20119876326), Ireland, EUR, Premium trial. **VAT not switched on yet.**

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

## Waiting on the owner
- [ ] **Choose a paid CRM plan before 12 Oct 2026.** Professional is the minimum for custom modules + Blueprint.
- [x] Vehicles module created
- [x] Job Cards module created
- [ ] Optional: tick *Do not allow duplicate values* on Vehicles → Registration
- [x] Sign up for Zoho Books (done 2026-09-27)
- [ ] Books → Settings → Taxes → tick *registered for VAT* and enter the VAT number (needed before VAT rates can be created)
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
1. [ ] Organise menu: rename Contacts → Customers, Accounts → Fleet & Business; hide unused modules
2. [x] Job Cards → add **Job Lines** subform (Line Type, Description, Part No, Qty, Unit Price, Line Total) + **Job Total** aggregate (doc 01 §1.3). ⚠️ Line Type still has placeholder values Option 1/Option 2 → change to Labour, Part, Sundry
3. [ ] Custom views: Today's workshop, Waiting parts, Ready, Not paid, Service due 30 days, NCT due 60 days (doc 01 §1.5)
4. [ ] Blueprint on Job Cards → Stage (doc 02)
5. [ ] Functions + workflow rules: normalize_registration, job_card_on_create, job_card_check_in, job_card_on_collected (doc 02 §2.2)
6. [ ] Books: switch on VAT → Claude creates VAT rates, items, suppliers → CRM sync → `zbooks` connection → Create Quote button (doc 03)
