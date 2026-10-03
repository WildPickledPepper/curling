#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""离线比较同一 K8 前缀的两条状态边。

本工具只读取两份完整续局和可选的有限末手反击探测报告。它不生成候选、不调用
PhysX，也不改比赛状态机。输出明确把三类事实分开：K8 后壶面、有限反击集结果、
以及指定对手完整续局结果。有限反击集找不到反例不代表连续动作空间安全。
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]

import sys

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import score_board  # noqa: E402
from planning_proxy.evaluate_vs_teammate_ppo import HOUSE_X, HOUSE_Y, STONE_R, is_in_house  # noqa: E402


def args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True, help="K8 原状态边的完整续局报告")
    parser.add_argument("--candidate", type=Path, required=True, help="K8 待比较状态边的完整续局报告")
    parser.add_argument("--baseline-counterplay", type=Path, help="原状态边 K8 后的有限反击报告")
    parser.add_argument("--candidate-counterplay", type=Path, help="待比较状态边 K8 后的有限反击报告")
    parser.add_argument("--baseline-reply-lattice", type=Path, help="原状态边 K8 后的有限终局反击格报告")
    parser.add_argument("--candidate-reply-lattice", type=Path, help="待比较状态边 K8 后的有限终局反击格报告")
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} 不是对象")
    return payload


def game_payload(payload: dict[str, Any], path: Path) -> dict[str, Any]:
    game = payload.get("game")
    if not isinstance(game, dict):
        raise ValueError(f"{path} 缺少 game")
    trace = game.get("trace")
    if not isinstance(trace, list):
        raise ValueError(f"{path} 缺少 game.trace")
    return game


def k8_row(game: dict[str, Any], path: Path) -> dict[str, Any]:
    row = next((item for item in game["trace"] if isinstance(item, dict) and int(item.get("shot", -1)) == 15), None)
    if not isinstance(row, dict) or not isinstance(row.get("stateAfter"), list):
        raise ValueError(f"{path} 缺少 K8 后壶面")
    return row


def board_summary(states: list[dict[str, Any]]) -> dict[str, Any]:
    live: list[dict[str, Any]] = []
    for index, state in enumerate(states):
        if not isinstance(state, dict) or not bool(state.get("enabled", False)):
            continue
        x, y = float(state["x"]), float(state["y"])
        owner = "先手" if index % 2 == 0 else "后手"
        live.append({
            "index": index,
            "owner": owner,
            "x": round(x, 6),
            "y": round(y, 6),
            "到按钮距离": round(math.hypot(x - HOUSE_X, y - HOUSE_Y), 6),
            "在大本营": bool(is_in_house(type("Stone", (), {"x": x, "y": y})())),
        })
    in_house = {
        side: sum(item["owner"] == side and item["在大本营"] for item in live)
        for side in ("先手", "后手")
    }
    first_distance = min((item["到按钮距离"] for item in live if item["owner"] == "先手"), default=None)
    second_distance = min((item["到按钮距离"] for item in live if item["owner"] == "后手"), default=None)
    return {
        "K8后即时比分_先手视角": int(score_board(states)),
        "在场壶数": {"先手": sum(item["owner"] == "先手" for item in live), "后手": sum(item["owner"] == "后手" for item in live)},
        "大本营壶数": in_house,
        "最近壶距离": {"先手": first_distance, "后手": second_distance},
        "壶面": live,
    }


def continuation_summary(path: Path) -> dict[str, Any]:
    payload = load(path)
    game = game_payload(payload, path)
    row = k8_row(game, path)
    plan = row.get("firstPlayerPlan")
    return {
        "source": str(path),
        "K8动作": row.get("bestshot"),
        "K8执行模式": row.get("mode"),
        "K8计划阶段": plan.get("phase") if isinstance(plan, dict) else None,
        "K8后壶面": board_summary(row["stateAfter"]),
        "完整续局": {
            "先手终局分数": game.get("finalScoreFirst"),
            "胜者": game.get("winner"),
            "续局对手": payload.get("continuationOpponent"),
            "物理前缀最大状态差": game.get("replayStartMaxStateDelta"),
        },
    }


def counterplay_summary(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    payload = load(path)
    rows = payload.get("rankedCounterplay")
    if not isinstance(rows, list):
        raise ValueError(f"{path} 缺少 rankedCounterplay")
    singles = [row for row in rows if isinstance(row, dict) and int(row.get("minimumOwnRemoved", 0)) >= 1]
    doubles = [row for row in rows if isinstance(row, dict) and int(row.get("minimumOwnRemoved", 0)) >= 2]
    timing = payload.get("strictTiming") if isinstance(payload.get("strictTiming"), dict) else {}
    refine = payload.get("strictLateralRefinement") if isinstance(payload.get("strictLateralRefinement"), dict) else {}
    return {
        "source": str(path),
        "有限严格候选数": int(payload.get("candidateCount", len(rows))),
        "跨全部物理种子至少清一颗先手壶的候选数": len(singles),
        "跨全部物理种子至少双清先手壶的候选数": len(doubles),
        "首条双清见证": doubles[0].get("bestshot") if doubles else None,
        "严格执行总秒数": timing.get("totalSeconds"),
        "严格单候选P95秒数": timing.get("p95CandidateSeconds"),
        "横移微细化候选数": refine.get("strictCandidateCount"),
        "边界": payload.get("scope"),
    }


def reply_lattice_summary(path: Path | None) -> dict[str, Any] | None:
    """只摘录有限最坏情况反击格的可比较统计，不把它写成安全认证。"""

    if path is None:
        return None
    payload = load(path)
    timing = payload.get("strictTiming") if isinstance(payload.get("strictTiming"), dict) else {}
    witness = payload.get("首个跨全部种子必败见证")
    return {
        "source": str(path),
        "有限严格候选数": payload.get("candidateCount"),
        "R内最坏分_先手视角": payload.get("R内最坏分_先手视角"),
        "跨全部种子必败动作数": payload.get("跨全部种子必败动作数"),
        "首个跨全部种子必败见证": witness.get("bestshot") if isinstance(witness, dict) else None,
        "首个见证族": witness.get("family") if isinstance(witness, dict) else None,
        "严格执行总秒数": timing.get("totalSeconds"),
        "严格单候选P95秒数": timing.get("p95CandidateSeconds"),
        "边界": payload.get("scope"),
    }


def main() -> int:
    options = args()
    baseline = continuation_summary(options.baseline)
    candidate = continuation_summary(options.candidate)
    # 连续重放由浮点序列化/反序列化可产生约 1e-8 的坐标差；这不是前缀分叉。
    # 阈值只用于报告“同一严格前缀是否复现”，不能替代 PhysX 合同验收。
    prefix_tolerance_m = 1e-6
    prefix_delta = max(
        float(baseline["完整续局"]["物理前缀最大状态差"] or 0.0),
        float(candidate["完整续局"]["物理前缀最大状态差"] or 0.0),
    )
    same_prefix = prefix_delta <= prefix_tolerance_m
    output = {
        "schema": "k8_state_edge_comparison_v1",
        "scope": "离线状态边比较；不构成连续对手动作空间安全证明，不改变生产状态机。",
        "sameStrictPrefixReplay": same_prefix,
        "sameStrictPrefixToleranceM": prefix_tolerance_m,
        "maximumRecordedPrefixDeltaM": prefix_delta,
        "baseline": baseline,
        "candidate": candidate,
        "finiteCounterplay": {
            "baseline": counterplay_summary(options.baseline_counterplay),
            "candidate": counterplay_summary(options.candidate_counterplay),
        },
        "finiteTerminalReplyLattice": {
            "baseline": reply_lattice_summary(options.baseline_reply_lattice),
            "candidate": reply_lattice_summary(options.candidate_reply_lattice),
        },
        "interpretationBoundary": (
            "完整续局的终局分数只说明该指定后续对手在该前缀的结果；有限反击候选集或终局反击格"
            "都不能覆盖连续动作空间，不能把其统计认证为候选状态边安全或更优。"
        ),
    }
    options.output.parent.mkdir(parents=True, exist_ok=True)
    options.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
