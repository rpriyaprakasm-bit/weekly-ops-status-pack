"""
Post weekly pack summary to Microsoft Teams via Incoming Webhook.

Secret: TEAMS_WEBHOOK_URL
If unset, exits 0 without failing the workflow.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "data" / "status_pack.json"
DASHBOARD = (
    "https://raw.githack.com/rpriyaprakasm-bit/weekly-ops-status-pack/main/docs/status-v2.html"
)


def notify() -> None:
    url = (os.environ.get("TEAMS_WEBHOOK_URL") or "").strip()
    if not url:
        print("TEAMS_WEBHOOK_URL not set — skip Teams notify")
        return

    if not PACK.exists():
        print("No status_pack.json — skip Teams notify", file=sys.stderr)
        return

    pack = json.loads(PACK.read_text(encoding="utf-8"))
    week = pack.get("week_ending") or pack.get("report_date") or ""
    health = pack.get("overall_business_health") or "—"
    rag = pack.get("overall_rag") or "—"
    summary = (pack.get("executive_summary") or "")[:900]
    hc = pack.get("headcount") or {}
    billable = hc.get("billable_pct")
    target = hc.get("target_billable_pct")
    at_risk = len(pack.get("projects_at_risk") or [])
    open_actions = len(
        [
            a
            for a in (pack.get("action_items") or [])
            if (a.get("status") or "").lower() not in ("done", "closed")
        ]
    )

    facts = [
        {"name": "Business health", "value": str(health)},
        {"name": "Delivery RAG", "value": str(rag)},
        {
            "name": "Billable %",
            "value": f"{billable}% (target {target}%)" if billable is not None else "—",
        },
        {"name": "Projects at risk", "value": str(at_risk)},
        {"name": "Open actions", "value": str(open_actions)},
    ]

    card = {
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "themeColor": "EA580C" if "risk" in str(rag).lower() else "16A34A",
        "summary": f"Weekly Ops Status — {week}",
        "sections": [
            {
                "activityTitle": f"Weekly Ops Status Pack — week ending {week}",
                "activitySubtitle": pack.get("program") or "Business Operations",
                "facts": facts,
                "text": summary,
                "markdown": True,
            }
        ],
        "potentialAction": [
            {
                "@type": "OpenUri",
                "name": "Open dashboard",
                "targets": [{"os": "default", "uri": DASHBOARD}],
            }
        ],
    }

    data = json.dumps(card).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"Teams notify status: {resp.status}")
    except Exception as e:
        print(f"Teams notify failed: {e}", file=sys.stderr)
        # Do not fail the whole job on webhook issues
        return


if __name__ == "__main__":
    notify()
