import unittest

from training_data.nwnht_curling.build_first_player_macro_state_graph import macro_type


class MacroStateTests(unittest.TestCase):
    def _features(self, **changes):
        base = {
            "first_visible": 0.0, "opponent_visible": 0.0,
            "first_in_house": 0.0, "opponent_in_house": 0.0,
            "first_guards": 0.0, "opponent_guards": 0.0,
            "first_centre_guards": 0.0, "opponent_centre_guards": 0.0,
            "first_currently_scoring": 0.0, "opponent_currently_scoring": 0.0,
        }
        base.update(changes)
        return base

    def test_empty_and_guard_exchange(self):
        self.assertEqual(macro_type(self._features()), "EMPTY")
        self.assertEqual(macro_type(self._features(first_visible=1, first_guards=1)), "GUARD_EXCHANGE")

    def test_crowded_has_priority_over_house_control(self):
        state = macro_type(self._features(first_visible=3, opponent_visible=3, first_in_house=2, opponent_in_house=1, first_currently_scoring=1))
        self.assertEqual(state, "CROWDED_HOUSE_SEARCH_REQUIRED")

    def test_shell_has_priority_over_generic_threat(self):
        state = macro_type(self._features(opponent_visible=2, opponent_in_house=1, opponent_centre_guards=1, opponent_currently_scoring=1))
        self.assertEqual(state, "OPPONENT_CENTRE_SHELL")


if __name__ == "__main__":
    unittest.main()
