# -*- coding: utf-8 -*-
"""Socket robot for the search-distilled tactic policy."""

from __future__ import annotations

import argparse
import sys
import time
import random
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
import torch

from AIRobot import AIRobot
from continuous_shot_search import choose_refined_plan, env_from_position
from curling_sweep import estimate_sweep_distance
from tactic_dqn_robot import ACTIONS, Shot, make_state_vector
from train_search_distill import PolicyValueNet


class SearchDistillRobot(AIRobot):
    def __init__(
        self,
        key: str,
        name: str,
        host: str,
        port: int,
        model_file: str = "model/search_distill_tactic_policy.pt",
        first_model_file: Optional[str] = None,
        second_model_file: Optional[str] = None,
        sweep_mode: str = "heuristic",
        shot_search: str = "local",
        search_top_k: int = 3,
        search_candidates: int = 24,
        search_rollouts: int = 2,
        adaptive_search: bool = True,
        late_search_top_k: int = 4,
        late_search_candidates: int = 32,
        late_search_rollouts: int = 3,
        hammer_search_candidates: int = 48,
        hammer_search_rollouts: int = 4,
        strategy_gate_strength: float = 0.0,
        search_seed: int = 20260705,
        show_msg: bool = False,
    ):
        super().__init__(key, name, host, port, show_msg=show_msg)
        self.first_model_file = first_model_file or model_file
        self.second_model_file = second_model_file or model_file
        self.first_model = self.load_policy_model(self.first_model_file)
        self.second_model = self.load_policy_model(self.second_model_file)
        self.model = self.first_model
        self.model_file = model_file
        self.sweep_mode = sweep_mode
        self.shot_search = shot_search
        self.search_top_k = search_top_k
        self.search_candidates = search_candidates
        self.search_rollouts = search_rollouts
        self.adaptive_search = adaptive_search
        self.late_search_top_k = late_search_top_k
        self.late_search_candidates = late_search_candidates
        self.late_search_rollouts = late_search_rollouts
        self.hammer_search_candidates = hammer_search_candidates
        self.hammer_search_rollouts = hammer_search_rollouts
        self.strategy_gate_strength = strategy_gate_strength
        self.search_rng = random.Random(search_seed)
        self.last_shot: Optional[Shot] = None
        self.last_action_name = ""
        self.planned_sweep = 0.0

    @staticmethod
    def load_policy_model(model_file: str) -> PolicyValueNet:
        payload = torch.load(model_file, map_location="cpu")
        model = PolicyValueNet()
        model.load_state_dict(payload["model_state"])
        model.eval()
        return model

    def active_model(self) -> PolicyValueNet:
        return self.first_model if self.player_is_init else self.second_model

    def current_search_budget(self) -> Tuple[int, int, int, str]:
        if not self.adaptive_search:
            return self.search_top_k, self.search_candidates, self.search_rollouts, "fixed"

        completed_own_shots = max(0, min(8, self.shot_num // 2))
        remaining_own_shots = max(1, 8 - completed_own_shots)
        is_final_own_shot = remaining_own_shots == 1
        has_hammer = not self.player_is_init

        if is_final_own_shot and has_hammer:
            return (
                max(self.search_top_k, self.late_search_top_k),
                max(self.search_candidates, self.hammer_search_candidates),
                max(self.search_rollouts, self.hammer_search_rollouts),
                "hammer",
            )
        if remaining_own_shots <= 2 or self.shot_num >= 12:
            return (
                max(self.search_top_k, self.late_search_top_k),
                max(self.search_candidates, self.late_search_candidates),
                max(self.search_rollouts, self.late_search_rollouts),
                "late",
            )
        return self.search_top_k, self.search_candidates, self.search_rollouts, "normal"

    def get_state_list(self) -> List[List[float]]:
        state_list: List[List[float]] = []
        for n in range(8):
            state_list.append([float(self.position[n * 4]), float(self.position[n * 4 + 1])])
            state_list.append([float(self.position[n * 4 + 2]), float(self.position[n * 4 + 3])])
        return state_list

    def build_action_options(self) -> List[Optional[Shot]]:
        is_init = 0 if self.player_is_init else 1
        state_list = self.get_state_list()
        return [action.try_shot(state_list, is_init, self.shot_num) for action in ACTIONS]

    def get_bestshot(self) -> str:
        self.planned_sweep = 0.0
        options = self.build_action_options()
        valid = [idx for idx, shot in enumerate(options) if shot is not None]
        if not valid:
            shot = (3.0, 0.0, 0.0)
            action_name = "fallback_draw"
        else:
            state = make_state_vector(
                self.position,
                self.shot_num,
                self.round_num,
                getattr(self, "round_total", 1),
                self.player_is_init,
                getattr(self, "next_shot", 0),
            )
            model = self.active_model()
            with torch.no_grad():
                logits, value = model(torch.tensor(state, dtype=torch.float32).unsqueeze(0))
            scores = logits.squeeze(0).numpy()
            masked = np.full_like(scores, -1e9)
            masked[valid] = scores[valid]
            action_idx = int(np.argmax(masked))
            shot = options[action_idx] or (3.0, 0.0, 0.0)
            action_name = ACTIONS[action_idx].name
            if self.shot_search == "local":
                top_k, candidates, rollouts, budget_name = self.current_search_budget()
                env = env_from_position(self.position, self.shot_num, seed=self.search_rng.randint(1, 2_000_000_000))
                plan = choose_refined_plan(
                    env,
                    self.search_rng,
                    model=model,
                    top_k=top_k,
                    max_candidates=candidates,
                    rollouts=rollouts,
                    player_is_init=self.player_is_init,
                    strategy_gate_strength=self.strategy_gate_strength,
                )
                shot = plan.shot
                action_name = plan.action_name
                self.planned_sweep = plan.sweep
                print(
                    f"refined budget={budget_name} top_k={top_k} candidates={candidates} rollouts={rollouts} "
                    f"gate={self.strategy_gate_strength:.2f} "
                    f"action={plan.action_name} "
                    f"mean={plan.mean_score:.3f} std={plan.std_score:.3f} "
                    f"sweep={plan.sweep:.2f}",
                    flush=True,
                )
        v0, h0, w0 = shot
        self.last_shot = shot
        self.last_action_name = action_name
        print(f"policy_tactic={action_name} shot=({v0:.3f},{h0:.3f},{w0:.3f})", flush=True)
        return f"BESTSHOT {v0} {h0} {w0}"

    def get_sweep_distance(self) -> Optional[float]:
        if self.sweep_mode == "off":
            return None
        if self.shot_search == "local":
            if self.planned_sweep > 0:
                print(f"sweep action={self.last_action_name} distance={self.planned_sweep:.2f}", flush=True)
                return self.planned_sweep
            return None
        distance = estimate_sweep_distance(
            self.last_shot,
            self.last_action_name,
            self.motioninfo,
        )
        if distance <= 0:
            return None
        print(f"sweep action={self.last_action_name} distance={distance:.2f}", flush=True)
        return distance


def main() -> None:
    parser = argparse.ArgumentParser(description="Search-distilled tactic policy robot")
    parser.add_argument("--key", default="local-test:0")
    parser.add_argument("-H", "--host", default="127.0.0.1")
    parser.add_argument("-p", "--port", type=int, default=7788)
    parser.add_argument("--name", default="SearchDistill")
    parser.add_argument("--model-file", default="model/search_distill_tactic_policy.pt")
    parser.add_argument("--first-model-file", default=None)
    parser.add_argument("--second-model-file", default=None)
    parser.add_argument("--sweep-mode", choices=["heuristic", "off"], default="heuristic")
    parser.add_argument("--shot-search", choices=["local", "off"], default="local")
    parser.add_argument("--search-top-k", type=int, default=3)
    parser.add_argument("--search-candidates", type=int, default=24)
    parser.add_argument("--search-rollouts", type=int, default=2)
    parser.add_argument("--fixed-search", action="store_true", help="disable late/hammer adaptive search budgets")
    parser.add_argument("--late-search-top-k", type=int, default=4)
    parser.add_argument("--late-search-candidates", type=int, default=32)
    parser.add_argument("--late-search-rollouts", type=int, default=3)
    parser.add_argument("--hammer-search-candidates", type=int, default=48)
    parser.add_argument("--hammer-search-rollouts", type=int, default=4)
    parser.add_argument("--strategy-gate-strength", type=float, default=0.0)
    parser.add_argument("--search-seed", type=int, default=20260705)
    parser.add_argument("--show-msg", action="store_true")
    args = parser.parse_args()

    robot = SearchDistillRobot(
        key=args.key,
        name=args.name,
        host=args.host,
        port=args.port,
        model_file=args.model_file,
        first_model_file=args.first_model_file,
        second_model_file=args.second_model_file,
        sweep_mode=args.sweep_mode,
        shot_search=args.shot_search,
        search_top_k=args.search_top_k,
        search_candidates=args.search_candidates,
        search_rollouts=args.search_rollouts,
        adaptive_search=not args.fixed_search,
        late_search_top_k=args.late_search_top_k,
        late_search_candidates=args.late_search_candidates,
        late_search_rollouts=args.late_search_rollouts,
        hammer_search_candidates=args.hammer_search_candidates,
        hammer_search_rollouts=args.hammer_search_rollouts,
        strategy_gate_strength=args.strategy_gate_strength,
        search_seed=args.search_seed,
        show_msg=args.show_msg,
    )
    robot.recv_forever()


if __name__ == "__main__":
    main()
