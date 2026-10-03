import unittest

from training_data.nwnht_curling.causal_state_machine.compile_conditional_fine_goals_v1 import build


class ConditionalFineGoalTests(unittest.TestCase):
    def test_stable_fine_endpoint_becomes_consensus(self):
        signature = ("ROLE_AND_REGION", (0, 1), "[]", "null", "{\"first\":{\"button\":1}}")
        records = [
            {
                "K": 8, "macro": "M", "template_id": "T", "source_state": "K8_A", "fold": fold,
                "fine_signature": signature, "panel_key": f"{fold}:1",
                "active_final_point": {"x_m": 0.01, "y_m": 0.2},
                "features": {"shape": "same"},
            }
            for fold in range(5) for _ in range(2)
        ]
        registry = {"state_plans": [{
            "state_id": "K8_A", "K": 8,
            "recommendation_status": "CONDITIONAL_SEMANTIC_GOAL_CONSENSUS_PENDING_FINE_COMPILATION",
            "primary_goal": {"template_id": "T", "goal_template": {"K": 8}},
        }]}
        result = build(records, registry)
        plan = result["state_plans"][0]
        self.assertEqual(plan["recommendation_status"], "CONDITIONAL_FINE_GOAL_CONSENSUS")
        self.assertEqual(plan["primary_fold_count"], 5)
        self.assertEqual(plan["primary_goal"]["active_final_region"]["point_count"], 8)

    def test_rejects_semantic_only_record_without_endpoint_or_binding(self):
        signature = ("ABSTAIN", None, "[]", "null", "{}")
        records = [
            {"K": 8, "macro": "M", "template_id": "T", "source_state": "K8_A", "fold": fold,
             "fine_signature": signature, "panel_key": f"{fold}:1", "active_final_point": None,
             "features": {"shape": "same"}}
            for fold in range(5) for _ in range(2)
        ]
        registry = {"state_plans": [{
            "state_id": "K8_A", "K": 8,
            "recommendation_status": "CONDITIONAL_SEMANTIC_GOAL_CONSENSUS_PENDING_FINE_COMPILATION",
            "primary_goal": {"template_id": "T", "goal_template": {"K": 8}},
        }]}
        self.assertEqual(build(records, registry)["state_plans"][0]["recommendation_status"], "NO_FINE_CONSENSUS")


if __name__ == "__main__":
    unittest.main()
