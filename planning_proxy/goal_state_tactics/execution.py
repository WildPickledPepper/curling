"""GoalState 的终局验收与搜索结果回退编排，不包含任何路径搜索。"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from typing import Any, Callable, Literal, Mapping, Sequence, TypeVar

from .models import LastReplyPolicy, OccupancyConstraint
from .proposer import BoundStoneConstraint, GoalProposalSet, ProposedGoal
from .last_reply import LastReplySearchReceipt, bounded_reply_pressure_key


@dataclass(frozen=True)
class GoalAcceptance:
    accepted: bool
    failures_by_seed: tuple[tuple[str, ...], ...]
    last_reply_search_status: str | None = None


T = TypeVar("T")


SearchStatus = Literal[
    "ACCEPTED",
    "NOT_FOUND_WITHIN_CURRENT_SEARCH_BUDGET",
    "REJECTED_BY_GOAL_GATE",
    "SEARCH_ERROR",
]


@dataclass(frozen=True)
class SearchAttempt:
    """一次规划调用的认识论结果，而不是物理可达性的证明。

    ``NOT_FOUND_WITHIN_CURRENT_SEARCH_BUDGET`` 的含义严格限于本次候选覆盖、算法和
    时间/计算预算；它不能被上层翻译成“物理无解”。
    """

    status: SearchStatus
    solution: Any | None = None
    detail: str | None = None


@dataclass(frozen=True)
class StrictGoalSolution:
    """路径层找到的参数及其每条 PhysX 摩擦种子终局。

    ``payload`` 可以保存 v/h/w、轨迹或规划器原始诊断；战术模块只依赖规则标记和
    终局棋盘，故不把某一种反解器的数据结构耦合进来。
    """

    payload: Any
    final_boards: Sequence[Sequence[Mapping[str, object]]]
    rule_legal: bool
    last_reply_receipt: LastReplySearchReceipt | None = None


@dataclass(frozen=True)
class FallbackResult:
    selected: ProposedGoal | None
    solution: Any | None
    attempted_transition_ids: tuple[str, ...]
    attempts: tuple[SearchAttempt, ...]


@dataclass(frozen=True)
class K8PressureRank:
    """同一 K8 当前状态中、一条已完整筛查候选的可审计排序项。"""

    proposal: ProposedGoal
    solution: StrictGoalSolution
    pressure_key: tuple[float, float, float, float]


@dataclass(frozen=True)
class GoalScreenResult:
    """一条 GoalState 在严格终局与末壶门后的完整筛查结果。"""

    proposal: ProposedGoal
    attempt: SearchAttempt


def accept_bound_goal(
    final_boards: Sequence[Sequence[Mapping[str, object]]],
    constraints: Sequence[BoundStoneConstraint],
    *, rule_legal: bool,
    occupancy_constraints: Sequence[OccupancyConstraint] = (),
    require_last_reply_search: bool = False,
    last_reply_policy: LastReplyPolicy = "REQUIRE_SEARCH_RECORD",
    last_reply_receipt: LastReplySearchReceipt | None = None,
) -> GoalAcceptance:
    """严格检查每条摩擦序列的终局是否满足已绑定 GoalState。

    规划器或严格 PhysX 调用方应先把每条种子的最终在场壶导出为 ``final_boards``。
    任一序列违规、目标壶存活或落在区域外，均不能接受该路径。
    """

    if not rule_legal:
        return GoalAcceptance(False, (("free_guard_or_other_rule_violation",),))
    if require_last_reply_search:
        if last_reply_receipt is None:
            return GoalAcceptance(False, (("last_reply_search_not_completed",),))
        if not last_reply_receipt.covers(final_boards):
            return GoalAcceptance(
                False, (("last_reply_search_board_mismatch",),), last_reply_receipt.status,
            )
        if (
            last_reply_receipt.status == "COUNTERPLAY_FOUND"
            and last_reply_policy == "REQUIRE_NO_COUNTERPLAY"
        ):
            return GoalAcceptance(
                False, (("last_reply_counterplay_found",),), last_reply_receipt.status,
            )
        if last_reply_receipt.status not in {
            "SCREENED_NO_COUNTERPLAY_WITHIN_CURRENT_SEARCH_BUDGET",
            "COUNTERPLAY_FOUND",
        }:
            return GoalAcceptance(
                False, (("last_reply_search_not_accepted",),), last_reply_receipt.status,
            )
    failures: list[tuple[str, ...]] = []
    for board in final_boards:
        by_index = {int(stone["index"]): stone for stone in board if bool(stone.get("enabled", True))}
        failed: list[str] = []
        for constraint in constraints:
            if constraint.stone_index is None:
                failed.append(f"{constraint.role}:active_slot_unbound")
                continue
            stone = by_index.get(int(constraint.stone_index))
            if constraint.disposition == "OUT_OF_PLAY":
                if stone is not None:
                    failed.append(f"{constraint.role}:still_in_play")
            elif constraint.disposition == "SURVIVE":
                if stone is None:
                    failed.append(f"{constraint.role}:not_in_play")
            elif constraint.disposition == "IN_REGION":
                region = constraint.final_region
                if stone is None:
                    failed.append(f"{constraint.role}:not_in_play")
                elif region is None:
                    failed.append(f"{constraint.role}:missing_region")
                elif math.hypot(float(stone["x"]) - region.centre_x, float(stone["y"]) - region.centre_y) > region.radius_m:
                    failed.append(f"{constraint.role}:outside_region")
            else:
                failed.append(f"{constraint.role}:unknown_disposition")
        for occupancy in occupancy_constraints:
            count = sum(
                1 for stone in board
                if bool(stone.get("enabled", True))
                and str(stone.get("owner")) == occupancy.owner
                and math.hypot(float(stone["x"]) - occupancy.region.centre_x, float(stone["y"]) - occupancy.region.centre_y)
                <= occupancy.region.radius_m
            )
            if count < occupancy.min_count:
                failed.append(f"occupancy:{occupancy.owner}:{occupancy.region.region_id}:below_min")
            if occupancy.max_count is not None and count > occupancy.max_count:
                failed.append(f"occupancy:{occupancy.owner}:{occupancy.region.region_id}:above_max")
        failures.append(tuple(failed))
    return GoalAcceptance(
        not any(failures), tuple(failures),
        None if last_reply_receipt is None else last_reply_receipt.status,
    )


def solve_with_fallback(
    proposal_set: GoalProposalSet,
    attempt: Callable[[ProposedGoal], SearchAttempt | T | None],
) -> FallbackResult:
    """依优先级调用外部路径规划器，并保留每次搜索的真实结论。

    为兼容早期接入，回调返回非 ``None`` 的普通对象会视为已接受的解；返回 ``None``
    仅规范化为“当前预算未找到”，绝不表示物理无解。新接入应显式返回
    :class:`SearchAttempt`，从而区分搜索预算不足、终局门拒绝及搜索错误。
    """

    attempted: list[str] = []
    records: list[SearchAttempt] = []
    for proposal in proposal_set.proposals:
        attempted.append(proposal.goal.transition_id)
        raw_result = attempt(proposal)
        if isinstance(raw_result, SearchAttempt):
            result = raw_result
        elif raw_result is None:
            result = SearchAttempt("NOT_FOUND_WITHIN_CURRENT_SEARCH_BUDGET")
        else:
            result = SearchAttempt("ACCEPTED", solution=raw_result)
        records.append(result)
        if result.status == "ACCEPTED" and result.solution is not None:
            return FallbackResult(proposal, result.solution, tuple(attempted), tuple(records))
    return FallbackResult(None, None, tuple(attempted), tuple(records))


def _verify_strict_attempt(
    proposal: ProposedGoal,
    result: SearchAttempt,
    *,
    screen_last_reply: Callable[[ProposedGoal, StrictGoalSolution], LastReplySearchReceipt] | None,
) -> SearchAttempt:
    """将路径层原始结果送过严格终局与末壶门。"""

    if not isinstance(result, SearchAttempt):
        return SearchAttempt("SEARCH_ERROR", detail="严格执行器要求路径层返回 SearchAttempt。")
    if result.status != "ACCEPTED":
        return result
    if not isinstance(result.solution, StrictGoalSolution):
        return SearchAttempt("SEARCH_ERROR", detail="ACCEPTED 结果缺少 StrictGoalSolution 终局证据。")
    solution = result.solution
    geometry = accept_bound_goal(
        solution.final_boards, proposal.bound_stone_constraints,
        rule_legal=solution.rule_legal,
        occupancy_constraints=proposal.goal.occupancy_constraints,
    )
    if not geometry.accepted:
        return SearchAttempt(
            "REJECTED_BY_GOAL_GATE",
            detail="严格终局门拒绝：" + ";".join(geometry.failures_by_seed[0]),
        )
    receipt = None
    if proposal.goal.require_last_reply_search:
        if screen_last_reply is None:
            return SearchAttempt("REJECTED_BY_GOAL_GATE", detail="第 8 手缺少对手末壶反击搜索。")
        try:
            receipt = screen_last_reply(proposal, solution)
        except Exception as exc:  # 路径端异常不能伪装为战术不可行。
            return SearchAttempt("SEARCH_ERROR", detail=f"末壶反击搜索异常：{exc}")
    accepted = accept_bound_goal(
        solution.final_boards, proposal.bound_stone_constraints,
        rule_legal=solution.rule_legal,
        occupancy_constraints=proposal.goal.occupancy_constraints,
        last_reply_policy=proposal.goal.last_reply_policy,
        require_last_reply_search=proposal.goal.require_last_reply_search,
        last_reply_receipt=receipt,
    )
    if not accepted.accepted:
        return SearchAttempt(
            "REJECTED_BY_GOAL_GATE",
            detail="终局验收拒绝：" + ";".join(accepted.failures_by_seed[0]),
        )
    return SearchAttempt("ACCEPTED", solution=replace(solution, last_reply_receipt=receipt))


def screen_all_strict_goals(
    proposal_set: GoalProposalSet,
    attempt: Callable[[ProposedGoal], SearchAttempt],
    *,
    screen_last_reply: Callable[[ProposedGoal, StrictGoalSolution], LastReplySearchReceipt] | None = None,
) -> tuple[GoalScreenResult, ...]:
    """筛查全部候选，不在第一条成功边停止，供 K8 同状态压力比较使用。"""

    return tuple(
        GoalScreenResult(proposal, _verify_strict_attempt(
            proposal, attempt(proposal), screen_last_reply=screen_last_reply,
        ))
        for proposal in proposal_set.proposals
    )


def solve_strict_goal_with_fallback(
    proposal_set: GoalProposalSet,
    attempt: Callable[[ProposedGoal], SearchAttempt],
    *,
    screen_last_reply: Callable[[ProposedGoal, StrictGoalSolution], LastReplySearchReceipt] | None = None,
) -> FallbackResult:
    """执行完整的“规划 → 严格终局门 → 末壶反击门 → 回退”控制流。

    这是路径层与战术层的唯一耦合点：路径层提供 :class:`StrictGoalSolution`，而本函数
    保证它不能绕过 GoalState 约束。第 8 手若没有 ``screen_last_reply``，或其报告发现
    不覆盖所有我方终局种子、未运行或搜索异常都会把该边记录为
    ``REJECTED_BY_GOAL_GATE`` 并继续尝试回退边。默认 K8 策略只要求末壶搜索被完成
    并留下反击记录；发现反例并不自动等价于本手无效，因先手目标可以是迫使对手走
    高难度窄门，而非保证对手绝不取分。仅显式 ``REQUIRE_NO_COUNTERPLAY`` 的安全声明
    才会因反例而拒绝。
    """

    return solve_with_fallback(
        proposal_set,
        lambda proposal: _verify_strict_attempt(
            proposal, attempt(proposal), screen_last_reply=screen_last_reply,
        ),
    )


def rank_same_state_k8_by_reply_pressure(
    candidates: Sequence[tuple[ProposedGoal, StrictGoalSolution]],
) -> tuple[K8PressureRank, ...]:
    """在同一源状态、相同完整筛查预算下按对手末壶压力排序。

    这不是跨 K8 状态的“哪个战术更强”函数。调用方必须先保证候选来自同一实际棋盘的
    同一 ``source_state``，并以同一反击候选族和物理种子预算筛查完毕；本函数会拒绝
    缺少完整收据或混合源状态的输入。历史支持度仅在压力键完全相同时作为最后的稳定
    tie-break，不能覆盖 PhysX 反击证据。
    """

    if not candidates:
        return ()
    source_states = {proposal.goal.source_state for proposal, _ in candidates}
    if len(source_states) != 1:
        raise ValueError("末壶压力排序只允许同一 source_state 的候选")
    ranked: list[K8PressureRank] = []
    for proposal, solution in candidates:
        if not proposal.goal.require_last_reply_search:
            raise ValueError("压力排序只适用于要求末壶搜索的 K8 GoalState")
        receipt = solution.last_reply_receipt
        if receipt is None:
            raise ValueError("K8 候选缺少末壶反击搜索收据")
        ranked.append(K8PressureRank(proposal, solution, bounded_reply_pressure_key(receipt)))
    return tuple(sorted(
        ranked,
        key=lambda item: (item.pressure_key, item.proposal.goal.priority, -item.proposal.support, item.proposal.goal.transition_id),
    ))


def rank_k8_proposal_set_by_reply_pressure(
    proposal_set: GoalProposalSet,
    screened: Sequence[GoalScreenResult],
) -> tuple[K8PressureRank, ...]:
    """对一次当前壶面生成的 K8 全部候选进行压力排序。

    同一真实棋盘可能同时有 collision/core/zone 三种历史抽象；它们的
    ``GoalState.source_state`` 字符串不同，却属于同一个 ``GoalProposalSet``。因此
    运行时比较的边界应是本次集合的规范 ``runtime_core_state``，而非历史工件的来源
    字符串。传入结果必须恰好来自该集合，防止把另一个棋盘或另一轮反解混进来。
    """

    if proposal_set.own_throw_number != 8:
        raise ValueError("末壶压力排序只适用于 own_throw_number=8")
    expected = tuple(item.goal.transition_id for item in proposal_set.proposals)
    actual = tuple(item.proposal.goal.transition_id for item in screened)
    if actual != expected:
        raise ValueError("筛查结果必须按原顺序完整覆盖同一个 GoalProposalSet")
    accepted = tuple(
        (item.proposal, item.attempt.solution)
        for item in screened
        if item.attempt.status == "ACCEPTED"
        and isinstance(item.attempt.solution, StrictGoalSolution)
        and item.proposal.goal.require_last_reply_search
    )
    # 这里不调用 rank_same_state...，因为 collision/core/zone 的历史标签允许不同；
    # ProposalSet 本身已提供更强的“同一实际壶面”边界。
    ranked: list[K8PressureRank] = []
    for proposal, solution in accepted:
        receipt = solution.last_reply_receipt
        if receipt is None:
            raise ValueError("K8 候选缺少末壶反击搜索收据")
        ranked.append(K8PressureRank(proposal, solution, bounded_reply_pressure_key(receipt)))
    return tuple(sorted(
        ranked,
        key=lambda item: (item.pressure_key, item.proposal.goal.priority, -item.proposal.support, item.proposal.goal.transition_id),
    ))
