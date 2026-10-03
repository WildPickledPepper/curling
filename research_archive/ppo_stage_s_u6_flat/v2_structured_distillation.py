"""Stage D3 supervised distillation for semantic family and stone slots.

The student keeps frozen Stage C preset and slot heads. D3 trains only a
family head from the teacher's 41-way policy distribution. It writes a
separate checkpoint and is not an inference replacement until its agreement
gate is passed.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Sequence

import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset

from ppo_actions import ACTION_NAMES, N_ACTIONS
from v2_legacy_action_mapper import legacy_to_structured
from v2_set_policy import (
    FAMILY_NAMES,
    N_ACTION_FAMILIES,
    DeepSetsActorCritic,
    load_stage_c_state_dict,
)


_FAMILY_ID_BY_NAME = {name: index for index, name in enumerate(FAMILY_NAMES)}
ACTION_TO_FAMILY = torch.as_tensor([
    _FAMILY_ID_BY_NAME[legacy_to_structured(name).family.value]
    for name in ACTION_NAMES
], dtype=torch.long)


def aggregate_family_probabilities(action_probabilities: torch.Tensor) -> torch.Tensor:
    """Sum a 41-way teacher distribution into the D3 family distribution."""
    if action_probabilities.shape[-1] != N_ACTIONS:
        raise ValueError("expected legacy action probabilities with width %d" % N_ACTIONS)
    mapping = F.one_hot(
        ACTION_TO_FAMILY.to(action_probabilities.device), num_classes=N_ACTION_FAMILIES,
    ).to(dtype=action_probabilities.dtype)
    return action_probabilities @ mapping


def family_mask_from_actions(action_masks: torch.Tensor) -> torch.Tensor:
    if action_masks.shape[-1] != N_ACTIONS:
        raise ValueError("expected legacy action mask with width %d" % N_ACTIONS)
    mapping = F.one_hot(
        ACTION_TO_FAMILY.to(action_masks.device), num_classes=N_ACTION_FAMILIES,
    ).bool()
    return (action_masks.to(torch.bool).unsqueeze(-1) & mapping).any(dim=-2)


def _slot_mask(rows: Sequence[Sequence[bool]], count: int) -> torch.Tensor:
    result = torch.zeros(len(rows), count, dtype=torch.bool)
    for index, row in enumerate(rows):
        if len(row) == count:
            result[index] = torch.as_tensor(row, dtype=torch.bool)
    return result


def _slot_nll(distribution, selected: torch.Tensor) -> torch.Tensor:
    active = selected >= 0
    if not active.any():
        return torch.zeros((), dtype=selected.dtype, device=selected.device).float()
    return -distribution.log_prob(selected)[active].mean()


def _freeze_legacy_preset_parameters(model: DeepSetsActorCritic) -> None:
    """Keep every inherited U6 execution head stable during D3 family distillation."""
    for name, parameter in model.named_parameters():
        parameter.requires_grad = name.startswith("family_heads.")


def structured_distillation_loss(
    model: DeepSetsActorCritic,
    states: torch.Tensor,
    action_masks: torch.Tensor,
    teacher_probs: torch.Tensor,
    behaviour_actions: torch.Tensor,
    target_indices: torch.Tensor,
    target_masks: torch.Tensor,
    middle_indices: torch.Tensor,
    middle_masks: torch.Tensor,
    second_indices: torch.Tensor,
    second_masks: torch.Tensor,
    *,
    family_weight: float,
    target_weight: float,
) -> Dict[str, torch.Tensor]:
    family_targets = aggregate_family_probabilities(teacher_probs)
    family_mask = family_mask_from_actions(action_masks)
    family_log_probs = model.family_distribution(states, family_mask=family_mask).logits
    family_loss = F.kl_div(family_log_probs, family_targets, reduction="batchmean")

    valid_action = behaviour_actions >= 0
    target_active = valid_action & (target_indices >= 0) & target_masks.any(dim=-1)
    target_loss = torch.zeros((), device=states.device)
    if target_active.any():
        distribution = model.target_distribution(
            states[target_active],
            target_mask=target_masks[target_active],
            action_ids=behaviour_actions[target_active],
        )
        target_loss = -distribution.log_prob(target_indices[target_active]).mean()

    relay_active = valid_action & (target_indices >= 0) & (middle_indices >= 0) & middle_masks.any(dim=-1)
    relay_loss = torch.zeros((), device=states.device)
    if relay_active.any():
        distribution = model.relay_distribution(
            states[relay_active],
            middle_mask=middle_masks[relay_active],
            action_ids=behaviour_actions[relay_active],
            target_ids=target_indices[relay_active],
        )
        relay_loss = -distribution.log_prob(middle_indices[relay_active]).mean()

    double_active = valid_action & (target_indices >= 0) & (second_indices >= 0) & second_masks.any(dim=-1)
    double_loss = torch.zeros((), device=states.device)
    if double_active.any():
        distribution = model.double_distribution(
            states[double_active],
            second_target_mask=second_masks[double_active],
            action_ids=behaviour_actions[double_active],
            target_ids=target_indices[double_active],
        )
        double_loss = -distribution.log_prob(second_indices[double_active]).mean()

    slot_loss = target_loss + relay_loss + double_loss
    return {
        "loss": float(family_weight) * family_loss + float(target_weight) * slot_loss,
        "family_loss": family_loss,
        "target_loss": target_loss,
        "relay_loss": relay_loss,
        "double_loss": double_loss,
    }


def train_structured_distillation(
    dataset_path: str | Path,
    output_checkpoint: str | Path,
    *,
    init_checkpoint: str | Path,
    epochs: int = 12,
    batch_size: int = 256,
    learning_rate: float = 3e-4,
    family_weight: float = 1.0,
    target_weight: float = 0.0,
    device: str = "cpu",
) -> Dict[str, float]:
    """Train the D3 student while preserving its inherited preset policy."""
    payload = torch.load(dataset_path, map_location="cpu")
    count = len(payload["stage_c_states"])
    actions = payload.get("behaviour_actions", torch.full((count,), -1, dtype=torch.long))
    targets = payload.get("behaviour_target_indices", torch.full((count,), -1, dtype=torch.long))
    middles = payload.get("behaviour_middle_indices", torch.full((count,), -1, dtype=torch.long))
    seconds = payload.get("behaviour_second_target_indices", torch.full((count,), -1, dtype=torch.long))
    target_masks = _slot_mask(payload.get("behaviour_target_masks", [[]] * count), 16)
    middle_masks = _slot_mask(payload.get("behaviour_middle_masks", [[]] * count), 16)
    second_masks = _slot_mask(payload.get("behaviour_second_target_masks", [[]] * count), 16)
    dataset = TensorDataset(
        payload["stage_c_states"], payload["action_masks"], payload["teacher_probs"],
        actions, targets, target_masks,
        middles, middle_masks,
        seconds, second_masks,
    )
    model = DeepSetsActorCritic().to(device)
    checkpoint = torch.load(init_checkpoint, map_location=device)
    load_stage_c_state_dict(model, checkpoint.get("model", checkpoint))
    _freeze_legacy_preset_parameters(model)
    trainable = [parameter for parameter in model.parameters() if parameter.requires_grad]
    frozen_reference = {
        name: parameter.detach().clone()
        for name, parameter in model.named_parameters()
        if not parameter.requires_grad
    }
    with torch.no_grad():
        initial_states = payload["stage_c_states"].to(device)
        initial_masks = payload["action_masks"].to(device)
        initial_teacher_probs = payload["teacher_probs"].to(device)
        initial_preset_dist, _ = model.distribution(initial_states, action_mask=initial_masks)
        initial_family_dist = model.family_distribution(
            initial_states, family_mask=family_mask_from_actions(initial_masks),
        )
        initial_family_targets = aggregate_family_probabilities(initial_teacher_probs)
        preset_top1_before = float((
            initial_preset_dist.probs.argmax(dim=-1)
            == initial_teacher_probs.argmax(dim=-1)
        ).float().mean())
        preset_kl_before = float(F.kl_div(
            initial_preset_dist.logits, initial_teacher_probs, reduction="batchmean",
        ))
        family_top1_before = float((
            initial_family_dist.probs.argmax(dim=-1)
            == initial_family_targets.argmax(dim=-1)
        ).float().mean())
        family_kl_before = float(F.kl_div(
            initial_family_dist.logits, initial_family_targets, reduction="batchmean",
        ))
    optimizer = torch.optim.Adam(trainable, lr=learning_rate)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    totals = {name: 0.0 for name in ("loss", "family_loss", "target_loss", "relay_loss", "double_loss")}
    model.train()
    for _ in range(max(1, int(epochs))):
        totals = {name: 0.0 for name in totals}
        batches = 0
        for batch in loader:
            tensors = [item.to(device) for item in batch]
            metrics = structured_distillation_loss(
                model, *tensors,
                family_weight=family_weight, target_weight=target_weight,
            )
            optimizer.zero_grad(set_to_none=True)
            metrics["loss"].backward()
            torch.nn.utils.clip_grad_norm_(trainable, 1.0)
            optimizer.step()
            for name in totals:
                totals[name] += float(metrics[name].detach())
            batches += 1
    model.eval()
    with torch.no_grad():
        states = payload["stage_c_states"].to(device)
        masks = payload["action_masks"].to(device)
        teacher_probs = payload["teacher_probs"].to(device)
        preset_dist, _ = model.distribution(states, action_mask=masks)
        family_dist = model.family_distribution(states, family_mask=family_mask_from_actions(masks))
        family_targets = aggregate_family_probabilities(teacher_probs)
        metrics = {name: value / max(1, batches) for name, value in totals.items()}
        metrics.update({
            "preset_top1_before": preset_top1_before,
            "preset_kl_before": preset_kl_before,
            "family_top1_before": family_top1_before,
            "family_kl_before": family_kl_before,
            "preset_top1_agreement": float((
                preset_dist.probs.argmax(dim=-1) == teacher_probs.argmax(dim=-1)
            ).float().mean()),
            "preset_kl": float(F.kl_div(preset_dist.logits, teacher_probs, reduction="batchmean")),
            "family_top1_agreement": float((
                family_dist.probs.argmax(dim=-1) == family_targets.argmax(dim=-1)
            ).float().mean()),
            "family_kl": float(F.kl_div(family_dist.logits, family_targets, reduction="batchmean")),
            "target_supervision_count": float((targets >= 0).sum()),
            "target_nontrivial_choice_count": float(((targets >= 0) & (target_masks.sum(dim=-1) > 1)).sum()),
            "relay_supervision_count": float((middles >= 0).sum()),
            "relay_nontrivial_choice_count": float(((middles >= 0) & (middle_masks.sum(dim=-1) > 1)).sum()),
            "double_supervision_count": float((seconds >= 0).sum()),
            "double_nontrivial_choice_count": float(((seconds >= 0) & (second_masks.sum(dim=-1) > 1)).sum()),
            "legacy_parameter_delta_max": max(
                float((parameter.detach() - frozen_reference[name]).abs().max())
                for name, parameter in model.named_parameters()
                if name in frozen_reference
            ),
        })
    output = Path(output_checkpoint)
    output.parent.mkdir(parents=True, exist_ok=True)
    torch.save({
        "version": "stage_d3_structured_distillation_v2_family_only",
        "model": model.state_dict(),
        "metrics": metrics,
        "initial_checkpoint": str(init_checkpoint),
        "family_names": FAMILY_NAMES,
        "frozen_legacy_execution": True,
    }, output)
    return metrics
