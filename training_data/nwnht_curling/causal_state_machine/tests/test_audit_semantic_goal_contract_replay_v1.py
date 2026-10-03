import unittest

from training_data.nwnht_curling.causal_state_machine.audit_semantic_goal_contract_replay_v1 import audit


class SemanticGoalContractReplayTests(unittest.TestCase):
    def test_reports_primary_goal_replay_acceptance(self):
        plan = {"state_plans": [{
            "state_id": "K8_TEST", "primary_goal": {
                "source_state": "K8_TEST", "goal_id": "nwnht_v2_semantic_goal_5b3365c1bca86532", "K": 8,
                "after_opponent_reply_state_distribution": [{"value": "END", "count": 1, "share": 1.0}],
                "goal_state": {
                    "goal_id": "nwnht_v2_semantic_goal_5b3365c1bca86532", "K": 8,
                    "semantic_effect": {"first_house_delta": 0, "opponent_house_delta": 0, "opponent_removed_count": 0, "opponent_house_removed_count": 0},
                    "semantic_terminal_predicate": {"control": "NONE_OR_UNCERTAIN", "macro": "EMPTY"},
                    "fine_execution_status": "HAS_HISTORICAL_FINE_IMPLEMENTATION",
                    "fine_goal_options": [{"historical_support": 1, "active_final_region": None, "stone_constraints_when_unambiguous": [{"x": 1}], "dynamic_house_removal_binding_request": None, "after_own_occupancy": {}}],
                },
            },
        }]}
        # The synthetic hash is intentionally checked through the real key
        # generator by deriving it below rather than trusting a text label.
        from training_data.nwnht_curling.causal_state_machine.build_universal_semantic_goal_mdp_v1 import _goal_id, _semantic_key
        raw = {"panel_key": "1:1", "source_state": "K8_TEST", "K": 8, "observed_template_kind": "NO_OBSERVABLE_BOARD_CHANGE", "observed_delta": {"first_house": 0, "opponent_house": 0, "opponent_removed_count": 0, "opponent_house_removed_count": 0}, "post_own_topology": "K8_POST_OWN[control=NONE_OR_UNCERTAIN;F_BUTTON=0;F_HOUSE_FRONT_LEFT=0;F_HOUSE_FRONT_RIGHT=0;F_HOUSE_BACK_LEFT=0;F_HOUSE_BACK_RIGHT=0;O_BUTTON=0;O_HOUSE_FRONT_LEFT=0;O_HOUSE_FRONT_RIGHT=0;O_HOUSE_BACK_LEFT=0;O_HOUSE_BACK_RIGHT=0;F_protected_house=0;O_protected_house=0;macro=EMPTY]", "active_final_point": None}
        gid = _goal_id("K8_TEST", _semantic_key(raw))
        plan["state_plans"][0]["primary_goal"]["goal_id"] = gid
        plan["state_plans"][0]["primary_goal"]["goal_state"]["goal_id"] = gid
        transition = {"end_id": 1, "own_global_shot_number": 1, "s_before_own": [], "u_after_own": []}
        result = audit(plan, [raw], [transition])
        self.assertEqual(result["summary"]["semantic_accept_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()
