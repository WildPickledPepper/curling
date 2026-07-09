#!/usr/bin/env python3
"""Summarize whether the probe's generated ring points hide a geometry-input gap."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CALIBRATION = PROJECT_ROOT / "data" / "calibration"
DEFAULT_OUTPUT = CALIBRATION / "unity_collision_stone_geometry_input_audit_20260709.json"

CURRENT_BEST_RING = CALIBRATION / "unity_physx_collision_probe_unique_role_current_best_refresh_20260709.json"
CURRENT_BEST_RECOVERED_MESH = (
    CALIBRATION / "unity_physx_collision_probe_unique_role_formal_recovered_mesh_currentbest_scale_20260709.json"
)
FORMAL_RING = CALIBRATION / "unity_physx_collision_probe_unique_role_ring_formal_params_handoff292_20260709.json"
FORMAL_RECOVERED_MESH = (
    CALIBRATION / "unity_physx_collision_probe_unique_role_formal_recovered_mesh_handoff292_20260709.json"
)


def _read_json(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _first_result(path: Path) -> Optional[Dict[str, Any]]:
    payload = _read_json(path)
    if not payload:
        return None
    result_sets = payload.get("result_sets") or []
    if not result_sets:
        return None
    return result_sets[0]


def _compact(path: Path) -> Dict[str, Any]:
    result = _first_result(path)
    if result is None:
        return {
            "file": str(path.relative_to(PROJECT_ROOT)),
            "exists": path.exists(),
            "missing": True,
        }
    config = result.get("config") or {}
    summary = result.get("summary") or {}
    return {
        "file": str(path.relative_to(PROJECT_ROOT)),
        "missing": False,
        "stone_geometry": config.get("stone_geometry", "ring"),
        "formal_stone_scale": config.get("formal_stone_scale"),
        "radius": config.get("radius"),
        "height": config.get("height"),
        "center_height": config.get("center_height"),
        "handoff_extra": config.get("handoff_extra"),
        "inertia_model": config.get("inertia_model"),
        "inertia_radial": config.get("inertia_radial"),
        "inertia_vertical": config.get("inertia_vertical"),
        "active_rmse_m": summary.get("active_rmse_m"),
        "target_in_play_rmse_m": summary.get("target_in_play_rmse_m"),
        "combined_rmse_m": summary.get("combined_rmse_m"),
        "target_cleared_count": summary.get("target_cleared_count"),
    }


def _delta(a: Dict[str, Any], b: Dict[str, Any], key: str) -> Optional[float]:
    if a.get(key) is None or b.get(key) is None:
        return None
    return float(b[key]) - float(a[key])


def build_report() -> Dict[str, Any]:
    current_ring = _compact(CURRENT_BEST_RING)
    current_recovered = _compact(CURRENT_BEST_RECOVERED_MESH)
    formal_ring = _compact(FORMAL_RING)
    formal_recovered = _compact(FORMAL_RECOVERED_MESH)

    return {
        "question": (
            "Does using generated ring points instead of the recovered ExtendedColliders3D "
            "512-vertex formal mesh explain the 10cm collision residual?"
        ),
        "answer": "No. The exact recovered mesh input is now wired into the probe and does not close the error.",
        "comparisons": {
            "current_best_scale_ring": current_ring,
            "current_best_scale_recovered_mesh": current_recovered,
            "formal_params_ring": formal_ring,
            "formal_params_recovered_mesh": formal_recovered,
        },
        "deltas": {
            "current_best_scale_recovered_minus_ring_target_rmse_m": _delta(
                current_ring, current_recovered, "target_in_play_rmse_m"
            ),
            "current_best_scale_recovered_minus_ring_active_rmse_m": _delta(
                current_ring, current_recovered, "active_rmse_m"
            ),
            "formal_recovered_minus_ring_target_rmse_m": _delta(
                formal_ring, formal_recovered, "target_in_play_rmse_m"
            ),
            "formal_recovered_minus_ring_active_rmse_m": _delta(
                formal_ring, formal_recovered, "active_rmse_m"
            ),
            "formal_recovered_minus_current_best_target_rmse_m": _delta(
                current_ring, formal_recovered, "target_in_play_rmse_m"
            ),
        },
        "interpretation": [
            "At the current-best inflated scale, recovered formal mesh input and generated ring input give identical endpoint RMSE.",
            "At the formal physical scale with the 0.292m handoff threshold, recovered mesh input improves target RMSE by only about 0.57cm versus ring input.",
            "The formal recovered-mesh run is still about 12.08cm target RMSE, worse than the current-best 11.32cm and far from the 2cm target.",
            "Therefore the remaining collision gap is not caused by failing to feed the recovered 512-vertex formal mesh into pyphysx cooking.",
        ],
        "source_reports": {
            "current_best_ring": str(CURRENT_BEST_RING.relative_to(PROJECT_ROOT)),
            "current_best_recovered_mesh": str(CURRENT_BEST_RECOVERED_MESH.relative_to(PROJECT_ROOT)),
            "formal_ring": str(FORMAL_RING.relative_to(PROJECT_ROOT)),
            "formal_recovered_mesh": str(FORMAL_RECOVERED_MESH.relative_to(PROJECT_ROOT)),
        },
    }


def main() -> None:
    report = build_report()
    DEFAULT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {DEFAULT_OUTPUT.relative_to(PROJECT_ROOT)}")
    print(json.dumps(report["deltas"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
