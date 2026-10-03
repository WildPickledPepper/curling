import unittest

from training_data.nwnht_curling.causal_state_machine.backward_value_iteration_v2 import build


def observation(match_id, k, state, goal, next_state, margin):
    return {
        "match_id": match_id, "fold": 0, "K": k, "source_state": state,
        "goal_id": goal, "next_state": next_state,
        "post_own_topology": f"POST_{goal}", "margin": margin,
    }


def goal(goal_id):
    return {
        "goal_id": goal_id, "observed_template_kind": "ACTIVE_STONE_PLACEMENT",
        "precision": "ROLE_AND_REGION", "active_final_region": {"shape": "circle"},
        "stone_constraints_when_unambiguous": [], "dynamic_house_removal_binding_request": None,
        "after_own_occupancy": {"first": {}, "opponent": {}},
    }


class BackwardValueIterationV2Tests(unittest.TestCase):
    def test_backward_pass_prefers_goal_with_better_supported_future(self):
        rows = []
        for match_id in range(1, 26):
            rows += [
                observation(match_id, 1, "K1_A", "g_good", "K2_GOOD", 0),
                observation(match_id, 1, "K1_A", "g_bad", "K2_BAD", 0),
                observation(match_id, 2, "K2_GOOD", "g_finish_good", "END", 2),
                observation(match_id, 2, "K2_BAD", "g_finish_bad", "END", -1),
            ]
        result = build(
            rows, {name: goal(name) for name in {row["goal_id"] for row in rows}},
            {"K1_A": 1, "K2_GOOD": 2, "K2_BAD": 2},
            holdout_fold=99, min_development_support=20, min_holdout_support=0,
        )
        plan = next(item for item in result["state_plans"] if item["state_id"] == "K1_A")
        self.assertEqual(plan["primary_goal"]["goal_id"], "g_good")
        values = {item["goal_id"]: item for item in result["candidate_values"]}
        self.assertGreater(values["g_good"]["backed_up_value_mean"], values["g_bad"]["backed_up_value_mean"])

    def test_low_support_goal_is_not_recommended(self):
        rows = [observation(1, 8, "K8_A", "g_one", "END", 2)]
        result = build(
            rows, {"g_one": goal("g_one")}, {"K8_A": 8},
            holdout_fold=99, min_development_support=2, min_holdout_support=0,
        )
        plan = result["state_plans"][0]
        self.assertEqual(plan["recommendation_status"], "SEARCH_REQUIRED_NO_SUPPORTED_GOAL")

    def test_bootstrap_lcb_is_exposed(self):
        rows = [observation(match_id, 8, "K8_A", "g_one", "END", 1) for match_id in range(1, 25)]
        result = build(
            rows, {"g_one": goal("g_one")}, {"K8_A": 8},
            holdout_fold=99, min_development_support=20, min_holdout_support=0,
            bootstrap_replicates=8,
        )
        item = result["candidate_values"][0]
        self.assertEqual(item["bootstrap_replicate_count"], 8)
        self.assertEqual(item["backed_up_value_lcb"], item["backed_up_value_mean"])


if __name__ == "__main__":
    unittest.main()
