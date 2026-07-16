#!/usr/bin/env python3
"""Cumulative C03 truth-fill waterfall on the strict C36 friction fixture."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.reverse.audit_hybrid_p6_endpoint_sixshot import install_pyphysx_extension
from tools.reverse.front_half_pcm_replay import event_shot_groups, load_jsonl
from tools.reverse.recovered_curling_motion import B2Vec2, STEP, newfrictionstep, unity_friction


DEFAULT_EXTENSION = Path(r"D:\esp\tmp\curling_pyphysx_hybrid_build\lib\_pyphysx.cp38-win_amd64.pyd")


def c03_truth(events_path: Path) -> list[dict[str, Any]]:
    for line in events_path.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event.get("type") == "c03.first_dynamic_writeback":
            return event["data"]["manager"]["coresBeforeSolve"]
    raise ValueError(f"no c03.first_dynamic_writeback in {events_path}")


def sample_endpoints(sample_path: Path) -> tuple[list[float], list[float]]:
    row = json.loads(next(line for line in sample_path.read_text(encoding="utf-8").splitlines() if line))
    return (
        [float(value) for value in row["final_xy"]],
        [float(row["target_moves"][0]["after_x"]), float(row["target_moves"][0]["after_y"])],
    )


def native_body_state(body: Any) -> dict[str, list[float]]:
    position, quaternion = body.get_global_pose()
    return {
        "p": [float(value) for value in position],
        "q": [
            float(getattr(quaternion, "x")),
            float(getattr(quaternion, "y")),
            float(getattr(quaternion, "z")),
            float(getattr(quaternion, "w")),
        ],
        "v": [float(value) for value in body.get_linear_velocity()],
        "w": [float(value) for value in body.get_angular_velocity()],
    }


def component_error(local: dict[str, list[float]], truth: dict[str, list[float]]) -> dict[str, float]:
    return {
        field: max(abs(a - b) for a, b in zip(local[field], truth[field]))
        for field in ("p", "q", "v", "w")
    }


def endpoint_error(local: list[float], unity: list[float]) -> dict[str, Any]:
    dx, dy = local[0] - unity[0], local[1] - unity[1]
    return {
        "localXY": local,
        "unityXY": unity,
        "deltaM": [dx, dy],
        "distanceMm": math.hypot(dx, dy) * 1000.0,
    }


def prepare_scene(
    pyphysx: Any,
    bestshot: list[float],
    noises: list[float],
    release_native_y_offset: float = 0.0,
    custom_sliding_zero_vertical_setter: bool = False,
) -> tuple[Any, list[dict[str, list[float]]]]:
    from unity_front_half_physx import PersistentPhysxFrontHalfScene

    scene = PersistentPhysxFrontHalfScene(
        stone_count=16,
        ice_mesh_mode="unity-source-once",
        ice_use_fast_midphase=True,
        emulate_unity_native_angular_setter_rotation=True,
        emulate_unity_setactive_no_sim=True,
        restore_active_friction_at_pcm_shell=True,
        custom_sliding_zero_vertical_setter=custom_sliding_zero_vertical_setter,
    )
    scene.reset_positions([0.0] * 32, settle_steps=0)
    scene.activate_stationary(8, 2.375, 5.2)
    scene.start_bestshot(0, bestshot)
    # Diagnostic-only release-pose ablation.  This is intentionally applied
    # before the first DCP tick so the subsequent gravity/contact evolution is
    # still produced by the normal local scene rather than by a C03 truth fill.
    if release_native_y_offset:
        active = scene.slots[0]
        position, quaternion = active.body.get_global_pose()
        lifted = [float(value) for value in position]
        lifted[1] += release_native_y_offset
        active.body.set_global_pose((lifted, quaternion))
        active.body.wake_up()
    for noise in noises[:-1]:
        scene.step_custom_sliding(0, noise)

    # Reproduce the final DCP Update setter, but deliberately stop immediately
    # before the Scene step in which C03 sees the dynamic pair.
    active = scene.slots[0]
    current = scene.state(0)
    speed = newfrictionstep(
        unity_friction(False, noise=noises[-1]),
        B2Vec2(float(current["vx"]), float(current["vy"])),
        float(current["w"]),
        STEP,
    )
    active.body.set_linear_velocity(
        scene._horizontal_velocity(
            speed.v.x,
            speed.v.y,
            0.0 if custom_sliding_zero_vertical_setter else float(current["vz"]),
        )
    )
    active.body.set_angular_velocity(scene._unity_native_angular_setter_vector(active, speed.angle))
    scene.slots[8].body.wake_up()
    return scene, [native_body_state(scene.slots[index].body) for index in (0, 8)]


def apply_field(body: Any, truth: dict[str, list[float]], field: str) -> None:
    if field in {"p", "q"}:
        position, quaternion = body.get_global_pose()
        if field == "p":
            position = truth["p"]
        else:
            qx, qy, qz, qw = truth["q"]
            quaternion = [qw, qx, qy, qz]
        body.set_global_pose((position, quaternion))
    elif field == "v":
        body.set_linear_velocity(truth["v"])
    elif field == "w":
        body.set_angular_velocity(truth["w"])
    else:
        raise ValueError(field)
    body.wake_up()


def settle(scene: Any) -> tuple[int, list[list[float]]]:
    for step in range(1, 6001):
        scene.scene.simulate(scene.dt)
        scene.scene.get_contact_reports()
        states = [scene.state(index) for index in (0, 8)]
        if all(
            math.sqrt(state["vx"] ** 2 + state["vy"] ** 2 + state["vz"] ** 2) < 0.001
            and abs(state["w"]) < 0.001
            for state in states
        ):
            return step, [[state["x"], state["y"]] for state in states]
    raise RuntimeError("local pair did not settle in 6000 steps")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest-events", type=Path, required=True)
    parser.add_argument("--unity-events", type=Path, required=True)
    parser.add_argument("--unity-sample", type=Path, required=True)
    parser.add_argument("--pyphysx-extension", type=Path, default=DEFAULT_EXTENSION)
    parser.add_argument(
        "--drop-manifest-tail-draws",
        type=int,
        default=0,
        help="Diagnostic boundary selection: exclude this many recorded friction draws from the manifest tail before replay.",
    )
    parser.add_argument(
        "--release-native-y-offset",
        type=float,
        default=0.0,
        help="Diagnostic-only native Y offset applied at BESTSHOT release, before DCP ticks.",
    )
    parser.add_argument(
        "--custom-sliding-zero-vertical-setter",
        action="store_true",
        help="Diagnostic-only: make every local custom-sliding linear setter write native Y=0.",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    groups = event_shot_groups(load_jsonl(args.manifest_events))
    if len(groups) != 1:
        raise ValueError(f"expected one BESTSHOT group in manifest source, got {len(groups)}")
    group = groups[0]
    all_noises = [float(item["noise"]) for item in group["friction"]]
    if args.drop_manifest_tail_draws < 0 or args.drop_manifest_tail_draws >= len(all_noises):
        raise ValueError("drop-manifest-tail-draws must leave at least one draw")
    noises = all_noises[:len(all_noises) - args.drop_manifest_tail_draws]
    if len(noises) < 2:
        raise ValueError("manifest has too few friction values")
    cores = c03_truth(args.unity_events)
    truth = [
        {
            "p": [float(value) for value in core["decodedCandidate"]["p"]],
            "q": [float(value) for value in core["decodedCandidate"]["q"]],
            "v": [float(value) for value in core["decodedCandidate"]["linearVelocity"]],
            "w": [float(value) for value in core["decodedCandidate"]["angularVelocity"]],
        }
        for core in cores
    ]
    unity_active, unity_target = sample_endpoints(args.unity_sample)
    install_pyphysx_extension(args.pyphysx_extension)
    import pyphysx  # loaded by install_pyphysx_extension

    cumulative = [
        ("baseline_no_truth", []),
        ("active_p", [(0, "p")]),
        ("active_pq", [(0, "p"), (0, "q")]),
        ("active_pqv", [(0, "p"), (0, "q"), (0, "v")]),
        ("active_pqvw", [(0, "p"), (0, "q"), (0, "v"), (0, "w")]),
        ("active_pqvw_target_p", [(0, "p"), (0, "q"), (0, "v"), (0, "w"), (1, "p")]),
        ("active_pqvw_target_pq", [(0, "p"), (0, "q"), (0, "v"), (0, "w"), (1, "p"), (1, "q")]),
        ("active_pqvw_target_pqv", [(0, "p"), (0, "q"), (0, "v"), (0, "w"), (1, "p"), (1, "q"), (1, "v")]),
        ("full_c03_pqvw", [(0, "p"), (0, "q"), (0, "v"), (0, "w"), (1, "p"), (1, "q"), (1, "v"), (1, "w")]),
    ]
    rows = []
    for label, fields in cumulative:
        scene, local_entry = prepare_scene(
            pyphysx,
            [group["v0"], group["h0"], group["w0"]],
            noises,
            release_native_y_offset=args.release_native_y_offset,
            custom_sliding_zero_vertical_setter=args.custom_sliding_zero_vertical_setter,
        )
        for stone_index, field in fields:
            apply_field(scene.slots[(0, 8)[stone_index]].body, truth[stone_index], field)
        scene.scene.simulate(scene.dt)
        scene.scene.get_contact_reports()
        # Matches the production material transition immediately after the first dynamic pair.
        for slot_index in (0, 8):
            scene.slots[slot_index].material.set_static_friction(0.6)
            scene.slots[slot_index].material.set_dynamic_friction(0.6)
        settle_steps, endpoints = settle(scene)
        rows.append({
            "cumulativeTruthFill": label,
            "fields": [{"stone": ("active", "target")[stone], "field": field} for stone, field in fields],
            "c03EntryLocal": local_entry,
            "c03EntryErrorBeforeFill": [component_error(local_entry[index], truth[index]) for index in range(2)],
            "settleSteps": settle_steps,
            "activeEndpoint": endpoint_error(endpoints[0], unity_active),
            "targetEndpoint": endpoint_error(endpoints[1], unity_target),
        })

    report = {
        "schema": "c39_manifest_front_half_waterfall_v2",
        "scope": "Diagnostic-only cumulative C03 pre-solver truth injection. It ranks the production BESTSHOT-to-C03 handoff residual after DCP friction is fixed; it is not a production correction.",
        "releaseNativeYOffset": args.release_native_y_offset,
        "customSlidingZeroVerticalSetter": bool(args.custom_sliding_zero_vertical_setter),
        "c03Truth": truth,
        "manifest": {
            "source": str(args.manifest_events),
            "recordedDrawCount": len(all_noises),
            "droppedTailDraws": args.drop_manifest_tail_draws,
            "drawCount": len(noises),
        },
        "unity": {"events": str(args.unity_events), "sample": str(args.unity_sample), "activeEndpoint": unity_active, "targetEndpoint": unity_target},
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for row in rows:
        print(row["cumulativeTruthFill"], f"active={row['activeEndpoint']['distanceMm']:.6f}mm", f"target={row['targetEndpoint']['distanceMm']:.6f}mm")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
