"""Configuration for the PPO V2.0 correctness pass."""

from dataclasses import dataclass


@dataclass(frozen=True)
class V2PPOConfig:
    """PPO settings shared by collection and training.

    `response_aware_reward` remains disabled in V2.0 so it is possible to
    compare against V1 reward shaping while fixing only the PPO data chain.
    V2.1 can enable it once this version has passed the probe experiments.
    """

    gamma: float = 0.99
    gae_lambda: float = 0.95
    clip_ratio: float = 0.20
    learning_rate: float = 5e-5
    update_epochs: int = 3
    batch_size: int = 128
    value_coef: float = 0.5
    value_clip_ratio: float = 0.20
    value_huber_delta: float = 1.0
    entropy_coef: float = 0.04
    entropy_target_ratio: float = 0.60
    entropy_target_coef: float = 0.08
    max_grad_norm: float = 0.50
    response_aware_reward: bool = False
    board_potential_weight: float = 0.90
    execution_reward_weight: float = 0.25
    terminal_score_weight: float = 0.10
    target_contract_direct_reward: float = 0.12
    target_contract_relay_reward: float = 0.15
    target_contract_double_reward: float = 0.18
    bypass_contract_reward: float = 0.18
    contract_requires_nonnegative_response: bool = False
    contract_response_board_floor: float = 0.0
    counterfactual_aux_coef: float = 0.0
    counterfactual_aux_batch_size: int = 64
    counterfactual_aux_epochs: int = 1
    role_aware_terminal_reward: bool = False
    match_result_weight: float = 2.0
    final_margin_weight: float = 0.08
    final_margin_clip: float = 8.0
    warmstart_kl_coef: float = 0.0
    score_aux_coef: float = 0.15
    match_aux_coef: float = 0.15
    critic_head_epochs: int = 0
    critic_head_learning_rate: float = 1e-4
    monte_carlo_value_targets: bool = False
    strategic_context_weight: float = 0.0
    stage_c_context_mask: bool = False
    complex_hit_target_mask: bool = False
    structured_action_adapter: bool = False
    structured_family_policy: str = "off"
    d5_target_residual: bool = False
    d5_target_kl_coef: float = 0.05
    d6_action_residual: bool = False
    d6_override_margin: float = 0.40
    stage_s_p1_peel_guard: bool = False
    stage_s_p2_blocked_draw: bool = False
