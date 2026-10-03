import unittest
import math
import time
from dataclasses import replace

import numpy as np

from planning_proxy.first_player_strategy import (
    EDGE_DEAD_RIGHT,
    DefenceShape,
    GUARD_TARGET,
    HOUSE_PAIR_LEFT,
    HOUSE_PAIR_RIGHT,
    HOUSE_X,
    HOUSE_Y,
    INNER_RING_R,
    OPENING_CENTRE_GUARD_SHOT,
    FirstPlayerPlan,
    StrategyStone,
    classify_first_player_situation,
    is_edge_dead,
    plan_first_player_turn,
    score_strict_outcome,
)
from local_simulator.examples.train_policy_tree_selfplay import install_bundled_pyphysx
from planning_proxy.analytic_proxy import ProxyStone
from planning_proxy.evaluate_vs_teammate_ppo import (
    ProxyMatchPlayer,
    declared_defence_shape_is_synthetically_reachable,
    existing_stones_remain_static,
    topology_diverse_rows,
)
from planning_proxy.strict_refine import BoardStone, make_position


def stone(index, owner, x, y, enabled=True):
    return {"index": index, "owner": owner, "x": x, "y": y, "enabled": enabled}


class FirstPlayerStrategyTests(unittest.TestCase):
    def test_plan_round_trips_explicit_own_loss_budget(self):
        plan = FirstPlayerPlan(
            shot_index=10, own_throw_number=6, phase="k6_preserve_anchor",
            target_points=((HOUSE_X, HOUSE_Y),), target_opponent_index=9,
            opponent_action="physical_clear", rationale="test", max_own_cleared=0,
        )
        recovered = FirstPlayerPlan.from_json(plan.to_json())
        self.assertEqual(recovered.max_own_cleared, 0)

    def test_preserve_initial_centre_guard_rejects_active_stone_impersonation(self):
        """新壶落进守壶带，不能冒充被本手撞开的原屏风。"""

        initial = [
            stone(0, "self", HOUSE_X, 7.15),
            stone(11, "opponent", 2.85, 6.79),
        ]
        target = (HOUSE_X - 0.18, HOUSE_Y + 1.59)
        plan = FirstPlayerPlan(
            shot_index=12, own_throw_number=7,
            phase="seventh_clear_and_roll_to_historical_control",
            target_points=(target,), target_opponent_index=11,
            opponent_action="physical_clear", rationale="test",
            landing_region_radius_m=0.22,
            defence_shapes=(DefenceShape(
                "保留原屏风", "test", (target,), required_inner_count=0,
                landing_region_radius_m=0.22,
                preserve_initial_centre_guard=True,
            ),),
            max_own_cleared=0,
        )
        final = [{"enabled": False, "x": 0.0, "y": 0.0} for _ in range(13)]
        # slot 12 自己落进前场守壶带，但 slot 0 已被拖走。
        final[0] = {"enabled": True, "x": 1.65, "y": 7.15}
        final[12] = {"enabled": True, "x": target[0], "y": target[1]}
        self.assertFalse(score_strict_outcome(final, initial, 12, plan)[1])
        # 原 slot 保持在屏风角色带内后，才可接受同一落点。
        final[0] = {"enabled": True, "x": 2.10, "y": 7.30}
        self.assertTrue(score_strict_outcome(final, initial, 12, plan)[1])

    def test_first_throw_is_centre_guard(self):
        plan = plan_first_player_turn([], 0)
        self.assertEqual(plan.phase, "open_centre_guard")
        self.assertEqual(plan.target_points, (GUARD_TARGET,))
        self.assertEqual(plan.situation_type, "P1_EMPTY_SHEET")
        self.assertEqual(plan.strategy_type, "PLACE_CENTRE_GUARD")
        self.assertEqual(plan.desired_state_type, "P2_CENTRE_GUARD_ESTABLISHED")

    def test_first_throw_uses_the_strictly_calibrated_fixed_guard_shot(self):
        self.assertEqual(OPENING_CENTRE_GUARD_SHOT, (2.739, -0.0243, 0.0))

    def test_house_pair_uses_widely_separated_diagonal_red_ring_slots(self):
        """两颗内圈壶须分布在红圈对角，不能退回按钮附近的紧凑双飞组合。"""

        for pair in (HOUSE_PAIR_LEFT, HOUSE_PAIR_RIGHT):
            with self.subTest(pair=pair):
                self.assertGreaterEqual(math.dist(*pair), 0.95)
                self.assertGreaterEqual(abs(pair[0][1] - pair[1][1]), 0.60)
                for x, y in pair:
                    self.assertLessEqual(math.hypot(x - HOUSE_X, y - HOUSE_Y), INNER_RING_R)

    def test_online_p1_returns_fixed_guard_without_candidate_search(self):
        # 绕过构造器中的粗代理资产初始化；P1 早返回不应使用任何这些资产。
        planner = ProxyMatchPlayer.__new__(ProxyMatchPlayer)
        planner.decision_budget_seconds = 90.0
        shot, detail = planner.choose([], proxy_team=0, shot_index=0, match_seed=0)
        self.assertEqual(shot, OPENING_CENTRE_GUARD_SHOT)
        self.assertEqual(detail["mode"], "first_player_opening_guard_fixed")
        self.assertEqual(detail["candidateCount"], 0)

    def test_classifier_identifies_the_two_protected_guard_cases(self):
        centre = classify_first_player_situation([stone(1, "opponent", 2.375, 7.20)], 2)
        side = classify_first_player_situation([stone(1, "opponent", 2.90, 7.20)], 2)
        self.assertEqual(centre.situation_type, "P2_PROTECTED_CENTRE_GUARD")
        self.assertEqual(centre.strategy_type, "AVOID_PROTECTED_GUARD_AND_DRAW_ANCHOR")
        self.assertEqual(side.situation_type, "P2_PROTECTED_SIDE_GUARD")
        self.assertEqual(side.strategy_type, "PUSH_GUARD_TO_EDGE_AND_ROLL_IN")

    def test_final_state_classification_requires_both_side_gates(self):
        state = classify_first_player_situation([
            stone(1, "self", 2.375, 7.15),
            stone(2, "self", 2.375, 4.88),
            stone(3, "self", 1.92, 6.12),
        ], 14)
        self.assertEqual(state.situation_type, "P8_FINAL_GATE_MISSING_THREE_PLUS_OWN")
        self.assertEqual(state.strategy_type, "COMPLETE_MISSING_GATE")
        self.assertEqual(state.desired_state_type, "P8_REPLY_SEARCH_REQUIRED_CENTRE_GUARD_DOUBLE_GATE")

    def test_strategy_tree_representative_branches_have_stable_labels(self):
        """每个主要策略节点至少有一个最小壶面，防止标签或优先级被误改。"""

        cases = [
            (2, [stone(1, "opponent", 2.375, 7.20)], "P2_PROTECTED_CENTRE_GUARD", "AVOID_PROTECTED_GUARD_AND_DRAW_ANCHOR"),
            (2, [stone(1, "opponent", 2.90, 7.20)], "P2_PROTECTED_SIDE_GUARD", "PUSH_GUARD_TO_EDGE_AND_ROLL_IN"),
            (2, [stone(1, "opponent", 2.375, 4.88)], "P2_ENEMY_ALREADY_SCORING", "CLEAR_AND_ROLL_TO_INNER_ANCHOR"),
            (2, [stone(1, "opponent", 0.30, 7.00)], "P2_NO_EFFECTIVE_ENEMY", "DRAW_FIRST_INNER_ANCHOR"),
            (4, [stone(1, "self", 2.10, 5.20), stone(2, "opponent", 2.375, 4.88)], "P3_ENEMY_HAS_CENTRE", "CLEAR_OR_OUTDRAW_TO_RETAKE_CENTRE"),
            (4, [stone(1, "self", 2.28, 4.70), stone(2, "opponent", 2.90, 7.20)], "P3_PROTECTED_SIDE_GUARD", "PUSH_EDGE_OR_BUILD_STAGGERED_PAIR"),
            (4, [stone(1, "self", 2.28, 4.70)], "P3_INNER_LAYER_MISSING", "BUILD_STAGGERED_INNER_PAIR"),
            (4, [stone(1, "self", 2.28, 4.70), stone(2, "self", 2.67, 5.18)], "P3_CENTRE_LAYER_PRESENT", "MAINTAIN_STAGGERED_ADVANTAGE"),
            (6, [stone(1, "self", 2.28, 4.70), stone(2, "opponent", 2.375, 4.88)], "P4_ENEMY_SCORING_THREAT", "CLEAR_AND_RECLAIM_CENTRE"),
            (6, [stone(1, "self", 2.28, 4.70)], "P4_INNER_LAYER_DAMAGED", "RESTORE_STAGGERED_INNER_PAIR"),
            (6, [stone(1, "self", 2.28, 4.70), stone(2, "self", 2.67, 5.18)], "P4_CENTRE_ADVANTAGE", "MAINTAIN_OR_SELECTIVE_CLEAR"),
            (8, [stone(1, "self", 2.28, 4.70), stone(2, "opponent", 2.375, 4.88)], "P5_ENEMY_THREAT_ONE_OWN", "CLEAR_THREAT_AND_ROLL_INTO_DEFENCE"),
            (8, [stone(1, "self", 2.28, 4.70)], "P5_NO_EFFECTIVE_ENEMY_ONE_OWN", "FILL_MISSING_DEFENCE_ROLE"),
            (10, [stone(1, "self", 2.28, 4.70), stone(2, "opponent", 2.375, 4.88)], "P6_ENEMY_THREAT_ONE_OWN", "CLEAR_THREAT_AND_ROLL_INTO_DEFENCE"),
            (10, [stone(1, "self", 2.28, 4.70), stone(2, "self", 2.67, 5.18)], "P6_NO_EFFECTIVE_ENEMY_TWO_OWN", "FILL_MISSING_DEFENCE_ROLE"),
        ]
        for shot_index, board, expected_type, expected_strategy in cases:
            with self.subTest(shot_index=shot_index, expected_type=expected_type):
                state = classify_first_player_situation(board, shot_index)
                self.assertEqual(state.situation_type, expected_type)
                self.assertEqual(state.strategy_type, expected_strategy)

    def test_second_throw_pushes_ordinary_protected_guard_to_edge(self):
        plan = plan_first_player_turn([stone(1, "opponent", 2.90, 7.20)], 2)
        self.assertEqual(plan.phase, "process_first_enemy_and_score")
        self.assertEqual(plan.target_opponent_index, 1)
        self.assertEqual(plan.opponent_action, "push_to_edge_dead")

    def test_second_throw_does_not_attack_protected_centre_guard(self):
        plan = plan_first_player_turn([stone(1, "opponent", 2.375, 7.20)], 2)
        self.assertIsNone(plan.target_opponent_index)
        self.assertEqual(plan.opponent_action, "avoid_protected_centre_guard")

    def test_k2_after_own_centre_guard_uses_the_around_guard_anchor(self):
        plan = plan_first_player_turn([stone(0, "self", 2.375, 7.14)], 2)
        self.assertEqual(plan.phase, "process_first_enemy_and_score")
        self.assertEqual(plan.target_points, ((1.932, 4.715),))
        self.assertIsNone(plan.target_opponent_index)
        self.assertEqual(plan.opponent_action, "none")

    def test_landing_target_is_an_explicit_region_not_an_exact_point(self):
        plan = replace(plan_first_player_turn([], 2), landing_region_radius_m=0.30)
        target_x, target_y = plan.target_points[0]
        inside = [
            {"enabled": False, "x": 0.0, "y": 0.0},
            {"enabled": False, "x": 0.0, "y": 0.0},
            {"enabled": True, "x": target_x + 0.29, "y": target_y},
        ]
        outside = [
            {"enabled": False, "x": 0.0, "y": 0.0},
            {"enabled": False, "x": 0.0, "y": 0.0},
            {"enabled": True, "x": target_x + 0.31, "y": target_y},
        ]
        self.assertTrue(score_strict_outcome(inside, [], 2, plan)[1])
        self.assertFalse(score_strict_outcome(outside, [], 2, plan)[1])

    def test_third_throw_reclaims_centre_instead_of_mechanically_adding_a_pair(self):
        plan = plan_first_player_turn([
            stone(1, "self", 2.10, 5.20),
            stone(2, "opponent", 2.375, 4.88),
        ], 4)
        self.assertEqual(plan.situation_type, "P3_ENEMY_HAS_CENTRE")
        self.assertEqual(plan.phase, "clear_then_repair_closest_scoring_anchor")
        self.assertEqual(plan.target_opponent_index, 2)
        self.assertEqual(plan.opponent_action, "physical_clear")

    def test_k3_counter_after_k2_anchor_is_cleared_offers_mirrored_inner_front_and_guard_aligned_targets(self):
        plan = plan_first_player_turn([
            stone(0, "self", 2.375, 7.14),
            stone(3, "opponent", 1.90, 5.006),
        ], 4)
        self.assertEqual(plan.situation_type, "P3_LEFT_HOUSE_COUNTER_AFTER_K2_CLEAR")
        self.assertEqual(plan.strategy_type, "CLEAR_AND_ROLL_TO_COUNTER_INNER_ANCHOR")
        self.assertEqual(plan.target_opponent_index, 3)
        self.assertEqual(
            plan.target_points,
            (
                (2.535, 4.985), (1.800, 5.250),
                (2.375, 5.12), (2.375, 4.86), (2.22, 5.0), (2.53, 5.0),
            ),
        )

    def test_centre_advantage_does_not_force_clear_an_outer_enemy(self):
        """P4 的“选择性处理”不能在规划层退化为见壶就清。"""

        plan = plan_first_player_turn([
            stone(1, "self", 2.28, 4.70),
            stone(2, "self", 2.67, 5.18),
            # 已过保护期、但既非营内也非自由防守区的外圈壶。
            stone(3, "opponent", 1.20, 10.90),
        ], 6)
        self.assertEqual(plan.situation_type, "P4_CENTRE_ADVANTAGE")
        self.assertEqual(plan.strategy_type, "MAINTAIN_OR_SELECTIVE_CLEAR")
        self.assertEqual(plan.phase, "maintain_centre_advantage")
        self.assertIsNone(plan.target_opponent_index)
        self.assertEqual(plan.opponent_action, "none")

    def test_k4_guard_only_rebuilds_first_anchor_instead_of_claiming_a_missing_second_layer(self):
        plan = plan_first_player_turn([
            stone(0, "self", 2.375, 7.14),
            stone(1, "opponent", 1.53, 7.50),
            stone(5, "opponent", 0.25, 4.31),
        ], 6)
        self.assertEqual(plan.situation_type, "P4_CENTRE_GUARD_ONLY_FIRST_ANCHOR_MISSING")
        self.assertEqual(plan.strategy_type, "REBUILD_FIRST_INNER_ANCHOR_AROUND_CENTRE_GUARD")
        self.assertEqual(plan.phase, "fourth_rebuild_first_anchor_around_centre_guard")
        self.assertEqual(plan.opponent_action, "none")
        self.assertEqual(plan.target_points, ((1.932, 4.715), (2.818, 4.715)))

    def test_k7_leading_with_only_external_enemies_adds_second_scoring_layer(self):
        plan = plan_first_player_turn([
            stone(1, "opponent", 1.53, 7.50),
            stone(5, "opponent", 0.25, 4.31),
            stone(8, "self", 1.49, 5.04),
            stone(11, "opponent", 2.29, 7.93),
        ], 12)
        self.assertEqual(plan.situation_type, "P7_SELF_SCORING_ONLY_EXTERNAL_OPPONENTS")
        self.assertEqual(plan.strategy_type, "ADD_SECOND_SCORING_LAYER_WITH_EXTERNAL_OBSTACLES")
        self.assertEqual(plan.phase, "seventh_add_second_scoring_layer_without_enemy_house_threat")
        self.assertEqual(plan.opponent_action, "none")
        self.assertEqual(plan.target_points, ((2.75, 4.56),))

    def test_k7_outer_house_threat_clears_then_reclaims_centre(self):
        plan = plan_first_player_turn([
            stone(0, "self", 0.78, 5.52),
            stone(1, "opponent", 1.53, 7.50),
            stone(5, "opponent", 0.25, 4.31),
            stone(11, "opponent", 3.64, 4.97),
        ], 12)
        self.assertEqual(plan.situation_type, "P7_ONE_OUTER_SELF_OUTER_ENEMY_HOUSE_THREAT")
        self.assertEqual(plan.strategy_type, "CLEAR_OUTER_THREAT_AND_RECLAIM_CENTRE")
        self.assertEqual(plan.phase, "seventh_clear_outer_threat_and_reclaim_centre")
        self.assertEqual(plan.target_points, ((2.375, 4.88),))
        self.assertEqual(plan.target_opponent_index, 11)
        self.assertEqual(plan.opponent_action, "physical_clear")

    def test_k4_single_anchor_clears_side_guard_and_holds_outer_roll(self):
        plan = plan_first_player_turn([
            stone(0, "self", 2.375, 7.14),
            stone(4, "self", 2.514, 5.046),
            stone(5, "opponent", 1.529, 7.427),
        ], 6)
        self.assertEqual(plan.situation_type, "P4_SINGLE_INNER_ANCHOR_OPPONENT_SIDE_GUARD")
        self.assertEqual(plan.strategy_type, "CLEAR_SIDE_GUARD_AND_HOLD_OUTER_ROLL")
        self.assertEqual(plan.phase, "clear_side_guard_and_hold_outer_roll")
        self.assertEqual(plan.target_points, ((1.50, 7.70),))
        self.assertEqual(plan.target_opponent_index, 5)

    def test_k5_single_anchor_uses_two_high_outer_exit_regions_against_near_centre_side_guard(self):
        plan = plan_first_player_turn([
            stone(0, "self", 2.375, 7.14),
            stone(4, "self", 2.514, 5.046),
            stone(7, "opponent", 2.299, 7.885),
        ], 8)
        self.assertEqual(plan.situation_type, "P5_SINGLE_INNER_ANCHOR_OPPONENT_SIDE_GUARD")
        self.assertEqual(plan.strategy_type, "CLEAR_SIDE_GUARD_AND_HOLD_OUTER_ROLL")
        self.assertEqual(plan.phase, "clear_side_guard_and_hold_outer_roll")
        self.assertEqual(plan.target_points, ((1.50, 7.70), (3.25, 7.70)))
        self.assertEqual(plan.target_opponent_index, 7)
        self.assertEqual(plan.max_own_cleared, 0)

    def test_k5_side_guard_hold_does_not_claim_a_single_threat_when_two_enemies_remain(self):
        """该边只适用于清掉唯一有效敌壶即可恢复结构的局面。"""

        plan = plan_first_player_turn([
            stone(0, "self", 2.375, 7.14),
            stone(4, "self", 2.514, 5.046),
            stone(5, "opponent", 3.45, 7.82),
            stone(7, "opponent", 2.299, 7.885),
        ], 8)
        self.assertNotEqual(plan.strategy_type, "CLEAR_SIDE_GUARD_AND_HOLD_OUTER_ROLL")

    def test_side_guard_hold_contract_rejects_a_roll_that_drags_the_centre_guard_into_house(self):
        initial = [
            stone(0, "self", 2.375, 7.14),
            stone(4, "self", 2.439, 4.945),
            stone(7, "opponent", 2.299, 7.885),
        ]
        plan = plan_first_player_turn(initial, 8)
        final = [{"enabled": False, "x": 0.0, "y": 0.0} for _ in range(9)]
        # 守壶虽然没有出界，却被带入大本营；这会让原锚裸露，不能验收。
        final[0] = {"enabled": True, "x": 1.93, "y": 5.76}
        final[4] = {"enabled": True, "x": 2.439, "y": 4.945}
        final[8] = {"enabled": True, "x": 1.26, "y": 7.70}
        self.assertFalse(score_strict_outcome(final, initial, 8, plan)[1])
        # 保持原锚和中线守壶后，同一清壶/高外环落位才构成有效状态转换。
        final[0] = {"enabled": True, "x": 2.375, "y": 7.14}
        self.assertTrue(score_strict_outcome(final, initial, 8, plan)[1])

    def test_k5_side_guard_displacement_requires_cross_centre_and_stay_out_of_house(self):
        """次级 K5 边不能把敌壶留在原侧或误推入营内。"""

        initial = [
            stone(0, "self", 2.375, 7.14),
            stone(4, "self", 2.519, 4.88),
            stone(7, "opponent", 2.146, 7.912),
        ]
        plan = replace(
            plan_first_player_turn(initial, 8),
            phase="displace_side_guard_across_centre_and_hold_outer_roll",
            opponent_action="physical_displace",
        )
        final = [{"enabled": False, "x": 0.0, "y": 0.0} for _ in range(9)]
        final[0] = {"enabled": True, "x": 2.375, "y": 7.14}
        final[4] = {"enabled": True, "x": 2.519, "y": 4.88}
        final[7] = {"enabled": True, "x": 2.64, "y": 7.34}
        final[8] = {"enabled": True, "x": 1.62, "y": 7.75}
        self.assertTrue(score_strict_outcome(final, initial, 8, plan)[1])
        final[7] = {"enabled": True, "x": 2.10, "y": 7.34}
        self.assertFalse(score_strict_outcome(final, initial, 8, plan)[1])
        final[7] = {"enabled": True, "x": 1.20, "y": 5.73}
        self.assertFalse(score_strict_outcome(final, initial, 8, plan)[1])


    def test_fifth_throw_starts_the_defence_role_search(self):
        """P5 不再沿用旧版的红圈补壶分支，而是提前一手进入原 P6 的阵型搜索。"""

        plan = plan_first_player_turn([stone(1, "self", 2.28, 4.70)], 8)
        self.assertEqual(plan.phase, "fifth_clear_and_choose_defence_shape")
        self.assertEqual(plan.strategy_type, "FILL_MISSING_DEFENCE_ROLE")
        self.assertEqual(
            {shape.name for shape in plan.defence_shapes},
            {"单壶_双红圈错层", "单壶_左侧护门", "单壶_右侧护门"},
        )

    def test_fifth_throw_side_house_threat_can_hold_high_front_shoulder(self):
        """P5 薄撞局面不能被低侧门模板错误排除。"""

        plan = plan_first_player_turn([
            stone(2, "self", 3.916, 6.653),
            stone(3, "opponent", 2.058, 6.731),
            stone(4, "self", 3.329, 3.390),
            stone(6, "self", 1.647, 7.135),
            stone(7, "opponent", 2.352, 8.264),
        ], 8)
        self.assertEqual(plan.phase, "fifth_clear_and_hold_front_shoulder")
        self.assertEqual(plan.situation_type, "P5_LEFT_FRONT_GUARD_CONTEST_NO_INNER")
        self.assertEqual(plan.strategy_type, "CLEAR_AND_HOLD_FRONT_SHOULDER")
        self.assertEqual(plan.target_opponent_index, 3)
        self.assertEqual(plan.target_points, ((1.88, 6.98),))
        self.assertEqual(plan.landing_region_radius_m, 0.10)

    def test_k5_after_screen_clears_inner_threat_and_restores_side_anchor(self):
        plan = plan_first_player_turn([
            stone(0, "self", 2.375, 7.137),
            stone(5, "opponent", 2.126, 5.152),
            stone(6, "self", 2.916, 6.347),
        ], 8)
        self.assertEqual(plan.situation_type, "P5_LEFT_INNER_THREAT_AFTER_SCREEN")
        self.assertEqual(plan.strategy_type, "CLEAR_AND_RESTORE_SIDE_INNER_ANCHOR")
        self.assertEqual(plan.phase, "fifth_clear_and_restore_side_inner_anchor")
        self.assertEqual(plan.target_opponent_index, 5)
        self.assertEqual(plan.target_points, ((1.78, 5.33),))

    def test_k5_after_k4_guard_clear_adds_the_second_staggered_inner_layer(self):
        plan = plan_first_player_turn([
            stone(0, "self", 2.375, 7.137),
            stone(4, "self", 2.200, 4.456),
            stone(6, "self", 0.169, 6.461),
        ], 8)
        self.assertEqual(plan.situation_type, "P5_ONE_INNER_LEFT_ANCHOR_NO_ENEMY")
        self.assertEqual(plan.strategy_type, "ADD_SECOND_STAGGERED_INNER_LAYER")
        self.assertEqual(plan.phase, "fifth_add_second_staggered_inner_layer")
        self.assertEqual(plan.target_points, ((2.139136, 5.123235),))
        self.assertEqual(plan.landing_region_radius_m, 0.153234)

    def test_k6_single_centre_guard_vs_near_centre_front_house_threat_clears_to_inner_side_control(self):
        plan = plan_first_player_turn([
            stone(0, "self", HOUSE_X, 7.15),
            stone(9, "opponent", HOUSE_X + 0.40, 6.20),
        ], 10)
        self.assertEqual(plan.phase, "sixth_clear_near_centre_front_house_threat")
        self.assertEqual(plan.target_opponent_index, 9)
        self.assertEqual(plan.target_points, ((HOUSE_X + 0.23, 6.16),))
        self.assertEqual(plan.max_own_cleared, 0)

    def test_k6_deeper_near_centre_house_threat_keeps_outdraw_path_available(self):
        plan = plan_first_player_turn([
            stone(0, "self", HOUSE_X, 7.15),
            stone(9, "opponent", HOUSE_X + 0.40, HOUSE_Y + 1.05),
        ], 10)
        self.assertNotEqual(plan.phase, "sixth_clear_near_centre_front_house_threat")

    def test_k6_with_one_inner_anchor_prefers_promote_over_automatic_clear(self):
        plan = plan_first_player_turn([
            stone(0, "self", 2.375, 7.137),
            stone(4, "self", 2.200, 4.456),
            stone(6, "self", 0.169, 6.461),
            stone(9, "opponent", 2.662, 5.151),
        ], 10)
        self.assertEqual(plan.situation_type, "P6_ONE_INNER_ANCHOR_OPPONENT_HOUSE_COUNTER")
        self.assertEqual(plan.strategy_type, "PROMOTE_TO_HISTORICAL_CONTROL")
        self.assertEqual(plan.phase, "sixth_promote_to_historical_control")
        self.assertEqual(plan.target_opponent_index, 9)
        self.assertEqual(plan.opponent_action, "physical_displace")
        self.assertEqual(plan.target_points, ((2.567868, 5.307504),))
        self.assertEqual(plan.landing_region_radius_m, 0.163308)
        final = [{"enabled": False, "x": 0.0, "y": 0.0} for _ in range(11)]
        final[0] = {"enabled": True, "x": 2.375, "y": 7.137}
        final[4] = {"enabled": True, "x": 2.200, "y": 4.456}
        final[6] = {"enabled": True, "x": 0.169, "y": 6.461}
        final[9] = {"enabled": True, "x": 3.100, "y": 5.151}
        final[10] = {"enabled": True, "x": 2.567868, "y": 5.307504}
        _, goal = score_strict_outcome(final, [
            stone(0, "self", 2.375, 7.137), stone(4, "self", 2.200, 4.456),
            stone(6, "self", 0.169, 6.461), stone(9, "opponent", 2.662, 5.151),
        ], 10, plan)
        self.assertTrue(goal)

    def test_k6_cross_layer_contract_counts_scoring_house_layers_not_two_inner_rings(self):
        """K5 跨侧后，旧锚可以在大本营外圈；G6 仍须接受两颗可得分壶。"""
        initial = [
            stone(0, "self", 2.375, 7.137),
            stone(4, "self", 2.200, 4.456),
            stone(6, "self", 0.169, 6.461),
            stone(9, "opponent", 2.671, 5.151),
        ]
        base = plan_first_player_turn(initial, 10)
        plan = replace(
            base,
            phase="sixth_clear_right_threat_keep_two_layers",
            target_points=((2.55, 5.445),),
            landing_region_radius_m=0.15,
            opponent_action="physical_clear",
            max_own_cleared=0,
        )
        final = [{"enabled": False, "x": 0.0, "y": 0.0} for _ in range(11)]
        final[0] = {"enabled": True, "x": 2.375, "y": 7.137}
        # 这颗不是最内圈，但仍在大本营，构成第二个可得分层。
        final[4] = {"enabled": True, "x": 2.200, "y": 4.456}
        final[6] = {"enabled": True, "x": 0.169, "y": 6.461}
        final[10] = {"enabled": True, "x": 2.457, "y": 5.426}
        _, goal = score_strict_outcome(final, initial, 10, plan)
        self.assertTrue(goal)

    def test_seventh_throw_repairs_missing_front_guard(self):
        board = [
            stone(1, "self", 2.28, 4.70),
            stone(2, "self", 2.67, 5.18),
            stone(3, "opponent", 1.20, 8.0),
        ]
        plan = plan_first_player_turn(board, 12)
        self.assertEqual(plan.phase, "clear_then_choose_defence_shape")
        self.assertEqual(plan.target_opponent_index, 3)
        self.assertEqual(plan.opponent_action, "physical_clear")
        self.assertEqual({shape.name for shape in plan.defence_shapes}, {"双壶_左侧三角", "双壶_右侧三角", "双壶_第三红圈错层"})
        self.assertGreaterEqual(len(plan.target_points), 8)

    def test_k7_single_house_threat_uses_clear_and_historical_control_transition(self):
        """这不是泛化 K7：只覆盖当前 PPO 失败轨迹中的两外圈残局。"""

        board = [
            stone(0, "self", 2.375, 7.137),
            stone(6, "self", 0.169, 6.461),
            stone(11, "opponent", 3.262, 5.535),
        ]
        plan = plan_first_player_turn(board, 12)
        self.assertEqual(plan.situation_type, "P7_TWO_OUTER_OWN_SINGLE_HOUSE_THREAT")
        self.assertEqual(plan.strategy_type, "CLEAR_AND_ROLL_TO_HISTORICAL_CONTROL")
        self.assertEqual(plan.phase, "seventh_clear_and_roll_to_historical_control")
        self.assertEqual(plan.target_opponent_index, 11)
        self.assertEqual(plan.target_points, ((2.136679, 5.285392),))
        self.assertEqual(plan.landing_region_radius_m, 0.10)
        final = [{"enabled": False, "x": 0.0, "y": 0.0} for _ in range(13)]
        final[0] = {"enabled": True, "x": 2.375, "y": 7.137}
        final[6] = {"enabled": True, "x": 0.169, "y": 6.461}
        final[12] = {"enabled": True, "x": 2.136679, "y": 5.285392}
        _, goal = score_strict_outcome(final, board, 12, plan)
        self.assertTrue(goal)

    def test_eighth_throw_reclaims_centre_before_everything_else(self):
        board = [
            stone(1, "self", 2.70, 5.20),
            stone(2, "self", 2.05, 5.30),
            stone(3, "opponent", 2.375, 4.88),
        ]
        plan = plan_first_player_turn(board, 14)
        self.assertEqual(plan.phase, "clear_then_choose_defence_shape")
        self.assertEqual({shape.name for shape in plan.defence_shapes}, {"双壶_左侧三角", "双壶_右侧三角", "双壶_第三红圈错层"})

    def test_k8_isolated_threat_uses_reachable_single_house_roll(self):
        """无营内己壶时，K8 不能伪造一手形成两层营内的历史高价值终局。"""

        board = [
            stone(4, "self", 0.184, 3.331),
            stone(6, "self", 0.192, 6.447),
            stone(13, "opponent", 2.270, 5.721),
        ]
        plan = plan_first_player_turn(board, 14)
        self.assertEqual(plan.situation_type, "P8_LEFT_HOUSE_THREAT_TWO_OWN_OUTER_ROLL")
        self.assertEqual(plan.strategy_type, "TERMINAL_CLEAR_AND_HOLD_SIDE_HOUSE_ROLL")
        self.assertEqual(plan.phase, "terminal_clear_and_hold_side_house_roll")
        self.assertEqual(plan.target_opponent_index, 13)
        self.assertEqual(plan.target_points, ((1.77, 5.88),))
        self.assertEqual(plan.landing_region_radius_m, 0.20)
        final = [{"enabled": False, "x": 0.0, "y": 0.0} for _ in range(15)]
        final[4] = {"enabled": True, "x": 0.184, "y": 3.331}
        final[6] = {"enabled": True, "x": 0.192, "y": 6.447}
        final[14] = {"enabled": True, "x": 1.77, "y": 5.88}
        _, goal = score_strict_outcome(final, board, 14, plan)
        self.assertTrue(goal)

    def test_k8_after_k7_button_reply_uses_the_same_house_roll_contract(self):
        """PPO 拆掉一颗外侧己壶后，不能退回无目标的安全球。"""

        board = [
            stone(0, "self", 2.375, 7.137),
            stone(12, "self", 2.803, 3.994),
            stone(13, "opponent", 2.125, 5.620),
        ]
        plan = plan_first_player_turn(board, 14)
        self.assertEqual(plan.situation_type, "P8_LEFT_HOUSE_THREAT_TWO_OWN_OUTER_ROLL")
        self.assertEqual(plan.strategy_type, "TERMINAL_CLEAR_AND_HOLD_SIDE_HOUSE_ROLL")
        self.assertEqual(plan.phase, "terminal_clear_and_hold_side_house_roll")
        self.assertEqual(plan.target_points, ((1.77, 5.88),))
        self.assertEqual(plan.target_opponent_index, 13)

    def test_k8_historical_winning_pair_contract_requires_both_front_house_sides(self):
        """K8 历史反推边不能被“清壶后单壶滚位”偷换。"""

        board = [
            # 已有己方前左壶；K8 要清唯一敌方营内壶并补前右壶。
            stone(4, "self", 1.72, 5.68),
            stone(13, "opponent", 2.375, 4.88),
        ]
        plan = plan_first_player_turn(board, 14)
        self.assertEqual(plan.situation_type, "P8_SINGLE_HOUSE_THREAT_COMPLETE_FRONT_RIGHT_PAIR")
        self.assertEqual(plan.strategy_type, "TERMINAL_CLEAR_AND_COMPLETE_FRONT_HOUSE_PAIR")
        self.assertEqual(plan.phase, "terminal_clear_and_complete_front_house_pair")
        self.assertEqual(plan.target_opponent_index, 13)
        self.assertAlmostEqual(plan.target_points[0][0], 3.075)
        self.assertAlmostEqual(plan.target_points[0][1], 5.23)
        shape = plan.defence_shapes[0]
        self.assertEqual(shape.required_own_front_left_count, 1)
        self.assertEqual(shape.required_own_front_right_count, 1)
        self.assertEqual(shape.max_opponent_house_count, 0)
        final = [{"enabled": False, "x": 0.0, "y": 0.0} for _ in range(15)]
        final[4] = {"enabled": True, "x": 1.72, "y": 5.68}
        final[14] = {"enabled": True, "x": 3.075, "y": 5.23}
        _, goal = score_strict_outcome(final, board, 14, plan)
        # 它满足历史 G8 的几何合同，但尚无 PPO 末壶通过收据，不得作为
        # 自动终局动作提交。
        self.assertFalse(goal)
        # 若出手壶仍停在左侧，即便清目标也不是该 G8。
        final[14] = {"enabled": True, "x": 1.675, "y": 5.23}
        _, goal = score_strict_outcome(final, board, 14, plan)
        self.assertFalse(goal)

    def test_k8_back_house_threat_reclaims_centre_instead_of_requesting_an_impossible_front_roll(self):
        """目标过 T 线时，清壶后的可达 G8 是按钮夺回，不是前营补门。"""

        board = [
            stone(8, "self", 1.493, 5.044),
            stone(13, "opponent", 2.615, 4.701),
        ]
        plan = plan_first_player_turn(board, 14)
        self.assertEqual(plan.situation_type, "P8_BACK_HOUSE_THREAT_RECLAIM_CENTRE")
        self.assertEqual(plan.strategy_type, "TERMINAL_CLEAR_AND_RECLAIM_CENTRE_FROM_BACK_HOUSE_THREAT")
        self.assertEqual(plan.phase, "terminal_clear_and_reclaim_centre_from_back_house_threat")
        self.assertEqual(plan.target_opponent_index, 13)
        self.assertEqual(plan.target_points, ((HOUSE_X, HOUSE_Y),))
        self.assertEqual(plan.landing_region_radius_m, 0.35)
        final = [{"enabled": False, "x": 0.0, "y": 0.0} for _ in range(15)]
        final[8] = {"enabled": True, "x": 1.493, "y": 5.044}
        final[14] = {"enabled": True, "x": 2.384, "y": 4.962}
        _, goal = score_strict_outcome(final, board, 14, plan)
        self.assertTrue(goal)

    def test_defence_shapes_change_with_own_stone_count(self):
        one_own = plan_first_player_turn([stone(1, "self", 2.28, 4.70)], 10)
        two_own = plan_first_player_turn([
            stone(1, "self", 2.28, 4.70),
            stone(2, "self", 2.67, 5.18),
        ], 10)
        three_own = plan_first_player_turn([
            stone(1, "self", 2.28, 4.70),
            stone(2, "self", 2.67, 5.18),
            stone(3, "self", 1.92, 6.12),
        ], 10)
        self.assertEqual({shape.name for shape in one_own.defence_shapes}, {"单壶_双红圈错层", "单壶_左侧护门", "单壶_右侧护门"})
        self.assertEqual({shape.name for shape in two_own.defence_shapes}, {"双壶_左侧三角", "双壶_右侧三角", "双壶_第三红圈错层"})
        self.assertEqual({shape.name for shape in three_own.defence_shapes}, {"三壶以上_中心锚双门", "三壶以上_左侧外壳", "三壶以上_右侧外壳", "三壶以上_红圈后备"})

    def test_any_one_defence_shape_is_an_acceptable_strict_goal(self):
        board = [
            stone(1, "self", 2.28, 4.70),
            stone(2, "self", 2.67, 5.18),
            stone(3, "opponent", 1.20, 8.0),
        ]
        plan = plan_first_player_turn(board, 12)
        # 对手 3 已被清出；出手壶落入左侧三角的其中一个保护槽。
        score, goal = score_strict_outcome(
            [
                {"enabled": True, "x": 2.28, "y": 4.70},
                {"enabled": True, "x": 2.67, "y": 5.18},
                {"enabled": False, "x": 0.0, "y": 0.0},
                {"enabled": False, "x": 0.0, "y": 0.0},
                {"enabled": True, "x": 1.92, "y": 6.12},
            ],
            board,
            4,
            plan,
        )
        self.assertTrue(goal)
        self.assertGreater(score, 0.0)

    def test_centre_anchor_double_gate_matches_the_reply_search_template(self):
        board = [
            stone(1, "self", 2.375, 7.15),
            stone(2, "self", 2.375, 4.88),
            stone(3, "self", 1.92, 6.12),
        ]
        plan = plan_first_player_turn(board, 14)
        self.assertIn("三壶以上_中心锚双门", {shape.name for shape in plan.defence_shapes})
        score, goal = score_strict_outcome(
            [
                {"enabled": False, "x": 0.0, "y": 0.0},
                {"enabled": True, "x": 2.375, "y": 7.15},
                {"enabled": True, "x": 2.375, "y": 4.88},
                {"enabled": True, "x": 1.92, "y": 6.12},
                {"enabled": True, "x": 2.83, "y": 6.12},
            ],
            board,
            4,
            plan,
        )
        self.assertTrue(goal)
        self.assertGreater(score, 0.0)

    def test_eighth_throw_does_not_certify_an_ordinary_side_shell(self):
        board = [
            stone(1, "self", 2.10, 4.52),
            stone(2, "self", 2.72, 5.15),
            stone(3, "self", 2.00, 4.70),
        ]
        plan = plan_first_player_turn(board, 14)
        _, goal = score_strict_outcome(
            [
                {"enabled": False, "x": 0.0, "y": 0.0},
                {"enabled": True, "x": 2.10, "y": 4.52},
                {"enabled": True, "x": 2.72, "y": 5.15},
                {"enabled": True, "x": 2.00, "y": 4.70},
                {"enabled": True, "x": 1.92, "y": 6.12},
            ],
            board,
            4,
            plan,
        )
        self.assertFalse(goal)

    def test_edge_dead_band_is_explicit(self):
        self.assertTrue(is_edge_dead(StrategyStone(1, "opponent", sum(EDGE_DEAD_RIGHT) / 2.0, 7.0)))

    def test_terminal_side_edge_enemy_is_not_selected_as_a_main_threat(self):
        # 高位贴边守壶仍可阻挡路径；但落在大本营纵向带、且已越过边缘带
        # 内缘的敌壶无法计分，K8 不应为清它放弃补己方得分/护门角色。
        plan = plan_first_player_turn([
            stone(0, "self", 2.375, 7.15),
            stone(13, "opponent", 0.18, 4.36),
        ], 14)
        self.assertIsNone(plan.target_opponent_index)
        self.assertEqual(plan.opponent_action, "none")

    def test_strict_outcome_recognizes_opening_guard(self):
        plan = plan_first_player_turn([], 0)
        score, goal = score_strict_outcome(
            [{"enabled": True, "x": GUARD_TARGET[0], "y": GUARD_TARGET[1]}], [], 0, plan,
        )
        self.assertTrue(goal)
        self.assertGreater(score, 0.0)

    def test_topology_diverse_rows_preserves_a_strong_curl_outside_nearest_half(self):
        """解析代理总榜不能静默删除反向强旋这类独立路线。"""

        candidates = np.asarray([
            (3.2, 1.0, -8.0), (3.2, 1.2, -9.0),
            (3.2, -1.0, 8.0), (3.2, -1.2, 9.0),
            (3.2, 0.0, 0.0), (3.2, 1.0, 8.0),
        ], dtype=np.float64)
        selected = topology_diverse_rows([0, 1, 4, 2, 3, 5], candidates, limit=4)
        self.assertIn(2, selected)  # 左横移 + 正强旋

    def test_k2_curling_draw_is_certified_at_its_declared_contract_radius(self):
        """真实 PhysX 回归：不能以 5cm 隐藏门槛拒绝 30cm 合同内的绕守壶球。"""

        # seed 20260720 的 K2 出手前壶面；K1 中线守壶仍在，目标只能用旋球
        # 绕开。yaw 也来自严格回放，防止把无碰撞约束弱化为二维假设。
        strict_board = (
            BoardStone(0, "self", 2.37542724609375, 7.154050364257813,
                       yaw=-1.3447864694148353),
        )
        proxy_board = (ProxyStone(0, "self", 2.37542724609375, 7.154050364257813),)
        plan = plan_first_player_turn(proxy_board, 2)
        seeds = [20276558, 20381287, 20486016]
        install_bundled_pyphysx()
        player = ProxyMatchPlayer(physics_seeds=3, parent_regions=3, decision_budget_seconds=45.0)
        result = player._try_fast_targeted_draw(
            strict_board=strict_board,
            proxy_board=proxy_board,
            position=make_position(strict_board),
            tactical_plan=plan,
            shot_index=2,
            seeds=seeds,
            deadline=time.perf_counter() + 45.0,
        )
        self.assertIsNotNone(result, "K2 绕中线守壶存在的严格 PhysX 路径不应被漏检")
        outcome, detail = result
        self.assertTrue(all(outcome.tactical_goal_met))
        self.assertTrue(existing_stones_remain_static(outcome, strict_board))
        self.assertLessEqual(detail["maxLandingErrorM"], plan.landing_region_radius_m)
        self.assertFalse(detail["preferredPrecisionMet"])
        self.assertTrue(detail["topologyAwareInitialisation"])

    def test_k8_dense_house_history_does_not_activate_exact_fixture(self):
        """默认决策不能以某次 PPO 回放的精确壶位作为状态机入口。"""

        states = [{"enabled": False} for _ in range(16)]
        for index, x, y, yaw in (
            (4, 2.3602523803710938, 6.492040171386719, 0.4944300643744172),
            (5, 3.573406219482422, 6.271276011230469, -0.8216371166145638),
            (11, 3.626434326171875, 5.909978403808594, -0.5465285023464285),
            (12, 2.3507843017578125, 7.7217841289062505, 0.6200968937683797),
            (13, 1.5294456481933594, 7.467793955566407, -1.369769461444558),
        ):
            states[index] = {"enabled": True, "x": x, "y": y, "yaw": yaw}
        install_bundled_pyphysx()
        player = ProxyMatchPlayer(physics_seeds=3, parent_regions=3, decision_budget_seconds=30.0)
        shot, detail = player.choose(states, proxy_team=0, shot_index=14, match_seed=20260720)
        self.assertNotEqual(shot, (3.0, -2.0, 12.0))
        self.assertNotEqual(detail["mode"], "first_player_k8_dense_house_reply_certified_hold")
        self.assertNotIn("lastReplyCertificate", detail)

    def test_repair_contract_accepts_clear_and_one_house_layer_when_full_shape_is_broken(self):
        """不能用缺失的历史内圈锚阻断已认证的清壶入营修复球。"""

        initial = [
            stone(0, "self", 2.37542724609375, 7.154050364257813),
            stone(7, "opponent", 2.7037200927734375, 5.4674506328125005),
        ]
        full_shape = plan_first_player_turn(initial, 8)
        self.assertTrue(full_shape.defence_shapes)
        strict_initial = (
            BoardStone(0, "self", 2.37542724609375, 7.154050364257813),
            BoardStone(7, "opponent", 2.7037200927734375, 5.4674506328125005),
        )
        self.assertFalse(
            declared_defence_shape_is_synthetically_reachable(full_shape, strict_initial, active_index=8),
        )
        repair = replace(
            full_shape,
            phase="clear_then_repair_outer_house_layer",
            defence_shapes=(),
        )
        final = [{"enabled": False, "x": 0.0, "y": 0.0} for _ in range(9)]
        final[0] = {"enabled": True, "x": 2.37542724609375, "y": 7.154050364257813}
        # 来自严格 PhysX 三种子认证的 K5 清壶滚位之一；它不是完整护门，
        # 但已经清威胁并补进大本营，故应走显式 repair 合同。
        final[8] = {"enabled": True, "x": 2.615215301513672, "y": 5.7613959453125005}
        _, full_goal = score_strict_outcome(final, initial, 8, full_shape)
        _, repair_goal = score_strict_outcome(final, initial, 8, repair)
        self.assertFalse(full_goal)
        self.assertTrue(repair_goal)

    def test_zero_own_and_one_own_are_different_late_state_machine_states(self):
        """零己方壶时不能声明需要两颗己方壶的防御形。"""

        enemy = stone(11, "opponent", 2.42, 5.37)
        zero_plan = plan_first_player_turn([enemy], 12)
        one_plan = plan_first_player_turn([
            stone(10, "self", 2.10, 3.36), enemy,
        ], 12)
        self.assertEqual(zero_plan.situation_type, "P7_ENEMY_THREAT_ZERO_OWN")
        self.assertEqual(zero_plan.strategy_type, "CLEAR_THREAT_AND_RECLAIM_FIRST_ANCHOR")
        self.assertEqual(zero_plan.defence_shapes, ())
        self.assertEqual(one_plan.situation_type, "P7_ENEMY_THREAT_ONE_OWN")
        self.assertTrue(one_plan.defence_shapes)

    def test_zero_own_reclaim_contract_requires_a_real_new_closest_inner_anchor(self):
        initial = [stone(11, "opponent", 2.42, 5.37)]
        plan = plan_first_player_turn(initial, 12)
        final = [{"enabled": False, "x": 0.0, "y": 0.0} for _ in range(13)]
        final[12] = {"enabled": True, "x": HOUSE_PAIR_LEFT[0][0], "y": HOUSE_PAIR_LEFT[0][1]}
        _, goal = score_strict_outcome(final, initial, 12, plan)
        self.assertTrue(goal)
        # 只把敌壶清掉、出手壶留在前场，不得误报为成功恢复第一锚。
        final[12] = {"enabled": True, "x": GUARD_TARGET[0], "y": GUARD_TARGET[1]}
        _, goal = score_strict_outcome(final, initial, 12, plan)
        self.assertFalse(goal)


if __name__ == "__main__":
    unittest.main()
