#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""固定壶面上筛选“本手严格 PhysX + PPO 下一手回应”的小动作网格。

用于 K5--K8 的局部反例排查：候选是有限手工网格，结果只描述这两手，
不能替代状态机、连续求解或完整 end 胜率验证。
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd, install_bundled_pyphysx, score_board
from planning_proxy.evaluate_vs_teammate_ppo import state_position
from planning_proxy.replay_fixed_transition_vs_ppo import expanded_fixture
from training_research.opponents.teammate_ppo_adapter import TeammatePPOOpponent


def _live_board(states: Sequence[dict[str, Any]]) -> list[dict[str, float | int]]:
    return [
        {"index": index, "x": float(state["x"]), "y": float(state["y"])}
        for index, state in enumerate(states) if bool(state.get("enabled", False))
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--board", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--shot-index", type=int, required=True, help="先手的零基偶数手号，例如 K6 为 10")
    parser.add_argument("--seeds", nargs="+", type=int, default=(20260718, 20260719, 20260720))
    parser.add_argument("--v-values", nargs="+", type=float, required=True)
    parser.add_argument("--h-values", nargs="+", type=float, required=True)
    parser.add_argument("--w-values", nargs="+", type=float, required=True)
    args = parser.parse_args()
    if not 0 <= int(args.shot_index) <= 14 or int(args.shot_index) % 2:
        raise SystemExit("--shot-index 必须是先手的 0,2,...,14；并且必须留出 PPO 回应。")

    board = expanded_fixture(args.board)
    candidates = list(itertools.product(args.v_values, args.h_values, args.w_values))
    ppo_reply_shot = int(args.shot_index) + 1
    install_bundled_pyphysx()
    ppo = TeammatePPOOpponent(deterministic=True)
    ranked: list[dict[str, Any]] = []
    try:
        for candidate in candidates:
            outcomes: list[dict[str, Any]] = []
            for seed in args.seeds:
                environment = StrictCurlingEnd(seed=int(seed), training_fast=True)
                environment.reset()
                environment.shot_number = int(args.shot_index)
                states = environment.restore_settled_states(board)
                own = environment.play(tuple(float(value) for value in candidate))
                own_score = int(score_board(own["states"]))
                reply = ppo.choose(
                    state_position(own["states"]), player_is_init=False, shot_num=ppo_reply_shot,
                    end_score=own_score, total_ends=1, current_player=1,
                )
                opponent = environment.play(reply.bestshot)
                outcomes.append({
                    "seed": int(seed),
                    "score_after_own": own_score,
                    "score_after_reply": int(score_board(opponent["states"])),
                    "own_cleared": [int(index) for index in own["cleared"]],
                    "own_final_board": _live_board(own["states"]),
                    "ppo_tactic": reply.tactic,
                    "ppo_bestshot": [float(value) for value in reply.bestshot],
                    "ppo_cleared": [int(index) for index in opponent["cleared"]],
                })
            scores = [int(row["score_after_reply"]) for row in outcomes]
            ranked.append({
                "bestshot": [float(value) for value in candidate],
                "worst_reply_score": min(scores),
                "mean_reply_score": sum(scores) / len(scores),
                "all_seeds_nonloss": all(score >= 0 for score in scores),
                "outcomes": outcomes,
            })
    finally:
        close = getattr(ppo, "close", None)
        if callable(close):
            close()

    ranked.sort(key=lambda row: (int(row["worst_reply_score"]), float(row["mean_reply_score"])), reverse=True)
    report = {
        "schema": "local_one_reply_grid_vs_deterministic_ppo_v1",
        "scope": "one fixed board, finite action grid, strict own shot then deterministic PPO one-shot reply; not a full-end proof",
        "board": str(args.board),
        "shot_index": int(args.shot_index),
        "seeds": [int(seed) for seed in args.seeds],
        "candidate_count": len(ranked),
        "all_seeds_nonloss_count": sum(bool(row["all_seeds_nonloss"]) for row in ranked),
        "ranked_candidates": ranked,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in ranked[:10]:
        print(json.dumps({
            "bestshot": row["bestshot"], "worst_reply_score": row["worst_reply_score"],
            "mean_reply_score": row["mean_reply_score"], "all_seeds_nonloss": row["all_seeds_nonloss"],
        }, ensure_ascii=False))
    print("all_seeds_nonloss_count=%d/%d" % (report["all_seeds_nonloss_count"], len(ranked)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
