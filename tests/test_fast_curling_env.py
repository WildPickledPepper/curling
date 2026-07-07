# -*- coding: utf-8 -*-
"""Tests for tactical behavior in the fast curling surrogate."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from fast_curling_env import HOUSE_X, HOUSE_Y, FastCurlingEnv, Stone


class FastCurlingEnvTest(unittest.TestCase):
    def test_fast_takeout_collides_along_path(self) -> None:
        env = FastCurlingEnv(seed=1)
        env.shot_num = 8
        env.stones[1] = Stone(HOUSE_X, HOUSE_Y, True)

        env.place_stone(8, (6.0, 0.0, 0.0))

        self.assertFalse(env.stones[1].in_play)


if __name__ == "__main__":
    unittest.main()
