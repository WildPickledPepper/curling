#!/usr/bin/env python3
"""Decode one Unity stone-stone solver writeback from existing native dumps.

This is deliberately a field decoder, not a parameter-fitting script.  The
finalize hook identifies one concrete ``PxSolverConstraintDesc``; the
with-writeback hook is joined only when constraint pointer, shape interaction
and both solver-body pointers agree.  ``PxSolverBody`` stores solver deltas,
while ``PxSolverBodyData`` stores the incoming physical velocities.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "calibration" / "front_half_pcm_solver_state_20260710.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_solver_writeback_14000_audit_20260710.json"


def _vec3(values: Iterable[Any], offset: int = 0) -> list[float]:
    rows = list(values)
    if len(rows) < offset + 3:
        raise ValueError("solver-body preview is shorter than PxSolverBody")
    return [float(rows[offset + index]) for index in range(3)]


def _solver_body(preview: list[Any]) -> dict[str, list[float]]:
    # PhysX 4.1 PxSolverBody: linearVelocity @ f32[0:3], padding/progress @
    # f32[3], angularState @ f32[4:7].  See solver/PxSolverDefs.h.
    return {
        "linearDelta": _vec3(preview, 0),
        "angularState": _vec3(preview, 4),
    }


def _mat_vec(matrix: dict[str, Any], vector: list[float]) -> list[float]:
    columns = [
        [float(item) for item in matrix[f"column{index}"]]
        for index in range(3)
    ]
    return [
        sum(columns[column][row] * vector[column] for column in range(3))
        for row in range(3)
    ]


def _add(left: list[float], right: list[float]) -> list[float]:
    return [float(left[index]) + float(right[index]) for index in range(3)]


def _sub(left: list[float], right: list[float]) -> list[float]:
    return [float(left[index]) - float(right[index]) for index in range(3)]


def _body_output(data: dict[str, Any], solver: dict[str, list[float]]) -> dict[str, list[float]]:
    angular_delta = _mat_vec(data["sqrtInvInertia"], solver["angularState"])
    return {
        "incomingLinearVelocity": [float(item) for item in data["linearVelocity"]],
        "incomingAngularVelocity": [float(item) for item in data["angularVelocity"]],
        "solverLinearDelta": solver["linearDelta"],
        "solverAngularState": solver["angularState"],
        "solverAngularVelocityDelta": angular_delta,
        "writtenLinearVelocity": _add(data["linearVelocity"], solver["linearDelta"]),
        "writtenAngularVelocity": _add(data["angularVelocity"], angular_delta),
    }


def _entry_key(row: dict[str, Any], entry: dict[str, Any]) -> tuple[int, int]:
    return (int(row["callIndex"]), int(entry["index"]))


def audit(document: dict[str, Any]) -> dict[str, Any]:
    first = document["firstStoneStone"]
    desc = first["contactDesc"]
    body_pair = {int(desc["body0"]), int(desc["body1"])}
    shape_interaction = int(desc["shapeInteraction"])

    finalized = []
    for entry in first.get("extraConstraintDumps") or []:
        header = (entry.get("decodedConstraint") or {}).get("header") or {}
        native_desc = entry.get("desc") or {}
        if int(header.get("shapeInteraction") or 0) != shape_interaction:
            continue
        if int(native_desc.get("bodyA") or 0) not in body_pair:
            continue
        if int(native_desc.get("bodyB") or 0) not in body_pair:
            continue
        finalized.append({
            "index": int(entry["index"]),
            "constraint": int(native_desc["constraint"]),
            "shapeInteraction": int(header["shapeInteraction"]),
        })
    if len(finalized) != 1:
        raise ValueError(f"expected exactly one first stone-stone finalized constraint, got {finalized}")
    finalized_constraint = finalized[0]

    paired: dict[tuple[int, int], dict[str, dict[str, Any]]] = {}
    for row in document.get("solverConsumeRows") or []:
        if row.get("hook") != "solveContactBlockWithWriteback":
            continue
        phase = row.get("phase")
        if phase not in {"before", "after"}:
            continue
        for entry in row.get("extraConstraintDumps") or []:
            native_desc = entry.get("desc") or {}
            header = (entry.get("decodedConstraint") or {}).get("header") or {}
            if int(native_desc.get("constraint") or 0) != finalized_constraint["constraint"]:
                continue
            if int(header.get("shapeInteraction") or 0) != shape_interaction:
                continue
            if {int(native_desc.get("bodyA") or 0), int(native_desc.get("bodyB") or 0)} != body_pair:
                continue
            paired.setdefault(_entry_key(row, entry), {})[str(phase)] = {
                "t": float(row["t"]),
                "desc": native_desc,
                "header": header,
                "bodyA": _solver_body(entry.get("bodyAF32Preview") or []),
                "bodyB": _solver_body(entry.get("bodyBF32Preview") or []),
                "appliedNormalForces": [
                    float(value)
                    for value in ((entry.get("decodedConstraint") or {}).get("appliedNormalForces") or [])
                ],
            }

    complete = [
        (key, phases["before"], phases["after"])
        for key, phases in paired.items()
        if "before" in phases and "after" in phases
    ]
    complete = [row for row in complete if row[1]["t"] >= float(first["t"])]
    if not complete:
        raise ValueError("no with-writeback pair follows the first stone-stone finalize event")
    # Constraint buffers are recycled in later contact ticks. The first consume
    # after this exact finalize event is the only pair belonging to this solve.
    (call_index, desc_index), before, after = min(
        complete,
        key=lambda row: (float(row[1]["t"]), int(row[0][0]), int(row[0][1])),
    )

    data0 = first["solverBodyData"]["data0"]
    data1 = first["solverBodyData"]["data1"]
    body_a_is_data0 = int(after["desc"]["bodyA"]) == int(desc["body0"])
    after_data_a, after_data_b = (data0, data1) if body_a_is_data0 else (data1, data0)
    before_data_a, before_data_b = (data0, data1) if body_a_is_data0 else (data1, data0)

    roles = {
        "bodyA": {
            "solverBefore": before["bodyA"],
            "solverAfter": after["bodyA"],
            "constraintOnlyLinearDelta": _sub(after["bodyA"]["linearDelta"], before["bodyA"]["linearDelta"]),
            "constraintOnlyAngularStateDelta": _sub(after["bodyA"]["angularState"], before["bodyA"]["angularState"]),
            "written": _body_output(after_data_a, after["bodyA"]),
        },
        "bodyB": {
            "solverBefore": before["bodyB"],
            "solverAfter": after["bodyB"],
            "constraintOnlyLinearDelta": _sub(after["bodyB"]["linearDelta"], before["bodyB"]["linearDelta"]),
            "constraintOnlyAngularStateDelta": _sub(after["bodyB"]["angularState"], before["bodyB"]["angularState"]),
            "written": _body_output(after_data_b, after["bodyB"]),
        },
    }
    return {
        "schema": "unity_solver_writeback_audit_v1",
        "purpose": "Decode the exact Unity first stone-stone solver writeback without parameter fitting.",
        "input": str(DEFAULT_INPUT.relative_to(PROJECT_ROOT)),
        "join": {
            "body0": int(desc["body0"]),
            "body1": int(desc["body1"]),
            "shapeInteraction": shape_interaction,
            "finalizedConstraint": finalized_constraint,
            "withWritebackHook": "solveContactBlockWithWriteback",
            "callIndex": call_index,
            "solverDescIndex": desc_index,
            "beforeTimestamp": before["t"],
            "afterTimestamp": after["t"],
        },
        "contact": {
            "count": int(desc["numContacts"]),
            "normal": after["header"].get("normal"),
            "normalForcesBefore": before["appliedNormalForces"],
            "normalForcesAfter": after["appliedNormalForces"],
        },
        "roles": roles,
        "limitations": [
            "This decodes the precise single constraint writeback only.",
            "A later audit must compare these fields with local scalar Scene state at the same solver boundary.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    document = json.loads(args.input.read_text(encoding="utf-8"))
    result = audit(document)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "join": result["join"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
