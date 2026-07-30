# Inputs: Excel · SharePoint · Jira

The dashboard does **not** invent numbers. Every weekly run starts from structured inputs.

## Option 1 — Excel (default)

1. Copy the column layout from `data/csv/*.csv` into an Excel workbook (sheets: **Header**, **Headcount**, **Programs**, **Projects**, **ActionItems**, **Wins**).
2. Save as `data/ops_status_input.xlsx` **or** keep editing the CSV files under `data/csv/`.
3. Run **Actions → Weekly Ops Status Pack** with `input_source = excel`.

Blue input cells / yellow highlights in a full `.xlsx` template are optional; CSV is enough for the collector.

**RAG values:** `On Track` | `At Risk` | `Blocked`  
**Dates:** `YYYY-MM-DD`  
**Billable:** `Yes` / `No`

---

## Option 2 — SharePoint

SharePoint is the collaboration front-end; this repo still reads **Excel or CSV**.

### Pattern A — Excel in a document library
1. Store `ops_status_input.xlsx` in a SharePoint library (e.g. *Business Ops / Weekly Status*).
2. Owners update the file during the week.
3. Before Friday run: download latest → commit to `data/ops_status_input.xlsx`, **or** use Power Automate to push the file into the repo / an API.

### Pattern B — SharePoint List → Export
1. Create a list with the same columns as `data/csv/Projects.csv` (and lists for actions / programs).
2. **Export to Excel** or use **Power Automate: List → Create CSV** into `data/csv/`.
3. Run the workflow with `input_source = excel` (CSV folder is used when no xlsx is present).

### Pattern C — Power Automate (enterprise)
```text
SharePoint list item created/updated
  → Compose JSON in workstream_updates shape
  → HTTP to Grok / or commit to GitHub
  → Post summary to Teams
```
Same data contract; different transport.

---

## Option 3 — Jira

1. Repo **Settings → Secrets**:
   - `JIRA_BASE_URL` — `https://yourorg.atlassian.net`
   - `JIRA_EMAIL`
   - `JIRA_API_TOKEN`
2. Edit `data/jira_config.json` (JQL, labels for action items / billable).
3. Run workflow with `input_source = jira` or `excel+jira`.

**excel+jira:** headcount + programs stay from Excel/CSV; projects and actions are enriched from Jira.

**Mapping (default):**
| Jira | Status pack |
|------|-------------|
| Issue summary + key | Project or action name |
| Status name | RAG heuristic (Blocked / At Risk / On Track) |
| Assignee | Owner |
| Due date | target_end / action due |
| Label `action-item` | Action item row |
| Label `billable` | Billable flag |

Tune JQL so only delivery-relevant issues appear in the weekly pack.

---

## What still needs a human

- Billability % and bench (usually from resource/finance sheet, not Jira)
- Overall business health label
- Narrative wins and “focus next week” (Grok drafts; you approve)
- Final send to leadership

---

## Quick test without secrets

```bash
pip install openpyxl
python -m src.collectors.run_collect   # reads data/csv
# inspect data/workstream_updates.json
```
