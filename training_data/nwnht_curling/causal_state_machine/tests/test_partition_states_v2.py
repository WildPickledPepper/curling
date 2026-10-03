import unittest

from training_data.nwnht_curling.causal_state_machine.partition_states_v2 import (
    Observation,
    best_stable_split,
    classify_runtime_state,
    macro_type,
    total_variation,
)


def feature(**changes):
    base = {
        "F_visible": "1", "O_visible": "1", "F_visible_exact": 1, "O_visible_exact": 1,
        "F_house_exact": 0, "O_house_exact": 1, "control": "OPPONENT",
        "F_BUTTON": "0", "F_HOUSE_FRONT_LEFT": "0", "F_HOUSE_FRONT_RIGHT": "0", "F_HOUSE_BACK_LEFT": "0", "F_HOUSE_BACK_RIGHT": "0",
        "O_BUTTON": "1", "O_HOUSE_FRONT_LEFT": "0", "O_HOUSE_FRONT_RIGHT": "0", "O_HOUSE_BACK_LEFT": "0", "O_HOUSE_BACK_RIGHT": "0",
        "F_GUARD_NEAR_CENTRE": "0", "F_GUARD_FAR_CENTRE": "0", "F_GUARD_NEAR_LEFT": "0", "F_GUARD_FAR_LEFT": "0", "F_GUARD_NEAR_RIGHT": "0", "F_GUARD_FAR_RIGHT": "0",
        "O_GUARD_NEAR_CENTRE": "0", "O_GUARD_FAR_CENTRE": "0", "O_GUARD_NEAR_LEFT": "0", "O_GUARD_FAR_LEFT": "0", "O_GUARD_NEAR_RIGHT": "0", "O_GUARD_FAR_RIGHT": "0",
        "F_protected_house": "0", "O_protected_house": "0", "O_house_pair_proximity": "NO_PAIR",
    }
    base.update(changes)
    return base


class PartitionStateV2Tests(unittest.TestCase):
    def test_macro_layer_is_explicit_and_not_a_safety_label(self):
        self.assertEqual(macro_type(feature(O_GUARD_NEAR_CENTRE="1")), "OPPONENT_CENTRE_CONFIGURATION")
        self.assertEqual(macro_type(feature(control="FIRST", F_BUTTON="1", O_BUTTON="0", F_house_exact=1, O_house_exact=0)), "FIRST_HOUSE_CONTROL")
        self.assertNotEqual(macro_type(feature(F_visible="2P", F_visible_exact=4, O_visible="0", O_visible_exact=0, F_house_exact=0, O_house_exact=0)), "SPARSE_OPEN")

    def test_total_variation_requires_two_nonempty_distributions(self):
        self.assertIsNone(total_variation({}, {"a": 1}))
        self.assertEqual(total_variation({"a": 2}, {"a": 2}), 0.0)
        self.assertEqual(total_variation({"a": 2}, {"b": 2}), 1.0)

    def test_split_requires_train_and_holdout_replication(self):
        rows = []
        # Two values, both with distinct transition signatures in each split.
        for match_id in range(400):
            side = "1" if match_id % 2 else "0"
            token = "A" if side == "1" else "B"
            rows.append(Observation(str(match_id), match_id, 5, "MIXED_CONTESTED", feature(F_protected_house=side), token))
        split = best_stable_split(
            rows,
            split_for_match=lambda match_id: "holdout" if match_id % 5 == 0 else "train",
            split_features=("F_protected_house",),
        )
        self.assertIsNotNone(split)
        self.assertEqual(split.feature, "F_protected_house")
        self.assertEqual(split.value, "1")
        self.assertEqual(split.train_tv, 1.0)
        self.assertEqual(split.holdout_tv, 1.0)

    def test_split_is_rejected_when_holdout_has_no_difference(self):
        rows = []
        for match_id in range(400):
            side = "1" if match_id % 2 else "0"
            token = ("A" if side == "1" else "B") if match_id % 5 else "A"
            rows.append(Observation(str(match_id), match_id, 5, "MIXED_CONTESTED", feature(F_protected_house=side), token))
        split = best_stable_split(
            rows,
            split_for_match=lambda match_id: "holdout" if match_id % 5 == 0 else "train",
            split_features=("F_protected_house",),
        )
        self.assertIsNone(split)

    def test_runtime_assignment_returns_supported_or_search_required_leaf(self):
        partition = {
            "states": [{
                "state_id": "K5_TEST", "K": 5, "macro_state": "OPPONENT_HOUSE_THREAT",
                "rule": [], "eligible_for_next_goal_stage": False,
            }]
        }
        board = [
            {"owner": "opponent", "x_m": 0.1, "y_m": 0.1},
            {"owner": "first", "x_m": 0.9, "y_m": 0.5},
        ]
        assigned = classify_runtime_state(partition, 5, board)
        self.assertEqual(assigned["state_id"], "K5_TEST")
        self.assertEqual(assigned["status"], "SEARCH_REQUIRED_INSUFFICIENT_STATE_SUPPORT")


if __name__ == "__main__":
    unittest.main()
