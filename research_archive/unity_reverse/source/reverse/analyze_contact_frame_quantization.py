#!/usr/bin/env python3
"""Compare required contact-frame rotations with cooked-hull facet angles.

The recovered formal-stone hull is a 64-sided prism.  If the remaining solver
row delta is caused by feature/manifold selection, the implied impulse direction
should often move toward a neighboring side-face normal rather than toward a
global constant angle.  This script checks that hypothesis against the existing
row-delta report and cooked hull topology.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROW_DELTA = PROJECT_ROOT / "data" / "calibration" / "unity_collision_solver_row_delta_from_tail_oracle_20260709.json"
DEFAULT_TOPOLOGY = PROJECT_ROOT / "data" / "calibration" / "pyphysx_raw_hull_topology_20260708.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_collision_contact_frame_quantization_20260709.json"


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _wrap_deg(angle: float) -> float:
    while angle > 180.0:
        angle -= 360.0
    while angle <= -180.0:
        angle += 360.0
    return angle


def _angle_diff_deg(a: float, b: float) -> float:
    return _wrap_deg(a - b)


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


def _nearest_angle(angle: float, candidates: List[float]) -> Tuple[float, float]:
    best = min(candidates, key=lambda candidate: abs(_angle_diff_deg(angle, candidate)))
    return best, _angle_diff_deg(angle, best)


def _side_face_angles(topology: Dict[str, Any]) -> List[float]:
    angles = []
    for poly in topology.get("polygon_summaries", []):
        if poly.get("class") == "side_quad" and poly.get("side_normal_angle_degrees") is not None:
            angles.append(float(poly["side_normal_angle_degrees"]))
    return sorted(angles)


def _uniform_angles(step: float, phase: float) -> List[float]:
    return [_wrap_deg(phase + step * index) for index in range(int(round(360.0 / step)))]


def _angle_from_vec2(vec: List[float]) -> float:
    return math.degrees(math.atan2(float(vec[1]), float(vec[0])))


def build_report(row_delta_path: Path, topology_path: Path) -> Dict[str, Any]:
    row_delta = _read_json(row_delta_path)
    topology = _read_json(topology_path)
    side_angles = _side_face_angles(topology)
    if not side_angles:
        raise ValueError("topology report has no side face angles")

    counts = topology.get("counts", {})
    polygon_counts = counts.get("polygon_class_counts", {})
    side_step_deg = float(polygon_counts.get("side_normal_step_min_mdeg", 5625)) / 1000.0
    half_step_deg = 0.5 * side_step_deg
    face_phase = min(side_angles, key=abs)
    vertex_angles = _uniform_angles(side_step_deg, face_phase + half_step_deg)

    rows = []
    for source in row_delta.get("rows", []):
        if source.get("status") != "ok":
            continue
        center_angle = _angle_from_vec2(source["contact_normal"])
        # The impulse angles in the row-delta report are measured in the center-line
        # contact frame.  Add them back to get world/protocol-frame impulse directions.
        local_impulse_angle = _wrap_deg(center_angle + float(source["local_impulse_angle_deg_in_contact_frame"]))
        implied_impulse_angle = _wrap_deg(center_angle + float(source["unity_implied_impulse_angle_deg_in_contact_frame"]))

        center_face, center_face_delta = _nearest_angle(center_angle, side_angles)
        local_face, local_face_delta = _nearest_angle(local_impulse_angle, side_angles)
        implied_face, implied_face_delta = _nearest_angle(implied_impulse_angle, side_angles)
        implied_vertex, implied_vertex_delta = _nearest_angle(implied_impulse_angle, vertex_angles)
        local_vertex, local_vertex_delta = _nearest_angle(local_impulse_angle, vertex_angles)

        feature_switch = abs(implied_face_delta) < abs(local_face_delta) - 1e-9
        crosses_midplane = abs(_angle_diff_deg(local_impulse_angle, center_face)) > half_step_deg and abs(
            _angle_diff_deg(implied_impulse_angle, center_face)
        ) <= half_step_deg
        rows.append(
            {
                "sample_id": source["sample_id"],
                "label": source.get("label"),
                "classification": source.get("classification"),
                "endpoint_error_before_m": source.get("endpoint_error_before_m"),
                "center_line_angle_deg": center_angle,
                "local_impulse_world_angle_deg": local_impulse_angle,
                "unity_implied_impulse_world_angle_deg": implied_impulse_angle,
                "required_angle_delta_deg": source.get("impulse_angle_delta_deg"),
                "required_angle_delta_as_side_steps": None
                if source.get("impulse_angle_delta_deg") is None
                else float(source["impulse_angle_delta_deg"]) / side_step_deg,
                "nearest_center_side_face_angle_deg": center_face,
                "center_to_side_face_delta_deg": center_face_delta,
                "nearest_local_side_face_angle_deg": local_face,
                "local_to_side_face_delta_deg": local_face_delta,
                "nearest_implied_side_face_angle_deg": implied_face,
                "implied_to_side_face_delta_deg": implied_face_delta,
                "nearest_local_vertex_angle_deg": local_vertex,
                "local_to_vertex_delta_deg": local_vertex_delta,
                "nearest_implied_vertex_angle_deg": implied_vertex,
                "implied_to_vertex_delta_deg": implied_vertex_delta,
                "implied_closer_to_side_face_than_local": feature_switch,
                "crosses_toward_center_side_face_cell": crosses_midplane,
                "side_step_deg": side_step_deg,
                "half_side_step_deg": half_step_deg,
                "hull_world_radius_minus_apothem_m": (topology.get("geometry_summary") or {}).get(
                    "world_radius_minus_apothem_m"
                ),
            }
        )

    ok = rows
    vals = lambda key: [float(row[key]) for row in ok if row.get(key) is not None]
    worst = sorted(ok, key=lambda row: float(row.get("endpoint_error_before_m") or 0.0), reverse=True)
    return {
        "row_delta": str(row_delta_path.relative_to(PROJECT_ROOT)),
        "topology": str(topology_path.relative_to(PROJECT_ROOT)),
        "hull_summary": {
            "side_face_count": len(side_angles),
            "side_normal_step_deg": side_step_deg,
            "half_side_step_deg": half_step_deg,
            "world_radius_minus_apothem_m": (topology.get("geometry_summary") or {}).get(
                "world_radius_minus_apothem_m"
            ),
            "side_angle_phase_deg": face_phase,
        },
        "summary": {
            "row_count": len(rows),
            "required_angle_delta_abs_mean_deg": _mean(abs(value) for value in vals("required_angle_delta_deg")),
            "required_angle_delta_abs_rmse_deg": _rmse(abs(value) for value in vals("required_angle_delta_deg")),
            "required_angle_delta_abs_max_deg": max(
                (abs(value) for value in vals("required_angle_delta_deg")), default=None
            ),
            "required_angle_delta_abs_mean_side_steps": _mean(
                abs(value) for value in vals("required_angle_delta_as_side_steps")
            ),
            "implied_to_side_face_abs_mean_deg": _mean(abs(value) for value in vals("implied_to_side_face_delta_deg")),
            "feature_switch_like_count": sum(1 for row in rows if row["implied_closer_to_side_face_than_local"]),
            "crosses_toward_center_side_face_cell_count": sum(
                1 for row in rows if row["crosses_toward_center_side_face_cell"]
            ),
        },
        "worst_rows": worst[:5],
        "rows": rows,
        "interpretation": [
            "The formal cooked hull is a 64-sided prism, so adjacent side-face normals are 5.625 degrees apart.",
            "A required impulse-angle delta of several degrees is the same order as a side-face/edge feature switch, not a small floating-point drift.",
            "12003 moving from the center-line frame toward the neighboring side-face normal supports a contact feature/tangent-basis/cache explanation.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--row-delta", type=Path, default=DEFAULT_ROW_DELTA)
    parser.add_argument("--topology", type=Path, default=DEFAULT_TOPOLOGY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    row_delta_path = args.row_delta if args.row_delta.is_absolute() else PROJECT_ROOT / args.row_delta
    topology_path = args.topology if args.topology.is_absolute() else PROJECT_ROOT / args.topology
    output_path = args.output if args.output.is_absolute() else PROJECT_ROOT / args.output
    report = build_report(row_delta_path, topology_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {output_path.relative_to(PROJECT_ROOT)}")
    print(json.dumps(report["hull_summary"], ensure_ascii=False, indent=2, sort_keys=True))
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
