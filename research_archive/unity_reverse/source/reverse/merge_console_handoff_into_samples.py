#!/usr/bin/env python3
"""Merge console-derived explicit PhysX handoff states into controlled samples."""

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

from tools.reverse.recovered_curling_motion import BASE_FRICTION, STEP, B2Vec2, newfrictionstep


def _distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _xy(position: list[float], index: int) -> tuple[float, float]:
    return float(position[2 * index]), float(position[2 * index + 1])


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _replay_angular_to_exit(motioninfo: list[float], exit_position: tuple[float, float]) -> float:
    if len(motioninfo) < 5:
        return 0.0
    x, y, vx, vy, w = [float(value) for value in motioninfo[:5]]
    best_distance = float("inf")
    best_w = w
    for _step_index in range(6000):
        distance = _distance((x, y), exit_position)
        if distance < best_distance:
            best_distance = distance
            best_w = w
        speed = newfrictionstep(BASE_FRICTION, B2Vec2(vx, vy), w, STEP)
        vx, vy, w = speed.v.x, speed.v.y, speed.angle
        x += vx * 0.01
        y += vy * 0.01
        if math.hypot(vx, vy) < 1e-5:
            break
    return best_w


def _angular_velocity(mode: str, sample: dict[str, Any], trace: dict[str, Any], exit_position: tuple[float, float]) -> float:
    motioninfo = sample.get("motioninfo") or trace.get("motioninfo") or [0, 0, 0, 0, 0]
    if mode == "zero":
        return 0.0
    if mode == "motioninfo":
        return float(motioninfo[4])
    if mode == "replay":
        return _replay_angular_to_exit([float(value) for value in motioninfo[:5]], exit_position)
    raise ValueError(f"unsupported angular mode: {mode}")


def _validate_bestshot(sample: dict[str, Any], trace: dict[str, Any], tolerance: float) -> None:
    requested = sample.get("requested") or {}
    bestshot = trace.get("bestshot") or []
    if len(bestshot) < 3:
        raise ValueError(f"console trace for sample {sample.get('sample_id')} has no BESTSHOT")
    expected = [float(requested.get("v0", 0.0)), float(requested.get("h0", 0.0)), float(requested.get("w0", 0.0))]
    observed = [float(value) for value in bestshot[:3]]
    deltas = [abs(a - b) for a, b in zip(expected, observed)]
    if any(delta > tolerance for delta in deltas):
        raise ValueError(
            f"BESTSHOT mismatch for sample {sample.get('sample_id')}: "
            f"expected={expected}, console={observed}, deltas={deltas}"
        )


def merge_samples(
    samples: list[dict[str, Any]],
    traces: list[dict[str, Any]],
    *,
    angular_mode: str,
    skip_console_shots: int,
    tolerance: float,
) -> list[dict[str, Any]]:
    selected = traces[skip_console_shots : skip_console_shots + len(samples)]
    if len(selected) != len(samples):
        raise ValueError(f"need {len(samples)} console traces, got {len(selected)}")

    merged: list[dict[str, Any]] = []
    for sample, trace in zip(samples, selected):
        _validate_bestshot(sample, trace, tolerance)
        exit_state = trace.get("estimated_exit_state") or {}
        exit_position = tuple(float(value) for value in exit_state["position"])
        exit_velocity = [float(value) for value in exit_state["velocity"]]
        target_indices = sample.get("target_indices") or []
        target_distance = 0.0
        if target_indices:
            target_distance = _distance(exit_position, _xy(sample["reset_position"], int(target_indices[0])))
        row = dict(sample)
        row["handoff_state"] = {
            "source": f"runtime_console_velocity_integral:{angular_mode}",
            "step": int(trace.get("velocity_count") or -1),
            "x": exit_position[0],
            "y": exit_position[1],
            "vx": exit_velocity[0],
            "vy": exit_velocity[1],
            "w": _angular_velocity(angular_mode, sample, trace, exit_position),
            "distance": target_distance,
            "threshold": 0.0,
        }
        row["console_trace"] = {
            "shot_index": trace.get("shot_index"),
            "line_start": trace.get("line_start"),
            "stop_line": trace.get("stop_line"),
            "motioninfo_line": trace.get("motioninfo_line"),
            "bestshot": trace.get("bestshot"),
            "motioninfo": trace.get("motioninfo"),
            "exit_speed": float(exit_state.get("speed") or 0.0),
            "active_final_position": exit_state.get("active_final_position"),
            "distance_to_active_final": exit_state.get("distance_to_active_final"),
        }
        merged.append(row)
    return merged


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=Path, required=True)
    parser.add_argument("--console-summary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--angular-mode", choices=("motioninfo", "zero", "replay"), default="replay")
    parser.add_argument("--skip-console-shots", type=int, default=0)
    parser.add_argument("--bestshot-tolerance", type=float, default=1e-4)
    args = parser.parse_args()

    samples = _read_jsonl(args.samples)
    summary = json.loads(args.console_summary.read_text(encoding="utf-8"))
    merged = merge_samples(
        samples,
        summary.get("shots", []),
        angular_mode=args.angular_mode,
        skip_console_shots=args.skip_console_shots,
        tolerance=args.bestshot_tolerance,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for row in merged:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    print(json.dumps({"output": str(args.output), "sample_count": len(merged)}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
