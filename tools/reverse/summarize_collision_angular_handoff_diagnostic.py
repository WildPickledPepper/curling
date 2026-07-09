#!/usr/bin/env python3
"""Summarize the active handoff angular-velocity diagnostic probes."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CALIBRATION = PROJECT_ROOT / "data" / "calibration"
DEFAULT_OUTPUT = CALIBRATION / "unity_collision_angular_handoff_diagnostic_20260709.json"

GLOBAL_W_REPORT = CALIBRATION / "unity_physx_collision_probe_unique_role_handoff_woffset_global_20260709.json"
SAMPLE_12005_W0_CONTACT = CALIBRATION / "unity_physx_collision_probe_12005_handoff_target_xy_best_contact_20260709.json"
SAMPLE_12005_W_BEST_CONTACT = (
    CALIBRATION / "unity_physx_collision_probe_12005_handoff_woffset_bestmax_contact_20260709.json"
)
SAMPLE_12005_W_ULTRAFINE = CALIBRATION / "unity_physx_collision_probe_12005_handoff_woffset_ultrafine_20260709.json"
SAMPLE_12005_VXY = CALIBRATION / "unity_physx_collision_probe_12005_handoff_vxyoffset_coarse_20260709.json"
SAMPLE_12005_YAW = CALIBRATION / "unity_physx_collision_probe_12005_active_target_yaw_micro_20260709.json"


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _rmse(values: Iterable[float]) -> Optional[float]:
    rows = list(values)
    if not rows:
        return None
    return math.sqrt(sum(value * value for value in rows) / len(rows))


def _best_result_set(path: Path, *, key: str = "max_endpoint") -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    report = _read_json(path)
    best = None
    best_score = float("inf")
    for result_set in report.get("result_sets") or []:
        rows = result_set.get("rows") or []
        if key == "target_rmse":
            score = float((result_set.get("summary") or {}).get("target_in_play_rmse_m") or float("inf"))
        else:
            row_scores = []
            for row in rows:
                active = row.get("active_error")
                target = row.get("target_error")
                if active is None:
                    continue
                row_scores.append(max(float(active), float(target or 0.0)))
            score = max(row_scores) if row_scores else float("inf")
        if score < best_score:
            best = result_set
            best_score = score
    return best


def _compact_best(path: Path, *, key: str = "max_endpoint") -> Optional[Dict[str, Any]]:
    best = _best_result_set(path, key=key)
    if best is None:
        return None
    config = best.get("config") or {}
    rows = best.get("rows") or []
    row = rows[0] if rows else {}
    active = row.get("active_error")
    target = row.get("target_error")
    return {
        "source": str(path.relative_to(PROJECT_ROOT)),
        "config": {
            "handoff_w_offset": config.get("handoff_w_offset"),
            "handoff_vx_offset": config.get("handoff_vx_offset"),
            "handoff_vy_offset": config.get("handoff_vy_offset"),
            "active_yaw": config.get("active_yaw"),
            "target_yaw": config.get("target_yaw"),
            "handoff_x_offset": config.get("handoff_x_offset"),
            "handoff_y_offset": config.get("handoff_y_offset"),
            "target_x_offset": config.get("target_x_offset"),
            "target_y_offset": config.get("target_y_offset"),
        },
        "summary": best.get("summary"),
        "sample_id": row.get("sample_id"),
        "handoff_w": (row.get("handoff") or {}).get("w"),
        "active_error_m": active,
        "target_error_m": target,
        "max_endpoint_error_m": max(float(active), float(target or 0.0)) if active is not None else None,
        "sim_active": row.get("sim_active"),
        "sim_target": row.get("sim_target"),
        "unity_active": row.get("unity_active"),
        "unity_target": row.get("unity_target"),
    }


def _snapshot_delta(base_row: Dict[str, Any], changed_row: Dict[str, Any], time_key: str) -> Dict[str, Any]:
    base = (base_row.get("snapshots") or {}).get(time_key) or {}
    changed = (changed_row.get("snapshots") or {}).get(time_key) or {}

    def delta(stone: str, field: str) -> Optional[List[float]]:
        a = ((base.get(stone) or {}).get(field))
        b = ((changed.get(stone) or {}).get(field))
        if a is None or b is None:
            return None
        if isinstance(a, list):
            return [float(bi) - float(ai) for ai, bi in zip(a, b)]
        return [float(b) - float(a)]

    return {
        "time_key": time_key,
        "active_linear_velocity_delta": delta("active", "linear_velocity"),
        "target_linear_velocity_delta": delta("target", "linear_velocity"),
        "active_angular_velocity_delta": delta("active", "angular_velocity"),
        "target_angular_velocity_delta": delta("target", "angular_velocity"),
    }


def _first_contact(row: Dict[str, Any]) -> Dict[str, Any]:
    report = ((row.get("stone_stone_contact_reports") or [{}])[0]) or {}
    point = ((report.get("points") or [{}])[0]) or {}
    return {
        "first_contact_time": row.get("first_stone_stone_contact_time"),
        "contact_count": report.get("contact_count"),
        "normal": point.get("normal"),
        "impulse": point.get("impulse"),
        "separation": point.get("separation"),
    }


def _contact_comparison() -> Dict[str, Any]:
    base = _read_json(SAMPLE_12005_W0_CONTACT)
    changed = _read_json(SAMPLE_12005_W_BEST_CONTACT)
    base_rs = (base.get("result_sets") or [{}])[0]
    changed_rs = (changed.get("result_sets") or [{}])[0]
    base_row = (base_rs.get("rows") or [{}])[0]
    changed_row = (changed_rs.get("rows") or [{}])[0]
    return {
        "baseline_source": str(SAMPLE_12005_W0_CONTACT.relative_to(PROJECT_ROOT)),
        "woffset_source": str(SAMPLE_12005_W_BEST_CONTACT.relative_to(PROJECT_ROOT)),
        "baseline_config": {
            "handoff_w_offset": (base_rs.get("config") or {}).get("handoff_w_offset"),
        },
        "woffset_config": {
            "handoff_w_offset": (changed_rs.get("config") or {}).get("handoff_w_offset"),
        },
        "baseline_errors_m": {
            "active": base_row.get("active_error"),
            "target": base_row.get("target_error"),
        },
        "woffset_errors_m": {
            "active": changed_row.get("active_error"),
            "target": changed_row.get("target_error"),
        },
        "handoff_w_visible_magnitude": (base_row.get("handoff") or {}).get("w"),
        "required_offset_over_visible_w": (
            abs(float((changed_rs.get("config") or {}).get("handoff_w_offset") or 0.0))
            / abs(float((base_row.get("handoff") or {}).get("w") or float("nan")))
        ),
        "baseline_first_contact": _first_contact(base_row),
        "woffset_first_contact": _first_contact(changed_row),
        "snapshot_delta_0p02": _snapshot_delta(base_row, changed_row, "0.020000"),
    }


def _global_w_summary() -> Dict[str, Any]:
    if not GLOBAL_W_REPORT.exists():
        return {}
    report = _read_json(GLOBAL_W_REPORT)
    rows = []
    for result_set in report.get("result_sets") or []:
        config = result_set.get("config") or {}
        summary = result_set.get("summary") or {}
        bad_pairs = 0
        for row in result_set.get("rows") or []:
            if row.get("target_error") is None:
                continue
            if float(row["active_error"]) > 0.02 or float(row["target_error"]) > 0.02:
                bad_pairs += 1
        rows.append(
            {
                "handoff_w_offset": config.get("handoff_w_offset"),
                "active_rmse_m": summary.get("active_rmse_m"),
                "target_in_play_rmse_m": summary.get("target_in_play_rmse_m"),
                "bad_in_play_pair_count": bad_pairs,
            }
        )
    best = min(rows, key=lambda row: float(row["target_in_play_rmse_m"]))
    baseline = next((row for row in rows if row.get("handoff_w_offset") == 0.0), None)
    return {
        "source": str(GLOBAL_W_REPORT.relative_to(PROJECT_ROOT)),
        "best_by_target_rmse": best,
        "baseline": baseline,
        "rows": rows,
    }


def build_report() -> Dict[str, Any]:
    contact = _contact_comparison()
    report = {
        "question": "Is the 12005 closure caused by a global handoff angular-velocity constant or a sample-specific tangent/angular proxy?",
        "sample_12005_vxy_offset_best": _compact_best(SAMPLE_12005_VXY),
        "sample_12005_yaw_best": _compact_best(SAMPLE_12005_YAW),
        "sample_12005_woffset_best_by_max_endpoint": _compact_best(SAMPLE_12005_W_ULTRAFINE),
        "sample_12005_contact_comparison": contact,
        "global_woffset_summary": _global_w_summary(),
    }
    report["interpretation"] = [
        "For 12005, independent handoff vx/vy offsets and active/target yaw probes do not improve the pair endpoint error.",
        "A handoff_w_offset around -0.44rad/s brings 12005 under 2cm, but the visible reconstructed handoff w is only about 0.00123rad/s.",
        "The required diagnostic offset is hundreds of times larger than the visible handoff w, so it is not a simple angular_sign or small unit-conversion fix.",
        "The same w offset as a global constant does not close the unique-role set; the best global target RMSE remains about 10.94cm.",
        "For the 12005 contact-report A/B, first contact time, point count, normal and separation are unchanged; the effect appears through post-contact linear/angular velocity distribution.",
        "The current best explanation is a sample-specific active-side tangent/angular native-state or friction/contact-row/cache proxy, not a proven managed-level angular-velocity formula.",
    ]
    return report


def main() -> None:
    report = build_report()
    DEFAULT_OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {DEFAULT_OUTPUT.relative_to(PROJECT_ROOT)}")
    print(json.dumps(report["sample_12005_woffset_best_by_max_endpoint"], ensure_ascii=False, indent=2))
    print(json.dumps(report["global_woffset_summary"].get("best_by_target_rmse"), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
