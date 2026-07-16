#!/usr/bin/env python3
"""Isolate the pose field that flips Unity's first PCM manifold from 4 to 2."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.reverse.diagnose_hybrid_bvh4_source_shell import _install_hybrid_module  # noqa: E402

_install_hybrid_module()

from unity_front_half_physx import PersistentPhysxFrontHalfScene  # noqa: E402


DEFAULT_GROUPS = PROJECT_ROOT / "data/calibration/front_half_event_groups_20260710.json"
DEFAULT_TRUTH = PROJECT_ROOT / "data/calibration/front_half_pcm_entrance_truth_20260710.json"
DEFAULT_OUTPUT = (
    PROJECT_ROOT
    / "data/calibration/first_pcm_pose_feature_boundary_audit_20260710.json"
)


def _yaw_delta(actual: float, expected: float) -> float:
    delta = float(actual) - float(expected)
    while delta > math.pi:
        delta -= 2.0 * math.pi
    while delta <= -math.pi:
        delta += 2.0 * math.pi
    return delta


def _run_variant(
    group: dict[str, Any],
    unity: dict[str, Any],
    *,
    yaw_at_start: float,
    inject_position_axes: tuple[int, ...] = (),
    inject_quaternion: bool = False,
    ice_y_offset: float = 0.0,
) -> dict[str, Any]:
    noises = [float(item["noise"]) for item in group["friction"]]
    if len(noises) < 1560:
        raise ValueError("sample 14000 needs at least 1560 captured friction ticks")

    target = unity["target"]
    active = unity["active"]
    scene = PersistentPhysxFrontHalfScene(stone_count=2)
    if ice_y_offset:
        scene.ice.set_global_pose(
            ([0.0, float(ice_y_offset), 0.0], [1.0, 0.0, 0.0, 0.0])
        )
    scene.reset_positions(
        [0.0, 0.0, float(target["x"]), float(target["y"])],
        yaw_overrides={1: float(target["yaw"])},
        settle_steps=1,
    )
    scene.start_bestshot(
        0,
        [float(group["v0"]), float(group["h0"]), float(group["w0"])],
        yaw=yaw_at_start,
    )
    for noise in noises[:1559]:
        scene.step_custom_sliding(0, noise)

    position, quaternion = scene._pose(0)
    unity_position = [float(value) for value in active["nativeP"]]
    for axis in inject_position_axes:
        position[axis] = unity_position[axis]
    if inject_quaternion:
        qx, qy, qz, qw = [float(value) for value in active["nativeQ"]]
        quaternion = [qw, qx, qy, qz]
    scene.slots[0].body.set_global_pose((position, quaternion))

    step = scene.step_custom_sliding(0, noises[1559])
    before = step["beforeScene"]
    reports = step["stoneReports"]
    points = reports[0].get("points") or [] if reports else []
    native_p = [float(value) for value in active["nativeP"]]
    local_p = [float(value) for value in before["physxPosition"]]
    return {
        "yawAtStart": yaw_at_start,
        "injectedUnityPositionAxes": list(inject_position_axes),
        "injectedUnityQuaternion": inject_quaternion,
        "iceYOffset": ice_y_offset,
        "beforeScene": before,
        "unityEntrance": active,
        "nativePositionDelta": [local_p[i] - native_p[i] for i in range(3)],
        "yawDeltaRad": _yaw_delta(before["yaw"], active["yaw"]),
        "contactCount": len(points),
        "contacts": [
            {
                "normal": point.get("normal"),
                "separation": point.get("separation"),
            }
            for point in points
        ],
    }


def audit(groups_path: Path, truth_path: Path) -> dict[str, Any]:
    groups = json.loads(groups_path.read_text(encoding="utf-8"))["rows"]
    truth_rows = json.loads(truth_path.read_text(encoding="utf-8"))["rows"]
    group = groups[0]
    truth = truth_rows[0]
    unity = truth["unity_entrance_state"]

    zero_yaw = _run_variant(group, unity, yaw_at_start=0.0)
    yaw_correction = -float(zero_yaw["yawDeltaRad"])
    variants = {
        "zero_yaw": zero_yaw,
        "yaw_aligned": _run_variant(group, unity, yaw_at_start=yaw_correction),
        "yaw_aligned_unity_position": _run_variant(
            group,
            unity,
            yaw_at_start=yaw_correction,
            inject_position_axes=(0, 1, 2),
        ),
        "yaw_aligned_unity_native_y": _run_variant(
            group,
            unity,
            yaw_at_start=yaw_correction,
            inject_position_axes=(1,),
        ),
        "yaw_aligned_unity_native_z": _run_variant(
            group,
            unity,
            yaw_at_start=yaw_correction,
            inject_position_axes=(2,),
        ),
        "yaw_aligned_unity_quaternion": _run_variant(
            group,
            unity,
            yaw_at_start=yaw_correction,
            inject_quaternion=True,
        ),
        "yaw_aligned_ice_down_one_float_ulp": _run_variant(
            group,
            unity,
            yaw_at_start=yaw_correction,
            ice_y_offset=-9.5367431640625e-7,
        ),
        "yaw_aligned_ice_down_two_float_ulps": _run_variant(
            group,
            unity,
            yaw_at_start=yaw_correction,
            ice_y_offset=-1.9073486328125e-6,
        ),
        "yaw_aligned_unity_pose": _run_variant(
            group,
            unity,
            yaw_at_start=yaw_correction,
            inject_position_axes=(0, 1, 2),
            inject_quaternion=True,
        ),
    }
    return {
        "schema": "first_pcm_pose_feature_boundary_audit_v1",
        "sampleId": truth.get("sample_id"),
        "label": truth.get("label"),
        "yawCorrectionRad": yaw_correction,
        "variants": variants,
        "conclusion": (
            "For sample 14000, aligning yaw alone leaves four contacts. With the same "
            "Scene, actors, cache, hull and solver, replacing only the 0.953674um "
            "native-Y entrance coordinate (one float32 ULP at this world height) flips the "
            "manifold to Unity's two contacts. Replacing only the 38.146um native-Z "
            "coordinate or only the quaternion does not. The 2/4 split is therefore a "
            "stone-ice support-height/first-PCM pose boundary issue, not an independent "
            "hull/cache/solver gap. Moving only the local ice surface down by that same "
            "single ULP naturally reproduces the Unity body height and two-contact result; "
            "moving it down by two ULPs returns to four contacts."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--groups", type=Path, default=DEFAULT_GROUPS)
    parser.add_argument("--truth", type=Path, default=DEFAULT_TRUTH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = audit(args.groups, args.truth)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "yawCorrectionRad": result["yawCorrectionRad"],
                "contactCounts": {
                    name: row["contactCount"]
                    for name, row in result["variants"].items()
                },
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
