#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from planning_proxy.endgame_shapes import ENDGAME_SHAPES, HOUSE_X, INNER_RING_R, match_shape, rank_shapes


def stone(x, y, owner, enabled=True):
    return {"x": x, "y": y, "owner": owner, "enabled": enabled}


class EndgameShapeTests(unittest.TestCase):
    def test_exact_lock_shape_is_feasible(self):
        shape = ENDGAME_SHAPES[0]
        board = [
            stone(shape.guard.x, shape.guard.y, "self"),
            stone(shape.house_slots[0].x, shape.house_slots[0].y, "self"),
            stone(shape.house_slots[1].x, shape.house_slots[1].y, "self"),
        ]
        result = match_shape(board, shape)
        self.assertTrue(result.feasible)
        self.assertEqual(result.guard_error, 0.0)
        self.assertEqual(result.house_error, 0.0)

    def test_enemy_in_inner_ring_rejects_feasibility(self):
        shape = ENDGAME_SHAPES[1]
        board = [
            stone(shape.guard.x, shape.guard.y, "self"),
            stone(shape.house_slots[0].x, shape.house_slots[0].y, "self"),
            stone(shape.house_slots[1].x, shape.house_slots[1].y, "self"),
            stone(HOUSE_X, 4.88 + INNER_RING_R / 2, "opponent"),
        ]
        self.assertFalse(match_shape(board, shape).feasible)

    def test_rank_selects_matching_shape(self):
        shape = ENDGAME_SHAPES[2]
        board = [
            stone(shape.guard.x, shape.guard.y, "self"),
            stone(shape.house_slots[0].x, shape.house_slots[0].y, "self"),
            stone(shape.house_slots[1].x, shape.house_slots[1].y, "self"),
        ]
        self.assertEqual(rank_shapes(board)[0].shape.name, shape.name)


if __name__ == "__main__":
    unittest.main()
