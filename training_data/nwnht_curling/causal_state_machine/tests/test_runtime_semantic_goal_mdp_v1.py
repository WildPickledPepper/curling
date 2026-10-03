import unittest

from training_data.nwnht_curling.causal_state_machine.runtime_semantic_goal_mdp_v1 import load_default


class RuntimeSemanticGoalMdpTests(unittest.TestCase):
    def test_k8_house_threat_has_same_k_semantic_goal_and_end_transition(self):
        planner = load_default()
        result = planner.recommend(8, [
            {"owner": "opponent", "x_m": 0.15, "y_m": 0.20},
            {"owner": "opponent", "x_m": 0.55, "y_m": 0.60},
        ])
        self.assertEqual(result["state_id"], "K8_V2_OPPONENT_HOUSE_THREAT_94")
        self.assertEqual(result["recommendation_status"], "SEMANTIC_GOAL_AVAILABLE")
        goal = result["primary_goal"]
        self.assertEqual(goal["goal_state"]["K"], 8)
        self.assertEqual(goal["after_opponent_reply_state_distribution"][0]["value"], "END")

    def test_empty_k1_goal_predicts_only_k2_successors(self):
        result = load_default().recommend(1, [])
        self.assertEqual(result["state_id"], "K1_V2_EMPTY_1")
        goal = result["primary_goal"]
        self.assertEqual(goal["goal_state"]["K"], 1)
        self.assertTrue(all(item["value"].startswith("K2_") for item in goal["after_opponent_reply_state_distribution"]))


if __name__ == "__main__":
    unittest.main()
