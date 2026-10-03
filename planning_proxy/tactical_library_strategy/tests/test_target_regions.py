import unittest

from planning_proxy.competition_rules import HOUSE_X, HOUSE_Y
from planning_proxy.tactical_library_strategy.target_regions import candidate_target_regions


def stone(index, owner, x, y):
    return {"index": index, "owner": owner, "x": x, "y": y}


class TacticalTargetRegionTests(unittest.TestCase):
    def test_empty_opening_yields_house_and_front_pressure_stop_regions(self):
        result = candidate_target_regions([], 1)
        self.assertEqual(result.tactical_plan.primary_intent, "BUILD_OWN_HOUSE_LAYER")
        self.assertTrue(any(region.tactical_role == "己方营内得分层" for region in result.regions))
        self.assertTrue(any(region.tactical_role == "前场压力壶" for region in result.regions))
        self.assertTrue(all(region.target_kind == "STOP_REGION" for region in result.regions))

    def test_house_threat_yields_contact_regions_for_closest_enemy(self):
        result = candidate_target_regions([
            stone(2, "opponent", HOUSE_X + 0.10, HOUSE_Y + 0.05),
        ], 4)
        contacts = [region for region in result.regions if region.target_kind == "STONE_CONTACT"]
        self.assertEqual(result.tactical_plan.primary_intent, "CHANGE_OPPONENT_SCORING_STONE")
        self.assertTrue(contacts)
        self.assertTrue(all(region.target_stone_index == 2 for region in contacts))

    def test_protected_centre_guard_produces_no_contact_target(self):
        result = candidate_target_regions([
            stone(3, "opponent", HOUSE_X, HOUSE_Y + 2.8),
        ], 2)
        self.assertEqual(result.tactical_plan.primary_intent, "DRAW_AROUND_PROTECTED_CENTRE_GUARD")
        self.assertFalse(any(region.target_kind == "STONE_CONTACT" for region in result.regions))
        self.assertTrue(result.regions)

    def test_occupied_stop_slot_is_not_offered_as_a_draw_region(self):
        result = candidate_target_regions([
            stone(1, "self", HOUSE_X - 0.42, HOUSE_Y + 0.30),
        ], 2)
        self.assertFalse(any(region.region_id == "left_front_house_layer" for region in result.regions))


if __name__ == "__main__":
    unittest.main()
