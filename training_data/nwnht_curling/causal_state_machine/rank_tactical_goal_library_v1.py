#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run K8->K1 empirical value ranking over hierarchical tactical actions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    from .backward_value_iteration_v2 import (
        BOOTSTRAP_SEED, DEFAULT_BOOTSTRAP_REPLICATES, HOLDOUT_FOLD,
        _state_k_from_partition, build,
    )
    from .build_causal_estimation_panel import fold_for_match
except ImportError:  # pragma: no cover - direct script invocation
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.backward_value_iteration_v2 import (  # type: ignore
        BOOTSTRAP_SEED, DEFAULT_BOOTSTRAP_REPLICATES, HOLDOUT_FOLD,
        _state_k_from_partition, build,
    )
    from causal_state_machine.build_causal_estimation_panel import fold_for_match  # type: ignore


def collect_observations(
    transition_rows: Iterable[Mapping[str, Any]], assignments: Iterable[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    by_panel = {
        f"{row['end_id']}:{row['own_global_shot_number']}": row
        for row in transition_rows
    }
    observations: list[dict[str, Any]] = []
    for assignment in assignments:
        source = by_panel.get(str(assignment["panel_key"]))
        if source is None:
            raise ValueError(f"missing transition row for tactical assignment {assignment['panel_key']}")
        match_id = int(source["match_id"])
        observations.append({
            "match_id": match_id,
            "fold": fold_for_match(match_id),
            "K": int(assignment["K"]),
            "source_state": str(assignment["source_state"]),
            "goal_id": str(assignment["tactical_goal_id"]),
            "next_state": str(assignment["after_opponent_reply_state"]),
            "post_own_topology": str(assignment["post_own_topology"]),
            "margin": float(source["terminal_end_label"]["first_end_margin"]),
        })
    if not observations:
        raise ValueError("no tactical action observations")
    return observations


def _read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--transitions", type=Path, default=root / "nwnht_first_player_causal_transitions_v0.jsonl")
    parser.add_argument("--assignments", type=Path, default=root / "nwnht_v2_tactical_goal_assignments_v1.jsonl")
    parser.add_argument("--tactical-goals", type=Path, default=root / "nwnht_v2_tactical_goal_families_v1.json")
    parser.add_argument("--partition", type=Path, default=root / "nwnht_first_player_state_partition_v2.json")
    parser.add_argument("--output", type=Path, default=root / "nwnht_v2_tactical_empirical_mdp_value_v1.json")
    parser.add_argument("--bootstrap-replicates", type=int, default=DEFAULT_BOOTSTRAP_REPLICATES)
    parser.add_argument("--holdout-fold", type=int, default=HOLDOUT_FOLD)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new output path.")
    tactical = json.loads(args.tactical_goals.read_text(encoding="utf-8"))
    goals = {str(row["goal_id"]): row for row in tactical["families"]}
    observations = collect_observations(_read_jsonl(args.transitions), _read_jsonl(args.assignments))
    partition = json.loads(args.partition.read_text(encoding="utf-8"))
    result = build(
        observations, goals, _state_k_from_partition(partition),
        holdout_fold=args.holdout_fold,
        bootstrap_replicates=args.bootstrap_replicates,
        bootstrap_seed=BOOTSTRAP_SEED,
    )
    result["manifest"]["schema"] = "nwnht_v2_hierarchical_empirical_mdp_value_v1"
    result["manifest"]["action_layer"] = "Parent tactical actions are ranked; each selected action exposes narrow fine_goal_options for later execution."
    result["manifest"]["input_tactical_action_count"] = len(goals)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), **result["manifest"]["summary"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
