# Weekly Ops Status Pack

**AI-assisted weekly status for Business Operations — program health, projects at risk, action items, and resource billability.**

Built for the kind of Friday review that Business Operations and delivery leadership actually run: not network cutovers, but **portfolio health, billable utilization, dated actions, and what needs a decision this week**.

Companion to [AI Project Risk Radar](https://github.com/rpriyaprakasm-bit/ai-project-risk-radar).

[![Grok](https://img.shields.io/badge/Powered%20by-Grok-000000?logo=x&logoColor=white)](https://x.ai)
[![Dashboard](https://img.shields.io/badge/Live-Demo-38bdf8)](https://raw.githack.com/rpriyaprakasm-bit/weekly-ops-status-pack/main/docs/index.html)

---

## Live demo

**→ [Open status pack](https://raw.githack.com/rpriyaprakasm-bit/weekly-ops-status-pack/main/docs/index.html)**

Sample week includes:

| Section | What it shows |
|--------|----------------|
| **Business health + Delivery RAG** | Watch / At Risk posture for leadership |
| **Billability KPIs** | Billable % vs target, billable vs non-billable headcount |
| **Program status** | Client Delivery, AI Enablement, Finance Close — with milestone dates |
| **Projects at risk** | Named projects, owners, target end dates, billable flag |
| **Action items** | ID, owner, **due date**, priority, status |
| **Wins + next-week focus** | What moved; what is dated for next week |

---

## Why this exists

Business Operations reporting pain:

- Updates arrive in different formats across programs
- Action items lose owners and dates by the time they hit the deck
- Leadership asks about **billability** and **which projects are at risk** — not only a green/amber/red logo
- Analysts spend hours assembling the same pack every week

This project drafts a **consistent one-pager** from structured inputs so the review starts from a shared picture.

---

## Role fit

**Business Operations** — weekly portfolio and resource view, dated actions, utilization signal.  
**AI Value Hub / Enablement** — same “collect → summarize → publish” pattern as other governed AI ops workflows.  
**Program / delivery support** — program RAG, projects at risk, milestone dates in one place.

---

## Quick start

- **Demo only:** open the live link (no API key).
- **With Grok:** add `XAI_API_KEY` under Actions secrets → run **Weekly Ops Status Pack**.
- Edit `data/workstream_updates.json` for your programs, projects, headcount, and action items.

---

## Input highlights

Structured JSON supports:

- `report_date` / `period` / `week_ending`
- `overall_business_health` + `overall_rag`
- `headcount` (billable, non-billable, % vs target)
- `programs[]` with milestone dates
- `projects[]` with target end + billable flag
- `action_items[]` with **owner, due, priority, status**

---

## Design choices

- **Ops language, not infra language** — delivery accounts, enablement, finance close, utilization
- **Dates on actions and milestones** — a status pack without due dates is not actionable
- **Billability visible on the first screen** — standard BO leadership question
- **AI drafts; humans send** — no silent auto-email to executives

---

## Related

- [AI Project Risk Radar](https://github.com/rpriyaprakasm-bit/ai-project-risk-radar) — early-warning risk categories and dashboard

---

## License

MIT
