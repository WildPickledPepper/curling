#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为历史困难净空盘面构造受控障碍位置变体，并先正向确认存在性。"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import STONE_COUNT  # noqa: E402
from planning_proxy.solver_benchmark.build_historical_recovery_draw_set import evaluate_input  # noqa: E402


SOURCE = ROOT / "planning_proxy" / "solver_benchmark" / "historical_targeted_draw_bulk_v2.json"
OUTPUT = ROOT / "planning_proxy" / "solver_benchmark" / "historical_targeted_draw_variants_v3.json"


def states_from_board(board: list[dict[str, Any]]) -> list[dict[str, Any]]:
    states = [{"enabled": False, "x": 0.0, "y": 0.0, "yaw": 0.0} for _ in range(STONE_COUNT)]
    for stone in board:
        states[int(stone["index"])] = dict(stone)
    return states


def perturb_front_obstacle(sample: dict[str, Any], delta_y: float) -> dict[str, Any] | None:
    """仅把最前方旧壶前/后移动 12 厘米；动作、目标和其它壶都不改。"""

    contract = sample["goal_contract"]
    active_index = int(contract["active_index"])
    old = [stone for stone in sample["board"] if int(stone["index"]) != active_index]
    if not old:
        return None
    # y 最大的是最靠近投壶入口的障碍壶，改变它最直接检验绕行通道的边界。
    moved_index = int(max(old, key=lambda stone: float(stone["y"]))["index"])
    board = [dict(stone) for stone in sample["board"]]
    for stone in board:
        if int(stone["index"]) == moved_index:
            stone["y"] = float(stone["y"]) + delta_y
    states = states_from_board(board)
    target = contract["active_target_region"]
    centre = tuple(float(value) for value in target["center"])
    shot = tuple(float(value) for value in sample["oracle_witness"]["bestshot"])
    report = evaluate_input(
        states, active_index, [int(seed) for seed in contract["required_physics_seeds"]], shot, centre,
        float(target["radius_m"]), float(contract["old_stone_position_tolerance_m"]),
    )
    if not bool(report["passed"]):
        return None
    result = dict(sample)
    result["board"] = board
    result["oracle_witness"] = {"bestshot": list(shot), "strict_forward": report["per_seed"]}
    result["controlled_variant"] = {"type": "最前方障碍壶纵向移动", "stone_index": moved_index, "delta_y_m": delta_y}
    return result


def main() -> int:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    # v2 中没有 centreline_mirrored 字段的 18 条才是原始历史结构。
    originals = [sample for sample in source["samples"] if not bool(sample.get("centreline_mirrored", False))]
    variants = []
    for sample in originals:
        for delta_y in (-0.12, 0.12):
            candidate = perturb_front_obstacle(sample, delta_y)
            if candidate is not None:
                variants.append(candidate)
    samples = list(source["samples"]) + variants
    for index, sample in enumerate(samples):
        sample["id"] = f"历史困难净空_v3_{index:03d}"
    payload = {
        "schema": "planning_proxy_historical_targeted_draw_variants_v3",
        "scope": "v2 的历史困难净空集，加最前方障碍壶前后 12 厘米受控变体；每条均三种子正向确认",
        "historical_original_structure_count": len(originals), "base_v2_sample_count": len(source["samples"]),
        "controlled_variant_count": len(variants), "sample_count": len(samples), "samples": samples,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT), "base": len(source["samples"]), "variants": len(variants), "total": len(samples)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
