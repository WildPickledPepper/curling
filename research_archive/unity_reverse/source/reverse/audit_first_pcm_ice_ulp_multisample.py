#!/usr/bin/env python3
"""Validate the first-PCM ice-height ULP boundary across captured shots."""

from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any, Sequence


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from unity_front_half_physx import PersistentPhysxFrontHalfScene  # noqa: E402


DEFAULT_GROUPS = PROJECT_ROOT / "data/calibration/front_half_event_groups_20260710.json"
DEFAULT_TRUTH = PROJECT_ROOT / "data/calibration/front_half_pcm_entrance_truth_20260710.json"
DEFAULT_SUMMARY = (
    PROJECT_ROOT
    / "log/unity_runtime_probe_20260710_012403/front_half_pcm_summary.json"
)
DEFAULT_CACHE = PROJECT_ROOT / "data/calibration/front_half_pcm_cache_truth_20260710.json"
DEFAULT_OUTPUT = (
    PROJECT_ROOT
    / "data/calibration/first_pcm_ice_ulp_multisample_audit_20260710.json"
)
FLOAT32_WORLD_HEIGHT_ULP = 9.5367431640625e-7


def _yaw_delta(actual: float, expected: float) -> float:
    delta = float(actual) - float(expected)
    while delta > math.pi:
        delta -= 2.0 * math.pi
    while delta <= -math.pi:
        delta += 2.0 * math.pi
    return delta


def _vector_delta(left: Sequence[float], right: Sequence[float]) -> float:
    return math.sqrt(
        sum((float(a) - float(b)) ** 2 for a, b in zip(left, right))
    )


def _signless_vector_delta(left: Sequence[float], right: Sequence[float]) -> float:
    return min(
        _vector_delta(left, right),
        _vector_delta(left, [-float(value) for value in right]),
    )


def _unity_contacts(shot: dict[str, Any]) -> list[dict[str, Any]]:
    after = shot.get("firstPcmWithContactsAfter") or {}
    contact_buffer = after.get("contactBuffer") or {}
    contacts = contact_buffer.get("contactsPreview") or []
    return [row for row in contacts if isinstance(row, dict)]


def _contact_points(reports: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    points: list[dict[str, Any]] = []
    for report in reports:
        raw = report.get("points") or []
        points.extend(point for point in raw if isinstance(point, dict))
    return points


def _contact_metrics(
    local: Sequence[dict[str, Any]], unity: Sequence[dict[str, Any]]
) -> dict[str, Any]:
    pair_count = min(len(local), len(unity))
    best: tuple[float, list[dict[str, float]]] | None = None
    for order in itertools.permutations(range(len(unity)), pair_count):
        pairs = []
        score = 0.0
        for local_index, unity_index in enumerate(order):
            local_row = local[local_index]
            unity_row = unity[unity_index]
            row = {
                "normalSignlessL2": _signless_vector_delta(
                    local_row.get("normal") or [0.0, 0.0, 0.0],
                    unity_row.get("normal") or [0.0, 0.0, 0.0],
                ),
                "separationAbsM": abs(
                    float(local_row.get("separation") or 0.0)
                    - float(unity_row.get("separation") or 0.0)
                ),
            }
            score += row["normalSignlessL2"] + row["separationAbsM"]
            pairs.append(row)
        if best is None or score < best[0]:
            best = (score, pairs)
    return {
        "localCount": len(local),
        "unityCount": len(unity),
        "countMatch": len(local) == len(unity),
        "bestPairs": [] if best is None else best[1],
    }


def _set_exact_native_pose(
    scene: PersistentPhysxFrontHalfScene,
    index: int,
    native: dict[str, Any],
) -> None:
    qx, qy, qz, qw = [float(value) for value in native["nativeQ"]]
    scene.slots[index].body.set_global_pose(
        (
            [float(value) for value in native["nativeP"]],
            [qw, qx, qy, qz],
        )
    )


def _run_direct_exact_pose(
    truth_row: dict[str, Any],
    unity_contacts: Sequence[dict[str, Any]],
    seed_manifold_raw: list[int] | None,
) -> dict[str, Any]:
    scene = PersistentPhysxFrontHalfScene(stone_count=2)
    for index, role in ((0, "active"), (1, "target")):
        scene.slots[index].shape.set_flag(
            scene.pyphysx.ShapeFlag.SIMULATION_SHAPE, True
        )
        _set_exact_native_pose(
            scene, index, truth_row["unity_entrance_state"][role]
        )
    result = scene.pyphysx.generate_contacts_between_direct_pcm_cache_step(
        scene.slots[0].body,
        scene.slots[0].shape,
        scene.slots[1].body,
        scene.slots[1].shape,
        seed_manifold_raw,
        0.019999999552965164,
        0.009999999776482582,
        1.0,
    )
    points = [dict(point) for point in result.get("points") or []]
    return {
        "seeded": seed_manifold_raw is not None,
        "seedBytes": len(seed_manifold_raw or []),
        "contact": _contact_metrics(points, unity_contacts),
        "contacts": points,
        "contactDistance": float(result["contact_distance"]),
        "meshContactMargin": float(result["mesh_contact_margin"]),
        "toleranceLength": float(result["tolerance_length"]),
    }


def _derive_yaw_at_start(
    group: dict[str, Any], unity_active: dict[str, Any], tick_count: int
) -> dict[str, float]:
    noises = [float(item["noise"]) for item in group["friction"]]
    scene = PersistentPhysxFrontHalfScene(stone_count=2)
    scene.reset_positions([0.0, 0.0, 0.0, 0.0], settle_steps=0)
    scene.start_bestshot(
        0,
        [float(group["v0"]), float(group["h0"]), float(group["w0"])],
        yaw=0.0,
    )
    final_step: dict[str, Any] | None = None
    for noise in noises[:tick_count]:
        final_step = scene.step_custom_sliding(0, noise)
    if final_step is None:
        raise ValueError("a first-PCM sample must contain at least one friction tick")
    zero_yaw = float(final_step["beforeScene"]["yaw"])
    correction = -_yaw_delta(zero_yaw, float(unity_active["yaw"]))
    return {
        "zeroYawEntrance": zero_yaw,
        "unityEntrance": float(unity_active["yaw"]),
        "yawAtStart": correction,
    }


def _run_variant(
    group: dict[str, Any],
    truth_row: dict[str, Any],
    unity_contacts: Sequence[dict[str, Any]],
    *,
    yaw_at_start: float,
    ice_y_offset: float = 0.0,
    inject_active_y: bool = False,
    inject_active_pose: bool = False,
) -> dict[str, Any]:
    unity = truth_row["unity_entrance_state"]
    active = unity["active"]
    target = unity["target"]
    tick_count = int(truth_row["first_contact_pcm"]["raw_friction_range_calls"])
    noises = [float(item["noise"]) for item in group["friction"]]
    if len(noises) < tick_count:
        raise ValueError(
            f"sample {truth_row['sample_id']} needs {tick_count} friction ticks, "
            f"only {len(noises)} are available"
        )

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
    _set_exact_native_pose(scene, 1, target)
    scene.slots[1].body.set_linear_velocity([0.0, 0.0, 0.0])
    scene.slots[1].body.set_angular_velocity([0.0, 0.0, 0.0])
    scene.slots[1].body.put_to_sleep()
    target_after_setup = scene.state(1)

    scene.start_bestshot(
        0,
        [float(group["v0"]), float(group["h0"]), float(group["w0"])],
        yaw=yaw_at_start,
    )
    early_contact_tick = None
    for tick, noise in enumerate(noises[: tick_count - 1], 1):
        step = scene.step_custom_sliding(0, noise)
        if _contact_points(step["stoneReports"]):
            early_contact_tick = tick
            break

    if early_contact_tick is not None:
        return {
            "valid": False,
            "reason": "local stone contact occurred before Unity first-PCM tick",
            "earlyContactTick": early_contact_tick,
            "unityContactTick": tick_count,
            "iceYOffsetM": ice_y_offset,
        }

    position, quaternion = scene._pose(0)
    if inject_active_y:
        position[1] = float(active["nativeP"][1])
    if inject_active_pose:
        position = [float(value) for value in active["nativeP"]]
        qx, qy, qz, qw = [float(value) for value in active["nativeQ"]]
        quaternion = [qw, qx, qy, qz]
    if inject_active_y or inject_active_pose:
        scene.slots[0].body.set_global_pose((position, quaternion))

    final_step = scene.step_custom_sliding(0, noises[tick_count - 1])
    before = final_step["beforeScene"]
    after = final_step["afterScene"]
    local_contacts = _contact_points(final_step["stoneReports"])
    native_p = [float(value) for value in active["nativeP"]]
    local_p = [float(value) for value in before["physxPosition"]]
    return {
        "valid": True,
        "unityContactTick": tick_count,
        "iceYOffsetM": ice_y_offset,
        "injectedActiveNativeY": inject_active_y,
        "injectedActiveNativePose": inject_active_pose,
        "targetAfterSetup": target_after_setup,
        "beforeScene": before,
        "afterScene": after,
        "nativePositionDeltaM": [local_p[i] - native_p[i] for i in range(3)],
        "yawDeltaRad": _yaw_delta(before["yaw"], float(active["yaw"])),
        "contact": _contact_metrics(local_contacts, unity_contacts),
        "contacts": [
            {
                "normal": point.get("normal"),
                "separation": point.get("separation"),
                "position": point.get("position"),
            }
            for point in local_contacts
        ],
    }


def audit(
    groups: dict[str, Any],
    truth: dict[str, Any],
    summary: dict[str, Any],
    cache_truth: dict[str, Any],
) -> dict[str, Any]:
    group_rows = groups.get("rows") or []
    truth_rows = truth.get("rows") or []
    summary_rows = summary.get("shots") or []
    cache_boundaries = cache_truth.get("sampleBoundaries") or []
    cache_calls = cache_truth.get("calls") or {}
    rows = []
    for seq, truth_row in enumerate(truth_rows):
        if seq >= len(group_rows) or seq >= len(summary_rows):
            break
        group = group_rows[seq]
        unity_active = truth_row["unity_entrance_state"]["active"]
        tick_count = int(truth_row["first_contact_pcm"]["raw_friction_range_calls"])
        yaw = _derive_yaw_at_start(group, unity_active, tick_count)
        contacts = _unity_contacts(summary_rows[seq])
        boundary = cache_boundaries[seq]
        first_contact_call = str(boundary["firstContactCallIndex"])
        seed = cache_calls[first_contact_call]["before"]["cache"][
            "manifoldWindowRaw"
        ]
        variants = {
            "baseline": _run_variant(
                group, truth_row, contacts, yaw_at_start=yaw["yawAtStart"]
            ),
            "ice_down_one_float32_ulp": _run_variant(
                group,
                truth_row,
                contacts,
                yaw_at_start=yaw["yawAtStart"],
                ice_y_offset=-FLOAT32_WORLD_HEIGHT_ULP,
            ),
            "ice_down_two_float32_ulps": _run_variant(
                group,
                truth_row,
                contacts,
                yaw_at_start=yaw["yawAtStart"],
                ice_y_offset=-2.0 * FLOAT32_WORLD_HEIGHT_ULP,
            ),
            "inject_unity_active_native_y": _run_variant(
                group,
                truth_row,
                contacts,
                yaw_at_start=yaw["yawAtStart"],
                inject_active_y=True,
            ),
            "inject_unity_active_pose": _run_variant(
                group,
                truth_row,
                contacts,
                yaw_at_start=yaw["yawAtStart"],
                inject_active_pose=True,
            ),
        }
        rows.append(
            {
                "seq": seq,
                "sampleId": truth_row.get("sample_id"),
                "label": truth_row.get("label"),
                "unityContactCount": len(contacts),
                "pcmCallBoundary": {
                    "firstAnyCallIndex": boundary["firstAnyCallIndex"],
                    "firstContactCallIndex": boundary["firstContactCallIndex"],
                    "preContactPcmCallCount": (
                        int(boundary["firstContactCallIndex"])
                        - int(boundary["firstAnyCallIndex"])
                    ),
                },
                "yawCalibration": yaw,
                "variants": variants,
                "directExactPose": {
                    "freshCache": _run_direct_exact_pose(
                        truth_row, contacts, None
                    ),
                    "unityBeforeCache": _run_direct_exact_pose(
                        truth_row, contacts, [int(value) for value in seed]
                    ),
                },
            }
        )

    aggregate: dict[str, Any] = {}
    for variant in rows[0]["variants"] if rows else []:
        valid = [row["variants"][variant] for row in rows if row["variants"][variant]["valid"]]
        aggregate[variant] = {
            "validCount": len(valid),
            "countMatchCount": sum(
                1 for item in valid if item["contact"]["countMatch"]
            ),
            "contactCounts": [item["contact"]["localCount"] for item in valid],
            "normalSignlessL2Max": max(
                (
                    pair["normalSignlessL2"]
                    for item in valid
                    for pair in item["contact"]["bestPairs"]
                ),
                default=None,
            ),
            "separationAbsMMax": max(
                (
                    pair["separationAbsM"]
                    for item in valid
                    for pair in item["contact"]["bestPairs"]
                ),
                default=None,
            ),
        }
    return {
        "schema": "first_pcm_ice_ulp_multisample_audit_v1",
        "purpose": (
            "Test whether the one-float32-ULP ice-height boundary found in sample "
            "14000 generalizes across all six captured first-PCM shots."
        ),
        "control": {
            "activeHistory": "captured Random.Range friction stream through the Unity PCM tick",
            "activeYaw": "local angular integration plus one constant hidden initial-yaw offset per shot",
            "targetPose": "exact captured Unity native pose, kept sleeping until impact",
            "sceneLifecycle": "persistent actors and Scene for every shot variant",
            "productionCaveat": (
                "Unity entrance yaw and target pose are truth boundary conditions in this "
                "isolation audit; this is not yet a production no-oracle replay."
            ),
        },
        "float32WorldHeightUlpM": FLOAT32_WORLD_HEIGHT_ULP,
        "aggregate": aggregate,
        "directExactPoseContactCounts": {
            "unity": [row["unityContactCount"] for row in rows],
            "freshCache": [
                row["directExactPose"]["freshCache"]["contact"]["localCount"]
                for row in rows
            ],
            "unityBeforeCache": [
                row["directExactPose"]["unityBeforeCache"]["contact"]["localCount"]
                for row in rows
            ],
        },
        "rows": rows,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--groups", type=Path, default=DEFAULT_GROUPS)
    parser.add_argument("--truth", type=Path, default=DEFAULT_TRUTH)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = audit(
        json.loads(args.groups.read_text(encoding="utf-8")),
        json.loads(args.truth.read_text(encoding="utf-8")),
        json.loads(args.summary.read_text(encoding="utf-8")),
        json.loads(args.cache.read_text(encoding="utf-8")),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "output": str(args.output),
                "aggregate": result["aggregate"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
