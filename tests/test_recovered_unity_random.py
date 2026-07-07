import unittest

from tools.reverse.recovered_unity_random import RecoveredUnityRandom


class RecoveredUnityRandomTest(unittest.TestCase):
    def test_init_state_matches_wasm_multiplier_chain(self):
        rng = RecoveredUnityRandom.from_seed(1)
        self.assertEqual((rng.s0, rng.s1, rng.s2, rng.s3), (0x00000001, 0x6C078966, 0x714ACB3F, 0xDBFFE6DC))

    def test_float_range_matches_recovered_sequence(self):
        rng = RecoveredUnityRandom.from_seed(1)
        values = [rng.range_float(-0.0002, 0.0002) for _ in range(3)]
        self.assertAlmostEqual(values[0], -0.00019987385894637555, places=15)
        self.assertAlmostEqual(values[1], -0.00010970510629704222, places=15)
        self.assertAlmostEqual(values[2], -0.0000723935299902223, places=15)

    def test_int_range_uses_unsigned_modulo(self):
        rng = RecoveredUnityRandom.from_seed(1)
        self.assertEqual([rng.range_int(0, 10) for _ in range(5)], [4, 8, 6, 2, 0])


if __name__ == "__main__":
    unittest.main()
