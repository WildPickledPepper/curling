#!/usr/bin/env python3
"""Compare one C54 Unity static constraint before-solve with its local trace row."""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
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
        "--local-start-frame",
        type=int,
        default=0,
        help=(
            "Unity C04 frame corresponding to local solveBlockTrace element zero. "
            "Use this when a targeted local trace begins at a later Unity C04 frame."
        ),
    )
    parser.add_argument("--iteration", type=int, required=True)
    parser.add_argument("--descriptor", type=int, required=True)
    parser.add_argument(
        "--swap-local-descriptors",
        action="store_true",
        help="Read local static descriptor 1/0 for Unity descriptor 0/1 when their pair ordering is reversed.",
    )
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def decoder() -> Any:
    path = ROOT / "tools/reverse/extract_physx_native_solver_state.py"
    spec = importlib.util.spec_from_file_location("c54_static_constraint_decoder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def values(value: Any, path: str = "") -> list[tuple[str, float]]:
    if isinstance(value, bool):
        return [(path, float(value))]
    if isinstance(value, (int, float)):
        return [(path, float(value))]
    if isinstance(value, list):
        out: list[tuple[str, float]] = []
        for index, item in enumerate(value):
            out.extend(values(item, f"{path}[{index}]"))
        return out
    if isinstance(value, dict):
        out = []
        for key, item in value.items():
            if key in {"index", "ptr", "rawByteLength", "decodedBytes", "layout"}:
                continue
            out.extend(values(item, f"{path}.{key}" if path else key))
        return out
    return []


def main() -> int:
    args = parse_args()
    decode = decoder().decode_solver_contact_block
    events = [json.loads(line) for line in args.events.read_text(encoding="utf-8").splitlines()]
    frame = next(
        row["data"]
        for row in events
        if row.get("type") == "c04.dynamic_solver_frame" and int(row["data"]["frameIndex"]) == args.frame
    )
    unity_window = frame["staticSolves"][args.iteration]["before"]["descs"][args.descriptor]["constraintWindow"]
    unity = decode(unity_window)
    if not isinstance(unity, dict):
        raise RuntimeError("cannot decode Unity static constraint")
    loaded_local = json.loads(args.local.read_text(encoding="utf-8"))
    local_doc = loaded_local.get("hybrid") if isinstance(loaded_local, dict) else None
    if not isinstance(local_doc, dict):
        local_doc = loaded_local
    if not isinstance(local_doc, dict) or not isinstance(local_doc.get("solveBlockTrace"), list):
        raise RuntimeError("local report has no solveBlockTrace")
    trace = local_doc["solveBlockTrace"]
    # Trace position, not its diagnostic sequence number, encodes the C04
    # interleave: dynamic pair, active--ice, target--ice for each iteration.
    local_descriptor = 1 - args.descriptor if args.swap_local_descriptors else args.descriptor
    local_frame = args.frame - args.local_start_frame
    if local_frame < 0:
        raise ValueError("--frame must be greater than or equal to --local-start-frame")
    trace_index = local_frame * 15 + args.iteration * 3 + 1 + local_descriptor
    if trace_index >= len(trace):
        raise ValueError(
            f"local solveBlockTrace does not contain Unity frame {args.frame} "
            f"from local start frame {args.local_start_frame}"
        )
    local_row = trace[trace_index]
    # Unity runtime bytes are wasm32; the local trace is emitted by native
    # x64 pyphysx.  Their SolverContactHeader pointer fields have different
    # widths, so decode each side with its actual ABI.
    local = decode({"rawBytes": local_row["constraint_bytes_before"]}, pointer_bytes=8)
    if not isinstance(local, dict):
        raise RuntimeError("cannot decode local static constraint")
    left = dict(values(local))
    right = dict(values(unity))
    diffs = []
    for key in sorted(set(left) | set(right)):
        local_value, unity_value = left.get(key), right.get(key)
        if local_value is None or unity_value is None:
            continue
        if not (math.isfinite(local_value) and math.isfinite(unity_value)):
            continue
        diffs.append({"field": key, "local": local_value, "unity": unity_value, "localMinusUnity": local_value - unity_value})
    diffs.sort(key=lambda row: abs(float(row["localMinusUnity"])), reverse=True)
    result = {
        "schema": "c54_static_constraint_input_v1",
        "scope": "read-only semantic decode of one C54 static constraint before solve",
        "artifacts": {"events": str(args.events), "local": str(args.local)},
        "identity": {
            "frame": args.frame,
            "localStartFrame": args.local_start_frame,
            "regularIteration": args.iteration,
            "descriptorIndex": args.descriptor,
            "localDescriptorIndex": local_descriptor,
            "localTraceIndex": trace_index,
            "localSequence": local_row.get("sequence"),
        },
        "firstDifferingByte": next((
            {"offset": index, "local": left_byte, "unity": right_byte}
            for index, (left_byte, right_byte) in enumerate(zip(local_row["constraint_bytes_before"], unity_window["rawBytes"]))
            if left_byte != right_byte
        ), None),
        "topSemanticDifferences": diffs[:32],
        "maxAbs": abs(float(diffs[0]["localMinusUnity"])) if diffs else 0.0,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "firstByte": result["firstDifferingByte"], "top": diffs[:3]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
