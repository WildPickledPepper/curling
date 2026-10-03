import unittest

from training_data.nwnht_curling.causal_state_machine.build_same_k_pooled_goal_policy_v1 import build


class SameKPooledGoalTests(unittest.TestCase):
    def test_state_without_direct_template_receives_same_k_pooled_candidate(self):
        prototypes = {"T": {"template_id": "T", "K": 8}}
        rows = [
            {"K": 8, "source_state": "S1", "template_id": "T", "next_state": "END", "margin": 1.0},
            {"K": 8, "source_state": "S1", "template_id": "T", "next_state": "END", "margin": 1.0},
            {"K": 8, "source_state": "S2", "template_id": "T", "next_state": "END", "margin": -1.0},
        ]
        result = build(rows, prototypes, {"S1": 8, "S2": 8, "S3": 8}, min_template_support=3, max_candidates=1)
        plan = next(row for row in result["state_plans"] if row["state_id"] == "S3")
        self.assertEqual(plan["primary_goal"]["template_id"], "T")
        self.assertEqual(plan["primary_goal"]["direct_support_in_this_state"], 0)
        self.assertEqual(plan["primary_goal"]["evidence_status"], "SAME_K_POOLED_NO_DIRECT_REALISATION")


if __name__ == "__main__":
    unittest.main()
