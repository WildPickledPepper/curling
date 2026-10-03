#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Instantiate a semantic G_k as current-board terminal constraints.

This is intentionally the boundary between the data MDP and a later inverse
path solver.  It binds only current-board *roles* (for example, one current
opponent house stone), never fictitious NWNHT stone identities.  It does not
choose v/h/w or establish physical reachability.
"""

from __future__ import annotations

import itertools
import math
from typing import Any, Iterable, Mapping

from training_data.nwnht_curling.causal_state_machine.extract_anonymous_goal_templates import house_count, zone_counts
from training_data.nwnht_curling.causal_state_machine.partition_states_v2 import macro_type
from training_data.nwnht_curling.causal_state_machine.state_features_v2 import state_features


MAX_DYNAMIC_BINDINGS = 3


def _stone_ref(stone: Mapping[str, Any], runtime_index: int) -> dict[str, Any]:
    """Keep a stable local id when supplied; otherwise expose a role locator."""

    ref: dict[str, Any] = {
        "owner": str(stone["owner"]),
        "runtime_index": runtime_index,
        "x_m": round(float(stone["x_m"]), 6),
        "y_m": round(float(stone["y_m"]), 6),
        "distance_to_button_m": round(math.hypot(float(stone["x_m"]), float(stone["y_m"])), 6),
    }
    for field in ("id", "index", "stone_id"):
        if field in stone:
            ref[field] = stone[field]
            break
    return ref


def _opponent_sets(board: list[Mapping[str, Any]], house_count_to_remove: int, total_count_to_remove: int) -> list[list[dict[str, Any]]]:
    """Bind only out-of-play removals to a small set of current-board roles."""

    opponents = [(index, stone) for index, stone in enumerate(board) if str(stone["owner"]) == "opponent"]
    house = [
        (index, stone) for index, stone in opponents
        if house_count(zone_counts([stone], "opponent")) == 1
    ]
    if total_count_to_remove > len(opponents) or house_count_to_remove > len(house):
        return []
    result: list[list[dict[str, Any]]] = []
    for house_group in itertools.combinations(house, house_count_to_remove):
        remaining = [(index, stone) for index, stone in opponents if (index, stone) not in house_group]
        for other_group in itertools.combinations(remaining, total_count_to_remove - house_count_to_remove):
            chosen = [*house_group, *other_group]
            result.append([_stone_ref(stone, index) for index, stone in chosen])
    result.sort(key=lambda group: sum(float(item["distance_to_button_m"]) for item in group))
    return result[:MAX_DYNAMIC_BINDINGS]


def _semantic_transition_met(before: list[Mapping[str, Any]], after: list[Mapping[str, Any]], k: int, goal_state: Mapping[str, Any]) -> bool:
    """Anonymous board-level acceptance; no claim of persistent same-colour ID."""

    effect = goal_state["semantic_effect"]
    before_first = house_count(zone_counts(before, "first"))
    before_opponent = house_count(zone_counts(before, "opponent"))
    after_first = house_count(zone_counts(after, "first"))
    after_opponent = house_count(zone_counts(after, "opponent"))
    total_opponent_before = sum(str(stone["owner"]) == "opponent" for stone in before)
    total_opponent_after = sum(str(stone["owner"]) == "opponent" for stone in after)
    if after_first - before_first != int(effect["first_house_delta"]):
        return False
    if after_opponent - before_opponent != int(effect["opponent_house_delta"]):
        return False
    if total_opponent_before - total_opponent_after != int(effect["opponent_removed_count"]):
        return False
    features = state_features(int(k), list(after))
    predicate = goal_state["semantic_terminal_predicate"]
    return str(features["control"]) == str(predicate["control"]) and str(macro_type(features)) == str(predicate["macro"])


def instantiate_goal_contracts(
    board: Iterable[Mapping[str, Any]], candidate: Mapping[str, Any], *,
    fine_options_override: Iterable[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Bind one selected MDP G to the current board, yielding <=3 contracts."""

    current = [dict(stone) for stone in board]
    goal_state = candidate["goal_state"]
    k = int(candidate["K"])
    if int(goal_state["K"]) != k:
        raise ValueError("G.K must equal S.K")
    effect = goal_state["semantic_effect"]
    # ``opponent_house_removed_count`` is an anonymous *house occupancy*
    # decrease.  A stone may leave the house but remain in play, so only the
    # overlap with total visible removals can be required to be out of play.
    required_total_out = max(0, int(effect["opponent_removed_count"]))
    required_house_out = max(0, min(
        int(effect["opponent_house_removed_count"]),
        required_total_out,
    ))
    removal_sets = _opponent_sets(
        current,
        required_house_out,
        required_total_out,
    )
    if required_total_out == 0:
        removal_sets = [[]]

    contracts: list[dict[str, Any]] = []
    fine_options = list(goal_state.get("fine_goal_options", [])) if fine_options_override is None else [dict(item) for item in fine_options_override]
    for fine_index, fine in enumerate(fine_options):
        for binding in removal_sets:
            contracts.append({
                "contract_id": f"{goal_state['goal_id']}:fine:{fine_index}:binding:{len(contracts)}",
                "state_id": str(candidate["source_state"]),
                "K": k,
                "goal_id": str(goal_state["goal_id"]),
                "semantic_effect": dict(effect),
                "semantic_terminal_predicate": dict(goal_state["semantic_terminal_predicate"]),
                "permitted_exact_post_own_topologies": list(goal_state.get("post_own_topology_distribution", [])),
                "required_removed_stones": binding,
                "active_final_region": fine.get("active_final_region"),
                "stone_constraints_when_unambiguous": fine.get("stone_constraints_when_unambiguous", []),
                "dynamic_house_removal_binding_request": fine.get("dynamic_house_removal_binding_request"),
                "after_own_occupancy": fine.get("after_own_occupancy", {}),
                "historical_fine_support": int(fine.get("historical_support", fine.get("neighbour_support", 0))),
                "execution_status": "CONTRACT_READY_FOR_PATH_SEARCH",
                "acceptance_rule": "After own shot, semantic deltas/control/macro must match; required bound stones must be out of play when an identity-preserving simulator can verify them.",
            })
            if len(contracts) >= MAX_DYNAMIC_BINDINGS:
                break
        if len(contracts) >= MAX_DYNAMIC_BINDINGS:
            break

    status = (
        "CONTRACT_READY_FOR_PATH_SEARCH" if contracts else
        "SEMANTIC_ONLY_NO_BINDABLE_FINE_IMPLEMENTATION" if goal_state.get("fine_execution_status") == "NO_HISTORICAL_BINDABLE_FINE_IMPLEMENTATION" else
        "SEMANTIC_CONTRACT_BINDING_UNSATISFIED_ON_CURRENT_BOARD"
    )
    return {
        "state_id": str(candidate["source_state"]),
        "K": k,
        "goal_id": str(goal_state["goal_id"]),
        "contract_status": status,
        "semantic_goal": dict(goal_state),
        "contracts": contracts,
        "fine_option_source": "GLOBAL_GOAL_LIBRARY" if fine_options_override is None else "CONTEXTUAL_NEAREST_NEIGHBOURS",
        "expected_after_opponent_reply_distribution": list(candidate["after_opponent_reply_state_distribution"]),
        "warning": "Contracts define desired post-own board conditions only. A solver miss is not physical impossibility, and the reply distribution is not an opponent guarantee.",
    }


def instantiate_recommendation(board: Iterable[Mapping[str, Any]], recommendation: Mapping[str, Any]) -> dict[str, Any]:
    """Instantiate primary then fallbacks without silently replacing a failed G."""

    primary = recommendation.get("primary_goal")
    if not isinstance(primary, Mapping):
        return {"state_id": recommendation.get("state_id"), "K": recommendation.get("K"), "primary": None, "fallbacks": [], "contract_status": "NO_SEMANTIC_GOAL"}
    return {
        "state_id": recommendation["state_id"], "K": recommendation["K"],
        "primary": instantiate_goal_contracts(board, primary),
        "fallbacks": [instantiate_goal_contracts(board, candidate) for candidate in recommendation.get("fallback_goals", []) if isinstance(candidate, Mapping)],
    }


def semantic_transition_met(before: Iterable[Mapping[str, Any]], after: Iterable[Mapping[str, Any]], contract: Mapping[str, Any]) -> bool:
    """Replay-check one semantic contract/result only; identities are separate.

    ``instantiate_goal_contracts`` returns an envelope containing
    ``semantic_goal``, while an individual emitted contract keeps the same
    fields flat.  Accept both forms so the strict-PhysX bridge can validate
    the exact contract it was asked to solve, rather than a neighbouring
    contract from the envelope.
    """

    goal_state = contract.get("semantic_goal")
    if not isinstance(goal_state, Mapping):
        goal_state = {
            "K": int(contract["K"]),
            "semantic_effect": dict(contract["semantic_effect"]),
            "semantic_terminal_predicate": dict(contract["semantic_terminal_predicate"]),
        }

    return _semantic_transition_met(
        [dict(stone) for stone in before], [dict(stone) for stone in after],
        int(contract["K"]), goal_state,
    )
