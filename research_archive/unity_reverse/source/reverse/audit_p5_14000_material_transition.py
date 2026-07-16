#!/usr/bin/env python3
"""Test the Unity first-solver material transition without eMODIFY_CONTACTS."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.reverse.diagnose_hybrid_bvh4_source_shell import _install_hybrid_module
from tools.reverse.audit_p5_14000_contactbuffer import (
    EVENTS,
    SAMPLES,
    UNITY_SOLVER,
    _load_jsonl,
    _score,
)


OUTPUT = PROJECT_ROOT / "data" / "calibration" / "p5_14000_material_transition_audit_20260711.json"


def _compact(row: dict[str, Any]) -> dict[str, Any]:
    manager = row.get("contact_manager_state") or {}
    return {
        "sequence": row.get("sequence"),
        "contactCount": row.get("contact_count"),
        "staticFriction": [item.get("static_friction") for item in row.get("contacts") or []],
        "dynamicFriction": [item.get("dynamic_friction") for item in row.get("contacts") or []],
        "flags": manager.get("flags"),
        "frictionPatchCount": manager.get("friction_patch_count"),
        "bodyFrame0": (row.get("body_frame0") or {}).get("p"),
        "bodyFrame1": (row.get("body_frame1") or {}).get("p"),
        "points": [item.get("point") for item in row.get("contacts") or []],
    }


def main() -> int:
    _install_hybrid_module()
    from tools.reverse.front_half_pcm_replay import event_shot_groups, load_jsonl
    from unity_front_half_physx import PersistentPhysxFrontHalfScene

    sample = _load_jsonl(SAMPLES)[0]
    group = event_shot_groups(load_jsonl(EVENTS))[0]
    unity = json.loads(UNITY_SOLVER.read_text(encoding="utf-8"))["stoneStoneRows"][0]
    scene = PersistentPhysxFrontHalfScene(
        stone_count=16,
        ice_mesh_mode="unity-source-once",
        ice_use_fast_midphase=True,
        restore_active_friction_at_pcm_shell=True,
    )
    # This removes the local-only eMODIFIABLE_CONTACT bit. The active material
    # becomes 0.6 only in the tick that reaches the PCM shell.
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
    rows = list(scene.pyphysx.get_scene_finalizer_trace(True))
    scene.pyphysx.set_scene_finalizer_trace_enabled(False)
    matched = min(rows, key=lambda row: _score(row, unity))
    report = {
        "schema": "p5_14000_material_transition_audit_v1",
        "purpose": "Verify the observed 0.36 first-solver friction without a contact-modify pair flag.",
        "policy": "one material-timing change; existing Unity raw state; no parameter scan",
        "unity": {
            "staticFriction": [0.36000001430511475, 0.36000001430511475],
            "dynamicFriction": [0.36000001430511475, 0.36000001430511475],
            "workUnitFlags": 611,
        },
        "local": _compact(matched),
        "framePositionSquaredError": _score(matched, unity),
    }
    report["conclusion"] = (
        "Pass only when the physical material transition yields 0.36 contact friction and flags=611; "
        "contact-point equality is deliberately a separate pair-lifecycle question."
    )
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT), "local": report["local"], "framePositionSquaredError": report["framePositionSquaredError"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
