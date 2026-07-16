#!/usr/bin/env python3
"""Run one Unity-source ice shell diagnostic through the SSE/BVH34 backend.

This is only a front-half ground-contact control. Stone-stone contact is
disabled and remains owned by the scalar direct PCM audit.
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

PYPHYSX_SSE = Path(
    r"D:\esp\tmp\curling_pyphysx_build_native_dump_py38\lib\_pyphysx.cp38-win_amd64.pyd"
)
OUTPUT = PROJECT_ROOT / "data/calibration/sse_bvh4_source_shell_14000_20260710.json"


def _install_sse_module() -> None:
    package = types.ModuleType("pyphysx")
    package.__path__ = []
    sys.modules["pyphysx"] = package
    spec = importlib.util.spec_from_file_location("pyphysx._pyphysx", PYPHYSX_SSE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load SSE pyphysx extension: {PYPHYSX_SSE}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["pyphysx._pyphysx"] = module
    spec.loader.exec_module(module)
    for name in dir(module):
        if not name.startswith("_"):
            setattr(package, name, getattr(module, name))
    # The archived/native extension predates this scalar-build marker. This
    # script intentionally audits ground contact only and never uses its PCM.
    package.is_scalar_math_enabled = lambda: True


def main() -> int:
    _install_sse_module()
    from tools.reverse import audit_persistent_scene_sequence as audit
    from tools.reverse.front_half_pcm_replay import FIRST_PCM_CENTER_DISTANCE, event_shot_groups, load_jsonl
    from unity_front_half_physx import PersistentPhysxFrontHalfScene

    sample = audit._load_jsonl(audit.DEFAULT_SAMPLES)[0]
    group = event_shot_groups(load_jsonl(audit.DEFAULT_EVENTS))[0]
    scene = PersistentPhysxFrontHalfScene(
        stone_count=16,
        ice_mesh_mode="unity-source-once",
        ice_use_fast_midphase=True,
        require_p4_contact_hooks=False,
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
    result: dict[str, object] = {"reachedPcmShell": False}
    for step, item in enumerate(group["friction"], 1):
        row = scene.step_custom_sliding(active_index, float(item["noise"]))
        active = row["afterScene"]
        target = scene.state(target_index)
        distance = ((active["x"] - target["x"]) ** 2 + (active["y"] - target["y"]) ** 2) ** 0.5
        if distance <= FIRST_PCM_CENTER_DISTANCE:
            result = {
                "reachedPcmShell": True,
                "step": step,
                "distance": distance,
                "active": active,
                "target": target,
            }
            break
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT), "result": result}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
