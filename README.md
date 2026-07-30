# Weekly Ops Status Pack

**AI-assisted weekly status for Business Operations — Excel / SharePoint / Jira in; leadership pack out. Friday via Power Automate or GitHub.**

[![Dashboard](https://img.shields.io/badge/Live-Demo-38bdf8)](https://raw.githack.com/rpriyaprakasm-bit/weekly-ops-status-pack/main/docs/status-v2.html)

---

## Live demo

**→ [Open dashboard](https://raw.githack.com/rpriyaprakasm-bit/weekly-ops-status-pack/main/docs/status-v2.html)**

8 KPIs · billability / RAG / actions graphs · **week-over-week trends** · programs · at-risk projects · dated actions.

---

## What’s included (upgrades)

| Upgrade | How |
|---------|-----|
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
