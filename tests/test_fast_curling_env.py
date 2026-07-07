# -*- coding: utf-8 -*-
"""Tests for tactical behavior in the fast curling surrogate."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from fast_curling_env import HOUSE_X, HOUSE_Y, FastCurlingEnv, Stone, within_calibration_support


class FastCurlingEnvTest(unittest.TestCase):
    def test_fast_takeout_collides_along_path(self) -> None:
        env = FastCurlingEnv(seed=1)
        env.shot_num = 8
        env.stones[1] = Stone(HOUSE_X, HOUSE_Y, True)

        env.place_stone(8, (6.0, 0.0, 0.0))

        self.assertFalse(env.stones[1].in_play)

    def test_unity_calibration_support_checks_sweep_range(self) -> None:
        payload = {
            "schema": "unity_landing_v2",
            "input_ranges": {
                "v0": [2.5, 3.5],
                "h0": [-0.5, 0.5],
                "w0": [-1.5, 1.5],
                "sweep": [0.0, 8.0],
            },
            "support_margin": 0.0,
        }

        self.assertTrue(within_calibration_support(payload, 3.0, 0.0, 0.0, sweep=8.0))
        self.assertFalse(within_calibration_support(payload, 3.0, 0.0, 0.0, sweep=9.0))


if __name__ == "__main__":
    unittest.main()
