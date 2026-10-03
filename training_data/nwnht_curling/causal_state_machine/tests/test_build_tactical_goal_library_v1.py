import unittest

from training_data.nwnht_curling.causal_state_machine.build_goal_library_v2 import _goal_id, _signature
from training_data.nwnht_curling.causal_state_machine.build_tactical_goal_library_v1 import build, tactical_target_zone


def template(panel_key, x):
    return {
        "panel_key": panel_key, "K": 1, "source_state": "K1_EMPTY",
        "observed_template_kind": "ACTIVE_STONE_PLACEMENT", "precision": "ROLE_AND_REGION",
        "observed_delta": {"opponent_removed_count": 0, "opponent_house_removed_count": 0},
        "stone_constraints_when_unambiguous": [], "dynamic_house_removal_binding_request": None,
        "after_own_occupancy": {"first": {"centre_guard": 1}, "opponent": {}},
        "active_final_point": {"x_m": x, "y_m": 2.3, "zone": "centre_guard"},
        "post_own_topology": "POST_CENTRE_GUARD", "after_opponent_reply_state": "K2_REPLY",
    }


def fine_goal(item):
    return {
        "goal_id": _goal_id(_signature(item)), "runtime_goal_candidate": True,
        "observed_template_kind": item["observed_template_kind"], "precision": item["precision"],
        "active_final_region": {"shape": "circle", "centre_x_m": item["active_final_point"]["x_m"]},
        "stone_constraints_when_unambiguous": [], "dynamic_house_removal_binding_request": None,
        "after_own_occupancy": item["after_own_occupancy"],
    }


class TacticalGoalLibraryV1Tests(unittest.TestCase):
    def test_neighbouring_fine_cells_become_one_tactical_action_but_are_retained(self):
        left, right = template("1:1", 0.0), template("1:2", 0.22)
        parents, assignments, manifest = build([left, right], [fine_goal(left), fine_goal(right)])
        self.assertEqual(manifest["tactical_action_count"], 1)
        self.assertEqual(len(parents[0]["fine_goal_options"]), 2)
        self.assertEqual(parents[0]["tactical_target_zone"], "CENTRE_GUARD_NEAR")
        self.assertEqual({row["tactical_goal_id"] for row in assignments}, {parents[0]["goal_id"]})

    def test_guard_zone_uses_existing_near_far_boundary(self):
        self.assertEqual(tactical_target_zone({"x_m": 0.0, "y_m": 2.3}), "CENTRE_GUARD_NEAR")
        self.assertEqual(tactical_target_zone({"x_m": 0.0, "y_m": 4.5}), "CENTRE_GUARD_FAR")


if __name__ == "__main__":
    unittest.main()
