# 8. What Zoho's API can automate (research, 27 Sep 2026)

Source: Zoho's official CRM OpenAPI files, **github.com/zoho/crm-oas** (`v8.0/`, one folder per API area,
each with an OpenAPI file and worked examples). This is where the list views (`crm-views`) and the
reminder workflows (`crm-workflows`) in this repo come from. Other repositories in github.com/zoho were
not reviewed yet.

## Remaining manual steps, checked against the API

| Roadmap step | API in crm-oas v8.0? | How it's done here |
|---|---|---|
| P1.6 Saved lists | ✅ `POST /settings/custom_views` | `crm-views`, config/crm_views.yaml (8 lists) |
| P4.2 Service / NCT reminders (as call tasks) | ✅ `POST /settings/automation/tasks` + `POST /settings/automation/workflow_rules` | `crm-workflows`, config/crm_workflows.yaml |
| Chase uncollected cars / unpaid jobs | ✅ same (field-update trigger + scheduled action) | `crm-workflows` |
| P1.4 Block duplicate registrations/mobiles | ⚠️ `PATCH /settings/fields` has a `unique` flag for **custom** fields only; Registration (record name) and Mobile are system fields | Owner ticks "Do not allow duplicate values" in the layout editor |
| Email templates (car ready, service due, quote) | ❌ read-only (`GET /settings/email_templates`) | Owner pastes the texts below (Setup → Templates → Email) |
| P1.3 Blueprint | ❌ no endpoint | Owner builds it, Claude guides (doc 02) |
| P1.5 Deluge functions, P2.5 Create Quote button | ❌ no endpoint for functions or buttons | Owner pastes `deluge/*.dg` (doc 02 §2.2, doc 03 §3.5) |
| Webhooks (e.g. to WhatsApp or a booking site later) | ✅ `/settings/automation/webhooks` | Not needed yet |
| Field updates, email alerts inside rules | ✅ `/settings/automation/field_updates`, `email_notifications` | Candidates once email templates exist |

## Reminder workflows (`python -m zoho_setup crm-workflows`)

| Rule | Module | Trigger | Creates task |
|---|---|---|---|
| Service due in 14 days | Vehicles | 14 days before Next Service Due, Status = Active | "Service due: <reg>" (High) |
| NCT due in 30 days | Vehicles | 30 days before NCT Due, Status = Active | "NCT due: <reg>" |
| Ready but not collected | Job Cards | Stage → Ready, still Ready 2 days later | "Not collected yet: <job>" (High) |
| Collected but not paid | Job Cards | Stage → Collected, 3 days later, Payment Status not Paid/Account Customer | "Chase payment: <job>" (High) |

Tasks are free (no SMS/WhatsApp cost) and appear in CRM → Tasks and on the car/job record. When WhatsApp
is connected (P4.1) the same rules can send a message instead of, or as well as, creating a task.

**Before the first run:** the Zoho API client needs two extra scopes,
`ZohoCRM.settings.workflow_rules.ALL` and `ZohoCRM.settings.automation_actions.ALL` (doc 07 §1 lists the full set).
Generate a new code with the full scope list, swap it for a new refresh token, and replace the
`ZOHO_REFRESH_TOKEN` secret in the GitHub environment.

## Email templates to paste (CRM → Setup → Templates → Email → New, module Customers)

Insert the merge fields with the template editor's "Insert merge field" button, not by typing.

**Your car is ready**
> Subject: Your car is ready for collection – SuperGear Motors
>
> Hi {First Name},
> Good news: your car is ready for collection at SuperGear Motors, Ballygoran Road, Maynooth.
> We're open Monday to Friday. Your invoice will be sent separately and can be paid by card on collection or online.
> Thanks,
> SuperGear Motors · info@supergearmotors.ie

**Service due**
> Subject: Your car is due a service
>
> Hi {First Name},
> Our records show your car is due its service soon. Reply to this email or call us to book a time that suits you.
> Thanks, SuperGear Motors

**NCT due**
> Subject: NCT coming up – book a pre-NCT check
>
> Hi {First Name},
> Your car's NCT is coming up. We can do a pre-NCT check beforehand to fix anything that might fail. Reply or call us to book.
> Thanks, SuperGear Motors

Only send the Service/NCT emails to customers with **Marketing Consent** ticked.
