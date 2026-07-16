#!/usr/bin/env python3
"""Verify the controlled friction-manifest replay fixture.

This audit deliberately treats Unity's global Random.InitState as insufficient:
it checks the per-DCP-friction manifest consumption, then compares two fresh
browser runs at their exposed physics boundaries.  Pointer-valued/raw solver
bytes are reported but never mistaken for physics disagreement.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


CORE_FIELDS = ("p", "q", "linearVelocity", "angularVelocity")
UNITY_NATIVE_ORIGIN_X = -64.37740020751953
UNITY_NATIVE_ORIGIN_Z = 56.525001525878906


def read_events(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def events_of(events: list[dict[str, Any]], event_type: str) -> list[dict[str, Any]]:
    return [event["data"] for event in events if event.get("type") == event_type]


def core_frame(frame: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {"frameIndex": frame["frameIndex"]}
    for edge in ("entryCores", "exitCores"):
        result[edge] = [
            {field: core["decodedCandidate"].get(field) for field in CORE_FIELDS}
            for core in frame[edge]
        ]
    return result


def without_pointers(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: without_pointers(item)
            for key, item in value.items()
            if key not in {"ptr", "solverContextPtr", "constraint", "writeBack", "bodyA", "bodyB"}
        }
    if isinstance(value, list):
        return [without_pointers(item) for item in value]
    return value


def raw_difference_positions(left: list[int], right: list[int]) -> list[int]:
    return [index for index, (a, b) in enumerate(zip(left, right)) if a != b]


def read_sample(path: Path) -> dict[str, Any]:
    return json.loads(next(line for line in path.read_text(encoding="utf-8").splitlines() if line))


def max_local_c04_error(local_audit: dict[str, Any]) -> float:
    comparison = local_audit.get("comparison")
    if isinstance(comparison, dict):
        local_audit = comparison
    maximum = 0.0
    for frame in local_audit.get("c04Window") or []:
        for stone_name in ("active", "target"):
            for field in ("p", "q", "v", "w"):
                maximum = max(maximum, float(frame[stone_name][field]["maxAbs"]))
    return maximum


def native_to_protocol_xy(native_p: list[float]) -> list[float]:
    return [
        UNITY_NATIVE_ORIGIN_Z - float(native_p[2]),
        UNITY_NATIVE_ORIGIN_X - float(native_p[0]),
    ]


def endpoint_error(local_xy: list[float], unity_xy: list[float]) -> dict[str, Any]:
    dx = local_xy[0] - unity_xy[0]
    dy = local_xy[1] - unity_xy[1]
    return {
        "localXY": local_xy,
        "unityXY": unity_xy,
        "deltaM": [dx, dy],
        "distanceM": math.hypot(dx, dy),
        "distanceMm": math.hypot(dx, dy) * 1000.0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events-a", type=Path, required=True)
    parser.add_argument("--events-b", type=Path, required=True)
    parser.add_argument("--sample-a", type=Path, required=True)
    parser.add_argument("--sample-b", type=Path, required=True)
    parser.add_argument("--local-audit", type=Path, required=True)
    parser.add_argument("--settle-audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    events_a, events_b = read_events(args.events_a), read_events(args.events_b)
    frames_a = events_of(events_a, "c04.dynamic_solver_frame")
    frames_b = events_of(events_b, "c04.dynamic_solver_frame")
    c26_a = events_of(events_a, "c26.target_static_frame")
    c26_b = events_of(events_b, "c26.target_static_frame")
    if len(c26_a) != 1 or len(c26_b) != 1:
        raise ValueError("expected exactly one C26 selected-frame event in each manifest run")
    static_a = c26_a[0]["staticWritebacks"]
    static_b = c26_b[0]["staticWritebacks"]
    if len(static_a) != 1 or len(static_b) != 1:
        raise ValueError("expected exactly one static writeback in each C26 event")

    raw_report: dict[str, Any] = {}
    for phase in ("before", "after"):
        left_rows = static_a[0][phase]
        right_rows = static_b[0][phase]
        raw_report[phase] = []
        for left, right in zip(left_rows, right_rows):
            left_raw = left["constraintWindow"]["rawBytes"]
            right_raw = right["constraintWindow"]["rawBytes"]
            diffs = raw_difference_positions(left_raw, right_raw)
            raw_report[phase].append({
                "constraintLengthOver16": left["desc"]["constraintLengthOver16"],
                "byteLength": len(left_raw),
                "rawExact": left_raw == right_raw,
                "rawDifferenceCount": len(diffs),
                "rawFirstDifferencePositions": diffs[:24],
            })

    local_audit = json.loads(args.local_audit.read_text(encoding="utf-8"))
    settle_audit = json.loads(args.settle_audit.read_text(encoding="utf-8"))
    sample_a, sample_b = read_sample(args.sample_a), read_sample(args.sample_b)
    manifest_status = []
    for name, events in (("a", events_a), ("b", events_b)):
        applied = events_of(events, "rng.friction_manifest_applied")
        last = events_of(events, "rng.friction_manifest_last_draw")
        exhausted = events_of(events, "rng.friction_manifest_exhausted")
        manifest_status.append({
            "run": name,
            "applied": len(applied) == 1,
            "drawCount": applied[0]["drawCount"] if applied else None,
            "fullyConsumed": len(last) == 1,
            "exhausted": bool(exhausted),
        })

    normalized_frames_a = [core_frame(frame) for frame in frames_a]
    normalized_frames_b = [core_frame(frame) for frame in frames_b]
    static_body_exact = {
        phase: without_pointers(static_a[0]["bodyData" + phase.title()])
        == without_pointers(static_b[0]["bodyData" + phase.title()])
        for phase in ("before", "after")
    }
    local_max = max_local_c04_error(local_audit)
    endpoint_exact = {
        "active": sample_a["final_xy"] == sample_b["final_xy"],
        "target": [sample_a["target_moves"][0]["after_x"], sample_a["target_moves"][0]["after_y"]]
        == [sample_b["target_moves"][0]["after_x"], sample_b["target_moves"][0]["after_y"]],
    }
    settle_comparison = settle_audit.get("comparison")
    if isinstance(settle_comparison, dict):
        settle_audit = settle_comparison
    settle_final = (settle_audit.get("settleTail") or {}).get("final") or []
    if len(settle_final) < 2:
        raise ValueError("settle audit does not contain active and target final native poses")
    settle_endpoint = {
        "active": endpoint_error(native_to_protocol_xy(settle_final[0]["p"]), sample_a["final_xy"]),
        "target": endpoint_error(
            native_to_protocol_xy(settle_final[1]["p"]),
            [sample_a["target_moves"][0]["after_x"], sample_a["target_moves"][0]["after_y"]],
        ),
    }
    report = {
        "schema": "c36_manifest_replay_audit_v1",
        "scope": "Fresh-browser fixed DCP-friction-manifest replay; raw pointer/tail bytes are reported separately from decoded physics fields.",
        "inputs": {key: str(getattr(args, key)) for key in ("events_a", "events_b", "sample_a", "sample_b", "local_audit", "settle_audit")},
        "manifest": manifest_status,
        "unityFreshRunAgreement": {
            "endpointExact": endpoint_exact,
            "c04FrameCount": [len(normalized_frames_a), len(normalized_frames_b)],
            "c04CoreExact": normalized_frames_a == normalized_frames_b,
            "c26FrameIndex": [c26_a[0]["frameIndex"], c26_b[0]["frameIndex"]],
            "c26StaticBodyPhysicsExact": static_body_exact,
            "c26RawConstraintBytes": raw_report,
        },
        "localAgainstUnity": {
            "c04MaxAbsError": local_max,
            "ulpScalePass": local_max <= 2.0e-6,
            "note": "This compares decoded P/Q/v/w only; it does not claim allocator pointers or uninitialized solver tail bytes are deterministic.",
        },
        "localPostContactSettle": {
            "settled": bool((settle_audit.get("settleTail") or {}).get("settled")),
            "steps": (settle_audit.get("settleTail") or {}).get("steps"),
            "endpoint": settle_endpoint,
            "millimeterPass": all(item["distanceM"] <= 0.001 for item in settle_endpoint.values()),
        },
        "verdict": {
            "manifestFixtureStrict": all(
                item["applied"] and item["fullyConsumed"] and not item["exhausted"]
                for item in manifest_status
            ) and all(endpoint_exact.values()) and normalized_frames_a == normalized_frames_b,
            "c31StaticFirstDifferenceClosed": local_max <= 2.0e-6,
            "postContactEndpointMillimeterPass": all(
                item["distanceM"] <= 0.001 for item in settle_endpoint.values()
            ),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report["verdict"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
