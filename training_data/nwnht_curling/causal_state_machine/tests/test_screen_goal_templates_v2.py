import unittest

from training_data.nwnht_curling.causal_state_machine.build_goal_library_v2 import _goal_id, _signature
from training_data.nwnht_curling.causal_state_machine.screen_goal_templates_v2 import build


def template(panel_key):
    return {
        "panel_key": panel_key, "source_state": "K5_TEST",
        "observed_template_kind": "ACTIVE_STONE_PLACEMENT", "precision": "ROLE_AND_REGION",
        "observed_delta": {"opponent_removed_count": 0, "opponent_house_removed_count": 0},
        "stone_constraints_when_unambiguous": [], "dynamic_house_removal_binding_request": None,
        "after_own_occupancy": {"first": {"button": 1}, "opponent": {}},
        "active_final_point": {"x_m": 0.0, "y_m": 0.1},
        "post_own_topology": "K5_POST_OWN[button]", "after_opponent_reply_state": "K6_TEST",
    }


class GoalTemplateScreenTests(unittest.TestCase):
    def test_descriptive_screen_never_promotes_endpoint_to_causal_action(self):
        templates = [template(f"1:{index}") for index in range(70)]
        goal = {"goal_id": _goal_id(_signature(templates[0])), "runtime_goal_candidate": True, "source_state": "K5_TEST"}
        transitions = [
            {"end_id": 1, "own_global_shot_number": index, "match_id": index,
             "terminal_end_label": {"first_end_margin": 1 if index % 2 else -1}}
            for index in range(70)
        ]
        rows, manifest = build(transitions, templates, [goal], holdout_fold=0)
        self.assertEqual(manifest["causal_deployable_goal_count"], 0)
        self.assertEqual(rows[0]["causal_deployment_status"], "REJECTED_POST_TREATMENT_ENDPOINT")
        self.assertIn("post-shot", rows[0]["causal_rejection_reason"])


if __name__ == "__main__":
    unittest.main()
