import unittest

from training_data.nwnht_curling.causal_state_machine.conditional_same_k_goal_audit_v1 import fit


class ConditionalSameKGoalAuditTests(unittest.TestCase):
    def test_neighbour_features_change_template_ranking(self):
        meta = {"A": (8, "M"), "B": (8, "M")}
        rows = [
            {"K": 8, "source_state": "A", "macro": "M", "template_id": "T1", "next_state": "END", "margin": 1.0, "features": {"x": "a"}},
            {"K": 8, "source_state": "A", "macro": "M", "template_id": "T1", "next_state": "END", "margin": 1.0, "features": {"x": "a"}},
            {"K": 8, "source_state": "B", "macro": "M", "template_id": "T2", "next_state": "END", "margin": 1.0, "features": {"x": "b"}},
            {"K": 8, "source_state": "B", "macro": "M", "template_id": "T2", "next_state": "END", "margin": 1.0, "features": {"x": "b"}},
        ]
        result = fit(rows, meta, min_template_support=1, max_candidates=1)
        self.assertEqual(result["A"][0]["template_id"], "T1")
        self.assertEqual(result["B"][0]["template_id"], "T2")


if __name__ == "__main__":
    unittest.main()
