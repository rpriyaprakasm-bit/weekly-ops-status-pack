# Weekly Ops Status Pack

**AI-assisted weekly status for Business Operations — Excel, SharePoint, or Jira in; leadership pack out. Trigger from GitHub schedule or Power Automate on Friday.**

[![Dashboard](https://img.shields.io/badge/Live-Demo-38bdf8)](https://raw.githack.com/rpriyaprakasm-bit/weekly-ops-status-pack/main/docs/status-v2.html)
[![Grok](https://img.shields.io/badge/Powered%20by-Grok-000000?logo=x&logoColor=white)](https://x.ai)

---

## Live demo

**→ [Open status pack](https://raw.githack.com/rpriyaprakasm-bit/weekly-ops-status-pack/main/docs/status-v2.html)**

---

## Triggers

| Trigger | When |
|--------|------|
| **Power Automate** (recommended for BO) | Friday recurrence → HTTP `repository_dispatch` |
| **GitHub schedule** | Cron Friday 14:00 UTC |
| **Manual** | Actions tab → Run workflow |

**Power Automate setup:** [POWER_AUTOMATE.md](./POWER_AUTOMATE.md)

```text
Friday (Power Automate)
  → optional SharePoint/Excel refresh
  → POST repository_dispatch (event: weekly-ops-status)
  → GitHub Action: collect → Grok → dashboard
  → optional Teams notification
```

---

## Inputs

| Source | How |
|--------|-----|
| **Excel / CSV** | `data/csv/*` or `data/ops_status_input.xlsx` |
| **SharePoint** | List/library → export or sync into `data/` |
| **Jira** | API secrets + `data/jira_config.json` |

Full guide: [INPUTS.md](./INPUTS.md)

---

## Quick start

1. Put weekly numbers in `data/csv/` (or Excel).
2. Add secrets as needed: `XAI_API_KEY`, optional `JIRA_*`.
3. Either:
   - Build the **Friday Power Automate** flow ([guide](./POWER_AUTOMATE.md)), or
   - **Actions → Weekly Ops Status Pack → Run workflow**

---

## Role fit

**Business Operations** — Friday pack without manual copy-paste.  
**AI / automation enablement** — Power Automate + GitHub Actions + LLM, governed and repeatable.

---

## Repo layout

```text
POWER_AUTOMATE.md      Friday flow + HTTP dispatch
INPUTS.md              Excel / SharePoint / Jira
data/csv/              Editable input tables
src/collectors/        Excel + Jira collectors
.github/workflows/     schedule + workflow_dispatch + repository_dispatch
docs/status-v2.html    Dashboard
```

---

## Related

- [AI Project Risk Radar](https://github.com/rpriyaprakasm-bit/ai-project-risk-radar)

---

## License

MIT
