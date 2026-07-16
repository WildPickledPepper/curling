# -*- coding: utf-8 -*-
"""DQN robot that chooses high-level curling tactics instead of raw shots."""

from __future__ import annotations

import argparse
import contextlib
import io
import math
import os
import random
import sys
import time
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Deque, Iterable, List, Optional, Sequence, Tuple

import numpy as np

from AIRobot import AIRobot


ROOT = Path(__file__).resolve().parent
TACTICS_DIR = ROOT / "tacticslib"
if str(TACTICS_DIR) not in sys.path:
    sys.path.insert(0, str(TACTICS_DIR))

import strategy_library as sl  # noqa: E402


HOUSE_X = 2.375
HOUSE_Y = 4.88
HOUSE_R = 1.830
STONE_R = 0.145
STATE_DIM = 88
FEATURE_DIM = STATE_DIM * 2 + 1


Shot = Tuple[float, float, float]


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def get_dist(x: float, y: float) -> float:
    return math.sqrt((x - HOUSE_X) ** 2 + (y - HOUSE_Y) ** 2)


def is_live_stone(x: float, y: float) -> bool:
    return bool(abs(x) > 1e-9 or abs(y) > 1e-9)


def get_infostate(position: Sequence[float]) -> Tuple[int, np.ndarray]:
    init = np.empty([8], dtype=float)
    gote = np.empty([8], dtype=float)
    both = np.empty([16], dtype=float)
    for i in range(8):
        init[i] = get_dist(position[4 * i], position[4 * i + 1])
        both[2 * i] = init[i]
        gote[i] = get_dist(position[4 * i + 2], position[4 * i + 3])
        both[2 * i + 1] = gote[i]

    if min(init) <= min(gote):
        win = 0
        d_std = min(gote)
    else:
        win = 1
        d_std = min(init)

    infostate = []
    init_score = 0
    for i in range(16):
        x = position[2 * i]
        y = position[2 * i + 1]
        dist = both[i]
        sn = i % 2 + 1
        if dist < d_std and dist < (HOUSE_R + STONE_R) and (i % 2) == win:
            valid = 1
            init_score += 1 if win == 0 else -1
        else:
            valid = 0
        if is_live_stone(x, y):
            infostate.append([x, y, dist, sn, valid])

    infostate = sorted(infostate, key=lambda item: item[2])
    while len(infostate) < 16:
        infostate.append([0, 0, 0, 0, 0])
    return init_score, np.array(infostate, dtype=np.float32).flatten()


def current_score_for_player(position: Sequence[float], player_is_init: bool) -> int:
    init_score, _ = get_infostate(position)
    return init_score if player_is_init else -init_score


def nearest_quality(position: Sequence[float], player_is_init: bool) -> Tuple[float, float, int]:
    own_best = HOUSE_R + STONE_R
    enemy_best = HOUSE_R + STONE_R
    stones_in_play = 0
    own_parity = 0 if player_is_init else 1
    for idx in range(16):
        x = position[2 * idx]
        y = position[2 * idx + 1]
        if not is_live_stone(x, y):
            continue
        stones_in_play += 1
        dist = min(get_dist(x, y), HOUSE_R + STONE_R)
        if idx % 2 == own_parity:
            own_best = min(own_best, dist)
        else:
            enemy_best = min(enemy_best, dist)
    own_quality = 1.0 - own_best / (HOUSE_R + STONE_R)
    enemy_quality = 1.0 - enemy_best / (HOUSE_R + STONE_R)
    return own_quality, enemy_quality, stones_in_play


def make_state_vector(
    position: Sequence[float],
    shot_num: int,
    round_num: int,
    round_total: int,
    player_is_init: bool,
    next_shot: int,
) -> np.ndarray:
    init_score, info = get_infostate(position)
    perspective_score = init_score if player_is_init else -init_score
    own_quality, enemy_quality, stones_in_play = nearest_quality(position, player_is_init)
    my_shot_idx = (shot_num // 2) + 1 if player_is_init else ((shot_num - 1) // 2) + 1
    round_scale = max(1, round_total if round_total > 0 else 1)
    extras = np.array(
        [
            shot_num / 15.0,
            clamp(my_shot_idx, 0, 8) / 8.0,
            1.0 if player_is_init else 0.0,
            float(next_shot),
            clamp(perspective_score, -8, 8) / 8.0,
            own_quality,
            enemy_quality,
            stones_in_play / 16.0 + min(round_num, round_scale) / (100.0 * round_scale),
        ],
        dtype=np.float32,
    )
    return np.concatenate([info, extras]).astype(np.float32)


def shaped_reward(
    before_position: Sequence[float],
    after_position: Sequence[float],
    player_is_init: bool,
    final_score: Optional[int] = None,
) -> float:
    before_score = current_score_for_player(before_position, player_is_init)
    after_score = current_score_for_player(after_position, player_is_init)
    before_own, before_enemy, _ = nearest_quality(before_position, player_is_init)
    after_own, after_enemy, _ = nearest_quality(after_position, player_is_init)

    reward = 2.5 * (after_score - before_score)
    reward += 0.8 * (after_own - before_own)
    reward += 0.8 * (before_enemy - after_enemy)
    if final_score is not None:
        reward += 5.0 * final_score
    return float(clamp(reward, -20.0, 20.0))


def sanitize_shot(result: object) -> Optional[Shot]:
    if result is None or result == 0:
        return None
    try:
        v0, h0, w0 = result  # type: ignore[misc]
        shot = (
            clamp(float(v0), 0.0, 6.0),
            clamp(float(h0), -2.23, 2.23),
            clamp(float(w0), -15.7, 15.7),
        )
    except (TypeError, ValueError):
        return None
    if any(math.isnan(value) or math.isinf(value) for value in shot):
        return None
    return shot


@dataclass(frozen=True)
class TacticAction:
    name: str
    func: Callable[[List[List[float]], int, int], Optional[Shot]]

    def try_shot(self, state_list: List[List[float]], is_init: int, shot_num: int) -> Optional[Shot]:
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                return sanitize_shot(self.func(state_list, is_init, shot_num))
        except Exception:
            return None


def fixed_shot(v0: float, h0: float, w0: float = 0.0) -> Callable[[List[List[float]], int, int], Optional[Shot]]:
    def _inner(_: List[List[float]], __: int, ___: int) -> Optional[Shot]:
        return (v0, h0, w0)

    return _inner


def tactic_func(func: Callable[..., object]) -> Callable[[List[List[float]], int, int], Optional[Shot]]:
    def _inner(state_list: List[List[float]], is_init: int, shot_num: int) -> Optional[Shot]:
        return sanitize_shot(func(state_list, is_init, shot_num))

    return _inner


ACTIONS: List[TacticAction] = [
    TacticAction("draw_center", fixed_shot(3.0, 0.0, 0.0)),
    TacticAction("guard_left", fixed_shot(2.8, -0.7, 0.0)),
    TacticAction("guard_right", fixed_shot(2.8, 0.7, 0.0)),
    TacticAction("curl_left", fixed_shot(3.0, -0.55, 3.14)),
    TacticAction("curl_right", fixed_shot(3.0, 0.55, -3.14)),
    TacticAction("occupy", tactic_func(sl.occupy)),
    TacticAction("take_out", tactic_func(sl.take_out)),
    TacticAction("hit_roll", tactic_func(sl.hit_roll)),
    TacticAction("defense", tactic_func(sl.defense)),
    TacticAction("freeze", tactic_func(sl.freeze)),
    TacticAction("clear", tactic_func(sl.clear)),
    TacticAction("middle_in_center", tactic_func(sl.middle_in_center)),
    TacticAction("push_in", tactic_func(sl.push_in)),
    TacticAction("push_in_14", tactic_func(sl.push_in_14)),
    TacticAction("double_hit_gote", tactic_func(sl.double_hit_gote)),
    TacticAction("defense_push_in", tactic_func(sl.defense_push_in)),
]


def featurize(state: np.ndarray) -> np.ndarray:
    state = state.astype(np.float32)
    return np.concatenate([state, state * state, np.array([1.0], dtype=np.float32)])


class ReplayBuffer:
    def __init__(self, capacity: int):
        self.buffer: Deque[Tuple[np.ndarray, int, float, np.ndarray, bool]] = deque(maxlen=capacity)

    def push(self, state: np.ndarray, action: int, reward: float, next_state: np.ndarray, done: bool) -> None:
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            np.array(states, dtype=np.float32),
            np.array(actions, dtype=np.int64),
            np.array(rewards, dtype=np.float32),
            np.array(next_states, dtype=np.float32),
            np.array(dones, dtype=np.float32),
        )

    def __len__(self) -> int:
        return len(self.buffer)


class TacticDQN:
    def __init__(
        self,
        model_file: Path,
        action_dim: int,
        train: bool = True,
        epsilon_start: float = 0.45,
        epsilon_end: float = 0.05,
        epsilon_decay: int = 2500,
        gamma: float = 0.92,
        lr: float = 0.002,
        batch_size: int = 64,
        memory_capacity: int = 20000,
        target_update: int = 200,
    ):
        self.model_file = model_file
        self.train = train
        self.action_dim = action_dim
        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.gamma = gamma
        self.lr = lr
        self.batch_size = batch_size
        self.target_update = target_update
        self.steps = 0
        self.learn_steps = 0
        self.last_loss: Optional[float] = None

        self.memory = ReplayBuffer(memory_capacity)
        scale = 0.02
        self.weights = np.random.normal(0.0, scale, size=(FEATURE_DIM, action_dim)).astype(np.float32)
        self.target_weights = self.weights.copy()
        if model_file.exists():
            with np.load(model_file, allow_pickle=False) as data:
                self.weights = data["weights"].astype(np.float32)
                self.target_weights = data.get("target_weights", self.weights).astype(np.float32)
                self.steps = int(data.get("steps", 0))
                self.learn_steps = int(data.get("learn_steps", 0))
        self.target_weights = self.weights.copy()

    def epsilon(self) -> float:
        if not self.train:
            return 0.0
        fraction = min(1.0, self.steps / max(1, self.epsilon_decay))
        return self.epsilon_start + fraction * (self.epsilon_end - self.epsilon_start)

    def choose_action(self, state: np.ndarray, valid_actions: Sequence[int]) -> int:
        self.steps += 1
        if not valid_actions:
            return 0
        if random.random() < self.epsilon():
            return random.choice(list(valid_actions))
        q_values = featurize(state) @ self.weights
        masked = np.full_like(q_values, -1e9)
        masked[list(valid_actions)] = q_values[list(valid_actions)]
        return int(np.argmax(masked))

    def remember(self, state: np.ndarray, action: int, reward: float, next_state: np.ndarray, done: bool) -> None:
        if self.train:
            self.memory.push(state, action, reward, next_state, done)

    def learn(self) -> Optional[float]:
        if not self.train or len(self.memory) < self.batch_size:
            return None
        states, actions, rewards, next_states, dones = self.memory.sample(self.batch_size)
        phis = np.array([featurize(state) for state in states], dtype=np.float32)
        next_phis = np.array([featurize(state) for state in next_states], dtype=np.float32)
        q_eval = np.sum(phis * self.weights[:, actions].T, axis=1)
        next_q = np.max(next_phis @ self.target_weights, axis=1)
        q_target = rewards + self.gamma * next_q * (1.0 - dones)
        errors = np.clip(q_eval - q_target, -10.0, 10.0)
        loss = float(np.mean(errors * errors))
        for idx, action in enumerate(actions):
            self.weights[:, action] -= self.lr * errors[idx] * phis[idx] / len(actions)
        self.learn_steps += 1
        if self.learn_steps % self.target_update == 0:
            self.target_weights = self.weights.copy()
        self.last_loss = loss
        return self.last_loss

    def save(self) -> None:
        self.model_file.parent.mkdir(parents=True, exist_ok=True)
        with self.model_file.open("wb") as fh:
            np.savez(
                fh,
                weights=self.weights,
                target_weights=self.target_weights,
                steps=np.array(self.steps),
                learn_steps=np.array(self.learn_steps),
            )


class TacticDQNRobot(AIRobot):
    def __init__(
        self,
        key: str,
        name: str,
        host: str,
        port: int,
        model_file: str = "model/tactic_dqn.pth",
        log_file: Optional[str] = None,
        train: bool = True,
        max_rounds: int = 0,
        save_every: int = 1,
        show_msg: bool = False,
        brain: Optional[TacticDQN] = None,
    ):
        super().__init__(key, name, host, port, show_msg=show_msg)
        self.brain = brain or TacticDQN(Path(model_file), action_dim=len(ACTIONS), train=train)
        self.log_file = Path(log_file or f"log/tactic_dqn_{time.strftime('%y%m%d_%H%M%S')}.log")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.max_rounds = max_rounds
        self.save_every = save_every
        self.pending: Optional[Tuple[np.ndarray, List[float], int, bool]] = None
        self.last_transition: Optional[Tuple[np.ndarray, int, np.ndarray]] = None
        self.last_action_name = ""
        self.last_reward = 0.0

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

    def state_vector(self) -> np.ndarray:
        return make_state_vector(
            self.position,
            self.shot_num,
            self.round_num,
            getattr(self, "round_total", 1),
            self.player_is_init,
            getattr(self, "next_shot", 0),
        )

    def finish_pending(self, done: bool = False, final_score: Optional[int] = None) -> None:
        if self.pending is None:
            return
        prev_state, prev_position, action_idx, player_is_init = self.pending
        next_state = self.state_vector()
        reward = shaped_reward(prev_position, self.position, player_is_init, final_score)
        self.brain.remember(prev_state, action_idx, reward, next_state, done)
        self.last_transition = (prev_state, action_idx, next_state)
        loss = self.brain.learn()
        self.last_reward = reward
        if loss is not None:
            self.brain.last_loss = loss
        self.pending = None

    def add_terminal_bonus(self, final_score: int) -> None:
        if self.pending is not None:
            self.finish_pending(done=True, final_score=final_score)
            return
        if self.last_transition is None:
            return
        prev_state, action_idx, next_state = self.last_transition
        reward = float(clamp(5.0 * final_score, -20.0, 20.0))
        self.brain.remember(prev_state, action_idx, reward, next_state, True)
        loss = self.brain.learn()
        self.last_reward = reward
        if loss is not None:
            self.brain.last_loss = loss

    def get_bestshot(self) -> str:
        state = self.state_vector()
        options = self.build_action_options()
        valid_actions = [idx for idx, shot in enumerate(options) if shot is not None]
        action_idx = self.brain.choose_action(state, valid_actions)
        shot = options[action_idx] if action_idx < len(options) else None
        if shot is None:
            action_idx = 0
            shot = (3.0, 0.0, 0.0)
        self.last_action_name = ACTIONS[action_idx].name
        self.pending = (state, list(self.position), action_idx, self.player_is_init)
        v0, h0, w0 = shot
        print(
            f"tactic={self.last_action_name} eps={self.brain.epsilon():.3f} "
            f"shot=({v0:.3f},{h0:.3f},{w0:.3f})",
            flush=True,
        )
        return f"BESTSHOT {v0} {h0} {w0}"

    def log_round(self, result: str) -> None:
        with self.log_file.open("a", encoding="utf-8") as fh:
            fh.write(
                " ".join(
                    [
                        f"round={self.round_num}",
                        f"score={getattr(self, 'score', 0)}",
                        f"result={result}",
                        f"epsilon={self.brain.epsilon():.4f}",
                        f"reward={self.last_reward:.4f}",
                        f"loss={self.brain.last_loss if self.brain.last_loss is not None else 'NA'}",
                    ]
                )
                + "\n"
            )

    def recv_forever(self) -> None:
        ret_null_time = 0
        self.on_line = True
        time0 = time.time()

        while self.on_line:
            msg_code, msg_list = self.recv_msg()
            if msg_code == "":
                ret_null_time += 1
            if ret_null_time == 5:
                break

            if msg_code == "CONNECTNAME":
                self.player_is_init = msg_list[0] == "Player1"
                print("玩家1，首局先手" if self.player_is_init else "玩家2，首局后手", flush=True)
            elif msg_code == "ISREADY":
                self.send_msg("READYOK")
                time.sleep(0.2)
                self.send_msg("NAME " + self.name)
                print(self.name + " 准备完毕！", flush=True)
            elif msg_code == "NEWGAME":
                time0 = time.time()
            elif msg_code == "SETSTATE":
                self.finish_pending(done=False)
                self.recv_setstate(msg_list)
            elif msg_code == "POSITION":
                for n in range(32):
                    self.position[n] = float(msg_list[n])
            elif msg_code == "GO":
                self.send_msg(self.get_bestshot())
            elif msg_code == "MOTIONINFO":
                for n in range(5):
                    self.motioninfo[n] = float(msg_list[n])
            elif msg_code == "CENTERLINE_VIOLATION":
                self.send_msg("CENTERLINE_CHOICE RESET")
            elif msg_code == "SCORE":
                self.score = int(msg_list[0])
                perspective_score = self.score if self.player_is_init else -self.score
                self.add_terminal_bonus(perspective_score)
                elapsed = time.time() - time0
                self.round_num += 1
                print(
                    f"{time.strftime('[%Y/%m/%d %H:%M:%S]')} {self.name}局耗时{elapsed:.1f}秒 "
                    f"score={self.score} reward={self.last_reward:.3f}",
                    flush=True,
                )
                self.log_round("score")
                if self.round_num % self.save_every == 0:
                    self.brain.save()
                    print("============= TacticDQN Checkpoint Saved =============", flush=True)
                if self.max_rounds and self.round_num >= self.max_rounds:
                    self.on_line = False
            elif msg_code == "GAMEOVER":
                result = msg_list[0] if msg_list else "UNKNOWN"
                print("GAMEOVER " + result, flush=True)

        self.brain.save()
        self.ai_sock.close()
        print("已关闭socket连接", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Tactic-level DQN curling robot")
    parser.add_argument("--key", default="local-test:0")
    parser.add_argument("-H", "--host", default="127.0.0.1")
    parser.add_argument("-p", "--port", type=int, default=7788)
    parser.add_argument("--name", default="TacticDQN")
    parser.add_argument("--model-file", default="model/tactic_dqn.pth")
    parser.add_argument("--log-file", default=None)
    parser.add_argument("--eval", action="store_true", help="disable exploration and learning")
    parser.add_argument("--max-rounds", type=int, default=0)
    parser.add_argument("--show-msg", action="store_true")
    args = parser.parse_args()

    robot = TacticDQNRobot(
        key=args.key,
        name=args.name,
        host=args.host,
        port=args.port,
        model_file=args.model_file,
        log_file=args.log_file,
        train=not args.eval,
        max_rounds=args.max_rounds,
        show_msg=args.show_msg,
    )
    robot.recv_forever()


if __name__ == "__main__":
    main()
