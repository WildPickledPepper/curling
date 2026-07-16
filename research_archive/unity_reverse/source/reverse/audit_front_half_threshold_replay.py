#!/usr/bin/env python3
"""Audit self-stopped BESTSHOT -> first-PCM entrance replay thresholds."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
DEFAULT_EVENTS = PROJECT_ROOT / "log" / "unity_runtime_probe_20260710_012403" / "events.jsonl"
DEFAULT_SUMMARY = PROJECT_ROOT / "log" / "unity_runtime_probe_20260710_012403" / "front_half_pcm_summary.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "front_half_threshold_replay_audit_20260710.json"
FORMAL_RADIUS = 0.140875
UNITY_CONTACT_OFFSET = 0.01

from tools.reverse.front_half_pcm_replay import (  # noqa: E402
    FIRST_PCM_CENTER_DISTANCE,
    error_to_unity,
    event_shot_groups,
    friction_noises_after_motioninfo,
    load_jsonl,
    replay_bestshot_until_center_distance,
    replay_motioninfo_until_center_distance,
    unity_protocol_transform,
)


def _parse_float_list(value: str) -> list[float]:
    return [float(part.strip()) for part in value.split(",") if part.strip()]


def _unity_active_target(shot: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    contact_before = shot.get("firstPcmWithContactsBefore") or shot.get("firstPcmBefore")
    if not isinstance(contact_before, dict):
        raise ValueError("shot lacks first PCM before transform")
    plan = shot.get("plan") or {}
    target_plan = (plan.get("stones") or [{}])[0]
    target_x = float(target_plan.get("x"))
    target_y = float(target_plan.get("y"))
    transform1 = contact_before.get("transform1") or {}
    target_native_p = transform1.get("p") or [0.0, 0.0, 0.0]
    native_to_protocol_x_const = target_x + float(target_native_p[2])
    native_to_protocol_y_const = target_y + float(target_native_p[0])
    active = unity_protocol_transform(
        contact_before.get("transform0") or {},
        native_to_protocol_x_const=native_to_protocol_x_const,
        native_to_protocol_y_const=native_to_protocol_y_const,
    )
    target = unity_protocol_transform(
        transform1,
        native_to_protocol_x_const=native_to_protocol_x_const,
        native_to_protocol_y_const=native_to_protocol_y_const,
    )
    contact_after = shot.get("firstPcmWithContactsAfter") or shot.get("firstPcmAfter") or {}
    meta = {
        "target_plan": {"x": target_x, "y": target_y},
        "contact_count": ((contact_after.get("contactBuffer") or {}).get("count")),
        "contact_boundary": "firstPcmWithContacts" if shot.get("firstPcmWithContactsBefore") else "firstPcmAny",
    }
    return active, target, meta


def _noises_before_next_shot(event_group: dict[str, Any]) -> list[float]:
    return [float(item["noise"]) for item in event_group.get("friction") or []]


def _summary(values: list[float]) -> dict[str, Any]:
    return {
        "count": len(values),
        "rmse": math.sqrt(sum(value * value for value in values) / len(values)) if values else None,
        "mean": sum(values) / len(values) if values else None,
        "max": max(values) if values else None,
    }


def audit(summary: dict[str, Any], event_groups: list[dict[str, Any]], thresholds: list[float]) -> dict[str, Any]:
    result_sets: list[dict[str, Any]] = []
    motioninfo_result_sets: list[dict[str, Any]] = []
    for threshold in thresholds:
        rows: list[dict[str, Any]] = []
        motioninfo_rows: list[dict[str, Any]] = []
        for seq, shot in enumerate(summary.get("shots") or []):
            if seq >= len(event_groups):
                continue
            unity_active, unity_target, meta = _unity_active_target(shot)
            event_group = event_groups[seq]
            noises = _noises_before_next_shot(event_group)
            local = replay_bestshot_until_center_distance(
                float(shot["v0"]),
                float(shot["h0"]),
                float(shot["w0"]),
                noises,
                target_x=float(unity_target["x"]),
                target_y=float(unity_target["y"]),
                threshold=threshold,
                interpolate=False,
            )
            error = error_to_unity(local, unity_active)
            rows.append(
                {
                    "seq": seq,
                    "label": (shot.get("plan") or {}).get("label"),
                    "contact_boundary": meta["contact_boundary"],
                    "contact_count": meta["contact_count"],
                    "unity_active": unity_active,
                    "unity_target": unity_target,
                    "unity_center_distance": math.hypot(
                        float(unity_active["x"]) - float(unity_target["x"]),
                        float(unity_active["y"]) - float(unity_target["y"]),
                    ),
                    "local": local,
                    "error": error,
                    "step_delta_vs_unity_friction_calls": (
                        float(local["steps"]) - int(shot.get("frictionRangeCountBeforeFirstPcm") or 0)
                    ),
                }
            )
            motion_event = event_group.get("motioninfo")
            if isinstance(motion_event, dict):
                motion_local = replay_motioninfo_until_center_distance(
                    motion_event.get("values") or [],
                    friction_noises_after_motioninfo(event_group),
                    target_x=float(unity_target["x"]),
                    target_y=float(unity_target["y"]),
                    threshold=threshold,
                    interpolate=False,
                )
                motion_error = error_to_unity(motion_local, unity_active)
                motioninfo_rows.append(
                    {
                        "seq": seq,
                        "label": (shot.get("plan") or {}).get("label"),
                        "contact_boundary": meta["contact_boundary"],
                        "contact_count": meta["contact_count"],
                        "unity_active": unity_active,
                        "unity_target": unity_target,
                        "motioninfo": motion_event,
                        "local": motion_local,
                        "error": motion_error,
                    }
                )
        errors = [float(row["error"]["positionError"]) for row in rows]
        step_abs = [abs(float(row["step_delta_vs_unity_friction_calls"])) for row in rows]
        missed_count = sum(1 for row in rows if (row.get("local") or {}).get("missedThreshold"))
        result_sets.append(
            {
                "threshold": threshold,
                "threshold_minus_2r": threshold - 2.0 * FORMAL_RADIUS,
                "summary": {
                    "position": _summary(errors),
                    "abs_step_delta": _summary(step_abs),
                    "row_count": len(rows),
                    "reached_threshold_count": len(rows) - missed_count,
                    "missed_threshold_count": missed_count,
                },
                "rows": rows,
            }
        )
        motion_errors = [float(row["error"]["positionError"]) for row in motioninfo_rows]
        motion_missed_count = sum(
            1 for row in motioninfo_rows if (row.get("local") or {}).get("missedThreshold")
        )
        motioninfo_result_sets.append(
            {
                "threshold": threshold,
                "threshold_minus_2r": threshold - 2.0 * FORMAL_RADIUS,
                "summary": {
                    "position": _summary(motion_errors),
                    "row_count": len(motioninfo_rows),
                    "reached_threshold_count": len(motioninfo_rows) - motion_missed_count,
                    "missed_threshold_count": motion_missed_count,
                },
                "rows": motioninfo_rows,
            }
        )
    best = min(
        result_sets,
        key=lambda item: float("inf")
        if item["summary"]["position"]["rmse"] is None
        else float(item["summary"]["position"]["rmse"]),
    )
    best_motioninfo = min(
        motioninfo_result_sets,
        key=lambda item: float("inf")
        if item["summary"]["position"]["rmse"] is None
        else float(item["summary"]["position"]["rmse"]),
    )
    observed_distances = [
        float(row["unity_center_distance"])
        for row in result_sets[0]["rows"]
        if row.get("unity_center_distance") is not None
    ] if result_sets else []
    return {
        "schema": "front_half_threshold_replay_audit_v2",
        "inputs": {
            "events": str(DEFAULT_EVENTS.relative_to(PROJECT_ROOT)),
            "summary": str(DEFAULT_SUMMARY.relative_to(PROJECT_ROOT)),
        },
        "constants": {
            "formal_radius": FORMAL_RADIUS,
            "unity_contact_offset": UNITY_CONTACT_OFFSET,
            "default_thresholds": {
                "2r": 2.0 * FORMAL_RADIUS,
                "2r_plus_contact_offset": 2.0 * FORMAL_RADIUS + UNITY_CONTACT_OFFSET,
                "2r_plus_2contact_offset": 2.0 * FORMAL_RADIUS + 2.0 * UNITY_CONTACT_OFFSET,
            },
        },
        "observed_unity_first_contact_center_distance": _summary(observed_distances),
        "best_threshold_by_position_rmse": best["threshold"] if result_sets else None,
        "best_summary": best["summary"] if result_sets else None,
        "motioninfo_best_threshold_by_position_rmse": (
            best_motioninfo["threshold"] if motioninfo_result_sets else None
        ),
        "motioninfo_best_summary": (
            best_motioninfo["summary"] if motioninfo_result_sets else None
        ),
        "first_pcm_discrete_tick_note": (
            "Both replay paths return the first post-FixedUpdate state inside the "
            "2R+2*contactOffset shell; no geometric interpolation is used."
        ),
        "result_sets": result_sets,
        "motioninfo_result_sets": motioninfo_result_sets,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--thresholds",
        default=",".join(
            str(value)
            for value in (
                2.0 * FORMAL_RADIUS,
                2.0 * FORMAL_RADIUS + UNITY_CONTACT_OFFSET,
                2.0 * FORMAL_RADIUS + 2.0 * UNITY_CONTACT_OFFSET,
            )
        ),
        help="Comma list of center-distance thresholds in protocol meters.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    events = load_jsonl(args.events)
    event_groups = event_shot_groups(events)
    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    report = audit(summary, event_groups, _parse_float_list(args.thresholds))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "observed": report["observed_unity_first_contact_center_distance"],
                "best_threshold_by_position_rmse": report["best_threshold_by_position_rmse"],
                "best_summary": report["best_summary"],
                "motioninfo_best_threshold_by_position_rmse": report[
                    "motioninfo_best_threshold_by_position_rmse"
                ],
                "motioninfo_best_summary": report["motioninfo_best_summary"],
                "threshold_summaries": [
                    {
                        "threshold": item["threshold"],
                        "position_rmse_m": item["summary"]["position"]["rmse"],
                        "position_max_m": item["summary"]["position"]["max"],
                        "abs_step_delta_mean": item["summary"]["abs_step_delta"]["mean"],
                        "reached_threshold_count": item["summary"]["reached_threshold_count"],
                        "missed_threshold_count": item["summary"]["missed_threshold_count"],
                    }
                    for item in report["result_sets"]
                ],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
