# 5. Data migration: from Excel and notebooks into Zoho

Import in this order, because each file links to the one before it:

| Order | File | Import into | Match / link on |
|---|---|---|---|
| 1 | `templates/customers.csv` | CRM → Contacts → Import | New records; de-duplicate on **Mobile** |
| 2 | `templates/vehicles.csv` | CRM → Vehicles → Import | Link `Customer Mobile` → Contact by **Mobile** |
| 3 | `templates/job_history.csv` | CRM → Job Cards → Import | Link `Registration` → Vehicle by **Registration** |
| 4 | `templates/suppliers.csv` | Books → Vendors → Import | none |

## Rules for cleaning the data

- **Mobile numbers:** use `+353` format with no spaces (`+353871234567`). The mobile number is how customers are matched, and WhatsApp needs this format later.
- **Registrations:** upper-case with dashes (`191-D-12345`). The normalize function also fixes these on edit, but import clean data anyway.
- **One row per vehicle**, even when the same customer owns two cars.
- **Job history:** you don't need every old job. The **last visit per vehicle** is enough, so the service and NCT reminders start working. Put old job details in `Work_Done` as text; old jobs don't need job lines.
- Past jobs import with Stage = **Collected**. Blueprint doesn't block imports.
- For the GDPR consent fields, leave them **blank** unless you have a record that the customer gave consent.

## Using Zoho MCP (optional)

If you've connected the Zoho MCP server to Claude, you can hand Claude the old Excel file and
ask it to clean the data into these templates, then create the records directly. Do a dry run with 10 rows first,
and check the result in CRM before running the rest.
