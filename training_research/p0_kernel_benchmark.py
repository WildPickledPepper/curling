#!/usr/bin/env python3
"""Paired P0.1 benchmark: fixed tactic versus late-end kernel search.

For each deterministic prelude seed, both methods receive exactly the same
settled board.  Their actions are evaluated using fresh, paired friction paths
which were not used by the search.  Results are split by current shooter, so a
single pooled score cannot hide a first/second-player failure.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
import math
import multiprocessing
import random
import sys
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.runtime_loader import install_bundled_pyphysx
from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd
from training_research.p0_kernel_end_teacher import (
    STONE_COUNT,
    prelude_to_search,
    rollout_to_end,
    scripted_continuation_shot,
    search_root,
)


_BENCH_MASTER = None
_BENCH_SEARCH = None
_BENCH_EVALUATION = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenarios", type=int, default=4, help="fixed seeded boards to compare")
    parser.add_argument(
        "--target-shots",
        type=str,
        default="14,15",
        help="comma-separated zero-based shots; default tests 15th (first) and 16th/hammer (second)",
    )
    parser.add_argument("--search-samples", type=int, default=16)
    parser.add_argument("--target-rollouts", type=int, default=4)
    parser.add_argument("--max-candidates", type=int, default=20)
    parser.add_argument("--evaluation-rollouts", type=int, default=12, help="fresh paired paths per board")
    parser.add_argument("--seed", type=int, default=20260715)
    parser.add_argument("--workers", type=int, default=4, help="independent persistent PhysX benchmark processes")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "training_research" / "benchmarks" / "p0_kernel_vs_fixed.json",
    )
    return parser.parse_args()


def mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def sample_std(values: Sequence[float]) -> float:
    if len(values) < 2:
        return 0.0
    average = mean(values)
    return math.sqrt(sum((value - average) ** 2 for value in values) / (len(values) - 1))


def summarize(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    deltas = [float(row["meanDeltaSearchMinusFixed"]) for row in rows]
    standard_deviation = sample_std(deltas)
    return {
        "scenarioCount": len(rows),
        "meanDeltaSearchMinusFixed": mean(deltas),
        "sampleStdDelta": standard_deviation,
        "standardErrorDelta": standard_deviation / math.sqrt(len(deltas)) if deltas else 0.0,
        "searchMeanScore": mean([float(row["searchMeanTerminalScoreForSelf"]) for row in rows]),
        "fixedMeanScore": mean([float(row["fixedMeanTerminalScoreForSelf"]) for row in rows]),
    }


def _init_benchmark_worker() -> None:
    global _BENCH_MASTER, _BENCH_SEARCH, _BENCH_EVALUATION
    install_bundled_pyphysx()
    _BENCH_MASTER = StrictCurlingEnd(seed=0, training_fast=True)
    _BENCH_SEARCH = StrictCurlingEnd(seed=1, training_fast=True)
    _BENCH_EVALUATION = StrictCurlingEnd(seed=2, training_fast=True)


def _benchmark_one(task: tuple[int, int, dict[str, Any]]) -> dict[str, Any]:
    """Evaluate one fixed board in one persistent native-PhysX worker."""

    global _BENCH_MASTER, _BENCH_SEARCH, _BENCH_EVALUATION
    if _BENCH_MASTER is None or _BENCH_SEARCH is None or _BENCH_EVALUATION is None:
        _init_benchmark_worker()
    scenario_index, target_shot, config = task
    scenario_seed = int(config["seed"]) + scenario_index * 500_009
    _BENCH_MASTER.seed = scenario_seed + target_shot * 31
    states = prelude_to_search(
        _BENCH_MASTER,
        target_shot,
        random.Random(scenario_seed + target_shot * 31),
    )
    team = target_shot % 2
    search = search_root(
        states=states,
        shot_number=target_shot,
        seed=scenario_seed + target_shot * 20_011 + 91,
        sample_budget=int(config["searchSamples"]),
        confidence_z=1.0,
        exploration=0.75,
        expand_every=3,
        initial_samples_per_template=2,
        target_rollouts=int(config["targetRollouts"]),
        max_candidates=int(config["maxCandidates"]),
        worker=_BENCH_SEARCH,
    )
    search_action = tuple(float(value) for value in search["search"]["selected"]["action"])
    fixed_action = scripted_continuation_shot(states, target_shot)
    paired: list[dict[str, int]] = []
    for repeat in range(int(config["evaluationRollouts"])):
        evaluation_seed = scenario_seed + target_shot * 20_011 + 200_003 + repeat * 11_003
        search_score, _ = rollout_to_end(
            _BENCH_EVALUATION, states, target_shot, team, search_action, evaluation_seed
        )
        fixed_score, _ = rollout_to_end(
            _BENCH_EVALUATION, states, target_shot, team, fixed_action, evaluation_seed
        )
        paired.append(
            {
                "episodeSeed": evaluation_seed,
                "searchTerminalScoreForSelf": search_score,
                "fixedTerminalScoreForSelf": fixed_score,
                "deltaSearchMinusFixed": search_score - fixed_score,
            }
        )
    search_scores = [row["searchTerminalScoreForSelf"] for row in paired]
    fixed_scores = [row["fixedTerminalScoreForSelf"] for row in paired]
    return {
        "scenario": scenario_index + 1,
        "scenarioSeed": scenario_seed,
        "targetShot": target_shot,
        "currentShooter": "first" if team == 0 else "second",
        "isHammerSide": bool(team == 1),
        "searchAction": list(search_action),
        "searchTactic": search["search"]["selected"]["tactic"],
        "fixedAction": list(fixed_action),
        "fixedPolicy": "scripted_continuation_v1",
        "searchMeanTerminalScoreForSelf": mean(search_scores),
        "fixedMeanTerminalScoreForSelf": mean(fixed_scores),
        "meanDeltaSearchMinusFixed": mean([row["deltaSearchMinusFixed"] for row in paired]),
        "pairedEvaluation": paired,
        "state": search["state"],
        "searchSummary": {
            "selected": search["search"]["selected"],
            "sampleBudget": int(config["searchSamples"]),
            "targetRollouts": int(config["targetRollouts"]),
        },
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    if args.scenarios < 1 or args.evaluation_rollouts < 1 or args.target_rollouts < 1 or args.workers < 1:
        raise ValueError("scenario and rollout counts must be positive")
    try:
        target_shots = tuple(sorted({int(value.strip()) for value in args.target_shots.split(",") if value.strip()}))
    except ValueError as exc:
        raise ValueError("--target-shots must be comma-separated integers") from exc
    if not target_shots or any(shot not in (14, 15) for shot in target_shots):
        raise ValueError("P0.1 benchmark intentionally supports only shots 15 or 16 (zero-based 14 or 15)")
    if args.search_samples < 10:
        raise ValueError("--search-samples must be at least 10 for two direct samples of five templates")

    config = {
        "seed": int(args.seed),
        "searchSamples": int(args.search_samples),
        "targetRollouts": int(args.target_rollouts),
        "maxCandidates": int(args.max_candidates),
        "evaluationRollouts": int(args.evaluation_rollouts),
    }
    tasks = [(scenario_index, target_shot, config) for scenario_index in range(args.scenarios) for target_shot in target_shots]
    scenario_rows: list[dict[str, Any]] = []
    if args.workers == 1:
        _init_benchmark_worker()
        for task in tasks:
            scenario_rows.append(_benchmark_one(task))
    else:
        context = multiprocessing.get_context("spawn")
        with ProcessPoolExecutor(max_workers=args.workers, mp_context=context, initializer=_init_benchmark_worker) as executor:
            for future in as_completed([executor.submit(_benchmark_one, task) for task in tasks]):
                scenario_rows.append(future.result())
    scenario_rows.sort(key=lambda row: (int(row["scenario"]), int(row["targetShot"])))
    for row in scenario_rows:
        print(
            f"P0 基准 场景 {row['scenario']}/{args.scenarios} 第 {int(row['targetShot']) + 1} 手 | "
            f"{'先手' if row['currentShooter'] == 'first' else '后手'} | 搜索-固定 {row['meanDeltaSearchMinusFixed']:+.3f}",
            flush=True,
        )

    first_rows = [row for row in scenario_rows if row["currentShooter"] == "first"]
    second_rows = [row for row in scenario_rows if row["currentShooter"] == "second"]
    report = {
        "schema": "p0_kernel_vs_fixed_paired_benchmark_v1",
        "scope": "non-sweeping; strict local PhysX; fresh paired evaluation paths excluded from root search",
        "configuration": {
            "targetShots": list(target_shots),
            "searchSamples": args.search_samples,
            "targetRollouts": args.target_rollouts,
            "maxCandidates": args.max_candidates,
            "evaluationRollouts": args.evaluation_rollouts,
            "workers": args.workers,
            "fixedPolicy": "scripted_continuation_v1",
        },
        "summary": {
            "all": summarize(scenario_rows),
            "first": summarize(first_rows),
            "second": summarize(second_rows),
        },
        "scenarios": scenario_rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> int:
    args = parse_args()
    report = run(args)
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    print(f"P0 paired benchmark written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
