# -*- coding: utf-8 -*-
"""Probe explainable offensive decisions on fixed tactical boards."""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from continuous_shot_search import choose_refined_plan, play_controlled_shot, tactic_group
from fast_curling_env import HOUSE_X, HOUSE_Y, FastCurlingEnv, Stone, distance
from train_search_distill import load_model


def make_scenario(name: str, player_is_init: bool) -> tuple[FastCurlingEnv, int]:
    env = FastCurlingEnv(seed=0)
    env.shot_num = 8 if player_is_init else 9
    target_idx = 1 if player_is_init else 0
    own_idx = 0 if player_is_init else 1

    if name == "enemy_button":
        env.stones[target_idx] = Stone(HOUSE_X, HOUSE_Y, True)
        env.stones[own_idx] = Stone(HOUSE_X + 1.15, HOUSE_Y + 0.45, True)
    elif name == "enemy_top_four":
        env.stones[target_idx] = Stone(HOUSE_X - 0.20, HOUSE_Y + 0.65, True)
        env.stones[own_idx] = Stone(HOUSE_X + 1.20, HOUSE_Y + 1.20, True)
    elif name == "center_guard_blocks":
        env.stones[target_idx] = Stone(HOUSE_X, HOUSE_Y + 2.25, True)
        env.stones[own_idx] = Stone(HOUSE_X + 0.90, HOUSE_Y + 0.25, True)
    else:
        raise ValueError(f"unknown scenario: {name}")
    return env, target_idx


def target_state(env: FastCurlingEnv, target_idx: int) -> Dict[str, Any]:
    stone = env.stones[target_idx]
    if not stone.in_play:
        return {"in_play": False, "x": 0.0, "y": 0.0, "house_distance": None}
    return {
        "in_play": True,
        "x": round(stone.x, 4),
        "y": round(stone.y, 4),
        "house_distance": round(distance(stone.x, stone.y, HOUSE_X, HOUSE_Y), 4),
    }


def probe_side(
    *,
    player: str,
    model_file: Path,
    scenarios: List[str],
    args: argparse.Namespace,
) -> List[Dict[str, Any]]:
    model = load_model(model_file)
    player_is_init = player == "first"
    rng = random.Random(args.seed + (0 if player_is_init else 1000))
    rows: List[Dict[str, Any]] = []
    for scenario in scenarios:
        env, target_idx = make_scenario(scenario, player_is_init)
        before = target_state(env, target_idx)
        plan = choose_refined_plan(
            env,
            rng,
            model=model,
            top_k=args.top_k,
            max_candidates=args.candidates,
            rollouts=args.rollouts,
            player_is_init=player_is_init,
            strategy_gate_strength=args.strategy_gate_strength,
        )
        after_env = env.clone(seed=args.seed + 33)
        play_controlled_shot(after_env, plan.swept_shot())
        after = target_state(after_env, target_idx)
        rows.append(
            {
                "player": player,
                "scenario": scenario,
                "action": plan.action_name,
                "tactic_group": tactic_group(plan.action_name),
                "shot": [round(float(x), 4) for x in plan.swept_shot()],
                "mean_score": round(plan.mean_score, 4),
                "std_score": round(plan.std_score, 4),
                "explanation": plan.explanation,
                "target_before": before,
                "target_after": after,
            }
        )
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--first-model-file", type=Path, default=PROJECT_ROOT / "model" / "search_distill_tactic_policy_first.pt")
    parser.add_argument("--second-model-file", type=Path, default=PROJECT_ROOT / "model" / "search_distill_tactic_policy_second.pt")
    parser.add_argument("--top-k", type=int, default=4)
    parser.add_argument("--candidates", type=int, default=24)
    parser.add_argument("--rollouts", type=int, default=2)
    parser.add_argument("--strategy-gate-strength", type=float, default=0.7)
    parser.add_argument("--seed", type=int, default=20260710)
    parser.add_argument("--report-file", type=Path, default=PROJECT_ROOT / "log" / "offense_probe.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scenarios = ["enemy_button", "enemy_top_four", "center_guard_blocks"]
    rows = []
    rows.extend(
        probe_side(
            player="first",
            model_file=args.first_model_file,
            scenarios=scenarios,
            args=args,
        )
    )
    rows.extend(
        probe_side(
            player="second",
            model_file=args.second_model_file,
            scenarios=scenarios,
            args=args,
        )
    )
    report = {"config": vars(args) | {"scenarios": scenarios}, "probes": rows}
    args.report_file.parent.mkdir(parents=True, exist_ok=True)
    args.report_file.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False, default=str), flush=True)


if __name__ == "__main__":
    main()
