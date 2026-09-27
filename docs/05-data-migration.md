# 5. Getting paper records into Zoho

The records are all on paper, so don't try to type in every old notebook. Use a **three-lane approach**
so the system becomes useful from day one while the typing effort stays small.

## Lane 1: capture on the next visit (all customers, zero backlog)

From go-live, **every customer who calls or walks in gets created in CRM at that moment**:
Customer → Vehicle → Job Card. It takes about 60 seconds at the desk. Within 3–6 months every active
customer is in the system without a separate data-entry project.

## Lane 2: regulars and fleet first (a one-off, a few evenings)

Go through the notebooks and pick out **regulars, fleet/trade accounts and anyone with a service or NCT
due in the next 3 months**. That's usually 50–200 people. Record for each one:
- customer name, mobile, and email if you have it
- each vehicle: registration, make, model, approximate mileage
- **last visit only**: date, what was done, and anything advised (e.g. "rear tyres soon")

Two ways to get this in:

**a) Spreadsheet → import.** Copy the three files from `templates/` into a folder that is **not** in
this repo (e.g. `Documents/garage-data/`), fill them in with Excel or Google Sheets (save as CSV), and run:

```bash
pip install -r requirements.txt
python -m zoho_setup validate --data-dir ~/Documents/garage-data              # checks regs, mobiles, dates
python -m zoho_setup import-data --data-dir ~/Documents/garage-data           # dry run
python -m zoho_setup import-data --data-dir ~/Documents/garage-data --apply   # import
```

Re-running is safe: customers match on mobile number, vehicles on registration, and jobs on registration + date.

**b) Photos → Claude with Zoho MCP.** Connect Zoho MCP in the Claude app, photograph a notebook page,
and ask Claude to read it and create the customers, vehicles and last-visit job cards. **Always ask
for a list to check before it creates anything.** Handwriting gets misread, especially registrations
and phone numbers.

## Lane 3: the notebooks stay the archive

Keep the old notebooks for the history of vehicles you don't see often. When one of those customers comes back,
look them up in the notebook once, and add the useful history to the vehicle's **Vehicle Notes**.

## Rules for the data

- **Mobile numbers:** use `+353871234567`, or just `087 123 4567` and the import converts it. The mobile number is how
  customers are matched, and WhatsApp needs it later.
- **Registrations:** anything like `191d12345` is fine. It's saved as `191-D-12345`.
- **GDPR:** leave the WhatsApp and marketing consent columns **blank** unless the customer actually agreed.
  Ask for consent at their next visit.
- **Customer data never goes in this GitHub repo.** `data/` is git-ignored, and the import refuses to run inside
  GitHub Actions.
