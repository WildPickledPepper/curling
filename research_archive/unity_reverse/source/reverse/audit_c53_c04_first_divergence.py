#!/usr/bin/env python3
"""Audit the first C04 dynamic-pair solver split without changing production state.

The C04 runtime hook records the native pair descriptor for five regular solver
iterations plus one writeback.  The local diagnostic trace records the same
pair interleaved with the two stone--ice blocks.  This tool aligns those two
views for one frame and reports the first non-zero observable difference.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--local", type=Path, required=True)
    parser.add_argument("--frame", type=int, required=True)
    parser.add_argument(
        "--local-frame",
        type=int,
        help="Optional local trace frame index; defaults to --frame for historical multi-frame reports.",
    )
    parser.add_argument(
        "--swap-local-bodies",
        action="store_true",
        help="Match local A/B trace roles to Unity B/A when their finalizer descriptors are reversed.",
    )
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def load_decoder() -> Any:
    path = ROOT / "tools/reverse/extract_physx_native_solver_state.py"
    spec = importlib.util.spec_from_file_location("c53_decoder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def c04_frame(events: Path, frame: int) -> dict[str, Any]:
    for line in events.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event.get("type") == "c04.dynamic_solver_frame" and int(event["data"].get("frameIndex", -1)) == frame:
            return event["data"]
    raise RuntimeError(f"C04 frame {frame} is absent from {events}")


def decode_pair(decoder: Any, solve: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    before_desc = solve["before"]["descs"][0]
    after_desc = solve["after"]["descs"][0]
    before = decoder.decode_solver_contact_block(before_desc["constraintWindow"])
    after = decoder.decode_solver_contact_block(after_desc["constraintWindow"])
    if not isinstance(before, dict) or not isinstance(after, dict):
        raise RuntimeError("failed to decode C04 native contact block")
    return before_desc, after_desc, before, after


def max_abs(values: list[float]) -> float:
    return max((abs(float(value)) for value in values), default=0.0)


def delta(local: list[float], unity: list[float]) -> dict[str, Any]:
    values = [float(left) - float(right) for left, right in zip(local, unity)]
    return {"components": values, "maxAbs": max_abs(values)}


def unity_body(desc: dict[str, Any], body: str) -> dict[str, list[float]]:
    values = desc[body]["f32Preview"]
    return {"linear": [float(value) for value in values[:3]], "angular": [float(value) for value in values[4:7]]}


def local_body(row: dict[str, Any], body: str, phase: str) -> dict[str, list[float]]:
    values = row[f"body_{body}_{phase}"]
    return {"linear": list(values["linear_velocity"]), "angular": list(values["angular_state"])}


def normal_forces(decoded: dict[str, Any]) -> list[float]:
    count = int((decoded.get("header") or {}).get("numNormalConstr", 0))
    return [float(value) for value in (decoded.get("appliedNormalForces") or [])[:count]]


def friction_forces(decoded: dict[str, Any]) -> list[float]:
    return [float(row["appliedForce"]) for row in decoded.get("frictionRows") or []]


def exact_rows(unity: list[dict[str, Any]], local: list[dict[str, Any]], names: dict[str, str]) -> dict[str, Any]:
    result: dict[str, Any] = {"sameCount": len(unity) == len(local), "exact": len(unity) == len(local), "firstDifference": None}
    for index, (unity_row, local_row) in enumerate(zip(unity, local)):
        for unity_name, local_name in names.items():
            left, right = unity_row.get(unity_name), local_row.get(local_name)
            if left != right:
                result["exact"] = False
                if result["firstDifference"] is None:
                    difference: dict[str, Any] = {"row": index, "field": unity_name}
                    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                        difference["localMinusUnity"] = float(right) - float(left)
                    else:
                        difference["unity"] = left
                        difference["local"] = right
                    result["firstDifference"] = difference
    return result


def phase_row(
    desc: dict[str, Any], decoded: dict[str, Any], local: dict[str, Any], phase: str, *, swap_local_bodies: bool,
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for body in ("a", "b"):
        unity = unity_body(desc, "bodyAWindow" if body == "a" else "bodyBWindow")
        local_body_values = local_body(local, ("b" if body == "a" else "a") if swap_local_bodies else body, phase)
        result[f"body{body.upper()}"] = {
            "linearDelta": delta(local_body_values["linear"], unity["linear"]),
            "angularDelta": delta(local_body_values["angular"], unity["angular"]),
        }
    count = len(normal_forces(decoded))
    result["normalForceDelta"] = delta(list(local[f"applied_normal_forces_{phase}"])[:count], normal_forces(decoded))
    result["frictionForceDelta"] = delta(list(local[f"applied_friction_forces_{phase}"]), friction_forces(decoded))
    return result


def prepared_local_rows(rows: list[dict[str, Any]], *, kind: str, swap_local_bodies: bool) -> list[dict[str, Any]]:
    if not swap_local_bodies:
        return rows
    result: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        if kind == "normal":
            # Swapping the solver descriptor bodies also reverses the contact
            # normal.  ``r x n`` therefore swaps *and* changes sign.
            item["ra_x_n"] = [-float(value) for value in row["rb_x_n"]]
            item["rb_x_n"] = [-float(value) for value in row["ra_x_n"]]
        elif kind == "friction":
            item["normal"] = [-float(value) for value in row["normal"]]
            item["ra_x_n"] = [-float(value) for value in row["rb_x_n"]]
            item["rb_x_n"] = [-float(value) for value in row["ra_x_n"]]
        result.append(item)
    return result


def first_difference(iterations: list[dict[str, Any]], writeback: dict[str, Any]) -> dict[str, Any] | None:
    return first_difference_at_or_above(iterations, writeback, 0.0)


def first_difference_at_or_above(iterations: list[dict[str, Any]], writeback: dict[str, Any], threshold: float) -> dict[str, Any] | None:
    for row in iterations + [{"regularIteration": "writeback", **writeback}]:
        for phase in ("before", "after"):
            for field, value in row[phase].items():
                if field.startswith("body"):
                    for vector, diff in value.items():
                        if diff["maxAbs"] >= threshold and diff["maxAbs"] > 0.0:
                            component = next(index for index, item in enumerate(diff["components"]) if abs(item) >= threshold and item != 0.0)
                            return {"iteration": row["regularIteration"], "phase": phase, "field": f"{field}.{vector}[{component}]", "localMinusUnity": diff["components"][component]}
                elif value["maxAbs"] >= threshold and value["maxAbs"] > 0.0:
                    component = next(index for index, item in enumerate(value["components"]) if abs(item) >= threshold and item != 0.0)
                    return {"iteration": row["regularIteration"], "phase": phase, "field": f"{field}[{component}]", "localMinusUnity": value["components"][component]}
    return None


def main() -> int:
    args = parse_args()
    local_frame = args.frame if args.local_frame is None else args.local_frame
    decoder = load_decoder()
    unity = c04_frame(args.events, args.frame)
    loaded_local = json.loads(args.local.read_text(encoding="utf-8"))
    # Historical C03 reports nest traces under ``hybrid``.  Targeted P6
    # captures deliberately keep the same three trace arrays at top level so
    # no Unity state can be injected by the collector.
    local_doc = loaded_local.get("hybrid") if isinstance(loaded_local, dict) else None
    if not isinstance(local_doc, dict):
        local_doc = loaded_local
    pair_blocks = [
        row for row in local_doc["solveBlockTrace"]
        if row.get("constraint_type") == 1
    ]
    start = local_frame * 5
    local_regular = pair_blocks[start:start + 5]
    if len(unity.get("dynamicSolves") or []) != 5 or len(local_regular) != 5:
        raise RuntimeError(f"frame {args.frame}: expected five regular pair solves, got unity={len(unity.get('dynamicSolves') or [])}, local={len(local_regular)}")
    if len(unity.get("dynamicWritebacks") or []) != 1 or len(local_doc["solveWritebackTrace"]) <= local_frame:
        raise RuntimeError(f"frame {args.frame}: missing pair writeback")

    first_desc, _after_desc, first_before, _after = decode_pair(decoder, unity["dynamicSolves"][0])
    prepared = local_doc["finalizerTrace"][local_frame]
    prepared_rows = {
        "normal": exact_rows(first_before["normalRows"], prepared_local_rows(prepared["normal_rows"], kind="normal", swap_local_bodies=args.swap_local_bodies), {"raXn": "ra_x_n", "rbXn": "rb_x_n", "velMultiplier": "vel_multiplier", "biasedErr": "biased_err", "unbiasedErr": "unbiased_err", "maxImpulse": "max_impulse"}),
        "friction": exact_rows(first_before["frictionRows"], prepared_local_rows(prepared["friction_rows"], kind="friction", swap_local_bodies=args.swap_local_bodies), {"normal": "normal", "appliedForce": "applied_force", "raXn": "ra_x_n", "velMultiplier": "vel_multiplier", "rbXn": "rb_x_n", "bias": "bias", "targetVel": "target_velocity"}),
        "descriptor": first_desc["desc"],
    }

    iterations: list[dict[str, Any]] = []
    for index, (unity_solve, local_solve) in enumerate(zip(unity["dynamicSolves"], local_regular)):
        before_desc, after_desc, before, after = decode_pair(decoder, unity_solve)
        iterations.append({"regularIteration": index, "localSequence": local_solve["sequence"], "before": phase_row(before_desc, before, local_solve, "before", swap_local_bodies=args.swap_local_bodies), "after": phase_row(after_desc, after, local_solve, "after", swap_local_bodies=args.swap_local_bodies)})

    writeback_solve = unity["dynamicWritebacks"][0]
    wb_before_desc, wb_after_desc, wb_before, wb_after = decode_pair(decoder, writeback_solve)
    local_wb = local_doc["solveWritebackTrace"][local_frame]
    writeback = {"before": phase_row(wb_before_desc, wb_before, local_wb, "before", swap_local_bodies=args.swap_local_bodies), "after": phase_row(wb_after_desc, wb_after, local_wb, "after", swap_local_bodies=args.swap_local_bodies)}
    result = {
        "schema": "c53_c04_first_divergence_v1",
        "scope": "read-only diagnostic; aligns captured Unity C04 pair solver state with local diagnostic trace and does not modify production simulation",
        "artifacts": {"events": str(args.events), "local": str(args.local), "frame": args.frame, "localFrame": local_frame, "swapLocalBodies": args.swap_local_bodies},
        "preparedRows": prepared_rows,
        "regularIterations": iterations,
        "writeback": writeback,
        "firstCapturedDifference": first_difference(iterations, writeback),
        "firstDifferenceAtOrAbove": {
            "1e-6": first_difference_at_or_above(iterations, writeback, 1.0e-6),
            "1e-4": first_difference_at_or_above(iterations, writeback, 1.0e-4),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "prepared": {key: value["exact"] for key, value in prepared_rows.items() if isinstance(value, dict) and "exact" in value}, "first": result["firstCapturedDifference"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
