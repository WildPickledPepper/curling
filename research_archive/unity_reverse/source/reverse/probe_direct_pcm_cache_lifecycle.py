#!/usr/bin/env python3
"""Probe whether direct PCM needs Unity's persistent manifold cache to match.

The full pyphysx Scene replay still enters the first stone-stone collision with
fresh 4-contact data.  This probe keeps the pose/hull fixed at the Unity PCM
capture and varies only the manifold cache: empty, Unity before, Unity after,
and a pyphysx roundtrip of its own after-cache raw bytes.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.reverse.probe_unity_runtime_hull_patch_contacts import (
    DEFAULT_EVENTS,
    DEFAULT_STONE_MESH,
    DEFAULT_UNITY,
    _convert_unity_manifold_raw_to_pyphysx_xzy,
    _jsonable,
    _load_pcm_seed_manifold_raw,
    _load_stone_points,
    _load_synthetic_bigconvex,
    _load_unity_runtime_feature_bundle,
    _make_shape,
    _select_pcm_pose_row,
    _summarize_contacts,
)

try:
    import pyphysx
except ImportError as exc:  # pragma: no cover - depends on external env.
    raise SystemExit("pyphysx is required; run with the pyphysx conda Python") from exc


DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_direct_pcm_cache_lifecycle_20260709.json"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _step(actor0: Any, shape0: Any, actor1: Any, shape1: Any, seed: list[int] | None) -> dict[str, Any]:
    result = pyphysx.generate_contacts_between_direct_pcm_cache_step(
        actor0,
        shape0,
        actor1,
        shape1,
        seed,
        -1.0,
        -1.0,
        -1.0,
    )
    return _jsonable(result)


def _make_actor_native(shape: Any, position: list[float], quat_xyzw: list[float]) -> Any:
    body = pyphysx.RigidDynamic()
    body.attach_shape(shape)
    body.set_global_pose(
        (
            [float(position[0]), float(position[1]), float(position[2])],
            [float(quat_xyzw[3]), float(quat_xyzw[0]), float(quat_xyzw[1]), float(quat_xyzw[2])],
        )
    )
    return body


def _case(
    name: str,
    points: Any,
    unity_raw: list[int],
    big_arrays: dict[str, list[int]] | None,
    active_position: list[float],
    target_position: list[float],
    active_quat_xyzw: list[float],
    target_quat_xyzw: list[float],
    seed_before: list[int],
    seed_after: list[int],
    patch_hull: bool,
    patch_big_convex: bool,
) -> dict[str, Any]:
    shape0 = _make_shape(points)
    shape1 = _make_shape(points)
    patch_info = None
    if patch_hull:
        patch_info = [
            shape0.patch_convex_mesh_runtime_hull_data_for_unity(unity_raw, True),
            shape1.patch_convex_mesh_runtime_hull_data_for_unity(unity_raw, True),
        ]
    big_patch_info = None
    if patch_big_convex and big_arrays is not None:
        big_patch_info = [
            shape0.patch_convex_mesh_big_convex_raw_data_for_unity(
                big_arrays["samples_raw_bytes"],
                big_arrays["valencies_raw_bytes"],
                big_arrays["adjacent_vertices_raw_bytes"],
            ),
            shape1.patch_convex_mesh_big_convex_raw_data_for_unity(
                big_arrays["samples_raw_bytes"],
                big_arrays["valencies_raw_bytes"],
                big_arrays["adjacent_vertices_raw_bytes"],
            ),
        ]

    actor0 = _make_actor_native(shape0, active_position, active_quat_xyzw)
    actor1 = _make_actor_native(shape1, target_position, target_quat_xyzw)

    fresh = _step(actor0, shape0, actor1, shape1, None)
    seeded_before = _step(actor0, shape0, actor1, shape1, seed_before)
    seeded_after = _step(actor0, shape0, actor1, shape1, seed_after)
    roundtrip_seed = seeded_after.get("manifold_after_raw")
    roundtrip = _step(
        actor0,
        shape0,
        actor1,
        shape1,
        roundtrip_seed if isinstance(roundtrip_seed, list) else None,
    )

    return {
        "name": name,
        "patch_hull": patch_hull,
        "patch_big_convex": patch_big_convex,
        "patch_info": _jsonable(patch_info),
        "big_convex_patch_info": _jsonable(big_patch_info),
        "fresh_empty_cache": {
            "summary": _summarize_contacts(fresh),
            "raw": fresh,
        },
        "unity_before_cache": {
            "summary": _summarize_contacts(seeded_before),
            "raw": seeded_before,
        },
        "unity_after_cache": {
            "summary": _summarize_contacts(seeded_after),
            "raw": seeded_after,
        },
        "pyphysx_after_raw_roundtrip": {
            "summary": _summarize_contacts(roundtrip),
            "raw": roundtrip,
        },
    }


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    points = _load_stone_points(args.stone_mesh)
    unity_bundle = _load_unity_runtime_feature_bundle(args.events, args.event_line)
    unity_state = _read_json(args.unity)
    first = unity_state["firstStoneStone"]
    unity_contacts = first["contactBuffer"]["candidate"]["contactsPreview"]
    pcm_pose_row = _select_pcm_pose_row(unity_state, unity_contacts)
    call_index = int(pcm_pose_row["callIndex"])
    pcm_inputs = pcm_pose_row["pcmInputs"]
    t0 = pcm_inputs["transform0"]
    t1 = pcm_inputs["transform1"]
    p0 = [float(value) for value in t0["p"]]
    p1 = [float(value) for value in t1["p"]]
    q0 = [float(value) for value in t0["q"]]
    q1 = [float(value) for value in t1["q"]]

    seed_before = _load_pcm_seed_manifold_raw(args.events, "before", call_index)
    seed_after = _load_pcm_seed_manifold_raw(args.events, "after", call_index)
    if args.seed_cache_coordinate == "pyphysx-xzy":
        seed_before = _convert_unity_manifold_raw_to_pyphysx_xzy(seed_before)
        seed_after = _convert_unity_manifold_raw_to_pyphysx_xzy(seed_after)

    big_arrays = None
    runtime_big = {
        "samples_raw_bytes": unity_bundle.get("samples_raw_bytes"),
        "valencies_raw_bytes": unity_bundle.get("valencies_raw_bytes"),
        "adjacent_vertices_raw_bytes": unity_bundle.get("adjacent_vertices_raw_bytes"),
    }
    if bool(unity_bundle.get("big_convex_arrays_complete")):
        big_arrays = runtime_big
        big_source = "runtime_capture"
    elif args.synthetic_bigconvex:
        big_arrays = _load_synthetic_bigconvex(args.synthetic_bigconvex)
        big_source = f"synthetic_rebuild:{args.synthetic_bigconvex}"
    else:
        big_source = "missing"

    cases = [
        _case(
            "local_4776_grb",
            points,
            unity_bundle["hull_raw_bytes"],
            big_arrays,
            p0,
            p1,
            q0,
            q1,
            seed_before,
            seed_after,
            False,
            False,
        ),
        _case(
            "unity_hull_only",
            points,
            unity_bundle["hull_raw_bytes"],
            big_arrays,
            p0,
            p1,
            q0,
            q1,
            seed_before,
            seed_after,
            True,
            False,
        ),
    ]
    if big_arrays is not None:
        cases.append(
            _case(
                "unity_hull_plus_bigconvex",
                points,
                unity_bundle["hull_raw_bytes"],
                big_arrays,
                p0,
                p1,
                q0,
                q1,
                seed_before,
                seed_after,
                True,
                True,
            )
        )

    summary = {
        case["name"]: {
            key: case[key]["summary"]
            for key in (
                "fresh_empty_cache",
                "unity_before_cache",
                "unity_after_cache",
                "pyphysx_after_raw_roundtrip",
            )
        }
        for case in cases
    }

    return {
        "question": "Does direct scene-style PCM match Unity only when the persistent manifold cache is carried?",
        "inputs": {
            "events": str(args.events.relative_to(PROJECT_ROOT)),
            "unity_state": str(args.unity.relative_to(PROJECT_ROOT)),
            "stone_mesh": str(args.stone_mesh),
            "event_line": args.event_line,
            "pcm_call_index": call_index,
            "seed_cache_coordinate": args.seed_cache_coordinate,
            "big_convex_source": big_source,
            "runtime_big_convex_arrays_complete": bool(unity_bundle.get("big_convex_arrays_complete")),
            "runtime_big_convex_lengths": {
                "samples": len(runtime_big["samples_raw_bytes"])
                if isinstance(runtime_big["samples_raw_bytes"], list)
                else None,
                "samples_expected": unity_bundle.get("samples_expected_bytes"),
                "valencies": len(runtime_big["valencies_raw_bytes"])
                if isinstance(runtime_big["valencies_raw_bytes"], list)
                else None,
                "valencies_expected": unity_bundle.get("valencies_expected_bytes"),
                "adjacent_vertices": len(runtime_big["adjacent_vertices_raw_bytes"])
                if isinstance(runtime_big["adjacent_vertices_raw_bytes"], list)
                else None,
                "adjacent_vertices_expected": unity_bundle.get("adjacent_vertices_expected_bytes"),
            },
        },
        "unity_expected": {
            "contact_count": len(unity_contacts),
            "separations": [contact.get("separation") for contact in unity_contacts],
            "normal0": unity_contacts[0].get("normal") if unity_contacts else None,
        },
        "pose": {
            "frame": "Unity/PhysX native xyz with pyphysx wxyz input quaternions",
            "active_position": p0,
            "target_position": p1,
            "active_quat_xyzw": q0,
            "target_quat_xyzw": q1,
        },
        "summary": summary,
        "cases": cases,
        "conclusion": (
            "Unity-after cache roundtrip tests the already-built manifold path.  If unity_after_cache "
            "and pyphysx_after_raw_roundtrip match Unity but fresh_empty_cache / unity_before_cache do "
            "not, the remaining gap is the fresh PCM first-generation support/feature path.  Do not "
            "promote a 2-contact after-cache replay to full Scene equivalence until fresh generation "
            "also matches."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--unity", type=Path, default=DEFAULT_UNITY)
    parser.add_argument("--stone-mesh", type=Path, default=DEFAULT_STONE_MESH)
    parser.add_argument("--event-line", type=int, default=221)
    parser.add_argument("--synthetic-bigconvex", type=Path, default=None)
    parser.add_argument("--seed-cache-coordinate", choices=["pyphysx-xzy", "unity-native"], default="unity-native")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    report = build_report(args)
    print(json.dumps({"unity_expected": report["unity_expected"], "summary": report["summary"]}, indent=2, ensure_ascii=False))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
