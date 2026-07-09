#!/usr/bin/env python3
"""Replay a single no-collision shot from BESTSHOT parameters.

This is a reverse-engineering helper, not the training fast simulator. It uses
the recovered CurlingMotion kernel and optionally the recovered Unity RNG
friction sequence. The remaining geometric constants are explicit CLI
parameters so they can be fitted or replaced with audited Unity scene values.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.reverse.recovered_curling_motion import (  # noqa: E402
    BASE_FRICTION,
    STEP,
    B2Vec2,
    RecoveredUnityRandom,
    newfrictionstep,
    unity_friction,
)


# Recovered from Start(): origin_postion = mBlueBalls[0].transform.position and
# teePosition = GameObject.Find("Terminal").transform.position. The protocol
# adds +2.375/+4.88 after subtracting origin from tee.
DEFAULT_RELEASE_X = 2.3506
DEFAULT_RELEASE_Y = 32.4768

# CrossLineEvent sends MOTIONINFO when the moving stone first enters the Midline
# trigger, so the trigger point is Midline center plus stone radius and trigger
# half-width in protocol y. Discrete FixedUpdate stepping can move the observed
# MOTIONINFO row a few centimeters past this geometric threshold.
DEFAULT_MIDLINE_TRIGGER_PROTOCOL_Y = 21.548575


@dataclass(frozen=True)
class Bestshot:
    velocity: float
    horizontal_offset: float
    rotation: float


@dataclass(frozen=True)
class ProtocolState:
    x: float
    y: float
    vx: float
    vy: float
    w: float
    steps: int


def clamp_bestshot(shot: Bestshot) -> Bestshot:
    velocity = shot.velocity
    if velocity < 0.0001:
        velocity = 1.0
    elif velocity > 6.0:
        velocity = 6.0
    return Bestshot(
        velocity=velocity,
        horizontal_offset=max(-2.23, min(2.23, shot.horizontal_offset)),
        rotation=max(-15.7, min(15.7, shot.rotation)),
    )


def initial_protocol_state(
    shot: Bestshot,
    *,
    release_x: float = DEFAULT_RELEASE_X,
    release_y: float,
) -> ProtocolState:
    shot = clamp_bestshot(shot)
    return ProtocolState(
        x=release_x + shot.horizontal_offset,
        y=release_y,
        vx=0.0,
        vy=-shot.velocity,
        w=shot.rotation,
        steps=0,
    )


def replay_until_y(
    shot: Bestshot,
    *,
    release_x: float = DEFAULT_RELEASE_X,
    release_y: float = DEFAULT_RELEASE_Y,
    stop_y: float = DEFAULT_MIDLINE_TRIGGER_PROTOCOL_Y,
    unity_seed: int | None = None,
    sweeping: bool = False,
    max_steps: int = 5000,
) -> ProtocolState:
    state = initial_protocol_state(shot, release_x=release_x, release_y=release_y)
    rng = RecoveredUnityRandom.from_seed(unity_seed) if unity_seed is not None else None
    x = state.x
    y = state.y
    vx = state.vx
    vy = state.vy
    w = state.w

    for step in range(max_steps):
        if math.hypot(vx, vy) <= 0.01:
            return ProtocolState(x, y, vx, vy, w, step)
        if y <= stop_y:
            return ProtocolState(x, y, vx, vy, w, step)
        # FixedUpdate writes the newly computed velocity before Unity advances
        # the Rigidbody for this fixed tick.
        friction = BASE_FRICTION if rng is None else unity_friction(sweeping, rng=rng, noise=None)
        speed = newfrictionstep(friction, B2Vec2(vx, vy), w, STEP)
        vx = speed.v.x
        vy = speed.v.y
        w = speed.angle
        x += vx * 0.01
        y += vy * 0.01
    return ProtocolState(x, y, vx, vy, w, max_steps)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--v0", type=float, required=True)
    parser.add_argument("--h0", type=float, required=True)
    parser.add_argument("--w0", type=float, required=True)
    parser.add_argument("--release-x", type=float, default=DEFAULT_RELEASE_X)
    parser.add_argument("--release-y", type=float, default=DEFAULT_RELEASE_Y)
    parser.add_argument("--stop-y", type=float, default=DEFAULT_MIDLINE_TRIGGER_PROTOCOL_Y)
    parser.add_argument("--unity-seed", type=int, default=None)
    parser.add_argument("--sweeping", action="store_true")
    parser.add_argument("--max-steps", type=int, default=5000)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    state = replay_until_y(
        Bestshot(args.v0, args.h0, args.w0),
        release_x=args.release_x,
        release_y=args.release_y,
        stop_y=args.stop_y,
        unity_seed=args.unity_seed,
        sweeping=args.sweeping,
        max_steps=args.max_steps,
    )
    if args.json:
        print(json.dumps(asdict(state), ensure_ascii=False))
    else:
        print(
            "x={x:.6f} y={y:.6f} vx={vx:.6f} vy={vy:.6f} w={w:.6f} steps={steps}".format(
                **asdict(state)
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
