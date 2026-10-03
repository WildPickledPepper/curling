import unittest

from training_data.nwnht_curling.causal_state_machine.screen_fine_goal_options_v1 import build
from training_data.nwnht_curling.causal_state_machine.build_causal_estimation_panel import FOLDS, fold_for_match


class ScreenFineGoalOptionsV1Tests(unittest.TestCase):
    def test_requires_each_match_fold_and_keeps_narrow_goal_payload(self):
        families = [{
            "goal_id": "A", "source_state": "K1_EMPTY", "tactical_target_zone": "BUTTON", "support": 10,
            "fine_goal_options": [
                {"goal_id": "G_STABLE", "active_final_region": {"shape": "circle", "radius_m": 0.17}},
                {"goal_id": "G_THIN", "active_final_region": {"shape": "circle", "radius_m": 0.17}},
            ],
        }]
        match_by_fold = {}
        for match_id in range(1, 100):
            match_by_fold.setdefault(fold_for_match(match_id), match_id)
        self.assertEqual(len(match_by_fold), FOLDS)
        transitions = [
            {"end_id": fold + 1, "own_global_shot_number": 1, "match_id": match_id}
            for fold, match_id in sorted(match_by_fold.items())
        ]
        assignments = [
            {"tactical_goal_id": "A", "fine_goal_id": "G_STABLE", "panel_key": f"{i}:1"}
            for i in range(1, FOLDS + 1)
        ] + [{"tactical_goal_id": "A", "fine_goal_id": "G_THIN", "panel_key": "1:1"}]
        result = build(families, assignments, transitions, min_support_per_fold=1)
        parent = result["parents"][0]
        self.assertEqual([item["goal_id"] for item in parent["representative_execution_options"]], ["G_STABLE"])
        self.assertEqual(parent["representative_execution_options"][0]["active_final_region"]["radius_m"], 0.17)


if __name__ == "__main__":
    unittest.main()
