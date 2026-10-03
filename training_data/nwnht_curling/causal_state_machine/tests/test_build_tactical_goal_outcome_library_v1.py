import unittest

from training_data.nwnht_curling.causal_state_machine.build_tactical_goal_outcome_library_v1 import build


TOPOLOGY = (
    "K8_POST_OWN[control=NONE_OR_UNCERTAIN;F_BUTTON=0;F_HOUSE_FRONT_LEFT=0;F_HOUSE_FRONT_RIGHT=0;"
    "F_HOUSE_BACK_LEFT=0;F_HOUSE_BACK_RIGHT=0;O_BUTTON=0;O_HOUSE_FRONT_LEFT=0;O_HOUSE_FRONT_RIGHT=0;"
    "O_HOUSE_BACK_LEFT=0;O_HOUSE_BACK_RIGHT=0;F_protected_house=0;O_protected_house=0;macro=EMPTY]"
)


class TacticalGoalOutcomeLibraryTests(unittest.TestCase):
    def test_outcome_goal_keeps_topology_and_child_constraint_together(self):
        family = {
            "goal_id": "A", "source_state": "K8_STATE", "observed_template_kind": "DOUBLE_OR_MULTI_OPPONENT_REMOVAL",
            "tactical_target_zone": "NO_ACTIVE_FINAL_POINT", "observed_opponent_removed_count": 2,
            "observed_opponent_house_removed_count": 2,
            "fine_goal_options": [{"goal_id": "g", "active_final_region": None, "dynamic_house_removal_binding_request": {"choose_count": 2}}],
        }
        assignments = [
            {"panel_key": f"{index}:15", "K": 8, "source_state": "K8_STATE", "tactical_goal_id": "A", "fine_goal_id": "g", "post_own_topology": TOPOLOGY, "after_opponent_reply_state": "END"}
            for index in range(1, 4)
        ]
        transitions = [
            {"end_id": index, "own_global_shot_number": 15, "match_id": index,
             "terminal_end_label": {"first_end_margin": 0}}
            for index in range(1, 4)
        ]
        result = build([family], assignments, transitions, min_outcome_support=3, min_outcome_support_per_fold=0)
        self.assertEqual(result["manifest"]["outcome_goal_count"], 1)
        goal = result["goals"][0]
        self.assertEqual(goal["terminal_board_predicate"]["macro"], "EMPTY")
        self.assertEqual(goal["fine_goal_options"][0]["goal_id"], "g")
        self.assertEqual(goal["parent_action"]["observed_opponent_removed_count"], 2)
        self.assertEqual(len(result["observations"]), 3)


if __name__ == "__main__":
    unittest.main()
