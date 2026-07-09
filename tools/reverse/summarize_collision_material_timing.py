#!/usr/bin/env python3
"""Summarize material-timing collision probes.

The probes vary whether stone material friction is 0 before contact and when it
is restored to 0.6. This report is meant to answer one question: can the
Unity-vs-pyphysx endpoint error be explained by OnCollisionEnter material timing?
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_collision_material_timing_audit_20260709.json"


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _candidate_row(path: Path) -> Dict[str, Any]:
    payload = _read_json(path)
    result_set = (payload.get("result_sets") or [{}])[0]
    config = result_set.get("config") or {}
    summary = result_set.get("summary") or {}
    rows = result_set.get("rows") or []
    return {
        "file": str(path.relative_to(PROJECT_ROOT)),
        "scope": config.get("pre_collision_friction_scope"),
        "material_switch_mode": config.get("material_switch_mode"),
        "pre_collision_dynamic_friction": config.get("pre_collision_dynamic_friction"),
        "pre_collision_static_friction": config.get("pre_collision_static_friction"),
        "active_rmse_m": summary.get("active_rmse_m"),
        "target_in_play_rmse_m": summary.get("target_in_play_rmse_m"),
        "combined_rmse_m": summary.get("combined_rmse_m"),
        "per_sample": [
            {
                "sample_id": row.get("sample_id"),
                "active_error_m": row.get("active_error"),
                "target_error_m": row.get("target_error"),
                "material_switch_time_s": row.get("material_switch_time"),
                "material_switch_distance_m": row.get("material_switch_distance"),
            }
            for row in rows
        ],
    }


def build_report(calibration_dir: Path) -> Dict[str, Any]:
    paths = sorted(calibration_dir.glob("unity_physx_collision_probe_unique_role_material_timing*_20260709.json"))
    candidates = [_candidate_row(path) for path in paths]
    candidates.sort(
        key=lambda row: (
            float("inf") if row["combined_rmse_m"] is None else float(row["combined_rmse_m"]),
            float("inf") if row["target_in_play_rmse_m"] is None else float(row["target_in_play_rmse_m"]),
        )
    )
    baseline = next((row for row in candidates if "baseline" in Path(row["file"]).name), None)
    best = candidates[0] if candidates else None
    dynamic_static_zero_post = [
        row
        for row in candidates
        if row["pre_collision_dynamic_friction"] == 0.0
        and row["pre_collision_static_friction"] == 0.0
        and row["material_switch_mode"] == "post-step-distance"
    ]
    dynamic_zero_static_default_post = [
        row
        for row in candidates
        if row["pre_collision_dynamic_friction"] == 0.0
        and row["pre_collision_static_friction"] is None
        and row["material_switch_mode"] == "post-step-distance"
    ]
    return {
        "candidate_count": len(candidates),
        "baseline": baseline,
        "best": best,
        "dynamic_static_zero_post_step": dynamic_static_zero_post,
        "dynamic_zero_static_default_post_step": dynamic_zero_static_default_post,
        "candidates": candidates,
        "interpretation": [
            "pre-step-distance with pre-friction 0 switches back to 0.6 before the first solve and matches baseline.",
            "dynamic=0/static=0.6 post-step candidates match baseline, so zero dynamic friction alone is not a missing 10cm effect.",
            "dynamic=0/static=0 post-step candidates are substantially worse, so first-contact friction cannot be fully zero in the matching model.",
            "never-switch candidates are catastrophic for the active stone, target stone, or both, so permanent pre-collision zero friction is ruled out.",
            "Adding all material-timing candidates does not improve the global oracle floor; material timing is not the remaining path to 2cm.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--calibration-dir", type=Path, default=PROJECT_ROOT / "data" / "calibration")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    report = build_report(args.calibration_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"candidate_count={report['candidate_count']}")
    if report["best"]:
        print(
            "best combined="
            f"{report['best']['combined_rmse_m']:.6f} target={report['best']['target_in_play_rmse_m']:.6f} "
            f"file={report['best']['file']}"
        )
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
