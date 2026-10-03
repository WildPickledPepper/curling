#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Choose reproducibly supported narrow GoalState options below each action.

This is intentionally *not* another end-result ranking.  The parent tactical
action has already been ranked by the finite-horizon model.  Here we ask a
separate execution question: which exact, narrow endpoint constraints recur
in every match-grouped fold within that parent action?  These become ordered
candidate constraints for the later inverse planner, not claims of a finer
causal advantage.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    from .build_causal_estimation_panel import FOLDS, fold_for_match
except ImportError:  # pragma: no cover - direct script invocation
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.build_causal_estimation_panel import FOLDS, fold_for_match  # type: ignore


MIN_FINE_OPTION_SUPPORT_PER_FOLD = 10
MAX_EXECUTION_OPTIONS = 3


def build(
    families: Iterable[Mapping[str, Any]],
    assignments: Iterable[Mapping[str, Any]],
    transition_rows: Iterable[Mapping[str, Any]],
    *,
    min_support_per_fold: int = MIN_FINE_OPTION_SUPPORT_PER_FOLD,
    max_execution_options: int = MAX_EXECUTION_OPTIONS,
) -> dict[str, Any]:
    by_panel = {
        f"{row['end_id']}:{row['own_global_shot_number']}": int(row["match_id"])
        for row in transition_rows
    }
    counts: dict[str, Counter[str]] = defaultdict(Counter)
    folds: dict[str, dict[str, Counter[int]]] = defaultdict(lambda: defaultdict(Counter))
    for row in assignments:
        parent_id = str(row["tactical_goal_id"])
        fine_id = str(row["fine_goal_id"])
        panel_key = str(row["panel_key"])
        if panel_key not in by_panel:
            raise ValueError(f"missing transition row for fine-option assignment {panel_key}")
        counts[parent_id][fine_id] += 1
        folds[parent_id][fine_id][fold_for_match(by_panel[panel_key])] += 1

    screened: list[dict[str, Any]] = []
    for family in families:
        parent_id = str(family["goal_id"])
        options: list[dict[str, Any]] = []
        for option in family.get("fine_goal_options", []):
            fine_id = str(option["goal_id"])
            fold_supports = [int(folds[parent_id][fine_id][fold]) for fold in range(FOLDS)]
            total = int(counts[parent_id][fine_id])
            options.append({
                **dict(option),
                "full_support_recomputed": total,
                "support_by_match_fold": fold_supports,
                "minimum_fold_support": min(fold_supports),
                "maximum_fold_support": max(fold_supports),
                "eligible_as_representative_execution_target": min(fold_supports) >= min_support_per_fold,
                "evidence_status": "REPRODUCIBLE_ENDPOINT_FREQUENCY_NOT_FINE_VALUE_PROOF",
            })
        options.sort(key=lambda item: (
            -int(item["minimum_fold_support"]), -int(item["full_support_recomputed"]), str(item["goal_id"])
        ))
        representatives = [item for item in options if item["eligible_as_representative_execution_target"]][:max_execution_options]
        screened.append({
            "tactical_goal_id": parent_id,
            "source_state": family["source_state"],
            "tactical_target_zone": family.get("tactical_target_zone"),
            "parent_support": family["support"],
            "fine_option_count": len(options),
            "representative_execution_options": representatives,
            "all_fine_options": options,
            "execution_option_status": "SUPPORTED_REPRESENTATIVE_OPTIONS" if representatives else "NO_CROSS_FOLD_SUPPORTED_NARROW_OPTION",
            "warning": "Representative order is recurrence stability only. Do not interpret it as a finer end-value rank or skip later local-rule/PhysX checks.",
        })
    screened.sort(key=lambda row: (str(row["source_state"]), str(row["tactical_goal_id"])))
    return {
        "manifest": {
            "schema": "nwnht_v2_tactical_fine_option_screen_v1",
            "purpose": "Supply up to three cross-fold-recurrent narrow GoalState constraints below a parent tactical action.",
            "thresholds": {
                "match_grouped_folds": FOLDS,
                "min_support_per_fold": min_support_per_fold,
                "max_execution_options": max_execution_options,
            },
            "prohibition": "This is not a fine-grained tactical value model or a PhysX feasibility result.",
        },
        "parents": screened,
    }


def _read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--families", type=Path, default=root / "nwnht_v2_tactical_goal_families_v1.json")
    parser.add_argument("--assignments", type=Path, default=root / "nwnht_v2_tactical_goal_assignments_v1.jsonl")
    parser.add_argument("--transitions", type=Path, default=root / "nwnht_first_player_causal_transitions_v0.jsonl")
    parser.add_argument("--output", type=Path, default=root / "nwnht_v2_tactical_fine_option_screen_v1.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new output path.")
    family_payload = json.loads(args.families.read_text(encoding="utf-8"))
    result = build(family_payload["families"], _read_jsonl(args.assignments), _read_jsonl(args.transitions))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "parent_count": len(result["parents"]), **result["manifest"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
