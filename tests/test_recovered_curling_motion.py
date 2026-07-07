import math
import unittest

from tools.reverse.recovered_curling_motion import (
    BASE_FRICTION,
    STEP,
    SWEEP_FRICTION,
    B2Vec2,
    recovered_unity_friction_from_seed,
    newfrictionstep,
    unity_friction,
)
from tools.reverse.recovered_unity_random import RecoveredUnityRandom


class RecoveredCurlingMotionTest(unittest.TestCase):
    def test_stationary_step_returns_zero(self):
        result = newfrictionstep(BASE_FRICTION, B2Vec2(0.0, 0.0), 0.0, STEP)

        self.assertEqual(result.v.x, 0.0)
        self.assertEqual(result.v.y, 0.0)
        self.assertEqual(result.angle, 0.0)

    def test_recovered_step_is_finite(self):
        result = newfrictionstep(BASE_FRICTION, B2Vec2(1.0, 2.0), 5.0, STEP)

        self.assertTrue(math.isfinite(result.v.x))
        self.assertTrue(math.isfinite(result.v.y))
        self.assertTrue(math.isfinite(result.angle))

    def test_recovered_middle_speed_band_is_finite(self):
        result = newfrictionstep(BASE_FRICTION, B2Vec2(0.2, 1.1), 0.5, STEP)

        self.assertTrue(math.isfinite(result.v.x))
        self.assertTrue(math.isfinite(result.v.y))
        self.assertTrue(math.isfinite(result.angle))

    def test_sweep_friction_matches_unity_constant(self):
        self.assertAlmostEqual(unity_friction(False, noise=0.0), 0.001)
        self.assertAlmostEqual(unity_friction(True, noise=0.0), SWEEP_FRICTION)

    def test_unity_friction_uses_recovered_rng_when_available(self):
        rng = RecoveredUnityRandom.from_seed(1)

        self.assertAlmostEqual(unity_friction(False, rng=rng, noise=None), 0.0008001261410536245, places=15)
        self.assertAlmostEqual(unity_friction(False, rng=rng, noise=None), 0.0008902948937029578, places=15)

    def test_recovered_unity_friction_sequence_from_seed(self):
        values = recovered_unity_friction_from_seed(1, sweeping=True, count=2)

        self.assertAlmostEqual(values[0], 0.00040012614105362444, places=15)
        self.assertAlmostEqual(values[1], 0.0004902948937029578, places=15)


if __name__ == "__main__":
    unittest.main()
