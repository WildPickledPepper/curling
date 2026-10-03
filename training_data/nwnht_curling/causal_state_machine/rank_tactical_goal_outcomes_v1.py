#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Five-fold finite-horizon ranking for topology-constrained GoalStates.

This is the missing ``A -> G`` layer.  Parent actions and their fine endpoint
children remain separate, while this module ranks the whole-board outcome
constraint that the later solver should attempt.  Only outcome goals observed
in every match-grouped fold can enter the consensus table.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    from .backward_value_iteration_v2 import _state_k_from_partition, build as value_build
    from .build_causal_estimation_panel import FOLDS
except ImportError:  # pragma: no cover - direct invocation
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.backward_value_iteration_v2 import _state_k_from_partition, build as value_build  # type: ignore
    from causal_state_machine.build_causal_estimation_panel import FOLDS  # type: ignore


MIN_DEVELOPMENT_SUPPORT = 8
MIN_HOLDOUT_SUPPORT = 1
MIN_PRIMARY_FOLD_CONSENSUS = 4
MAX_GOALS_PER_STATE = 3


def build(
    outcome_library: Mapping[str, Any], state_k: Mapping[str, int], *,
    min_development_support: int = MIN_DEVELOPMENT_SUPPORT,
    min_holdout_support: int = MIN_HOLDOUT_SUPPORT,
    min_primary_fold_consensus: int = MIN_PRIMARY_FOLD_CONSENSUS,
    max_goals_per_state: int = MAX_GOALS_PER_STATE,
) -> dict[str, Any]:
    """Rank all-fold-recurrent G candidates, without physics or causal claims."""

    all_goals = {str(row["goal_id"]): dict(row) for row in outcome_library["goals"]}
    goals = {
        goal_id: goal for goal_id, goal in all_goals.items()
        if str(goal.get("execution_status")) == "CROSS_FOLD_TOPOLOGY_TARGET_CANDIDATE"
    }
    observations = [
        dict(row) for row in outcome_library["observations"] if str(row["goal_id"]) in goals
    ]
    if not goals or not observations:
        raise ValueError("no cross-fold topology GoalState observations")

    folds: list[dict[str, Any]] = []
    for holdout_fold in range(FOLDS):
        result = value_build(
            observations, goals, state_k, holdout_fold=holdout_fold,
            min_development_support=min_development_support,
            min_holdout_support=min_holdout_support,
            bootstrap_replicates=0,
        )
        folds.append(result)

    by_state: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for result in folds:
        for plan in result["state_plans"]:
            by_state[str(plan["state_id"])].append(plan)
    plans: list[dict[str, Any]] = []
    for state, k in sorted(state_k.items(), key=lambda item: (item[1], item[0])):
        fold_plans = by_state.get(state, [])
        primary_ids = Counter(
            str(plan["primary_goal"]["goal_id"])
            for plan in fold_plans if plan.get("primary_goal") is not None
        )
        # Preserve the goal returned by value_build for each fold so the final
        # table contains the full predicate and fine constraint menu rather
        # than just an opaque hash.
        rendered: dict[str, Mapping[str, Any]] = {}
        q_values: dict[str, list[float]] = defaultdict(list)
        for plan in fold_plans:
            for candidate in [plan.get("primary_goal"), *plan.get("fallback_goals", [])]:
                if candidate is None:
                    continue
                goal_id = str(candidate["goal_id"])
                rendered.setdefault(goal_id, candidate)
                q_values[goal_id].append(float(candidate["backed_up_value_mean"]))
        ordered = sorted(
            primary_ids,
            key=lambda goal_id: (-primary_ids[goal_id], -(sum(q_values[goal_id]) / len(q_values[goal_id])), goal_id),
        )
        consensus = [
            {
                **rendered[goal_id],
                "primary_fold_count": int(primary_ids[goal_id]),
                "primary_fold_share": round(primary_ids[goal_id] / FOLDS, 6),
                "mean_backed_up_value_across_selected_folds": round(sum(q_values[goal_id]) / len(q_values[goal_id]), 6),
            }
            for goal_id in ordered
            if primary_ids[goal_id] >= min_primary_fold_consensus
        ][:max_goals_per_state]
        plans.append({
            "state_id": state,
            "K": k,
            "recommendation_status": "EMPIRICAL_GOAL_OUTCOME_CONSENSUS" if consensus else "SEARCH_REQUIRED_NO_CROSS_FOLD_GOAL_OUTCOME_CONSENSUS",
            "primary_goal": consensus[0] if consensus else None,
            "fallback_goals": consensus[1:],
            "folds_with_any_eligible_goal": sum(plan.get("primary_goal") is not None for plan in fold_plans),
            "primary_goal_id_distribution": dict(primary_ids.most_common()),
            "runtime_note": "Every selected item is a whole-board terminal predicate plus fine endpoint/binding options. The execution layer must satisfy both; a solver miss is not physical impossibility.",
        })
    return {
        "manifest": {
            "schema": "nwnht_v2_tactical_goal_outcome_value_v1",
            "decision_model": "five match-grouped holdout folds; K8->K1 historical finite-horizon value recursion on topology-constrained GoalStates",
            "input_goal_count_after_cross_fold_topology_gate": len(goals),
            "input_observation_count": len(observations),
            "thresholds": {
                "min_development_support": min_development_support,
                "min_holdout_support": min_holdout_support,
                "min_primary_fold_consensus": min_primary_fold_consensus,
                "max_goals_per_state": max_goals_per_state,
            },
            "summary": {
                "states_with_goal_outcome_consensus": sum(plan["primary_goal"] is not None for plan in plans),
                "consensus_goal_count": sum(1 + len(plan["fallback_goals"]) for plan in plans if plan["primary_goal"] is not None),
            },
            "prohibition": "Ranking is historical trajectory association under a fixed state abstraction. It is not causal proof, a winning guarantee, rule validation, or a PhysX feasibility result.",
        },
        "state_plans": plans,
    }


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outcomes", type=Path, default=root / "nwnht_v2_tactical_goal_outcome_library_v2.json")
    parser.add_argument("--partition", type=Path, default=root / "nwnht_first_player_state_partition_v2.json")
    parser.add_argument("--output", type=Path, default=root / "nwnht_v2_tactical_goal_outcome_value_v1.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new output path.")
    outcomes = json.loads(args.outcomes.read_text(encoding="utf-8"))
    partition = json.loads(args.partition.read_text(encoding="utf-8"))
    result = build(outcomes, _state_k_from_partition(partition))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), **result["manifest"]["summary"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
