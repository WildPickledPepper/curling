#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从真实 K8 后壶面探测有限的、与对手模型无关的 K16 击打反击线。

对每颗先手仍在场的壶，复用当前粗代理的“首撞该壶”初值，并以严格 PhysX
在给定物理种子执行。它的用途是区分“PPO 实际找到了一条普通清壶线”和
“只在 PPO 模型里出现的回应”。候选集合有限：找不到反击不证明不存在反击。
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Sequence

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd, install_bundled_pyphysx, score_board  # noqa: E402
from planning_proxy.evaluate_vs_teammate_ppo import (  # noqa: E402
    FULL_COARSE_LATERAL_COUNT,
    FULL_COARSE_SPIN_COUNT,
    FULL_COARSE_VELOCITY_COUNT,
    HOUSE_X,
    ProxyMatchPlayer,
    attack_score,
    canonical_board,
    make_initial_candidates,
    simulate_batch,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="含 game.trace 的真实回放报告")
    parser.add_argument("--after-shot", type=int, default=15, help="读取的 trace 投壶编号")
    parser.add_argument(
        "--state", choices=("before", "after"), default="after",
        help="使用该手的 stateBefore 或 stateAfter；默认保持原 K8 后反击语义。",
    )
    parser.add_argument(
        "--strict-lateral-refine", action="store_true",
        help="默认关闭：对初轮最危险的有限首撞父路线做严格横移微细化；仅用于暴露窄碰撞通道。",
    )
    parser.add_argument("--refine-parent-count", type=int, default=4, help="横移微细化的父路线数，默认 4。")
    parser.add_argument("--refine-half-width", type=float, default=0.04, help="每个父路线横移微细化半宽，默认 0.04m。")
    parser.add_argument("--refine-step", type=float, default=0.005, help="横移微细化步长，默认 0.005m。")
    parser.add_argument(
        "--target-parity", choices=(0, 1), type=int, default=0,
        help="作为首撞目标的壶方：0=先手、1=后手；默认保持原 K16 反击语义。",
    )
    parser.add_argument("--seeds", nargs="+", type=int, required=True)
    parser.add_argument("--per-target", type=int, default=3, help="每颗先手壶保留的粗代理首撞初值数")
    parser.add_argument(
        "--diversity", choices=("spin", "spin_speed", "spin_lateral_envelope", "spin_lateral_envelope_preserve_base", "spin_lateral_envelope_preserve_base_low_spin"), default="spin",
        help=(
            "初值去重：spin=每旋转一条（历史基线）；spin_speed=每个旋转与速度组合一条；"
            "spin_lateral_envelope=每旋转保留评分最佳与最高速度的横向两端（覆盖实验）；"
            "spin_lateral_envelope_preserve_base=先完整保留 spin，再按粗代理评分补最高速度横向两端；"
            "spin_lateral_envelope_preserve_base_low_spin=先完整保留 spin，再按低旋到高旋补边界。"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def source_state(path: Path, shot: int, state_position: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    report = json.loads(path.read_text(encoding="utf-8"))
    game = report.get("game")
    trace = game.get("trace") if isinstance(game, dict) else None
    if not isinstance(trace, list):
        raise SystemExit(f"{path} 不含 game.trace")
    row = next((item for item in trace if isinstance(item, dict) and int(item.get("shot", -1)) == int(shot)), None)
    state_key = "stateBefore" if state_position == "before" else "stateAfter"
    states = row.get(state_key) if isinstance(row, dict) else None
    if not isinstance(states, list) or len(states) < 16:
        raise SystemExit(f"{path} 第 {shot} 手缺少完整 {state_key}")
    return states, row


def live_indices(states: Sequence[dict[str, Any]], parity: int) -> list[int]:
    return [
        index for index, state in enumerate(states)
        if bool(state.get("enabled", False)) and index % 2 == parity
    ]


def shared_target_hit_candidates(
    generator: ProxyMatchPlayer,
    states: Sequence[dict[str, Any]],
    targets: Sequence[int],
    *,
    limit: int,
    diversity: str,
) -> tuple[dict[int, tuple[tuple[float, float, float], ...]], int]:
    """一次粗代理模拟后，按首撞目标分组。

    与 ``_adaptive_target_hit_candidates`` 保持同一网格、攻击分与高守壶补充初值；
    只消除“每个 target 重跑同一批 4305 条粗代理”的重复计算。
    """

    try:
        _, proxy_board = canonical_board(states, 0)
        coarse_shots = make_initial_candidates(
            velocity_count=FULL_COARSE_VELOCITY_COUNT,
            lateral_count=FULL_COARSE_LATERAL_COUNT,
            spin_count=FULL_COARSE_SPIN_COUNT,
        )
        coarse = simulate_batch(coarse_shots, proxy_board, generator.params, force_lookup=generator.lookup, dt=0.02)
    except (FloatingPointError, ValueError):
        return {int(target): () for target in targets}, 0
    output: dict[int, tuple[tuple[float, float, float], ...]] = {}
    for target_index in targets:
        candidates: list[tuple[float, float, float]] = []
        target_state = states[int(target_index)] if 0 <= int(target_index) < len(states) else None
        if target_state is not None and bool(target_state.get("enabled", False)) and float(target_state.get("y", 0.0)) >= 7.60:
            side = -1.0 if float(target_state.get("x", HOUSE_X)) < HOUSE_X else 1.0
            candidates.extend(
                (5.60, -side * lateral, side * spin)
                for lateral, spin in ((0.66, 7.0), (0.88, 8.5), (0.44, 5.5))
            )
        hit_rows = np.flatnonzero(coarse.first_hit_index == int(target_index))
        if len(hit_rows):
            hit_scores = attack_score(coarse, protected_opponent_indices=set(), must_clear_index=int(target_index))
            if diversity == "spin_lateral_envelope":
                # 一个首撞目标在同旋转下仍可能存在不同速度/横移的碰撞拓扑。
                # 对每档旋转取：粗代理最高分、最高速度下最左横移、最高速度下
                # 最右横移。它不根据任何 fixture 坐标选择，也不宣布可行；只是
                # 把严格 PhysX 的入口从“一档旋转一条”扩展为有限的拓扑包络。
                rows_by_spin: dict[int, list[int]] = {}
                for row in hit_rows:
                    spin_bin = int(round(float(coarse_shots[int(row)][2]) * 1000.0))
                    rows_by_spin.setdefault(spin_bin, []).append(int(row))
                ordered_rows: list[int] = []
                for spin_bin in sorted(rows_by_spin, key=lambda value: (abs(value), value)):
                    group = rows_by_spin[spin_bin]
                    ordered_rows.append(max(group, key=lambda row: float(hit_scores[row])))
                    max_speed = max(float(coarse_shots[row][0]) for row in group)
                    fastest = [row for row in group if abs(float(coarse_shots[row][0]) - max_speed) < 1e-8]
                    ordered_rows.append(min(fastest, key=lambda row: float(coarse_shots[row][1])))
                    ordered_rows.append(max(fastest, key=lambda row: float(coarse_shots[row][1])))
                seen_exact: set[tuple[float, float, float]] = {
                    tuple(round(float(value), 6) for value in candidate) for candidate in candidates
                }
                for row in ordered_rows:
                    candidate = tuple(float(value) for value in coarse_shots[row])
                    exact = tuple(round(value, 6) for value in candidate)
                    if exact in seen_exact:
                        continue
                    seen_exact.add(exact)
                    candidates.append(candidate)
                    if len(candidates) >= int(limit):
                        break
            elif diversity in ("spin_lateral_envelope_preserve_base", "spin_lateral_envelope_preserve_base_low_spin"):
                # 先逐项重现历史 spin 筛选，确保新增边界线不会在固定上限内
                # 挤掉旧的代表候选；随后只使用剩余名额。该分支仅是诊断实验。
                seen_spin: set[int] = {
                    int(round(float(candidate[2]) * 1000.0)) for candidate in candidates
                }
                seen_exact = {
                    tuple(round(float(value), 6) for value in candidate) for candidate in candidates
                }
                for row in hit_rows[np.argsort(-hit_scores[hit_rows])]:
                    candidate = tuple(float(value) for value in coarse_shots[int(row)])
                    spin_bin = int(round(candidate[2] * 1000.0))
                    if spin_bin in seen_spin:
                        continue
                    seen_spin.add(spin_bin)
                    exact = tuple(round(value, 6) for value in candidate)
                    if exact not in seen_exact:
                        seen_exact.add(exact)
                        candidates.append(candidate)
                    if len(candidates) >= int(limit):
                        break
                if len(candidates) < int(limit):
                    boundary_rows: list[int] = []
                    for spin_bin in sorted({int(round(float(coarse_shots[int(row)][2]) * 1000.0)) for row in hit_rows}):
                        group = [
                            int(row) for row in hit_rows
                            if int(round(float(coarse_shots[int(row)][2]) * 1000.0)) == spin_bin
                        ]
                        max_speed = max(float(coarse_shots[row][0]) for row in group)
                        fastest = [row for row in group if abs(float(coarse_shots[row][0]) - max_speed) < 1e-8]
                        boundary_rows.extend((
                            min(fastest, key=lambda row: float(coarse_shots[row][1])),
                            max(fastest, key=lambda row: float(coarse_shots[row][1])),
                        ))
                    # 不读取 fixture 或对手动作。两种排序分别检验：粗代理评分是否
                    # 足以代表边界价值，以及低旋优先能否更早覆盖不同碰撞拓扑。
                    unique_boundary_rows = sorted(set(boundary_rows))
                    if diversity == "spin_lateral_envelope_preserve_base_low_spin":
                        ordered_boundary_rows = sorted(
                            unique_boundary_rows,
                            key=lambda row: (abs(float(coarse_shots[row][2])), float(coarse_shots[row][2]), float(coarse_shots[row][1])),
                        )
                    else:
                        ordered_boundary_rows = sorted(
                            unique_boundary_rows, key=lambda row: float(hit_scores[row]), reverse=True,
                        )
                    for row in ordered_boundary_rows:
                        candidate = tuple(float(value) for value in coarse_shots[row])
                        exact = tuple(round(value, 6) for value in candidate)
                        if exact in seen_exact:
                            continue
                        seen_exact.add(exact)
                        candidates.append(candidate)
                        if len(candidates) >= int(limit):
                            break
            else:
                seen_keys: set[tuple[int, ...]] = set()
                for candidate in candidates:
                    spin_bin = int(round(candidate[2] * 1000.0))
                    speed_bin = int(round(candidate[0] * 1000.0))
                    seen_keys.add((spin_bin,) if diversity == "spin" else (spin_bin, speed_bin))
                for row in hit_rows[np.argsort(-hit_scores[hit_rows])]:
                    candidate = tuple(float(value) for value in coarse_shots[int(row)])
                    spin_bin = int(round(candidate[2] * 1000.0))
                    speed_bin = int(round(candidate[0] * 1000.0))
                    key = (spin_bin,) if diversity == "spin" else (spin_bin, speed_bin)
                    if key in seen_keys:
                        continue
                    seen_keys.add(key)
                    candidates.append(candidate)
                    if len(candidates) >= int(limit):
                        break
        output[int(target_index)] = tuple(candidates)
    return output, int(len(coarse_shots))


def main() -> int:
    args = parse_args()
    if int(args.per_target) < 1:
        raise SystemExit("--per-target 必须至少为 1")
    if int(args.refine_parent_count) < 1 or float(args.refine_half_width) <= 0.0 or float(args.refine_step) <= 0.0:
        raise SystemExit("横移微细化参数必须为正数")
    states, source_row = source_state(args.source, int(args.after_shot), str(args.state))
    target_indices = live_indices(states, int(args.target_parity))
    if not target_indices:
        raise SystemExit(f"所选壶面没有第 {int(args.target_parity)} 方壶可供首撞探测")
    # stateAfter 是下一手出手前局面；stateBefore 则仍是本手出手前局面。
    simulation_shot_number = int(args.after_shot) if args.state == "after" else int(args.after_shot) - 1
    install_bundled_pyphysx()
    generator = ProxyMatchPlayer(physics_seeds=1, parent_regions=1, decision_budget_seconds=5.0)
    candidate_rows: list[dict[str, Any]] = []
    strict_durations: list[float] = []
    seen: set[tuple[float, float, float]] = set()
    generation_started = time.perf_counter()
    by_target, coarse_count = shared_target_hit_candidates(
        generator, states, target_indices, limit=int(args.per_target), diversity=str(args.diversity),
    )
    generation_seconds = time.perf_counter() - generation_started
    def strict_row(target_index: int, shot: tuple[float, float, float]) -> dict[str, Any]:
        """在给定物理种子上执行一条有限的严格反击候选。"""
        seed_rows: list[dict[str, Any]] = []
        strict_started = time.perf_counter()
        for seed in args.seeds:
            environment = StrictCurlingEnd(seed=int(seed), training_fast=True)
            environment.reset()
            environment.shot_number = simulation_shot_number
            environment.restore_settled_states(states)
            result = environment.play(tuple(float(value) for value in shot))
            after = result["states"]
            before_target = set(target_indices)
            after_target = set(live_indices(after, int(args.target_parity)))
            removed_target = sorted(before_target - after_target)
            seed_rows.append({
                "seed": int(seed),
                "scoreAfterCounterplay": int(score_board(after)),
                "cleared": [int(index) for index in result["cleared"]],
                # 保留历史字段，以免已有 K16 诊断读取失败；新字段才是通用语义。
                "firstSideOwnRemoved": removed_target if int(args.target_parity) == 0 else [],
                "firstSideOwnRemovedCount": len(removed_target) if int(args.target_parity) == 0 else 0,
                "targetSideRemoved": removed_target,
                "targetSideRemovedCount": len(removed_target),
            })
        strict_seconds = time.perf_counter() - strict_started
        strict_durations.append(strict_seconds)
        scores = [int(item["scoreAfterCounterplay"]) for item in seed_rows]
        removals = [int(item["targetSideRemovedCount"]) for item in seed_rows]
        return {
            "targetIndex": int(target_index),
            "bestshot": [float(value) for value in shot],
            "worstScoreForFirst": min(scores),
            "meanScoreForFirst": sum(scores) / len(scores),
            "minimumOwnRemoved": min(removals),
            "meanOwnRemoved": sum(removals) / len(removals),
            # 只记录该诊断候选跨所有给定物理种子的 reset/恢复/严格执行时间；
            # 不参与候选排序，也不改变任何物理或合同语义。
            "strictSeconds": strict_seconds,
            "seeds": seed_rows,
        }

    for target_index in target_indices:
        for shot in by_target[int(target_index)]:
            key = tuple(round(float(value), 6) for value in shot)
            if key in seen:
                continue
            seen.add(key)
            candidate_rows.append(strict_row(int(target_index), shot))
    candidate_rows.sort(
        key=lambda row: (
            int(row["worstScoreForFirst"]),
            -int(row["minimumOwnRemoved"]),
            -float(row["meanOwnRemoved"]),
            float(row["meanScoreForFirst"]),
        )
    )
    refinement_summary: dict[str, Any] | None = None
    if args.strict_lateral_refine:
        # 只对初轮按“最坏先手分数、最低清除数”排出的少量风险父路线细化。
        # 这不是连续空间穷尽；不命中只能说明本微网格未找到，不能称为安全。
        parents = list(candidate_rows[: int(args.refine_parent_count)])
        refined_count = 0
        new_rows: list[dict[str, Any]] = []
        initial_keys = {
            tuple(round(float(value), 6) for value in row["bestshot"]) for row in candidate_rows
        }
        offsets = np.arange(
            -float(args.refine_half_width),
            float(args.refine_half_width) + float(args.refine_step) * 0.25,
            float(args.refine_step),
        )
        for parent in parents:
            base_v, base_h, base_w = (float(value) for value in parent["bestshot"])
            for offset in offsets:
                shot = (base_v, float(np.clip(base_h + float(offset), -2.23, 2.23)), base_w)
                key = tuple(round(float(value), 6) for value in shot)
                if key in initial_keys:
                    continue
                initial_keys.add(key)
                new_rows.append(strict_row(int(parent["targetIndex"]), shot))
                refined_count += 1
        candidate_rows.extend(new_rows)
        candidate_rows.sort(
            key=lambda row: (
                int(row["worstScoreForFirst"]),
                -int(row["minimumOwnRemoved"]),
                -float(row["meanOwnRemoved"]),
                float(row["meanScoreForFirst"]),
            )
        )
        refinement_summary = {
            "scope": "初轮最危险父路线的严格横移微细化；默认关闭，不覆盖连续空间",
            "parentCount": len(parents),
            "halfWidthM": float(args.refine_half_width),
            "stepM": float(args.refine_step),
            "strictCandidateCount": refined_count,
            "parentBestshots": [parent["bestshot"] for parent in parents],
        }
    output = {
        "schema": "k16_generic_counterplay_probe_v2",
        "scope": (
            "从固定真实壶面生成有限首撞击打初值并严格执行；不使用 PPO，"
            "不覆盖连续动作空间，未找到反击不能证明不存在。"
        ),
        "source": str(args.source),
        "afterShot": int(args.after_shot),
        "statePosition": str(args.state),
        "simulationShotNumber": simulation_shot_number,
        "sourceK8Bestshot": source_row.get("bestshot"),
        "seeds": [int(seed) for seed in args.seeds],
        "diversity": str(args.diversity),
        "targetParity": int(args.target_parity),
        "firstSideLiveIndices": target_indices if int(args.target_parity) == 0 else [],
        "targetSideLiveIndices": target_indices,
        "coarseCandidateCount": coarse_count,
        "candidateGenerationSeconds": generation_seconds,
        "candidateCount": len(candidate_rows),
        "strictLateralRefinement": refinement_summary,
        "strictTiming": {
            "scope": "每个候选跨所有 --seeds 的 StrictCurlingEnd reset、壶面恢复与 play 总时间",
            "totalSeconds": sum(strict_durations),
            "meanCandidateSeconds": (sum(strict_durations) / len(strict_durations)) if strict_durations else 0.0,
            "p95CandidateSeconds": float(np.percentile(strict_durations, 95)) if strict_durations else 0.0,
            "maxCandidateSeconds": max(strict_durations, default=0.0),
        },
        "rankedCounterplay": candidate_rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"candidateCount": len(candidate_rows), "best": candidate_rows[0] if candidate_rows else None}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
