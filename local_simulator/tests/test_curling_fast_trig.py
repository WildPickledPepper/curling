"""Pure-Python numerical guard for the native CurlingMotion fast path.

This intentionally imports no pyphysx extension.  It checks the algebra used
by ``CURLING_FAST_TRIG`` against the recovered literal Unity formula.
"""

from __future__ import annotations

import math
import random
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


RUNTIME_SUPPORT = Path(__file__).resolve().parents[1] / "runtime_support"
if str(RUNTIME_SUPPORT) not in sys.path:
    sys.path.insert(0, str(RUNTIME_SUPPORT))

from tools.reverse import recovered_curling_motion as motion


class CurlingFastTrigTest(unittest.TestCase):
    def test_direct_integrand_matches_literal_formula_over_physical_domain(self):
        rng = random.Random(20260722)
        for _ in range(256):
            params = motion.MyParams(
                vx=rng.uniform(0.01, 6.0),
                vy=rng.uniform(0.0, 6.0),
                w=rng.uniform(1e-6, 30.0),
                r1=motion.R1,
                r2=motion.R2,
            )
            x = rng.uniform(0.0, motion.PI / 2.0)
            for kernel in motion.SUPPORTED_KERNELS:
                literal = motion.integrand(*kernel, x, params)
                direct = motion.integrand_direct_trig(*kernel, x, params)
                self.assertTrue(math.isfinite(literal))
                self.assertTrue(math.isfinite(direct))
                self.assertLessEqual(abs(literal - direct), 2e-12)

    def test_complete_step_preserves_physx_float_inputs(self):
        # Exercise the three recovered speed branches.  PhysX receives these
        # values after f64 computation is rounded to f32.
        cases = (
            (0.30, 0.12, 8.0),
            (1.30, 0.12, 8.0),
            (2.60, 0.12, 8.0),
        )
        for vx, vy, angular in cases:
            literal = motion.newfrictionstep(
                0.001, motion.B2Vec2(vx, vy), angular, motion.STEP
            )
            with patch.object(motion, "integrand", motion.integrand_direct_trig):
                direct = motion.newfrictionstep(
                    0.001, motion.B2Vec2(vx, vy), angular, motion.STEP
                )
            self.assertEqual(motion._f32(literal.v.x), motion._f32(direct.v.x))
            self.assertEqual(motion._f32(literal.v.y), motion._f32(direct.v.y))
            self.assertEqual(motion._f32(literal.angle), motion._f32(direct.angle))


if __name__ == "__main__":
    unittest.main()
