#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""汇总已有严格 PhysX 对局中的先手状态机证据。

只读取真实对局回放：每条样本都保留原始文件、种子、对手、每手入局壶面、
当时实际执行合同和最终比分。它不读取 ``ideal_state_machine`` 结果，也不把
不同版本的同种子回放当作重复实验自动合并。

用途是先回答两个可核查的问题：
1. 当前状态机在历史真实壶面上会把它们归到哪一种状态；
2. 每一种状态在已有不同对手/种子中，实际执行的是原合同、降级合同，还是
   安全回退，以及这些样本最后是胜、平还是负。
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from planning_proxy.first_player_strategy import plan_first_player_turn  # noqa: E402


RUNS = ROOT / "planning_proxy" / "runs"
DEFAULT_OUTPUT = RUNS / "first_player_state_data_audit.json"


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def board_for_first_player(states: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """由真实 slot 恢复先手视角，slot 偶数为先手。"""

    board: list[dict[str, Any]] = []
    for index, state in enumerate(states):
        if not bool(state.get("enabled", False)):
            continue
        board.append({
            "index": int(index),
            "owner": "self" if index % 2 == 0 else "opponent",
            "x": float(state["x"]),
            "y": float(state["y"]),
            "enabled": True,
        })
    return board


def terminal_result(game: dict[str, Any]) -> str:
    score = game.get("finalScoreProxy")
    if score is None:
        # 旧报告只留 finalScoreFirst；本审计只收 proxyTeam=0 的先手回放，
        # 故它与 proxy 视角同号。
        score = game.get("finalScoreFirst")
    try:
        score_value = int(score)
    except (TypeError, ValueError):
        return "未知"
    return "胜" if score_value > 0 else "平" if score_value == 0 else "负"


def plan_execution_kind(detail: dict[str, Any]) -> str:
    """区分原合同、执行层降级和安全回退；不根据 mode 名字猜战术。"""

    if not isinstance(detail, dict):
        return "无规划详情"
    if detail.get("fallbackReason"):
        return "安全回退"
    current = detail.get("firstPlayerPlan")
    original = detail.get("fallbackFromPlan")
    if isinstance(current, dict) and isinstance(original, dict):
        current_phase = current.get("phase")
        original_phase = original.get("phase")
        if current_phase != original_phase:
            return "执行层改写合同"
    return "原合同"


def classify_file(path: Path, *, include_partial: bool = False) -> list[dict[str, Any]]:
    report = read_json(path)
    if report is None or "ideal_state_machine" in path.name:
        return []
    games = report.get("games")
    if not isinstance(games, list):
        return []
    rows: list[dict[str, Any]] = []
    opponent = str(report.get("opponent", "未知"))
    for game_index, game in enumerate(games, start=1):
        # 对局报告用 first/second 表示代理的颜色；只有 first 才使用本文件
        # 的先手状态机，且偶数 slot 属于己方。
        if not isinstance(game, dict) or str(game.get("proxyTeam", "")) != "first":
            continue
        trace = game.get("trace")
        if not isinstance(trace, list):
            continue
        # 状态—胜负关联只能使用真正结束的一局。``stop8``、``shot12`` 等
        # 回放很适合研究某个几何入口，却没有最终比分的统计含义；默认完全
        # 排除，除非调用者显式要求列出部分回放。
        completed = bool(game.get("completedEnd", False)) and len(trace) >= 16
        if not completed and not include_partial:
            continue
        result = terminal_result(game)
        for turn in trace:
            if not isinstance(turn, dict) or turn.get("actor") != "proxy":
                continue
            shot_index = int(turn.get("shot", 0)) - 1
            if shot_index < 0 or shot_index % 2:
                continue
            states = turn.get("stateBefore")
            if not isinstance(states, list):
                continue
            current_plan = plan_first_player_turn(board_for_first_player(states), shot_index)
            detail = turn.get("detail") if isinstance(turn.get("detail"), dict) else {}
            executed = detail.get("firstPlayerPlan") if isinstance(detail.get("firstPlayerPlan"), dict) else {}
            strict = detail.get("strict") if isinstance(detail.get("strict"), dict) else {}
            goal = strict.get("tactical_goal_met")
            goal_all_seeds = bool(isinstance(goal, list) and goal and all(goal))
            rows.append({
                "source": path.name,
                "game": int(game_index),
                "opponent": opponent,
                "seed": game.get("seed"),
                "shot": shot_index + 1,
                "k": shot_index // 2 + 1,
                "finalResult": result,
                "finalScoreProxy": game.get("finalScoreProxy", game.get("finalScoreFirst")),
                "currentSituation": current_plan.situation_type,
                "currentStrategy": current_plan.strategy_type,
                "historicalSituation": executed.get("situation_type"),
                "historicalStrategy": executed.get("strategy_type"),
                "historicalPhase": executed.get("phase"),
                "executionKind": plan_execution_kind(detail),
                "mode": detail.get("mode"),
                "strictGoalAllSeeds": goal_all_seeds if goal is not None else None,
                "decisionSeconds": turn.get("decisionSeconds"),
                "stateBefore": states,
            })
    return rows


def summarise(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(row["currentSituation"], row["currentStrategy"], row["executionKind"])].append(row)
    result: list[dict[str, Any]] = []
    for (situation, strategy, execution), items in sorted(groups.items()):
        outcome = Counter(item["finalResult"] for item in items)
        strict_known = [item["strictGoalAllSeeds"] for item in items if item["strictGoalAllSeeds"] is not None]
        result.append({
            "currentSituation": situation,
            "currentStrategy": strategy,
            "executionKind": execution,
            "samples": len(items),
            "wins": outcome["胜"], "draws": outcome["平"], "losses": outcome["负"],
            "strictGoalPasses": sum(bool(value) for value in strict_known),
            "strictGoalKnown": len(strict_known),
            "opponents": dict(sorted(Counter(item["opponent"] for item in items).items())),
            "sources": sorted({item["source"] for item in items}),
        })
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=Path, default=RUNS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--include-partial", action="store_true", help="额外纳入未完成的诊断回放；不应用于胜率统计")
    args = parser.parse_args()

    rows: list[dict[str, Any]] = []
    for path in sorted(args.runs.glob("*.json")):
        rows.extend(classify_file(path, include_partial=bool(args.include_partial)))
    payload = {
        "schema": "first_player_state_data_audit_v1",
        "meaning": (
            "历史真实严格 PhysX 回放的先手状态审计。不同文件可能对应不同代码版本，"
            "因此保留 source，不把它们合成同一轮独立胜率试验。默认只包含完整 16 壶对局。"
        ),
        "sampleCount": len(rows),
        "summaryByCurrentStateAndExecution": summarise(rows),
        "samples": rows,
    }
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "output": str(args.output), "sampleCount": len(rows),
        "stateGroups": len(payload["summaryByCurrentStateAndExecution"]),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
