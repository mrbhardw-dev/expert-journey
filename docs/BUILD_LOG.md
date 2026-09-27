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

## Waiting on the owner
- [ ] **Choose a paid CRM plan before 12 Oct 2026.** Professional is the minimum for custom modules + Blueprint.
- [x] Vehicles module created
- [ ] **Job Cards module**: name it Job Card / Job Cards and Save
- [ ] Optional: tick *Do not allow duplicate values* on Vehicles → Registration
- [x] Sign up for Zoho Books (done 2026-09-27)
- [ ] Books → Settings → Taxes → tick *registered for VAT* and enter the VAT number (needed before VAT rates can be created)
- [ ] Send real prices (`config/items.csv`) and supplier names (`config/suppliers.csv`)
- [ ] Accountant confirms VAT 13.5% labour / 23% parts

## Next for Claude (once the above is done)
- [x] Create the Vehicles fields (17)
- [ ] Create the Job Cards fields (18) + a *Job Number* auto-number (JC-1001)
- [ ] Create the Books VAT rates, items and suppliers
- [ ] Walk through the Job Lines subform, Blueprint, Deluge functions and Books sync (docs 01–03)
- [ ] Enter the first regular customers from notebook photos
