import unittest

from planning_proxy.evaluate_vs_teammate_ppo import (
    active_stays_in_house, backhand_guard_draw_coarse_score, is_guard_draw_candidate,
    is_in_backhand_house_threat_zone, requires_single_enemy_roll_in,
)
from planning_proxy.strict_refine import BoardStone, Candidate, StrictEvaluation


def evaluation(active_distances, *, enemy_cleared=1):
    return StrictEvaluation(
        candidate=Candidate(4.0, 0.0, 0.0, 1),
        active_index=1,
        scores=[0.0] * len(active_distances),
        enemy_cleared=[enemy_cleared] * len(active_distances),
        own_cleared=[0] * len(active_distances),
        active_cleared=[False] * len(active_distances),
        total_self_cleared=[0] * len(active_distances),
        own_in_house=[1] * len(active_distances),
        preserves_all_own=True,
        rule_legal=True,
        rule_violations=[[] for _ in active_distances],
        enemy_cleared_indices=[[0] for _ in active_distances],
        final_center_distance_by_index=[{1: distance} for distance in active_distances],
        mean_score=0.0,
        worst_score=0.0,
    )


class BackhandRollInTests(unittest.TestCase):
    def test_active_must_stay_in_house_on_every_seed(self):
        self.assertTrue(active_stays_in_house(evaluation([0.25, 1.80, 1.975])))
        self.assertFalse(active_stays_in_house(evaluation([0.25, 2.00])))

    def test_guard_draw_keeps_active_in_house_and_does_not_clear_enemy(self):
        valid = evaluation([0.25, 1.50], enemy_cleared=0)
        self.assertTrue(is_guard_draw_candidate(valid))
        cleared = evaluation([0.25, 1.50], enemy_cleared=1)
        self.assertFalse(is_guard_draw_candidate(cleared))

    def test_guard_draw_coarse_score_prefers_clear_path_to_button(self):
        clear = backhand_guard_draw_coarse_score(2.375, 4.88, -1)
        hit = backhand_guard_draw_coarse_score(2.375, 4.88, 3)
        self.assertGreater(clear, hit)

    def test_centre_line_enemy_does_not_use_single_enemy_exchange_template(self):
        enemy = BoardStone(0, "opponent", 2.375, 5.50)
        self.assertFalse(requires_single_enemy_roll_in(
            proxy_team=1, board=[enemy], enemies=[enemy], target=enemy,
            target_index=0, last_hammer=False,
        ))

    def test_off_centre_lone_enemy_uses_single_enemy_exchange_template(self):
        enemy = BoardStone(0, "opponent", 2.80, 5.50)
        self.assertTrue(requires_single_enemy_roll_in(
            proxy_team=1, board=[enemy], enemies=[enemy], target=enemy,
            target_index=0, last_hammer=False,
        ))

    def test_front_threat_buffer_is_not_the_official_house_for_roll_in(self):
        # 2.10m 在正式边界 1.975m 外，但仍位于 25cm 的战术威胁带内。
        enemy = BoardStone(0, "opponent", 2.60, 6.96)
        self.assertTrue(is_in_backhand_house_threat_zone(enemy))
        self.assertFalse(requires_single_enemy_roll_in(
            proxy_team=1, board=[enemy], enemies=[enemy], target=enemy,
            target_index=0, last_hammer=False,
        ))


if __name__ == "__main__":
    unittest.main()
