import unittest

from training_data.nwnht_curling.causal_state_machine.derive_action_effects import action_effect


def stone(owner, x, y):
    return {"owner": owner, "colour": "red" if owner == "first" else "yellow", "x_m": x, "y_m": y}


class ActionEffectTests(unittest.TestCase):
    def test_taking_scoring_control_has_priority_over_house_add(self):
        result = action_effect([stone("opponent", 0.0, 0.1)], [stone("first", 0.0, 0.05)])
        self.assertEqual(result["primary_effect"], "GAIN_OWN_SCORING_CONTROL")
        self.assertIn("OPPONENT_HOUSE_LAYER_REDUCED", result["effect_tags"])

    def test_guard_add_is_effect_not_called_shot_name(self):
        result = action_effect([], [stone("first", 0.7, 3.0)])
        self.assertEqual(result["primary_effect"], "ADD_PRESSURE_GUARD")

    def test_unchanged_empty_board_is_not_invented_as_a_tactic(self):
        result = action_effect([], [])
        self.assertEqual(result["primary_effect"], "NO_CLASSIFIABLE_MACRO_EFFECT")

    def test_losing_only_our_own_stone_is_not_called_a_clear_or_trade(self):
        result = action_effect(
            [stone("first", 0.0, 0.1), stone("opponent", 0.5, 3.0)],
            [stone("opponent", 0.5, 3.0)],
        )
        self.assertEqual(result["primary_effect"], "REDUCE_STONE_COUNT_WITHOUT_CONTROL")

    def test_near_tie_does_not_invent_scoring_control(self):
        result = action_effect(
            [stone("opponent", 0.0, 0.5)],
            [stone("opponent", 0.0, 0.5), stone("first", 0.0, 0.496)],
        )
        self.assertIsNone(result["after"]["scoring_owner"])
        self.assertNotIn("FIRST_TAKES_SCORING_CONTROL", result["effect_tags"])

    def test_scoring_count_only_includes_stones_closer_than_opponent(self):
        result = action_effect(
            [],
            [stone("first", 0.0, 0.1), stone("first", 0.0, 1.0), stone("opponent", 0.0, 0.5)],
        )
        self.assertEqual(result["after"]["scoring_owner"], "first")
        self.assertEqual(result["after"]["scoring_count"], 1)


if __name__ == "__main__":
    unittest.main()
