# 6. Go-live checklist

## Week 1: build
- [ ] CRM Sandbox created (Setup → Sandbox) and all the steps below done there first
- [ ] Contacts fields added (doc 01 §1.1)
- [ ] Vehicles module and fields, registration unique and validated (§1.2)
- [ ] Job Cards module, fields and the Job Lines subform (§1.3)
- [ ] Related lists and custom views (§1.4, §1.5)
- [ ] Blueprint published (doc 02)
- [ ] Functions added: `normalize_registration`, `job_card_on_create`, `job_card_check_in`, `job_card_on_collected`, `create_books_estimate`
- [ ] Workflow rules linked to the functions (doc 02 §2.2)

## Week 2: Books
- [ ] Books organisation created (Ireland, EUR, VAT number)
- [ ] VAT rates **confirmed by your accountant**
- [ ] Items / price list entered
- [ ] CRM sync on; Zoho Finance tab visible on Contacts
- [ ] Books connection `zbooks` created in CRM; CONFIG IDs filled into `create_books_estimate`
- [ ] Stripe connected; test invoice paid with a real card and refunded
- [ ] Estimate and invoice templates branded (logo, bank details, T&Cs, warranty text)
- [ ] Document inbox address noted; Autoscan on; supplier email forwarding rules live
- [ ] Taxes, items and vendors created by the *SuperGear Motors Ltd* workflow (doc 07)

## Week 3: data and training
- [ ] Regulars, fleet customers and anyone due soon entered from the notebooks (doc 05, lane 2)
- [ ] Spot-check 20 entered vehicles against the notebooks
- [ ] Desk routine agreed: every new caller or walk-in is created in CRM on the spot (doc 05, lane 1)
- [ ] Sandbox changes deployed to production
- [ ] Staff walkthrough: book a job → check in → add lines → Create Quote → Ready → invoice → paid → Collected
- [ ] Run **3 real jobs end to end** in parallel with paper
- [ ] Paper stops; notebooks archived

## End-to-end test script

1. Create a customer Mary Test with mobile `+353870000000`.
2. Create vehicle `12d1234`. It should save as `12-D-1234`.
3. New Job Card on that vehicle. The Customer should fill in automatically.
4. Check In with mileage 150000. The vehicle's Current Mileage should show 150000.
5. Add lines: 1.5 h Labour at €75, 1 × Oil filter at €12. Job Total should be €124.50.
6. Click **Create Quote in Books**. Estimate `QT-…` appears in Books: labour at 13.5%, filter at 23%. The estimate number shows on the Job Card.
7. In Books, convert the estimate to an invoice, email it and pay by Stripe (test).
8. Work Complete → Collected. The vehicle's Last Service Date should be today and Next Service Due today + 12 months.
9. Forward a sample supplier PDF to the Books inbox. Within a few minutes it should show as Scanned. Convert it to a bill.
