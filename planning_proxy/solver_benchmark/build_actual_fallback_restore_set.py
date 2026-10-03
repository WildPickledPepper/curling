#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从真实安全回退记录构造“补第二颗得分壶”的困难净空正样本。"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from planning_proxy.solver_benchmark.build_historical_recovery_draw_set import evaluate_input  # noqa: E402


OUTPUT = ROOT / "planning_proxy" / "solver_benchmark" / "actual_fallback_restore_draw_v1.json"

# 此输入表在数据构建前固定：来自两条严格成功的、绕守壶补第二得分层的历史出手。
# 它只用于离线证明“这张曾回退的盘面有解”，正式反解验收不读取它。
FIXED_INPUTS = (
    (3.17000004768372, 1.69499997615814, -15.0),
    (3.0577425430863, -1.188821419488, 6.41565997474422),
)


def signature(row: dict[str, Any]) -> tuple[Any, ...]:
    plan = row["detail"]["firstPlayerPlan"]
    board = tuple(
        (index, round(float(state["x"]) / 0.10), round(float(state["y"]) / 0.10))
        for index, state in enumerate(row["stateBefore"]) if bool(state.get("enabled", False))
    )
    target = tuple(round(float(value) / 0.10) for value in plan["target_points"][0])
    return board + (("target", *target),)


def candidate_rows() -> list[tuple[str, dict[str, Any]]]:
    rows = []
    seen: set[tuple[Any, ...]] = set()
    for path in sorted((ROOT / "planning_proxy" / "runs").glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            detail = row.get("detail") or {}
            plan = detail.get("firstPlayerPlan") or {}
            if not (
                row.get("type") == "shot" and row.get("actor") == "proxy"
                and detail.get("mode") == "first_player_safe_fallback_after_mads"
                and plan.get("phase") == "restore_second_scoring_stone"
                and plan.get("opponent_action") == "none"
                and len(plan.get("target_points", [])) == 1
                and float(row.get("decisionSeconds", 0.0)) >= 15.0
                and len(detail.get("physicsSeeds", [])) >= 3
            ):
                continue
            key = signature(row)
            if key in seen:
                continue
            seen.add(key)
            rows.append((path.relative_to(ROOT).as_posix(), row))
    return rows


def build_sample(source: str, row: dict[str, Any], input_values: tuple[float, float, float]) -> dict[str, Any]:
    plan = row["detail"]["firstPlayerPlan"]
    active_index = int(plan["shot_index"])
    target = tuple(float(value) for value in plan["target_points"][0])
    seeds = [int(seed) for seed in row["detail"]["physicsSeeds"]]
    report = evaluate_input(
        row["stateBefore"], active_index, seeds, input_values, target,
        float(plan["landing_region_radius_m"]), 0.035,
    )
    if not bool(report["passed"]):
        raise ValueError("调用者只能传入已正向通过的输入")
    board = [
        {"index": index, "owner": "self" if index % 2 == 0 else "opponent", "x": float(state["x"]),
         "y": float(state["y"]), "yaw": float(state.get("yaw", 0.0)), "enabled": True}
        for index, state in enumerate(row["stateBefore"]) if bool(state.get("enabled", False))
    ]
    return {
        "history_source": source, "fallback_shot": int(row["shot"]),
        "original_fallback_seconds": float(row["decisionSeconds"]),
        "category": "实战回退_K3补第二颗得分壶",
        "board": board,
        "goal_contract": {
            "version": "实战回退净空合同_v1", "kind": "补第二颗得分壶", "active_index": active_index,
            "active_target_region": {"center": list(target), "radius_m": float(plan["landing_region_radius_m"])},
            "must_preserve_indices": [stone["index"] for stone in board],
            "old_stone_position_tolerance_m": 0.035, "required_physics_seeds": seeds,
        },
        "oracle_witness": {"bestshot": list(input_values), "strict_forward": report["per_seed"]},
    }


def main() -> int:
    accepted = []
    for source, row in candidate_rows():
        for input_values in FIXED_INPUTS:
            plan = row["detail"]["firstPlayerPlan"]
            report = evaluate_input(
                row["stateBefore"], int(plan["shot_index"]), [int(seed) for seed in row["detail"]["physicsSeeds"]],
                input_values, tuple(float(value) for value in plan["target_points"][0]),
                float(plan["landing_region_radius_m"]), 0.035,
            )
            if bool(report["passed"]):
                accepted.append(build_sample(source, row, input_values))
                print(json.dumps({"来源": source, "原回退秒数": row["decisionSeconds"], "找到固定正向解": list(input_values)}, ensure_ascii=False), flush=True)
                break
    for index, sample in enumerate(accepted):
        sample["id"] = f"实战回退净空_v1_{index:03d}"
    payload = {
        "schema": "planning_proxy_actual_fallback_restore_draw_v1",
        "scope": "真实 safe_fallback_after_mads 壶面；回退至少 15 秒；固定离线输入表证明有解",
        "fixed_input_count": len(FIXED_INPUTS), "sample_count": len(accepted), "samples": accepted,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT), "samples": len(accepted)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
