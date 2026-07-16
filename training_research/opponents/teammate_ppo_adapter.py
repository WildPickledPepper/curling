"""Pure local inference adapter for the teammate PPO tactical robot.

The original package is intentionally preserved under
``research_archive/teammate_ppo_deploy``.  This adapter reuses its state
encoder, action mask, tactic library, and checkpoint, but exposes no socket
or Unity lifecycle.  It is for local-opponent evaluation only.
"""

from __future__ import annotations

import contextlib
import io
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PPO_ROOT = PROJECT_ROOT / "research_archive" / "teammate_ppo_deploy"
DEFAULT_CHECKPOINT = PPO_ROOT / "latest.pt"
DEFAULT_DRAW = "BESTSHOT 3.0 0 0"


@dataclass(frozen=True)
class PPOOpponentDecision:
    """One deterministic or sampled decision from the untouched PPO policy."""

    bestshot: Tuple[float, float, float]
    command: str
    tactic: str
    action_id: int
    policy_probability: float
    value: float
    fallback: bool
    legal_tactics: Tuple[str, ...]


class TeammatePPOOpponent:
    """Run the teammate's discrete PPO tactic policy without a socket."""

    def __init__(
        self,
        checkpoint: Path = DEFAULT_CHECKPOINT,
        *,
        deterministic: bool = True,
    ) -> None:
        if not PPO_ROOT.is_dir():
            raise FileNotFoundError(f"teammate PPO package not found: {PPO_ROOT}")
        if str(PPO_ROOT) not in sys.path:
            sys.path.insert(0, str(PPO_ROOT))

        try:
            import torch
        except ImportError as exc:  # pragma: no cover - environment-specific.
            raise RuntimeError("TeammatePPOOpponent requires a local PyTorch installation.") from exc

        from ppo_actions import ACTION_NAMES, N_ACTIONS, action_id
        from ppo_policy import ActorCritic, load_compatible_state_dict
        from ppo_state_reward import build_state
        import strategy_library

        checkpoint = Path(checkpoint)
        if not checkpoint.is_file():
            raise FileNotFoundError(f"PPO checkpoint not found: {checkpoint}")

        try:
            payload = torch.load(checkpoint, map_location="cpu", weights_only=True)
        except TypeError as exc:  # pragma: no cover - old PyTorch only.
            raise RuntimeError(
                "Use a PyTorch version that supports safe weights_only checkpoint loading."
            ) from exc

        state_dict = payload.get("model", payload) if isinstance(payload, dict) else payload
        self._torch = torch
        self._action_names = tuple(ACTION_NAMES)
        self._n_actions = int(N_ACTIONS)
        self._action_id = action_id
        self._build_state = build_state
        self._strategy_library = strategy_library
        self._deterministic = bool(deterministic)
        self._model = ActorCritic()
        load_compatible_state_dict(self._model, state_dict)
        self._model.eval()

    @staticmethod
    def _state_list(position: Sequence[float]) -> List[List[float]]:
        values = [float(value) for value in position[:32]]
        values.extend([0.0] * (32 - len(values)))
        return [[values[index * 2], values[index * 2 + 1]] for index in range(16)]

    @staticmethod
    def _parse_bestshot(command: str) -> Tuple[float, float, float]:
        parts = command.split()
        if len(parts) != 4 or parts[0] != "BESTSHOT":
            raise ValueError(f"invalid BESTSHOT command: {command!r}")
        return float(parts[1]), float(parts[2]), float(parts[3])

    @staticmethod
    def _result_to_command(result: object) -> Optional[str]:
        if result is None or result == 0:
            return None
        try:
            v0, h0, w0 = result  # type: ignore[misc]
        except (TypeError, ValueError):
            return None
        return f"BESTSHOT {v0} {h0} {w0}"

    def _tactic_result(
        self,
        tactic: str,
        state_list: List[List[float]],
        player_is_init: bool,
        shot_num: int,
    ) -> Optional[str]:
        is_init = 0 if player_is_init else 1
        if tactic == "double_hit":
            function = (
                self._strategy_library.double_hit_init
                if player_is_init
                else self._strategy_library.double_hit_gote
            )
        elif tactic == "double_push_in":
            function = self._strategy_library.double_push_in
        else:
            function = getattr(self._strategy_library, tactic, None)
        if function is None:
            return None
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                result = function(state_list, is_init, int(shot_num))
        except TypeError:
            return None
        return self._result_to_command(result)

    def _legal_actions(
        self,
        position: Sequence[float],
        player_is_init: bool,
        shot_num: int,
    ) -> Tuple[Dict[int, Optional[str]], List[bool]]:
        state_list = self._state_list(position)
        legal: Dict[int, Optional[str]] = {}
        for index, tactic in enumerate(self._action_names):
            legal[index] = (
                DEFAULT_DRAW
                if tactic == "default_draw"
                else self._tactic_result(tactic, state_list, player_is_init, shot_num)
            )

        default_id = self._action_id("default_draw")
        mask = [legal.get(index) is not None and index != default_id for index in range(self._n_actions)]
        if not any(mask):
            mask[default_id] = True
        return legal, mask

    def choose(
        self,
        position: Sequence[float],
        *,
        player_is_init: bool,
        shot_num: int,
        end_score: int = 0,
        total_ends: int = -1,
        current_player: int = 0,
    ) -> PPOOpponentDecision:
        """Choose one shot using the original policy and tactic parameters."""

        values = [float(value) for value in position[:32]]
        values.extend([0.0] * (32 - len(values)))
        state = self._build_state(
            position=values,
            player_is_init=bool(player_is_init),
            shot_num=int(shot_num),
            end_score=int(end_score),
            total_ends=int(total_ends),
            current_player=int(current_player),
        )
        legal, action_mask = self._legal_actions(values, bool(player_is_init), int(shot_num))
        with self._torch.no_grad():
            state_tensor = self._torch.as_tensor(state, dtype=self._torch.float32).unsqueeze(0)
            distribution, value_tensor = self._model.distribution(state_tensor, action_mask=action_mask)
            if self._deterministic:
                action_tensor = self._torch.argmax(distribution.probs, dim=-1)
            else:
                action_tensor = distribution.sample()
            action = int(action_tensor.item())
            probability = float(distribution.probs[0, action].item())
            value = float(value_tensor.item())

        command = legal.get(action)
        tactic = self._action_names[action]
        fallback = False
        if command is None:
            fallback = True
            for fallback_id, fallback_command in legal.items():
                if fallback_id != action and fallback_command is not None:
                    action = fallback_id
                    tactic = self._action_names[action]
                    command = fallback_command
                    break
        if command is None:
            fallback = True
            action = self._action_id("default_draw")
            tactic = "default_draw"
            command = DEFAULT_DRAW

        legal_tactics = tuple(
            self._action_names[index] for index, allowed in enumerate(action_mask) if allowed
        )
        return PPOOpponentDecision(
            bestshot=self._parse_bestshot(command),
            command=command,
            tactic=tactic,
            action_id=action,
            policy_probability=probability,
            value=value,
            fallback=fallback,
            legal_tactics=legal_tactics,
        )
