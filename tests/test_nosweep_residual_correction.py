from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from tools.reverse.nosweep_residual_correction import correct_endpoint, predict_residual


class NoSweepResidualCorrectionTest(unittest.TestCase):
    def test_predict_residual_uses_motion_features(self) -> None:
        payload = {
            "features": ["1", "motion_speed", "motion_vx", "motion_w", "abs_motion_w", "motion_w2", "motion_vx_motion_w"],
            "coefficients_dx": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],
            "coefficients_dy": [-1.0, -2.0, -3.0, -4.0, -5.0, -6.0, -7.0],
        }
        dx, dy = predict_residual(payload, motion_vx=3.0, motion_vy=4.0, motion_w=-2.0)
        expected = 1.0 + 2.0 * 5.0 + 3.0 * 3.0 + 4.0 * -2.0 + 5.0 * 2.0 + 6.0 * 4.0 + 7.0 * -6.0

        self.assertTrue(math.isclose(dx, expected))
        self.assertTrue(math.isclose(dy, -expected))

    def test_correct_endpoint_subtracts_sim_minus_unity_residual(self) -> None:
        payload = {
            "features": ["1"],
            "coefficients_dx": [0.03],
            "coefficients_dy": [-0.02],
        }

        self.assertEqual(
            correct_endpoint(2.0, 5.0, motion_vx=0.0, motion_vy=-1.0, motion_w=0.0, payload=payload),
            (1.97, 5.02),
        )


if __name__ == "__main__":
    unittest.main()
