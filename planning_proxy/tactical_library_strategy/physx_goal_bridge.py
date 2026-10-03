"""Bridge v2 circle goals to the existing coarse-proxy/PhysX draw solver.

The v2 tactical library owns *which final region to seek*.  This module does
not choose a different tactic, score attacks, or change the legacy player. It
only adapts an ``ACTIVE_STONE_PLACEMENT`` circle request to the existing
continuous solver:

    coarse proxy -> strict PhysX -> Newton/MADS -> multi-seed final check

Only clear-path placement is admitted in this first bridge.  A collision goal
needs explicit bindings for stones that must survive/move/out; silently
feeding it to the old takeout scorer would turn the new library into a
"clear whatever is nearby" policy.
"""

from __future__ import annotations

import copy
import time
from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping, Sequence

from planning_proxy.analytic_proxy import ProxyStone
from planning_proxy.evaluate_vs_teammate_ppo import ProxyMatchPlayer
from planning_proxy.competition_rules import HOUSE_R, HOUSE_X, HOUSE_Y, STONE_R
from planning_proxy.first_player_strategy import FirstPlayerPlan
from planning_proxy.strict_refine import BoardStone, make_position

from .v2_circle_goal_adapter import CircleGoalRequest, _historical_board
from .semantic_region_circle_adapter import circle_subgoals


PLACEMENT_KIND = "ACTIVE_STONE_PLACEMENT"
REMOVAL_KINDS = frozenset({"SINGLE_OPPONENT_REMOVAL", "DOUBLE_OR_MULTI_OPPONENT_REMOVAL"})


@dataclass(frozen=True)
class PhysxGoalAttempt:
    """One ordered terminal-circle attempt; a budget miss is not infeasibility."""

    request_id: str
    priority: int
    status: str
    detail: dict[str, Any]
    bestshot: tuple[float, float, float] | None = None

    def to_json(self) -> dict[str, Any]:
        data = asdict(self)
        if self.bestshot is not None:
            data["bestshot"] = list(self.bestshot)
        return data


@dataclass(frozen=True)
class BoundCollisionGoalRequest:
    """One current-board binding of a data-derived single-removal contract."""

    request_id: str
    priority: int
    collision_goal_id: str
    source_state: str
    tactical_goal_id: str
    target_opponent_index: int
    local_centre_x: float
    local_centre_y: float
    radius_m: float
    coverage_status: str
    expected_next_state_distribution: tuple[dict[str, Any], ...]

    def to_json(self) -> dict[str, Any]:
        return asdict(self)


def _as_board(local_board: Iterable[Mapping[str, Any]]) -> tuple[list[BoardStone], list[ProxyStone]]:
    strict: list[BoardStone] = []
    proxy: list[ProxyStone] = []
    seen: set[int] = set()
    for raw in local_board:
        if not bool(raw.get("enabled", True)):
            continue
        index = int(raw["index"])
        owner = str(raw["owner"])
        if owner not in {"self", "opponent"}:
            raise ValueError("local board owner must be self or opponent")
        if index in seen:
            raise ValueError("local board stone index must be unique")
        seen.add(index)
        x, y = float(raw["x"]), float(raw["y"])
        strict.append(BoardStone(index, owner, x, y, yaw=float(raw.get("yaw", 0.0))))
        proxy.append(ProxyStone(index, owner, x, y))
    return strict, proxy


def draw_plan_for_circle(request: CircleGoalRequest, *, own_throw_number: int, shot_index: int) -> FirstPlayerPlan:
    """Make the smallest compatibility object required by the existing solver.

    ``phase`` deliberately has no legacy semantic meaning.  Its strict scorer
    therefore accepts only the region predicate for this clear-path bridge;
    rule legality and no-existing-stone movement remain enforced separately by
    the existing solver.
    """

    if request.action_kind != PLACEMENT_KIND:
        raise ValueError(f"{request.request_id} is not a clear-placement goal")
    return FirstPlayerPlan(
        shot_index=int(shot_index),
        own_throw_number=int(own_throw_number),
        phase="v2_terminal_circle",
        target_points=((float(request.local_centre_x), float(request.local_centre_y)),),
        target_opponent_index=None,
        opponent_action="none",
        rationale=(
            "v2 tactical-library terminal circle; the existing solver may only use a clear path. "
            f"source_state={request.source_state}; action={request.action_id}; request={request.request_id}"
        ),
        landing_region_radius_m=float(request.radius_m),
        situation_type=request.source_state,
        strategy_type=request.action_id,
        desired_state_type="v2_observed_next_state_distribution",
    )


def _rank_stones(stones: Sequence[Mapping[str, Any]], rank_by: str) -> list[Mapping[str, Any]]:
    if rank_by == "closest_to_button":
        return sorted(stones, key=lambda stone: ((float(stone["x"]) - HOUSE_X) ** 2 + (float(stone["y"]) - HOUSE_Y) ** 2, int(stone["index"])))
    if rank_by == "frontmost":
        return sorted(stones, key=lambda stone: (-float(stone["y"]), int(stone["index"])))
    if rank_by == "backmost":
        return sorted(stones, key=lambda stone: (float(stone["y"]), int(stone["index"])))
    if rank_by == "leftmost":
        return sorted(stones, key=lambda stone: (float(stone["x"]), int(stone["index"])))
    if rank_by == "rightmost":
        return sorted(stones, key=lambda stone: (-float(stone["x"]), int(stone["index"])))
    raise ValueError(f"unsupported target rank {rank_by!r}")


def _bound_target_indices(contract: Mapping[str, Any], local_board: Iterable[Mapping[str, Any]]) -> list[int]:
    """Bind only single-target contracts to current geometric stone roles."""

    binding = contract.get("target_binding")
    if not isinstance(binding, Mapping) or int(binding.get("choose_count", 0)) != 1:
        return []
    opponents = [
        stone for stone in local_board
        if bool(stone.get("enabled", True)) and str(stone.get("owner")) == "opponent"
    ]
    mode = str(binding.get("binding_mode"))
    if mode == "DYNAMIC_OPPONENT_HOUSE_SET":
        candidates = [
            stone for stone in opponents
            if ((float(stone["x"]) - HOUSE_X) ** 2 + (float(stone["y"]) - HOUSE_Y) ** 2) ** 0.5 <= HOUSE_R + STONE_R
        ]
        return [int(stone["index"]) for stone in _rank_stones(candidates, "closest_to_button")]
    if mode == "UNAMBIGUOUS_SELECTOR_SET":
        selectors = binding.get("selectors")
        if not isinstance(selectors, list) or len(selectors) != 1 or not isinstance(selectors[0], Mapping):
            return []
        selector = selectors[0]
        candidates = opponents
        if str(selector.get("source_region")) == "house":
            candidates = [
                stone for stone in candidates
                if ((float(stone["x"]) - HOUSE_X) ** 2 + (float(stone["y"]) - HOUSE_Y) ** 2) ** 0.5 <= HOUSE_R + STONE_R
            ]
        ordered = _rank_stones(candidates, str(selector.get("rank_by")))
        rank = int(selector.get("rank", 0))
        return [] if rank < 1 or rank > len(ordered) else [int(ordered[rank - 1]["index"])]
    return []


def _unmirror_region(region: Mapping[str, Any]) -> dict[str, Any]:
    """Return a canonical semantic region in the caller's left/right frame."""

    result = copy.deepcopy(dict(region))
    if "centre_x_m" in result:
        result["centre_x_m"] = -float(result["centre_x_m"])
    relation = result.get("x_relation")
    swaps = {"<0": ">=0", ">=0": "<0", "<-0.38": ">0.38", ">0.38": "<-0.38"}
    if relation in swaps:
        result["x_relation"] = swaps[relation]
    return result


def bind_single_collision_contract(
    contract: Mapping[str, Any],
    local_board: Iterable[Mapping[str, Any]],
    *,
    max_tiles: int = 4,
    max_target_candidates: int = 3,
    runtime_orientation_mirrored: bool = False,
) -> tuple[BoundCollisionGoalRequest, ...]:
    """Bind one data contract to target slot(s) and local active-stone circles.

    A contract is not emitted if it asks for anything other than exactly one
    opponent stone out of play.  The current MADS endpoint only solves that
    single-target topology; a double clear must get a separate solver rather
    than being weakened to one clear.
    """

    if str(contract.get("observed_template_kind")) not in REMOVAL_KINDS:
        return ()
    if int(contract.get("required_opponent_removed_count", 0)) != 1:
        return ()
    region = contract.get("active_target_region")
    if not isinstance(region, Mapping) or max_tiles < 1 or max_target_candidates < 1:
        return ()
    targets = _bound_target_indices(contract, local_board)[:max_target_candidates]
    caller_region = _unmirror_region(region) if runtime_orientation_mirrored else dict(region)
    canonical_circles = circle_subgoals(caller_region, max_tiles=max_tiles, region_id_prefix=str(contract["collision_goal_id"]))
    requests: list[BoundCollisionGoalRequest] = []
    for target_rank, target_index in enumerate(targets, start=1):
        for circle_rank, circle in enumerate(canonical_circles, start=1):
            requests.append(BoundCollisionGoalRequest(
                request_id=f"{contract['collision_goal_id']}|target={target_index}|circle={circle_rank}",
                priority=len(requests) + 1,
                collision_goal_id=str(contract["collision_goal_id"]),
                source_state=str(contract["source_state"]),
                tactical_goal_id=str(contract["tactical_goal_id"]),
                target_opponent_index=int(target_index),
                local_centre_x=HOUSE_X + float(circle["centre_x_m"]),
                local_centre_y=HOUSE_Y + float(circle["centre_y_m"]),
                radius_m=float(circle["radius_m"]),
                coverage_status=str(circle["coverage_status"]),
                expected_next_state_distribution=tuple(contract.get("expected_next_state_distribution", [])),
            ))
    return tuple(requests)


def bind_contract_for_runtime_state(
    planner: Any,
    contract: Mapping[str, Any],
    own_throw_number: int,
    local_board: Iterable[Mapping[str, Any]],
    *,
    max_tiles: int = 4,
    max_target_candidates: int = 3,
) -> tuple[dict[str, Any], tuple[BoundCollisionGoalRequest, ...]]:
    """Classify first, then bind a contract only in its own v2 source state."""

    board = list(local_board)
    plan = planner.recommend(int(own_throw_number), _historical_board(board))
    if str(plan.get("state_id")) != str(contract.get("source_state")):
        return plan, ()
    return plan, bind_single_collision_contract(
        contract, board, max_tiles=max_tiles, max_target_candidates=max_target_candidates,
        runtime_orientation_mirrored=bool(plan.get("runtime_orientation_mirrored", False)),
    )


def collision_plan_for_request(
    request: BoundCollisionGoalRequest, *, own_throw_number: int, shot_index: int,
) -> FirstPlayerPlan:
    """Adapt a single-target exact-out contract to the existing MADS API."""

    return FirstPlayerPlan(
        shot_index=int(shot_index), own_throw_number=int(own_throw_number), phase="v2_collision_terminal",
        target_points=((float(request.local_centre_x), float(request.local_centre_y)),),
        target_opponent_index=int(request.target_opponent_index), opponent_action="physical_clear",
        rationale=(
            "v2 collision contract: named runtime target must be OUT_OF_PLAY; "
            f"source_state={request.source_state}; contract={request.collision_goal_id}"
        ),
        landing_region_radius_m=float(request.radius_m), situation_type=request.source_state,
        strategy_type=request.tactical_goal_id, desired_state_type="v2_observed_next_state_distribution",
    )


def _target_is_out_in_every_seed(evaluation: Any, target_index: int) -> bool:
    """Stricter than legacy ``physical_clear``: edge-dead is not OUT_OF_PLAY."""

    rows = getattr(evaluation, "enemy_cleared_indices", ())
    return bool(rows) and all(int(target_index) in {int(index) for index in row} for row in rows)


def solve_clear_path_circle_requests(
    requests: Sequence[CircleGoalRequest],
    local_board: Iterable[Mapping[str, Any]],
    *,
    own_throw_number: int,
    physics_seeds: int = 3,
    match_seed: int = 20260717,
    decision_budget_seconds: float = 20.0,
    shot_index: int | None = None,
    solver: ProxyMatchPlayer | None = None,
) -> tuple[PhysxGoalAttempt, ...]:
    """Try circle requests in priority order using existing Newton/MADS draw code.

    ``NOT_FOUND_WITHIN_BUDGET`` means that this configured solver did not
    produce a certified clear-path shot.  It must never be read as a proof that
    the original tactical region is physically unreachable.
    """

    if not 1 <= int(own_throw_number) <= 8:
        raise ValueError("own_throw_number must be 1..8")
    if int(physics_seeds) < 1 or float(decision_budget_seconds) <= 0.0:
        raise ValueError("physics_seeds and decision_budget_seconds must be positive")
    actual_shot_index = 2 * (int(own_throw_number) - 1) if shot_index is None else int(shot_index)
    if not 0 <= actual_shot_index <= 15:
        raise ValueError("shot_index must be 0..15")

    strict_board, proxy_board = _as_board(local_board)
    if any(stone.index == actual_shot_index for stone in strict_board):
        raise ValueError("active shot slot is already occupied on the input board")
    engine = solver or ProxyMatchPlayer(
        physics_seeds=int(physics_seeds), parent_regions=1, decision_budget_seconds=float(decision_budget_seconds),
    )
    deadline = time.perf_counter() + float(decision_budget_seconds)
    seeds = [int(match_seed) + actual_shot_index * 7919 + 104729 * offset for offset in range(int(physics_seeds))]
    position = make_position(strict_board)
    attempts: list[PhysxGoalAttempt] = []

    for request in sorted(requests, key=lambda item: int(item.priority)):
        if request.action_kind != PLACEMENT_KIND:
            attempts.append(PhysxGoalAttempt(
                request.request_id, int(request.priority), "REQUIRES_COLLISION_GOAL_CONSTRAINTS",
                {"action_kind": request.action_kind, "reason": "clear-path bridge never substitutes a takeout objective"},
            ))
            continue
        if time.perf_counter() >= deadline:
            attempts.append(PhysxGoalAttempt(
                request.request_id, int(request.priority), "NOT_ATTEMPTED_BUDGET_EXHAUSTED",
                {"reason": "previous ordered requests consumed the configured total budget"},
            ))
            continue
        plan = draw_plan_for_circle(request, own_throw_number=int(own_throw_number), shot_index=actual_shot_index)
        result = engine._try_fast_targeted_draw(  # existing tested Newton/MADS solver; bridge supplies only its target contract
            strict_board=strict_board,
            proxy_board=proxy_board,
            position=position,
            tactical_plan=plan,
            shot_index=actual_shot_index,
            seeds=seeds,
            deadline=deadline,
        )
        if result is None:
            attempts.append(PhysxGoalAttempt(
                request.request_id, int(request.priority), "NOT_FOUND_WITHIN_BUDGET",
                {
                    "coverage_status": request.coverage_status,
                    "reason": "no certified clear-path Newton/MADS result under this search budget; not physical infeasibility",
                },
            ))
            continue
        evaluation, detail = result
        attempts.append(PhysxGoalAttempt(
            request.request_id, int(request.priority), "CERTIFIED_CLEAR_PATH",
            {**detail, "coverage_status": request.coverage_status, "rule_legal": bool(evaluation.rule_legal)},
            (float(evaluation.candidate.v0), float(evaluation.candidate.h0), float(evaluation.candidate.w0)),
        ))
        break
    return tuple(attempts)


def solve_single_collision_requests(
    requests: Sequence[BoundCollisionGoalRequest],
    local_board: Iterable[Mapping[str, Any]],
    *,
    own_throw_number: int,
    physics_seeds: int = 3,
    match_seed: int = 20260717,
    decision_budget_seconds: float = 30.0,
    shot_index: int | None = None,
    solver: ProxyMatchPlayer | None = None,
) -> tuple[PhysxGoalAttempt, ...]:
    """Run existing MADS only for a bound, exact-single-out collision request.

    The legacy MADS objective permits a target pushed to a tactical dead zone
    under its generic ``physical_clear`` label.  This wrapper adds the v2
    contract's stronger postcondition: the *bound target slot* must be disabled
    in every final PhysX sequence.
    """

    if not 1 <= int(own_throw_number) <= 8:
        raise ValueError("own_throw_number must be 1..8")
    if int(physics_seeds) < 1 or float(decision_budget_seconds) <= 0.0:
        raise ValueError("physics_seeds and decision_budget_seconds must be positive")
    actual_shot_index = 2 * (int(own_throw_number) - 1) if shot_index is None else int(shot_index)
    if not 0 <= actual_shot_index <= 15:
        raise ValueError("shot_index must be 0..15")
    strict_board, proxy_board = _as_board(local_board)
    if any(stone.index == actual_shot_index for stone in strict_board):
        raise ValueError("active shot slot is already occupied on the input board")
    engine = solver or ProxyMatchPlayer(
        physics_seeds=int(physics_seeds), parent_regions=1, decision_budget_seconds=float(decision_budget_seconds),
    )
    deadline = time.perf_counter() + float(decision_budget_seconds)
    seeds = [int(match_seed) + actual_shot_index * 7919 + 104729 * offset for offset in range(int(physics_seeds))]
    position = make_position(strict_board)
    attempts: list[PhysxGoalAttempt] = []

    for request in sorted(requests, key=lambda item: int(item.priority)):
        if time.perf_counter() >= deadline:
            attempts.append(PhysxGoalAttempt(
                request.request_id, int(request.priority), "NOT_ATTEMPTED_BUDGET_EXHAUSTED",
                {"reason": "previous ordered collision requests consumed the configured total budget"},
            ))
            continue
        if not any(stone.index == int(request.target_opponent_index) and stone.owner == "opponent" for stone in strict_board):
            attempts.append(PhysxGoalAttempt(
                request.request_id, int(request.priority), "TARGET_BINDING_NOT_PRESENT",
                {"target_opponent_index": int(request.target_opponent_index)},
            ))
            continue
        plan = collision_plan_for_request(request, own_throw_number=int(own_throw_number), shot_index=actual_shot_index)
        result = engine._try_fast_targeted_hit_roll(  # existing coarse-proxy -> strict PhysX -> MADS single-hit solver
            strict_board=strict_board,
            proxy_board=proxy_board,
            position=position,
            tactical_plan=plan,
            shot_index=actual_shot_index,
            seeds=seeds,
            deadline=deadline,
        )
        if result is None:
            attempts.append(PhysxGoalAttempt(
                request.request_id, int(request.priority), "NOT_FOUND_WITHIN_BUDGET",
                {"reason": "no certified single-target MADS result under this search budget; not physical infeasibility"},
            ))
            continue
        evaluation, detail = result
        if not _target_is_out_in_every_seed(evaluation, int(request.target_opponent_index)):
            attempts.append(PhysxGoalAttempt(
                request.request_id, int(request.priority), "REJECTED_TARGET_NOT_OUT_OF_PLAY",
                {
                    "target_opponent_index": int(request.target_opponent_index),
                    "reason": "legacy MADS returned a tactical dead-zone clear, but v2 contract requires actual OUT_OF_PLAY in every seed",
                },
            ))
            continue
        attempts.append(PhysxGoalAttempt(
            request.request_id, int(request.priority), "CERTIFIED_SINGLE_TARGET_OUT",
            {**detail, "coverage_status": request.coverage_status, "rule_legal": bool(evaluation.rule_legal)},
            (float(evaluation.candidate.v0), float(evaluation.candidate.h0), float(evaluation.candidate.w0)),
        ))
        break
    return tuple(attempts)
