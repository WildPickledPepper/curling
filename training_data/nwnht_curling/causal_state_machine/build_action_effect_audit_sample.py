#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create a deterministic, K-stratified manual audit set for board-effect labels."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any, Iterable


def read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            yield json.loads(line)


def _compact(row: dict[str, Any]) -> dict[str, Any]:
    effect = row["observed_own_board_effect"]
    return {
        "audit_key": f"{row['end_id']}:{row['own_global_shot_number']}",
        "match_id": row["match_id"],
        "end_id": row["end_id"],
        "end_number": row["end_number"],
        "own_throw_number": row["own_throw_number"],
        "source_frames": row["source_frames"],
        "upstream_own_call": row["observed_own_delivery"],
        "upstream_opponent_reply": row["observed_opponent_reply"],
        "primary_effect": effect["primary_effect"],
        "effect_tags": effect["effect_tags"],
        "before_facts": effect["before"],
        "after_facts": effect["after"],
        "delta": effect["delta"],
        "s_before_own": row["s_before_own"],
        "u_after_own": row["u_after_own"],
        "s_after_opponent_reply": row["s_after_opponent_reply"],
    }


def select_audit_rows(rows: Iterable[dict[str, Any]], per_effect: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    groups: dict[str, dict[int, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    call_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        effect = str(row["observed_own_board_effect"]["primary_effect"])
        k = int(row["own_throw_number"])
        groups[effect][k].append(row)
        call_counts[effect][str(row["observed_own_delivery"]["called_shot"])] += 1

    selected: list[dict[str, Any]] = []
    coverage: dict[str, Any] = {}
    for effect, by_k in sorted(groups.items()):
        queues = {k: deque(sorted(items, key=lambda row: (int(row["match_id"]), int(row["end_id"])))) for k, items in by_k.items()}
        picked: list[dict[str, Any]] = []
        while len(picked) < per_effect and any(queues.values()):
            for k in sorted(queues):
                if queues[k] and len(picked) < per_effect:
                    # Spread samples through each K bucket instead of taking an
                    # arbitrary adjacent run from one match.
                    queue = queues[k]
                    index = len(queue) // 2
                    queue.rotate(-index)
                    picked.append(queue.popleft())
                    queue.rotate(index)
        selected.extend(_compact(row) for row in picked)
        coverage[effect] = {
            "available_by_K": {str(k): len(items) for k, items in sorted(by_k.items())},
            "selected_by_K": dict(sorted(Counter(int(row["own_throw_number"]) for row in picked).items())),
            "selected_count": len(picked),
            "upstream_call_distribution": dict(call_counts[effect].most_common()),
        }
    return selected, {
        "schema": "nwnht_first_player_board_effect_manual_audit_manifest_v1",
        "sampling": "deterministic round-robin over own throw K; source rows are sorted by match/end before selection",
        "per_primary_effect_target": per_effect,
        "effects": coverage,
        "review_protocol": [
            "Check the S->U board change, not just the upstream call label.",
            "Mark correct / ambiguous / incorrect primary effect.",
            "Record whether source colour/stone detection itself appears ambiguous.",
            "Do not use terminal end result while judging the immediate effect.",
        ],
    }


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=root / "nwnht_first_player_board_effects_v2.jsonl")
    parser.add_argument("--output", type=Path, default=root / "nwnht_first_player_board_effect_manual_audit_v2.jsonl")
    parser.add_argument("--manifest", type=Path, default=root / "nwnht_first_player_board_effect_manual_audit_v2_manifest.json")
    parser.add_argument("--per-effect", type=int, default=30)
    args = parser.parse_args()
    if args.per_effect < 1:
        raise SystemExit("--per-effect must be positive")
    for path in (args.output, args.manifest):
        if path.exists():
            raise SystemExit(f"Refusing to overwrite {path}; choose a new path deliberately.")
    selected, manifest = select_audit_rows(read_jsonl(args.input), args.per_effect)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for row in selected:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "manifest": str(args.manifest), "rows": len(selected)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
