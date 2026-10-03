#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从手工摆盘面与有限输入网格正向构造鲁棒 PhysX 测试集。

用途：构造“这个盘面、这个目标区域确实有解”的正样本，供以后测试线上
反解器的 105 秒召回率。手工输入只保存在 oracle_witness 中，正式求解器
测试时不会读取该字段。

v0 仅收集净空 draw：旧壶不接触、不移动；碰撞清壶/滚位另做专门基准集。
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import (  # noqa: E402
    HOUSE_R, HOUSE_X, HOUSE_Y, STONE_COUNT, STONE_R, StrictCurlingEnd,
)
from planning_proxy.competition_rules import (  # noqa: E402
    RuleBoardStone, free_guard_rule_violations, is_in_free_guard_zone,
)


ACTIVE_INDEX = 12  # 用 K7 的 slot，避免测试集被早期自由守壶区规则混淆。
DEFAULT_OUTPUT = ROOT / "planning_proxy" / "solver_benchmark" / "manual_forward_draw_v0.json"


@dataclass(frozen=True)
class ManualStone:
    index: int
    owner: str
    x: float
    y: float


# 这些坐标是人为摆出的结构，不来自历史比赛坐标或线上求解器输出。
# 每一组只描述“当前盘面”，不伪造此前投壶过程。
MANUAL_BOARDS: dict[str, tuple[ManualStone, ...]] = {
    "single_centre_guard": (
        ManualStone(1, "opponent", HOUSE_X, 7.55),
    ),
    "left_side_guard": (
        ManualStone(1, "opponent", 1.82, 7.55),
    ),
    "right_side_guard": (
        ManualStone(1, "opponent", 2.93, 7.55),
    ),
    "two_guard_gate": (
        ManualStone(1, "opponent", 1.88, 7.55),
        ManualStone(3, "opponent", 2.86, 7.55),
    ),
    "inner_anchor_with_opposite_guard": (
        ManualStone(0, "self", 2.58, 4.96),
        ManualStone(1, "opponent", 2.08, 7.62),
    ),
    "inner_anchor_with_two_high_guards": (
        ManualStone(0, "self", 2.58, 4.96),
        ManualStone(1, "opponent", 2.02, 7.62),
        ManualStone(3, "opponent", 2.96, 7.56),
    ),
}


def distance(left: tuple[float, float], right: tuple[float, float]) -> float:
    return math.hypot(left[0] - right[0], left[1] - right[1])


def manual_inputs() -> Iterable[tuple[float, float, float]]:
    """人工限定、优先瞄准大本营的 draw 输入范围。

    先列少量人工检查点，再做围绕按钮的有限网格。这里的顺序只决定测试集
    制作效率；它绝不进入线上求解器。
    """

    probes = (
        (3.10, -0.20, 9.0), (3.10, 0.20, -9.0),
        (3.20, -0.35, 12.0), (3.20, 0.35, -12.0),
        (3.00, -0.45, 6.0), (3.00, 0.45, -6.0),
    )
    seen: set[tuple[float, float, float]] = set()
    for values in probes:
        seen.add(values)
        yield values
    velocities = (2.95, 3.15, 3.35, 3.55, 3.75)
    laterals = (-0.90, -0.60, -0.30, 0.0, 0.30, 0.60, 0.90)
    spins = (-15.0, -10.0, -5.0, 5.0, 10.0, 15.0)
    for velocity in velocities:
        for lateral in laterals:
            for spin in spins:
                values = (velocity, lateral, spin)
                if values not in seen:
                    yield values


def blank_states(board: tuple[ManualStone, ...]) -> list[dict[str, Any]]:
    states = [
        {"enabled": False, "x": 0.0, "y": 0.0, "yaw": 0.0}
        for _ in range(STONE_COUNT)
    ]
    for stone in board:
        states[stone.index] = {"enabled": True, "x": stone.x, "y": stone.y, "yaw": 0.0}
    return states


def reset_data(states: list[dict[str, Any]]) -> tuple[list[float], dict[int, float]]:
    position = [0.0] * (STONE_COUNT * 2)
    yaws = {index: 0.0 for index in range(STONE_COUNT)}
    for index, state in enumerate(states):
        if bool(state["enabled"]):
            position[2 * index] = float(state["x"])
            position[2 * index + 1] = float(state["y"])
            yaws[index] = float(state.get("yaw", 0.0))
    return position, yaws


def classify_target(points: list[tuple[float, float]]) -> str | None:
    if all(math.hypot(x - HOUSE_X, y - HOUSE_Y) <= HOUSE_R + STONE_R for x, y in points):
        return "营内净空落点"
    return None


def build_sample(
    environment: StrictCurlingEnd,
    board_name: str,
    board: tuple[ManualStone, ...],
    input_values: tuple[float, float, float],
    physics_seeds: list[int],
    old_stone_tolerance: float,
    maximum_seed_spread: float,
) -> dict[str, Any] | None:
    states = blank_states(board)
    position, yaws = reset_data(states)
    initial = {stone.index: (stone.x, stone.y) for stone in board}
    final_rows: list[dict[str, Any]] = []
    active_points: list[tuple[float, float]] = []

    for seed in physics_seeds:
        environment.seed = int(seed) - ACTIVE_INDEX * 7919
        environment.scene.reset_positions(position, yaw_overrides=yaws)
        environment.shot_number = ACTIVE_INDEX
        result = environment.play(input_values)
        final_states = result["states"]
        rule_rows = [RuleBoardStone(stone.index, stone.owner, stone.x, stone.y, True) for stone in board]
        if bool(result.get("contact", False)) or free_guard_rule_violations(rule_rows, final_states, shot_index=ACTIVE_INDEX):
            return None
        active = final_states[ACTIVE_INDEX]
        if not bool(active.get("enabled", False)):
            return None
        for index, start in initial.items():
            final = final_states[index]
            if not bool(final.get("enabled", False)):
                return None
            if distance(start, (float(final["x"]), float(final["y"]))) > old_stone_tolerance:
                return None
        point = (float(active["x"]), float(active["y"]))
        active_points.append(point)
        final_rows.append({"physics_seed": int(seed), "active_final": [point[0], point[1]]})

    kind = classify_target(active_points)
    if kind is None:
        return None
    centre = (
        sum(point[0] for point in active_points) / len(active_points),
        sum(point[1] for point in active_points) / len(active_points),
    )
    spread = max(distance(point, centre) for point in active_points)
    if spread > maximum_seed_spread:
        return None
    return {
        "board_name": board_name,
        "board": [
            {"index": stone.index, "owner": stone.owner, "x": stone.x, "y": stone.y, "yaw": 0.0, "enabled": True}
            for stone in board
        ],
        "goal_contract": {
            "version": "手工正向净空落点合同_v0",
            "kind": kind,
            "active_index": ACTIVE_INDEX,
            "active_target_region": {"center": [centre[0], centre[1]], "radius_m": max(0.10, spread + 0.04)},
            "must_preserve_indices": sorted(initial),
            "old_stone_position_tolerance_m": old_stone_tolerance,
            "required_physics_seeds": physics_seeds,
        },
        "oracle_witness": {"bestshot": list(input_values), "strict_forward": final_rows},
    }


def target_bin(sample: dict[str, Any]) -> tuple[str, int, int]:
    target = sample["goal_contract"]["active_target_region"]["center"]
    return (
        str(sample["goal_contract"]["kind"]),
        round(float(target[0]) / 0.25),
        round(float(target[1]) / 0.25),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--physics-seed", type=int, default=20260720)
    parser.add_argument("--physics-seed-count", type=int, default=3)
    parser.add_argument("--old-stone-tolerance-m", type=float, default=0.035)
    parser.add_argument("--maximum-seed-spread-m", type=float, default=0.075)
    parser.add_argument("--max-samples-per-board", type=int, default=4)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.physics_seed_count < 1 or args.max_samples_per_board < 1:
        raise SystemExit("物理种子数和每盘面样本数必须为正")
    environment = StrictCurlingEnd(seed=0, training_fast=True)
    all_samples: list[dict[str, Any]] = []
    attempts = 0
    for board_rank, (board_name, board) in enumerate(MANUAL_BOARDS.items()):
        seeds = [int(args.physics_seed) + board_rank * 1_000_003 + offset * 104_729 for offset in range(args.physics_seed_count)]
        chosen_bins: set[tuple[str, int, int]] = set()
        chosen_count = 0
        for input_values in manual_inputs():
            attempts += 1
            sample = build_sample(
                environment, board_name, board, input_values, seeds,
                float(args.old_stone_tolerance_m), float(args.maximum_seed_spread_m),
            )
            if sample is None:
                continue
            bin_key = target_bin(sample)
            if bin_key in chosen_bins:
                continue
            chosen_bins.add(bin_key)
            sample["id"] = f"手工正向净空_v0_{len(all_samples):04d}"
            all_samples.append(sample)
            chosen_count += 1
            if chosen_count >= args.max_samples_per_board:
                break
    payload = {
        "schema": "planning_proxy_manual_forward_fixture_set_v0",
        "scope": "手工摆盘面 + 手工限定输入网格 + 严格 PhysX 多种子正向复验；仅净空 draw",
        "manual_board_count": len(MANUAL_BOARDS),
        "forward_attempt_count": attempts,
        "physics_seed_count": int(args.physics_seed_count),
        "samples": all_samples,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "samples": len(all_samples), "attempts": attempts}, ensure_ascii=False))
    return 0 if all_samples else 2


if __name__ == "__main__":
    raise SystemExit(main())
