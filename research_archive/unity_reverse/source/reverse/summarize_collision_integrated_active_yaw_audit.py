#!/usr/bin/env python3
"""Summarize the BESTSHOT->handoff active-yaw integration probe."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CALIBRATION = PROJECT_ROOT / "data" / "calibration"
DEFAULT_OUTPUT = CALIBRATION / "unity_collision_integrated_active_yaw_audit_20260709.json"
BASELINE_PROBE = CALIBRATION / "unity_physx_collision_probe_unique_role_current_best_refresh_20260709.json"
INTEGRATED_PROBE = CALIBRATION / "unity_physx_collision_probe_unique_role_integrated_active_yaw_currentbest_20260709.json"


def _read_json(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _first_summary(path: Path) -> Dict[str, Any]:
    payload = _read_json(path) or {}
    result_sets = payload.get("result_sets") or []
    if not result_sets:
        return {}
    return result_sets[0].get("summary") or {}


def _rmse(values: List[float]) -> Optional[float]:
    if not values:
        return None
    return math.sqrt(sum(value * value for value in values) / len(values))


def build_report() -> Dict[str, Any]:
    baseline_summary = _first_summary(BASELINE_PROBE)
    integrated_payload = _read_json(INTEGRATED_PROBE) or {}
    result_sets = integrated_payload.get("result_sets") or []

    sign_summaries: List[Dict[str, Any]] = []
    for result_set in result_sets:
        config = result_set.get("config") or {}
        rows = []
        for row in result_set.get("rows") or []:
            if row.get("unity_target_in_play") is False:
                continue
            integrated = row.get("integrated_precontact_yaw") or {}
            rows.append(
                {
                    "sample_id": row.get("sample_id"),
                    "label": row.get("label"),
                    "effective_active_yaw_deg": row.get("effective_active_yaw_deg"),
                    "integrated_yaw_deg": integrated.get("yaw_deg"),
                    "release_to_motioninfo_yaw_deg": integrated.get("release_to_motioninfo_yaw_deg"),
                    "motioninfo_to_handoff_yaw_deg": integrated.get("motioninfo_to_handoff_yaw_deg"),
                    "active_error_m": row.get("active_error"),
                    "target_error_m": row.get("target_error"),
                }
            )
        sign_summaries.append(
            {
                "active_yaw_integral_sign": config.get("active_yaw_integral_sign"),
                "active_rmse_m": (result_set.get("summary") or {}).get("active_rmse_m"),
                "target_in_play_rmse_m": (result_set.get("summary") or {}).get("target_in_play_rmse_m"),
                "target_delta_vs_baseline_m": (
                    None
                    if baseline_summary.get("target_in_play_rmse_m") is None
                    else (result_set.get("summary") or {}).get("target_in_play_rmse_m")
                    - baseline_summary.get("target_in_play_rmse_m")
                ),
                "integrated_yaw_deg_rmse": _rmse(
                    [float(row["integrated_yaw_deg"]) for row in rows if row.get("integrated_yaw_deg") is not None]
                ),
                "rows": rows,
            }
        )

    best = min(
        (item for item in sign_summaries if item.get("target_in_play_rmse_m") is not None),
        key=lambda item: item["target_in_play_rmse_m"],
        default=None,
    )
    return {
        "question": (
            "Does setting active actor yaw to the recovered BESTSHOT->handoff integrated spin phase "
            "close the collision residual?"
        ),
        "answer": "No. The integrated active-yaw replay is worse than the current 0-yaw baseline.",
        "baseline": {
            "file": str(BASELINE_PROBE.relative_to(PROJECT_ROOT)),
            "active_rmse_m": baseline_summary.get("active_rmse_m"),
            "target_in_play_rmse_m": baseline_summary.get("target_in_play_rmse_m"),
        },
        "integrated_probe": str(INTEGRATED_PROBE.relative_to(PROJECT_ROOT)),
        "best_integrated_by_target_rmse": best,
        "sign_summaries": sign_summaries,
        "interpretation": [
            "The simple recovered-motion yaw integration gives only about 2deg for most hard samples and about 14deg for 12000.",
            "Using +integrated yaw worsens target RMSE from about 11.32cm to about 16.30cm; -integrated yaw is much worse.",
            "This rules out a simple missing active visible-spin phase as the global 10cm source.",
            "Wide-yaw improvements remain best interpreted as contact-feature/manifold compensation or runtime carryover not captured by this deterministic yaw integral.",
        ],
    }


def main() -> None:
    report = build_report()
    DEFAULT_OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {DEFAULT_OUTPUT.relative_to(PROJECT_ROOT)}")
    print(
        json.dumps(
            {
                "baseline_target_rmse_m": report["baseline"].get("target_in_play_rmse_m"),
                "best_integrated_target_rmse_m": (report.get("best_integrated_by_target_rmse") or {}).get(
                    "target_in_play_rmse_m"
                ),
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
