"""Independent multi-target MADS for v2 double-outcome contracts.

This solver is intentionally separate from the legacy single-target hit-roll
method.  Its hard outcome is not "clear something": two *bound* target slots
must be out of play and the anonymous whole-board topology must match the
data-derived double outcome contract.
"""

from __future__ import annotations

import math
import time
from typing import Any, Iterable, Mapping, Sequence

import numpy as np

from local_simulator.examples.train_policy_tree_selfplay import STONE_COUNT, StrictCurlingEnd
from local_simulator.runtime_loader import install_bundled_pyphysx
from planning_proxy.analytic_proxy import attack_score, calibrate_force_lookup, calibrate_from_recovered_formula, make_initial_candidates, simulate_batch
from planning_proxy.strict_refine import Candidate, evaluate_one, make_position

from .double_outcome_goal import (
    BoundDoubleTargets, anonymous_topology_mismatch, anonymous_topology_mismatch_features,
    double_outcome_contract_met,
)
from .physx_goal_bridge import PhysxGoalAttempt, _as_board


FULL_GRID = (7, 41, 15)
DEFAULT_PARENT_LIMIT = 3
DEFAULT_MAX_ITERATIONS = 4


def _clamp(values: np.ndarray) -> np.ndarray:
    return np.asarray((
        np.clip(values[0], 1.0, 6.0), np.clip(values[1], -2.23, 2.23), np.clip(values[2], -15.7, 15.7),
    ), dtype=np.float64)


def _pseudo_states(final_board: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Restore a full enabled/disabled vector from StrictEvaluation export."""

    states: list[dict[str, Any]] = [{"enabled": False, "x": 0.0, "y": 0.0} for _ in range(STONE_COUNT)]
    for stone in final_board:
        index = int(stone["index"])
        if 0 <= index < STONE_COUNT:
            states[index] = {"enabled": bool(stone.get("enabled", True)), "x": float(stone["x"]), "y": float(stone["y"])}
    return states


def _mads_directions(iteration: int) -> list[np.ndarray]:
    phase = (iteration + 1) * 2.399963229728653
    diagonal = np.asarray((math.cos(phase), math.sin(phase), math.cos(phase * 0.6180339887498948)), dtype=np.float64)
    diagonal /= max(float(np.linalg.norm(diagonal)), 1.0e-12)
    directions = [diagonal, -diagonal]
    for axis in range(3):
        unit = np.zeros(3, dtype=np.float64)
        unit[axis] = 1.0
        directions.extend((unit, -unit))
    return directions


def select_double_parent_rows(coarse: Any, coarse_shots: np.ndarray, target_indices: tuple[int, int], *, parent_limit: int) -> list[int]:
    """Balance first-contact topology before filling with global attack score.

    A double clear can start by hitting either target.  A global score is often
    dominated by the easier/closer target, so selecting its top three rows is
    not legitimate coverage of the double-collision search space.
    """

    if parent_limit < 1:
        return []
    rows = np.flatnonzero(np.isin(coarse.first_hit_index, target_indices))
    if not len(rows):
        return []
    by_target = {
        target: rows[coarse.first_hit_index[rows] == target]
        for target in target_indices
    }
    scores = {
        target: attack_score(coarse, protected_opponent_indices=set(), must_clear_index=target)
        for target in target_indices
    }
    selected: list[int] = []
    seen_spins: set[int] = set()

    # First reserve one branch for each available first-hit target.  Iterate
    # target order deterministically; a spin collision falls through to the
    # next row for that target rather than deleting the topology altogether.
    for target in target_indices:
        ordered = by_target[target][np.argsort(-scores[target][by_target[target]])]
        for row in ordered:
            spin = int(round(float(coarse_shots[int(row)][2]) * 1000.0))
            if spin in seen_spins:
                continue
            seen_spins.add(spin)
            selected.append(int(row))
            break
        if len(selected) >= parent_limit:
            return selected

    combined = np.maximum(scores[target_indices[0]], scores[target_indices[1]])
    for row in rows[np.argsort(-combined[rows])]:
        spin = int(round(float(coarse_shots[int(row)][2]) * 1000.0))
        if int(row) in selected or spin in seen_spins:
            continue
        seen_spins.add(spin)
        selected.append(int(row))
        if len(selected) >= parent_limit:
            break
    return selected


def _double_result(
    contract: Mapping[str, Any], target_indices: tuple[int, int], evaluation: Any,
    initial_board: Sequence[Mapping[str, Any]], *, own_throw_number: int, active_index: int,
    mirrored_from_runtime_board: bool,
) -> tuple[bool, int, int]:
    """Return (exactly_met, max_targets_remaining, max_topology_mismatch)."""

    final_boards = getattr(evaluation, "final_boards", ())
    if not final_boards or not bool(getattr(evaluation, "rule_legal", False)):
        return False, 2, 10_000
    remaining, topology = 0, 0
    all_met = True
    for final_board in final_boards:
        states = _pseudo_states(final_board)
        remaining = max(remaining, sum(bool(states[index]["enabled"]) for index in target_indices))
        topology = max(topology, anonymous_topology_mismatch(
            contract, final_states=states, initial_local_board=initial_board,
            own_throw_number=int(own_throw_number), active_index=int(active_index),
            mirrored_from_runtime_board=bool(mirrored_from_runtime_board),
        ))
        all_met = all_met and double_outcome_contract_met(
            contract, target_indices=target_indices, final_states=states, initial_local_board=initial_board,
            own_throw_number=int(own_throw_number), active_index=int(active_index),
            mirrored_from_runtime_board=bool(mirrored_from_runtime_board),
        )
    return bool(all_met), int(remaining), int(topology)


def _mismatch_feature_names(
    contract: Mapping[str, Any], evaluation: Any, initial_board: Sequence[Mapping[str, Any],],
    *, own_throw_number: int, active_index: int, mirrored_from_runtime_board: bool,
) -> list[str]:
    """Union failed anonymous terminal predicates across strict friction runs."""

    names: set[str] = set()
    for final_board in getattr(evaluation, "final_boards", ()):
        names.update(anonymous_topology_mismatch_features(
            contract, final_states=_pseudo_states(final_board), initial_local_board=initial_board,
            own_throw_number=int(own_throw_number), active_index=int(active_index),
            mirrored_from_runtime_board=bool(mirrored_from_runtime_board),
        ))
    return sorted(names)


def solve_double_outcome_contract(
    contract: Mapping[str, Any], target_sets: Sequence[BoundDoubleTargets], local_board: Iterable[Mapping[str, Any]],
    *, own_throw_number: int, mirrored_from_runtime_board: bool, physics_seeds: int = 3,
    match_seed: int = 20260717, decision_budget_seconds: float = 45.0, shot_index: int | None = None,
    parent_limit: int = DEFAULT_PARENT_LIMIT, max_iterations: int = DEFAULT_MAX_ITERATIONS,
) -> tuple[PhysxGoalAttempt, ...]:
    """Try bounded target pairs with strict-PhysX multi-objective MADS.

    A failure is always a configured-search miss.  It is deliberately not
    interpreted as the double goal being physically impossible.
    """

    required_out = int(contract.get("semantic_effect", {}).get("opponent_removed_count", contract.get("required_opponent_removed_count", 0)))
    if required_out != 2:
        raise ValueError("double MADS requires a two-opponent-out contract")
    if not 1 <= int(own_throw_number) <= 8 or int(physics_seeds) < 1:
        raise ValueError("invalid own_throw_number or physics_seeds")
    if parent_limit < 1 or max_iterations < 1 or float(decision_budget_seconds) <= 0.0:
        raise ValueError("invalid MADS budget")
    active_index = 2 * (int(own_throw_number) - 1) if shot_index is None else int(shot_index)
    # Keep one materialised copy: ``local_board`` is part of the public API and
    # may be a generator.  Passing it through _as_board first would consume it,
    # silently turning the later anonymous-topology check into an empty board.
    raw_board = list(local_board)
    strict_board, proxy_board = _as_board(raw_board)
    if any(stone.index == active_index for stone in strict_board):
        raise ValueError("active shot slot is already occupied on the input board")
    # ``StrictCurlingEnd`` imports the native binding lazily at scene creation.
    # Match the existing strict-refine/runtime entrypoints rather than relying
    # on a developer-specific Conda environment.
    install_bundled_pyphysx()
    engine = StrictCurlingEnd(seed=0, training_fast=True)
    params, lookup = calibrate_from_recovered_formula(), calibrate_force_lookup()
    position = make_position(strict_board)
    seeds = [int(match_seed) + active_index * 7919 + 104729 * offset for offset in range(int(physics_seeds))]
    deadline = time.perf_counter() + float(decision_budget_seconds)
    attempts: list[PhysxGoalAttempt] = []

    for target_set in target_sets:
        targets = tuple(int(index) for index in target_set.target_indices)
        request_id = f"{contract.get('double_goal_id', 'double')}|targets={targets[0]},{targets[1]}"
        if time.perf_counter() >= deadline:
            attempts.append(PhysxGoalAttempt(request_id, int(target_set.priority), "NOT_ATTEMPTED_BUDGET_EXHAUSTED", {"reason": "previous target sets consumed total budget"}))
            continue
        if len(targets) != 2 or any(not any(stone.index == target and stone.owner == "opponent" for stone in strict_board) for target in targets):
            attempts.append(PhysxGoalAttempt(request_id, int(target_set.priority), "TARGET_BINDING_NOT_PRESENT", {"target_indices": list(targets)}))
            continue

        coarse_shots = make_initial_candidates(
            velocity_count=FULL_GRID[0], lateral_count=FULL_GRID[1], spin_count=FULL_GRID[2],
        )
        coarse = simulate_batch(coarse_shots, proxy_board, params, force_lookup=lookup, dt=0.02)
        rows = np.flatnonzero(np.isin(coarse.first_hit_index, targets))
        if not len(rows):
            attempts.append(PhysxGoalAttempt(request_id, int(target_set.priority), "NO_COARSE_FIRST_HIT_BRANCH", {"coarseCandidateCount": int(len(coarse_shots)), "target_indices": list(targets)}))
            continue
        parent_rows = select_double_parent_rows(coarse, coarse_shots, targets, parent_limit=int(parent_limit))

        calls = 0
        legal_evaluations = 0
        # The failure report must distinguish three very different cases:
        # all tested throws are illegal; legal throws cannot clear both targets;
        # or a double clear is found but leaves the wrong next-board topology.
        # Rank only legal evaluations, since an illegal "better" collision is
        # not a tactical fallback.
        best_legal_outcome: tuple[int, int, int] | None = None
        best_legal_item: Any | None = None
        def evaluate(values: np.ndarray) -> tuple[float, Any] | None:
            nonlocal calls, legal_evaluations, best_legal_outcome, best_legal_item
            if time.perf_counter() >= deadline:
                return None
            values = _clamp(values)
            item = evaluate_one(
                engine, Candidate(float(values[0]), float(values[1]), float(values[2]), 1),
                strict_board, position, seeds, active_index, active_index=active_index, tactical_plan=None,
            )
            calls += len(seeds)
            met, remaining, mismatch = _double_result(
                contract, targets, item, raw_board, own_throw_number=int(own_throw_number), active_index=active_index,
                mirrored_from_runtime_board=bool(mirrored_from_runtime_board),
            )
            own_loss = max(getattr(item, "total_self_cleared", [0]), default=0)
            rule_legal = bool(getattr(item, "rule_legal", False))
            if rule_legal:
                legal_evaluations += 1
                outcome = (int(remaining), int(mismatch), int(own_loss))
                if best_legal_outcome is None or outcome < best_legal_outcome:
                    best_legal_outcome = outcome
                    best_legal_item = item
            penalty = (0.0 if rule_legal else 100_000.0) + 10_000.0 * remaining + 500.0 * mismatch + 5.0 * own_loss
            return (0.0 if met else penalty), item

        eligible: list[tuple[Any, float]] = []
        for row in parent_rows:
            current = _clamp(np.asarray(coarse_shots[row], dtype=np.float64))
            result = evaluate(current)
            if result is None:
                break
            score, item = result
            mesh = 1.0
            for iteration in range(int(max_iterations)):
                if score <= 0.0:
                    break
                best_score, best_values, best_item = score, current, item
                for direction in _mads_directions(iteration):
                    trial = _clamp(current + mesh * np.asarray((0.12, 0.12, 1.60), dtype=np.float64) * direction)
                    trial_result = evaluate(trial)
                    if trial_result is None:
                        break
                    trial_score, trial_item = trial_result
                    if trial_score < best_score:
                        best_score, best_values, best_item = trial_score, trial, trial_item
                if best_score < score:
                    current, score, item = best_values, best_score, best_item
                    mesh = min(1.0, mesh * 1.5)
                else:
                    mesh *= 0.5
                    if mesh < 1.0 / 16.0:
                        break
            met, remaining, mismatch = _double_result(
                contract, targets, item, raw_board, own_throw_number=int(own_throw_number), active_index=active_index,
                mirrored_from_runtime_board=bool(mirrored_from_runtime_board),
            )
            if met:
                eligible.append((item, score))

        if not eligible:
            failure_detail: dict[str, Any] = {
                "target_indices": list(targets), "coarseCandidateCount": int(len(coarse_shots)),
                "coarseHitBranchCount": int(len(rows)), "madsParentCount": len(parent_rows),
                "physicsCalls": calls, "ruleLegalEvaluationCount": legal_evaluations,
                "reason": "no rule-legal two-target-out plus whole-board-topology result under this configured search budget; not physical infeasibility",
            }
            if best_legal_outcome is None:
                failure_detail["bestLegalTargetsRemaining"] = None
                failure_detail["bestLegalTopologyMismatch"] = None
                failure_detail["diagnosis"] = "no rule-legal strict evaluation was observed"
            else:
                failure_detail["bestLegalTargetsRemaining"] = best_legal_outcome[0]
                failure_detail["bestLegalTopologyMismatch"] = best_legal_outcome[1]
                failure_detail["bestLegalOwnStonesCleared"] = best_legal_outcome[2]
                failure_detail["bestLegalTopologyMismatchFeatures"] = _mismatch_feature_names(
                    contract, best_legal_item, raw_board, own_throw_number=int(own_throw_number),
                    active_index=active_index, mirrored_from_runtime_board=bool(mirrored_from_runtime_board),
                )
                failure_detail["diagnosis"] = (
                    "double clear observed but required anonymous next-board topology was not met"
                    if best_legal_outcome[0] == 0 and best_legal_outcome[1] > 0
                    else "no rule-legal double clear was observed"
                )
            attempts.append(PhysxGoalAttempt(
                request_id, int(target_set.priority), "NOT_FOUND_WITHIN_BUDGET",
                failure_detail,
            ))
            continue
        chosen, score = min(eligible, key=lambda row: row[1])
        attempts.append(PhysxGoalAttempt(
            request_id, int(target_set.priority), "CERTIFIED_DOUBLE_OUTCOME",
            {"target_indices": list(targets), "coarseCandidateCount": int(len(coarse_shots)), "coarseHitBranchCount": int(len(rows)), "madsParentCount": len(parent_rows), "physicsCalls": calls, "rule_legal": bool(chosen.rule_legal), "whole_board_topology_met": True, "finalBoards": chosen.final_boards},
            (float(chosen.candidate.v0), float(chosen.candidate.h0), float(chosen.candidate.w0)),
        ))
        break
    return tuple(attempts)
