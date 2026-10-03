"""Runtime binding and strict final-board checks for anonymous double goals.

Historical data cannot reliably identify the delivered stone after a collision,
but strict PhysX can identify every runtime slot.  This module bridges that
asymmetry: targets are bound to current opponent house slots; the post-shot
result is checked as an *anonymous whole-board topology* in the v2 canonical
frame.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

from planning_proxy.competition_rules import HOUSE_R, HOUSE_X, HOUSE_Y, STONE_R
from training_data.nwnht_curling.causal_state_machine.partition_states_v2 import macro_type
from training_data.nwnht_curling.causal_state_machine.state_features_v2 import state_features
from .semantic_goal_contract import semantic_transition_met


@dataclass(frozen=True)
class BoundDoubleTargets:
    target_indices: tuple[int, int]
    priority: int


def bind_double_target_sets(
    contract: Mapping[str, Any], local_board: Iterable[Mapping[str, Any]], *, max_sets: int = 6,
) -> tuple[BoundDoubleTargets, ...]:
    """Enumerate current-house target pairs; closest-to-button pair is first."""

    # New semantic GoalContracts already bind anonymous historical roles to
    # concrete current PhysX slots.  Prefer that exact identity binding over
    # rebuilding a possibly different pair from the local house order.
    explicit = list(contract.get("required_removed_stones", []))
    if int(contract.get("semantic_effect", {}).get("opponent_removed_count", -1)) == 2 and len(explicit) == 2 and all("index" in stone for stone in explicit):
        targets = tuple(sorted(int(stone["index"]) for stone in explicit))
        return (BoundDoubleTargets(targets, 1),)
    binding = contract.get("target_binding")
    if (
        not isinstance(binding, Mapping)
        or str(binding.get("binding_mode")) != "DYNAMIC_OPPONENT_HOUSE_SET"
        or int(binding.get("choose_count", 0)) != 2
        or int(contract.get("required_opponent_removed_count", 0)) != 2
        or max_sets < 1
    ):
        return ()
    opponents = [
        stone for stone in local_board
        if bool(stone.get("enabled", True)) and str(stone.get("owner")) == "opponent"
        and math.hypot(float(stone["x"]) - HOUSE_X, float(stone["y"]) - HOUSE_Y) <= HOUSE_R + STONE_R
    ]
    pairs = sorted(
        itertools.combinations(opponents, 2),
        key=lambda pair: (
            min(math.hypot(float(item["x"]) - HOUSE_X, float(item["y"]) - HOUSE_Y) for item in pair),
            sum(math.hypot(float(item["x"]) - HOUSE_X, float(item["y"]) - HOUSE_Y) for item in pair),
            tuple(sorted(int(item["index"]) for item in pair)),
        ),
    )
    return tuple(
        BoundDoubleTargets(tuple(sorted((int(pair[0]["index"]), int(pair[1]["index"])))), rank)
        for rank, pair in enumerate(pairs[:max_sets], start=1)
    )


def _canonical_final_board(
    final_states: Sequence[Mapping[str, Any]], initial_local_board: Iterable[Mapping[str, Any]],
    *, active_index: int, mirrored_from_runtime_board: bool,
) -> list[dict[str, Any]]:
    owners = {
        int(stone["index"]): str(stone["owner"])
        for stone in initial_local_board if bool(stone.get("enabled", True))
    }
    owners[int(active_index)] = "self"
    board: list[dict[str, Any]] = []
    for index, state in enumerate(final_states):
        if not bool(state.get("enabled", False)) or owners.get(index) not in {"self", "opponent"}:
            continue
        x = float(state["x"]) - HOUSE_X
        if mirrored_from_runtime_board:
            x = -x
        board.append({
            "owner": "first" if owners[index] == "self" else "opponent",
            "x_m": x, "y_m": float(state["y"]) - HOUSE_Y,
        })
    return board


def double_outcome_contract_met(
    contract: Mapping[str, Any], *, target_indices: Sequence[int], final_states: Sequence[Mapping[str, Any]],
    initial_local_board: Iterable[Mapping[str, Any]], own_throw_number: int, active_index: int,
    mirrored_from_runtime_board: bool,
) -> bool:
    """Check both named targets out and every anonymous v2 terminal feature."""

    required_out = int(contract.get("semantic_effect", {}).get("opponent_removed_count", contract.get("required_opponent_removed_count", 0)))
    if len(target_indices) != 2 or required_out != 2:
        return False
    if any(index < 0 or index >= len(final_states) or bool(final_states[index].get("enabled", False)) for index in target_indices):
        return False
    if isinstance(contract.get("semantic_effect"), Mapping):
        canonical_after = _canonical_final_board(
            final_states, initial_local_board, active_index=int(active_index),
            mirrored_from_runtime_board=bool(mirrored_from_runtime_board),
        )
        canonical_before = [
            {"owner": "first" if str(stone["owner"]) == "self" else "opponent", "x_m": float(stone["x"]) - HOUSE_X, "y_m": float(stone["y"]) - HOUSE_Y}
            for stone in initial_local_board if bool(stone.get("enabled", True))
        ]
        if bool(mirrored_from_runtime_board):
            for stone in canonical_before:
                stone["x_m"] = -float(stone["x_m"])
        if not semantic_transition_met(canonical_before, canonical_after, contract):
            return False
        region = contract.get("active_final_region")
        if isinstance(region, Mapping):
            active = final_states[int(active_index)] if 0 <= int(active_index) < len(final_states) else None
            if not isinstance(active, Mapping) or not bool(active.get("enabled", False)):
                return False
            x_m = float(active["x"]) - HOUSE_X
            if bool(mirrored_from_runtime_board):
                x_m = -x_m
            y_m = float(active["y"]) - HOUSE_Y
            if (x_m - float(region["centre_x_m"])) ** 2 + (y_m - float(region["centre_y_m"])) ** 2 > float(region["radius_m"]) ** 2 + 1.0e-9:
                return False
        return True
    if not isinstance(contract.get("terminal_board_predicate"), Mapping):
        return False
    return anonymous_topology_mismatch(
        contract, final_states=final_states, initial_local_board=initial_local_board,
        own_throw_number=own_throw_number, active_index=active_index,
        mirrored_from_runtime_board=mirrored_from_runtime_board,
    ) == 0


def anonymous_topology_mismatch(
    contract: Mapping[str, Any], *, final_states: Sequence[Mapping[str, Any]],
    initial_local_board: Iterable[Mapping[str, Any]], own_throw_number: int, active_index: int,
    mirrored_from_runtime_board: bool,
) -> int:
    """Number of unsatisfied anonymous terminal features; zero is an exact match."""

    return len(anonymous_topology_mismatch_features(
        contract, final_states=final_states, initial_local_board=initial_local_board,
        own_throw_number=own_throw_number, active_index=active_index,
        mirrored_from_runtime_board=mirrored_from_runtime_board,
    ))


def anonymous_topology_mismatch_features(
    contract: Mapping[str, Any], *, final_states: Sequence[Mapping[str, Any]],
    initial_local_board: Iterable[Mapping[str, Any]], own_throw_number: int, active_index: int,
    mirrored_from_runtime_board: bool,
) -> tuple[str, ...]:
    """Return named terminal predicates that fail, for search diagnostics."""

    if isinstance(contract.get("semantic_effect"), Mapping):
        # Target-slot status is diagnosed separately by the MADS solver; this
        # label identifies that the remaining whole-board G predicate failed.
        return ("SEMANTIC_GK",)
    predicate = contract.get("terminal_board_predicate")
    if not isinstance(predicate, Mapping):
        return ("INVALID_TERMINAL_BOARD_PREDICATE",)
    features = state_features(
        int(own_throw_number),
        _canonical_final_board(
            final_states, initial_local_board, active_index=int(active_index),
            mirrored_from_runtime_board=bool(mirrored_from_runtime_board),
        ),
    )
    mismatch: list[str] = []
    for name, expected in predicate.items():
        actual = macro_type(features) if name == "macro" else features.get(name)
        if str(actual) != str(expected):
            mismatch.append(str(name))
    return tuple(mismatch)
