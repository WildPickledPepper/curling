"""Stage D4.1 factorised family -> preset decision helpers.

The action probability is represented as
``P(family) * P(legacy preset | family)``.  Target, relay and double slots
remain conditioned on the chosen legacy preset and continue to use the frozen
U6 heads.  This module does not replace the live collector by itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import torch

from ppo_actions import ACTION_NAMES, N_ACTIONS, action_name
from v2_legacy_action_mapper import legacy_to_structured
from v2_set_policy import FAMILY_NAMES, DeepSetsActorCritic
from v2_structured_distillation import family_mask_from_actions


_FAMILY_INDEX = {name: index for index, name in enumerate(FAMILY_NAMES)}
ACTION_FAMILY_IDS = torch.as_tensor([
    _FAMILY_INDEX[legacy_to_structured(name).family.value]
    for name in ACTION_NAMES
], dtype=torch.long)


@dataclass(frozen=True)
class FactorisedAction:
    family_id: int
    family_name: str
    preset_id: int
    preset_name: str
    family_source: str
    log_prob: float
    value: float


def _as_mask(action_mask, *, device) -> torch.Tensor:
    mask = torch.as_tensor(action_mask, dtype=torch.bool, device=device)
    if mask.ndim == 1:
        mask = mask.unsqueeze(0)
    if mask.shape[-1] != N_ACTIONS:
        raise ValueError("expected a %d-wide legacy action mask" % N_ACTIONS)
    return mask


def preset_mask_for_family(action_mask, family_id: int, *, device) -> torch.Tensor:
    mask = _as_mask(action_mask, device=device)
    family_ids = ACTION_FAMILY_IDS.to(device)
    result = mask & (family_ids.unsqueeze(0) == int(family_id))
    if not result.any(dim=-1).all():
        raise ValueError("selected family has no legal legacy preset")
    return result


def factorized_action_probabilities(
    model: DeepSetsActorCritic,
    states: torch.Tensor,
    action_mask,
    *,
    family_source: str = "learned",
) -> torch.Tensor:
    """Return induced 41-way probabilities from D4 family/preset factors."""
    mask = _as_mask(action_mask, device=states.device)
    legacy_dist, _ = model.distribution(states, action_mask=mask)
    family_ids = ACTION_FAMILY_IDS.to(states.device)
    if family_source == "legacy_exact":
        family_probs = torch.zeros(
            legacy_dist.probs.shape[0], len(FAMILY_NAMES),
            dtype=legacy_dist.probs.dtype, device=states.device,
        )
        for family_id in range(len(FAMILY_NAMES)):
            family_probs[:, family_id] = legacy_dist.probs[:, family_ids == family_id].sum(dim=-1)
    elif family_source == "learned":
        family_probs = model.family_distribution(
            states, family_mask=family_mask_from_actions(mask),
        ).probs
    else:
        raise ValueError("family_source must be 'legacy_exact' or 'learned'")
    result = torch.zeros_like(legacy_dist.probs)
    for family_id in range(len(FAMILY_NAMES)):
        family_actions = mask & (family_ids.unsqueeze(0) == family_id)
        active = family_actions.any(dim=-1)
        if not active.any():
            continue
        conditional = legacy_dist.probs[active] * family_actions[active]
        conditional = conditional / conditional.sum(dim=-1, keepdim=True).clamp_min(1e-12)
        result[active] += conditional * family_probs[active, family_id].unsqueeze(-1)
    return result


@torch.no_grad()
def choose_factorized_action(
    model: DeepSetsActorCritic,
    state: Sequence[float],
    action_mask,
    *,
    deterministic: bool = False,
    family_source: str = "legacy_exact",
) -> FactorisedAction:
    """Sample one legal D4 family/preset pair and its exact joint log-probability."""
    device = next(model.parameters()).device
    states = torch.as_tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
    mask = _as_mask(action_mask, device=device)
    legacy_dist, values = model.distribution(states, action_mask=mask)
    if family_source == "legacy_exact" and deterministic:
        preset = torch.argmax(legacy_dist.probs, dim=-1)
        preset_id = int(preset.item())
        family_id = int(ACTION_FAMILY_IDS[preset_id].item())
        return FactorisedAction(
            family_id=family_id,
            family_name=FAMILY_NAMES[family_id],
            preset_id=preset_id,
            preset_name=action_name(preset_id),
            family_source=family_source,
            log_prob=float(legacy_dist.log_prob(preset).item()),
            value=float(values.item()),
        )
    family_mask = family_mask_from_actions(mask)
    if family_source == "legacy_exact":
        family_probs = torch.zeros((1, len(FAMILY_NAMES)), dtype=legacy_dist.probs.dtype, device=device)
        family_ids = ACTION_FAMILY_IDS.to(device)
        for family_id in range(len(FAMILY_NAMES)):
            family_probs[:, family_id] = legacy_dist.probs[:, family_ids == family_id].sum(dim=-1)
        family_dist = torch.distributions.Categorical(probs=family_probs)
    elif family_source == "learned":
        family_dist = model.family_distribution(states, family_mask=family_mask)
    else:
        raise ValueError("family_source must be 'legacy_exact' or 'learned'")
    family = torch.argmax(family_dist.probs, dim=-1) if deterministic else family_dist.sample()
    selected_family = int(family.item())
    preset_mask = preset_mask_for_family(mask, selected_family, device=device)
    preset_dist, values = model.distribution(states, action_mask=preset_mask)
    preset = torch.argmax(preset_dist.probs, dim=-1) if deterministic else preset_dist.sample()
    preset_id = int(preset.item())
    return FactorisedAction(
        family_id=selected_family,
        family_name=FAMILY_NAMES[selected_family],
        preset_id=preset_id,
        preset_name=action_name(preset_id),
        family_source=family_source,
        log_prob=float((family_dist.log_prob(family) + preset_dist.log_prob(preset)).item()),
        value=float(values.item()),
    )
