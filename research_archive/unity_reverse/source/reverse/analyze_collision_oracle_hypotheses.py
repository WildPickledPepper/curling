#!/usr/bin/env python3
"""Classify what existing collision oracle winners are really substituting for.

The parameter oracle can get some individual endpoints close to Unity, but its
per-sample winning configs are not necessarily physically valid. This script
turns those winners into a hypothesis report: which hidden native-state detail
does each artificial knob appear to stand in for?
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ORACLE = (
    PROJECT_ROOT / "data" / "calibration" / "unity_collision_parameter_oracle_floor_20260709.json"
)
DEFAULT_OUTPUT = (
    PROJECT_ROOT / "data" / "calibration" / "unity_collision_oracle_hypothesis_audit_20260709.json"
)

EPS = 1e-9
FORMAL_RADIUS_M = 0.140875
COMPENSATED_RADIUS_M = 0.146
FORMAL_CENTER_HEIGHT_M = 0.115
COMPENSATED_CENTER_HEIGHT_M = 0.1276
UNITY_CONTACT_OFFSET_M = 0.01
UNITY_RESTITUTION = 1.0
UNITY_ICE_FRICTION = 0.02
UNITY_STONE_FRICTION = 0.6
UNITY_SOLVER_POSITION_ITERATIONS = 6
UNITY_SOLVER_VELOCITY_ITERATIONS = 1
COOKED_INERTIA_RADIAL = 0.178810612362
COOKED_INERTIA_VERTICAL = 0.189222883199


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _close(value: Any, expected: float, tol: float = 1e-6) -> bool:
    if value is None:
        return False
    return abs(float(value) - expected) <= tol


def _nonzero(value: Any, tol: float = 1e-9) -> bool:
    return value is not None and abs(float(value)) > tol


def _config_value(config: Dict[str, Any], key: str, default: Any = None) -> Any:
    return config.get(key, default)


def _classify_config(config: Dict[str, Any]) -> List[str]:
    tags: List[str] = []

    radius = _config_value(config, "radius")
    if radius is not None:
        radius_f = float(radius)
        if _close(radius_f, FORMAL_RADIUS_M, 5e-6):
            tags.append("formal_radius")
        elif _close(radius_f, COMPENSATED_RADIUS_M, 5e-6):
            tags.append("compensated_radius_0.146")
        elif radius_f > COMPENSATED_RADIUS_M + 5e-6:
            tags.append("inflated_radius")
        elif radius_f < COMPENSATED_RADIUS_M - 5e-6:
            tags.append("shrunk_radius")

    if _nonzero(_config_value(config, "active_yaw")):
        tags.append("active_rotation_yaw")
    if _nonzero(_config_value(config, "target_yaw")):
        tags.append("target_rotation_yaw")

    if _nonzero(_config_value(config, "handoff_x_offset")):
        tags.append("handoff_position_x_offset")
    if _nonzero(_config_value(config, "handoff_y_offset")):
        tags.append("handoff_position_y_offset")
    if not _close(_config_value(config, "handoff_v_scale", 1.0), 1.0, 1e-9):
        tags.append("handoff_velocity_scale")

    if _nonzero(_config_value(config, "shape_local_x")):
        tags.append("shape_local_x_offset")
    if _nonzero(_config_value(config, "shape_local_y")):
        tags.append("shape_local_y_offset")
    if _nonzero(_config_value(config, "shape_local_z")):
        tags.append("shape_local_z_offset")
    if _nonzero(_config_value(config, "shape_local_yaw")):
        tags.append("shape_local_yaw")

    handoff_friction = _config_value(config, "handoff_friction")
    if handoff_friction is not None and not _close(handoff_friction, 0.001, 1e-12):
        tags.append("handoff_friction_changed")

    vertex_limit = _config_value(config, "convex_vertex_limit")
    quantized_count = _config_value(config, "convex_quantized_count")
    stone_faces = _config_value(config, "stone_faces")
    if vertex_limit is not None and int(vertex_limit) < 255:
        tags.append("reduced_convex_vertex_limit")
    if quantized_count is not None and int(quantized_count) < 255:
        tags.append("reduced_convex_quantized_count")
    if stone_faces is not None and int(stone_faces) != 256:
        tags.append("changed_source_mesh_faces")

    center_height = _config_value(config, "center_height")
    if center_height is not None:
        if _close(center_height, FORMAL_CENTER_HEIGHT_M, 5e-6):
            tags.append("formal_center_height")
        elif _close(center_height, COMPENSATED_CENTER_HEIGHT_M, 5e-6):
            tags.append("compensated_center_height")
        else:
            tags.append("other_center_height")

    contact_offset = _config_value(config, "contact_offset")
    if contact_offset is not None and not _close(contact_offset, UNITY_CONTACT_OFFSET_M, 1e-9):
        tags.append("contact_offset_changed")

    restitution = _config_value(config, "stone_restitution")
    if restitution is not None and not _close(restitution, UNITY_RESTITUTION, 1e-9):
        tags.append("restitution_changed")
    stone_friction = _config_value(config, "stone_friction")
    if stone_friction is not None and not _close(stone_friction, UNITY_STONE_FRICTION, 1e-9):
        tags.append("stone_friction_changed")
    ice_friction = _config_value(config, "ice_friction")
    if ice_friction is not None and not _close(ice_friction, UNITY_ICE_FRICTION, 1e-9):
        tags.append("ice_friction_changed")

    inertia_model = _config_value(config, "inertia_model")
    inertia_radial = _config_value(config, "inertia_radial")
    inertia_vertical = _config_value(config, "inertia_vertical")
    if inertia_model == "custom":
        if _close(inertia_radial, COOKED_INERTIA_RADIAL, 1e-6) and _close(
            inertia_vertical, COOKED_INERTIA_VERTICAL, 1e-6
        ):
            tags.append("formal_cooked_inertia")
        else:
            tags.append("custom_inertia")
    elif inertia_model and inertia_model != "solid-cylinder":
        tags.append(f"inertia_model_{inertia_model}")

    if bool(_config_value(config, "lock_upright", False)):
        tags.append("lock_upright")
    if bool(_config_value(config, "disable_stone_gravity", False)):
        tags.append("disable_stone_gravity")

    rink_geometry = _config_value(config, "rink_geometry")
    if rink_geometry == "unity-plane-mesh":
        tags.append("rink_triangle_mesh")
    elif rink_geometry and rink_geometry != "plane":
        tags.append(f"rink_geometry_{rink_geometry}")

    if _config_value(config, "solver_position_iterations") not in (None, UNITY_SOLVER_POSITION_ITERATIONS):
        tags.append("solver_position_iterations_changed")
    if _config_value(config, "solver_velocity_iterations") not in (None, UNITY_SOLVER_VELOCITY_ITERATIONS):
        tags.append("solver_velocity_iterations_changed")

    if not tags:
        tags.append("nominal_or_unclassified")
    return tags


def _round_value(value: Any) -> Any:
    if isinstance(value, float):
        return round(value, 12)
    if isinstance(value, list):
        return tuple(_round_value(item) for item in value)
    return value


def _config_signature(config: Dict[str, Any]) -> Dict[str, Any]:
    keys = [
        "radius",
        "height",
        "stone_faces",
        "convex_vertex_limit",
        "convex_quantized_count",
        "active_yaw",
        "target_yaw",
        "handoff_x_offset",
        "handoff_y_offset",
        "handoff_v_scale",
        "handoff_friction",
        "shape_local_x",
        "shape_local_y",
        "shape_local_z",
        "shape_local_yaw",
        "center_height",
        "contact_offset",
        "stone_restitution",
        "stone_friction",
        "ice_friction",
        "inertia_model",
        "inertia_radial",
        "inertia_vertical",
        "lock_upright",
        "disable_stone_gravity",
        "rink_geometry",
        "rink_mesh_center_x",
        "rink_mesh_center_y",
        "rink_mesh_width",
        "rink_mesh_length",
        "rink_mesh_subdivisions",
    ]
    return {key: _round_value(config.get(key)) for key in keys if key in config}


def _summarize_rows(rows: Sequence[Dict[str, Any]], metric_key: str) -> Dict[str, Any]:
    tag_counts: Counter[str] = Counter()
    parameter_values: Dict[str, Counter[Any]] = defaultdict(Counter)
    per_sample: List[Dict[str, Any]] = []

    for row in rows:
        config = row.get("config") or {}
        tags = _classify_config(config)
        tag_counts.update(tags)
        for key, value in _config_signature(config).items():
            parameter_values[key][_round_value(value)] += 1
        per_sample.append(
            {
                "sample_id": row.get("sample_id"),
                "label": row.get("label"),
                metric_key: row.get(metric_key),
                "target_error_m": row.get("target_error_m"),
                "active_error_m": row.get("active_error_m"),
                "source_sample_id": row.get("source_sample_id"),
                "file": row.get("file"),
                "result_index": row.get("result_index"),
                "tags": tags,
                "config_signature": _config_signature(config),
            }
        )

    conflicts = {}
    for key, counts in sorted(parameter_values.items()):
        values = [{"value": value, "count": count} for value, count in counts.most_common()]
        if len(values) > 1:
            conflicts[key] = values

    return {
        "tag_counts": dict(tag_counts.most_common()),
        "conflicting_parameter_values": conflicts,
        "per_sample": per_sample,
    }


def _top_global_hypotheses(rows: Sequence[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
    output = []
    for row in rows[:limit]:
        config = row.get("config") or {}
        output.append(
            {
                "file": row.get("file"),
                "result_index": row.get("result_index"),
                "score": row.get("score"),
                "target_in_play_rmse_m": (row.get("summary") or {}).get("target_in_play_rmse_m"),
                "active_rmse_m": (row.get("summary") or {}).get("active_rmse_m"),
                "tags": _classify_config(config),
                "config_signature": _config_signature(config),
            }
        )
    return output


def _interpret(target_summary: Dict[str, Any], pair_summary: Dict[str, Any]) -> List[str]:
    target_conflicts = target_summary["conflicting_parameter_values"]
    pair_conflicts = pair_summary["conflicting_parameter_values"]
    notes = []
    if "radius" in target_conflicts or "radius" in pair_conflicts:
        notes.append(
            "Per-sample winners require different effective radii. Treat radius changes as a proxy for "
            "missing shape/local-pose/contact-manifold state, not as a valid global radius."
        )
    if any(
        key in target_conflicts or key in pair_conflicts
        for key in ("active_yaw", "target_yaw", "handoff_x_offset", "handoff_y_offset", "handoff_v_scale")
    ):
        notes.append(
            "Several winners modify yaw or handoff state. This points at the first-contact native input "
            "state rather than late endpoint friction."
        )
    if any(
        tag in target_summary["tag_counts"] or tag in pair_summary["tag_counts"]
        for tag in ("reduced_convex_vertex_limit", "reduced_convex_quantized_count", "changed_source_mesh_faces")
    ):
        notes.append(
            "Some winners alter convex topology. This is not compatible with a single formal stone mesh; "
            "it suggests current pyphysx shape/contact manifold is still standing in for Unity's runtime shape."
        )
    if any(
        tag in target_summary["tag_counts"] or tag in pair_summary["tag_counts"]
        for tag in (
            "shape_local_x_offset",
            "shape_local_y_offset",
            "shape_local_z_offset",
            "shape_local_yaw",
        )
    ):
        notes.append(
            "Shape local-pose changes appear only as small local improvements in the current grids. "
            "If their global RMSE remains high, simple common shape offsets should be deprioritized."
        )
    notes.append(
        "Because the target-only and active+target winners disagree, endpoint tuning cannot be promoted to "
        "the training simulator. The next proof target is the exact native state at first contact."
    )
    return notes


def build_report(oracle: Dict[str, Any], top_global_limit: int) -> Dict[str, Any]:
    target_rows = oracle.get("target_only_oracle", {}).get("per_sample_best") or []
    pair_rows = oracle.get("active_and_target_pair_oracle", {}).get("per_sample_best") or []
    target_summary = _summarize_rows(target_rows, "target_error_m")
    pair_summary = _summarize_rows(pair_rows, "pair_rmse_m")
    return {
        "source_oracle_report": oracle.get("probe_files"),
        "oracle_threshold_m": oracle.get("threshold_m"),
        "processed_probe_file_count": oracle.get("processed_probe_file_count"),
        "processed_result_set_count": oracle.get("processed_result_set_count"),
        "target_only_oracle_summary": {
            key: value
            for key, value in (oracle.get("target_only_oracle") or {}).items()
            if key != "per_sample_best"
        },
        "active_and_target_pair_oracle_summary": {
            key: value
            for key, value in (oracle.get("active_and_target_pair_oracle") or {}).items()
            if key != "per_sample_best"
        },
        "top_global_hypotheses": _top_global_hypotheses(
            oracle.get("best_global_result_sets") or [], top_global_limit
        ),
        "target_only_winner_hypotheses": target_summary,
        "active_and_target_pair_winner_hypotheses": pair_summary,
        "interpretation": _interpret(target_summary, pair_summary),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--oracle", type=Path, default=DEFAULT_ORACLE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--top-global-limit", type=int, default=10)
    args = parser.parse_args()

    oracle = _read_json(args.oracle)
    report = build_report(oracle, args.top_global_limit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"source probe files: {report['processed_probe_file_count']}")
    print(f"source result sets: {report['processed_result_set_count']}")
    print("target winner tags:", report["target_only_winner_hypotheses"]["tag_counts"])
    print("pair winner tags:", report["active_and_target_pair_winner_hypotheses"]["tag_counts"])
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
