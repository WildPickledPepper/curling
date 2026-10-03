import unittest

from training_data.nwnht_curling.causal_state_machine.build_goal_library_v2 import (
    aggregate_templates,
    extract_v2_template,
)


def stone(owner, x, y):
    return {"owner": owner, "x_m": x, "y_m": y}


PARTITION = {
    "states": [{
        "state_id": "K8_OPP_THREAT", "K": 8, "macro_state": "OPPONENT_HOUSE_THREAT",
        "rule": [], "eligible_for_next_goal_stage": True,
    }]
}

PLACEMENT_PARTITION = {
    "states": [{
        "state_id": "K8_GUARD_EXCHANGE", "K": 8, "macro_state": "GUARD_EXCHANGE",
        "rule": [], "eligible_for_next_goal_stage": True,
    }]
}


def source_row(key):
    return {
        "match_id": 1, "end_id": 10, "own_global_shot_number": key, "own_throw_number": 8,
        "s_before_own": [stone("opponent", -0.2, 0.1), stone("opponent", 0.2, 0.1)],
        "u_after_own": [],
        "s_after_opponent_reply": [],
        "terminal_end_label": {"first_end_margin": 0},
    }


class GoalLibraryV2Tests(unittest.TestCase):
    def test_unambiguous_all_opponent_removal_becomes_dynamic_binding(self):
        template = extract_v2_template(source_row(1), PARTITION)
        self.assertEqual(template["source_state"], "K8_OPP_THREAT")
        self.assertEqual(template["precision"], "ROLE_AND_REGION")
        self.assertEqual(template["dynamic_house_removal_binding_request"]["choose_count"], 2)
        self.assertEqual(template["after_opponent_reply_state"], "END")

    def test_supported_double_removal_family_is_candidate_without_winning_claim(self):
        templates = [extract_v2_template(source_row(index), PARTITION) for index in range(30)]
        goals, manifest = aggregate_templates(templates)
        self.assertEqual(manifest["runtime_goal_candidate_count"], 1)
        goal = goals[0]
        self.assertTrue(goal["runtime_goal_candidate"])
        self.assertEqual(goal["dynamic_house_removal_binding_request"]["choose_count"], 2)
        self.assertEqual(goal["evidence_status"], "HISTORICAL_GOAL_TEMPLATE")
        self.assertIn("not a causal", goal["warning"])

    def test_active_endpoint_is_mirrored_into_source_canonical_frame(self):
        row = {
            "match_id": 1, "end_id": 11, "own_global_shot_number": 1, "own_throw_number": 8,
            "s_before_own": [stone("first", 0.8, 3.0)],
            "u_after_own": [stone("first", 0.8, 3.0), stone("first", 1.0, 0.2)],
            "s_after_opponent_reply": [], "terminal_end_label": {"first_end_margin": 0},
        }
        template = extract_v2_template(row, PLACEMENT_PARTITION)
        self.assertLess(template["active_final_point"]["x_m"], 0.0)
        self.assertEqual(template["active_final_point"]["zone"], "house_front_left")


if __name__ == "__main__":
    unittest.main()
