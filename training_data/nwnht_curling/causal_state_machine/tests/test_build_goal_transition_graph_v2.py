import unittest

from training_data.nwnht_curling.causal_state_machine.build_goal_library_v2 import _goal_id, _signature
from training_data.nwnht_curling.causal_state_machine.build_goal_transition_graph_v2 import build


def template(panel_key):
    return {
        "panel_key": panel_key,
        "source_state": "K5_TEST",
        "observed_template_kind": "ACTIVE_STONE_PLACEMENT",
        "precision": "ROLE_AND_REGION",
        "observed_delta": {"opponent_removed_count": 0, "opponent_house_removed_count": 0},
        "stone_constraints_when_unambiguous": [],
        "dynamic_house_removal_binding_request": None,
        "after_own_occupancy": {"first": {"button": 1}, "opponent": {}},
        "active_final_point": {"x_m": 0.0, "y_m": 0.1},
        "post_own_topology": "K5_POST_OWN[button]",
        "after_opponent_reply_state": "K6_TEST",
    }


class GoalTransitionGraphV2Tests(unittest.TestCase):
    def test_candidate_goal_is_joined_with_reply_and_terminal_result(self):
        templates = [template("1:1"), template("1:2")]
        goal_id = _goal_id(_signature(templates[0]))
        goals = [{"goal_id": goal_id, "runtime_goal_candidate": True, "support": 2}]
        rows = [
            {"end_id": 1, "own_global_shot_number": 1, "terminal_end_label": {"first_end_margin": 2}},
            {"end_id": 1, "own_global_shot_number": 2, "terminal_end_label": {"first_end_margin": -1}},
        ]
        edges, manifest = build(rows, templates, goals)
        self.assertEqual(manifest["state_goal_edge_count"], 1)
        edge = edges[0]
        self.assertEqual(edge["support"], 2)
        self.assertEqual(edge["observed_mean_first_end_margin"], 0.5)
        self.assertEqual(edge["observed_first_scores_rate"], 0.5)
        self.assertEqual(edge["after_opponent_reply_state_distribution"][0]["value"], "K6_TEST")
        self.assertEqual(edge["evidence_status"], "OBSERVATIONAL_EDGE_ONLY")

    def test_goal_support_mismatch_is_rejected(self):
        item = template("1:1")
        goals = [{"goal_id": _goal_id(_signature(item)), "runtime_goal_candidate": True, "support": 2}]
        rows = [{"end_id": 1, "own_global_shot_number": 1, "terminal_end_label": {"first_end_margin": 0}}]
        with self.assertRaises(ValueError):
            build(rows, [item], goals)


if __name__ == "__main__":
    unittest.main()
