import unittest

from planning_proxy.tactical_library_strategy.semantic_goal_contract import instantiate_goal_contracts, semantic_transition_met


class SemanticGoalContractTests(unittest.TestCase):
    def test_binds_current_opponent_house_stone_and_checks_transition(self):
        candidate = {
            "source_state": "K8_TEST", "K": 8,
            "after_opponent_reply_state_distribution": [{"value": "END", "count": 1, "share": 1.0}],
            "goal_state": {
                "goal_id": "G", "K": 8,
                "semantic_effect": {"first_house_delta": 0, "opponent_house_delta": -1, "opponent_removed_count": 1, "opponent_house_removed_count": 1},
                "semantic_terminal_predicate": {"control": "NONE_OR_UNCERTAIN", "macro": "EMPTY"},
                "post_own_topology_distribution": [],
                "fine_execution_status": "HAS_HISTORICAL_FINE_IMPLEMENTATION",
                "fine_goal_options": [{"historical_support": 9, "active_final_region": None, "stone_constraints_when_unambiguous": [], "dynamic_house_removal_binding_request": {"binding_kind": "OPPONENT_HOUSE_SET"}, "after_own_occupancy": {}}],
            },
        }
        before = [{"owner": "opponent", "x_m": 0.1, "y_m": 0.2, "index": 7}]
        result = instantiate_goal_contracts(before, candidate)
        self.assertEqual(result["contract_status"], "CONTRACT_READY_FOR_PATH_SEARCH")
        self.assertEqual(result["contracts"][0]["required_removed_stones"][0]["index"], 7)
        self.assertTrue(semantic_transition_met(before, [], result))

    def test_rejects_cross_k_candidate(self):
        candidate = {"source_state": "K1_TEST", "K": 1, "goal_state": {"goal_id": "G", "K": 2}}
        with self.assertRaises(ValueError):
            instantiate_goal_contracts([], candidate)

    def test_contextual_fine_override_replaces_global_fine_child(self):
        candidate = {
            "source_state": "K1_TEST", "K": 1,
            "after_opponent_reply_state_distribution": [],
            "goal_state": {
                "goal_id": "G", "K": 1,
                "semantic_effect": {"first_house_delta": 0, "opponent_house_delta": 0, "opponent_removed_count": 0, "opponent_house_removed_count": 0},
                "semantic_terminal_predicate": {"control": "NONE_OR_UNCERTAIN", "macro": "EMPTY"},
                "post_own_topology_distribution": [], "fine_execution_status": "HAS_HISTORICAL_FINE_IMPLEMENTATION",
                "fine_goal_options": [],
            },
        }
        override = [{"active_final_region": {"shape": "circle", "centre_x_m": 0.2, "centre_y_m": 0.3, "radius_m": 0.12}, "neighbour_support": 4}]
        result = instantiate_goal_contracts([], candidate, fine_options_override=override)
        self.assertEqual(result["fine_option_source"], "CONTEXTUAL_NEAREST_NEIGHBOURS")
        self.assertAlmostEqual(result["contracts"][0]["active_final_region"]["centre_x_m"], 0.2)


if __name__ == "__main__":
    unittest.main()
