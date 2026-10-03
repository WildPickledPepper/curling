#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Summarise outer-fold stability of hierarchical tactical-action rankings."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping


def build(fold_results: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    result_count = 0
    for result in fold_results:
        result_count += 1
        for plan in result["state_plans"]:
            grouped[str(plan["state_id"])].append(plan)
    states: list[dict[str, Any]] = []
    for state_id, plans in sorted(grouped.items()):
        primary_zones = Counter()
        primary_goal_ids = Counter()
        ranks: list[int] = []
        correlations: list[float] = []
        for plan in plans:
            primary = plan.get("primary_goal")
            if primary is not None:
                primary_goal_ids[str(primary["goal_id"])] += 1
                zone = primary["goal_state"].get("tactical_target_zone")
                primary_zones[str(zone)] += 1
            diagnostic = plan.get("descriptive_holdout_rank_diagnostic", {})
            if diagnostic.get("primary_goal_holdout_rank") is not None:
                ranks.append(int(diagnostic["primary_goal_holdout_rank"]))
            if diagnostic.get("development_vs_holdout_spearman") is not None:
                correlations.append(float(diagnostic["development_vs_holdout_spearman"]))
        primary_count = sum(primary_goal_ids.values())
        mode_goal, mode_count = (None, 0) if not primary_goal_ids else primary_goal_ids.most_common(1)[0]
        states.append({
            "state_id": state_id,
            "outer_fold_count": len(plans),
            "primary_goal_id_distribution": dict(primary_goal_ids.most_common()),
            "primary_tactical_zone_distribution": dict(primary_zones.most_common()),
            "primary_mode_goal_id": mode_goal,
            "primary_mode_share": None if not primary_count else round(mode_count / primary_count, 6),
            "folds_with_primary": primary_count,
            "holdout_primary_rank_values": ranks,
            "holdout_primary_rank_mean": None if not ranks else round(sum(ranks) / len(ranks), 6),
            "development_vs_holdout_spearman_values": correlations,
            "development_vs_holdout_spearman_mean": None if not correlations else round(sum(correlations) / len(correlations), 6),
            "evidence_status": "OUTER_FOLD_DESCRIPTIVE_STABILITY_ONLY",
            "warning": "This measures agreement across repeated grouped splits. It is not a causal evaluation, and the state/structural candidate definitions were still learned from the corpus before the splits.",
        })
    return {
        "manifest": {
            "schema": "nwnht_v2_tactical_outer_fold_summary_v1",
            "fold_result_count": result_count,
            "purpose": "Inspect whether the same parent tactical action is repeatedly selected across match-grouped folds before any runtime policy is frozen.",
            "prohibition": "Do not treat a high mode share as a winning proof or bypass local-rule/PhysX validation.",
        },
        "states": states,
    }


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, default=root / "nwnht_v2_tactical_outer_fold_summary_v1.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new output path.")
    result = build(json.loads(path.read_text(encoding="utf-8")) for path in args.inputs)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), **result["manifest"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
