#!/usr/bin/env python3
"""Locate the first persistent-scene post-contact divergence for sample 14000.

The script runs the rebuilt hybrid/x64 backend with the already-closed A19/B24
semantics.  It compares three same-run boundaries against existing Unity data:
the first PCM input, its generated ContactBuffer, and the next positive PCM
transform after the first dynamic-dynamic simulation step.
"""

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

from tools.reverse.audit_hybrid_p6_endpoint_sixshot import (  # noqa: E402
    EVENTS,
    SAMPLES,
    _load_jsonl,
    install_pyphysx_extension,
)


UNITY_SOLVER = ROOT / "data/calibration/front_half_pcm_solver_state_20260710.json"
DEFAULT_EXTENSION = Path(r"D:\esp\tmp\curling_pyphysx_hybrid_build\lib\_pyphysx.cp38-win_amd64.pyd")
DEFAULT_OUTPUT = ROOT / "data/calibration/c03_first_writeback_14000_20260712.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pyphysx-extension", type=Path, default=DEFAULT_EXTENSION)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--wake-target-at-current-pcm-shell",
        action="store_true",
        help="Diagnostic C05 timing A/B: wake target at current PCM shell rather than predicted next pose.",
    )
    return parser.parse_args()


def _max_delta(left: list[float], right: list[float]) -> float:
    return max(abs(float(a) - float(b)) for a, b in zip(left, right))


def _state_pose(state: dict[str, Any]) -> tuple[list[float], list[float]]:
    q_wxyz = state["quaternionWxyz"]
    return list(state["physxPosition"]), [q_wxyz[1], q_wxyz[2], q_wxyz[3], q_wxyz[0]]


def _unity_positive_rows(state: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in state["pcmContactRows"]:
        if row.get("hook") != "PxcPCMContactConvexConvex" or row.get("phase") != "after":
            continue
        buffer = (row.get("pcmInputs") or {}).get("contactBuffer") or {}
        candidate = buffer.get("candidate") or {}
        if int(candidate.get("count") or 0) > 0:
            rows.append(row)
    return rows


def _contact_pairs(unity: list[dict[str, Any]], local: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unmatched = set(range(len(local)))
    pairs: list[dict[str, Any]] = []
    for expected in unity:
        index = min(
            unmatched,
            key=lambda candidate: sum(
                (float(local[candidate]["position"][axis]) - float(expected["point"][axis])) ** 2
                for axis in range(3)
            ),
        )
        unmatched.remove(index)
        actual = local[index]
        pairs.append(
            {
                "pointMaxComponent": _max_delta(actual["position"], expected["point"]),
                "normalMaxComponent": _max_delta(actual["normal"], expected["normal"]),
                "separation": float(actual["separation"]) - float(expected["separation"]),
                "unity": expected,
                "hybrid": actual,
            }
        )
    return pairs


def main() -> int:
    args = parse_args()
    install_pyphysx_extension(args.pyphysx_extension)
    from tools.reverse.front_half_pcm_replay import event_shot_groups, load_jsonl
    from unity_front_half_physx import PersistentPhysxFrontHalfScene

    sample = _load_jsonl(SAMPLES)[0]
    group = event_shot_groups(load_jsonl(EVENTS))[0]
    unity = json.loads(UNITY_SOLVER.read_text(encoding="utf-8"))
    unity_pcm = _unity_positive_rows(unity)
    if len(unity_pcm) < 2:
        raise RuntimeError("expected at least two positive Unity PCM calls for 14000")
    first_unity, next_unity = unity_pcm[:2]
    first_dump = first_unity["pcmInputs"]
    first_contacts = first_dump["contactBuffer"]["candidate"]["contactsPreview"]

    scene = PersistentPhysxFrontHalfScene(
        stone_count=16,
        ice_mesh_mode="unity-source-once",
        ice_use_fast_midphase=True,
        emulate_unity_native_angular_setter_rotation=True,
        emulate_unity_setactive_no_sim=True,
        restore_active_friction_at_pcm_shell=True,
        enable_stone_stone_contact_friction_override=False,
        wake_target_at_current_pcm_shell=args.wake_target_at_current_pcm_shell,
    )
    scene.pyphysx.clear_scene_finalizer_trace()
    scene.pyphysx.clear_scene_solve_writeback_trace()
    scene.pyphysx.clear_scene_solve_block_trace()
    scene.pyphysx.set_scene_finalizer_trace_enabled(True)
    scene.pyphysx.set_scene_solve_writeback_trace_enabled(True)
    scene.pyphysx.set_scene_solve_block_trace_enabled(True)
    scene.reset_positions(sample["reset_position"], settle_steps=1)
    replay = scene.run_bestshot_to_first_contact(
        int(sample["active_shot_num"]),
        [float(group["v0"]), float(group["h0"]), float(group["w0"])],
        [float(item["noise"]) for item in group["friction"]],
        target_indices=[int(sample["target_indices"][0])],
        max_steps=len(group["friction"]),
    )
    local_before = replay["beforeScene"]
    local_after = replay["afterScene"]
    local_reports = replay["firstContactReports"]
    if len(local_reports) != 1:
        raise RuntimeError(f"expected one first local stone report, got {len(local_reports)}")

    unity_before_p = list(first_dump["transform0"]["p"])
    unity_before_q = list(first_dump["transform0"]["q"])
    unity_next_p = list(next_unity["pcmInputs"]["transform0"]["p"])
    unity_next_q = list(next_unity["pcmInputs"]["transform0"]["q"])
    local_before_p, local_before_q = _state_pose(local_before)
    local_after_p, local_after_q = _state_pose(local_after)
    local_contact_pairs = _contact_pairs(first_contacts, local_reports[0]["points"])

    report = {
        "schema": "c03_first_writeback_v1",
        "policy": "No Unity pose/cache/setter/state is injected. Existing Unity raw PCM rows are only comparison truth.",
        "configuration": {
            "a19SolverBodyLockedAxes": True,
            "identityPreservingNoSimulation": True,
            "currentPoseMaterialRestore": True,
            "contactModifyFrictionOverride": False,
            "wakeTargetAtCurrentPcmShell": bool(args.wake_target_at_current_pcm_shell),
        },
        "unity": {
            "firstPcmCall": int(first_unity["callIndex"]),
            "nextPcmCall": int(next_unity["callIndex"]),
            "firstPcmTransform": {"p": unity_before_p, "q": unity_before_q},
            "nextPcmTransform": {"p": unity_next_p, "q": unity_next_q},
            "firstContacts": first_contacts,
        },
        "hybrid": {
            "firstContactStep": int(replay["steps"]),
            "beforeScene": local_before,
            "afterScene": local_after,
            "firstContactReport": local_reports[0],
            "finalizerTrace": list(scene.pyphysx.get_scene_finalizer_trace(True)),
            "solveWritebackTrace": list(scene.pyphysx.get_scene_solve_writeback_trace(True)),
            "solveBlockTrace": list(scene.pyphysx.get_scene_solve_block_trace(True)),
        },
        "comparison": {
            "pcmInput": {
                "positionMaxComponent": _max_delta(local_before_p, unity_before_p),
                "quaternionMaxComponent": _max_delta(local_before_q, unity_before_q),
            },
            "contactBuffer": {
                "countDelta": len(local_reports[0]["points"]) - len(first_contacts),
                "pairs": local_contact_pairs,
                "maxPointComponent": max(pair["pointMaxComponent"] for pair in local_contact_pairs),
                "maxNormalComponent": max(pair["normalMaxComponent"] for pair in local_contact_pairs),
                "maxSeparation": max(abs(pair["separation"]) for pair in local_contact_pairs),
            },
            "nextPcmConsumer": {
                "positionMaxComponent": _max_delta(local_after_p, unity_next_p),
                "quaternionMaxComponent": _max_delta(local_after_q, unity_next_q),
            },
        },
        "conclusion": (
            "If pcmInput/contactBuffer are within their recorded numeric windows but nextPcmConsumer diverges, "
            "the first remaining producer is the dynamic-dynamic consume/writeback/integrate step, not A entrance or PCM generation."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "pcmInput": report["comparison"]["pcmInput"],
        "contactBuffer": {
            key: report["comparison"]["contactBuffer"][key]
            for key in ("countDelta", "maxPointComponent", "maxNormalComponent", "maxSeparation")
        },
        "nextPcmConsumer": report["comparison"]["nextPcmConsumer"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
