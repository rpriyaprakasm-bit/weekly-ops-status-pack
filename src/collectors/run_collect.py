"""
Entry: collect from Excel/CSV and optionally merge Jira, write workstream_updates.json

Env:
  INPUT_SOURCE=excel|csv|jira|excel+jira  (default excel)
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.collectors import excel_collector, jira_collector


def main():
    source = (os.environ.get("INPUT_SOURCE") or "excel").lower().strip()
    print(f"INPUT_SOURCE={source}")

    base = {}
    if source in ("excel", "csv", "excel+jira", "csv+jira"):
        base = excel_collector.collect()
    elif source == "jira":
        base = {
            "week_ending": "",
            "report_date": "",
            "period": "",
            "program": "Business Operations",
            "overall_business_health": "Watch",
            "overall_rag": "At Risk",
            "headcount": {},
            "programs": [],
            "projects": [],
            "projects_at_risk": [],
            "action_items": [],
            "wins": [],
            "metrics": {},
        }

    if "jira" in source or source == "jira":
        jira = jira_collector.collect()
        base = jira_collector.merge_with_base(base, jira)

    if not base.get("projects") and not base.get("programs"):
        print("WARNING: no programs/projects collected — check data/csv or Excel", file=sys.stderr)

    dest = excel_collector.write_workstream_json(base)
    print(f"Ready for analyzer: {dest}")


if __name__ == "__main__":
    main()
