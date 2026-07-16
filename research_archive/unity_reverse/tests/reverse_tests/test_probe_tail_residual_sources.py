import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from tools.reverse import probe_tail_residual_sources as probe
from tools.reverse.parse_autodcp_record import parse_record
from tools.reverse.recovered_curling_motion import B2Vec2, RecoveredUnityRandom, SWEEP_FRICTION, Speed, unity_friction
from tools.reverse.recovered_sweep_window import MIDLINE_TRIGGER_PROTOCOL_Y


class ProbeTailResidualSourcesTest(unittest.TestCase):
    def make_row(self) -> dict:
        return {
            "sample_id": 0,
            "motion_x": 0.0,
            "motion_y": 0.0,
            "motion_vx": 0.02,
            "motion_vy": 0.0,
            "motion_w": 0.0,
            "final_x": 0.0,
            "final_y": 0.0,
        }

    def test_seeded_simulation_uses_unity_rng_after_skip(self):
        frictions: list[float] = []

        def fake_newfrictionstep(friction: float, vec: B2Vec2, angle: float, steptime: float) -> Speed:
            frictions.append(friction)
            return Speed(B2Vec2(0.0, 0.0), 0.0)

        with patch.object(probe, "newfrictionstep", side_effect=fake_newfrictionstep):
            _, _, steps, err = probe.simulate(
                self.make_row(),
                0.001,
                dt_pos=0.010,
                max_steps=3,
                unity_seed=12345,
                rng_skip=2,
                sweeping=False,
            )

        rng = RecoveredUnityRandom.from_seed(12345)
        unity_friction(False, rng=rng, noise=None)
        unity_friction(False, rng=rng, noise=None)
        expected = unity_friction(False, rng=rng, noise=None)

        self.assertEqual(steps, 1)
        self.assertEqual(err, 0.0)
        self.assertEqual(frictions, [expected])

    def test_constant_simulation_keeps_constant_friction(self):
        frictions: list[float] = []

        def fake_newfrictionstep(friction: float, vec: B2Vec2, angle: float, steptime: float) -> Speed:
            frictions.append(friction)
            return Speed(B2Vec2(0.0, 0.0), 0.0)

        with patch.object(probe, "newfrictionstep", side_effect=fake_newfrictionstep):
            probe.simulate(self.make_row(), 0.001, dt_pos=0.010, max_steps=3)

        self.assertEqual(frictions, [0.001])

    def test_autodcp_record_seed_can_feed_seeded_tail_probe(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.save"
            path.write_text(
                """
[0000]
BESTSHOT = BESTSHOT 3.0 0 0
RANDSEED = 2468
SWEEP = SWEEP 0
""".strip(),
                encoding="utf-8",
            )
            seed = parse_record(path).shots[0].randseed

        frictions: list[float] = []

        def fake_newfrictionstep(friction: float, vec: B2Vec2, angle: float, steptime: float) -> Speed:
            frictions.append(friction)
            return Speed(B2Vec2(0.0, 0.0), 0.0)

        with patch.object(probe, "newfrictionstep", side_effect=fake_newfrictionstep):
            probe.simulate(self.make_row(), 0.001, dt_pos=0.010, max_steps=3, unity_seed=seed)

        rng = RecoveredUnityRandom.from_seed(2468)
        self.assertEqual(frictions, [unity_friction(False, rng=rng, noise=None)])

    def test_sweep_distance_uses_recovered_y_window(self):
        row = {
            **self.make_row(),
            "motion_y": MIDLINE_TRIGGER_PROTOCOL_Y + 0.05,
            "motion_vx": 0.0,
            "motion_vy": -1.0,
            "final_y": MIDLINE_TRIGGER_PROTOCOL_Y - 0.45,
        }
        frictions: list[float] = []

        def fake_newfrictionstep(friction: float, vec: B2Vec2, angle: float, steptime: float) -> Speed:
            frictions.append(friction)
            return Speed(vec, angle)

        with patch.object(probe, "newfrictionstep", side_effect=fake_newfrictionstep):
            probe.simulate(row, 0.001, dt_pos=0.1, max_steps=5, sweep_distance=0.05)

        self.assertEqual(frictions[0], 0.001)
        self.assertEqual(frictions[1], SWEEP_FRICTION)
        self.assertEqual(frictions[2], SWEEP_FRICTION)
        self.assertEqual(frictions[3], SWEEP_FRICTION)
        self.assertEqual(frictions[4], 0.001)

    def test_row_sweep_distance_honors_sent_sweep_false(self):
        row = {"requested_sweep_distance": 8.0, "sent_sweep": False}

        self.assertIsNone(probe.row_sweep_distance(row, None, "requested_sweep_distance"))
        self.assertEqual(probe.row_sweep_distance(row, 8.0, "requested_sweep_distance"), 8.0)


if __name__ == "__main__":
    unittest.main()
