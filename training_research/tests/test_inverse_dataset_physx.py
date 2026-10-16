"""Native observer equivalence gate; run with bundled Windows CP39."""
import json
import sys
import unittest


@unittest.skipUnless(sys.version_info[:2] == (3, 9) and sys.platform == "win32", "bundled CP39 native gate")
class InverseDatasetPhysXTests(unittest.TestCase):
    def test_recording_does_not_change_prediction_or_random_consumption(self):
        from training_research.inverse_dataset.cli import make_environment, reset_environment
        from training_research.inverse_dataset.sampling import synthetic_scene
        from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd
        recorded = make_environment()
        baseline = StrictCurlingEnd(seed=0)
        cases = [
            (synthetic_scene(1, 20261004), [3.4, 0.0, 0.0]),
            (synthetic_scene(3, 20261004), [6.0, 0.2, 0.0]),
            (synthetic_scene(2, 20261004), [3.35, 0.18, 9.42]),
        ]
        for i, (scene, shot) in enumerate(cases):
            with self.subTest(case=i):
                reset_environment(recorded, scene, 100 + i)
                observed = recorded.play(shot)
                reset_environment(baseline, scene, 100 + i)
                original = baseline.play(shot)
                # Round-trip float representations, zero signs, all 16 native
                # states, RNG state, clock, first contact and counters match.
                self.assertEqual(json.dumps(observed, sort_keys=True, allow_nan=False),
                                 json.dumps(original, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    unittest.main()
