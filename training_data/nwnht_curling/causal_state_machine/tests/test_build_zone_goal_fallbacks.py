import unittest

from training_data.nwnht_curling.causal_state_machine.build_zone_goal_fallbacks import build, compact_zone_state


SOURCE = "K5_CORE[control=FIRST;F_house=1;O_house=0;F_centre_guard=1;O_centre_guard=0;F_wing_guard=0;O_wing_guard=0]"


def row(index):
    return {
        "panel_key": str(index), "source_state": SOURCE,
        "observed_template_kind": "ACTIVE_STONE_PLACEMENT",
        "active_final_point": {"x_m": 0.05, "y_m": 2.45, "zone": "centre_guard"},
        "expected_own_after_state": "K5_CORE[next]", "expected_after_reply_state": "K6_CORE[reply]",
    }


class ZoneGoalFallbackTests(unittest.TestCase):
    def test_compact_state_uses_phase_and_board_topology_only(self):
        result = compact_zone_state(SOURCE)
        self.assertEqual(result, "K5_6_ZONE[control=FIRST;F_house=1;O_house=0]")
        self.assertNotIn("guard", result.casefold())

    def test_supported_points_become_a_physx_search_required_circle(self):
        edges, manifest = build([row(index) for index in range(30)])
        self.assertEqual(manifest["edge_count"], 1)
        edge = edges[0]
        self.assertTrue(edge["physx_search_required"])
        self.assertEqual(edge["support"], 30)
        self.assertGreaterEqual(edge["active_final_region"]["radius_m"], .30)


if __name__ == "__main__":
    unittest.main()
