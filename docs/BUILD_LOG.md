# Build log

What has actually been built in the live Zoho account. Update this after each session.

**CRM org:** Supergear Motors Ltd. (org id 1042240000000023712), EU data centre, Europe/Dublin, EUR.
**Edition:** Enterprise **trial, ends 12 Oct 2026**. After that it drops to the Free edition unless a plan is bought.
**Books:** SuperGear Motors Ltd. (org id 20119876326), Ireland, EUR, Premium trial. **Company:** CRO 782596, VAT IE4393123CH. **VAT registration not switched on yet.** Connected to CRM: CRM Contacts ↔ Books Customers, Vendors ↔ Vendors; Products↔Items paused.

## ▶ RESUME HERE (last session: 27 Sep 2026, ~14:55)

**Live data in CRM:** 1 customer (Mritunjay Bhardwaj, id 1042240000000643985: email set, **mobile missing**),
1 vehicle (181-KE-6745, BMW 530e 2018, 16,800 km, id 1042240000000643987), 0 job cards (first real = JC-1002),
33 roadmap Tasks (P1.0–P5.1; only P1.0 Completed, P2.4 In Progress). Fleet Accounts: none.
**Live data in Books:** 3 VAT rates, 28 items (labour €80 confirmed; rest ESTIMATED; item sync to CRM Products now paused), 2 vendors (Clane Motor Factors, Fergal Allen Motor Factors; also synced to CRM Vendors), 1 customer (Mritunjay, synced from CRM, id 1426684000000073015).
**CRM Services (`Services__s`):** 16 services (LAB-HR + 15 SVC-*), prices = Books, custom fields `SKU` (unique) and `VAT_Rate`; see config/services.csv.

**Waiting on the owner (check these first, in this order):**
1. ~~Books sync set to Contacts~~ done 27 Sep 14:53, Mritunjay verified in Books. CRM task P2.4 marked Completed.
2. ~~CRM Services module~~ **done 27 Sep 14:45**: 16 services live (re-verified 15:05 against config/items.csv). Owner: review prices/durations together with the Books items (P2.1b); a price change must be made in BOTH Books and CRM Services (same SKU).
3. ~~P1.2b~~ done 15:20: Vehicles + Job Cards Owner → "Handled By"; Secondary Email removed from both; owner chose to KEEP Email + Email Opt Out (verified via API).
4. P1.1: hide unused modules: owner chose NOT to hide for now (27 Sep). Don't re-ask; revisit later.
5. **VAT registration in Books (P2.3): number received (IE4393123CH, CRO 782596); owner must enter it in Books → Taxes → VAT Settings (no API) plus VAT registration date.** Also: accountant VAT confirmation (P2.2), owner price review (P2.1b), suppliers list (P2.1).
6. **P1.9 buy paid CRM plan before 12 Oct 2026.**
7. **DNS (parked by owner, revisit):** owner removed ns1/ns2.dns-parking.com in Hosting Ireland panel, but .ie registry still lists them (checked ~16:30). If still there: owner asks Hosting Ireland support to push the NS update. Until then some mail to info@ lands in old Hostinger mailbox. Then check site TLS cert (expired 28 May 2026).

**Next build steps:** P1.6 saved lists now automated: `python -m zoho_setup crm-views` (config/crm_views.yaml, CRM API v8 custom_views POST, found in github.com/zoho/crm-oas). Needs the owner to create the Zoho API client + GitHub secrets (docs/07) first; not yet run against live CRM. Then P1.3 Blueprint → P1.5 Deluge scripts → P2.5 Create Quote button (no API, manual).

**Gotchas learned:**
- Clicking "customize layout" and being asked for a *layout name* = creating a NEW layout. Cancel; edit "Standard".
- Line_Type picklist stored values are "Option 1" (Labour) / "Option 2" (Part) / "Sundry"; scripts handle both.
- Job Lines qty field API name is `QTY` (not `Qty`).
- Zoho CRM MCP: `deleteRecords` (bulk) fails with parse error; use `deleteRecord` one at a time.
- Books `create_tax` rejects `country_code`; omit it.
- Services module API name is `Services__s`. Required on create: Service_Name, Price, Duration (minutes), Location, Availability_Type, Members as `[{"Members": {"id": <user id>}}]`. Its built-in Tax picklist only has 0% placeholders, hence the custom VAT_Rate field.
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
| 2026-09-27 | Books Organisation Profile saved by owner: logo, address Ballygoran Road, Maynooth, Co. Kildare W23 TR5X, Company ID label 'CRO' = 782596 (verified). VAT number NOT yet stored (tax_id / tax_reg_no still blank); phone blank | Owner in Books UI, verified by Claude |
| 2026-09-27 | Service catalog: Services module enabled by owner; fields SKU (unique, 1042240000000657007) and VAT_Rate (13.5/23/0, 1042240000000657016) added; 16 services created matching the Books service items 1:1 (price, name, SKU), durations in minutes, provider = owner user, Mon–Fri business days. Prices still ESTIMATED except labour €80. config/services.csv + crm_schema.yaml updated | Claude via Zoho CRM MCP |
| 2026-09-27 | Email domain supergearmotors.ie (registrar Hosting Ireland; website on Hostinger IPs). Owner signed up for Zoho Mail (EU) and added in Hosting Ireland DNS: zoho-verification TXT + MX mx/mx2/mx3.zoho.eu (10/20/30). Public DNS at ~15:00 is mid-switch: ~1/3 of lookups see Hosting Ireland nameservers with the Zoho records, ~2/3 still see the old Hostinger zone (ns1/ns2.dns-parking.com: MX mx1/mx2.hostinger.com, SPF _spf.mail.hostinger.com). Still to do: confirm nameservers at registrar, add Zoho SPF + DKIM, re-check | Owner in DNS, checked by Claude |
| 2026-09-27 | Zoho Mail mailbox info@supergearmotors.ie created by owner. Re-check: MX Zoho ~45% / Hostinger ~55% of lookups (inbound mail unreliable until Hostinger zone updated or nameservers settled); SPF still Hostinger; DKIM (zmail._domainkey) not set. Next: owner updates Hostinger MX+TXT, SPF `v=spf1 include:zohomail.eu ~all` in both zones, DKIM selector zmail; then connect info@ to CRM (Setup → Channels → Email) and Books sender | Owner, checked by Claude |
| 2026-09-27 | Confirmed: supergearmotors.ie nameservers are **Hostinger** (ns1/ns2.dns-parking.com); Hosting Ireland is registrar only and its zone is not live. Decision: keep DNS at Hostinger (website is there). All Zoho Mail records (MX mx/mx2/mx3.zoho.eu, verification TXT, SPF `v=spf1 include:zohomail.eu ~all`, DKIM `zmail._domainkey`) go in Hostinger hPanel | Owner / Claude |
| 2026-09-27 | Owner has no Hostinger login (website is a Hostinger-built site: www CNAME www.supergearmotors.ie.cdn.hstgr.net, apex on rotating Hostinger CDN IPs). Plan changed to move DNS to Hosting Ireland: first fix HI zone (apex A 185.43.232.251 → 191.101.104.246 + 195.35.60.196; www CNAME → www.supergearmotors.ie.cdn.hstgr.net; Zoho MX/TXT/SPF/DKIM), Claude reviews, then owner sets nameservers ns1/ns2.webhostingireland.ie. Risk: pinned apex IPs may change; find who owns the Hostinger account | Owner / Claude |
| 2026-09-27 | Books↔CRM sync switched Accounts → **Contacts** (duplicates: Skip, view: All Contacts); Products↔Items sync **paused**. Org Address Format already contains Company ID + Tax ID placeholders (saved). Verified: Mritunjay synced into Books as customer (is_linked_with_zohocrm) | Claude via Chrome, verified via Zoho Books MCP |
| 2026-09-27 | Books → Taxes → Tax Settings: Tax Registration Number type VAT = 4393123CH is saved (seen on fresh page load). Note: org API still returns tax_reg_no blank / is_tax_registered false, so verify on a test invoice PDF | Checked by Claude via Chrome |
| 2026-09-27 | DNS check ~15:40: .ie registry lists 4 nameservers, 2 Hostinger (ns1/ns2.dns-parking.com) + 2 Hosting Ireland (ns3.webhostingireland.ie, ns4.webhostingireland.eu). Hosting Ireland zone has all Zoho Mail records correct (MX mx/mx2/mx3.zoho.eu, verification TXT, SPF zohomail.eu, DKIM zmail) but its website records are wrong (apex A 185.43.232.251 = Hosting Ireland holding page, www → apex). Hostinger zone has the working website (apex 91.108.98.100 + 93.127.179.128, www CNAME www.supergearmotors.ie.cdn.hstgr.net) but old Hostinger MX/SPF. Result: ~half of mail and ~half of website visitors go to the wrong place. Fix: in Hosting Ireland zone set apex A to the Hostinger IPs + www CNAME, then remove the two dns-parking.com nameservers at the registrar | Checked by Claude (dig) |
| 2026-09-27 | Hosting Ireland zone fixed by owner (serial 2026092716): apex A 91.108.98.100 + 93.127.179.128, www CNAME supergearmotors.ie.cdn.hstgr.net (works: same 301 → https://supergearmotors.ie/ as Hostinger's www target), Zoho MX/SPF/verification intact. Verified site title 'Supergearmotors' on both apex IPs. Next: owner removes ns1/ns2.dns-parking.com at registrar. NOTE: site TLS cert (Let's Encrypt, CN supergearmotors.ie) expired 28 May 2026; renewal lives in the Hostinger account (owner has no login) | Owner in DNS, checked by Claude |

| 2026-09-27 | GitHub Actions confirmed working against live Zoho (owner set up secrets): run on PR #1 dry-run = 77 exist, 8 CRM list views would create. Books custom fields created, shown on PDF: Quote Vehicle Reg 1426684000000070030 / Mileage (km) 1426684000000072009; Invoice Vehicle Reg 1426684000000070032 / Mileage (km) 1426684000000076001 (api names cf_vehicle_reg, cf_mileage_km); create_books_estimate.dg now fills them. CRM tasks: P1.2 re-scoped to info@ via Zoho Mail, P2.1 In Progress, P1.1 Deferred, P1.6 = merge PR #1; new P1.2c (finish DNS switch) and P2.9 (Books sender info@). DNS 16:25: DKIM + Zoho SPF live everywhere; MX still ~80% Hostinger; NS mixed | Claude via MCP |
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
