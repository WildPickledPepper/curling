#!/usr/bin/env python3
"""Project tail-oracle velocity corrections back onto first collision solver rows.

``analyze_collision_tail_replay_oracle`` showed that changing only the target
stone's early horizontal velocity can drive endpoints to Unity within
millimeters.  This script converts that velocity correction into an equivalent
normal/tangent impulse delta and compares it with the local 0.00s-0.01s target
collision impulse.

The output is a row-level localization aid: it does not claim the delta is the
literal PhysX applied impulse, but it tells us which solver-row family must
change to make the endpoint match.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LOCAL_IMPULSE = PROJECT_ROOT / "data" / "calibration" / "unity_collision_local_impulse_trace_20260709.json"
DEFAULT_TAIL_ORACLE = PROJECT_ROOT / "data" / "calibration" / "unity_collision_tail_replay_oracle_002s_20260709.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_collision_solver_row_delta_from_tail_oracle_20260709.json"

MASS_KG = 19.1


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _mean(values: Iterable[float]) -> Optional[float]:
    rows = [float(value) for value in values if value is not None]
    if not rows:
        return None
    return sum(rows) / len(rows)


def _rmse(values: Iterable[float]) -> Optional[float]:
    rows = [float(value) for value in values if value is not None]
    if not rows:
        return None
    return math.sqrt(sum(value * value for value in rows) / len(rows))


def _dominant(normal: float, tangent: float) -> str:
    if abs(tangent) > 1.25 * abs(normal):
        return "tangent"
    if abs(normal) > 1.25 * abs(tangent):
        return "normal"
    return "mixed"


def _angle_deg(normal: float, tangent: float) -> float:
    return math.degrees(math.atan2(tangent, normal))


def _classify(delta_normal: float, delta_tangent: float, local_normal: float, local_tangent: float) -> str:
    dominant = _dominant(delta_normal, delta_tangent)
    implied_tangent = local_tangent + delta_tangent
    if local_tangent * implied_tangent < 0.0:
        return "tangent_sign_flip_contact_basis_or_cache"
    if dominant == "tangent":
        return "friction_row_contact_point_or_cache"
    if dominant == "normal":
        return "normal_row_magnitude_or_separation_bias"
    return "mixed_contact_manifold"


def build_report(local_impulse_path: Path, tail_oracle_path: Path) -> Dict[str, Any]:
    local_impulse = _read_json(local_impulse_path)
    tail_oracle = _read_json(tail_oracle_path)
    local_by_sample = {
        int(row["sample_id"]): row
        for row in local_impulse.get("rows", [])
        if row.get("status") == "ok" and row.get("main_local_interval")
    }

    rows: List[Dict[str, Any]] = []
    for tail_row in tail_oracle.get("rows", []):
        if tail_row.get("status") != "ok":
            continue
        sample_id = int(tail_row["sample_id"])
        local_row = local_by_sample.get(sample_id)
        if not local_row:
            rows.append({"sample_id": sample_id, "status": "missing_local_impulse"})
            continue

        main = local_row["main_local_interval"]
        local_normal = float(main["target_impulse_normal_Ns"])
        local_tangent = float(main["target_impulse_tangent_Ns"])
        delta_normal = float(tail_row["oracle_linear_delta_v_normal_mps"]) * MASS_KG
        delta_tangent = float(tail_row["oracle_linear_delta_v_tangent_mps"]) * MASS_KG
        implied_normal = local_normal + delta_normal
        implied_tangent = local_tangent + delta_tangent
        local_angle = _angle_deg(local_normal, local_tangent)
        implied_angle = _angle_deg(implied_normal, implied_tangent)
        angle_delta = implied_angle - local_angle
        if angle_delta > 180.0:
            angle_delta -= 360.0
        if angle_delta < -180.0:
            angle_delta += 360.0
        local_norm = math.hypot(local_normal, local_tangent)
        delta_norm = math.hypot(delta_normal, delta_tangent)
        implied_norm = math.hypot(implied_normal, implied_tangent)
        row = {
            "sample_id": sample_id,
            "label": tail_row.get("label"),
            "status": "ok",
            "endpoint_error_before_m": tail_row.get("local_full_vs_unity_m"),
            "endpoint_error_after_tail_oracle_m": tail_row.get("oracle_linear_tail_vs_unity_m"),
            "local_target_impulse_normal_Ns": local_normal,
            "local_target_impulse_tangent_Ns": local_tangent,
            "local_target_impulse_norm_Ns": float(main["target_impulse_norm_Ns"]),
            "tail_oracle_delta_impulse_normal_Ns": delta_normal,
            "tail_oracle_delta_impulse_tangent_Ns": delta_tangent,
            "tail_oracle_delta_impulse_norm_Ns": delta_norm,
            "unity_implied_target_impulse_normal_Ns": implied_normal,
            "unity_implied_target_impulse_tangent_Ns": implied_tangent,
            "unity_implied_target_impulse_norm_Ns": implied_norm,
            "delta_fraction_of_local_impulse": None if local_norm <= 1e-12 else delta_norm / local_norm,
            "normal_scale_vs_local": None if abs(local_normal) <= 1e-12 else implied_normal / local_normal,
            "tangent_scale_vs_local": None if abs(local_tangent) <= 1e-12 else implied_tangent / local_tangent,
            "local_impulse_angle_deg_in_contact_frame": local_angle,
            "unity_implied_impulse_angle_deg_in_contact_frame": implied_angle,
            "impulse_angle_delta_deg": angle_delta,
            "equivalent_small_angle_from_tangent_delta_deg": None
            if abs(local_normal) <= 1e-12
            else math.degrees(delta_tangent / local_normal),
            "delta_dominant_axis": _dominant(delta_normal, delta_tangent),
            "classification": _classify(delta_normal, delta_tangent, local_normal, local_tangent),
            "tail_oracle_delta_v_component": tail_row.get("oracle_linear_delta_v_component"),
            "tail_oracle_delta_v_norm_mps": tail_row.get("oracle_linear_delta_v_norm_from_snapshot_mps"),
            "contact_normal": main.get("contact_normal"),
            "contact_tangent": main.get("contact_tangent"),
        }
        rows.append(row)

    ok = [row for row in rows if row.get("status") == "ok"]

    def vals(key: str) -> List[float]:
        return [float(row[key]) for row in ok if row.get(key) is not None]

    classifications: Dict[str, int] = {}
    dominant_counts: Dict[str, int] = {}
    for row in ok:
        classifications[row["classification"]] = classifications.get(row["classification"], 0) + 1
        dominant_counts[row["delta_dominant_axis"]] = dominant_counts.get(row["delta_dominant_axis"], 0) + 1

    worst = sorted(ok, key=lambda row: float(row.get("endpoint_error_before_m") or 0.0), reverse=True)
    return {
        "local_impulse": str(local_impulse_path.relative_to(PROJECT_ROOT)),
        "tail_oracle": str(tail_oracle_path.relative_to(PROJECT_ROOT)),
        "summary": {
            "row_count": len(rows),
            "ok_count": len(ok),
            "endpoint_before_rmse_m": _rmse(vals("endpoint_error_before_m")),
            "endpoint_after_tail_oracle_rmse_m": _rmse(vals("endpoint_error_after_tail_oracle_m")),
            "delta_impulse_norm_mean_Ns": _mean(vals("tail_oracle_delta_impulse_norm_Ns")),
            "delta_impulse_norm_rmse_Ns": _rmse(vals("tail_oracle_delta_impulse_norm_Ns")),
            "delta_fraction_of_local_impulse_mean": _mean(vals("delta_fraction_of_local_impulse")),
            "delta_fraction_of_local_impulse_rmse": _rmse(vals("delta_fraction_of_local_impulse")),
            "normal_scale_mean": _mean(vals("normal_scale_vs_local")),
            "normal_scale_rmse_from_1": _rmse(value - 1.0 for value in vals("normal_scale_vs_local")),
            "tangent_scale_mean": _mean(vals("tangent_scale_vs_local")),
            "impulse_angle_delta_abs_mean_deg": _mean(abs(value) for value in vals("impulse_angle_delta_deg")),
            "impulse_angle_delta_abs_rmse_deg": _rmse(abs(value) for value in vals("impulse_angle_delta_deg")),
            "classification_counts": classifications,
            "delta_dominant_axis_counts": dominant_counts,
        },
        "worst_rows": worst[:5],
        "rows": rows,
        "interpretation": [
            "The tail oracle makes the endpoint match by only changing target vx/vy; this report maps that change back into the first contact frame.",
            "A tangent_sign_flip classification means the local friction/contact-point basis is qualitatively wrong for that sample, not merely slightly scaled.",
            "normal_row classifications point at contact normal, separation bias, restitution or normal applied-force magnitude.",
            "friction_row classifications point at tangent basis, friction anchors/cache or contact point angular coupling.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local-impulse", type=Path, default=DEFAULT_LOCAL_IMPULSE)
    parser.add_argument("--tail-oracle", type=Path, default=DEFAULT_TAIL_ORACLE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    local_impulse_path = args.local_impulse if args.local_impulse.is_absolute() else PROJECT_ROOT / args.local_impulse
    tail_oracle_path = args.tail_oracle if args.tail_oracle.is_absolute() else PROJECT_ROOT / args.tail_oracle
    output_path = args.output if args.output.is_absolute() else PROJECT_ROOT / args.output
    report = build_report(local_impulse_path, tail_oracle_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {output_path.relative_to(PROJECT_ROOT)}")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
