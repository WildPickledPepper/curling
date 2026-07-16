#!/usr/bin/env python3
"""Compare a local P6 first-contact frame with a targeted Unity C03/C04 frame.

The audit is read-only.  It does not inject Unity state into the local Scene:
it merely compares the local ``beforeScene/afterScene`` records already
emitted by ``audit_hybrid_p6_endpoint_sixshot.py`` with Unity's first actual
stone--stone solver consume boundary.  C04 starts at the first selected
dynamic island frame, which can precede the first PCM-consuming solve by a
tick; when present, C03's manager-validated ``coresBeforeSolve`` and
``coresAfterSolverSetup`` are therefore authoritative.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def native_state(local: dict[str, Any]) -> dict[str, list[float]]:
    # Local state serializes the quaternion as w,x,y,z; the C04 decoder emits
    # the native PhysX x,y,z,w order.
    q_wxyz = [float(value) for value in local["quaternionWxyz"]]
    return {
        "p": [float(value) for value in local["physxPosition"]],
        "v": [float(value) for value in local["physxLinearVelocity"]],
        "w": [float(value) for value in local["physxAngularVelocity"]],
        "q": [q_wxyz[1], q_wxyz[2], q_wxyz[3], q_wxyz[0]],
    }


def unity_state(core: dict[str, Any]) -> dict[str, list[float]]:
    decoded = core.get("decodedCandidate") or {}
    return {
        "p": [float(value) for value in decoded["p"]],
        "v": [float(value) for value in decoded["linearVelocity"]],
        "w": [float(value) for value in decoded["angularVelocity"]],
        "q": [float(value) for value in decoded["q"]],
    }


def euclidean(left: list[float], right: list[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(left, right)))


def compare(local: dict[str, Any], unity: dict[str, Any]) -> dict[str, Any]:
    left = native_state(local)
    right = unity_state(unity)
    result: dict[str, Any] = {}
    for key in ("p", "v", "w", "q"):
        # q and -q represent the same orientation.  Do not turn a native
        # representation sign flip into a fictitious two-unit quaternion
        # error in a first-divergence audit.
        if key == "q" and sum(a * b for a, b in zip(left[key], right[key])) < 0.0:
            right[key] = [-value for value in right[key]]
        delta = [a - b for a, b in zip(left[key], right[key])]
        result[key] = {"local": left[key], "unity": right[key], "localMinusUnity": delta, "norm": euclidean(left[key], right[key])}
    return result


def match_core(local: dict[str, Any], cores: list[dict[str, Any]]) -> dict[str, Any]:
    position = native_state(local)["p"]
    return min(cores, key=lambda core: euclidean(position, unity_state(core)["p"]))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", type=Path, required=True, help="P6 endpoint audit with firstContactEntrance fields.")
    parser.add_argument("--events", type=Path, required=True, help="Matching Unity events.jsonl containing C04 frames.")
    parser.add_argument("--label", required=True, help="Exact sample label to compare.")
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = json.loads(args.audit.read_text(encoding="utf-8"))
    row = next((item for item in audit.get("rows", []) if item.get("label") == args.label), None)
    if row is None:
        raise ValueError(f"label not found in audit: {args.label}")
    entrance = row.get("firstContactEntrance") or {}
    active_before = entrance.get("active")
    active_after = entrance.get("afterScene")
    targets_before = entrance.get("targets") or {}
    targets_after = entrance.get("targetsAfterScene") or {}
    if not active_before or not active_after or len(targets_before) != 1 or len(targets_after) != 1:
        raise ValueError("audit does not contain a complete single-target first-contact frame")

    events = load_jsonl(args.events)
    c03 = [event.get("data") or {} for event in events if event.get("type") == "c03.first_dynamic_writeback"]
    if c03:
        frame = c03[0]
        manager = frame.get("manager") or {}
        entry = manager.get("coresBeforeSolve") or []
        exit_ = manager.get("coresAfterSolverSetup") or []
        boundary = "c03.first_dynamic_writeback"
        if len(entry) < 2 or len(exit_) < 2:
            raise ValueError("C03 first dynamic writeback lacks both dynamic cores")
    else:
        c04 = [event.get("data") or {} for event in events if event.get("type") == "c04.dynamic_solver_frame"]
        if not c04:
            raise ValueError("no C03 or C04 frames in events")
        frame = min(c04, key=lambda item: int(item.get("frameIndex") or 0))
        entry = frame.get("entryCores") or []
        exit_ = frame.get("exitCores") or []
        boundary = "c04.dynamic_solver_frame_fallback"
        if len(entry) < 2 or len(exit_) < 2:
            raise ValueError("first C04 frame lacks both dynamic cores")

    target_key = next(iter(targets_before))
    target_before = targets_before[target_key]
    target_after = targets_after[target_key]
    report = {
        "schema": "c03_c04_local_first_contact_v2",
        "policy": "read-only comparison; no Unity state is injected into local replay",
        "label": args.label,
        "unityBoundary": boundary,
        "c04FrameIndex": frame.get("frameIndex"),
        "c04TickSerial": frame.get("tickSerial"),
        "active": {
            "entry": compare(active_before, match_core(active_before, entry)),
            "exit": compare(active_after, match_core(active_after, exit_)),
        },
        "target": {
            "entry": compare(target_before, match_core(target_before, entry)),
            "exit": compare(target_after, match_core(target_after, exit_)),
        },
        "endpointErrorM": row.get("endpointErrorM"),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "label": args.label, "endpointErrorM": row.get("endpointErrorM")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
