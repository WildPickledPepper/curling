import unittest

from training_data.nwnht_curling.causal_state_machine.build_tactical_goal_library_v2 import build


def template(panel_key, occupancy, x):
    return {
        "panel_key": panel_key, "K": 4, "source_state": "K4_CROWDED", "source_state_status": "DATA_SUPPORTED_STATE",
        "observed_template_kind": "ACTIVE_STONE_PLACEMENT", "precision": "ROLE_AND_REGION",
        "observed_delta": {"opponent_removed_count": 0, "opponent_house_removed_count": 0},
        "stone_constraints_when_unambiguous": [], "dynamic_house_removal_binding_request": None,
        "after_own_occupancy": occupancy,
        "active_final_point": {"x_m": x, "y_m": 0.2, "zone": "button"},
        "post_own_topology": "POST", "after_opponent_reply_state": "K5_REPLY",
    }


class TacticalGoalLibraryV2Tests(unittest.TestCase):
    def test_parent_support_is_before_exact_occupancy_and_fine_grid_gate(self):
        first = template("1:1", {"first": {"button": 1}, "opponent": {}}, 0.0)
        second = template("1:2", {"first": {"button": 2}, "opponent": {}}, 0.21)
        parents, assignments, manifest = build([first, second], min_parent_action_support=2)
        self.assertEqual(manifest["parent_action_count"], 1)
        self.assertEqual(parents[0]["support"], 2)
        self.assertEqual(parents[0]["tactical_target_zone"], "BUTTON")
        self.assertEqual(parents[0]["fine_goal_count_all"], 2)
        self.assertEqual(len(assignments), 2)
        self.assertTrue(all(row["fine_goal_retained"] for row in assignments))

    def test_unexpressible_or_low_support_parent_is_not_admitted(self):
        item = template("1:1", {"first": {}, "opponent": {}}, 0.0)
        item["precision"] = "ABSTAIN"
        parents, assignments, _ = build([item], min_parent_action_support=1)
        self.assertEqual(parents, [])
        self.assertEqual(assignments, [])


if __name__ == "__main__":
    unittest.main()
