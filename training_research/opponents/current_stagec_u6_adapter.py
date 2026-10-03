"""Local adapter for the current teammate Stage-C U6 checkpoint.

The current U6 package is kept outside ``research_archive`` because it is the
active PPO training workspace.  Strict PhysX still runs in CP39, while this
adapter starts its Torch inference in the project's Anaconda environment.
No socket is opened and no historical PPO checkpoint is substituted.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PPO_ROOT = PROJECT_ROOT / "ppo_stagec_physx_teammate_training_cp38_20260724"
DEFAULT_CHECKPOINT = PPO_ROOT / "checkpoints" / "u6_server_synced_latest.pt"
DEFAULT_PROJECT_PYTHON = Path(os.environ.get("DCCOURSE_TORCH_PYTHON", r"D:\Anaconda3\python.exe"))
WORKER_PATH = Path(__file__).with_name("current_stagec_u6_worker.py")


@dataclass(frozen=True)
class CurrentStageCU6Decision:
    bestshot: Tuple[float, float, float]
    tactic: str
    action_id: int
    policy_probability: float
    value: float
    fallback: bool
    legal_tactics: Tuple[str, ...]
    stage_s_p1_peel_guard: bool
    stage_s_p2_blocked_draw: bool
    # Kept for diagnostics and for verifying that CP39 strict ranking receives
    # exactly the same optional inference prior as the Torch PPO choice.
    historical_k5_k7_prior: dict


class CurrentStageCU6Opponent:
    """Use the active U6 checkpoint as a deterministic local opponent."""

    def __init__(
        self,
        checkpoint: Path = DEFAULT_CHECKPOINT,
        *,
        deterministic: bool = True,
        python_executable: Path = DEFAULT_PROJECT_PYTHON,
        force_local: bool = False,
        rule_aware_early_hit_mask: bool = False,
        historical_k5_k7_prior: bool = False,
    ) -> None:
        if not PPO_ROOT.is_dir():
            raise FileNotFoundError(f"current Stage-C PPO package not found: {PPO_ROOT}")
        checkpoint = Path(checkpoint)
        if not checkpoint.is_file():
            raise FileNotFoundError(f"current Stage-C checkpoint not found: {checkpoint}")
        self._worker: subprocess.Popen[str] | None = None
        requested_python = Path(python_executable)
        if not force_local and requested_python.is_file() and requested_python.resolve() != Path(sys.executable).resolve():
            self._worker = subprocess.Popen(
                [
                    str(requested_python), str(WORKER_PATH),
                    "--checkpoint", str(checkpoint),
                    "--deterministic" if deterministic else "--stochastic",
                    *( ["--rule-aware-early-hit-mask"] if rule_aware_early_hit_mask else [] ),
                    *( ["--historical-k5-k7-prior"] if historical_k5_k7_prior else [] ),
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                bufsize=1,
                cwd=str(PPO_ROOT),
            )
            return

        if str(PPO_ROOT) not in sys.path:
            sys.path.insert(0, str(PPO_ROOT))
        try:
            import torch  # noqa: F401
        except ImportError as exc:  # pragma: no cover - environment-specific.
            raise RuntimeError("CurrentStageCU6Opponent requires a local PyTorch installation.") from exc

        from ppo_framework.actions import ACTION_NAMES
        from ppo_framework.v2.config import V2PPOConfig
        from ppo_framework.v2.stage_c_collector import StageCRolloutRobot, load_stage_c_model

        self._action_names = tuple(ACTION_NAMES)
        self._robot = _LocalCurrentStageCRobot(
            StageCRolloutRobot,
            model=load_stage_c_model(checkpoint),
            deterministic=bool(deterministic),
            config=V2PPOConfig(
                response_aware_reward=True,
                stage_c_context_mask=True,
                complex_hit_target_mask=True,
                stage_s_p1_peel_guard=True,
                stage_s_p2_blocked_draw=True,
                rule_aware_early_hit_mask=bool(rule_aware_early_hit_mask),
                historical_k5_k7_prior_enabled=bool(historical_k5_k7_prior),
            ),
        )

    @staticmethod
    def _parse_bestshot(command: str) -> Tuple[float, float, float]:
        parts = command.split()
        if len(parts) != 4 or parts[0] != "BESTSHOT":
            raise ValueError(f"current Stage-C U6 emitted an invalid BESTSHOT: {command!r}")
        return float(parts[1]), float(parts[2]), float(parts[3])

    def choose(
        self,
        position: Sequence[float],
        *,
        player_is_init: bool,
        shot_num: int,
        end_score: int = 0,
        total_ends: int = 1,
        current_player: int = 0,
    ) -> CurrentStageCU6Decision:
        if self._worker is not None:
            if self._worker.stdin is None or self._worker.stdout is None:
                raise RuntimeError("current Stage-C U6 worker pipes are unavailable")
            payload = {
                "position": [float(value) for value in position[:32]],
                "player_is_init": bool(player_is_init),
                "shot_num": int(shot_num),
                "end_score": int(end_score),
                "total_ends": int(total_ends),
                "current_player": int(current_player),
            }
            self._worker.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
            self._worker.stdin.flush()
            line = self._worker.stdout.readline()
            if not line:
                error = self._worker.stderr.read().strip() if self._worker.stderr is not None else ""
                raise RuntimeError(f"current Stage-C U6 worker exited before replying: {error}")
            result = json.loads(line)
            if not bool(result.get("ok", False)):
                raise RuntimeError(f"current Stage-C U6 worker failed: {result.get('error', 'unknown error')}")
            return CurrentStageCU6Decision(
                bestshot=tuple(float(value) for value in result["bestshot"]),
                tactic=str(result["tactic"]), action_id=int(result["action_id"]),
                policy_probability=float(result["policy_probability"]), value=float(result["value"]),
                fallback=bool(result["fallback"]), legal_tactics=tuple(str(value) for value in result["legal_tactics"]),
                stage_s_p1_peel_guard=bool(result["stage_s_p1_peel_guard"]),
                stage_s_p2_blocked_draw=bool(result["stage_s_p2_blocked_draw"]),
                historical_k5_k7_prior=dict(result.get("historical_k5_k7_prior", {})),
            )

        command = self._robot.choose_local(
            position,
            player_is_init=bool(player_is_init),
            shot_num=int(shot_num),
            end_score=int(end_score),
            total_ends=int(total_ends),
            current_player=int(current_player),
        )
        pending = self._robot.pending_transition or {}
        action_mask = tuple(bool(item) for item in pending.get("action_mask", ()))
        legal_tactics = tuple(
            name for index, name in enumerate(self._action_names)
            if index < len(action_mask) and action_mask[index]
        )
        return CurrentStageCU6Decision(
            bestshot=self._parse_bestshot(command),
            tactic=str(pending.get("action_name", "unknown")), action_id=int(pending.get("action", -1)),
            policy_probability=0.0, value=float(pending.get("value", 0.0)),
            fallback=bool(pending.get("invalid_action", False) or pending.get("fallback_draw", False)),
            legal_tactics=legal_tactics,
            stage_s_p1_peel_guard=bool(pending.get("stage_s_p1_peel_guard_override", False)),
            stage_s_p2_blocked_draw=bool(pending.get("stage_s_p2_blocked_draw_override", False)),
            historical_k5_k7_prior=dict(pending.get("historical_k5_k7_prior", {})),
        )

    def close(self) -> None:
        if self._worker is None:
            return
        try:
            if self._worker.stdin is not None:
                self._worker.stdin.write('{"close": true}\n')
                self._worker.stdin.flush()
        except (OSError, ValueError):
            pass
        self._worker.terminate()
        try:
            self._worker.wait(timeout=3)
        except subprocess.TimeoutExpired:
            self._worker.kill()
        self._worker = None


def _LocalCurrentStageCRobot(stage_c_base, *, model, deterministic: bool, config):
    """Build the current live Stage-C robot without its socket transport."""

    class LocalCurrentStageCRobot(stage_c_base):
        def __init__(self) -> None:
            self.model = model
            self.deterministic = deterministic
            self.v2_config = config
            self.position = [0.0] * 32
            self.player_is_init = True
            self.shot_num = 0
            self.next_shot = 0
            self.round_num = 0
            self.round_total = 1
            self.last_end_score = 0
            self.match_score_diff = 0
            self.completed_match_ends = 0
            self.virtual_match_ends = 0
            self.pending_transition = None
            self.pending_phase = "idle"
            self.after_own_position = None
            self.record_distillation_states = False
            self.invalid_action_count = 0
            self.fallback_draw_count = 0
            self.mask_guard_takeout = False
            self.mask_guard_hit_actions = False
            self.guard_takeout_max_shot = 6
            self.mask_guard_takeout_when_scoring = False
            self.last_sent_bestshot = ""
            self.server_physx_topk = None
            self.server_physx_sequence = 0
            self.stage_s_endgame_sequence = 0
            self.rule_risk_model = None
            self.rule_risk_threshold = 0.0
            self.rule_risk_sequence = 0

        def choose_local(
            self,
            position: Sequence[float],
            *,
            player_is_init: bool,
            shot_num: int,
            end_score: int,
            total_ends: int,
            current_player: int,
        ) -> str:
            values = [float(value) for value in position[:32]]
            values.extend([0.0] * (32 - len(values)))
            self.position = values
            self.player_is_init = bool(player_is_init)
            self.shot_num = int(shot_num)
            self.next_shot = int(current_player)
            self.round_total = max(1, int(total_ends))
            self.round_num = 0
            self.last_end_score = int(end_score)
            self.match_score_diff = 0
            self.pending_transition = None
            return self.get_bestshot()

    return LocalCurrentStageCRobot()
