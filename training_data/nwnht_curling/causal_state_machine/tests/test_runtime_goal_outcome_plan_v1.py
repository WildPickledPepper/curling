import unittest

from training_data.nwnht_curling.causal_state_machine.runtime_goal_outcome_plan_v1 import _unmirror_goal_state, load_default


class RuntimeGoalOutcomePlanTests(unittest.TestCase):
    def test_mirror_restores_topology_and_fine_endpoint_constraints(self):
        goal = {
            "tactical_target_zone": "HOUSE_FRONT_LEFT",
            "post_own_topology": "K8_POST_OWN[F_HOUSE_FRONT_LEFT=1;O_HOUSE_BACK_RIGHT=0]",
            "terminal_board_predicate": {"F_HOUSE_FRONT_LEFT": "1", "O_HOUSE_BACK_RIGHT": "0"},
            "fine_goal_options": [{
                "active_final_region": {"centre_x_m": -0.4},
                "after_own_occupancy": {"first": {"house_front_left": 1}},
                "stone_constraints_when_unambiguous": [{"historical_source_zone": "house_back_right"}],
            }],
        }
        mirrored = _unmirror_goal_state(goal)
        self.assertEqual(mirrored["tactical_target_zone"], "HOUSE_FRONT_RIGHT")
        self.assertIn("F_HOUSE_FRONT_RIGHT", mirrored["terminal_board_predicate"])
        self.assertAlmostEqual(mirrored["fine_goal_options"][0]["active_final_region"]["centre_x_m"], 0.4)
        self.assertEqual(mirrored["fine_goal_options"][0]["after_own_occupancy"]["first"], {"house_front_right": 1})

    def test_default_plan_never_invents_goal_for_k8_house_threat(self):
        planner = load_default()
        # Canonical K8 opponent-house threat: two opponent stones in house.
        result = planner.recommend(8, [
            {"owner": "opponent", "x_m": 0.15, "y_m": 0.20},
            {"owner": "opponent", "x_m": 0.55, "y_m": 0.60},
        ])
        self.assertEqual(result["state_id"], "K8_V2_OPPONENT_HOUSE_THREAT_94")
        self.assertEqual(result["recommendation_status"], "SEARCH_REQUIRED_NO_CROSS_FOLD_GOAL_OUTCOME_CONSENSUS")
        self.assertIsNone(result["primary_goal"])


if __name__ == "__main__":
    unittest.main()
