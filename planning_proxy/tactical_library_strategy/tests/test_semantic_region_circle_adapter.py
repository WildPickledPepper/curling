import math
import unittest

from planning_proxy.tactical_library_strategy.semantic_region_circle_adapter import circle_subgoals


class SemanticRegionCircleAdapterTests(unittest.TestCase):
    def test_circle_region_is_preserved_exactly(self):
        goals = circle_subgoals({"kind": "CIRCLE", "centre_x_m": 0.0, "centre_y_m": 0.0, "max_radius_m": 0.6096})
        self.assertEqual(len(goals), 1)
        self.assertEqual(goals[0]["radius_m"], 0.6096)
        self.assertEqual(goals[0]["coverage_status"], "EXACT_SEMANTIC_REGION")

    def test_guard_tiles_stay_inside_lane(self):
        region = {"kind": "GUARD_LANE", "abs_x_max_m": 0.38, "y_min_exclusive_m": 1.8288, "y_max_inclusive_m": 4.14}
        goals = circle_subgoals(region, radius_m=0.17)
        self.assertTrue(goals)
        self.assertTrue(any(abs(goal["centre_x_m"]) < 1e-9 for goal in goals))
        for goal in goals:
            self.assertLessEqual(abs(goal["centre_x_m"]) + goal["radius_m"], 0.38)
            self.assertGreater(goal["centre_y_m"] - goal["radius_m"], 1.8288)
            self.assertLessEqual(goal["centre_y_m"] + goal["radius_m"], 4.14)

    def test_house_tiles_do_not_cross_sector_or_annulus(self):
        region = {"kind": "HOUSE_SECTOR", "min_radius_m": 0.6096, "max_radius_m": 1.8288, "x_relation": "<0", "y_relation": ">=0"}
        goals = circle_subgoals(region, radius_m=0.17)
        self.assertTrue(goals)
        for goal in goals:
            x, y, r = goal["centre_x_m"], goal["centre_y_m"], goal["radius_m"]
            self.assertLess(x + r, 0.0)
            self.assertGreaterEqual(y - r, 0.0)
            self.assertGreaterEqual(math.hypot(x, y) - r, 0.6096)
            self.assertLessEqual(math.hypot(x, y) + r, 1.8288)


if __name__ == "__main__":
    unittest.main()
