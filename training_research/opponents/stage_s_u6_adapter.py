"""Pure local inference adapter for the supplied Stage-S U6 Deep-Sets PPO.

The deployment archive is preserved unchanged under
``research_archive/ppo_stage_s_u6_flat``.  Its live robot opens a socket in
``__init__``; this adapter deliberately avoids that transport setup but calls
the same Stage-C state encoder, legal-action masks, target heads and Stage-S
P1/P2 overrides used by the supplied ``main.py``.
"""

from __future__ import annotations

import sys
import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PPO_ROOT = PROJECT_ROOT / "research_archive" / "ppo_stage_s_u6_flat"
DEFAULT_CHECKPOINT = PPO_ROOT / "latest.pt"
DEFAULT_PROJECT_PYTHON = Path(os.environ.get("DCCOURSE_TORCH_PYTHON", r"D:\anaconda3\python.exe"))
WORKER_PATH = Path(__file__).with_name("stage_s_u6_worker.py")


@dataclass(frozen=True)
class StageSPPOOpponentDecision:
    bestshot: Tuple[float, float, float]
    tactic: str
    action_id: int
    policy_probability: float
    value: float
    fallback: bool
    legal_tactics: Tuple[str, ...]
    stage_s_p1_peel_guard: bool
    stage_s_p2_blocked_draw: bool


class StageSU6Opponent:
    """Run the teammate-supplied Stage-S policy without a socket connection."""

    def __init__(
        self,
        checkpoint: Path = DEFAULT_CHECKPOINT,
        *,
        deterministic: bool = True,
        python_executable: Path = DEFAULT_PROJECT_PYTHON,
        force_local: bool = False,
    ) -> None:
        if not PPO_ROOT.is_dir():
            raise FileNotFoundError(f"Stage-S PPO package not found: {PPO_ROOT}")
        checkpoint = Path(checkpoint)
        if not checkpoint.is_file():
            raise FileNotFoundError(f"Stage-S checkpoint not found: {checkpoint}")
        self._worker: subprocess.Popen[str] | None = None
        requested_python = Path(python_executable)
        # 项目的严格 PhysX 默认运行在 CPython 3.13，而项目的 Torch 环境是
        # Anaconda CPython 3.11。两者 ABI 无法混装；因此默认让 PPO 在已有
        # Torch 环境中推理，父进程仍保持项目自带 pyphysx。
        if not force_local and requested_python.is_file() and requested_python.resolve() != Path(sys.executable).resolve():
            self._worker = subprocess.Popen(
                [
                    str(requested_python), str(WORKER_PATH),
                    "--checkpoint", str(checkpoint),
                    "--deterministic" if deterministic else "--stochastic",
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                bufsize=1,
                cwd=str(PROJECT_ROOT),
            )
            return

        if str(PPO_ROOT) not in sys.path:
            sys.path.insert(0, str(PPO_ROOT))

        try:
            import torch  # noqa: F401
        except ImportError as exc:  # pragma: no cover - environment-specific.
            raise RuntimeError("StageSU6Opponent requires a local PyTorch installation.") from exc

        # Import only after PPO_ROOT is at the front of sys.path.  These are
        # the archive's own modules, not copies in our project.
        from ppo_actions import ACTION_NAMES
        from v2_config import V2PPOConfig
        from v2_stage_c_collector import StageCRolloutRobot, load_stage_c_model

        model = load_stage_c_model(checkpoint)
        self._action_names = tuple(ACTION_NAMES)
        self._robot = _LocalStageSRobot(
            StageCRolloutRobot,
            model=model,
            deterministic=bool(deterministic),
            config=V2PPOConfig(
                response_aware_reward=True,
                stage_c_context_mask=True,
                complex_hit_target_mask=True,
                stage_s_p1_peel_guard=True,
                stage_s_p2_blocked_draw=True,
            ),
        )

    @staticmethod
    def _parse_bestshot(command: str) -> Tuple[float, float, float]:
        parts = command.split()
        if len(parts) != 4 or parts[0] != "BESTSHOT":
            raise ValueError(f"Stage-S PPO emitted an invalid BESTSHOT: {command!r}")
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
    ) -> StageSPPOOpponentDecision:
        if self._worker is not None:
            if self._worker.stdin is None or self._worker.stdout is None:
                raise RuntimeError("Stage-S PPO worker pipes are unavailable")
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
                error = ""
                if self._worker.stderr is not None:
                    error = self._worker.stderr.read().strip()
                raise RuntimeError(f"Stage-S PPO worker exited before replying: {error}")
            result = json.loads(line)
            if not bool(result.get("ok", False)):
                raise RuntimeError(f"Stage-S PPO worker failed: {result.get('error', 'unknown error')}")
            return StageSPPOOpponentDecision(
                bestshot=tuple(float(value) for value in result["bestshot"]),
                tactic=str(result["tactic"]), action_id=int(result["action_id"]),
                policy_probability=float(result["policy_probability"]), value=float(result["value"]),
                fallback=bool(result["fallback"]), legal_tactics=tuple(str(value) for value in result["legal_tactics"]),
                stage_s_p1_peel_guard=bool(result["stage_s_p1_peel_guard"]),
                stage_s_p2_blocked_draw=bool(result["stage_s_p2_blocked_draw"]),
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
        return StageSPPOOpponentDecision(
            bestshot=self._parse_bestshot(command),
            tactic=str(pending.get("action_name", "unknown")),
            action_id=int(pending.get("action", -1)),
            policy_probability=0.0,  # Stage-C stores log-prob, not probability.
            value=float(pending.get("value", 0.0)),
            fallback=bool(pending.get("invalid_action", False) or pending.get("fallback_draw", False)),
            legal_tactics=legal_tactics,
            stage_s_p1_peel_guard=bool(pending.get("stage_s_p1_peel_guard_override", False)),
            stage_s_p2_blocked_draw=bool(pending.get("stage_s_p2_blocked_draw_override", False)),
        )

    def close(self) -> None:
        if self._worker is None:
            return
        try:
            if self._worker.stdin is not None:
                self._worker.stdin.write("{\"close\":true}\n")
                self._worker.stdin.flush()
        except (OSError, ValueError):
            pass
        self._worker.terminate()
        try:
            self._worker.wait(timeout=3)
        except subprocess.TimeoutExpired:
            self._worker.kill()
        self._worker = None


def _LocalStageSRobot(stage_c_base, *, model, deterministic: bool, config):
    """Construct a socket-free instance of the archive's live robot class.

    We subclass dynamically so every behavioral method remains the source
    archive's method.  Only transport initialisation is omitted.
    """

    class LocalStageSRobot(stage_c_base):
        def __init__(self) -> None:
            # Do not call the archive parent: AIRobot.__init__ opens a socket.
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
            # PPOTacticsRobot defaults which its mask helpers read even when
            # this socket-free adapter never collects a rollout.
            self.mask_guard_takeout = False
            self.mask_guard_hit_actions = False
            self.guard_takeout_max_shot = 6
            self.mask_guard_takeout_when_scoring = False
            self.last_sent_bestshot = ""

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

    return LocalStageSRobot()
