#!/usr/bin/env python3
"""Replay Unity finalizer bodyFrame poses through local pyphysx contact generation.

This is a targeted native-state parity probe, not an endpoint sweep.  It takes
the captured Unity stone-stone finalizer bodyFrame0/bodyFrame1 transforms and
asks local PhysX immediate contact generation what manifold it would create for
the same relative pose.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    import pyphysx
except ImportError as exc:  # pragma: no cover - depends on external env.
    raise SystemExit("pyphysx is required; run with the pyphysx conda Python") from exc

from tools.reverse.probe_physx_collision_alignment import (
    DEFAULT_FORMAL_STONE_MESH,
    HEIGHT,
    _combine_mode_from_name,
    _formal_stone_points,
    _make_stone,
    _stone_points,
)


DEFAULT_UNITY = PROJECT_ROOT / "data" / "calibration" / "unity_physx_native_solver_state_withwriteback_20260709.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_finalizer_pose_contact_replay_20260709.json"


def _yaw_from_unity_y_up_quat(q: Dict[str, float]) -> float:
    return 2.0 * math.atan2(float(q["y"]), float(q["w"]))


def _angle_deg(x: float, y: float) -> float:
    return math.degrees(math.atan2(y, x))


def _target_side_angle_from_local_normal(normal: Iterable[float]) -> float | None:
    row = list(normal)
    if len(row) < 2:
        return None
    return _angle_deg(-float(row[0]), -float(row[1]))


def _target_side_angle_from_unity_normal(normal: Iterable[float]) -> float | None:
    row = list(normal)
    if len(row) < 3:
        return None
    return _angle_deg(-float(row[0]), -float(row[2]))


def _jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if isinstance(value, np.ndarray):
        return [_jsonable(item) for item in value.tolist()]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    return value


def _summarize_contacts(result: Dict[str, Any]) -> Dict[str, Any]:
    points = result.get("points") or []
    separations = [
        float(point["separation"])
        for point in points
        if isinstance(point, dict) and point.get("separation") is not None
    ]
    first = points[0] if points else {}
    normal = first.get("normal") if isinstance(first, dict) else None
    return {
        "contact_count": result.get("contact_count"),
        "separation_min_m": min(separations) if separations else None,
        "separation_max_m": max(separations) if separations else None,
        "target_side_normal_angle_deg": _target_side_angle_from_local_normal(normal or []),
        "points_preview": points[:4],
    }


def _make_actor_pair(
    *,
    stone_points: np.ndarray,
    active_xy: Tuple[float, float],
    target_xy: Tuple[float, float],
    active_yaw: float,
    target_yaw: float,
    radius: float,
    center_height: float,
    contact_offset: float,
    rest_offset: float,
    combine_mode: Any,
) -> Tuple[Any, Any, Any, Any]:
    kwargs = dict(
        stone_points=stone_points,
        radius=radius,
        height=HEIGHT,
        stone_faces=256,
        inertia_model="solid-cylinder",
        inertia_radial=None,
        inertia_vertical=None,
        center_height=center_height,
        stone_friction=0.6,
        static_friction=0.6,
        dynamic_friction=0.6,
        stone_restitution=1.0,
        combine_mode=combine_mode,
        contact_offset=contact_offset,
        rest_offset=rest_offset,
        shape_local_x=0.0,
        shape_local_y=0.0,
        shape_local_z=0.0,
        shape_local_yaw=0.0,
        convex_quantized_count=255,
        convex_vertex_limit=255,
        quantize_input=False,
        gpu_compatible=False,
        solver_position_iterations=6,
        solver_velocity_iterations=1,
        max_depenetration_velocity=10.0,
        lock_upright=False,
        disable_stone_gravity=False,
        disable_strong_friction=False,
        improved_patch_friction=False,
    )
    active, active_shape, _ = _make_stone(
        active_xy[0], active_xy[1], 0.0, 0.0, 0.0, active_yaw, **kwargs
    )
    target, target_shape, _ = _make_stone(
        target_xy[0], target_xy[1], 0.0, 0.0, 0.0, target_yaw, **kwargs
    )
    return active, active_shape, target, target_shape


def build_report(args: argparse.Namespace) -> Dict[str, Any]:
    unity = json.loads(args.unity.read_text(encoding="utf-8"))
    first = unity["firstStoneStone"]
    desc = first["contactDesc"]
    contacts = first["contactBuffer"]["candidate"]["contactsPreview"]

    body0 = desc["bodyFrame0"]
    body1 = desc["bodyFrame1"]
    p0 = [float(value) for value in body0["p"]]
    p1 = [float(value) for value in body1["p"]]
    unity_dx = p0[0] - p1[0]
    unity_dz = p0[2] - p1[2]
    active_xy = (unity_dx, unity_dz)
    target_xy = (0.0, 0.0)
    center_height = args.center_height

    unity_active_yaw = _yaw_from_unity_y_up_quat(body0["q"])
    unity_target_yaw = _yaw_from_unity_y_up_quat(body1["q"])
    yaw_cases = [
        ("zero_yaw", 0.0, 0.0),
        ("unity_yaw_same_sign", unity_active_yaw, unity_target_yaw),
        ("unity_yaw_flipped_sign", -unity_active_yaw, -unity_target_yaw),
    ]

    combine_mode = _combine_mode_from_name("multiply")
    geometries: List[Tuple[str, np.ndarray, float]] = [
        ("ring_r0p146", _stone_points(radius=args.radius, height=HEIGHT, faces=256), args.radius),
        ("formal_recovered", _formal_stone_points(
            args.formal_stone_mesh,
            scale_x=args.formal_stone_scale_x,
            scale_y=args.formal_stone_scale_y,
            scale_z=args.formal_stone_scale_z,
        ), args.radius),
    ]

    cases = []
    for geometry_name, points, radius in geometries:
        for yaw_name, active_yaw, target_yaw in yaw_cases:
            active, active_shape, target, target_shape = _make_actor_pair(
                stone_points=points,
                active_xy=active_xy,
                target_xy=target_xy,
                active_yaw=active_yaw,
                target_yaw=target_yaw,
                radius=radius,
                center_height=center_height,
                contact_offset=args.contact_offset,
                rest_offset=args.rest_offset,
                combine_mode=combine_mode,
            )
            result = pyphysx.generate_contacts_between(
                active,
                active_shape,
                target,
                target_shape,
                -1.0,
                -1.0,
                -1.0,
            )
            cases.append(
                {
                    "geometry": geometry_name,
                    "yaw_case": yaw_name,
                    "active_pose": {
                        "xy": list(active_xy),
                        "z": center_height,
                        "yaw_rad": active_yaw,
                        "yaw_deg": math.degrees(active_yaw),
                    },
                    "target_pose": {
                        "xy": list(target_xy),
                        "z": center_height,
                        "yaw_rad": target_yaw,
                        "yaw_deg": math.degrees(target_yaw),
                    },
                    "raw_result": _jsonable(result),
                    "summary": _summarize_contacts(_jsonable(result)),
                }
            )

    unity_normal = contacts[0]["normal"] if contacts else None
    return {
        "question": "Does local PxGenerateContacts match Unity finalizer ContactBuffer when fed Unity bodyFrame relative pose?",
        "unity_source": str(args.unity.relative_to(PROJECT_ROOT)),
        "unity_first_stone_stone": {
            "body0_is_assumed_active": True,
            "body0_p": p0,
            "body1_p": p1,
            "relative_body0_minus_body1_unity_xz": [unity_dx, unity_dz],
            "relative_distance_xz_m": math.hypot(unity_dx, unity_dz),
            "body0_yaw_y_up_rad": unity_active_yaw,
            "body0_yaw_y_up_deg": math.degrees(unity_active_yaw),
            "body1_yaw_y_up_rad": unity_target_yaw,
            "contact_count": len(contacts),
            "separations_m": [contact["separation"] for contact in contacts],
            "target_side_normal_angle_deg_xz": _target_side_angle_from_unity_normal(unity_normal or []),
            "contacts_preview": contacts[:4],
        },
        "local_mapping": {
            "local_x": "unity_x - unity_body1_x",
            "local_y": "unity_z - unity_body1_z",
            "local_z": "unity_y - unity_body1_y + center_height",
            "center_height": center_height,
            "note": "Only relative pose matters for immediate contact generation; absolute Unity world offset is removed.",
        },
        "cases": cases,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unity", type=Path, default=DEFAULT_UNITY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--radius", type=float, default=0.146)
    parser.add_argument("--center-height", type=float, default=0.115)
    parser.add_argument("--contact-offset", type=float, default=0.005)
    parser.add_argument("--rest-offset", type=float, default=0.0)
    parser.add_argument("--formal-stone-mesh", type=Path, default=DEFAULT_FORMAL_STONE_MESH)
    parser.add_argument("--formal-stone-scale-x", type=float, default=0.1127)
    parser.add_argument("--formal-stone-scale-y", type=float, default=0.115)
    parser.add_argument("--formal-stone-scale-z", type=float, default=0.1127)
    args = parser.parse_args()

    report = build_report(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {args.output.relative_to(PROJECT_ROOT)}")
    print(json.dumps({
        "unity": report["unity_first_stone_stone"],
        "cases": [
            {
                "geometry": case["geometry"],
                "yaw_case": case["yaw_case"],
                "summary": case["summary"],
            }
            for case in report["cases"]
        ],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
