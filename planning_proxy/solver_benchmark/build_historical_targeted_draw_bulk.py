#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从历史困难类别中提取去重后的单目标净空正样本。

这是离线数据构建器：只使用历史记录中的成功出手做正向存在性复验。运行时
反解器不会读取 ``oracle_witness``。每条样本必须在记录所用的三个物理种子
上重新通过“不撞旧壶、旧壶不动、进入声明目标区”的严格检查。
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from planning_proxy.solver_benchmark.build_historical_recovery_draw_set import evaluate_input  # noqa: E402
from local_simulator.examples.train_policy_tree_selfplay import HOUSE_X, STONE_COUNT  # noqa: E402


OUTPUT = ROOT / "planning_proxy" / "solver_benchmark" / "historical_targeted_draw_bulk_v2.json"

# 只取此前出现过回退或需要长时间反解的结构。每类限制样本数，避免同一局面
# 的多次回放在统计上反复计数。
QUOTAS = {
    ("process_first_enemy_and_score", "DRAW_FIRST_INNER_ANCHOR"): 12,
    ("fourth_rebuild_first_anchor_around_centre_guard", "REBUILD_FIRST_INNER_ANCHOR_AROUND_CENTRE_GUARD"): 10,
    ("fifth_add_second_staggered_inner_layer", "ADD_SECOND_STAGGERED_INNER_LAYER"): 7,
    ("restore_second_scoring_stone", "RESTORE_STAGGERED_INNER_PAIR"): 2,
    ("seventh_add_second_scoring_layer_without_enemy_house_threat", "ADD_SECOND_SCORING_LAYER_WITH_EXTERNAL_OBSTACLES"): 3,
    ("seventh_outdraw_single_outer_house_threat", "OUTDRAW_SINGLE_OUTER_HOUSE_THREAT"): 2,
    ("screen_single_inner_anchor", "ADD_ANCHOR_SIDE_SCREEN"): 1,
    ("sixth_add_second_inner_layer_around_external_guard", "ADD_SECOND_INNER_LAYER_AROUND_EXTERNAL_GUARD"): 1,
}


def board_signature(row: dict[str, Any], active_index: int, target: tuple[float, float]) -> tuple[Any, ...]:
    stones = tuple(
        (index, round(float(state["x"]) / 0.10), round(float(state["y"]) / 0.10))
        for index, state in enumerate(row["stateBefore"])
        if bool(state.get("enabled", False)) and index != active_index
    )
    return stones + (("target", round(target[0] / 0.10), round(target[1] / 0.10)),)


def build_candidate(relative_path: str, row: dict[str, Any]) -> dict[str, Any] | None:
    detail = row.get("detail", {})
    plan = detail.get("firstPlayerPlan") or {}
    phase_strategy = (str(plan.get("phase", "")), str(plan.get("strategy_type", "")))
    if phase_strategy not in QUOTAS:
        return None
    if str(detail.get("mode")) != "first_player_targeted_physx_inverse":
        return None
    if str(plan.get("opponent_action")) != "none" or len(plan.get("target_points", [])) != 1:
        return None
    if bool(row.get("contact", True)):
        return None
    seeds = [int(seed) for seed in detail.get("physicsSeeds", [])]
    if len(seeds) < 3:
        return None
    active_index = int(plan["shot_index"])
    states = [dict(state) for state in row["stateBefore"]]
    target = tuple(float(value) for value in plan["target_points"][0])
    radius = float(plan["landing_region_radius_m"])
    shot = tuple(float(value) for value in row["bestshot"])
    report = evaluate_input(states, active_index, seeds, shot, target, radius, 0.035)
    if not bool(report["passed"]):
        return None
    board = [
        {"index": index, "owner": "self" if index % 2 == 0 else "opponent", "x": float(state["x"]),
         "y": float(state["y"]), "yaw": float(state.get("yaw", 0.0)), "enabled": True}
        for index, state in enumerate(states) if bool(state.get("enabled", False))
    ]
    return {
        "phase_strategy": phase_strategy,
        "signature": board_signature(row, active_index, target),
        "source": relative_path,
        "source_shot": int(row["shot"]),
        "board": board,
        "goal_contract": {
            "version": "历史困难类别净空合同_v2", "kind": "历史单目标净空反解",
            "active_index": active_index, "active_target_region": {"center": list(target), "radius_m": radius},
            "must_preserve_indices": [stone["index"] for stone in board],
            "old_stone_position_tolerance_m": 0.035, "required_physics_seeds": seeds,
        },
        "oracle_witness": {"bestshot": list(shot), "strict_forward": report["per_seed"]},
    }


def mirror_candidate(candidate: dict[str, Any]) -> dict[str, Any] | None:
    """独立正向确认左右镜像，不假定物理引擎一定完全对称。"""

    contract = candidate["goal_contract"]
    active_index = int(contract["active_index"])
    states = [{"enabled": False, "x": 0.0, "y": 0.0, "yaw": 0.0} for _ in range(STONE_COUNT)]
    mirrored_board = []
    for stone in candidate["board"]:
        mirrored = dict(stone)
        mirrored["x"] = 2.0 * HOUSE_X - float(stone["x"])
        mirrored["yaw"] = -float(stone.get("yaw", 0.0))
        states[int(mirrored["index"])] = dict(mirrored)
        mirrored_board.append(mirrored)
    target = contract["active_target_region"]
    centre = (2.0 * HOUSE_X - float(target["center"][0]), float(target["center"][1]))
    base = candidate["oracle_witness"]["bestshot"]
    shot = (float(base[0]), -float(base[1]), -float(base[2]))
    report = evaluate_input(
        states, active_index, [int(seed) for seed in contract["required_physics_seeds"]], shot, centre,
        float(target["radius_m"]), float(contract["old_stone_position_tolerance_m"]),
    )
    if not bool(report["passed"]):
        return None
    mirror = dict(candidate)
    mirror["source"] = f"{candidate['source']} [左右镜像]"
    mirror["board"] = mirrored_board
    mirror["goal_contract"] = {**contract, "active_target_region": {"center": list(centre), "radius_m": float(target["radius_m"])}}
    mirror["oracle_witness"] = {"bestshot": list(shot), "strict_forward": report["per_seed"]}
    mirror["centreline_mirrored"] = True
    return mirror


def main() -> int:
    selected: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    seen: dict[tuple[str, str], set[tuple[Any, ...]]] = defaultdict(set)
    considered: dict[tuple[str, str], set[tuple[Any, ...]]] = defaultdict(set)
    for path in sorted((ROOT / "planning_proxy" / "runs").glob("*.jsonl")):
        relative_path = path.relative_to(ROOT).as_posix()
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("type") != "shot" or row.get("actor") != "proxy":
                continue
            # 在昂贵的三种子正向复验之前，先按类别、壶面和目标区去掉重复回放。
            detail = row.get("detail", {})
            plan = detail.get("firstPlayerPlan") or {}
            key = (str(plan.get("phase", "")), str(plan.get("strategy_type", "")))
            if key not in QUOTAS or len(selected[key]) >= QUOTAS[key]:
                continue
            if str(detail.get("mode")) != "first_player_targeted_physx_inverse":
                continue
            if str(plan.get("opponent_action")) != "none" or len(plan.get("target_points", [])) != 1:
                continue
            raw_signature = board_signature(
                row, int(plan["shot_index"]), tuple(float(value) for value in plan["target_points"][0])
            )
            if raw_signature in considered[key]:
                continue
            considered[key].add(raw_signature)
            candidate = build_candidate(relative_path, row)
            if candidate is None:
                continue
            if candidate["signature"] in seen[key]:
                continue
            seen[key].add(candidate["signature"])
            selected[key].append(candidate)
            print(json.dumps({"类别": list(key), "已收集": len(selected[key]), "来源": relative_path, "手": row["shot"]}, ensure_ascii=False), flush=True)
    originals: list[dict[str, Any]] = []
    for key in QUOTAS:
        for candidate in selected[key]:
            candidate["category"] = {"phase": key[0], "strategy": key[1]}
            del candidate["phase_strategy"]
            del candidate["signature"]
            originals.append(candidate)
    mirrors = [mirror for candidate in originals if (mirror := mirror_candidate(candidate)) is not None]
    samples = originals + mirrors
    for index, candidate in enumerate(samples):
        candidate["id"] = f"历史困难净空_v2_{index:03d}"
    counts = {f"{key[0]} / {key[1]}": len(selected[key]) for key in QUOTAS}
    payload = {
        "schema": "planning_proxy_historical_targeted_draw_bulk_v2",
        "scope": "从历史困难类别抽取、按壶面和目标区去重、严格 PhysX 多种子正向确认的净空正样本",
        "requested_quota": {f"{key[0]} / {key[1]}": value for key, value in QUOTAS.items()},
        "accepted_by_category": counts, "original_structure_count": len(originals),
        "strictly_verified_mirror_count": len(mirrors), "sample_count": len(samples), "samples": samples,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT), "sample_count": len(samples), "accepted_by_category": counts}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
