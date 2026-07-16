#!/usr/bin/env python3
"""Run the captured six-shot session through the hybrid local Scene for P6.

This is an offline, no-oracle audit.  It uses only recorded reset positions,
BESTSHOT commands, and Random.Range friction values.  Unity final positions are
read from the original controlled sampler records, not supplied to the Scene.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
import types
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

SAMPLES = PROJECT_ROOT / "data/calibration/front_half_pcm_samples_20260710_012534.jsonl"
EVENTS = PROJECT_ROOT / "log/unity_runtime_probe_20260710_012403/events.jsonl"
OUTPUT = PROJECT_ROOT / "data/calibration/hybrid_p6_endpoint_sixshot_20260711.json"
BUNDLED_PYPHYSX_EXTENSION = (
    PROJECT_ROOT / "local_simulator" / "runtime" / "pyphysx" / "_pyphysx.cp38-win_amd64.pyd"
)


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _distance(left: dict[str, Any], right: list[float]) -> float:
    return math.hypot(float(left["x"]) - float(right[0]), float(left["y"]) - float(right[1]))


def _endpoint(position: list[float], index: int) -> list[float]:
    return [float(position[2 * index]), float(position[2 * index + 1])]


def _is_cleared(position: list[float]) -> bool:
    return abs(float(position[0])) < 1e-12 and abs(float(position[1])) < 1e-12


def _load_orientation_manifest(path: Path | None) -> dict[str, dict[str, Any]]:
    """Load per-sample reset yaw truth captured from Unity.

    ``RESETPOSITION`` changes only positions: it intentionally preserves each
    Rigidbody's quaternion.  A protocol POSITION record consequently cannot
    reconstruct a later reset shot on its own.  The manifest is deliberately
    small and human-readable, for example::

        {
          "12008": {"yaws": {"0": 0.0, "10": 0.0}}
        }

    The active stone's yaw may alternatively be supplied as ``activeYaw``.
    ``yaws`` uses stone indices as JSON object keys.
    """

    if path is None:
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("orientation manifest must be a JSON object")
    rows = raw.get("samples", raw)
    if not isinstance(rows, dict):
        raise ValueError("orientation manifest 'samples' must be a JSON object")
    result: dict[str, dict[str, Any]] = {}
    for sample_id, value in rows.items():
        if not isinstance(value, dict):
            raise ValueError(f"orientation manifest entry {sample_id!r} must be an object")
        result[str(sample_id)] = value
    return result


def _orientation_for_sample(
    manifest: dict[str, dict[str, Any]],
    sample: dict[str, Any],
    *,
    active_index: int,
    target_indices: list[int],
) -> tuple[dict[int, float], float | None, list[int]]:
    """Return reset yaw overrides, active yaw, and missing required indices."""

    entry = manifest.get(str(sample.get("sample_id")))
    required = [active_index, *target_indices]
    if entry is None:
        return {}, None, required
    raw_yaws = entry.get("yaws", entry.get("yawOverrides", {}))
    if not isinstance(raw_yaws, dict):
        raise ValueError(f"sample {sample.get('sample_id')}: yaws must be an object")
    yaws = {int(index): float(value) for index, value in raw_yaws.items()}
    active_yaw = entry.get("activeYaw", yaws.get(active_index))
    if active_yaw is not None:
        active_yaw = float(active_yaw)
        yaws[active_index] = active_yaw
    missing = [index for index in required if index not in yaws]
    return yaws, active_yaw, missing


def _settle(scene: Any, *, max_steps: int = 6000) -> dict[str, Any]:
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
            linear = math.sqrt(state["vx"] ** 2 + state["vy"] ** 2 + state["vz"] ** 2)
            angular = math.sqrt(state["wx"] ** 2 + state["wy"] ** 2 + state["w"] ** 2)
            if linear > 0.01 or angular > 0.01:
                moving.append(slot.index)
        quiet = quiet + 1 if not moving else 0
        if quiet >= 20:
            return {"settled": True, "steps": step, "movingIndices": []}
    return {"settled": False, "steps": max_steps, "movingIndices": moving}


def _summary(values: Iterable[float]) -> dict[str, float | int | None]:
    items = [float(value) for value in values]
    if not items:
        return {"count": 0, "rmseM": None, "meanM": None, "maxM": None}
    return {
        "count": len(items),
        "rmseM": math.sqrt(sum(value * value for value in items) / len(items)),
        "meanM": sum(items) / len(items),
        "maxM": max(items),
    }


def install_pyphysx_extension(extension: Path) -> None:
    """Load an isolated audit binding without replacing the production package."""

    resolved = extension.resolve()
    if not resolved.is_file():
        raise RuntimeError(f"pyphysx extension does not exist: {resolved}")
    package = types.ModuleType("pyphysx")
    package.__path__ = []
    sys.modules["pyphysx"] = package
    spec = importlib.util.spec_from_file_location("pyphysx._pyphysx", resolved)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load pyphysx extension: {resolved}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["pyphysx._pyphysx"] = module
    spec.loader.exec_module(module)
    for name in dir(module):
        if not name.startswith("_"):
            setattr(package, name, getattr(module, name))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--samples",
        type=Path,
        default=SAMPLES,
        help="Controlled Unity sample JSONL. Defaults to the historical six-shot capture.",
    )
    parser.add_argument(
        "--events",
        type=Path,
        default=EVENTS,
        help="Matching Unity runtime events JSONL containing the friction stream.",
    )
    parser.add_argument(
        "--max-shots",
        type=int,
        help=(
            "Audit only this leading number of recorded shots. Diagnostic-only: "
            "use when a targeted raw C04 capture is complete through the selected "
            "shot but its later high-volume event stream is intentionally discarded."
        ),
    )
    angular_setter = parser.add_mutually_exclusive_group()
    angular_setter.add_argument(
        "--unity-native-angular-setter-wrapper",
        dest="unity_native_angular_setter_wrapper",
        action="store_true",
        default=False,
        help="Historical A/B: apply the superseded quaternion-projected angular setter wrapper.",
    )
    angular_setter.add_argument(
        "--no-unity-native-angular-setter-wrapper",
        dest="unity_native_angular_setter_wrapper",
        action="store_false",
        help="Use the A9-backed tilt-only native bridge setter (production default).",
    )
    parser.add_argument(
        "--set-active-scene-membership",
        action="store_true",
        help="Diagnostic B-chain switch: remove/re-add inactive actors to reproduce the alternate work-unit role order.",
    )
    refilter = parser.add_mutually_exclusive_group()
    refilter.add_argument(
        "--unity-setactive-refilter",
        dest="unity_setactive_refilter",
        action="store_true",
        default=True,
        help="Rebuild interactions after Unity-style shape refresh (production default).",
    )
    refilter.add_argument(
        "--no-unity-setactive-refilter",
        dest="unity_setactive_refilter",
        action="store_false",
        help="Historical A/B only: do not rebuild interactions after shape refresh.",
    )
    parser.add_argument(
        "--unity-setactive-no-sim",
        action="store_true",
        help="Source-backed B-chain candidate: preserve actor/shape while recreating PhysX RigidSim on SetActive.",
    )
    parser.add_argument(
        "--unity-material-transition",
        action="store_true",
        help="Use the physical 0 -> 0.6 material transition at the current PCM-shell pose instead of eMODIFY_CONTACTS.",
    )
    parser.add_argument(
        "--wake-target-at-current-pcm-shell",
        action="store_true",
        help="Diagnostic C05 timing: wake the stationary target only once the current active pose enters the PCM shell.",
    )
    parser.add_argument(
        "--pyphysx-extension",
        type=Path,
        help="Override the bundled pyphysx extension. Intended only for extension A/B work.",
    )
    parser.add_argument(
        "--orientation-manifest",
        type=Path,
        help=(
            "JSON mapping sample ids to Unity reset yaw truth. Required for a strict "
            "persistent RESETPOSITION endpoint audit because the protocol omits quaternions."
        ),
    )
    parser.add_argument(
        "--require-orientation-truth",
        action="store_true",
        help="fail instead of producing a non-strict row when active/target reset yaw truth is absent",
    )
    parser.add_argument(
        "--motion-kernel",
        choices=("recovered-python", "native-pyphysx", "unity-wasm-oracle"),
        default="native-pyphysx",
        help=(
            "Motion update implementation before PCM. native-pyphysx uses the compiled "
            "f64 replica in the local scalar pyphysx extension; unity-wasm-oracle calls "
            "the recovered Unity wasm once per tick. Neither consumes captured Unity "
            "setters or state."
        ),
    )
    parser.add_argument(
        "--unity-native-angular-setter-residual-z",
        action="store_true",
        help="Diagnostic A9-backed native setter mode: preserve the observed bridge Z residual while writing script Y.",
    )
    parser.add_argument(
        "--unity-native-angular-setter-tilt-only",
        action="store_true",
        default=True,
        help="Diagnostic A9-backed native setter mode: keep tilt bridge residuals but do not project through yaw.",
    )
    parser.add_argument(
        "--unity-native-angular-setter-direct-y",
        dest="unity_native_angular_setter_tilt_only",
        action="store_false",
        help="Historical A/B: clear native bridge tilt residuals and write a literal [0, wy, 0].",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    extension = args.pyphysx_extension or BUNDLED_PYPHYSX_EXTENSION
    if sys.version_info[:2] != (3, 8) or sys.maxsize <= 2**32:
        raise RuntimeError(
            "The bundled pyphysx extension requires 64-bit CPython 3.8. "
            "Use that interpreter for strict PhysX replay."
        )
    install_pyphysx_extension(extension)
    from tools.reverse import audit_persistent_scene_sequence as sequence
    from tools.reverse.front_half_pcm_replay import event_shot_groups, load_jsonl
    from tools.reverse.unity_wasm_motion_oracle import WasmMotionStepper
    from unity_front_half_physx import NativePyphysxMotionStepper, PersistentPhysxFrontHalfScene

    samples = _load_jsonl(args.samples)
    groups = event_shot_groups(load_jsonl(args.events))
    orientation_manifest = _load_orientation_manifest(args.orientation_manifest)
    if args.max_shots is not None:
        if args.max_shots < 1:
            raise ValueError("--max-shots must be positive")
        samples = samples[:args.max_shots]
        groups = groups[:args.max_shots]
    if len(samples) != len(groups):
        raise ValueError(f"sample/event count mismatch: {len(samples)} != {len(groups)}")

    scene = PersistentPhysxFrontHalfScene(
        stone_count=16,
        ice_mesh_mode="unity-source-once",
        ice_use_fast_midphase=True,
        emulate_unity_native_angular_setter_rotation=args.unity_native_angular_setter_wrapper,
        emulate_unity_native_angular_setter_residual_z=args.unity_native_angular_setter_residual_z,
        emulate_unity_native_angular_setter_tilt_only=(
            args.unity_native_angular_setter_tilt_only
            and not args.unity_native_angular_setter_wrapper
        ),
        set_active_scene_membership=args.set_active_scene_membership,
        emulate_unity_setactive_refilter=args.unity_setactive_refilter,
        emulate_unity_setactive_no_sim=args.unity_setactive_no_sim,
        restore_active_friction_at_pcm_shell=args.unity_material_transition,
        enable_stone_stone_contact_friction_override=not args.unity_material_transition,
        wake_target_at_current_pcm_shell=args.wake_target_at_current_pcm_shell,
    )
    rows: list[dict[str, Any]] = []
    if args.motion_kernel == "unity-wasm-oracle":
        motion_stepper = WasmMotionStepper()
    elif args.motion_kernel == "native-pyphysx":
        motion_stepper = NativePyphysxMotionStepper(scene.pyphysx)
    else:
        motion_stepper = None
    for seq, (sample, group) in enumerate(zip(samples, groups)):
        active_index = int(sample["active_shot_num"])
        target_indices = [int(value) for value in sample.get("target_indices") or []]
        if len(target_indices) != 1:
            raise ValueError(f"sample {sample.get('sample_id')} must have one target")
        target_index = target_indices[0]
        yaw_overrides, active_yaw, missing_orientation_indices = _orientation_for_sample(
            orientation_manifest,
            sample,
            active_index=active_index,
            target_indices=target_indices,
        )
        if args.require_orientation_truth and missing_orientation_indices:
            raise ValueError(
                f"sample {sample.get('sample_id')}: missing Unity reset yaw truth for "
                f"stone indices {missing_orientation_indices}"
            )
        scene.reset_positions(
            sample["reset_position"],
            yaw_overrides=yaw_overrides,
            settle_steps=1,
        )
        noises = [float(item["noise"]) for item in group["friction"]]
        replay = scene.run_bestshot_to_first_contact(
            active_index,
            [float(group["v0"]), float(group["h0"]), float(group["w0"])],
            noises,
            target_indices=target_indices,
            max_steps=len(noises),
            motion_stepper=motion_stepper,
            yaw=active_yaw,
        )

        row: dict[str, Any] = {
            "seq": seq,
            "sampleId": int(sample["sample_id"]),
            "label": sample["label"],
            "finalSource": sample.get("final_source"),
            "policy": "no Unity pose, velocity, cache, or post-collision state is injected",
            "unityMaterialTransition": bool(args.unity_material_transition),
            "wakeTargetAtCurrentPcmShell": bool(args.wake_target_at_current_pcm_shell),
            "motionKernel": args.motion_kernel,
            "reachedFirstContact": bool(replay.get("reachedFirstContact")),
            "firstContactStep": replay.get("steps"),
            "firstContactCounts": [
                int(report.get("contact_count") or 0) for report in replay.get("firstContactReports") or []
            ],
            "physicsOnlyTrailingStep": bool(replay.get("physicsOnlyTrailingStep")),
            "orientationEvidence": {
                "resetSemantics": "RESETPOSITION preserves Rigidbody quaternion",
                "provided": not missing_orientation_indices,
                "missingStoneIndices": missing_orientation_indices,
                "strictEndpointComparable": not missing_orientation_indices,
            },
        }
        if replay.get("reachedFirstContact"):
            row["firstContactEntrance"] = {
                "active": replay.get("beforeScene"),
                "targets": replay.get("targetsBeforeScene"),
                "afterScene": replay.get("afterScene"),
                "targetsAfterScene": replay.get("targetsAfterScene"),
            }
            # Match the P6 single-shot audit: advance the first writeback frame,
            # then let only the local Scene carry the rest of the collision tail.
            scene.scene.simulate(scene.dt)
            scene.scene.get_contact_reports()
            row["settle"] = _settle(scene)
        else:
            row["settle"] = {"settled": False, "steps": 0, "reason": "no local stone-stone contact"}

        unity_active = _endpoint(sample["after_position"], active_index)
        unity_target = _endpoint(sample["after_position"], target_index)
        local_active = scene.state(active_index)
        local_target = scene.state(target_index)
        row["unityEndpoint"] = {"active": unity_active, "target": unity_target}
        row["localEndpoint"] = {
            "active": [local_active["x"], local_active["y"]],
            "target": [local_target["x"], local_target["y"]],
            "activeEnabled": bool(local_active["enabled"]),
            "targetEnabled": bool(local_target["enabled"]),
        }
        # Infinite mode routes the completed board state together with GO for
        # the next player.  That is a normal terminal position, not a timeout
        # fallback; the sampler labels it explicitly to distinguish it from a
        # stale reset POSITION.
        reliable_final_sources = {"position", "next_go_final_position"}
        if sample.get("final_source") in reliable_final_sources:
            row["endpointErrorM"] = {
                "active": None if _is_cleared(unity_active) else _distance(local_active, unity_active),
                "target": None if _is_cleared(unity_target) else _distance(local_target, unity_target),
            }
            row["unityCleared"] = {
                "active": _is_cleared(unity_active),
                "target": _is_cleared(unity_target),
            }
        else:
            row["endpointErrorM"] = None
            row["reasonNoEndpointError"] = "Unity sampler did not receive a reliable final POSITION"
        rows.append(row)

    if motion_stepper is not None:
        motion_stepper.close()

    active_errors = [
        row["endpointErrorM"]["active"]
        for row in rows
        if row.get("endpointErrorM") and row["endpointErrorM"]["active"] is not None
    ]
    target_errors = [
        row["endpointErrorM"]["target"]
        for row in rows
        if row.get("endpointErrorM") and row["endpointErrorM"]["target"] is not None
    ]
    report = {
        "schema": "hybrid_p6_endpoint_sixshot_v1",
        "purpose": "P6 no-oracle endpoint audit for the captured six-shot session.",
        "policy": "no Unity pose, velocity, cache, or post-collision state is injected",
        "configuration": {
            "scalarMath": bool(scene.pyphysx.is_scalar_math_enabled()),
            "iceMidphase": scene.runtime_ice_mesh_meta.get("useFastMidphase"),
            "sceneLifecycle": "one persistent local Scene; each recorded reset changes positions only",
            "orientationManifest": str(args.orientation_manifest) if args.orientation_manifest else None,
            "strictOrientationTruthRequired": bool(args.require_orientation_truth),
            "motionKernel": args.motion_kernel,
            "unityNativeAngularSetterWrapper": bool(args.unity_native_angular_setter_wrapper),
            "unityNativeAngularSetterResidualZ": bool(args.unity_native_angular_setter_residual_z),
            "unityNativeAngularSetterTiltOnly": bool(
                args.unity_native_angular_setter_tilt_only
                and not args.unity_native_angular_setter_wrapper
            ),
            "setActiveSceneMembership": bool(args.set_active_scene_membership),
            "unitySetActiveRefilter": bool(args.unity_setactive_refilter),
            "unitySetActiveNoSim": bool(args.unity_setactive_no_sim),
            "unityMaterialTransition": bool(args.unity_material_transition),
            "wakeTargetAtCurrentPcmShell": bool(args.wake_target_at_current_pcm_shell),
            "stoneStoneContactFrictionOverride": not bool(args.unity_material_transition),
            "pyphysxExtension": str(extension),
        },
        "aggregate": {
            "rowCount": len(rows),
            "reachedFirstContactCount": sum(1 for row in rows if row["reachedFirstContact"]),
            "strictEndpointComparableCount": sum(
                1 for row in rows if row["orientationEvidence"]["strictEndpointComparable"]
            ),
            "activeEndpointError": _summary(active_errors),
            "targetEndpointError": _summary(target_errors),
            "unreliableUnityEndpointSampleIds": [
                row["sampleId"]
                for row in rows
                if row.get("finalSource") not in {"position", "next_go_final_position"}
            ],
        },
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "aggregate": report["aggregate"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
