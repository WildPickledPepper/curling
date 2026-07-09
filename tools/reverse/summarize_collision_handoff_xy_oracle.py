#!/usr/bin/env python3
"""Summarize handoff x/y counterfactual probes for collision hard samples."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CALIBRATION = PROJECT_ROOT / "data" / "calibration"
DEFAULT_OUTPUT = CALIBRATION / "unity_collision_handoff_xy_oracle_20260709.json"

BASELINE = CALIBRATION / "unity_physx_collision_probe_unique_role_current_best_refresh_20260709.json"
HANDOFF_REPORTS = [
    CALIBRATION / "unity_physx_collision_probe_unique_role_xoffset_y0_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12003_contact_xyoffset_wide_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12003_handoff_xy_fine_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12003_handoff_xy_ultrafine_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12003_handoff_target_xy_micro_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12003_handoff_vscale_micro_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12004_handoff_xy_wide_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12005_handoff_xy_fine_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12006_handoff_xy_fine_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12007_handoff_xy_wide_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12007_target_xyoffset_wide_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12007_handoff_target_xy_coarse_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12007_handoff_target_xy_fine_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12007_handoff_target_xy_tx_micro_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12007_handoff_target_xy_tx_ultramicro_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12007_handoff_target_xy_tx_ultramicro2_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12007_handoff_target_xy_tx_ultramicro3_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12005_handoff_target_xy_micro_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12005_handoff_vscale_micro_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12005_handoff_vxyoffset_coarse_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12005_handoff_woffset_coarse_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12005_handoff_woffset_fine_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12005_handoff_woffset_ultrafine_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12005_handoff_woffset_subfine_20260709.json",
]
CONTACT_BEST_REPORTS = [
    CALIBRATION / "unity_physx_collision_probe_12003_handoff_xy_fine_best_contact_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12004_handoff_xy_best_contact_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12007_handoff_xy_best_contact_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12007_handoff_target_xy_best_contact_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12005_handoff_woffset_bestmax_contact_20260709.json",
]
NORMAL_PARAM_12007 = CALIBRATION / "unity_physx_collision_probe_12007_normal_param_grid_20260709.json"
TAIL_ORACLE_AFTER_HANDOFF_BEST = [
    CALIBRATION / "unity_collision_tail_replay_oracle_12003_handoff_xy_best_020s_20260709.json",
    CALIBRATION / "unity_collision_tail_replay_oracle_12004_handoff_xy_best_020s_20260709.json",
    CALIBRATION / "unity_collision_tail_replay_oracle_12007_handoff_xy_best_020s_20260709.json",
]


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _rmse(values: Iterable[float]) -> Optional[float]:
    rows = list(values)
    if not rows:
        return None
    return math.sqrt(sum(value * value for value in rows) / len(rows))


def _compact_config(config: Dict[str, Any]) -> Dict[str, Any]:
    keys = [
        "handoff_x_offset",
        "handoff_y_offset",
        "handoff_v_scale",
        "handoff_vx_offset",
        "handoff_vy_offset",
        "handoff_w_offset",
        "target_x_offset",
        "target_y_offset",
        "radius",
        "contact_offset",
        "stone_restitution",
        "active_yaw",
        "target_yaw",
        "shape_local_yaw",
    ]
    return {key: config.get(key) for key in keys if key in config}


def _row_item(path: Path, result_set: Dict[str, Any], row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    active_error = row.get("active_error")
    target_error = row.get("target_error")
    if active_error is None:
        return None
    max_error = max(float(active_error), float(target_error or 0.0))
    return {
        "source": str(path.relative_to(PROJECT_ROOT)),
        "sample_id": row.get("sample_id"),
        "label": row.get("label"),
        "unity_target_in_play": row.get("unity_target_in_play"),
        "active_error_m": active_error,
        "target_error_m": target_error,
        "max_endpoint_error_m": max_error if target_error is not None else active_error,
        "combined_pair_rmse_m": math.sqrt((float(active_error) ** 2 + float(target_error or 0.0) ** 2) / 2.0)
        if target_error is not None
        else active_error,
        "config": _compact_config(result_set.get("config") or {}),
        "sim_active": row.get("sim_active"),
        "sim_target": row.get("sim_target"),
        "unity_active": row.get("unity_active"),
        "unity_target": row.get("unity_target"),
    }


def _iter_items(path: Path) -> Iterable[Dict[str, Any]]:
    if not path.exists():
        return []
    report = _read_json(path)
    rows: List[Dict[str, Any]] = []
    for result_set in report.get("result_sets") or []:
        for row in result_set.get("rows") or []:
            item = _row_item(path, result_set, row)
            if item is not None:
                rows.append(item)
    return rows


def _best_by_sample(items: Iterable[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    best: Dict[str, Dict[str, Any]] = {}
    for item in items:
        sample_key = str(item.get("sample_id"))
        current = best.get(sample_key)
        if current is None or item["max_endpoint_error_m"] < current["max_endpoint_error_m"]:
            best[sample_key] = item
    return dict(sorted(best.items(), key=lambda kv: int(kv[0])))


def _best_active_by_sample(items: Iterable[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    best: Dict[str, Dict[str, Any]] = {}
    for item in items:
        sample_key = str(item.get("sample_id"))
        current = best.get(sample_key)
        if current is None or float(item["active_error_m"]) < float(current["active_error_m"]):
            best[sample_key] = item
    return dict(sorted(best.items(), key=lambda kv: int(kv[0])))


def _active_only_summary(best: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    active_errors = [float(row["active_error_m"]) for row in best.values() if row.get("active_error_m") is not None]
    within = [
        row.get("sample_id")
        for row in best.values()
        if row.get("active_error_m") is not None and float(row["active_error_m"]) <= 0.02
    ]
    return {
        "sample_count": len(best),
        "active_rmse_m": _rmse(active_errors),
        "active_within_2cm_count": len(within),
        "active_within_2cm_sample_ids": within,
        "active_bottlenecks_over_2cm": [
            {
                "sample_id": row.get("sample_id"),
                "label": row.get("label"),
                "active_error_m": row.get("active_error_m"),
                "target_error_m_at_active_best": row.get("target_error_m"),
                "config": row.get("config"),
            }
            for row in best.values()
            if row.get("active_error_m") is not None and float(row["active_error_m"]) > 0.02
        ],
    }


def _summary_from_best(best: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    active_errors = [float(row["active_error_m"]) for row in best.values() if row.get("active_error_m") is not None]
    in_play_pair_rows = [
        row
        for row in best.values()
        if row.get("target_error_m") is not None and row.get("unity_target_in_play") is not False
    ]
    target_errors = [
        float(row["target_error_m"])
        for row in in_play_pair_rows
    ]
    both_in_2cm = [
        row.get("sample_id")
        for row in in_play_pair_rows
        if row.get("active_error_m") is not None
        and float(row["active_error_m"]) <= 0.02
        and float(row["target_error_m"]) <= 0.02
    ]
    return {
        "sample_count": len(best),
        "in_play_pair_count": len(in_play_pair_rows),
        "active_rmse_m": _rmse(active_errors),
        "target_in_play_rmse_m": _rmse(target_errors),
        "both_endpoints_within_2cm_count": len(both_in_2cm),
        "both_endpoints_within_2cm_sample_ids": both_in_2cm,
        "all_in_play_pairs_within_2cm": len(both_in_2cm) == len(in_play_pair_rows) and bool(in_play_pair_rows),
        "bottlenecks_over_2cm": [
            {
                "sample_id": row.get("sample_id"),
                "label": row.get("label"),
                "active_error_m": row.get("active_error_m"),
                "target_error_m": row.get("target_error_m"),
                "max_endpoint_error_m": row.get("max_endpoint_error_m"),
                "config": row.get("config"),
            }
            for row in best.values()
            if row.get("target_error_m") is not None
            and (float(row["active_error_m"]) > 0.02 or float(row["target_error_m"]) > 0.02)
        ],
    }


def _contact_summary(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    items = list(_iter_items(path))
    if not items:
        return None
    report = _read_json(path)
    row = (report.get("result_sets") or [{}])[0].get("rows", [{}])[0]
    first_report = (row.get("stone_stone_contact_reports") or [{}])[0]
    first_point = (first_report.get("points") or [{}])[0]
    item = items[0]
    item.update(
        {
            "first_contact_time": row.get("first_stone_stone_contact_time"),
            "stone_stone_contact_report_count": row.get("stone_stone_contact_report_count"),
            "first_contact_count": first_report.get("contact_count"),
            "first_contact_normal": first_point.get("normal"),
            "first_contact_impulse": first_point.get("impulse"),
            "first_contact_separation": first_point.get("separation"),
        }
    )
    return item


def _tail_oracle_summary(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    report = _read_json(path)
    rows = report.get("rows") or []
    sample_id = rows[0].get("sample_id") if rows else None
    return {
        "source": str(path.relative_to(PROJECT_ROOT)),
        "sample_id": sample_id,
        "summary": report.get("summary"),
        "rows": rows,
    }


def build_report() -> Dict[str, Any]:
    baseline_best = _best_by_sample(_iter_items(BASELINE))
    handoff_items: List[Dict[str, Any]] = []
    for path in HANDOFF_REPORTS:
        handoff_items.extend(_iter_items(path))
    handoff_best = _best_by_sample(handoff_items)
    handoff_active_best = _best_active_by_sample(handoff_items)
    normal_12007_best = _best_by_sample(_iter_items(NORMAL_PARAM_12007)).get("12007")
    contact_best = [
        summary
        for summary in (_contact_summary(path) for path in CONTACT_BEST_REPORTS)
        if summary is not None
    ]
    tail_oracles = [
        summary
        for summary in (_tail_oracle_summary(path) for path in TAIL_ORACLE_AFTER_HANDOFF_BEST)
        if summary is not None
    ]

    return {
        "baseline_source": str(BASELINE.relative_to(PROJECT_ROOT)),
        "handoff_sources": [str(path.relative_to(PROJECT_ROOT)) for path in HANDOFF_REPORTS if path.exists()],
        "normal_param_12007_source": str(NORMAL_PARAM_12007.relative_to(PROJECT_ROOT)),
        "contact_best_sources": [str(path.relative_to(PROJECT_ROOT)) for path in CONTACT_BEST_REPORTS if path.exists()],
        "tail_oracle_after_handoff_best_sources": [
            str(path.relative_to(PROJECT_ROOT)) for path in TAIL_ORACLE_AFTER_HANDOFF_BEST if path.exists()
        ],
        "baseline_summary": _summary_from_best(baseline_best),
        "handoff_xy_oracle_summary": _summary_from_best(handoff_best),
        "handoff_xy_active_only_oracle_summary": _active_only_summary(handoff_active_best),
        "baseline_by_sample": baseline_best,
        "handoff_xy_oracle_by_sample": handoff_best,
        "handoff_xy_active_only_oracle_by_sample": handoff_active_best,
        "normal_param_12007_best": normal_12007_best,
        "contact_best_points": contact_best,
        "tail_oracle_after_handoff_best": tail_oracles,
        "interpretation": [
            "Entrance-state perturbations are a real lever: handoff x/y solves 12004/12006, a tiny handoff_v_scale solves 12003, and diagnostic target reset offsets solve 12007.",
            "The lever is not a global coordinate constant: the all-sample y=0 handoff-x sweep keeps the best target RMSE at the baseline x=0 setting.",
            "Adding an active handoff angular-velocity offset solves the last in-play pair bottleneck, 12005. The current per-sample entrance-state oracle has every in-play target pair under 2cm.",
            "If the score is active endpoint only, the same family of perturbations can put all 8 active stones under 2cm. That proves active endpoint drift is mostly entrance reconstruction, but it does not prove pair-contact parity.",
            "Sample 12005 is specifically sensitive to handoff angular velocity: vx/vy offsets and actor yaw did not improve it, while handoff_w_offset around -0.44rad/s gives active/target errors about 1.77cm/1.37cm.",
            "The required -0.44rad/s diagnostic offset is much larger than the visible sampled w value, so it should be read as missing angular/tangent native state or contact-row/cache state, not as a new proven managed formula.",
            "For 12007, target reset offsets bring both endpoints under 2cm, which points at active/target relative entrance geometry rather than a hard PhysX formula mismatch for that sample.",
        ],
    }


def main() -> None:
    report = build_report()
    DEFAULT_OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {DEFAULT_OUTPUT.relative_to(PROJECT_ROOT)}")
    print(json.dumps(report["handoff_xy_oracle_summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
