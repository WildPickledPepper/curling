import unittest
from unittest.mock import patch

from tools.reverse.recovered_curling_motion import B2Vec2, RecoveredUnityRandom, Speed, unity_friction
from tools.reverse.replay_bestshot_seeded import Bestshot, clamp_bestshot, initial_protocol_state, replay_until_y


class ReplayBestshotSeededTest(unittest.TestCase):
    def test_clamp_bestshot_matches_socket_entry_policy(self):
        low = clamp_bestshot(Bestshot(-2.0, -5.0, -20.0))
        high = clamp_bestshot(Bestshot(8.0, 5.0, 20.0))

        self.assertEqual(low, Bestshot(1.0, -2.23, -15.7))
        self.assertEqual(high, Bestshot(6.0, 2.23, 15.7))

    def test_initial_protocol_state_matches_recovered_axis_mapping(self):
        state = initial_protocol_state(Bestshot(3.0, -0.25, 1.5), release_x=2.3506, release_y=31.5)

        self.assertAlmostEqual(state.x, 2.1006)
        self.assertAlmostEqual(state.y, 31.5)
        self.assertAlmostEqual(state.vx, 0.0)
        self.assertAlmostEqual(state.vy, -3.0)
        self.assertAlmostEqual(state.w, 1.5)
        self.assertEqual(state.steps, 0)

    def test_seeded_replay_uses_first_unity_rng_friction_from_bestshot(self):
        frictions: list[float] = []

        def fake_newfrictionstep(friction: float, vec: B2Vec2, angle: float, steptime: float) -> Speed:
            frictions.append(friction)
            return Speed(B2Vec2(0.0, -2.0), 0.0)

        with patch("tools.reverse.replay_bestshot_seeded.newfrictionstep", side_effect=fake_newfrictionstep):
            state = replay_until_y(
                Bestshot(1.0, 0.0, 0.0),
                release_y=22.0,
                stop_y=21.99,
                unity_seed=2468,
                max_steps=3,
            )

        rng = RecoveredUnityRandom.from_seed(2468)
        self.assertEqual(frictions, [unity_friction(False, rng=rng, noise=None)])
        self.assertEqual(state.steps, 1)
        self.assertLessEqual(state.y, 21.99)

    def test_replay_stops_immediately_when_already_past_stop_y(self):
        with patch("tools.reverse.replay_bestshot_seeded.newfrictionstep") as mocked:
            state = replay_until_y(Bestshot(3.0, 0.0, 0.0), release_y=21.0, stop_y=21.52)

        mocked.assert_not_called()
        self.assertEqual(state.steps, 0)


if __name__ == "__main__":
    unittest.main()
