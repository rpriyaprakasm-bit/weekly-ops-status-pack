"""
Build a weekly ops status pack with Grok (xAI).
"""

import json
import os
import re
import sys
from pathlib import Path

from openai import OpenAI


def build_pack():
    data_path = Path("data/workstream_updates.json")
    if not data_path.exists():
        print("ERROR: data/workstream_updates.json not found", file=sys.stderr)
        sys.exit(1)

    updates = json.loads(data_path.read_text())
    prompt_path = Path("prompts/weekly_status.md")
    system_prompt = prompt_path.read_text() if prompt_path.exists() else (
        "Produce a concise weekly operations status pack from the JSON input."
    )

    user_content = (
        "Create this week's status pack from the following structured updates.\n\n"
        + json.dumps(updates, indent=2)
    )

    api_key = os.environ.get("XAI_API_KEY")
    if not api_key:
        print("ERROR: XAI_API_KEY is not set", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    model = os.environ.get("XAI_MODEL", "grok-3")

    print(f"Building status pack with {model}...")
    try:
        response = client.chat.completions.create(
            model=model,
            max_tokens=2500,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
        )
    except Exception as e:
        print(f"ERROR calling xAI API: {e}", file=sys.stderr)
        sys.exit(1)

    full_text = response.choices[0].message.content or ""

    out_dir = Path("data")
    out_dir.mkdir(parents=True, exist_ok=True)
    Path("data/status_pack.md").write_text(full_text)
    print("Wrote data/status_pack.md")

    pack_json = None
    match = re.search(r"```json\s*(\{.*?\})\s*```", full_text, re.DOTALL)
    if match:
        try:
            pack_json = json.loads(match.group(1))
        except json.JSONDecodeError:
            print("Warning: could not parse JSON block")

    if not pack_json:
        pack_json = _fallback_from_updates(updates)

    Path("data/status_pack.json").write_text(json.dumps(pack_json, indent=2))
    docs = Path("docs")
    docs.mkdir(parents=True, exist_ok=True)
    Path("docs/status_pack.json").write_text(json.dumps(pack_json, indent=2))
    print("Wrote data/status_pack.json and docs/status_pack.json")
    return pack_json


def _fallback_from_updates(updates):
    """Deterministic pack if the model omits JSON — keeps the pipeline usable."""
    streams = updates.get("workstreams", [])
    rags = [s.get("rag", "On Track") for s in streams]
    if "Blocked" in rags:
        overall = "Blocked"
    elif "At Risk" in rags:
        overall = "At Risk"
    else:
        overall = "On Track"

    risks = []
    wins = []
    for s in streams:
        for r in s.get("risks") or []:
            risks.append(f"{s.get('name')}: {r}")
        for a in s.get("asks") or []:
            risks.append(f"ASK — {s.get('name')}: {a}")
        for w in s.get("wins") or []:
            wins.append(f"{s.get('name')}: {w}")

    return {
        "week_ending": updates.get("week_ending", ""),
        "program": updates.get("program", ""),
        "overall_rag": overall,
        "executive_summary": (
            "Automated fallback summary: see workstream table and risks list. "
            "Re-run with a valid API response for a full narrative summary."
        ),
        "workstreams": [
            {
                "name": s.get("name"),
                "owner": s.get("owner"),
                "rag": s.get("rag"),
                "summary_line": s.get("update", ""),
            }
            for s in streams
        ],
        "top_risks_and_asks": risks[:8],
        "wins": wins[:8],
        "focus_next_week": updates.get("cross_cutting_notes") or [],
    }


if __name__ == "__main__":
    build_pack()
