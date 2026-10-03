"""终局约束战术模块。

该包只负责把当前局面映射为按优先级排列的 :class:`GoalState`。
它不输出 ``v/h/w``，也不调用 PhysX；连续规划器负责将当前棋盘反解到
``GoalState``，失败时由调用方尝试下一条回退边。
"""

from .models import (
    CircleRegion,
    GoalState,
    LastReplyPolicy,
    OccupancyConstraint,
    StoneConstraint,
    StoneSelector,
)
from .proposer import BoundStoneConstraint, GoalProposalSet, ProposedGoal, propose_goal_states
from .execution import (
    GoalAcceptance,
    FallbackResult,
    GoalScreenResult,
    K8PressureRank,
    SearchAttempt,
    StrictGoalSolution,
    accept_bound_goal,
    rank_same_state_k8_by_reply_pressure,
    rank_k8_proposal_set_by_reply_pressure,
    solve_strict_goal_with_fallback,
    screen_all_strict_goals,
    solve_with_fallback,
)
from .last_reply import (
    LastReplySearchReceipt,
    board_fingerprint,
    bounded_reply_pressure_key,
    receipt_from_final_defence_reports,
)

__all__ = [
    "CircleRegion",
    "GoalState",
    "LastReplyPolicy",
    "OccupancyConstraint",
    "StoneConstraint",
    "StoneSelector",
    "BoundStoneConstraint",
    "GoalProposalSet",
    "ProposedGoal",
    "propose_goal_states",
    "GoalAcceptance",
    "FallbackResult",
    "GoalScreenResult",
    "K8PressureRank",
    "SearchAttempt",
    "StrictGoalSolution",
    "accept_bound_goal",
    "rank_same_state_k8_by_reply_pressure",
    "rank_k8_proposal_set_by_reply_pressure",
    "solve_with_fallback",
    "solve_strict_goal_with_fallback",
    "screen_all_strict_goals",
    "LastReplySearchReceipt",
    "board_fingerprint",
    "bounded_reply_pressure_key",
    "receipt_from_final_defence_reports",
]
