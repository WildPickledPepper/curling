#!/usr/bin/env python3
"""Recovered protocol-space sweep window helpers.

Unity's Sweep.Sweeper keeps ``isSweeping`` while:

    target.x < Hogline2.x
    target.x < Midline.x + sweepDistance

The protocol y axis is ``teePosition.x - unity_x + 4.88``, so the active
tail window is represented by decreasing protocol y values.
"""

from __future__ import annotations

from dataclasses import dataclass


# Derived from assets and Start(): protocol_y = tee.x - unity_x + 4.88.
MIDLINE_CENTER_PROTOCOL_Y = 21.3342
MIDLINE_TRIGGER_PROTOCOL_Y = 21.548575
HOGLINE2_PROTOCOL_Y = 10.3442
MAX_SWEEP_DISTANCE = MIDLINE_CENTER_PROTOCOL_Y - HOGLINE2_PROTOCOL_Y


@dataclass(frozen=True)
class SweepWindow:
    start_y: float
    end_y: float
    requested_distance: float
    capped_distance: float

    def active_at(self, protocol_y: float) -> bool:
        return protocol_y <= self.start_y and protocol_y > self.end_y


def sweep_window(distance: float, *, start_y: float = MIDLINE_TRIGGER_PROTOCOL_Y) -> SweepWindow:
    capped = max(0.0, min(float(distance), MAX_SWEEP_DISTANCE))
    return SweepWindow(
        start_y=start_y,
        end_y=MIDLINE_CENTER_PROTOCOL_Y - capped,
        requested_distance=float(distance),
        capped_distance=capped,
    )


def is_sweeping_at_protocol_y(protocol_y: float, distance: float | None) -> bool:
    if distance is None:
        return False
    return sweep_window(distance).active_at(protocol_y)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("distance", type=float)
    parser.add_argument("--y", type=float, default=None)
    args = parser.parse_args()

    window = sweep_window(args.distance)
    print(
        f"start_y={window.start_y:.6f} end_y={window.end_y:.6f} "
        f"requested={window.requested_distance:.6f} capped={window.capped_distance:.6f}"
    )
    if args.y is not None:
        print(f"active={window.active_at(args.y)}")


if __name__ == "__main__":
    main()
