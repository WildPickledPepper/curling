import unittest

from planning_proxy.competition_rules import HOUSE_X, HOUSE_Y
from planning_proxy.tactical_library_strategy import plan_first_player_from_tactical_library


def stone(index, owner, x, y):
    return {"index": index, "owner": owner, "x": x, "y": y}


class FirstPlayerTacticalLibraryTests(unittest.TestCase):
    def test_empty_opening_is_a_data_supported_build_layer_goal(self):
        plan = plan_first_player_from_tactical_library([], 1)
        self.assertEqual(plan.state_id, "FIRST_K1_EMPTY")
        self.assertEqual(plan.primary_intent, "BUILD_OWN_HOUSE_LAYER")
        self.assertEqual(plan.historical_candidate_intents, ("DRAW",))
        self.assertEqual(plan.desired_next_state, "FIRST_K2_OWN_HOUSE_CONTROL")

    def test_protected_centre_guard_is_not_sent_to_clear(self):
        plan = plan_first_player_from_tactical_library(
            [stone(1, "opponent", HOUSE_X, HOUSE_Y + 2.8)], 2,
        )
        self.assertEqual(plan.primary_intent, "DRAW_AROUND_PROTECTED_CENTRE_GUARD")
        self.assertIsNone(plan.target_opponent_index)
        self.assertIn("MUST_REMAIN_ON_CENTRE_LINE", plan.rule_constraint)

    def test_low_support_geometry_explicitly_refuses_a_learned_action(self):
        plan = plan_first_player_from_tactical_library([], 3)
        self.assertEqual(plan.policy_status, "LOW_SUPPORT_SEARCH_REQUIRED")
        self.assertEqual(plan.primary_intent, "SEARCH_REQUIRED")

    def test_guard_exchange_anti_evidence_blocks_default_clear(self):
        plan = plan_first_player_from_tactical_library(
            [stone(1, "opponent", HOUSE_X + 0.55, HOUSE_Y + 2.3)], 6,
        )
        self.assertEqual(plan.state_id, "FIRST_K6_GUARD_EXCHANGE")
        self.assertEqual(plan.policy_status, "ANTI_DEFAULT_CLEAR")
        self.assertEqual(plan.primary_intent, "PHYSX_COMPARE_WING_ROLL_RAISE")
        self.assertIn("CLEARING", plan.alternative_intents)

    def test_eighth_throw_requires_actual_reply_search(self):
        board = [
            stone(1, "self", HOUSE_X, HOUSE_Y),
            stone(2, "self", HOUSE_X - 0.2, HOUSE_Y + 0.25),
            stone(3, "self", HOUSE_X + 0.25, HOUSE_Y + 0.2),
            stone(4, "opponent", HOUSE_X + 0.6, HOUSE_Y - 0.2),
            stone(5, "opponent", HOUSE_X - 0.65, HOUSE_Y + 0.1),
        ]
        plan = plan_first_player_from_tactical_library(board, 8)
        self.assertTrue(plan.require_last_reply_search)
        self.assertEqual(plan.policy_status, "PHYSX_SEARCH_REQUIRED")


if __name__ == "__main__":
    unittest.main()
