# -*- coding: utf-8 -*-
"""Head-to-head evaluation between local curling policies."""

from __future__ import annotations

import argparse
import json
import random
import time
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

import numpy as np

from continuous_shot_search import (
    choose_refined_plan,
    legal_options_for_player,
    play_controlled_shot,
    scripted_index_for_player,
)
from fast_curling_env import FastCurlingEnv, Shot
from tactic_dqn_robot import ACTIONS
from train_search_distill import load_model, rollout_shot, valid_indices


class Policy:
    def __init__(
        self,
        name: str,
        first_model_file: Optional[Path],
        second_model_file: Optional[Path],
        top_k: int,
        candidates: int,
        rollouts: int,
        late_top_k: int,
        late_candidates: int,
        late_rollouts: int,
        hammer_candidates: int,
        hammer_rollouts: int,
    ) -> None:
        self.name = name
        self.first_model = load_model(first_model_file) if first_model_file else None
        self.second_model = load_model(second_model_file) if second_model_file else None
        self.top_k = top_k
        self.candidates = candidates
        self.rollouts = rollouts
        self.late_top_k = late_top_k
        self.late_candidates = late_candidates
        self.late_rollouts = late_rollouts
        self.hammer_candidates = hammer_candidates
        self.hammer_rollouts = hammer_rollouts

    def budget(self, shot_num: int, player_is_init: bool) -> tuple[int, int, int, str]:
        completed_own_shots = max(0, min(8, shot_num // 2))
        remaining_own_shots = max(1, 8 - completed_own_shots)
        if remaining_own_shots == 1 and not player_is_init:
            return (
                max(self.top_k, self.late_top_k),
                max(self.candidates, self.hammer_candidates),
                max(self.rollouts, self.hammer_rollouts),
                "hammer",
            )
        if remaining_own_shots <= 2 or shot_num >= 12:
            return (
                max(self.top_k, self.late_top_k),
                max(self.candidates, self.late_candidates),
                max(self.rollouts, self.late_rollouts),
                "late",
            )
        return self.top_k, self.candidates, self.rollouts, "normal"

    def choose(self, env: FastCurlingEnv, rng: random.Random, player_is_init: bool) -> tuple[Sequence[float], str, str]:
        options = legal_options_for_player(env, player_is_init)
        valid = valid_indices(options)
        if self.name == "random":
            idx = rng.choice(valid) if valid else 0
            shot = options[idx] if valid else (3.0, 0.0, 0.0)
            return shot or (3.0, 0.0, 0.0), ACTIONS[idx].name if valid else "fallback", "none"
        if self.name == "rollout":
            return rollout_shot(env, rng), "rollout", "none"
        if self.name == "scripted":
            idx = scripted_index_for_player(env, options, player_is_init)
            shot = options[idx] or (3.0, 0.0, 0.0)
            return shot, ACTIONS[idx].name, "none"
        if self.name in {"shared_refined", "dual_refined"}:
            if self.name == "shared_refined":
                model = self.first_model
            else:
                model = self.first_model if player_is_init else self.second_model
            if model is None:
                raise ValueError(f"{self.name} requires model files")
            top_k, candidates, rollouts, budget = self.budget(env.shot_num, player_is_init)
            plan = choose_refined_plan(
                env,
                rng,
                model=model,
                top_k=top_k,
                max_candidates=candidates,
                rollouts=rollouts,
                player_is_init=player_is_init,
            )
            return plan.swept_shot(), plan.action_name, budget
        raise ValueError(f"unknown policy: {self.name}")


def make_policy(
    name: str,
    first_model_file: Path,
    second_model_file: Path,
    args: argparse.Namespace,
) -> Policy:
    needs_first = name in {"shared_refined", "dual_refined"}
    needs_second = name == "dual_refined"
    return Policy(
        name=name,
        first_model_file=first_model_file if needs_first else None,
        second_model_file=second_model_file if needs_second else None,
        top_k=args.top_k,
        candidates=args.candidates,
        rollouts=args.rollouts,
        late_top_k=args.late_top_k,
        late_candidates=args.late_candidates,
        late_rollouts=args.late_rollouts,
        hammer_candidates=args.hammer_candidates,
        hammer_rollouts=args.hammer_rollouts,
    )


def play_match(
    blue: Policy,
    red: Policy,
    seed: int,
    trace: bool = False,
) -> Dict[str, Any]:
    rng = random.Random(seed)
    env = FastCurlingEnv(seed=rng.randint(1, 2_000_000_000))
    blue_actions: Counter[str] = Counter()
    red_actions: Counter[str] = Counter()
    budgets: Counter[str] = Counter()
    shots = []

    while env.shot_num < 16:
        player_is_init = env.shot_num % 2 == 0
        policy = blue if player_is_init else red
        shot, action, budget = policy.choose(env, rng, player_is_init)
        shot_num = env.shot_num
        play_controlled_shot(env, shot)
        if player_is_init:
            blue_actions[action] += 1
        else:
            red_actions[action] += 1
        budgets[f"{'blue' if player_is_init else 'red'}:{budget}"] += 1
        if trace:
            shots.append(
                {
                    "shot_num": shot_num,
                    "side": "blue" if player_is_init else "red",
                    "action": action,
                    "budget": budget,
                    "shot": [round(float(x), 4) for x in shot],
                }
            )

    score = env.end_score()
    return {
        "score_blue": score,
        "blue_actions": dict(blue_actions.most_common()),
        "red_actions": dict(red_actions.most_common()),
        "budget_counts": dict(budgets.most_common()),
        "trace": shots,
    }


def summarize(scores: list[int]) -> Dict[str, float]:
    return {
        "games": len(scores),
        "avg_score_blue": float(np.mean(scores)) if scores else 0.0,
        "blue_win_rate": float(np.mean([score > 0 for score in scores])) if scores else 0.0,
        "red_win_rate": float(np.mean([score < 0 for score in scores])) if scores else 0.0,
        "draw_rate": float(np.mean([score == 0 for score in scores])) if scores else 0.0,
        "min_score_blue": float(np.min(scores)) if scores else 0.0,
        "max_score_blue": float(np.max(scores)) if scores else 0.0,
    }


def run_series(
    blue: Policy,
    red: Policy,
    games: int,
    rng: random.Random,
    trace_games: int,
) -> tuple[list[int], Counter[str], Counter[str], Counter[str], list[Dict[str, Any]]]:
    scores: list[int] = []
    blue_actions: Counter[str] = Counter()
    red_actions: Counter[str] = Counter()
    budgets: Counter[str] = Counter()
    traces = []
    for game_idx in range(games):
        result = play_match(
            blue,
            red,
            seed=rng.randint(1, 2_000_000_000),
            trace=game_idx < trace_games,
        )
        scores.append(int(result["score_blue"]))
        blue_actions.update(result["blue_actions"])
        red_actions.update(result["red_actions"])
        budgets.update(result["budget_counts"])
        if game_idx < trace_games:
            traces.append({"game": game_idx, **result})
    return scores, blue_actions, red_actions, budgets, traces


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local head-to-head policy matches")
    parser.add_argument("--blue-policy", choices=["random", "rollout", "scripted", "shared_refined", "dual_refined"], default="dual_refined")
    parser.add_argument("--red-policy", choices=["random", "rollout", "scripted", "shared_refined", "dual_refined"], default="shared_refined")
    parser.add_argument("--swap-sides", action="store_true", help="also run red policy as blue and report policy-level symmetric results")
    parser.add_argument("--first-model-file", default="model/search_distill_tactic_policy_first.pt")
    parser.add_argument("--second-model-file", default="model/search_distill_tactic_policy_second.pt")
    parser.add_argument("--games", type=int, default=40)
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--candidates", type=int, default=16)
    parser.add_argument("--rollouts", type=int, default=1)
    parser.add_argument("--late-top-k", type=int, default=4)
    parser.add_argument("--late-candidates", type=int, default=24)
    parser.add_argument("--late-rollouts", type=int, default=2)
    parser.add_argument("--hammer-candidates", type=int, default=32)
    parser.add_argument("--hammer-rollouts", type=int, default=2)
    parser.add_argument("--seed", type=int, default=20260708)
    parser.add_argument("--trace-games", type=int, default=2)
    parser.add_argument("--report-file", default="log/head_to_head_eval.json")
    args = parser.parse_args()

    started = time.time()
    first_model_file = Path(args.first_model_file)
    second_model_file = Path(args.second_model_file)
    blue = make_policy(args.blue_policy, first_model_file, second_model_file, args)
    red = make_policy(args.red_policy, first_model_file, second_model_file, args)
    rng = random.Random(args.seed)
    scores, blue_actions, red_actions, budgets, traces = run_series(blue, red, args.games, rng, args.trace_games)

    report = {
        "config": vars(args),
        "summary": summarize(scores),
        "blue_action_counts": dict(blue_actions.most_common()),
        "red_action_counts": dict(red_actions.most_common()),
        "budget_counts": dict(budgets.most_common()),
        "traces": traces,
        "elapsed_sec": time.time() - started,
    }

    if args.swap_sides:
        swapped_scores, swapped_blue_actions, swapped_red_actions, swapped_budgets, swapped_traces = run_series(
            red,
            blue,
            args.games,
            rng,
            args.trace_games,
        )
        # Positive means args.blue_policy is better after averaging both side assignments.
        policy_a_scores = scores + [-score for score in swapped_scores]
        report["swapped"] = {
            "summary": summarize(swapped_scores),
            "blue_action_counts": dict(swapped_blue_actions.most_common()),
            "red_action_counts": dict(swapped_red_actions.most_common()),
            "budget_counts": dict(swapped_budgets.most_common()),
            "traces": swapped_traces,
        }
        report["symmetric_summary"] = {
            "policy_a": args.blue_policy,
            "policy_b": args.red_policy,
            "games_per_assignment": args.games,
            "policy_a_avg_score": float(np.mean(policy_a_scores)) if policy_a_scores else 0.0,
            "policy_a_win_rate": float(np.mean([score > 0 for score in policy_a_scores])) if policy_a_scores else 0.0,
            "policy_b_win_rate": float(np.mean([score < 0 for score in policy_a_scores])) if policy_a_scores else 0.0,
            "draw_rate": float(np.mean([score == 0 for score in policy_a_scores])) if policy_a_scores else 0.0,
        }
        report["elapsed_sec"] = time.time() - started
    path = Path(args.report_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
