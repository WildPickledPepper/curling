#!/usr/bin/env python3
"""Compare local pyphysx contact reports with Unity-implied row deltas."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CALIBRATION = PROJECT_ROOT / "data" / "calibration"
CONTACT_PROBE = CALIBRATION / "unity_physx_collision_probe_unique_role_contact_report_current_best_20260709.json"
ROW_DELTA = CALIBRATION / "unity_collision_solver_row_delta_from_tail_oracle_020s_20260709.json"
DEFAULT_OUTPUT = CALIBRATION / "unity_collision_contact_report_vs_row_delta_20260709.json"


def _read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _vec2(values: Iterable[float]) -> Tuple[float, float]:
    rows = list(values)
    return float(rows[0]), float(rows[1])


def _physx_xy_to_protocol(vec: Iterable[float]) -> Tuple[float, float]:
    x, y = _vec2(vec)
    return -y, -x


def _angle_deg(vec: Iterable[float]) -> float:
    x, y = _vec2(vec)
    return math.degrees(math.atan2(y, x))


def _angle_delta_deg(a: float, b: float) -> float:
    return (a - b + 180.0) % 360.0 - 180.0


def _norm(vec: Iterable[float]) -> float:
    x, y = _vec2(vec)
    return math.hypot(x, y)


def _add_vec3(points: List[Dict[str, Any]], key: str) -> List[float]:
    total = [0.0, 0.0, 0.0]
    for point in points:
        for index, value in enumerate(point.get(key, [])[:3]):
            total[index] += float(value)
    return total


def _first_contact_row(row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    reports = row.get("stone_stone_contact_reports") or []
    for report in reports:
        if report.get("points"):
            return report
    return None


def _row_delta_by_sample(payload: Dict[str, Any]) -> Dict[int, Dict[str, Any]]:
    rows = payload.get("rows") or []
    return {int(row["sample_id"]): row for row in rows if row.get("status") == "ok"}


def _world_impulse_from_row_delta(row: Dict[str, Any], prefix: str) -> Tuple[float, float]:
    normal = _vec2(row["contact_normal"])
    tangent = _vec2(row["contact_tangent"])
    n = float(row[f"{prefix}_normal_Ns"])
    t = float(row[f"{prefix}_tangent_Ns"])
    return normal[0] * n + tangent[0] * t, normal[1] * n + tangent[1] * t


def build_report() -> Dict[str, Any]:
    contact_payload = _read_json(CONTACT_PROBE)
    row_delta_payload = _read_json(ROW_DELTA)
    result_set = (contact_payload.get("result_sets") or [])[0]
    delta_by_sample = _row_delta_by_sample(row_delta_payload)
    rows: List[Dict[str, Any]] = []
    for row in result_set.get("rows") or []:
        sample_id = int(row["sample_id"])
        first = _first_contact_row(row)
        if first is None:
            rows.append({"sample_id": sample_id, "status": "missing_contact_report"})
            continue
        points = first.get("points") or []
        impulse_physx = _add_vec3(points, "impulse")
        normal_physx = list(points[0].get("normal", [0.0, 0.0, 0.0]))
        # PhysX contact report impulse is for actor0. Convert it to target-side impulse.
        if first.get("active_is_actor0"):
            target_impulse_physx = [-value for value in impulse_physx]
            target_normal_physx = [-value for value in normal_physx]
        else:
            target_impulse_physx = impulse_physx
            target_normal_physx = normal_physx
        target_impulse_protocol = _physx_xy_to_protocol(target_impulse_physx)
        target_normal_protocol = _physx_xy_to_protocol(target_normal_physx)
        report_angle = _angle_deg(target_impulse_protocol)
        normal_angle = _angle_deg(target_normal_protocol)

        delta = delta_by_sample.get(sample_id)
        delta_fields: Dict[str, Any] = {}
        if delta:
            local_world = _world_impulse_from_row_delta(delta, "local_target_impulse")
            unity_world = _world_impulse_from_row_delta(delta, "unity_implied_target_impulse")
            local_angle = _angle_deg(local_world)
            unity_angle = _angle_deg(unity_world)
            delta_fields = {
                "row_delta_classification": delta.get("classification"),
                "endpoint_error_before_m": delta.get("endpoint_error_before_m"),
                "endpoint_error_after_tail_oracle_m": delta.get("endpoint_error_after_tail_oracle_m"),
                "row_delta_contact_normal_angle_deg": _angle_deg(delta["contact_normal"]),
                "local_row_delta_impulse_angle_deg": local_angle,
                "unity_implied_impulse_angle_deg": unity_angle,
                "unity_minus_contact_report_angle_deg": _angle_delta_deg(unity_angle, report_angle),
                "local_row_minus_contact_report_angle_deg": _angle_delta_deg(local_angle, report_angle),
                "unity_minus_local_row_angle_deg": _angle_delta_deg(unity_angle, local_angle),
                "tail_oracle_delta_impulse_normal_Ns": delta.get("tail_oracle_delta_impulse_normal_Ns"),
                "tail_oracle_delta_impulse_tangent_Ns": delta.get("tail_oracle_delta_impulse_tangent_Ns"),
            }

        face_pairs = [
            [point.get("internal_face_index0"), point.get("internal_face_index1")]
            for point in points
        ]
        rows.append(
            {
                "sample_id": sample_id,
                "label": row.get("label"),
                "status": "ok",
                "first_contact_time": first.get("time"),
                "contact_count": first.get("contact_count"),
                "point_count": len(points),
                "active_is_actor0": first.get("active_is_actor0"),
                "target_contact_normal_protocol": list(target_normal_protocol),
                "target_contact_normal_angle_deg": normal_angle,
                "target_contact_impulse_protocol_Ns": list(target_impulse_protocol),
                "target_contact_impulse_norm_Ns": _norm(target_impulse_protocol),
                "target_contact_impulse_angle_deg": report_angle,
                "target_contact_impulse_angle_minus_normal_deg": _angle_delta_deg(report_angle, normal_angle),
                "separation_min_m": min((float(point.get("separation")) for point in points), default=None),
                "separation_max_m": max((float(point.get("separation")) for point in points), default=None),
                "internal_face_index_pairs": face_pairs,
                **delta_fields,
            }
        )

    ok_rows = [row for row in rows if row.get("status") == "ok"]
    unity_minus_report = [
        abs(float(row["unity_minus_contact_report_angle_deg"]))
        for row in ok_rows
        if row.get("unity_minus_contact_report_angle_deg") is not None
    ]
    summary = {
        "row_count": len(rows),
        "ok_count": len(ok_rows),
        "all_first_contact_times": sorted({row.get("first_contact_time") for row in ok_rows}),
        "contact_report_angle_delta_abs_mean_deg": (
            sum(unity_minus_report) / len(unity_minus_report) if unity_minus_report else None
        ),
        "contact_report_angle_delta_abs_max_deg": max(unity_minus_report) if unity_minus_report else None,
        "worst_unity_minus_contact_report_sample": max(
            ok_rows,
            key=lambda row: abs(float(row.get("unity_minus_contact_report_angle_deg") or 0.0)),
            default=None,
        ),
    }
    return {
        "contact_probe": str(CONTACT_PROBE.relative_to(PROJECT_ROOT)),
        "row_delta": str(ROW_DELTA.relative_to(PROJECT_ROOT)),
        "summary": summary,
        "rows": rows,
        "interpretation": [
            "pyphysx contact reports now expose the local first stone-stone ContactPairPoint normal, separation and normal impulse.",
            "For sample 12003, the reported local contact impulse is aligned with the -87.19deg side-face normal, while Unity-implied impulse is about 5deg away, near the adjacent cooked-hull side normal.",
            "This moves the suspect layer from endpoint/tail replay to first-contact manifold feature selection, friction anchor/cache, or Unity runtime shape rotation/cooked stream.",
            "PxContactPairPoint internal face indices are 0xffffffff for these convex-convex reports, so they do not directly name the hull polygon.",
        ],
    }


def main() -> None:
    report = build_report()
    DEFAULT_OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {DEFAULT_OUTPUT.relative_to(PROJECT_ROOT)}")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
