import unittest

from training_data.nwnht_curling.build_first_player_success_subgraph import build, wilson_lower


class SuccessSubgraphTests(unittest.TestCase):
    def test_win_association_is_aggregated_without_redefining_the_state(self):
        rows = [
            {"state_id": "S", "observed_own_action": "A", "observed_opponent_reply": "R", "next_state_id": "T", "game_result": "FIRST_WINS", "end_result": "FIRST_SCORES"},
            {"state_id": "S", "observed_own_action": "A", "observed_opponent_reply": "R", "next_state_id": "T", "game_result": "FIRST_WINS", "end_result": "FIRST_SCORES"},
            {"state_id": "S", "observed_own_action": "B", "observed_opponent_reply": "R", "next_state_id": "U", "game_result": "FIRST_LOSES", "end_result": "OPPONENT_SCORES"},
        ]
        result = build(rows, min_edge_support=1)
        self.assertEqual(result["state_summary"][0]["state_id"], "S")
        edge = next(row for row in result["edge_summary"] if row["observed_own_action"] == "A")
        self.assertEqual(edge["total_count"], 2)
        self.assertEqual(edge["observed_win_rate"], 1.0)
        self.assertIn("warning", result)

    def test_wilson_lower_is_conservative(self):
        self.assertEqual(wilson_lower(0, 10), 0.0)
        self.assertLess(wilson_lower(2, 2), 1.0)
        self.assertGreater(wilson_lower(10, 10), wilson_lower(5, 10))


if __name__ == "__main__":
    unittest.main()
