import unittest

from planning_proxy.tactical_library_strategy.double_outcome_goal import (
    anonymous_topology_mismatch,
    anonymous_topology_mismatch_features,
    bind_double_target_sets,
    double_outcome_contract_met,
)


PREDICATE_EMPTY = {
    "control": "NONE_OR_UNCERTAIN", "F_BUTTON": "0", "F_HOUSE_FRONT_LEFT": "0", "F_HOUSE_FRONT_RIGHT": "0",
    "F_HOUSE_BACK_LEFT": "0", "F_HOUSE_BACK_RIGHT": "0", "O_BUTTON": "0", "O_HOUSE_FRONT_LEFT": "0",
    "O_HOUSE_FRONT_RIGHT": "0", "O_HOUSE_BACK_LEFT": "0", "O_HOUSE_BACK_RIGHT": "0",
    "F_protected_house": "0", "O_protected_house": "0", "macro": "EMPTY",
}


class DoubleOutcomeGoalTests(unittest.TestCase):
    def test_binding_enumerates_current_opponent_house_pairs(self):
        contract = {"required_opponent_removed_count": 2, "target_binding": {"binding_mode": "DYNAMIC_OPPONENT_HOUSE_SET", "choose_count": 2}}
        board = [
            {"index": 1, "owner": "opponent", "x": 2.38, "y": 4.89},
            {"index": 2, "owner": "opponent", "x": 2.90, "y": 4.88},
            {"index": 3, "owner": "opponent", "x": 2.375, "y": 7.8},
        ]
        pairs = bind_double_target_sets(contract, board)
        self.assertEqual(pairs[0].target_indices, (1, 2))

    def test_whole_board_predicate_requires_both_target_out_and_empty_topology(self):
        contract = {"required_opponent_removed_count": 2, "terminal_board_predicate": PREDICATE_EMPTY}
        before = [
            {"index": 0, "owner": "self", "x": 2.375, "y": 4.88},
            {"index": 1, "owner": "opponent", "x": 2.40, "y": 4.88},
            {"index": 2, "owner": "opponent", "x": 2.60, "y": 4.88},
        ]
        final = [{"enabled": False, "x": 0.0, "y": 0.0} for _ in range(4)]
        self.assertTrue(double_outcome_contract_met(
            contract, target_indices=(1, 2), final_states=final, initial_local_board=before,
            own_throw_number=7, active_index=3, mirrored_from_runtime_board=False,
        ))
        final[2] = {"enabled": True, "x": 2.60, "y": 4.88}
        self.assertFalse(double_outcome_contract_met(
            contract, target_indices=(1, 2), final_states=final, initial_local_board=before,
            own_throw_number=7, active_index=3, mirrored_from_runtime_board=False,
        ))
        self.assertGreater(anonymous_topology_mismatch(
            contract, final_states=final, initial_local_board=before, own_throw_number=7,
            active_index=3, mirrored_from_runtime_board=False,
        ), 0)
        self.assertIn("O_BUTTON", anonymous_topology_mismatch_features(
            contract, final_states=final, initial_local_board=before, own_throw_number=7,
            active_index=3, mirrored_from_runtime_board=False,
        ))

    def test_semantic_contract_uses_same_full_gk_predicate_as_other_physx_routes(self):
        contract = {
            "K": 3,
            "semantic_effect": {"first_house_delta": 1, "opponent_house_delta": -2, "opponent_removed_count": 2, "opponent_house_removed_count": 2},
            "semantic_terminal_predicate": {"control": "FIRST", "macro": "FIRST_HOUSE_CONTROL"},
            "required_removed_stones": [{"index": 1}, {"index": 2}],
            "active_final_region": {"shape": "circle", "centre_x_m": 0.0, "centre_y_m": 0.0, "radius_m": 0.2},
        }
        before = [
            {"index": 1, "owner": "opponent", "x": 2.40, "y": 4.88},
            {"index": 2, "owner": "opponent", "x": 2.60, "y": 4.88},
        ]
        final = [{"enabled": False, "x": 0.0, "y": 0.0} for _ in range(5)]
        final[4] = {"enabled": True, "x": 2.375, "y": 4.88}
        self.assertEqual(bind_double_target_sets(contract, before)[0].target_indices, (1, 2))
        self.assertTrue(double_outcome_contract_met(
            contract, target_indices=(1, 2), final_states=final, initial_local_board=before,
            own_throw_number=3, active_index=4, mirrored_from_runtime_board=False,
        ))


if __name__ == "__main__":
    unittest.main()
