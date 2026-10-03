"""Numerical checks required before running a PPO V2 long training job."""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from typing import Dict, Optional

import torch

from ppo_actions import action_name
from ppo_rollout import HIT_ACTIONS, SETUP_ACTIONS


def explained_variance(prediction: torch.Tensor, target: torch.Tensor) -> float:
    target_variance = torch.var(target, unbiased=False)
    if float(target_variance) < 1e-8:
        return 0.0
    return float(1.0 - torch.var(target - prediction, unbiased=False) / target_variance)


@torch.no_grad()
def pre_update_policy_diagnostics(
    model,
    batch: Dict[str, object],
    device: str = "cpu",
    *,
    use_d5_target_residual: bool = False,
) -> Dict[str, object]:
    """Measure behaviour-policy agreement before the first optimizer step."""
    states = torch.as_tensor(batch["states"], dtype=torch.float32, device=device)
    actions = torch.as_tensor(batch["actions"], dtype=torch.long, device=device)
    masks = torch.as_tensor(batch["action_masks"], dtype=torch.bool, device=device)
    action_logit_biases = torch.as_tensor(
        batch.get("action_logit_biases", [[0.0] * masks.shape[1]] * len(actions)),
        dtype=torch.float32,
        device=device,
    )
    old_log_probs = torch.as_tensor(batch["log_probs"], dtype=torch.float32, device=device)
    dist, values = model.distribution(
        states, action_mask=masks, action_logit_bias=action_logit_biases,
    )
    new_log_probs = dist.log_prob(actions)
    target_indices = torch.as_tensor(
        batch.get("target_indices", [-1] * len(batch["actions"])),
        dtype=torch.long,
        device=device,
    )
    target_reference_indices = torch.as_tensor(
        batch.get("target_reference_indices", [-1] * len(batch["actions"])),
        dtype=torch.long,
        device=device,
    )
    raw_target_masks = batch.get("target_masks", [[] for _ in batch["actions"]])
    target_active = target_indices >= 0
    if target_active.any():
        if not hasattr(model, "target_distribution"):
            raise ValueError("target-conditioned batch requires a target-capable model")
        target_masks = torch.as_tensor(
            [list(mask) if len(mask) == 16 else [False] * 16 for mask in raw_target_masks],
            dtype=torch.bool,
            device=device,
        )
        target_dist = model.target_distribution(
            states[target_active],
            target_mask=target_masks[target_active],
            action_ids=actions[target_active],
            use_d5_residual=use_d5_target_residual,
            legacy_target_ids=target_reference_indices[target_active],
        )
        new_log_probs = new_log_probs.clone()
        new_log_probs[target_active] += target_dist.log_prob(target_indices[target_active])
    middle_indices = torch.as_tensor(
        batch.get("middle_indices", [-1] * len(batch["actions"])), dtype=torch.long, device=device,
    )
    relay_active = middle_indices >= 0
    if relay_active.any():
        if not hasattr(model, "relay_distribution"):
            raise ValueError("relay-conditioned batch requires a relay-capable model")
        raw_middle_masks = batch.get("middle_masks", [[] for _ in batch["actions"]])
        middle_masks = torch.as_tensor(
            [list(mask) if len(mask) == 16 else [False] * 16 for mask in raw_middle_masks],
            dtype=torch.bool, device=device,
        )
        relay_dist = model.relay_distribution(
            states[relay_active],
            middle_mask=middle_masks[relay_active],
            action_ids=actions[relay_active],
            target_ids=target_indices[relay_active],
        )
        new_log_probs = new_log_probs.clone()
        new_log_probs[relay_active] += relay_dist.log_prob(middle_indices[relay_active])
    second_target_indices = torch.as_tensor(
        batch.get("second_target_indices", [-1] * len(batch["actions"])),
        dtype=torch.long,
        device=device,
    )
    double_active = second_target_indices >= 0
    if double_active.any():
        if not hasattr(model, "double_distribution"):
            raise ValueError("double-conditioned batch requires a double-capable model")
        raw_second_target_masks = batch.get("second_target_masks", [[] for _ in batch["actions"]])
        second_target_masks = torch.as_tensor(
            [list(mask) if len(mask) == 16 else [False] * 16 for mask in raw_second_target_masks],
            dtype=torch.bool,
            device=device,
        )
        double_dist = model.double_distribution(
            states[double_active],
            second_target_mask=second_target_masks[double_active],
            action_ids=actions[double_active],
            target_ids=target_indices[double_active],
        )
        new_log_probs = new_log_probs.clone()
        new_log_probs[double_active] += double_dist.log_prob(second_target_indices[double_active])
    log_ratio = new_log_probs - old_log_probs
    ratios = torch.exp(log_ratio)
    deterministic_actions = torch.argmax(dist.probs, dim=-1).cpu().tolist()
    deterministic_names = [action_name(int(action)) for action in deterministic_actions]
    deterministic_counts = Counter(deterministic_names)
    probabilities = [
        count / max(1, len(deterministic_names))
        for count in deterministic_counts.values()
    ]
    shot_nums = [int(value) for value in batch.get("shot_nums", [])]
    late_names = [
        name for name, shot_num in zip(deterministic_names, shot_nums)
        if shot_num >= 12
    ]
    # This is the same first-order KL estimator convention used by PPO logs.
    approx_kl = (old_log_probs - new_log_probs).mean()
    return {
        "ratio_mean_before_update": float(ratios.mean()),
        "ratio_std_before_update": float(ratios.std(unbiased=False)),
        "approx_kl_before_update": float(approx_kl),
        "value_mean_before_update": float(values.mean()),
        "deterministic_unique_actions": float(len(deterministic_counts)),
        "deterministic_effective_actions": float(math.exp(-sum(
            probability * math.log(probability) for probability in probabilities
        ))) if probabilities else 0.0,
        "deterministic_top_action_rate": float(
            max(deterministic_counts.values()) / len(deterministic_names)
        ) if deterministic_names else 0.0,
        "deterministic_top_actions": "/".join(
            f"{name}:{count / len(deterministic_names):.3f}"
            for name, count in deterministic_counts.most_common(8)
        ) if deterministic_names else "none",
        "deterministic_hit_rate": float(
            sum(name in HIT_ACTIONS for name in deterministic_names) / len(deterministic_names)
        ) if deterministic_names else 0.0,
        "deterministic_setup_rate": float(
            sum(name in SETUP_ACTIONS for name in deterministic_names) / len(deterministic_names)
        ) if deterministic_names else 0.0,
        "deterministic_late_hit_rate": float(
            sum(name in HIT_ACTIONS for name in late_names) / len(late_names)
        ) if late_names else 0.0,
    }


def _wld_summary(batch: Dict[str, object], field: str) -> str:
    results = defaultdict(lambda: [0, 0, 0])
    for result, group in zip(batch.get("match_results", []), batch.get(field, [])):
        result = int(result)
        if result == -100:
            continue
        index = 0 if result > 0 else 1 if result < 0 else 2
        results[str(group)][index] += 1
    return "/".join(
        f"{group}:{values[0]}-{values[1]}-{values[2]}"
        for group, values in sorted(results.items())
    ) or "none"


def _reward_component_summary(batch: Dict[str, object]) -> str:
    component_rows = batch.get("reward_components", [])
    names = sorted({name for row in component_rows for name in row})
    absolute_total = sum(abs(float(value)) for row in component_rows for value in row.values())
    parts = []
    for name in names:
        values = [float(row.get(name, 0.0)) for row in component_rows]
        mean = sum(values) / max(1, len(values))
        share = sum(abs(value) for value in values) / max(1e-12, absolute_total)
        parts.append(f"{name}:{mean:.3f}@{share:.2f}")
    return "/".join(parts) or "none"


def batch_diagnostics(batch: Dict[str, object]) -> Dict[str, object]:
    bootstrap_values = batch.get("bootstrap_values", [])
    rewards = batch.get("rewards", [])
    action_names = batch.get("action_names", [])
    action_counts = Counter(action_names)
    action_probabilities = [count / max(1, len(action_names)) for count in action_counts.values()]
    flags = batch.get("outcome_flags", [])
    bypass_draw_attempts = sum(bool(item.get("bypass_draw_attempt")) for item in flags)
    bypass_takeout_attempts = sum(bool(item.get("bypass_takeout_attempt")) for item in flags)
    blocked_threats = sum(bool(item.get("blocked_multi_stone_threat")) for item in flags)
    blocked_bypass_attempts = sum(bool(item.get("blocked_threat_bypass_attempt")) for item in flags)
    late_multi_stone_threats = sum(bool(item.get("late_multi_stone_threat")) for item in flags)
    match_results = [
        int(value) for value in batch.get("match_results", []) if int(value) != -100
    ]
    return {
        "samples": float(len(batch["actions"])),
        "trajectory_count": float(batch.get("trajectory_count", 0)),
        "terminated_count": float(sum(batch.get("terminated", []))),
        "truncated_count": float(sum(batch.get("truncated", []))),
        "end_boundary_count": float(sum(batch.get("end_boundaries", []))),
        "completed_matches": float(len(match_results)),
        "match_win_rate": float(sum(value > 0 for value in match_results) / len(match_results))
        if match_results else 0.0,
        "opponent_wld": _wld_summary(batch, "opponent_names"),
        "role_wld": _wld_summary(batch, "candidate_roles"),
        "bootstrap_value_mean": float(sum(bootstrap_values) / len(bootstrap_values))
        if bootstrap_values else 0.0,
        "mean_reward": float(sum(rewards) / len(rewards)) if rewards else 0.0,
        "reward_components": _reward_component_summary(batch),
        "positive_reward_rate": float(sum(value > 0.0 for value in rewards) / len(rewards)) if rewards else 0.0,
        "negative_reward_rate": float(sum(value < 0.0 for value in rewards) / len(rewards)) if rewards else 0.0,
        "unique_actions": float(len(action_counts)),
        "effective_actions": float(math.exp(-sum(prob * math.log(prob) for prob in action_probabilities)))
        if action_probabilities else 0.0,
        "top_action_rate": float(max(action_counts.values()) / len(action_names)) if action_names else 0.0,
        "top_actions": "/".join(
            f"{name}:{count / len(action_names):.3f}"
            for name, count in action_counts.most_common(8)
        ) if action_names else "none",
        "hit_rate": float(sum(name in HIT_ACTIONS for name in action_names) / len(action_names))
        if action_names else 0.0,
        "setup_rate": float(sum(name in SETUP_ACTIONS for name in action_names) / len(action_names))
        if action_names else 0.0,
        "invalid_action_rate": float(sum(bool(item.get("invalid_action")) for item in flags) / len(flags)) if flags else 0.0,
        "fallback_draw_rate": float(sum(bool(item.get("fallback_draw")) for item in flags) / len(flags)) if flags else 0.0,
        "bypass_draw_success_rate": float(
            sum(bool(item.get("bypass_draw_success")) for item in flags) / max(1, bypass_draw_attempts)
        ),
        "bypass_takeout_success_rate": float(
            sum(bool(item.get("bypass_takeout_success")) for item in flags) / max(1, bypass_takeout_attempts)
        ),
        "blocked_threat_rate": float(blocked_threats / len(flags)) if flags else 0.0,
        "blocked_threat_bypass_rate": float(blocked_bypass_attempts / max(1, blocked_threats)),
        "blocked_threat_bypass_success_rate": float(
            sum(bool(item.get("blocked_threat_bypass_success")) for item in flags)
            / max(1, blocked_bypass_attempts)
        ),
        "blocked_threat_improvement_rate": float(
            sum(bool(item.get("blocked_threat_improved")) for item in flags)
            / max(1, blocked_threats)
        ),
        "guard_only_failure_rate": float(
            sum(bool(item.get("guard_only_failure")) for item in flags)
            / max(1, blocked_threats)
        ),
        "late_multi_stone_threat_rate": float(late_multi_stone_threats / len(flags)) if flags else 0.0,
        "late_multi_stone_hit_rate": float(
            sum(bool(item.get("late_multi_stone_hit_attempt")) for item in flags)
            / max(1, late_multi_stone_threats)
        ),
        "late_multi_stone_setup_rate": float(
            sum(bool(item.get("late_multi_stone_setup_attempt")) for item in flags)
            / max(1, late_multi_stone_threats)
        ),
        "late_multi_stone_improvement_rate": float(
            sum(bool(item.get("late_multi_stone_threat_improved")) for item in flags)
            / max(1, late_multi_stone_threats)
        ),
        "late_multi_stone_nonproductive_hit_rate": float(
            sum(bool(item.get("late_multi_stone_nonproductive_hit")) for item in flags)
            / max(1, late_multi_stone_threats)
        ),
        "late_multi_stone_guard_only_failure_rate": float(
            sum(bool(item.get("late_multi_stone_guard_only_failure")) for item in flags)
            / max(1, late_multi_stone_threats)
        ),
    }
