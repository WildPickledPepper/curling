"""Regression checks for the pure local teammate PPO adapter.

Run from the repository root with a Python environment containing PyTorch:
    python training_research\\opponents\\test_teammate_ppo_adapter.py
"""

from __future__ import annotations

import contextlib
import io
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from teammate_ppo_adapter import PPO_ROOT, TeammatePPOOpponent


class TeammatePPOAdapterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        try:
            import torch
        except ImportError as exc:
            raise unittest.SkipTest("PyTorch is not installed") from exc
        cls.torch = torch
        cls.adapter = TeammatePPOOpponent()
        sys.path.insert(0, str(PPO_ROOT))
        from ppo_actions import N_ACTIONS
        from ppo_robot_flat import PPOTacticsRobot

        cls.N_ACTIONS = N_ACTIONS
        cls.PPOTacticsRobot = PPOTacticsRobot

    def _original_robot_without_socket(self, position, player_is_init, shot_num):
        robot = object.__new__(self.PPOTacticsRobot)
        robot.position = list(position)
        robot.player_is_init = bool(player_is_init)
        robot.shot_num = int(shot_num)
        robot.score = 0
        robot.round_total = -1
        robot.next_shot = 0
        robot.model = self.adapter._model
        robot.deterministic = True
        robot.mask_guard_takeout = False
        robot.mask_guard_hit_actions = False
        robot.guard_takeout_max_shot = 6
        robot.mask_guard_takeout_when_scoring = False
        robot.action_logit_bias = [0.0] * self.N_ACTIONS
        robot.invalid_action_count = 0
        robot.fallback_draw_count = 0
        robot.pending_transition = None
        robot.last_sent_bestshot = ""
        return robot

    def test_matches_original_robot_on_representative_positions(self):
        fixtures = [
            ([0.0] * 32, True, 0),
            ([2.375, 4.88, 0.0, 0.0] + [0.0] * 28, True, 4),
            ([2.1, 5.1, 2.65, 7.3, 2.7, 4.5, 1.8, 8.0] + [0.0] * 24, False, 11),
        ]
        for position, player_is_init, shot_num in fixtures:
            decision = self.adapter.choose(
                position,
                player_is_init=player_is_init,
                shot_num=shot_num,
            )
            original = self._original_robot_without_socket(position, player_is_init, shot_num)
            with contextlib.redirect_stdout(io.StringIO()):
                command = original.get_bestshot()
            self.assertEqual(decision.command, command)
            self.assertEqual(decision.tactic, original.pending_transition["action_name"])


if __name__ == "__main__":
    unittest.main()
