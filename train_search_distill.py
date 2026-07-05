# -*- coding: utf-8 -*-
"""Train a tactic policy by distilling Monte Carlo search decisions."""

from __future__ import annotations

import argparse
import json
import math
import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from fast_curling_env import FastCurlingEnv
from tactic_dqn_robot import ACTIONS, STATE_DIM, Shot, make_state_vector


ROOT = Path(__file__).resolve().parent
ROLLOUT_SHOTS: List[Tuple[str, Shot]] = [
    ("draw_center", (3.0, 0.0, 0.0)),
    ("guard_left", (2.8, -0.7, 0.0)),
    ("guard_right", (2.8, 0.7, 0.0)),
    ("curl_left", (3.0, -0.55, 3.14)),
    ("curl_right", (3.0, 0.55, -3.14)),
    ("fast_center", (4.4, 0.0, 0.0)),
    ("fast_left", (4.4, -0.45, 0.0)),
    ("fast_right", (4.4, 0.45, 0.0)),
]


def softmax_np(values: Sequence[float], temperature: float = 0.7) -> np.ndarray:
    arr = np.array(values, dtype=np.float32) / max(temperature, 1e-6)
    arr = arr - np.max(arr)
    probs = np.exp(arr)
    total = float(np.sum(probs))
    if total <= 0 or not np.isfinite(total):
        return np.ones_like(arr) / len(arr)
    return probs / total


def legal_options(env: FastCurlingEnv) -> List[Optional[Shot]]:
    return [action.try_shot(env.state_list(), 0, env.shot_num) for action in ACTIONS]


def legal_options_for_player(env: FastCurlingEnv, player_is_init: bool) -> List[Optional[Shot]]:
    is_init = 0 if player_is_init else 1
    return [action.try_shot(env.state_list(), is_init, env.shot_num) for action in ACTIONS]


def valid_indices(options: Sequence[Optional[Shot]]) -> List[int]:
    return [idx for idx, shot in enumerate(options) if shot is not None]


def scripted_index(env: FastCurlingEnv, options: Sequence[Optional[Shot]]) -> int:
    score = env.end_score()
    if score < 0:
        priorities = [
            "take_out",
            "hit_roll",
            "push_in",
            "push_in_14",
            "double_hit_gote",
            "clear",
            "draw_center",
            "curl_left",
            "curl_right",
        ]
    elif score > 0:
        priorities = [
            "guard_left",
            "guard_right",
            "defense",
            "freeze",
            "occupy",
            "draw_center",
            "curl_left",
            "curl_right",
        ]
    else:
        priorities = [
            "draw_center",
            "occupy",
            "curl_left",
            "curl_right",
            "guard_left",
            "guard_right",
            "take_out",
        ]
    name_to_idx = {action.name: idx for idx, action in enumerate(ACTIONS)}
    for name in priorities:
        idx = name_to_idx[name]
        if options[idx] is not None:
            return idx
    valid = valid_indices(options)
    return valid[0] if valid else 0


def score_for_player(env: FastCurlingEnv, player_is_init: bool) -> int:
    score = env.end_score()
    return score if player_is_init else -score


def is_our_turn(shot_num: int, player_is_init: bool) -> bool:
    return (shot_num % 2 == 0) == player_is_init


def play_controlled_shot(env: FastCurlingEnv, shot: Sequence[float]) -> None:
    if env.shot_num >= 16:
        return
    env.place_stone(env.shot_num, shot)
    env.shot_num += 1


def play_uncontrolled_shot(env: FastCurlingEnv) -> None:
    if env.shot_num >= 16:
        return
    env.place_stone(env.shot_num, env.choose_opponent_shot())
    env.shot_num += 1


def scripted_index_for_player(
    env: FastCurlingEnv,
    options: Sequence[Optional[Shot]],
    player_is_init: bool,
) -> int:
    score = score_for_player(env, player_is_init)
    if score < 0:
        priorities = [
            "take_out",
            "hit_roll",
            "push_in",
            "push_in_14",
            "double_hit_gote",
            "clear",
            "draw_center",
            "curl_left",
            "curl_right",
        ]
    elif score > 0:
        priorities = [
            "guard_left",
            "guard_right",
            "defense",
            "freeze",
            "occupy",
            "draw_center",
            "curl_left",
            "curl_right",
        ]
    else:
        priorities = [
            "draw_center",
            "occupy",
            "curl_left",
            "curl_right",
            "guard_left",
            "guard_right",
            "take_out",
        ]
    name_to_idx = {action.name: idx for idx, action in enumerate(ACTIONS)}
    for name in priorities:
        idx = name_to_idx[name]
        if options[idx] is not None:
            return idx
    valid = valid_indices(options)
    return valid[0] if valid else 0


def rollout_shot(env: FastCurlingEnv, rng: random.Random) -> Shot:
    # Cheap rollout policy: no expensive tactic-library calls inside simulations.
    # This keeps root search useful without making every rollout a full strategy search.
    score = env.end_score()
    if rng.random() < 0.15:
        return rng.choice(ROLLOUT_SHOTS)[1]
    if score < 0:
        choices = [("fast_center", (4.4, 0.0, 0.0)), ("fast_left", (4.4, -0.45, 0.0)), ("fast_right", (4.4, 0.45, 0.0))]
    elif score > 0:
        choices = [("guard_left", (2.8, -0.7, 0.0)), ("guard_right", (2.8, 0.7, 0.0)), ("draw_center", (3.0, 0.0, 0.0))]
    else:
        choices = [("draw_center", (3.0, 0.0, 0.0)), ("curl_left", (3.0, -0.55, 3.14)), ("curl_right", (3.0, 0.55, -3.14))]
    return rng.choice(choices)[1]


def rollout_shot_for_player(env: FastCurlingEnv, rng: random.Random, player_is_init: bool) -> Shot:
    # Same cheap policy as rollout_shot, but evaluated from the controlled side.
    score = score_for_player(env, player_is_init)
    if rng.random() < 0.15:
        return rng.choice(ROLLOUT_SHOTS)[1]
    if score < 0:
        choices = [("fast_center", (4.4, 0.0, 0.0)), ("fast_left", (4.4, -0.45, 0.0)), ("fast_right", (4.4, 0.45, 0.0))]
    elif score > 0:
        choices = [("guard_left", (2.8, -0.7, 0.0)), ("guard_right", (2.8, 0.7, 0.0)), ("draw_center", (3.0, 0.0, 0.0))]
    else:
        choices = [("draw_center", (3.0, 0.0, 0.0)), ("curl_left", (3.0, -0.55, 3.14)), ("curl_right", (3.0, 0.55, -3.14))]
    return rng.choice(choices)[1]


def finish_rollout(env: FastCurlingEnv, rng: random.Random) -> int:
    while env.shot_num < 16:
        if env.shot_num % 2 == 1:
            env.step()
        else:
            env.step(rollout_shot(env, rng))
    return env.end_score()


def finish_rollout_for_player(env: FastCurlingEnv, rng: random.Random, player_is_init: bool) -> int:
    while env.shot_num < 16:
        if is_our_turn(env.shot_num, player_is_init):
            play_controlled_shot(env, rollout_shot_for_player(env, rng, player_is_init))
        else:
            play_uncontrolled_shot(env)
    return score_for_player(env, player_is_init)


def search_action(
    env: FastCurlingEnv,
    rollouts_per_action: int,
    rng: random.Random,
) -> Tuple[int, np.ndarray, np.ndarray]:
    options = legal_options(env)
    valid = valid_indices(options)
    if not valid:
        probs = np.zeros(len(ACTIONS), dtype=np.float32)
        probs[0] = 1.0
        values = np.full(len(ACTIONS), -99.0, dtype=np.float32)
        return 0, probs, values

    values = np.full(len(ACTIONS), -99.0, dtype=np.float32)
    for idx in valid:
        scores = []
        shot = options[idx]
        assert shot is not None
        for _ in range(rollouts_per_action):
            sim = env.clone(seed=rng.randint(1, 2_000_000_000))
            sim.step(shot)
            scores.append(finish_rollout(sim, rng))
        values[idx] = float(np.mean(scores))

    valid_values = [values[idx] for idx in valid]
    valid_probs = softmax_np(valid_values, temperature=0.55)
    probs = np.zeros(len(ACTIONS), dtype=np.float32)
    for idx, prob in zip(valid, valid_probs):
        probs[idx] = prob
    best_idx = valid[int(np.argmax(valid_values))]
    return best_idx, probs, values


def search_action_for_player(
    env: FastCurlingEnv,
    rollouts_per_action: int,
    rng: random.Random,
    player_is_init: bool,
) -> Tuple[int, np.ndarray, np.ndarray]:
    options = legal_options_for_player(env, player_is_init)
    valid = valid_indices(options)
    if not valid:
        probs = np.zeros(len(ACTIONS), dtype=np.float32)
        probs[0] = 1.0
        values = np.full(len(ACTIONS), -99.0, dtype=np.float32)
        return 0, probs, values

    values = np.full(len(ACTIONS), -99.0, dtype=np.float32)
    for idx in valid:
        scores = []
        shot = options[idx]
        assert shot is not None
        for _ in range(rollouts_per_action):
            sim = env.clone(seed=rng.randint(1, 2_000_000_000))
            play_controlled_shot(sim, shot)
            scores.append(finish_rollout_for_player(sim, rng, player_is_init))
        values[idx] = float(np.mean(scores))

    valid_values = [values[idx] for idx in valid]
    valid_probs = softmax_np(valid_values, temperature=0.55)
    probs = np.zeros(len(ACTIONS), dtype=np.float32)
    for idx, prob in zip(valid, valid_probs):
        probs[idx] = prob
    best_idx = valid[int(np.argmax(valid_values))]
    return best_idx, probs, values


@dataclass
class Sample:
    state: np.ndarray
    mask: np.ndarray
    policy: np.ndarray
    action: int
    value: float = 0.0


def generate_dataset(
    games: int,
    rollouts_per_action: int,
    seed: int,
    player_is_init: bool = True,
    progress_every: int = 25,
) -> List[Sample]:
    rng = random.Random(seed)
    samples: List[Sample] = []
    started = time.time()
    for game in range(1, games + 1):
        env = FastCurlingEnv(seed=rng.randint(1, 2_000_000_000))
        game_samples: List[Sample] = []
        while env.shot_num < 16:
            if not is_our_turn(env.shot_num, player_is_init):
                play_uncontrolled_shot(env)
                continue

            options = legal_options_for_player(env, player_is_init)
            valid = valid_indices(options)
            state = make_state_vector(env.position(), env.shot_num, 0, 1, player_is_init, 0)
            mask = np.zeros(len(ACTIONS), dtype=np.float32)
            mask[valid] = 1.0
            action, probs, _ = search_action_for_player(env, rollouts_per_action, rng, player_is_init)
            game_samples.append(Sample(state=state, mask=mask, policy=probs, action=action))
            play_controlled_shot(env, options[action] or (3.0, 0.0, 0.0))

        final_score = float(score_for_player(env, player_is_init))
        for sample in game_samples:
            sample.value = final_score / 8.0
        samples.extend(game_samples)
        if progress_every and game % progress_every == 0:
            elapsed = time.time() - started
            print(f"generated games={game}/{games} samples={len(samples)} elapsed={elapsed:.1f}s", flush=True)
    return samples


class PolicyValueNet(nn.Module):
    def __init__(self, state_dim: int = STATE_DIM, action_dim: int = len(ACTIONS)):
        super().__init__()
        self.fc1 = nn.Linear(state_dim, 256)
        self.fc2 = nn.Linear(256, 256)
        self.policy = nn.Linear(256, action_dim)
        self.value = nn.Linear(256, 1)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.policy(x), torch.tanh(self.value(x))


def train_model(
    samples: List[Sample],
    model_file: Path,
    epochs: int,
    batch_size: int,
    lr: float,
    seed: int,
    player: str = "first",
) -> Dict[str, float]:
    torch.manual_seed(seed)
    np.random.seed(seed)
    model = PolicyValueNet()
    optim = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)

    states = torch.tensor(np.array([s.state for s in samples]), dtype=torch.float32)
    masks = torch.tensor(np.array([s.mask for s in samples]), dtype=torch.float32)
    policies = torch.tensor(np.array([s.policy for s in samples]), dtype=torch.float32)
    actions = torch.tensor([s.action for s in samples], dtype=torch.long)
    values = torch.tensor([[s.value] for s in samples], dtype=torch.float32)

    n = len(samples)
    indices = np.arange(n)
    final_metrics: Dict[str, float] = {}
    for epoch in range(1, epochs + 1):
        np.random.shuffle(indices)
        total_loss = 0.0
        total_acc = 0
        for start in range(0, n, batch_size):
            batch_idx = indices[start : start + batch_size]
            b_states = states[batch_idx]
            b_masks = masks[batch_idx]
            b_policies = policies[batch_idx]
            b_actions = actions[batch_idx]
            b_values = values[batch_idx]

            logits, pred_values = model(b_states)
            masked_logits = logits.masked_fill(b_masks <= 0, -1e9)
            log_probs = F.log_softmax(masked_logits, dim=1)
            policy_loss = -(b_policies * log_probs).sum(dim=1).mean()
            action_loss = F.cross_entropy(masked_logits, b_actions)
            value_loss = F.mse_loss(pred_values, b_values)
            loss = policy_loss + 0.35 * action_loss + 0.5 * value_loss

            optim.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 4.0)
            optim.step()

            total_loss += float(loss.item()) * len(batch_idx)
            total_acc += int((torch.argmax(masked_logits, dim=1) == b_actions).sum().item())

        final_metrics = {
            "loss": total_loss / n,
            "action_acc": total_acc / n,
        }
        print(
            f"epoch={epoch}/{epochs} loss={final_metrics['loss']:.4f} "
            f"action_acc={final_metrics['action_acc']:.3f}",
            flush=True,
        )

    model_file.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "model_state": model.state_dict(),
            "action_names": [a.name for a in ACTIONS],
            "state_dim": STATE_DIM,
            "player": player,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        },
        model_file,
    )
    return final_metrics


def choose_model_action(model: PolicyValueNet, env: FastCurlingEnv) -> int:
    options = legal_options(env)
    valid = valid_indices(options)
    if not valid:
        return 0
    state = torch.tensor(
        make_state_vector(env.position(), env.shot_num, 0, 1, True, 0),
        dtype=torch.float32,
    ).unsqueeze(0)
    with torch.no_grad():
        logits, _ = model(state)
    scores = logits.squeeze(0).numpy()
    masked = np.full_like(scores, -1e9)
    masked[valid] = scores[valid]
    return int(np.argmax(masked))


def choose_model_action_for_player(model: PolicyValueNet, env: FastCurlingEnv, player_is_init: bool) -> int:
    options = legal_options_for_player(env, player_is_init)
    valid = valid_indices(options)
    if not valid:
        return 0
    state = torch.tensor(
        make_state_vector(env.position(), env.shot_num, 0, 1, player_is_init, 0),
        dtype=torch.float32,
    ).unsqueeze(0)
    with torch.no_grad():
        logits, _ = model(state)
    scores = logits.squeeze(0).numpy()
    masked = np.full_like(scores, -1e9)
    masked[valid] = scores[valid]
    return int(np.argmax(masked))


def load_model(model_file: Path) -> PolicyValueNet:
    payload = torch.load(model_file, map_location="cpu")
    model = PolicyValueNet()
    model.load_state_dict(payload["model_state"])
    model.eval()
    return model


def evaluate_policy(policy: str, games: int, seed: int, model_file: Optional[Path] = None) -> Dict[str, float]:
    rng = random.Random(seed)
    model = load_model(model_file) if policy == "model" and model_file else None
    scores: List[int] = []
    for _ in range(games):
        env = FastCurlingEnv(seed=rng.randint(1, 2_000_000_000))
        while env.shot_num < 16:
            if env.shot_num % 2 == 1:
                env.step()
            else:
                options = legal_options(env)
                valid = valid_indices(options)
                if policy == "random":
                    idx = rng.choice(valid) if valid else 0
                elif policy == "scripted":
                    idx = scripted_index(env, options)
                elif policy == "model":
                    assert model is not None
                    idx = choose_model_action(model, env)
                elif policy == "search":
                    idx, _, _ = search_action(env, rollouts_per_action=4, rng=rng)
                else:
                    raise ValueError(policy)
                env.step(options[idx] or (3.0, 0.0, 0.0))
        scores.append(env.end_score())
    return {
        "games": games,
        "avg_score": float(np.mean(scores)),
        "win_rate": float(np.mean([s > 0 for s in scores])),
        "loss_rate": float(np.mean([s < 0 for s in scores])),
        "min_score": float(np.min(scores)),
        "max_score": float(np.max(scores)),
    }


def evaluate_policy_for_player(
    policy: str,
    games: int,
    seed: int,
    player_is_init: bool,
    model_file: Optional[Path] = None,
) -> Dict[str, float]:
    rng = random.Random(seed)
    model = load_model(model_file) if policy == "model" and model_file else None
    scores: List[int] = []
    for _ in range(games):
        env = FastCurlingEnv(seed=rng.randint(1, 2_000_000_000))
        while env.shot_num < 16:
            if not is_our_turn(env.shot_num, player_is_init):
                play_uncontrolled_shot(env)
                continue

            options = legal_options_for_player(env, player_is_init)
            valid = valid_indices(options)
            if policy == "random":
                idx = rng.choice(valid) if valid else 0
            elif policy == "scripted":
                idx = scripted_index_for_player(env, options, player_is_init)
            elif policy == "model":
                assert model is not None
                idx = choose_model_action_for_player(model, env, player_is_init)
            elif policy == "search":
                idx, _, _ = search_action_for_player(env, rollouts_per_action=4, rng=rng, player_is_init=player_is_init)
            else:
                raise ValueError(policy)
            play_controlled_shot(env, options[idx] or (3.0, 0.0, 0.0))
        scores.append(score_for_player(env, player_is_init))
    return {
        "games": games,
        "player_is_init": player_is_init,
        "avg_score": float(np.mean(scores)),
        "win_rate": float(np.mean([s > 0 for s in scores])),
        "loss_rate": float(np.mean([s < 0 for s in scores])),
        "min_score": float(np.min(scores)),
        "max_score": float(np.max(scores)),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Search-distilled tactic policy trainer")
    parser.add_argument("--games", type=int, default=600)
    parser.add_argument("--rollouts", type=int, default=5)
    parser.add_argument("--epochs", type=int, default=24)
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--eval-games", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260705)
    parser.add_argument("--player", choices=["first", "second"], default="first")
    parser.add_argument("--model-file", default="model/search_distill_tactic_policy.pt")
    parser.add_argument("--report-file", default="log/search_distill_report.json")
    args = parser.parse_args()

    started = time.time()
    player_is_init = args.player == "first"
    samples = generate_dataset(args.games, args.rollouts, args.seed, player_is_init=player_is_init)
    model_file = Path(args.model_file)
    metrics = train_model(samples, model_file, args.epochs, args.batch_size, args.lr, args.seed, player=args.player)

    report = {
        "config": vars(args),
        "player_is_init": player_is_init,
        "samples": len(samples),
        "training_metrics": metrics,
        "evaluation": {
            "random": evaluate_policy_for_player("random", args.eval_games, args.seed + 1, player_is_init),
            "scripted": evaluate_policy_for_player("scripted", args.eval_games, args.seed + 2, player_is_init),
            "model": evaluate_policy_for_player("model", args.eval_games, args.seed + 3, player_is_init, model_file),
            "search_rollouts4": evaluate_policy_for_player(
                "search",
                max(200, args.eval_games // 5),
                args.seed + 4,
                player_is_init,
            ),
        },
        "elapsed_sec": time.time() - started,
    }
    Path(args.report_file).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report_file).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
