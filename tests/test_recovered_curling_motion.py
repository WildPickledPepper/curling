import math
import unittest
from pathlib import Path

from tools.reverse.recovered_curling_motion import (
    BASE_FRICTION,
    EPS,
    FSIMP_SAFETY_MAX_ITERATIONS,
    PI,
    STEP,
    SWEEP_FRICTION,
    B2Vec2,
    MyParams,
    SUPPORTED_KERNELS,
    fsimp_diagnostics,
    integrand,
    recovered_unity_friction_from_seed,
    newfrictionstep,
    unity_friction,
)
from tools.reverse.recovered_unity_random import RecoveredUnityRandom
from tools.reverse.probe_unity_tail_mapping import evaluate, read_rows


PROJECT_ROOT = Path(__file__).resolve().parents[1]


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

    def test_recovered_fsimp_dispatch_has_22_unique_kernels(self):
        self.assertEqual(len(SUPPORTED_KERNELS), 22)
        self.assertEqual(len(set(SUPPORTED_KERNELS)), 22)
        self.assertEqual(SUPPORTED_KERNELS[0], (1, 1))
        self.assertEqual(SUPPORTED_KERNELS[-1], (3, 8))

    def test_all_recovered_integrands_are_finite(self):
        params = MyParams(vx=0.7, vy=1.3, w=2.0, r1=0.122, r2=0.128)

        for type_, index in SUPPORTED_KERNELS:
            with self.subTest(type=type_, index=index):
                self.assertTrue(math.isfinite(integrand(type_, index, 0.37, params)))

    def test_recovered_fsimp_converges_before_local_safety_cap(self):
        params = MyParams(vx=0.7, vy=1.3, w=2.0, r1=0.122, r2=0.128)

        for type_, index in SUPPORTED_KERNELS:
            with self.subTest(type=type_, index=index):
                diagnostics = fsimp_diagnostics(0.0, PI / 2.0, EPS, params, type_, index)
                self.assertTrue(diagnostics.converged)
                self.assertLess(diagnostics.iterations, FSIMP_SAFETY_MAX_ITERATIONS)
                self.assertTrue(math.isfinite(diagnostics.value))

    def test_unsupported_integrand_raises(self):
        params = MyParams(vx=0.7, vy=1.3, w=2.0, r1=0.122, r2=0.128)

        with self.assertRaises(ValueError):
            integrand(3, 9, 0.37, params)

    def test_recovered_middle_speed_band_is_finite(self):
        result = newfrictionstep(BASE_FRICTION, B2Vec2(0.2, 1.1), 0.5, STEP)

        self.assertTrue(math.isfinite(result.v.x))
        self.assertTrue(math.isfinite(result.v.y))
        self.assertTrue(math.isfinite(result.angle))

    def test_protocol_tail_replay_rejects_wrong_position_timestep(self):
        rows = read_rows([PROJECT_ROOT / "data" / "calibration" / "no_sweep_200.jsonl"], limit=1)

        unity_dt = evaluate(
            rows,
            dt_pos=0.010,
            sx=1,
            sy=1,
            sw=1,
            max_steps=5000,
            x_bound=10.0,
            y_min=-10.0,
            y_max=30.0,
            speed_bound=10.0,
            direction_precheck=False,
        )
        slow_dt = evaluate(
            rows,
            dt_pos=0.009,
            sx=1,
            sy=1,
            sw=1,
            max_steps=5000,
            x_bound=10.0,
            y_min=-10.0,
            y_max=30.0,
            speed_bound=10.0,
            direction_precheck=False,
        )
        fast_dt = evaluate(
            rows,
            dt_pos=0.011,
            sx=1,
            sy=1,
            sw=1,
            max_steps=5000,
            x_bound=10.0,
            y_min=-10.0,
            y_max=30.0,
            speed_bound=10.0,
            direction_precheck=False,
        )

        self.assertLess(unity_dt["rmse"], 0.06)
        self.assertGreater(slow_dt["rmse"], 1.0)
        self.assertGreater(fast_dt["rmse"], 1.0)

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
