#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""对一条已记录盘面的严格 PhysX 候选做重复分段测时。

它不运行状态机、不生成候选，也不改变生产逻辑。用途是复现某一严格候选的
“滑至首次碰撞”尾部耗时，并同时记录原生循环返回的物理步数和是否真的接触。
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import replace
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="含 game.trace 的真实续局报告")
    parser.add_argument("--shot", type=int, required=True, help="目标投壶编号（1..16）")
    parser.add_argument("--action", type=float, nargs=3, metavar=("V0", "H0", "W0"), required=True)
    parser.add_argument("--physics-seed", type=int, action="append", default=None, help="可重复指定；默认使用该手真实摩擦种子")
    parser.add_argument(
        "--three-standard-seeds",
        action="store_true",
        help="使用正式规划器该手的三条标准物理种子；不能与 --physics-seed 同时使用。",
    )
    parser.add_argument("--repeat", type=int, default=3, help="同一候选重复次数")
    parser.add_argument("--include-free-slide", action="store_true", help="额外测量无目标壶时的原生滑行步数；默认关闭。")
    parser.add_argument(
        "--current-plan",
        action="store_true",
        help="把当前状态机从 stateBefore 生成的合同传入严格回放，验证合同判定；默认不传合同。",
    )
    parser.add_argument(
        "--mirror-current-plan",
        action="store_true",
        help="传入当前状态机合同的镜像防御区版本；仅用于镜像分支回归。",
    )
    parser.add_argument(
        "--landing-radius",
        type=float,
        help="仅离线覆盖合同落点半径；用于诊断半径是否为唯一失败条件。",
    )
    parser.add_argument("--extension", type=Path, help="可选：仅本进程临时加载指定 CP39 原生扩展，不覆盖运行时文件。")
    parser.add_argument(
        "--native-timing",
        action="store_true",
        help="读取带诊断计时功能的隔离扩展的首碰撞循环分段时间；普通运行时扩展不支持。",
    )
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.repeat < 1:
        raise SystemExit("--repeat 必须为正数")
    if args.physics_seed is not None and args.three_standard_seeds:
        raise SystemExit("--physics-seed 与 --three-standard-seeds 不能同时使用")
    if args.current_plan and args.mirror_current_plan:
        raise SystemExit("--current-plan 与 --mirror-current-plan 不能同时使用")
    from local_simulator import runtime_loader

    if args.extension is not None:
        extension = args.extension.resolve()
        if not extension.is_file():
            raise SystemExit(f"候选原生扩展不存在：{extension}")
        runtime_dir = PROJECT_ROOT / "local_simulator" / "runtime" / "pyphysx"
        if str(runtime_dir) not in sys.path:
            sys.path.insert(0, str(runtime_dir))
        runtime_loader.BUNDLED_EXTENSION = extension
    pyphysx = runtime_loader.install_bundled_pyphysx()
    native_timing_getter = getattr(pyphysx, "get_curling_first_contact_timing", None)
    if args.native_timing and native_timing_getter is None:
        raise SystemExit("当前扩展未编入首碰撞原生计时；请使用独立诊断构建。")
    from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd
    from planning_proxy.evaluate_vs_teammate_ppo import canonical_board
    from planning_proxy.first_player_strategy import HOUSE_X, plan_first_player_turn
    from planning_proxy.strict_refine import Candidate, evaluate_one, make_position

    source = json.loads(args.source.read_text(encoding="utf-8"))
    game = source.get("game", {})
    row = next((item for item in game.get("trace", []) if int(item.get("shot", -1)) == int(args.shot)), None)
    if row is None or not isinstance(row.get("stateBefore"), list):
        raise SystemExit(f"来源报告缺少第 {args.shot} 手的 stateBefore")
    active_index = int(args.shot) - 1
    match_seed = int(game.get("seed", source.get("sourceSeed", 0)))
    physics_seeds = (
        [match_seed + active_index * 7919 + 104729 * offset for offset in range(3)]
        if args.three_standard_seeds
        else args.physics_seed or [match_seed + active_index * 7919]
    )
    strict_board, proxy_board = canonical_board(row["stateBefore"], proxy_team=0)
    position = make_position(strict_board)
    tactical_plan = plan_first_player_turn(proxy_board, active_index) if (args.current_plan or args.mirror_current_plan) else None
    if args.mirror_current_plan:
        if tactical_plan is None:
            raise SystemExit("该手没有先手状态机合同，不能生成镜像合同")
        tactical_plan = replace(
            tactical_plan,
            phase=f"{tactical_plan.phase}_mirror_region",
            target_points=tuple((2.0 * HOUSE_X - x, y) for x, y in tactical_plan.target_points),
            defence_shapes=tuple(
                replace(
                    shape,
                    active_targets=tuple((2.0 * HOUSE_X - x, y) for x, y in shape.active_targets),
                )
                for shape in tactical_plan.defence_shapes
            ),
            rationale=f"{tactical_plan.rationale}；原防御区域无解时，尝试关于中线的对称防御区域。",
        )
    if args.landing_radius is not None:
        if tactical_plan is None or args.landing_radius <= 0.0:
            raise SystemExit("--landing-radius 需要正数且必须同时指定当前或镜像合同")
        tactical_plan = replace(tactical_plan, landing_region_radius_m=float(args.landing_radius))
    candidate = Candidate(*[float(value) for value in args.action], parent_rank=1)
    environment = StrictCurlingEnd(seed=match_seed, training_fast=True)

    original_front_half = environment.scene.run_bestshot_to_first_contact_training
    front_calls: list[dict[str, Any]] = []

    def timed_front_half(*call_args: Any, **call_kwargs: Any) -> dict[str, Any]:
        started = time.perf_counter()
        result = original_front_half(*call_args, **call_kwargs)
        call_record = {
            "seconds": time.perf_counter() - started,
            "steps": int(result.get("steps", -1)),
            "reachedFirstContact": bool(result.get("reachedFirstContact", False)),
            "nativeLoop": bool(result.get("nativeLoop", False)),
        }
        if args.native_timing:
            # 原生扩展仅保存刚刚完成的本线程首碰撞调用；读取操作不影响物理。
            call_record["nativeTiming"] = dict(native_timing_getter())
        front_calls.append(call_record)
        return result

    environment.scene.run_bestshot_to_first_contact_training = timed_front_half
    repeats: list[dict[str, Any]] = []
    for repeat_index in range(int(args.repeat)):
        start_call = len(front_calls)
        started = time.perf_counter()
        evaluation = evaluate_one(
            environment,
            candidate,
            strict_board,
            position,
            physics_seeds,
            active_index,
            active_index=active_index,
            tactical_plan=tactical_plan,
        )
        repeats.append({
            "repeat": repeat_index + 1,
            "seconds": time.perf_counter() - started,
            "frontHalf": front_calls[start_call:],
            "enemyCleared": evaluation.enemy_cleared,
            "ownCleared": evaluation.own_cleared,
            "activeCleared": evaluation.active_cleared,
            # 保留逐种子终局壶面，供不同原生扩展做逐壶等价比较。该字段只
            # 来自严格 PhysX 的 evaluate_one，不参与候选选择或合同判断。
            "strictEvaluation": evaluation.to_json(),
        })

    # 同一摩擦种子、同一输入在无目标壶时的严格原生滑行步数。它不替代带
    # 目标壶的回放，只用于测量“若始终未碰撞，物理上何时已静止”。
    free_slide: list[dict[str, Any]] = []
    if args.include_free_slide:
        for physics_seed in physics_seeds:
            free_environment = StrictCurlingEnd(seed=match_seed, training_fast=True)
            free_environment.scene.reset_positions([0.0] * 32, yaw_overrides={index: 0.0 for index in range(16)})
            free_environment.scene.start_bestshot(active_index, args.action, yaw=0.0)
            native_quiet = getattr(free_environment.scene.scene, "simulate_curling_until_quiet_seeded", None)
            if native_quiet is None:
                raise RuntimeError("当前原生扩展没有 simulate_curling_until_quiet_seeded")
            started = time.perf_counter()
            steps = native_quiet(
                free_environment.scene.slots[active_index].body,
                int(physics_seed),
                free_environment.scene.dt,
                5000,
                free_environment.scene.custom_sliding_zero_vertical_setter,
                free_environment.scene.emulate_unity_native_angular_setter_tilt_only,
            )
            state = free_environment.scene.state(active_index)
            free_slide.append({
                "physicsSeed": int(physics_seed),
                "seconds": time.perf_counter() - started,
                "steps": int(steps),
                "settledByLinearSpeed": bool((float(state["vx"]) ** 2 + float(state["vy"]) ** 2) ** 0.5 <= 0.01),
            })

    report = {
        "schema": "strict_candidate_tail_probe_v1",
        "scope": "diagnostic only; no state-machine or solver change",
        "source": str(args.source),
        "shot": int(args.shot),
        "matchSeed": match_seed,
        "extension": str(getattr(pyphysx, "__file__", "")),
        "physicsSeeds": [int(seed) for seed in physics_seeds],
        "action": [float(value) for value in args.action],
        "currentPlan": tactical_plan.to_json() if tactical_plan is not None else None,
        "repeat": repeats,
        "freeSlideToQuiet": free_slide if args.include_free_slide else None,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "repeatCount": len(repeats)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
