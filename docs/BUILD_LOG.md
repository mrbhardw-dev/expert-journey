# Build log

What has actually been built in the live Zoho account. Update this after each session.

**CRM org:** Supergear Motors Ltd. (org id 1042240000000023712), EU data centre, Europe/Dublin, EUR.
**Edition:** Enterprise **trial, ends 12 Oct 2026**. After that it drops to the Free edition unless a plan is bought.
**Books:** SuperGear Motors Ltd. (org id 20119876326), Ireland, EUR, Premium trial. **VAT not switched on yet.**

## Done
| Date | What | How |
|---|---|---|
| 2026-09-27 | Contacts fields: Eircode, Customer_Type, Preferred_Contact, WhatsApp_Consent, Marketing_Consent, Consent_Date (API names verified) | Claude via Zoho CRM MCP |

## Waiting on the owner
- [ ] **Choose a paid CRM plan before 12 Oct 2026.** Professional is the minimum for custom modules + Blueprint.
- [ ] **Create the two custom modules in CRM** (Setup → Customization → Modules and Fields → + New Module):
  - **Vehicles**: rename the record-name field to *Registration*, tick *Do not allow duplicate values*
  - **Job Cards**: set the record-name field to *Auto-Number*, label *Job Number*, prefix `JC-`, start `1001`
- [x] Sign up for Zoho Books (done 2026-09-27)
- [ ] Books → Settings → Taxes → tick *registered for VAT* and enter the VAT number (needed before VAT rates can be created)
- [ ] Send real prices (`config/items.csv`) and supplier names (`config/suppliers.csv`)
- [ ] Accountant confirms VAT 13.5% labour / 23% parts

## Next for Claude (once the above is done)
- [ ] Create the Vehicles fields (17) and Job Cards fields (18) from `config/crm_schema.yaml`
- [ ] Create the Books VAT rates, items and suppliers
- [ ] Walk through the Job Lines subform, Blueprint, Deluge functions and Books sync (docs 01–03)
- [ ] Enter the first regular customers from notebook photos
