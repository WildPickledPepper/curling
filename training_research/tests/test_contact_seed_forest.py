import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import numpy as np

from training_research.contact_seed_forest import board_fold, encode_request, learned_initials, impact_action, impact_features


class ContactSeedForestTests(unittest.TestCase):
    def setUp(self):
        self.scene = json.loads((Path(__file__).parents[1]/"fixtures/sampled_goal_collision.json").read_text(encoding="utf-8"))

    def test_online_features_ignore_reference_action_seed_and_final_pose(self):
        first = self.scene["selection"]["first_contact_any"][0]
        expected = encode_request(self.scene, first)
        changed = copy.deepcopy(self.scene)
        changed.update(shot=[6., 2., 15.], physics_seed=1, physical_final="must not be read")
        self.assertEqual(expected.shape, (88,))
        np.testing.assert_array_equal(expected, encode_request(changed, first))

    def test_current_board_in_training_is_rejected_before_any_prediction(self):
        key = self.scene["scene_key"]
        with patch("training_research.contact_seed_forest.load_fold", return_value=({}, {key})), \
             patch("training_research.contact_seed_forest.predict_trees", side_effect=AssertionError("leak")):
            with self.assertRaisesRegex(ValueError, "leaked"):
                learned_initials(self.scene)
        self.assertIn(board_fold(key), range(5))

    def test_contact_coordinate_round_trip_and_request_only_features(self):
        first = self.scene["selection"]["first_contact_any"][0]
        target = next(s for s in self.scene["stones"] if s["index"] == first)
        shot = np.array((5.4, .12, -8.))
        with patch("training_research.inverse_initials.path_array", return_value=np.zeros((2, 4))), \
             patch("training_research.inverse_initials.interpolate", return_value=(np.array([2.5, 5., 0., -1.]), 1)):
            encoded = impact_action(shot, target)
            np.testing.assert_allclose(impact_action(encoded, target, decode=True), shot, rtol=0., atol=1e-15)
        changed = copy.deepcopy(self.scene)
        changed.update(shot=[6., 2., 15.], physics_seed=1, physical_final="must not be read")
        expected = impact_features(self.scene, first)
        self.assertEqual(expected.shape, (94,))
        np.testing.assert_array_equal(expected, impact_features(changed, first))


if __name__ == "__main__":
    unittest.main()
