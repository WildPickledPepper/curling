"""Live Socket collector for boundary-correct PPO V2 trajectories.

The simulator alternates actions.  A V2 transition therefore stays pending
until the next opponent response is visible, so its successor state and
bootstrap value are genuine rather than inferred from another worker rollout.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Dict, List, Optional

import torch

from ppo_actions import ACTION_NAMES, N_ACTIONS, action_id, action_name
from ppo_policy import ActorCritic, load_compatible_state_dict
from ppo_robot_flat_v2 import (
    BYPASS_DRAW_ACTIONS,
    BYPASS_TAKEOUT_ACTIONS,
    DEFAULT_DRAW_BESTSHOT,
    PPOTacticsRobot,
    get_state_list,
    result_to_bestshot,
    sl,
)
from ppo_rollout import (
    GUARD_HIT_ACTIONS,
    HIT_ACTIONS,
    HOUSE_HIT_ACTIONS,
    SETUP_ACTIONS,
    SOFT_DISPLACEMENT_ACTIONS,
)
from ppo_state_reward import (
    blocked_house_threat,
    delayed_setup_reward,
    hit_outcome_metrics,
    hit_outcome_reward,
    setup_outcome_reward,
    shaped_reward,
    situation_evaluation_reward,
    strategic_match_context_reward,
    summarize_position,
    terminal_score_reward,
)
from v2_config import V2PPOConfig
from v2_policy import choose_action
from v2_trajectory import Trajectory, Transition
from ppo_tactic_targets import (
    TARGETED_DIRECT_HIT_ACTIONS,
    TARGETED_DOUBLE_ACTIONS,
    TARGETED_RELAY_ACTIONS,
    bestshot_for_double,
    bestshot_for_relay,
    bestshot_for_target,
    executable_target_mask,
    executable_double_second_mask,
    executable_double_target_mask,
    double_outcome,
    executable_relay_middle_mask,
    executable_relay_target_mask,
    relay_outcome,
    target_outcome,
)
from v2_action_realizer import realize_legacy_selection
from v2_structured_policy import choose_factorized_action
from v2_stage_s_guard import (
    AROUND_GUARD_DRAW_LEFT,
    PEEL_GUARD,
    should_override_p1_peel_guard,
    should_override_p2_blocked_draw,
)


class V2RolloutRobot(PPOTacticsRobot):
    """PPOTacticsRobot transport/tactic adapter with a V2 trajectory state machine."""

    def __init__(
        self,
        *args,
        trajectory_id: str,
        v2_config: Optional[V2PPOConfig] = None,
        record_distillation_states: bool = False,
        next_end_command_file: str = "",
        virtual_match_ends: int = 0,
        **kwargs,
    ) -> None:
        # V2 never accepts V1 sampling-only logit biases.
        kwargs["action_logit_bias"] = [0.0] * N_ACTIONS
        kwargs["exploration_logit_bias"] = [0.0] * N_ACTIONS
        super().__init__(*args, **kwargs)
        self.v2_config = v2_config or V2PPOConfig()
        self.trajectory = Trajectory(trajectory_id=trajectory_id)
        self.pending_transition: Optional[Dict[str, object]] = None
        self.pending_phase = "idle"
        self.after_own_position: Optional[List[float]] = None
        self.record_distillation_states = bool(record_distillation_states)
        self.current_end_record_indices: List[int] = []
        self.current_end_transition_indices: List[int] = []
        self.score = 0
        self.last_end_score = 0
        self.match_score_diff = 0
        self.virtual_match_ends = max(0, int(virtual_match_ends))
        self.completed_match_ends = 0
        self.pending_end_bootstrap_index: Optional[int] = None
        self.next_end_command_file = (
            Path(next_end_command_file) if next_end_command_file else None
        )

    def _is_fixed_match(self) -> bool:
        return int(getattr(self, "round_total", -1)) > 0

    def _is_virtual_match(self) -> bool:
        return self.virtual_match_ends > 0 and not self._is_fixed_match()

    def _uses_match_context(self) -> bool:
        return self._is_fixed_match() or self._is_virtual_match()

    def _match_end_limit(self) -> int:
        if self._is_virtual_match():
            return self.virtual_match_ends
        return int(getattr(self, "round_total", -1))

    def _current_match_end(self) -> int:
        if self._is_virtual_match():
            return self.completed_match_ends + 1
        return int(getattr(self, "round_num", 0)) + 1

    def recv_setstate(self, msg_list):
        super().recv_setstate(msg_list)
        if self.pending_end_bootstrap_index is None or self.shot_num != 0:
            return
        self.position = [0.0] * 32
        next_state = list(self.current_state())
        transition = self.trajectory.transitions[self.pending_end_bootstrap_index]
        transition.next_state = next_state
        transition.next_value = self._estimate_value(next_state)
        self.pending_end_bootstrap_index = None

    def choose_action(self, state, action_mask):
        family_policy = self.v2_config.structured_family_policy
        if family_policy != "off":
            if family_policy != "legacy_exact":
                raise ValueError("only legacy_exact structured family policy is safe for live collection")
            if self.model is None or not hasattr(self.model, "family_distribution"):
                raise ValueError("structured family policy requires a Stage C model")
            decision = choose_factorized_action(
                self.model,
                state,
                action_mask,
                deterministic=self.deterministic,
                family_source="legacy_exact",
            )
            return decision.preset_id, decision.log_prob, decision.value
        if self.model is None:
            legal = [index for index, enabled in enumerate(action_mask) if enabled]
            action = legal[int(time.time_ns() % len(legal))]
            return action, 0.0, 0.0
        return choose_action(self.model, state, action_mask, deterministic=self.deterministic)

    def _targeted_position(self) -> List[float]:
        return [value for stone in get_state_list(self.position) for value in stone]

    def _target_conditioned_mask(self, action_mask: List[bool]) -> List[bool]:
        """Remove a conditional family when its required stone slots are absent."""
        if self.model is None or not hasattr(self.model, "act_target"):
            return action_mask
        mask = list(action_mask)
        position = self._targeted_position()
        for index, name in enumerate(ACTION_NAMES):
            if name in TARGETED_DIRECT_HIT_ACTIONS:
                mask[index] = any(executable_target_mask(
                    position,
                    action_name=name,
                    player_is_first=self.player_is_init,
                ))
            elif name in TARGETED_RELAY_ACTIONS:
                mask[index] = any(executable_relay_target_mask(
                    position,
                    action_name=name,
                    player_is_first=self.player_is_init,
                ))
            elif name in TARGETED_DOUBLE_ACTIONS:
                mask[index] = any(executable_double_target_mask(
                    position,
                    action_name=name,
                    player_is_first=self.player_is_init,
                ))
        if not any(mask):
            mask[action_id("default_draw")] = True
        return mask

    def get_bestshot(self):
        if self.pending_transition is not None:
            raise RuntimeError("Received GO before the previous V2 action was finalised.")
        state = self.current_state()
        legal = self.legal_action_map()
        action_mask = self._target_conditioned_mask(self.legal_action_mask(legal))
        selected_action, log_prob, value = self.choose_action(state, action_mask)
        stage_s_p1_peel_guard_override = False
        stage_s_p2_blocked_draw_override = False
        if (
            selected_action is not None
            and (
                self.v2_config.stage_s_p1_peel_guard
                or self.v2_config.stage_s_p2_blocked_draw
            )
        ):
            bypass_diagnostics = sl.bypass_action_diagnostics(
                get_state_list(self.position),
                0 if self.player_is_init else 1,
                int(self.shot_num),
            )
            if self.v2_config.stage_s_p1_peel_guard and should_override_p1_peel_guard(
                self.position,
                candidate_is_first=self.player_is_init,
                shot_num=int(self.shot_num),
                prior_action=int(selected_action),
                action_mask=action_mask,
                bypass_diagnostics=bypass_diagnostics,
            ):
                selected_action = PEEL_GUARD
                stage_s_p1_peel_guard_override = True
            elif self.v2_config.stage_s_p2_blocked_draw and should_override_p2_blocked_draw(
                self.position,
                candidate_is_first=self.player_is_init,
                shot_num=int(self.shot_num),
                prior_action=int(selected_action),
                action_mask=action_mask,
                bypass_diagnostics=bypass_diagnostics,
            ):
                selected_action = AROUND_GUARD_DRAW_LEFT
                stage_s_p2_blocked_draw_override = True
        selected_target = None
        selected_target_mask: List[bool] = []
        selected_middle = None
        selected_middle_mask: List[bool] = []
        selected_second_target = None
        selected_second_target_mask: List[bool] = []
        target_shot = None
        if (
            selected_action is not None
            and action_name(selected_action) in TARGETED_DIRECT_HIT_ACTIONS
            and self.model is not None
            and hasattr(self.model, "act_target")
        ):
            selected_name = action_name(selected_action)
            position = self._targeted_position()
            selected_target_mask = executable_target_mask(
                position,
                action_name=selected_name,
                player_is_first=self.player_is_init,
            )
            if not any(selected_target_mask):
                raise RuntimeError(f"selected target action {selected_name} without a target")
            selected_target, target_log_prob = self.model.act_target(
                state,
                target_mask=selected_target_mask,
                action_id=selected_action,
                deterministic=self.deterministic,
                use_d5_residual=self.v2_config.d5_target_residual,
            )
            log_prob += target_log_prob
            target_shot = result_to_bestshot(bestshot_for_target(
                position,
                action_name=selected_name,
                player_is_first=self.player_is_init,
                target_index=selected_target,
            ))
        elif (
            selected_action is not None
            and action_name(selected_action) in TARGETED_RELAY_ACTIONS
            and self.model is not None
            and hasattr(self.model, "act_target")
            and hasattr(self.model, "act_relay")
        ):
            selected_name = action_name(selected_action)
            position = self._targeted_position()
            selected_target_mask = executable_relay_target_mask(
                position, action_name=selected_name, player_is_first=self.player_is_init,
            )
            if not any(selected_target_mask):
                raise RuntimeError(f"selected relay action {selected_name} without a target")
            selected_target, target_log_prob = self.model.act_target(
                state, target_mask=selected_target_mask, action_id=selected_action,
                deterministic=self.deterministic,
                use_d5_residual=self.v2_config.d5_target_residual,
            )
            selected_middle_mask = executable_relay_middle_mask(
                position, action_name=selected_name, player_is_first=self.player_is_init,
                target_index=selected_target,
            )
            if not any(selected_middle_mask):
                raise RuntimeError(f"selected relay action {selected_name} target {selected_target} without a middle")
            selected_middle, middle_log_prob = self.model.act_relay(
                state, middle_mask=selected_middle_mask, action_id=selected_action,
                target_index=selected_target,
                deterministic=self.deterministic,
            )
            log_prob += target_log_prob + middle_log_prob
            target_shot = result_to_bestshot(bestshot_for_relay(
                position,
                action_name=selected_name,
                player_is_first=self.player_is_init,
                target_index=selected_target,
                middle_index=selected_middle,
            ))
        elif (
            selected_action is not None
            and action_name(selected_action) in TARGETED_DOUBLE_ACTIONS
            and self.model is not None
            and hasattr(self.model, "act_target")
            and hasattr(self.model, "act_double")
        ):
            selected_name = action_name(selected_action)
            position = self._targeted_position()
            selected_target_mask = executable_double_target_mask(
                position, action_name=selected_name, player_is_first=self.player_is_init,
            )
            if not any(selected_target_mask):
                raise RuntimeError(f"selected double action {selected_name} without a target")
            selected_target, target_log_prob = self.model.act_target(
                state, target_mask=selected_target_mask, action_id=selected_action,
                deterministic=self.deterministic,
                use_d5_residual=self.v2_config.d5_target_residual,
            )
            selected_second_target_mask = executable_double_second_mask(
                position,
                action_name=selected_name,
                player_is_first=self.player_is_init,
                target_index=selected_target,
            )
            if not any(selected_second_target_mask):
                raise RuntimeError(f"selected double action {selected_name} target {selected_target} without a partner")
            selected_second_target, second_log_prob = self.model.act_double(
                state,
                second_target_mask=selected_second_target_mask,
                action_id=selected_action,
                target_index=selected_target,
                deterministic=self.deterministic,
            )
            log_prob += target_log_prob + second_log_prob
            target_shot = result_to_bestshot(bestshot_for_double(
                position,
                action_name=selected_name,
                player_is_first=self.player_is_init,
                target_index=selected_target,
                second_target_index=selected_second_target,
            ))
        if target_shot is not None:
            shot_msg = target_shot
            executed_name = action_name(selected_action)
            invalid_action = False
            fallback_draw = False
        else:
            shot_msg, executed_name, invalid_action, fallback_draw = self.action_to_shot(selected_action, legal)
        structured_action = None
        if (
            self.v2_config.structured_action_adapter
            or self.v2_config.structured_family_policy != "off"
        ) and selected_action is not None:
            realized = realize_legacy_selection(
                selected_action,
                self._targeted_position(),
                player_is_first=self.player_is_init,
                shot_num=self.shot_num,
                primary_target=selected_target,
                middle_target=selected_middle,
                second_target=selected_second_target,
            )
            structured_action = realized.action
            structured_shot = result_to_bestshot(realized.bestshot)
            if target_shot is not None and structured_shot is None:
                raise RuntimeError(
                    "D2 structured realizer failed for an executable target action "
                    f"{structured_action.preset}"
                )
            if structured_shot is not None:
                if structured_shot != shot_msg:
                    raise RuntimeError(
                        "D2 structured realizer changed the legacy BESTSHOT for "
                        f"{structured_action.preset}: {structured_shot} != {shot_msg}"
                    )
                shot_msg = structured_shot
        if self.record_distillation_states:
            record_index = len(self.trajectory.distillation_records)
            self.trajectory.distillation_records.append({
                "position": list(self.position),
                "player_is_init": bool(self.player_is_init),
                "shot_num": int(self.shot_num),
                "end_score": int(self.last_end_score),
                "total_ends": self._match_end_limit(),
                "current_player": int(getattr(self, "next_shot", 0)),
                "current_end": self._current_match_end(),
                "cumulative_score_diff": int(self.match_score_diff),
                "action_mask": list(action_mask),
                "action": int(selected_action) if selected_action is not None else -1,
                "action_name": executed_name,
                "target_index": selected_target if selected_target is not None else -1,
                "target_mask": list(selected_target_mask),
                "middle_index": selected_middle if selected_middle is not None else -1,
                "middle_mask": list(selected_middle_mask),
                "second_target_index": selected_second_target if selected_second_target is not None else -1,
                "second_target_mask": list(selected_second_target_mask),
                "terminal_score": None,
                "match_result": None,
                "final_score_diff": None,
                "steps_to_match_end": None,
            })
            self.current_end_record_indices.append(record_index)
        self.pending_transition = {
            "state": list(state),
            "position_before": list(self.position),
            "action": selected_action if selected_action is not None else action_id("occupy"),
            "log_prob": log_prob,
            "value": value,
            "action_name": executed_name,
            "action_family": structured_action.family.value if structured_action else "",
            "action_preset": structured_action.preset if structured_action else "",
            "action_mask": list(action_mask),
            "target_index": selected_target,
            "target_mask": list(selected_target_mask),
            "middle_index": selected_middle,
            "middle_mask": list(selected_middle_mask),
            "second_target_index": selected_second_target,
            "second_target_mask": list(selected_second_target_mask),
            "shot_num": self.shot_num,
            "invalid_action": invalid_action,
            "fallback_draw": fallback_draw,
            "player_is_init": bool(self.player_is_init),
            "current_end": self._current_match_end(),
            "total_ends": self._match_end_limit(),
            "cumulative_score_diff": int(self.match_score_diff),
            "stage_s_p1_peel_guard_override": stage_s_p1_peel_guard_override,
            "stage_s_p2_blocked_draw_override": stage_s_p2_blocked_draw_override,
        }
        self.pending_phase = "await_own_position"
        self.after_own_position = None
        self.last_sent_bestshot = shot_msg
        print(
            "PPO V2决策:",
            f"shot={self.shot_num + 1}",
            f"selected={action_name(selected_action) if selected_action is not None else 'none'}",
            f"executed={executed_name}",
            f"family={structured_action.family.value if structured_action else 'legacy'}",
            f"target={selected_target if selected_target is not None else 'none'}",
            f"middle={selected_middle if selected_middle is not None else 'none'}",
            f"second={selected_second_target if selected_second_target is not None else 'none'}",
            flush=True,
        )
        return shot_msg

    def _estimate_value(self, state: List[float]) -> float:
        if self.model is None:
            return 0.0
        with torch.no_grad():
            state_tensor = torch.as_tensor(state, dtype=torch.float32).unsqueeze(0)
            outputs = self.model.forward(state_tensor)
            values = outputs[1]
        return float(values.item())

    @staticmethod
    def _clip_reward(value: float) -> float:
        return max(-5.0, min(5.0, float(value)))

    def _set_reward_components(
        self,
        transition: Transition,
        additions: Dict[str, float],
    ) -> None:
        components = dict(transition.reward_components)
        components.pop("clip", None)
        for name, value in additions.items():
            components[name] = components.get(name, 0.0) + float(value)
        raw_reward = sum(components.values())
        clipped_reward = self._clip_reward(raw_reward)
        components["clip"] = clipped_reward - raw_reward
        transition.reward_components = components
        transition.reward = clipped_reward

    def _action_outcome_flags(self, pending: Dict[str, object], after_position: List[float]) -> Dict[str, bool]:
        executed = str(pending["action_name"])
        before_summary = summarize_position(pending["position_before"], self.player_is_init)
        after_summary = summarize_position(after_position, self.player_is_init)
        blocked_target, blocking_guards = blocked_house_threat(before_summary)
        blocked_multi_stone_threat = bool(
            int(pending["shot_num"]) >= 12
            and int(before_summary["score_for_my"]) < 0
            and len(before_summary["opp_house"]) >= 2
            and blocked_target is not None
            and blocking_guards
        )
        threat_improved = bool(
            blocked_multi_stone_threat
            and (
                len(after_summary["opp_house"]) < len(before_summary["opp_house"])
                or int(after_summary["score_for_my"]) > int(before_summary["score_for_my"])
            )
        )
        late_multi_stone_threat = bool(
            int(pending["shot_num"]) >= 12
            and int(before_summary["score_for_my"]) < 0
            and len(before_summary["opp_house"]) >= 2
        )
        late_threat_improved = bool(
            late_multi_stone_threat
            and (
                len(after_summary["opp_house"]) < len(before_summary["opp_house"])
                or int(after_summary["score_for_my"]) > int(before_summary["score_for_my"])
            )
        )
        bypass_attempt = executed in BYPASS_DRAW_ACTIONS | BYPASS_TAKEOUT_ACTIONS
        flags = {
            "invalid_action": bool(pending["invalid_action"]),
            "fallback_draw": bool(pending["fallback_draw"]),
            "stage_s_p1_peel_guard_override": bool(
                pending.get("stage_s_p1_peel_guard_override", False)
            ),
            "stage_s_p2_blocked_draw_override": bool(
                pending.get("stage_s_p2_blocked_draw_override", False)
            ),
            "bypass_draw_attempt": executed in BYPASS_DRAW_ACTIONS,
            "bypass_draw_success": executed in BYPASS_DRAW_ACTIONS
            and len(after_summary["my_house"]) > len(before_summary["my_house"]),
            "bypass_takeout_attempt": executed in BYPASS_TAKEOUT_ACTIONS,
            "bypass_takeout_success": executed in BYPASS_TAKEOUT_ACTIONS
            and len(after_summary["opp_house"]) < len(before_summary["opp_house"]),
            "blocked_multi_stone_threat": blocked_multi_stone_threat,
            "blocked_threat_bypass_attempt": blocked_multi_stone_threat and bypass_attempt,
            "blocked_threat_bypass_success": blocked_multi_stone_threat
            and bypass_attempt
            and threat_improved,
            "blocked_threat_improved": threat_improved,
            "blocked_threat_hit_attempt": False,
            "guard_only_failure": False,
            "late_multi_stone_threat": late_multi_stone_threat,
            "late_multi_stone_hit_attempt": late_multi_stone_threat and executed in HIT_ACTIONS,
            "late_multi_stone_setup_attempt": late_multi_stone_threat and executed in SETUP_ACTIONS,
            "late_multi_stone_threat_improved": late_threat_improved,
            "late_multi_stone_nonproductive_hit": False,
            "late_multi_stone_guard_only_failure": False,
        }
        before_target_position = [value for stone in get_state_list(pending["position_before"]) for value in stone]
        after_target_position = [value for stone in get_state_list(after_position) for value in stone]
        target_flags = (
            double_outcome(
                before_target_position, after_target_position,
                action_name=executed,
                target_index=pending.get("target_index"),
                second_target_index=pending.get("second_target_index"),
            ) if executed in TARGETED_DOUBLE_ACTIONS else relay_outcome(
                before_target_position, after_target_position,
                action_name=executed,
                target_index=pending.get("target_index"),
                middle_index=pending.get("middle_index"),
            ) if executed in TARGETED_RELAY_ACTIONS else target_outcome(
                before_target_position, after_target_position,
                action_name=executed,
                target_index=pending.get("target_index"),
                candidate_index=int(pending["shot_num"]),
            )
        )
        flags["target_contract_evaluable"] = bool(target_flags["evaluable"])
        flags["target_contract_success"] = bool(target_flags["success"])
        if executed in HOUSE_HIT_ACTIONS | GUARD_HIT_ACTIONS | SOFT_DISPLACEMENT_ACTIONS:
            metrics = hit_outcome_metrics(
                before_position=pending["position_before"],
                after_position=after_position,
                player_is_init=self.player_is_init,
                shot_num=int(pending["shot_num"]),
            )
            flags["blocked_threat_hit_attempt"] = bool(metrics["blocked_multi_stone_threat"])
            flags["guard_only_failure"] = bool(
                metrics["blocked_multi_stone_threat"]
                and not metrics["threat_house_reduced"]
                and metrics["opp_guard_removed"] > 0
                and metrics["score_delta"] <= 0
            )
            flags["late_multi_stone_nonproductive_hit"] = bool(
                late_multi_stone_threat
                and not late_threat_improved
            )
            flags["late_multi_stone_guard_only_failure"] = bool(
                late_multi_stone_threat
                and not late_threat_improved
                and metrics["opp_guard_removed"] > 0
                and metrics["score_delta"] <= 0
            )
        return flags

    def _execution_reward(self, pending: Dict[str, object], after_position: List[float]) -> float:
        """Small action-quality signal, deliberately excluding board potential."""
        reward = hit_outcome_reward(
            before_position=pending["position_before"], after_position=after_position,
            player_is_init=self.player_is_init, shot_num=int(pending["shot_num"]),
            action_name=str(pending["action_name"]),
        )
        reward += setup_outcome_reward(
            before_position=pending["position_before"], after_position=after_position,
            player_is_init=self.player_is_init, shot_num=int(pending["shot_num"]),
            action_name=str(pending["action_name"]),
        )
        if pending["action_name"] == "take_out":
            reward -= self.take_out_penalty
            if self.bad_takeout_penalty > 0.0:
                delta = situation_evaluation_reward(
                    before_position=pending["position_before"], after_position=after_position,
                    player_is_init=self.player_is_init, shot_num=int(pending["shot_num"]),
                )
                if delta < self.bad_takeout_min_delta:
                    reward -= self.bad_takeout_penalty
        return reward

    def _transition_reward_components(
        self,
        pending: Dict[str, object],
        response_position: List[float],
    ) -> Dict[str, float]:
        assert self.after_own_position is not None
        execution = self._execution_reward(pending, self.after_own_position)
        if not self.v2_config.response_aware_reward:
            # V2.0 compatibility path, retained only for direct comparisons.
            board_reward = shaped_reward(
                before_position=pending["position_before"], after_position=self.after_own_position,
                player_is_init=self.player_is_init, shot_num=int(pending["shot_num"]),
                invalid_action=bool(pending["invalid_action"]),
                fallback_draw=bool(pending["fallback_draw"]),
                invalid_action_penalty=self.invalid_penalty,
                fallback_draw_penalty=self.fallback_draw_penalty,
            )
            return {"board": board_reward, "execution": execution}

        board_reward = self.v2_config.board_potential_weight * situation_evaluation_reward(
            before_position=pending["position_before"], after_position=response_position,
            player_is_init=self.player_is_init, shot_num=int(pending["shot_num"]),
        )
        return {
            "board": board_reward,
            "execution": self.v2_config.execution_reward_weight * execution,
            "strategy": self.v2_config.strategic_context_weight * strategic_match_context_reward(
                before_position=pending["position_before"],
                after_position=self.after_own_position,
                player_is_init=bool(pending["player_is_init"]),
                shot_num=int(pending["shot_num"]),
                action_name=str(pending["action_name"]),
                current_end=int(pending["current_end"]),
                total_ends=int(pending["total_ends"]),
                cumulative_score_diff=int(pending["cumulative_score_diff"]),
            ),
            "invalid": -self.invalid_penalty if pending["invalid_action"] else 0.0,
            "fallback": -self.fallback_draw_penalty if pending["fallback_draw"] else 0.0,
        }

    def _append_pending(
        self,
        *,
        next_state: List[float],
        next_value: float,
        terminated: bool,
        terminal_score: Optional[int] = None,
    ) -> None:
        if self.pending_transition is None:
            return
        pending = self.pending_transition
        own_position = self.after_own_position or list(self.position)
        response_position = list(self.position)
        reward_components = self._transition_reward_components(pending, response_position)
        if terminal_score is not None:
            reward_components["end_score"] = (
                self.v2_config.terminal_score_weight * terminal_score_reward(terminal_score)
            )
        transition_index = len(self.trajectory.transitions)
        transition = Transition(
                state=pending["state"], action=int(pending["action"]),
                action_mask=pending["action_mask"], log_prob=float(pending["log_prob"]),
                value=float(pending["value"]), reward=0.0,
                next_state=list(next_state), next_value=0.0 if terminated else float(next_value),
                terminated=terminated, action_name=str(pending["action_name"]),
                action_family=str(pending.get("action_family", "")),
                action_preset=str(pending.get("action_preset", "")),
                target_index=pending.get("target_index"),
                target_mask=list(pending.get("target_mask", [])),
                middle_index=pending.get("middle_index"),
                middle_mask=list(pending.get("middle_mask", [])),
                second_target_index=pending.get("second_target_index"),
                second_target_mask=list(pending.get("second_target_mask", [])),
                shot_num=int(pending["shot_num"]),
                terminal_score=terminal_score,
                outcome_flags=self._action_outcome_flags(pending, own_position),
            )
        self._set_reward_components(transition, reward_components)
        self.trajectory.append(transition)
        self.current_end_transition_indices.append(transition_index)
        self.pending_transition = None
        self.pending_phase = "idle"
        self.after_own_position = None
        if (
            self.rollout_steps > 0
            and len(self.trajectory) >= self.rollout_steps
            and not self._uses_match_context()
        ):
            if not terminated:
                self.trajectory.mark_last_truncated()
            self.on_line = False

    def handle_position(self) -> None:
        if self.pending_transition is None:
            return
        if self.pending_phase == "await_own_position":
            self.after_own_position = list(self.position)
            self.pending_phase = "await_opponent_position"
            return
        if self.pending_phase == "await_opponent_position":
            next_state = list(self.current_state())
            self._append_pending(
                next_state=next_state,
                next_value=self._estimate_value(next_state),
                terminated=False,
            )

    def handle_score(self, end_score: int) -> None:
        has_end_activity = bool(
            self.current_end_transition_indices
            or self.current_end_record_indices
            or self.pending_transition is not None
        )
        if self._uses_match_context() and not has_end_activity:
            print("忽略无投壶的重复SCORE", flush=True)
            return

        self.score = int(end_score)
        self.last_end_score = self.score
        match_context = self._uses_match_context()
        if match_context:
            self.match_score_diff += self.score
            self.completed_match_ends += 1
        if self.score > 0:
            print(f"我方得{self.score}分", flush=True)
        elif self.score < 0:
            print(f"对方得{-self.score}分", flush=True)
        else:
            print("双方均未得分", flush=True)
        for record_index in self.current_end_record_indices:
            self.trajectory.distillation_records[record_index]["terminal_score"] = self.score
        self.current_end_record_indices = []
        terminal_state = list(self.current_state())
        if self.pending_transition is not None:
            self._append_pending(
                next_state=terminal_state, next_value=0.0,
                terminated=not match_context, terminal_score=self.score,
            )
        elif self.trajectory.transitions and not self.trajectory.transitions[-1].terminated:
            # Opponent's final response may have completed the last pending
            # transition just before SCORE. Convert that transition to terminal.
            last = self.trajectory.transitions[-1]
            self._set_reward_components(last, {
                "end_score": self.v2_config.terminal_score_weight
                * terminal_score_reward(self.score),
            })
            last.next_value = 0.0
            last.terminated = not match_context
            last.truncated = False
        for transition_index in self.current_end_transition_indices:
            self.trajectory.transitions[transition_index].terminal_score = self.score
        if self.current_end_transition_indices:
            final_index = self.current_end_transition_indices[-1]
            final_transition = self.trajectory.transitions[final_index]
            final_transition.end_boundary = True
            if match_context and not final_transition.truncated:
                self.pending_end_bootstrap_index = final_index
        self.current_end_transition_indices = []
        if match_context:
            if self.score > 0:
                self.player_is_init = True
            elif self.score < 0:
                self.player_is_init = False
            else:
                self.player_is_init = not self.player_is_init
            role = "先手" if self.player_is_init else "后手"
            print(f"我方下局{role}", flush=True)
            if self._is_virtual_match() and self.completed_match_ends >= self.virtual_match_ends:
                self._finish_virtual_match()
                self.on_line = False
            elif self._is_fixed_match():
                self._request_next_fixed_end()

    def _finish_virtual_match(self) -> None:
        if self.match_score_diff > 0:
            result = "WIN"
        elif self.match_score_diff < 0:
            result = "LOSE"
        else:
            result = "DRAW"
        self.handle_gameover(result)
        print(
            f"虚拟{self.virtual_match_ends}局结束: "
            f"累计分差={self.match_score_diff} 结果={result}",
            flush=True,
        )

    def _request_next_fixed_end(self) -> None:
        """Advance the headless Unity UI after a non-final fixed-match end."""
        command_file = getattr(self, "next_end_command_file", None)
        if command_file is None:
            return
        completed_ends = int(getattr(self, "round_num", 0)) + 1
        total_ends = int(getattr(self, "round_total", 0))
        if total_ends <= 0 or completed_ends >= total_ends:
            return
        try:
            command_file.write_text(
                json.dumps(
                    {
                        "action": "next",
                        "generation": time.time_ns(),
                        # Give the score board one render frame window, but
                        # click before the fixed-end server closes the current
                        # player sockets under multi-lane load.
                        "retries": 1,
                        "delayMs": 500,
                        # The Unity controller must observe both the next
                        # SETSTATE 0 and a fresh GO before this end is ACKed.
                        "ackWaitMs": 1500,
                        "ackRetryWaves": 4,
                        "resumeRetries": 3,
                        "resumeWaitMs": 9000,
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            print(f"请求后台进入第{completed_ends + 1}局", flush=True)
        except OSError as error:
            print(f"后台下一局请求失败: {error}", flush=True)

    def handle_gameover(self, result: str) -> None:
        match_result = 1 if result == "WIN" else -1 if result == "LOSE" else 0
        self.trajectory.final_score_diff = int(self.match_score_diff)
        record_count = len(self.trajectory.distillation_records)
        for record_index, record in enumerate(self.trajectory.distillation_records):
            record["match_result"] = match_result
            record["final_score_diff"] = int(self.match_score_diff)
            record["steps_to_match_end"] = record_count - record_index - 1
        for transition in self.trajectory.transitions:
            transition.match_result_target = match_result
        if self.trajectory.transitions:
            last = self.trajectory.transitions[-1]
            margin_limit = max(0.0, float(self.v2_config.final_margin_clip))
            clipped_margin = max(
                -margin_limit,
                min(margin_limit, float(self.match_score_diff)),
            )
            self._set_reward_components(last, {
                "match": self.v2_config.match_result_weight * match_result,
                "margin": self.v2_config.final_margin_weight * clipped_margin,
            })
            last.next_value = 0.0
            last.terminated = True
            last.truncated = False
            last.match_result = match_result
        self.pending_end_bootstrap_index = None

    def recv_forever(self):
        null_messages = 0
        self.on_line = True
        while self.on_line:
            msg_code, msg_list = self.recv_msg()
            if msg_code == "":
                null_messages += 1
                if null_messages >= 5:
                    break
                continue
            null_messages = 0
            if msg_code == "CONNECTNAME":
                self.player_is_init = msg_list[0] == "Player1"
            elif msg_code == "ISREADY":
                self.send_msg("READYOK")
                time.sleep(0.5)
                self.send_msg("NAME " + self.name)
            elif msg_code == "SETSTATE":
                self.recv_setstate(msg_list)
            elif msg_code == "POSITION":
                for index in range(32):
                    self.position[index] = float(msg_list[index])
                self.handle_position()
            elif msg_code == "GO":
                self.send_msg(self.get_bestshot())
            elif msg_code == "MOTIONINFO":
                for index in range(5):
                    self.motioninfo[index] = float(msg_list[index])
            elif msg_code == "CENTERLINE_VIOLATION":
                self.send_msg("CENTERLINE_CHOICE RESET")
            elif msg_code == "SCORE":
                self.handle_score(int(msg_list[0]))
            elif msg_code == "GAMEOVER":
                result = msg_list[0] if msg_list else ""
                self.handle_gameover(result)
                if result == "WIN":
                    print("我方获胜", flush=True)
                elif result == "LOSE":
                    print("对方获胜", flush=True)
                else:
                    print("双方平局", flush=True)
                break
        self.ai_sock.close()
        print(
            f"PPO V2 rollout: transitions={len(self.trajectory)} "
            f"terminated={self.trajectory.terminated_count} truncated={self.trajectory.truncated_count}",
            flush=True,
        )
        return self.trajectory


def collect_trajectory(
    *,
    key: str,
    host: str,
    port: int,
    rollout_steps: int,
    trajectory_id: str,
    model_state_dict=None,
    deterministic: bool = False,
    name: str = "PPOV2Worker",
    config: Optional[V2PPOConfig] = None,
    record_distillation_states: bool = False,
    **robot_kwargs,
) -> Trajectory:
    """Collect one worker trajectory, suitable for a multiprocessing queue."""
    model = ActorCritic()
    if model_state_dict is not None:
        load_compatible_state_dict(model, model_state_dict)
    model.eval()
    robot = V2RolloutRobot(
        key=key, name=name, host=host, port=port, model=model,
        deterministic=deterministic, rollout_steps=rollout_steps,
        trajectory_id=trajectory_id, v2_config=config, **robot_kwargs,
        record_distillation_states=record_distillation_states,
    )
    return robot.recv_forever()
