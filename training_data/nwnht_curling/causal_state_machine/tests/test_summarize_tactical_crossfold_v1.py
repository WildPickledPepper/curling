import unittest

from training_data.nwnht_curling.causal_state_machine.summarize_tactical_crossfold_v1 import build


def result(goal_id, zone, rank, correlation):
    return {"state_plans": [{
        "state_id": "K1_EMPTY",
        "primary_goal": {"goal_id": goal_id, "goal_state": {"tactical_target_zone": zone}},
        "descriptive_holdout_rank_diagnostic": {
            "primary_goal_holdout_rank": rank, "development_vs_holdout_spearman": correlation,
        },
    }]}


class SummarizeTacticalCrossfoldV1Tests(unittest.TestCase):
    def test_reports_repeated_primary_action_frequency(self):
        summary = build([result("A", "BUTTON", 1, 1.0), result("A", "BUTTON", 2, 0.5), result("B", "GUARD", 4, -0.2)])
        state = summary["states"][0]
        self.assertEqual(state["primary_mode_goal_id"], "A")
        self.assertEqual(state["primary_mode_share"], 0.666667)
        self.assertEqual(state["holdout_primary_rank_mean"], 2.333333)


if __name__ == "__main__":
    unittest.main()
