#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从已有完整对局报告构建真实 fallback/长耗时壶面的代表性测试集。

只提取报告中带 ``game.trace`` 的真实对局记录。每条样本保留原始壶面和来源；
按状态机已声明的语义、壶数和失败模式聚类。跨版本报告仅标为模式挖掘来源，
不被解释成当前版本胜率。
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RUNS = PROJECT_ROOT / "planning_proxy" / "runs"
DEFAULT_OUTPUT = PROJECT_ROOT / "planning_proxy" / "diagnostics" / "representative_failure_corpus.json"
HOUSE_X = 2.375
HOUSE_Y = 4.88
HOUSE_R = 1.83
STONE_R = 0.145


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--slow-seconds", type=float, default=60.0, help="纳入长耗时样本的决策秒数阈值")
    parser.add_argument(
        "--max-independent-per-cluster",
        type=int,
        default=3,
        help="每个语义簇最多保留的不同对局种子数；默认 3，避免正反例被两条样本上限截断",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any] | None:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    return raw if isinstance(raw, dict) else None


def report_games(report: dict[str, Any]) -> list[dict[str, Any]]:
    """兼容单局 ``game`` 与评测批次 ``games`` 两种已存报告格式。"""

    game = report.get("game")
    if isinstance(game, dict):
        return [game]
    games = report.get("games")
    return [item for item in games if isinstance(item, dict)] if isinstance(games, list) else []


def board_summary(
    states: list[dict[str, Any]], acting_team: str | None, target_index: int | None,
) -> dict[str, Any]:
    enabled = [
        {"index": int(index), "x": float(state["x"]), "y": float(state["y"]), "yaw": float(state.get("yaw", 0.0))}
        for index, state in enumerate(states)
        if bool(state.get("enabled", False))
    ]
    own = opponent = own_house = opponent_house = 0
    if acting_team in {"first", "second"}:
        acting_parity = 0 if acting_team == "first" else 1
        own = sum(int(item["index"]) % 2 == acting_parity for item in enabled)
        opponent = len(enabled) - own
        own_house = sum(
            int(item["index"]) % 2 == acting_parity
            and math.hypot(float(item["x"]) - HOUSE_X, float(item["y"]) - HOUSE_Y) <= HOUSE_R + STONE_R
            for item in enabled
        )
        opponent_house = sum(
            int(item["index"]) % 2 != acting_parity
            and math.hypot(float(item["x"]) - HOUSE_X, float(item["y"]) - HOUSE_Y) <= HOUSE_R + STONE_R
            for item in enabled
        )
    target = next((item for item in enabled if int(item["index"]) == target_index), None)
    return {
        "enabledStoneCount": len(enabled),
        "ownStoneCount": own,
        "opponentStoneCount": opponent,
        "ownHouseStoneCount": own_house,
        "opponentHouseStoneCount": opponent_house,
        "target": None if target is None else {
            "index": int(target["index"]),
            "x": float(target["x"]),
            "y": float(target["y"]),
            "dxFromHouseCentre": float(target["x"]) - HOUSE_X,
            "dyFromHouseCentre": float(target["y"]) - HOUSE_Y,
        },
        "stones": enabled,
    }


def event_kind(detail: dict[str, Any], decision_seconds: float, slow_seconds: float) -> list[str]:
    kinds: list[str] = []
    mode = str(detail.get("mode", ""))
    reason = str(detail.get("fallbackReason", ""))
    if "fallback" in mode.lower() or reason:
        kinds.append("fallback")
    if bool(detail.get("plannerBudgetExceeded", False)):
        kinds.append("planner_budget_exceeded")
    if decision_seconds >= slow_seconds:
        kinds.append("slow_decision")
    return kinds


def reply_summary(
    trace: list[dict[str, Any]],
    row: dict[str, Any],
    acting_team: str,
) -> dict[str, Any] | None:
    """记录该手之后真实对手回应造成的壶损失。

    只作失败模式标签：不推断对手策略，也不把历史 K16 当成当前版本价值结论。
    """

    try:
        next_shot = int(row.get("shot", -1)) + 1
    except (TypeError, ValueError):
        return None
    def is_reply(item: object) -> bool:
        if not isinstance(item, dict):
            return False
        try:
            return int(item.get("shot", -1)) == next_shot
        except (TypeError, ValueError):
            return False

    reply = next((item for item in trace if is_reply(item)), None)
    if not isinstance(reply, dict) or str(reply.get("team", "")) == acting_team:
        return None
    before = row.get("stateAfter")
    after = reply.get("stateAfter")
    if not isinstance(before, list) or not isinstance(after, list):
        return None
    parity = 0 if acting_team == "first" else 1
    own_before = [index for index, state in enumerate(before) if bool(state.get("enabled", False)) and index % 2 == parity]
    own_after = [index for index, state in enumerate(after) if bool(state.get("enabled", False)) and index % 2 == parity]
    removed = sorted(set(own_before) - set(own_after))
    return {
        "shot": next_shot,
        "bestshot": reply.get("bestshot"),
        "cleared": reply.get("cleared"),
        "actingSideOwnBefore": own_before,
        "actingSideOwnAfter": own_after,
        "actingSideOwnRemoved": removed,
        "actingSideOwnRemovedCount": len(removed),
        "scoreAfterReply": reply.get("temporaryScoreFirst"),
    }


def main() -> None:
    args = parse_args()
    if int(args.max_independent_per_cluster) < 1:
        raise SystemExit("--max-independent-per-cluster 必须至少为 1")
    entries: list[dict[str, Any]] = []
    scanned_reports = 0
    for path in sorted(args.runs_dir.rglob("*.json")):
        report = load_json(path)
        if report is None:
            continue
        for game in report_games(report):
            trace = game.get("trace")
            if not isinstance(trace, list):
                continue
            scanned_reports += 1
            for row in trace:
                if not isinstance(row, dict):
                    continue
                detail = row.get("detail")
                states = row.get("stateBefore")
                if not isinstance(detail, dict) or not isinstance(states, list):
                    continue
                seconds = float(row.get("decisionSeconds", 0.0) or 0.0)
                kinds = event_kind(detail, seconds, float(args.slow_seconds))
                if not kinds:
                    continue
                plan = detail.get("firstPlayerPlan") if isinstance(detail.get("firstPlayerPlan"), dict) else {}
                team = str(row.get("team", ""))
                target_value = plan.get("target_opponent_index")
                target_index = int(target_value) if isinstance(target_value, int) else None
                board = board_summary(states, team, target_index)
                semantic = {
                    "shot": int(row.get("shot", -1)),
                    "team": team,
                    "situationType": str(plan.get("situation_type", "UNKNOWN")),
                    "phase": str(plan.get("phase", "UNKNOWN")),
                    "strategyType": str(plan.get("strategy_type", "UNKNOWN")),
                    "opponentAction": str(plan.get("opponent_action", "UNKNOWN")),
                    "failureKinds": kinds,
                    "enabledStoneCount": int(board["enabledStoneCount"]),
                    "ownStoneCount": int(board["ownStoneCount"]),
                    "opponentStoneCount": int(board["opponentStoneCount"]),
                    "ownHouseStoneCount": int(board["ownHouseStoneCount"]),
                    "opponentHouseStoneCount": int(board["opponentHouseStoneCount"]),
                }
                cluster_key = "|".join(str(semantic[key]) for key in (
                    "shot", "team", "situationType", "phase", "strategyType",
                    "opponentAction", "enabledStoneCount", "ownStoneCount", "opponentStoneCount",
                    "ownHouseStoneCount", "opponentHouseStoneCount",
                ))
                entries.append({
                    "clusterKey": cluster_key,
                    "semantic": semantic,
                    "source": str(path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
                    "matchSeed": game.get("seed"),
                    "shot": int(row.get("shot", -1)),
                    "decisionSeconds": seconds,
                    "mode": detail.get("mode"),
                    "fallbackReason": detail.get("fallbackReason"),
                    "bestshot": row.get("bestshot"),
                    "temporaryScoreFirst": row.get("temporaryScoreFirst"),
                    "finalScoreProxy": game.get("finalScoreProxy"),
                    "winner": game.get("winner"),
                    "board": board,
                    "firstPlayerPlan": plan,
                    "nextOpponentReply": reply_summary(trace, row, team),
                    "evidenceScope": "historical report; version compatibility must be verified before current causal comparison",
                })

    clusters: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        clusters[str(entry["clusterKey"])].append(entry)
    representatives: list[dict[str, Any]] = []
    candidate_test_cases: list[dict[str, Any]] = []
    for key, group in sorted(clusters.items(), key=lambda item: (-len(item[1]), item[0])):
        ordered = sorted(group, key=lambda item: float(item["decisionSeconds"]), reverse=True)
        selected: list[dict[str, Any]] = []
        seen_seeds: set[str] = set()
        for item in ordered:
            # 同一 seed 的不同旧版本报告可保留在 cluster 里，但不能伪装成
            # 独立测试盘面。优先保留多个不同 seed；不能让同一状态簇的
            # 第三个反例仅因历史抽样上限而从回归集中消失。
            seed_key = str(item.get("matchSeed"))
            if seed_key in seen_seeds:
                continue
            seen_seeds.add(seed_key)
            selected.append(item)
            if len(selected) >= int(args.max_independent_per_cluster):
                break
        representatives.append({
            "clusterKey": key,
            "count": len(group),
            "semantic": ordered[0]["semantic"],
            "representative": ordered[0],
            "independentSources": sorted({str(item["source"]) for item in group}),
            "decisionSeconds": {
                "max": max(float(item["decisionSeconds"]) for item in group),
                "min": min(float(item["decisionSeconds"]) for item in group),
            },
        })
        for index, item in enumerate(selected, 1):
            candidate_test_cases.append({
                "id": f"{len(candidate_test_cases) + 1:03d}",
                "clusterKey": key,
                "independentRankWithinCluster": index,
                "source": item["source"],
                "matchSeed": item["matchSeed"],
                "shot": item["shot"],
                "semantic": item["semantic"],
                "historicalObservation": {
                    "decisionSeconds": item["decisionSeconds"],
                    "mode": item["mode"],
                    "fallbackReason": item["fallbackReason"],
                    "winner": item["winner"],
                    "finalScoreProxy": item["finalScoreProxy"],
                },
                "nextOpponentReply": item["nextOpponentReply"],
                "requiredBeforeUse": [
                    "在当前代码与当前严格扩展下恢复 stateBefore",
                    "验证恢复壶面、当前合同和物理种子可重放",
                    "历史标签仅用于模式检索；不得当作当前版本结论",
                ],
            })
    report = {
        "schema": "representative_real_failure_corpus_v2",
        "scope": "historical evidence for test-set construction; not a current-version win-rate report",
        "runsDirectory": str(args.runs_dir),
        "slowDecisionThresholdSeconds": float(args.slow_seconds),
        "maxIndependentPerCluster": int(args.max_independent_per_cluster),
        "scannedReportsWithTrace": scanned_reports,
        "eventCount": len(entries),
        "clusterCount": len(representatives),
        "failureKindCounts": dict(Counter(kind for entry in entries for kind in entry["semantic"]["failureKinds"])),
        "clusters": representatives,
        "candidateTestCases": candidate_test_cases,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "scannedReportsWithTrace": scanned_reports,
        "eventCount": len(entries),
        "clusterCount": len(representatives),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
