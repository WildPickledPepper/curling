import unittest

from planning_proxy.competition_rules import HOUSE_X, HOUSE_Y
from planning_proxy.first_player_macro_state import classify_first_player_macro_state


class FirstPlayerMacroStateTests(unittest.TestCase):
    def test_empty_at_local_button_frame(self):
        state = classify_first_player_macro_state(1, [])
        self.assertEqual(state.state_id, "FIRST_K1_EMPTY")

    def test_local_coordinates_are_translated_before_house_test(self):
        state = classify_first_player_macro_state(2, [{"index": 0, "owner": "self", "x": HOUSE_X, "y": HOUSE_Y}])
        self.assertEqual(state.raw_macro_state, "OWN_HOUSE_CONTROL")
        self.assertEqual(state.features["first_in_house"], 1.0)

    def test_opponent_centre_shell_requires_both_guard_and_house_stone(self):
        board = [
            {"index": 0, "owner": "opponent", "x": HOUSE_X, "y": HOUSE_Y + 3.0},
            {"index": 1, "owner": "opponent", "x": HOUSE_X + 0.2, "y": HOUSE_Y + 0.2},
        ]
        state = classify_first_player_macro_state(4, board)
        self.assertEqual(state.raw_macro_state, "OPPONENT_CENTRE_SHELL")
        self.assertTrue(state.physx_detail_required)

    def test_low_support_geometry_routes_to_fallback_at_k3(self):
        state = classify_first_player_macro_state(3, [])
        self.assertEqual(state.raw_macro_state, "EMPTY")
        self.assertEqual(state.macro_state, "LOW_SUPPORT_SEARCH_REQUIRED")


if __name__ == "__main__":
    unittest.main()
