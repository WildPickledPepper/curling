"""Regression tests for the optional compiled training rollout backend."""

from __future__ import annotations

import random
import unittest

from fast_curling_env import FastCurlingEnv, NUMBA_AVAILABLE, numba_rollout_scores


@unittest.skipUnless(NUMBA_AVAILABLE, "Numba is optional for the fast simulator")
class FastCurlingNumbaTest(unittest.TestCase):
    def test_single_shot_kernel_matches_python_surrogate(self) -> None:
        shots = [(3.0, 0.1, 0.0), (4.4, 0.0, 0.0), (3.0, -0.55, 3.14), (2.8, 0.7, 0.0)]
        reference = FastCurlingEnv(seed=11, accelerated=False)
        compiled = FastCurlingEnv(seed=11, accelerated=True)
        for index in range(16):
            shot = shots[index % len(shots)] if index % 2 == 0 else None
            if shot is None:
                reference.step()
                compiled.step()
            else:
                reference.step(shot)
                compiled.step(shot)
        self.assertLessEqual(
            max(abs(left - right) for left, right in zip(reference.position(), compiled.position())),
            1e-12,
        )
        self.assertEqual(reference.end_score(), compiled.end_score())

    def test_batch_rollouts_are_seed_deterministic_and_valid_scores(self) -> None:
        env = FastCurlingEnv(seed=4)
        for index in range(6):
            env.step((3.0, 0.1, 0.0)) if index % 2 == 0 else env.step()
        first = numba_rollout_scores(env, (3.0, 0.0, 0.0), 64, random.Random(91))
        second = numba_rollout_scores(env, (3.0, 0.0, 0.0), 64, random.Random(91))
        self.assertEqual(first.tolist(), second.tolist())
        self.assertTrue(all(-8 <= int(score) <= 8 for score in first))

    def test_batch_rollouts_support_second_player(self) -> None:
        env = FastCurlingEnv(seed=9)
        env.step((3.0, 0.0, 0.0))
        first = numba_rollout_scores(
            env, (3.0, 0.0, 0.0), 48, random.Random(12), player_is_init=False
        )
        second = numba_rollout_scores(
            env, (3.0, 0.0, 0.0), 48, random.Random(12), player_is_init=False
        )
        self.assertEqual(first.tolist(), second.tolist())
        self.assertTrue(all(-8 <= int(score) <= 8 for score in first))


if __name__ == "__main__":
    unittest.main()
