#!/usr/bin/env python3
"""Extract per-shot velocity traces from Unity browser console logs."""

from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


BESTSHOT_RE = re.compile(r"Handle message:BESTSHOT\s+([^\r\n]+)")
VELOCITY_RE = re.compile(
    r"b2Vec2 velocity:\s*x=([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:E[+-]?\d+)?),\s*"
    r"y=([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:E[+-]?\d+)?)",
    re.IGNORECASE,
)
POSITION_RE = re.compile(r"Send POSITION\s+(.+)")
SETSTATE_RE = re.compile(r"Send SETSTATE\s+(.+)")
SCORE_RE = re.compile(r"Send SCORE\s+(.+)")
MOTIONINFO_RE = re.compile(r"Send MOTIONINFO\s+(.+)")


@dataclass
class VelocityPoint:
    line: int
    x: float
    y: float
    speed: float


@dataclass
class ShotTrace:
    shot_index: int
    line_start: int
    bestshot: list[float]
    velocities: list[VelocityPoint] = field(default_factory=list)
    stop_line: int | None = None
    first_position_line: int | None = None
    first_position: list[float] | None = None
    motioninfo_line: int | None = None
    motioninfo: list[float] | None = None
    setstates: list[tuple[int, str]] = field(default_factory=list)
    scores: list[tuple[int, str]] = field(default_factory=list)


def _parse_float_list(text: str) -> list[float]:
    values: list[float] = []
    for part in text.strip().split():
        try:
            values.append(float(part))
        except ValueError:
            pass
    return values


def parse_console_log(path: Path) -> list[ShotTrace]:
    shots: list[ShotTrace] = []
    current: ShotTrace | None = None

    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line_no, line in enumerate(handle, start=1):
            bestshot_match = BESTSHOT_RE.search(line)
            if bestshot_match:
                current = ShotTrace(
                    shot_index=len(shots) + 1,
                    line_start=line_no,
                    bestshot=_parse_float_list(bestshot_match.group(1)),
                )
                shots.append(current)
                continue

            if current is None:
                continue

            velocity_match = VELOCITY_RE.search(line)
            if velocity_match:
                x = float(velocity_match.group(1))
                y = float(velocity_match.group(2))
                current.velocities.append(VelocityPoint(line=line_no, x=x, y=y, speed=math.hypot(x, y)))
                continue

            if "Curling stop" in line:
                current.stop_line = line_no
                continue

            position_match = POSITION_RE.search(line)
            if position_match and current.first_position is None:
                current.first_position_line = line_no
                current.first_position = _parse_float_list(position_match.group(1))
                continue

            motioninfo_match = MOTIONINFO_RE.search(line)
            if motioninfo_match and current.motioninfo is None:
                current.motioninfo_line = line_no
                current.motioninfo = _parse_float_list(motioninfo_match.group(1))
                continue

            setstate_match = SETSTATE_RE.search(line)
            if setstate_match:
                current.setstates.append((line_no, setstate_match.group(1).strip()))
                continue

            score_match = SCORE_RE.search(line)
            if score_match:
                current.scores.append((line_no, score_match.group(1).strip()))
                continue

    return shots


def _largest_speed_jumps(points: list[VelocityPoint], limit: int = 5) -> list[dict[str, Any]]:
    jumps: list[dict[str, Any]] = []
    for prev, cur in zip(points, points[1:]):
        dx = cur.x - prev.x
        dy = cur.y - prev.y
        ds = cur.speed - prev.speed
        jumps.append(
            {
                "line": cur.line,
                "prev_line": prev.line,
                "delta_vx": dx,
                "delta_vy": dy,
                "delta_speed": ds,
                "jump_norm": math.hypot(dx, dy),
                "prev": asdict(prev),
                "cur": asdict(cur),
            }
        )
    jumps.sort(key=lambda row: row["jump_norm"], reverse=True)
    return jumps[:limit]


def _active_pair(values: list[float] | None, shot_index: int) -> list[float] | None:
    if not values:
        return None
    pair_index = (shot_index - 1) % 16
    offset = pair_index * 2
    if offset + 1 >= len(values):
        return None
    return [values[offset], values[offset + 1]]


def _integrated_exit_state(
    shot: ShotTrace,
    *,
    release_x: float,
    release_y: float,
    dt: float,
) -> dict[str, Any] | None:
    if not shot.velocities or len(shot.bestshot) < 2:
        return None
    initial_x = release_x + shot.bestshot[1]
    initial_y = release_y

    # Unity logs the first velocity before the first position advance. Dropping it
    # matches no-collision stop positions to millimetre level in the console traces.
    integrated_points = shot.velocities[1:]
    x = initial_x + sum(point.x for point in integrated_points) * dt
    y = initial_y + sum(point.y for point in integrated_points) * dt
    last = shot.velocities[-1]
    active_final = _active_pair(shot.first_position, shot.shot_index)
    residual = None
    if active_final is not None:
      residual = math.hypot(x - active_final[0], y - active_final[1])
    return {
        "initial_position": [initial_x, initial_y],
        "dt": dt,
        "position": [x, y],
        "velocity": [last.x, last.y],
        "speed": last.speed,
        "active_final_position": active_final,
        "distance_to_active_final": residual,
    }


def summarize_shot(shot: ShotTrace, *, release_x: float, release_y: float, dt: float) -> dict[str, Any]:
    velocities = shot.velocities
    first = velocities[0] if velocities else None
    last = velocities[-1] if velocities else None
    speed_max = max((point.speed for point in velocities), default=None)
    speed_min = min((point.speed for point in velocities), default=None)
    return {
        "shot_index": shot.shot_index,
        "line_start": shot.line_start,
        "bestshot": shot.bestshot,
        "velocity_count": len(velocities),
        "first_velocity": asdict(first) if first else None,
        "last_velocity": asdict(last) if last else None,
        "speed_max": speed_max,
        "speed_min": speed_min,
        "stop_line": shot.stop_line,
        "first_position_line": shot.first_position_line,
        "first_position": shot.first_position,
        "active_final_position": _active_pair(shot.first_position, shot.shot_index),
        "motioninfo_line": shot.motioninfo_line,
        "motioninfo": shot.motioninfo,
        "estimated_exit_state": _integrated_exit_state(
            shot,
            release_x=release_x,
            release_y=release_y,
            dt=dt,
        ),
        "setstates": shot.setstates[:6],
        "scores": shot.scores[:4],
        "largest_jumps": _largest_speed_jumps(velocities),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--limit", type=int, default=0, help="Print first N summaries; 0 prints all.")
    parser.add_argument("--release-x", type=float, default=2.3506)
    parser.add_argument("--release-y", type=float, default=32.4768)
    parser.add_argument("--dt", type=float, default=0.01)
    args = parser.parse_args()

    shots = parse_console_log(args.input)
    summary = {
        "input": str(args.input),
        "release_x": args.release_x,
        "release_y": args.release_y,
        "dt": args.dt,
        "shot_count": len(shots),
        "shots": [
            summarize_shot(shot, release_x=args.release_x, release_y=args.release_y, dt=args.dt)
            for shot in shots
        ],
    }

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    printable = summary if args.limit <= 0 else {**summary, "shots": summary["shots"][: args.limit]}
    print(json.dumps(printable, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
