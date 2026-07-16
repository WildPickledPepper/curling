#!/usr/bin/env python3
"""P6 no-oracle endpoint audit for the controlled Unity sample 14000."""

from __future__ import annotations

import json
import math
import sys
import argparse
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.reverse.diagnose_hybrid_bvh4_source_shell import _install_hybrid_module  # noqa: E402


CONTROLLED_TRUTH = PROJECT_ROOT / (
    "log/unity_runtime_probe_20260710_p4_second_pcm/"
    "unity_runtime_probe_20260710_233626/controlled_14000.jsonl"
)
CONTROLLED_EVENTS = CONTROLLED_TRUTH.with_name("events.jsonl")
OUTPUT = PROJECT_ROOT / "data/calibration/hybrid_p6_endpoint_14000_controlled_matched_20260711.json"


def _distance(left: dict[str, float], right: list[float]) -> float:
    return math.hypot(float(left["x"]) - float(right[0]), float(left["y"]) - float(right[1]))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--role-swap",
        action="store_true",
        help="Diagnostic only: allocate the target in slot 0 and active stone in slot 8.",
    )
    parser.add_argument(
        "--unity-solver-inertia-locks",
        action="store_true",
        help="Diagnostic only: make X/Z inverse inertia zero, as captured in Unity PxSolverBodyData.",
    )
    parser.add_argument(
        "--initial-yaw",
        type=float,
        default=0.0,
        help=(
            "Diagnostic only: add this yaw (radians) before the local BESTSHOT replay. "
            "It is never a production/oracle correction."
        ),
    )
    args = parser.parse_args()
    _install_hybrid_module()
    from tools.reverse import audit_persistent_scene_sequence as audit
    from tools.reverse.front_half_pcm_replay import event_shot_groups, load_jsonl
    from unity_front_half_physx import PersistentPhysxFrontHalfScene, UNITY_STONE_VERTICAL_INERTIA

    sample = audit._load_jsonl(audit.DEFAULT_SAMPLES)[0]
    groups = event_shot_groups(load_jsonl(CONTROLLED_EVENTS))
    if len(groups) != 1:
        raise ValueError(f"expected one controlled BESTSHOT group, found {len(groups)}")
    group = groups[0]
    unity = json.loads(CONTROLLED_TRUTH.read_text(encoding="utf-8").splitlines()[0])
    unity_target_index = int((sample.get("target_indices") or [8])[0])
    unity_active_index = int(sample["active_shot_num"])
    target_index = unity_target_index
    active_index = unity_active_index
    reset_position = [float(value) for value in sample["reset_position"]]
    if args.role_swap:
        original_active, original_target = active_index, target_index
        active_index, target_index = original_target, original_active
        reset_position[2 * target_index : 2 * target_index + 2] = reset_position[
            2 * original_target : 2 * original_target + 2
        ]
        reset_position[2 * active_index : 2 * active_index + 2] = [0.0, 0.0]
    unity_active = [
        float(unity["after_position"][2 * unity_active_index]),
        float(unity["after_position"][2 * unity_active_index + 1]),
    ]
    unity_target = [
        float(unity["after_position"][2 * unity_target_index]),
        float(unity["after_position"][2 * unity_target_index + 1]),
    ]

    scene = PersistentPhysxFrontHalfScene(
        stone_count=16,
        ice_mesh_mode="unity-source-once",
        ice_use_fast_midphase=True,
    )
    if args.unity_solver_inertia_locks:
        for slot in scene.slots:
            # Unity's raw solver-body matrix has zero X/Z inverse inertia. This
            # is a state-equivalence diagnostic, not an inertia fit.
            slot.body.set_mass_space_inertia_tensor([0.0, UNITY_STONE_VERTICAL_INERTIA, 0.0])
    scene.pyphysx.clear_scene_pcm_trace()
    scene.pyphysx.clear_scene_finalizer_trace()
    scene.pyphysx.clear_scene_solve_writeback_trace()
    scene.pyphysx.clear_scene_solve_block_trace()
    scene.pyphysx.set_scene_pcm_trace_enabled(True)
    scene.pyphysx.set_scene_finalizer_trace_enabled(True)
    scene.pyphysx.set_scene_solve_writeback_trace_enabled(True)
    scene.pyphysx.set_scene_solve_block_trace_enabled(True)
    scene.reset_positions(reset_position, settle_steps=1)
    replay = scene.run_bestshot_to_first_contact(
        active_index,
        [float(group["v0"]), float(group["h0"]), float(group["w0"])],
        [float(item["noise"]) for item in group["friction"]],
        target_indices=[target_index],
        yaw=float(args.initial_yaw),
        max_steps=len(group["friction"]),
    )
    result: dict[str, object] = {
        "schema": "hybrid_p6_endpoint_audit_v1",
        "policy": "no Unity pose, velocity, cache, or post-collision state is injected",
        "inputs": {
            "sampleReset": str(audit.DEFAULT_SAMPLES.relative_to(PROJECT_ROOT)),
            "controlledEvents": str(CONTROLLED_EVENTS.relative_to(PROJECT_ROOT)),
            "controlledEndpoint": str(CONTROLLED_TRUTH.relative_to(PROJECT_ROOT)),
            "motioninfo": group.get("motioninfo"),
        },
        "sampleId": int(sample["sample_id"]),
        "roleSwapDiagnostic": bool(args.role_swap),
        "unitySolverInertiaLocksDiagnostic": bool(args.unity_solver_inertia_locks),
        "initialYawDiagnosticRad": float(args.initial_yaw),
        "scalarMath": bool(scene.pyphysx.is_scalar_math_enabled()),
        "iceMidphase": scene.runtime_ice_mesh_meta.get("useFastMidphase"),
        "reachedFirstContact": bool(replay.get("reachedFirstContact")),
        "firstContactStep": replay.get("steps"),
        "firstContactCounts": [int(row.get("contact_count") or 0) for row in replay.get("firstContactReports") or []],
        "unityEndpoint": {"active": unity_active, "target": unity_target},
    }
    if replay.get("reachedFirstContact"):
        result["firstContactAfterScene"] = {
            "active": replay["afterScene"],
            "target": replay["targetsAfterScene"][str(target_index)],
        }
        scene.scene.simulate(scene.dt)
        first_post_solver_reports = scene.scene.get_contact_reports()
        result["firstPostSolverScene"] = {
            "active": scene.state(active_index),
            "target": scene.state(target_index),
            "contactReportCount": len(first_post_solver_reports),
        }
        result["localPcmCallsThroughFirstWriteback"] = list(scene.pyphysx.get_scene_pcm_trace(True))
        result["localFinalizerCallsThroughFirstWriteback"] = list(
            scene.pyphysx.get_scene_finalizer_trace(True)
        )
        result["localSolveWritebackCallsThroughFirstWriteback"] = list(
            scene.pyphysx.get_scene_solve_writeback_trace(True)
        )
        result["localSolveBlockCallsThroughFirstWriteback"] = list(
            scene.pyphysx.get_scene_solve_block_trace(True)
        )
        scene.pyphysx.set_scene_pcm_trace_enabled(False)
        scene.pyphysx.set_scene_finalizer_trace_enabled(False)
        scene.pyphysx.set_scene_solve_writeback_trace_enabled(False)
        scene.pyphysx.set_scene_solve_block_trace_enabled(False)
        settle = audit._settle_after_contact(
            scene,
            max_steps=6000,
            linear_threshold=0.01,
            angular_threshold=0.01,
            consecutive_steps=20,
        )
        active = scene.state(active_index)
        target = scene.state(target_index)
        result.update(
            {
                "settle": settle,
                "localEndpoint": {
                    "active": [active["x"], active["y"]],
                    "target": [target["x"], target["y"]],
                },
                "endpointErrorM": {
                    "active": _distance(active, unity_active),
                    "target": _distance(target, unity_target),
                },
            }
        )
    if args.role_swap:
        output = OUTPUT.with_name("hybrid_p6_endpoint_14000_role_swap_20260711.json")
    elif args.unity_solver_inertia_locks:
        output = OUTPUT.with_name("hybrid_p6_endpoint_14000_unity_solver_inertia_locks_20260711.json")
    elif args.initial_yaw:
        output = OUTPUT.with_name("hybrid_p6_endpoint_14000_initial_yaw_diagnostic_20260711.json")
    else:
        output = OUTPUT
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "output": str(output),
        "firstContactCounts": result["firstContactCounts"],
        "finalizerCallCount": len(result.get("localFinalizerCallsThroughFirstWriteback", [])),
        "solveWritebackCallCount": len(result.get("localSolveWritebackCallsThroughFirstWriteback", [])),
        "solveBlockCallCount": len(result.get("localSolveBlockCallsThroughFirstWriteback", [])),
        "endpointErrorM": result.get("endpointErrorM"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
