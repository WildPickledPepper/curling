"""Compile a v2 StatePlan into local circle-terminal requests for a planner.

This is deliberately narrower than the legacy ``GoalState`` package: it does
not translate v2 states into old state keys or pretend that an area goal has a
unique exact post-shot board.  It emits only active-delivery circle requests
in local PhysX coordinates, carrying the original v2 action/precision evidence
alongside them.  A future strict solver must still apply local rules and
validate every simulated final board.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Iterable, Mapping

from planning_proxy.competition_rules import HOUSE_X, HOUSE_Y
from training_data.nwnht_curling.causal_state_machine.runtime_state_plan_v1 import RuntimeStatePlan

from .semantic_region_circle_adapter import circle_subgoals


@dataclass(frozen=True)
class CircleGoalRequest:
    request_id: str
    priority: int
    source_state: str
    action_id: str
    action_precision_level: str
    action_kind: str
    local_centre_x: float
    local_centre_y: float
    radius_m: float
    coverage_status: str
    expected_next_state_distribution: tuple[dict[str, Any], ...]
    evidence_note: str

    def to_json(self) -> dict[str, Any]:
        return asdict(self)


def _historical_board(local_board: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for stone in local_board:
        if not bool(stone.get("enabled", True)):
            continue
        owner = str(stone["owner"])
        if owner not in {"self", "opponent"}:
            raise ValueError("local board owner must be self or opponent")
        result.append({
            "owner": "first" if owner == "self" else "opponent",
            "x_m": float(stone["x"]) - HOUSE_X,
            "y_m": float(stone["y"]) - HOUSE_Y,
        })
    return result


def _circles_for_action(action: Mapping[str, Any], *, max_tiles: int) -> list[dict[str, Any]]:
    precision = str(action["precision_level"])
    if precision == "NARROW_CROSS_FOLD_GOAL":
        return [
            {
                "region_id": str(fine["goal_id"]), "shape": "circle",
                "centre_x_m": float(fine["active_final_region"]["centre_x_m"]),
                "centre_y_m": float(fine["active_final_region"]["centre_y_m"]),
                "radius_m": float(fine["active_final_region"]["radius_m"]),
                "coverage_status": "NARROW_CROSS_FOLD_GOAL",
            }
            for fine in action["fine_goal_options"]
            if fine.get("active_final_region", {}).get("shape") == "circle"
        ]
    if precision == "SEMANTIC_REGION_GOAL":
        return circle_subgoals(action["target_region"], max_tiles=max_tiles, region_id_prefix=str(action["tactical_goal_id"]))
    return []


def compile_circle_goal_requests(
    planner: RuntimeStatePlan,
    own_throw_number: int,
    local_board: Iterable[Mapping[str, Any]],
    *,
    max_tiles_per_action: int = 12,
) -> tuple[dict[str, Any], list[CircleGoalRequest]]:
    """Return runtime plan metadata plus ordered local-coordinate circle goals."""

    if max_tiles_per_action < 1:
        raise ValueError("max_tiles_per_action must be at least one")
    plan = planner.recommend(int(own_throw_number), _historical_board(local_board))
    if plan["recommendation_status"] != "EMPIRICAL_ACTION_CONSENSUS":
        return plan, []
    actions = [plan["primary_action"], *plan.get("fallback_actions", [])]
    requests: list[CircleGoalRequest] = []
    for action_priority, action in enumerate(actions, start=1):
        for circle_index, circle in enumerate(_circles_for_action(action, max_tiles=max_tiles_per_action), start=1):
            requests.append(CircleGoalRequest(
                request_id=f"{action['tactical_goal_id']}|{circle['region_id']}",
                priority=len(requests) + 1,
                source_state=str(plan["state_id"]),
                action_id=str(action["tactical_goal_id"]),
                action_precision_level=str(action["precision_level"]),
                action_kind=str(action["observed_template_kind"]),
                local_centre_x=HOUSE_X + float(circle["centre_x_m"]),
                local_centre_y=HOUSE_Y + float(circle["centre_y_m"]),
                radius_m=float(circle["radius_m"]),
                coverage_status=str(circle["coverage_status"]),
                expected_next_state_distribution=tuple(action.get("expected_next_state_distribution", [])),
                evidence_note=(
                    "Circle target compiled from v2 StatePlan. Local rule checks and strict final-board validation remain mandatory; "
                    f"action-list position={action_priority}, circle-list position={circle_index}."
                ),
            ))
    return plan, requests
