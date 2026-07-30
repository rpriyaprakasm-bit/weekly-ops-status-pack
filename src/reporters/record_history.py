"""
Append a weekly snapshot for trend charts.
Writes/updates data/history.json and docs/history.json (last 16 weeks).
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HISTORY = ROOT / "data" / "history.json"
PACK = ROOT / "data" / "status_pack.json"
UPDATES = ROOT / "data" / "workstream_updates.json"


def _load(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def snapshot_from_pack(pack: dict, updates: dict | None = None) -> dict:
    hc = (pack.get("headcount") or (updates or {}).get("headcount") or {})
    metrics = pack.get("metrics") or (updates or {}).get("metrics") or {}
    week = pack.get("week_ending") or pack.get("report_date") or ""
    return {
        "week_ending": week,
        "report_date": pack.get("report_date") or week,
        "overall_rag": pack.get("overall_rag"),
        "overall_business_health": pack.get("overall_business_health"),
        "billable_pct": hc.get("billable_pct"),
        "target_billable_pct": hc.get("target_billable_pct"),
        "bench": hc.get("bench"),
        "projects_at_risk": metrics.get("projects_at_risk")
        if metrics.get("projects_at_risk") is not None
        else len(pack.get("projects_at_risk") or []),
        "open_actions": metrics.get("open_actions")
        if metrics.get("open_actions") is not None
        else len(pack.get("action_items") or []),
        "overdue_actions": metrics.get("overdue_actions", 0),
    }


def record(max_weeks: int = 16) -> Path:
    pack = _load(PACK)
    if not pack:
        print("No status_pack.json — skip history")
        return HISTORY

    updates = _load(UPDATES) or {}
    # Prefer headcount from updates if pack omitted it
    if not pack.get("headcount") and updates.get("headcount"):
        pack = dict(pack)
        pack["headcount"] = updates["headcount"]
    if not pack.get("metrics") and updates.get("metrics"):
        pack = dict(pack)
        pack["metrics"] = updates["metrics"]

    snap = snapshot_from_pack(pack, updates)
    history = _load(HISTORY) or {"weeks": []}
    weeks = history.get("weeks") or []

    # Upsert by week_ending
    weeks = [w for w in weeks if w.get("week_ending") != snap["week_ending"]]
    weeks.append(snap)
    weeks.sort(key=lambda w: w.get("week_ending") or "")
    weeks = weeks[-max_weeks:]

    history = {"weeks": weeks, "updated_at": snap.get("report_date")}
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    HISTORY.write_text(json.dumps(history, indent=2), encoding="utf-8")

    docs = ROOT / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "history.json").write_text(json.dumps(history, indent=2), encoding="utf-8")
    print(f"History: {len(weeks)} weeks → {HISTORY}")
    return HISTORY


if __name__ == "__main__":
    record()
