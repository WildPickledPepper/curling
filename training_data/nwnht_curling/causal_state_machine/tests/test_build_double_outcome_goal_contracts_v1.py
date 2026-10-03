import unittest

from training_data.nwnht_curling.causal_state_machine.build_double_outcome_goal_contracts_v1 import build, parse_post_own_topology


TOPOLOGY = (
    "K7_POST_OWN[control=NONE_OR_UNCERTAIN;F_BUTTON=0;F_HOUSE_FRONT_LEFT=0;F_HOUSE_FRONT_RIGHT=0;"
    "F_HOUSE_BACK_LEFT=0;F_HOUSE_BACK_RIGHT=0;O_BUTTON=0;O_HOUSE_FRONT_LEFT=0;O_HOUSE_FRONT_RIGHT=0;"
    "O_HOUSE_BACK_LEFT=0;O_HOUSE_BACK_RIGHT=0;F_protected_house=0;O_protected_house=0;macro=EMPTY]"
)


def family():
    return {
        "goal_id": "DOUBLE", "source_state": "K7_DOUBLE", "observed_template_kind": "DOUBLE_OR_MULTI_OPPONENT_REMOVAL",
        "support": 30, "observed_opponent_removed_count": 2, "observed_opponent_house_removed_count": 2,
        "fine_goal_options": [{"assigned_support": 30, "dynamic_house_removal_binding_request": {
            "binding_kind": "OPPONENT_HOUSE_SET", "owner": "opponent", "source_region": "house",
            "required_disposition": "OUT_OF_PLAY", "choose_count": 2,
        }, "stone_constraints_when_unambiguous": []}],
    }


def assignment(panel):
    return {"tactical_goal_id": "DOUBLE", "panel_key": panel, "post_own_topology": TOPOLOGY, "after_opponent_reply_state": "K8_S"}


def transition(panel, match):
    end, shot = panel.split(":")
    return {
        "end_id": int(end), "own_global_shot_number": int(shot), "match_id": match,
        "terminal_end_label": {"first_end_margin": 1, "end_result": "FIRST_SCORES"},
    }


class DoubleOutcomeGoalContractTests(unittest.TestCase):
    def test_topology_parser_keeps_whole_board_predicate(self):
        predicate = parse_post_own_topology(TOPOLOGY)
        self.assertEqual(predicate["F_BUTTON"], "0")
        self.assertEqual(predicate["O_HOUSE_BACK_RIGHT"], "0")
        self.assertEqual(predicate["macro"], "EMPTY")

    def test_double_contract_requires_two_out_and_records_fold_support(self):
        rows = [assignment("1:13"), assignment("2:13"), assignment("3:13")]
        transitions = [transition("1:13", 1), transition("2:13", 2), transition("3:13", 3)]
        result = build([family()], rows, transitions, min_outcome_support=3, min_outcome_fold_support=0)
        self.assertEqual(result["manifest"]["contract_count"], 1)
        contract = result["contracts"][0]
        self.assertEqual(contract["required_opponent_removed_count"], 2)
        self.assertEqual(contract["target_binding"]["choose_count"], 2)
        self.assertEqual(contract["terminal_board_predicate"]["macro"], "EMPTY")
        evidence = contract["observed_terminal_evidence"]
        self.assertEqual(evidence["observed_trajectory_count"], 3)
        self.assertEqual(evidence["first_end_margin_mean"], 1.0)
        self.assertEqual(evidence["end_result_distribution"][0]["value"], "FIRST_SCORES")


if __name__ == "__main__":
    unittest.main()
