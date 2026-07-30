# Weekly Ops Status Pack

**AI-assisted weekly status for Business Operations — Excel / SharePoint / Jira in; leadership pack out. Friday via Power Automate or GitHub.**

[![Dashboard](https://img.shields.io/badge/Live-Demo-38bdf8)](https://raw.githack.com/rpriyaprakasm-bit/weekly-ops-status-pack/main/docs/dashboard.html)

---

## Summary

Business Operations teams often spend Friday mornings stitching status from spreadsheets, email, and ticketing tools. Numbers get out of date, actions lose owners and due dates, and leadership still asks the same questions: billability, what’s red, and what happens next week.

This project turns structured weekly inputs into a single **status pack and dashboard**:

1. **Collect** — Excel/CSV, SharePoint export, and/or Jira  
2. **Draft** — optional Grok summary (metrics stay from the data; narrative is assisted)  
3. **Publish** — HTML dashboard + JSON history  
4. **Notify** — optional Microsoft Teams webhook after each run  

**Triggers:** Power Automate on Friday, GitHub schedule, or manual workflow run.

**Dashboard includes:** business health and delivery RAG, 8 KPI tiles with week-over-week deltas, billability / portfolio RAG / action urgency charts, trend history, program table, full project list, projects at risk, overdue actions, filterable action items with source links, data-quality warnings, and print-friendly layout.

Sample data is embedded so the demo works without secrets. Replace `data/csv/` (or Excel) with live inputs for a real weekly cycle.

---

## Live demo

**→ [Open dashboard](https://raw.githack.com/rpriyaprakasm-bit/weekly-ops-status-pack/main/docs/dashboard.html)**

After GitHub Pages is enabled: `https://rpriyaprakasm-bit.github.io/weekly-ops-status-pack/dashboard.html`

---

## Features

| Feature | Detail |
|---------|--------|
| **Teams notify** | Secret `TEAMS_WEBHOOK_URL` → MessageCard after each successful run |
| **Weekly history / trends** | `data/history.json` + trend charts on the dashboard |
| **SharePoint list template** | [SHAREPOINT_LIST_TEMPLATE.md](./SHAREPOINT_LIST_TEMPLATE.md) — columns 1:1 with `data/csv/` |

Also: [INPUTS.md](./INPUTS.md) · [POWER_AUTOMATE.md](./POWER_AUTOMATE.md)

---

## Triggers

| Trigger | When |
|--------|------|
| Power Automate | Friday → `repository_dispatch` |
| GitHub schedule | Friday 14:00 UTC |
| Manual | Actions → Run workflow |

---

## Secrets

| Secret | Purpose |
|--------|--------|
| `XAI_API_KEY` | Grok narrative (optional for demo) |
| `TEAMS_WEBHOOK_URL` | Incoming webhook for Teams card |
| `JIRA_BASE_URL` / `JIRA_EMAIL` / `JIRA_API_TOKEN` | Optional Jira collect |

---

## License

MIT
