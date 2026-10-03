#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把历史上曾回退、后来找到绕行解的真实壶面制成净空反解基准集。

这里允许读取历史对局的 ``stateBefore``，因为这些正是要复测的困难类别。
每一条仅以当时已经严格通过的出手为已知存在性证据；正式反解测试不会读取
``oracle_witness``。除原出手外，还正向检验六个事先写死的小扰动，用来量化
该路径是否狭窄，而不是用在线求解器生成任何测试答案。
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import HOUSE_X, STONE_COUNT, StrictCurlingEnd  # noqa: E402
from planning_proxy.competition_rules import RuleBoardStone, free_guard_rule_violations  # noqa: E402


OUTPUT = ROOT / "planning_proxy" / "solver_benchmark" / "historical_recovery_draw_v1.json"

# 这些条目不是“历史坐标查表策略”。它们是曾触发安全回退、随后在同类真实
# 对局中已由严格 PhysX 找到绕守壶重建锚解的困难壶面。三条分别来自三个摩擦
# 序列，盘面由对局自然形成。
BASE_CASES = (
    {
        "id": "历史K2_中线守壶绕行_20260720",
        "source": "planning_proxy/runs/ppo_k1k8_k8_connected_acceptance_seed20260720.jsonl",
        "shot": 3,
        # 这个原始壶面当时走了 safe_fallback_after_mads。下面的输入来自随后
        # 通过严格 PhysX 的同类 K2 绕行，不使用该回退球 (3, 0, 0)。
        "base_shot": (3.080000162124634, -1.8600000143051147, 8.571428298950195),
        "later_solution_source": "planning_proxy/runs/k3_guard_recovery_current_ppo_seed20713579_exact_full.jsonl:3",
        "category": "受保护中线守壶后的第一红圈锚绕行",
    },
    {
        "id": "历史K3_守壶对齐重建_20713579",
        "source": "planning_proxy/runs/k3_guard_recovery_current_ppo_seed20713579_exact_full.jsonl",
        "shot": 7,
        "prior_fallback_source": "planning_proxy/runs/k3_guard_aligned_recovery_ppo_seed20713579_exact_full.jsonl",
        "category": "中线守壶对齐后的红圈锚重建",
    },
    {
        "id": "历史K3_守壶对齐重建_21457791",
        "source": "planning_proxy/runs/k3_guard_recovery_current_ppo_seed21457791_exact_full.jsonl",
        "shot": 7,
        "prior_fallback_source": "planning_proxy/runs/k3_guard_aligned_recovery_ppo_seed21457791_exact_full.jsonl",
        "category": "中线守壶对齐后的红圈锚重建",
    },
    {
        "id": "历史K3_守壶对齐重建_21457792",
        "source": "planning_proxy/runs/k3_guard_recovery_current_ppo_seed21457792_exact_full.jsonl",
        "shot": 7,
        "prior_fallback_source": "planning_proxy/runs/k3_guard_aligned_recovery_ppo_seed21457792_exact_full.jsonl",
        "category": "中线守壶对齐后的红圈锚重建",
    },
)

# 对每条真实困难壶面做左右镜像。只有镜像后的固定输入在严格 PhysX 中仍通过，
# 才会作为独立的对称性测试样本写入数据集。
CASES = BASE_CASES + tuple({
    **case,
    "id": f"{case['id']}_左右镜像",
    "mirror_about_centreline": True,
} for case in BASE_CASES)


def read_shot(relative_path: str, shot_number: int) -> dict[str, Any]:
    path = ROOT / relative_path
    for line in path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row.get("type") == "shot" and int(row.get("shot", -1)) == shot_number:
            return row
    raise ValueError(f"{relative_path} 中没有第 {shot_number} 手")


def reset_data(states: list[dict[str, Any]]) -> tuple[list[float], dict[int, float]]:
    position = [0.0] * (STONE_COUNT * 2)
    yaws = {index: 0.0 for index in range(STONE_COUNT)}
    for index, state in enumerate(states):
        if bool(state.get("enabled", False)):
            position[2 * index] = float(state["x"])
            position[2 * index + 1] = float(state["y"])
            yaws[index] = float(state.get("yaw", 0.0))
    return position, yaws


def evaluate_input(
    states: list[dict[str, Any]],
    active_index: int,
    seeds: list[int],
    shot: tuple[float, float, float],
    target: tuple[float, float],
    radius: float,
    tolerance: float,
) -> dict[str, Any]:
    """独立严格正向检查一个写死的输入，不调用反解器。"""

    position, yaws = reset_data(states)
    old = {
        index: (float(state["x"]), float(state["y"]))
        for index, state in enumerate(states)
        if index != active_index and bool(state.get("enabled", False))
    }
    rule_board = [
        RuleBoardStone(index, "self" if index % 2 == 0 else "opponent", x, y, True)
        for index, (x, y) in old.items()
    ]
    environment = StrictCurlingEnd(seed=0, training_fast=True)
    rows: list[dict[str, Any]] = []
    passed = True
    for seed in seeds:
        environment.seed = int(seed) - active_index * 7919
        environment.scene.reset_positions(position, yaw_overrides=yaws)
        environment.shot_number = active_index
        result = environment.play(shot)
        final = result["states"]
        active = final[active_index]
        point = None if not bool(active.get("enabled", False)) else (float(active["x"]), float(active["y"]))
        error = math.inf if point is None else math.hypot(point[0] - target[0], point[1] - target[1])
        static = all(
            bool(final[index].get("enabled", False))
            and math.hypot(float(final[index]["x"]) - x, float(final[index]["y"]) - y) <= tolerance
            for index, (x, y) in old.items()
        )
        legal = not free_guard_rule_violations(rule_board, final, shot_index=active_index)
        row_passed = not bool(result.get("contact", False)) and static and legal and error <= radius
        passed = passed and row_passed
        rows.append({
            "physics_seed": seed, "passed": row_passed, "contact": bool(result.get("contact", False)),
            "old_stones_static": static, "rule_legal": legal, "landing_error_m": error,
            "active_final": None if point is None else list(point),
        })
    return {"passed": passed, "per_seed": rows}


def input_probes(base: tuple[float, float, float]) -> list[tuple[str, tuple[float, float, float]]]:
    v, h, w = base
    # 先验固定的七个测点；不根据仿真结果继续扩展。
    return [
        ("原历史解", base), ("速度减0.08", (v - 0.08, h, w)), ("速度加0.08", (v + 0.08, h, w)),
        ("横向减0.12", (v, h - 0.12, w)), ("横向加0.12", (v, h + 0.12, w)),
        ("旋转减2.14", (v, h, w - 2.14)), ("旋转加2.14", (v, h, w + 2.14)),
    ]


def build_case(spec: dict[str, Any]) -> dict[str, Any]:
    row = read_shot(str(spec["source"]), int(spec["shot"]))
    detail = row["detail"]
    plan = detail["firstPlayerPlan"]
    active_index = int(plan["shot_index"])
    if str(plan["opponent_action"]) != "none" or len(plan["target_points"]) != 1:
        raise ValueError(f"{spec['id']} 不是单目标净空绕行")
    states = [dict(state) for state in row["stateBefore"]]
    target = tuple(float(value) for value in plan["target_points"][0])
    radius = float(plan["landing_region_radius_m"])
    seeds = [int(seed) for seed in detail["physicsSeeds"]]
    base = tuple(float(value) for value in spec.get("base_shot", row["bestshot"]))
    if bool(spec.get("mirror_about_centreline", False)):
        for state in states:
            if bool(state.get("enabled", False)):
                state["x"] = 2.0 * HOUSE_X - float(state["x"])
                state["yaw"] = -float(state.get("yaw", 0.0))
        target = (2.0 * HOUSE_X - target[0], target[1])
        base = (base[0], -base[1], -base[2])
    tolerance = 0.035
    probe_rows = []
    for name, values in input_probes(base):
        report = evaluate_input(states, active_index, seeds, values, target, radius, tolerance)
        probe_rows.append({"name": name, "bestshot": list(values), **report})
    if not probe_rows[0]["passed"]:
        raise ValueError(f"{spec['id']} 的原历史解未能通过独立正向复验")
    board = [
        {"index": index, "owner": "self" if index % 2 == 0 else "opponent", "x": float(state["x"]),
         "y": float(state["y"]), "yaw": float(state.get("yaw", 0.0)), "enabled": True}
        for index, state in enumerate(states) if bool(state.get("enabled", False))
    ]
    return {
        "id": spec["id"], "category": spec["category"],
        "history_source": {
            "successful_replay": spec.get("later_solution_source", spec["source"]), "shot": spec["shot"],
            "earlier_fallback_replay": spec.get("prior_fallback_source", spec["source"]),
            "board_source": spec["source"],
            "centreline_mirrored": bool(spec.get("mirror_about_centreline", False)),
        },
        "board": board,
        "goal_contract": {
            "version": "历史困难净空绕行合同_v1", "kind": "绕守壶重建红圈锚", "active_index": active_index,
            "active_target_region": {"center": list(target), "radius_m": radius},
            "must_preserve_indices": [stone["index"] for stone in board],
            "old_stone_position_tolerance_m": tolerance, "required_physics_seeds": seeds,
        },
        "oracle_witness": {"bestshot": list(base), "strict_forward": probe_rows[0]["per_seed"]},
        "fixed_input_probe_report": probe_rows,
    }


def main() -> int:
    samples = [build_case(spec) for spec in CASES]
    payload = {
        "schema": "planning_proxy_historical_recovery_draw_set_v1",
        "scope": "历史真实壶面；曾安全回退、后来找到解的同类绕行盘面；固定输入正向复验",
        "sample_count": len(samples), "samples": samples,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    for sample in samples:
        probes = sample["fixed_input_probe_report"]
        print(json.dumps({"id": sample["id"], "原历史解通过": probes[0]["passed"],
                          "七个固定输入通过数": sum(bool(row["passed"]) for row in probes)}, ensure_ascii=False))
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
