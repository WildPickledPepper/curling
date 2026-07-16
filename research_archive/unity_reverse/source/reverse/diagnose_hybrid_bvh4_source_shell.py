#!/usr/bin/env python3
"""Verify the scalar-PCM/SIMD-BVH4 hybrid through one Unity-source shell.

The extension is loaded from its isolated build output.  This probe keeps the
P4 pair/cache bindings enabled, but disables the target shape before replay so
it measures only the Unity cooked-ice traversal before stone-stone contact.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import types
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

PYPHYSX_HYBRID = Path(
    r"D:\esp\tmp\curling_pyphysx_hybrid_build\lib\_pyphysx.cp38-win_amd64.pyd"
)
OUTPUT = PROJECT_ROOT / "data/calibration/hybrid_bvh4_source_shell_14000_20260711.json"


def _install_hybrid_module() -> None:
    package = types.ModuleType("pyphysx")
    package.__path__ = []
    sys.modules["pyphysx"] = package
    spec = importlib.util.spec_from_file_location("pyphysx._pyphysx", PYPHYSX_HYBRID)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load hybrid pyphysx extension: {PYPHYSX_HYBRID}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["pyphysx._pyphysx"] = module
    spec.loader.exec_module(module)
    for name in dir(module):
        if not name.startswith("_"):
            setattr(package, name, getattr(module, name))


def main() -> int:
    _install_hybrid_module()
    from tools.reverse import audit_persistent_scene_sequence as audit
    from tools.reverse.front_half_pcm_replay import FIRST_PCM_CENTER_DISTANCE, event_shot_groups, load_jsonl
    from unity_front_half_physx import PersistentPhysxFrontHalfScene

    sample = audit._load_jsonl(audit.DEFAULT_SAMPLES)[0]
    group = event_shot_groups(load_jsonl(audit.DEFAULT_EVENTS))[0]
    scene = PersistentPhysxFrontHalfScene(
        stone_count=16,
        ice_mesh_mode="unity-source-once",
        ice_use_fast_midphase=True,
    )
    scene.reset_positions(sample["reset_position"], settle_steps=1)
    target_index = int((sample.get("target_indices") or [8])[0])
    target_slot = scene.slots[target_index]
    target_slot.shape.set_flag(scene.pyphysx.ShapeFlag.SIMULATION_SHAPE, False)
    target_slot.body.disable_gravity()
    target_slot.body.set_linear_velocity([0.0, 0.0, 0.0])
    target_slot.body.set_angular_velocity([0.0, 0.0, 0.0])
    target_slot.body.put_to_sleep()
    active_index = int(sample["active_shot_num"])
    scene.start_bestshot(active_index, [float(group["v0"]), float(group["h0"]), float(group["w0"])])

    result: dict[str, object] = {
        "scalarMath": bool(scene.pyphysx.is_scalar_math_enabled()),
        "hasP4PairHook": hasattr(scene.scene, "set_stone_stone_contact_friction_override"),
        "hasP4CacheHook": hasattr(scene.pyphysx, "set_scene_pcm_unity_cache_lifecycle_enabled"),
        "iceMidphase": scene.runtime_ice_mesh_meta.get("useFastMidphase"),
        "reachedPcmShell": False,
    }
    for step, item in enumerate(group["friction"], 1):
        row = scene.step_custom_sliding(active_index, float(item["noise"]))
        active = row["afterScene"]
        target = scene.state(target_index)
        distance = ((active["x"] - target["x"]) ** 2 + (active["y"] - target["y"]) ** 2) ** 0.5
        if distance <= FIRST_PCM_CENTER_DISTANCE:
            result.update(
                {
                    "reachedPcmShell": True,
                    "step": step,
                    "distance": distance,
                    "active": active,
                    "target": target,
                }
            )
            break
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT), "result": result}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
