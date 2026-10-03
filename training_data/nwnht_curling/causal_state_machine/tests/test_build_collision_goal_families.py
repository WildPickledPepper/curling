import unittest

from training_data.nwnht_curling.causal_state_machine.build_collision_goal_families import (
    build,
    macro_collision_state,
)


SOURCE = "K6_CORE[control=OPPONENT;F_house=0;O_house=2P;F_centre_guard=0;O_centre_guard=0;F_wing_guard=0;O_wing_guard=0]"
AFTER = "K6_CORE[control=NONE_OR_UNCERTAIN;F_house=0;O_house=0;F_centre_guard=0;O_centre_guard=0;F_wing_guard=0;O_wing_guard=0]"


def row(key):
    return {
        "panel_key": key,
        "source_state": SOURCE,
        "expected_own_after_state": AFTER,
        "expected_after_reply_state": "K7_CORE[next]",
        "observed_template_kind": "DOUBLE_OR_MULTI_OPPONENT_REMOVAL",
        "precision": "ROLE_AND_REGION",
        "observed_delta": {"opponent_removed_count": 2, "opponent_house_removed_count": 2},
        "active_final_point": None,
        "after_own_occupancy": {"first": {}, "opponent": {}},
    }


class CollisionGoalFamilyTests(unittest.TestCase):
    def test_macro_state_is_runtime_safe(self):
        state = macro_collision_state(SOURCE)
        self.assertEqual(state, "K6_COLLISION[control=OPPONENT;F_house=0;O_house=2P;F_guards=N;O_guards=N]")
        self.assertNotIn("score", state.casefold())

    def test_supported_house_double_becomes_dynamic_pair_request(self):
        families, manifest = build([row(str(index)) for index in range(30)])
        self.assertEqual(manifest["runtime_candidate_for_physx_screen_count"], 1)
        family = families[0]
        self.assertTrue(family["runtime_candidate_for_physx_screen"])
        self.assertEqual(family["dynamic_binding_request"]["choose_count"], 2)
        self.assertEqual(family["observed_active_final_outcomes"][0]["value"], "UNRESOLVED_OR_OUT")

    def test_supported_single_removal_can_be_the_double_fallback(self):
        rows = [row(str(index)) for index in range(30)]
        for index in range(40):
            single = row(f"single-{index}")
            single["observed_template_kind"] = "SINGLE_OPPONENT_REMOVAL"
            single["observed_delta"] = {"opponent_removed_count": 1, "opponent_house_removed_count": 1}
            rows.append(single)
        families, manifest = build(rows)
        self.assertEqual(manifest["runtime_candidate_for_physx_screen_count"], 2)
        self.assertEqual({item["dynamic_binding_request"]["choose_count"] for item in families}, {1, 2})

    def test_non_house_removal_is_retained_but_not_bound_as_house_target(self):
        rows = [row(str(index)) for index in range(30)]
        for item in rows:
            item["source_state"] = "K6_CORE[control=NONE_OR_UNCERTAIN;F_house=0;O_house=0;F_centre_guard=0;O_centre_guard=0;F_wing_guard=0;O_wing_guard=2P]"
        families, manifest = build(rows)
        self.assertEqual(manifest["runtime_candidate_for_physx_screen_count"], 0)
        self.assertIsNone(families[0]["dynamic_binding_request"])
        self.assertIn("source_state_does_not_guarantee_required_opponent_house_targets", families[0]["not_runtime_candidate_reasons"])

    def test_total_removal_without_house_removal_is_excluded_from_house_families(self):
        rows = [row(str(index)) for index in range(30)]
        for item in rows:
            item["observed_delta"] = {"opponent_removed_count": 2, "opponent_house_removed_count": 0}
        families, manifest = build(rows)
        self.assertEqual(families, [])
        self.assertEqual(manifest["input_rows_with_opponent_house_removal"], 0)


if __name__ == "__main__":
    unittest.main()
