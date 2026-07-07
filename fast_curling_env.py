# -*- coding: utf-8 -*-
"""Fast in-process simulator matching the local mock curling server."""

from __future__ import annotations

import math
import random
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence, Tuple


HOUSE_X = 2.375
HOUSE_Y = 4.88
HOUSE_R = 1.830
STONE_R = 0.145
SHEET_WIDTH = 4.75
SHEET_LENGTH = 44.5
START_Y = 32.0
ROOT = Path(__file__).resolve().parent
CALIBRATION_FILE = ROOT / "config" / "physics_calibration.json"
UNITY_CALIBRATION_FILE = ROOT / "config" / "unity_physics_calibration.json"
_CALIBRATION_CACHE: Optional[dict] = None
_CALIBRATION_LOADED = False

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


def load_physics_calibration() -> Optional[dict]:
    global _CALIBRATION_CACHE, _CALIBRATION_LOADED
    if _CALIBRATION_LOADED:
        return _CALIBRATION_CACHE
    _CALIBRATION_LOADED = True
    for path in (UNITY_CALIBRATION_FILE, CALIBRATION_FILE):
        if not path.exists():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not payload.get("enabled", True):
            continue
        if payload.get("schema") not in {"official_no_sweep_landing_v1", "unity_landing_v2"}:
            continue
        _CALIBRATION_CACHE = payload
        break
    return _CALIBRATION_CACHE


def calibration_features(v0: float, h0: float, w0: float, sweep: float = 0.0, schema: str = "official_no_sweep_landing_v1") -> List[float]:
    if schema == "unity_landing_v2":
        return [
            1.0,
            v0,
            h0,
            w0,
            sweep,
            abs(w0),
            math.tanh(w0),
            v0 * v0,
            h0 * h0,
            w0 * w0,
            sweep * sweep,
            v0 * h0,
            v0 * w0,
            h0 * w0,
            v0 * sweep,
            h0 * sweep,
            w0 * sweep,
        ]
    return [
        1.0,
        v0,
        h0,
        w0,
        abs(w0),
        math.tanh(w0),
        v0 * v0,
        h0 * h0,
        w0 * w0,
        v0 * h0,
        v0 * w0,
        h0 * w0,
    ]


def within_calibration_support(payload: dict, v0: float, h0: float, w0: float) -> bool:
    ranges = payload.get("input_ranges", {})
    margin = float(payload.get("support_margin", 0.0))
    for name, value in [("v0", v0), ("h0", h0), ("w0", w0)]:
        bounds = ranges.get(name)
        if not bounds or len(bounds) != 2:
            return False
        low, high = float(bounds[0]) - margin, float(bounds[1]) + margin
        if value < low or value > high:
            return False
    return True


def calibrated_landing_point(v0: float, h0: float, w0: float, sweep: float = 0.0) -> Optional[Tuple[float, float, float, float]]:
    payload = load_physics_calibration()
    if payload is None or not within_calibration_support(payload, v0, h0, w0):
        return None
    schema = str(payload.get("schema", "official_no_sweep_landing_v1"))
    features = calibration_features(v0, h0, w0, sweep=sweep, schema=schema)
    coef_x = payload.get("coef_x", [])
    coef_y = payload.get("coef_y", [])
    if len(coef_x) != len(features) or len(coef_y) != len(features):
        return None
    x = sum(float(coef) * feature for coef, feature in zip(coef_x, features))
    y = sum(float(coef) * feature for coef, feature in zip(coef_y, features))
    return (
        x,
        y,
        float(payload.get("residual_std_x", 0.0)),
        float(payload.get("residual_std_y", 0.0)),
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

    def landing_point(self, v0: float, h0: float, w0: float, sweep: float = 0.0) -> Tuple[float, float]:
        speed_term = clamp(v0, 0.0, 6.0)
        calibrated = calibrated_landing_point(speed_term, h0, w0, sweep=sweep)
        if calibrated is None:
            x = HOUSE_X + h0 * 0.88 + math.tanh(w0 / 5.0) * 0.55
            y = 8.0 - speed_term * 1.02 + abs(w0) * 0.05
            x += self.random.gauss(0.0, 0.035)
            y += self.random.gauss(0.0, 0.05)
        else:
            x, y, std_x, std_y = calibrated
            x += self.random.gauss(0.0, std_x)
            y += self.random.gauss(0.0, std_y)
        return (
            clamp(x, STONE_R, SHEET_WIDTH - STONE_R),
            clamp(y, STONE_R, START_Y),
        )

    def apply_simple_collision(
        self,
        stone_index: int,
        x: float,
        y: float,
        v0: float = 3.0,
        h0: float = 0.0,
    ) -> Tuple[float, float]:
        nearest_idx = None
        nearest_dist = float("inf")
        if v0 >= 4.0:
            release_x = clamp(HOUSE_X + h0, STONE_R, SHEET_WIDTH - STONE_R)
            release_y = START_Y
            path_dx = x - release_x
            path_dy = y - release_y
            path_len2 = path_dx * path_dx + path_dy * path_dy
            for idx, stone in enumerate(self.stones):
                if idx == stone_index or not stone.in_play:
                    continue
                if path_len2 <= 1e-9:
                    d = distance(x, y, stone.x, stone.y)
                    t = 1.0
                else:
                    t = ((stone.x - release_x) * path_dx + (stone.y - release_y) * path_dy) / path_len2
                    if t < 0.0 or t > 1.05:
                        continue
                    closest_x = release_x + clamp(t, 0.0, 1.0) * path_dx
                    closest_y = release_y + clamp(t, 0.0, 1.0) * path_dy
                    d = distance(closest_x, closest_y, stone.x, stone.y)
                if d < nearest_dist:
                    nearest_dist = d
                    nearest_idx = idx
            if nearest_idx is None or nearest_dist > STONE_R * 2.4:
                return x, y

            target = self.stones[nearest_idx]
            dx = x - release_x
            dy = y - START_Y
            mag = math.hypot(dx, dy) or 1.0
            ux, uy = dx / mag, dy / mag
            power = clamp((v0 - 3.5) / 2.5, 0.25, 1.0)
            travel = 1.2 + 5.0 * power
            new_x = target.x + ux * travel
            new_y = target.y + uy * travel
            target.x = clamp(new_x, STONE_R, SHEET_WIDTH - STONE_R)
            target.y = clamp(new_y, STONE_R, START_Y)
            target.in_play = STONE_R < new_x < SHEET_WIDTH - STONE_R and STONE_R < new_y < START_Y
            roll = 0.25 + 0.55 * (1.0 - power)
            return (
                clamp(target.x - ux * (STONE_R * 2.05 + roll), STONE_R, SHEET_WIDTH - STONE_R),
                clamp(target.y - uy * (STONE_R * 2.05 + roll), STONE_R, START_Y),
            )

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
        x, y = self.landing_point(v0, h0, w0, sweep=sweep)
        payload = load_physics_calibration()
        if payload is None or payload.get("schema") != "unity_landing_v2":
            y = clamp(y - sweep * 0.045, STONE_R, START_Y)
        x, y = self.apply_simple_collision(stone_index, x, y, v0=v0, h0=h0)
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
