#!/usr/bin/env python3
"""Audit persistent pyphysx MOTIONINFO -> first-contact replay against Unity."""

from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any, Sequence


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.reverse.front_half_pcm_replay import (  # noqa: E402
    event_shot_groups,
    friction_noises_after_motioninfo,
    load_jsonl,
)
from unity_front_half_physx import (  # noqa: E402
    DEFAULT_RUNTIME_FEATURE_EVENTS,
    PersistentPhysxFrontHalfScene,
)


DEFAULT_EVENTS = PROJECT_ROOT / "log" / "unity_runtime_probe_20260710_012403" / "events.jsonl"
DEFAULT_SUMMARY = (
    PROJECT_ROOT / "log" / "unity_runtime_probe_20260710_012403" / "front_half_pcm_summary.json"
)
DEFAULT_TRUTH = PROJECT_ROOT / "data" / "calibration" / "front_half_pcm_entrance_truth_20260710.json"
DEFAULT_OUTPUT = (
    PROJECT_ROOT / "data" / "calibration" / "persistent_scene_front_half_state_audit_20260710.json"
)


def _yaw_delta(actual: float, expected: float) -> float:
    delta = float(actual) - float(expected)
    while delta > math.pi:
        delta -= 2.0 * math.pi
    while delta <= -math.pi:
        delta += 2.0 * math.pi
    return delta


def _norm(values: Sequence[float]) -> float:
    return math.sqrt(sum(float(value) * float(value) for value in values))


def _vector_delta(left: Sequence[float], right: Sequence[float]) -> float:
    return _norm([float(a) - float(b) for a, b in zip(left, right)])


def _signless_vector_delta(left: Sequence[float], right: Sequence[float]) -> float:
    return min(
        _vector_delta(left, right),
        _vector_delta(left, [-float(value) for value in right]),
    )


def _summary(values: Sequence[float]) -> dict[str, Any]:
    rows = [float(value) for value in values]
    return {
        "count": len(rows),
        "rmse": math.sqrt(sum(value * value for value in rows) / len(rows)) if rows else None,
        "mean": sum(rows) / len(rows) if rows else None,
        "max": max(rows) if rows else None,
    }


def _position_error(local: dict[str, Any], unity: dict[str, Any]) -> dict[str, float]:
    dx = float(local["x"]) - float(unity["x"])
    dy = float(local["y"]) - float(unity["y"])
    return {"dx": dx, "dy": dy, "distance": math.hypot(dx, dy)}


def _contact_points(report: dict[str, Any]) -> list[dict[str, Any]]:
    points = report.get("points")
    return [point for point in points if isinstance(point, dict)] if isinstance(points, list) else []


def _unity_contacts(shot: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    after = shot.get("firstPcmWithContactsAfter") or {}
    before = shot.get("firstPcmWithContactsBefore") or {}
    contact_buffer = after.get("contactBuffer") if isinstance(after, dict) else {}
    contacts = (
        contact_buffer.get("contactsPreview")
        if isinstance(contact_buffer, dict)
        else []
    )
    transform1 = before.get("transform1") if isinstance(before, dict) else {}
    return (
        [contact for contact in contacts if isinstance(contact, dict)]
        if isinstance(contacts, list)
        else [],
        transform1 if isinstance(transform1, dict) else {},
    )


def _contact_field_diff(
    local_report: dict[str, Any],
    local_target: dict[str, Any],
    unity_contacts: list[dict[str, Any]],
    unity_target_transform: dict[str, Any],
) -> dict[str, Any]:
    local_points = _contact_points(local_report)
    unity_target_p = [float(value) for value in (unity_target_transform.get("p") or [0.0, 0.0, 0.0])]
    local_target_p = [float(value) for value in local_target["physxPosition"]]

    local_rows = []
    for point in local_points:
        position = [float(value) for value in point.get("position") or [0.0, 0.0, 0.0]]
        local_rows.append(
            {
                "normal": [float(value) for value in point.get("normal") or [0.0, 0.0, 0.0]],
                "separation": float(point.get("separation") or 0.0),
                "pointRelativeTarget": [position[i] - local_target_p[i] for i in range(3)],
            }
        )
    unity_rows = []
    for contact in unity_contacts:
        native_point = [float(value) for value in contact.get("point") or [0.0, 0.0, 0.0]]
        native_normal = [float(value) for value in contact.get("normal") or [0.0, 0.0, 0.0]]
        unity_rows.append(
            {
                "normal": [native_normal[0], native_normal[2], native_normal[1]],
                "separation": float(contact.get("separation") or 0.0),
                "pointRelativeTarget": [
                    native_point[0] - unity_target_p[0],
                    native_point[2] - unity_target_p[2],
                    native_point[1] - unity_target_p[1],
                ],
            }
        )

    pair_count = min(len(local_rows), len(unity_rows))
    best: tuple[float, list[dict[str, float]]] | None = None
    for order in itertools.permutations(range(len(unity_rows)), pair_count):
        pairs = []
        score = 0.0
        for local_index, unity_index in enumerate(order):
            local = local_rows[local_index]
            unity = unity_rows[unity_index]
            row = {
                "normalSignlessL2": _signless_vector_delta(local["normal"], unity["normal"]),
                "separationAbs": abs(local["separation"] - unity["separation"]),
                "pointRelativeTargetL2": _vector_delta(
                    local["pointRelativeTarget"], unity["pointRelativeTarget"]
                ),
            }
            score += sum(row.values())
            pairs.append(row)
        if best is None or score < best[0]:
            best = (score, pairs)

    return {
        "localCount": len(local_rows),
        "unityCount": len(unity_rows),
        "countMatch": len(local_rows) == len(unity_rows),
        "local": local_rows,
        "unity": unity_rows,
        "bestPairs": [] if best is None else best[1],
    }


def audit(
    truth: dict[str, Any],
    summary: dict[str, Any],
    event_groups: list[dict[str, Any]],
    *,
    runtime_feature_events: Path,
    runtime_feature_line: int,
    patch_runtime_features: bool,
    settle_steps: int,
    max_steps: int,
    start_source: str,
    boundary: str,
) -> dict[str, Any]:
    scene = PersistentPhysxFrontHalfScene(
        stone_count=2,
        runtime_feature_events=runtime_feature_events,
        runtime_feature_line=runtime_feature_line,
        patch_runtime_features=patch_runtime_features,
    )
    summary_shots = summary.get("shots") or []
    rows = []
    for seq, truth_row in enumerate(truth.get("rows") or []):
        if seq >= len(event_groups) or seq >= len(summary_shots):
            continue
        unity_active = truth_row["unity_entrance_state"]["active"]
        unity_target = truth_row["unity_entrance_state"]["target"]
        target_x = float(unity_target["x"])
        target_y = float(unity_target["y"])
        target_yaw = float(unity_target["yaw"])
        scene.reset_positions(
            [0.0, 0.0, target_x, target_y],
            yaw_overrides={1: target_yaw},
            settle_steps=settle_steps,
        )

        event_group = event_groups[seq]
        motion_event = event_group.get("motioninfo") or {}
        motioninfo = motion_event.get("values")
        if not isinstance(motioninfo, list):
            continue
        if start_source == "bestshot":
            start_values = [
                float(event_group["v0"]),
                float(event_group["h0"]),
                float(event_group["w0"]),
            ]
            run = (
                scene.run_bestshot_to_pcm_shell
                if boundary == "pcm-shell"
                else scene.run_bestshot_to_first_contact
            )
            replay = run(
                0,
                start_values,
                [float(item["noise"]) for item in event_group.get("friction") or []],
                target_indices=[1],
                yaw=0.0,
                max_steps=max_steps,
            )
        elif start_source == "motioninfo":
            start_values = motioninfo
            run = (
                scene.run_motioninfo_to_pcm_shell
                if boundary == "pcm-shell"
                else scene.run_motioninfo_to_first_contact
            )
            replay = run(
                0,
                motioninfo,
                friction_noises_after_motioninfo(event_group),
                target_indices=[1],
                yaw=0.0,
                max_steps=max_steps,
            )
        else:
            raise ValueError(f"unsupported start source: {start_source}")
        reached = bool(
            replay.get("reachedPcmShell")
            if boundary == "pcm-shell"
            else replay.get("reachedFirstContact")
        )
        row: dict[str, Any] = {
            "seq": seq,
            "sampleId": truth_row.get("sample_id"),
            "label": truth_row.get("label"),
            "startSource": start_source,
            "boundary": boundary,
            "startValues": start_values,
            "activeYawAtStart": 0.0,
            "targetYawInput": target_yaw,
            "motioninfo": motioninfo,
            "reachedBoundary": reached,
            "stepsAfterStart": replay.get("steps"),
        }
        if reached:
            if boundary == "pcm-shell":
                local_active = replay["entranceState"]
                local_target = replay["targetEntranceStates"]["1"]
                local_report = None
            else:
                local_active = replay["beforeScene"]
                local_target = replay["targetBeforeScene"]["1"]
                local_report = replay["firstContactReports"][0]
            unity_contacts, unity_target_transform = _unity_contacts(summary_shots[seq])
            native_solver = (
                truth_row.get("native_solver_velocity")
                if boundary == "local-contact"
                else None
            )
            velocity_delta = None
            if isinstance(native_solver, dict):
                velocity_delta = {
                    key: float(local_active[key]) - float(native_solver[key])
                    for key in ("vx", "vy", "w")
                    if native_solver.get(key) is not None
                }
            row.update(
                {
                    "localActiveEntrance": local_active,
                    "localTargetEntrance": local_target,
                    "unityActiveEntrance": unity_active,
                    "unityTargetEntrance": unity_target,
                    "activePositionError": _position_error(local_active, unity_active),
                    "targetPositionError": _position_error(local_target, unity_target),
                    "activeYawDelta": _yaw_delta(local_active["yaw"], unity_active["yaw"]),
                    "targetYawDelta": _yaw_delta(local_target["yaw"], unity_target["yaw"]),
                    "nativeSolverHorizontalVelocity": native_solver,
                    "velocityDeltaVsNativeSolver": velocity_delta,
                    "localAfterScene": replay["afterScene"],
                    "contact": None
                    if local_report is None
                    else _contact_field_diff(
                        local_report,
                        local_target,
                        unity_contacts,
                        unity_target_transform,
                    ),
                }
            )
            row["requiredHiddenYawAtStart"] = -float(row["activeYawDelta"])
        rows.append(row)

    reached = [row for row in rows if row.get("reachedBoundary")]
    active_position = [float(row["activePositionError"]["distance"]) for row in reached]
    target_position = [float(row["targetPositionError"]["distance"]) for row in reached]
    active_yaw = [abs(float(row["activeYawDelta"])) for row in reached]
    target_yaw = [abs(float(row["targetYawDelta"])) for row in reached]
    velocity_delta = {
        key: [
            abs(float(row["velocityDeltaVsNativeSolver"][key]))
            for row in reached
            if isinstance(row.get("velocityDeltaVsNativeSolver"), dict)
            and key in row["velocityDeltaVsNativeSolver"]
        ]
        for key in ("vx", "vy", "w")
    }
    normal = [
        float(pair["normalSignlessL2"])
        for row in reached
        if isinstance(row.get("contact"), dict)
        for pair in row["contact"]["bestPairs"]
    ]
    separation = [
        float(pair["separationAbs"])
        for row in reached
        if isinstance(row.get("contact"), dict)
        for pair in row["contact"]["bestPairs"]
    ]
    point = [
        float(pair["pointRelativeTargetL2"])
        for row in reached
        if isinstance(row.get("contact"), dict)
        for pair in row["contact"]["bestPairs"]
    ]
    return {
        "schema": "persistent_scene_front_half_audit_v2",
        "purpose": (
            "Mechanism audit: recovered velocity updates drive stable actors in one pyphysx "
            f"Scene from {start_source} to the {boundary} boundary."
        ),
        "inputs": {
            "events": str(DEFAULT_EVENTS.relative_to(PROJECT_ROOT)),
            "summary": str(DEFAULT_SUMMARY.relative_to(PROJECT_ROOT)),
            "truth": str(DEFAULT_TRUTH.relative_to(PROJECT_ROOT)),
            "runtimeFeatureEvents": str(runtime_feature_events),
            "runtimeFeatureLine": runtime_feature_line,
            "startSource": start_source,
            "boundary": boundary,
        },
        "configuration": {
            "dt": 0.01,
            "settleSteps": settle_steps,
            "runtimeFeatures": scene.runtime_feature_meta,
            "activeYawPolicy": (
                f"cold actor yaw = 0 at {start_source}; no Unity entrance yaw is injected"
            ),
            "targetYawPolicy": (
                "Unity target yaw is injected only to isolate front-half active progression; "
                "production obtains it from the persistent prior-shot actor state."
            ),
        },
        "aggregate": {
            "rowCount": len(rows),
            "reachedBoundaryCount": len(reached),
            "contactCountComparedCount": sum(
                1 for row in reached if isinstance(row.get("contact"), dict)
            ),
            "contactCountMatchCount": sum(
                1
                for row in reached
                if isinstance(row.get("contact"), dict) and bool(row["contact"]["countMatch"])
            ),
            "activePositionErrorM": _summary(active_position),
            "targetPositionErrorM": _summary(target_position),
            "activeYawAbsErrorRad": _summary(active_yaw),
            "targetYawAbsErrorRad": _summary(target_yaw),
            "velocityAbsDeltaVsNativeSolver": {
                key: _summary(values) for key, values in velocity_delta.items()
            },
            "contactNormalSignlessL2": _summary(normal),
            "contactSeparationAbsM": _summary(separation),
            "contactPointRelativeTargetL2M": _summary(point),
        },
        "rows": rows,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--truth", type=Path, default=DEFAULT_TRUTH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--runtime-feature-events",
        type=Path,
        default=DEFAULT_RUNTIME_FEATURE_EVENTS,
    )
    parser.add_argument("--runtime-feature-line", type=int, default=221)
    parser.add_argument("--no-runtime-features", action="store_true")
    parser.add_argument("--settle-steps", type=int, default=1)
    parser.add_argument("--max-steps", type=int, default=5000)
    parser.add_argument(
        "--start-source",
        choices=("bestshot", "motioninfo"),
        default="bestshot",
    )
    parser.add_argument(
        "--boundary",
        choices=("pcm-shell", "local-contact"),
        default="pcm-shell",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    events = load_jsonl(args.events)
    event_groups = event_shot_groups(events)
    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    truth = json.loads(args.truth.read_text(encoding="utf-8"))
    result = audit(
        truth,
        summary,
        event_groups,
        runtime_feature_events=args.runtime_feature_events,
        runtime_feature_line=args.runtime_feature_line,
        patch_runtime_features=not args.no_runtime_features,
        settle_steps=args.settle_steps,
        max_steps=args.max_steps,
        start_source=args.start_source,
        boundary=args.boundary,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(args.output), **result["aggregate"]}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
