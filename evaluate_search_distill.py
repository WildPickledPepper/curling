# -*- coding: utf-8 -*-
"""Evaluate trained search-distilled policy against local fast simulator."""

from __future__ import annotations

import argparse
import json
import random
import time
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

from continuous_shot_search import (
    ShotPlan,
    choose_refined_plan,
    is_our_turn,
    play_controlled_shot,
    play_uncontrolled_shot,
    score_for_player,
)
from fast_curling_env import FastCurlingEnv
from train_search_distill import (
    choose_model_action,
    evaluate_policy,
    legal_options,
    load_model,
    scripted_index,
    search_action,
    valid_indices,
)
from tactic_dqn_robot import ACTIONS


def summarize_scores(scores: List[int]) -> Dict[str, float]:
    return {
        "games": len(scores),
        "avg_score": float(np.mean(scores)),
        "win_rate": float(np.mean([s > 0 for s in scores])),
        "loss_rate": float(np.mean([s < 0 for s in scores])),
        "draw_rate": float(np.mean([s == 0 for s in scores])),
        "min_score": float(np.min(scores)),
        "max_score": float(np.max(scores)),
    }


def evaluate_refined_model(
    games: int,
    seed: int,
    model_file: Path,
    top_k: int,
    candidates: int,
    rollouts: int,
    player_is_init: bool = True,
    adaptive: bool = False,
    late_top_k: int = 4,
    late_candidates: int = 32,
    late_rollouts: int = 3,
    hammer_candidates: int = 48,
    hammer_rollouts: int = 4,
    strategy_gate_strength: float = 0.0,
    trace_games: int = 0,
) -> Dict[str, Any]:
    rng = random.Random(seed)
    model = load_model(model_file)
    scores: List[int] = []
    tactic_counts: Counter[str] = Counter()
    sweep_count = 0
    own_shots = 0
    traces: List[Dict[str, Any]] = []

    for game_idx in range(games):
        env = FastCurlingEnv(seed=rng.randint(1, 2_000_000_000))
        trace: Dict[str, Any] = {"game": game_idx, "player_is_init": player_is_init, "shots": []}
        while env.shot_num < 16:
            if not is_our_turn(env.shot_num, player_is_init):
                play_uncontrolled_shot(env)
                continue

            budget_name = "fixed"
            cur_top_k = top_k
            cur_candidates = candidates
            cur_rollouts = rollouts
            if adaptive:
                completed_own_shots = max(0, min(8, env.shot_num // 2))
                remaining_own_shots = max(1, 8 - completed_own_shots)
                if remaining_own_shots == 1 and not player_is_init:
                    budget_name = "hammer"
                    cur_top_k = max(cur_top_k, late_top_k)
                    cur_candidates = max(cur_candidates, hammer_candidates)
                    cur_rollouts = max(cur_rollouts, hammer_rollouts)
                elif remaining_own_shots <= 2 or env.shot_num >= 12:
                    budget_name = "late"
                    cur_top_k = max(cur_top_k, late_top_k)
                    cur_candidates = max(cur_candidates, late_candidates)
                    cur_rollouts = max(cur_rollouts, late_rollouts)

            plan = choose_refined_plan(
                env,
                rng,
                model=model,
                top_k=cur_top_k,
                max_candidates=cur_candidates,
                rollouts=cur_rollouts,
                player_is_init=player_is_init,
                strategy_gate_strength=strategy_gate_strength,
            )
            shot_num = env.shot_num
            play_controlled_shot(env, plan.swept_shot())
            tactic_counts[plan.action_name] += 1
            own_shots += 1
            if plan.sweep > 0:
                sweep_count += 1
            if game_idx < trace_games:
                trace["shots"].append(
                    {
                        "shot_num": shot_num,
                        "budget": budget_name,
                        "action": plan.action_name,
                        "shot": [round(x, 4) for x in plan.shot],
                        "sweep": round(plan.sweep, 4),
                        "search_mean": round(plan.mean_score, 4),
                        "search_std": round(plan.std_score, 4),
                        "top_candidates": [
                            {
                                "shot": [round(x, 4) for x in item.shot[:3]],
                                "sweep": round(item.shot[3], 4),
                                "mean": round(item.mean_score, 4),
                                "std": round(item.std_score, 4),
                            }
                            for item in plan.candidates[:3]
                        ],
                    }
                )

        score = score_for_player(env, player_is_init)
        scores.append(score)
        if game_idx < trace_games:
            trace["score"] = score
            trace["final_position"] = [round(x, 3) for x in env.position()]
            traces.append(trace)

    summary = summarize_scores(scores)
    summary.update(
        {
            "top_k": top_k,
            "candidates": candidates,
            "rollouts": rollouts,
            "player_is_init": player_is_init,
            "adaptive": adaptive,
            "strategy_gate_strength": strategy_gate_strength,
            "sweep_rate": float(sweep_count / max(1, own_shots)),
            "tactic_counts": dict(tactic_counts.most_common()),
            "traces": traces,
        }
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate search-distilled tactic policy")
    parser.add_argument("--model-file", default="model/search_distill_tactic_policy.pt")
    parser.add_argument("--first-model-file", default=None)
    parser.add_argument("--second-model-file", default=None)
    parser.add_argument("--games", type=int, default=2000)
    parser.add_argument("--search-games", type=int, default=200)
    parser.add_argument("--refined-games", type=int, default=300)
    parser.add_argument("--refined-top-k", type=int, default=3)
    parser.add_argument("--refined-candidates", type=int, default=24)
    parser.add_argument("--refined-rollouts", type=int, default=2)
    parser.add_argument("--adaptive-refined", action="store_true")
    parser.add_argument("--late-refined-top-k", type=int, default=4)
    parser.add_argument("--late-refined-candidates", type=int, default=32)
    parser.add_argument("--late-refined-rollouts", type=int, default=3)
    parser.add_argument("--hammer-refined-candidates", type=int, default=48)
    parser.add_argument("--hammer-refined-rollouts", type=int, default=4)
    parser.add_argument("--strategy-gate-strength", type=float, default=0.0)
    parser.add_argument("--trace-games", type=int, default=5)
    parser.add_argument("--seed", type=int, default=20260706)
    parser.add_argument("--report-file", default="log/search_distill_eval.json")
    args = parser.parse_args()

    started = time.time()
    model_file = Path(args.model_file)
    first_model_file = Path(args.first_model_file) if args.first_model_file else model_file
    second_model_file = Path(args.second_model_file) if args.second_model_file else model_file
    report = {
        "model_file": str(model_file),
        "first_model_file": str(first_model_file),
        "second_model_file": str(second_model_file),
        "games": args.games,
        "search_games": args.search_games,
        "evaluation": {
            "random": evaluate_policy("random", args.games, args.seed + 1),
            "scripted": evaluate_policy("scripted", args.games, args.seed + 2),
            "model": evaluate_policy("model", args.games, args.seed + 3, model_file),
            "search_rollouts4": evaluate_policy("search", args.search_games, args.seed + 4),
            "model_refined_continuous": evaluate_refined_model(
                args.refined_games,
                args.seed + 5,
                first_model_file,
                top_k=args.refined_top_k,
                candidates=args.refined_candidates,
                rollouts=args.refined_rollouts,
                player_is_init=True,
                adaptive=args.adaptive_refined,
                late_top_k=args.late_refined_top_k,
                late_candidates=args.late_refined_candidates,
                late_rollouts=args.late_refined_rollouts,
                hammer_candidates=args.hammer_refined_candidates,
                hammer_rollouts=args.hammer_refined_rollouts,
                strategy_gate_strength=args.strategy_gate_strength,
                trace_games=args.trace_games,
            ),
            "model_refined_continuous_second": evaluate_refined_model(
                args.refined_games,
                args.seed + 6,
                second_model_file,
                top_k=args.refined_top_k,
                candidates=args.refined_candidates,
                rollouts=args.refined_rollouts,
                player_is_init=False,
                adaptive=args.adaptive_refined,
                late_top_k=args.late_refined_top_k,
                late_candidates=args.late_refined_candidates,
                late_rollouts=args.late_refined_rollouts,
                hammer_candidates=args.hammer_refined_candidates,
                hammer_rollouts=args.hammer_refined_rollouts,
                strategy_gate_strength=args.strategy_gate_strength,
                trace_games=args.trace_games,
            ),
        },
        "elapsed_sec": time.time() - started,
    }
    Path(args.report_file).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report_file).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
