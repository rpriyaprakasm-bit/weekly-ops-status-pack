# SharePoint list template (1:1 with `data/csv/`)

Create these lists (or one Excel in a library with matching sheets). Column **internal names** can differ; **display names** below match the CSV headers the collector expects after export.

Export → save under `data/csv/` with the filenames shown, then run the Friday pack (`input_source=excel`).

---

## List 1 — `OpsStatus_Header` → `Header.csv`

| Column (display) | Type | Required | Example | Notes |
|------------------|------|----------|---------|--------|
| Field | Single line of text | Yes | `week_ending` | Use one row per field name |
| Value | Single line of text | Yes | `2026-07-25` | |

**Rows to maintain each week**

| Field | Value example |
|-------|----------------|
| week_ending | 2026-07-25 |
| report_date | 2026-07-25 |
| period | Week of 2026-07-21 to 2026-07-25 |
| program | Business Operations — Delivery & Enablement |
| prepared_for | Weekly Business Operations Review |
| overall_business_health | Good \| Watch \| Poor |
| overall_rag | On Track \| At Risk \| Blocked |

Export columns: `Field,Value` → `data/csv/Header.csv`

---

## List 2 — `OpsStatus_Headcount` → `Headcount.csv`

| Column | Type | Required | Example |
|--------|------|----------|--------|
| total | Number | Yes | 28 |
| billable | Number | Yes | 22 |
| non_billable | Number | Yes | 6 |
| billable_pct | Number | Yes | 79 |
| target_billable_pct | Number | Yes | 85 |
| bench | Number | No | 3 |
| notes | Multiple lines | No | Below target; 3 on bench |

One item per week (or edit the single item weekly).  
Export → `data/csv/Headcount.csv`

---

## List 3 — `OpsStatus_Programs` → `Programs.csv`

| Column | Type | Required | Example |
|--------|------|----------|--------|
| name | Single line | Yes | Client Delivery Portfolio |
| owner | Person or text | Yes | P. Sharma |
| rag | Choice | Yes | On Track, At Risk, Blocked |
| next_milestone | Date or text | No | 2026-08-15 |
| update | Multiple lines | Yes | Revenue on plan; two accounts at risk |

Export → `data/csv/Programs.csv`

---

## List 4 — `OpsStatus_Projects` → `Projects.csv`

| Column | Type | Required | Example |
|--------|------|----------|--------|
| name | Single line | Yes | North Region Account — Q3 |
| program | Single line / lookup | Yes | Client Delivery Portfolio |
| owner | Person or text | Yes | A. Chen |
| rag | Choice | Yes | On Track, At Risk, Blocked |
| start | Date | No | 2026-05-01 |
| target_end | Date | No | 2026-09-30 |
| update | Multiple lines | Yes | M3 slipped 8 days |
| billable | Choice | Yes | Yes, No |

Export → `data/csv/Projects.csv`

---

## List 5 — `OpsStatus_ActionItems` → `ActionItems.csv`

| Column | Type | Required | Example |
|--------|------|----------|--------|
| id | Single line | Yes | AI-01 |
| action | Multiple lines | Yes | Confirm UAT fix plan |
| owner | Person or text | Yes | A. Chen |
| due | Date | Yes | 2026-07-29 |
| priority | Choice | Yes | High, Medium, Low |
| status | Choice | Yes | Open, Scheduled, Done, Closed |

Export → `data/csv/ActionItems.csv`

---

## List 6 — `OpsStatus_Wins` → `Wins.csv`

| Column | Type | Required | Example |
|--------|------|----------|--------|
| win | Multiple lines | Yes | 3 teams trained on status automation |

Export → `data/csv/Wins.csv`

---

## Power Automate export pattern (Friday)

1. **Recurrence** — Friday morning  
2. **SharePoint — Get items** for each list (or get Excel file)  
3. **Select / Create CSV table** with the exact headers above  
4. **Create file** in GitHub (via HTTP) or OneDrive path your process commits from  
5. **HTTP repository_dispatch** — `event_type: weekly-ops-status`  
6. Optional: after delay, Teams message with dashboard link  

See [POWER_AUTOMATE.md](./POWER_AUTOMATE.md).

---

## Permissions tip

- **Contribute** for workstream leads on Programs / Projects / ActionItems / Wins  
- **Restrict** Header + Headcount to Business Operations analysts (billability is sensitive)
