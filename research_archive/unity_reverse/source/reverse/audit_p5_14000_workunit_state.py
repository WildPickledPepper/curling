#!/usr/bin/env python3
"""Compare the 14000 Unity/local PxcNpWorkUnit state without re-sampling Unity."""

from __future__ import annotations

import json
import struct
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.reverse.diagnose_hybrid_bvh4_source_shell import _install_hybrid_module
from tools.reverse.audit_p5_14000_contactbuffer import EVENTS, SAMPLES, UNITY_SOLVER, _load_jsonl, _score


RAW_EVENTS = PROJECT_ROOT / "log/unity_runtime_probe_20260710_012403/events.jsonl"
OUTPUT = PROJECT_ROOT / "data/calibration/p5_14000_workunit_state_audit_20260711.json"


def _u32(raw: list[int], offset: int) -> int:
    return struct.unpack_from("<I", bytes(raw), offset)[0]


def _u16(raw: list[int], offset: int) -> int:
    return struct.unpack_from("<H", bytes(raw), offset)[0]


def _decode_unity_manager(shape_interaction: int) -> dict[str, int]:
    for line in RAW_EVENTS.open(encoding="utf-8"):
        event = json.loads(line)
        data = event.get("data") or {}
        if (data.get("hook") or {}).get("name") != "createFinalizeSolverContacts":
            continue
        if data.get("phase") != "after":
            continue
        for extra in data.get("extraDumps") or []:
            if not isinstance(extra, dict) or extra.get("shapeInteractionPtr") != shape_interaction:
                continue
            window = extra.get("shapeInteractionWindow") or {}
            raw = window.get("rawBytes") or []
            manager = _u32(raw, 56)  # wasm32 Sc::ShapeInteraction::mManager.
            target = next(
                item for item in window.get("pointerTargets") or []
                if item.get("sourceOffset") == 56 and item.get("ptr") == manager
            )
            state = target["rawBytes"]
            return {
                "shape_interaction": shape_interaction,
                "contact_manager": manager,
                "rigid_core0": _u32(state, 16),
                "rigid_core1": _u32(state, 20),
                "shape_core0": _u32(state, 24),
                "shape_core1": _u32(state, 28),
                "friction_data": _u32(state, 36),
                "flags": _u16(state, 40),
                "friction_patch_count": state[42],
                "status_flags": state[43],
                "index": _u32(state, 48),
                "transform_cache0": _u32(state, 56),
                "transform_cache1": _u32(state, 60),
                "edge_index": _u32(state, 64),
                "np_index": _u32(state, 68),
            }
    raise ValueError(f"missing Unity ShapeInteraction {shape_interaction}")


def main() -> int:
    _install_hybrid_module()
    from tools.reverse.front_half_pcm_replay import event_shot_groups, load_jsonl
    from unity_front_half_physx import PersistentPhysxFrontHalfScene

    sample = _load_jsonl(SAMPLES)[0]
    group = event_shot_groups(load_jsonl(EVENTS))[0]
    unity = json.loads(UNITY_SOLVER.read_text(encoding="utf-8"))["stoneStoneRows"][0]
    unity_state = _decode_unity_manager(int(unity["contactDesc"]["shapeInteraction"]))

    scene = PersistentPhysxFrontHalfScene(
        stone_count=16,
        ice_mesh_mode="unity-source-once",
        ice_use_fast_midphase=True,
    )
    # This is the factual A/B: disabled means no eMODIFY_CONTACTS pair flag.
    scene.scene.set_stone_stone_contact_friction_override(False)
    scene.pyphysx.clear_scene_finalizer_trace()
    scene.pyphysx.set_scene_finalizer_trace_enabled(True)
    scene.reset_positions(sample["reset_position"], settle_steps=1)
    scene.run_bestshot_to_first_contact(
        int(sample["active_shot_num"]),
        [float(group["v0"]), float(group["h0"]), float(group["w0"])],
        [float(item["noise"]) for item in group["friction"]],
        target_indices=[int(sample["target_indices"][0])],
        max_steps=len(group["friction"]),
    )
    scene.scene.simulate(scene.dt)
    scene.scene.get_contact_reports()
    local = min(scene.pyphysx.get_scene_finalizer_trace(True), key=lambda row: _score(row, unity))
    local_state = dict(local["contact_manager_state"])
    compared = ("flags", "friction_patch_count", "status_flags", "index", "transform_cache0", "transform_cache1", "edge_index", "np_index")
    report = {
        "schema": "p5_14000_workunit_state_audit_v1",
        "policy": "existing Unity runtime log; local read-only trace; no parameter fitting",
        "unity": unity_state,
        "localModifyDisabled": local_state,
        "fieldComparison": {
            key: {"unity": unity_state[key], "local": local_state[key], "equal": unity_state[key] == local_state[key]}
            for key in compared
        },
        "localContactPoints": [contact["point"] for contact in local["contacts"]],
        "conclusion": (
            "The callback-created eMODIFY_CONTACTS bit is a proven local-only work-unit divergence. "
            "Removing it does not by itself close the tangential ContactBuffer displacement."
        ),
    }
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT), "fieldComparison": report["fieldComparison"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
