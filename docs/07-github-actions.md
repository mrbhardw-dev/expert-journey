# 7. Automated setup with GitHub Actions

Two workflows live in `.github/workflows/`:

| Workflow | Runs | Needs credentials | Does |
|---|---|---|---|
| **Validate** | automatically on every push | no | tests, config checks, CSV template checks, and checks that the Deluge scripts only use fields that exist |
| **SuperGear Motors Ltd** | by hand (Actions tab → SuperGear Motors Ltd → Run workflow) | yes | creates CRM custom fields, CRM list views, Books VAT rates, the Books item price list and Books suppliers |

## What gets automated and what doesn't

| Automated (Zoho has an API) | Manual (no Zoho API; printed as a checklist after every run) |
|---|---|
| ✅ CRM custom fields on Contacts, Vehicles, Job Cards (`config/crm_schema.yaml`) | Creating the Vehicles and Job Cards **modules** (one click each) |
| ✅ CRM list views: Today in the workshop, Waiting parts, Not paid, Service/NCT due… (`config/crm_views.yaml`) | |
| ✅ Books VAT rates (`config/books.yaml`) | Job Lines subform and the Job Total field |
| ✅ Books items / price list (`config/items.csv`) | Blueprint, workflow rules, the Create Quote button |
| ✅ Books suppliers (`config/suppliers.csv`) | Pasting the Deluge functions and creating the `zbooks` connection |
| ✅ Customer / vehicle / job import (**run locally only**, see doc 05) | Books ↔ CRM sync toggle, Stripe, Autoscan, email forwarding |

Every run is **safe to repeat**: anything that already exists is left alone and reported as `exists`.

## One-time setup

### 1. Create a Zoho API client (5 minutes)

1. Go to **https://api-console.zoho.eu** (EU data centre, which is right for Irish accounts) → *Add Client* → **Self Client**.
2. Copy the **Client ID** and **Client Secret**.
3. Click the *Generate Code* tab and paste in these scopes:
   ```
   ZohoCRM.settings.modules.READ,ZohoCRM.settings.fields.ALL,ZohoCRM.settings.custom_views.ALL,ZohoCRM.modules.ALL,ZohoBooks.settings.ALL,ZohoBooks.contacts.ALL
   ```
   Duration: 10 minutes. Description: `github setup`. Click Create and copy the **code**.
4. Within 10 minutes, swap the code for a **refresh token** on your own computer:
   ```bash
   curl -s -X POST "https://accounts.zoho.eu/oauth/v2/token" \
     -d grant_type=authorization_code -d client_id=YOUR_ID -d client_secret=YOUR_SECRET -d code=THE_CODE
   ```
   Copy `refresh_token` from the response. It doesn't expire unless you revoke it.

> Never paste these values into a chat, an issue, a commit or a file in this repo. They belong only in GitHub secrets.

### 2. Create two GitHub environments

Repo → **Settings → Environments → New environment**. Create `sandbox` and `production`.

In each environment, add the following.

**Secrets** (Environment secrets → Add secret):

| Name | Value |
|---|---|
| `ZOHO_CLIENT_ID` | from step 1 |
| `ZOHO_CLIENT_SECRET` | from step 1 |
| `ZOHO_REFRESH_TOKEN` | from step 1 |

**Variables** (Environment variables → Add variable):

| Name | sandbox | production |
|---|---|---|
| `ZOHO_CRM_API_DOMAIN` | `https://sandbox.zohoapis.eu` | `https://www.zohoapis.eu` |
| `ZOHO_BOOKS_API_DOMAIN` | `https://www.zohoapis.eu` | `https://www.zohoapis.eu` |
| `ZOHO_BOOKS_ORG_ID` | ID of a **test** Books organisation | ID of your real Books organisation |
| `ZOHO_ACCOUNTS_URL` | `https://accounts.zoho.eu` | `https://accounts.zoho.eu` |

Books has no sandbox. Create a second, free test organisation in Books (top-right org menu → *New organisation*)
and use its ID for `sandbox`. The org ID is in Books → Settings → Organisation Profile.

On the **production** environment, tick **Required reviewers** and add yourself. A production run then waits
for you to approve it.

### 3. Create the CRM Sandbox

CRM → Setup → **Sandbox** → create one (Professional includes one). Create the Vehicles and Job Cards
modules there first (doc 01), because fields can only be added to modules that already exist.

## Running it

1. Edit `config/items.csv` with **your real prices** and `config/suppliers.csv` with your real suppliers,
   and **delete the example supplier row**. Commit. The Validate workflow checks them.
2. Actions → **SuperGear Motors Ltd** → Run workflow → target `sandbox`, step `all`, apply **unticked**.
   Read the job summary: it lists what *would* be created, plus the manual checklist.
3. Run again with **apply ticked**.
4. Finish the manual steps in the sandbox and run the end-to-end test in doc 06.
5. Repeat steps 2–4 with target `production`.

If a module is missing, its fields are reported as `blocked`. Create the module in CRM and run again.

## Running locally instead

```bash
pip install -r requirements.txt
export ZOHO_CLIENT_ID=... ZOHO_CLIENT_SECRET=... ZOHO_REFRESH_TOKEN=... ZOHO_BOOKS_ORG_ID=...
export ZOHO_CRM_API_DOMAIN=https://sandbox.zohoapis.eu   # leave unset for production
python -m zoho_setup all            # dry run
python -m zoho_setup all --apply
```

## Where the API limits are

Checked against Zoho's own OpenAPI files (https://github.com/zoho/crm-oas, v8.0), Sep 2026:
list views, workflow rules, field updates, email alerts, webhooks, layouts (PATCH) and module labels/profiles
have create/update APIs. **Blueprint setup, Deluge functions, buttons and hiding modules from the menu do not**,
so they stay on the manual checklist. Workflow rules that run a Deluge function also need the function
pasted by hand first.

## Relation to Zoho MCP

Zoho MCP (connected in the Claude app) is best for **day-to-day and one-off work**: entering paper
records from photos, asking questions about jobs and invoices, and drafting quotes. These workflows are for the
**repeatable configuration**: it's written down in this repo, reviewed, and can be rebuilt in a sandbox at any time.
Both use the same Zoho account and don't conflict.
