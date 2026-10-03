"""PPO V2 update using the unchanged V1 ActorCritic architecture."""

from __future__ import annotations

from typing import Dict, Optional

import torch
import torch.nn.functional as F

from ppo_policy import ActorCritic, entropy_ratio
from v2_config import V2PPOConfig
from v2_diagnostics import explained_variance, pre_update_policy_diagnostics
from v2_set_policy import D5_DIRECT_TARGET_ACTION_IDS


def choose_action(model: ActorCritic, state, action_mask, deterministic: bool = False):
    """Sample from the exact distribution later used by PPO, with no logit bias."""
    return model.act(state, deterministic=deterministic, action_mask=action_mask)


def ppo_update_v2(
    model: ActorCritic,
    optimizer: torch.optim.Optimizer,
    batch: Dict[str, object],
    config: V2PPOConfig,
    *,
    device: str = "cpu",
    reference_model: Optional[ActorCritic] = None,
) -> Dict[str, float]:
    """Update PPO and report both pre-update and optimisation diagnostics."""
    model.to(device)
    model.train()
    states = torch.as_tensor(batch["states"], dtype=torch.float32, device=device)
    actions = torch.as_tensor(batch["actions"], dtype=torch.long, device=device)
    masks = torch.as_tensor(batch["action_masks"], dtype=torch.bool, device=device)
    action_logit_biases = torch.as_tensor(
        batch.get("action_logit_biases", [[0.0] * masks.shape[1]] * len(batch["actions"])),
        dtype=torch.float32,
        device=device,
    )
    raw_target_indices = batch.get("target_indices", [-1] * len(batch["actions"]))
    target_indices = torch.as_tensor(raw_target_indices, dtype=torch.long, device=device)
    raw_target_masks = batch.get("target_masks", [[] for _ in batch["actions"]])
    target_masks = torch.as_tensor(
        [list(mask) if len(mask) == 16 else [False] * 16 for mask in raw_target_masks],
        dtype=torch.bool,
        device=device,
    )
    target_reference_indices = torch.as_tensor(
        batch.get("target_reference_indices", [-1] * len(batch["actions"])),
        dtype=torch.long,
        device=device,
    )
    middle_indices = torch.as_tensor(
        batch.get("middle_indices", [-1] * len(batch["actions"])), dtype=torch.long, device=device,
    )
    raw_middle_masks = batch.get("middle_masks", [[] for _ in batch["actions"]])
    middle_masks = torch.as_tensor(
        [list(mask) if len(mask) == 16 else [False] * 16 for mask in raw_middle_masks],
        dtype=torch.bool, device=device,
    )
    second_target_indices = torch.as_tensor(
        batch.get("second_target_indices", [-1] * len(batch["actions"])), dtype=torch.long, device=device,
    )
    raw_second_target_masks = batch.get("second_target_masks", [[] for _ in batch["actions"]])
    second_target_masks = torch.as_tensor(
        [list(mask) if len(mask) == 16 else [False] * 16 for mask in raw_second_target_masks],
        dtype=torch.bool, device=device,
    )
    old_log_probs = torch.as_tensor(batch["log_probs"], dtype=torch.float32, device=device)
    returns = torch.as_tensor(batch["returns"], dtype=torch.float32, device=device)
    value_targets = torch.as_tensor(
        batch.get("value_targets", batch["returns"]), dtype=torch.float32, device=device
    )
    old_values = torch.as_tensor(batch["values"], dtype=torch.float32, device=device)
    advantages = torch.as_tensor(batch["advantages"], dtype=torch.float32, device=device)
    terminal_scores = torch.as_tensor(
        batch.get("terminal_scores", [-100] * len(batch["actions"])),
        dtype=torch.long,
        device=device,
    )
    match_result_targets = torch.as_tensor(
        batch.get("match_result_targets", [-100] * len(batch["actions"])),
        dtype=torch.long,
        device=device,
    )
    pre_metrics = pre_update_policy_diagnostics(
        model,
        batch,
        device=device,
        use_d5_target_residual=config.d5_target_residual,
    )
    pre_metrics["value_target_mean"] = float(value_targets.mean())
    pre_metrics["value_target_std"] = float(value_targets.std(unbiased=False))
    pre_metrics["value_mae_before_update"] = float((old_values - value_targets).abs().mean())
    sample_count = states.shape[0]
    if sample_count == 0:
        raise ValueError("Cannot update PPO V2 from an empty batch.")

    totals = {
        "loss": 0.0, "policy_loss": 0.0, "value_loss": 0.0,
        "entropy": 0.0, "entropy_ratio": 0.0, "entropy_coef": 0.0,
        "approx_kl": 0.0, "clip_fraction": 0.0, "gradient_norm": 0.0,
        "score_loss": 0.0, "score_accuracy": 0.0,
        "match_loss": 0.0, "match_accuracy": 0.0,
        "value_clip_fraction": 0.0,
        "warmstart_kl": 0.0,
        "target_entropy": 0.0, "target_sample_rate": 0.0,
        "target_anchor_kl": 0.0,
        "relay_entropy": 0.0, "relay_sample_rate": 0.0,
        "double_entropy": 0.0, "double_sample_rate": 0.0,
        "batches": 0,
    }
    d5_action_ids = torch.as_tensor(
        sorted(D5_DIRECT_TARGET_ACTION_IDS), dtype=torch.long, device=device,
    )
    d5_target_active = (target_indices >= 0) & (actions.unsqueeze(-1) == d5_action_ids).any(dim=-1)
    d5_target_nontrivial = d5_target_active & (target_masks.sum(dim=-1) > 1)
    totals["d5_target_active_samples"] = float(d5_target_active.sum().item())
    totals["d5_target_nontrivial_samples"] = float(d5_target_nontrivial.sum().item())
    indices = torch.arange(sample_count, device=device)
    for _ in range(config.update_epochs):
        shuffled = indices[torch.randperm(sample_count, device=device)]
        for start in range(0, sample_count, config.batch_size):
            index = shuffled[start : start + config.batch_size]
            dist, values = model.distribution(
                states[index],
                action_mask=masks[index],
                action_logit_bias=action_logit_biases[index],
            )
            new_log_probs = dist.log_prob(actions[index])
            entropy_values = dist.entropy()
            minibatch_targets = target_indices[index]
            target_active = minibatch_targets >= 0
            target_entropy = torch.zeros((), dtype=values.dtype, device=device)
            target_anchor_kl = torch.zeros((), dtype=values.dtype, device=device)
            if target_active.any():
                if not hasattr(model, "target_distribution"):
                    raise ValueError("target-conditioned trajectory requires a target-capable model")
                active_states = states[index][target_active]
                active_masks = target_masks[index][target_active]
                target_dist = model.target_distribution(
                    active_states,
                    target_mask=active_masks,
                    action_ids=actions[index][target_active],
                    use_d5_residual=config.d5_target_residual,
                    legacy_target_ids=target_reference_indices[index][target_active],
                )
                selected_targets = minibatch_targets[target_active]
                new_log_probs = new_log_probs.clone()
                new_log_probs[target_active] += target_dist.log_prob(selected_targets)
                entropy_values = entropy_values.clone()
                target_entropies = target_dist.entropy()
                entropy_values[target_active] += target_entropies
                target_entropy = target_entropies.mean()
                if config.d5_target_residual:
                    if reference_model is None:
                        raise ValueError("D5 target residual PPO requires a frozen reference model")
                    with torch.no_grad():
                        reference_target_dist = reference_model.target_distribution(
                            active_states,
                            target_mask=active_masks,
                            action_ids=actions[index][target_active],
                            use_d5_residual=False,
                            legacy_target_ids=target_reference_indices[index][target_active],
                        )
                    d5_active_here = (
                        (actions[index][target_active].unsqueeze(-1) == d5_action_ids).any(dim=-1)
                        & (active_masks.sum(dim=-1) > 1)
                    )
                    if d5_active_here.any():
                        target_anchor_kl = torch.distributions.kl_divergence(
                            target_dist, reference_target_dist
                        )[d5_active_here].mean()
            minibatch_middles = middle_indices[index]
            relay_active = minibatch_middles >= 0
            relay_entropy = torch.zeros((), dtype=values.dtype, device=device)
            if relay_active.any():
                if not hasattr(model, "relay_distribution"):
                    raise ValueError("relay-conditioned trajectory requires a relay-capable model")
                relay_dist = model.relay_distribution(
                    states[index][relay_active],
                    middle_mask=middle_masks[index][relay_active],
                    action_ids=actions[index][relay_active],
                    target_ids=target_indices[index][relay_active],
                )
                selected_middles = minibatch_middles[relay_active]
                new_log_probs = new_log_probs.clone()
                new_log_probs[relay_active] += relay_dist.log_prob(selected_middles)
                entropy_values = entropy_values.clone()
                relay_entropies = relay_dist.entropy()
                entropy_values[relay_active] += relay_entropies
                relay_entropy = relay_entropies.mean()
            minibatch_seconds = second_target_indices[index]
            double_active = minibatch_seconds >= 0
            double_entropy = torch.zeros((), dtype=values.dtype, device=device)
            if double_active.any():
                if not hasattr(model, "double_distribution"):
                    raise ValueError("double-conditioned trajectory requires a double-capable model")
                double_dist = model.double_distribution(
                    states[index][double_active],
                    second_target_mask=second_target_masks[index][double_active],
                    action_ids=actions[index][double_active],
                    target_ids=target_indices[index][double_active],
                )
                selected_seconds = minibatch_seconds[double_active]
                new_log_probs = new_log_probs.clone()
                new_log_probs[double_active] += double_dist.log_prob(selected_seconds)
                entropy_values = entropy_values.clone()
                double_entropies = double_dist.entropy()
                entropy_values[double_active] += double_entropies
                double_entropy = double_entropies.mean()
            if config.d5_target_residual:
                d5_policy_active = d5_target_nontrivial[index]
                # Only these terms can change under D5.1.  Retaining the
                # remaining frozen action/value losses would merely dilute the
                # target-selection gradient and can leave a minibatch without
                # a differentiable loss.
                if not d5_policy_active.any():
                    continue
                entropy = entropy_values[d5_policy_active].mean()
                relative_entropy = torch.zeros((), dtype=values.dtype, device=device)
            else:
                d5_policy_active = None
                entropy = entropy_values.mean()
                relative_entropy = entropy_ratio(entropy_values, masks[index])
            entropy_bonus = config.entropy_coef
            if (
                not config.d5_target_residual
                and config.entropy_target_ratio > 0.0
                and config.entropy_target_coef > 0.0
            ):
                entropy_bonus += config.entropy_target_coef * max(
                    0.0, config.entropy_target_ratio - float(relative_entropy.detach())
                )
            if d5_policy_active is not None:
                policy_new_log_probs = new_log_probs[d5_policy_active]
                policy_old_log_probs = old_log_probs[index][d5_policy_active]
                policy_advantages = advantages[index][d5_policy_active]
            else:
                policy_new_log_probs = new_log_probs
                policy_old_log_probs = old_log_probs[index]
                policy_advantages = advantages[index]
            ratio = torch.exp(policy_new_log_probs - policy_old_log_probs)
            unclipped = ratio * policy_advantages
            clipped = torch.clamp(ratio, 1.0 - config.clip_ratio, 1.0 + config.clip_ratio) * policy_advantages
            policy_loss = -torch.minimum(unclipped, clipped).mean()
            value_loss_unclipped = F.smooth_l1_loss(
                values, value_targets[index], reduction="none", beta=config.value_huber_delta
            )
            value_clip_fraction = torch.zeros((), dtype=values.dtype, device=device)
            if config.value_clip_ratio > 0.0:
                clipped_values = old_values[index] + torch.clamp(
                    values - old_values[index],
                    -config.value_clip_ratio,
                    config.value_clip_ratio,
                )
                value_loss_clipped = F.smooth_l1_loss(
                    clipped_values,
                    value_targets[index],
                    reduction="none",
                    beta=config.value_huber_delta,
                )
                value_loss = torch.maximum(value_loss_unclipped, value_loss_clipped).mean()
                value_clip_fraction = (
                    torch.abs(values - old_values[index]) > config.value_clip_ratio
                ).float().mean()
            else:
                value_loss = value_loss_unclipped.mean()
            score_loss = torch.zeros((), dtype=values.dtype, device=device)
            score_accuracy = torch.zeros((), dtype=values.dtype, device=device)
            match_loss = torch.zeros((), dtype=values.dtype, device=device)
            match_accuracy = torch.zeros((), dtype=values.dtype, device=device)
            warmstart_kl = torch.zeros((), dtype=values.dtype, device=device)
            forward_outputs = model.forward(states[index])
            if isinstance(forward_outputs, tuple) and len(forward_outputs) >= 3:
                score_logits = forward_outputs[2]
                labelled = terminal_scores[index] >= -8
                if labelled.any():
                    score_targets = terminal_scores[index][labelled] + 8
                    score_loss = F.cross_entropy(score_logits[labelled], score_targets)
                    score_accuracy = (
                        score_logits[labelled].argmax(dim=-1) == score_targets
                    ).float().mean()
                if len(forward_outputs) >= 4:
                    match_logits = forward_outputs[3]
                    match_labelled = match_result_targets[index] >= -1
                    if match_labelled.any():
                        match_targets = match_result_targets[index][match_labelled] + 1
                        match_loss = F.cross_entropy(
                            match_logits[match_labelled], match_targets
                        )
                        match_accuracy = (
                            match_logits[match_labelled].argmax(dim=-1) == match_targets
                        ).float().mean()
            if reference_model is not None and config.warmstart_kl_coef > 0.0:
                with torch.no_grad():
                    reference_dist, _ = reference_model.distribution(
                        states[index], action_mask=masks[index],
                        action_logit_bias=action_logit_biases[index],
                    )
                warmstart_kl = torch.distributions.kl_divergence(
                    dist, reference_dist
                ).mean()
            if config.d5_target_residual:
                loss = policy_loss + config.d5_target_kl_coef * target_anchor_kl - entropy_bonus * entropy
            else:
                loss = (
                    policy_loss
                    + config.value_coef * value_loss
                    + config.score_aux_coef * score_loss
                    + config.match_aux_coef * match_loss
                    + config.warmstart_kl_coef * warmstart_kl
                    - entropy_bonus * entropy
                )

            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            trainable_parameters = [parameter for parameter in model.parameters() if parameter.requires_grad]
            gradient_norm = torch.nn.utils.clip_grad_norm_(trainable_parameters, config.max_grad_norm)
            optimizer.step()

            totals["loss"] += float(loss.detach())
            totals["policy_loss"] += float(policy_loss.detach())
            totals["value_loss"] += float(value_loss.detach())
            totals["entropy"] += float(entropy.detach())
            totals["entropy_ratio"] += float(relative_entropy.detach())
            totals["entropy_coef"] += entropy_bonus
            totals["approx_kl"] += float((policy_old_log_probs - policy_new_log_probs).mean().detach())
            totals["clip_fraction"] += float((torch.abs(ratio - 1.0) > config.clip_ratio).float().mean().detach())
            totals["gradient_norm"] += float(gradient_norm)
            totals["score_loss"] += float(score_loss.detach())
            totals["score_accuracy"] += float(score_accuracy.detach())
            totals["match_loss"] += float(match_loss.detach())
            totals["match_accuracy"] += float(match_accuracy.detach())
            totals["value_clip_fraction"] += float(value_clip_fraction.detach())
            totals["warmstart_kl"] += float(warmstart_kl.detach())
            totals["target_entropy"] += float(target_entropy.detach())
            totals["target_anchor_kl"] += float(target_anchor_kl.detach())
            totals["target_sample_rate"] += float(target_active.float().mean().detach())
            totals["relay_entropy"] += float(relay_entropy.detach())
            totals["relay_sample_rate"] += float(relay_active.float().mean().detach())
            totals["double_entropy"] += float(double_entropy.detach())
            totals["double_sample_rate"] += float(double_active.float().mean().detach())
            totals["batches"] += 1

    d5_active_samples = totals.pop("d5_target_active_samples")
    d5_nontrivial_samples = totals.pop("d5_target_nontrivial_samples")
    divisor = max(1, totals.pop("batches"))
    metrics = {name: value / divisor for name, value in totals.items()}
    metrics["d5_target_active_samples"] = d5_active_samples
    metrics["d5_target_nontrivial_samples"] = d5_nontrivial_samples
    if config.d5_target_residual:
        if reference_model is None:
            raise ValueError("D5 target residual PPO requires a frozen reference model")
        if d5_target_nontrivial.any():
            with torch.no_grad():
                eligible_states = states[d5_target_nontrivial]
                eligible_masks = target_masks[d5_target_nontrivial]
                eligible_actions = actions[d5_target_nontrivial]
                post_target_dist = model.target_distribution(
                    eligible_states,
                    target_mask=eligible_masks,
                action_ids=eligible_actions,
                use_d5_residual=True,
                legacy_target_ids=target_reference_indices[d5_target_nontrivial],
                )
                reference_target_dist = reference_model.target_distribution(
                    eligible_states,
                    target_mask=eligible_masks,
                action_ids=eligible_actions,
                use_d5_residual=False,
                legacy_target_ids=target_reference_indices[d5_target_nontrivial],
                )
                post_probabilities = post_target_dist.probs
                reference_probabilities = reference_target_dist.probs
                metrics["d5_target_post_kl"] = float(torch.distributions.kl_divergence(
                    post_target_dist, reference_target_dist
                ).mean())
                metrics["d5_target_argmax_change_rate"] = float((
                    post_probabilities.argmax(dim=-1) != reference_probabilities.argmax(dim=-1)
                ).float().mean())
                metrics["d5_target_mean_total_variation"] = float(
                    0.5 * torch.abs(post_probabilities - reference_probabilities).sum(dim=-1).mean()
                )
        else:
            metrics["d5_target_post_kl"] = 0.0
            metrics["d5_target_argmax_change_rate"] = 0.0
            metrics["d5_target_mean_total_variation"] = 0.0
        residual_parameters = [
            parameter.detach()
            for name, parameter in model.named_parameters()
            if name.startswith((
                "target_residual_heads.", "target_guard_residual_heads.", "target_roll_residual_heads.",
            ))
        ]
        metrics["d5_residual_max_abs"] = max(
            (float(parameter.abs().max()) for parameter in residual_parameters), default=0.0,
        )
    with torch.no_grad():
        _, values_after = model.distribution(
            states, action_mask=masks, action_logit_bias=action_logit_biases,
        )
    metrics["explained_variance"] = explained_variance(values_after, value_targets)
    metrics["value_mean_after_update"] = float(values_after.mean())
    metrics["value_mae_after_update"] = float((values_after - value_targets).abs().mean())
    metrics.update(pre_metrics)
    model.eval()
    return metrics
