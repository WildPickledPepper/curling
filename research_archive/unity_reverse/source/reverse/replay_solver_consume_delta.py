#!/usr/bin/env python3
"""Replay single-pair PhysX patch-friction solver rows from captured Unity bytes.

This script consumes the compact report produced by
``extract_physx_native_solver_state.py``. It takes the captured
``solveContact*`` before/after body windows and the raw decoded
``SolverContactHeader/Point/Friction`` rows, then replays the wasm/PhysX
single-pair solver formula offline.
"""

from __future__ import annotations

import argparse
import json
import math
import struct
from collections import Counter
from pathlib import Path
from typing import Any


def f32(value: float) -> float:
    return struct.unpack("<f", struct.pack("<f", float(value)))[0]


def as_float(value: Any) -> float | None:
    if isinstance(value, (int, float)) and math.isfinite(value):
        return float(value)
    return None


def vec3(values: Any, start: int = 0) -> list[float] | None:
    if not isinstance(values, list) or len(values) < start + 3:
        return None
    out = [as_float(values[start + index]) for index in range(3)]
    return out if all(value is not None for value in out) else None  # type: ignore[return-value]


def body_state(dump: dict[str, Any], prefix: str) -> dict[str, list[float]] | None:
    values = dump.get(f"{prefix}F32Preview")
    lin = vec3(values, 0)
    ang = vec3(values, 4)
    if lin is None or ang is None:
        return None
    return {"lin": lin, "ang": ang}


def clone_state(state: dict[str, list[float]]) -> dict[str, list[float]]:
    return {"lin": list(state["lin"]), "ang": list(state["ang"])}


def dot(a: list[float], b: list[float], use_f32: bool) -> float:
    if use_f32:
        return f32(f32(f32(a[0] * b[0]) + f32(a[1] * b[1])) + f32(a[2] * b[2]))
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def add_scaled(dst: list[float], src: list[float], scale: float, sign: float, use_f32: bool) -> None:
    for index in range(3):
        value = dst[index] + sign * src[index] * scale
        dst[index] = f32(value) if use_f32 else value


def clamp(value: float, lo: float, hi: float) -> float:
    return min(max(value, lo), hi)


def solve_dynamic(
    header: dict[str, Any],
    normal_rows: list[dict[str, Any]],
    force_buffer: list[float],
    friction_rows: list[dict[str, Any]],
    body_a: dict[str, list[float]],
    body_b: dict[str, list[float]],
    use_f32: bool,
) -> dict[str, Any]:
    normal = vec3(header.get("normal"), 0)
    if normal is None:
        raise ValueError("missing header normal")
    inv_mass0 = float(header.get("invMass0") or 0.0)
    inv_mass1 = float(header.get("invMass1") or 0.0)
    ang_dom0 = float(header.get("angDom0") or 0.0)
    ang_dom1 = float(header.get("angDom1") or 0.0)
    static_friction = float(header.get("staticFriction") or 0.0)
    dynamic_friction = float(header.get("dynamicFriction") or static_friction)

    if use_f32:
        normal = [f32(v) for v in normal]
        inv_mass0 = f32(inv_mass0)
        inv_mass1 = f32(inv_mass1)
        ang_dom0 = f32(ang_dom0)
        ang_dom1 = f32(ang_dom1)
        static_friction = f32(static_friction)
        dynamic_friction = f32(dynamic_friction)

    normal_impulse_sum = 0.0
    normal_trace = []
    for index, row in enumerate(normal_rows):
        old = force_buffer[index] if index < len(force_buffer) else 0.0
        ra = vec3(row.get("raXn"), 0)
        rb = vec3(row.get("rbXn"), 0)
        if ra is None or rb is None:
            continue
        vel_multiplier = float(row.get("velMultiplier") or 0.0)
        biased_err = float(row.get("biasedErr") or 0.0)
        max_impulse = float(row.get("maxImpulse") or 0.0)
        if use_f32:
            old = f32(old)
            ra = [f32(v) for v in ra]
            rb = [f32(v) for v in rb]
            vel_multiplier = f32(vel_multiplier)
            biased_err = f32(biased_err)
            max_impulse = f32(max_impulse)

        normal_vel = dot(normal, body_a["lin"], use_f32)
        normal_vel = normal_vel + dot(ra, body_a["ang"], use_f32)
        normal_vel = normal_vel - dot(normal, body_b["lin"], use_f32)
        normal_vel = normal_vel - dot(rb, body_b["ang"], use_f32)
        normal_vel = f32(normal_vel) if use_f32 else normal_vel

        candidate_delta = biased_err - vel_multiplier * normal_vel
        if use_f32:
            candidate_delta = f32(candidate_delta)
        delta = max(candidate_delta, -old)
        new_force = min(old + delta, max_impulse)
        delta = new_force - old
        if use_f32:
            new_force = f32(new_force)
            delta = f32(delta)

        add_scaled(body_a["lin"], normal, inv_mass0 * delta, +1.0, use_f32)
        add_scaled(body_b["lin"], normal, inv_mass1 * delta, -1.0, use_f32)
        add_scaled(body_a["ang"], ra, ang_dom0 * delta, +1.0, use_f32)
        add_scaled(body_b["ang"], rb, ang_dom1 * delta, -1.0, use_f32)
        if index < len(force_buffer):
            force_buffer[index] = new_force
        normal_impulse_sum += new_force
        if use_f32:
            normal_impulse_sum = f32(normal_impulse_sum)
        normal_trace.append(
            {
                "index": index,
                "normalVel": normal_vel,
                "oldForce": old,
                "newForce": new_force,
                "delta": delta,
            }
        )

    friction_trace = []
    static_limit = static_friction * normal_impulse_sum
    dynamic_limit = dynamic_friction * normal_impulse_sum
    if use_f32:
        static_limit = f32(static_limit)
        dynamic_limit = f32(dynamic_limit)

    for index, row in enumerate(friction_rows):
        tangent = vec3(row.get("normal"), 0)
        ra = vec3(row.get("raXn"), 0)
        rb = vec3(row.get("rbXn"), 0)
        if tangent is None or ra is None or rb is None:
            continue
        old = float(row.get("appliedForce") or 0.0)
        vel_multiplier = float(row.get("velMultiplier") or 0.0)
        bias = float(row.get("bias") or 0.0)
        target_vel = float(row.get("targetVel") or 0.0)
        if use_f32:
            tangent = [f32(v) for v in tangent]
            ra = [f32(v) for v in ra]
            rb = [f32(v) for v in rb]
            old = f32(old)
            vel_multiplier = f32(vel_multiplier)
            bias = f32(bias)
            target_vel = f32(target_vel)

        tangent_vel = dot(tangent, body_a["lin"], use_f32)
        tangent_vel = tangent_vel + dot(ra, body_a["ang"], use_f32)
        tangent_vel = tangent_vel - dot(tangent, body_b["lin"], use_f32)
        tangent_vel = tangent_vel - dot(rb, body_b["ang"], use_f32)
        tangent_vel = f32(tangent_vel) if use_f32 else tangent_vel

        candidate = old - vel_multiplier * (bias - target_vel) - vel_multiplier * tangent_vel
        if use_f32:
            candidate = f32(candidate)
        if abs(candidate) > static_limit:
            new_force = clamp(candidate, -dynamic_limit, dynamic_limit)
        else:
            new_force = candidate
        delta = new_force - old
        if use_f32:
            new_force = f32(new_force)
            delta = f32(delta)

        add_scaled(body_a["lin"], tangent, inv_mass0 * delta, +1.0, use_f32)
        add_scaled(body_b["lin"], tangent, inv_mass1 * delta, -1.0, use_f32)
        add_scaled(body_a["ang"], ra, ang_dom0 * delta, +1.0, use_f32)
        add_scaled(body_b["ang"], rb, ang_dom1 * delta, -1.0, use_f32)
        friction_trace.append(
            {
                "index": index,
                "tangentVel": tangent_vel,
                "oldForce": old,
                "newForce": new_force,
                "delta": delta,
            }
        )

    return {
        "bodyA": body_a,
        "bodyB": body_b,
        "normalImpulseSum": normal_impulse_sum,
        "normalTrace": normal_trace,
        "frictionTrace": friction_trace,
    }


def solve_static(
    header: dict[str, Any],
    normal_rows: list[dict[str, Any]],
    force_buffer: list[float],
    friction_rows: list[dict[str, Any]],
    body_a: dict[str, list[float]],
    use_f32: bool,
) -> dict[str, Any]:
    dummy_b = {"lin": [0.0, 0.0, 0.0], "ang": [0.0, 0.0, 0.0]}
    dynamic_header = dict(header)
    dynamic_header["invMass1"] = 0.0
    dynamic_header["angDom1"] = 0.0
    return solve_dynamic(
        dynamic_header,
        normal_rows,
        force_buffer,
        friction_rows,
        body_a,
        dummy_b,
        use_f32,
    )


def max_state_error(predicted: dict[str, list[float]], actual: dict[str, list[float]]) -> dict[str, Any]:
    rows = []
    max_abs = 0.0
    for group in ("lin", "ang"):
        for index in range(3):
            delta = predicted[group][index] - actual[group][index]
            max_abs = max(max_abs, abs(delta))
            rows.append(
                {
                    "field": f"{group}[{index}]",
                    "predicted": predicted[group][index],
                    "actual": actual[group][index],
                    "delta": delta,
                }
            )
    return {"maxAbs": max_abs, "fields": rows}


def first_dump(row: dict[str, Any]) -> dict[str, Any]:
    dumps = row.get("extraConstraintDumps")
    return dumps[0] if isinstance(dumps, list) and dumps and isinstance(dumps[0], dict) else {}


def pair_rows(rows: list[dict[str, Any]]) -> dict[tuple[str, int, int], dict[str, dict[str, Any]]]:
    pairs: dict[tuple[str, int, int], dict[str, dict[str, Any]]] = {}
    for row in rows:
        key = (
            str(row.get("hook")),
            int(row.get("callIndex") or -1),
            int(row.get("armSerial") or -1),
        )
        pairs.setdefault(key, {})[str(row.get("phase"))] = row
    return pairs


def replay_pair(key: tuple[str, int, int], before: dict[str, Any], after: dict[str, Any], use_f32: bool) -> dict[str, Any] | None:
    before_dump = first_dump(before)
    after_dump = first_dump(after)
    decoded = before_dump.get("decodedConstraint")
    if not isinstance(decoded, dict):
        return None
    header = decoded.get("header")
    normal_rows = decoded.get("normalRows")
    friction_rows = decoded.get("frictionRows")
    forces = decoded.get("appliedNormalForces")
    if not (isinstance(header, dict) and isinstance(normal_rows, list) and isinstance(friction_rows, list) and isinstance(forces, list)):
        return None
    body_a_before = body_state(before_dump, "bodyA")
    body_a_after = body_state(after_dump, "bodyA")
    if body_a_before is None or body_a_after is None:
        return None
    force_buffer = [float(value) if as_float(value) is not None else 0.0 for value in forces]
    if use_f32:
        force_buffer = [f32(value) for value in force_buffer]

    hook = key[0]
    dynamic = "BStatic" not in hook and "Static" not in hook
    body_b_before = body_state(before_dump, "bodyB")
    body_b_after = body_state(after_dump, "bodyB")
    if dynamic:
        if body_b_before is None or body_b_after is None:
            return None
        replay = solve_dynamic(
            header,
            normal_rows,
            force_buffer,
            friction_rows,
            clone_state(body_a_before),
            clone_state(body_b_before),
            use_f32,
        )
        body_b_error = max_state_error(replay["bodyB"], body_b_after)
    else:
        replay = solve_static(
            header,
            normal_rows,
            force_buffer,
            friction_rows,
            clone_state(body_a_before),
            use_f32,
        )
        body_b_error = None

    body_a_error = max_state_error(replay["bodyA"], body_a_after)
    return {
        "hook": hook,
        "callIndex": key[1],
        "armSerial": key[2],
        "tBefore": before.get("t"),
        "tAfter": after.get("t"),
        "dynamic": dynamic,
        "header": header,
        "normalForceBefore": decoded.get("appliedNormalForces"),
        "normalTrace": replay.get("normalTrace"),
        "frictionTrace": replay.get("frictionTrace"),
        "normalImpulseSum": replay.get("normalImpulseSum"),
        "bodyAError": body_a_error,
        "bodyBError": body_b_error,
        "bodyAPredicted": replay["bodyA"],
        "bodyAActual": body_a_after,
        "bodyBPredicted": replay.get("bodyB"),
        "bodyBActual": body_b_after,
    }


def replay_report(path: Path, use_f32: bool) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    pairs = pair_rows([row for row in data.get("solverConsumeRows") or [] if isinstance(row, dict)])
    rows = []
    skipped = Counter()
    for key, phases in pairs.items():
        if "before" not in phases or "after" not in phases:
            skipped["missing_phase"] += 1
            continue
        row = replay_pair(key, phases["before"], phases["after"], use_f32)
        if row is None:
            skipped["unreplayable"] += 1
            continue
        rows.append(row)

    def row_error(row: dict[str, Any]) -> float:
        values = [row["bodyAError"]["maxAbs"]]
        if isinstance(row.get("bodyBError"), dict):
            values.append(row["bodyBError"]["maxAbs"])
        return max(values)

    top = sorted(rows, key=row_error, reverse=True)[:20]
    return {
        "input": str(path),
        "useF32": use_f32,
        "replayedCount": len(rows),
        "skipped": dict(sorted(skipped.items())),
        "maxErrorByHook": {
            hook: max(row_error(row) for row in rows if row["hook"] == hook)
            for hook in sorted({row["hook"] for row in rows})
        },
        "topErrors": top,
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("solver_state_json", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--float64", action="store_true", help="Disable f32 rounding after scalar operations.")
    parser.add_argument("--top", type=int, default=8)
    args = parser.parse_args()

    report = replay_report(args.solver_state_json, use_f32=not args.float64)
    print(
        json.dumps(
            {
                "input": report["input"],
                "useF32": report["useF32"],
                "replayedCount": report["replayedCount"],
                "skipped": report["skipped"],
                "maxErrorByHook": report["maxErrorByHook"],
                "topErrors": report["topErrors"][: args.top],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
