import unittest

from training_data.nwnht_curling.causal_state_machine.build_universal_semantic_goal_mdp_v1 import build, physically_admissible_own_shot_observation


class UniversalSemanticGoalMdpTests(unittest.TestCase):
    def test_every_state_gets_same_k_goal_and_successor_distribution(self):
        state_k = {"K7_A": 7, "K8_B": 8}
        goals = {
            "G7": {"goal_id": "G7", "K": 7, "source_state": "K7_A"},
            "G8": {"goal_id": "G8", "K": 8, "source_state": "K8_B"},
        }
        rows = [
            {"source_state": "K7_A", "goal_id": "G7", "K": 7, "match_id": fold, "fold": fold, "next_state": "K8_B", "margin": 1.0}
            for fold in range(5)
        ] + [
            {"source_state": "K8_B", "goal_id": "G8", "K": 8, "match_id": fold + 10, "fold": fold, "next_state": "END", "margin": 1.0}
            for fold in range(5)
        ]
        result = build(goals, rows, state_k)
        plans = {row["state_id"]: row for row in result["state_plans"]}
        self.assertEqual(set(plans), set(state_k))
        self.assertEqual(plans["K7_A"]["primary_goal"]["goal_state"]["K"], 7)
        self.assertEqual(plans["K7_A"]["primary_goal"]["after_opponent_reply_state_distribution"][0]["value"], "K8_B")
        self.assertEqual(plans["K8_B"]["primary_goal"]["after_opponent_reply_state_distribution"][0]["value"], "END")

    def test_rejects_missing_full_data_goal(self):
        with self.assertRaises(ValueError):
            build({}, [], {"K1_A": 1})

    def test_rejects_opponent_stone_creation_as_physically_impossible(self):
        self.assertFalse(physically_admissible_own_shot_observation({"observed_delta": {"opponent_removed_count": -1}}))
        self.assertTrue(physically_admissible_own_shot_observation({"observed_delta": {"opponent_removed_count": 0}}))


if __name__ == "__main__":
    unittest.main()
