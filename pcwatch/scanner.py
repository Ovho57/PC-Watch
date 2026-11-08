"""PC Watch file-integrity scanner.

This is a defensive, local-only utility. It hashes files under a folder chosen
by the user and compares them with a saved baseline. It does not delete files,
upload data, or claim to detect malware.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Any
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

APP_DIR = Path.home() / ".pcwatch"
BASELINE_FILE = APP_DIR / "baseline.json"
REPORT_DIR = APP_DIR / "reports"

# These suffixes are only review hints. An extension alone does NOT mean a file
# is malicious. Users can edit this list to suit their environment.
REVIEW_EXTENSIONS = {
    ".exe", ".dll", ".bat", ".cmd", ".ps1", ".vbs", ".js",
    ".scr", ".pif", ".com", ".jar", ".msi"
}

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def iter_files(root: Path):
    """Yield regular files beneath root without following symlinks."""
    root = root.resolve()
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        dirs[:] = [d for d in dirs if not (current_path / d).is_symlink()]
        for filename in files:
            path = current_path / filename
            try:
                if path.is_symlink() or not path.is_file():
                    continue
                yield path
            except (OSError, PermissionError):
                continue

def build_snapshot(folder: str | Path) -> dict[str, Any]:
    root = Path(folder).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Folder does not exist or is not a directory: {root}")

    snapshot = {}
    errors = []
    count = 0
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]{task.description}"),
        TimeElapsedColumn(),
        transient=False,
    ) as progress:
        task = progress.add_task(f"PC Watch hashing files in {root}", total=None)
        for path in iter_files(root):
            try:
                rel = path.relative_to(root).as_posix()
                stat = path.stat()
                snapshot[rel] = {
                    "sha256": sha256_file(path),
                    "size_bytes": stat.st_size,
                    "modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat()
                }
                count += 1
                progress.update(task, description=f"Hashing files... {count} processed")
            except (OSError, PermissionError) as exc:
                errors.append({"path": str(path), "error": str(exc)})
                progress.update(task, description=f"Hashing files... {count} processed (some skipped)")
        progress.update(task, description=f"Finished hashing {count} files")

    return {
        "folder": str(root),
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "files": snapshot,
        "scan_errors": errors
    }

def save_baseline(folder: str | Path, destination: Path = BASELINE_FILE):
    snapshot = build_snapshot(folder)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(".tmp")
    temporary.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    temporary.replace(destination)
    return snapshot

def load_baseline(path: Path = BASELINE_FILE) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            "No baseline found. Create one first with the 'baseline' command."
        )
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data.get("files"), dict) or not data.get("folder"):
        raise ValueError("Baseline file is malformed.")
    return data

def compare_to_baseline(baseline: dict[str, Any]) -> dict[str, Any]:
    root = Path(baseline["folder"])
    current = build_snapshot(root)
    old_files = baseline["files"]
    new_files = current["files"]

    added = sorted(set(new_files) - set(old_files))
    missing = sorted(set(old_files) - set(new_files))
    modified = sorted(
        name for name in set(old_files) & set(new_files)
        if old_files[name]["sha256"] != new_files[name]["sha256"]
    )

    review = sorted(
        name for name in new_files
        if Path(name).suffix.lower() in REVIEW_EXTENSIONS
    )

    return {
        "folder": str(root),
        "checked_utc": current["created_utc"],
        "added": added,
        "modified": modified,
        "missing": missing,
        "review_extensions": review,
        "scan_errors": current["scan_errors"],
        "total_files": len(new_files)
    }

def save_report(report: dict[str, Any], destination: Path | None = None):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    if destination is None:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        destination = REPORT_DIR / f"scan-{stamp}.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return destination
