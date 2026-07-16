#!/usr/bin/env python3
"""Audit whether actor Scene membership alone reproduces Unity SetActive contact state."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.reverse.diagnose_hybrid_bvh4_source_shell import _install_hybrid_module
from tools.reverse.audit_p5_14000_contactbuffer import SAMPLES, EVENTS, UNITY_SOLVER, _load_jsonl, _score


OUTPUT = PROJECT_ROOT / "data/calibration/setactive_membership_contactbuffer_audit_20260711.json"


def _run(membership: bool, sample: dict[str, Any], group: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    from unity_front_half_physx import PersistentPhysxFrontHalfScene

    scene = PersistentPhysxFrontHalfScene(
        stone_count=16,
        ice_mesh_mode="unity-source-once",
        ice_use_fast_midphase=True,
        set_active_scene_membership=membership,
        restore_active_friction_at_pcm_shell=True,
    )
    scene.scene.set_stone_stone_contact_friction_override(False)
    scene.pyphysx.clear_scene_finalizer_trace()
    scene.pyphysx.set_scene_finalizer_trace_enabled(True)
    scene.pyphysx.clear_scene_pcm_trace()
    scene.pyphysx.set_scene_pcm_trace_enabled(True)
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
    pcm_rows = list(scene.pyphysx.get_scene_pcm_trace(True))
    scene.pyphysx.set_scene_finalizer_trace_enabled(False)
    scene.pyphysx.set_scene_pcm_trace_enabled(False)
    return {"finalizers": rows, "pcm": pcm_rows}


def _compact(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "sequence": row["sequence"],
        "contactCount": row["contact_count"],
        "bodyFrame0": row["body_frame0"]["p"],
        "bodyFrame1": row["body_frame1"]["p"],
        "contactManagerState": row.get("contact_manager_state"),
        "points": [entry["point"] for entry in row.get("contacts") or []],
    }


def _compact_pcm(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "sequence": row.get("sequence"),
        "transform0": row.get("transform0"),
        "transform1": row.get("transform1"),
        "contactCountBefore": row.get("contact_count_before"),
        "contactCountAfter": row.get("contact_count_after"),
        "cacheBefore": row.get("cache_before"),
        "cacheAfter": row.get("cache_after"),
        "points": row.get("contacts"),
    }


def main() -> int:
    _install_hybrid_module()
    from tools.reverse.front_half_pcm_replay import event_shot_groups, load_jsonl

    sample = _load_jsonl(SAMPLES)[0]
    group = event_shot_groups(load_jsonl(EVENTS))[0]
    unity_rows = json.loads(UNITY_SOLVER.read_text(encoding="utf-8"))["stoneStoneRows"]
    unity = unity_rows[0]
    report: dict[str, Any] = {
        "schema": "setactive_membership_contactbuffer_audit_v1",
        "purpose": "Falsify whether remove/add of the stable actor alone reproduces Unity SetActive.",
        "policy": "same 14000 input; no Unity re-sampling; no parameter tuning",
        "unity": {
            "rowIndex": 0,
            "points": (
                (unity.get("contactBuffer") or {}).get("candidate", {}).get("contactsPreview") or []
            ),
        },
        "variants": {},
    }
    for membership in (False, True):
        trace = _run(membership, sample, group)
        rows = trace["finalizers"]
        best = min(rows, key=lambda row: _score(row, unity))
        report["variants"]["removeAddActor" if membership else "shapeFlagOnly"] = {
            "matchedFinalizer": _compact(best),
            "framePositionSquaredError": _score(best, unity),
            "pcmTrace": [_compact_pcm(row) for row in trace["pcm"]],
        }
    report["conclusion"] = (
        "If membership flips body order and tangential points while changing contact count, "
        "actor membership is a sensitivity, not a production-equivalent SetActive implementation."
    )
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT), "variants": report["variants"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
