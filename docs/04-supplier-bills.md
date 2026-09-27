# 4. Supplier invoices: email → Books bill, no typing

## 4.1 Set up suppliers (vendors)

List them in `config/suppliers.csv` and let the *Zoho setup* workflow create them (doc 07), or use Purchases → Vendors → Import. List your motor factors,
tyre suppliers, oil supplier, etc. For each vendor set:
- a default expense account (e.g. *Cost of Goods Sold – Parts*, *Tyres*, *Consumables*)
- a default tax (VAT 23% for most parts suppliers)
- payment terms (e.g. Net 30 / end of month)

## 4.2 The Books document inbox

Books → **Documents** → Inbox. Books gives your organisation a unique email address
(shown at the top of the Inbox, e.g. `something@<your-org>.zohobooks…`). Anything sent there
lands in Documents.

Turn on **Autoscan** (Documents → Settings). Books then reads the PDF and pre-fills the vendor, date,
bill number, amounts and VAT. Autoscan has a monthly limit that depends on your Books plan. Check that it covers your
monthly supplier invoice count; if not, the higher plan or a scan add-on usually costs less than the time spent typing.

## 4.3 Make supplier emails forward automatically

Set up a forwarding rule in the mailbox where suppliers send invoices:

**Gmail:** Settings → Forwarding → add the Books inbox address (verify it) → Filters →
`from:(@supplier1.ie OR @supplier2.ie OR @tyresupplier.ie) has:attachment` → Forward to the Books inbox.

**Outlook / Microsoft 365:** Rules → New rule → *From* contains supplier domains AND *has attachment* → *Forward to* the Books inbox.

**Paper invoices:** use the Zoho Books mobile app → Documents → **Scan** at the counter, or snap a photo and email it in.

## 4.4 Daily 5-minute routine

1. Books → Documents → Inbox. Each scanned invoice shows as *Scanned*.
2. Open it → check vendor, total and VAT → **Convert to Bill**.
3. Books remembers the account and tax per vendor, so after a few weeks this is mostly just clicking **Save**.
4. Pay bills from Purchases → Bills → Record Payment, or in bulk. If you connect your bank feed
   (Banking → Add bank: AIB, BOI and PTSB feeds are available via Open Banking; check yours), payments match automatically.

## 4.5 Optional: link parts cost to the job

To see profit per job, put the Job Number (`JC-1234`) in the bill's **Reference** field when
the parts were ordered for a specific car. This is enough for Phase 1; per-job costing can come later with Inventory or Analytics.
