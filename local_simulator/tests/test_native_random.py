"""Exact state and float mapping of the optional per-draw native helper."""
import random
import struct
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from local_simulator.native_random import NativeUnityRandom, load_random_kernel
from local_simulator.runtime_support.tools.reverse.recovered_unity_random import RecoveredUnityRandom
from local_simulator.runtime_support.tools.reverse.recovered_curling_motion import unity_friction
from local_simulator.runtime_support.tools.reverse.front_half_pcm_replay import iter_unity_friction_noises
from local_simulator.unity_prediction import UnityPredictionDriver


def state(rng):
    return rng.s0, rng.s1, rng.s2, rng.s3


@unittest.skipUnless(load_random_kernel() is not None, 'optional Windows random helper unavailable')
class NativeRandomTest(unittest.TestCase):
    def test_state_words_and_asymmetric_float_ranges_match(self):
        sampler = random.Random(20261003)
        inputs = [(0, 0, 0, 0), (0xffffffff,)*4]
        inputs += [tuple(sampler.getrandbits(32) for _ in range(4)) for _ in range(100)]
        ranges = [(-.0002, .0002), (-7.3, 19.9), (3.27, 19.73), (-0., 0.)]
        for words in inputs:
            native, reference = NativeUnityRandom(words), RecoveredUnityRandom(*words)
            for _ in range(50):
                self.assertEqual(native.next_u32(), reference.next_u32())
                for minimum, maximum in ranges:
                    self.assertEqual(struct.pack('<f', native.range_float(minimum, maximum)),
                                     struct.pack('<f', reference.range_float(minimum, maximum)))
                self.assertEqual(state(native), state(reference))

    def test_friction_iterator_is_lazy_and_matches_both_material_modes(self):
        for seed in (0, 1, -1, 20261003, 2**32+17):
            for sweeping in (False, True):
                native, reference = NativeUnityRandom.from_seed(seed), RecoveredUnityRandom.from_seed(seed)
                a = native.friction_noises(sweeping=sweeping)
                b = iter_unity_friction_noises(reference, sweeping=sweeping)
                self.assertEqual(state(native), state(reference))
                for _ in range(2000):
                    noise_a, noise_b = next(a), next(b)
                    self.assertEqual(struct.pack('<d', noise_a), struct.pack('<d', noise_b))
                    self.assertEqual(state(native), state(reference))
                    self.assertEqual(struct.pack('<f', unity_friction(sweeping, noise=noise_a)),
                                     struct.pack('<f', unity_friction(sweeping, noise=noise_b)))


class NativeRandomFallbackTest(unittest.TestCase):
    def test_missing_helper_and_injected_inputs_preserve_reference_stream(self):
        scene = SimpleNamespace(coordinate_mode='unity-native-yup',
            emulate_unity_setactive_no_sim=True, _custom_sliding_index=0,
            _custom_sliding_release_origin=(0., 0., 0.), dt=.01)
        with patch('local_simulator.native_random.load_random_kernel', return_value=None):
            driver = UnityPredictionDriver(scene, 0, seed=123, use_lean_steps=True)
        reference = RecoveredUnityRandom.from_seed(123)
        noises = iter_unity_friction_noises(reference)
        self.assertNotIsInstance(driver.rng, NativeUnityRandom)
        for _ in range(100):
            self.assertEqual(next(driver.noises), next(noises))
            self.assertEqual(state(driver.rng), state(reference))
        with patch('local_simulator.native_random.load_random_kernel') as loader:
            supplied = UnityPredictionDriver(scene, 0, noises=[.1, .2], use_lean_steps=True)
            self.assertEqual(list(supplied.noises), [.1, .2])
            self.assertIsNone(supplied.rng)
            loader.assert_not_called()


if __name__ == '__main__':
    unittest.main()
