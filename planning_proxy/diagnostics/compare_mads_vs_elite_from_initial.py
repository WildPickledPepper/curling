#!/usr/bin/env python3
"""在相同严格 PhysX、合同、初值下比较 MADS 与随机精英搜索。

这是离线诊断：不改状态机、不改生产选择器。输入审计报告中的一条
``rawBestshot``，从同一真实 ``stateBefore`` 恢复壶面；两种搜索都只调用
主项目当前冻结的严格求解器。随机精英一侧复现队友 ``InverseSolver`` 的
高斯采样、历史精英均值和方差收缩机制，但使用与 MADS 完全相同的严格合同
评分，避免把“评分不同”误判为“搜索法不同”。
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
import time
from pathlib import Path
from typing import Any, Sequence

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", type=Path, required=True, help="含 rawBestshot、合同和 sourceReport 的 K8 审计 JSON")
    parser.add_argument("--rank", type=int, required=True, help="primaryRows 中的初值序号，从 1 开始")
    parser.add_argument("--elite-budget", type=int, default=49, help="随机精英阶段的单种子严格评估上限")
    parser.add_argument("--random-seed", type=int, default=20260725)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def resolve_report(path: Path, *, base: Path) -> Path:
    if path.is_absolute():
        return path
    candidate = (base / path).resolve()
    if candidate.is_file():
        return candidate
    candidate = (PROJECT_ROOT / path).resolve()
    if candidate.is_file():
        return candidate
    raise FileNotFoundError(path)


def main() -> None:
    args = parse_args()
    if args.rank < 1 or args.elite_budget < 1:
        raise SystemExit("--rank 与 --elite-budget 必须为正数")

    from local_simulator.runtime_loader import install_bundled_pyphysx

    install_bundled_pyphysx()
    from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd
    from planning_proxy.evaluate_vs_teammate_ppo import canonical_board
    from planning_proxy.strict_refine import Candidate, evaluate_one, make_position

    audit_path = args.audit.resolve()
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    rows = list(audit.get("primaryRows", ()))
    if args.rank > len(rows):
        raise SystemExit(f"--rank 超出 primaryRows 范围（共 {len(rows)} 条）")
    row = rows[args.rank - 1]
    source_path = resolve_report(Path(str(audit["sourceReport"])), base=audit_path.parent)
    source = json.loads(source_path.read_text(encoding="utf-8"))
    shot = int(audit["shot"])
    trace = source.get("game", {}).get("trace", ())
    trace_row = next((item for item in trace if int(item.get("shot", -1)) == shot), None)
    if trace_row is None or not isinstance(trace_row.get("stateBefore"), list):
        raise SystemExit(f"来源报告缺少第 {shot} 手的 stateBefore")

    strict_board, _proxy_board = canonical_board(trace_row["stateBefore"], proxy_team=0)
    position = make_position(strict_board)
    active_index = shot - 1
    physics_seeds = [int(value) for value in audit["physicsSeeds"]]
    plan = dict(audit["plan"])
    target_index = int(plan["target_opponent_index"])
    targets = tuple((float(x), float(y)) for x, y in plan["target_points"])
    radius = float(plan["landing_region_radius_m"])
    start = np.asarray(row["rawBestshot"], dtype=np.float64)
    environment = StrictCurlingEnd(seed=physics_seeds[0], training_fast=True)

    def clamp(values: Sequence[float]) -> np.ndarray:
        return np.asarray((
            np.clip(float(values[0]), 1.0, 6.0),
            np.clip(float(values[1]), -2.23, 2.23),
            np.clip(float(values[2]), -15.7, 15.7),
        ), dtype=np.float64)

    def evaluate(values: Sequence[float], seeds: Sequence[int]) -> tuple[float, Any, bool, list[float]]:
        candidate = clamp(values)
        item = evaluate_one(
            environment,
            Candidate(float(candidate[0]), float(candidate[1]), float(candidate[2]), parent_rank=int(args.rank)),
            strict_board,
            position,
            seeds,
            active_index,
            active_index=active_index,
            tactical_plan=None,
        )
        errors: list[float] = []
        success_rows: list[bool] = []
        score = 0.0
        for index, final_position in enumerate(item.active_final_positions):
            error = (
                min(math.hypot(float(final_position[0]) - x, float(final_position[1]) - y) for x, y in targets)
                if final_position is not None else 99.0
            )
            target_cleared = int(target_index) in item.enemy_cleared_indices[index]
            own_loss = int(item.total_self_cleared[index])
            passed = bool(item.rule_legal) and target_cleared and own_loss == 0 and error <= radius
            errors.append(float(error))
            success_rows.append(passed)
            score += float(error)
            score += 100.0 if not target_cleared else 0.0
            score += 100.0 if not item.rule_legal else 0.0
            score += 40.0 * own_loss
            score += 100.0 if not passed else 0.0
        return float(score), item, bool(all(success_rows)), errors

    def directions(iteration: int) -> list[np.ndarray]:
        phase = (iteration + 1) * 2.399963229728653
        diagonal = np.asarray((
            math.cos(phase), math.sin(phase), math.cos(phase * 0.6180339887498948),
        ), dtype=np.float64)
        diagonal /= max(float(np.linalg.norm(diagonal)), 1.0e-12)
        result = [diagonal, -diagonal]
        for axis in range(3):
            unit = np.zeros(3, dtype=np.float64)
            unit[axis] = 1.0
            result.extend((unit, -unit))
        return result

    def run_mads() -> dict[str, Any]:
        current = clamp(start)
        score, _item, success, _errors = evaluate(current, [physics_seeds[0]])
        calls = 1
        mesh = 1.0
        history: list[dict[str, Any]] = []
        started = time.perf_counter()
        for iteration in range(6):
            history.append({"iteration": iteration, "centre": current.tolist(), "score": score, "success": success})
            if success:
                break
            best_score, best_values, best_success = score, current, success
            for direction in directions(iteration):
                trial = clamp(current + mesh * np.asarray((0.12, 0.12, 1.60)) * direction)
                trial_score, _trial_item, trial_success, _trial_errors = evaluate(trial, [physics_seeds[0]])
                calls += 1
                if trial_score < best_score:
                    best_score, best_values, best_success = trial_score, trial, trial_success
            if best_score < score:
                current, score, success = best_values, best_score, best_success
                mesh = min(1.0, mesh * 1.5)
            else:
                mesh *= 0.5
                if mesh < 1.0 / 16.0:
                    break
        final_score, _final_item, final_success, final_errors = evaluate(current, physics_seeds)
        return {
            "shot": current.tolist(),
            "optimizationSingleSeedCalls": calls,
            "finalVerificationPhysicalCalls": len(physics_seeds),
            "totalPhysicalCalls": calls + len(physics_seeds),
            "singleSeedScore": score,
            "multiSeedScore": final_score,
            "singleSeedSuccess": success,
            "multiSeedSuccess": final_success,
            "multiSeedErrorsM": final_errors,
            "history": history,
            "seconds": time.perf_counter() - started,
        }

    def run_elite() -> dict[str, Any]:
        rng = random.Random(int(args.random_seed))
        mean = clamp(start)
        standard_deviation = np.asarray((0.30, 0.08, 1.00), dtype=np.float64)
        history: list[tuple[float, np.ndarray, bool]] = []
        started = time.perf_counter()
        score, _item, success, _errors = evaluate(mean, [physics_seeds[0]])
        history.append((score, mean.copy(), success))
        calls = 1
        while calls < int(args.elite_budget):
            for _ in range(min(6, int(args.elite_budget) - calls)):
                proposal = clamp([rng.gauss(float(mean[index]), float(standard_deviation[index])) for index in range(3)])
                proposal_score, _proposal_item, proposal_success, _proposal_errors = evaluate(proposal, [physics_seeds[0]])
                history.append((proposal_score, proposal, proposal_success))
                calls += 1
            elite = sorted(history, key=lambda item: item[0])[: min(3, len(history))]
            mean = np.mean([item[1] for item in elite], axis=0)
            standard_deviation = np.maximum(
                np.asarray((0.02, 0.005, 0.05), dtype=np.float64),
                np.std([item[1] for item in elite], axis=0),
            )
        best_score, best_values, best_success = min(history, key=lambda item: item[0])
        final_score, _final_item, final_success, final_errors = evaluate(best_values, physics_seeds)
        return {
            "shot": best_values.tolist(),
            "optimizationSingleSeedCalls": calls,
            "finalVerificationPhysicalCalls": len(physics_seeds),
            "totalPhysicalCalls": calls + len(physics_seeds),
            "singleSeedScore": best_score,
            "multiSeedScore": final_score,
            "singleSeedSuccess": best_success,
            "multiSeedSuccess": final_success,
            "singleSeedSuccessCount": sum(int(item[2]) for item in history),
            "finalEliteCentre": mean.tolist(),
            "finalEliteStd": standard_deviation.tolist(),
            "multiSeedErrorsM": final_errors,
            "seconds": time.perf_counter() - started,
        }

    result = {
        "schema": "mads_vs_elite_same_initial_v1",
        "scope": "offline only; same frozen main strict PhysX and same explicit K8 contract; no production change",
        "fixture": {
            "audit": str(audit_path), "sourceReport": str(source_path), "shot": shot,
            "rank": int(args.rank), "initial": start.tolist(), "physicsSeeds": physics_seeds,
            "contract": {"clearTargetIndex": target_index, "targetPoints": [list(point) for point in targets], "radiusM": radius, "maxOldOwnCleared": 0},
        },
        "mads": run_mads(),
        "eliteRandom": run_elite(),
        "comparisonRule": "MADS 找到单种子严格解即停止；随机精英按明确的单种子调用上限运行。两者随后都用同一三种子集合复核最终最佳球。",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "mads": result["mads"], "eliteRandom": result["eliteRandom"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
