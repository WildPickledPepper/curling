#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""离线枚举 K8 候选及对手无模型高速反击。

用途仅是发现/排除状态合同：K8 候选完全由当前唯一营内威胁的左右关系生成；
K16 不是 PPO，而是固定的高速直击、旋进直击覆盖。它不是“任意对手完整证明”，
更不能把任何一条 BESTSHOT 写回比赛状态机。

每个候选先从来源报告逐手重放到 K8，再以 K8 后坐标恢复批量召回反击；每个召回
到的最差反击再重新从完整前缀连续回放复核，防止把坐标恢复结果误作因果结论。
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Sequence

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import (  # noqa: E402
    HOUSE_X,
    HOUSE_Y,
    StrictCurlingEnd,
    install_bundled_pyphysx,
    score_board,
)
from planning_proxy.evaluate_vs_teammate_ppo import canonical_board  # noqa: E402


def replay_prefix(environment: StrictCurlingEnd, trace: Sequence[dict[str, Any]], upto_shot: int) -> list[dict[str, Any]]:
    """连续回放报告中的前缀和规则回滚。"""

    states = environment.reset()
    for item in trace:
        if int(item.get("shot", 0)) > int(upto_shot):
            break
        result = environment.play(item["bestshot"])
        states = result["states"]
        if item.get("ruleRollback"):
            states = environment.restore_settled_states(item["stateBefore"])
    if environment.shot_number != int(upto_shot):
        raise ValueError("来源报告缺少完整 K8 前缀")
    return states


def max_state_delta(actual: Sequence[dict[str, Any]], expected: Sequence[dict[str, Any]]) -> float:
    values: list[float] = []
    for got, wanted in zip(actual, expected):
        if bool(got.get("enabled")) != bool(wanted.get("enabled")):
            return float("inf")
        if bool(got.get("enabled")):
            values.extend((
                abs(float(got["x"]) - float(wanted["x"])),
                abs(float(got["y"]) - float(wanted["y"])),
                abs(float(got.get("yaw", 0.0)) - float(wanted.get("yaw", 0.0))),
            ))
    return max(values, default=0.0)


def own_k8_candidates(states: Sequence[dict[str, Any]]) -> list[tuple[float, float, float]]:
    """按威胁相对中线镜像的 K8 初始拓扑；不读取对手策略。"""

    strict, _ = canonical_board(states, 0)
    enemies = [stone for stone in strict if stone.owner == "opponent"]
    if not enemies:
        return []
    threat = min(enemies, key=lambda stone: math.hypot(stone.x - HOUSE_X, stone.y - HOUSE_Y))
    side = 1.0 if threat.x >= HOUSE_X else -1.0
    # 这些是现有 K8 通用角色的镜像初值；每条都要经过严格物理和下方反击扫描。
    templates = (
        (5.60, side * 2.08, -side * 13.80),
        (5.00, side * 1.47, -side * 10.00),
        (3.00, side * 0.73, side * 5.00),
        (3.00, -side * 1.47, 0.00),
        (4.00, side * 2.20, -side * 15.00),
        (4.00, 0.00, 0.00),
        (5.00, 0.00, 0.00),
        (6.00, 0.00, 0.00),
        (5.00, side * 2.20, -side * 10.00),
    )
    candidates: list[tuple[float, float, float]] = []
    seen: set[tuple[float, float, float]] = set()
    for candidate in templates:
        key = tuple(round(value, 6) for value in candidate)
        if key not in seen:
            seen.add(key)
            candidates.append(candidate)
    return candidates


def opponent_reply_grid() -> list[tuple[float, float, float]]:
    """无模型的高速 hit / promote 覆盖；不声称穷尽所有对手动作。"""

    return [
        (6.0, float(horizontal), float(spin))
        for horizontal in np.linspace(-2.2, 2.2, 45)
        for spin in (-12.0, -6.0, 0.0, 6.0, 12.0)
    ]


def scan_candidate(
    *, source_trace: Sequence[dict[str, Any]], seed: int, source_k8_before: Sequence[dict[str, Any]], own_shot: tuple[float, float, float], replies: Sequence[tuple[float, float, float]],
) -> dict[str, Any]:
    environment = StrictCurlingEnd(seed=seed, training_fast=True)
    before = replay_prefix(environment, source_trace, 14)
    delta = max_state_delta(before, source_k8_before)
    if delta > 1e-4:
        raise RuntimeError(f"K8 前连续重放误差 {delta:.6g}")
    after_k8 = environment.play(own_shot)["states"]
    score_after_k8 = int(score_board(after_k8))
    # 批量召回阶段仅恢复已静止 K8 后壶面；最终最差动作必须再连续复核。
    response_environment = StrictCurlingEnd(seed=seed, training_fast=True)
    response_environment.reset()
    recalled: list[tuple[int, tuple[float, float, float], list[int]]] = []
    for reply in replies:
        response_environment.restore_settled_states(after_k8)
        response_environment.shot_number = 15
        result = response_environment.play(reply)
        recalled.append((int(score_board(result["states"])), reply, [int(index) for index in result["cleared"]]))
    recalled.sort(key=lambda row: row[0])
    restored_worst_score, worst_reply, restored_cleared = recalled[0]

    exact_environment = StrictCurlingEnd(seed=seed, training_fast=True)
    replay_prefix(exact_environment, source_trace, 14)
    exact_environment.play(own_shot)
    exact_final = exact_environment.play(worst_reply)
    exact_score = int(score_board(exact_final["states"]))
    return {
        "bestshot": [float(value) for value in own_shot],
        "replayStartMaxStateDelta": delta,
        "scoreAfterK8": score_after_k8,
        "restoredWorstReply": [float(value) for value in worst_reply],
        "restoredWorstScore": restored_worst_score,
        "restoredWorstCleared": restored_cleared,
        "continuousWorstScore": exact_score,
        "continuousWorstFinalStones": [
            {"index": index, "x": float(state["x"]), "y": float(state["y"])}
            for index, state in enumerate(exact_final["states"])
            if bool(state["enabled"])
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-report", type=Path, required=True)
    parser.add_argument(
        "--override-trace-report", type=Path, default=None,
        help="可选的连续续局报告；按 shot 覆盖来源 trace，用于验收 K7 候选后的新 K8 壶面。",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = json.loads(args.source_report.read_text(encoding="utf-8"))
    game = report.get("game") or report["games"][0]
    trace = [dict(item) for item in game["trace"]]
    if args.override_trace_report is not None:
        override_payload = json.loads(args.override_trace_report.read_text(encoding="utf-8"))
        override_game = override_payload.get("game") or override_payload["games"][0]
        if int(override_game["seed"]) != int(game["seed"]):
            raise ValueError("override trace 的物理种子必须与来源报告一致")
        overrides = {int(item["shot"]): dict(item) for item in override_game["trace"]}
        trace = [overrides.get(int(item["shot"]), item) for item in trace]
        # 续局报告只含它的后半局 trace；为使 K8 前壶面来自真实新轨迹，追加
        # 不在来源报告中的覆盖记录（正常情况下这里不会触发）。
        existing = {int(item["shot"]) for item in trace}
        trace.extend(item for shot, item in overrides.items() if shot not in existing)
        trace.sort(key=lambda item: int(item["shot"]))
    source_k8_turn = next(item for item in trace if int(item.get("shot", 0)) == 15)
    source_k8_before = source_k8_turn["stateBefore"]
    install_bundled_pyphysx()
    prefix_environment = StrictCurlingEnd(seed=int(game["seed"]), training_fast=True)
    replayed_before = replay_prefix(prefix_environment, trace, 14)
    candidates = own_k8_candidates(replayed_before)
    replies = opponent_reply_grid()
    rows = [
        scan_candidate(
            source_trace=trace, seed=int(game["seed"]), source_k8_before=source_k8_before,
            own_shot=candidate, replies=replies,
        )
        for candidate in candidates
    ]
    payload = {
        "schema": "k8_adversarial_reply_explore_v1",
        "scope": "offline diagnostic; finite high-speed reply lattice is a counterexample generator, not a proof of universal defence",
        "sourceReport": str(args.source_report),
        "overrideTraceReport": None if args.override_trace_report is None else str(args.override_trace_report),
        "seed": int(game["seed"]),
        "ownCandidateCount": len(candidates), "replyCandidateCount": len(replies),
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    for row in rows:
        print(
            f"K8 {row['bestshot']} after={row['scoreAfterK8']:+d} "
            f"worst={row['continuousWorstScore']:+d} reply={row['restoredWorstReply']}",
            flush=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
