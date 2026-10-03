import unittest

from training_data.nwnht_curling.causal_state_machine.build_local_k1_anchor_k2_subset_v1 import build


def row(*, after_reply):
    return {
        "end_id": 9, "own_global_shot_number": 1, "own_throw_number": 1, "match_id": 3,
        "u_after_own": [{"owner": "first", "x_m": 0.0, "y_m": 2.27}],
        "s_after_opponent_reply": after_reply,
        "offline_context": {"event_start_date": "2024-01-01"},
        "observed_opponent_reply": {"called_shot": "DRAW"},
    }


class LocalK1AnchorSubsetTests(unittest.TestCase):
    def test_keeps_legal_reply_with_anchor_and_house_stone(self):
        result = build([row(after_reply=[
            {"owner": "first", "x_m": 0.0, "y_m": 2.27},
            {"owner": "opponent", "x_m": 0.1, "y_m": 0.1},
        ])], old_state_by_panel={"9:1": "OLD"})
        self.assertEqual(result["manifest"]["retained_local_legal_reply_rows"], 1)
        self.assertEqual(result["states"][0]["state_id"], "S2_LOCAL_ANCHOR_OPPONENT_HOUSE")

    def test_excludes_a_ticked_anchor(self):
        result = build([row(after_reply=[
            {"owner": "first", "x_m": 0.4, "y_m": 2.27},
            {"owner": "opponent", "x_m": 0.1, "y_m": 0.1},
        ])], old_state_by_panel={})
        self.assertEqual(result["manifest"]["retained_local_legal_reply_rows"], 0)
        self.assertEqual(result["manifest"]["excluded_no_tick_conflict_rows"], 1)
