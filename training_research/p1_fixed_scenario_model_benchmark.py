#!/usr/bin/env python3
"""Strict-PhysX P1 check: direct distilled-model action versus fixed script.

This is deliberately an *action-only* model check.  It does not add a root
search after the model prediction, so any score belongs to the trained model
rather than to its search teacher.  For each pre-registered stationary late-end
board, model and fixed script are completed with the same fresh friction seeds.

The report separates first/non-hammer and second/hammer results.  It is still
limited to one non-sweeping end and ``scripted_continuation_v1`` after the
tested action; it says nothing about full-match win rate or opponent-pool play.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
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
from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd
from training_research.p0_fixed_scenario_benchmark import states_from_scenario, validate_scenarios
from training_research.p0_kernel_end_teacher import canonical_state, rollout_to_end, scripted_continuation_shot
from training_research.p1_policy_value_distill import ACTION_SCALE, TACTICS, build_model, encode_state


_MODEL = None
_EVALUATION = None
_CHECKPOINT_SHA256 = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--checkpoint", type=Path,
        default=ROOT / "training_research" / "runs" / "p1_distill_500x5_v1" / "policy_value.pt",
    )
    parser.add_argument(
        "--scenario-file", type=Path,
        default=ROOT / "training_research" / "fixtures" / "p0_representative_late_end_scenarios_v1.json",
    )
    parser.add_argument("--evaluation-rollouts", type=int, default=24)
    parser.add_argument("--seed", type=int, default=20260715)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument(
        "--output", type=Path,
        default=ROOT / "training_research" / "runs" / "p1_distill_500x5_v1" / "fixed_physics_benchmark_24.json",
    )
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def sample_std(values: Sequence[float]) -> float:
    if len(values) < 2:
        return 0.0
    average = mean(values)
    return math.sqrt(sum((value - average) ** 2 for value in values) / (len(values) - 1))


def summarize(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    deltas = [float(row["meanDeltaModelMinusFixed"]) for row in rows]
    std = sample_std(deltas)
    return {
        "scenarioCount": len(rows),
        "meanDeltaModelMinusFixed": mean(deltas),
        "sampleStdDelta": std,
        "standardErrorDelta": std / math.sqrt(len(deltas)) if deltas else 0.0,
        "modelMeanTerminalScore": mean([float(row["modelMeanTerminalScoreForSelf"]) for row in rows]),
        "fixedMeanTerminalScore": mean([float(row["fixedMeanTerminalScoreForSelf"]) for row in rows]),
        "positiveDeltaCount": sum(delta > 0.0 for delta in deltas),
        "zeroDeltaCount": sum(delta == 0.0 for delta in deltas),
        "negativeDeltaCount": sum(delta < 0.0 for delta in deltas),
    }


def _init_worker(checkpoint_path: str) -> None:
    global _MODEL, _EVALUATION, _CHECKPOINT_SHA256
    install_bundled_pyphysx()
    import torch

    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    if checkpoint.get("schema") != "strict_p1_policy_value_checkpoint_v1":
        raise ValueError("unexpected P1 checkpoint schema")
    if tuple(checkpoint.get("tactics", ())) != TACTICS:
        raise ValueError("checkpoint tactic vocabulary does not match evaluator")
    _MODEL = build_model(torch, int(checkpoint["hiddenSize"]))
    _MODEL.load_state_dict(checkpoint["stateDict"])
    _MODEL.eval()
    _EVALUATION = StrictCurlingEnd(seed=0, training_fast=True)
    _CHECKPOINT_SHA256 = sha256_file(Path(checkpoint_path))


def model_action(states: list[dict[str, Any]], target_shot: int) -> tuple[list[float], str]:
    if _MODEL is None:
        raise RuntimeError("worker model is not initialized")
    import torch

    team = target_shot % 2
    state = canonical_state(states, target_shot, team)
    features = torch.tensor([encode_state(state)], dtype=torch.float32)
    hammer = torch.tensor([1 if state["turn"]["isHammerSide"] else 0], dtype=torch.long)
    with torch.no_grad():
        policy_logits, action, _ = _MODEL(features, hammer)
    normalized = action[0].tolist()
    return [
        float(normalized[0]) * ACTION_SCALE[0],
        float(normalized[1]) * ACTION_SCALE[1],
        float(normalized[2]) * ACTION_SCALE[2],
    ], TACTICS[int(policy_logits.argmax(dim=1).item())]


def _benchmark_one(task: tuple[int, dict[str, Any], dict[str, int]]) -> dict[str, Any]:
    global _EVALUATION
    if _EVALUATION is None:
        raise RuntimeError("worker simulator is not initialized")
    scenario_index, scenario, config = task
    target = int(scenario["targetShot"])
    team = target % 2
    scenario_seed = int(config["seed"]) + scenario_index * 500_009 + target * 31
    states = states_from_scenario(_EVALUATION, scenario, scenario_seed)
    action, tactic = model_action(states, target)
    fixed_action = list(scripted_continuation_shot(states, target))
    paired: list[dict[str, int]] = []
    for repeat in range(int(config["evaluationRollouts"])):
        episode_seed = scenario_seed + 400_003 + repeat * 11_003
        model_score, _ = rollout_to_end(_EVALUATION, states, target, team, action, episode_seed)
        fixed_score, _ = rollout_to_end(_EVALUATION, states, target, team, fixed_action, episode_seed)
        paired.append({"episodeSeed": episode_seed, "modelTerminalScoreForSelf": model_score, "fixedTerminalScoreForSelf": fixed_score, "deltaModelMinusFixed": model_score - fixed_score})
    model_scores = [row["modelTerminalScoreForSelf"] for row in paired]
    fixed_scores = [row["fixedTerminalScoreForSelf"] for row in paired]
    return {
        "scenario": str(scenario["id"]), "category": str(scenario["category"]), "scenarioSeed": scenario_seed,
        "targetShot": target, "currentShooter": "first" if team == 0 else "second", "isHammerSide": bool(team == 1),
        "fixedBoard": scenario, "modelAction": action, "modelTactic": tactic,
        "fixedAction": fixed_action, "fixedPolicy": "scripted_continuation_v1",
        "modelMeanTerminalScoreForSelf": mean(model_scores), "fixedMeanTerminalScoreForSelf": mean(fixed_scores),
        "meanDeltaModelMinusFixed": mean([row["deltaModelMinusFixed"] for row in paired]),
        "pairedEvaluation": paired,
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    if args.evaluation_rollouts < 1 or args.workers < 1:
        raise ValueError("evaluation rollouts and workers must be positive")
    if not args.checkpoint.is_file():
        raise FileNotFoundError(args.checkpoint)
    document = json.loads(args.scenario_file.read_text(encoding="utf-8"))
    scenarios = validate_scenarios(document)
    config = {"seed": int(args.seed), "evaluationRollouts": int(args.evaluation_rollouts)}
    tasks = [(index, scenario, config) for index, scenario in enumerate(scenarios)]
    rows: list[dict[str, Any]] = []
    checkpoint_path = str(args.checkpoint.resolve())
    if args.workers == 1:
        _init_worker(checkpoint_path)
        for task in tasks:
            rows.append(_benchmark_one(task))
    else:
        context = multiprocessing.get_context("spawn")
        with ProcessPoolExecutor(max_workers=args.workers, mp_context=context, initializer=_init_worker, initargs=(checkpoint_path,)) as executor:
            for future in as_completed([executor.submit(_benchmark_one, task) for task in tasks]):
                rows.append(future.result())
    rows.sort(key=lambda row: (int(row["targetShot"]), str(row["scenario"])))
    first = [row for row in rows if row["currentShooter"] == "first"]
    second = [row for row in rows if row["currentShooter"] == "second"]
    report = {
        "schema": "strict_p1_model_vs_fixed_paired_benchmark_v1",
        "scope": "non-sweeping; strict local PhysX; fixed late-end boards; model acts directly; fresh paired paths excluded from training",
        "claimBoundary": "This compares a direct P1 action with a fixed continuation script on one-end late positions. It is not a model-guided-search, opponent-pool, whole-end, or full-match result.",
        "checkpoint": {"path": str(args.checkpoint), "sha256": sha256_file(args.checkpoint)},
        "scenarioFixture": str(args.scenario_file),
        "configuration": {**config, "workers": int(args.workers), "fixedPolicy": "scripted_continuation_v1"},
        "summary": {"all": summarize(rows), "first": summarize(first), "second": summarize(second)},
        "scenarios": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> int:
    report = run(parse_args())
    for role in ("all", "first", "second"):
        summary = report["summary"][role]
        print("P1 物理评测 %s：模型-固定 %+.4f 分（%d 个局面）" % (role, summary["meanDeltaModelMinusFixed"], summary["scenarioCount"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
