#!/usr/bin/env python3
"""Compare local PhysX step impulses with Unity-inferred residual impulses.

The probe snapshots record body velocities after every local 0.01s step.  This
script estimates the local horizontal impulse given to the target stone by
differencing consecutive target velocities, then compares that impulse with the
endpoint-inferred impulse needed to land on Unity's endpoint.

It is not a replacement for a ContactBuffer/SolverContact dump: support friction
and solver integration are mixed into the velocity differences.  It does,
however, tell us whether the Unity-vs-local gap is a tiny percentage of the
local collision impulse or a completely different impulse scale.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PROBE = (
    PROJECT_ROOT
    / "data"
    / "calibration"
    / "unity_physx_collision_probe_unique_role_current_best_step_snapshots_20260709.json"
)
DEFAULT_IMPULSE = PROJECT_ROOT / "data" / "calibration" / "unity_collision_impulse_residual_refresh_20260709.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_collision_local_impulse_trace_20260709.json"

MASS_KG = 19.1

Vec2 = Tuple[float, float]


def _read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _vec2(values: Iterable[float]) -> Vec2:
    a, b = list(values)[:2]
    return (float(a), float(b))


def _sub(a: Vec2, b: Vec2) -> Vec2:
    return (a[0] - b[0], a[1] - b[1])


def _add(a: Vec2, b: Vec2) -> Vec2:
    return (a[0] + b[0], a[1] + b[1])


def _mul(a: Vec2, scale: float) -> Vec2:
    return (a[0] * scale, a[1] * scale)


def _dot(a: Vec2, b: Vec2) -> float:
    return a[0] * b[0] + a[1] * b[1]


def _norm(a: Vec2) -> float:
    return math.hypot(a[0], a[1])


def _unit(a: Vec2) -> Optional[Vec2]:
    n = _norm(a)
    if n <= 1e-12:
        return None
    return (a[0] / n, a[1] / n)


def _mean(values: Iterable[float]) -> Optional[float]:
    vals = [float(value) for value in values if value is not None]
    if not vals:
        return None
    return sum(vals) / len(vals)


def _rmse(values: Iterable[float]) -> Optional[float]:
    vals = [float(value) for value in values if value is not None]
    if not vals:
        return None
    return math.sqrt(sum(value * value for value in vals) / len(vals))


def _result_set(report: Dict[str, Any]) -> Dict[str, Any]:
    result_sets = report.get("result_sets") or []
    if not result_sets:
        raise ValueError("probe has no result_sets")
    return result_sets[0]


def _impulse_rows(report: Dict[str, Any]) -> Dict[int, Dict[str, Any]]:
    for result in report.get("results", []):
        if result.get("label") in {"unique_role_current_best_refresh", "unique_role_current_best"}:
            return {int(row["sample_id"]): row for row in result.get("rows", [])}
    if report.get("results"):
        return {int(row["sample_id"]): row for row in report["results"][0].get("rows", [])}
    return {}


def _velocity(snapshot: Dict[str, Any], actor: str) -> Vec2:
    return _vec2(snapshot[actor]["linear_velocity"])


def _position(snapshot: Dict[str, Any], actor: str) -> Vec2:
    return _vec2(snapshot[actor]["position"])


def _dominant_axis(normal: float, tangent: float) -> str:
    abs_normal = abs(normal)
    abs_tangent = abs(tangent)
    if abs_normal <= 1e-12 and abs_tangent <= 1e-12:
        return "none"
    if abs_normal >= 1.75 * abs_tangent:
        return "normal"
    if abs_tangent >= 1.75 * abs_normal:
        return "tangent"
    return "mixed"


def _interval_rows(row: Dict[str, Any]) -> List[Dict[str, Any]]:
    snapshots = row.get("snapshots") or {}
    times = sorted(float(key) for key in snapshots)
    out = []
    for t0, t1 in zip(times, times[1:]):
        if t1 > 0.2000001:
            continue
        s0 = snapshots[f"{t0:.6f}"]
        s1 = snapshots[f"{t1:.6f}"]
        active_dv = _sub(_velocity(s1, "active"), _velocity(s0, "active"))
        target_dv = _sub(_velocity(s1, "target"), _velocity(s0, "target"))
        pair_dv_sum = _add(active_dv, target_dv)
        contact_normal = _unit(_sub(_position(s0, "target"), _position(s0, "active"))) or (0.0, -1.0)
        contact_tangent = (-contact_normal[1], contact_normal[0])
        target_normal = _dot(target_dv, contact_normal)
        target_tangent = _dot(target_dv, contact_tangent)
        out.append(
            {
                "t0": t0,
                "t1": t1,
                "target_delta_v_mps": list(target_dv),
                "target_delta_v_norm_mps": _norm(target_dv),
                "target_impulse_Ns": list(_mul(target_dv, MASS_KG)),
                "target_impulse_norm_Ns": _norm(target_dv) * MASS_KG,
                "target_impulse_normal_Ns": target_normal * MASS_KG,
                "target_impulse_tangent_Ns": target_tangent * MASS_KG,
                "target_dominant_axis": _dominant_axis(target_normal, target_tangent),
                "active_delta_v_mps": list(active_dv),
                "active_delta_v_norm_mps": _norm(active_dv),
                "active_impulse_norm_Ns": _norm(active_dv) * MASS_KG,
                "pair_delta_v_sum_norm_mps": _norm(pair_dv_sum),
                "pair_impulse_sum_norm_Ns": _norm(pair_dv_sum) * MASS_KG,
                "contact_normal": list(contact_normal),
                "contact_tangent": list(contact_tangent),
            }
        )
    return out


def _compare_row(row: Dict[str, Any], impulse_row: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    intervals = _interval_rows(row)
    main = None
    if intervals:
        main = max(intervals, key=lambda item: item["target_delta_v_norm_mps"])

    out: Dict[str, Any] = {
        "sample_id": row.get("sample_id"),
        "label": row.get("label"),
        "target_error_m": row.get("target_error"),
        "main_local_interval": main,
        "intervals": intervals,
    }
    if impulse_row is None or impulse_row.get("status") != "ok" or main is None:
        out["status"] = "no_unity_residual"
        return out

    required_norm = float(impulse_row["required_impulse_norm_Ns"])
    required_normal = float(impulse_row["required_impulse_normal_Ns"])
    required_tangent = float(impulse_row["required_impulse_tangent_Ns"])
    local_norm = float(main["target_impulse_norm_Ns"])
    local_normal = float(main["target_impulse_normal_Ns"])
    local_tangent = float(main["target_impulse_tangent_Ns"])
    implied_normal = local_normal + required_normal
    implied_tangent = local_tangent + required_tangent
    implied_norm = math.hypot(implied_normal, implied_tangent)
    residual_fraction = None if local_norm <= 1e-12 else required_norm / local_norm
    normal_fraction = None if abs(local_normal) <= 1e-12 else required_normal / local_normal
    tangent_fraction = None if abs(local_tangent) <= 1e-12 else required_tangent / local_tangent
    implied_normal_scale = None if abs(local_normal) <= 1e-12 else implied_normal / local_normal
    implied_tangent_scale = None if abs(local_tangent) <= 1e-12 else implied_tangent / local_tangent

    out.update(
        {
            "status": "ok",
            "unity_required_impulse_norm_Ns": required_norm,
            "unity_required_impulse_normal_Ns": required_normal,
            "unity_required_impulse_tangent_Ns": required_tangent,
            "unity_required_dominant_axis": impulse_row.get("dominant_delta_v_component"),
            "residual_fraction_of_local_target_impulse": residual_fraction,
            "normal_fraction_of_local_target_impulse": normal_fraction,
            "tangent_fraction_of_local_target_impulse": tangent_fraction,
            "unity_implied_target_impulse_norm_Ns": implied_norm,
            "unity_implied_target_impulse_normal_Ns": implied_normal,
            "unity_implied_target_impulse_tangent_Ns": implied_tangent,
            "unity_implied_normal_scale_vs_local": implied_normal_scale,
            "unity_implied_tangent_scale_vs_local": implied_tangent_scale,
            "unity_implied_tangent_sign_flip": local_tangent * implied_tangent < 0.0,
            "local_minus_required_impulse_norm_Ns": local_norm - required_norm,
            "local_impulse_dominant_axis": main["target_dominant_axis"],
            "same_dominant_axis": main["target_dominant_axis"] == impulse_row.get("dominant_delta_v_component"),
        }
    )
    return out


def build_report(probe_path: Path, impulse_path: Path) -> Dict[str, Any]:
    probe = _read_json(probe_path)
    impulse = _read_json(impulse_path)
    impulse_by_sample = _impulse_rows(impulse)
    rows = [_compare_row(row, impulse_by_sample.get(int(row["sample_id"]))) for row in _result_set(probe).get("rows", [])]
    ok_rows = [row for row in rows if row.get("status") == "ok"]

    def vals(key: str) -> List[float]:
        return [float(row[key]) for row in ok_rows if row.get(key) is not None]

    main_intervals = [row["main_local_interval"] for row in ok_rows if row.get("main_local_interval")]
    summary = {
        "row_count": len(rows),
        "ok_count": len(ok_rows),
        "main_interval_counts": {},
        "local_target_impulse_norm_mean_Ns": _mean(item["target_impulse_norm_Ns"] for item in main_intervals),
        "local_target_impulse_norm_rmse_Ns": _rmse(item["target_impulse_norm_Ns"] for item in main_intervals),
        "unity_required_impulse_norm_mean_Ns": _mean(vals("unity_required_impulse_norm_Ns")),
        "unity_required_impulse_norm_rmse_Ns": _rmse(vals("unity_required_impulse_norm_Ns")),
        "residual_fraction_mean": _mean(vals("residual_fraction_of_local_target_impulse")),
        "residual_fraction_rmse": _rmse(vals("residual_fraction_of_local_target_impulse")),
        "unity_implied_normal_scale_mean": _mean(vals("unity_implied_normal_scale_vs_local")),
        "unity_implied_normal_scale_rmse_from_1": _rmse(
            row["unity_implied_normal_scale_vs_local"] - 1.0
            for row in ok_rows
            if row.get("unity_implied_normal_scale_vs_local") is not None
        ),
        "unity_implied_tangent_scale_mean": _mean(vals("unity_implied_tangent_scale_vs_local")),
        "unity_implied_tangent_sign_flip_count": sum(1 for row in ok_rows if row.get("unity_implied_tangent_sign_flip")),
        "same_dominant_axis_count": sum(1 for row in ok_rows if row.get("same_dominant_axis")),
    }
    for item in main_intervals:
        label = f"{item['t0']:.2f}-{item['t1']:.2f}"
        summary["main_interval_counts"][label] = summary["main_interval_counts"].get(label, 0) + 1

    return {
        "probe": str(probe_path.relative_to(PROJECT_ROOT)),
        "impulse": str(impulse_path.relative_to(PROJECT_ROOT)),
        "summary": summary,
        "rows": rows,
        "interpretation": [
            "The local target impulse is estimated from consecutive snapshot velocity differences, so it includes solver output plus support/friction integration effects.",
            "A residual_fraction around a few percent means the endpoint gap is a small row/manifold perturbation of the local collision impulse, not a wholly different collision event.",
            "Dominant-axis disagreement points at friction tangent basis/contact point/cache differences; dominant normal residuals point at normal row magnitude, normal, restitution, or separation bias.",
        ],
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", type=Path, default=DEFAULT_PROBE)
    parser.add_argument("--impulse", type=Path, default=DEFAULT_IMPULSE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    probe_path = args.probe if args.probe.is_absolute() else PROJECT_ROOT / args.probe
    impulse_path = args.impulse if args.impulse.is_absolute() else PROJECT_ROOT / args.impulse
    output_path = args.output if args.output.is_absolute() else PROJECT_ROOT / args.output

    report = build_report(probe_path, impulse_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {output_path.relative_to(PROJECT_ROOT)}")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
