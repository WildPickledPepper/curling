#!/usr/bin/env python3
"""Verify scalar PhysX against Unity's captured first-contact PCM manifolds."""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path
from typing import Any, Sequence


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from unity_front_half_physx import PersistentPhysxFrontHalfScene  # noqa: E402


DEFAULT_TRUTH = PROJECT_ROOT / "data/calibration/front_half_pcm_entrance_truth_20260710.json"
DEFAULT_CACHE = PROJECT_ROOT / "data/calibration/front_half_pcm_cache_truth_20260710.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data/calibration/scalar_pcm_backend_audit_20260710.json"


def _set_exact_pose(scene: PersistentPhysxFrontHalfScene, index: int, state: dict[str, Any]) -> None:
    qx, qy, qz, qw = [float(value) for value in state["nativeQ"]]
    scene.slots[index].shape.set_flag(scene.pyphysx.ShapeFlag.SIMULATION_SHAPE, True)
    scene.slots[index].body.set_global_pose(
        ([float(value) for value in state["nativeP"]], [qw, qx, qy, qz])
    )


def _flat_contact(contact: dict[str, Any]) -> list[float]:
    return [
        *[float(value) for value in contact["local_point_a"]],
        *[float(value) for value in contact["local_point_b"]],
        *[float(value) for value in contact["local_normal_pen"]],
    ]


def _best_contact_delta(
    local: Sequence[dict[str, Any]], unity: Sequence[dict[str, Any]]
) -> tuple[float | None, list[int]]:
    if len(local) != len(unity):
        return None, []
    if not local:
        return 0.0, []
    best: tuple[float, list[int]] | None = None
    for order in itertools.permutations(range(len(unity))):
        delta = max(
            abs(local_value - unity_value)
            for local_index, unity_index in enumerate(order)
            for local_value, unity_value in zip(
                _flat_contact(local[local_index]), _flat_contact(unity[unity_index])
            )
        )
        candidate = (delta, list(order))
        if best is None or candidate[0] < best[0]:
            best = candidate
    assert best is not None
    return best


def audit(truth: dict[str, Any], cache: dict[str, Any]) -> dict[str, Any]:
    boundaries = {
        int(row["seq"]): int(row["firstContactCallIndex"])
        for row in cache["sampleBoundaries"]
    }
    rows: list[dict[str, Any]] = []
    for truth_row in truth["rows"]:
        scene = PersistentPhysxFrontHalfScene(stone_count=2)
        scalar_enabled = bool(scene.pyphysx.is_scalar_math_enabled())
        for index, role in ((0, "active"), (1, "target")):
            _set_exact_pose(scene, index, truth_row["unity_entrance_state"][role])

        call_index = boundaries[int(truth_row["seq"])]
        unity_before = cache["calls"][str(call_index)]["before"]
        unity_after = cache["calls"][str(call_index)]["after"]
        params = unity_before["narrowPhaseParams"]
        args = (
            scene.slots[0].body,
            scene.slots[0].shape,
            scene.slots[1].body,
            scene.slots[1].shape,
        )
        generated = scene.pyphysx.diagnose_direct_pcm_full_manifold_stages(
            *args,
            [int(value) for value in unity_before["cache"]["manifoldWindowRaw"]],
            float(params["contactDistance"]),
            float(params["toleranceLength"]),
        )
        unity_manifold = scene.pyphysx.diagnose_direct_pcm_full_manifold_stages(
            *args,
            [int(value) for value in unity_after["cache"]["manifoldWindowRaw"]],
            float(params["contactDistance"]),
            float(params["toleranceLength"]),
        )["seed_manifold"]
        local_contacts = generated["manifold_after_batch"]["contacts"]
        unity_contacts = unity_manifold["contacts"]
        max_delta, order = _best_contact_delta(local_contacts, unity_contacts)
        rows.append(
            {
                "sampleId": int(truth_row["sample_id"]),
                "callIndex": call_index,
                "unityContactCount": len(unity_contacts),
                "scalarGeneratedContactCount": int(
                    generated["generated_contact_count_before_batch"]
                ),
                "scalarManifoldContactCount": len(local_contacts),
                "gjkStatus": int(generated["gjk_status"]),
                "gjkWarmStartCount": int(generated["gjk_warm_start_count"]),
                "contactPermutationToUnity": order,
                "maxContactComponentDelta": max_delta,
            }
        )

    count_match = all(
        row["unityContactCount"] == row["scalarManifoldContactCount"] for row in rows
    )
    max_delta = max(float(row["maxContactComponentDelta"] or 0.0) for row in rows)
    return {
        "schema": "scalar_pcm_backend_audit_v1",
        "purpose": "Prove that scalar PhysX reproduces Unity WebGL first-contact PCM manifold generation.",
        "backend": {
            "scalarMathEnabled": scalar_enabled,
            "coordinateMode": "unity-native-yup",
            "boundary": "exact Unity first-contact transform + Unity before-manifold raw",
        },
        "summary": {
            "sampleCount": len(rows),
            "countMatch": count_match,
            "maxContactComponentDelta": max_delta,
            "pass": scalar_enabled and count_match and max_delta <= 1.0e-6,
        },
        "rows": rows,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--truth", type=Path, default=DEFAULT_TRUTH)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = audit(
        json.loads(args.truth.read_text(encoding="utf-8")),
        json.loads(args.cache.read_text(encoding="utf-8")),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "summary": result["summary"]}, ensure_ascii=False, indent=2))
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
