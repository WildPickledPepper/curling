#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按真实入局壶面分组历史对局，区分“可比较对照”与跨版本线索。

历史 runs 中同一个物理种子常被不同版本重复使用；若更早的一手不同，后半局
的 K6/K7 不是同一输入，不能把终局差异归因给某一条状态机边。本审计以某一手
``stateBefore`` 的全部启用壶（编号、x/y/yaw）和局种子为指纹：只有指纹相同的
报告才构成同盘面续局对照。默认检查 K6（shot=11；内部 shot index=10）。
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "planning_proxy" / "runs"
DEFAULT_OUTPUT = RUNS / "state_input_lineage_audit.json"


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def games_in(report: dict[str, Any]) -> Iterable[dict[str, Any]]:
    games = report.get("games")
    if isinstance(games, list):
        yield from (item for item in games if isinstance(item, dict))
    game = report.get("game")
    if isinstance(game, dict):
        yield game


def input_fingerprint(states: list[dict[str, Any]]) -> tuple[str, list[dict[str, Any]]]:
    """返回可读的规范化状态和稳定短哈希；保留 yaw，避免只看落点的伪同盘面。"""

    normalized = []
    for index, state in enumerate(states):
        if not isinstance(state, dict) or not bool(state.get("enabled", False)):
            continue
        try:
            normalized.append({
                "index": index,
                "x": round(float(state["x"]), 6),
                "y": round(float(state["y"]), 6),
                "yaw": round(float(state.get("yaw", 0.0)), 6),
            })
        except (KeyError, TypeError, ValueError):
            # 坏记录不能成为“同盘面”的证据。
            return "", []
    encoded = json.dumps(normalized, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(encoded.encode("ascii")).hexdigest()[:16], normalized


def result(game: dict[str, Any]) -> str:
    value = game.get("finalScoreProxy", game.get("finalScoreFirst"))
    try:
        score = int(value)
    except (TypeError, ValueError):
        return "未知"
    return "胜" if score > 0 else "平" if score == 0 else "负"


def record_from(path: Path, report: dict[str, Any], game: dict[str, Any], shot: int) -> dict[str, Any] | None:
    # 本工具的结果字段用于比较整局胜负；中途 stop 的单手/两手探针只能说明
    # 局部合同是否可达，不能混进终局因果对照。
    if not bool(game.get("completedEnd")):
        return None
    trace = game.get("trace")
    if not isinstance(trace, list):
        return None
    turn = next((item for item in trace if isinstance(item, dict) and int(item.get("shot", -1)) == shot), None)
    if not isinstance(turn, dict) or str(turn.get("actor")) != "proxy":
        return None
    states = turn.get("stateBefore")
    detail = turn.get("detail")
    if not isinstance(states, list) or not isinstance(detail, dict):
        return None
    fingerprint, normalized = input_fingerprint(states)
    if not fingerprint:
        return None
    plan = detail.get("firstPlayerPlan")
    plan = plan if isinstance(plan, dict) else {}
    return {
        "source": path.name,
        "sourceSchema": report.get("schema", "legacy"),
        "opponent": report.get("opponent", report.get("sourceOpponent", "未知")),
        "seed": game.get("seed", report.get("sourceSeed")),
        "proxyTeam": game.get("proxyTeam"),
        "inputFingerprint": fingerprint,
        "inputState": normalized,
        "shot": shot,
        "plan": {
            "phase": plan.get("phase"),
            "situation": plan.get("situation_type"),
            "strategy": plan.get("strategy_type"),
            "opponentAction": plan.get("opponent_action"),
            "targetPoints": plan.get("target_points"),
        },
        "mode": detail.get("mode"),
        "fallback": bool(detail.get("fallbackReason")),
        "decisionSeconds": detail.get("plannerDecisionSeconds", turn.get("decisionSeconds")),
        "finalScore": game.get("finalScoreProxy", game.get("finalScoreFirst")),
        "finalResult": result(game),
    }


def plan_signature(row: dict[str, Any]) -> tuple[Any, ...]:
    plan = row["plan"]
    return (plan["phase"], plan["strategy"], plan["opponentAction"], json.dumps(plan["targetPoints"], sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=Path, default=RUNS)
    parser.add_argument("--shot", type=int, default=11, help="真实回放中的 shot 编号；11 即 K6")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    rows: list[dict[str, Any]] = []
    for path in sorted(args.runs.glob("*.json")):
        report = read_json(path)
        if report is None:
            continue
        for game in games_in(report):
            row = record_from(path, report, game, int(args.shot))
            if row is not None:
                rows.append(row)

    grouped: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        # 物理输入相同还不足够：局种子决定后续摩擦序列；两者都相同才算对照。
        grouped[(row["inputFingerprint"], str(row["seed"]), str(row["opponent"]), row["proxyTeam"])].append(row)

    lineages = []
    for key, values in sorted(grouped.items(), key=lambda item: (-len(item[1]), str(item[0]))):
        if len(values) < 2:
            continue
        plans = {plan_signature(row) for row in values}
        modes = {str(row["mode"]) for row in values}
        outcomes = Counter(str(row["finalResult"]) for row in values)
        lineages.append({
            "inputFingerprint": key[0], "seed": key[1], "opponent": key[2], "proxyTeam": key[3],
            "records": len(values),
            "distinctPlans": len(plans), "distinctModes": len(modes),
            "isContractComparison": len(plans) > 1 or len(modes) > 1,
            "outcomes": {"wins": outcomes["胜"], "draws": outcomes["平"], "losses": outcomes["负"]},
            "inputState": values[0]["inputState"],
            "recordsDetail": values,
        })

    contract_groups = [item for item in lineages if bool(item["isContractComparison"])]
    payload = {
        "schema": "state_input_lineage_audit_v1",
        "meaning": "同一输入指纹+同一种子+同一对手才构成因果续局候选；跨输入历史记录只可用于生成假设。",
        "shot": int(args.shot),
        "recordCount": len(rows),
        "sameInputLineageCount": len(lineages),
        "contractComparisonLineageCount": len(contract_groups),
        # 单独保留所有记录，便于定位某个当前基线是否尚无历史同盘面对照；
        # 不把这类孤立记录混入下方的因果分组。
        "records": rows,
        "contractComparisonLineages": contract_groups,
        "sameInputLineages": lineages,
    }
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "output": str(args.output), "records": len(rows), "sameInputLineages": len(lineages),
        "contractComparisonLineages": len(contract_groups),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
