#!/usr/bin/env python3
"""Replay the captured six-shot session with persistent PhysX actors.

This is a P4 audit, not an endpoint-fitting tool.  Every reset changes only
the recorded protocol positions; actor quaternion and scene-owned contact
history remain on the same local actors.  A shot's first-contact boundary is
the first actual stone-stone contact report emitted by the Scene.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.reverse.front_half_pcm_replay import event_shot_groups, load_jsonl  # noqa: E402
from unity_front_half_physx import DEFAULT_RUNTIME_FEATURE_EVENTS, PersistentPhysxFrontHalfScene  # noqa: E402


DEFAULT_SAMPLES = PROJECT_ROOT / "data/calibration/front_half_pcm_samples_20260710_012534.jsonl"
DEFAULT_EVENTS = PROJECT_ROOT / "log/unity_runtime_probe_20260710_012403/events.jsonl"
DEFAULT_TRUTH = PROJECT_ROOT / "data/calibration/front_half_pcm_entrance_truth_20260710.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data/calibration/persistent_scene_sequence_audit_20260710.json"


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _norm(values: Iterable[float]) -> float:
    return math.sqrt(sum(float(value) * float(value) for value in values))


def _yaw_delta(left: float, right: float) -> float:
    value = float(left) - float(right)
    while value > math.pi:
        value -= 2.0 * math.pi
    while value <= -math.pi:
        value += 2.0 * math.pi
    return value


def _unity_wxyz(native_q: list[float]) -> list[float]:
    if len(native_q) != 4:
        raise ValueError("Unity native quaternion must be xyzw")
    return [float(native_q[3]), float(native_q[0]), float(native_q[1]), float(native_q[2])]


def _quaternion_delta(local_wxyz: list[float], unity_xyzw: list[float]) -> float:
    target = _unity_wxyz(unity_xyzw)
    return min(
        _norm(a - b for a, b in zip(local_wxyz, target)),
        _norm(a + b for a, b in zip(local_wxyz, target)),
    )


def _selected_states(scene: PersistentPhysxFrontHalfScene, indices: Iterable[int]) -> dict[str, dict[str, Any]]:
    return {str(index): scene.state(index) for index in sorted(set(int(item) for item in indices))}


def _compact_pcm_cache(cache: Any) -> dict[str, Any] | None:
    """Keep semantic cache fields; raw windows are allocator-dependent and enormous."""

    if not isinstance(cache, dict):
        return None
    manifold = cache.get("manifold")
    if not isinstance(manifold, dict):
        manifold = {}
    return {
        "cachedDataPointer": cache.get("cached_data_ptr"),
        "isManifold": cache.get("is_manifold"),
        "isMultiManifold": cache.get("is_multi_manifold"),
        "cachedSize": cache.get("cached_size"),
        "pairData": cache.get("pair_data"),
        "manifoldFlags": cache.get("manifold_flags"),
        "numContacts": manifold.get("num_contacts"),
        "numWarmStartPoints": manifold.get("num_warm_start_points"),
        "aIndices": manifold.get("a_indices"),
        "bIndices": manifold.get("b_indices"),
    }


def _settle_after_contact(
    scene: PersistentPhysxFrontHalfScene,
    *,
    max_steps: int,
    linear_threshold: float,
    angular_threshold: float,
    consecutive_steps: int,
) -> dict[str, Any]:
    """Advance the local Scene only; this is explicitly reported as a candidate history."""

    quiet = 0
    moving: list[int] = []
    for step in range(1, max_steps + 1):
        scene.scene.simulate(scene.dt)
        scene.scene.get_contact_reports()
        moving = []
        for slot in scene.slots:
            if not slot.enabled:
                continue
            state = scene.state(slot.index)
            if _norm((state["vx"], state["vy"], state["vz"])) > linear_threshold or _norm(
                (state["wx"], state["wy"], state["w"])
            ) > angular_threshold:
                moving.append(slot.index)
        quiet = quiet + 1 if not moving else 0
        if quiet >= consecutive_steps:
            return {"settled": True, "steps": step, "movingIndices": []}
    return {"settled": False, "steps": max_steps, "movingIndices": moving}


def build_audit(
    samples: list[dict[str, Any]],
    groups: list[dict[str, Any]],
    truth_rows: list[dict[str, Any]],
    *,
    tail_steps: int,
    settle_steps: int,
    set_active_scene_membership: bool = False,
    restore_active_friction_at_pcm_shell: bool = False,
    enable_stone_stone_contact_friction_override: bool = True,
    enable_unity_pcm_task_cache_lifecycle: bool = True,
    repeat_pose_after_shape_activation: bool = True,
    trace_pcm: bool = False,
) -> dict[str, Any]:
    if not (len(samples) == len(groups) == len(truth_rows)):
        raise ValueError("sample, event, and Unity truth counts must agree")

    scene = PersistentPhysxFrontHalfScene(
        stone_count=16,
        set_active_scene_membership=set_active_scene_membership,
        restore_active_friction_at_pcm_shell=restore_active_friction_at_pcm_shell,
        enable_stone_stone_contact_friction_override=enable_stone_stone_contact_friction_override,
        enable_unity_pcm_task_cache_lifecycle=enable_unity_pcm_task_cache_lifecycle,
        repeat_pose_after_shape_activation=repeat_pose_after_shape_activation,
    )
    if trace_pcm:
        scene.pyphysx.clear_scene_pcm_trace()
        scene.pyphysx.set_scene_pcm_trace_enabled(True)
    rows: list[dict[str, Any]] = []
    for seq, (sample, group, truth) in enumerate(zip(samples, groups, truth_rows)):
        active_index = int(sample["active_shot_num"])
        targets = [int(value) for value in sample.get("target_indices") or []]
        tracked = [active_index, *targets]
        before_reset = _selected_states(scene, tracked)
        scene.reset_positions(sample["reset_position"], settle_steps=settle_steps)
        after_reset = _selected_states(scene, tracked)
        reset_quaternion_changed = {
            str(index): _norm(
                a - b
                for a, b in zip(
                    before_reset[str(index)]["quaternionWxyz"],
                    after_reset[str(index)]["quaternionWxyz"],
                )
            )
            for index in tracked
        }
        noises = [float(item["noise"]) for item in group.get("friction") or []]
        replay = scene.run_bestshot_to_first_contact(
            active_index,
            [float(group["v0"]), float(group["h0"]), float(group["w0"])],
            noises,
            target_indices=targets,
            yaw=None,
            max_steps=len(noises),
        )
        row: dict[str, Any] = {
            "seq": seq,
            "sampleId": sample.get("sample_id"),
            "label": sample.get("label"),
            "activeIndex": active_index,
            "targetIndices": targets,
            "beforeReset": before_reset,
            "afterReset": after_reset,
            "resetQuaternionDelta": reset_quaternion_changed,
            "reachedFirstContact": bool(replay.get("reachedFirstContact")),
            "firstContactStep": replay.get("steps"),
        }
        if replay.get("reachedFirstContact"):
            local_active = replay["beforeScene"]
            local_target = replay["targetBeforeScene"][str(targets[0])]
            unity = truth["unity_entrance_state"]
            unity_active = unity["active"]
            unity_target = unity["target"]
            reports = replay.get("firstContactReports") or []
            row["firstContact"] = {
                "localActive": local_active,
                "localTarget": local_target,
                "localContactCount": int(reports[0].get("contact_count") or 0) if reports else None,
                "positionDeltaM": {
                    "active": _norm(
                        local_active["physxPosition"][i] - unity_active["nativeP"][i]
                        for i in range(3)
                    ),
                    "target": _norm(
                        local_target["physxPosition"][i] - unity_target["nativeP"][i]
                        for i in range(3)
                    ),
                },
                "quaternionDelta": {
                    "active": _quaternion_delta(local_active["quaternionWxyz"], unity_active["nativeQ"]),
                    "target": _quaternion_delta(local_target["quaternionWxyz"], unity_target["nativeQ"]),
                },
                "yawDeltaRad": {
                    "active": _yaw_delta(local_active["yaw"], unity_active["yaw"]),
                    "target": _yaw_delta(local_target["yaw"], unity_target["yaw"]),
                },
            }
            row["tail"] = _settle_after_contact(
                scene,
                max_steps=tail_steps,
                linear_threshold=0.01,
                angular_threshold=0.01,
                consecutive_steps=20,
            )
        if trace_pcm:
            pcm_rows = list(scene.pyphysx.get_scene_pcm_trace(True))
            row["pcmTrace"] = [
                {
                    "sequence": entry.get("sequence"),
                    "contactCountBefore": entry.get("contact_count_before"),
                    "contactCountAfter": entry.get("contact_count_after"),
                    "cacheBefore": _compact_pcm_cache(entry.get("cache_before")),
                    "cacheAfter": _compact_pcm_cache(entry.get("cache_after")),
                }
                for entry in pcm_rows
            ]
        rows.append(row)

    if trace_pcm:
        scene.pyphysx.set_scene_pcm_trace_enabled(False)

    reached = [row for row in rows if row["reachedFirstContact"]]
    return {
        "schema": "persistent_scene_sequence_audit_v1",
        "purpose": "P4 continuous local history audit; no Unity state is injected.",
        "configuration": {
            "actorCount": 16,
            "resetPolicy": "recorded 2D positions only; quaternion and local cache persist",
            "firstContactPolicy": "first Scene stone-stone contact report",
            "tailPolicy": "local scalar PhysX candidate history after first contact",
            "tailMaxSteps": tail_steps,
            "resetSettleSteps": settle_steps,
            "setActiveSceneMembership": set_active_scene_membership,
            "restoreActiveFrictionAtPcmShell": restore_active_friction_at_pcm_shell,
            "stoneStoneContactFrictionOverride": enable_stone_stone_contact_friction_override,
            "unityPcmTaskCacheLifecycle": enable_unity_pcm_task_cache_lifecycle,
            "repeatPoseAfterShapeActivation": repeat_pose_after_shape_activation,
            "pcmTrace": trace_pcm,
            "runtimeFeatures": scene.runtime_feature_meta,
        },
        "aggregate": {
            "rowCount": len(rows),
            "reachedFirstContactCount": len(reached),
            "maxResetQuaternionDelta": max(
                (value for row in rows for value in row["resetQuaternionDelta"].values()), default=None
            ),
        },
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--truth", type=Path, default=DEFAULT_TRUTH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--tail-steps", type=int, default=2500)
    parser.add_argument("--reset-settle-steps", type=int, default=1)
    parser.add_argument("--set-active-scene-membership", action="store_true")
    parser.add_argument("--restore-active-friction-at-pcm-shell", action="store_true")
    parser.add_argument("--disable-stone-stone-contact-friction-override", action="store_true")
    parser.add_argument("--disable-unity-pcm-task-cache-lifecycle", action="store_true")
    parser.add_argument("--omit-post-activation-pose-sync", action="store_true")
    parser.add_argument("--trace-pcm", action="store_true")
    args = parser.parse_args()
    # The P4/P5 lifecycle audit requires the isolated hybrid extension, which
    # supplies Scene.remove_actor and the PCM trace bindings.
    if args.set_active_scene_membership or args.trace_pcm:
        from tools.reverse.diagnose_hybrid_bvh4_source_shell import _install_hybrid_module

        _install_hybrid_module()
    truth = json.loads(args.truth.read_text(encoding="utf-8"))
    report = build_audit(
        _load_jsonl(args.samples),
        event_shot_groups(load_jsonl(args.events)),
        truth.get("rows") or [],
        tail_steps=max(0, int(args.tail_steps)),
        settle_steps=max(0, int(args.reset_settle_steps)),
        set_active_scene_membership=bool(args.set_active_scene_membership),
        restore_active_friction_at_pcm_shell=bool(args.restore_active_friction_at_pcm_shell),
        enable_stone_stone_contact_friction_override=not bool(
            args.disable_stone_stone_contact_friction_override
        ),
        enable_unity_pcm_task_cache_lifecycle=not bool(
            args.disable_unity_pcm_task_cache_lifecycle
        ),
        repeat_pose_after_shape_activation=not bool(args.omit_post_activation_pose_sync),
        trace_pcm=bool(args.trace_pcm),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "aggregate": report["aggregate"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
