#!/usr/bin/env python3
"""Export reusable first-contact PCM entrance truth from the front-half capture."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SAMPLES = PROJECT_ROOT / "data" / "calibration" / "front_half_pcm_samples_20260710_012534.jsonl"
DEFAULT_SUMMARY = PROJECT_ROOT / "log" / "unity_runtime_probe_20260710_012403" / "front_half_pcm_summary.json"
DEFAULT_COMPARE = PROJECT_ROOT / "data" / "calibration" / "front_half_pcm_replay_compare_20260710.json"
DEFAULT_SOLVER = PROJECT_ROOT / "data" / "calibration" / "front_half_pcm_solver_state_20260710.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "front_half_pcm_entrance_truth_20260710.json"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                item = json.loads(line)
                if isinstance(item, dict):
                    rows.append(item)
    return rows


def norm_angle(angle: float) -> float:
    value = float(angle)
    while value > math.pi:
        value -= 2.0 * math.pi
    while value <= -math.pi:
        value += 2.0 * math.pi
    return value


def first_stone_stone_solver_rows(
    solver: dict[str, Any],
    summary: dict[str, Any],
) -> dict[int, dict[str, Any]]:
    shot_times = [float(shot.get("t") or 0.0) for shot in summary.get("shots") or []]
    next_times = shot_times[1:] + [float("inf")]
    out: dict[int, dict[str, Any]] = {}
    for seq, (start, end) in enumerate(zip(shot_times, next_times)):
        rows = [
            row
            for row in solver.get("rows") or []
            if row.get("phase") == "after"
            and row.get("pairClass") == "stone_stone"
            and start <= float(row.get("t") or 0.0) < end
        ]
        if rows:
            out[seq] = rows[0]
    return out


def solver_body_protocol_velocity(data: dict[str, Any], body: str) -> dict[str, Any] | None:
    lv = data.get("linearVelocity")
    av = data.get("angularVelocity")
    if not isinstance(lv, list) or len(lv) < 3 or not isinstance(av, list) or len(av) < 3:
        return None
    return {
        "body": body,
        "vx": -float(lv[2]),
        "vy": -float(lv[0]),
        "vz": float(lv[1]),
        "wx": float(av[0]),
        "wy": float(av[2]),
        "w": float(av[1]),
        "nativeLinearVelocity": lv,
        "nativeAngularVelocity": av,
    }


def solver_protocol_velocity(row: dict[str, Any] | None) -> dict[str, Any] | None:
    if not row:
        return None
    data0 = ((row.get("solverBodyData") or {}).get("data0") or {})
    data1 = ((row.get("solverBodyData") or {}).get("data1") or {})
    active = solver_body_protocol_velocity(data0, "body0_active")
    target = solver_body_protocol_velocity(data1, "body1_target")
    if active is None:
        return None
    out = {
        "source": "first stone_stone createFinalizeSolverContacts.after body0/body1",
        "t": row.get("t"),
        "active": active,
        "target": target,
        "vx": active["vx"],
        "vy": active["vy"],
        "vz": active["vz"],
        "wx": active["wx"],
        "wy": active["wy"],
        "w": active["w"],
        "nativeLinearVelocity": active["nativeLinearVelocity"],
        "nativeAngularVelocity": active["nativeAngularVelocity"],
        "numContacts": ((row.get("contactDesc") or {}).get("numContacts")),
    }
    return out


def build_truth(
    samples: list[dict[str, Any]],
    summary: dict[str, Any],
    compare: dict[str, Any],
    solver: dict[str, Any],
) -> dict[str, Any]:
    solver_by_seq = first_stone_stone_solver_rows(solver, summary)
    rows: list[dict[str, Any]] = []
    for seq, (sample, shot, row) in enumerate(
        zip(samples, summary.get("shots") or [], compare.get("rows") or [])
    ):
        active_index = int(sample.get("active_shot_num"))
        target_indices = [int(value) for value in sample.get("target_indices") or []]
        target_index = target_indices[0] if target_indices else None
        best = row.get("bestPositionCandidate") or {}
        local = best.get("local") or {}
        error = best.get("error") or {}
        unity_active = row.get("unityActive") or {}
        unity_target = row.get("unityTarget") or {}
        active_xy = [float(unity_active["x"]), float(unity_active["y"])]
        target_xy = [float(unity_target["x"]), float(unity_target["y"])]
        solver_velocity = solver_protocol_velocity(solver_by_seq.get(seq))
        local_velocity = {
            "source": "BESTSHOT replay with captured Random.Range friction sequence",
            "vx": local.get("vx"),
            "vy": local.get("vy"),
            "w": local.get("w"),
            "yawIntegratedFromZero": norm_angle(float(local.get("yaw") or 0.0)),
            "steps": local.get("steps"),
        }
        rows.append(
            {
                "seq": seq,
                "sample_id": sample.get("sample_id"),
                "label": sample.get("label"),
                "final_source": sample.get("final_source"),
                "requested": sample.get("requested"),
                "active_index": active_index,
                "target_index": target_index,
                "first_contact_pcm": {
                    "boundary": row.get("contactBoundary"),
                    "contact_count": row.get("contactCount"),
                    "raw_friction_range_calls": row.get("rawFrictionRangeCallsBeforeContact"),
                    "unity_center_distance_m": row.get("unityCenterDistance"),
                    "unity_relative_xy_m": row.get("unityRelative"),
                },
                "unity_entrance_state": {
                    "coordinate_system": "protocol x/y plus yaw converted from Unity y-up quaternion",
                    "active": {
                        "x": active_xy[0],
                        "y": active_xy[1],
                        "yaw": unity_active.get("yaw"),
                        "nativeP": unity_active.get("nativeP"),
                        "nativeQ": unity_active.get("nativeQ"),
                    },
                    "target": {
                        "x": target_xy[0],
                        "y": target_xy[1],
                        "yaw": unity_target.get("yaw"),
                        "nativeP": unity_target.get("nativeP"),
                        "nativeQ": unity_target.get("nativeQ"),
                    },
                },
                "local_front_half_replay": {
                    "state": local,
                    "velocity": local_velocity,
                    "position_error_vs_unity_m": error.get("positionError"),
                    "dx_m": error.get("dx"),
                    "dy_m": error.get("dy"),
                    "yaw_delta_vs_unity_rad": error.get("yawDelta"),
                    "inferred_initial_yaw_offset_rad": row.get("inferredInitialYawOffset"),
                },
                "native_solver_velocity": solver_velocity,
                "flags": {
                    "target_yaw_hidden": abs(float(unity_target.get("yaw") or 0.0)) > 1e-4,
                    "active_initial_yaw_offset_nonzero": abs(
                        float(row.get("inferredInitialYawOffset") or 0.0)
                    )
                    > 1e-4,
                    "has_native_solver_velocity": solver_velocity is not None,
                    "sampler_endpoint_reliable": sample.get("final_source") == "position",
                },
            }
        )

    position_errors = [
        float(item["local_front_half_replay"]["position_error_vs_unity_m"])
        for item in rows
        if item["local_front_half_replay"].get("position_error_vs_unity_m") is not None
    ]
    return {
        "schema": "front_half_pcm_entrance_truth_v1",
        "purpose": (
            "Reusable Unity first-contact PCM entrance truth for validating the local "
            "shot/motioninfo -> first PCM front-half replay."
        ),
        "inputs": {
            "samples": str(DEFAULT_SAMPLES.relative_to(PROJECT_ROOT)),
            "summary": str(DEFAULT_SUMMARY.relative_to(PROJECT_ROOT)),
            "compare": str(DEFAULT_COMPARE.relative_to(PROJECT_ROOT)),
            "solver": str(DEFAULT_SOLVER.relative_to(PROJECT_ROOT)),
        },
        "aggregate": {
            "row_count": len(rows),
            "position_rmse_m": (
                math.sqrt(sum(value * value for value in position_errors) / len(position_errors))
                if position_errors
                else None
            ),
            "position_max_error_m": max(position_errors) if position_errors else None,
            "first_contact_pose_truth_count": len(rows),
            "native_solver_velocity_count": sum(
                1 for item in rows if item["flags"]["has_native_solver_velocity"]
            ),
            "hidden_yaw_required": any(
                item["flags"]["target_yaw_hidden"]
                or item["flags"]["active_initial_yaw_offset_nonzero"]
                for item in rows
            ),
        },
        "rows": rows,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--compare", type=Path, default=DEFAULT_COMPARE)
    parser.add_argument("--solver", type=Path, default=DEFAULT_SOLVER)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    samples = read_jsonl(args.samples)
    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    compare = json.loads(args.compare.read_text(encoding="utf-8"))
    solver = json.loads(args.solver.read_text(encoding="utf-8")) if args.solver.exists() else {}
    report = build_truth(samples, summary, compare, solver)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(
        json.dumps(
            {"output": str(args.output), "aggregate": report["aggregate"]},
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
