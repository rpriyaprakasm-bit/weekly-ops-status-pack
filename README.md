# Weekly Ops Status Pack

**AI-assisted weekly status for multi-workstream operations — less manual reporting, clearer leadership view.**

Business Operations teams often spend hours every week collecting updates across workstreams, rewriting them into a consistent format, and chasing missing inputs. This project shows a practical pattern: structured inputs in → LLM summary out → one page leaders can scan in under five minutes.

Same automation idea as [AI Project Risk Radar](https://github.com/rpriyaprakasm-bit/ai-project-risk-radar), focused on **recurring status reporting** instead of risk detection.

[![Grok](https://img.shields.io/badge/Powered%20by-Grok-000000?logo=x&logoColor=white)](https://x.ai)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-2088FF?logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![Dashboard](https://img.shields.io/badge/Live-Demo-38bdf8)](https://raw.githack.com/rpriyaprakasm-bit/weekly-ops-status-pack/main/docs/index.html)

---

## Why this exists

Typical weekly reporting pain:

- 8–12 workstreams, each with a different update style
- Status decks rebuilt by hand every Friday
- Leaders still ask “are we on track?” because the pack is late or inconsistent

**Weekly Ops Status Pack** standardizes the first draft:

1. Read structured workstream updates (JSON / form-style input)
2. Ask Grok to produce a consistent executive summary + per-stream RAG status
3. Publish a one-page HTML pack (and optional Markdown for email/Slack)

Humans still own the numbers and the final send. AI handles structure, tone, and the “so what?” summary.

---

## Live demo

**→ [Open status pack dashboard](https://raw.githack.com/rpriyaprakasm-bit/weekly-ops-status-pack/main/docs/index.html)**

Sample week includes multiple workstreams with mixed On Track / At Risk / Blocked status, key wins, risks, and asks for leadership.

---

## What you get each run

| Output | Purpose |
|--------|--------|
| Executive summary (5–8 lines) | Leadership skim |
| Workstream table | RAG status + one-line update |
| Top risks & asks | Escalation list |
| Wins this week | Positive signal for morale and continuity |
| JSON + Markdown | Reuse in email, Confluence, or Power Automate |

---

## How this maps to real roles

**Business Operations**  
Directly supports multi-workstream weekly reporting, less copy-paste, consistent format across countries or teams.

**AI Value Hub / Enablement**  
Reusable “collect → summarize → publish” pattern — same shape as intake digests, risk scans, or meeting action packs. Good demo of governed AI for recurring ops work.

**Tools shown:** structured prompting, Grok, GitHub Actions, dashboard reporting — complementary to Power Automate / n8n / Copilot workflows used in enterprise ops.

---

## Quick start

### Option A — View the demo only
Open the [live dashboard](https://raw.githack.com/rpriyaprakasm-bit/weekly-ops-status-pack/main/docs/index.html). No keys required.

### Option B — Run with Grok

1. **Settings → Secrets → Actions** → `XAI_API_KEY` from [console.x.ai](https://console.x.ai)
2. Edit `data/workstream_updates.json` with your streams (or keep sample data)
3. **Actions → Weekly Ops Status Pack → Run workflow**

The workflow writes `docs/status_pack.json` and refreshes the dashboard data path.

---

## Sample input shape

```json
{
  "week_ending": "2026-07-25",
  "program": "Platform Operations",
  "workstreams": [
    {
      "name": "Data Centre Migration",
      "owner": "A. Chen",
      "rag": "At Risk",
      "update": "Cutover rehearsal delayed; dependency on network window.",
      "wins": ["Inventory freeze completed"],
      "risks": ["Vendor change window still unconfirmed"],
      "asks": ["Approve weekend change slot by Wednesday"]
    }
  ]
}
```

---

## Repo layout

```text
.github/workflows/     Scheduled + manual status run
data/                  Sample workstream updates
docs/                  Dashboard + published pack JSON
prompts/               Status summary prompt
src/
  analyzers/           Grok status pack builder
  reporters/           Write Markdown + JSON
```

---

## Design choices

- **AI drafts; humans approve** — no auto-send to leadership without review
- **Fixed sections every week** — summary, RAG table, risks, asks, wins — so readers learn the layout once
- **Works offline for portfolio** — rich sample data so the demo never looks empty
- **Composable** — same pattern as Risk Radar; swap the prompt and input schema for other ops digests

---

## Related

- [AI Project Risk Radar](https://github.com/rpriyaprakasm-bit/ai-project-risk-radar) — early-warning risk scan + category dashboard

---

## License

MIT
