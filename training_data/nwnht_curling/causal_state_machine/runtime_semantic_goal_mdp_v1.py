#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Runtime adapter for the universal semantic S_k -> G_k -> S_(k+1) MDP.

Unlike the older direct-fine adapter, this never treats a missing narrow
endpoint circle as a missing tactical objective.  It returns one same-K
semantic GoalState for every recognised state and labels the fine-child
execution evidence separately.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Mapping

try:
    from .partition_states_v2 import classify_runtime_state
    from .runtime_goal_outcome_plan_v1 import _swap_lateral, _unmirror_goal_state
except ImportError:  # pragma: no cover
    import sys
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.partition_states_v2 import classify_runtime_state  # type: ignore
    from causal_state_machine.runtime_goal_outcome_plan_v1 import _swap_lateral, _unmirror_goal_state  # type: ignore


def _unmirror_semantic_goal(goal: Mapping[str, Any]) -> dict[str, Any]:
    result = _unmirror_goal_state(goal)
    for field in ("post_own_topology_distribution",):
        values = result.get(field)
        if isinstance(values, list):
            for item in values:
                if isinstance(item, dict) and isinstance(item.get("value"), str):
                    item["value"] = _swap_lateral(item["value"])
    for fine in result.get("fine_goal_options", []):
        if not isinstance(fine, dict):
            continue
        values = fine.get("post_own_topology_distribution")
        if isinstance(values, list):
            for item in values:
                if isinstance(item, dict) and isinstance(item.get("value"), str):
                    item["value"] = _swap_lateral(item["value"])
    return result


def _unmirror_candidate(candidate: Mapping[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(dict(candidate))
    goal = result.get("goal_state")
    if isinstance(goal, Mapping):
        result["goal_state"] = _unmirror_semantic_goal(goal)
    return result


class RuntimeSemanticGoalMdp:
    """Frozen state partition plus a universal same-K semantic goal table."""

    def __init__(self, partition: Mapping[str, Any], plan: Mapping[str, Any]) -> None:
        self.partition = dict(partition)
        self.plans = {str(row["state_id"]): dict(row) for row in plan["state_plans"]}
        self.manifest = dict(plan.get("manifest", {}))

    @classmethod
    def load(cls, partition_path: Path, plan_path: Path) -> "RuntimeSemanticGoalMdp":
        return cls(
            json.loads(partition_path.read_text(encoding="utf-8")),
            json.loads(plan_path.read_text(encoding="utf-8")),
        )

    def recommend(self, k: int, board: list[dict[str, Any]]) -> dict[str, Any]:
        runtime_state = classify_runtime_state(self.partition, int(k), board)
        state_id = str(runtime_state["state_id"])
        plan = self.plans.get(state_id)
        mirrored = bool(runtime_state["mirrored_from_runtime_board"])
        if plan is None:
            return {
                "state_id": state_id,
                "recommendation_status": "SEARCH_REQUIRED_NO_SEMANTIC_PLAN",
                "primary_goal": None,
                "fallback_goals": [],
                "runtime_orientation_mirrored": mirrored,
                "runtime_state_features": runtime_state["features"],
            }
        result = copy.deepcopy(plan)
        primary = result.get("primary_goal")
        if not isinstance(primary, Mapping) or int(primary["goal_state"]["K"]) != int(k):
            raise ValueError(f"invalid same-K GoalState for {state_id}")
        if mirrored:
            result["primary_goal"] = _unmirror_candidate(primary)
            result["fallback_goals"] = [
                _unmirror_candidate(item) for item in result.get("fallback_goals", []) if isinstance(item, Mapping)
            ]
        result["runtime_orientation_mirrored"] = mirrored
        result["runtime_state_features"] = runtime_state["features"]
        return result


def load_default() -> RuntimeSemanticGoalMdp:
    root = Path(__file__).resolve().parent / "artifacts"
    return RuntimeSemanticGoalMdp.load(
        root / "nwnht_first_player_state_partition_v2.json",
        root / "nwnht_v2_universal_semantic_goal_mdp_v3_physx_admissible.json",
    )
