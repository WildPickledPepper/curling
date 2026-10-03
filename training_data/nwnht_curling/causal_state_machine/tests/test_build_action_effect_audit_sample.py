import unittest

from training_data.nwnht_curling.causal_state_machine.build_action_effect_audit_sample import select_audit_rows


def row(effect, k, end_id):
    return {
        "match_id": 1,
        "end_id": end_id,
        "end_number": 1,
        "own_throw_number": k,
        "own_global_shot_number": 2 * k - 1,
        "source_frames": {},
        "observed_own_delivery": {"called_shot": "DRAW"},
        "observed_opponent_reply": {"called_shot": "FRONT"},
        "observed_own_board_effect": {"primary_effect": effect, "effect_tags": [], "before": {}, "after": {}, "delta": {}},
        "s_before_own": [],
        "u_after_own": [],
        "s_after_opponent_reply": [],
    }


class AuditSampleTests(unittest.TestCase):
    def test_sampling_is_bounded_and_covers_available_k_values(self):
        selected, manifest = select_audit_rows([
            row("ADD_PRESSURE_GUARD", 1, 1), row("ADD_PRESSURE_GUARD", 2, 2), row("ADD_PRESSURE_GUARD", 3, 3),
            row("ADD_OWN_HOUSE_LAYER", 1, 4),
        ], per_effect=2)
        self.assertEqual(len(selected), 3)
        self.assertEqual(manifest["effects"]["ADD_PRESSURE_GUARD"]["selected_count"], 2)
        self.assertEqual({item["own_throw_number"] for item in selected if item["primary_effect"] == "ADD_PRESSURE_GUARD"}, {1, 2})


if __name__ == "__main__":
    unittest.main()
