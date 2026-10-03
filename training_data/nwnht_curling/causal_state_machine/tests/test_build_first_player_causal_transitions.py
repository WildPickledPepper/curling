import unittest

from training_data.nwnht_curling.causal_state_machine.build_first_player_causal_transitions import rows_from_record
from training_data.nwnht_curling.discover_state_graph import EndRecord, Frame


def complete_record() -> EndRecord:
    record = EndRecord(
        end_id=7,
        match_id=3,
        end_number=1,
        match_type="Mens_Teams",
        teams=("A", "B"),
        score_before={"A": 0, "B": 0},
        score_after={"A": 1, "B": 0},
        final_score={"A": 6, "B": 4},
    )
    for shot in range(17):
        frame = Frame()
        if shot:
            frame.throwing_team = "A" if shot % 2 else "B"
            frame.call = "Draw" if shot % 2 else "Take-out"
            frame.rating = 3
        if shot >= 1:
            frame.stones.append(("red", 0.0, 0.8))
        if shot >= 2:
            frame.stones.append(("yellow", 0.2, 0.5))
        record.frames[shot] = frame
    return record


class CausalTransitionExportTests(unittest.TestCase):
    def test_complete_end_has_eight_s_u_reply_s_prime_rows(self):
        rows, reason = rows_from_record(complete_record(), {"event_name": "event", "event_start_date": "2018-01-01"})
        self.assertIsNone(reason)
        assert rows is not None
        self.assertEqual(len(rows), 8)
        first = rows[0]
        last = rows[-1]
        self.assertEqual(first["source_frames"], {"before_own": 0, "after_own": 1, "after_opponent_reply": 2})
        self.assertEqual(last["source_frames"], {"before_own": 14, "after_own": 15, "after_opponent_reply": 16})
        self.assertEqual(first["observed_own_delivery"]["called_shot"], "DRAW")
        self.assertEqual(first["observed_opponent_reply"]["called_shot"], "TAKEOUT")
        self.assertEqual(first["terminal_end_label"]["end_result"], "FIRST_SCORES")

    def test_missing_snapshot_is_rejected_not_repaired(self):
        record = complete_record()
        del record.frames[8]
        rows, reason = rows_from_record(record)
        self.assertIsNone(rows)
        self.assertEqual(reason, "missing_frame_0_to_16")


if __name__ == "__main__":
    unittest.main()
