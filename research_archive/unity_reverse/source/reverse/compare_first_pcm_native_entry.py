#!/usr/bin/env python3
"""Compare Unity and local pyphysx inputs at one first-contact PCM call."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from unity_front_half_physx import PersistentPhysxFrontHalfScene  # noqa: E402


DEFAULT_TRUTH = PROJECT_ROOT / "data/calibration/front_half_pcm_entrance_truth_20260710.json"
DEFAULT_CACHE = PROJECT_ROOT / "data/calibration/front_half_pcm_cache_truth_20260710.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data/calibration/first_pcm_native_entry_diff_14001_20260710.json"


def _sha16(values: list[int]) -> str:
    return hashlib.sha256(bytes(int(value) & 0xFF for value in values)).hexdigest()[:16]


def _f32_bits(value: float) -> str:
    return struct.pack("<f", float(value)).hex()


def _jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _field(path: str, unity: Any, local: Any) -> dict[str, Any]:
    row: dict[str, Any] = {"path": path, "unity": unity, "local": local}
    if unity is None or local is None:
        row["status"] = "unavailable"
        return row
    if isinstance(unity, (list, tuple)) and isinstance(local, (list, tuple)):
        if len(unity) != len(local):
            row["status"] = "different"
            row["lengthDelta"] = len(local) - len(unity)
            return row
        components = [_field(f"{path}[{index}]", a, b) for index, (a, b) in enumerate(zip(unity, local))]
        row["components"] = components
        row["status"] = "equal" if all(item["status"] == "equal" for item in components) else "different"
        return row
    if isinstance(unity, bool) or isinstance(local, bool):
        row["status"] = "equal" if bool(unity) == bool(local) else "different"
        return row
    if isinstance(unity, (int, float)) and isinstance(local, (int, float)):
        row["delta"] = float(local) - float(unity)
        if isinstance(unity, float) or isinstance(local, float):
            row["unityF32Bytes"] = _f32_bits(float(unity))
            row["localF32Bytes"] = _f32_bits(float(local))
            row["status"] = (
                "equal" if row["unityF32Bytes"] == row["localF32Bytes"] else "different"
            )
        else:
            row["status"] = "equal" if int(unity) == int(local) else "different"
        return row
    row["status"] = "equal" if unity == local else "different"
    return row


def _set_exact_pose(scene: PersistentPhysxFrontHalfScene, index: int, state: dict[str, Any]) -> None:
    qx, qy, qz, qw = [float(value) for value in state["nativeQ"]]
    scene.slots[index].shape.set_flag(scene.pyphysx.ShapeFlag.SIMULATION_SHAPE, True)
    scene.slots[index].body.set_global_pose(
        ([float(value) for value in state["nativeP"]], [qw, qx, qy, qz])
    )


def compare(truth: dict[str, Any], cache_truth: dict[str, Any], sample_id: int) -> dict[str, Any]:
    truth_row = next(row for row in truth["rows"] if int(row["sample_id"]) == sample_id)
    boundary = next(
        row for row in cache_truth["sampleBoundaries"] if int(row["seq"]) == int(truth_row["seq"])
    )
    call_index = int(boundary["firstContactCallIndex"])
    unity_call = cache_truth["calls"][str(call_index)]["before"]
    scene = PersistentPhysxFrontHalfScene(stone_count=2)
    _set_exact_pose(scene, 0, truth_row["unity_entrance_state"]["active"])
    _set_exact_pose(scene, 1, truth_row["unity_entrance_state"]["target"])
    hulls = [scene.slots[index].shape.get_convex_mesh_runtime_hull_data() for index in range(2)]
    params = unity_call["narrowPhaseParams"]
    seed = [int(value) for value in unity_call["cache"]["manifoldWindowRaw"]]
    fresh = scene.pyphysx.generate_contacts_between_direct_pcm_cache_step(
        scene.slots[0].body,
        scene.slots[0].shape,
        scene.slots[1].body,
        scene.slots[1].shape,
        None,
        float(params["contactDistance"]),
        float(params["meshContactMargin"]),
        float(params["toleranceLength"]),
    )
    seeded = scene.pyphysx.generate_contacts_between_direct_pcm_cache_step(
        scene.slots[0].body,
        scene.slots[0].shape,
        scene.slots[1].body,
        scene.slots[1].shape,
        seed,
        float(params["contactDistance"]),
        float(params["meshContactMargin"]),
        float(params["toleranceLength"]),
    )

    fields: list[dict[str, Any]] = []
    for index in range(2):
        unity_shape = unity_call[f"shape{index}"]
        local = hulls[index]
        prefix = f"shape{index}"
        fields.extend(
            [
                _field(f"{prefix}.geometry.scale", unity_shape["geometry"]["scale"], local["scale"]),
                _field(
                    f"{prefix}.geometry.scaleRotation",
                    unity_shape["geometry"]["scaleRotation"],
                    local["scale_rotation_xyzw"],
                ),
                _field(
                    f"{prefix}.geometry.meshFlags",
                    unity_shape["geometry"]["meshFlags"],
                    local["mesh_flags"],
                ),
                _field(
                    f"{prefix}.hull.aabbCenter",
                    unity_shape["hullData"]["aabbCenter"],
                    local["aabb_center"],
                ),
                _field(
                    f"{prefix}.hull.aabbExtents",
                    unity_shape["hullData"]["aabbExtents"],
                    local["aabb_extents"],
                ),
                _field(
                    f"{prefix}.hull.centerOfMass",
                    unity_shape["hullData"]["centerOfMass"],
                    local["center_of_mass"],
                ),
                _field(
                    f"{prefix}.hull.nbEdges",
                    unity_shape["hullData"]["nbEdges"],
                    local["nb_edges"],
                ),
                _field(
                    f"{prefix}.hull.nbHullVertices",
                    unity_shape["hullData"]["nbHullVertices"],
                    local["nb_hull_vertices"],
                ),
                _field(
                    f"{prefix}.hull.nbPolygons",
                    unity_shape["hullData"]["nbPolygons"],
                    local["nb_polygons"],
                ),
                _field(
                    f"{prefix}.hull.internal",
                    unity_shape["hullData"]["internal"],
                    local["internal"],
                ),
                _field(
                    f"{prefix}.runtimeHull.sha16",
                    unity_shape["runtime"]["runtimeBuffer"]["sha16"],
                    _sha16(local["raw_bytes"]),
                ),
                _field(
                    f"{prefix}.bigConvex.samples.sha16",
                    unity_shape["runtime"]["bigConvexArrays"]["samples"]["sha16"],
                    _sha16(local["big_convex_raw_data"]["samples_raw_bytes"]),
                ),
                _field(
                    f"{prefix}.bigConvex.valencies.sha16",
                    unity_shape["runtime"]["bigConvexArrays"]["valencies"]["sha16"],
                    _sha16(local["big_convex_raw_data"]["valencies_raw_bytes"]),
                ),
                _field(
                    f"{prefix}.bigConvex.adjacentVertices.sha16",
                    unity_shape["runtime"]["bigConvexArrays"]["adjacentVertices"]["sha16"],
                    _sha16(local["big_convex_raw_data"]["adjacent_vertices_raw_bytes"]),
                ),
            ]
        )

    for index in range(2):
        fields.append(
            _field(
                f"transform{index}.p",
                unity_call[f"transform{index}"]["p"],
                seeded[f"input_transform{index}"]["p"],
            )
        )
        fields.append(
            _field(
                f"transform{index}.q",
                unity_call[f"transform{index}"]["q"],
                seeded[f"input_transform{index}"]["q"],
            )
        )
    for key, local_key in (
        ("contactDistance", "contact_distance"),
        ("meshContactMargin", "mesh_contact_margin"),
        ("toleranceLength", "tolerance_length"),
    ):
        fields.append(_field(f"narrowPhase.{key}", params[key], seeded[local_key]))

    unity_candidate = unity_call["cache"]["decoded"]["persistentManifoldCandidate"]
    local_seed = seeded["seed_manifold_before"]
    for unity_key, local_key in (
        ("numContacts", "num_contacts"),
        ("capacity", "capacity"),
        ("numWarmStartPoints", "num_warm_start_points"),
        ("aIndices", "a_indices"),
        ("bIndices", "b_indices"),
    ):
        fields.append(
            _field(
                f"cache.manifold.{unity_key}",
                unity_candidate[unity_key],
                local_seed[local_key],
            )
        )

    different = [row["path"] for row in fields if row["status"] == "different"]
    unavailable = [
        {
            "path": "shape*.geometryUnion.rawBytes",
            "reason": "Unity capture and local binding expose decoded fields, not the complete native object bytes.",
        },
        {
            "path": "shape*.hull.headerRawBytes",
            "reason": "The decoded header is available, but neither side currently exports one pointer-normalized raw header block.",
        },
        {
            "path": "cache.manifold.relativeTransform/quatA/quatB",
            "reason": "Local seed parser exposes these fields; the current Unity compact decoder does not list them separately.",
        },
        {
            "path": "PCM support/witness feature IDs before fullContactsGeneration",
            "reason": "Not exported by the current direct PCM binding.",
        },
    ]
    return {
        "schema": "first_pcm_native_entry_diff_v1",
        "sampleId": sample_id,
        "unityCallIndex": call_index,
        "boundary": "PxcPCMContactConvexConvex before",
        "contactCounts": {
            "unity": int(truth_row["first_contact_pcm"]["contact_count"]),
            "localFresh": int(fresh["contact_count"]),
            "localUnityBeforeSeed": int(seeded["contact_count"]),
        },
        "summary": {
            "fieldCount": len(fields),
            "differentCount": len(different),
            "differentPaths": different,
            "unavailableCount": len(unavailable),
        },
        "fields": _jsonable(fields),
        "unavailable": unavailable,
        "localFreshContacts": _jsonable(fresh["points"]),
        "localSeededContacts": _jsonable(seeded["points"]),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--truth", type=Path, default=DEFAULT_TRUTH)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--sample-id", type=int, default=14001)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = compare(
        json.loads(args.truth.read_text(encoding="utf-8")),
        json.loads(args.cache.read_text(encoding="utf-8")),
        args.sample_id,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "contactCounts": result["contactCounts"],
                "summary": result["summary"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
