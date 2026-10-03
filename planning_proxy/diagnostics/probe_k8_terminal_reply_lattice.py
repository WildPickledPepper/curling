#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""以有限、对手无关的 K16 严格反击集合比较一个 K8 后壶面。

这不是“证明没有解”的搜索器，也不会接入比赛状态机。它定义一个可复现的
有限反击集合 R：

* 对每颗仍在场的先手壶，粗代理提出首撞该壶的不同碰撞入口；
* 对每颗先手壶，补高速零旋直击走廊；
* 补不撞任何旧壶、向按钮抢分的直达路线。

所有入口都在给定物理种子上由严格 PhysX 实际执行。输出的 ``R内最坏分`` 是
``min(action in R, seed) score``，只能作为下界反例生成器：小于零说明 R 内有
一个严格输局见证；大于等于零绝不代表连续反击空间不存在输局。
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd, install_bundled_pyphysx, score_board  # noqa: E402
from planning_proxy.diagnostics.probe_k16_generic_counterplay import shared_target_hit_candidates  # noqa: E402
from planning_proxy.evaluate_vs_teammate_ppo import (  # noqa: E402
    FULL_COARSE_LATERAL_COUNT,
    FULL_COARSE_SPIN_COUNT,
    FULL_COARSE_VELOCITY_COUNT,
    HOUSE_X,
    ProxyMatchPlayer,
    canonical_board,
    make_initial_candidates,
    simulate_batch,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="含 K8/K16 trace 的完整续局报告")
    parser.add_argument("--after-shot", type=int, default=15, help="读取 K8 的 stateAfter，默认 15")
    parser.add_argument("--seeds", nargs="+", type=int, required=True, help="逐个严格执行的物理种子")
    parser.add_argument("--per-target", type=int, default=12, help="每颗先手壶的首撞粗代理入口数")
    parser.add_argument("--direct-draw-count", type=int, default=9, help="不碰旧壶的按钮直达入口数")
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def source_state(path: Path, shot: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    report = json.loads(path.read_text(encoding="utf-8"))
    game = report.get("game")
    trace = game.get("trace") if isinstance(game, dict) else None
    if not isinstance(trace, list):
        raise ValueError(f"{path} 缺少 game.trace")
    row = next((item for item in trace if isinstance(item, dict) and int(item.get("shot", -1)) == int(shot)), None)
    states = row.get("stateAfter") if isinstance(row, dict) else None
    if not isinstance(states, list) or len(states) < 16:
        raise ValueError(f"{path} 第 {shot} 手缺少 stateAfter")
    return states, row


def live_first_indices(states: Sequence[dict[str, Any]]) -> list[int]:
    return [index for index, item in enumerate(states) if index % 2 == 0 and bool(item.get("enabled", False))]


def append_unique(
    items: list[tuple[str, tuple[float, float, float]]],
    seen: set[tuple[float, float, float]],
    family: str,
    values: Iterable[float],
) -> None:
    action = tuple(float(value) for value in values)
    key = tuple(round(value, 6) for value in action)
    if key not in seen:
        seen.add(key)
        items.append((family, action))


def reply_lattice(
    states: Sequence[dict[str, Any]], *, per_target: int, direct_draw_count: int,
) -> tuple[list[tuple[str, tuple[float, float, float]]], dict[str, Any]]:
    """从当前壶面构造固定有限入口，不读取 PPO/aggressive 或历史动作。"""

    targets = live_first_indices(states)
    generator = ProxyMatchPlayer(physics_seeds=1, parent_regions=1, decision_budget_seconds=5.0)
    hit_groups, coarse_count = shared_target_hit_candidates(
        generator, states, targets, limit=int(per_target), diversity="spin_lateral_envelope",
    )
    items: list[tuple[str, tuple[float, float, float]]] = []
    seen: set[tuple[float, float, float]] = set()
    for target in targets:
        for action in hit_groups.get(int(target), ()):
            append_unique(items, seen, f"首撞先手壶_{target}", action)
        # 粗代理横移网格不必恰好经过窄直击通道；这组相对当前目标横坐标的
        # 有限直线用于发现明确的高速清壶/双清反例，不是连续微网格证明。
        centre_h = float(states[target]["x"]) - HOUSE_X
        for velocity in (5.4, 5.7, 6.0):
            for offset in (-0.08, -0.04, 0.0, 0.04, 0.08):
                append_unique(items, seen, f"高速直击走廊_{target}", (velocity, max(-2.23, min(2.23, centre_h + offset)), 0.0))

    # 直达按钮路线不能用“首撞某颗先手壶”表示；它覆盖对手不清壶而直接抢分。
    try:
        _, proxy_board = canonical_board(states, 0)
        coarse_shots = make_initial_candidates(
            velocity_count=FULL_COARSE_VELOCITY_COUNT,
            lateral_count=FULL_COARSE_LATERAL_COUNT,
            spin_count=FULL_COARSE_SPIN_COUNT,
        )
        coarse = simulate_batch(coarse_shots, proxy_board, generator.params, force_lookup=generator.lookup, dt=0.02)
        direct = np.flatnonzero((coarse.first_hit_index < 0) & ~coarse.exits_play)
        if len(direct):
            distances = np.hypot(coarse.stop_points[direct, 0] - HOUSE_X, coarse.stop_points[direct, 1] - 4.88)
            selected = direct[np.argsort(distances)]
            used_spin: set[int] = set()
            for row in selected:
                action = tuple(float(value) for value in coarse_shots[int(row)])
                spin_bin = int(round(action[2] * 1000.0))
                if spin_bin in used_spin:
                    continue
                used_spin.add(spin_bin)
                append_unique(items, seen, "直达按钮", action)
                if sum(family == "直达按钮" for family, _ in items) >= int(direct_draw_count):
                    break
    except (FloatingPointError, ValueError):
        pass
    return items, {"coarseCandidateCount": int(coarse_count), "firstSideTargetIndices": targets}


def execute(
    states: Sequence[dict[str, Any]], *, action: tuple[float, float, float], seeds: Sequence[int], shot_number: int,
) -> tuple[list[int], float]:
    scores: list[int] = []
    started = time.perf_counter()
    for seed in seeds:
        environment = StrictCurlingEnd(seed=int(seed), training_fast=True)
        environment.reset()
        environment.shot_number = int(shot_number)
        environment.restore_settled_states(states)
        final = environment.play(action)
        scores.append(int(score_board(final["states"])))
    return scores, time.perf_counter() - started


def main() -> int:
    options = parse_args()
    if int(options.per_target) < 1 or int(options.direct_draw_count) < 0:
        raise SystemExit("候选数必须为非负，且每目标候选至少为 1")
    states, source_row = source_state(options.source, int(options.after_shot))
    targets = live_first_indices(states)
    if not targets:
        raise SystemExit("K8 后没有先手在场壶，无法构造反击目标")
    install_bundled_pyphysx()
    actions, generation = reply_lattice(states, per_target=int(options.per_target), direct_draw_count=int(options.direct_draw_count))
    rows: list[dict[str, Any]] = []
    durations: list[float] = []
    for rank, (family, action) in enumerate(actions, start=1):
        scores, seconds = execute(states, action=action, seeds=options.seeds, shot_number=int(options.after_shot))
        durations.append(seconds)
        rows.append({
            "rank": rank,
            "family": family,
            "bestshot": [float(value) for value in action],
            "scoresForFirst": scores,
            "worstScoreForFirst": min(scores),
            "bestScoreForFirst": max(scores),
            "allSeedsFirstLoses": all(score < 0 for score in scores),
            "anySeedFirstLoses": any(score < 0 for score in scores),
            "strictSeconds": seconds,
        })
    rows.sort(key=lambda row: (int(row["worstScoreForFirst"]), int(row["bestScoreForFirst"]), int(row["rank"])))
    all_loss = [row for row in rows if bool(row["allSeedsFirstLoses"])]
    payload = {
        "schema": "k8_terminal_reply_lattice_v1",
        "scope": (
            "离线有限反击格；R内最坏分是严格反例下界。没有输局见证不代表连续对手动作空间安全，"
            "不得直接作为生产状态机选择规则。"
        ),
        "source": str(options.source),
        "afterShot": int(options.after_shot),
        "sourceK8Bestshot": source_row.get("bestshot"),
        "seeds": [int(seed) for seed in options.seeds],
        "generation": generation,
        "candidateCount": len(rows),
        "R内最坏分_先手视角": int(rows[0]["worstScoreForFirst"]) if rows else None,
        "首个R内最坏动作": rows[0] if rows else None,
        "跨全部种子必败动作数": len(all_loss),
        "首个跨全部种子必败见证": all_loss[0] if all_loss else None,
        "strictTiming": {
            "totalSeconds": float(sum(durations)),
            "meanCandidateSeconds": float(np.mean(durations)) if durations else 0.0,
            "p95CandidateSeconds": float(np.percentile(durations, 95)) if durations else 0.0,
            "maxCandidateSeconds": float(max(durations, default=0.0)),
        },
        "rankedReplies": rows,
    }
    options.output.parent.mkdir(parents=True, exist_ok=True)
    options.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "candidateCount": payload["candidateCount"],
        "R内最坏分_先手视角": payload["R内最坏分_先手视角"],
        "跨全部种子必败动作数": payload["跨全部种子必败动作数"],
        "strictTiming": payload["strictTiming"],
    }, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
