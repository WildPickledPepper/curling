#!/usr/bin/env python3
"""Compare C11's fully captured dynamic solver tail against the local replay."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LOCAL = ROOT / "data/calibration/c11_c04_solver_tail_friction0_14000_20260712.json"
DEFAULT_OUTPUT = ROOT / "data/calibration/c11_solver_tail_audit_14000_20260712.json"
DEFAULT_LOG_ROOT = ROOT / "log/c11_solver_tail_20260712"


def load_decoder() -> Any:
    path = ROOT / "tools/reverse/extract_physx_native_solver_state.py"
    spec = importlib.util.spec_from_file_location("c11_decoder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def event_path() -> Path:
    runs = sorted(path for path in DEFAULT_LOG_ROOT.iterdir() if path.is_dir())
    if len(runs) != 1:
        raise RuntimeError(f"expected one C11 probe run, found {len(runs)}")
    return runs[0] / "events.jsonl"


def delta(left: list[float], right: list[float]) -> dict[str, Any]:
    values = [float(a) - float(b) for a, b in zip(left, right)]
    return {"components": values, "maxAbs": max((abs(value) for value in values), default=0.0)}


def unity_body(desc: dict[str, Any], key: str) -> dict[str, list[float]]:
    values = desc[key]["f32Preview"]
    return {"linear": [float(value) for value in values[:3]], "angular": [float(value) for value in values[4:7]]}


def local_body(row: dict[str, Any], key: str) -> dict[str, list[float]]:
    values = row[key]
    return {"linear": list(values["linear_velocity"]), "angular": list(values["angular_state"])}


def decode_pair(decoder: Any, solve: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    before_desc = solve["before"]["descs"][0]
    after_desc = solve["after"]["descs"][0]
    before = decoder.decode_solver_contact_block(before_desc["constraintWindow"])
    after = decoder.decode_solver_contact_block(after_desc["constraintWindow"])
    if not isinstance(before, dict) or not isinstance(after, dict):
        raise RuntimeError("failed to decode solver constraint")
    return before_desc, after_desc, before, after


def force_prefix(decoded: dict[str, Any]) -> list[float]:
    count = int((decoded.get("header") or {}).get("numNormalConstr", 0))
    return list(decoded.get("appliedNormalForces") or [])[:count]


def friction_forces(decoded: dict[str, Any]) -> list[float]:
    return [float(row["appliedForce"]) for row in decoded.get("frictionRows") or []]


def rows_exact(unity_rows: list[dict[str, Any]], local_rows: list[dict[str, Any]], names: dict[str, str]) -> bool:
    if len(unity_rows) != len(local_rows):
        return False
    for unity, local in zip(unity_rows, local_rows):
        for unity_name, local_name in names.items():
            if unity.get(unity_name) != local.get(local_name):
                return False
    return True


def main() -> int:
    decoder = load_decoder()
    events = event_path()
    local = json.loads(DEFAULT_LOCAL.read_text(encoding="utf-8"))["hybrid"]
    unity_frame: dict[str, Any] | None = None
    for line in events.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event.get("type") == "c04.dynamic_solver_frame" and event["data"].get("frameIndex") == 1:
            unity_frame = event["data"]
            break
    if unity_frame is None:
        raise RuntimeError("C11 frame 1 not found")

    regular = unity_frame["dynamicSolves"]
    local_regular = local["solveBlockTrace"][5:10]
    if len(regular) != 5 or len(local_regular) != 5:
        raise RuntimeError("C11 did not retain five regular solver iterations")
    if len(unity_frame["dynamicWritebacks"]) != 1 or len(local["solveWritebackTrace"]) < 2:
        raise RuntimeError("C11 final writeback coverage is incomplete")

    _, _, first_before, _ = decode_pair(decoder, regular[0])
    prepared = local["finalizerTrace"][1]
    prepared_normal_exact = rows_exact(
        first_before["normalRows"],
        prepared["normal_rows"],
        {
            "raXn": "ra_x_n",
            "rbXn": "rb_x_n",
            "velMultiplier": "vel_multiplier",
            "biasedErr": "biased_err",
            "unbiasedErr": "unbiased_err",
            "maxImpulse": "max_impulse",
        },
    )
    prepared_friction_exact = rows_exact(
        first_before["frictionRows"],
        prepared["friction_rows"],
        {
            "normal": "normal",
            "appliedForce": "applied_force",
            "raXn": "ra_x_n",
            "velMultiplier": "vel_multiplier",
            "rbXn": "rb_x_n",
            "bias": "bias",
            "targetVel": "target_velocity",
        },
    )

    rows: list[dict[str, Any]] = []
    first_field_difference: dict[str, Any] | None = None
    for index, (unity_solve, local_solve) in enumerate(zip(regular, local_regular)):
        before_desc, after_desc, before, after = decode_pair(decoder, unity_solve)
        phases: dict[str, Any] = {}
        for phase, desc, decoded, local_key in (
            ("before", before_desc, before, "before"),
            ("after", after_desc, after, "after"),
        ):
            unity_a = unity_body(desc, "bodyAWindow")
            unity_b = unity_body(desc, "bodyBWindow")
            local_a = local_body(local_solve, "body_a_" + local_key)
            local_b = local_body(local_solve, "body_b_" + local_key)
            normal_count = len(force_prefix(decoded))
            local_normal = list(local_solve["applied_normal_forces_" + local_key])[:normal_count]
            local_friction = list(local_solve["applied_friction_forces_" + local_key])
            phase_row = {
                "normalForcesUnity": force_prefix(decoded),
                "normalForcesLocal": local_normal,
                "normalForceDelta": delta(local_normal, force_prefix(decoded)),
                "frictionForcesUnity": friction_forces(decoded),
                "frictionForcesLocal": local_friction,
                "frictionForceDelta": delta(local_friction, friction_forces(decoded)),
                "bodyA": {
                    "linearDelta": delta(local_a["linear"], unity_a["linear"]),
                    "angularDelta": delta(local_a["angular"], unity_a["angular"]),
                },
                "bodyB": {
                    "linearDelta": delta(local_b["linear"], unity_b["linear"]),
                    "angularDelta": delta(local_b["angular"], unity_b["angular"]),
                },
            }
            phases[phase] = phase_row
            if first_field_difference is None:
                for body_name in ("bodyA", "bodyB"):
                    for component_name in ("linearDelta", "angularDelta"):
                        values = phase_row[body_name][component_name]["components"]
                        for component, value in enumerate(values):
                            if value != 0.0:
                                first_field_difference = {
                                    "regularIteration": index,
                                    "phase": phase,
                                    "field": f"{body_name}.{component_name[:-5]}[{component}]",
                                    "localMinusUnity": value,
                                }
                                break
                        if first_field_difference is not None:
                            break
                    if first_field_difference is not None:
                        break
        rows.append({"regularIteration": index, "localSequence": local_solve["sequence"], **phases})

    unity_wb = unity_frame["dynamicWritebacks"][0]
    wb_before_desc, wb_after_desc, wb_before, wb_after = decode_pair(decoder, unity_wb)
    local_wb = local["solveWritebackTrace"][1]
    writeback: dict[str, Any] = {}
    for phase, desc, decoded, local_key in (
        ("before", wb_before_desc, wb_before, "before"),
        ("after", wb_after_desc, wb_after, "after"),
    ):
        unity_a = unity_body(desc, "bodyAWindow")
        unity_b = unity_body(desc, "bodyBWindow")
        local_a = local_body(local_wb, "body_a_" + local_key)
        local_b = local_body(local_wb, "body_b_" + local_key)
        normal_count = len(force_prefix(decoded))
        local_normal = list(local_wb["applied_normal_forces_" + local_key])[:normal_count]
        local_friction = list(local_wb["applied_friction_forces_" + local_key])
        writeback[phase] = {
            "normalForcesUnity": force_prefix(decoded),
            "normalForcesLocal": local_normal,
            "normalForceDelta": delta(local_normal, force_prefix(decoded)),
            "frictionForcesUnity": friction_forces(decoded),
            "frictionForcesLocal": local_friction,
            "frictionForceDelta": delta(local_friction, friction_forces(decoded)),
            "bodyA": {
                "linearDelta": delta(local_a["linear"], unity_a["linear"]),
                "angularDelta": delta(local_a["angular"], unity_a["angular"]),
            },
            "bodyB": {
                "linearDelta": delta(local_b["linear"], unity_b["linear"]),
                "angularDelta": delta(local_b["angular"], unity_b["angular"]),
            },
        }

    result = {
        "schema": "c11-solver-tail-audit-v1",
        "boundary": "14000 C11 frame-1 dynamic solver, five regular iterations plus final writeback",
        "singleVariable": "read-only local friction-force trace added after Unity C11 capture",
        "expectedDiscriminator": "find the first differing native force/state field after exact prepared rows and normal forces",
        "scope": "same C11 Unity run and oracle local replay only; not a production fix",
        "artifacts": {"unityEvents": str(events), "localReplay": str(DEFAULT_LOCAL)},
        "preparedRows": {
            "normalExact": prepared_normal_exact,
            "frictionExact": prepared_friction_exact,
        },
        "regularIterations": rows,
        "writeback": writeback,
        "firstCapturedSolverStateDifference": first_field_difference,
        "conclusion": (
            "The prepared rows and normal-force accumulation do not explain the split: regular iteration 0 starts "
            "with zero solver bodies and equal normal force, then target PxSolverBody.linearVelocity.y differs after "
            "that call. The second friction applied-force becomes observably different later, at regular iteration 3. "
            "This is a state-propagation observation, not yet a permission to alter friction or solver code."
        ),
    }
    DEFAULT_OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(DEFAULT_OUTPUT),
        "first": first_field_difference,
        "regular3FrictionAfter": rows[3]["after"]["frictionForceDelta"],
        "writebackFrictionAfter": writeback["after"]["frictionForceDelta"],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
