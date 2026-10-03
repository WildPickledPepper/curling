import unittest

from training_data.nwnht_curling.causal_state_machine.extract_anonymous_goal_templates import (
    extract_template,
    infer_active_final_point,
)


def stone(owner, x, y):
    return {"owner": owner, "colour": "red" if owner == "first" else "yellow", "x_m": x, "y_m": y}


def row(before, after_own, after_reply, *, k=2):
    return {
        "end_id": 1,
        "match_id": 3,
        "own_throw_number": k,
        "own_global_shot_number": 2 * k - 1,
        "s_before_own": before,
        "u_after_own": after_own,
        "s_after_opponent_reply": after_reply,
    }


class AnonymousGoalTemplateTests(unittest.TestCase):
    def test_clean_draw_recovers_active_final_point(self):
        before = [stone("opponent", 0.0, 3.0)]
        after = [stone("opponent", 0.01, 3.01), stone("first", 0.35, 0.20)]
        active = infer_active_final_point(before, after)
        self.assertEqual(active["zone"], "button")
        self.assertAlmostEqual(active["x_m"], 0.35)

    def test_full_double_removal_emits_bindable_anonymous_roles(self):
        before = [stone("opponent", -0.2, 0.2), stone("opponent", 0.3, 0.4)]
        after = []
        result = extract_template(row(before, after, after, k=6))
        self.assertEqual(result["observed_template_kind"], "DOUBLE_OR_MULTI_OPPONENT_REMOVAL")
        self.assertEqual(result["precision"], "ROLE_AND_REGION")
        self.assertEqual(len(result["stone_constraints_when_unambiguous"]), 2)
        self.assertEqual(result["stone_constraints_when_unambiguous"][0]["required_disposition"], "OUT_OF_PLAY")
        self.assertEqual(result["observed_delta"]["opponent_house_removed_count"], 2)

    def test_ambiguous_same_colour_collision_only_keeps_occupancy(self):
        before = [stone("first", -0.03, 0.0), stone("opponent", 0.0, 3.0)]
        after = [stone("first", -0.50, 0.0), stone("first", 0.50, 0.0), stone("opponent", 0.0, 3.0)]
        result = extract_template(row(before, after, after))
        self.assertIsNone(result["active_final_point"])
        self.assertEqual(result["precision"], "REGION_OCCUPANCY_ONLY")

    def test_no_change_abstains(self):
        before = [stone("opponent", 0.0, 3.0)]
        result = extract_template(row(before, before, before))
        self.assertEqual(result["precision"], "ABSTAIN")
        self.assertIsNotNone(result["abstention_reason"])


if __name__ == "__main__":
    unittest.main()
