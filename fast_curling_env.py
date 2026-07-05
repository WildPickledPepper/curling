# -*- coding: utf-8 -*-
"""Fast in-process simulator matching the local mock curling server."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple


HOUSE_X = 2.375
HOUSE_Y = 4.88
HOUSE_R = 1.830
STONE_R = 0.145
SHEET_WIDTH = 4.75
SHEET_LENGTH = 44.5
START_Y = 32.0

Shot = Tuple[float, float, float]
SweepShot = Tuple[float, float, float, float]


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.hypot(x1 - x2, y1 - y2)


def split_shot(shot: Sequence[float]) -> SweepShot:
    if len(shot) >= 4:
        v0, h0, w0, sweep = shot[:4]
    else:
        v0, h0, w0 = shot[:3]
        sweep = 0.0
    return (
        clamp(float(v0), 0.0, 6.0),
        clamp(float(h0), -2.23, 2.23),
        clamp(float(w0), -15.7, 15.7),
        clamp(float(sweep), 0.0, 12.0),
    )


@dataclass
class Stone:
    x: float = 0.0
    y: float = 0.0
    in_play: bool = False

    def pair(self) -> Tuple[float, float]:
        return (self.x, self.y) if self.in_play else (0.0, 0.0)


class FastCurlingEnv:
    """Single-end simulator where our agent is blue/first player."""

    def __init__(self, seed: Optional[int] = None):
        self.random = random.Random(seed)
        self.stones: List[Stone] = [Stone() for _ in range(16)]
        self.shot_num = 0

    def clone(self, seed: Optional[int] = None) -> "FastCurlingEnv":
        other = FastCurlingEnv(seed)
        other.stones = [Stone(s.x, s.y, s.in_play) for s in self.stones]
        other.shot_num = self.shot_num
        return other

    def reset(self, seed: Optional[int] = None) -> None:
        if seed is not None:
            self.random.seed(seed)
        self.stones = [Stone() for _ in range(16)]
        self.shot_num = 0

    def position(self) -> List[float]:
        values: List[float] = []
        for shot_idx in range(8):
            blue = self.stones[shot_idx * 2].pair()
            red = self.stones[shot_idx * 2 + 1].pair()
            values.extend([blue[0], blue[1], red[0], red[1]])
        return values

    def state_list(self) -> List[List[float]]:
        values = []
        pos = self.position()
        for n in range(8):
            values.append([pos[n * 4], pos[n * 4 + 1]])
            values.append([pos[n * 4 + 2], pos[n * 4 + 3]])
        return values

    def landing_point(self, v0: float, h0: float, w0: float) -> Tuple[float, float]:
        speed_term = clamp(v0, 0.0, 6.0)
        x = HOUSE_X + h0 * 0.88 + math.tanh(w0 / 5.0) * 0.55
        y = 8.0 - speed_term * 1.02 + abs(w0) * 0.05
        x += self.random.gauss(0.0, 0.035)
        y += self.random.gauss(0.0, 0.05)
        return (
            clamp(x, STONE_R, SHEET_WIDTH - STONE_R),
            clamp(y, STONE_R, START_Y),
        )

    def apply_simple_collision(self, stone_index: int, x: float, y: float) -> Tuple[float, float]:
        nearest_idx = None
        nearest_dist = float("inf")
        for idx, stone in enumerate(self.stones):
            if idx == stone_index or not stone.in_play:
                continue
            d = distance(x, y, stone.x, stone.y)
            if d < nearest_dist:
                nearest_dist = d
                nearest_idx = idx
        if nearest_idx is None or nearest_dist > STONE_R * 2.2:
            return x, y

        target = self.stones[nearest_idx]
        dx = target.x - x
        dy = target.y - y
        mag = math.hypot(dx, dy) or 1.0
        ux, uy = dx / mag, dy / mag
        target.x = clamp(target.x + ux * 0.55, STONE_R, SHEET_WIDTH - STONE_R)
        target.y = clamp(target.y + uy * 0.75, STONE_R, START_Y)
        return (
            clamp(target.x - ux * (STONE_R * 2.05), STONE_R, SHEET_WIDTH - STONE_R),
            clamp(target.y - uy * (STONE_R * 2.05), STONE_R, START_Y),
        )

    def place_stone(self, stone_index: int, shot: Sequence[float]) -> None:
        v0, h0, w0, sweep = split_shot(shot)
        x, y = self.landing_point(v0, h0, w0)
        y = clamp(y - sweep * 0.045, STONE_R, START_Y)
        x, y = self.apply_simple_collision(stone_index, x, y)
        self.stones[stone_index] = Stone(x=x, y=y, in_play=(y < SHEET_LENGTH and 0.0 < x < SHEET_WIDTH))

    def choose_opponent_shot(self) -> Shot:
        v0 = self.random.uniform(2.7, 3.5)
        h0 = self.random.uniform(-0.9, 0.9)
        w0 = self.random.uniform(-2.2, 2.2)
        if self.random.random() < 0.18:
            v0 += 1.1
        return (v0, h0, w0)

    def step(self, shot: Optional[Sequence[float]] = None) -> None:
        if self.shot_num >= 16:
            return
        if self.shot_num % 2 == 0:
            if shot is None:
                raise ValueError("Blue/player step requires a shot")
            self.place_stone(self.shot_num, shot)
        else:
            self.place_stone(self.shot_num, self.choose_opponent_shot())
        self.shot_num += 1

    def end_score(self) -> int:
        in_house: List[Tuple[float, bool]] = []
        for idx, stone in enumerate(self.stones):
            if not stone.in_play:
                continue
            d = distance(stone.x, stone.y, HOUSE_X, HOUSE_Y)
            if d <= HOUSE_R + STONE_R:
                in_house.append((d, idx % 2 == 0))
        if not in_house:
            return 0
        in_house.sort(key=lambda item: item[0])
        winning_is_blue = in_house[0][1]
        losing_best = min(
            [d for d, is_blue in in_house if is_blue != winning_is_blue],
            default=float("inf"),
        )
        score = sum(1 for d, is_blue in in_house if is_blue == winning_is_blue and d < losing_best)
        return score if winning_is_blue else -score


def score_position(position: Sequence[float]) -> int:
    env = FastCurlingEnv()
    for shot_idx in range(8):
        bx, by, rx, ry = position[shot_idx * 4 : shot_idx * 4 + 4]
        env.stones[shot_idx * 2] = Stone(bx, by, bool(bx or by))
        env.stones[shot_idx * 2 + 1] = Stone(rx, ry, bool(rx or ry))
    return env.end_score()
