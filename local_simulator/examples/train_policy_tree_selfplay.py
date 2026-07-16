#!/usr/bin/env python3
"""最小策略树自对弈训练：让两方在严格 PhysX 模拟器中完成一局 16 手。

这不是“固定局面找一手参数”的搜索。每一手策略都会看到当前整盘壶的
位置、当前壶次和暂时得分，再从课程中的基础战术中选择一个：左/右守壶、
进营、清壶或出界。整局结束后，赢家使用过的策略分支会被强化，输家会被
削弱；下一局便会据此改变选择概率。

它刻意保持简单，采用课程第 4 课中的基础战术，而不是声称已经训练出了
可交付的 PPO 模型。用途是展示“严格模拟器怎样接进完整博弈训练闭环”。

从仓库根目录运行：
    python local_simulator\\examples\\train_policy_tree_selfplay.py --games 3

Python 依赖只有严格模拟器已有的 NumPy / pyphysx；不需要 Unity 或 PyTorch。
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


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from local_simulator.runtime_loader import install_bundled_pyphysx


# 与 notebooks/08 的 get_infostate() 使用同一套大本营几何和计分规则。
HOUSE_X = 2.375
HOUSE_Y = 4.88
HOUSE_R = 1.830
STONE_R = 0.145
STONE_COUNT = 16


@dataclass(frozen=True)
class Tactic:
    """策略树的一个叶子；shot 为无目标时的默认 BESTSHOT。"""

    name: str
    shot: tuple[float, float, float]


# 课程第 4 课 InitRobot 使用了 guard_left 和 throw_out；其余是同类的
# 对称守壶、进营与简化清壶。策略树学习的是“何时选哪一个”，而不是重做
# 底层物理或把 Unity 的结果倒灌进来。
TACTICS = (
    Tactic("guard_left", (2.7, -1.0, 0.0)),
    Tactic("guard_right", (2.7, 1.0, 0.0)),
    Tactic("draw_center", (3.0, 0.0, 0.0)),
    Tactic("takeout", (4.2, 0.0, 0.0)),
    Tactic("throw_out", (6.0, -2.23, 0.0)),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--games", type=int, default=3, help="自对弈局数；演示默认 3 局")
    parser.add_argument("--seed", type=int, default=20260715, help="训练采样器随机种子")
    parser.add_argument("--learning-rate", type=float, default=0.18, help="策略树更新步长")
    parser.add_argument(
        "--model-file",
        type=Path,
        default=PROJECT_ROOT / "model" / "strict_policy_tree.json",
        help="保存策略树权重的位置",
    )
    parser.add_argument(
        "--report-file",
        type=Path,
        default=PROJECT_ROOT / "log" / "strict_policy_tree_training.json",
        help="保存每局结果的位置",
    )
    return parser.parse_args()


def stable_softmax(values: Sequence[float]) -> list[float]:
    ceiling = max(values)
    exps = [math.exp(value - ceiling) for value in values]
    total = sum(exps)
    return [value / total for value in exps]


def choose_weighted(rng: random.Random, probabilities: Sequence[float]) -> int:
    threshold = rng.random()
    cumulative = 0.0
    for index, probability in enumerate(probabilities):
        cumulative += probability
        if threshold <= cumulative:
            return index
    return len(probabilities) - 1


def distance(x: float, y: float) -> float:
    return math.hypot(x - HOUSE_X, y - HOUSE_Y)


def score_board(states: Sequence[dict[str, Any]]) -> int:
    """按课程 notebook 的规则计分：偶数索引（先手）得分为正。"""

    in_house: list[tuple[float, bool]] = []
    for index, state in enumerate(states):
        if not state["enabled"]:
            continue
        d = distance(float(state["x"]), float(state["y"]))
        if d <= HOUSE_R + STONE_R:
            in_house.append((d, index % 2 == 0))
    if not in_house:
        return 0
    in_house.sort(key=lambda item: item[0])
    first_scores = in_house[0][1]
    other_best = min(
        (d for d, is_first in in_house if is_first != first_scores),
        default=math.inf,
    )
    points = sum(1 for d, is_first in in_house if is_first == first_scores and d < other_best)
    return points if first_scores else -points


def team_score(board_score: int, team: int) -> int:
    """从当前出手方看比分；team=0 是先手，team=1 是后手。"""

    return board_score if team == 0 else -board_score


def context_key(states: Sequence[dict[str, Any]], shot_number: int, team: int) -> str:
    """一个很小但真实依赖整局局面的策略树节点。"""

    score = team_score(score_board(states), team)
    phase = "early" if shot_number < 6 else "middle" if shot_number < 12 else "late"
    score_bucket = "ahead" if score > 0 else "behind" if score < 0 else "level"
    opponent_in_house = any(
        state["enabled"]
        and index % 2 != team
        and distance(float(state["x"]), float(state["y"])) <= HOUSE_R + STONE_R
        for index, state in enumerate(states)
    )
    return f"{phase}|{score_bucket}|{'enemy_scoring' if opponent_in_house else 'open'}"


class LearnedPolicyTree:
    """以策略树节点为键的最小 REINFORCE 表；不是 PPO。"""

    def __init__(self, *, learning_rate: float) -> None:
        self.learning_rate = float(learning_rate)
        self.logits: dict[str, list[float]] = {}

    def probabilities(self, node: str) -> list[float]:
        if node not in self.logits:
            # 轻微先验：局面开放时先尝试守壶/进营；其余由对局结果修正。
            self.logits[node] = [0.0] * len(TACTICS)
        return stable_softmax(self.logits[node])

    def choose(self, rng: random.Random, node: str) -> tuple[int, list[float]]:
        probabilities = self.probabilities(node)
        return choose_weighted(rng, probabilities), probabilities

    def update(self, trajectory: Sequence[tuple[str, int, list[float], int]], final_score: int) -> None:
        """用每方最终净得分更新其选择过的策略分支。"""

        for node, action, probabilities, team in trajectory:
            # 归一化到较温和的范围，避免一局多分导致更新过猛。
            advantage = max(-1.0, min(1.0, team_score(final_score, team) / 3.0))
            weights = self.logits[node]
            for index, probability in enumerate(probabilities):
                indicator = 1.0 if index == action else 0.0
                weights[index] += self.learning_rate * advantage * (indicator - probability)

    def to_json(self) -> dict[str, Any]:
        return {
            "schema": "strict_policy_tree_v1",
            "method": "self-play REINFORCE over notebook basic tactics",
            "tactics": [tactic.name for tactic in TACTICS],
            "learningRate": self.learning_rate,
            "nodes": self.logits,
        }


class StrictCurlingEnd:
    """一局 16 手的严格本地物理环境；每手都由同一个 PhysX Scene 连续推进。"""

    def __init__(self, *, seed: int, training_fast: bool = True) -> None:
        from local_simulator.unity_physx import NativePyphysxMotionStepper, PersistentPhysxFrontHalfScene

        self.seed = int(seed)
        self.scene = PersistentPhysxFrontHalfScene(stone_count=STONE_COUNT, ice_use_fast_midphase=True)
        self.motion_stepper = NativePyphysxMotionStepper(self.scene.pyphysx)
        self.shot_number = 0
        # This only skips Python audit-payload construction between fixed
        # ticks.  It retains the same native friction setter, PhysX Scene and
        # contact reports; turn it off for forensic per-tick investigations.
        self.training_fast = bool(training_fast)

    def reset(self) -> list[dict[str, Any]]:
        self.shot_number = 0
        # 新的一局显式恢复所有朝向；一局内则不 reset，PhysX 持续保留每颗壶状态。
        self.scene.reset_positions([0.0] * (STONE_COUNT * 2), yaw_overrides={i: 0.0 for i in range(STONE_COUNT)})
        return self.states()

    def states(self) -> list[dict[str, Any]]:
        return [self.scene.state(index) for index in range(STONE_COUNT)]

    def _friction_noises(self) -> list[float]:
        from tools.reverse.front_half_pcm_replay import unity_seed_friction_noises

        # 每一手一条新的本地 RNG 序列；给定 seed 时整局仍可复现。
        return unity_seed_friction_noises(self.seed + self.shot_number * 7919, 5000)

    def _settle(self, *, max_steps: int = 6000) -> bool:
        """Advance until the existing Unity-aligned quiet criterion is met.

        New bundled runtimes provide the exact loop in the native extension:
        they execute the same ``Scene.simulate(dt)`` calls and the same
        linear/angular thresholds, but do not serialise every velocity into
        Python on every tick.  Keep the Python implementation below as a
        compatibility fallback for older shipped extensions.
        """
        native_settle = getattr(self.scene.scene, "simulate_until_quiet", None)
        if native_settle is not None:
            bodies = [slot.body for slot in self.scene.slots if slot.enabled]
            settled, _steps = native_settle(
                bodies,
                self.scene.dt,
                max_steps,
                0.01,
                0.01,
                20,
            )
            return bool(settled)

        quiet = 0
        for _ in range(max_steps):
            self.scene.scene.simulate(self.scene.dt)
            self.scene.scene.get_contact_reports()
            moving = False
            for slot in self.scene.slots:
                if not slot.enabled:
                    continue
                linear_velocity = slot.body.get_linear_velocity()
                angular_velocity = slot.body.get_angular_velocity()
                # Coordinate remapping only permutes/sign-flips components,
                # so these native norms are identical to the protocol norms.
                linear = math.sqrt(sum(float(value) ** 2 for value in linear_velocity))
                angular = math.sqrt(sum(float(value) ** 2 for value in angular_velocity))
                moving = moving or linear > 0.01 or angular > 0.01
            quiet = quiet + 1 if not moving else 0
            if quiet >= 20:
                return True
        return False

    def _run_without_target(self, active_index: int, shot: Sequence[float], noises: Sequence[float]) -> None:
        """首壶没有碰撞目标时的严格逐 tick 滑行路径。"""

        self.scene.start_bestshot(active_index, shot, yaw=0.0)
        for noise in noises:
            step = self.scene.step_custom_sliding(active_index, noise, motion_stepper=self.motion_stepper)
            state = step["afterScene"]
            if math.hypot(state["vx"], state["vy"]) <= 0.01:
                break
        # 该壶后续不再由自定义滑行器控制；下一手开始前它是普通静止 PhysX 壶。
        self.scene.slots[active_index].material.set_static_friction(0.6)
        self.scene.slots[active_index].material.set_dynamic_friction(0.6)
        self.scene._custom_sliding_index = None  # 清除刚结束的前半段控制权。

    def play(self, shot: Sequence[float]) -> dict[str, Any]:
        if self.shot_number >= STONE_COUNT:
            raise RuntimeError("本局 16 手已结束")
        active_index = self.shot_number
        targets = [slot.index for slot in self.scene.slots if slot.enabled]
        noises = self._friction_noises()
        if targets:
            replay_method = (
                self.scene.run_bestshot_to_first_contact_training
                if self.training_fast
                else self.scene.run_bestshot_to_first_contact
            )
            replay = replay_method(
                active_index,
                shot,
                noises,
                target_indices=targets,
                yaw=0.0,
                max_steps=len(noises),
                motion_stepper=self.motion_stepper,
            )
            if replay.get("reachedFirstContact"):
                # 严格审计同样让第一个接触帧后的尾段只由本地 Scene 继续推进。
                self.scene.scene.simulate(self.scene.dt)
                self.scene.scene.get_contact_reports()
                settled = self._settle()
            else:
                settled = math.hypot(self.scene.state(active_index)["vx"], self.scene.state(active_index)["vy"]) <= 0.01
        else:
            self._run_without_target(active_index, shot, noises)
            settled = True
            replay = {"reachedFirstContact": False}
        cleared = self.scene.clear_out_of_play_stones()
        self.shot_number += 1
        return {
            "contact": bool(replay.get("reachedFirstContact")),
            "settled": bool(settled),
            "cleared": cleared,
            "states": self.states(),
        }


def closest_enemy_shot(states: Sequence[dict[str, Any]], team: int) -> tuple[float, float, float]:
    """简化 takeout：瞄准离圆心最近的敌壶；没有敌壶则进营。"""

    enemies = [
        state
        for index, state in enumerate(states)
        if state["enabled"] and index % 2 != team
    ]
    if not enemies:
        return TACTICS[2].shot
    target = min(enemies, key=lambda state: distance(float(state["x"]), float(state["y"])))
    # 默认出手线 x=2.3506；这个近似只负责把“清壶”变成可执行的一手。
    return (4.2, max(-0.8, min(0.8, float(target["x"]) - 2.3506)), 0.0)


def tactic_shot(tactic_index: int, states: Sequence[dict[str, Any]], team: int) -> tuple[float, float, float]:
    if TACTICS[tactic_index].name == "takeout":
        return closest_enemy_shot(states, team)
    return TACTICS[tactic_index].shot


def train(args: argparse.Namespace) -> dict[str, Any]:
    if args.games < 1:
        raise ValueError("--games 至少为 1")
    install_bundled_pyphysx()
    rng = random.Random(args.seed)
    policy = LearnedPolicyTree(learning_rate=args.learning_rate)
    environment = StrictCurlingEnd(seed=args.seed)
    games: list[dict[str, Any]] = []

    for game_index in range(args.games):
        states = environment.reset()
        trajectory: list[tuple[str, int, list[float], int]] = []
        trace: list[dict[str, Any]] = []
        while environment.shot_number < STONE_COUNT:
            shot_number = environment.shot_number
            team = shot_number % 2
            node = context_key(states, shot_number, team)
            action, probabilities = policy.choose(rng, node)
            shot = tactic_shot(action, states, team)
            result = environment.play(shot)
            trajectory.append((node, action, probabilities, team))
            states = result["states"]
            trace.append(
                {
                    "shot": shot_number + 1,
                    "team": "first" if team == 0 else "second",
                    "node": node,
                    "tactic": TACTICS[action].name,
                    "bestshot": list(shot),
                    "contact": result["contact"],
                    "cleared": result["cleared"],
                    "temporaryScoreFirst": score_board(states),
                }
            )
        final_score = score_board(states)
        policy.update(trajectory, final_score)
        game = {
            "game": game_index + 1,
            "finalScoreFirst": final_score,
            "winner": "first" if final_score > 0 else "second" if final_score < 0 else "draw",
            "trace": trace,
        }
        games.append(game)
        print(
            f"第 {game_index + 1:03d} 局 | 先手得分 {final_score:+d} | "
            f"胜方 {game['winner']} | 已更新 {len(trajectory)} 个策略决策",
            flush=True,
        )

    report = {
        "schema": "strict_policy_tree_selfplay_report_v1",
        "scope": "non-sweeping, one end, 16 continuous shots, local strict PhysX only",
        "games": games,
        "policy": policy.to_json(),
    }
    args.model_file.parent.mkdir(parents=True, exist_ok=True)
    args.report_file.parent.mkdir(parents=True, exist_ok=True)
    args.model_file.write_text(json.dumps(policy.to_json(), ensure_ascii=False, indent=2), encoding="utf-8")
    args.report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> int:
    args = parse_args()
    report = train(args)
    first_wins = sum(1 for game in report["games"] if game["finalScoreFirst"] > 0)
    second_wins = sum(1 for game in report["games"] if game["finalScoreFirst"] < 0)
    draws = args.games - first_wins - second_wins
    print(f"完成：先手胜 {first_wins}，后手胜 {second_wins}，平局 {draws}")
    print(f"策略树：{args.model_file}")
    print(f"训练报告：{args.report_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
