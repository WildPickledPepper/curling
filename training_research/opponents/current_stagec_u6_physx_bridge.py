"""CP39-side proxy for current U6 action ranking and conditional heads."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Sequence

from .current_stagec_u6_adapter import (
    DEFAULT_CHECKPOINT,
    DEFAULT_PROJECT_PYTHON,
    PPO_ROOT,
    WORKER_PATH,
    CurrentStageCU6Decision,
)


class CurrentStageCU6PhysXBridge:
    """Keep U6/Torch isolated while CP39 performs strict Top-K selection."""

    def __init__(
        self,
        checkpoint: Path = DEFAULT_CHECKPOINT,
        *,
        python_executable: Path = DEFAULT_PROJECT_PYTHON,
        rule_aware_early_hit_mask: bool = True,
        historical_k5_k7_prior: bool = False,
    ) -> None:
        checkpoint = Path(checkpoint)
        if not checkpoint.is_file():
            raise FileNotFoundError(f"current Stage-C checkpoint not found: {checkpoint}")
        if not Path(python_executable).is_file():
            raise FileNotFoundError(f"Torch interpreter not found: {python_executable}")
        command = [str(python_executable), str(WORKER_PATH), "--checkpoint", str(checkpoint), "--deterministic"]
        if rule_aware_early_hit_mask:
            command.append("--rule-aware-early-hit-mask")
        if historical_k5_k7_prior:
            command.append("--historical-k5-k7-prior")
        self._process = subprocess.Popen(
            command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", bufsize=1, cwd=str(PPO_ROOT),
        )
        self._last_historical_action_bias: list[float] = []
        self._last_historical_prior: dict[str, object] = {}

    def _request(self, payload: dict) -> dict:
        if self._process.stdin is None or self._process.stdout is None:
            raise RuntimeError("current U6 PhysX bridge pipes are unavailable")
        self._process.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
        self._process.stdin.flush()
        line = self._process.stdout.readline()
        if not line:
            error = self._process.stderr.read().strip() if self._process.stderr is not None else ""
            raise RuntimeError(f"current U6 PhysX bridge exited before replying: {error}")
        reply = json.loads(line)
        if not bool(reply.get("ok", False)):
            raise RuntimeError(f"current U6 PhysX bridge failed: {reply.get('error', 'unknown error')}")
        return reply

    def choose(self, position: Sequence[float], *, player_is_init: bool, shot_num: int, end_score: int, total_ends: int, current_player: int):
        reply = self._request({
            "operation": "decision", "position": [float(value) for value in position[:32]],
            "player_is_init": bool(player_is_init), "shot_num": int(shot_num),
            "end_score": int(end_score), "total_ends": int(total_ends),
            "current_player": int(current_player),
        })
        prior = reply.get("historical_k5_k7_prior", {})
        self._last_historical_prior = dict(prior) if isinstance(prior, dict) else {}
        raw_bias = self._last_historical_prior.get("action_logit_bias", ())
        self._last_historical_action_bias = [float(value) for value in raw_bias] if isinstance(raw_bias, list) else []
        decision = CurrentStageCU6Decision(
            bestshot=tuple(float(value) for value in reply["bestshot"]), tactic=str(reply["tactic"]),
            action_id=int(reply["action_id"]), policy_probability=float(reply["policy_probability"]),
            value=float(reply["value"]), fallback=bool(reply["fallback"]),
            legal_tactics=tuple(str(value) for value in reply["legal_tactics"]),
            stage_s_p1_peel_guard=bool(reply["stage_s_p1_peel_guard"]),
            stage_s_p2_blocked_draw=bool(reply["stage_s_p2_blocked_draw"]),
            historical_k5_k7_prior=dict(self._last_historical_prior),
        )
        return decision, list(reply["state"]), list(reply["action_mask"])

    def rank_actions(self, state, mask: Sequence[bool], bias: Sequence[float], top_k: int):
        merged_bias = [float(value) for value in bias]
        if len(self._last_historical_action_bias) == len(merged_bias):
            merged_bias = [
                base + history
                for base, history in zip(merged_bias, self._last_historical_action_bias)
            ]
        reply = self._request({"operation": "rank", "state": list(state), "mask": list(mask), "bias": merged_bias, "top_k": int(top_k)})
        return [(int(action), float(probability)) for action, probability in reply["ranked"]]

    def act_target(self, state, target_mask, action_id: int, deterministic: bool, use_d5_residual: bool = False, legacy_target_id=None):
        reply = self._request({"operation": "target", "state": list(state), "mask": list(target_mask), "action_id": int(action_id), "use_d5_residual": bool(use_d5_residual), "legacy_target_id": legacy_target_id})
        return reply["value"], reply["log_prob"]

    def act_relay(self, state, middle_mask, action_id: int, target_index: int, deterministic: bool):
        reply = self._request({"operation": "relay", "state": list(state), "mask": list(middle_mask), "action_id": int(action_id), "target_index": int(target_index)})
        return reply["value"], reply["log_prob"]

    def act_double(self, state, second_target_mask, action_id: int, target_index: int, deterministic: bool):
        reply = self._request({"operation": "double", "state": list(state), "mask": list(second_target_mask), "action_id": int(action_id), "target_index": int(target_index)})
        return reply["value"], reply["log_prob"]

    def close(self) -> None:
        try:
            if self._process.stdin is not None:
                self._process.stdin.write('{"close": true}\n')
                self._process.stdin.flush()
            self._process.wait(timeout=5)
        except (OSError, subprocess.TimeoutExpired):
            self._process.kill()
