import unittest

from training_data.nwnht_curling.causal_state_machine.verify_causal_artifacts import _independent_primary_violation, key, same


class VerifyHelperTests(unittest.TestCase):
    def test_key_and_canonical_equality(self):
        self.assertEqual(key({"end_id": 4, "own_throw_number": 2}), (4, 2))
        self.assertTrue(same({"a": [1, 2]}, {"a": [1, 2]}))
        self.assertFalse(same({"a": 1}, {"a": 2}))

    def test_independent_contract_accepts_a_real_house_addition(self):
        row = {
            "s_before_own": [],
            "u_after_own": [{"owner": "first", "x_m": 0.0, "y_m": 0.0}],
            "observed_own_board_effect": {"primary_effect": "ADD_OWN_HOUSE_LAYER"},
        }
        self.assertIsNone(_independent_primary_violation(row))

    def test_independent_contract_rejects_false_clear_label(self):
        row = {
            "s_before_own": [{"owner": "opponent", "x_m": 0.0, "y_m": 0.0}],
            "u_after_own": [{"owner": "opponent", "x_m": 0.0, "y_m": 0.0}],
            "observed_own_board_effect": {"primary_effect": "REDUCE_STONE_COUNT_WITHOUT_CONTROL"},
        }
        self.assertEqual(_independent_primary_violation(row), "stone_count_not_reduced")


if __name__ == "__main__":
    unittest.main()
