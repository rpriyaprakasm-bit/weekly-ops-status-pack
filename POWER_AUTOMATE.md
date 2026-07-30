# Power Automate — Friday trigger

Use **Power Automate** to kick off this status pack every Friday (and optionally pull SharePoint/Excel first).

The flow does **not** replace GitHub Actions. It **starts** the pack on a business schedule and can notify Teams when done.

```text
Friday recurrence (Power Automate)
    → optional: export SharePoint list / Excel → update repo or file
    → HTTP POST repository_dispatch  →  GitHub Action runs collect → Grok → dashboard
    → optional: post “pack ready” to Teams
```

---

## Prerequisites

1. GitHub **Personal Access Token** (classic) with `repo` scope  
   — or a fine-grained token with **Contents: Read/Write** + **Metadata** on this repo.
2. Store the token in Power Automate as a **secret** (not in plain text in the flow definition).
3. Repo secrets already set if you use AI/Jira: `XAI_API_KEY`, optional `JIRA_*`.

---

## Flow A — Friday trigger only (minimum)

### 1. Create flow
- **Automated cloud flow** or **Scheduled cloud flow**
- Name: `Weekly Ops Status Pack — Friday`

### 2. Trigger: Recurrence
| Setting | Value |
|--------|--------|
| Interval | 1 |
| Frequency | Week |
| On these days | **Friday** |
| At these hours | 9 (or your ops review time) |
| Time zone | Eastern Time (or local) |

### 3. Action: HTTP

| Setting | Value |
|--------|--------|
| Method | **POST** |
| URI | `https://api.github.com/repos/rpriyaprakasm-bit/weekly-ops-status-pack/dispatches` |
| Headers | See below |
| Body | See below |

**Headers**

```text
Accept: application/vnd.github+json
Authorization: Bearer <YOUR_GITHUB_PAT>
X-GitHub-Api-Version: 2022-11-28
Content-Type: application/json
```

**Body**

```json
{
  "event_type": "weekly-ops-status",
  "client_payload": {
    "input_source": "excel",
    "triggered_by": "power-automate",
    "week": "@{formatDateTime(utcNow(), 'yyyy-MM-dd')}"
  }
}
```

`input_source` options: `excel` | `jira` | `excel+jira`

### 4. (Optional) Condition on HTTP status
- If status code = **204** → success (GitHub accepted the dispatch)
- Else → post failure to Teams / email

### 5. (Optional) Delay + Teams message
- **Delay** 3–5 minutes (pack usually finishes quickly)
- **Post message in a chat or channel**:

```text
Weekly Ops Status Pack has been triggered for @{formatDateTime(utcNow(), 'yyyy-MM-dd')}.
Dashboard: https://raw.githack.com/rpriyaprakasm-bit/weekly-ops-status-pack/main/docs/dashboard.html
Actions: https://github.com/rpriyaprakasm-bit/weekly-ops-status-pack/actions
```

---

## Flow B — SharePoint → then trigger

1. **Recurrence** — Friday morning  
2. **SharePoint — Get items** (or **List folder** / get Excel file)  
3. **Create CSV table** or **Update file** in a location the repo can read  
4. **HTTP repository_dispatch** (same as Flow A) with `input_source: excel`  
5. **Teams** — inputs refreshed; status pack running  

Lighter cadence:

```text
Friday 8:30  Reminder: update the ops Excel / list
Friday 9:30  Power Automate dispatch → GitHub builds the pack
Friday 10:00 Ops review uses the dashboard
```

---

## Flow C — After pack: notify with summary

1. HTTP GET  
   `https://raw.githubusercontent.com/rpriyaprakasm-bit/weekly-ops-status-pack/main/docs/status_pack.json`  
2. Parse JSON → post **Executive Summary** + **overall_rag** to Teams.

```text
**Weekly Ops Status**
Health: @{body('Parse_JSON')?['overall_business_health']}
RAG: @{body('Parse_JSON')?['overall_rag']}

@{body('Parse_JSON')?['executive_summary']}

Dashboard: https://raw.githack.com/rpriyaprakasm-bit/weekly-ops-status-pack/main/docs/dashboard.html
```

(Add a short **Delay** after dispatch so the Action can finish and push.)

Alternatively use repo secret `TEAMS_WEBHOOK_URL` — the GitHub Action posts a MessageCard automatically after publish.

---

## Test without waiting for Friday

1. In Power Automate: **Test → Manually**  
2. Or:

```bash
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR_PAT" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/rpriyaprakasm-bit/weekly-ops-status-pack/dispatches \
  -d '{"event_type":"weekly-ops-status","client_payload":{"input_source":"excel"}}'
```

3. Check **Actions** — event `repository_dispatch`.

---

## Security notes

- Prefer a **dedicated PAT** limited to this repo; rotate if leaked.
- Do not commit the PAT or paste it into public screenshots.
- In enterprise tenants, prefer a service account + Key Vault if required by policy.
