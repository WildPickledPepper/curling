import unittest

from training_data.nwnht_curling.causal_state_machine.state_features_v2 import (
    canonical_orientation,
    micro_state_key,
    state_features,
    stone_zone,
)


def stone(owner, x, y):
    return {"owner": owner, "x_m": x, "y_m": y}


class StateFeaturesV2Tests(unittest.TestCase):
    def test_zone_partition_keeps_button_house_and_guard_distinct(self):
        self.assertEqual(stone_zone(stone("first", 0.1, 0.1)), "BUTTON")
        self.assertEqual(stone_zone(stone("first", -0.9, 0.5)), "HOUSE_FRONT_LEFT")
        self.assertEqual(stone_zone(stone("first", 0.9, -0.5)), "HOUSE_BACK_RIGHT")
        self.assertEqual(stone_zone(stone("first", 0.0, 2.2)), "GUARD_NEAR_CENTRE")
        self.assertEqual(stone_zone(stone("first", 0.8, 5.0)), "GUARD_FAR_RIGHT")

    def test_left_right_mirrors_share_a_micro_state_but_preserve_orientation(self):
        right = [stone("first", 0.8, 0.5), stone("opponent", 1.0, 3.0)]
        left = [stone("first", -0.8, 0.5), stone("opponent", -1.0, 3.0)]
        self.assertEqual(micro_state_key(5, right), micro_state_key(5, left))
        self.assertNotEqual(
            canonical_orientation(5, right)["mirrored_from_runtime_board"],
            canonical_orientation(5, left)["mirrored_from_runtime_board"],
        )

    def test_features_record_cover_without_claiming_safety(self):
        board = [
            stone("first", 0.05, 0.1),
            stone("first", 0.10, 3.2),
            stone("opponent", -0.25, 0.2),
        ]
        features = state_features(4, board)
        self.assertEqual(features["F_BUTTON"], "1")
        self.assertEqual(features["F_GUARD_NEAR_CENTRE"], "1")
        self.assertEqual(features["F_protected_house"], "1")
        self.assertEqual(features["control"], "FIRST")

    def test_pair_feature_is_geometry_only(self):
        board = [stone("opponent", -0.1, 0.1), stone("opponent", 0.2, 0.2)]
        features = state_features(6, board)
        self.assertEqual(features["O_house_clear_cardinality"], "2P")
        self.assertEqual(features["O_house_pair_proximity"], "NEAR_PAIR")

    def test_rejects_non_runtime_input(self):
        with self.assertRaises(ValueError):
            state_features(0, [])
        with self.assertRaises(ValueError):
            state_features(2, [{"owner": "team_a", "x_m": 0.0, "y_m": 0.0}])


if __name__ == "__main__":
    unittest.main()
