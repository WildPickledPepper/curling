# -*- coding: utf-8 -*-
"""Focused checks for the paper-inspired free-running simulator."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from paper_curling_sim import (
    CalibratedPaperSimulator,
    PaperPhysicsParams,
    simulate_tail,
)


class PaperCurlingSimulatorTest(unittest.TestCase):
    def test_stationary_rock_does_not_move(self) -> None:
        final, stop_time = simulate_tail(
            [2.0, 10.0, 0.0, 0.0, 0.0], PaperPhysicsParams()
        )
        self.assertEqual(final, (2.0, 10.0))
        self.assertEqual(stop_time, 0.0)

    def test_opposite_rotation_mirrors_lateral_curl(self) -> None:
        params = PaperPhysicsParams()
        positive, _ = simulate_tail([2.375, 21.52, 0.0, -1.8, 0.4], params)
        negative, _ = simulate_tail([2.375, 21.52, 0.0, -1.8, -0.4], params)
        self.assertAlmostEqual(positive[0] + negative[0], 2.0 * 2.375, places=8)
        self.assertAlmostEqual(positive[1], negative[1], places=8)

    def test_fitted_pipeline_returns_finite_landing(self) -> None:
        simulator = CalibratedPaperSimulator.from_file()
        final, stop_time = simulator.predict_landing(3.0, 0.0, 0.8)
        self.assertTrue(all(math.isfinite(value) for value in final))
        self.assertGreater(final[0], 0.0)
        self.assertGreater(final[1], 0.0)
        self.assertGreater(stop_time, 0.0)
        self.assertLess(stop_time, 40.0)

    def test_fitted_hybrid_pipeline_returns_finite_landing(self) -> None:
        simulator = CalibratedPaperSimulator.from_file()
        final, _ = simulator.predict_hybrid_landing(3.0, 0.0, -0.8)
        self.assertTrue(all(math.isfinite(value) for value in final))


if __name__ == "__main__":
    unittest.main()
