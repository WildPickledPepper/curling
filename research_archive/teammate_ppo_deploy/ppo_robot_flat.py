"""PPO-driven tactic robot and live rollout collection helpers."""

import argparse
import contextlib
import io
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import torch
except ImportError:  # pragma: no cover
    torch = None

ROOT = Path(__file__).resolve().parent

from ppo_actions import ACTION_NAMES, N_ACTIONS, action_id, action_name
from ppo_policy import ActorCritic, load_compatible_state_dict
from ppo_rollout import RolloutBuffer
from ppo_state_reward import (
    FALLBACK_DRAW_PENALTY,
    FR_WEIGHT,
    INVALID_ACTION_PENALTY,
    build_state,
    delayed_setup_reward,
    hit_outcome_reward,
    shaped_reward,
    situation_evaluation_reward,
    summarize_position,
)

# tacticslib/AIRobot.py parses command-line args at import time. Hide this
# module's args during import so ppo_framework owns its own CLI.
_ORIGINAL_ARGV = sys.argv[:]
try:
    sys.argv = [sys.argv[0]]
    from AIRobot import AIRobot  # noqa: E402
finally:
    sys.argv = _ORIGINAL_ARGV

import strategy_library as sl  # noqa: E402

DEFAULT_DRAW_BESTSHOT = "BESTSHOT 3.0 0 0"
SETUP_CREDIT_ACTIONS = {
    "occupy",
    "middle_in_center",
    "defense",
    "defense_push_in",
    "push_in",
    "push_in_14",
    "freeze",
    "double_push_in",
}


def parse_args():
    parser = argparse.ArgumentParser(description="PPO tactic robot.")
    parser.add_argument("-k", "--key", default="localtest")
    parser.add_argument("-H", "--host", default="127.0.0.1")
    parser.add_argument("-p", "--port", default="7788")
    parser.add_argument("--name", default="PPOTacticsAI")
    parser.add_argument("--checkpoint", default="")
    parser.add_argument("--deterministic", action="store_true")
    parser.add_argument("--rollout-steps", type=int, default=0)
    parser.add_argument("--invalid-penalty", type=float, default=INVALID_ACTION_PENALTY)
    parser.add_argument("--fallback-draw-penalty", type=float, default=FALLBACK_DRAW_PENALTY)
    parser.add_argument("--take-out-penalty", type=float, default=0.0)
    parser.add_argument("--bad-takeout-penalty", type=float, default=0.0)
    parser.add_argument("--bad-takeout-min-delta", type=float, default=0.05)
    parser.add_argument("--delayed-setup-weight", type=float, default=0.25)
    parser.add_argument("--delayed-setup-max-abs", type=float, default=0.75)
    parser.add_argument(
        "--mask-guard-takeout",
        action="store_true",
        help="Mask take_out when its nearest opponent target is a guard and the position is not urgent.",
    )
    parser.add_argument(
        "--mask-guard-hit-actions",
        action="store_true",
        help="Mask take_out/hit_roll/double_hit/clear for early guard targets.",
    )
    parser.add_argument("--guard-takeout-max-shot", type=int, default=6)
    parser.add_argument(
        "--mask-guard-takeout-when-scoring",
        action="store_true",
        help="Also mask guard take_out when the current house score is non-negative.",
    )
    parser.add_argument(
        "--action-logit-bias",
        action="append",
        default=[],
        help="Inference-only action prior, e.g. take_out=-0.4. Can be repeated.",
    )
    parser.add_argument("--show-msg", action="store_true")
    return parser.parse_args()


def parse_action_logit_bias(items: List[str]) -> List[float]:
    bias = [0.0 for _ in range(N_ACTIONS)]
    for item in items or []:
        if "=" not in item:
            raise ValueError(f"Invalid --action-logit-bias value: {item!r}")
        name, value = item.split("=", 1)
        bias[action_id(name.strip())] = float(value)
    return bias


def get_state_list(position):
    state_list = []
    for n in range(8):
        init_x, init_y = float(position[n * 4]), float(position[n * 4 + 1])
        gote_x, gote_y = float(position[n * 4 + 2]), float(position[n * 4 + 3])
        state_list.append([init_x, init_y])
        state_list.append([gote_x, gote_y])
    return state_list


def result_to_bestshot(result) -> Optional[str]:
    if result is not None and result != 0:
        v0, h0, w0 = result
        return f"BESTSHOT {v0} {h0} {w0}"
    return None


class PPOTacticsRobot(AIRobot):
    def __init__(
        self,
        key: str,
        name: str,
        host: str,
        port: int,
        model: Optional[ActorCritic] = None,
        deterministic: bool = False,
        rollout_steps: int = 0,
        invalid_penalty: float = INVALID_ACTION_PENALTY,
        fallback_draw_penalty: float = FALLBACK_DRAW_PENALTY,
        take_out_penalty: float = 0.0,
        bad_takeout_penalty: float = 0.0,
        bad_takeout_min_delta: float = 0.05,
        delayed_setup_weight: float = 0.25,
        delayed_setup_max_abs: float = 0.75,
        mask_guard_takeout: bool = False,
        mask_guard_hit_actions: bool = False,
        guard_takeout_max_shot: int = 6,
        mask_guard_takeout_when_scoring: bool = False,
        action_logit_bias: Optional[List[float]] = None,
        show_msg: bool = False,
    ):
        super().__init__(
            key=key,
            name=name,
            host=host,
            port=port,
            show_msg=show_msg,
            enable_centerline_choice=True,
            centerline_choice="RESET",
        )
        self.model = model
        self.deterministic = deterministic
        self.rollout_steps = rollout_steps
        self.rollout = RolloutBuffer()
        self.pending_transition: Optional[Dict[str, object]] = None
        self.invalid_action_count = 0
        self.fallback_draw_count = 0
        self.invalid_penalty = invalid_penalty
        self.fallback_draw_penalty = fallback_draw_penalty
        self.take_out_penalty = max(0.0, take_out_penalty)
        self.bad_takeout_penalty = max(0.0, bad_takeout_penalty)
        self.bad_takeout_min_delta = bad_takeout_min_delta
        self.delayed_setup_weight = max(0.0, delayed_setup_weight)
        self.delayed_setup_max_abs = max(0.0, delayed_setup_max_abs)
        self.mask_guard_takeout = mask_guard_takeout
        self.mask_guard_hit_actions = mask_guard_hit_actions
        self.guard_takeout_max_shot = max(0, guard_takeout_max_shot)
        self.mask_guard_takeout_when_scoring = mask_guard_takeout_when_scoring
        self.action_logit_bias = action_logit_bias or [0.0 for _ in range(N_ACTIONS)]
        self.last_sent_bestshot = ""
        self.pending_setup_credit: Optional[Dict[str, object]] = None

    def is_init_flag(self) -> int:
        return 0 if self.player_is_init else 1

    def current_state(self):
        return build_state(
            position=self.position,
            player_is_init=self.player_is_init,
            shot_num=self.shot_num,
            end_score=getattr(self, "score", 0),
            total_ends=getattr(self, "round_total", -1),
            current_player=getattr(self, "next_shot", 0),
        )

    def legal_action_map(self) -> Dict[int, Optional[str]]:
        legal: Dict[int, Optional[str]] = {}
        for index, tactic_name in enumerate(ACTION_NAMES):
            if tactic_name == "default_draw":
                shot_msg = DEFAULT_DRAW_BESTSHOT
            else:
                shot_msg = result_to_bestshot(self.tactic_result(tactic_name, quiet=True))
            legal[index] = shot_msg
        return legal

    def legal_action_mask(self, legal: Dict[int, Optional[str]]):
        default_id = action_id("default_draw")
        mask = [
            legal.get(index) is not None and index != default_id
            for index in range(N_ACTIONS)
        ]
        if self.should_mask_guard_takeout():
            mask[action_id("take_out")] = False
        if self.should_mask_guard_hit_actions():
            for name in ("take_out", "hit_roll", "double_hit", "clear"):
                mask[action_id(name)] = False
        if not any(mask):
            mask[default_id] = True
        return mask

    def should_mask_guard_takeout(self) -> bool:
        if not self.mask_guard_takeout:
            return False
        summary = summarize_position(self.position, self.player_is_init)
        opp_stones = [stone for stone in summary["stones"] if stone.owner == "opp"]
        if not opp_stones:
            return False
        nearest_opp = min(opp_stones, key=lambda stone: stone.dist)
        if nearest_opp in summary["opp_house"]:
            return False
        score_for_my = int(summary["score_for_my"])
        return (
            self.shot_num <= self.guard_takeout_max_shot
            or (self.mask_guard_takeout_when_scoring and score_for_my >= 0)
        )

    def should_mask_guard_hit_actions(self) -> bool:
        if not self.mask_guard_hit_actions:
            return False
        summary = summarize_position(self.position, self.player_is_init)
        opp_stones = [stone for stone in summary["stones"] if stone.owner == "opp"]
        if not opp_stones:
            return False
        nearest_opp = min(opp_stones, key=lambda stone: stone.dist)
        return nearest_opp not in summary["opp_house"] and self.shot_num <= self.guard_takeout_max_shot

    def choose_action(self, state, action_mask) -> Tuple[Optional[int], float, float]:
        if self.model is None:
            legal_indices = [index for index, legal in enumerate(action_mask) if legal]
            action = legal_indices[int(time.time_ns() % len(legal_indices))]
            return action, 0.0, 0.0
        if any(self.action_logit_bias):
            with torch.no_grad():
                state_tensor = torch.as_tensor(state, dtype=torch.float32).unsqueeze(0)
                dist, value_tensor = self.model.distribution(state_tensor, action_mask=action_mask)
                bias_tensor = torch.as_tensor(self.action_logit_bias, dtype=torch.float32).unsqueeze(0)
                dist = torch.distributions.Categorical(logits=dist.logits + bias_tensor)
                if self.deterministic:
                    action_tensor = torch.argmax(dist.probs, dim=-1)
                else:
                    action_tensor = dist.sample()
                return (
                    int(action_tensor.item()),
                    float(dist.log_prob(action_tensor).item()),
                    float(value_tensor.item()),
                )
        return self.model.act(
            state,
            deterministic=self.deterministic,
            action_mask=action_mask,
        )

    def tactic_result(self, tactic_name: str, quiet: bool = False):
        state_list = get_state_list(self.position)
        is_init = self.is_init_flag()

        if tactic_name == "double_hit":
            func = sl.double_hit_init if self.player_is_init else sl.double_hit_gote
        elif tactic_name == "double_push_in":
            func = sl.double_push_in
        else:
            func = getattr(sl, tactic_name, None)

        if func is None:
            return None
        try:
            if quiet:
                with contextlib.redirect_stdout(io.StringIO()):
                    return func(state_list, is_init, self.shot_num)
            return func(state_list, is_init, self.shot_num)
        except TypeError:
            return None

    def action_to_shot(self, selected_action: Optional[int], legal: Dict[int, Optional[str]]) -> Tuple[str, str, bool, bool]:
        if selected_action is None:
            self.invalid_action_count += 1
            self.fallback_draw_count += 1
            return DEFAULT_DRAW_BESTSHOT, "default_draw", True, True

        selected_name = action_name(selected_action)
        shot_msg = legal.get(selected_action)
        if shot_msg:
            if selected_name == "default_draw":
                self.fallback_draw_count += 1
            return shot_msg, selected_name, False, selected_name == "default_draw"

        self.invalid_action_count += 1
        for fallback_id, fallback_name in enumerate(ACTION_NAMES):
            if fallback_id == selected_action:
                continue
            shot_msg = legal.get(fallback_id)
            if shot_msg:
                if fallback_name == "default_draw":
                    self.fallback_draw_count += 1
                return shot_msg, fallback_name, True, fallback_name == "default_draw"

        self.fallback_draw_count += 1
        return DEFAULT_DRAW_BESTSHOT, "default_draw", True, True

    def get_bestshot(self):
        state = self.current_state()
        legal = self.legal_action_map()
        action_mask = self.legal_action_mask(legal)
        selected_action, log_prob, value = self.choose_action(state, action_mask)
        shot_msg, executed_name, invalid_action, fallback_draw = self.action_to_shot(selected_action, legal)
        stored_action = selected_action if selected_action is not None else action_id("occupy")
        self.pending_transition = {
            "state": state,
            "position_before": list(self.position),
            "action": stored_action,
            "log_prob": log_prob,
            "value": value,
            "action_name": executed_name,
            "action_mask": action_mask,
            "shot_num": self.shot_num,
            "invalid_action": invalid_action,
            "fallback_draw": fallback_draw,
        }
        self.last_sent_bestshot = shot_msg
        print(
            "PPO决策:",
            f"shot={self.shot_num + 1}",
            f"selected={action_name(selected_action) if selected_action is not None else 'none'}",
            f"executed={executed_name}",
            f"invalid={invalid_action}",
            f"fallback={fallback_draw}",
            flush=True,
        )
        return shot_msg

    def attach_position_after(self):
        if self.pending_transition is None:
            return False
        pending = self.pending_transition
        reward = shaped_reward(
            before_position=pending["position_before"],
            after_position=self.position,
            player_is_init=self.player_is_init,
            shot_num=int(pending["shot_num"]),
            invalid_action=bool(pending["invalid_action"]),
            fallback_draw=bool(pending.get("fallback_draw", False)),
            invalid_action_penalty=self.invalid_penalty,
            fallback_draw_penalty=self.fallback_draw_penalty,
        )
        reward += hit_outcome_reward(
            before_position=pending["position_before"],
            after_position=self.position,
            player_is_init=self.player_is_init,
            shot_num=int(pending["shot_num"]),
            action_name=str(pending.get("action_name", "")),
        )
        if pending.get("action_name") == "take_out":
            reward -= self.take_out_penalty
            if self.bad_takeout_penalty > 0:
                board_delta = situation_evaluation_reward(
                    before_position=pending["position_before"],
                    after_position=self.position,
                    player_is_init=self.player_is_init,
                    shot_num=int(pending["shot_num"]),
                )
                if board_delta < self.bad_takeout_min_delta:
                    reward -= self.bad_takeout_penalty
        reward = max(-5.0, min(5.0, reward))
        reward_index = len(self.rollout)
        self.rollout.append(
            state=pending["state"],
            action=int(pending["action"]),
            log_prob=float(pending["log_prob"]),
            reward=reward,
            done=False,
            value=float(pending["value"]),
            action_name=str(pending["action_name"]),
            action_mask=pending["action_mask"],
        )
        if (
            self.delayed_setup_weight > 0.0
            and str(pending.get("action_name", "")) in SETUP_CREDIT_ACTIONS
        ):
            self.pending_setup_credit = {
                "reward_index": reward_index,
                "position_before": list(pending["position_before"]),
                "position_after": list(self.position),
                "shot_num": int(pending["shot_num"]),
                "action_name": str(pending.get("action_name", "")),
            }
        else:
            self.pending_setup_credit = None
        self.pending_transition = None
        if self.rollout_steps > 0 and len(self.rollout) >= self.rollout_steps:
            self.on_line = False
        return True

    def apply_delayed_setup_credit(self):
        if not self.pending_setup_credit or self.delayed_setup_weight <= 0.0:
            return
        reward_index = int(self.pending_setup_credit["reward_index"])
        if reward_index < 0 or reward_index >= len(self.rollout.rewards):
            self.pending_setup_credit = None
            return
        bonus = delayed_setup_reward(
            before_position=self.pending_setup_credit["position_before"],
            after_own_position=self.pending_setup_credit["position_after"],
            after_response_position=self.position,
            player_is_init=self.player_is_init,
            shot_num=int(self.pending_setup_credit["shot_num"]),
            weight=self.delayed_setup_weight,
            max_abs=self.delayed_setup_max_abs,
        )
        self.rollout.rewards[reward_index] = max(
            -5.0,
            min(5.0, self.rollout.rewards[reward_index] + bonus),
        )
        if abs(bonus) >= 0.01:
            print(
                "延迟战术奖励:",
                f"action={self.pending_setup_credit['action_name']}",
                f"bonus={bonus:.3f}",
                flush=True,
            )
        self.pending_setup_credit = None

    def add_terminal_reward(self, end_score: int):
        if len(self.rollout) == 0:
            return
        self.pending_setup_credit = None
        shaped = self.rollout.rewards[-1] + FR_WEIGHT * float(end_score)
        self.rollout.rewards[-1] = max(-5.0, min(5.0, shaped))
        self.rollout.dones[-1] = 1.0

    def recv_forever(self):
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
                if msg_list[0] == "Player1":
                    self.player_is_init = True
                    print("玩家1，首局先手", flush=True)
                else:
                    self.player_is_init = False
                    print("玩家2，首局后手", flush=True)
            if msg_code == "ISREADY":
                self.send_msg("READYOK")
                time.sleep(0.5)
                self.send_msg("NAME " + self.name)
                print(self.name + " 准备完毕！", flush=True)
            if msg_code == "NEWGAME":
                time0 = time.time()
                self.pending_setup_credit = None
            if msg_code == "SETSTATE":
                self.recv_setstate(msg_list)
            if msg_code == "POSITION":
                for n in range(32):
                    self.position[n] = float(msg_list[n])
                if not self.attach_position_after():
                    self.apply_delayed_setup_credit()
            if msg_code == "GO":
                self.send_msg(self.get_bestshot())
            if msg_code == "MOTIONINFO":
                for n in range(5):
                    self.motioninfo[n] = float(msg_list[n])
            if msg_code == "CENTERLINE_VIOLATION":
                self.send_msg("CENTERLINE_CHOICE RESET")
            if msg_code == "SCORE":
                time1 = time.time()
                self.score = int(msg_list[0])
                self.add_terminal_reward(self.score)
                print(
                    "%s %s第%d局耗时%.1f秒"
                    % (time.strftime("[%Y/%m/%d %H:%M:%S]"), self.name, self.round_num + 1, time1 - time0),
                    end=" ",
                    flush=True,
                )
                time0 = time1
                if self.score > 0:
                    print("我方得" + str(self.score) + "分", end=" ", flush=True)
                    if self.round_total != -1:
                        self.player_is_init = True
                elif self.score < 0:
                    print("对方得" + str(self.score * -1) + "分", end=" ", flush=True)
                    if self.round_total != -1:
                        self.player_is_init = False
                else:
                    print("双方均未得分", end=" ", flush=True)
                    if self.round_total != -1:
                        self.player_is_init = not self.player_is_init
                print("我方下局先手" if self.player_is_init else "我方下局后手", flush=True)
            if msg_code == "GAMEOVER":
                break

        self.ai_sock.close()
        print("已关闭socket连接", flush=True)
        return self.rollout


def load_model(checkpoint_path: str) -> Optional[ActorCritic]:
    if not checkpoint_path:
        return None
    if torch is None:
        raise ImportError("PyTorch is required to load PPO checkpoints.")
    model = ActorCritic()
    checkpoint = torch.load(checkpoint_path, map_location="cpu")
    state_dict = checkpoint.get("model", checkpoint)
    load_compatible_state_dict(model, state_dict)
    model.eval()
    return model


def collect_rollout(
    key: str,
    host: str,
    port: int,
    rollout_steps: int,
    model_state_dict=None,
    deterministic: bool = False,
    name: str = "PPOWorker",
    invalid_penalty: float = INVALID_ACTION_PENALTY,
    fallback_draw_penalty: float = FALLBACK_DRAW_PENALTY,
    take_out_penalty: float = 0.0,
    bad_takeout_penalty: float = 0.0,
    bad_takeout_min_delta: float = 0.05,
    delayed_setup_weight: float = 0.25,
    delayed_setup_max_abs: float = 0.75,
    mask_guard_takeout: bool = False,
    mask_guard_hit_actions: bool = False,
    guard_takeout_max_shot: int = 6,
    mask_guard_takeout_when_scoring: bool = False,
):
    model = ActorCritic() if torch is not None else None
    if model is not None and model_state_dict is not None:
        load_compatible_state_dict(model, model_state_dict)
        model.eval()
    robot = PPOTacticsRobot(
        key=key,
        name=name,
        host=host,
        port=port,
        model=model,
        deterministic=deterministic,
        rollout_steps=rollout_steps,
        invalid_penalty=invalid_penalty,
        fallback_draw_penalty=fallback_draw_penalty,
        take_out_penalty=take_out_penalty,
        bad_takeout_penalty=bad_takeout_penalty,
        bad_takeout_min_delta=bad_takeout_min_delta,
        delayed_setup_weight=delayed_setup_weight,
        delayed_setup_max_abs=delayed_setup_max_abs,
        mask_guard_takeout=mask_guard_takeout,
        mask_guard_hit_actions=mask_guard_hit_actions,
        guard_takeout_max_shot=guard_takeout_max_shot,
        mask_guard_takeout_when_scoring=mask_guard_takeout_when_scoring,
        show_msg=False,
    )
    return robot.recv_forever()


def main():
    args = parse_args()
    model = load_model(args.checkpoint)
    action_logit_bias = parse_action_logit_bias(args.action_logit_bias)
    robot = PPOTacticsRobot(
        key=args.key,
        name=args.name,
        host=args.host,
        port=int(args.port),
        model=model,
        deterministic=args.deterministic,
        rollout_steps=args.rollout_steps,
        invalid_penalty=args.invalid_penalty,
        fallback_draw_penalty=args.fallback_draw_penalty,
        take_out_penalty=args.take_out_penalty,
        bad_takeout_penalty=args.bad_takeout_penalty,
        bad_takeout_min_delta=args.bad_takeout_min_delta,
        delayed_setup_weight=args.delayed_setup_weight,
        delayed_setup_max_abs=args.delayed_setup_max_abs,
        mask_guard_takeout=args.mask_guard_takeout,
        mask_guard_hit_actions=args.mask_guard_hit_actions,
        guard_takeout_max_shot=args.guard_takeout_max_shot,
        mask_guard_takeout_when_scoring=args.mask_guard_takeout_when_scoring,
        action_logit_bias=action_logit_bias,
        show_msg=args.show_msg,
    )
    rollout = robot.recv_forever()
    print(
        f"PPO rollout collected: {len(rollout)} transitions, "
        f"invalid_actions={robot.invalid_action_count}, "
        f"fallback_draws={robot.fallback_draw_count}",
        flush=True,
    )


if __name__ == "__main__":
    main()
