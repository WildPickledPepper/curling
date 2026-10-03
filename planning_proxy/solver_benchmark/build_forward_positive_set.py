#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""正向构造“确实有解”的鲁棒净空 draw 基准集。

这个工具不参与比赛策略，也不会把生成的 witness 参数交给线上求解器。
它做的只是为求解器召回率建立分母：

    (可达盘面 S, 自动归纳的目标合同 G, 严格 PhysX witness)

每条样本均由同一输入在多个摩擦种子上正向严格 PhysX 验证。v0 只收集
不移动任何旧壶的净空 draw；接触型清壶、推壶和滚位应另建 v1，而不能
混进这个基准集后伪造“反解不漏”的指标。
"""

from __future__ import annotations

import argparse
import glob
import json
import math
import sys
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import (  # noqa: E402
    HOUSE_R,
    HOUSE_X,
    HOUSE_Y,
    STONE_COUNT,
    STONE_R,
    StrictCurlingEnd,
)
from planning_proxy.competition_rules import (  # noqa: E402
    RuleBoardStone,
    free_guard_rule_violations,
    is_in_free_guard_zone,
)


DEFAULT_OUTPUT = ROOT / "planning_proxy" / "solver_benchmark" / "forward_positive_draw_v0.json"


def halton(index: int, base: int) -> float:
    """确定性低差异序列；不依赖随机数，便于以后完全复现基准集。"""

    value = 0.0
    factor = 1.0
    number = int(index)
    while number:
        factor /= float(base)
        value += factor * float(number % base)
        number //= base
    return value


def candidate_stream(count: int, *, offset: int = 0) -> Iterable[tuple[float, float, float]]:
    """覆盖常用 draw 速度、横移与正反旋；不是线上反解算法。"""

    for index in range(int(offset) + 1, int(offset) + int(count) + 1):
        yield (
            2.70 + 3.10 * halton(index, 2),
            -1.85 + 3.70 * halton(index, 3),
            -15.0 + 30.0 * halton(index, 5),
        )


def read_source_states(pattern: str, limit: int, min_existing_stones: int) -> list[dict[str, Any]]:
    """从已有完整/分段对局报告读取真实连续 PhysX 壶面。"""

    states: list[dict[str, Any]] = []
    seen: set[tuple[str, int, int]] = set()
    for raw_path in sorted(glob.glob(pattern)):
        path = Path(raw_path)
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for game in report.get("games", []):
            for trace in game.get("trace", []):
                if trace.get("type") != "shot" or not isinstance(trace.get("stateBefore"), list):
                    continue
                shot_index = int(trace.get("shot", 0)) - 1
                if not 0 <= shot_index < STONE_COUNT:
                    continue
                key = (str(path.resolve()), int(game.get("seed", -1)), shot_index)
                if key in seen:
                    continue
                seen.add(key)
                snapshot = trace["stateBefore"]
                existing_count = sum(bool(item.get("enabled", False)) for item in snapshot)
                if existing_count < int(min_existing_stones):
                    continue
                states.append({
                    "source_report": str(path.relative_to(ROOT)).replace("\\", "/"),
                    "match_seed": int(game.get("seed", -1)),
                    "shot_index": shot_index,
                    "acting_team": shot_index % 2,
                    "existing_stone_count": existing_count,
                    "states": snapshot,
                })
    # 不能按文件顺序截断：那会把基准集锁在某一局的开局。按“第几手 ×
    # 壶数”分层轮转，优先覆盖结构差异，不需要离线枚举所有壶面。
    buckets: dict[tuple[int, int], list[dict[str, Any]]] = {}
    for state in states:
        buckets.setdefault((int(state["shot_index"]), int(state["existing_stone_count"])), []).append(state)
    selected: list[dict[str, Any]] = []
    cursor = 0
    ordered = [buckets[key] for key in sorted(buckets)]
    while len(selected) < int(limit):
        progressed = False
        for bucket in ordered:
            if cursor < len(bucket):
                selected.append(bucket[cursor])
                progressed = True
                if len(selected) >= int(limit):
                    break
        if not progressed:
            break
        cursor += 1
    return selected


def enabled_board(states: list[dict[str, Any]], acting_team: int) -> list[dict[str, Any]]:
    return [
        {
            "index": index,
            "owner": "self" if index % 2 == int(acting_team) else "opponent",
            "x": float(state["x"]),
            "y": float(state["y"]),
            "yaw": float(state.get("yaw", 0.0)),
            "enabled": True,
        }
        for index, state in enumerate(states)
        if bool(state.get("enabled", False))
    ]


def reset_position(states: list[dict[str, Any]]) -> tuple[list[float], dict[int, float]]:
    position = [0.0] * (STONE_COUNT * 2)
    yaw_overrides: dict[int, float] = {index: 0.0 for index in range(STONE_COUNT)}
    for index, state in enumerate(states):
        if bool(state.get("enabled", False)):
            position[2 * index] = float(state["x"])
            position[2 * index + 1] = float(state["y"])
            yaw_overrides[index] = float(state.get("yaw", 0.0))
    return position, yaw_overrides


def distance(left: tuple[float, float], right: tuple[float, float]) -> float:
    return math.hypot(left[0] - right[0], left[1] - right[1])


def forward_draw_witness(
    *,
    environment: StrictCurlingEnd,
    states: list[dict[str, Any]],
    shot_index: int,
    acting_team: int,
    shot: tuple[float, float, float],
    physics_seeds: list[int],
    old_stone_tolerance: float,
    maximum_seed_spread: float,
) -> dict[str, Any] | None:
    """正向验证一个净空 draw，并把严格结果归纳为可复测目标合同。"""

    board = enabled_board(states, acting_team)
    position, yaws = reset_position(states)
    active_index = int(shot_index)
    initial = {int(stone["index"]): (float(stone["x"]), float(stone["y"])) for stone in board}
    finals: list[dict[str, Any]] = []
    active_positions: list[tuple[float, float]] = []

    for physics_seed in physics_seeds:
        environment.seed = int(physics_seed) - active_index * 7919
        environment.scene.reset_positions(position, yaw_overrides=yaws)
        environment.shot_number = active_index
        result = environment.play(shot)
        final_states = result["states"]
        rules = free_guard_rule_violations(
            [RuleBoardStone(int(stone["index"]), str(stone["owner"]), float(stone["x"]), float(stone["y"]), True) for stone in board],
            final_states,
            shot_index=active_index,
        )
        if rules or bool(result.get("contact", False)) or not bool(final_states[active_index].get("enabled", False)):
            return None
        # v0 的合同是净空：任一旧壶出界或移动超过容差均拒绝。
        for index, point in initial.items():
            state = final_states[index]
            if not bool(state.get("enabled", False)):
                return None
            if distance(point, (float(state["x"]), float(state["y"]))) > old_stone_tolerance:
                return None
        active = final_states[active_index]
        active_position = (float(active["x"]), float(active["y"]))
        active_positions.append(active_position)
        finals.append({
            "physics_seed": int(physics_seed),
            "active_final": [active_position[0], active_position[1]],
            "contact": bool(result.get("contact", False)),
            "cleared": [int(index) for index in result.get("cleared", [])],
        })

    centre = (
        sum(point[0] for point in active_positions) / len(active_positions),
        sum(point[1] for point in active_positions) / len(active_positions),
    )
    spread = max(distance(point, centre) for point in active_positions)
    if spread > maximum_seed_spread:
        return None
    radius = max(0.10, spread + 0.04)
    all_house = all(math.hypot(point[0] - HOUSE_X, point[1] - HOUSE_Y) <= HOUSE_R + STONE_R for point in active_positions)
    all_guard = all(is_in_free_guard_zone(point[0], point[1]) for point in active_positions)
    if not (all_house or all_guard):
        return None
    role = "house_draw" if all_house else "front_guard_draw"
    return {
        "goal_contract": {
            "version": "forward_draw_contract_v0",
            "kind": role,
            "active_index": active_index,
            "active_target_region": {"center": [centre[0], centre[1]], "radius_m": radius},
            "must_preserve_indices": sorted(initial),
            "old_stone_position_tolerance_m": old_stone_tolerance,
            "rule_legal": True,
            "required_physics_seeds": list(physics_seeds),
        },
        "oracle_witness": {"bestshot": [float(value) for value in shot], "strict_forward": finals},
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-glob", default=str(ROOT / "planning_proxy" / "runs" / "*.json"))
    parser.add_argument("--source-states", type=int, default=24)
    parser.add_argument("--min-existing-stones", type=int, default=3)
    parser.add_argument("--candidates-per-state", type=int, default=18)
    parser.add_argument("--samples", type=int, default=20)
    parser.add_argument("--physics-seed", type=int, default=20260720)
    parser.add_argument("--physics-seed-count", type=int, default=3)
    parser.add_argument("--old-stone-tolerance-m", type=float, default=0.035)
    parser.add_argument("--maximum-seed-spread-m", type=float, default=0.075)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.source_states < 1 or args.candidates_per_state < 1 or args.samples < 1 or args.physics_seed_count < 1:
        raise SystemExit("样本数、候选数与物理种子数必须为正")
    source_states = read_source_states(args.source_glob, args.source_states, args.min_existing_stones)
    if not source_states:
        raise SystemExit("没有从 source-glob 找到可用的连续对局报告")
    environment = StrictCurlingEnd(seed=0, training_fast=True)
    samples: list[dict[str, Any]] = []
    attempts = 0
    for state_rank, source in enumerate(source_states):
        seeds = [int(args.physics_seed) + state_rank * 1_000_003 + offset * 104_729 for offset in range(args.physics_seed_count)]
        for shot in candidate_stream(args.candidates_per_state, offset=state_rank * args.candidates_per_state):
            attempts += 1
            witness = forward_draw_witness(
                environment=environment,
                states=source["states"],
                shot_index=int(source["shot_index"]),
                acting_team=int(source["acting_team"]),
                shot=shot,
                physics_seeds=seeds,
                old_stone_tolerance=float(args.old_stone_tolerance_m),
                maximum_seed_spread=float(args.maximum_seed_spread_m),
            )
            if witness is None:
                continue
            samples.append({
                "id": f"forward_draw_v0_{len(samples):04d}",
                "source": {key: value for key, value in source.items() if key != "states"},
                "board": enabled_board(source["states"], int(source["acting_team"])),
                **witness,
            })
            if len(samples) >= args.samples:
                break
        if len(samples) >= args.samples:
            break
    payload = {
        "schema": "planning_proxy_forward_positive_set_v0",
        "scope": "strict PhysX robust positive fixtures; no-contact draw only",
        "source_state_count": len(source_states),
        "forward_attempt_count": attempts,
        "physics_seed_count": int(args.physics_seed_count),
        "samples": samples,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "samples": len(samples), "attempts": attempts}, ensure_ascii=False))
    return 0 if samples else 2


if __name__ == "__main__":
    raise SystemExit(main())
