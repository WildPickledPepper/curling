#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Archive AutoDCP record files while Unity is running.

Unity writes useful replay records under scene-dependent ``Records`` folders.
This helper watches likely roots, copies candidate files to a timestamped
archive directory, and emits parsed shot records as JSONL when possible.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import time
from dataclasses import asdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.reverse.parse_autodcp_record import parse_record  # noqa: E402


RECORD_FIELD_HINTS = ("BESTSHOT", "RANDSEED", "TRACE", "SWEEP", "POSITION", "SETSTATE", "SCORE")
RECORD_SECTION_RE = re.compile(r"(?m)^\[\d{4}\]\s*$")
SKIP_DIR_PARTS = {".git", "__pycache__", ".pytest_cache", "node_modules"}
DEFAULT_RELATIVE_DIRS = (
    Path("Records"),
    Path("Records") / "4Games",
    Path("Records") / "8Games",
    Path("AutoGame"),
    Path("数字冰壶单机版_win") / "数字冰壶单机版" / "Records",
    Path("数字冰壶单机版_win") / "数字冰壶单机版" / "Records" / "4Games",
    Path("数字冰壶单机版_win") / "数字冰壶单机版" / "Records" / "8Games",
    Path("数字冰壶单机版_win") / "数字冰壶单机版" / "AutoGame",
)


def default_watch_roots() -> list[Path]:
    return [PROJECT_ROOT / relative for relative in DEFAULT_RELATIVE_DIRS]


def has_record_hint(path: Path, max_bytes: int) -> bool:
    try:
        with path.open("rb") as handle:
            raw = handle.read(max_bytes)
    except OSError:
        return False
    if not raw:
        return False
    text = raw.decode("utf-8-sig", errors="ignore")
    return bool(RECORD_SECTION_RE.search(text)) and any(hint in text for hint in RECORD_FIELD_HINTS)


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def should_skip_path(path: Path, excluded_roots: list[Path], excluded_files: list[Path]) -> bool:
    resolved = path.resolve()
    if any(part.lower() in SKIP_DIR_PARTS for part in resolved.parts):
        return True
    if any(resolved == item.resolve() for item in excluded_files):
        return True
    return any(_is_relative_to(resolved, root) for root in excluded_roots)


def iter_candidate_files(
    roots: list[Path],
    max_bytes: int,
    excluded_roots: list[Path] | None = None,
    excluded_files: list[Path] | None = None,
) -> list[Path]:
    excluded_roots = excluded_roots or []
    excluded_files = excluded_files or []
    candidates: dict[Path, None] = {}
    for root in roots:
        if not root.exists():
            continue
        if should_skip_path(root, excluded_roots, excluded_files):
            continue
        if root.is_file():
            if should_skip_path(root, excluded_roots, excluded_files):
                continue
            if has_record_hint(root, max_bytes):
                candidates[root.resolve()] = None
            continue
        for path in root.rglob("*"):
            if should_skip_path(path, excluded_roots, excluded_files):
                continue
            if not path.is_file():
                continue
            if "archive" in {part.lower() for part in path.parts}:
                continue
            try:
                if path.stat().st_size > max_bytes:
                    continue
            except OSError:
                continue
            if has_record_hint(path, max_bytes):
                candidates[path.resolve()] = None
    return sorted(candidates)


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_existing_digests(archive_dir: Path) -> set[str]:
    seen: set[str] = set()
    if not archive_dir.exists():
        return seen
    for path in archive_dir.rglob("*"):
        if not path.is_file():
            continue
        try:
            seen.add(file_digest(path))
        except OSError:
            continue
    return seen


def safe_relative_name(path: Path) -> str:
    try:
        relative = path.resolve().relative_to(PROJECT_ROOT.resolve())
    except ValueError:
        relative = Path(path.name)
    return "__".join(relative.parts).replace(":", "")


def archive_file(path: Path, archive_dir: Path, seen: set[str], jsonl_handle) -> bool:
    try:
        digest = file_digest(path)
    except OSError:
        return False
    if digest in seen:
        return False
    seen.add(digest)

    archive_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    output = archive_dir / f"{stamp}__{digest[:12]}__{safe_relative_name(path)}"
    shutil.copy2(path, output)

    print(f"[record] archived {path} -> {output}", flush=True)
    try:
        parsed = parse_record(output)
    except Exception as exc:  # noqa: BLE001 - keep watcher alive on partial writes.
        print(f"[record] parse failed for {output}: {exc}", flush=True)
        return True

    for shot in parsed.shots:
        row = asdict(shot)
        row["archive_path"] = str(output)
        jsonl_handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    jsonl_handle.flush()
    print(f"[record] parsed shots={len(parsed.shots)} from {output}", flush=True)
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--watch-root",
        action="append",
        type=Path,
        default=None,
        help="root directory or file to scan; can be repeated",
    )
    parser.add_argument("--archive-dir", type=Path, default=PROJECT_ROOT / "data" / "calibration" / "autodcp_records")
    parser.add_argument("--jsonl", type=Path, default=PROJECT_ROOT / "data" / "calibration" / "autodcp_records.jsonl")
    parser.add_argument("--poll-seconds", type=float, default=2.0)
    parser.add_argument("--max-bytes", type=int, default=20_000_000)
    parser.add_argument("--once", action="store_true", help="scan once and exit")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    roots = args.watch_root if args.watch_root else default_watch_roots()
    args.archive_dir.mkdir(parents=True, exist_ok=True)
    args.jsonl.parent.mkdir(parents=True, exist_ok=True)
    seen = load_existing_digests(args.archive_dir)
    print(f"[record] initialized seen_digests={len(seen)}", flush=True)

    with args.jsonl.open("a", encoding="utf-8") as jsonl_handle:
        while True:
            archived = 0
            for path in iter_candidate_files(
                roots,
                args.max_bytes,
                excluded_roots=[args.archive_dir],
                excluded_files=[args.jsonl],
            ):
                if archive_file(path, args.archive_dir, seen, jsonl_handle):
                    archived += 1
            print(f"[record] scan complete candidates_archived={archived}", flush=True)
            if args.once:
                break
            time.sleep(args.poll_seconds)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
