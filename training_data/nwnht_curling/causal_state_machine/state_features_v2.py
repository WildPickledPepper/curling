#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministic geometry features for the first-player decision state.

This module is deliberately *before* clustering.  It consumes only the own
throw number ``K`` and the current button-centred stone coordinates.  It does
not read scores, teams, end numbers, calls, post-shot outcomes or PhysX.

The feature set is a reproducible starting partition, not an assertion that
all rows with the same key are tactically equivalent.  The next stage must use
the observed S -> U -> S' sequences to merge or split these micro-states.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

try:
    from .derive_action_effects import (
        CENTER_LANE_M,
        FRONT_GUARD_Y_MAX,
        HOUSE_RADIUS_M,
        board_facts,
    )
except ImportError:  # pragma: no cover - direct script invocation
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.derive_action_effects import (  # type: ignore
        CENTER_LANE_M,
        FRONT_GUARD_Y_MAX,
        HOUSE_RADIUS_M,
        board_facts,
    )


BUTTON_RADIUS_M = 0.6096
GUARD_NEAR_FAR_SPLIT_M = 4.14
PROTECTION_LATERAL_M = 0.42
PAIR_NEAR_M = 0.75
OWNERS = ("first", "opponent")


def _cap_2(value: int) -> str:
    """Use a small, interpretable count vocabulary in a state key."""

    return "2P" if value >= 2 else str(max(0, value))


def _as_stone(raw: Mapping[str, Any]) -> dict[str, float | str]:
    owner = str(raw.get("owner", ""))
    if owner not in OWNERS:
        raise ValueError(f"stone owner must be one of {OWNERS}, got {owner!r}")
    try:
        x, y = float(raw["x_m"]), float(raw["y_m"])
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("each stone needs finite x_m and y_m") from error
    if not math.isfinite(x) or not math.isfinite(y):
        raise ValueError("each stone needs finite x_m and y_m")
    return {"owner": owner, "x_m": x, "y_m": y}


def normalise_board(board: Iterable[Mapping[str, Any]]) -> list[dict[str, float | str]]:
    """Validate and copy just the runtime-safe geometry fields."""

    return [_as_stone(raw) for raw in board]


def _mirror(board: Sequence[Mapping[str, Any]]) -> list[dict[str, float | str]]:
    return [
        {"owner": str(stone["owner"]), "x_m": -float(stone["x_m"]), "y_m": float(stone["y_m"])}
        for stone in board
    ]


def _geometry_key(board: Sequence[Mapping[str, Any]]) -> tuple[tuple[str, float, float], ...]:
    """A stable, noise-tolerant key for choosing one left/right orientation."""

    return tuple(sorted(
        (str(stone["owner"]), round(float(stone["y_m"]), 3), round(float(stone["x_m"]), 3))
        for stone in board
    ))


def canonicalise_left_right(board: Iterable[Mapping[str, Any]]) -> tuple[list[dict[str, float | str]], bool]:
    """Return the lexicographically canonical board under x -> -x reflection.

    ``mirrored`` tells a later target compiler whether it must reflect a
    canonical target region back to the actual board.  It is deliberately not
    part of the state identity.
    """

    normal = normalise_board(board)
    reflected = _mirror(normal)
    if _geometry_key(reflected) < _geometry_key(normal):
        return reflected, True
    return normal, False


def stone_zone(stone: Mapping[str, Any]) -> str:
    """Classify a stone into a finite button-centred tactical zone."""

    x, y = float(stone["x_m"]), float(stone["y_m"])
    radius = math.hypot(x, y)
    if radius <= BUTTON_RADIUS_M:
        return "BUTTON"
    if radius <= HOUSE_RADIUS_M:
        return f"HOUSE_{'FRONT' if y >= 0.0 else 'BACK'}_{'LEFT' if x < 0.0 else 'RIGHT'}"
    if HOUSE_RADIUS_M < y <= FRONT_GUARD_Y_MAX:
        if abs(x) <= CENTER_LANE_M:
            lane = "CENTRE"
        else:
            lane = "LEFT" if x < 0.0 else "RIGHT"
        depth = "NEAR" if y <= GUARD_NEAR_FAR_SPLIT_M else "FAR"
        return f"GUARD_{depth}_{lane}"
    return "OUTSIDE_TACTICAL_ZONE"


HOUSE_ZONES = ("BUTTON", "HOUSE_FRONT_LEFT", "HOUSE_FRONT_RIGHT", "HOUSE_BACK_LEFT", "HOUSE_BACK_RIGHT")
GUARD_ZONES = (
    "GUARD_NEAR_CENTRE", "GUARD_FAR_CENTRE",
    "GUARD_NEAR_LEFT", "GUARD_FAR_LEFT",
    "GUARD_NEAR_RIGHT", "GUARD_FAR_RIGHT",
)


def _house_stones(board: Sequence[Mapping[str, Any]], owner: str) -> list[Mapping[str, Any]]:
    return [
        stone for stone in board
        if stone["owner"] == owner and math.hypot(float(stone["x_m"]), float(stone["y_m"])) <= HOUSE_RADIUS_M
    ]


def _guard_stones(board: Sequence[Mapping[str, Any]], owner: str) -> list[Mapping[str, Any]]:
    return [stone for stone in board if stone["owner"] == owner and stone_zone(stone).startswith("GUARD_")]


def _protected_house_count(board: Sequence[Mapping[str, Any]], owner: str) -> int:
    """Count geometrically covered own house stones; this is not a safety claim."""

    guards = _guard_stones(board, owner)
    return sum(
        any(float(guard["y_m"]) > float(stone["y_m"]) and abs(float(guard["x_m"]) - float(stone["x_m"])) <= PROTECTION_LATERAL_M
            for guard in guards)
        for stone in _house_stones(board, owner)
    )


def _nearest_depth_bin(board: Sequence[Mapping[str, Any]], owner: str) -> str:
    distances = [math.hypot(float(stone["x_m"]), float(stone["y_m"])) for stone in _house_stones(board, owner)]
    if not distances:
        return "NONE"
    nearest = min(distances)
    if nearest <= BUTTON_RADIUS_M:
        return "BUTTON"
    if nearest <= 1.22:
        return "INNER_HOUSE"
    return "OUTER_HOUSE"


def _opponent_pair_proximity(board: Sequence[Mapping[str, Any]]) -> str:
    stones = _house_stones(board, "opponent")
    if len(stones) < 2:
        return "NO_PAIR"
    closest = min(
        math.hypot(float(left["x_m"]) - float(right["x_m"]), float(left["y_m"]) - float(right["y_m"]))
        for index, left in enumerate(stones) for right in stones[index + 1 :]
    )
    return "NEAR_PAIR" if closest <= PAIR_NEAR_M else "SEPARATED_PAIR"


def feature_names() -> tuple[str, ...]:
    names = ["K", "control"]
    for owner in OWNERS:
        prefix = "F" if owner == "first" else "O"
        names.extend(f"{prefix}_{zone}" for zone in HOUSE_ZONES)
        names.extend(f"{prefix}_{zone}" for zone in GUARD_ZONES)
        # Exact counts are retained only for the pre-existing macro topology
        # tests (not for fine-state splitting).  A 2+ bucket cannot tell four
        # stones from five, which matters for the crowded-house guard.
        names.extend((
            f"{prefix}_visible", f"{prefix}_visible_exact", f"{prefix}_house_exact",
            f"{prefix}_nearest_depth", f"{prefix}_protected_house",
        ))
    names.extend(("O_house_clear_cardinality", "O_house_pair_proximity"))
    return tuple(names)


FEATURE_NAMES = feature_names()


def state_features(k: int, board: Iterable[Mapping[str, Any]]) -> dict[str, str | int]:
    """Calculate one runtime-safe, canonical feature row.

    The returned fields are intentionally all finite categories/integers; no
    raw score or historical result can leak into a state cluster.
    """

    if not isinstance(k, int) or not 1 <= k <= 8:
        raise ValueError("K must be an integer from 1 through 8")
    canonical, _ = canonicalise_left_right(board)
    facts = board_facts(canonical)
    result: dict[str, str | int] = {
        "K": k,
        "control": {None: "NONE_OR_UNCERTAIN", "first": "FIRST", "opponent": "OPPONENT"}[facts["scoring_owner"]],
    }
    for owner in OWNERS:
        prefix = "F" if owner == "first" else "O"
        zones = Counter(stone_zone(stone) for stone in canonical if stone["owner"] == owner)
        for zone in HOUSE_ZONES + GUARD_ZONES:
            result[f"{prefix}_{zone}"] = _cap_2(int(zones[zone]))
        visible_count = sum(stone["owner"] == owner for stone in canonical)
        house_count = len(_house_stones(canonical, owner))
        result[f"{prefix}_visible"] = _cap_2(visible_count)
        result[f"{prefix}_visible_exact"] = visible_count
        result[f"{prefix}_house_exact"] = house_count
        result[f"{prefix}_nearest_depth"] = _nearest_depth_bin(canonical, owner)
        result[f"{prefix}_protected_house"] = _cap_2(_protected_house_count(canonical, owner))
    opponent_house_count = len(_house_stones(canonical, "opponent"))
    result["O_house_clear_cardinality"] = _cap_2(opponent_house_count)
    result["O_house_pair_proximity"] = _opponent_pair_proximity(canonical)
    return result


def micro_state_key(k: int, board: Iterable[Mapping[str, Any]]) -> str:
    """Stable key for the pre-clustering micro-state; not a final state ID."""

    features = state_features(k, board)
    return "K%d_MICRO[%s]" % (k, ";".join(f"{name}={features[name]}" for name in FEATURE_NAMES))


def canonical_orientation(k: int, board: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Expose the canonical state and orientation needed to unmirror targets."""

    if not isinstance(k, int) or not 1 <= k <= 8:
        raise ValueError("K must be an integer from 1 through 8")
    canonical, mirrored = canonicalise_left_right(board)
    return {
        "features": state_features(k, canonical),
        "micro_state_key": micro_state_key(k, canonical),
        "mirrored_from_runtime_board": mirrored,
    }


def build_feature_rows(rows: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Create a feature panel without inspecting post-shot fields or labels."""

    result: list[dict[str, Any]] = []
    for row in rows:
        k = int(row["own_throw_number"])
        orientation = canonical_orientation(k, row["s_before_own"])
        result.append({
            "panel_key": f"{row['end_id']}:{row['own_global_shot_number']}",
            "match_id": int(row["match_id"]),  # offline split key, never a feature
            "K": k,
            **orientation,
        })
    return result


def _read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=root / "nwnht_first_player_causal_transitions_v0.jsonl")
    parser.add_argument("--output", type=Path, default=root / "nwnht_first_player_state_features_v2.jsonl")
    parser.add_argument("--limit", type=int, default=None, help="Only export the first N rows for a smoke check.")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new output path.")
    rows: Iterable[dict[str, Any]] = _read_jsonl(args.input)
    if args.limit is not None:
        if args.limit < 1:
            raise SystemExit("--limit must be positive")
        rows = (row for _, row in zip(range(args.limit), rows))
    output = build_feature_rows(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for row in output:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    print(json.dumps({"output": str(args.output), "rows": len(output), "feature_count": len(FEATURE_NAMES)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
