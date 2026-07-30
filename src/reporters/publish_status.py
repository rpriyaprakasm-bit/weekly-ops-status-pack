"""Copy status outputs into docs/ for the dashboard; record history."""

import shutil
from pathlib import Path

from src.reporters.record_history import record


def publish():
    src = Path("data/status_pack.json")
    if not src.exists():
        print("No data/status_pack.json — skip publish")
        return
    docs = Path("docs")
    docs.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, docs / "status_pack.json")
    print("Published docs/status_pack.json")

    md = Path("data/status_pack.md")
    if md.exists():
        shutil.copy(md, docs / "status_pack.md")
        print("Published docs/status_pack.md")

    record()


if __name__ == "__main__":
    publish()
