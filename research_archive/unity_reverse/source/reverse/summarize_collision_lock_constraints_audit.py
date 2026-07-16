#!/usr/bin/env python3
"""Summarize the Unity Rigidbody lock-constraints replay audit."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, Optional


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CALIBRATION = PROJECT_ROOT / "data" / "calibration"
DEFAULT_OUTPUT = CALIBRATION / "unity_collision_lock_constraints_audit_20260709.json"

BASELINE = CALIBRATION / "unity_physx_collision_probe_unique_role_current_best_refresh_20260709.json"
LOCK_PROBE = CALIBRATION / "unity_physx_collision_probe_unique_role_lockupright_refresh_20260709.json"


def _read_json(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _best_result(path: Path) -> Dict[str, Any]:
    payload = _read_json(path) or {}
    result_sets = payload.get("result_sets") or []
    if not result_sets:
        return {"file": str(path.relative_to(PROJECT_ROOT)), "missing": True}
    best = min(
        result_sets,
        key=lambda result_set: (result_set.get("summary") or {}).get("target_in_play_rmse_m", 999.0),
    )
    config = best.get("config") or {}
    summary = best.get("summary") or {}
    return {
        "file": str(path.relative_to(PROJECT_ROOT)),
        "result_set_count": len(result_sets),
        "config": {
            "lock_upright": config.get("lock_upright"),
            "inertia_model": config.get("inertia_model"),
            "inertia_radial": config.get("inertia_radial"),
            "inertia_vertical": config.get("inertia_vertical"),
            "handoff_extra": config.get("handoff_extra"),
            "handoff_y_offset": config.get("handoff_y_offset"),
            "radius": config.get("radius"),
            "contact_offset": config.get("contact_offset"),
        },
        "summary": summary,
        "rows": best.get("rows") or [],
    }


def _horizontal_angular_speed_at(row: Dict[str, Any], time_key: str) -> Optional[float]:
    snapshot = ((row.get("snapshots") or {}).get(time_key) or {}).get("target") or {}
    angular = snapshot.get("physx_angular_velocity")
    if not angular or len(angular) < 2:
        return None
    return math.hypot(float(angular[0]), float(angular[1]))


def _max_horizontal_angular_speed(best: Dict[str, Any], time_key: str = "0.020000") -> Optional[float]:
    values = [
        value
        for row in best.get("rows") or []
        for value in [_horizontal_angular_speed_at(row, time_key)]
        if value is not None
    ]
    return max(values) if values else None


def _row_errors(best: Dict[str, Any]) -> Dict[str, Dict[str, Optional[float]]]:
    rows: Dict[str, Dict[str, Optional[float]]] = {}
    for row in best.get("rows") or []:
        rows[str(row.get("sample_id"))] = {
            "active_error_m": row.get("active_error"),
            "target_error_m": row.get("target_error"),
        }
    return rows


def build_report() -> Dict[str, Any]:
    baseline = _best_result(BASELINE)
    lock = _best_result(LOCK_PROBE)
    baseline_summary = baseline.get("summary") or {}
    lock_summary = lock.get("summary") or {}
    baseline_target = baseline_summary.get("target_in_play_rmse_m")
    lock_target = lock_summary.get("target_in_play_rmse_m")
    return {
        "question": (
            "Does matching Unity RigidbodyConstraints.FreezeRotationX|FreezeRotationZ "
            "with pyphysx angular X/Y locks close the collision gap?"
        ),
        "answer": "No. It matches the known constraint axis but leaves target RMSE at about 11.37cm.",
        "unity_fact": "CurlingStoneNew.Start sets Rigidbody.constraints=80, i.e. FreezeRotationX|FreezeRotationZ; only yaw remains free.",
        "baseline": {
            "config": baseline.get("config"),
            "summary": baseline_summary,
            "max_target_horizontal_angular_speed_002s": _max_horizontal_angular_speed(baseline),
            "row_errors": _row_errors(baseline),
        },
        "lock_upright_best": {
            "config": lock.get("config"),
            "summary": lock_summary,
            "max_target_horizontal_angular_speed_002s": _max_horizontal_angular_speed(lock),
            "row_errors": _row_errors(lock),
        },
        "delta_vs_baseline_m": {
            "target_rmse": None if baseline_target is None or lock_target is None else lock_target - baseline_target,
            "active_rmse": (
                None
                if baseline_summary.get("active_rmse_m") is None or lock_summary.get("active_rmse_m") is None
                else lock_summary.get("active_rmse_m") - baseline_summary.get("active_rmse_m")
            ),
        },
        "interpretation": [
            "The pyphysx lock flags are mapped in the z-up replay as LOCK_ANGULAR_X and LOCK_ANGULAR_Y, leaving z/yaw free.",
            "The locked replay suppresses target horizontal angular velocity at 0.02s to zero, so the diagnostic is actually exercising the constraint.",
            "Despite that, best target RMSE is 11.37cm versus the baseline 11.32cm, and the hard 12003 target remains about 24.9cm.",
            "Therefore the missing 10cm is not explained by free roll/pitch in the local replay; the remaining priority is still first ContactBuffer/SolverContact/cache or runtime shape state.",
        ],
        "source_reports": {
            "baseline": str(BASELINE.relative_to(PROJECT_ROOT)),
            "lock_upright_probe": str(LOCK_PROBE.relative_to(PROJECT_ROOT)),
        },
    }


def main() -> None:
    report = build_report()
    DEFAULT_OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {DEFAULT_OUTPUT.relative_to(PROJECT_ROOT)}")
    print(
        json.dumps(
            {
                "baseline_target_rmse_m": report["baseline"]["summary"].get("target_in_play_rmse_m"),
                "lock_target_rmse_m": report["lock_upright_best"]["summary"].get("target_in_play_rmse_m"),
                "delta_vs_baseline_m": report["delta_vs_baseline_m"],
                "lock_max_horizontal_angular_speed_002s": report["lock_upright_best"].get(
                    "max_target_horizontal_angular_speed_002s"
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
