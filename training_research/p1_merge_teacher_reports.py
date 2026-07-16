#!/usr/bin/env python3
"""Merge compatible strict P0.1 teacher reports into one reproducible P1 dataset.

Each input keeps its original SHA-256, seed, and game number in the merged
record.  Merged ``game`` numbers are unique, so the P1 trainer's game-level
split cannot accidentally put identically numbered ends from different random
seeds into the same group.

Only reports with identical search settings (apart from random seed and output
path) may be merged.  This prevents a low-budget collection from silently
being treated as equivalent to a high-budget teacher dataset.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONFIG_KEYS = (
    "firstSearchShot", "searchSamples", "confidenceZ", "exploration",
    "expandEvery", "initialSamplesPerTemplate", "targetRollouts", "maxCandidates",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, action="append", required=True, help="repeat for every strict P0.1 report")
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def comparable_config(document: dict[str, Any]) -> dict[str, Any]:
    config = document.get("collection", {}).get("config", {})
    missing = [key for key in CONFIG_KEYS if key not in config]
    if missing:
        raise ValueError("teacher collection config lacks: %s" % ", ".join(missing))
    return {key: config[key] for key in CONFIG_KEYS}


def load(path: Path) -> dict[str, Any]:
    document = json.loads(path.read_text(encoding="utf-8"))
    if document.get("schema") != "strict_p0_kernel_late_end_teacher_v1" or not document.get("trainingUsable"):
        raise ValueError("%s is not a training-usable strict P0.1 teacher report" % path)
    if not document.get("games"):
        raise ValueError("%s contains no games" % path)
    comparable_config(document)
    return document


def run(args: argparse.Namespace) -> dict[str, Any]:
    if len(set(args.input)) != len(args.input):
        raise ValueError("an input report was supplied more than once")
    loaded = [(path, load(path)) for path in args.input]
    expected = comparable_config(loaded[0][1])
    scope = loaded[0][1].get("scope")
    merged_games: list[dict[str, Any]] = []
    sources: list[dict[str, Any]] = []
    next_game = 1
    for source_index, (path, document) in enumerate(loaded, start=1):
        if comparable_config(document) != expected:
            raise ValueError("%s has a different search configuration" % path)
        if document.get("scope") != scope:
            raise ValueError("%s has a different collection scope" % path)
        original_config = document["collection"]["config"]
        sources.append({
            "sourceIndex": source_index,
            "path": str(path),
            "sha256": sha256_file(path),
            "seed": original_config.get("seed"),
            "originalGameCount": len(document["games"]),
        })
        for original_game in document["games"]:
            game = dict(original_game)
            game["source"] = {
                "sourceIndex": source_index,
                "sourcePath": str(path),
                "sourceSha256": sources[-1]["sha256"],
                "sourceSeed": original_config.get("seed"),
                "sourceGame": int(original_game["game"]),
            }
            game["game"] = next_game
            merged_games.append(game)
            next_game += 1
    report = {
        "schema": "strict_p0_kernel_late_end_teacher_v1",
        "trainingUsable": True,
        "scope": scope,
        "warning": "Teacher values are against scripted_continuation_v1 until P2 opponent-pool search is implemented.",
        "collection": {
            "merged": True,
            "config": {**expected, "seed": "multiple; see mergedSources"},
            "mergedSources": sources,
        },
        "games": merged_games,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(args.output)
    return report


def main() -> int:
    report = run(parse_args())
    print("P1 教师数据已合并：%d 个来源，%d 个独立 end，%d 条决策" % (
        len(report["collection"]["mergedSources"]), len(report["games"]), sum(len(game["decisions"]) for game in report["games"]),
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
