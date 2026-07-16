import json
import tempfile
import unittest
from pathlib import Path

from tools.calibration.controlled_scene_sampler import (
    ControlledShot,
    StonePlacement,
    connect_key_for_reset,
    format_payload,
    parse_plan_file,
    resolve_active_shot_num,
    reset_position_for_shot,
    stone_moves,
    stone_xy,
)


class ControlledSceneSamplerTest(unittest.TestCase):
    def test_connect_key_for_reset_appends_debug_suffix(self):
        self.assertEqual(connect_key_for_reset("localtest", True), "localtest:0")
        self.assertEqual(connect_key_for_reset("localtest:0", True), "localtest:0")
        self.assertEqual(connect_key_for_reset("localtest", False), "localtest")

    def test_reset_position_assigns_relative_target_indices(self):
        shot = ControlledShot(
            sample_id=0,
            label="collision",
            category="test",
            v0=3.0,
            h0=0.0,
            w0=0.0,
            stones=[StonePlacement(x=2.375, y=6.2), StonePlacement(x=2.5, y=5.0)],
        )

        position, indices = reset_position_for_shot(shot, active_shot_num=1)

        self.assertEqual(indices, [3, 5])
        self.assertEqual(stone_xy(position, 3), [2.375, 6.2])
        self.assertEqual(stone_xy(position, 5), [2.5, 5.0])

    def test_reset_position_rejects_active_stone_conflict(self):
        shot = ControlledShot(
            sample_id=0,
            label="bad",
            category="test",
            v0=3.0,
            h0=0.0,
            w0=0.0,
            stones=[StonePlacement(x=2.375, y=6.2, index=0)],
        )

        with self.assertRaisesRegex(ValueError, "conflicts with active stone"):
            reset_position_for_shot(shot, active_shot_num=0)

    def test_format_payload_requires_32_values(self):
        self.assertEqual(len(format_payload([0.0] * 32).split()), 32)
        with self.assertRaisesRegex(ValueError, "32 values"):
            format_payload([0.0] * 31)

    def test_stone_moves_reports_displacements(self):
        before = [0.0] * 32
        after = [0.0] * 32
        before[0] = 2.0
        before[1] = 5.0
        after[0] = 2.3
        after[1] = 5.4

        moves = stone_moves(before, after)

        self.assertAlmostEqual(moves[0]["distance"], 0.5)
        self.assertEqual(moves[1]["distance"], 0.0)

    def test_parse_plan_file(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "plan.json"
        path.write_text(
            json.dumps(
                [
                    {
                        "label": "sample",
                        "category": "collision",
                        "v0": 3.0,
                        "h0": 0.0,
                        "w0": 0.0,
                        "sweep": 4.0,
                        "active_index": 4,
                        "stones": [{"x": 2.375, "y": 6.2}],
                        "source_sample_id": 78,
                        "assigned_target_index": 2,
                    }
                ]
            ),
            encoding="utf-8",
        )

        shots = parse_plan_file(path)

        self.assertEqual(len(shots), 1)
        self.assertEqual(shots[0].label, "sample")
        self.assertEqual(shots[0].active_index, 4)
        self.assertEqual(shots[0].stones[0].y, 6.2)
        self.assertEqual(shots[0].metadata["source_sample_id"], 78)
        self.assertEqual(shots[0].metadata["assigned_target_index"], 2)

    def test_resolve_active_shot_num_uses_plan_index_when_enabled(self):
        shot = ControlledShot(
            sample_id=0,
            label="active",
            category="test",
            v0=3.0,
            h0=0.0,
            w0=0.0,
            active_index=4,
        )

        active = resolve_active_shot_num(
            shot,
            0,
            player_is_init=True,
            connect_name="Player1",
            use_reset=True,
            use_plan_active_index=True,
        )

        self.assertEqual(active, 4)

    def test_resolve_active_shot_num_rejects_wrong_parity(self):
        shot = ControlledShot(
            sample_id=0,
            label="active",
            category="test",
            v0=3.0,
            h0=0.0,
            w0=0.0,
            active_index=3,
        )

        with self.assertRaisesRegex(ValueError, "does not match"):
            resolve_active_shot_num(
                shot,
                0,
                player_is_init=True,
                connect_name="Player1",
                use_reset=True,
                use_plan_active_index=True,
            )


if __name__ == "__main__":
    unittest.main()
