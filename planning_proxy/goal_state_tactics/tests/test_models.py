import unittest

from planning_proxy.goal_state_tactics.models import (
    CircleRegion,
    GoalState,
    OccupancyConstraint,
    StoneConstraint,
    StoneSelector,
)


class GoalStateModelTests(unittest.TestCase):
    def test_goal_state_serializes_anonymous_selector_and_region_constraints(self):
        house = CircleRegion("house", 2.375, 4.88, 1.83)
        right_front = CircleRegion("right_front", 2.80, 5.18, 0.25)
        target = StoneSelector("opponent_house_1", "opponent", "house", "closest_to_button")
        active = StoneSelector("active", "self", "active_delivery", "closest_to_button")
        goal = GoalState(
            transition_id="double_takeout_to_open_house",
            priority=1,
            source_state="K6_CORE[test]",
            expected_own_after_state="K6_CORE[open_house]",
            expected_after_reply_state="K7_CORE[reply_unknown]",
            stone_constraints=(
                StoneConstraint(target, "OUT_OF_PLAY"),
                StoneConstraint(active, "IN_REGION", right_front, required=False),
            ),
            occupancy_constraints=(OccupancyConstraint("opponent", house, min_count=0, max_count=0),),
            forbidden_outcomes=("free_guard_zone_violation",),
            fallback_transition_ids=("single_takeout",),
            require_last_reply_search=True,
        )

        payload = goal.to_json()
        self.assertEqual(payload["schema"], "goal_state_tactics_v0")
        self.assertEqual(payload["stone_constraints"][0]["selector"]["selector_id"], "opponent_house_1")
        self.assertEqual(payload["occupancy_constraints"][0]["max_count"], 0)
        self.assertTrue(payload["require_last_reply_search"])
        self.assertEqual(payload["last_reply_policy"], "REQUIRE_SEARCH_RECORD")

    def test_in_region_requires_a_range(self):
        selector = StoneSelector("target", "opponent", "house", "closest_to_button")
        with self.assertRaisesRegex(ValueError, "final_region"):
            StoneConstraint(selector, "IN_REGION")

    def test_goal_rejects_historical_fixed_slot_style_duplicate_selector(self):
        selector = StoneSelector("role", "opponent", "house", "closest_to_button")
        with self.assertRaisesRegex(ValueError, "重复"):
            GoalState(
                transition_id="bad",
                priority=1,
                source_state="S",
                expected_own_after_state="U",
                expected_after_reply_state=None,
                stone_constraints=(StoneConstraint(selector, "OUT_OF_PLAY"), StoneConstraint(selector, "SURVIVE")),
            )

    def test_non_final_goal_cannot_claim_no_counterplay(self):
        with self.assertRaisesRegex(ValueError, "未要求末壶搜索"):
            GoalState("bad_policy", 1, "S", "U", None, last_reply_policy="REQUIRE_NO_COUNTERPLAY")


if __name__ == "__main__":
    unittest.main()
