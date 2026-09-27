# 3. Zoho Books + CRM: quote → invoice → payment

## 3.1 Create the Books organisation

1. Sign up for Zoho Books with **the same Zoho account/organisation as CRM**. This is required for the native sync.
2. Country: **Ireland**. Currency: EUR. Financial year: match your accountant (usually Jan–Dec).
3. Enter your VAT number, Eircode address and logo. Invoice/estimate prefixes: `INV-` and `QT-`.

## 3.2 VAT rates (confirm with your accountant)

Settings → Taxes. Motor repairs in Ireland usually use:

| Tax name | Rate | Use for |
|---|---|---|
| VAT 13.5% | 13.5% | Labour / repair and maintenance services |
| VAT 23% | 23% | Parts sold separately, tyres, accessories, and jobs where the **two-thirds rule** applies (parts > 2/3 of the total) |
| VAT 0% / Exempt | 0% | e.g. NCT fee passed through at cost, if applicable |

⚠️ These are typical rates, not tax advice. Get your accountant to confirm them, including when the two-thirds rule applies, before you send your first invoice.

## 3.3 Items (price list)

Items → New. Create the common lines once, so quotes are quick and consistent:

| Item | Type | Rate (example) | Tax |
|---|---|---|---|
| Labour (per hour) | Service | €75.00 | 13.5% |
| Full Service – small car | Service | fixed price | 13.5% |
| Diagnostic check | Service | €60.00 | 13.5% |
| Engine oil (per litre) | Goods | | 23% |
| Oil filter | Goods | | 23% |
| Brake pads (front) | Goods | | 23% |
| Sundries / consumables | Goods | | 23% |

Put **your own** prices in `config/items.csv`. The *SuperGear Motors Ltd* workflow creates the taxes and items for you (doc 07). Import the full parts list later using Items → Import.

## 3.4 Turn on the CRM ↔ Books sync

In Books: Settings → Integrations → **Zoho Apps → Zoho CRM** → Connect.

- Sync: **Contacts** (not Accounts only). Direction: CRM → Books.
- Sync criteria: all contacts, or only contacts with a Job Card (simplest: all).
- Conflict: CRM wins.
- Enable **"Show Zoho Finance in CRM"**. Estimates, invoices and payments then appear on the CRM contact page, and advisors can create a Books invoice from inside CRM.

## 3.5 The "Create Quote" button on Job Cards

The native sync handles customers. Turning a **Job Card's lines** into a Books estimate needs one small function:

1. CRM: Setup → Developer Hub → **Connections** → New → service **Zoho Books**. Name it `zbooks`.
   Scopes: `ZohoBooks.estimates.CREATE`, `ZohoBooks.estimates.READ`, `ZohoBooks.contacts.READ`, `ZohoBooks.contacts.CREATE`, `ZohoBooks.settings.READ`.
2. Setup → Developer Hub → **Functions** → New → Button. Paste in `deluge/create_books_estimate.dg`.
   Argument: `jobId` = Job Cards → Job Card Id.
3. Fill in the `CONFIG` block at the top: Books organisation ID (Books → Settings → Organisation Profile), and the tax IDs for 13.5% and 23% (Books → Settings → Taxes; the ID is in the URL when you open a tax).
4. Setup → Modules → Job Cards → **Links & Buttons** → New Button "Create Quote in Books" → View page → run function.

What the button does:
- finds the customer in Books by email (and creates them if missing)
- copies every Job Line to the estimate: Labour lines at 13.5%, Parts/Sundry lines at 23%
- sets the estimate reference to the Job Number and adds the vehicle registration and mileage to the notes
- writes the estimate number and ID back to the Job Card

Then, in Books: **Send estimate** (email or PDF) → customer approves → **Convert to Invoice** → send it with a payment link.

## 3.6 Card payments (Stripe)

Books → Settings → **Online Payments** → Stripe → connect your Stripe account.
Tick "Allow customers to pay online" on your invoice template. Every invoice email then includes a **Pay Now** link, and payments are recorded automatically.

For card-machine or cash payments at the counter: open the invoice → **Record Payment**.

When the invoice is paid, the advisor sets Payment Status = Paid on the Job Card during the *Collected* transition. You can automate this later; it isn't needed for Phase 1.

## 3.7 Payment reminders

Books → Settings → Reminders → turn on the automated reminder at **7 and 14 days overdue**, for account/fleet customers only.
