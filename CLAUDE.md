# Super Gears Motors: Zoho CRM + Books build

Irish motor garage moving from paper to Zoho CRM + Zoho Books. Claude builds through the Zoho CRM / Zoho Books MCP connectors
and guides the owner through UI-only steps.

**Start every session by reading `docs/BUILD_LOG.md` → "RESUME HERE"**, then check live state with the connectors before acting.
Master plan: `docs/ROADMAP.md` (mirrored as numbered Tasks P1.0–P5.1 in Zoho CRM → Tasks).

Key IDs: CRM org 1042240000000023712 (EU); Books org 20119876326; VAT 13.5% 1426684000000064001, 23% 1426684000000065001, 0% 1426684000000063002.
Modules: Contacts (label "Customers"), Accounts ("Fleet Accounts"), Vehicles, Job_Cards (+ subform Job_Lines).

Rules: look before changing; confirm before deleting or anything involving money; verify API names after creating fields;
keep `config/` and `docs/BUILD_LOG.md` in sync with what's live; never commit customer data.
Checks: `python -m pytest -q` and `python -m zoho_setup validate`.
