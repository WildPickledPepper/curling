import unittest

from training_data.nwnht_curling.causal_state_machine.rank_tactical_goal_library_v1 import collect_observations


class RankTacticalGoalLibraryV1Tests(unittest.TestCase):
    def test_assignment_is_joined_to_terminal_label_without_context_features(self):
        transitions = [{
            "end_id": 4, "own_global_shot_number": 1, "match_id": 9,
            "terminal_end_label": {"first_end_margin": 2},
        }]
        assignments = [{
            "panel_key": "4:1", "K": 1, "source_state": "K1_EMPTY",
            "tactical_goal_id": "A_GUARD", "after_opponent_reply_state": "K2_REPLY",
            "post_own_topology": "POST_GUARD",
        }]
        rows = collect_observations(transitions, assignments)
        self.assertEqual(rows[0]["goal_id"], "A_GUARD")
        self.assertEqual(rows[0]["margin"], 2.0)
        self.assertNotIn("end_number", rows[0])


if __name__ == "__main__":
    unittest.main()
