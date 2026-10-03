"""Live trajectory collector using the Stage C Deep Sets state and model."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import torch

from v2_collector import V2RolloutRobot
from v2_config import V2PPOConfig
from v2_set_policy import DeepSetsActorCritic, load_stage_c_state_dict
from v2_state_encoder import build_stage_c_state
from v2_trajectory import Trajectory


class StageCRolloutRobot(V2RolloutRobot):
    def current_state(self):
        return build_stage_c_state(
            position=self.position,
            player_is_init=self.player_is_init,
            shot_num=self.shot_num,
            end_score=getattr(self, "last_end_score", 0),
            total_ends=self._match_end_limit(),
            current_player=getattr(self, "next_shot", 0),
            current_end=self._current_match_end(),
            cumulative_score_diff=getattr(self, "match_score_diff", 0),
        )

    def legal_action_mask(self, legal):
        from v2_tactical_constraints import apply_stage_c_action_constraints

        base_mask = super().legal_action_mask(legal)
        return apply_stage_c_action_constraints(
            base_mask,
            self.position,
            self.player_is_init,
            self.shot_num,
            current_end=self._current_match_end(),
            total_ends=self._match_end_limit(),
            cumulative_score_diff=int(getattr(self, "match_score_diff", 0)),
            context_mask=self.v2_config.stage_c_context_mask,
            complex_hit_mask=self.v2_config.complex_hit_target_mask,
        )


def load_stage_c_model(checkpoint_path: str | Path, device: str = "cpu") -> DeepSetsActorCritic:
    checkpoint = torch.load(checkpoint_path, map_location=device)
    model = DeepSetsActorCritic().to(device)
    load_stage_c_state_dict(model, checkpoint.get("model", checkpoint))
    model.eval()
    return model


def collect_stage_c_trajectory(
    *,
    key: str,
    host: str,
    port: int,
    rollout_steps: int,
    trajectory_id: str,
    model_state_dict=None,
    deterministic: bool = False,
    name: str = "PPOStageCWorker",
    config: Optional[V2PPOConfig] = None,
    record_distillation_states: bool = False,
    **robot_kwargs,
) -> Trajectory:
    model = DeepSetsActorCritic()
    if model_state_dict is not None:
        load_stage_c_state_dict(model, model_state_dict)
    model.eval()
    robot = StageCRolloutRobot(
        key=key,
        name=name,
        host=host,
        port=port,
        model=model,
        deterministic=deterministic,
        rollout_steps=rollout_steps,
        trajectory_id=trajectory_id,
        v2_config=config,
        record_distillation_states=record_distillation_states,
        **robot_kwargs,
    )
    return robot.recv_forever()
