import unittest
from unittest.mock import patch
from itertools import islice

import numpy as np

from training_research.inverse_goal_search import clip, solve
from training_research.solver_experiments import streamed_initials, augmented_initials


class StreamedSolverTests(unittest.TestCase):
    def test_simple_collision_is_certified_before_expensive_initials_are_generated(self):
        scene = {"scene_key": "board", "active_index": 3,
                 "stones": [{"index": 1, "x": 2.4, "y": 4.8, "yaw": .3}],
                 "selection": {"tactic": "achieved_goal", "first_contact_any": [1],
                               "goal": {"stones": {"1": {"type": "OUT_OF_PLAY"}}}}}
        record = {"status": "complete", "task_failure": None,
                  "physical_final": [{"index": 1, "enabled": False, "x": 0., "y": 0.}],
                  "prediction": {"settled": True, "firstContactTargets": [1]},
                  "collision_events": [], "rule_violations": []}
        calls = []
        def evaluate(shot, seed, phase):
            calls.append(shot)
            return record
        with patch("training_research.inverse_initials.path_array", return_value=np.zeros((2, 4))), \
             patch("training_research.inverse_initials.interpolate", return_value=(np.array([2.375, 5.09, 0., -1.]), 1)), \
             patch("training_research.inverse_contact_atlas.atlas_initials", side_effect=AssertionError("unneeded atlas")), \
             patch("training_research.inverse_goal_search.proposals", side_effect=AssertionError("unneeded full grid")):
            result, diagnostics = solve(scene, evaluate=evaluate, elapsed=lambda: 0.,
                                        initial_provider=streamed_initials)
        self.assertEqual(result[0]["bestshot"], [6., .025, 0.])
        self.assertEqual(len(calls), 1)
        self.assertTrue(diagnostics["initial_success"])

    def test_exhausted_time_does_not_start_another_free_path(self):
        scene = {"active_index": 0, "stones": [], "selection": {
            "require_no_contact": True, "goal": {"stones": {
                "0": {"type": "IN_REGION", "x": 2.375, "y": 4.88, "radius": .15}}}}}
        with patch("training_research.inverse_initials.path_array", side_effect=AssertionError("budget exhausted")):
            self.assertEqual(list(streamed_initials(scene, lambda: 10., 10., clip, {})), [])

    def test_augmentation_keeps_all_24_original_candidates_before_reading_prior(self):
        original = [(3.+i*.01, 0., 0.) for i in range(30)]
        scene = {"selection": {"first_contact_any": [0]}}
        with patch("training_research.solver_experiments.fast_first_initials", return_value=iter(original)), \
             patch("training_research.full_contact_prior.proposals", return_value=[(5., .1, 3.)]) as model:
            source = augmented_initials(scene, lambda: 0., 10., clip, {})
            self.assertEqual(list(islice(source, 24)), original[:24])
            model.assert_not_called()
            self.assertEqual(next(source), (5., .1, 3.))
            self.assertEqual(list(source), original[24:])


if __name__ == "__main__":
    unittest.main()
