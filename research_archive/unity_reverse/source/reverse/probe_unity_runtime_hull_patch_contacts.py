#!/usr/bin/env python3
"""A/B test local contact generation with Unity's runtime convex hull buffer.

This is not an endpoint sweep. It replays the captured Unity first stone-stone
bodyFrame pose through local PhysX immediate contact generation, using the raw
512-point ExtendedCollider mesh plus Unity's non-uniform PxMeshScale. The only
experimental switch is whether the local Gu::ConvexHullData runtime buffer is
left as local PhysX cooked it or overwritten with Unity's captured 4008-byte
runtime buffer.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import struct
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

from tools.reverse.probe_physx_collision_alignment import _combine_mode_from_name


DEFAULT_EVENTS = PROJECT_ROOT / "log" / "unity_runtime_probe_20260709_171257" / "events.jsonl"
DEFAULT_UNITY = PROJECT_ROOT / "data" / "calibration" / "unity_physx_native_solver_state_pcm_hull_runtime_20260709_171257.json"
DEFAULT_STONE_MESH = Path(r"D:\esp\tmp\curling_reverse_il2cpp\stone_extendedcollider_mesh_256.json")
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_runtime_hull_patch_contact_ab_20260709.json"
UNITY_SCALE = [0.11270000785589218, 0.11500000208616257, 0.11270000785589218]


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


def _yaw_from_unity_y_up_quat(q: Dict[str, float]) -> float:
    return 2.0 * math.atan2(float(q["y"]), float(q["w"]))


def _yaw_from_unity_y_up_quat_list(q: List[float]) -> float:
    return 2.0 * math.atan2(float(q[1]), float(q[3]))


def _target_side_angle_from_local_normal(normal: Iterable[float]) -> float | None:
    row = list(normal)
    if len(row) < 3:
        return None
    return math.degrees(math.atan2(-float(row[2]), -float(row[0])))


def _target_side_angle_from_unity_normal(normal: Iterable[float]) -> float | None:
    row = list(normal)
    if len(row) < 3:
        return None
    return math.degrees(math.atan2(-float(row[2]), -float(row[0])))


def _raw_bytes_at_path(row: Dict[str, Any], path: List[str]) -> List[int] | None:
    cur: Any = row
    for key in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    if isinstance(cur, dict) and isinstance(cur.get("rawBytes"), list):
        return [int(value) for value in cur["rawBytes"]]
    return None


def _first_hull_runtime_from_event(event: Dict[str, Any]) -> Dict[str, Any]:
    data = event.get("data") if isinstance(event.get("data"), dict) else {}
    extras = data.get("extraDumps") if isinstance(data.get("extraDumps"), list) else []
    for extra in extras:
        if not isinstance(extra, dict):
            continue
        for shape_key in ("shape0", "shape1"):
            shape = extra.get(shape_key) if isinstance(extra.get(shape_key), dict) else None
            runtime = shape.get("hullRuntime") if isinstance(shape, dict) else None
            if not isinstance(runtime, dict):
                continue
            window = runtime.get("runtimeBufferWindow")
            if isinstance(window, dict) and isinstance(window.get("rawBytes"), list):
                return runtime
    raise ValueError("event has no convex hull runtimeBufferWindow raw bytes")


def _raw_len(value: Any) -> int | None:
    return len(value) if isinstance(value, list) else None


def _raw_len_matches(raw: Any, expected: Any) -> bool:
    return isinstance(raw, list) and isinstance(expected, int) and len(raw) == expected


def _load_unity_runtime_feature_bundle(events_path: Path, line_number: int) -> Dict[str, Any]:
    with events_path.open("r", encoding="utf-8") as handle:
        for current, line in enumerate(handle, 1):
            if current != line_number:
                continue
            event = json.loads(line)
            runtime = _first_hull_runtime_from_event(event)
            arrays = runtime.get("bigConvexRawDataArrays") if isinstance(runtime, dict) else None
            big = runtime.get("bigConvexRawData") if isinstance(runtime.get("bigConvexRawData"), dict) else {}
            samples_raw = _raw_bytes_at_path(runtime, ["bigConvexRawDataArrays", "samplesWindow"])
            valencies_raw = _raw_bytes_at_path(runtime, ["bigConvexRawDataArrays", "valenciesWindow"])
            adjacent_raw = _raw_bytes_at_path(runtime, ["bigConvexRawDataArrays", "adjacentVertsWindow"])
            samples_expected = big.get("samplesBytes")
            valencies_expected = big.get("valenciesBytes")
            adjacent_expected = big.get("adjacentVertsBytes")
            return {
                "event_type": event.get("type"),
                "hull_raw_bytes": runtime["runtimeBufferWindow"]["rawBytes"],
                "byte_layout": runtime.get("byteLayout"),
                "runtime_layout": runtime.get("layout"),
                "vertex_ref_count": runtime.get("vertexRefCount"),
                "big_convex": big or None,
                "big_convex_arrays_available": isinstance(arrays, dict),
                "big_convex_arrays_complete": (
                    _raw_len_matches(samples_raw, samples_expected)
                    and _raw_len_matches(valencies_raw, valencies_expected)
                    and _raw_len_matches(adjacent_raw, adjacent_expected)
                ),
                "samples_raw_bytes": samples_raw,
                "samples_expected_bytes": samples_expected,
                "valencies_raw_bytes": valencies_raw,
                "valencies_expected_bytes": valencies_expected,
                "adjacent_vertices_raw_bytes": adjacent_raw,
                "adjacent_vertices_expected_bytes": adjacent_expected,
            }
    raise ValueError(f"line {line_number} not found in {events_path}")


def _load_synthetic_bigconvex(path: Path) -> Dict[str, List[int]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    big = payload["unity_rebuilt"]["big_convex"]
    return {
        "samples_raw_bytes": [int(value) & 0xFF for value in big["samples_raw_bytes"]],
        "valencies_raw_bytes": [int(value) & 0xFF for value in big["valencies_raw_bytes"]],
        "adjacent_vertices_raw_bytes": [
            int(value) & 0xFF for value in big["adjacent_vertices_raw_bytes"]
        ],
    }


def _load_pcm_seed_manifold_raw(events_path: Path, phase: str, call_index: int) -> List[int]:
    with events_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if "PxcPCMContactConvexConvex" not in line or "manifoldWindow" not in line:
                continue
            event = json.loads(line)
            data = event.get("data") if isinstance(event.get("data"), dict) else {}
            hook = data.get("hook") if isinstance(data.get("hook"), dict) else {}
            if hook.get("name") != "PxcPCMContactConvexConvex":
                continue
            if data.get("phase") != phase or int(data.get("callIndex") or -1) != int(call_index):
                continue
            extras = data.get("extraDumps") if isinstance(data.get("extraDumps"), list) else []
            for extra in extras:
                if not isinstance(extra, dict) or not str(extra.get("label") or "").endswith(".pcmInputs"):
                    continue
                cache = extra.get("cache") if isinstance(extra.get("cache"), dict) else {}
                manifold_window = (
                    cache.get("manifoldWindow") if isinstance(cache.get("manifoldWindow"), dict) else {}
                )
                raw = manifold_window.get("rawBytes")
                if isinstance(raw, list):
                    return [int(value) & 0xFF for value in raw]
    raise ValueError(f"no PxcPCMContactConvexConvex {phase} seed manifold found for callIndex={call_index}")


def _read_f32(raw: bytearray, offset: int) -> float:
    return struct.unpack_from("<f", raw, offset)[0]


def _write_f32(raw: bytearray, offset: int, value: float) -> None:
    struct.pack_into("<f", raw, offset, float(value))


def _swap_yz_vec3_inplace(raw: bytearray, offset: int) -> None:
    y = _read_f32(raw, offset + 4)
    z = _read_f32(raw, offset + 8)
    _write_f32(raw, offset + 4, z)
    _write_f32(raw, offset + 8, y)


def _swap_yz_quat_inplace(raw: bytearray, offset: int) -> None:
    y = _read_f32(raw, offset + 4)
    z = _read_f32(raw, offset + 8)
    _write_f32(raw, offset + 4, z)
    _write_f32(raw, offset + 8, y)


def _convert_unity_manifold_raw_to_pyphysx_xzy(raw_bytes: List[int]) -> List[int]:
    raw = bytearray(int(value) & 0xFF for value in raw_bytes)
    if len(raw) < 80:
        return list(raw)

    # WebGL PersistentContactManifold layout: q(0), p(16), quatA(32), quatB(48),
    # counters/indices(64), contact pointer(76), then 48-byte contacts at 80.
    _swap_yz_quat_inplace(raw, 0)
    _swap_yz_vec3_inplace(raw, 16)
    _swap_yz_quat_inplace(raw, 32)
    _swap_yz_quat_inplace(raw, 48)

    num_contacts = min(int(raw[64]), 4)
    for index in range(num_contacts):
        base = 80 + index * 48
        if base + 48 > len(raw):
            break
        _swap_yz_vec3_inplace(raw, base)
        _swap_yz_vec3_inplace(raw, base + 16)
        _swap_yz_vec3_inplace(raw, base + 32)
    return list(raw)


def _load_stone_points(path: Path) -> np.ndarray:
    data = json.loads(path.read_text(encoding="utf-8"))
    return np.asarray(data["vertices"], dtype=np.float32)


def _contact_count_from_pcm_row(row: Dict[str, Any]) -> int:
    candidate = (
        ((row.get("pcmInputs") or {}).get("contactBuffer") or {}).get("candidate")
        if isinstance(row.get("pcmInputs"), dict)
        else {}
    )
    if isinstance(candidate, dict):
        if candidate.get("count") is not None:
            return int(candidate["count"])
        contacts = candidate.get("contactsPreview")
        if isinstance(contacts, list):
            return len(contacts)
    return 0


def _first_separation_from_pcm_row(row: Dict[str, Any]) -> float | None:
    candidate = (
        ((row.get("pcmInputs") or {}).get("contactBuffer") or {}).get("candidate")
        if isinstance(row.get("pcmInputs"), dict)
        else {}
    )
    contacts = candidate.get("contactsPreview") if isinstance(candidate, dict) else None
    if isinstance(contacts, list) and contacts:
        first = contacts[0]
        if isinstance(first, dict) and first.get("separation") is not None:
            return float(first["separation"])
    return None


def _select_pcm_pose_row(unity_state: Dict[str, Any], unity_contacts: List[Dict[str, Any]]) -> Dict[str, Any]:
    target_count = len(unity_contacts)
    target_sep = float(unity_contacts[0]["separation"]) if unity_contacts else None
    candidates = [
        row
        for row in unity_state.get("pcmContactRows", [])
        if row.get("hook") == "PxcPCMContactConvexConvex"
        and row.get("phase") == "after"
        and _contact_count_from_pcm_row(row) == target_count
    ]
    if not candidates:
        raise ValueError("no matching PxcPCMContactConvexConvex after row with Unity contact count")
    if target_sep is not None:
        candidates.sort(
            key=lambda row: abs((_first_separation_from_pcm_row(row) or float("inf")) - target_sep)
        )
    return candidates[0]


def _make_shape(points: np.ndarray) -> Any:
    combine = _combine_mode_from_name("multiply")
    material = pyphysx.Material(0.6, 0.6, 1.0)
    material.set_friction_combine_mode(combine)
    material.set_restitution_combine_mode(combine)
    shape = pyphysx.Shape.create_convex_mesh_from_points_with_scale(
        points,
        material,
        True,
        UNITY_SCALE,
        255,
        255,
        False,
        False,
    )
    shape.set_contact_offset(0.005)
    shape.set_rest_offset(0.0)
    return shape


def _make_actor(shape: Any, xy: Tuple[float, float], yaw_rad: float) -> Any:
    body = pyphysx.RigidDynamic()
    body.attach_shape(shape)
    half_yaw = 0.5 * yaw_rad
    body.set_global_pose(
        ([xy[0], xy[1], 0.115], [math.cos(half_yaw), 0.0, 0.0, math.sin(half_yaw)])
    )
    return body


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
        "contact_count": int(result.get("contact_count", 0)),
        "separation_min_m": min(separations) if separations else None,
        "separation_max_m": max(separations) if separations else None,
        "target_side_normal_angle_deg": _target_side_angle_from_local_normal(normal or []),
        "cache_size": result.get("cache_size"),
        "cache_manifold_flags": result.get("cache_manifold_flags"),
        "points_preview": points[:4],
    }


def build_report(args: argparse.Namespace) -> Dict[str, Any]:
    points = _load_stone_points(args.stone_mesh)
    unity_bundle = _load_unity_runtime_feature_bundle(args.events, args.event_line)
    unity_raw = unity_bundle["hull_raw_bytes"]
    unity_state = json.loads(args.unity.read_text(encoding="utf-8"))
    first = unity_state["firstStoneStone"]
    desc = first["contactDesc"]
    unity_contacts = first["contactBuffer"]["candidate"]["contactsPreview"]

    pose_source = getattr(args, "pose_source", "finalizer")
    pcm_pose_row: Dict[str, Any] | None = None
    seed_pcm_row: Dict[str, Any] | None = None
    if pose_source == "pcm-after":
        pcm_pose_row = _select_pcm_pose_row(unity_state, unity_contacts)
        seed_pcm_row = pcm_pose_row
        pcm_inputs = pcm_pose_row["pcmInputs"]
        t0 = pcm_inputs["transform0"]
        t1 = pcm_inputs["transform1"]
        p0 = [float(value) for value in t0["p"]]
        p1 = [float(value) for value in t1["p"]]
        active_yaw = _yaw_from_unity_y_up_quat_list([float(value) for value in t0["q"]])
        target_yaw = _yaw_from_unity_y_up_quat_list([float(value) for value in t1["q"]])
    else:
        body0 = desc["bodyFrame0"]
        body1 = desc["bodyFrame1"]
        p0 = [float(value) for value in body0["p"]]
        p1 = [float(value) for value in body1["p"]]
        active_yaw = _yaw_from_unity_y_up_quat(body0["q"])
        target_yaw = _yaw_from_unity_y_up_quat(body1["q"])

    seed_cache_source = getattr(args, "seed_cache_source", "none")
    seed_manifold_raw: List[int] | None = None
    seed_call_index: int | None = None
    if seed_cache_source != "none":
        if seed_pcm_row is None:
            seed_pcm_row = _select_pcm_pose_row(unity_state, unity_contacts)
        seed_call_index = int(seed_pcm_row["callIndex"])
        seed_phase = "before" if seed_cache_source == "pcm-before" else "after"
        seed_manifold_raw = _load_pcm_seed_manifold_raw(args.events, seed_phase, seed_call_index)
        if getattr(args, "seed_cache_coordinate", "pyphysx-xzy") == "pyphysx-xzy":
            seed_manifold_raw = _convert_unity_manifold_raw_to_pyphysx_xzy(seed_manifold_raw)

    active_xy = (p0[0] - p1[0], p0[2] - p1[2])
    target_xy = (0.0, 0.0)

    big_samples = unity_bundle.get("samples_raw_bytes")
    big_valencies = unity_bundle.get("valencies_raw_bytes")
    big_adjacent = unity_bundle.get("adjacent_vertices_raw_bytes")
    big_convex_source = "runtime_capture"
    big_arrays_available = bool(unity_bundle.get("big_convex_arrays_complete"))
    if not big_arrays_available and getattr(args, "synthetic_bigconvex", None):
        synthetic = _load_synthetic_bigconvex(args.synthetic_bigconvex)
        big_samples = synthetic["samples_raw_bytes"]
        big_valencies = synthetic["valencies_raw_bytes"]
        big_adjacent = synthetic["adjacent_vertices_raw_bytes"]
        big_convex_source = f"synthetic_rebuild:{args.synthetic_bigconvex}"
        big_arrays_available = True

    case_specs = [
        ("local_4776_grb", False, False),
        ("unity_4008_no_grb_hull_only", True, False),
    ]
    if big_arrays_available:
        case_specs.append(("unity_4008_no_grb_plus_bigconvex", True, True))

    cases = []
    for name, patch_hull, patch_big_convex in case_specs:
        shape0 = _make_shape(points)
        shape1 = _make_shape(points)
        before = shape0.get_convex_mesh_runtime_hull_data()
        patch_info = None
        if patch_hull:
            patch_info = [
                shape0.patch_convex_mesh_runtime_hull_data_for_unity(unity_raw, True),
                shape1.patch_convex_mesh_runtime_hull_data_for_unity(unity_raw, True),
            ]
        big_convex_patch_info = None
        if patch_big_convex:
            big_convex_patch_info = [
                shape0.patch_convex_mesh_big_convex_raw_data_for_unity(big_samples, big_valencies, big_adjacent),
                shape1.patch_convex_mesh_big_convex_raw_data_for_unity(big_samples, big_valencies, big_adjacent),
            ]
        after = shape0.get_convex_mesh_runtime_hull_data()

        actor0 = _make_actor(shape0, active_xy, active_yaw)
        actor1 = _make_actor(shape1, target_xy, target_yaw)
        if seed_manifold_raw is not None:
            result = pyphysx.generate_contacts_between_with_seeded_cache(
                actor0,
                shape0,
                actor1,
                shape1,
                seed_manifold_raw,
                -1.0,
                -1.0,
                -1.0,
            )
        else:
            result = pyphysx.generate_contacts_between(actor0, shape0, actor1, shape1, -1.0, -1.0, -1.0)
        cases.append(
            {
                "name": name,
                "patch_hull": patch_hull,
                "patch_big_convex": patch_big_convex,
                "seed_cache_source": seed_cache_source,
                "seed_cache_coordinate": getattr(args, "seed_cache_coordinate", "pyphysx-xzy"),
                "seed_cache_call_index": seed_call_index,
                "seed_cache_raw_bytes": len(seed_manifold_raw) if isinstance(seed_manifold_raw, list) else None,
                "patch_info": _jsonable(patch_info),
                "big_convex_patch_info": _jsonable(big_convex_patch_info),
                "hull_before": {
                    "buffer_size": before.get("buffer_size"),
                    "has_grb_edges": before.get("has_grb_edges"),
                    "byte_layout": before.get("byte_layout"),
                    "scale": before.get("scale"),
                },
                "hull_after": {
                    "buffer_size": after.get("buffer_size"),
                    "has_grb_edges": after.get("has_grb_edges"),
                    "byte_layout": after.get("byte_layout"),
                    "scale": after.get("scale"),
                },
                "raw_result": _jsonable(result),
                "summary": _summarize_contacts(_jsonable(result)),
            }
        )

    unity_normal = unity_contacts[0]["normal"] if unity_contacts else None
    unity_contact_count = len(unity_contacts)
    local_count = next(
        (case["summary"]["contact_count"] for case in cases if case["name"] == "local_4776_grb"),
        None,
    )
    hull_only_count = next(
        (case["summary"]["contact_count"] for case in cases if case["name"] == "unity_4008_no_grb_hull_only"),
        None,
    )
    plus_big_count = next(
        (case["summary"]["contact_count"] for case in cases if case["name"] == "unity_4008_no_grb_plus_bigconvex"),
        None,
    )
    if plus_big_count is None:
        answer = (
            "No. This capture predates BigConvex pointed-array dumps. It proves the mismatch is in the "
            "convex PCM cooked runtime feature bundle, but the hull buffer alone is not sufficient: "
            f"local 4776/GRB gives {local_count} contacts, while Unity 4008/no-GRB hull-only patch gives "
            f"{hull_only_count} contacts instead of Unity's {unity_contact_count}. The next missing piece is "
            "BigConvexRawData/support-map arrays and then PCM cache feature state if still needed."
        )
    elif plus_big_count == unity_contact_count:
        answer = (
            "BigConvex arrays are available and the hull+BigConvex patch matches Unity contact_count. "
            "Next check separation/normal and then run endpoint replay toward the 2cm gate."
        )
    else:
        answer = (
            "BigConvex arrays are available, but hull+BigConvex still does not match Unity contact_count: "
            f"patched={plus_big_count}, Unity={unity_contact_count}. The next missing piece is likely PCM "
            "persistent manifold/cache feature state."
        )
    return {
        "question": "Does replacing only local Gu::ConvexHullData runtime bytes with Unity's 4008-byte buffer make local contact generation match Unity?",
        "answer": answer,
        "sources": {
            "events": str(args.events.relative_to(PROJECT_ROOT)),
            "unity_state": str(args.unity.relative_to(PROJECT_ROOT)),
            "stone_mesh": str(args.stone_mesh),
            "event_line": args.event_line,
            "pose_source": pose_source,
            "pcm_pose_call_index": pcm_pose_row.get("callIndex") if pcm_pose_row else None,
            "pcm_pose_dump_index": pcm_pose_row.get("dumpIndex") if pcm_pose_row else None,
            "seed_cache_source": seed_cache_source,
            "seed_cache_coordinate": getattr(args, "seed_cache_coordinate", "pyphysx-xzy"),
            "seed_cache_call_index": seed_call_index,
        },
        "unity_runtime_hull": {
            "raw_byte_count": len(unity_raw),
            "scale": UNITY_SCALE,
        },
        "unity_runtime_big_convex": {
            "arrays_available": big_arrays_available,
            "arrays_complete": bool(unity_bundle.get("big_convex_arrays_complete"))
            if big_convex_source == "runtime_capture"
            else None,
            "source": big_convex_source if big_arrays_available else None,
            "decoded": unity_bundle.get("big_convex"),
            "samples_raw_bytes": len(big_samples) if isinstance(big_samples, list) else None,
            "samples_expected_bytes": unity_bundle.get("samples_expected_bytes"),
            "valencies_raw_bytes": len(big_valencies) if isinstance(big_valencies, list) else None,
            "valencies_expected_bytes": unity_bundle.get("valencies_expected_bytes"),
            "adjacent_vertices_raw_bytes": len(big_adjacent) if isinstance(big_adjacent, list) else None,
            "adjacent_vertices_expected_bytes": unity_bundle.get("adjacent_vertices_expected_bytes"),
            "note": (
                "This old capture predates BigConvex pointed-array dumps."
                if not big_arrays_available
                else "BigConvex arrays are available or synthetically rebuilt and were used for the plus_bigconvex case."
            ),
        },
        "unity_first_stone_stone": {
            "contact_count": unity_contact_count,
            "separations_m": [contact["separation"] for contact in unity_contacts],
            "target_side_normal_angle_deg": _target_side_angle_from_unity_normal(unity_normal or []),
            "contacts_preview": unity_contacts[:4],
            "relative_body0_minus_body1_unity_xz": [active_xy[0], active_xy[1]],
            "body0_yaw_deg": math.degrees(active_yaw),
            "body1_yaw_deg": math.degrees(target_yaw),
        },
        "cases": cases,
        "next_needed_runtime_fields": [
            "BigConvexRawData.mSamples array",
            "BigConvexRawData.mValencies array",
            "BigConvexRawData.mAdjacentVerts array",
            "PCM manifold/cache feature state if BigConvex parity is still not enough",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--event-line", type=int, default=221)
    parser.add_argument("--unity", type=Path, default=DEFAULT_UNITY)
    parser.add_argument("--stone-mesh", type=Path, default=DEFAULT_STONE_MESH)
    parser.add_argument(
        "--pose-source",
        choices=["finalizer", "pcm-after"],
        default="finalizer",
        help="Use finalizer bodyFrame pose or exact PxcPCMContactConvexConvex after transform pose.",
    )
    parser.add_argument(
        "--seed-cache-source",
        choices=["none", "pcm-before", "pcm-after"],
        default="none",
        help="Seed pyphysx immediate PxCache from Unity PCM manifold raw bytes for the selected call.",
    )
    parser.add_argument(
        "--seed-cache-coordinate",
        choices=["unity-raw", "pyphysx-xzy"],
        default="pyphysx-xzy",
        help="Coordinate frame for the seeded Unity manifold raw bytes before passing to pyphysx.",
    )
    parser.add_argument(
        "--synthetic-bigconvex",
        type=Path,
        default=None,
        help="Optional output from rebuild_bigconvex_from_runtime_hull.py.",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    report = build_report(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        output_label = args.output.resolve().relative_to(PROJECT_ROOT)
    except ValueError:
        output_label = args.output
    print(f"wrote {output_label}")
    for case in report["cases"]:
        summary = case["summary"]
        print(
            f"{case['name']}: count={summary['contact_count']} "
            f"sep=[{summary['separation_min_m']}, {summary['separation_max_m']}]"
        )
    unity = report["unity_first_stone_stone"]
    print(f"Unity: count={unity['contact_count']} separations={unity['separations_m']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
