#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""白盒规划代理 P1：快速判断一颗壶自由滑行时最先会碰到谁。

这个模块不是 PhysX 的替代品。它只复用已经恢复的旋球自由滑行公式，把每
颗静止壶近似成圆盘，快速筛掉明显不可能的路线：先撞己方、完全擦不到敌方、
或在进入比赛区后直接出界。多壶连锁和最终落点仍必须由严格 PhysX 复核。

模块不依赖 pyphysx，所以可以用于一次生成数千个候选的粗筛阶段。
"""

from __future__ import annotations

import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_SUPPORT_ROOT = PROJECT_ROOT / "local_simulator" / "runtime_support"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(RUNTIME_SUPPORT_ROOT) not in sys.path:
    sys.path.insert(0, str(RUNTIME_SUPPORT_ROOT))

from tools.reverse.front_half_pcm_replay import (  # noqa: E402
    FORMAL_STONE_RADIUS,
    UNITY_FIXED_TIMESTEP,
    local_initial_state,
)
from tools.reverse.recovered_curling_motion import BASE_FRICTION, STEP, B2Vec2, newfrictionstep  # noqa: E402


# 与严格本地模拟器清场使用同一片比赛区。起始出手点在此区域之外，因此只有
# 壶首次进入 y <= PLAY_Y_MAX 后才开始判定出界。
PLAY_X_MIN = 0.145
PLAY_X_MAX = 4.605
PLAY_Y_MIN = 2.865
PLAY_Y_MAX = 10.525
CONTACT_DISTANCE = 2.0 * FORMAL_STONE_RADIUS + 0.02

_NATIVE_MOTION_STEP = None
_NATIVE_MOTION_CHECKED = False


def _motion_step(friction: float, vx: float, vy: float, w: float) -> Tuple[float, float, float]:
    """优先调用随项目交付的原生旋球步进；不可用时自动退回纯 Python。

    这里调用的不是完整 PhysX 碰撞世界，而只是已经打包在 pyphysx 扩展里的
    ``CurlingMotion.Newfrictionstep`` 数学步进。它保留 P1 的白盒性质，却避开
    Python 重复执行数百万次公式的开销。
    """

    global _NATIVE_MOTION_STEP, _NATIVE_MOTION_CHECKED
    if not _NATIVE_MOTION_CHECKED:
        _NATIVE_MOTION_CHECKED = True
        try:
            from local_simulator.runtime_loader import install_bundled_pyphysx

            install_bundled_pyphysx()
            import pyphysx  # type: ignore

            candidate = getattr(pyphysx, "curling_new_friction_step", None)
            if candidate is not None:
                _NATIVE_MOTION_STEP = candidate
        except Exception:
            # 开发机没有 CPython 3.8 运行时也能运行代理，只是会慢一些。
            _NATIVE_MOTION_STEP = None
    if _NATIVE_MOTION_STEP is not None:
        next_vx, next_vy, next_w = _NATIVE_MOTION_STEP(float(friction), float(vx), float(vy), float(w), STEP)
        return float(next_vx), float(next_vy), float(next_w)
    speed = newfrictionstep(friction, B2Vec2(vx, vy), w, STEP)
    return float(speed.v.x), float(speed.v.y), float(speed.angle)


@dataclass(frozen=True)
class Stone:
    """粗筛需要的最小局面信息；owner 只能是 self 或 opponent。"""

    index: int
    owner: str
    x: float
    y: float
    enabled: bool = True

    def __post_init__(self) -> None:
        if self.owner not in {"self", "opponent"}:
            raise ValueError("Stone.owner 必须是 self 或 opponent")


@dataclass(frozen=True)
class Shot:
    """比赛协议里的 BESTSHOT 三个输入。"""

    v0: float
    h0: float
    w0: float


@dataclass
class FreeSlidePrediction:
    """自由滑行阶段的预测；hit 后不继续伪造后续物理。"""

    shot: Shot
    first_hit_index: Optional[int]
    first_hit_owner: Optional[str]
    first_hit_point: Optional[Tuple[float, float]]
    incoming_velocity: Optional[Tuple[float, float]]
    entered_play: bool
    exits_play: bool
    stop_point: Tuple[float, float]
    ticks: int
    nearest_enemy_distance: float
    nearest_own_distance: float
    proxy_score: float = 0.0
    notes: Tuple[str, ...] = ()

    def to_json(self) -> dict:
        data = asdict(self)
        data["bestshot"] = [self.shot.v0, self.shot.h0, self.shot.w0]
        return data


def _segment_circle_fraction(
    start: Tuple[float, float], end: Tuple[float, float], center: Tuple[float, float], radius: float
) -> Optional[float]:
    """返回线段第一次进入圆盘的比例；没有相交时返回 None。"""

    sx, sy = start[0] - center[0], start[1] - center[1]
    dx, dy = end[0] - start[0], end[1] - start[1]
    a = dx * dx + dy * dy
    if a <= 1e-15:
        return 0.0 if sx * sx + sy * sy <= radius * radius else None
    c = sx * sx + sy * sy - radius * radius
    if c <= 0.0:
        return 0.0
    b = 2.0 * (sx * dx + sy * dy)
    discriminant = b * b - 4.0 * a * c
    if discriminant < 0.0:
        return None
    root = math.sqrt(discriminant)
    for t in ((-b - root) / (2.0 * a), (-b + root) / (2.0 * a)):
        if 0.0 <= t <= 1.0:
            return t
    return None


def _segment_distance(point: Tuple[float, float], start: Tuple[float, float], end: Tuple[float, float]) -> float:
    dx, dy = end[0] - start[0], end[1] - start[1]
    length_sq = dx * dx + dy * dy
    if length_sq <= 1e-15:
        return math.hypot(point[0] - start[0], point[1] - start[1])
    t = max(0.0, min(1.0, ((point[0] - start[0]) * dx + (point[1] - start[1]) * dy) / length_sq))
    return math.hypot(point[0] - (start[0] + t * dx), point[1] - (start[1] + t * dy))


def _nearest_boundary_direction(x: float, y: float) -> Tuple[float, float]:
    """从一颗目标壶指向最近边线的单位方向。"""

    candidates = (
        (x - PLAY_X_MIN, (-1.0, 0.0)),
        (PLAY_X_MAX - x, (1.0, 0.0)),
        (y - PLAY_Y_MIN, (0.0, -1.0)),
        (PLAY_Y_MAX - y, (0.0, 1.0)),
    )
    return min(candidates, key=lambda item: item[0])[1]


def predict_free_slide(
    shot: Shot,
    stones: Sequence[Stone],
    *,
    friction: float = BASE_FRICTION,
    max_ticks: int = 5000,
) -> FreeSlidePrediction:
    """推进无碰撞旋球，直到首次接触、停下或从比赛区出界。

    使用平均摩擦而非随机摩擦，正是它能很快粗筛的原因。最终 PhysX 阶段必须
    重新使用多条随机摩擦序列。
    """

    active = [stone for stone in stones if stone.enabled]
    state = local_initial_state(shot.v0, shot.h0, shot.w0)
    x, y, vx, vy, w = state.x, state.y, state.vx, state.vy, state.w
    entered_play = False
    nearest_enemy = math.inf
    nearest_own = math.inf

    for tick in range(1, max_ticks + 1):
        if math.hypot(vx, vy) <= 0.01:
            break
        previous = (x, y)
        vx, vy, w = _motion_step(friction, vx, vy, w)
        x += vx * UNITY_FIXED_TIMESTEP
        y += vy * UNITY_FIXED_TIMESTEP
        current = (x, y)
        entered_play = entered_play or y <= PLAY_Y_MAX

        first: Optional[Tuple[float, Stone]] = None
        for stone in active:
            distance = _segment_distance((stone.x, stone.y), previous, current)
            if stone.owner == "opponent":
                nearest_enemy = min(nearest_enemy, distance)
            else:
                nearest_own = min(nearest_own, distance)
            fraction = _segment_circle_fraction(previous, current, (stone.x, stone.y), CONTACT_DISTANCE)
            if fraction is not None and (first is None or fraction < first[0]):
                first = (fraction, stone)
        if first is not None:
            fraction, stone = first
            hit_point = (previous[0] + (current[0] - previous[0]) * fraction, previous[1] + (current[1] - previous[1]) * fraction)
            return FreeSlidePrediction(
                shot=shot,
                first_hit_index=stone.index,
                first_hit_owner=stone.owner,
                first_hit_point=hit_point,
                incoming_velocity=(vx, vy),
                entered_play=entered_play,
                exits_play=False,
                stop_point=hit_point,
                ticks=tick,
                nearest_enemy_distance=nearest_enemy,
                nearest_own_distance=nearest_own,
            )

        if entered_play and (x < PLAY_X_MIN or x > PLAY_X_MAX or y < PLAY_Y_MIN):
            return FreeSlidePrediction(
                shot=shot,
                first_hit_index=None,
                first_hit_owner=None,
                first_hit_point=None,
                incoming_velocity=None,
                entered_play=True,
                exits_play=True,
                stop_point=current,
                ticks=tick,
                nearest_enemy_distance=nearest_enemy,
                nearest_own_distance=nearest_own,
            )

    return FreeSlidePrediction(
        shot=shot,
        first_hit_index=None,
        first_hit_owner=None,
        first_hit_point=None,
        incoming_velocity=None,
        entered_play=entered_play,
        exits_play=False,
        stop_point=(x, y),
        ticks=tick if "tick" in locals() else 0,
        nearest_enemy_distance=nearest_enemy,
        nearest_own_distance=nearest_own,
    )


def score_attack_prediction(prediction: FreeSlidePrediction, stones: Sequence[Stone]) -> FreeSlidePrediction:
    """给 P1 粗筛用的保守评分，不预测碰后具体落点。

    分高只代表“值得交给严格 PhysX 再算”，不代表可以直接出手。
    """

    notes: List[str] = []
    score = 0.0
    by_index = {stone.index: stone for stone in stones if stone.enabled}
    if prediction.first_hit_owner == "opponent" and prediction.first_hit_index is not None:
        score += 100.0
        notes.append("首撞敌方")
        target = by_index[prediction.first_hit_index]
        assert prediction.incoming_velocity is not None
        speed = math.hypot(*prediction.incoming_velocity)
        if speed > 1e-9:
            direction = (prediction.incoming_velocity[0] / speed, prediction.incoming_velocity[1] / speed)
            to_edge = _nearest_boundary_direction(target.x, target.y)
            alignment = direction[0] * to_edge[0] + direction[1] * to_edge[1]
            score += 20.0 * alignment
            notes.append("传力朝边线" if alignment > 0.35 else "传力不朝边线")
    elif prediction.first_hit_owner == "self":
        score -= 150.0
        notes.append("先撞己方，剔除")
    elif prediction.exits_play:
        score -= 60.0
        notes.append("出手壶自由滑行出界")
    else:
        # 没撞到敌壶也保留一个很低分，供调用方了解是“差一点”还是“完全不沾边”。
        score -= min(50.0, prediction.nearest_enemy_distance * 10.0)
        notes.append("未命中敌方")

    # 即使首撞敌方，路线若非常贴近己方，也标为风险，不直接淘汰。
    if prediction.nearest_own_distance < CONTACT_DISTANCE + 0.04:
        score -= 30.0
        notes.append("贴近己方，有随机摩擦风险")

    prediction.proxy_score = score
    prediction.notes = tuple(notes)
    return prediction


def rank_attack_candidates(shots: Iterable[Shot], stones: Sequence[Stone]) -> List[FreeSlidePrediction]:
    """按“值得严格复核”的优先级排序所有候选。"""

    ranked = [score_attack_prediction(predict_free_slide(shot, stones), stones) for shot in shots]
    ranked.sort(key=lambda item: item.proxy_score, reverse=True)
    return ranked


def regular_shot_grid(
    *,
    velocities: Sequence[float] = (3.6, 4.4, 5.2),
    horizontal_offsets: Sequence[float] = tuple(-2.2 + 0.44 * i for i in range(11)),
    rotations: Sequence[float] = (-12.0, -6.0, 0.0, 6.0, 12.0),
) -> Iterable[Shot]:
    """165 条确定性种子路线；P2 再在其中少数路线附近用严格 PhysX 密搜。

    这里刻意不铺上千条路线：粗筛阶段要留出时间给严格 PhysX。范围和密度可
    在固定基准上调整，但每一轮的种子网格都必须记录进报告，保证可复现。
    """

    for v0 in velocities:
        for h0 in horizontal_offsets:
            for w0 in rotations:
                yield Shot(float(v0), float(h0), float(w0))
