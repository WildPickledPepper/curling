#!/usr/bin/env python3
"""Classify endpoint residuals as pair-impulse-like or late-tail-like.

``analyze_collision_impulse_residual.py`` estimates how the target stone's
early post-contact velocity would need to change to hit Unity's final endpoint.
This script extends that idea to both stones.  If the residual is caused by the
stone-stone impulse at first contact, the required active and target velocity
corrections should be close to equal and opposite.  If they are not, the error
is more likely coming from post-contact sliding/support state or from a bad
handoff for one stone.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.reverse.analyze_collision_impulse_residual import (
    MASS_KG,
    _angle_rad,
    _closest_snapshot_key,
    _cross,
    _dot,
    _mean,
    _mul,
    _norm,
    _read_probe,
    _rotate,
    _rmse,
    _sub,
    _unit,
    _vec2,
)


DEFAULT_PROBE = (
    PROJECT_ROOT
    / "data"
    / "calibration"
    / "unity_physx_collision_probe_unique_role_current_best_20260708.json"
)
DEFAULT_OUTPUT = (
    PROJECT_ROOT
    / "data"
    / "calibration"
    / "unity_collision_pair_impulse_residual_20260709.json"
)
DEFAULT_SNAPSHOT_TIMES = (0.02, 0.05, 0.1, 0.2)

Vector = Tuple[float, float]


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


def _median(values: Iterable[float]) -> Optional[float]:
    rows = sorted(values)
    if not rows:
        return None
    mid = len(rows) // 2
    if len(rows) % 2:
        return rows[mid]
    return 0.5 * (rows[mid - 1] + rows[mid])


def _stone_tail_residual(
    row: Dict[str, Any],
    role: str,
    snapshot_time: float,
) -> Dict[str, Any]:
    snapshots = row.get("snapshots") or {}
    key = _closest_snapshot_key(snapshots, snapshot_time)
    if not key:
        return {"role": role, "status": "missing_snapshot", "requested_time_s": snapshot_time}
    if role == "active":
        if not row.get("unity_active_in_play"):
            return {"role": role, "status": "unity_not_in_play", "requested_time_s": snapshot_time}
        unity_endpoint = _vec2(row["unity_active"])
        sim_endpoint = _vec2(row["sim_active"])
    elif role == "target":
        if not row.get("unity_target_in_play"):
            return {"role": role, "status": "unity_not_in_play", "requested_time_s": snapshot_time}
        unity_endpoint = _vec2(row["unity_target"])
        sim_endpoint = _vec2(row["sim_target"])
    else:
        raise ValueError(f"unsupported role: {role}")

    snapshot = snapshots[key][role]
    early_position = _vec2(snapshot["position"])
    early_velocity = _vec2(snapshot["linear_velocity"])
    sim_tail = _sub(sim_endpoint, early_position)
    unity_tail = _sub(unity_endpoint, early_position)
    sim_tail_len = _norm(sim_tail)
    unity_tail_len = _norm(unity_tail)
    early_speed = _norm(early_velocity)
    angle = _angle_rad(sim_tail, unity_tail)
    if angle is None or sim_tail_len <= 1e-12 or early_speed <= 1e-12:
        return {
            "role": role,
            "status": "degenerate_tail",
            "snapshot_key": key,
            "requested_time_s": snapshot_time,
            "early_speed_mps": early_speed,
            "sim_tail_m": sim_tail_len,
            "unity_tail_m": unity_tail_len,
        }

    scale = unity_tail_len / sim_tail_len
    required_velocity = _mul(_rotate(early_velocity, angle), scale)
    delta_v = _sub(required_velocity, early_velocity)
    endpoint_error = _norm(_sub(sim_endpoint, unity_endpoint))
    tail_quality_reasons: List[str] = []
    if sim_tail_len < 0.10:
        tail_quality_reasons.append("short_sim_tail")
    if unity_tail_len < 0.10:
        tail_quality_reasons.append("short_unity_tail")
    if not (0.5 <= scale <= 1.5):
        tail_quality_reasons.append("large_tail_scale")
    if early_speed < 0.02:
        tail_quality_reasons.append("low_early_speed")
    return {
        "role": role,
        "status": "ok",
        "tail_quality": "good" if not tail_quality_reasons else "weak",
        "tail_quality_reasons": tail_quality_reasons,
        "snapshot_key": key,
        "requested_time_s": snapshot_time,
        "early_position": list(early_position),
        "early_velocity": list(early_velocity),
        "early_speed_mps": early_speed,
        "sim_endpoint": list(sim_endpoint),
        "unity_endpoint": list(unity_endpoint),
        "endpoint_error_m": endpoint_error,
        "sim_tail_m": sim_tail_len,
        "unity_tail_m": unity_tail_len,
        "tail_distance_scale_required": scale,
        "tail_direction_delta_deg_required": math.degrees(angle),
        "required_early_velocity": list(required_velocity),
        "delta_v_required_mps": list(delta_v),
        "delta_v_required_norm_mps": _norm(delta_v),
    }


def _pair_row(row: Dict[str, Any], snapshot_time: float) -> Dict[str, Any]:
    active = _stone_tail_residual(row, "active", snapshot_time)
    target = _stone_tail_residual(row, "target", snapshot_time)
    result: Dict[str, Any] = {
        "sample_id": int(row["sample_id"]),
        "label": row.get("label"),
        "snapshot_time_s": snapshot_time,
        "active": active,
        "target": target,
    }
    if active.get("status") != "ok" or target.get("status") != "ok":
        result["status"] = "missing_role_residual"
        return result
    active_quality = active.get("tail_quality")
    target_quality = target.get("tail_quality")

    snapshots = row.get("snapshots") or {}
    zero = snapshots.get("0.000000")
    if not zero:
        result["status"] = "missing_zero_snapshot"
        return result
    active0 = _vec2(zero["active"]["position"])
    target0 = _vec2(zero["target"]["position"])
    normal = _unit(_sub(target0, active0)) or (0.0, -1.0)
    tangent = (-normal[1], normal[0])

    active_delta = _vec2(active["delta_v_required_mps"])
    target_delta = _vec2(target["delta_v_required_mps"])
    sum_delta = (active_delta[0] + target_delta[0], active_delta[1] + target_delta[1])
    relative_delta = (target_delta[0] - active_delta[0], target_delta[1] - active_delta[1])
    active_norm = _norm(active_delta)
    target_norm = _norm(target_delta)
    sum_norm = _norm(sum_delta)
    relative_norm = _norm(relative_delta)
    denom = active_norm + target_norm
    closure_fraction = None if denom <= 1e-12 else sum_norm / denom
    opposition_cosine = None
    if active_norm > 1e-12 and target_norm > 1e-12:
        opposition_cosine = _dot(active_delta, target_delta) / (active_norm * target_norm)

    if active_quality != "good" or target_quality != "good":
        classification = "pair_check_weak"
    elif closure_fraction is not None and opposition_cosine is not None:
        if closure_fraction < 0.35 and opposition_cosine < -0.5:
            classification = "pair_impulse_like"
        elif target_norm > 2.5 * max(active_norm, 1e-12):
            classification = "target_dominant"
        elif active_norm > 2.5 * max(target_norm, 1e-12):
            classification = "active_dominant"
        else:
            classification = "non_closing_pair"
    else:
        classification = "undetermined"

    result.update(
        {
            "status": "ok",
            "contact_normal": list(normal),
            "contact_tangent": list(tangent),
            "active_delta_normal_mps": _dot(active_delta, normal),
            "active_delta_tangent_mps": _dot(active_delta, tangent),
            "target_delta_normal_mps": _dot(target_delta, normal),
            "target_delta_tangent_mps": _dot(target_delta, tangent),
            "pair_delta_sum_mps": list(sum_delta),
            "pair_delta_sum_norm_mps": sum_norm,
            "pair_delta_relative_mps": list(relative_delta),
            "pair_delta_relative_norm_mps": relative_norm,
            "pair_impulse_closure_fraction": closure_fraction,
            "opposition_cosine": opposition_cosine,
            "equivalent_unbalanced_pair_impulse_Ns": sum_norm * MASS_KG,
            "classification": classification,
        }
    )
    return result


def _snapshot_stability(row: Dict[str, Any], snapshot_times: Sequence[float]) -> Dict[str, Any]:
    roles: Dict[str, Any] = {}
    for role in ("active", "target"):
        residuals = [_stone_tail_residual(row, role, time_value) for time_value in snapshot_times]
        ok = [item for item in residuals if item.get("status") == "ok"]
        norms = [float(item["delta_v_required_norm_mps"]) for item in ok]
        angles = [float(item["tail_direction_delta_deg_required"]) for item in ok]
        scales = [float(item["tail_distance_scale_required"]) for item in ok]
        roles[role] = {
            "residuals": residuals,
            "ok_count": len(ok),
            "delta_v_norm_mean_mps": _mean(norms),
            "delta_v_norm_range_mps": None if not norms else max(norms) - min(norms),
            "tail_direction_delta_abs_mean_deg": _mean(abs(value) for value in angles),
            "tail_scale_median": _median(scales),
        }
    return {"sample_id": int(row["sample_id"]), "label": row.get("label"), "roles": roles}


def _summarize(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    ok = [row for row in rows if row.get("status") == "ok"]

    def vals(key: str) -> List[float]:
        return [float(row[key]) for row in ok if row.get(key) is not None]

    classifications: Dict[str, int] = {}
    for row in ok:
        label = str(row.get("classification", "undetermined"))
        classifications[label] = classifications.get(label, 0) + 1

    return {
        "row_count": len(rows),
        "ok_count": len(ok),
        "classification_counts": classifications,
        "active_delta_rmse_mps": _rmse(
            row["active"]["delta_v_required_norm_mps"]
            for row in ok
            if row.get("active", {}).get("status") == "ok"
        ),
        "target_delta_rmse_mps": _rmse(
            row["target"]["delta_v_required_norm_mps"]
            for row in ok
            if row.get("target", {}).get("status") == "ok"
        ),
        "pair_delta_sum_mean_mps": _mean(vals("pair_delta_sum_norm_mps")),
        "pair_delta_sum_rmse_mps": _rmse(vals("pair_delta_sum_norm_mps")),
        "pair_impulse_closure_fraction_mean": _mean(vals("pair_impulse_closure_fraction")),
        "opposition_cosine_mean": _mean(vals("opposition_cosine")),
        "equivalent_unbalanced_pair_impulse_mean_Ns": _mean(vals("equivalent_unbalanced_pair_impulse_Ns")),
        "normal_residual_rmse_mps": {
            "active": _rmse(vals("active_delta_normal_mps")),
            "target": _rmse(vals("target_delta_normal_mps")),
        },
        "tangent_residual_rmse_mps": {
            "active": _rmse(vals("active_delta_tangent_mps")),
            "target": _rmse(vals("target_delta_tangent_mps")),
        },
    }


def analyze_probe(
    path: Path,
    *,
    snapshot_time: float,
    snapshot_times: Sequence[float],
    result_index: Optional[int],
) -> Dict[str, Any]:
    payload = _read_probe(path)
    result_set = _best_result_set(payload, result_index)
    rows = [_pair_row(row, snapshot_time) for row in result_set.get("rows") or []]
    stability = [_snapshot_stability(row, snapshot_times) for row in result_set.get("rows") or []]
    worst = sorted(
        [row for row in rows if row.get("status") == "ok"],
        key=lambda row: float(row.get("target", {}).get("endpoint_error_m") or 0.0),
        reverse=True,
    )[:5]
    return {
        "probe": str(path),
        "snapshot_time_s": snapshot_time,
        "snapshot_times_s": list(snapshot_times),
        "probe_summary": result_set.get("summary"),
        "config_excerpt": {
            key: (result_set.get("config") or {}).get(key)
            for key in (
                "radius",
                "height",
                "center_height",
                "stone_restitution",
                "stone_friction",
                "ice_friction",
                "contact_offset",
                "combine_mode",
                "rink_geometry",
            )
        },
        "summary": _summarize(rows),
        "worst_rows": worst,
        "rows": rows,
        "snapshot_stability": stability,
        "interpretation": [
            "pair_impulse_like means active and target endpoint-inferred early velocity corrections are approximately equal and opposite.",
            "non_closing_pair means the residual cannot be explained by a single missing pair impulse at the chosen snapshot.",
            "This is still endpoint-inferred evidence; it narrows the suspect layer but does not replace a Unity ContactBuffer/SolverContact dump.",
        ],
    }


def _parse_times(value: str) -> List[float]:
    return [float(part.strip()) for part in value.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probe", type=Path, default=DEFAULT_PROBE)
    parser.add_argument("--snapshot-time", type=float, default=0.02)
    parser.add_argument("--snapshot-times", default=",".join(str(value) for value in DEFAULT_SNAPSHOT_TIMES))
    parser.add_argument("--result-index", type=int, default=None)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    probe_path = args.probe if args.probe.is_absolute() else PROJECT_ROOT / args.probe
    report = analyze_probe(
        probe_path,
        snapshot_time=args.snapshot_time,
        snapshot_times=_parse_times(args.snapshot_times),
        result_index=args.result_index,
    )
    output = args.output if args.output.is_absolute() else PROJECT_ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = report["summary"]
    print(f"wrote {output.relative_to(PROJECT_ROOT)}")
    print("classification_counts=" + json.dumps(summary["classification_counts"], sort_keys=True))
    print(f"pair_delta_sum_mean_mps={summary['pair_delta_sum_mean_mps']:.6f}")
    print(f"closure_fraction_mean={summary['pair_impulse_closure_fraction_mean']:.6f}")
    print(f"opposition_cosine_mean={summary['opposition_cosine_mean']:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
