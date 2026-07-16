#!/usr/bin/env python3
"""Check whether captured cooked hulls match the formal curling stone collider."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "calibration" / "unity_cooked_hulls_20260708_225950.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_cooked_hull_identity_20260708_225950.json"

STONE_RADIUS_WORLD = 0.14087501
STONE_HEIGHT_WORLD = 0.23
STONE_EXPECTED_EXTENTS = sorted([2.0 * STONE_RADIUS_WORLD, 2.0 * STONE_RADIUS_WORLD, STONE_HEIGHT_WORLD])


def _relative_rmse(observed: list[float], expected: list[float]) -> float:
    return math.sqrt(sum(((obs - exp) / exp) ** 2 for obs, exp in zip(observed, expected)) / len(expected))


def _max_relative_error(observed: list[float], expected: list[float]) -> float:
    return max(abs(obs - exp) / exp for obs, exp in zip(observed, expected))


def analyze(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    candidates: list[dict[str, Any]] = []
    for item in data.get("summary", []):
        extents = [float(value) for value in item["extents"]]
        sorted_extents = sorted(extents)
        rmse = _relative_rmse(sorted_extents, STONE_EXPECTED_EXTENTS)
        max_rel = _max_relative_error(sorted_extents, STONE_EXPECTED_EXTENTS)
        candidate = {
            "sha256_16": item["sha256_16"],
            "first_event_index": item["first_event_index"],
            "duplicate_count": item["duplicate_count"],
            "unity_source_meshes": item.get("unity_source_meshes", []),
            "counts": {
                "vertices": item["vertices"],
                "polygons": item["polygons"],
                "indices": item["indices"],
            },
            "extents": extents,
            "sorted_extents": sorted_extents,
            "stone_extent_relative_rmse": rmse,
            "stone_extent_max_relative_error": max_rel,
            "matches_formal_stone_by_extent": max_rel <= 0.05,
        }
        candidates.append(candidate)

    candidates.sort(key=lambda entry: entry["stone_extent_relative_rmse"])
    return {
        "source": str(path),
        "formal_stone_expected": {
            "source": "ExtendedColliders3D size=(2.5,2.0,2.5), scene scale ~= (0.1127,0.115,0.1127)",
            "radius_world": STONE_RADIUS_WORLD,
            "height_world": STONE_HEIGHT_WORLD,
            "diameter_world": 2.0 * STONE_RADIUS_WORLD,
            "sorted_extents": STONE_EXPECTED_EXTENTS,
        },
        "best_candidate": candidates[0] if candidates else None,
        "any_extent_match_5pct": any(item["matches_formal_stone_by_extent"] for item in candidates),
        "candidates": candidates,
        "conclusion": (
            "No captured hull matches the formal curling stone collider extents within 5%; "
            "the captured waiting-page hulls are real cooked convex meshes but are not proven "
            "to be the gameplay stone collision hull."
            if candidates and not any(item["matches_formal_stone_by_extent"] for item in candidates)
            else "At least one captured hull matches the formal stone extents within 5%."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    result = analyze(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    expected = result["formal_stone_expected"]
    print(f"input: {args.input}")
    print(f"output: {args.output}")
    print(
        "formal stone expected sorted extents: "
        + ", ".join(f"{value:.6f}" for value in expected["sorted_extents"])
    )
    for item in result["candidates"]:
        extents = ", ".join(f"{value:.6f}" for value in item["sorted_extents"])
        print(
            f"event={item['first_event_index']:3d} hash={item['sha256_16']} "
            f"source={','.join(item['unity_source_meshes']) or '-'} "
            f"sorted_extents=({extents}) "
            f"max_rel={item['stone_extent_max_relative_error']:.3f} "
            f"match={item['matches_formal_stone_by_extent']}"
        )
    print(result["conclusion"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
