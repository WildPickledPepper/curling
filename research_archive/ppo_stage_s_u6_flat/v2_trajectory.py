"""Independent worker trajectories and boundary-safe GAE for PPO V2."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Sequence

import torch

from v2_config import V2PPOConfig


@dataclass
class Transition:
    """One policy decision and the state reached after its environment step."""

    state: List[float]
    action: int
    action_mask: List[bool]
    log_prob: float
    value: float
    reward: float
    next_state: List[float]
    next_value: float
    action_logit_bias: List[float] = field(default_factory=list)
    terminated: bool = False
    truncated: bool = False
    action_name: str = ""
    action_family: str = ""
    action_preset: str = ""
    target_index: Optional[int] = None
    target_mask: List[bool] = field(default_factory=list)
    target_reference_index: Optional[int] = None
    middle_index: Optional[int] = None
    middle_mask: List[bool] = field(default_factory=list)
    second_target_index: Optional[int] = None
    second_target_mask: List[bool] = field(default_factory=list)
    shot_num: int = 0
    position_before: List[float] = field(default_factory=list)
    position_after_own: List[float] = field(default_factory=list)
    position_after_response: List[float] = field(default_factory=list)
    outcome_flags: Dict[str, bool] = field(default_factory=dict)
    bypass_diagnostics: Dict[str, Dict[str, object]] = field(default_factory=dict)
    reward_components: Dict[str, float] = field(default_factory=dict)
    terminal_score: Optional[int] = None
    end_boundary: bool = False
    match_result: Optional[int] = None
    match_result_target: Optional[int] = None

    def __post_init__(self) -> None:
        if self.terminated and self.truncated:
            raise ValueError("A transition cannot be both terminated and truncated.")
        if not self.action_mask:
            raise ValueError("V2 transitions must store the exact action mask.")
        if not any(self.action_mask):
            raise ValueError("V2 transition action mask has no legal action.")
        if not self.action_logit_bias:
            self.action_logit_bias = [0.0] * len(self.action_mask)
        if len(self.action_logit_bias) != len(self.action_mask):
            raise ValueError("action logit bias must match the action mask width.")


@dataclass
class Trajectory:
    """All transitions from exactly one rollout worker attempt."""

    trajectory_id: str
    transitions: List[Transition] = field(default_factory=list)
    distillation_records: List[Dict[str, object]] = field(default_factory=list)
    opponent_name: str = "unknown"
    candidate_role: str = "unknown"
    final_score_diff: Optional[int] = None
    initial_shot_num: int = 0
    curriculum_case: Optional[str] = None

    def append(self, transition: Transition) -> None:
        self.transitions.append(transition)

    def __len__(self) -> int:
        return len(self.transitions)

    @property
    def terminated_count(self) -> int:
        return sum(item.terminated for item in self.transitions)

    @property
    def truncated_count(self) -> int:
        return sum(item.truncated for item in self.transitions)

    def mark_last_truncated(self) -> None:
        """Close a nonterminal rollout without discarding its bootstrap value."""
        if not self.transitions:
            return
        last = self.transitions[-1]
        if not last.terminated:
            last.truncated = True

    def compute_gae(self, config: V2PPOConfig) -> tuple[torch.Tensor, torch.Tensor]:
        """Return unnormalised returns and advantages for this trajectory only.

        Each transition stores the value of its *actual* successor state.  A
        truncated endpoint uses that value in TD error, while both terminal and
        truncated endpoints stop advantage recursion into another trajectory.
        """
        count = len(self.transitions)
        rewards = torch.empty(count, dtype=torch.float32)
        values = torch.empty(count, dtype=torch.float32)
        next_values = torch.empty(count, dtype=torch.float32)
        boundaries = torch.empty(count, dtype=torch.float32)
        terminated = torch.empty(count, dtype=torch.float32)
        for index, item in enumerate(self.transitions):
            rewards[index] = item.reward
            values[index] = item.value
            next_values[index] = item.next_value
            terminated[index] = float(item.terminated)
            boundaries[index] = float(item.terminated or item.truncated)

        advantages = torch.zeros(count, dtype=torch.float32)
        next_advantage = torch.tensor(0.0, dtype=torch.float32)
        for index in reversed(range(count)):
            # A real terminal has no bootstrap; an artificial truncation does.
            bootstrap = 1.0 - terminated[index]
            delta = rewards[index] + config.gamma * bootstrap * next_values[index] - values[index]
            continuation = 1.0 - boundaries[index]
            next_advantage = delta + config.gamma * config.gae_lambda * continuation * next_advantage
            advantages[index] = next_advantage
        return advantages + values, advantages

    def compute_discounted_returns(self, config: V2PPOConfig) -> torch.Tensor:
        """Return Monte Carlo targets, bootstrapping only artificial truncation."""
        returns = torch.zeros(len(self.transitions), dtype=torch.float32)
        next_return = torch.tensor(0.0, dtype=torch.float32)
        for index in reversed(range(len(self.transitions))):
            item = self.transitions[index]
            if item.terminated:
                continuation = torch.tensor(0.0, dtype=torch.float32)
            elif item.truncated:
                continuation = torch.tensor(float(item.next_value), dtype=torch.float32)
            else:
                continuation = next_return
            next_return = torch.tensor(float(item.reward)) + config.gamma * continuation
            returns[index] = next_return
        return returns

    def to_batch(self, config: V2PPOConfig) -> Dict[str, object]:
        returns, advantages = self.compute_gae(config)
        value_targets = (
            self.compute_discounted_returns(config)
            if config.monte_carlo_value_targets
            else returns
        )
        return {
            "states": [item.state for item in self.transitions],
            "actions": [item.action for item in self.transitions],
            "action_masks": [item.action_mask for item in self.transitions],
            "action_logit_biases": [item.action_logit_bias for item in self.transitions],
            "log_probs": [item.log_prob for item in self.transitions],
            "values": [item.value for item in self.transitions],
            "rewards": [item.reward for item in self.transitions],
            "reward_components": [item.reward_components for item in self.transitions],
            "returns": returns,
            "value_targets": value_targets,
            "advantages": advantages,
            "trajectory_ids": [self.trajectory_id] * len(self),
            "opponent_names": [self.opponent_name] * len(self),
            "candidate_roles": [self.candidate_role] * len(self),
            "action_names": [item.action_name for item in self.transitions],
            "action_families": [item.action_family for item in self.transitions],
            "action_presets": [item.action_preset for item in self.transitions],
            "target_indices": [item.target_index if item.target_index is not None else -1 for item in self.transitions],
            "target_masks": [item.target_mask for item in self.transitions],
            "target_reference_indices": [
                item.target_reference_index if item.target_reference_index is not None else -1
                for item in self.transitions
            ],
            "middle_indices": [item.middle_index if item.middle_index is not None else -1 for item in self.transitions],
            "middle_masks": [item.middle_mask for item in self.transitions],
            "second_target_indices": [item.second_target_index if item.second_target_index is not None else -1 for item in self.transitions],
            "second_target_masks": [item.second_target_mask for item in self.transitions],
            "shot_nums": [item.shot_num for item in self.transitions],
            "outcome_flags": [item.outcome_flags for item in self.transitions],
            "bypass_diagnostics": [item.bypass_diagnostics for item in self.transitions],
            "terminal_scores": [
                item.terminal_score if item.terminal_score is not None else -100
                for item in self.transitions
            ],
            "end_boundaries": [item.end_boundary for item in self.transitions],
            "match_results": [
                item.match_result if item.match_result is not None else -100
                for item in self.transitions
            ],
            "match_result_targets": [
                item.match_result_target if item.match_result_target is not None else -100
                for item in self.transitions
            ],
            "terminated": [item.terminated for item in self.transitions],
            "truncated": [item.truncated for item in self.transitions],
            "bootstrap_values": [
                item.next_value for item in self.transitions if item.truncated and not item.terminated
            ],
        }


def merge_trajectory_batches(
    trajectories: Iterable[Trajectory], config: V2PPOConfig
) -> Dict[str, object]:
    """Compute GAE per trajectory, then merge and normalise advantages once."""
    trajectory_list = [trajectory for trajectory in trajectories if len(trajectory)]
    if not trajectory_list:
        raise ValueError("Cannot train PPO V2 from zero transitions.")

    fields: Dict[str, list] = {
        "states": [], "actions": [], "action_masks": [], "action_logit_biases": [], "log_probs": [],
        "values": [], "rewards": [], "reward_components": [],
        "returns": [], "value_targets": [], "advantages": [], "trajectory_ids": [],
        "opponent_names": [], "candidate_roles": [],
        "action_names": [], "action_families": [], "action_presets": [], "target_indices": [], "target_masks": [], "target_reference_indices": [], "middle_indices": [], "middle_masks": [], "second_target_indices": [], "second_target_masks": [], "outcome_flags": [], "bypass_diagnostics": [], "terminal_scores": [],
        "shot_nums": [],
        "end_boundaries": [], "match_results": [], "match_result_targets": [],
        "terminated": [], "truncated": [],
        "bootstrap_values": [],
    }
    for trajectory in trajectory_list:
        batch = trajectory.to_batch(config)
        for name, values in batch.items():
            if isinstance(values, torch.Tensor):
                fields[name].extend(values.tolist())
            else:
                fields[name].extend(values)

    advantages = torch.as_tensor(fields["advantages"], dtype=torch.float32)
    fields["advantages"] = (
        (advantages - advantages.mean()) / (advantages.std(unbiased=False) + 1e-8)
    )
    fields["returns"] = torch.as_tensor(fields["returns"], dtype=torch.float32)
    fields["value_targets"] = torch.as_tensor(fields["value_targets"], dtype=torch.float32)
    fields["trajectory_count"] = len(trajectory_list)
    return fields
