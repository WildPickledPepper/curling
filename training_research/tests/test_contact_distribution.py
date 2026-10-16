import unittest
from unittest.mock import patch

import numpy as np

from training_research.contact_distribution_prior import conditional_weights, proposals, joint_groups


class ContactDistributionTests(unittest.TestCase):
    def setUp(self):
        self.model = {"offsets": np.array([0, 3, 6]), "max_depth": np.asarray(1),
            "features": np.array([0, -2, -2, 0, -2, -2]),
            "thresholds": np.array([.5, -2., -2., .5, -2., -2.]),
            "left": np.array([1, -1, -1, 1, -1, -1]), "right": np.array([2, -1, -1, 2, -1, -1]),
            "leaf_row_offsets": np.array([0, 0, 2, 4, 4, 6, 8]),
            "leaf_row_indices": np.array([0, 1, 2, 3, 0, 2, 1, 3]),
            "training_y": np.array([[5./6., .2, 7./15.7], [4./6., -.1, -9./15.7],
                                    [4.5/6., .5, 2./15.7], [5.5/6., -.3, -4./15.7]]),
            "training_row_boards": np.array(["other"]*4)}
        self.request = {"scene_key": "0"*64, "active_index": 5,
            "stones": [{"index": 0, "x": 2.375, "y": 4.8}],
            "selection": {"first_contact_any": [0], "goal": {"stones": {
                "0": {"type": "IN_REGION", "x": 2.4, "y": 4.4, "radius": .15},
                "5": {"type": "IN_REGION", "x": 2., "y": 4.8, "radius": .15}}}}}

    def tearDown(self):
        joint_groups.cache_clear()

    def test_weights_retain_the_leaf_empirical_distribution(self):
        np.testing.assert_allclose(conditional_weights(self.model, np.array([.2])), [.5, .25, .25, 0.], rtol=0., atol=1e-15)

    def test_proposals_keep_joint_actions_instead_of_mixing_axis_quantiles(self):
        with patch("training_research.contact_distribution_prior.load_fold", return_value=(self.model, {"other"})), \
             patch("training_research.contact_distribution_prior._anchor", return_value=2.375):
            actual = proposals(self.request, path="test-model", limit=3)
        self.assertGreaterEqual(len(actual), 2)
        source = self.model["training_y"]*np.array([6., .29, 15.7])
        for action in actual:
            self.assertTrue(any(np.allclose(action, row, rtol=0., atol=1e-12) for row in source))

    def test_query_board_is_rejected_before_leaf_scoring(self):
        with patch("training_research.contact_distribution_prior.load_fold", return_value=({}, {"0"*64})), \
             patch("training_research.contact_distribution_prior.conditional_weights", side_effect=AssertionError("leak")):
            with self.assertRaisesRegex(ValueError, "leaked"):
                proposals(self.request, path="test-model")


if __name__ == "__main__":
    unittest.main()
