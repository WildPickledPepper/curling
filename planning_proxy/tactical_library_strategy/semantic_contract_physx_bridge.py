"""Strictly validate a contextual semantic placement contract with PhysX.

This is deliberately a narrow, independent bridge.  The data MDP selects a
same-K semantic goal and the retriever supplies an active-stone circle.  This
module asks the existing clear-path coarse-proxy -> PhysX Newton/MADS solver
for that circle, then checks the *complete simulated board* against the
selected semantic contract in every physics seed.

It does not turn a removal, hit-and-roll, or double-out contract into a draw.
Those need their own bound collision solvers.  A search miss is explicitly a
budget/algorithm result, never a proof that the tactical goal is unreachable.
"""

from __future__ import annotations

import concurrent.futures
import ctypes
import os
import time
from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping, Sequence

import numpy as np

from planning_proxy.analytic_proxy import calibrate_force_lookup, calibrate_from_recovered_formula, make_initial_candidates, simulate_batch
from planning_proxy.competition_rules import HOUSE_X, HOUSE_Y
from planning_proxy.evaluate_vs_teammate_ppo import ProxyMatchPlayer
from planning_proxy.strict_refine import Candidate, evaluate_one, make_position

from .physx_goal_bridge import (
    PLACEMENT_KIND, BoundCollisionGoalRequest, _as_board, collision_plan_for_request, draw_plan_for_circle,
)
from .semantic_goal_contract import semantic_transition_met
from .v2_circle_goal_adapter import CircleGoalRequest


@dataclass(frozen=True)
class SemanticPhysxAttempt:
    """One strict attempt; status names intentionally distinguish miss/reject."""

    contract_id: str
    priority: int
    status: str
    detail: dict[str, Any]
    bestshot: tuple[float, float, float] | None = None

    def to_json(self) -> dict[str, Any]:
        result = asdict(self)
        if self.bestshot is not None:
            result["bestshot"] = list(self.bestshot)
        return result


def canonical_board_to_local(board: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Convert tactical canonical coordinates to the existing local PhysX frame."""

    local: list[dict[str, Any]] = []
    for runtime_index, stone in enumerate(board):
        if not bool(stone.get("enabled", True)):
            continue
        owner = str(stone["owner"])
        if owner not in {"first", "opponent"}:
            raise ValueError("canonical board owner must be first or opponent")
        local.append({
            "index": int(stone.get("index", runtime_index)),
            "owner": "self" if owner == "first" else "opponent",
            "x": HOUSE_X + float(stone["x_m"]),
            "y": HOUSE_Y + float(stone["y_m"]),
            "yaw": float(stone.get("yaw", 0.0)),
            "enabled": True,
        })
    return local


def _final_board_to_canonical(final_board: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "index": int(stone["index"]),
            "owner": "first" if str(stone["owner"]) == "self" else "opponent",
            "x_m": float(stone["x"]) - HOUSE_X,
            "y_m": float(stone["y"]) - HOUSE_Y,
            "yaw": float(stone.get("yaw", 0.0)),
        }
        for stone in final_board
        if bool(stone.get("enabled", True))
    ]


def _active_circle_met(final_board: Iterable[Mapping[str, Any]], *, active_index: int, region: Mapping[str, Any]) -> bool:
    if str(region.get("shape", "circle")).lower() != "circle":
        return False
    centre_x, centre_y, radius = (float(region[key]) for key in ("centre_x_m", "centre_y_m", "radius_m"))
    active = next((stone for stone in final_board if int(stone["index"]) == int(active_index)), None)
    if active is None:
        return False
    dx = float(active["x"]) - HOUSE_X - centre_x
    dy = float(active["y"]) - HOUSE_Y - centre_y
    return dx * dx + dy * dy <= radius * radius + 1.0e-9


def _bound_removals_met(final_board: Iterable[Mapping[str, Any]], contract: Mapping[str, Any]) -> bool:
    final_indices = {int(stone["index"]) for stone in final_board if bool(stone.get("enabled", True))}
    return all(int(stone["index"]) not in final_indices for stone in contract.get("required_removed_stones", []))


def _strict_semantic_contract_met(
    before: Iterable[Mapping[str, Any]], final_boards: Iterable[Iterable[Mapping[str, Any]]],
    contract: Mapping[str, Any], *, active_index: int, rule_legal: bool,
) -> bool:
    """One acceptance predicate shared by placement and collision routes."""

    region = contract.get("active_final_region")
    boards = [list(board) for board in final_boards]
    return (
        bool(rule_legal)
        and bool(boards)
        and all(_bound_removals_met(final, contract) for final in boards)
        and all(region is None or _active_circle_met(final, active_index=active_index, region=region) for final in boards)
        and all(semantic_transition_met(before, _final_board_to_canonical(final), contract) for final in boards)
    )


def _screen_last_reply(final_boards: Iterable[Iterable[Mapping[str, Any]]], *, match_seed: int) -> tuple[bool, dict[str, Any]]:
    """Bounded strict-PhysX opponent-last-shot screen for each K8 final seed.

    A pass means no counterexample in the fixed direct/impact parent families;
    it is deliberately not called an absolute safe position.
    """

    from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd
    from local_simulator.runtime_loader import install_bundled_pyphysx
    from planning_proxy.strict_refine import BoardStone
    from planning_proxy.validate_final_defence import DefenceFixture, evaluate_fixture

    install_bundled_pyphysx()
    reports: list[dict[str, Any]] = []
    for seed_offset, final in enumerate(final_boards):
        stones = tuple(
            BoardStone(int(stone["index"]), str(stone["owner"]), float(stone["x"]), float(stone["y"]), yaw=float(stone.get("yaw", 0.0)))
            for stone in final if bool(stone.get("enabled", True))
        )
        if not stones or any(stone.index == 15 for stone in stones):
            return False, {"reason": "invalid K8 final board for opponent slot 15", "reports": reports}
        report = evaluate_fixture(
            DefenceFixture(f"semantic_k8_seed_{seed_offset}", "semantic K8 final", "runtime final board", stones),
            StrictCurlingEnd(seed=int(match_seed) + seed_offset, training_fast=True),
            direct_count=1, impact_count=1, physics_seeds=(int(match_seed) + seed_offset * 104729,),
            stop_on_first_counterexample=True,
        )
        reports.append(report)
    safe = all(bool(report["screenedSafe"]) for report in reports)
    return safe, {
        "reply_search": "bounded strict PhysX: 1 direct parent + 1 impact parent, stop at first counterexample per own final seed",
        "screened_safe": safe,
        "counterexample_count": sum(int(report["counterexampleCandidateCount"]) for report in reports),
        "reports": reports,
    }


def _placement_request(contract: Mapping[str, Any], priority: int) -> CircleGoalRequest | None:
    effect = contract.get("semantic_effect", {})
    region = contract.get("active_final_region")
    if (
        not isinstance(region, Mapping)
        or str(region.get("shape", "circle")).lower() != "circle"
        or int(effect.get("opponent_removed_count", 0)) != 0
        or contract.get("required_removed_stones")
    ):
        return None
    return CircleGoalRequest(
        request_id=str(contract["contract_id"]), priority=int(priority),
        source_state=str(contract["state_id"]), action_id=str(contract["goal_id"]),
        action_precision_level="CONTEXTUAL_SEMANTIC_CONTRACT", action_kind=PLACEMENT_KIND,
        local_centre_x=HOUSE_X + float(region["centre_x_m"]),
        local_centre_y=HOUSE_Y + float(region["centre_y_m"]), radius_m=float(region["radius_m"]),
        coverage_status="CONTEXTUAL_FINE_REGION",
        expected_next_state_distribution=(),
        evidence_note="Contextual fine circle; strict final boards must satisfy this contract's semantic G_k.",
    )


def solve_semantic_placement_contracts(
    canonical_before_board: Iterable[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
    *,
    own_throw_number: int,
    physics_seeds: int = 3,
    match_seed: int = 20260717,
    decision_budget_seconds: float = 10.0,
    solver: ProxyMatchPlayer | None = None,
) -> tuple[SemanticPhysxAttempt, ...]:
    """Attempt ordered placement contracts and certify their full G_k predicate.

    The input board is the tactical module's canonical board (`first` is our
    side, button at `(0, 0)`).  This first bridge assumes our regular slots
    `0,2,...,14`, so `K` is both the MDP step and the active local shot slot.
    """

    if not 1 <= int(own_throw_number) <= 8:
        raise ValueError("own_throw_number must be 1..8")
    if int(physics_seeds) < 1 or float(decision_budget_seconds) <= 0.0:
        raise ValueError("physics_seeds and decision_budget_seconds must be positive")
    before = [dict(stone) for stone in canonical_before_board if bool(stone.get("enabled", True))]
    local_board = canonical_board_to_local(before)
    active_index = 2 * (int(own_throw_number) - 1)
    if any(int(stone["index"]) == active_index for stone in local_board):
        raise ValueError("active first-player shot slot is already occupied")
    strict_board, proxy_board = _as_board(local_board)
    # Keep unsupported contracts cheap: only initialise a PhysX scene once a
    # placement contract has passed the tactical-interface checks.
    engine = solver
    deadline = time.perf_counter() + float(decision_budget_seconds)
    seeds = [int(match_seed) + active_index * 7919 + 104729 * offset for offset in range(int(physics_seeds))]
    position = make_position(strict_board)
    attempts: list[SemanticPhysxAttempt] = []

    for priority, contract in enumerate(contracts, start=1):
        request = _placement_request(contract, priority)
        if request is None:
            attempts.append(SemanticPhysxAttempt(
                str(contract.get("contract_id", "unknown")), priority, "UNSUPPORTED_NONPLACEMENT_CONTRACT",
                {"reason": "This bridge admits only zero-removal contracts with an active circle; collision goals remain separate."},
            ))
            continue
        if int(contract.get("K", -1)) != int(own_throw_number):
            attempts.append(SemanticPhysxAttempt(
                str(contract["contract_id"]), priority, "REJECTED_CROSS_K_CONTRACT",
                {"contract_K": contract.get("K"), "own_throw_number": int(own_throw_number)},
            ))
            continue
        if time.perf_counter() >= deadline:
            attempts.append(SemanticPhysxAttempt(str(contract["contract_id"]), priority, "NOT_ATTEMPTED_BUDGET_EXHAUSTED", {}))
            continue
        if engine is None:
            engine = ProxyMatchPlayer(
                physics_seeds=int(physics_seeds), parent_regions=1, decision_budget_seconds=float(decision_budget_seconds),
            )
        plan = draw_plan_for_circle(request, own_throw_number=int(own_throw_number), shot_index=active_index)
        result = engine._try_fast_targeted_draw(
            strict_board=strict_board, proxy_board=proxy_board, position=position,
            tactical_plan=plan, shot_index=active_index, seeds=seeds, deadline=deadline,
        )
        if result is None:
            attempts.append(SemanticPhysxAttempt(
                str(contract["contract_id"]), priority, "NOT_FOUND_WITHIN_CURRENT_SEARCH_BUDGET",
                {"reason": "Current coarse-proxy/Newton/MADS budget produced no certified route; this is not physical infeasibility."},
            ))
            continue
        evaluation, detail = result
        final_boards = list(getattr(evaluation, "final_boards", []))
        accepted = len(final_boards) == len(seeds) and _strict_semantic_contract_met(
            before, final_boards, contract, active_index=active_index, rule_legal=bool(getattr(evaluation, "rule_legal", False)),
        )
        if not accepted:
            attempts.append(SemanticPhysxAttempt(
                str(contract["contract_id"]), priority, "REJECTED_BY_STRICT_SEMANTIC_CONTRACT",
                {**detail, "rule_legal": bool(getattr(evaluation, "rule_legal", False)), "physics_final_board_count": len(final_boards)},
            ))
            continue
        if int(own_throw_number) == 8:
            reply_safe, reply_detail = _screen_last_reply(final_boards, match_seed=int(match_seed))
            if not reply_safe:
                attempts.append(SemanticPhysxAttempt(
                    str(contract["contract_id"]), priority, "REJECTED_BY_OPPONENT_LAST_REPLY_SEARCH",
                    {**detail, "last_reply_search": reply_detail},
                ))
                continue
        attempts.append(SemanticPhysxAttempt(
            str(contract["contract_id"]), priority, "CERTIFIED_SEMANTIC_CONTRACT",
            {**detail, "rule_legal": True, "physics_final_board_count": len(final_boards)},
            (float(evaluation.candidate.v0), float(evaluation.candidate.h0), float(evaluation.candidate.w0)),
        ))
        break
    return tuple(attempts)


def _single_removal_request(contract: Mapping[str, Any], priority: int) -> BoundCollisionGoalRequest | None:
    """Bind one identity-preserving semantic removal contract to legacy MADS."""

    effect = contract.get("semantic_effect", {})
    targets = list(contract.get("required_removed_stones", []))
    region = contract.get("active_final_region")
    if (
        int(effect.get("opponent_removed_count", 0)) != 1
        or len(targets) != 1
        or "index" not in targets[0]
        or not isinstance(region, Mapping)
        or str(region.get("shape", "circle")).lower() != "circle"
    ):
        return None
    return BoundCollisionGoalRequest(
        request_id=str(contract["contract_id"]), priority=int(priority), collision_goal_id=str(contract["contract_id"]),
        source_state=str(contract["state_id"]), tactical_goal_id=str(contract["goal_id"]),
        target_opponent_index=int(targets[0]["index"]),
        local_centre_x=HOUSE_X + float(region["centre_x_m"]), local_centre_y=HOUSE_Y + float(region["centre_y_m"]),
        radius_m=float(region["radius_m"]), coverage_status="CONTEXTUAL_FINE_REGION",
        expected_next_state_distribution=(),
    )


def solve_semantic_single_removal_contracts(
    canonical_before_board: Iterable[Mapping[str, Any]], contracts: Sequence[Mapping[str, Any]], *,
    own_throw_number: int, physics_seeds: int = 3, match_seed: int = 20260717,
    decision_budget_seconds: float = 20.0, solver: ProxyMatchPlayer | None = None,
) -> tuple[SemanticPhysxAttempt, ...]:
    """Coarse proxy -> strict PhysX MADS for exact-one-out semantic contracts.

    The old hit-roll solver supplies collision-topology initialisation only.
    Its legacy 'tactically dead' acceptance is ignored: this bridge certifies
    only actual out-of-play identity bindings plus the full semantic `G_k`.
    """

    if not 1 <= int(own_throw_number) <= 8:
        raise ValueError("own_throw_number must be 1..8")
    if int(physics_seeds) < 1 or float(decision_budget_seconds) <= 0.0:
        raise ValueError("physics_seeds and decision_budget_seconds must be positive")
    before = [dict(stone) for stone in canonical_before_board if bool(stone.get("enabled", True))]
    local_board = canonical_board_to_local(before)
    active_index = 2 * (int(own_throw_number) - 1)
    strict_board, proxy_board = _as_board(local_board)
    if any(stone.index == active_index for stone in strict_board):
        raise ValueError("active first-player shot slot is already occupied")
    engine = solver
    deadline = time.perf_counter() + float(decision_budget_seconds)
    seeds = [int(match_seed) + active_index * 7919 + 104729 * offset for offset in range(int(physics_seeds))]
    position = make_position(strict_board)
    attempts: list[SemanticPhysxAttempt] = []
    for priority, contract in enumerate(contracts, start=1):
        request = _single_removal_request(contract, priority)
        if request is None:
            attempts.append(SemanticPhysxAttempt(str(contract.get("contract_id", "unknown")), priority, "UNSUPPORTED_SINGLE_REMOVAL_CONTRACT", {
                "reason": "Requires exactly one bound target, one active final circle, and one opponent out-of-play semantic effect."}))
            continue
        if int(contract.get("K", -1)) != int(own_throw_number):
            attempts.append(SemanticPhysxAttempt(str(contract["contract_id"]), priority, "REJECTED_CROSS_K_CONTRACT", {}))
            continue
        if time.perf_counter() >= deadline:
            attempts.append(SemanticPhysxAttempt(str(contract["contract_id"]), priority, "NOT_ATTEMPTED_BUDGET_EXHAUSTED", {}))
            continue
        if engine is None:
            engine = ProxyMatchPlayer(physics_seeds=int(physics_seeds), parent_regions=1, decision_budget_seconds=float(decision_budget_seconds))
        plan = collision_plan_for_request(request, own_throw_number=int(own_throw_number), shot_index=active_index)
        result = engine._try_fast_targeted_hit_roll(
            strict_board=strict_board, proxy_board=proxy_board, position=position,
            tactical_plan=plan, shot_index=active_index, seeds=seeds, deadline=deadline,
        )
        if result is None:
            attempts.append(SemanticPhysxAttempt(str(contract["contract_id"]), priority, "NOT_FOUND_WITHIN_CURRENT_SEARCH_BUDGET", {
                "reason": "Current coarse-proxy/MADS budget produced no candidate; not physical infeasibility."}))
            continue
        evaluation, detail = result
        final_boards = list(getattr(evaluation, "final_boards", []))
        accepted = len(final_boards) == len(seeds) and _strict_semantic_contract_met(
            before, final_boards, contract, active_index=active_index, rule_legal=bool(getattr(evaluation, "rule_legal", False)),
        )
        if not accepted:
            attempts.append(SemanticPhysxAttempt(str(contract["contract_id"]), priority, "REJECTED_BY_STRICT_SEMANTIC_CONTRACT", {
                **detail, "rule_legal": bool(getattr(evaluation, "rule_legal", False)), "physics_final_board_count": len(final_boards),
            }))
            continue
        if int(own_throw_number) == 8:
            reply_safe, reply_detail = _screen_last_reply(final_boards, match_seed=int(match_seed))
            if not reply_safe:
                attempts.append(SemanticPhysxAttempt(
                    str(contract["contract_id"]), priority, "REJECTED_BY_OPPONENT_LAST_REPLY_SEARCH",
                    {**detail, "last_reply_search": reply_detail},
                ))
                continue
        attempts.append(SemanticPhysxAttempt(
            str(contract["contract_id"]), priority, "CERTIFIED_SEMANTIC_CONTRACT",
            {**detail, "rule_legal": True, "physics_final_board_count": len(final_boards), "solver": "coarse_proxy_then_strict_physx_mads_single_collision"},
            (float(evaluation.candidate.v0), float(evaluation.candidate.h0), float(evaluation.candidate.w0)),
        ))
        break
    return tuple(attempts)


def _solve_one_single_removal_contract_worker(
    canonical_before_board: list[dict[str, Any]], contract: dict[str, Any], own_throw_number: int,
    physics_seeds: int, match_seed: int, decision_budget_seconds: float, worker_core: int,
) -> SemanticPhysxAttempt:
    _limit_worker_to_one_core(worker_core)
    attempt = solve_semantic_single_removal_contracts(
        canonical_before_board, [contract], own_throw_number=int(own_throw_number), physics_seeds=int(physics_seeds),
        match_seed=int(match_seed), decision_budget_seconds=float(decision_budget_seconds), solver=None,
    )[0]
    return SemanticPhysxAttempt(attempt.contract_id, 1, attempt.status, {
        **attempt.detail, "parallel_worker_core": int(worker_core), "worker_thread_limit": 1,
    }, attempt.bestshot)


def solve_semantic_single_removal_contracts_parallel(
    canonical_before_board: Iterable[Mapping[str, Any]], contracts: Sequence[Mapping[str, Any]], *,
    own_throw_number: int, physics_seeds: int = 3, match_seed: int = 20260717,
    decision_budget_seconds: float = 20.0, max_workers: int | None = None,
) -> tuple[SemanticPhysxAttempt, ...]:
    """Parallel one-core MADS attempts for alternative bindings/fine circles."""

    if not contracts:
        return ()
    before = [dict(stone) for stone in canonical_before_board if bool(stone.get("enabled", True))]
    cpu_limit = min(max(1, int(os.cpu_count() or 1)), 64)
    worker_count = min(len(contracts), cpu_limit, int(max_workers) if max_workers is not None else cpu_limit)
    if worker_count < 1:
        raise ValueError("max_workers must be positive")
    if worker_count == 1:
        return tuple(SemanticPhysxAttempt(
            item.contract_id, priority, item.status, item.detail, item.bestshot,
        ) for priority, contract in enumerate(contracts, start=1) for item in solve_semantic_single_removal_contracts(
            before, [dict(contract)], own_throw_number=int(own_throw_number), physics_seeds=int(physics_seeds),
            match_seed=int(match_seed), decision_budget_seconds=float(decision_budget_seconds), solver=None,
        ))
    context = __import__("multiprocessing").get_context("spawn")
    completed: list[tuple[int, SemanticPhysxAttempt]] = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=worker_count, mp_context=context) as executor:
        futures = {
            executor.submit(
                _solve_one_single_removal_contract_worker, before, dict(contract), int(own_throw_number),
                int(physics_seeds), int(match_seed), float(decision_budget_seconds), (priority - 1) % cpu_limit,
            ): (priority, dict(contract))
            for priority, contract in enumerate(contracts, start=1)
        }
        for future in concurrent.futures.as_completed(futures):
            priority, contract = futures[future]
            try:
                attempt = future.result()
            except Exception as error:
                attempt = SemanticPhysxAttempt(str(contract.get("contract_id", "unknown")), priority, "WORKER_EXECUTION_ERROR", {
                    "error_type": type(error).__name__, "message": str(error),
                })
            completed.append((priority, SemanticPhysxAttempt(
                attempt.contract_id, priority, attempt.status, attempt.detail, attempt.bestshot,
            )))
    return tuple(attempt for _, attempt in sorted(completed, key=lambda item: item[0]))


def solve_semantic_double_removal_contracts(
    canonical_before_board: Iterable[Mapping[str, Any]], contracts: Sequence[Mapping[str, Any]], *,
    own_throw_number: int, physics_seeds: int = 3, match_seed: int = 20260717,
    decision_budget_seconds: float = 45.0,
) -> tuple[SemanticPhysxAttempt, ...]:
    """Run the independent coarse-proxy/strict-PhysX double MADS on semantic Gs."""

    from .double_mads_solver import solve_double_outcome_contract
    from .double_outcome_goal import bind_double_target_sets

    before = [dict(stone) for stone in canonical_before_board if bool(stone.get("enabled", True))]
    local = canonical_board_to_local(before)
    attempts: list[SemanticPhysxAttempt] = []
    for priority, contract in enumerate(contracts, start=1):
        if int(contract.get("K", -1)) != int(own_throw_number):
            attempts.append(SemanticPhysxAttempt(str(contract.get("contract_id", "unknown")), priority, "REJECTED_CROSS_K_CONTRACT", {}))
            continue
        targets = bind_double_target_sets(contract, local, max_sets=1)
        if not targets:
            attempts.append(SemanticPhysxAttempt(str(contract.get("contract_id", "unknown")), priority, "UNSUPPORTED_DOUBLE_REMOVAL_CONTRACT", {
                "reason": "Requires two explicit current opponent slot bindings."}))
            continue
        result = solve_double_outcome_contract(
            contract, targets, local, own_throw_number=int(own_throw_number), mirrored_from_runtime_board=False,
            physics_seeds=int(physics_seeds), match_seed=int(match_seed), decision_budget_seconds=float(decision_budget_seconds),
        )
        for item in result:
            if item.status != "CERTIFIED_DOUBLE_OUTCOME":
                attempts.append(SemanticPhysxAttempt(str(contract["contract_id"]), priority, item.status, dict(item.detail), item.bestshot))
                continue
            final_boards = item.detail.get("finalBoards", [])
            if int(own_throw_number) == 8:
                reply_safe, reply_detail = _screen_last_reply(final_boards, match_seed=int(match_seed))
                if not reply_safe:
                    attempts.append(SemanticPhysxAttempt(str(contract["contract_id"]), priority, "REJECTED_BY_OPPONENT_LAST_REPLY_SEARCH", {
                        **item.detail, "last_reply_search": reply_detail,
                    }, item.bestshot))
                    continue
            attempts.append(SemanticPhysxAttempt(str(contract["contract_id"]), priority, "CERTIFIED_SEMANTIC_CONTRACT", {
                **item.detail, "solver": "coarse_proxy_then_strict_physx_mads_double_collision",
            }, item.bestshot))
            return tuple(attempts)
    return tuple(attempts)


def _mixed_contract_penalty(
    before: Sequence[Mapping[str, Any]], final_board: Sequence[Mapping[str, Any]], contract: Mapping[str, Any], *, active_index: int,
    rule_legal: bool,
) -> float:
    """Dense MADS score for a mixed collision, with exact G as zero only."""

    if not rule_legal:
        return 10_000.0
    region = contract.get("active_final_region")
    active_error = 3.0
    if isinstance(region, Mapping):
        active = next((stone for stone in final_board if int(stone["index"]) == int(active_index)), None)
        if active is not None:
            distance = ((float(active["x"]) - HOUSE_X - float(region["centre_x_m"])) ** 2 + (float(active["y"]) - HOUSE_Y - float(region["centre_y_m"])) ** 2) ** 0.5
            active_error = max(0.0, distance - float(region["radius_m"]))
    # The discontinuous topology predicate is a hard tier; distance provides
    # local direction only inside a compatible collision branch.
    semantic_ok = _strict_semantic_contract_met(before, [final_board], contract, active_index=active_index, rule_legal=True)
    return float(active_error if semantic_ok else 100.0 + active_error)


def solve_semantic_mixed_collision_contracts(
    canonical_before_board: Iterable[Mapping[str, Any]], contracts: Sequence[Mapping[str, Any]], *,
    own_throw_number: int, physics_seeds: int = 3, match_seed: int = 20260717,
    decision_budget_seconds: float = 30.0, parent_limit: int = 4, max_iterations: int = 4,
) -> tuple[SemanticPhysxAttempt, ...]:
    """Solve zero-out mixed collision Gs without pretending they are draws.

    It deliberately searches both clear and contact coarse branches.  The
    final acceptance remains the same complete semantic contract as the other
    solvers; a hit that merely looks plausible is never accepted.
    """

    from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd
    from local_simulator.runtime_loader import install_bundled_pyphysx

    if not 1 <= int(own_throw_number) <= 8 or int(physics_seeds) < 1:
        raise ValueError("invalid own_throw_number or physics_seeds")
    before = [dict(stone) for stone in canonical_before_board if bool(stone.get("enabled", True))]
    local = canonical_board_to_local(before)
    strict_board, proxy_board = _as_board(local)
    active_index = 2 * (int(own_throw_number) - 1)
    if any(stone.index == active_index for stone in strict_board):
        raise ValueError("active first-player shot slot is already occupied")
    position = make_position(strict_board)
    install_bundled_pyphysx()
    engine = StrictCurlingEnd(seed=0, training_fast=True)
    params, lookup = calibrate_from_recovered_formula(), calibrate_force_lookup()
    seeds = [int(match_seed) + active_index * 7919 + 104729 * offset for offset in range(int(physics_seeds))]
    deadline = time.perf_counter() + float(decision_budget_seconds)
    attempts: list[SemanticPhysxAttempt] = []

    def clamp(values: np.ndarray) -> np.ndarray:
        return np.asarray((np.clip(values[0], 1.0, 6.0), np.clip(values[1], -2.23, 2.23), np.clip(values[2], -15.7, 15.7)), dtype=np.float64)

    for priority, contract in enumerate(contracts, start=1):
        effect = contract.get("semantic_effect", {})
        region = contract.get("active_final_region")
        if int(contract.get("K", -1)) != int(own_throw_number) or int(effect.get("opponent_removed_count", -1)) != 0 or not isinstance(region, Mapping):
            attempts.append(SemanticPhysxAttempt(str(contract.get("contract_id", "unknown")), priority, "UNSUPPORTED_MIXED_COLLISION_CONTRACT", {
                "reason": "Requires same-K zero-opponent-out contract with an active final circle."}))
            continue
        if time.perf_counter() >= deadline:
            attempts.append(SemanticPhysxAttempt(str(contract["contract_id"]), priority, "NOT_ATTEMPTED_BUDGET_EXHAUSTED", {}))
            continue
        coarse_shots = make_initial_candidates(velocity_count=7, lateral_count=41, spin_count=15)
        coarse = simulate_batch(coarse_shots, proxy_board, params, force_lookup=lookup, dt=0.02)
        target = np.asarray((HOUSE_X + float(region["centre_x_m"]), HOUSE_Y + float(region["centre_y_m"])), dtype=np.float64)
        distance = np.linalg.norm(coarse.stop_points - target, axis=1)
        # Preserve contact diversity: one closest clear lane and up to three
        # distinct first-hit branches, rather than a draw-biased nearest list.
        selected: list[int] = []
        clear = np.flatnonzero(coarse.first_hit_index < 0)
        if len(clear):
            selected.append(int(clear[np.argmin(distance[clear])]))
        for row in np.argsort(distance):
            if int(coarse.first_hit_index[row]) < 0:
                continue
            hit = int(coarse.first_hit_index[row])
            if any(int(coarse.first_hit_index[item]) == hit for item in selected if int(coarse.first_hit_index[item]) >= 0):
                continue
            selected.append(int(row))
            if len(selected) >= int(parent_limit):
                break
        if not selected:
            attempts.append(SemanticPhysxAttempt(str(contract["contract_id"]), priority, "NO_COARSE_BRANCH", {"coarseCandidateCount": int(len(coarse_shots))}))
            continue
        calls = 0
        best: Any | None = None
        for parent_rank, row in enumerate(selected, start=1):
            current = clamp(np.asarray(coarse_shots[row], dtype=np.float64))
            def evaluate(values: np.ndarray, multi_seed: bool = False) -> tuple[float, Any] | None:
                nonlocal calls
                if time.perf_counter() >= deadline:
                    return None
                used_seeds = seeds if multi_seed else seeds[:1]
                item = evaluate_one(engine, Candidate(float(values[0]), float(values[1]), float(values[2]), parent_rank),
                                    strict_board, position, used_seeds, active_index, active_index=active_index, tactical_plan=None)
                calls += len(used_seeds)
                penalty = max(_mixed_contract_penalty(before, board, contract, active_index=active_index, rule_legal=bool(item.rule_legal)) for board in item.final_boards)
                return penalty, item
            initial = evaluate(current)
            if initial is None:
                break
            score, item = initial
            mesh = 1.0
            for iteration in range(int(max_iterations)):
                if score <= 0.0:
                    break
                phase = (iteration + 1) * 2.399963229728653
                diagonal = np.asarray((np.cos(phase), np.sin(phase), np.cos(phase * 0.6180339887498948)))
                diagonal /= max(float(np.linalg.norm(diagonal)), 1.0e-12)
                directions = [diagonal, -diagonal] + [np.eye(3)[axis] for axis in range(3)] + [-np.eye(3)[axis] for axis in range(3)]
                best_score, best_values, best_item = score, current, item
                for direction in directions:
                    result = evaluate(clamp(current + mesh * np.asarray((0.12, 0.12, 1.60)) * direction))
                    if result is not None and result[0] < best_score:
                        best_score, best_values, best_item = result[0], clamp(current + mesh * np.asarray((0.12, 0.12, 1.60)) * direction), result[1]
                if best_score < score:
                    current, score, item = best_values, best_score, best_item
                    mesh = min(1.0, mesh * 1.5)
                else:
                    mesh *= 0.5
                    if mesh < 1.0 / 16.0:
                        break
            verified = evaluate(current, multi_seed=True)
            if verified is not None and verified[0] <= 0.0:
                best = verified[1]
                break
        if best is None:
            attempts.append(SemanticPhysxAttempt(str(contract["contract_id"]), priority, "NOT_FOUND_WITHIN_CURRENT_SEARCH_BUDGET", {
                "coarseCandidateCount": int(len(coarse_shots)), "madsParentCount": len(selected), "physicsCalls": calls,
                "reason": "No complete semantic mixed-collision result under this configured search budget; not physical infeasibility.",
            }))
            continue
        if int(own_throw_number) == 8:
            reply_safe, reply_detail = _screen_last_reply(best.final_boards, match_seed=int(match_seed))
            if not reply_safe:
                attempts.append(SemanticPhysxAttempt(str(contract["contract_id"]), priority, "REJECTED_BY_OPPONENT_LAST_REPLY_SEARCH", {"physicsCalls": calls, "last_reply_search": reply_detail}))
                continue
        attempts.append(SemanticPhysxAttempt(str(contract["contract_id"]), priority, "CERTIFIED_SEMANTIC_CONTRACT", {
            "coarseCandidateCount": int(len(coarse_shots)), "madsParentCount": len(selected), "physicsCalls": calls,
            "solver": "coarse_proxy_then_strict_physx_mads_mixed_collision",
        }, (float(best.candidate.v0), float(best.candidate.h0), float(best.candidate.w0))))
        break
    return tuple(attempts)


def _solve_one_mixed_collision_contract_worker(
    before: list[dict[str, Any]], contract: dict[str, Any], own_throw_number: int, physics_seeds: int,
    match_seed: int, decision_budget_seconds: float, worker_core: int,
) -> SemanticPhysxAttempt:
    _limit_worker_to_one_core(worker_core)
    attempt = solve_semantic_mixed_collision_contracts(
        before, [contract], own_throw_number=int(own_throw_number), physics_seeds=int(physics_seeds),
        match_seed=int(match_seed), decision_budget_seconds=float(decision_budget_seconds),
    )[0]
    return SemanticPhysxAttempt(attempt.contract_id, 1, attempt.status, {
        **attempt.detail, "parallel_worker_core": int(worker_core), "worker_thread_limit": 1,
    }, attempt.bestshot)


def solve_semantic_mixed_collision_contracts_parallel(
    canonical_before_board: Iterable[Mapping[str, Any]], contracts: Sequence[Mapping[str, Any]], *,
    own_throw_number: int, physics_seeds: int = 3, match_seed: int = 20260717,
    decision_budget_seconds: float = 30.0, max_workers: int | None = None,
) -> tuple[SemanticPhysxAttempt, ...]:
    """One-core process parallelism for alternate mixed-collision contracts."""

    if not contracts:
        return ()
    before = [dict(stone) for stone in canonical_before_board if bool(stone.get("enabled", True))]
    cpu_limit = min(max(1, int(os.cpu_count() or 1)), 64)
    worker_count = min(len(contracts), cpu_limit, int(max_workers) if max_workers is not None else cpu_limit)
    if worker_count < 1:
        raise ValueError("max_workers must be positive")
    if worker_count == 1:
        return tuple(SemanticPhysxAttempt(item.contract_id, priority, item.status, item.detail, item.bestshot)
                     for priority, contract in enumerate(contracts, start=1)
                     for item in solve_semantic_mixed_collision_contracts(
                         before, [dict(contract)], own_throw_number=int(own_throw_number), physics_seeds=int(physics_seeds),
                         match_seed=int(match_seed), decision_budget_seconds=float(decision_budget_seconds)))
    context = __import__("multiprocessing").get_context("spawn")
    completed: list[tuple[int, SemanticPhysxAttempt]] = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=worker_count, mp_context=context) as executor:
        futures = {
            executor.submit(_solve_one_mixed_collision_contract_worker, before, dict(contract), int(own_throw_number),
                            int(physics_seeds), int(match_seed), float(decision_budget_seconds), (priority - 1) % cpu_limit): (priority, dict(contract))
            for priority, contract in enumerate(contracts, start=1)
        }
        for future in concurrent.futures.as_completed(futures):
            priority, contract = futures[future]
            try:
                item = future.result()
            except Exception as error:
                item = SemanticPhysxAttempt(str(contract.get("contract_id", "unknown")), priority, "WORKER_EXECUTION_ERROR", {
                    "error_type": type(error).__name__, "message": str(error),
                })
            completed.append((priority, SemanticPhysxAttempt(item.contract_id, priority, item.status, item.detail, item.bestshot)))
    return tuple(item for _, item in sorted(completed, key=lambda row: row[0]))


def _limit_worker_to_one_core(core_index: int) -> None:
    """Best-effort one-core affinity plus one BLAS thread for a worker.

    The proxy's NumPy work must not multiply into ``workers × all cores``.
    Affinity is deliberately best-effort: restricted containers and processor
    groups may reject it, while the search itself remains valid.
    """

    for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
        os.environ[key] = "1"
    cpu_count = max(1, int(os.cpu_count() or 1))
    core = int(core_index) % min(cpu_count, 64)
    try:
        if os.name == "nt":
            # Windows affinity masks are group-local and up to 64 bits here.
            ctypes.windll.kernel32.SetProcessAffinityMask(  # type: ignore[attr-defined]
                ctypes.windll.kernel32.GetCurrentProcess(), ctypes.c_size_t(1 << core),
            )
        elif hasattr(os, "sched_setaffinity"):
            os.sched_setaffinity(0, {core})
    except (AttributeError, OSError):
        pass


def _solve_one_placement_contract_worker(
    canonical_before_board: list[dict[str, Any]], contract: dict[str, Any],
    own_throw_number: int, physics_seeds: int, match_seed: int,
    decision_budget_seconds: float, worker_core: int,
) -> SemanticPhysxAttempt:
    """Pickle-safe worker entrypoint; never shares a PhysX scene between jobs."""

    _limit_worker_to_one_core(worker_core)
    attempt = solve_semantic_placement_contracts(
        canonical_before_board, [contract], own_throw_number=int(own_throw_number),
        physics_seeds=int(physics_seeds), match_seed=int(match_seed),
        decision_budget_seconds=float(decision_budget_seconds), solver=None,
    )[0]
    return SemanticPhysxAttempt(
        attempt.contract_id, attempt.priority, attempt.status,
        {**attempt.detail, "parallel_worker_core": int(worker_core), "worker_thread_limit": 1},
        attempt.bestshot,
    )


def solve_semantic_placement_contracts_parallel(
    canonical_before_board: Iterable[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
    *,
    own_throw_number: int,
    physics_seeds: int = 3,
    match_seed: int = 20260717,
    decision_budget_seconds: float = 10.0,
    max_workers: int | None = None,
) -> tuple[SemanticPhysxAttempt, ...]:
    """Solve independent fine-circle alternatives concurrently, one core each.

    Each worker owns a new coarse-proxy model and a new strict PhysX scene; it
    never shares mutable physics state.  ``decision_budget_seconds`` applies
    **per contract**, so three circles on three cores cost roughly one search
    budget in wall-clock time, rather than three serial budgets.  Results stay
    sorted by original priority; the caller still chooses the first certified
    contract, preserving the tactical ordering.

    This parallelises only alternatives for one already-selected `S_k -> G_k`.
    It does not race different semantic G values and therefore cannot alter the
    data-MDP's tactical ranking.
    """

    if not 1 <= int(own_throw_number) <= 8:
        raise ValueError("own_throw_number must be 1..8")
    if int(physics_seeds) < 1 or float(decision_budget_seconds) <= 0.0:
        raise ValueError("physics_seeds and decision_budget_seconds must be positive")
    before = [dict(stone) for stone in canonical_before_board if bool(stone.get("enabled", True))]
    indexed = [(priority, dict(contract)) for priority, contract in enumerate(contracts, start=1)]
    if not indexed:
        return ()
    cpu_limit = min(max(1, int(os.cpu_count() or 1)), 64)
    worker_count = min(len(indexed), cpu_limit, int(max_workers) if max_workers is not None else cpu_limit)
    if worker_count < 1:
        raise ValueError("max_workers must be positive")
    if worker_count == 1:
        return tuple(SemanticPhysxAttempt(
            item.contract_id, priority, item.status, item.detail, item.bestshot,
        ) for priority, contract in indexed for item in solve_semantic_placement_contracts(
            before, [contract], own_throw_number=int(own_throw_number), physics_seeds=int(physics_seeds),
            match_seed=int(match_seed), decision_budget_seconds=float(decision_budget_seconds), solver=None,
        ))

    # Spawn is required on Windows and also prevents a copied PhysX scene on
    # Unix.  Every process imports and initialises its own simulator.
    context = __import__("multiprocessing").get_context("spawn")
    completed: list[tuple[int, SemanticPhysxAttempt]] = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=worker_count, mp_context=context) as executor:
        futures = {
            executor.submit(
                _solve_one_placement_contract_worker,
                before, contract, int(own_throw_number), int(physics_seeds), int(match_seed),
                float(decision_budget_seconds), (priority - 1) % cpu_limit,
            ): priority
            for priority, contract in indexed
        }
        for future in concurrent.futures.as_completed(futures):
            priority = futures[future]
            try:
                attempt = future.result()
            except Exception as error:  # worker crash is execution evidence, not a claimed no-solution
                contract = indexed[priority - 1][1]
                attempt = SemanticPhysxAttempt(
                    str(contract.get("contract_id", "unknown")), priority, "WORKER_EXECUTION_ERROR",
                    {"error_type": type(error).__name__, "message": str(error)},
                )
            # A one-contract worker naturally labels its own job priority as
            # one. Restore the caller's stable ordering before returning it.
            completed.append((priority, SemanticPhysxAttempt(
                attempt.contract_id, priority, attempt.status, attempt.detail, attempt.bestshot,
            )))
    return tuple(attempt for _, attempt in sorted(completed, key=lambda item: item[0]))
