"""Rollout container shared by simulator workers and the PPO trainer."""

import math
from collections import Counter
from dataclasses import dataclass, field
from typing import Dict, List

from ppo_policy import PPOConfig, compute_gae

HOUSE_HIT_ACTIONS = {
    "take_out",
    "take_out_house",
    "hit_and_stay",
    "hit_roll",
    "hit_roll_left",
    "hit_roll_right",
    "double_hit",
    "raise_takeout",
    "runback_takeout",
    "around_guard_takeout_left",
    "around_guard_takeout_right",
}
GUARD_HIT_ACTIONS = {
    "take_out_guard",
    "peel_guard",
    "clear",
}
SOFT_DISPLACEMENT_ACTIONS = {
    "push_in",
    "push_in_14",
    "double_push_in",
    "tap_back",
}
SETUP_ACTIONS = {
    "default_draw",
    "draw_button",
    "draw_top4",
    "draw_back4",
    "occupy",
    "middle_in_center",
    "defense",
    "defense_push_in",
    "freeze",
    "freeze_no1",
    "freeze_no2",
    "center_guard",
    "center_guard_high",
    "center_guard_low",
    "corner_guard_left",
    "corner_guard_right",
    "corner_guard_left_high",
    "corner_guard_right_high",
    "guard_my_shot",
    "come_around_left",
    "come_around_right",
    "around_guard_draw_left",
    "around_guard_draw_right",
}
HIT_ACTIONS = HOUSE_HIT_ACTIONS | GUARD_HIT_ACTIONS | SOFT_DISPLACEMENT_ACTIONS
NEW_EXPLORATION_ACTIONS = {
    "center_guard_high",
    "center_guard_low",
    "corner_guard_left_high",
    "corner_guard_right_high",
    "freeze_no1",
    "freeze_no2",
    "guard_my_shot",
    "hit_roll_left",
    "hit_roll_right",
    "raise_takeout",
    "runback_takeout",
    "around_guard_takeout_left",
    "around_guard_takeout_right",
    "around_guard_draw_left",
    "around_guard_draw_right",
    "tap_back",
}


@dataclass
class RolloutBuffer:
    states: List[List[float]] = field(default_factory=list)
    actions: List[int] = field(default_factory=list)
    log_probs: List[float] = field(default_factory=list)
    rewards: List[float] = field(default_factory=list)
    dones: List[float] = field(default_factory=list)
    values: List[float] = field(default_factory=list)
    action_names: List[str] = field(default_factory=list)
    action_masks: List[List[bool]] = field(default_factory=list)
    outcome_flags: List[Dict[str, bool]] = field(default_factory=list)

    def append(
        self,
        state,
        action: int,
        log_prob: float,
        reward: float,
        done: bool,
        value: float,
        action_name: str = "",
        action_mask=None,
        outcome_flags=None,
    ):
        self.states.append(list(state))
        self.actions.append(int(action))
        self.log_probs.append(float(log_prob))
        self.rewards.append(float(reward))
        self.dones.append(1.0 if done else 0.0)
        self.values.append(float(value))
        self.action_names.append(action_name)
        self.action_masks.append(list(action_mask) if action_mask is not None else [])
        self.outcome_flags.append(dict(outcome_flags or {}))

    def __len__(self):
        return len(self.rewards)

    def extend(self, other: "RolloutBuffer"):
        self.states.extend(other.states)
        self.actions.extend(other.actions)
        self.log_probs.extend(other.log_probs)
        self.rewards.extend(other.rewards)
        self.dones.extend(other.dones)
        self.values.extend(other.values)
        self.action_names.extend(other.action_names)
        self.action_masks.extend(other.action_masks)
        self.outcome_flags.extend(other.outcome_flags)

    def summary_metrics(self) -> Dict[str, float]:
        count = len(self)
        if count == 0:
            return {
                "mean_reward": 0.0,
                "takeout_rate": 0.0,
                "hit_rate": 0.0,
                "draw_rate": 0.0,
                "house_hit_rate": 0.0,
                "guard_hit_rate": 0.0,
                "soft_displacement_rate": 0.0,
                "setup_rate": 0.0,
                "new_action_rate": 0.0,
                "unique_actions": 0.0,
                "effective_actions": 0.0,
                "top_action_rate": 0.0,
                "positive_reward_rate": 0.0,
                "negative_reward_rate": 0.0,
                "bypass_draw_attempts": 0.0,
                "bypass_draw_success_rate": 0.0,
                "bypass_takeout_attempts": 0.0,
                "bypass_takeout_success_rate": 0.0,
                "blocked_threat_hit_attempts": 0.0,
                "guard_only_failure_rate": 0.0,
            }
        takeout_actions = {
            "take_out",
            "take_out_house",
            "take_out_guard",
            "around_guard_takeout_left",
            "around_guard_takeout_right",
        }
        action_counts = Counter(self.action_names)
        action_probs = [value / count for value in action_counts.values() if value]
        action_entropy = -sum(prob * math.log(prob) for prob in action_probs)
        bypass_draw_attempts = sum(
            1 for flags in self.outcome_flags if flags.get("bypass_draw_attempt")
        )
        bypass_draw_successes = sum(
            1 for flags in self.outcome_flags if flags.get("bypass_draw_success")
        )
        bypass_takeout_attempts = sum(
            1 for flags in self.outcome_flags if flags.get("bypass_takeout_attempt")
        )
        bypass_takeout_successes = sum(
            1 for flags in self.outcome_flags if flags.get("bypass_takeout_success")
        )
        blocked_threat_hit_attempts = sum(
            1 for flags in self.outcome_flags if flags.get("blocked_threat_hit_attempt")
        )
        guard_only_failures = sum(
            1 for flags in self.outcome_flags if flags.get("guard_only_failure")
        )
        return {
            "mean_reward": sum(self.rewards) / count,
            "takeout_rate": sum(1 for name in self.action_names if name in takeout_actions) / count,
            "hit_rate": sum(1 for name in self.action_names if name in HIT_ACTIONS) / count,
            "draw_rate": sum(1 for name in self.action_names if name in SETUP_ACTIONS) / count,
            "house_hit_rate": sum(1 for name in self.action_names if name in HOUSE_HIT_ACTIONS) / count,
            "guard_hit_rate": sum(1 for name in self.action_names if name in GUARD_HIT_ACTIONS) / count,
            "soft_displacement_rate": sum(
                1 for name in self.action_names if name in SOFT_DISPLACEMENT_ACTIONS
            ) / count,
            "setup_rate": sum(1 for name in self.action_names if name in SETUP_ACTIONS) / count,
            "new_action_rate": sum(
                1 for name in self.action_names if name in NEW_EXPLORATION_ACTIONS
            ) / count,
            "unique_actions": float(len(action_counts)),
            "effective_actions": math.exp(action_entropy),
            "top_action_rate": max(action_counts.values()) / count,
            "positive_reward_rate": sum(1 for reward in self.rewards if reward > 0.0) / count,
            "negative_reward_rate": sum(1 for reward in self.rewards if reward < 0.0) / count,
            "bypass_draw_attempts": float(bypass_draw_attempts),
            "bypass_draw_success_rate": bypass_draw_successes / max(1, bypass_draw_attempts),
            "bypass_takeout_attempts": float(bypass_takeout_attempts),
            "bypass_takeout_success_rate": bypass_takeout_successes / max(1, bypass_takeout_attempts),
            "blocked_threat_hit_attempts": float(blocked_threat_hit_attempts),
            "guard_only_failure_rate": guard_only_failures / max(1, blocked_threat_hit_attempts),
        }

    def to_training_batch(self, next_value: float, config: PPOConfig) -> Dict[str, object]:
        returns, advantages = compute_gae(
            rewards=self.rewards,
            dones=self.dones,
            values=self.values,
            next_value=next_value,
            config=config,
        )
        return {
            "states": self.states,
            "actions": self.actions,
            "log_probs": self.log_probs,
            "returns": returns,
            "advantages": advantages,
            "action_names": self.action_names,
            "action_masks": self.action_masks if all(self.action_masks) else None,
        }
