#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Runtime adapter for five-fold topology-constrained GoalState consensus.

Input is only ``K`` plus the current canonical NWNHT board.  Output is either
an evidence-labelled primary/fallback whole-board goal or an explicit search
abstention.  This module deliberately does not call rules or PhysX.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Mapping

try:
    from .partition_states_v2 import classify_runtime_state
except ImportError:  # pragma: no cover - direct script invocation
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.partition_states_v2 import classify_runtime_state  # type: ignore


def _swap_lateral(value: str) -> str:
    marker = "__SIDE_SWAP__"
    return (
        value.replace("_LEFT", marker).replace("_RIGHT", "_LEFT").replace(marker, "_RIGHT")
        .replace("_left", marker).replace("_right", "_left").replace(marker, "_right")
    )


def _unmirror_goal_state(goal_state: Mapping[str, Any]) -> dict[str, Any]:
    """Return a caller-frame G; leave its evidence and canonical state ID intact."""

    result = copy.deepcopy(dict(goal_state))
    if "tactical_target_zone" in result and result["tactical_target_zone"] is not None:
        result["tactical_target_zone"] = _swap_lateral(str(result["tactical_target_zone"]))
    if isinstance(result.get("post_own_topology"), str):
        result["post_own_topology"] = _swap_lateral(str(result["post_own_topology"]))
    predicate = result.get("terminal_board_predicate")
    if isinstance(predicate, dict):
        result["terminal_board_predicate"] = {
            _swap_lateral(str(name)): value for name, value in predicate.items()
        }
    for fine in result.get("fine_goal_options", []):
        if not isinstance(fine, dict):
            continue
        active = fine.get("active_final_region")
        if isinstance(active, dict) and "centre_x_m" in active:
            active["centre_x_m"] = -float(active["centre_x_m"])
        occupancy = fine.get("after_own_occupancy")
        if isinstance(occupancy, dict):
            for owner, zones in occupancy.items():
                if isinstance(zones, dict):
                    occupancy[owner] = {_swap_lateral(str(zone)): count for zone, count in zones.items()}
        for selector in fine.get("stone_constraints_when_unambiguous", []):
            if isinstance(selector, dict) and "historical_source_zone" in selector:
                selector["historical_source_zone"] = _swap_lateral(str(selector["historical_source_zone"]))
    return result


def _unmirror_candidate(candidate: Mapping[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(dict(candidate))
    goal_state = result.get("goal_state")
    if isinstance(goal_state, Mapping):
        result["goal_state"] = _unmirror_goal_state(goal_state)
    return result


class RuntimeGoalOutcomePlan:
    """Frozen v2 classifier plus G-level five-fold consensus table."""

    def __init__(self, partition: Mapping[str, Any], value_plan: Mapping[str, Any]) -> None:
        self.partition = dict(partition)
        self.plans = {str(row["state_id"]): dict(row) for row in value_plan["state_plans"]}
        self.manifest = dict(value_plan.get("manifest", {}))

    @classmethod
    def load(cls, partition_path: Path, value_plan_path: Path) -> "RuntimeGoalOutcomePlan":
        return cls(
            json.loads(partition_path.read_text(encoding="utf-8")),
            json.loads(value_plan_path.read_text(encoding="utf-8")),
        )

    def recommend(self, k: int, board: list[dict[str, Any]]) -> dict[str, Any]:
        """Map a current board to a full G, or abstain without nearest-state fallback."""

        runtime_state = classify_runtime_state(self.partition, int(k), board)
        state_id = str(runtime_state["state_id"])
        plan = self.plans.get(state_id)
        mirrored = bool(runtime_state["mirrored_from_runtime_board"])
        if plan is None:
            return {
                "state_id": state_id,
                "recommendation_status": "SEARCH_REQUIRED_NO_GOAL_OUTCOME_PLAN",
                "primary_goal": None,
                "fallback_goals": [],
                "runtime_orientation_mirrored": mirrored,
                "runtime_state_features": runtime_state["features"],
            }
        result = copy.deepcopy(plan)
        if mirrored:
            if isinstance(result.get("primary_goal"), Mapping):
                result["primary_goal"] = _unmirror_candidate(result["primary_goal"])
            result["fallback_goals"] = [
                _unmirror_candidate(item) for item in result.get("fallback_goals", []) if isinstance(item, Mapping)
            ]
        result["runtime_orientation_mirrored"] = mirrored
        result["runtime_state_features"] = runtime_state["features"]
        return result


def load_default() -> RuntimeGoalOutcomePlan:
    root = Path(__file__).resolve().parent / "artifacts"
    return RuntimeGoalOutcomePlan.load(
        root / "nwnht_first_player_state_partition_v2.json",
        root / "nwnht_v2_tactical_goal_outcome_value_v1.json",
    )
