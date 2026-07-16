#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""已知场上守壶位置，反推一颗绕壶旋进目标点的 BESTSHOT 参数。

这是严格本地 PhysX 搜索：每个候选都会重置为同一组守壶位置，随后走当前
交付的非扫冰旋球 + PhysX 碰撞路径。它不会启动 Unity，也不会使用 Unity
的终点、碰撞后位置或扫冰信息。

从仓库根目录执行（必须使用随包 pyphysx 支持的 CPython 3.8）：

    python local_simulator\\examples\\inverse_spin_shot.py `
        --guard 2.375,6.7 --target 2.375,4.88 `
        --candidate-count 96 --output log\\inverse_spin_result.json

输出的 bestshot 就是可直接发送给比赛端的：

    BESTSHOT v0 h0 w0

注意：一次搜索固定一条本地 RNG 摩擦序列，目的是公平比较候选。真正训练或
上线前，应对前几名参数用多个 --physics-seed 重跑，比较落点分布和碰撞率。
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable, List, Sequence, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from local_simulator.examples.train_policy_tree_selfplay import (  # noqa: E402
    HOUSE_X,
    HOUSE_Y,
    STONE_COUNT,
    StrictCurlingEnd,
)
from local_simulator.runtime_loader import install_bundled_pyphysx  # noqa: E402


ACTIVE_STONE_INDEX = 0
FIRST_GUARD_INDEX = 2
V_MIN, V_MAX = 2.55, 3.75
H_MIN, H_MAX = -2.23, 2.23
W_MIN, W_MAX = -15.7, 15.7


@dataclass(frozen=True)
class Candidate:
    v0: float
    h0: float
    w0: float
    source: str


@dataclass
class Evaluation:
    candidate: Candidate
    endpoint: Tuple[float, float] | None
    target_error_m: float
    contact: bool
    active_in_play: bool
    max_guard_move_m: float
    score: float


def parse_xy(raw: str) -> Tuple[float, float]:
    try:
        x_text, y_text = raw.split(",", 1)
        return float(x_text), float(y_text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("坐标格式应为 x,y，例如 2.375,6.7") from exc


def parse_bestshot(raw: str) -> Candidate:
    try:
        v_text, h_text, w_text = raw.split(",", 2)
        return Candidate(float(v_text), float(h_text), float(w_text), "manual_seed")
    except ValueError as exc:
        raise argparse.ArgumentTypeError("--seed-shot 格式应为 v0,h0,w0，例如 3.1,-1.9,12") from exc


def clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def distance(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def make_coarse_candidates(args: argparse.Namespace) -> List[Candidate]:
    rng = random.Random(args.search_seed)
    result: List[Candidate] = list(args.seed_shot)

    # 两侧旋转都覆盖。h0 不能固定为零：它与 w0 一起决定能否从守壶外侧绕过。
    for _ in range(args.candidate_count):
        curl_abs = rng.uniform(args.min_curl_abs, W_MAX)
        curl = curl_abs if rng.random() < 0.5 else -curl_abs
        result.append(
            Candidate(
                v0=rng.uniform(args.v_min, args.v_max),
                h0=rng.uniform(H_MIN, H_MAX),
                w0=curl,
                source="coarse_random",
            )
        )
    return result


def refinement_candidates(base: Candidate, v_step: float, h_step: float, w_step: float) -> Iterable[Candidate]:
    for dv in (-v_step, 0.0, v_step):
        for dh in (-h_step, 0.0, h_step):
            for dw in (-w_step, 0.0, w_step):
                if dv == dh == dw == 0.0:
                    continue
                yield Candidate(
                    v0=clamp(base.v0 + dv, V_MIN, V_MAX),
                    h0=clamp(base.h0 + dh, H_MIN, H_MAX),
                    w0=clamp(base.w0 + dw, W_MIN, W_MAX),
                    source="local_refine",
                )


def positions_for_guards(guards: Sequence[Tuple[float, float]]) -> Tuple[List[float], List[int]]:
    if len(guards) > STONE_COUNT - FIRST_GUARD_INDEX:
        raise ValueError("守壶数量过多；至少必须留出 index 0 给本次出手壶")
    position = [0.0] * (STONE_COUNT * 2)
    guard_indices: List[int] = []
    for offset, (x, y) in enumerate(guards):
        index = FIRST_GUARD_INDEX + offset
        position[2 * index] = float(x)
        position[2 * index + 1] = float(y)
        guard_indices.append(index)
    return position, guard_indices


def evaluate(
    environment: StrictCurlingEnd,
    candidate: Candidate,
    position: Sequence[float],
    guard_indices: Sequence[int],
    guards: Sequence[Tuple[float, float]],
    target: Tuple[float, float],
    guard_move_limit: float,
) -> Evaluation:
    # 每个候选从完全相同的静止局面、朝向和 RNG 种子重新开始。
    environment.scene.reset_positions(
        position,
        yaw_overrides={index: 0.0 for index in range(STONE_COUNT)},
    )
    environment.shot_number = 0
    result = environment.play((candidate.v0, candidate.h0, candidate.w0))
    states = result["states"]
    active = states[ACTIVE_STONE_INDEX]
    active_in_play = bool(active["enabled"])
    endpoint = (float(active["x"]), float(active["y"])) if active_in_play else None
    target_error = distance(endpoint, target) if endpoint is not None else 10.0

    guard_moves = []
    for guard_index, before in zip(guard_indices, guards):
        state = states[guard_index]
        if not state["enabled"]:
            guard_moves.append(10.0)
        else:
            guard_moves.append(distance((float(state["x"]), float(state["y"])), before))
    max_guard_move = max(guard_moves, default=0.0)

    # 这是一个硬优先级：撞到守壶或把守壶撞走的参数，不能因为终点近而胜出。
    collision_penalty = 100.0 if bool(result["contact"]) else 0.0
    guard_penalty = 100.0 * max(0.0, max_guard_move - guard_move_limit)
    out_penalty = 100.0 if not active_in_play else 0.0
    return Evaluation(
        candidate=candidate,
        endpoint=endpoint,
        target_error_m=target_error,
        contact=bool(result["contact"]),
        active_in_play=active_in_play,
        max_guard_move_m=max_guard_move,
        score=target_error + collision_penalty + guard_penalty + out_penalty,
    )


def to_report_row(item: Evaluation) -> dict[str, Any]:
    row = asdict(item)
    row["bestshot"] = [item.candidate.v0, item.candidate.h0, item.candidate.w0]
    return row


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--guard",
        type=parse_xy,
        action="append",
        required=True,
        help="一颗守壶的坐标 x,y；可重复传入多次。",
    )
    parser.add_argument("--target", type=parse_xy, default=(HOUSE_X, HOUSE_Y), help="目标终点 x,y；默认大本营圆心。")
    parser.add_argument("--candidate-count", type=int, default=96, help="粗搜索随机候选数（不含 --seed-shot）。")
    parser.add_argument("--refine-top", type=int, default=3, help="对粗搜索前几名做局部细化。")
    parser.add_argument("--v-min", type=float, default=2.7)
    parser.add_argument("--v-max", type=float, default=3.5)
    parser.add_argument("--min-curl-abs", type=float, default=6.0, help="粗搜索旋转绝对值下限。")
    parser.add_argument("--guard-move-limit", type=float, default=0.005, help="允许守壶移动上限（米）。")
    parser.add_argument("--physics-seed", type=int, default=20260715, help="同一轮搜索固定使用的摩擦 RNG 种子。")
    parser.add_argument("--search-seed", type=int, default=20260715, help="候选参数采样 RNG 种子。")
    parser.add_argument(
        "--seed-shot",
        type=parse_bestshot,
        action="append",
        default=[],
        help="额外加入已知候选 v0,h0,w0；可重复传入。",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "log" / "inverse_spin_result.json",
        help="JSON 结果文件。",
    )
    args = parser.parse_args()
    if args.candidate_count < 1:
        parser.error("--candidate-count 必须大于 0")
    if args.refine_top < 0:
        parser.error("--refine-top 不能小于 0")
    if not V_MIN <= args.v_min <= args.v_max <= V_MAX:
        parser.error("速度范围必须落在 %.2f..%.2f" % (V_MIN, V_MAX))
    if not 0.0 <= args.min_curl_abs <= W_MAX:
        parser.error("--min-curl-abs 必须落在 0..%.1f" % W_MAX)
    return args


def main() -> None:
    args = parse_args()
    install_bundled_pyphysx()
    position, guard_indices = positions_for_guards(args.guard)
    environment = StrictCurlingEnd(seed=args.physics_seed, training_fast=True)

    coarse = [
        evaluate(environment, candidate, position, guard_indices, args.guard, args.target, args.guard_move_limit)
        for candidate in make_coarse_candidates(args)
    ]
    coarse.sort(key=lambda item: item.score)

    refined: List[Evaluation] = []
    for item in coarse[: args.refine_top]:
        for candidate in refinement_candidates(item.candidate, v_step=0.08, h_step=0.12, w_step=1.2):
            refined.append(
                evaluate(environment, candidate, position, guard_indices, args.guard, args.target, args.guard_move_limit)
            )

    ranked = sorted(coarse + refined, key=lambda item: item.score)
    best = ranked[0]
    report = {
        "schema": "strict_inverse_spin_shot_v1",
        "guards": [list(point) for point in args.guard],
        "target": list(args.target),
        "physicsSeed": args.physics_seed,
        "searchSeed": args.search_seed,
        "guardMoveLimitM": args.guard_move_limit,
        "evaluatedCount": len(ranked),
        "best": to_report_row(best),
        "top10": [to_report_row(item) for item in ranked[:10]],
        "interpretation": (
            "bestshot 可直接发送给比赛端；contact=false 且 max_guard_move_m 接近 0 表示没有擦到守壶。"
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("BESTSHOT %.6g %.6g %.6g" % (best.candidate.v0, best.candidate.h0, best.candidate.w0))
    print(
        "endpoint=%s target_error=%.4fm contact=%s guard_move=%.4fm evaluated=%d"
        % (best.endpoint, best.target_error_m, best.contact, best.max_guard_move_m, len(ranked))
    )
    print("report=%s" % args.output)


if __name__ == "__main__":
    main()
