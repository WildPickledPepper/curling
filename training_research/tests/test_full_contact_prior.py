import copy
import unittest

import numpy as np

from training_research.contact_seed_forest import impact_features
from training_research.full_contact_prior import full_features


class FullBoardFeatureTests(unittest.TestCase):
    def test_far_required_goal_is_encoded_and_reference_fields_are_ignored(self):
        stones = [{"index": i, "x": 2.375+.35*i, "y": 5.5, "yaw": 0.} for i in range(6)]
        request = {"active_index": 7, "stones": stones, "selection": {
            "first_contact_any": [0], "goal": {"stones": {
                str(s["index"]): {"type": "IN_REGION", "x": s["x"], "y": s["y"], "radius": .15}
                for s in stones}}}}
        request["selection"]["goal"]["stones"]["7"] = {"type": "OUT_OF_PLAY"}
        changed = copy.deepcopy(request)
        changed["selection"]["goal"]["stones"]["5"] = {"type": "OUT_OF_PLAY"}
        np.testing.assert_array_equal(impact_features(request, 0), impact_features(changed, 0))
        self.assertEqual(full_features(request, 0).shape, (319,))
        self.assertFalse(np.array_equal(full_features(request, 0), full_features(changed, 0)))
        expected = full_features(changed, 0)
        changed.update(shot=[6., 0., 9.], physics_seed=1, physical_final="must not be read")
        np.testing.assert_array_equal(expected, full_features(changed, 0))


if __name__ == "__main__":
    unittest.main()
