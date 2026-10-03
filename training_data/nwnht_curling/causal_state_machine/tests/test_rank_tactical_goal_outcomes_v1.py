import unittest

from training_data.nwnht_curling.causal_state_machine.rank_tactical_goal_outcomes_v1 import build


class GoalOutcomeRankTests(unittest.TestCase):
    def test_requires_repeated_primary_before_returning_goal(self):
        topology = "K8_POST_OWN[control=NONE_OR_UNCERTAIN;F_BUTTON=0;F_HOUSE_FRONT_LEFT=0;F_HOUSE_FRONT_RIGHT=0;F_HOUSE_BACK_LEFT=0;F_HOUSE_BACK_RIGHT=0;O_BUTTON=0;O_HOUSE_FRONT_LEFT=0;O_HOUSE_FRONT_RIGHT=0;O_HOUSE_BACK_LEFT=0;O_HOUSE_BACK_RIGHT=0;F_protected_house=0;O_protected_house=0;macro=EMPTY]"
        goal = {
            "goal_id": "G", "source_state": "K8_STATE", "observed_template_kind": "DRAW_TO_HOUSE",
            "precision": "TOPOLOGY_CONSTRAINED_HIERARCHICAL_GOAL", "active_final_region": None,
            "stone_constraints_when_unambiguous": [], "dynamic_house_removal_binding_request": None,
            "after_own_occupancy": {"first": {}, "opponent": {}}, "fine_goal_options": [],
            "execution_status": "CROSS_FOLD_TOPOLOGY_TARGET_CANDIDATE", "post_own_topology": topology,
            "terminal_board_predicate": {"macro": "EMPTY"},
        }
        observations = [
            {"match_id": fold + 1, "fold": fold, "K": 8, "source_state": "K8_STATE", "goal_id": "G", "next_state": "END", "post_own_topology": topology, "margin": 0.0}
            for fold in range(5)
        ]
        result = build({"goals": [goal], "observations": observations}, {"K8_STATE": 8}, min_development_support=1, min_holdout_support=1)
        plan = result["state_plans"][0]
        self.assertEqual(plan["recommendation_status"], "EMPIRICAL_GOAL_OUTCOME_CONSENSUS")
        self.assertEqual(plan["primary_goal"]["goal_id"], "G")
        self.assertEqual(plan["primary_goal"]["goal_state"]["terminal_board_predicate"]["macro"], "EMPTY")


if __name__ == "__main__":
    unittest.main()
