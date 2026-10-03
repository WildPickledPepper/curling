import unittest

from planning_proxy.competition_rules import HOUSE_X, HOUSE_Y
from planning_proxy.tactical_library_strategy.v2_circle_goal_adapter import compile_circle_goal_requests


class FakePlanner:
    def __init__(self, plan):
        self.plan = plan

    def recommend(self, _k, _board):
        return self.plan


class V2CircleGoalAdapterTests(unittest.TestCase):
    def test_narrow_goal_is_mapped_to_local_button_coordinates(self):
        plan = {
            "state_id": "K1_EMPTY", "recommendation_status": "EMPIRICAL_ACTION_CONSENSUS",
            "primary_action": {
                "tactical_goal_id": "A", "precision_level": "NARROW_CROSS_FOLD_GOAL", "observed_template_kind": "ACTIVE_STONE_PLACEMENT",
                "fine_goal_options": [{"goal_id": "G", "active_final_region": {"shape": "circle", "centre_x_m": 0.1, "centre_y_m": 0.2, "radius_m": 0.17}}],
                "expected_next_state_distribution": [],
            }, "fallback_actions": [],
        }
        _, goals = compile_circle_goal_requests(FakePlanner(plan), 1, [])
        self.assertEqual(len(goals), 1)
        self.assertAlmostEqual(goals[0].local_centre_x, HOUSE_X + 0.1)
        self.assertAlmostEqual(goals[0].local_centre_y, HOUSE_Y + 0.2)

    def test_semantic_guard_action_is_explicit_inner_approximation(self):
        plan = {
            "state_id": "K2_EMPTY", "recommendation_status": "EMPIRICAL_ACTION_CONSENSUS",
            "primary_action": {
                "tactical_goal_id": "A", "precision_level": "SEMANTIC_REGION_GOAL", "observed_template_kind": "ACTIVE_STONE_PLACEMENT",
                "target_region": {"kind": "GUARD_LANE", "abs_x_max_m": 0.38, "y_min_exclusive_m": 1.8288, "y_max_inclusive_m": 4.14},
                "expected_next_state_distribution": [],
            }, "fallback_actions": [],
        }
        _, goals = compile_circle_goal_requests(FakePlanner(plan), 2, [])
        self.assertTrue(goals)
        self.assertTrue(all(goal.coverage_status == "INNER_APPROXIMATION_ONLY" for goal in goals))


if __name__ == "__main__":
    unittest.main()
