"""从真实壶面直接执行严格全局合同搜索，隔离检查候选顺序与物理耗时。

它跳过正式 ``choose`` 中的快速 draw/MADS 分支，因此不能代表整手对局表现。
用途仅是确认同一状态机合同下，严格全局搜索本身覆盖了哪些候选、能否找到
合同解以及耗时；不修改任何状态机规则。
"""

from __future__ import annotations

import argparse
import json
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
    parser.add_argument("--budget", type=float, default=105.0)
    parser.add_argument("--physics-seeds", type=int, default=3)
    parser.add_argument("--extension", type=Path, help="仅本进程临时加载候选 CP39 扩展，不覆盖运行时文件。")
    parser.add_argument(
        "--use-source-plan",
        action="store_true",
        help="显式复用 trace 中的历史合同，只用于回归候选顺序；不代表当前状态机。",
    )
    parser.add_argument(
        "--override-clear-roll-target", nargs=2, type=float, metavar=("X", "Y"),
        help="仅离线：把当前先手合同改为清指定目标并让出手壶进入该落区；用于审计某个声明状态边的严格覆盖。",
    )
    parser.add_argument(
        "--override-radius", type=float, default=0.10,
        help="--override-clear-roll-target 的落区半径，默认 0.10m。",
    )
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


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
    import planning_proxy.evaluate_vs_teammate_ppo as planner
    from planning_proxy.first_player_strategy import FirstPlayerPlan, plan_first_player_turn
    from planning_proxy.strict_refine import make_position

    source = json.loads(args.source.read_text(encoding="utf-8"))
    game = source.get("game", {})
    trace = game.get("trace", [])
    row = next((item for item in trace if int(item.get("shot", -1)) == args.shot), None)
    if not isinstance(row, dict) or not isinstance(row.get("stateBefore"), list):
        raise SystemExit("目标手缺少可恢复的 stateBefore")
    shot_index = args.shot - 1
    strict_board, proxy_board = planner.canonical_board(row["stateBefore"], 0)
    plan = plan_first_player_turn(proxy_board, shot_index)
    plan_source = "当前状态机"
    if args.use_source_plan:
        detail = row.get("detail")
        historical_plan = detail.get("firstPlayerPlan") if isinstance(detail, dict) else None
        if not isinstance(historical_plan, dict):
            raise SystemExit("目标 trace 没有历史 firstPlayerPlan")
        plan = FirstPlayerPlan(**historical_plan)
        plan_source = "历史 trace 合同（仅回归）"
    if args.override_clear_roll_target is not None:
        if plan.target_opponent_index is None or plan.opponent_action != "physical_clear":
            raise SystemExit("覆盖合同要求当前状态机已声明一个 physical_clear 目标")
        if float(args.override_radius) <= 0.0:
            raise SystemExit("--override-radius 必须为正数")
        # 诊断合同由命令行显式传入；它不会被写回状态机，也不会运行完整 choose
        # 中的快捷分支。保留原目标壶、规则与零自清预算，只替换落区语义。
        plan = replace(
            plan,
            phase="diagnostic_clear_and_roll_region",
            target_points=((float(args.override_clear_roll_target[0]), float(args.override_clear_roll_target[1])),),
            defence_shapes=(),
            landing_region_radius_m=float(args.override_radius),
            max_own_cleared=0,
            rationale="离线严格覆盖探针：清当前状态机目标并进入显式传入的落区。",
        )
        plan_source = "命令行显式离线清壶滚位合同"
    if plan is None:
        raise SystemExit("该手不是先手状态机合同，不能用本工具")
    match_seed = int(game.get("seed", source.get("sourceSeed", 0)))
    seeds = [match_seed + shot_index * 7919 + 104729 * offset for offset in range(args.physics_seeds)]
    deadline_seconds = args.budget - planner.STRICT_EVALUATION_TAIL_RESERVE_SECONDS
    if int(plan.own_throw_number) == 7:
        deadline_seconds = min(deadline_seconds, args.budget - 40.0)
    player = planner.ProxyMatchPlayer(
        physics_seeds=args.physics_seeds,
        parent_regions=3,
        decision_budget_seconds=args.budget,
    )
    started = time.perf_counter()
    found, detail = player._try_strict_global_contract_search(
        strict_board=strict_board,
        position=make_position(strict_board),
        tactical_plan=plan,
        shot_index=shot_index,
        seeds=seeds,
        deadline=started + max(0.0, deadline_seconds),
    )
    elapsed = time.perf_counter() - started
    result: dict[str, Any] = {
        "schema": "strict_global_contract_probe_v1",
        "scope": {
            "source": str(args.source),
            "shot": args.shot,
            "matchSeed": match_seed,
            "physicsSeeds": seeds,
            "budgetSeconds": args.budget,
            "searchDeadlineSeconds": deadline_seconds,
            "planSource": plan_source,
            "extension": str(getattr(pyphysx, "__file__", "")),
            "note": "只测严格全局层，未执行完整 choose 或后续对局。",
        },
        "stateMachinePlan": plan.to_json(),
        "elapsedSeconds": elapsed,
        "strictGlobalSearch": detail,
        "found": found.to_json() if found is not None else None,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "elapsedSeconds": elapsed,
        "found": found is not None,
        "samples": detail["globalStrictSampleCount"],
        "deferred": detail.get("experimentalDeferredCandidateCount", 0),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
