"""
Collect delivery signals from Jira Cloud REST API.

Secrets (GitHub Actions):
  JIRA_BASE_URL   e.g. https://yourorg.atlassian.net
  JIRA_EMAIL
  JIRA_API_TOKEN

Config: data/jira_config.json (JQL, field names)

Maps issues → projects / action items shape used by the status pack.
Does not replace headcount (still from Excel/CSV) — merges when both run.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "data" / "jira_config.json"


def _load_config() -> dict:
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    return {
        "jql": "status != Done AND updated >= -14d ORDER BY priority DESC",
        "max_results": 50,
    }


def _jira_search(base: str, email: str, token: str, jql: str, max_results: int = 50) -> list:
    auth = __import__("base64").b64encode(f"{email}:{token}".encode()).decode()
    params = urlencode({
        "jql": jql,
        "maxResults": max_results,
        "fields": "summary,status,assignee,priority,duedate,labels,issuetype,updated",
    })
    url = f"{base.rstrip('/')}/rest/api/3/search?{params}"
    req = Request(url, headers={
        "Authorization": f"Basic {auth}",
        "Accept": "application/json",
    })
    with urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode())
    return data.get("issues", [])


def collect() -> dict:
    base = os.environ.get("JIRA_BASE_URL", "").strip()
    email = os.environ.get("JIRA_EMAIL", "").strip()
    token = os.environ.get("JIRA_API_TOKEN", "").strip()
    if not (base and email and token):
        print("Jira secrets not set — skipping Jira collector", file=sys.stderr)
        return {}

    cfg = _load_config()
    jql = cfg.get("jql") or "status != Done ORDER BY priority DESC"
    max_results = int(cfg.get("max_results") or 50)
    print(f"Jira search: {jql}")
    issues = _jira_search(base, email, token, jql, max_results)

    projects = []
    actions = []
    action_label = (cfg.get("action_label") or "action-item").lower()
    billable_label = (cfg.get("billable_label") or "billable").lower()

    for issue in issues:
        key = issue.get("key", "")
        fields = issue.get("fields") or {}
        summary = fields.get("summary") or ""
        status = ((fields.get("status") or {}).get("name") or "").lower()
        assignee = ((fields.get("assignee") or {}).get("displayName") or "Unassigned")
        priority = ((fields.get("priority") or {}).get("name") or "Medium")
        due = fields.get("duedate") or ""
        labels = [str(x).lower() for x in (fields.get("labels") or [])]

        if "block" in status:
            rag = "Blocked"
        elif any(x in status for x in ("progress", "review")):
            rag = "On Track"
        elif any(x in status for x in ("impediment", "hold", "wait")):
            rag = "At Risk"
        else:
            rag = "On Track"

        if action_label in labels or "action" in (fields.get("issuetype") or {}).get("name", "").lower():
            actions.append({
                "id": key,
                "action": summary,
                "owner": assignee,
                "due": due,
                "priority": "High" if "high" in priority.lower() or "highest" in priority.lower() else "Medium",
                "status": "Open" if status not in ("done", "closed") else "Done",
            })
        else:
            projects.append({
                "name": f"{key} {summary}".strip(),
                "program": "Jira delivery",
                "owner": assignee,
                "rag": rag,
                "start": "",
                "target_end": due,
                "update": f"Status: {(fields.get('status') or {}).get('name', '')}",
                "billable": billable_label in labels,
            })

    at_risk = [p for p in projects if p["rag"] in ("At Risk", "Blocked")]
    return {
        "source": "jira",
        "projects": projects,
        "projects_at_risk": [
            {
                "name": p["name"],
                "owner": p["owner"],
                "rag": p["rag"],
                "target_end": p.get("target_end", ""),
                "summary_line": p.get("update", ""),
                "billable": p.get("billable", False),
            }
            for p in at_risk
        ],
        "action_items": actions,
        "metrics": {
            "active_projects": len(projects),
            "projects_at_risk": len(at_risk),
            "open_actions": len(actions),
        },
    }


def merge_with_base(base: dict, jira: dict) -> dict:
    if not jira:
        return base
    out = dict(base)
    # Prefer Excel headcount/programs; enrich projects & actions from Jira when present
    if jira.get("projects"):
        out["projects"] = jira["projects"]
        out["projects_at_risk"] = jira.get("projects_at_risk") or []
    if jira.get("action_items"):
        # Merge by id
        by_id = {a["id"]: a for a in out.get("action_items") or [] if a.get("id")}
        for a in jira["action_items"]:
            by_id[a["id"]] = a
        out["action_items"] = list(by_id.values())
    return out


if __name__ == "__main__":
    result = collect()
    print(json.dumps(result, indent=2)[:2000])
