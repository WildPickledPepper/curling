import unittest

from training_data.nwnht_curling.build_first_player_candidate_policy import build


class CandidatePolicyTests(unittest.TestCase):
    def test_candidate_keeps_reply_branches_and_does_not_emit_shot_parameters(self):
        rows = []
        for _ in range(30):
            rows.append({"state_id": "S", "observed_own_action": "DRAW", "observed_opponent_reply": "FRONT", "next_state_id": "T", "game_result": "FIRST_WINS", "end_result": "FIRST_SCORES", "end_points": {"first": 1, "opponent": 0}})
        for _ in range(30):
            rows.append({"state_id": "S", "observed_own_action": "TAKEOUT", "observed_opponent_reply": "DRAW", "next_state_id": "U", "game_result": "FIRST_LOSES", "end_result": "OPPONENT_SCORES", "end_points": {"first": 0, "opponent": 1}})
        result = build(rows, {"S": {"physx_detail_required": False}}, min_action_support=20, max_actions=2)
        state = result["policy_states"][0]
        self.assertEqual(state["candidate_action_intents"][0]["observed_action_intent"], "DRAW")
        branch = state["candidate_action_intents"][0]["opponent_reply_branches"][0]
        self.assertEqual(branch["next_state_id"], "T")
        self.assertNotIn("v", state["candidate_action_intents"][0])


if __name__ == "__main__":
    unittest.main()
