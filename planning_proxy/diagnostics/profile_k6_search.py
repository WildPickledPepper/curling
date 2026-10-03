#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""对一条已记录的 K6 决策做分段计时，不改变状态机或搜索结果。

输入是 ``evaluate_k6_outdraw_full_continuations.py`` 生成的完整回放报告。
脚本从指定投壶前的真实壶面恢复 ``ProxyMatchPlayer.choose``，统计粗代理、
严格候选和严格物理内部三段的累计时间与调用次数。它只用于找速度瓶颈。
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="含 game.trace 的 K6 续局回放 JSON")
    parser.add_argument("--shot", type=int, default=11, help="从 trace 中读取的投壶编号（默认 K6 的第 11 手）")
    parser.add_argument("--budget", type=float, default=105.0, help="复现的单手总预算（秒）")
    parser.add_argument("--physics-seeds", type=int, default=3)
    parser.add_argument(
        "--strict-tail-reserve",
        type=float,
        help=(
            "仅本次诊断覆盖的严格 PhysX 单候选尾部预留秒数。"
            "默认沿用正式常量；该参数不修改生产代码或运行时文件。"
        ),
    )
    parser.add_argument("--summary", action="store_true", help="只输出动作、模式与分段计时，便于批量对照。")
    parser.add_argument(
        "--output",
        type=Path,
        help="可选：把结构化计时报告写入该 JSON 文件；标准输出只保留一行摘要。",
    )
    parser.add_argument("--extension", type=Path, help="可选：仅本进程临时加载指定 CP39 原生扩展，不覆盖运行时文件。")
    return parser.parse_args()


def _wrap(totals: dict[str, float], counts: dict[str, int], name: str, fn: Callable[..., Any]) -> Callable[..., Any]:
    def timed(*args: Any, **kwargs: Any) -> Any:
        started = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            totals[name] += time.perf_counter() - started
            counts[name] += 1
    return timed


def main() -> None:
    args = parse_args()
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
    import planning_proxy.evaluate_vs_teammate_ppo as planner

    if args.strict_tail_reserve is not None:
        if args.strict_tail_reserve < 0.0 or args.strict_tail_reserve >= args.budget:
            raise SystemExit("--strict-tail-reserve 必须满足 0 <= 值 < --budget")
        planner.STRICT_EVALUATION_TAIL_RESERVE_SECONDS = float(args.strict_tail_reserve)

    source = json.loads(args.source.read_text(encoding="utf-8"))
    trace = source.get("game", {}).get("trace", [])
    row = next((item for item in trace if int(item.get("shot", -1)) == int(args.shot)), None)
    if row is None:
        raise SystemExit(f"报告中没有第 {args.shot} 手的 trace")
    states = row.get("stateBefore")
    if not isinstance(states, list):
        raise SystemExit("目标 trace 缺少 stateBefore")

    totals: dict[str, float] = defaultdict(float)
    counts: dict[str, int] = defaultdict(int)
    strict_candidates_by_contract: dict[str, set[tuple[float, float, float]]] = defaultdict(set)
    strict_evaluation_samples: list[dict[str, Any]] = []
    coarse_batch_samples: list[dict[str, Any]] = []
    adaptive_target_hit_calls: list[dict[str, Any]] = []
    original_evaluate = planner.evaluate_one
    original_batch = planner.simulate_batch
    original_refine = planner.refine_candidates
    def timed_evaluate(*call_args: Any, **call_kwargs: Any) -> Any:
        candidate = call_args[1]
        plan = call_kwargs.get("tactical_plan")
        if plan is None and len(call_args) >= 8:
            plan = call_args[7]
        if plan is None:
            contract = "无战术合同"
        else:
            targets = tuple(
                (round(float(point[0]), 3), round(float(point[1]), 3))
                for point in getattr(plan, "target_points", ())
            )
            contract = f"{getattr(plan, 'phase', '')}|{getattr(plan, 'opponent_action', '')}|{targets}"
        values = tuple(round(float(value), 6) for value in (candidate.v0, candidate.h0, candidate.w0))
        strict_candidates_by_contract[contract].add(values)
        # evaluate_one(environment, candidate, board, position, physics_seeds, shot_index, ...)
        seeds = call_args[4] if len(call_args) >= 5 else call_kwargs.get("physics_seeds", ())
        normalized_seeds = (int(seeds),) if isinstance(seeds, int) else tuple(int(seed) for seed in seeds)
        started = time.perf_counter()
        outcome = None
        try:
            outcome = original_evaluate(*call_args, **call_kwargs)
            return outcome
        finally:
            seconds = time.perf_counter() - started
            totals["严格候选总计"] += seconds
            counts["严格候选总计"] += 1
            sample = {
                "seconds": seconds,
                "bestshot": list(values),
                "physicsSeeds": list(normalized_seeds),
                "contract": contract,
            }
            # 仅记录严格终局的判定摘要，供区分“合同过严”与“候选未覆盖”；
            # 不记录整块 final_boards，避免把 profile 报告膨胀成逐壶回放包。
            if outcome is not None:
                sample["outcome"] = {
                    "scores": [float(value) for value in outcome.scores],
                    "enemyCleared": [int(value) for value in outcome.enemy_cleared],
                    "ownCleared": [int(value) for value in outcome.own_cleared],
                    "totalSelfCleared": [int(value) for value in outcome.total_self_cleared],
                    "ownInHouse": [int(value) for value in outcome.own_in_house],
                    "ruleLegal": bool(outcome.rule_legal),
                    "tacticalScores": [float(value) for value in outcome.tactical_scores],
                    "tacticalGoalMet": [bool(value) for value in outcome.tactical_goal_met],
                    "activeFinalPositions": [
                        list(point) if point is not None else None for point in outcome.active_final_positions
                    ],
                }
            strict_evaluation_samples.append(sample)

    planner.evaluate_one = timed_evaluate
    def timed_batch(*call_args: Any, **call_kwargs: Any) -> Any:
        shots = call_args[0]
        stones = call_args[1]
        started = time.perf_counter()
        try:
            result = original_batch(*call_args, **call_kwargs)
            coarse_batch_samples.append({
                "seconds": time.perf_counter() - started,
                "candidateCount": int(len(shots)),
                "stoneCount": int(len(stones)),
                "dt": float(call_kwargs.get("dt", 0.05)),
                "firstHitCount": int((result.first_hit_index >= 0).sum()),
            })
            return result
        finally:
            seconds = time.perf_counter() - started
            totals["粗代理批量模拟"] += seconds
            counts["粗代理批量模拟"] += 1

    planner.simulate_batch = timed_batch
    planner.refine_candidates = _wrap(totals, counts, "粗代理局部细分", original_refine)
    try:
        player = planner.ProxyMatchPlayer(
            physics_seeds=args.physics_seeds,
            parent_regions=3,
            decision_budget_seconds=args.budget,
        )
        original_adaptive_target_hit = player._adaptive_target_hit_candidates

        def recorded_adaptive_target_hit(*call_args: Any, **call_kwargs: Any) -> tuple[tuple[float, float, float], ...]:
            result = original_adaptive_target_hit(*call_args, **call_kwargs)
            target_index = call_kwargs.get("target_index")
            if target_index is None and len(call_args) >= 2:
                target_index = call_args[1]
            adaptive_target_hit_calls.append({
                "targetIndex": int(target_index) if target_index is not None else None,
                "requestedLimit": int(call_kwargs.get("limit", 3)),
                "returnedCount": len(result),
                "candidates": [[float(value) for value in candidate] for candidate in result],
            })
            return result

        # 仅记录此临时 player 的调用，不改变候选、顺序或严格执行。
        player._adaptive_target_hit_candidates = recorded_adaptive_target_hit
        # ``evaluate_one`` 内部严格物理三段；这里仅包计时，不改变参数或顺序。
        player.environment.scene.reset_positions = _wrap(
            totals, counts, "严格物理：重置壶面", player.environment.scene.reset_positions
        )
        player.environment.scene.run_bestshot_to_first_contact_training = _wrap(
            totals, counts, "严格物理：滑行至首次碰撞", player.environment.scene.run_bestshot_to_first_contact_training
        )
        player.environment._settle = _wrap(
            totals, counts, "严格物理：碰撞后静止", player.environment._settle
        )
        started = time.perf_counter()
        action, detail = player.choose(
            states,
            proxy_team=0,
            shot_index=int(args.shot) - 1,
            match_seed=int(source.get("game", {}).get("seed", source.get("sourceSeed", 0))),
        )
        elapsed = time.perf_counter() - started
    finally:
        planner.evaluate_one = original_evaluate
        planner.simulate_batch = original_batch
        planner.refine_candidates = original_refine

    result = {
        "source": str(args.source), "shot": int(args.shot), "elapsedSeconds": elapsed,
        "extension": str(getattr(pyphysx, "__file__", "")),
        "action": [float(value) for value in action],
        "mode": detail.get("mode"), "phase": detail.get("phase"),
        "strictPhysicsCache": detail.get("strictPhysicsCache"),
        "adaptiveTargetHitCalls": adaptive_target_hit_calls,
        "timing": {
            name: {"seconds": seconds, "calls": counts[name], "share": seconds / elapsed if elapsed else 0.0}
            for name, seconds in sorted(totals.items(), key=lambda item: item[1], reverse=True)
        },
        "strictUniqueCandidatesByContract": {
            contract: len(candidates)
            for contract, candidates in sorted(strict_candidates_by_contract.items())
        },
        "slowestStrictEvaluations": sorted(
            strict_evaluation_samples,
            key=lambda item: float(item["seconds"]),
            reverse=True,
        )[:10],
        "strictEvaluationSummary": strict_evaluation_samples,
        "coarseBatches": coarse_batch_samples,
    }
    contracts = list(strict_candidates_by_contract)
    result["strictCandidateOverlap"] = [
        {
            "left": left, "right": right,
            "shared": len(strict_candidates_by_contract[left] & strict_candidates_by_contract[right]),
        }
        for index, left in enumerate(contracts)
        for right in contracts[index + 1:]
        if strict_candidates_by_contract[left] & strict_candidates_by_contract[right]
    ]
    if not args.summary:
        result["plannerDetail"] = detail
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(
            json.dumps(
                {
                    "output": str(args.output),
                    "elapsedSeconds": elapsed,
                    "mode": result["mode"],
                    "phase": result["phase"],
                },
                ensure_ascii=False,
            )
        )
    else:
        print(rendered)


if __name__ == "__main__":
    main()
