"""Numeric, local-coordinate classifier for the first-player macro graph.

This module is deliberately a state recogniser only.  It does not choose a
shot, treat a centre guard as an invulnerable shield, or bypass the local
competition-rule / PhysX layers.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Mapping

from planning_proxy.competition_rules import FRONT_HOG_Y, HOUSE_R, HOUSE_X, HOUSE_Y


# These reproduce the NWNHT macro-feature convention after translating a
# local board to button-relative coordinates.  They are state features, not
# official scoring/FGZ definitions.
CENTRE_LANE_HALF_WIDTH = 0.38
STATE_HOUSE_RADIUS = HOUSE_R
FRONT_GUARD_Y_MAX = FRONT_HOG_Y - HOUSE_Y

# Derived from nwnht_first_player_macro_state_graph_v1_supported.json with
# minimum support 250.  The raw geometries remain observable, but route to a
# PhysX-only fallback instead of receiving an unsupported learned policy.
LOW_SUPPORT_RAW_BY_K: dict[int, frozenset[str]] = {
    1: frozenset(),
    2: frozenset({"SPARSE_OPEN"}),
    3: frozenset({"EMPTY", "CROWDED_HOUSE_SEARCH_REQUIRED", "MIXED_CONTESTED", "SPARSE_OPEN"}),
    4: frozenset({"EMPTY", "MIXED_CONTESTED", "SPARSE_OPEN"}),
    5: frozenset({"EMPTY", "MIXED_CONTESTED", "SPARSE_OPEN"}),
    6: frozenset({"EMPTY", "MIXED_CONTESTED", "SPARSE_OPEN"}),
    7: frozenset({"EMPTY", "MIXED_CONTESTED", "SPARSE_OPEN"}),
    8: frozenset({"EMPTY", "MIXED_CONTESTED", "SPARSE_OPEN"}),
}


@dataclass(frozen=True)
class MacroStateStone:
    index: int
    owner: str
    x: float
    y: float
    enabled: bool = True


@dataclass(frozen=True)
class FirstPlayerMacroState:
    own_throw_number: int
    state_id: str
    raw_macro_state: str
    macro_state: str
    physx_detail_required: bool
    features: dict[str, float]


def _as_stones(board: Iterable[object]) -> list[MacroStateStone]:
    stones: list[MacroStateStone] = []
    for item in board:
        if isinstance(item, Mapping):
            stone = MacroStateStone(
                index=int(item["index"]), owner=str(item["owner"]), x=float(item["x"]), y=float(item["y"]), enabled=bool(item.get("enabled", True))
            )
        else:
            stone = MacroStateStone(
                index=int(getattr(item, "index")), owner=str(getattr(item, "owner")), x=float(getattr(item, "x")), y=float(getattr(item, "y")), enabled=bool(getattr(item, "enabled", True))
            )
        if stone.enabled:
            stones.append(stone)
    return stones


def _relative(stone: MacroStateStone) -> tuple[float, float]:
    """Convert local PhysX board coordinates to NWNHT-style button-relative m."""
    return stone.x - HOUSE_X, stone.y - HOUSE_Y


def _features(stones: list[MacroStateStone], own_owner: str, opponent_owner: str) -> dict[str, float]:
    result: dict[str, float] = {}
    by_owner = {"first": [stone for stone in stones if stone.owner == own_owner], "opponent": [stone for stone in stones if stone.owner == opponent_owner]}
    in_house_all: list[tuple[float, str]] = []
    for prefix, owned in by_owner.items():
        result[f"{prefix}_visible"] = float(len(owned))
        in_house = guards = centre_guards = centre_house = 0
        for stone in owned:
            x_rel, y_rel = _relative(stone)
            radius = math.hypot(x_rel, y_rel)
            inside = radius <= STATE_HOUSE_RADIUS
            front_guard = STATE_HOUSE_RADIUS < y_rel <= FRONT_GUARD_Y_MAX
            centre = abs(x_rel) <= CENTRE_LANE_HALF_WIDTH
            in_house += int(inside)
            guards += int(front_guard)
            centre_guards += int(front_guard and centre)
            centre_house += int(inside and centre)
            if inside:
                in_house_all.append((radius, prefix))
        result[f"{prefix}_in_house"] = float(in_house)
        result[f"{prefix}_guards"] = float(guards)
        result[f"{prefix}_centre_guards"] = float(centre_guards)
        result[f"{prefix}_centre_house"] = float(centre_house)
    in_house_all.sort()
    result["first_currently_scoring"] = float(bool(in_house_all) and in_house_all[0][1] == "first")
    result["opponent_currently_scoring"] = float(bool(in_house_all) and in_house_all[0][1] == "opponent")
    return result


def raw_macro_type(features: Mapping[str, float]) -> str:
    """Exact priority order of the supported macro-state artifact."""
    total_visible = features["first_visible"] + features["opponent_visible"]
    total_house = features["first_in_house"] + features["opponent_in_house"]
    if total_visible == 0:
        return "EMPTY"
    if total_visible >= 5 and total_house >= 3:
        return "CROWDED_HOUSE_SEARCH_REQUIRED"
    if features["opponent_centre_guards"] >= 1 and features["opponent_in_house"] >= 1:
        return "OPPONENT_CENTRE_SHELL"
    if features["first_centre_guards"] >= 1 and features["first_in_house"] >= 1:
        return "OWN_CENTRE_SHELL"
    if features["opponent_currently_scoring"] >= 1 and features["opponent_in_house"] >= 1:
        return "OPPONENT_HOUSE_THREAT"
    if features["first_currently_scoring"] >= 1 and features["first_in_house"] >= 1:
        return "OWN_HOUSE_CONTROL"
    if total_house == 0 and features["first_guards"] + features["opponent_guards"] >= 1:
        return "GUARD_EXCHANGE"
    if total_visible <= 2:
        return "SPARSE_OPEN"
    return "MIXED_CONTESTED"


def classify_first_player_macro_state(
    own_throw_number: int,
    board: Iterable[object],
    *,
    own_owner: str = "self",
    opponent_owner: str = "opponent",
) -> FirstPlayerMacroState:
    """Return the local-board macro state for first player's K1..K8 decision."""
    if not 1 <= int(own_throw_number) <= 8:
        raise ValueError("own_throw_number must be in 1..8")
    features = _features(_as_stones(board), own_owner=own_owner, opponent_owner=opponent_owner)
    raw = raw_macro_type(features)
    macro = "LOW_SUPPORT_SEARCH_REQUIRED" if raw in LOW_SUPPORT_RAW_BY_K[int(own_throw_number)] else raw
    requires_physx = macro in {"CROWDED_HOUSE_SEARCH_REQUIRED", "OPPONENT_CENTRE_SHELL", "OWN_CENTRE_SHELL", "LOW_SUPPORT_SEARCH_REQUIRED"}
    return FirstPlayerMacroState(
        own_throw_number=int(own_throw_number),
        state_id=f"FIRST_K{int(own_throw_number)}_{macro}",
        raw_macro_state=raw,
        macro_state=macro,
        physx_detail_required=requires_physx,
        features=features,
    )
