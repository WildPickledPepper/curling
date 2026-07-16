#!/usr/bin/env python3
"""P0 formal check: kernel search versus fixed tactics on fixed late-end boards.

Unlike ``p0_kernel_benchmark.py``, this script never creates a board by a
random prelude.  The JSON fixture is the pre-registered evaluation set.  For
every board it uses root-search rollouts to choose one action, then evaluates
that action and the fixed-tactic action on the same *fresh* friction seeds.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
import math
import multiprocessing
import sys
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.runtime_loader import install_bundled_pyphysx
from local_simulator.examples.train_policy_tree_selfplay import STONE_R, StrictCurlingEnd
from local_simulator.unity_physx import UNITY_RETAINED_PROTOCOL_X, UNITY_RETAINED_PROTOCOL_Y
from training_research.p0_kernel_end_teacher import (
    canonical_state,
    rollout_to_end,
    scripted_continuation_shot,
    search_root,
)


_MASTER = None
_SEARCH = None
_EVALUATION = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scenario-file", type=Path,
        default=ROOT / "training_research" / "fixtures" / "p0_representative_late_end_scenarios_v1.json",
    )
    parser.add_argument("--search-samples", type=int, default=1600)
    parser.add_argument("--target-rollouts", type=int, default=32)
    parser.add_argument("--max-candidates", type=int, default=20)
    parser.add_argument("--evaluation-rollouts", type=int, default=24)
    parser.add_argument("--seed", type=int, default=20260715)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument(
        "--output", type=Path,
        default=ROOT / "training_research" / "benchmarks" / "runs" / "p0_fixed_representative_v1.json",
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
    sd = sample_std(deltas)
    return {
        "scenarioCount": len(rows),
        "meanDeltaSearchMinusFixed": mean(deltas),
        "sampleStdDelta": sd,
        "standardErrorDelta": sd / math.sqrt(len(deltas)) if deltas else 0.0,
        "searchMeanScore": mean([float(row["searchMeanTerminalScoreForSelf"]) for row in rows]),
        "fixedMeanScore": mean([float(row["fixedMeanTerminalScoreForSelf"]) for row in rows]),
        "positiveDeltaCount": sum(delta > 0 for delta in deltas),
        "zeroDeltaCount": sum(delta == 0 for delta in deltas),
        "negativeDeltaCount": sum(delta < 0 for delta in deltas),
    }


def validate_scenarios(document: dict[str, Any]) -> list[dict[str, Any]]:
    if document.get("schema") != "p0_fixed_representative_late_end_scenarios_v1":
        raise ValueError("unexpected fixed-scenario schema")
    scenarios = document.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        raise ValueError("scenario file contains no scenarios")
    seen_ids: set[str] = set()
    minimum_gap = 2.0 * STONE_R - 1e-6
    for scenario in scenarios:
        name = str(scenario.get("id", ""))
        target = scenario.get("targetShot")
        stones = scenario.get("stones")
        if not name or name in seen_ids or target not in (14, 15) or not isinstance(stones, list):
            raise ValueError(f"invalid scenario metadata: {scenario!r}")
        seen_ids.add(name)
        seen_stones: list[tuple[float, float]] = []
        ids: set[int] = set()
        for stone in stones:
            index = int(stone["id"])
            x, y = float(stone["x"]), float(stone["y"])
            if index in ids or not 0 <= index < target:
                raise ValueError(f"{name}: stone id {index} must be unique and lower than targetShot")
            if not (UNITY_RETAINED_PROTOCOL_X[0] < x < UNITY_RETAINED_PROTOCOL_X[1] and UNITY_RETAINED_PROTOCOL_Y[0] < y < UNITY_RETAINED_PROTOCOL_Y[1]):
                raise ValueError(f"{name}: stone {index} is outside retained ice")
            if any(math.hypot(x - px, y - py) < minimum_gap for px, py in seen_stones):
                raise ValueError(f"{name}: overlapping stationary stones")
            ids.add(index)
            seen_stones.append((x, y))
    return scenarios


def _init_worker() -> None:
    global _MASTER, _SEARCH, _EVALUATION
    install_bundled_pyphysx()
    _MASTER = StrictCurlingEnd(seed=0, training_fast=True)
    _SEARCH = StrictCurlingEnd(seed=1, training_fast=True)
    _EVALUATION = StrictCurlingEnd(seed=2, training_fast=True)


def states_from_scenario(worker: StrictCurlingEnd, scenario: dict[str, Any], seed: int) -> list[dict[str, Any]]:
    positions = [0.0] * 32
    yaws: dict[int, float] = {}
    for stone in scenario["stones"]:
        index = int(stone["id"])
        positions[index * 2] = float(stone["x"])
        positions[index * 2 + 1] = float(stone["y"])
        yaws[index] = float(stone.get("yaw", 0.0))
    worker.scene.reset_positions(positions, yaw_overrides=yaws)
    worker.shot_number = int(scenario["targetShot"])
    worker.seed = int(seed)
    return worker.states()


def _benchmark_one(task: tuple[int, dict[str, Any], dict[str, Any]]) -> dict[str, Any]:
    global _MASTER, _SEARCH, _EVALUATION
    if _MASTER is None or _SEARCH is None or _EVALUATION is None:
        _init_worker()
    scenario_index, scenario, config = task
    target = int(scenario["targetShot"])
    team = target % 2
    scenario_seed = int(config["seed"]) + scenario_index * 500_009 + target * 31
    states = states_from_scenario(_MASTER, scenario, scenario_seed)
    search = search_root(
        states=states, shot_number=target, seed=scenario_seed + 91,
        sample_budget=int(config["searchSamples"]), confidence_z=1.0, exploration=0.75,
        expand_every=3, initial_samples_per_template=2,
        target_rollouts=int(config["targetRollouts"]), max_candidates=int(config["maxCandidates"]), worker=_SEARCH,
    )
    search_action = tuple(float(value) for value in search["search"]["selected"]["action"])
    fixed_action = scripted_continuation_shot(states, target)
    paired: list[dict[str, int]] = []
    for repeat in range(int(config["evaluationRollouts"])):
        episode_seed = scenario_seed + 200_003 + repeat * 11_003
        searched, _ = rollout_to_end(_EVALUATION, states, target, team, search_action, episode_seed)
        fixed, _ = rollout_to_end(_EVALUATION, states, target, team, fixed_action, episode_seed)
        paired.append({"episodeSeed": episode_seed, "searchTerminalScoreForSelf": searched, "fixedTerminalScoreForSelf": fixed, "deltaSearchMinusFixed": searched - fixed})
    search_scores = [row["searchTerminalScoreForSelf"] for row in paired]
    fixed_scores = [row["fixedTerminalScoreForSelf"] for row in paired]
    return {
        "scenario": str(scenario["id"]), "category": str(scenario["category"]), "scenarioSeed": scenario_seed,
        "targetShot": target, "currentShooter": "first" if team == 0 else "second", "isHammerSide": bool(team == 1),
        "fixedBoard": scenario, "searchAction": list(search_action), "searchTactic": search["search"]["selected"]["tactic"],
        "fixedAction": list(fixed_action), "fixedPolicy": "scripted_continuation_v1",
        "searchMeanTerminalScoreForSelf": mean(search_scores), "fixedMeanTerminalScoreForSelf": mean(fixed_scores),
        "meanDeltaSearchMinusFixed": mean([row["deltaSearchMinusFixed"] for row in paired]),
        "pairedEvaluation": paired, "state": canonical_state(states, target, team),
        "searchSummary": {"selected": search["search"]["selected"], "sampleBudget": int(config["searchSamples"]), "targetRollouts": int(config["targetRollouts"])},
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    if args.search_samples < 10 or args.target_rollouts < 1 or args.evaluation_rollouts < 1 or args.workers < 1:
        raise ValueError("search samples must be >=10; rollout and worker counts must be positive")
    document = json.loads(args.scenario_file.read_text(encoding="utf-8"))
    scenarios = validate_scenarios(document)
    config = {"seed": int(args.seed), "searchSamples": int(args.search_samples), "targetRollouts": int(args.target_rollouts), "maxCandidates": int(args.max_candidates), "evaluationRollouts": int(args.evaluation_rollouts)}
    tasks = [(index, scenario, config) for index, scenario in enumerate(scenarios)]
    rows: list[dict[str, Any]] = []
    if args.workers == 1:
        _init_worker()
        for task in tasks:
            rows.append(_benchmark_one(task))
    else:
        context = multiprocessing.get_context("spawn")
        with ProcessPoolExecutor(max_workers=args.workers, mp_context=context, initializer=_init_worker) as executor:
            for future in as_completed([executor.submit(_benchmark_one, task) for task in tasks]):
                rows.append(future.result())
    rows.sort(key=lambda row: (int(row["targetShot"]), str(row["scenario"])))
    for row in rows:
        print(f"P0 固定局面 {row['scenario']} | {'先手' if row['currentShooter'] == 'first' else '后手'} | 搜索-固定 {row['meanDeltaSearchMinusFixed']:+.3f}", flush=True)
    first = [row for row in rows if row["currentShooter"] == "first"]
    second = [row for row in rows if row["currentShooter"] == "second"]
    by_category = {category: summarize([row for row in rows if row["category"] == category]) for category in sorted({str(row["category"]) for row in rows})}
    report = {
        "schema": "p0_fixed_representative_paired_benchmark_v1", "scope": "non-sweeping; strict local PhysX; fixed fixture boards; fresh paired paths excluded from root search",
        "scenarioFixture": str(args.scenario_file), "configuration": {**config, "workers": args.workers, "fixedPolicy": "scripted_continuation_v1"},
        "summary": {"all": summarize(rows), "first": summarize(first), "second": summarize(second), "byCategory": by_category}, "scenarios": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> int:
    report = run(parse_args())
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
