"""Fast, local-only file and folder change monitor. No content hashing."""
from __future__ import annotations

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Any

APP_DIR = Path.home() / ".pcwatch"
BASELINE_FILE = APP_DIR / "baseline.json"
REPORT_DIR = APP_DIR / "reports"


def local_time(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).astimezone().strftime("%Y-%m-%d %I:%M:%S %p")


def collect_metadata(folder: str | Path) -> dict[str, Any]:
    root = Path(folder).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Folder does not exist or is not a directory: {root}")

    entries: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    # Include folders as well as files. os.walk does not follow symlinks.
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        dirs[:] = [d for d in dirs if not (current_path / d).is_symlink()]
        for name in list(dirs) + files:
            path = current_path / name
            try:
                if path.is_symlink():
                    continue
                stat = path.stat()
                relative = path.relative_to(root).as_posix()
                entries[relative] = {
                    "type": "folder" if path.is_dir() else "file",
                    "size": stat.st_size,
                    "modified": stat.st_mtime,
                    "modified_display": local_time(stat.st_mtime),
                }
            except OSError as exc:
                errors.append(f"{path}: {exc}")

    return {
        "folder": str(root),
        "updated": datetime.now().astimezone().isoformat(),
        "entries": entries,
        "errors": errors,
    }


def save_baseline(folder: str | Path):
    snapshot = collect_metadata(folder)
    APP_DIR.mkdir(parents=True, exist_ok=True)
    temp = BASELINE_FILE.with_suffix(".tmp")
    temp.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    temp.replace(BASELINE_FILE)
    return snapshot


def load_baseline() -> dict[str, Any]:
    if not BASELINE_FILE.exists():
        raise FileNotFoundError("No folder is selected yet. Choose option 2 first.")
    data = json.loads(BASELINE_FILE.read_text(encoding="utf-8"))
    if not isinstance(data.get("entries"), dict) or not data.get("folder"):
        raise ValueError("Saved monitor data is invalid. Choose option 2 to reset it.")
    return data


def check_changes(baseline: dict[str, Any]) -> dict[str, Any]:
    current = collect_metadata(baseline["folder"])
    old = baseline["entries"]
    new = current["entries"]
    added = [(name, new[name]) for name in sorted(set(new) - set(old))]
    missing = [(name, old[name]) for name in sorted(set(old) - set(new))]
    modified = []
    for name in sorted(set(old) & set(new)):
        before, after = old[name], new[name]
        if (before.get("type") != after.get("type")
                or before.get("size") != after.get("size")
                or before.get("modified") != after.get("modified")):
            modified.append((name, after))
    return {
        "folder": baseline["folder"],
        "checked": datetime.now().astimezone().strftime("%Y-%m-%d %I:%M:%S %p"),
        "added": added,
        "modified": modified,
        "missing": missing,
        "errors": current["errors"],
    }


def save_report(report: dict[str, Any]):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = REPORT_DIR / f"changes-{stamp}.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return path
