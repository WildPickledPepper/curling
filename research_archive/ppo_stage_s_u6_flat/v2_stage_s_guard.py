"""Pure-geometry Stage S endgame guards shared by local and Socket inference."""

from __future__ import annotations

from typing import Dict, Sequence

from ppo_actions import action_id
from ppo_state_reward import summarize_position


AROUND_GUARD_DRAW_LEFT = action_id("around_guard_draw_left")
PEEL_GUARD = action_id("peel_guard")
HIT_ROLL_RIGHT = action_id("hit_roll_right")


def should_override_p1_peel_guard(
    position: Sequence[float],
    *,
    candidate_is_first: bool,
    shot_num: int,
    prior_action: int,
    action_mask: Sequence[bool],
    bypass_diagnostics: Dict[str, Dict[str, object]],
) -> bool:
    """Return whether the approved P1 final-shot defensive peel applies."""
    bypass_available = any(
        bool(detail.get("available")) for detail in bypass_diagnostics.values()
    )
    current_score = int(summarize_position(position, candidate_is_first)["score_for_my"])
    return bool(
        candidate_is_first
        and int(shot_num) == 14
        and current_score <= 0
        and int(prior_action) == AROUND_GUARD_DRAW_LEFT
        and bool(action_mask[PEEL_GUARD])
        and bypass_available
    )


def should_override_p2_blocked_draw(
    position: Sequence[float],
    *,
    candidate_is_first: bool,
    shot_num: int,
    prior_action: int,
    action_mask: Sequence[bool],
    bypass_diagnostics: Dict[str, Dict[str, object]],
) -> bool:
    """Return whether the approved-for-testing P2 blocked button draw applies."""
    current_score = int(summarize_position(position, candidate_is_first)["score_for_my"])
    draw_available = bool(
        bypass_diagnostics.get("around_guard_draw_left", {}).get("available")
    )
    return bool(
        not candidate_is_first
        and int(shot_num) == 15
        and current_score <= 0
        and int(prior_action) == HIT_ROLL_RIGHT
        and bool(action_mask[AROUND_GUARD_DRAW_LEFT])
        and draw_available
    )
