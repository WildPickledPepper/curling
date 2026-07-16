#!/usr/bin/env python3
"""Infer early post-contact velocity/impulse residuals from endpoint errors.

The local PhysX probe stores snapshots shortly after handoff/contact.  This
script asks: if the post-snapshot sliding model were correct, how much would the
target stone's early velocity need to be scaled/rotated to land on Unity's
endpoint?  The answer is not a replacement simulator; it is a diagnostic for
whether the residual looks like missing normal impulse, tangential impulse, or a
late sliding drift.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MASS_KG = 19.1
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_collision_impulse_residual_20260709.json"
DEFAULT_PROBES = [
    (
        "unique_role_current_best",
        PROJECT_ROOT / "data" / "calibration" / "unity_physx_collision_probe_unique_role_current_best_20260708.json",
    ),
    (
        "unique_role_material_baseline",
        PROJECT_ROOT
        / "data"
        / "calibration"
        / "unity_physx_collision_probe_unique_role_material_timing_baseline_20260709.json",
    ),
]

Vector = Tuple[float, float]


def _vec2(values: Sequence[float]) -> Vector:
    return (float(values[0]), float(values[1]))


def _add(a: Vector, b: Vector) -> Vector:
    return (a[0] + b[0], a[1] + b[1])


def _sub(a: Vector, b: Vector) -> Vector:
    return (a[0] - b[0], a[1] - b[1])


def _mul(a: Vector, scalar: float) -> Vector:
    return (a[0] * scalar, a[1] * scalar)


def _dot(a: Vector, b: Vector) -> float:
    return a[0] * b[0] + a[1] * b[1]


def _cross(a: Vector, b: Vector) -> float:
    return a[0] * b[1] - a[1] * b[0]


def _norm(a: Vector) -> float:
    return math.hypot(a[0], a[1])


def _unit(a: Vector) -> Optional[Vector]:
    length = _norm(a)
    if length <= 1e-12:
        return None
    return (a[0] / length, a[1] / length)


def _rotate(a: Vector, angle_rad: float) -> Vector:
    c = math.cos(angle_rad)
    s = math.sin(angle_rad)
    return (a[0] * c - a[1] * s, a[0] * s + a[1] * c)


def _angle_rad(a: Vector, b: Vector) -> Optional[float]:
    if _norm(a) <= 1e-12 or _norm(b) <= 1e-12:
        return None
    return math.atan2(_cross(a, b), _dot(a, b))


def _mean(values: Iterable[float]) -> Optional[float]:
    rows = list(values)
    if not rows:
        return None
    return sum(rows) / len(rows)


def _rmse(values: Iterable[float]) -> Optional[float]:
    rows = list(values)
    if not rows:
        return None
    return math.sqrt(sum(value * value for value in rows) / len(rows))


def _median(values: Iterable[float]) -> Optional[float]:
    rows = sorted(values)
    if not rows:
        return None
    mid = len(rows) // 2
    if len(rows) % 2:
        return rows[mid]
    return 0.5 * (rows[mid - 1] + rows[mid])


def _closest_snapshot_key(snapshots: Dict[str, Any], requested_time: float) -> Optional[str]:
    candidates: List[Tuple[float, str]] = []
    for key in snapshots:
        try:
            time_value = float(key)
        except ValueError:
            continue
        if time_value <= 0.0:
            continue
        candidates.append((abs(time_value - requested_time), key))
    if not candidates:
        return None
    candidates.sort()
    return candidates[0][1]


def _read_probe(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _best_result_set(payload: Dict[str, Any], result_index: Optional[int]) -> Dict[str, Any]:
    result_sets = payload.get("result_sets") or []
    if not result_sets:
        raise ValueError("probe has no result_sets")
    if result_index is not None:
        return result_sets[result_index]
    return min(
        result_sets,
        key=lambda result_set: float("inf")
        if (result_set.get("summary") or {}).get("combined_rmse_m") is None
        else float((result_set.get("summary") or {})["combined_rmse_m"]),
    )


def _row_residual(row: Dict[str, Any], snapshot_time: float) -> Dict[str, Any]:
    snapshots = row.get("snapshots") or {}
    zero = snapshots.get("0.000000")
    key = _closest_snapshot_key(snapshots, snapshot_time)
    if not zero or not key:
        return {"sample_id": row.get("sample_id"), "status": "missing_snapshots"}
    if not row.get("unity_target_in_play"):
        return {"sample_id": row.get("sample_id"), "status": "unity_target_cleared"}

    active0 = _vec2(zero["active"]["position"])
    target0 = _vec2(zero["target"]["position"])
    snapshot = snapshots[key]["target"]
    early_position = _vec2(snapshot["position"])
    early_velocity = _vec2(snapshot["linear_velocity"])
    unity_target = _vec2(row["unity_target"])
    sim_target = _vec2(row["sim_target"])

    sim_tail = _sub(sim_target, early_position)
    unity_tail = _sub(unity_target, early_position)
    sim_tail_len = _norm(sim_tail)
    unity_tail_len = _norm(unity_tail)
    early_speed = _norm(early_velocity)
    angle = _angle_rad(sim_tail, unity_tail)
    speed_scale = None if sim_tail_len <= 1e-12 else unity_tail_len / sim_tail_len

    if angle is None or speed_scale is None:
        required_velocity = None
        delta_v = None
    else:
        required_velocity = _mul(_rotate(early_velocity, angle), speed_scale)
        delta_v = _sub(required_velocity, early_velocity)

    contact_normal = _unit(_sub(target0, active0))
    if contact_normal is None:
        contact_normal = (0.0, -1.0)
    contact_tangent = (-contact_normal[1], contact_normal[0])

    endpoint_error = _sub(sim_target, unity_target)
    delta_v_norm = _norm(delta_v) if delta_v is not None else None
    delta_v_normal = _dot(delta_v, contact_normal) if delta_v is not None else None
    delta_v_tangent = _dot(delta_v, contact_tangent) if delta_v is not None else None
    required_impulse = None if delta_v_norm is None else delta_v_norm * MASS_KG
    required_impulse_normal = None if delta_v_normal is None else delta_v_normal * MASS_KG
    required_impulse_tangent = None if delta_v_tangent is None else delta_v_tangent * MASS_KG
    if delta_v_normal is None or delta_v_tangent is None:
        dominant_component = None
    elif abs(delta_v_tangent) > abs(delta_v_normal) * 1.25:
        dominant_component = "tangent"
    elif abs(delta_v_normal) > abs(delta_v_tangent) * 1.25:
        dominant_component = "normal"
    else:
        dominant_component = "mixed"

    unity_disp_from_zero = _sub(unity_target, target0)
    sim_disp_from_zero = _sub(sim_target, target0)
    contact_angle_to_unity = _angle_rad(contact_normal, unity_disp_from_zero)
    early_velocity_to_contact = _angle_rad(early_velocity, contact_normal)

    return {
        "sample_id": int(row["sample_id"]),
        "label": row.get("label"),
        "status": "ok",
        "snapshot_key": key,
        "active0": list(active0),
        "target0": list(target0),
        "early_position": list(early_position),
        "early_velocity": list(early_velocity),
        "early_speed_mps": early_speed,
        "sim_target": list(sim_target),
        "unity_target": list(unity_target),
        "endpoint_error_m": _norm(endpoint_error),
        "sim_tail_m": sim_tail_len,
        "unity_tail_m": unity_tail_len,
        "tail_distance_scale_required": speed_scale,
        "tail_direction_delta_deg_required": None if angle is None else math.degrees(angle),
        "required_early_velocity": None if required_velocity is None else list(required_velocity),
        "delta_v_required_mps": None if delta_v is None else list(delta_v),
        "delta_v_required_norm_mps": delta_v_norm,
        "delta_v_required_normal_mps": delta_v_normal,
        "delta_v_required_tangent_mps": delta_v_tangent,
        "delta_v_required_fraction_of_early_speed": None
        if delta_v_norm is None or early_speed <= 1e-12
        else delta_v_norm / early_speed,
        "dominant_delta_v_component": dominant_component,
        "required_impulse_norm_Ns": required_impulse,
        "required_impulse_normal_Ns": required_impulse_normal,
        "required_impulse_tangent_Ns": required_impulse_tangent,
        "contact_normal": list(contact_normal),
        "contact_tangent": list(contact_tangent),
        "contact_normal_to_unity_disp_deg": None
        if contact_angle_to_unity is None
        else math.degrees(contact_angle_to_unity),
        "early_velocity_to_contact_normal_deg": None
        if early_velocity_to_contact is None
        else math.degrees(early_velocity_to_contact),
        "target_error_m": row.get("target_error"),
        "active_error_m": row.get("active_error"),
    }


def _summarize(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    ok = [row for row in rows if row.get("status") == "ok"]

    def vals(key: str) -> List[float]:
        return [float(row[key]) for row in ok if row.get(key) is not None]

    component_counts: Dict[str, int] = {}
    for row in ok:
        component = row.get("dominant_delta_v_component")
        if component:
            component_counts[component] = component_counts.get(component, 0) + 1

    return {
        "row_count": len(rows),
        "ok_count": len(ok),
        "skipped_count": len(rows) - len(ok),
        "endpoint_rmse_m": _rmse(vals("endpoint_error_m")),
        "delta_v_norm_rmse_mps": _rmse(vals("delta_v_required_norm_mps")),
        "delta_v_norm_mean_mps": _mean(vals("delta_v_required_norm_mps")),
        "delta_v_normal_rmse_mps": _rmse(vals("delta_v_required_normal_mps")),
        "delta_v_tangent_rmse_mps": _rmse(vals("delta_v_required_tangent_mps")),
        "required_impulse_norm_mean_Ns": _mean(vals("required_impulse_norm_Ns")),
        "required_impulse_norm_max_Ns": max(vals("required_impulse_norm_Ns")) if vals("required_impulse_norm_Ns") else None,
        "delta_v_fraction_of_early_speed_mean": _mean(vals("delta_v_required_fraction_of_early_speed")),
        "dominant_delta_v_component_counts": component_counts,
        "tail_distance_scale_required_mean": _mean(vals("tail_distance_scale_required")),
        "tail_distance_scale_required_median": _median(vals("tail_distance_scale_required")),
        "tail_direction_delta_abs_deg_mean": _mean(abs(value) for value in vals("tail_direction_delta_deg_required")),
        "tail_direction_delta_abs_deg_median": _median(abs(value) for value in vals("tail_direction_delta_deg_required")),
        "early_velocity_to_contact_abs_deg_mean": _mean(abs(value) for value in vals("early_velocity_to_contact_normal_deg")),
        "contact_normal_to_unity_abs_deg_mean": _mean(abs(value) for value in vals("contact_normal_to_unity_disp_deg")),
    }


def analyze_probe(label: str, path: Path, snapshot_time: float, result_index: Optional[int]) -> Dict[str, Any]:
    payload = _read_probe(path)
    result_set = _best_result_set(payload, result_index)
    rows = [_row_residual(row, snapshot_time) for row in result_set.get("rows") or []]
    worst = sorted(
        [row for row in rows if row.get("status") == "ok"],
        key=lambda row: float(row.get("endpoint_error_m") or 0.0),
        reverse=True,
    )[:5]
    return {
        "label": label,
        "path": str(path),
        "probe_summary": result_set.get("summary"),
        "config_excerpt": {
            key: (result_set.get("config") or {}).get(key)
            for key in (
                "radius",
                "height",
                "center_height",
                "stone_restitution",
                "contact_offset",
                "handoff_x_offset",
                "handoff_y_offset",
                "handoff_v_scale",
                "pre_collision_dynamic_friction",
                "pre_collision_static_friction",
                "material_switch_mode",
            )
        },
        "summary": _summarize(rows),
        "worst_rows": worst,
        "rows": rows,
    }


def _parse_probe_arg(values: Optional[List[str]]) -> List[Tuple[str, Path]]:
    if not values:
        return DEFAULT_PROBES
    probes = []
    for value in values:
        if "=" in value:
            label, path_text = value.split("=", 1)
        else:
            path = Path(value)
            label = path.stem
            path_text = value
        probes.append((label, Path(path_text)))
    return probes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probe", action="append", help="label=path or path. Can be repeated.")
    parser.add_argument("--snapshot-time", type=float, default=0.02)
    parser.add_argument("--result-index", type=int, default=None)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    probes = _parse_probe_arg(args.probe)
    report = {
        "snapshot_time_s": args.snapshot_time,
        "mass_kg": MASS_KG,
        "results": [
            analyze_probe(label, path if path.is_absolute() else PROJECT_ROOT / path, args.snapshot_time, args.result_index)
            for label, path in probes
        ],
        "interpretation": [
            "delta_v_required is the early target velocity correction that would make the post-snapshot tail point to Unity's endpoint under a local linear approximation.",
            "Large normal components point at missing normal impulse/contact normal. Large tangent components point at contact point/friction/rotation coupling.",
            "This is a diagnostic only; it should guide native contact/cooked-stream reverse engineering, not become a residual correction model.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    for result in report["results"]:
        summary = result["summary"]
        print(
            result["label"],
            f"endpoint_rmse={summary['endpoint_rmse_m']:.6f}",
            f"delta_v_mean={summary['delta_v_norm_mean_mps']:.6f}",
            f"delta_v_tangent_rmse={summary['delta_v_tangent_rmse_mps']:.6f}",
            f"delta_v_normal_rmse={summary['delta_v_normal_rmse_mps']:.6f}",
        )
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
