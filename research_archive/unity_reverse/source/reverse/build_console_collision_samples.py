#!/usr/bin/env python3
"""Build conservative one-target collision samples from console trajectory summaries."""

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


def _xy(position: list[float], index: int) -> tuple[float, float]:
    return float(position[2 * index]), float(position[2 * index + 1])


def _set_xy(position: list[float], index: int, xy: tuple[float, float]) -> None:
    position[2 * index] = float(xy[0])
    position[2 * index + 1] = float(xy[1])


def _distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _position_or_zero(values: Any) -> list[float]:
    if not isinstance(values, list):
        return [0.0] * 32
    result = [float(value) for value in values[:32]]
    if len(result) < 32:
        result.extend([0.0] * (32 - len(result)))
    return result


def _nonzero(xy: tuple[float, float]) -> bool:
    return abs(xy[0]) > 1e-9 or abs(xy[1]) > 1e-9


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


def build_samples(
    summary: dict[str, Any],
    *,
    move_threshold: float,
    exit_speed_threshold: float,
    max_target_distance: float,
    angular_mode: str,
) -> list[dict[str, Any]]:
    samples: list[dict[str, Any]] = []
    previous_position = [0.0] * 32

    for shot in summary.get("shots", []):
        shot_index = int(shot["shot_index"])
        active_index = (shot_index - 1) % 16
        if active_index == 0:
            previous_position = [0.0] * 32

        after_position = _position_or_zero(shot.get("first_position"))
        exit_state = shot.get("estimated_exit_state") or {}
        exit_speed = float(exit_state.get("speed") or 0.0)
        if exit_speed <= exit_speed_threshold:
            previous_position = after_position
            continue

        moved_targets: list[int] = []
        for index in range(active_index):
            before_xy = _xy(previous_position, index)
            after_xy = _xy(after_position, index)
            if not _nonzero(before_xy):
                continue
            if _distance(before_xy, after_xy) > move_threshold:
                moved_targets.append(index)

        if len(moved_targets) != 1:
            previous_position = after_position
            continue

        target_index = moved_targets[0]
        target_before = _xy(previous_position, target_index)
        exit_position = tuple(float(value) for value in exit_state["position"])
        target_distance = _distance(exit_position, target_before)
        if target_distance > max_target_distance:
            previous_position = after_position
            continue

        exit_velocity = [float(value) for value in exit_state["velocity"]]
        motioninfo = [float(value) for value in shot.get("motioninfo") or [0.0, 0.0, 0.0, 0.0, 0.0]]
        if angular_mode == "motioninfo":
            angular_velocity = motioninfo[4]
        elif angular_mode == "zero":
            angular_velocity = 0.0
        elif angular_mode == "replay":
            angular_velocity = _replay_angular_to_exit(motioninfo, exit_position)
        else:
            raise ValueError(f"unsupported angular mode: {angular_mode}")

        sample_id = 30000 + shot_index
        reset_position = previous_position.copy()
        _set_xy(reset_position, active_index, exit_position)
        sample = {
            "sample_id": sample_id,
            "label": f"console_match_shot_{shot_index:02d}_target_{target_index:02d}",
            "category": "collision_console_explicit_handoff",
            "collision_observed": True,
            "sent_sweep": False,
            "active_shot_num": active_index,
            "target_indices": [target_index],
            "motioninfo": motioninfo,
            "reset_position": reset_position,
            "after_position": after_position,
            "handoff_state": {
                "source": f"console_velocity_integral:{angular_mode}",
                "step": int(shot.get("velocity_count") or -1),
                "x": exit_position[0],
                "y": exit_position[1],
                "vx": exit_velocity[0],
                "vy": exit_velocity[1],
                "w": angular_velocity,
                "distance": target_distance,
                "threshold": 0.0,
            },
            "console_trace": {
                "shot_index": shot_index,
                "bestshot": shot.get("bestshot"),
                "line_start": shot.get("line_start"),
                "stop_line": shot.get("stop_line"),
                "motioninfo_line": shot.get("motioninfo_line"),
                "exit_speed": exit_speed,
                "moved_targets": moved_targets,
            },
        }
        samples.append(sample)
        previous_position = after_position

    return samples


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("summary", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--move-threshold", type=float, default=0.02)
    parser.add_argument("--exit-speed-threshold", type=float, default=0.05)
    parser.add_argument("--max-target-distance", type=float, default=0.45)
    parser.add_argument("--angular-mode", choices=("motioninfo", "zero", "replay"), default="motioninfo")
    args = parser.parse_args()

    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    samples = build_samples(
        summary,
        move_threshold=args.move_threshold,
        exit_speed_threshold=args.exit_speed_threshold,
        max_target_distance=args.max_target_distance,
        angular_mode=args.angular_mode,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for sample in samples:
            handle.write(json.dumps(sample, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "sample_count": len(samples)}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
