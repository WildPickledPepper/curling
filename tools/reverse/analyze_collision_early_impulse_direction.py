#!/usr/bin/env python3
"""Analyze whether collision endpoint errors are set by early target impulse.

The PhysX replay reports include snapshots at 0.02s, 0.05s, ... after handoff.
This script compares the target's early velocity direction with both the
simulation endpoint direction and the Unity endpoint direction.  If the early
velocity direction and simulation endpoint direction agree, but both disagree
with Unity, the residual is contact/handoff at the first collision frames rather
than late sliding drift.
"""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_collision_early_impulse_direction_20260709.json"
DEFAULT_PROBES = [
    (
        "unique_role_current_best",
        PROJECT_ROOT / "data" / "calibration" / "unity_physx_collision_probe_unique_role_current_best_20260708.json",
    ),
    (
        "unique_role_formal_solid_inertia",
        PROJECT_ROOT
        / "data"
        / "calibration"
        / "unity_physx_collision_probe_unique_role_formal_geometry_rebuilt_unityflags_handoff292_20260708.json",
    ),
    (
        "unique_role_formal_cooked_inertia",
        PROJECT_ROOT
        / "data"
        / "calibration"
        / "unity_physx_collision_probe_unique_role_formal_geometry_cooked_inertia_20260709.json",
    ),
]

Vector = tuple[float, float]


def _vec2(values: Any) -> Vector:
    return (float(values[0]), float(values[1]))


def _sub(a: Vector, b: Vector) -> Vector:
    return (a[0] - b[0], a[1] - b[1])


def _dot(a: Vector, b: Vector) -> float:
    return a[0] * b[0] + a[1] * b[1]


def _cross(a: Vector, b: Vector) -> float:
    return a[0] * b[1] - a[1] * b[0]


def _norm(a: Vector) -> float:
    return math.hypot(a[0], a[1])


def _unit(a: Vector) -> Vector | None:
    length = _norm(a)
    if length <= 1e-12:
        return None
    return (a[0] / length, a[1] / length)


def _angle_deg(a: Vector, b: Vector) -> float | None:
    if _norm(a) <= 1e-12 or _norm(b) <= 1e-12:
        return None
    return math.degrees(math.atan2(_cross(a, b), _dot(a, b)))


def _abs_angle_deg(a: Vector, b: Vector) -> float | None:
    angle = _angle_deg(a, b)
    if angle is None:
        return None
    return abs(angle)


def _mean(values: Iterable[float]) -> float | None:
    rows = list(values)
    if not rows:
        return None
    return sum(rows) / len(rows)


def _rmse(values: Iterable[float]) -> float | None:
    rows = list(values)
    if not rows:
        return None
    return math.sqrt(sum(value * value for value in rows) / len(rows))


def _median(values: Iterable[float]) -> float | None:
    rows = sorted(values)
    if not rows:
        return None
    mid = len(rows) // 2
    if len(rows) % 2:
        return rows[mid]
    return 0.5 * (rows[mid - 1] + rows[mid])


def _closest_snapshot_key(snapshots: dict[str, Any], requested_time: float) -> str | None:
    candidates: list[tuple[float, str]] = []
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


def _row_metrics(row: dict[str, Any], snapshot_time: float) -> dict[str, Any]:
    snapshots = row.get("snapshots") or {}
    zero = snapshots.get("0.000000")
    key = _closest_snapshot_key(snapshots, snapshot_time)
    if not zero or not key:
        return {"sample_id": row.get("sample_id"), "status": "missing_snapshots"}
    if not row.get("unity_target_in_play"):
        return {"sample_id": row.get("sample_id"), "status": "unity_target_cleared"}

    target0 = _vec2(zero["target"]["position"])
    unity_target = _vec2(row["unity_target"])
    sim_target = _vec2(row["sim_target"])
    snapshot = snapshots[key]["target"]
    early_velocity = _vec2(snapshot["linear_velocity"])
    early_position = _vec2(snapshot["position"])

    unity_disp = _sub(unity_target, target0)
    sim_disp = _sub(sim_target, target0)
    early_disp = _sub(early_position, target0)
    endpoint_error = _sub(sim_target, unity_target)
    unity_axis = _unit(unity_disp)
    if unity_axis is None:
        return {"sample_id": row.get("sample_id"), "status": "zero_unity_displacement"}
    normal_axis = (-unity_axis[1], unity_axis[0])

    early_to_unity = _angle_deg(early_velocity, unity_disp)
    sim_final_to_unity = _angle_deg(sim_disp, unity_disp)
    early_to_sim_final = _angle_deg(early_velocity, sim_disp)
    early_disp_to_unity = _angle_deg(early_disp, unity_disp)

    unity_length = _norm(unity_disp)
    sim_length = _norm(sim_disp)
    return {
        "sample_id": int(row["sample_id"]),
        "label": row.get("label"),
        "status": "ok",
        "snapshot_key": key,
        "target0": list(target0),
        "unity_target": list(unity_target),
        "sim_target": list(sim_target),
        "unity_displacement_m": unity_length,
        "sim_displacement_m": sim_length,
        "sim_to_unity_distance_ratio": None if unity_length <= 1e-12 else sim_length / unity_length,
        "target_endpoint_error_m": _norm(endpoint_error),
        "target_endpoint_error_along_unity_m": _dot(endpoint_error, unity_axis),
        "target_endpoint_error_cross_unity_m": _dot(endpoint_error, normal_axis),
        "early_target_speed_mps": _norm(early_velocity),
        "early_velocity": list(early_velocity),
        "early_position": list(early_position),
        "early_velocity_to_unity_disp_deg": early_to_unity,
        "sim_final_disp_to_unity_disp_deg": sim_final_to_unity,
        "early_velocity_to_sim_final_disp_deg": early_to_sim_final,
        "early_position_disp_to_unity_disp_deg": early_disp_to_unity,
        "abs_early_velocity_to_unity_disp_deg": None if early_to_unity is None else abs(early_to_unity),
        "abs_sim_final_disp_to_unity_disp_deg": None if sim_final_to_unity is None else abs(sim_final_to_unity),
        "abs_early_velocity_to_sim_final_disp_deg": None
        if early_to_sim_final is None
        else abs(early_to_sim_final),
        "abs_early_position_disp_to_unity_disp_deg": None
        if early_disp_to_unity is None
        else abs(early_disp_to_unity),
    }


def _summarize_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    ok = [row for row in rows if row.get("status") == "ok"]

    def values(key: str) -> list[float]:
        return [float(row[key]) for row in ok if row.get(key) is not None]

    cross_errors = values("target_endpoint_error_cross_unity_m")
    along_errors = values("target_endpoint_error_along_unity_m")
    early_to_unity = values("abs_early_velocity_to_unity_disp_deg")
    final_to_unity = values("abs_sim_final_disp_to_unity_disp_deg")
    early_to_final = values("abs_early_velocity_to_sim_final_disp_deg")
    distance_ratios = values("sim_to_unity_distance_ratio")
    return {
        "row_count": len(rows),
        "ok_count": len(ok),
        "skipped_count": len(rows) - len(ok),
        "target_endpoint_rmse_m": _rmse(values("target_endpoint_error_m")),
        "target_cross_track_rmse_m": _rmse(cross_errors),
        "target_along_track_rmse_m": _rmse(along_errors),
        "target_cross_track_mean_abs_m": _mean(abs(value) for value in cross_errors),
        "target_along_track_mean_abs_m": _mean(abs(value) for value in along_errors),
        "early_velocity_to_unity_disp_abs_deg_mean": _mean(early_to_unity),
        "early_velocity_to_unity_disp_abs_deg_median": _median(early_to_unity),
        "sim_final_disp_to_unity_disp_abs_deg_mean": _mean(final_to_unity),
        "sim_final_disp_to_unity_disp_abs_deg_median": _median(final_to_unity),
        "early_velocity_to_sim_final_disp_abs_deg_mean": _mean(early_to_final),
        "early_velocity_to_sim_final_disp_abs_deg_median": _median(early_to_final),
        "sim_to_unity_distance_ratio_mean": _mean(distance_ratios),
        "sim_to_unity_distance_ratio_median": _median(distance_ratios),
    }


def _snapshot_drift_rows(row: dict[str, Any]) -> list[dict[str, Any]]:
    snapshots = row.get("snapshots") or {}
    zero = snapshots.get("0.000000")
    if not zero or not row.get("unity_target_in_play"):
        return []
    target0 = _vec2(zero["target"]["position"])
    unity_target = _vec2(row["unity_target"])
    unity_disp = _sub(unity_target, target0)
    unity_length = _norm(unity_disp)
    if unity_length <= 1e-12:
        return []

    rows: list[dict[str, Any]] = []
    for key, snapshot_pair in snapshots.items():
        try:
            time_s = float(key)
        except ValueError:
            continue
        if time_s <= 0.0:
            continue
        target_snapshot = snapshot_pair.get("target") or {}
        if "position" not in target_snapshot or "linear_velocity" not in target_snapshot:
            continue
        position = _vec2(target_snapshot["position"])
        velocity = _vec2(target_snapshot["linear_velocity"])
        displacement = _sub(position, target0)
        rows.append(
            {
                "sample_id": int(row["sample_id"]),
                "time_s": time_s,
                "position_disp_to_unity_disp_deg": _angle_deg(displacement, unity_disp),
                "velocity_to_unity_disp_deg": _angle_deg(velocity, unity_disp),
                "displacement_fraction_of_unity": _norm(displacement) / unity_length,
                "target_speed_mps": _norm(velocity),
            }
        )
    return rows


def _snapshot_drift_summary(probe_rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_time: dict[float, list[dict[str, Any]]] = {}
    for row in probe_rows:
        if row.get("status") != "ok":
            continue
        for item in row.get("snapshot_drift_rows") or []:
            by_time.setdefault(float(item["time_s"]), []).append(item)

    result: dict[str, Any] = {}
    for time_s, rows in sorted(by_time.items()):
        pos_angles = [
            abs(float(row["position_disp_to_unity_disp_deg"]))
            for row in rows
            if row.get("position_disp_to_unity_disp_deg") is not None
        ]
        vel_angles = [
            abs(float(row["velocity_to_unity_disp_deg"]))
            for row in rows
            if row.get("velocity_to_unity_disp_deg") is not None
        ]
        fractions = [float(row["displacement_fraction_of_unity"]) for row in rows]
        speeds = [float(row["target_speed_mps"]) for row in rows]
        result[f"{time_s:.6f}"] = {
            "count": len(rows),
            "position_disp_to_unity_abs_deg_mean": _mean(pos_angles),
            "position_disp_to_unity_abs_deg_median": _median(pos_angles),
            "velocity_to_unity_abs_deg_mean": _mean(vel_angles),
            "velocity_to_unity_abs_deg_median": _median(vel_angles),
            "displacement_fraction_of_unity_mean": _mean(fractions),
            "target_speed_mps_mean": _mean(speeds),
        }
    return result


def _load_probe(label: str, path: Path, snapshot_time: float) -> dict[str, Any]:
    report = json.loads(path.read_text(encoding="utf-8"))
    result_sets = report.get("result_sets") or []
    if not result_sets:
        rows = []
        summary = {}
        config = {}
    else:
        first = result_sets[0]
        rows = []
        raw_rows = first.get("rows") or []
        raw_by_sample_id = {int(row["sample_id"]): row for row in raw_rows if "sample_id" in row}
        for raw_row in raw_rows:
            metrics = _row_metrics(raw_row, snapshot_time)
            if metrics.get("status") == "ok":
                metrics["snapshot_drift_rows"] = _snapshot_drift_rows(raw_row)
            rows.append(metrics)
        summary = first.get("summary") or {}
        config = first.get("config") or {}
    return {
        "label": label,
        "path": str(path),
        "probe_summary": summary,
        "config_excerpt": {
            "radius": config.get("radius"),
            "height": config.get("height"),
            "center_height": config.get("center_height"),
            "inertia_model": config.get("inertia_model"),
            "inertia_radial": config.get("inertia_radial"),
            "inertia_vertical": config.get("inertia_vertical"),
            "contact_offset": config.get("contact_offset"),
            "handoff_extra": config.get("handoff_extra"),
        },
        "early_direction_summary": _summarize_rows(rows),
        "snapshot_drift_summary": _snapshot_drift_summary(rows),
        "rows": rows,
    }


def analyze(probes: list[tuple[str, Path]], snapshot_time: float) -> dict[str, Any]:
    results = [_load_probe(label, path, snapshot_time) for label, path in probes]
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "snapshot_time_s": snapshot_time,
        "inputs": [{"label": label, "path": str(path)} for label, path in probes],
        "results": results,
        "interpretation": (
            "If early_velocity_to_sim_final_disp is small but early_velocity_to_unity_disp "
            "and sim_final_disp_to_unity_disp are larger, the replay's first contact impulse "
            "already chooses the wrong target direction. That points to contact geometry, "
            "shape wrapper, handoff tick/state, or contact solver state rather than late sliding drift."
        ),
    }


def _parse_probe(value: str) -> tuple[str, Path]:
    if "=" not in value:
        path = Path(value)
        return path.stem, path
    label, path_text = value.split("=", 1)
    return label, Path(path_text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--probe",
        action="append",
        default=[],
        help="Probe report as label=path. Defaults to key unique-role reports.",
    )
    parser.add_argument("--snapshot-time", type=float, default=0.02)
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    probes = [_parse_probe(value) for value in args.probe] if args.probe else DEFAULT_PROBES
    result = analyze(probes, args.snapshot_time)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"output: {args.output}")
    for item in result["results"]:
        summary = item["early_direction_summary"]
        drift = item.get("snapshot_drift_summary") or {}
        drift_002 = drift.get("0.020000") or {}
        drift_200 = drift.get("2.000000") or {}
        print(
            f"{item['label']}: target RMSE={summary.get('target_endpoint_rmse_m')}, "
            f"early->final median deg={summary.get('early_velocity_to_sim_final_disp_abs_deg_median')}, "
            f"early->unity median deg={summary.get('early_velocity_to_unity_disp_abs_deg_median')}, "
            f"pos@0.02 median deg={drift_002.get('position_disp_to_unity_abs_deg_median')}, "
            f"pos@2.0 median deg={drift_200.get('position_disp_to_unity_abs_deg_median')}, "
            f"cross RMSE={summary.get('target_cross_track_rmse_m')}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
