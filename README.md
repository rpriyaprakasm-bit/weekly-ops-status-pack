# Weekly Ops Status Pack

**AI-assisted weekly status for Business Operations — from Excel, SharePoint, or Jira to a leadership-ready pack.**

Inputs are structured (not free-form chat). Grok drafts the executive summary; humans still own the numbers and the send.

[![Dashboard](https://img.shields.io/badge/Live-Demo-38bdf8)](https://raw.githack.com/rpriyaprakasm-bit/weekly-ops-status-pack/main/docs/status-v2.html)
[![Grok](https://img.shields.io/badge/Powered%20by-Grok-000000?logo=x&logoColor=white)](https://x.ai)

---

## Live demo

**→ [Open status pack](https://raw.githack.com/rpriyaprakasm-bit/weekly-ops-status-pack/main/docs/status-v2.html)**

8 KPI tiles · billability graph · portfolio RAG · actions by urgency · programs · projects at risk · dated action items.

---

## How inputs work

| Source | How |
|--------|-----|
| **Excel** | `data/ops_status_input.xlsx` or `data/csv/*.csv` |
| **SharePoint** | List or library Excel → export/sync into `data/` (same columns) |
| **Jira** | REST API via secrets + `data/jira_config.json` |

**Details:** [INPUTS.md](./INPUTS.md)

```text
Excel / SharePoint export / Jira
        ↓  collectors
workstream_updates.json
        ↓  Grok (optional)
status pack JSON + Markdown
        ↓
HTML dashboard
```

Manual workflow run lets you pick: `excel` · `jira` · `excel+jira`.

---

## Role fit

**Business Operations** — weekly portfolio, billability, dated actions.  
**AI enablement** — governed “collect → summarize → publish” pattern reusable with Power Automate / n8n.

---

## Quick start

1. Edit `data/csv/` (or add Excel under `data/ops_status_input.xlsx`).
2. Optional: set `XAI_API_KEY` for AI narrative; without it, use the embedded demo dashboard.
3. Optional Jira: `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`.
4. **Actions → Weekly Ops Status Pack → Run workflow**.

Local collect test:

```bash
pip install openpyxl openai
python -m src.collectors.run_collect
```

---

## Repo layout

```text
data/csv/              SharePoint/Excel-friendly tables
data/jira_config.json  JQL + label mapping
src/collectors/        excel_collector, jira_collector
src/analyzers/         Grok status pack builder
docs/status-v2.html    Dashboard
INPUTS.md              Full input guide
```

---

## Related

- [AI Project Risk Radar](https://github.com/rpriyaprakasm-bit/ai-project-risk-radar)

---

## License

MIT
