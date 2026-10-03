import unittest

from training_data.nwnht_curling.causal_state_machine.aggregate_goal_state_edges import build


def template(*, point, reply="K2_CORE[next]", own_after="K1_CORE[after]", support_key="p"):
    return {
        "panel_key": support_key,
        "source_state": "K1_CORE[source]",
        "expected_own_after_state": own_after,
        "expected_after_reply_state": reply,
        "observed_template_kind": "ACTIVE_STONE_PLACEMENT",
        "precision": "ROLE_AND_REGION",
        "observed_delta": {"opponent_removed_count": 0},
        "stone_constraints_when_unambiguous": [],
        "after_own_occupancy": {"first": {"button": 1}, "opponent": {}},
        "active_final_point": point,
    }


class GoalStateEdgeAggregationTests(unittest.TestCase):
    def test_nearby_points_merge_and_reply_stays_a_distribution(self):
        rows = [
            template(point={"x_m": 0.03, "y_m": 0.02}, reply="K2_CORE[a]", support_key="1"),
            template(point={"x_m": 0.06, "y_m": 0.03}, reply="K2_CORE[b]", support_key="2"),
        ]
        edges, manifest = build(rows)
        self.assertEqual(manifest["edge_count"], 1)
        edge = edges[0]
        self.assertEqual(edge["support"], 2)
        self.assertEqual(len(edge["expected_after_reply_states"]), 2)
        self.assertAlmostEqual(edge["active_final_region"]["centre_x_m"], 0.045)
        self.assertFalse(edge["runtime_candidate"])
        self.assertIn("support<30", edge["not_runtime_candidate_reasons"])

    def test_ambiguous_template_cannot_pass_runtime_data_gate(self):
        row = template(point=None)
        row["precision"] = "REGION_OCCUPANCY_ONLY"
        edges, _ = build([row] * 30)
        self.assertFalse(edges[0]["runtime_candidate"])
        self.assertIn("no_role_and_region_precision", edges[0]["not_runtime_candidate_reasons"])


if __name__ == "__main__":
    unittest.main()
