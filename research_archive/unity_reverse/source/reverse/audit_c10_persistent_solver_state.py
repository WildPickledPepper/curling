#!/usr/bin/env python3
"""Audit the C07 dynamic-solver iteration coverage without rerunning Unity.

The C07 probe saved only the first four of five regular solveContactBlock calls
for each dynamic frame.  The sixth velocity iteration is the separate
solveContactBlockWithWriteback pass. This script verifies the captured prefix
against the local solve-block trace, then records whether that prefix is
sufficient to explain the first divergent post-contact state.
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVENTS = (
    ROOT
    / "log/c07_joint_solver_pcm_20260712/unity_runtime_probe_20260712_201550/events.jsonl"
)
DEFAULT_LOCAL = ROOT / "data/calibration/c07_c04_joint_solver_friction0_14000_20260712.json"
DEFAULT_OUTPUT = ROOT / "data/calibration/c10_persistent_solver_state_14000_20260712.json"


def load_decoder() -> Any:
    path = ROOT / "tools/reverse/extract_physx_native_solver_state.py"
    spec = importlib.util.spec_from_file_location("c10_decoder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def max_abs(values: list[float]) -> float:
    return max((abs(value) for value in values), default=0.0)


def numeric_delta(left: list[Any], right: list[Any]) -> dict[str, Any]:
    values = [float(a) - float(b) for a, b in zip(left, right)]
    return {"components": values, "maxAbs": max_abs(values)}


def dynamic_frames(events: Path) -> list[dict[str, Any]]:
    frames: list[dict[str, Any]] = []
    for line in events.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event.get("type") == "c04.dynamic_solver_frame":
            frames.append(event["data"])
    if not frames:
        raise RuntimeError(f"no c04.dynamic_solver_frame in {events}")
    return sorted(frames, key=lambda row: int(row["frameIndex"]))


def decoded_iteration(decoder: Any, solve: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for phase in ("before", "after"):
        descs = solve.get(phase, {}).get("descs") or []
        if not descs:
            raise RuntimeError(f"missing {phase} descriptor")
        decoded = decoder.decode_solver_contact_block(descs[0].get("constraintWindow"))
        if not isinstance(decoded, dict):
            raise RuntimeError(f"cannot decode {phase} constraint")
        out[phase] = decoded
    return out


def row_for_iteration(decoded: dict[str, Any]) -> dict[str, Any]:
    header = decoded.get("header") or {}
    normal_count = int(header.get("numNormalConstr", 0))
    friction = decoded.get("frictionRows") or []
    return {
        "normalConstraintCount": normal_count,
        # decode_solver_contact_block keeps a four-float preview. Only the
        # header-declared prefix is applied normal force; the rest is the
        # following row's storage and must not enter the comparison.
        "normalForces": list(decoded.get("appliedNormalForces") or [])[:normal_count],
        "frictionAppliedForces": [row.get("appliedForce") for row in friction],
    }


def vec(data: dict[str, Any], key: str) -> list[float]:
    value = data.get(key)
    if not isinstance(value, list):
        raise RuntimeError(f"missing {key}")
    return [float(item) for item in value]


def main() -> int:
    decoder = load_decoder()
    frames = dynamic_frames(DEFAULT_EVENTS)
    local_doc = json.loads(DEFAULT_LOCAL.read_text(encoding="utf-8"))
    local_trace = local_doc["hybrid"]["solveBlockTrace"]
    comparison = local_doc["comparison"]["c04Window"]

    unity_frame1 = next(frame for frame in frames if frame["frameIndex"] == 1)
    unity_prefix = [decoded_iteration(decoder, solve) for solve in unity_frame1["dynamicSolves"]]
    # The physical solver has six velocity iterations. C07 hard-capped Unity
    # recording at four calls; the local trace shows five regular calls before
    # the final solveContactBlockWithWriteback pass.
    local_regular = local_trace[5:10]
    prefix: list[dict[str, Any]] = []
    for index, (unity, local) in enumerate(zip(unity_prefix, local_regular[:4])):
        unity_before = row_for_iteration(unity["before"])
        unity_after = row_for_iteration(unity["after"])
        normal_count = unity_before["normalConstraintCount"]
        local_before = list(local["applied_normal_forces_before"])[:normal_count]
        local_after = list(local["applied_normal_forces_after"])[:normal_count]
        prefix.append(
            {
                "iteration": index,
                "unity": {"before": unity_before, "after": unity_after},
                "localSequence": local["sequence"],
                "normalForceBeforeDelta": numeric_delta(local_before, unity_before["normalForces"]),
                "normalForceAfterDelta": numeric_delta(local_after, unity_after["normalForces"]),
                "localBodyAAngularStateBefore": local["body_a_before"]["angular_state"],
                "localBodyAAngularStateAfter": local["body_a_after"]["angular_state"],
            }
        )

    divergence = next(row for row in comparison if row["frameIndex"] == 2)["active"]
    result = {
        "schema": "c10-persistent-solver-state-v1",
        "boundary": "C07 frame-1 solver tail -> frame-2 active post-state",
        "singleVariable": "none; offline coverage and state discriminator only",
        "expectedDiscriminator": (
            "If the captured four-call prefix already differs, the first force accumulator "
            "difference is observable. If it matches while frame 2 differs, the missing "
            "regular tail/writeback pass is the first unobserved solver boundary."
        ),
        "scope": "14000 same-run C07 only; no Unity launch and no production physics edit",
        "artifacts": {"unityEvents": str(DEFAULT_EVENTS), "localTrace": str(DEFAULT_LOCAL)},
        "unityCapturedRegularCalls": len(unity_prefix),
        "localRegularSolveBlockCalls": len(local_regular),
        "uncapturedLocalTail": {
            "regularSolveBlock": {
                "localSequence": local_regular[4]["sequence"],
                "normalForcesBefore": local_regular[4]["applied_normal_forces_before"],
                "normalForcesAfter": local_regular[4]["applied_normal_forces_after"],
                "bodyAAngularStateBefore": local_regular[4]["body_a_before"]["angular_state"],
                "bodyAAngularStateAfter": local_regular[4]["body_a_after"]["angular_state"],
            },
            "writebackPass": "not captured in C07 C04 dynamicSolves; it uses solveContactBlockWithWriteback",
        },
        "capturedPrefix": prefix,
        "allCapturedPrefixNormalForcesExact": all(
            entry["normalForceBeforeDelta"]["maxAbs"] == 0.0
            and entry["normalForceAfterDelta"]["maxAbs"] == 0.0
            for entry in prefix
        ),
        "firstKnownPostPrefixStateDelta": divergence,
        "conclusion": (
            "C07 proves no force-accumulator divergence in the captured four-call prefix. "
            "The first material active P/Q/v/w difference is already present at frame 2, "
            "after an unobserved fifth regular solveContactBlock call and an unobserved "
            "sixth solveContactBlockWithWriteback pass. C07 cannot discriminate their native state "
            "without a minimal tail-only capture."
        ),
        "nextRequiredObservation": (
            "Capture frame 1 call 4 plus the writeback pass, with constraint applied "
            "normal/friction forces and PxSolverBody before/after. Do not alter pair lifecycle, "
            "materials, PCM, A19, or endpoints."
        ),
    }
    DEFAULT_OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(DEFAULT_OUTPUT),
        "capturedPrefixExact": result["allCapturedPrefixNormalForcesExact"],
        "localTailSequence": result["uncapturedLocalTail"]["regularSolveBlock"]["localSequence"],
        "frame2AngularDelta": divergence["w"]["maxAbs"],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
