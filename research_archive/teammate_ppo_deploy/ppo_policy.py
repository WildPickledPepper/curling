"""Discrete-action PPO policy for high-level curling tactics."""

from dataclasses import dataclass
from typing import Dict, Iterable, Optional, Tuple

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
except ImportError:  # pragma: no cover - allows reward tools without torch.
    torch = None
    nn = None
    F = None

from ppo_actions import N_ACTIONS
from ppo_state_reward import STATE_DIM


@dataclass
class PPOConfig:
    gamma: float = 0.99
    gae_lambda: float = 0.95
    clip_ratio: float = 0.2
    entropy_coef: float = 0.03
    entropy_target_ratio: float = 0.35
    entropy_target_coef: float = 0.05
    value_coef: float = 0.5
    max_grad_norm: float = 0.5
    learning_rate: float = 3e-4
    update_epochs: int = 4
    batch_size: int = 128


def apply_action_mask(logits, action_mask):
    if action_mask is None:
        return logits
    mask = torch.as_tensor(action_mask, dtype=torch.bool, device=logits.device)
    if mask.dim() == 1:
        mask = mask.unsqueeze(0)
    if mask.shape != logits.shape:
        mask = mask.expand_as(logits)
    all_masked = ~mask.any(dim=-1, keepdim=True)
    mask = torch.where(all_masked, torch.ones_like(mask), mask)
    return logits.masked_fill(~mask, -1e9)


def entropy_ratio(entropy_values, action_mask):
    if action_mask is None:
        max_entropy = torch.log(
            torch.as_tensor(float(N_ACTIONS), dtype=torch.float32, device=entropy_values.device)
        )
        return (entropy_values / max_entropy.clamp_min(1e-8)).mean()
    mask = torch.as_tensor(action_mask, dtype=torch.bool, device=entropy_values.device)
    if mask.dim() == 1:
        mask = mask.unsqueeze(0)
    legal_counts = mask.sum(dim=-1).float()
    max_entropy = torch.log(legal_counts.clamp_min(1.0)).clamp_min(1e-8)
    ratios = torch.where(
        legal_counts > 1.0,
        entropy_values / max_entropy,
        torch.ones_like(entropy_values),
    )
    return ratios.mean()


def _no_grad(func):
    if torch is None:
        return func
    return torch.no_grad()(func)


class ActorCritic(nn.Module if nn is not None else object):
    def __init__(self, state_dim: int = STATE_DIM, n_actions: int = N_ACTIONS):
        if nn is None:
            raise ImportError("PyTorch is required for ActorCritic.")
        super().__init__()
        self.body = nn.Sequential(
            nn.Linear(state_dim, 256),
            nn.Tanh(),
            nn.Linear(256, 128),
            nn.Tanh(),
        )
        self.policy_head = nn.Linear(128, n_actions)
        self.value_head = nn.Linear(128, 1)

    def forward(self, states):
        hidden = self.body(states)
        logits = self.policy_head(hidden)
        values = self.value_head(hidden).squeeze(-1)
        return logits, values

    def distribution(self, states, action_mask=None):
        logits, values = self.forward(states)
        logits = apply_action_mask(logits, action_mask)
        return torch.distributions.Categorical(logits=logits), values

    @_no_grad
    def act(self, state, deterministic: bool = False, action_mask=None):
        state_tensor = torch.as_tensor(state, dtype=torch.float32).unsqueeze(0)
        dist, value = self.distribution(state_tensor, action_mask=action_mask)
        if deterministic:
            action = torch.argmax(dist.probs, dim=-1)
        else:
            action = dist.sample()
        log_prob = dist.log_prob(action)
        return int(action.item()), float(log_prob.item()), float(value.item())


def load_compatible_state_dict(model: ActorCritic, state_dict: Dict[str, object]) -> None:
    """Load checkpoints across small state/action-space expansions."""
    if torch is None:
        raise ImportError("PyTorch is required to load PPO checkpoints.")

    target = model.state_dict()
    adapted = {}
    for key, target_value in target.items():
        source_value = state_dict.get(key)
        if source_value is None:
            adapted[key] = target_value
            continue
        if tuple(source_value.shape) == tuple(target_value.shape):
            adapted[key] = source_value
            continue
        if (
            key == "body.0.weight"
            and source_value.dim() == target_value.dim()
            and source_value.shape[0] == target_value.shape[0]
            and source_value.shape[1] <= target_value.shape[1]
        ):
            merged = target_value.clone()
            merged[:, : source_value.shape[1]] = source_value
            adapted[key] = merged
            continue
        if (
            key == "policy_head.weight"
            and source_value.dim() == target_value.dim()
            and source_value.shape[-1] == target_value.shape[-1]
            and source_value.shape[0] <= target_value.shape[0]
        ):
            merged = target_value.clone()
            merged[: source_value.shape[0]] = source_value
            if source_value.shape[0] < target_value.shape[0]:
                merged[source_value.shape[0] :] = 0.0
            adapted[key] = merged
            continue
        if (
            key == "policy_head.bias"
            and source_value.dim() == target_value.dim()
            and source_value.shape[0] <= target_value.shape[0]
        ):
            merged = target_value.clone()
            merged[: source_value.shape[0]] = source_value
            if source_value.shape[0] < target_value.shape[0]:
                merged[source_value.shape[0] :] = -5.0
            adapted[key] = merged
            continue
        raise RuntimeError(
            f"Incompatible checkpoint tensor for {key}: "
            f"checkpoint={tuple(source_value.shape)} model={tuple(target_value.shape)}"
        )
    model.load_state_dict(adapted)


def compute_gae(rewards, dones, values, next_value: float, config: PPOConfig):
    if torch is None:
        raise ImportError("PyTorch is required for compute_gae.")

    rewards = torch.as_tensor(rewards, dtype=torch.float32)
    dones = torch.as_tensor(dones, dtype=torch.float32)
    values = torch.as_tensor(values, dtype=torch.float32)
    advantages = torch.zeros_like(rewards)

    last_advantage = 0.0
    for step in reversed(range(len(rewards))):
        next_non_terminal = 1.0 - dones[step]
        next_values = next_value if step == len(rewards) - 1 else values[step + 1]
        delta = rewards[step] + config.gamma * next_values * next_non_terminal - values[step]
        last_advantage = delta + config.gamma * config.gae_lambda * next_non_terminal * last_advantage
        advantages[step] = last_advantage

    returns = advantages + values
    advantages = (advantages - advantages.mean()) / (advantages.std(unbiased=False) + 1e-8)
    return returns, advantages


def ppo_update(model: ActorCritic, optimizer, rollout: Dict[str, object], config: PPOConfig) -> Dict[str, float]:
    if torch is None:
        raise ImportError("PyTorch is required for ppo_update.")

    states = torch.as_tensor(rollout["states"], dtype=torch.float32)
    actions = torch.as_tensor(rollout["actions"], dtype=torch.long)
    old_log_probs = torch.as_tensor(rollout["log_probs"], dtype=torch.float32)
    returns = torch.as_tensor(rollout["returns"], dtype=torch.float32)
    advantages = torch.as_tensor(rollout["advantages"], dtype=torch.float32)
    action_masks = rollout.get("action_masks")
    if action_masks is not None:
        action_masks = torch.as_tensor(action_masks, dtype=torch.bool)

    n_samples = states.shape[0]
    indices = torch.arange(n_samples)
    last_metrics = {
        "loss": 0.0,
        "policy_loss": 0.0,
        "value_loss": 0.0,
        "entropy": 0.0,
        "entropy_ratio": 0.0,
        "entropy_coef": config.entropy_coef,
        "approx_kl": 0.0,
    }

    for _ in range(config.update_epochs):
        shuffled = indices[torch.randperm(n_samples)]
        for start in range(0, n_samples, config.batch_size):
            batch_idx = shuffled[start : start + config.batch_size]
            batch_masks = action_masks[batch_idx] if action_masks is not None else None
            dist, values = model.distribution(states[batch_idx], action_mask=batch_masks)
            new_log_probs = dist.log_prob(actions[batch_idx])
            entropy_values = dist.entropy()
            entropy = entropy_values.mean()
            entropy_ratio_value = entropy_ratio(entropy_values, batch_masks)
            entropy_coef = config.entropy_coef
            if config.entropy_target_ratio > 0 and config.entropy_target_coef > 0:
                entropy_gap = max(0.0, config.entropy_target_ratio - float(entropy_ratio_value.item()))
                entropy_coef += config.entropy_target_coef * entropy_gap

            ratio = torch.exp(new_log_probs - old_log_probs[batch_idx])
            unclipped = ratio * advantages[batch_idx]
            clipped = torch.clamp(ratio, 1.0 - config.clip_ratio, 1.0 + config.clip_ratio) * advantages[batch_idx]
            policy_loss = -torch.min(unclipped, clipped).mean()
            value_loss = F.mse_loss(values, returns[batch_idx])
            loss = policy_loss + config.value_coef * value_loss - entropy_coef * entropy

            optimizer.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), config.max_grad_norm)
            optimizer.step()

            approx_kl = (old_log_probs[batch_idx] - new_log_probs).mean().item()
            last_metrics = {
                "loss": float(loss.item()),
                "policy_loss": float(policy_loss.item()),
                "value_loss": float(value_loss.item()),
                "entropy": float(entropy.item()),
                "entropy_ratio": float(entropy_ratio_value.item()),
                "entropy_coef": float(entropy_coef),
                "approx_kl": float(approx_kl),
            }

    return last_metrics
