import unittest

from training_data.nwnht_curling.causal_state_machine.build_causal_state_abstraction import (
    build,
    _opponent_reply_effect,
    state_key,
    topology_features,
)


def stone(owner, x, y):
    return {"owner": owner, "colour": "red" if owner == "first" else "yellow", "x_m": x, "y_m": y}


class CausalStateAbstractionTests(unittest.TestCase):
    def test_state_key_is_runtime_safe_and_includes_k(self):
        board = [stone("first", 0.0, 3.0)]
        key = state_key(3, board)
        self.assertTrue(key.startswith("K3_CORE["))
        self.assertNotIn("score", key.casefold())
        self.assertIn("F_centre_guard=1", key)

    def test_near_measure_is_not_declared_controlled(self):
        features = topology_features([stone("first", 0.0, 0.496), stone("opponent", 0.0, 0.5)])
        self.assertEqual(features["control"], "NONE_OR_UNCERTAIN")

    def test_opponent_reply_is_from_opponent_perspective(self):
        result = _opponent_reply_effect(
            [stone("first", 0.0, 0.1)],
            [stone("opponent", 0.0, 0.05)],
        )
        self.assertEqual(result, "OPPONENT_GAINS_SCORING_CONTROL")

    def test_core_state_tracks_its_fine_substates(self):
        row = {
            "end_id": 1, "own_global_shot_number": 1, "own_throw_number": 1, "match_id": 7,
            "s_before_own": [],
            "u_after_own": [stone("first", 0.0, 3.0)],
            "s_after_opponent_reply": [stone("first", 0.0, 3.0), stone("opponent", 0.7, 3.0)],
            "observed_own_board_effect": {"primary_effect": "ADD_PRESSURE_GUARD"},
            "terminal_end_label": {"first_end_margin": 0},
        }
        result = build([row])
        state = result["states"][0]
        self.assertEqual(state["fine_substate_count"], 1)
        self.assertEqual(state["fine_sample_count"], 1)


if __name__ == "__main__":
    unittest.main()
