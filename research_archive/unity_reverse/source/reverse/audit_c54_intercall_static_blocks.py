#!/usr/bin/env python3
"""Align C54 Unity static batches with local interleaved stone--ice blocks."""

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
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--start-frame",
        type=int,
        default=0,
        help="First Unity C04 frame to join to local trace frame zero (default: 0).",
    )
    parser.add_argument(
        "--max-frames",
        type=int,
        default=None,
        help="Optional earliest C04 frame count to compare; use when the local trace was intentionally retained for a shorter window.",
    )
    parser.add_argument(
        "--swap-local-descriptors",
        action="store_true",
        help="Join Unity static descriptor 0/1 to local 1/0 when the pair body ordering is reversed.",
    )
    return parser.parse_args()


def decoder() -> Any:
    path = ROOT / "tools/reverse/extract_physx_native_solver_state.py"
    spec = importlib.util.spec_from_file_location("c54_decoder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def frames(events: Path) -> list[dict[str, Any]]:
    rows = []
    for line in events.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event.get("type") == "c04.dynamic_solver_frame":
            rows.append(event["data"])
    return sorted(rows, key=lambda row: int(row["frameIndex"]))


def decode(decoder_module: Any, solve: dict[str, Any], phase: str) -> tuple[dict[str, Any], dict[str, Any]]:
    desc = solve[phase]["descs"][0]
    value = decoder_module.decode_solver_contact_block(desc["constraintWindow"])
    if not isinstance(value, dict):
        raise RuntimeError("cannot decode static constraint")
    return desc, value


def delta(local: list[float], unity: list[float]) -> dict[str, Any]:
    values = [float(left) - float(right) for left, right in zip(local, unity)]
    return {"components": values, "maxAbs": max((abs(value) for value in values), default=0.0)}


def unity_body(desc: dict[str, Any], name: str) -> dict[str, list[float]]:
    values = desc[name]["f32Preview"]
    return {"linear": [float(value) for value in values[:3]], "angular": [float(value) for value in values[4:7]]}


def local_body(row: dict[str, Any], name: str, phase: str) -> dict[str, list[float]]:
    value = row[f"body_{name}_{phase}"]
    return {"linear": list(value["linear_velocity"]), "angular": list(value["angular_state"])}


def normal(decoded: dict[str, Any]) -> list[float]:
    count = int((decoded.get("header") or {}).get("numNormalConstr", 0))
    return [float(value) for value in (decoded.get("appliedNormalForces") or [])[:count]]


def friction(decoded: dict[str, Any]) -> list[float]:
    return [float(row["appliedForce"]) for row in decoded.get("frictionRows") or []]


def compare_phase(unity_desc: dict[str, Any], unity: dict[str, Any], local: dict[str, Any], phase: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for local_name, unity_name in (("a", "bodyAWindow"), ("b", "bodyBWindow")):
        result[f"body{local_name.upper()}"] = {
            key: delta(local_body(local, local_name, phase)[key], unity_body(unity_desc, unity_name)[key])
            for key in ("linear", "angular")
        }
    count = len(normal(unity))
    result["normalForce"] = delta(list(local[f"applied_normal_forces_{phase}"])[:count], normal(unity))
    result["frictionForce"] = delta(list(local[f"applied_friction_forces_{phase}"]), friction(unity))
    return result


def max_difference(row: dict[str, Any]) -> tuple[float, str, float]:
    maximum, path, signed = 0.0, "", 0.0
    for phase in ("before", "after"):
        for field, value in row[phase].items():
            if field.startswith("body"):
                for vector, diff in value.items():
                    if diff["maxAbs"] > maximum:
                        maximum = diff["maxAbs"]
                        index = max(range(len(diff["components"])), key=lambda item: abs(diff["components"][item]))
                        path, signed = f"{phase}.{field}.{vector}[{index}]", diff["components"][index]
            elif value["maxAbs"] > maximum:
                maximum = value["maxAbs"]
                index = max(range(len(value["components"])), key=lambda item: abs(value["components"][item]))
                path, signed = f"{phase}.{field}[{index}]", value["components"][index]
    return maximum, path, signed


def main() -> int:
    args = parse_args()
    decode_module = decoder()
    unity_frames = frames(args.events)
    if not unity_frames:
        raise RuntimeError(
            "no c04.dynamic_solver_frame events: capture ended before the collision solver window; "
            "this is not a zero-difference result"
        )
    if args.start_frame < 0:
        raise RuntimeError("--start-frame must be non-negative")
    unity_frames = [row for row in unity_frames if int(row["frameIndex"]) >= args.start_frame]
    if args.max_frames is not None:
        if args.max_frames <= 0:
            raise RuntimeError("--max-frames must be positive")
        unity_frames = unity_frames[:args.max_frames]
    loaded_local = json.loads(args.local.read_text(encoding="utf-8"))
    # Historical C54 reports place traces under ``hybrid``.  The targeted P6
    # collector intentionally writes the same arrays at the document root so
    # its capture cannot inherit any Unity state.  Accept both schemas.
    local_doc = loaded_local.get("hybrid") if isinstance(loaded_local, dict) else None
    if not isinstance(local_doc, dict):
        local_doc = loaded_local
    if not isinstance(local_doc, dict) or not isinstance(local_doc.get("solveBlockTrace"), list):
        raise RuntimeError("local report has no solveBlockTrace")
    local = local_doc["solveBlockTrace"]
    rows: list[dict[str, Any]] = []
    for local_frame_index, frame in enumerate(unity_frames):
        index = int(frame["frameIndex"])
        static_calls = frame.get("staticSolves") or []
        if len(static_calls) != 5:
            raise RuntimeError(f"frame {index}: expected five static regular calls, got {len(static_calls)}")
        # A C04 regular iteration is dynamic pair, active--ice, target--ice.
        block_window = local[local_frame_index * 15:(local_frame_index + 1) * 15]
        if len(block_window) != 15:
            raise RuntimeError(f"frame {index}: local interleaved block window missing")
        for iteration, static_call in enumerate(static_calls):
            for descriptor_index in range(2):
                local_descriptor_index = 1 - descriptor_index if args.swap_local_descriptors else descriptor_index
                local_block = block_window[iteration * 3 + 1 + local_descriptor_index]
                if local_block.get("constraint_type") != 5 or int(local_block.get("descriptor_index", -1)) != local_descriptor_index:
                    raise RuntimeError(f"frame {index} iteration {iteration}: static descriptor order mismatch")
                synthetic = {phase: {"descs": [static_call[phase]["descs"][descriptor_index]]} for phase in ("before", "after")}
                before_desc, before = decode(decode_module, synthetic, "before")
                after_desc, after = decode(decode_module, synthetic, "after")
                comparison = {
                    "frame": index,
                    "regularIteration": iteration,
                    "descriptorIndex": descriptor_index,
                    "localSequence": local_block["sequence"],
                    "before": compare_phase(before_desc, before, local_block, "before"),
                    "after": compare_phase(after_desc, after, local_block, "after"),
                }
                maximum, path, signed = max_difference(comparison)
                comparison["maxAbs"] = maximum
                comparison["maxField"] = path
                comparison["localMinusUnityAtMax"] = signed
                rows.append(comparison)
    first = next((row for row in rows if row["maxAbs"] >= 1.0e-6), None)
    result = {
        "schema": "c54_intercall_static_blocks_v1",
        "scope": "read-only C54 comparison; Unity static regular batches are joined to local interleaved active/target--ice solver blocks by frame, iteration and descriptor order",
        "artifacts": {"events": str(args.events), "local": str(args.local), "startFrame": args.start_frame, "swapLocalDescriptors": args.swap_local_descriptors},
        "rows": rows,
        "firstDifferenceAtOrAbove1e-6": (
            None if first is None else {key: first[key] for key in ("frame", "regularIteration", "descriptorIndex", "localSequence", "maxAbs", "maxField", "localMinusUnityAtMax")}
        ),
        "maxAbs": max((row["maxAbs"] for row in rows), default=0.0),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "rows": len(rows), "maxAbs": result["maxAbs"], "first": result["firstDifferenceAtOrAbove1e-6"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
