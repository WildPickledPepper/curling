#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Runtime-only adapter: exact board + K -> evidence-labelled StatePlan.

No historical label, score, event, rule legality check, or PhysX call enters
this adapter.  It merely applies the frozen v2 state partition and returns the
already-built tactical endpoint contract in the caller's left/right frame.
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
    return value.replace("_LEFT", marker).replace("_RIGHT", "_LEFT").replace(marker, "_RIGHT").replace("_left", marker).replace("_right", "_left").replace(marker, "_right")


def _unmirror_target(option: Mapping[str, Any]) -> dict[str, Any]:
    """Reflect only executable target coordinates/predicates, never state IDs."""

    result = copy.deepcopy(dict(option))
    if "tactical_target_zone" in result:
        result["tactical_target_zone"] = _swap_lateral(str(result["tactical_target_zone"]))
    region = result.get("target_region")
    if isinstance(region, dict):
        if "centre_x_m" in region:
            region["centre_x_m"] = -float(region["centre_x_m"])
        if region.get("x_relation") == "<0":
            region["x_relation"] = ">=0"
        elif region.get("x_relation") == ">=0":
            region["x_relation"] = "<0"
        elif region.get("x_relation") == "<-0.38":
            region["x_relation"] = ">0.38"
        elif region.get("x_relation") == ">0.38":
            region["x_relation"] = "<-0.38"
    for fine in result.get("fine_goal_options", []):
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


class RuntimeStatePlan:
    def __init__(self, partition: Mapping[str, Any], state_plan: Mapping[str, Any]) -> None:
        self.partition = partition
        self.plans = {str(row["state_id"]): row for row in state_plan["state_plans"]}

    @classmethod
    def load(cls, partition_path: Path, state_plan_path: Path) -> "RuntimeStatePlan":
        return cls(
            json.loads(partition_path.read_text(encoding="utf-8")),
            json.loads(state_plan_path.read_text(encoding="utf-8")),
        )

    def recommend(self, k: int, board: list[dict[str, Any]]) -> dict[str, Any]:
        runtime_state = classify_runtime_state(self.partition, k, board)
        plan = self.plans.get(str(runtime_state["state_id"]))
        if plan is None:
            return {
                "state_id": runtime_state["state_id"],
                "recommendation_status": "SEARCH_REQUIRED_NO_STATE_PLAN",
                "runtime_orientation_mirrored": runtime_state["mirrored_from_runtime_board"],
            }
        result = copy.deepcopy(plan)
        mirrored = bool(runtime_state["mirrored_from_runtime_board"])
        if mirrored:
            if result.get("primary_action") is not None:
                result["primary_action"] = _unmirror_target(result["primary_action"])
            result["fallback_actions"] = [_unmirror_target(item) for item in result.get("fallback_actions", [])]
        result["runtime_orientation_mirrored"] = mirrored
        result["runtime_state_features"] = runtime_state["features"]
        return result


def load_default() -> RuntimeStatePlan:
    root = Path(__file__).resolve().parent / "artifacts"
    return RuntimeStatePlan.load(
        root / "nwnht_first_player_state_partition_v2.json",
        root / "nwnht_first_player_runtime_state_plan_v1.json",
    )
