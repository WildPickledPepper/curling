#!/usr/bin/env python3
"""One-step strict-PhysX search smoke test for non-sweeping curling.

This script verifies scene reuse and friction-path injection only.  It
evaluates the board immediately after the proposed shot, without an opponent
response or a continuation rollout.  Its score therefore is *not* an end-score
target and its output must not enter policy/value training.  The formal P0
collector is specified in ``05_detailed_literature_to_system_spec.md`` and
must add kernel sharing, role/match state, and continuation rollouts first.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.runtime_loader import install_bundled_pyphysx
from local_simulator.examples.train_policy_tree_selfplay import (
    STONE_COUNT,
    StrictCurlingEnd,
    TACTICS,
    score_board,
    tactic_shot,
    team_score,
)


@dataclass(frozen=True)
class Proposal:
    tactic: str
    shot: tuple[float, float, float]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--games", type=int, default=1)
    parser.add_argument("--rollouts", type=int, default=2, help="friction samples per proposed shot")
    parser.add_argument("--seed", type=int, default=20260715)
    parser.add_argument("--risk-penalty", type=float, default=0.25)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "training_research" / "runs" / "p0_one_step_smoke_only.json",
    )
    return parser.parse_args()


def state_snapshot(states: Sequence[dict[str, Any]]) -> tuple[list[float], dict[int, float]]:
    """Turn a settled public board into an independently replayable reset."""

    positions = [0.0] * 32
    yaws: dict[int, float] = {}
    for state in states:
        index = int(state["index"])
        yaws[index] = float(state["yaw"])
        if not state["enabled"]:
            continue
        pair = index // 2
        offset = pair * 4 + (0 if index % 2 == 0 else 2)
        positions[offset] = float(state["x"])
        positions[offset + 1] = float(state["y"])
    return positions, yaws


def proposed_shots(states: Sequence[dict[str, Any]], team: int) -> list[Proposal]:
    """Use verified tactics, then make small continuous parameter variations."""

    proposals: list[Proposal] = []
    # The tactical set is intentionally small for P0; it covers guards, draw,
    # take-out and deliberate blanking without inventing an unvalidated shot.
    for tactic_index, tactic in enumerate(TACTICS):
        base = tactic_shot(tactic_index, states, team)
        proposals.append(Proposal(tactic.name, tuple(float(value) for value in base)))
        for dv, dh, dw in ((-0.06, 0.0, 0.0), (0.06, 0.0, 0.0), (0.0, -0.08, 0.0), (0.0, 0.08, 0.0)):
            v, h, w = base
            proposals.append(
                Proposal(
                    tactic.name,
                    (max(0.0, min(6.0, v + dv)), max(-2.23, min(2.23, h + dh)), max(-15.7, min(15.7, w + dw))),
                )
            )
    # Identical tactical formulas can occasionally emit the same shot.
    unique: dict[tuple[float, float, float], Proposal] = {}
    for proposal in proposals:
        unique.setdefault(tuple(round(value, 7) for value in proposal.shot), proposal)
    return list(unique.values())


def evaluate_proposal(
    *,
    positions: list[float],
    yaws: dict[int, float],
    shot_number: int,
    team: int,
    proposal: Proposal,
    rollout_seeds: Sequence[int],
    workers: Sequence[StrictCurlingEnd],
) -> dict[str, Any]:
    """Evaluate one action from the same settled board under several RNG paths."""

    values: list[int] = []
    contacts = 0
    out_of_play = 0
    for worker_index, seed in enumerate(rollout_seeds):
        # Reuse the already-cooked persistent PhysX scene.  A rollout starts
        # from a settled reset, so changing this deterministic seed changes
        # only its friction sequence, not the scene construction or geometry.
        environment = workers[worker_index % len(workers)]
        environment.seed = int(seed)
        environment.scene.reset_positions(positions, yaw_overrides=yaws)
        environment.shot_number = shot_number
        result = environment.play(proposal.shot)
        values.append(team_score(score_board(result["states"]), team))
        contacts += int(result["contact"])
        out_of_play += len(result["cleared"])
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    return {
        "tactic": proposal.tactic,
        "bestshot": list(proposal.shot),
        "rolloutCount": len(values),
        "scores": values,
        "meanScore": mean,
        "scoreStd": math.sqrt(variance),
        "scoreDistribution": {str(score): values.count(score) for score in sorted(set(values))},
        "contactProbability": contacts / len(values),
        "outOfPlayMean": out_of_play / len(values),
    }


def choose_teacher_action(
    states: Sequence[dict[str, Any]],
    shot_number: int,
    team: int,
    seed: int,
    rollouts: int,
    risk_penalty: float,
    workers: Sequence[StrictCurlingEnd],
) -> dict[str, Any]:
    positions, yaws = state_snapshot(states)
    proposals = proposed_shots(states, team)
    stats = []
    for proposal_index, proposal in enumerate(proposals):
        rollout_seeds = [seed + proposal_index * 1009 + repeat * 7919 for repeat in range(rollouts)]
        row = evaluate_proposal(
            positions=positions,
            yaws=yaws,
            shot_number=shot_number,
            team=team,
            proposal=proposal,
            rollout_seeds=rollout_seeds,
            workers=workers,
        )
        row["robustScore"] = row["meanScore"] - risk_penalty * row["scoreStd"]
        stats.append(row)
    stats.sort(key=lambda row: (float(row["robustScore"]), float(row["meanScore"])), reverse=True)
    selected = stats[0]
    return {
        "shot": shot_number + 1,
        "team": "first" if team == 0 else "second",
        "boardScoreBefore": score_board(states),
        "candidateCount": len(stats),
        "selected": selected,
        "candidates": stats,
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    if args.games < 1 or args.rollouts < 1:
        raise ValueError("--games and --rollouts must be positive")
    install_bundled_pyphysx()
    master = StrictCurlingEnd(seed=args.seed, training_fast=True)
    # These scenes stay alive for the entire collection run.  They are reset
    # before every candidate, exactly as an independent rollout would be.
    rollout_workers = [
        StrictCurlingEnd(seed=args.seed + index + 1, training_fast=True)
        for index in range(args.rollouts)
    ]
    games = []
    for game_index in range(args.games):
        states = master.reset()
        decisions = []
        for _ in range(STONE_COUNT):
            shot_number = master.shot_number
            team = shot_number % 2
            teacher = choose_teacher_action(
                states,
                shot_number,
                team,
                args.seed + game_index * 100_003 + shot_number * 5_003,
                args.rollouts,
                args.risk_penalty,
                rollout_workers,
            )
            shot = tuple(float(value) for value in teacher["selected"]["bestshot"])
            executed = master.play(shot)
            teacher["executed"] = {
                "contact": bool(executed["contact"]),
                "cleared": list(executed["cleared"]),
                "boardScoreAfter": score_board(executed["states"]),
            }
            decisions.append(teacher)
            states = executed["states"]
            print(
                f"P0 第 {game_index + 1} 局第 {shot_number + 1:02d} 手 | "
                f"{teacher['selected']['tactic']} {teacher['selected']['bestshot']} | "
                f"稳健分 {teacher['selected']['robustScore']:.2f}",
                flush=True,
            )
        games.append({"game": game_index + 1, "finalScoreFirst": score_board(states), "decisions": decisions})
    report = {
        "schema": "strict_p0_one_step_smoke_v1_not_training_data",
        "scope": "non-sweeping; tactic proposals plus local continuous perturbations; strict local PhysX only; no continuation rollout",
        "trainingUsable": False,
        "rolloutsPerCandidate": args.rollouts,
        "riskPenalty": args.risk_penalty,
        "games": games,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> int:
    args = parse_args()
    report = run(args)
    print(f"P0 完成：{len(report['games'])} 局，搜索数据写入 {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
