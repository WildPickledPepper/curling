"""在已知单种子 witness 周围执行三物理种子严格局部搜索。

用于判断某个 witness 是否只是对摩擦种子不稳，或其邻域存在三种子共同满足
当前合同的输入。它不改状态机、候选排序或正式搜索器；局部盒未找到不等于
合同无解。
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
import time
from dataclasses import replace
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--shot", type=int, required=True)
    parser.add_argument("--center", type=float, nargs=3, metavar=("V0", "H0", "W0"), required=True)
    parser.add_argument("--mirror-current-plan", action="store_true")
    parser.add_argument(
        "--override-region-radius",
        type=float,
        help=(
            "仅离线：同时替换当前合同与其防御形的落区半径。"
            "用于区分窄合同边界与局部路径覆盖；不修改状态机。"
        ),
    )
    parser.add_argument("--span", type=float, nargs=3, default=(0.08, 0.08, 0.8), metavar=("DV", "DH", "DW"))
    parser.add_argument("--points", type=int, default=5, help="每维等距点数，必须为奇数。")
    parser.add_argument("--budget", type=float, default=60.0)
    parser.add_argument("--extension", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def centered_offsets(span: float, count: int) -> list[float]:
    if count < 1 or count % 2 == 0:
        raise ValueError("--points 必须是正奇数")
    if count == 1:
        return [0.0]
    return [span * (-1.0 + 2.0 * index / float(count - 1)) for index in range(count)]


def main() -> None:
    args = parse_args()
    from local_simulator import runtime_loader
    if args.extension is not None:
        extension = args.extension.resolve()
        if not extension.is_file():
            raise SystemExit(f"候选原生扩展不存在：{extension}")
        runtime_dir = ROOT / "local_simulator" / "runtime" / "pyphysx"
        if str(runtime_dir) not in sys.path:
            sys.path.insert(0, str(runtime_dir))
        runtime_loader.BUNDLED_EXTENSION = extension
    pyphysx = runtime_loader.install_bundled_pyphysx()
    from local_simulator.examples.train_policy_tree_selfplay import HOUSE_X, StrictCurlingEnd
    from planning_proxy.evaluate_vs_teammate_ppo import canonical_board
    from planning_proxy.first_player_strategy import plan_first_player_turn
    from planning_proxy.strict_refine import Candidate, evaluate_one, make_position

    report = json.loads(args.source.read_text(encoding="utf-8"))
    game = report.get("game", {})
    row = next((item for item in game.get("trace", []) if int(item.get("shot", -1)) == args.shot), None)
    if not isinstance(row, dict) or not isinstance(row.get("stateBefore"), list):
        raise SystemExit("目标手缺少 stateBefore")
    active_index = args.shot - 1
    strict_board, proxy_board = canonical_board(row["stateBefore"], 0)
    plan = plan_first_player_turn(proxy_board, active_index)
    if plan is None:
        raise SystemExit("该手没有当前先手状态机合同")
    if args.mirror_current_plan:
        plan = replace(
            plan,
            phase=f"{plan.phase}_mirror_region",
            target_points=tuple((2.0 * HOUSE_X - x, y) for x, y in plan.target_points),
            defence_shapes=tuple(
                replace(shape, active_targets=tuple((2.0 * HOUSE_X - x, y) for x, y in shape.active_targets))
                for shape in plan.defence_shapes
            ),
            rationale=f"{plan.rationale}；局部搜索镜像防御区。",
        )
    if args.override_region_radius is not None:
        if float(args.override_region_radius) <= 0.0:
            raise SystemExit("--override-region-radius 必须为正数")
        plan = replace(
            plan,
            landing_region_radius_m=float(args.override_region_radius),
            defence_shapes=tuple(
                replace(shape, landing_region_radius_m=float(args.override_region_radius))
                for shape in plan.defence_shapes
            ),
            rationale=f"{plan.rationale}；仅离线覆盖诊断半径={float(args.override_region_radius):.6f}m。",
        )
    match_seed = int(game.get("seed", report.get("sourceSeed", 0)))
    seeds = [match_seed + active_index * 7919 + 104729 * offset for offset in range(3)]
    target = tuple(float(value) for value in plan.target_points[0]) if plan.target_points else None
    offsets = list(itertools.product(*(centered_offsets(float(span), args.points) for span in args.span)))
    # 先测中心及较近点，便于在预算内尽量完成连通局部盒的核心。
    offsets.sort(key=lambda values: sum((values[index] / float(args.span[index])) ** 2 if args.span[index] else 0.0 for index in range(3)))
    environment = StrictCurlingEnd(seed=match_seed, training_fast=True)
    started = time.perf_counter()
    rows: list[dict[str, Any]] = []
    for rank, delta in enumerate(offsets, 1):
        if time.perf_counter() - started >= args.budget:
            break
        action = tuple(float(args.center[index]) + float(delta[index]) for index in range(3))
        evaluation = evaluate_one(
            environment, Candidate(*action, parent_rank=rank), strict_board, make_position(strict_board), seeds,
            active_index, active_index=active_index, tactical_plan=plan,
        )
        positions = evaluation.active_final_positions
        distances = (
            [math.dist((float(point[0]), float(point[1])), target) for point in positions if point is not None]
            if target is not None else []
        )
        rows.append({
            "action": list(action),
            "delta": list(delta),
            "goalBySeed": [bool(value) for value in evaluation.tactical_goal_met],
            "allGoal": bool(evaluation.tactical_goal_met) and all(evaluation.tactical_goal_met),
            "enemyCleared": [int(value) for value in evaluation.enemy_cleared],
            "selfCleared": [int(value) for value in evaluation.total_self_cleared],
            "ruleLegal": bool(evaluation.rule_legal),
            "activeFinalPositions": [list(point) if point is not None else None for point in positions],
            "worstTargetDistance": max(distances) if len(distances) == len(seeds) else None,
            "meanTargetDistance": sum(distances) / len(distances) if len(distances) == len(seeds) else None,
        })
    ordered = sorted(
        rows,
        key=lambda item: (
            not bool(item["allGoal"]),
            -sum(item["goalBySeed"]),
            float(item["worstTargetDistance"]) if item["worstTargetDistance"] is not None else float("inf"),
        ),
    )
    output = {
        "schema": "strict_multiseed_neighborhood_v1",
        "scope": {
            "source": str(args.source), "shot": args.shot, "matchSeed": match_seed,
            "physicsSeeds": seeds, "center": list(args.center), "span": list(args.span),
            "pointsPerDimension": args.points, "candidateBoxSize": len(offsets), "budgetSeconds": args.budget,
            "overrideRegionRadiusM": args.override_region_radius,
            "extension": str(getattr(pyphysx, "__file__", "")),
            "limitation": "局部盒未找到不证明合同无解。",
        },
        "plan": plan.to_json(),
        "elapsedSeconds": time.perf_counter() - started,
        "evaluated": len(rows),
        "allGoalCount": sum(bool(row["allGoal"]) for row in rows),
        "topCandidates": ordered[:20],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: output[key] for key in ("elapsedSeconds", "evaluated", "allGoalCount")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
