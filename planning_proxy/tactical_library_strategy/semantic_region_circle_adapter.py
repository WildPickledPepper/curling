"""Convert a semantic tactical region to circle-only planner subgoals.

This is a geometry adapter, not a tactical scorer.  Each emitted circle lies
wholly inside the input semantic region, so accepting a circle preserves the
tactical constraint.  The finite circle set is an *inner approximation*:
failure on every circle means only that the current tiled search failed, never
that the original semantic region is physically unreachable.
"""

from __future__ import annotations

import math
from typing import Any, Mapping


DEFAULT_TILE_RADIUS_M = 0.17
DEFAULT_MAX_TILES = 24


def _inside_circle_region(x: float, y: float, r: float, region: Mapping[str, Any]) -> bool:
    return math.hypot(x - float(region["centre_x_m"]), y - float(region["centre_y_m"])) + r <= float(region["max_radius_m"])


def _inside_house_sector(x: float, y: float, r: float, region: Mapping[str, Any]) -> bool:
    d = math.hypot(x, y)
    if d - r < float(region["min_radius_m"]) or d + r > float(region["max_radius_m"]):
        return False
    if region["x_relation"] == "<0" and not x + r < 0.0:
        return False
    if region["x_relation"] == ">=0" and not x - r >= 0.0:
        return False
    if region["y_relation"] == "<0" and not y + r < 0.0:
        return False
    if region["y_relation"] == ">=0" and not y - r >= 0.0:
        return False
    return True


def _inside_guard_lane(x: float, y: float, r: float, region: Mapping[str, Any]) -> bool:
    return (
        abs(x) + r <= float(region["abs_x_max_m"])
        and y - r > float(region["y_min_exclusive_m"])
        and y + r <= float(region["y_max_inclusive_m"])
    )


def _inside_wing_guard(x: float, y: float, r: float, region: Mapping[str, Any]) -> bool:
    x_relation = str(region["x_relation"])
    if x_relation == "<-0.38" and not x + r < -0.38:
        return False
    if x_relation == ">0.38" and not x - r > 0.38:
        return False
    return y - r > float(region["y_min_exclusive_m"]) and y + r <= float(region["y_max_inclusive_m"])


def _grid(minimum: float, maximum: float, spacing: float, *, anchor: float | None = None) -> list[float]:
    if anchor is not None and minimum <= anchor <= maximum:
        values = [anchor]
        cursor = anchor - spacing
        while cursor >= minimum - 1e-9:
            values.append(round(cursor, 6))
            cursor -= spacing
        cursor = anchor + spacing
        while cursor <= maximum + 1e-9:
            values.append(round(cursor, 6))
            cursor += spacing
        return sorted(set(values))
    values: list[float] = []
    cursor = minimum
    while cursor <= maximum + 1e-9:
        values.append(round(cursor, 6))
        cursor += spacing
    return values


def _tile_centres(region: Mapping[str, Any], radius_m: float) -> list[tuple[float, float]]:
    kind = str(region["kind"])
    spacing = 2.0 * radius_m
    if kind == "HOUSE_SECTOR":
        bound = float(region["max_radius_m"])
        predicate = _inside_house_sector
        xs = _grid(-bound + radius_m, bound - radius_m, spacing, anchor=0.0)
        ys = _grid(-bound + radius_m, bound - radius_m, spacing)
    elif kind == "GUARD_LANE":
        predicate = _inside_guard_lane
        bound = float(region["abs_x_max_m"])
        xs = _grid(-bound + radius_m, bound - radius_m, spacing, anchor=0.0)
        ys = _grid(float(region["y_min_exclusive_m"]) + radius_m, float(region["y_max_inclusive_m"]) - radius_m, spacing)
    elif kind == "WING_GUARD":
        predicate = _inside_wing_guard
        y0, y1 = float(region["y_min_exclusive_m"]), float(region["y_max_inclusive_m"])
        if str(region["x_relation"]) == "<-0.38":
            xs = _grid(-3.0, -0.38 - radius_m, spacing)
        else:
            xs = _grid(0.38 + radius_m, 3.0, spacing)
        ys = _grid(y0 + radius_m, y1 - radius_m, spacing)
    else:
        raise ValueError(f"unsupported semantic region kind {kind!r}")
    return [(x, y) for y in ys for x in xs if predicate(x, y, radius_m, region)]


def circle_subgoals(
    region: Mapping[str, Any], *, radius_m: float = DEFAULT_TILE_RADIUS_M,
    max_tiles: int = DEFAULT_MAX_TILES, region_id_prefix: str = "semantic",
) -> list[dict[str, Any]]:
    """Return circle-only subgoals that are all inside ``region``.

    A circular semantic region is returned exactly as one circle; non-circular
    regions are tiled internally.  Ordering is geometrical and deterministic,
    not a value ranking.
    """

    if radius_m <= 0.0 or max_tiles < 1:
        raise ValueError("radius_m must be positive and max_tiles must be at least one")
    kind = str(region["kind"])
    if kind == "CIRCLE":
        return [{
            "region_id": f"{region_id_prefix}:exact-circle",
            "shape": "circle",
            "centre_x_m": float(region["centre_x_m"]),
            "centre_y_m": float(region["centre_y_m"]),
            "radius_m": float(region["max_radius_m"]),
            "coverage_status": "EXACT_SEMANTIC_REGION",
        }]
    centres = _tile_centres(region, radius_m)
    # Prefer deterministic central/deeper-safe ordering only to make planner
    # retries reproducible; it is explicitly not a tactical preference score.
    centres.sort(key=lambda point: (math.hypot(point[0], point[1]), point[1], point[0]))
    return [
        {
            "region_id": f"{region_id_prefix}:inner-tile:{index}",
            "shape": "circle", "centre_x_m": x, "centre_y_m": y, "radius_m": radius_m,
            "coverage_status": "INNER_APPROXIMATION_ONLY",
        }
        for index, (x, y) in enumerate(centres[:max_tiles], start=1)
    ]
