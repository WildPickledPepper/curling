#!/usr/bin/env python3
"""Summarize handoff threshold / pre-contact placement refinement probes."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CALIBRATION = PROJECT_ROOT / "data" / "calibration"
DEFAULT_OUTPUT = CALIBRATION / "unity_collision_handoff_threshold_audit_20260709.json"

BASELINE = CALIBRATION / "unity_physx_collision_probe_unique_role_current_best_refresh_20260709.json"
EXTRA_GRID = CALIBRATION / "unity_physx_collision_probe_unique_role_handoff_extra_refine_20260709.json"
EXTRA_Y_GRID = CALIBRATION / "unity_physx_collision_probe_unique_role_handoff_extra_yoffset_refine_20260709.json"


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
        "handoff_extra": config.get("handoff_extra"),
        "handoff_y_offset": config.get("handoff_y_offset"),
        "handoff_x_offset": config.get("handoff_x_offset"),
        "radius": config.get("radius"),
        "contact_offset": config.get("contact_offset"),
        "active_rmse_m": summary.get("active_rmse_m"),
        "target_in_play_rmse_m": summary.get("target_in_play_rmse_m"),
        "combined_rmse_m": summary.get("combined_rmse_m"),
        "active_mean_m": summary.get("active_mean_m"),
        "target_in_play_mean_m": summary.get("target_in_play_mean_m"),
    }


def build_report() -> Dict[str, Any]:
    baseline = _best_result(BASELINE)
    extra = _best_result(EXTRA_GRID)
    extra_y = _best_result(EXTRA_Y_GRID)
    baseline_target = baseline.get("target_in_play_rmse_m")
    best_target = extra_y.get("target_in_play_rmse_m")
    return {
        "question": "Can a better Newfrictionstep->PhysX handoff threshold or millimeter placement offset close the 10cm collision gap?",
        "answer": "No. It helps by about 1cm RMSE but remains around 10cm, far above the 2cm target.",
        "baseline": baseline,
        "best_handoff_extra_only": extra,
        "best_handoff_extra_plus_yoffset": extra_y,
        "improvement_vs_baseline_m": (
            None if baseline_target is None or best_target is None else baseline_target - best_target
        ),
        "interpretation": [
            "Current-best starts the local PhysX pair at center distance about 0.0002m-0.0104m inside 2R, depending on sample.",
            "Starting about 5mm earlier and shifting protocol y by -5mm is the best tested local refinement.",
            "That reduces target RMSE from about 11.32cm to about 10.27cm, so entry timing/placement contributes but is not the main source.",
            "The remaining error still has the row-level normal/tangent split seen in solver-row delta reports, so first ContactBuffer/SolverContact/cache remains the priority.",
        ],
        "source_reports": {
            "baseline": str(BASELINE.relative_to(PROJECT_ROOT)),
            "handoff_extra_grid": str(EXTRA_GRID.relative_to(PROJECT_ROOT)),
            "handoff_extra_yoffset_grid": str(EXTRA_Y_GRID.relative_to(PROJECT_ROOT)),
        },
    }


def main() -> None:
    report = build_report()
    DEFAULT_OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {DEFAULT_OUTPUT.relative_to(PROJECT_ROOT)}")
    print(
        json.dumps(
            {
                "baseline_target_rmse_m": report["baseline"].get("target_in_play_rmse_m"),
                "best_target_rmse_m": report["best_handoff_extra_plus_yoffset"].get("target_in_play_rmse_m"),
                "improvement_vs_baseline_m": report.get("improvement_vs_baseline_m"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
