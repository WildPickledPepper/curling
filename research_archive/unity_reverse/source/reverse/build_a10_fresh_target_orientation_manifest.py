#!/usr/bin/env python3
"""Build a strict yaw manifest from A10 release-pose runtime evidence.

Use only for a fresh Unity session where every target stone is unique and has
not taken part in an earlier shot.  In that narrowly defined design its target
yaw is the factory identity (zero); the repeatedly used active stones receive
their observed A10 native-bridge yaw before each BESTSHOT.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def _rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _yaw_from_quaternion(quaternion: list[float]) -> float:
    if len(quaternion) != 4:
        raise ValueError(f"A10 quaternion must have four components, got {quaternion!r}")
    yaw = 2.0 * math.atan2(float(quaternion[1]), float(quaternion[3]))
    return (yaw + math.pi) % (2.0 * math.pi) - math.pi


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=Path, required=True)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--fresh-unique-targets",
        action="store_true",
        help="Required safety gate: authorize zero target yaw only for fresh, never-before-used unique targets.",
    )
    args = parser.parse_args()
    if not args.fresh_unique_targets:
        raise SystemExit("Refusing to infer target yaw: pass --fresh-unique-targets only for a verified fresh/unique-target session.")

    samples = _rows(args.samples)
    events = _rows(args.events)
    a10 = [event["data"] for event in events if event.get("type") == "a10.release_reset_orientation"]
    if len(a10) != len(samples):
        raise SystemExit(f"A10 release count {len(a10)} does not equal sample count {len(samples)}")

    target_indices: list[int] = []
    output_rows: dict[str, dict[str, Any]] = {}
    for sample, observed in zip(samples, a10, strict=True):
        active_index = int(sample["active_shot_num"])
        targets = [int(index) for index in sample["target_indices"]]
        if not targets:
            raise SystemExit(f"sample {sample.get('sample_id')}: no collision target")
        bridge = observed.get("bridgePoseBeforeAngularSetter") or {}
        transform = bridge.get("transform") if isinstance(bridge, dict) else None
        quaternion = transform.get("q") if isinstance(transform, dict) else None
        if not isinstance(quaternion, list):
            raise SystemExit(f"sample {sample.get('sample_id')}: A10 bridge pose/quaternion missing")
        active_yaw = _yaw_from_quaternion(quaternion)
        yaws = {str(active_index): active_yaw, **{str(index): 0.0 for index in targets}}
        output_rows[str(sample["sample_id"])] = {
            "activeYaw": active_yaw,
            "yaws": yaws,
            "a10": {
                "bridgeRootOffset": bridge.get("rootOffset"),
                "bridgeTransformOffset": bridge.get("offset"),
                "nativeQuaternion": quaternion,
            },
        }
        target_indices.extend(targets)

    if len(set(target_indices)) != len(target_indices):
        raise SystemExit("Target indices are reused; this manifest must not assume zero target yaw.")
    payload = {
        "evidence": {
            "active": "A10 native bridge pose before first angular setter of each BESTSHOT",
            "target": "fresh Unity session with unique never-before-used targets; factory yaw identity (0 rad)",
            "sourceSamples": str(args.samples),
            "sourceEvents": str(args.events),
        },
        "samples": output_rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "sampleCount": len(output_rows)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
