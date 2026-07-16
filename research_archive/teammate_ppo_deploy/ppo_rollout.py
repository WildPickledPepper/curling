"""Rollout container shared by simulator workers and the PPO trainer."""

from dataclasses import dataclass, field
from typing import Dict, List

from ppo_policy import PPOConfig, compute_gae


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
    ):
        self.states.append(list(state))
        self.actions.append(int(action))
        self.log_probs.append(float(log_prob))
        self.rewards.append(float(reward))
        self.dones.append(1.0 if done else 0.0)
        self.values.append(float(value))
        self.action_names.append(action_name)
        self.action_masks.append(list(action_mask) if action_mask is not None else [])

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

    def summary_metrics(self) -> Dict[str, float]:
        count = len(self)
        if count == 0:
            return {
                "mean_reward": 0.0,
                "takeout_rate": 0.0,
                "hit_rate": 0.0,
                "draw_rate": 0.0,
                "positive_reward_rate": 0.0,
                "negative_reward_rate": 0.0,
            }
        hit_actions = {"take_out", "hit_roll", "double_hit", "clear", "push_in", "push_in_14", "double_push_in"}
        return {
            "mean_reward": sum(self.rewards) / count,
            "takeout_rate": sum(1 for name in self.action_names if name == "take_out") / count,
            "hit_rate": sum(1 for name in self.action_names if name in hit_actions) / count,
            "draw_rate": sum(1 for name in self.action_names if name == "default_draw") / count,
            "positive_reward_rate": sum(1 for reward in self.rewards if reward > 0.0) / count,
            "negative_reward_rate": sum(1 for reward in self.rewards if reward < 0.0) / count,
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
