"""第 8 手终局的对手末壶反击筛查收据。

本模块不自己假装枚举连续空间。严格 PhysX 搜索由
``planning_proxy.validate_final_defence`` 执行；本文件只把它的有限搜索报告绑定到
实际终局壶面，并把结果交给 GoalState 验收门。

“未发现反例”始终带有当前候选族、反解算法、物理种子和预算的边界，不能改写成
物理上的绝对安全。
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Literal, Mapping, Sequence


LastReplySearchStatus = Literal[
    "SCREENED_NO_COUNTERPLAY_WITHIN_CURRENT_SEARCH_BUDGET",
    "COUNTERPLAY_FOUND",
    "NOT_RUN",
    "SEARCH_ERROR",
]


def board_fingerprint(board: Sequence[Mapping[str, object]]) -> str:
    """返回与壶序无关、但对 slot/归属/坐标/yaw 敏感的终局指纹。"""

    normalized = []
    for stone in board:
        if not bool(stone.get("enabled", True)):
            continue
        normalized.append({
            "index": int(stone["index"]),
            "owner": str(stone["owner"]),
            # 搜索报告和 PhysX 的 JSON 往返可有浮点尾差；微米级足够区分终局壶面。
            "x": round(float(stone["x"]), 6),
            "y": round(float(stone["y"]), 6),
            "yaw": round(float(stone.get("yaw", 0.0)), 6),
        })
    normalized.sort(key=lambda item: item["index"])
    encoded = json.dumps(normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class LastReplySearchReceipt:
    """一次或多次末壶严格反击搜索的可审计摘要。"""

    status: LastReplySearchStatus
    final_board_fingerprints: tuple[str, ...] = ()
    strict_candidate_count: int = 0
    physics_seeds_per_candidate: int = 0
    counterexample_count: int = 0
    stable_counterexample_count: int = 0
    button_counterexample_count: int = 0
    direct_counterexample_count: int = 0
    impact_counterexample_count: int = 0
    complete_search: bool = False
    detail: str = ""

    def covers(self, final_boards: Sequence[Sequence[Mapping[str, object]]]) -> bool:
        expected = tuple(board_fingerprint(board) for board in final_boards)
        return expected == self.final_board_fingerprints

    @property
    def counterexample_rate(self) -> float | None:
        """完整且同预算筛查后才可用于候选间比较的反例比率。"""

        if not self.complete_search or self.strict_candidate_count < 1:
            return None
        return self.counterexample_count / self.strict_candidate_count


def receipt_from_final_defence_reports(
    final_boards: Sequence[Sequence[Mapping[str, object]]],
    reports: Sequence[Mapping[str, object]],
    *,
    physics_seeds_per_candidate: int,
    complete_search: bool = False,
) -> LastReplySearchReceipt:
    """将 `validate_final_defence` 对每条终局种子的报告编成一份收据。

    调用方必须对 ``final_boards`` 的每一条 PhysX 种子终局各跑一次反击筛查；报告数
    不匹配、零严格候选或字段异常都会拒绝放行，而不是用空报告推断“安全”。
    """

    fingerprints = tuple(board_fingerprint(board) for board in final_boards)
    if len(final_boards) != len(reports):
        return LastReplySearchReceipt(
            "SEARCH_ERROR", fingerprints, detail="每条终局 PhysX 种子必须各有一份末壶反击报告。",
        )
    if physics_seeds_per_candidate < 1:
        return LastReplySearchReceipt(
            "SEARCH_ERROR", fingerprints, detail="末壶反击报告未声明有效的物理种子数。",
        )
    try:
        strict_candidate_count = sum(int(report["strictCandidateCount"]) for report in reports)
        counterexample_count = sum(int(report["counterexampleCandidateCount"]) for report in reports)
        all_screened = all(bool(report["screenedSafe"]) for report in reports)
        stable_counterexample_count = sum(int(report.get("stableCounterexampleCandidateCount", 0)) for report in reports)
        button_counterexample_count = sum(int(report.get("buttonCounterexampleCandidateCount", 0)) for report in reports)
        direct_counterexample_count = sum(int(report.get("directCounterexampleCandidateCount", 0)) for report in reports)
        impact_counterexample_count = sum(int(report.get("impactCounterexampleCandidateCount", 0)) for report in reports)
        report_fingerprints = tuple(
            board_fingerprint(report["fixture"]["stones"])
            for report in reports
        )
    except (KeyError, TypeError, ValueError):
        return LastReplySearchReceipt(
            "SEARCH_ERROR", fingerprints, detail="末壶反击报告字段不完整。",
        )
    if report_fingerprints != fingerprints:
        return LastReplySearchReceipt(
            "SEARCH_ERROR", fingerprints, strict_candidate_count, physics_seeds_per_candidate,
            detail="末壶反击报告所记录的壶面与待验收终局壶面不一致。",
        )
    if strict_candidate_count < 1:
        return LastReplySearchReceipt(
            "SEARCH_ERROR", fingerprints, 0, physics_seeds_per_candidate,
            detail="反击搜索没有严格 PhysX 候选，不能据此放行终局。",
        )
    if counterexample_count > 0 or not all_screened:
        return LastReplySearchReceipt(
            "COUNTERPLAY_FOUND", fingerprints, strict_candidate_count, physics_seeds_per_candidate,
            counterexample_count, stable_counterexample_count, button_counterexample_count,
            direct_counterexample_count, impact_counterexample_count, complete_search,
            "有限末壶反击集合中发现至少一条破局路线。",
        )
    return LastReplySearchReceipt(
        "SCREENED_NO_COUNTERPLAY_WITHIN_CURRENT_SEARCH_BUDGET",
        fingerprints, strict_candidate_count, physics_seeds_per_candidate,
        0, stable_counterexample_count, button_counterexample_count,
        direct_counterexample_count, impact_counterexample_count, complete_search,
        "有限严格 PhysX 反击集合暂未发现反例；不构成连续空间安全证明。",
    )


def bounded_reply_pressure_key(receipt: LastReplySearchReceipt) -> tuple[float, float, float, float]:
    """返回同状态、同搜索预算候选间的末壶压力排序键，越小越好。

顺序体现先手的局面目标：先减少不先撞壶的直接/旋进反击，再减少按钮反例、全部
反例与跨摩擦种子稳定反例。它是有限 PhysX 候选族内的可比较代理，**不是**真实胜率、
连续空间证明或跨不同棋盘状态的全局排序。
    """

    if not receipt.complete_search or receipt.strict_candidate_count < 1:
        raise ValueError("只有完整且非空的末壶搜索才可用于反击压力排序")
    denom = float(receipt.strict_candidate_count)
    return (
        receipt.direct_counterexample_count / denom,
        receipt.button_counterexample_count / denom,
        receipt.counterexample_count / denom,
        receipt.stable_counterexample_count / denom,
    )
