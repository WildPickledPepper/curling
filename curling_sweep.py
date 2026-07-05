# -*- coding: utf-8 -*-
"""Conservative sweeping heuristics for the digital curling protocol."""

from __future__ import annotations

import math
from typing import Optional, Sequence, Tuple


HOUSE_Y = 4.88
MAX_SWEEP_DISTANCE = 12.0
SWEEP_Y_GAIN = 0.045

Shot = Tuple[float, float, float]

NO_SWEEP_ACTIONS = {
    "guard_left",
    "guard_right",
    "occupy",
    "take_out",
    "hit_roll",
    "clear",
    "double_hit_gote",
    "defense",
    "defense_push_in",
}


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def estimate_mock_landing_y(shot: Shot) -> float:
    """Match the local mock server's no-sweep y estimate."""
    v0, _, w0 = shot
    return 8.0 - clamp(v0, 0.0, 6.0) * 1.02 + abs(w0) * 0.05


def estimate_sweep_distance(
    shot: Optional[Shot],
    action_name: str = "",
    motioninfo: Optional[Sequence[float]] = None,
) -> float:
    """Return a conservative sweep distance in meters.

    This is deliberately a post-shot heuristic, not a learned policy. It mainly
    helps draw-style shots that are predicted to stop short of the tee line in
    the local physics model, and avoids high-speed takeout/guard actions.
    """
    if shot is None or action_name in NO_SWEEP_ACTIONS:
        return 0.0

    v0, _, _ = shot
    if v0 >= 3.6:
        return 0.0

    target_y = HOUSE_Y
    predicted_y = estimate_mock_landing_y(shot)

    if motioninfo and len(motioninfo) >= 5:
        _, mid_y, _, vy, _ = motioninfo[:5]
        if mid_y < HOUSE_Y or vy >= -0.15:
            return 0.0

    short_by = predicted_y - target_y
    if short_by <= 0.035:
        return 0.0

    distance = short_by / SWEEP_Y_GAIN
    if action_name in {"freeze", "push_in", "push_in_14"}:
        distance *= 0.5
    return float(clamp(distance, 0.0, MAX_SWEEP_DISTANCE))
