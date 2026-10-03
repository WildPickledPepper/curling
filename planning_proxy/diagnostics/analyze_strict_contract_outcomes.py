"""汇总 profile_k6_search 输出中的严格候选合同结果。

它只分析已严格回放的候选，用于区分“尚未覆盖到足够候选”和“已接近合同但
某个硬条件失败”；不对合同有无解作结论。
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--top", type=int, default=12)
    return parser.parse_args()


def target_from_contract(contract: str) -> tuple[float, float] | None:
    # profile 的合同字符串以 ``...|((x, y),)`` 结尾；仅用于相对落点诊断。
    values = re.findall(r"[-+]?\d+\.\d+", contract)
    if len(values) < 2:
        return None
    return float(values[-2]), float(values[-1])


def summarize(entries: list[dict[str, Any]], top: int) -> dict[str, Any]:
    contract = str(entries[0].get("contract", ""))
    target = target_from_contract(contract)
    total = len(entries)
    valid_rule = 0
    all_clear = 0
    preserve_own = 0
    any_goal = 0
    all_goal = 0
    with_active = 0
    clean_active = 0
    outcome_classes: Counter[str] = Counter()
    nearest: list[dict[str, Any]] = []
    nearest_clean_active: list[dict[str, Any]] = []
    for row in entries:
        outcome = row.get("outcome") or {}
        goal = [bool(value) for value in outcome.get("tacticalGoalMet", [])]
        enemy = [int(value) for value in outcome.get("enemyCleared", [])]
        self_loss = [int(value) for value in outcome.get("totalSelfCleared", [])]
        legal = bool(outcome.get("ruleLegal"))
        cleared = bool(enemy) and min(enemy) >= 1
        preserved = bool(self_loss) and max(self_loss) <= 0
        valid_rule += int(legal)
        all_clear += int(cleared)
        preserve_own += int(preserved)
        any_goal += int(any(goal))
        all_goal += int(bool(goal) and all(goal))
        positions = outcome.get("activeFinalPositions") or []
        active = bool(positions) and not any(point is None for point in positions)
        if not legal:
            outcome_classes["规则不合法"] += 1
        elif not cleared:
            outcome_classes["未清目标"] += 1
        elif not preserved:
            outcome_classes["清目标但损失己方壶"] += 1
        elif not active:
            outcome_classes["清目标保己壶但出手壶离场"] += 1
        elif bool(goal) and all(goal):
            outcome_classes["三种子满足合同"] += 1
        else:
            outcome_classes["清目标保己壶且出手壶在场但未达合同"] += 1
        if not active or target is None:
            continue
        with_active += 1
        distances = [math.dist((float(point[0]), float(point[1])), target) for point in positions]
        candidate = {
            "worstTargetDistance": max(distances),
            "meanTargetDistance": sum(distances) / len(distances),
            "action": row.get("bestshot"),
            "enemyClearedMin": min(enemy, default=0),
            "selfClearedMax": max(self_loss, default=99),
            "ruleLegal": legal,
            "tacticalScores": outcome.get("tacticalScores", []),
            "tacticalGoalMet": goal,
        }
        nearest.append(candidate)
        if legal and cleared and preserved:
            clean_active += 1
            nearest_clean_active.append(candidate)
    nearest.sort(key=lambda item: (float(item["worstTargetDistance"]), float(item["meanTargetDistance"])))
    nearest_clean_active.sort(key=lambda item: (float(item["worstTargetDistance"]), float(item["meanTargetDistance"])))
    return {
        "contract": contract,
        "target": list(target) if target is not None else None,
        "evaluated": total,
        "ruleLegal": valid_rule,
        "allPhysicalClear": all_clear,
        "preservesOwn": preserve_own,
        "anyTacticalGoal": any_goal,
        "allTacticalGoal": all_goal,
        "activeStoneStillInPlay": with_active,
        "cleanClearPreserveActiveCandidates": clean_active,
        "outcomeClassCounts": dict(sorted(outcome_classes.items())),
        "nearestActiveCandidates": nearest[:top],
        "nearestCleanClearPreserveActiveCandidates": nearest_clean_active[:top],
    }


def main() -> None:
    args = parse_args()
    report = json.loads(args.source.read_text(encoding="utf-8"))
    rows = report.get("strictEvaluationSummary")
    if not isinstance(rows, list):
        raise SystemExit("来源报告没有 strictEvaluationSummary；请用新版 profile_k6_search.py 重跑。")
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if isinstance(row, dict) and isinstance(row.get("outcome"), dict):
            groups[str(row.get("contract", "无合同"))].append(row)
    output = {
        "schema": "strict_contract_outcome_analysis_v2",
        "source": str(args.source),
        "strictCandidateCount": len(rows),
        "contracts": [summarize(entries, args.top) for _, entries in sorted(groups.items())],
        "limitation": "严格回放样本未覆盖整个连续空间；未找到合同解不能证明无解。",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"strictCandidateCount": len(rows), "contractCount": len(groups)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
