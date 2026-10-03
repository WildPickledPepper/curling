import unittest

from training_data.nwnht_curling.causal_state_machine.build_goal_evidence_registry_v1 import build


class GoalEvidenceRegistryTests(unittest.TestCase):
    def test_direct_goal_has_priority_over_conditional_template(self):
        direct = {"state_plans": [
            {"state_id": "K1_A", "K": 1, "recommendation_status": "EMPIRICAL_GOAL_OUTCOME_CONSENSUS", "primary_goal": {"goal_id": "exact"}},
            {"state_id": "K1_B", "K": 1, "recommendation_status": "SEARCH_REQUIRED", "primary_goal": None},
            {"state_id": "K1_C", "K": 1, "recommendation_status": "SEARCH_REQUIRED", "primary_goal": None},
        ]}
        conditional = {"state_plans": [
            {"state_id": "K1_A", "K": 1, "recommendation_status": "CONDITIONAL_TEMPLATE_CONSENSUS_WITH_DIRECT_HOLDOUT_EVIDENCE", "primary_goal": {"goal_template": {"K": 1}}},
            {"state_id": "K1_B", "K": 1, "recommendation_status": "CONDITIONAL_TEMPLATE_CONSENSUS_WITH_DIRECT_HOLDOUT_EVIDENCE", "primary_goal": {"goal_template": {"K": 1}}},
            {"state_id": "K1_C", "K": 1, "recommendation_status": "CONDITIONAL_TEMPLATE_AUDIT_ONLY", "primary_goal": None},
        ]}
        result = build(direct, conditional)
        statuses = {row["state_id"]: row["recommendation_status"] for row in result["state_plans"]}
        self.assertEqual(statuses["K1_A"], "DIRECT_FINE_GOAL_CONSENSUS")
        self.assertEqual(statuses["K1_B"], "CONDITIONAL_SEMANTIC_GOAL_CONSENSUS_PENDING_FINE_COMPILATION")
        self.assertEqual(statuses["K1_C"], "SEARCH_REQUIRED_NO_HIGH_CONFIDENCE_GOAL")

    def test_rejects_cross_k_conditional_template(self):
        direct = {"state_plans": [{"state_id": "K1_A", "K": 1, "recommendation_status": "SEARCH_REQUIRED"}]}
        conditional = {"state_plans": [{"state_id": "K1_A", "K": 1, "recommendation_status": "CONDITIONAL_TEMPLATE_CONSENSUS_WITH_DIRECT_HOLDOUT_EVIDENCE", "primary_goal": {"goal_template": {"K": 2}}}]}
        with self.assertRaises(ValueError):
            build(direct, conditional)


if __name__ == "__main__":
    unittest.main()
