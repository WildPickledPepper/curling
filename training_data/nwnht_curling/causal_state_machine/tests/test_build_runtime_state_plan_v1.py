import unittest

from training_data.nwnht_curling.causal_state_machine.build_runtime_state_plan_v1 import build, semantic_region


def family(goal_id, zone):
    return {
        "goal_id": goal_id, "source_state": "K1_EMPTY", "observed_template_kind": "ACTIVE_STONE_PLACEMENT",
        "tactical_target_zone": zone, "observed_opponent_removed_count": 0, "observed_opponent_house_removed_count": 0,
        "post_own_topology_distribution": [{"value": f"POST_{zone}", "count": 10, "share": 1.0}],
        "after_opponent_reply_state_distribution": [{"value": "K2_REPLY", "count": 10, "share": 1.0}],
    }


class BuildRuntimeStatePlanV1Tests(unittest.TestCase):
    def test_consensus_plan_keeps_narrow_goal_and_semantic_fallback_separate(self):
        partition = {"states": [{"state_id": "K1_EMPTY", "K": 1, "eligible_for_next_goal_stage": True}]}
        families = [family("A", "BUTTON"), family("B", "CENTRE_GUARD_NEAR")]
        fine_screen = {"parents": [{"tactical_goal_id": "A", "representative_execution_options": [{"goal_id": "G", "active_final_region": {"shape": "circle"}}]}]}
        outer = {"states": [{"state_id": "K1_EMPTY", "primary_mode_goal_id": "A", "primary_mode_share": 1.0}]}
        folds = [{"candidate_values": [
            {"source_state": "K1_EMPTY", "goal_id": "A", "eligible_for_empirical_ranking": True, "backed_up_value_mean": 1.0},
            {"source_state": "K1_EMPTY", "goal_id": "B", "eligible_for_empirical_ranking": True, "backed_up_value_mean": 0.5},
        ]} for _ in range(5)]
        result = build(partition, families, fine_screen, outer, folds)
        plan = result["state_plans"][0]
        self.assertEqual(plan["recommendation_status"], "EMPIRICAL_ACTION_CONSENSUS")
        self.assertEqual(plan["primary_action"]["precision_level"], "NARROW_CROSS_FOLD_GOAL")
        self.assertEqual(plan["fallback_actions"][0]["precision_level"], "SEMANTIC_REGION_GOAL")

    def test_semantic_region_has_canonical_geometry(self):
        self.assertEqual(semantic_region("BUTTON")["max_radius_m"], 0.6096)
        self.assertIsNone(semantic_region("NO_ACTIVE_FINAL_POINT"))


if __name__ == "__main__":
    unittest.main()
