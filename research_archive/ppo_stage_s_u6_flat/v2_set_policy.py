"""Deep Sets policy and distributional value model for PPO Stage C."""

from __future__ import annotations

from typing import Mapping, Optional

import torch
import torch.nn as nn

from ppo_actions import N_ACTIONS, action_id
from ppo_policy import apply_action_mask
from v2_action_space import ActionFamily
from v2_state_encoder import (
    GLOBAL_FEATURE_DIM,
    HAMMER_GLOBAL_INDEX,
    LEGACY_GLOBAL_FEATURE_DIM,
    STONE_FEATURE_DIM,
    split_stage_c_tensor,
)

SCORE_MIN = -8
SCORE_MAX = 8
SCORE_BINS = SCORE_MAX - SCORE_MIN + 1
FAMILY_NAMES = tuple(family.value for family in ActionFamily)
N_ACTION_FAMILIES = len(FAMILY_NAMES)
D5_PRIMARY_TARGET_ACTION_IDS = frozenset({
    action_id("take_out"),
    action_id("take_out_house"),
    action_id("hit_and_stay"),
})
D5_GUARD_TARGET_ACTION_IDS = frozenset({
    action_id("take_out_guard"),
    action_id("peel_guard"),
})
D5_ROLL_TARGET_ACTION_IDS = frozenset({
    action_id("hit_roll"),
    action_id("hit_roll_left"),
    action_id("hit_roll_right"),
})
D5_DIRECT_TARGET_ACTION_IDS = (
    D5_PRIMARY_TARGET_ACTION_IDS | D5_GUARD_TARGET_ACTION_IDS | D5_ROLL_TARGET_ACTION_IDS
)
D5_ROLL_LEGACY_LOGIT = 0.2
D5_ROLL_RESIDUAL_SCALE = 20.0
GLOBAL_INPUT_WEIGHT_KEY = "global_encoder.0.weight"


def load_stage_c_state_dict(
    model: "DeepSetsActorCritic",
    state_dict: Mapping[str, torch.Tensor],
) -> bool:
    """Load current or legacy Stage C weights, zero-initialising new globals."""
    migrated = dict(state_dict)
    source_weight = migrated.get(GLOBAL_INPUT_WEIGHT_KEY)
    target_weight = model.state_dict()[GLOBAL_INPUT_WEIGHT_KEY]
    expanded = False
    if source_weight is not None and source_weight.shape != target_weight.shape:
        if (
            source_weight.shape[0] == target_weight.shape[0]
            and source_weight.shape[1] == LEGACY_GLOBAL_FEATURE_DIM
            and target_weight.shape[1] == GLOBAL_FEATURE_DIM
        ):
            expanded_weight = torch.zeros_like(target_weight)
            expanded_weight[:, :LEGACY_GLOBAL_FEATURE_DIM] = source_weight.to(
                device=expanded_weight.device,
                dtype=expanded_weight.dtype,
            )
            migrated[GLOBAL_INPUT_WEIGHT_KEY] = expanded_weight
            expanded = True
        else:
            raise ValueError(
                "Unsupported Stage C global encoder shape: "
                f"checkpoint={tuple(source_weight.shape)} model={tuple(target_weight.shape)}"
            )
    target_state = model.state_dict()
    for key, target_value in target_state.items():
        if not key.startswith("critic_") or key in migrated:
            continue
        source_key = key[len("critic_"):]
        source_value = migrated.get(source_key)
        if source_value is None:
            migrated[key] = target_value
        elif source_value.shape == target_value.shape:
            migrated[key] = source_value
        elif (
            key == "critic_global_encoder.0.weight"
            and source_value.shape[0] == target_value.shape[0]
            and source_value.shape[1] == LEGACY_GLOBAL_FEATURE_DIM
            and target_value.shape[1] == GLOBAL_FEATURE_DIM
        ):
            expanded_weight = torch.zeros_like(target_value)
            expanded_weight[:, :LEGACY_GLOBAL_FEATURE_DIM] = source_value.to(
                device=expanded_weight.device, dtype=expanded_weight.dtype
            )
            migrated[key] = expanded_weight
        else:
            raise ValueError(
                f"Unsupported Stage C critic migration for {key}: "
                f"checkpoint={tuple(source_value.shape)} model={tuple(target_value.shape)}"
            )
    for key, value in target_state.items():
        source_value = migrated.get(key)
        if key.startswith("target_heads.") and source_value is not None and source_value.shape != value.shape:
            # Earlier target heads saw only the state trunk. Preserve that
            # part while zeroing the new action-family embedding columns.
            if source_value.shape[0] == value.shape[0] and source_value.shape[1] + 16 == value.shape[1]:
                expanded_value = torch.zeros_like(value)
                expanded_value[:, :source_value.shape[1]] = source_value.to(
                    device=expanded_value.device, dtype=expanded_value.dtype
                )
                migrated[key] = expanded_value
            else:
                migrated[key] = torch.zeros_like(value)
        elif key.startswith("relay_heads.") and source_value is not None and source_value.shape != value.shape:
            # Preserve the state/action columns from a prior relay head while
            # zeroing the newly added selected-target embedding columns.
            if source_value.shape[0] == value.shape[0] and source_value.shape[1] + 8 == value.shape[1]:
                expanded_value = torch.zeros_like(value)
                expanded_value[:, :source_value.shape[1]] = source_value.to(
                    device=expanded_value.device, dtype=expanded_value.dtype
                )
                migrated[key] = expanded_value
            else:
                migrated[key] = torch.zeros_like(value)
        elif key.startswith((
            "target_heads.", "relay_heads.", "double_heads.", "family_heads.",
            "target_residual_heads.", "target_guard_residual_heads.", "target_roll_residual_heads.",
            "action_residual_heads.",
        )) and key not in migrated:
            # An old checkpoint has no slot policy. Start it uniformly so a
            # new head cannot encode arbitrary random preferences.
            migrated[key] = torch.zeros_like(value)
        elif key.startswith("slot_action_embedding.") and key not in migrated:
            migrated[key] = torch.zeros_like(value)
        elif key.startswith("slot_target_embedding.") and key not in migrated:
            migrated[key] = torch.zeros_like(value)
        elif key.startswith("match_heads.") and key not in migrated:
            migrated[key] = value
    model.load_state_dict(migrated)
    return expanded


class DeepSetsActorCritic(nn.Module):
    def __init__(self, n_actions: int = N_ACTIONS):
        super().__init__()
        self.stone_encoder = nn.Sequential(
            nn.Linear(STONE_FEATURE_DIM, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
        )
        self.global_encoder = nn.Sequential(
            nn.Linear(GLOBAL_FEATURE_DIM, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
        )
        self.hammer_embedding = nn.Embedding(2, 8)
        self.trunk = nn.Sequential(
            nn.Linear(64 + 64 + 64 + 8, 192),
            nn.ReLU(),
            nn.Linear(192, 128),
            nn.ReLU(),
        )
        self.critic_stone_encoder = nn.Sequential(
            nn.Linear(STONE_FEATURE_DIM, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
        )
        self.critic_global_encoder = nn.Sequential(
            nn.Linear(GLOBAL_FEATURE_DIM, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
        )
        self.critic_hammer_embedding = nn.Embedding(2, 8)
        self.critic_trunk = nn.Sequential(
            nn.Linear(64 + 64 + 64 + 8, 192),
            nn.ReLU(),
            nn.Linear(192, 128),
            nn.ReLU(),
        )
        self.policy_heads = nn.ModuleList([nn.Linear(128, n_actions) for _ in range(2)])
        # D6 is zero at construction, so a Stage C checkpoint remains exact
        # until a response-aware heldout experiment earns an override.
        self.action_residual_heads = nn.ModuleList([nn.Linear(128, n_actions) for _ in range(2)])
        for head in self.action_residual_heads:
            nn.init.zeros_(head.weight)
            nn.init.zeros_(head.bias)
        # D3 learns this semantic view of the unchanged 41-way policy. It is
        # not consumed by ``forward`` so old inference remains bitwise stable.
        self.family_heads = nn.ModuleList([
            nn.Linear(128, N_ACTION_FAMILIES) for _ in range(2)
        ])
        self.slot_action_embedding = nn.Embedding(n_actions, 16)
        self.slot_target_embedding = nn.Embedding(16, 8)
        # This head chooses a physical stone slot after a target-conditioned
        # tactic family has been selected. It does not alter the 41-way family
        # head, so legacy checkpoints remain behaviour-compatible.
        self.target_heads = nn.ModuleList([nn.Linear(128 + 16, 16) for _ in range(2)])
        self.target_residual_heads = nn.ModuleList([nn.Linear(128 + 16, 16) for _ in range(2)])
        for head in self.target_residual_heads:
            nn.init.zeros_(head.weight)
            nn.init.zeros_(head.bias)
        self.target_guard_residual_heads = nn.ModuleList([nn.Linear(128 + 16, 16) for _ in range(2)])
        for head in self.target_guard_residual_heads:
            nn.init.zeros_(head.weight)
            nn.init.zeros_(head.bias)
        self.target_roll_residual_heads = nn.ModuleList([nn.Linear(128 + 16, 16) for _ in range(2)])
        for head in self.target_roll_residual_heads:
            nn.init.zeros_(head.weight)
            nn.init.zeros_(head.bias)
        # Selected after a relay target. This makes relay likelihoods
        # p(family) * p(target | family) * p(middle | family, target).
        self.relay_heads = nn.ModuleList([nn.Linear(128 + 16 + 8, 16) for _ in range(2)])
        self.double_heads = nn.ModuleList([nn.Linear(128 + 16 + 8, 16) for _ in range(2)])
        self.value_heads = nn.ModuleList([nn.Linear(128, 1) for _ in range(2)])
        self.score_heads = nn.ModuleList([nn.Linear(128, SCORE_BINS) for _ in range(2)])
        self.match_heads = nn.ModuleList([nn.Linear(128, 3) for _ in range(2)])
        self.register_buffer(
            "score_values",
            torch.arange(SCORE_MIN, SCORE_MAX + 1, dtype=torch.float32),
        )

    @staticmethod
    def _encode_with(
        states: torch.Tensor,
        stone_encoder: nn.Module,
        global_encoder: nn.Module,
        hammer_embedding: nn.Module,
        trunk: nn.Module,
    ):
        stones, globals_, valid_mask = split_stage_c_tensor(states)
        stone_embeddings = stone_encoder(stones)
        mask = valid_mask.unsqueeze(-1)
        valid_count = mask.sum(dim=-2).clamp_min(1)
        mean_pool = (stone_embeddings * mask).sum(dim=-2) / valid_count
        masked_for_max = stone_embeddings.masked_fill(~mask, torch.finfo(stone_embeddings.dtype).min)
        max_pool = masked_for_max.max(dim=-2).values
        has_stone = valid_mask.any(dim=-1, keepdim=True)
        max_pool = torch.where(has_stone, max_pool, torch.zeros_like(max_pool))
        global_embedding = global_encoder(globals_)
        hammer = (globals_[..., HAMMER_GLOBAL_INDEX] > 0.5).long()
        hidden = trunk(torch.cat([
            mean_pool,
            max_pool,
            global_embedding,
            hammer_embedding(hammer),
        ], dim=-1))
        return hidden, hammer

    def _encode(self, states: torch.Tensor):
        return self._encode_with(
            states, self.stone_encoder, self.global_encoder,
            self.hammer_embedding, self.trunk,
        )

    def _encode_critic(self, states: torch.Tensor):
        return self._encode_with(
            states, self.critic_stone_encoder, self.critic_global_encoder,
            self.critic_hammer_embedding, self.critic_trunk,
        )

    @staticmethod
    def _select_head(heads: nn.ModuleList, hidden: torch.Tensor, hammer: torch.Tensor) -> torch.Tensor:
        outputs = torch.stack([head(hidden) for head in heads], dim=-2)
        gather_index = hammer.unsqueeze(-1).unsqueeze(-1).expand(*hammer.shape, 1, outputs.shape[-1])
        return outputs.gather(dim=-2, index=gather_index).squeeze(-2)

    def forward(self, states: torch.Tensor):
        hidden, hammer = self._encode(states)
        critic_hidden, critic_hammer = self._encode_critic(states)
        policy_logits = self._select_head(self.policy_heads, hidden, hammer)
        values = self._select_head(
            self.value_heads, critic_hidden, critic_hammer
        ).squeeze(-1)
        score_logits = self._select_head(self.score_heads, hidden, hammer)
        match_logits = self._select_head(self.match_heads, hidden, hammer)
        return policy_logits, values, score_logits, match_logits

    def distribution(
        self,
        states: torch.Tensor,
        action_mask=None,
        action_logit_bias=None,
        *,
        use_d6_action_residual: bool = False,
    ):
        policy_logits, values = self.forward(states)[:2]
        if use_d6_action_residual:
            hidden, hammer = self._encode(states)
            policy_logits = policy_logits + self._select_head(
                self.action_residual_heads, hidden, hammer,
            )
        if action_logit_bias is not None:
            bias = torch.as_tensor(
                action_logit_bias, dtype=policy_logits.dtype, device=policy_logits.device,
            )
            if bias.ndim == 1:
                bias = bias.unsqueeze(0)
            if bias.shape != policy_logits.shape:
                raise ValueError(
                    f"action logit bias shape {tuple(bias.shape)} does not match "
                    f"policy logits {tuple(policy_logits.shape)}"
                )
            policy_logits = policy_logits + bias
        policy_logits = apply_action_mask(policy_logits, action_mask)
        return torch.distributions.Categorical(logits=policy_logits), values

    def family_distribution(self, states: torch.Tensor, family_mask=None):
        """Semantic D3 distribution, separate from the legacy 41-way actor."""
        hidden, hammer = self._encode(states)
        family_logits = self._select_head(self.family_heads, hidden, hammer)
        family_logits = apply_action_mask(family_logits, family_mask)
        return torch.distributions.Categorical(logits=family_logits)

    def _slot_distribution(
        self,
        heads: nn.ModuleList,
        states: torch.Tensor,
        slot_mask,
        action_ids,
        target_ids=None,
        residual_heads: Optional[nn.ModuleList] = None,
        residual_action_ids=None,
        extra_residual_heads: Optional[nn.ModuleList] = None,
        extra_residual_action_ids=None,
        third_residual_heads: Optional[nn.ModuleList] = None,
        third_residual_action_ids=None,
        legacy_target_ids=None,
        legacy_target_action_ids=None,
    ):
        hidden, hammer = self._encode(states)
        actions = torch.as_tensor(action_ids, dtype=torch.long, device=states.device)
        if actions.ndim == 0:
            actions = actions.expand(hammer.shape)
        if actions.shape != hammer.shape:
            raise ValueError(f"slot action ids shape {tuple(actions.shape)} does not match state batch {tuple(hammer.shape)}")
        features = [hidden, self.slot_action_embedding(actions)]
        if target_ids is not None:
            targets = torch.as_tensor(target_ids, dtype=torch.long, device=states.device)
            if targets.ndim == 0:
                targets = targets.expand(hammer.shape)
            if targets.shape != hammer.shape:
                raise ValueError(f"slot target ids shape {tuple(targets.shape)} does not match state batch {tuple(hammer.shape)}")
            features.append(self.slot_target_embedding(targets))
        conditioned_hidden = torch.cat(features, dim=-1)
        logits = self._select_head(heads, conditioned_hidden, hammer)
        if legacy_target_ids is not None and legacy_target_action_ids:
            legacy_targets = torch.as_tensor(legacy_target_ids, dtype=torch.long, device=states.device)
            if legacy_targets.ndim == 0:
                legacy_targets = legacy_targets.expand(hammer.shape)
            if legacy_targets.shape != hammer.shape:
                raise ValueError("legacy target ids must match the state batch")
            legacy_enabled = legacy_targets >= 0
            legacy_actions = torch.zeros_like(actions, dtype=torch.bool)
            for action_id_value in legacy_target_action_ids:
                legacy_actions |= actions == int(action_id_value)
            legacy_enabled &= legacy_actions
            legacy_logits = torch.zeros_like(logits)
            legacy_logits.scatter_(
                -1, legacy_targets.clamp_min(0).unsqueeze(-1), D5_ROLL_LEGACY_LOGIT,
            )
            logits = torch.where(legacy_enabled.unsqueeze(-1), legacy_logits, logits)
        if residual_heads is not None and residual_action_ids:
            residual = self._select_head(residual_heads, conditioned_hidden, hammer)
            enabled = torch.zeros_like(actions, dtype=torch.bool)
            for action_id_value in residual_action_ids:
                enabled |= actions == int(action_id_value)
            logits = logits + residual * enabled.unsqueeze(-1).to(dtype=logits.dtype)
        if extra_residual_heads is not None and extra_residual_action_ids:
            extra_residual = self._select_head(extra_residual_heads, conditioned_hidden, hammer)
            extra_enabled = torch.zeros_like(actions, dtype=torch.bool)
            for action_id_value in extra_residual_action_ids:
                extra_enabled |= actions == int(action_id_value)
            logits = logits + extra_residual * extra_enabled.unsqueeze(-1).to(dtype=logits.dtype)
        if third_residual_heads is not None and third_residual_action_ids:
            third_residual = self._select_head(third_residual_heads, conditioned_hidden, hammer)
            third_enabled = torch.zeros_like(actions, dtype=torch.bool)
            for action_id_value in third_residual_action_ids:
                third_enabled |= actions == int(action_id_value)
            logits = logits + (
                D5_ROLL_RESIDUAL_SCALE * third_residual
                * third_enabled.unsqueeze(-1).to(dtype=logits.dtype)
            )
        logits = apply_action_mask(logits, slot_mask)
        return torch.distributions.Categorical(logits=logits)

    def target_distribution(
        self, states: torch.Tensor, target_mask, action_ids, *,
        use_d5_residual: bool = False, legacy_target_ids=None,
    ):
        return self._slot_distribution(
            self.target_heads,
            states,
            target_mask,
            action_ids,
            residual_heads=self.target_residual_heads if use_d5_residual else None,
            residual_action_ids=D5_PRIMARY_TARGET_ACTION_IDS if use_d5_residual else None,
            extra_residual_heads=self.target_guard_residual_heads if use_d5_residual else None,
            extra_residual_action_ids=D5_GUARD_TARGET_ACTION_IDS if use_d5_residual else None,
            third_residual_heads=self.target_roll_residual_heads if use_d5_residual else None,
            third_residual_action_ids=D5_ROLL_TARGET_ACTION_IDS if use_d5_residual else None,
            legacy_target_ids=legacy_target_ids,
            legacy_target_action_ids=D5_ROLL_TARGET_ACTION_IDS if legacy_target_ids is not None else None,
        )

    def relay_distribution(self, states: torch.Tensor, middle_mask, action_ids, target_ids):
        return self._slot_distribution(
            self.relay_heads, states, middle_mask, action_ids, target_ids=target_ids,
        )

    def double_distribution(self, states: torch.Tensor, second_target_mask, action_ids, target_ids):
        return self._slot_distribution(
            self.double_heads, states, second_target_mask, action_ids, target_ids=target_ids,
        )

    def score_distribution(self, states: torch.Tensor):
        score_logits = self.forward(states)[2]
        distribution = torch.distributions.Categorical(logits=score_logits)
        expected_score = (distribution.probs * self.score_values).sum(dim=-1)
        return distribution, expected_score

    @torch.no_grad()
    def act(
        self,
        state,
        deterministic: bool = False,
        action_mask: Optional[list] = None,
        action_logit_bias: Optional[list] = None,
    ):
        device = next(self.parameters()).device
        state_tensor = torch.as_tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
        dist, value = self.distribution(
            state_tensor,
            action_mask=action_mask,
            action_logit_bias=action_logit_bias,
        )
        action = torch.argmax(dist.probs, dim=-1) if deterministic else dist.sample()
        return int(action.item()), float(dist.log_prob(action).item()), float(value.item())

    @torch.no_grad()
    def act_with_d6_override(
        self,
        state,
        *,
        action_mask: Optional[list] = None,
        action_logit_bias: Optional[list] = None,
        override_margin: float = 0.40,
    ):
        """Use U6 unless a residual action wins by the configured margin."""
        device = next(self.parameters()).device
        state_tensor = torch.as_tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
        base_dist, value = self.distribution(
            state_tensor, action_mask=action_mask, action_logit_bias=action_logit_bias,
        )
        residual_dist, _ = self.distribution(
            state_tensor,
            action_mask=action_mask,
            action_logit_bias=action_logit_bias,
            use_d6_action_residual=True,
        )
        baseline = base_dist.probs.argmax(dim=-1)
        proposed = residual_dist.probs.argmax(dim=-1)
        proposed_gain = residual_dist.log_prob(proposed) - residual_dist.log_prob(baseline)
        apply_override = bool(
            proposed.item() != baseline.item() and proposed_gain.item() >= float(override_margin)
        )
        action = proposed if apply_override else baseline
        distribution = residual_dist if apply_override else base_dist
        return (
            int(action.item()),
            float(distribution.log_prob(action).item()),
            float(value.item()),
            apply_override,
            float(proposed_gain.item()),
        )

    @torch.no_grad()
    def act_target(
        self,
        state,
        target_mask,
        action_id: int,
        deterministic: bool = False,
        use_d5_residual: bool = False,
        legacy_target_id: Optional[int] = None,
    ):
        device = next(self.parameters()).device
        state_tensor = torch.as_tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
        dist = self.target_distribution(
            state_tensor,
            target_mask=target_mask,
            action_ids=action_id,
            use_d5_residual=use_d5_residual,
            legacy_target_ids=legacy_target_id,
        )
        target = torch.argmax(dist.probs, dim=-1) if deterministic else dist.sample()
        return int(target.item()), float(dist.log_prob(target).item())

    @torch.no_grad()
    def act_relay(
        self,
        state,
        middle_mask,
        action_id: int,
        target_index: int,
        deterministic: bool = False,
    ):
        device = next(self.parameters()).device
        state_tensor = torch.as_tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
        dist = self.relay_distribution(
            state_tensor, middle_mask=middle_mask, action_ids=action_id, target_ids=target_index,
        )
        middle = torch.argmax(dist.probs, dim=-1) if deterministic else dist.sample()
        return int(middle.item()), float(dist.log_prob(middle).item())

    @torch.no_grad()
    def act_double(
        self,
        state,
        second_target_mask,
        action_id: int,
        target_index: int,
        deterministic: bool = False,
    ):
        device = next(self.parameters()).device
        state_tensor = torch.as_tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
        dist = self.double_distribution(
            state_tensor,
            second_target_mask=second_target_mask,
            action_ids=action_id,
            target_ids=target_index,
        )
        second = torch.argmax(dist.probs, dim=-1) if deterministic else dist.sample()
        return int(second.item()), float(dist.log_prob(second).item())
