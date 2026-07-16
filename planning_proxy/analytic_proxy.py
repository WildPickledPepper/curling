#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""连续、低阶、白盒的自由滑行粗代理。

代理不调用 PhysX，也不调用昂贵的逐 tick 数值积分。它用三个可解释参数近似
自由滑行：纵向减速度、旋转衰减率、旋转造成的转向率。参数由恢复出的
Newfrictionstep 在少量代表状态上即时标定，之后可批量推进任意连续的出手参数。

这是筛选器，不是严格模拟器：一旦路径可能首撞任一壶，就停止在接触前，交给
严格 PhysX 计算真实碰撞链和终局。
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence, Tuple

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FORCE_LOOKUP_ASSET = Path(__file__).resolve().parent / "assets" / "recovered_formula_force_lookup_compact_v1.npz"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
RUNTIME_SUPPORT_ROOT = PROJECT_ROOT / "local_simulator" / "runtime_support"
if str(RUNTIME_SUPPORT_ROOT) not in sys.path:
    sys.path.insert(0, str(RUNTIME_SUPPORT_ROOT))

from tools.reverse.front_half_pcm_replay import FORMAL_STONE_RADIUS, UNITY_FIXED_TIMESTEP  # noqa: E402
from tools.reverse.recovered_curling_motion import BASE_FRICTION, STEP  # noqa: E402
from tools.reverse.replay_bestshot_seeded import DEFAULT_RELEASE_X, DEFAULT_RELEASE_Y  # noqa: E402


PLAY_X_MIN, PLAY_X_MAX = 0.145, 4.605
PLAY_Y_MIN, PLAY_Y_MAX = 2.865, 10.525
CONTACT_DISTANCE = 2.0 * FORMAL_STONE_RADIUS + 0.02


@dataclass(frozen=True)
class ProxyStone:
    index: int
    owner: str  # self / opponent
    x: float
    y: float


@dataclass(frozen=True)
class AnalyticParameters:
    drag_floor_mps2: float
    drag_quadratic_per_m: float
    spin_decay_per_s: float
    curl_turn_per_m_per_spin: float


@dataclass(frozen=True)
class ForceLookup:
    """恢复公式的小型白盒受力表，不是学习得到的神经网络。

    每个格点直接调用一次 ``Newfrictionstep``，记录该状态下的减速、转向、
    旋转衰减；粗代理运行时只做双线性插值。这样保留速度段/旋转段的非线性，
    又不在每条候选路径的每一小步跨 Python 调用原生扩展。
    """

    speed_nodes: np.ndarray
    spin_nodes: np.ndarray
    drag_mps2: np.ndarray
    turn_rate_radps: np.ndarray
    spin_decay_per_s: np.ndarray

    def metadata(self) -> dict:
        return {
            "kind": "recovered_formula_force_lookup_v1",
            "speedNodeCount": int(len(self.speed_nodes)),
            "spinNodeCount": int(len(self.spin_nodes)),
            "speedRangeMps": [float(self.speed_nodes[0]), float(self.speed_nodes[-1])],
            "spinRange": [float(self.spin_nodes[0]), float(self.spin_nodes[-1])],
        }


@dataclass
class BatchPrediction:
    shots: np.ndarray
    first_hit_index: np.ndarray
    first_hit_owner: np.ndarray
    exits_play: np.ndarray
    stop_points: np.ndarray
    nearest_enemy: np.ndarray
    nearest_own: np.ndarray


def calibrate_from_recovered_formula() -> AnalyticParameters:
    """用 18 个代表状态把低阶模型贴到当前恢复公式的一阶局部行为上。

    这不是训练黑箱网络；三个量都有明确物理含义，并且每次改动恢复公式后都可
    立即重新标定。这里只调用少量 Newfrictionstep，不创建 PhysX Scene。
    """

    try:
        from local_simulator.runtime_loader import install_bundled_pyphysx

        install_bundled_pyphysx()
        import pyphysx  # type: ignore
    except Exception as exc:
        raise RuntimeError("需要项目随包的 CPython 3.8 / pyphysx 来标定粗代理") from exc

    drag_speeds: List[float] = []
    drags: List[float] = []
    decays: List[float] = []
    curls: List[float] = []
    for speed in (3.2, 4.2, 5.2):
        for spin in (-15.0, -10.0, -5.0, 5.0, 10.0, 15.0):
            next_vx, next_vy, next_w = pyphysx.curling_new_friction_step(
                float(BASE_FRICTION), 0.0, -float(speed), float(spin), float(STEP)
            )
            next_speed = math.hypot(float(next_vx), float(next_vy))
            # Newfrictionstep 的参数 STEP=0.001，但它内部乘以 10/20 后，
            # Unity/本地 Scene 实际是每 0.01 秒才用新速度推进一次位置。
            # 粗代理的时间单位必须与位置积分的 0.01 秒保持一致。
            drags.append(max(0.0, (speed - next_speed) / UNITY_FIXED_TIMESTEP))
            drag_speeds.append(speed)
            decays.append(max(0.0, -math.log(max(abs(float(next_w)), 1e-9) / abs(spin)) / UNITY_FIXED_TIMESTEP))
            # dvx/speed 是小角度转向率；再除 spin 得每单位旋转的曲率。
            curls.append(float(next_vx) / (UNITY_FIXED_TIMESTEP * speed * spin))
    # 已恢复公式在可达速度范围内呈现明显的速度平方阻力。用 a0+a2*v²
    # 代替“恒定减速度”，可避免高速段过早停下、低速段又滑得过远。
    design = np.column_stack((np.ones(len(drag_speeds)), np.square(drag_speeds)))
    drag_floor, drag_quadratic = np.linalg.lstsq(design, np.asarray(drags), rcond=None)[0]
    return AnalyticParameters(
        drag_floor_mps2=max(0.0, float(drag_floor)),
        drag_quadratic_per_m=max(0.0, float(drag_quadratic)),
        spin_decay_per_s=float(np.median(decays)),
        curl_turn_per_m_per_spin=float(np.median(curls)),
    )


def calibrate_force_lookup(
    *, speed_nodes: np.ndarray | None = None, spin_nodes: np.ndarray | None = None,
    prefer_packaged: bool = True,
) -> ForceLookup:
    """从恢复出的公式建立小型速度×旋转受力表。

    表只在一次规划的开始创建；之后所有候选共用，不随候选数量线性增加原生
    调用次数。正旋/负旋由对称性共用同一张“绝对旋转量”表，运行时恢复符号。
    """

    # 默认表是由本函数对当前恢复公式离线生成的确定性资产。它不是拟合模型，
    # 只避免在比赛服务器重复做 140 次昂贵的公式积分。传入自定义节点或显式
    # 关闭 prefer_packaged 时，仍会现场重新生成，便于反推公式变更后的开发校验。
    if prefer_packaged and speed_nodes is None and spin_nodes is None and DEFAULT_FORCE_LOOKUP_ASSET.is_file():
        with np.load(DEFAULT_FORCE_LOOKUP_ASSET) as archive:
            return ForceLookup(
                archive["speed_nodes"].astype(np.float32),
                archive["spin_nodes"].astype(np.float32),
                archive["drag_mps2"].astype(np.float32),
                archive["turn_rate_radps"].astype(np.float32),
                archive["spin_decay_per_s"].astype(np.float32),
            )
    try:
        from local_simulator.runtime_loader import install_bundled_pyphysx

        install_bundled_pyphysx()
        import pyphysx  # type: ignore
    except Exception as exc:
        raise RuntimeError("需要项目随包的 CPython 3.8 / pyphysx 来标定粗代理") from exc
    # 速度 1.0/1.5 是恢复公式切换分段的边界，必须显式保留；其余节点把
    # 低速、常用速度和高速段分开即可。140 格相比原先 825 格把冷启动压低，
    # 同时不跨越这两个物理分段硬插值。
    speeds = np.asarray(
        (0.05, 0.30, 0.50, 0.75, 1.00, 1.25, 1.50, 2.00, 2.50, 3.00, 3.80, 4.60, 5.30, 6.00)
        if speed_nodes is None else speed_nodes,
        dtype=np.float32,
    )
    spins = np.asarray(
        (0.01, 0.10, 0.50, 1.50, 3.00, 5.00, 7.50, 10.00, 13.00, 16.00)
        if spin_nodes is None else spin_nodes,
        dtype=np.float32,
    )
    drag = np.empty((len(speeds), len(spins)), dtype=np.float32)
    turn = np.empty_like(drag)
    spin_decay = np.empty_like(drag)
    for speed_index, speed in enumerate(speeds):
        for spin_index, spin in enumerate(spins):
            next_vx, next_vy, next_spin = pyphysx.curling_new_friction_step(
                float(BASE_FRICTION), 0.0, -float(speed), float(spin), float(STEP)
            )
            next_speed = math.hypot(float(next_vx), float(next_vy))
            next_heading = math.atan2(float(next_vy), float(next_vx))
            # 初始朝向固定为 -pi/2；这一项是“每秒拐多少弯”，而非全局位置。
            delta_heading = (next_heading + math.pi / 2.0 + math.pi) % (2.0 * math.pi) - math.pi
            drag[speed_index, spin_index] = max(0.0, (float(speed) - next_speed) / UNITY_FIXED_TIMESTEP)
            turn[speed_index, spin_index] = delta_heading / UNITY_FIXED_TIMESTEP
            spin_decay[speed_index, spin_index] = max(0.0, (float(spin) - float(next_spin)) / UNITY_FIXED_TIMESTEP)
    return ForceLookup(speeds, spins, drag, turn, spin_decay)


def _lookup_bilinear(table: np.ndarray, speeds: np.ndarray, spins: np.ndarray, lookup: ForceLookup) -> np.ndarray:
    """对同一批候选按速度与绝对旋转量双线性插值。"""

    x = np.clip(speeds, lookup.speed_nodes[0], lookup.speed_nodes[-1])
    y = np.clip(spins, lookup.spin_nodes[0], lookup.spin_nodes[-1])
    ix_hi = np.searchsorted(lookup.speed_nodes, x, side="right")
    iy_hi = np.searchsorted(lookup.spin_nodes, y, side="right")
    ix_hi = np.clip(ix_hi, 1, len(lookup.speed_nodes) - 1)
    iy_hi = np.clip(iy_hi, 1, len(lookup.spin_nodes) - 1)
    ix_lo, iy_lo = ix_hi - 1, iy_hi - 1
    x0, x1 = lookup.speed_nodes[ix_lo], lookup.speed_nodes[ix_hi]
    y0, y1 = lookup.spin_nodes[iy_lo], lookup.spin_nodes[iy_hi]
    tx = (x - x0) / np.maximum(x1 - x0, 1e-9)
    ty = (y - y0) / np.maximum(y1 - y0, 1e-9)
    return (
        (1.0 - tx) * (1.0 - ty) * table[ix_lo, iy_lo]
        + tx * (1.0 - ty) * table[ix_hi, iy_lo]
        + (1.0 - tx) * ty * table[ix_lo, iy_hi]
        + tx * ty * table[ix_hi, iy_hi]
    )


def make_initial_candidates(
    *, velocity_count: int = 5, lateral_count: int = 25, spin_count: int = 9,
) -> np.ndarray:
    """首轮做连续空间覆盖；后续只在命中的区域局部细分。

    三个计数被显式暴露给调用方，便于在比赛的单核时间预算内扩大粗筛。
    它们不改变输入范围，只是把速度、横向偏移和旋转的网格切得更细。
    """

    if min(int(velocity_count), int(lateral_count), int(spin_count)) < 1:
        raise ValueError("初筛的速度、横向、旋转档数都必须至少为 1")
    return np.asarray(
        [
            (float(v0), float(h0), float(w0))
            for v0 in np.linspace(3.2, 5.6, int(velocity_count))
            for h0 in np.linspace(-2.2, 2.2, int(lateral_count))
            for w0 in np.linspace(-15.0, 15.0, int(spin_count))
        ],
        dtype=np.float32,
    )


def refine_candidates(parents: np.ndarray, *, dv: float = 0.12, dh: float = 0.10, dw: float = 1.2) -> np.ndarray:
    rows: List[Tuple[float, float, float]] = []
    seen = set()
    for v0, h0, w0 in parents:
        for delta_v in (-dv, 0.0, dv):
            for delta_h in (-dh, 0.0, dh):
                for delta_w in (-dw, 0.0, dw):
                    item = (
                        max(1.0, min(6.0, float(v0 + delta_v))),
                        max(-2.23, min(2.23, float(h0 + delta_h))),
                        max(-15.7, min(15.7, float(w0 + delta_w))),
                    )
                    key = tuple(round(value, 6) for value in item)
                    if key not in seen:
                        seen.add(key)
                        rows.append(item)
    return np.asarray(rows, dtype=np.float32)


def simulate_batch(
    shots: np.ndarray,
    stones: Sequence[ProxyStone],
    params: AnalyticParameters,
    *,
    force_lookup: ForceLookup | None = None,
    dt: float = 0.05,
    max_time: float = 48.0,
    stop_speed_mps: float = 0.01,
) -> BatchPrediction:
    """批量推进低阶方程，并以扫掠圆盘检测首次可能接触。"""

    count = len(shots)
    centers = np.asarray([(stone.x, stone.y) for stone in stones], dtype=np.float32).reshape((-1, 2))
    owners = np.asarray([stone.owner for stone in stones], dtype=object)
    indexes = np.asarray([stone.index for stone in stones], dtype=np.int32)
    enemy_columns = np.asarray([owner == "opponent" for owner in owners], dtype=bool)
    own_columns = np.asarray([owner == "self" for owner in owners], dtype=bool)

    x = np.full(count, DEFAULT_RELEASE_X, dtype=np.float32) + shots[:, 1]
    y = np.full(count, DEFAULT_RELEASE_Y, dtype=np.float32)
    speed = shots[:, 0].astype(np.float32).copy()
    heading = np.full(count, -math.pi / 2.0, dtype=np.float32)
    spin = shots[:, 2].astype(np.float32).copy()
    active = np.ones(count, dtype=bool)
    entered = np.zeros(count, dtype=bool)
    exits = np.zeros(count, dtype=bool)
    first_hit = np.full(count, -1, dtype=np.int32)
    first_owner = np.full(count, "", dtype=object)
    nearest_enemy = np.full(count, np.inf, dtype=np.float32)
    nearest_own = np.full(count, np.inf, dtype=np.float32)

    spin_decay = math.exp(-params.spin_decay_per_s * dt)
    for _step in range(int(math.ceil(max_time / dt))):
        rows = np.flatnonzero(active)
        if not len(rows):
            break
        old_x, old_y = x[rows].copy(), y[rows].copy()
        # 半隐式推进：先让旋转衰减和方向弯曲，再更新速度和位置。
        # 有白盒受力表时，三项均按当前速度和旋转插值；否则保留旧的四常数近似。
        if force_lookup is None:
            spin[rows] *= spin_decay
            heading[rows] += params.curl_turn_per_m_per_spin * spin[rows] * dt
            drag = params.drag_floor_mps2 + params.drag_quadratic_per_m * np.square(speed[rows])
        else:
            abs_spin = np.abs(spin[rows])
            signs = np.where(spin[rows] < 0.0, -1.0, 1.0)
            local_drag = _lookup_bilinear(force_lookup.drag_mps2, speed[rows], abs_spin, force_lookup)
            local_turn = _lookup_bilinear(force_lookup.turn_rate_radps, speed[rows], abs_spin, force_lookup)
            local_spin_decay = _lookup_bilinear(force_lookup.spin_decay_per_s, speed[rows], abs_spin, force_lookup)
            spin[rows] -= signs * local_spin_decay * dt
            # 恢复公式在极小旋转下会使用极小的正回退量；粗代理保留当前旋转符号，
            # 但不允许在一个步长内穿过零而反向。
            spin[rows] = signs * np.maximum(0.01, np.abs(spin[rows]))
            heading[rows] += signs * local_turn * dt
            drag = local_drag
        speed[rows] = np.maximum(0.0, speed[rows] - drag * dt)
        x[rows] += np.cos(heading[rows]) * speed[rows] * dt
        y[rows] += np.sin(heading[rows]) * speed[rows] * dt
        entered[rows] |= y[rows] <= PLAY_Y_MAX

        start = np.stack((old_x, old_y), axis=1)
        end = np.stack((x[rows], y[rows]), axis=1)
        delta = end - start
        length_sq = np.maximum(np.sum(delta * delta, axis=1, keepdims=True), 1e-12)
        relative = centers[None, :, :] - start[:, None, :]
        fraction = np.clip(np.sum(relative * delta[:, None, :], axis=2) / length_sq, 0.0, 1.0)
        closest = start[:, None, :] + fraction[:, :, None] * delta[:, None, :]
        distance = np.sqrt(np.sum((closest - centers[None, :, :]) ** 2, axis=2))
        if np.any(enemy_columns):
            nearest_enemy[rows] = np.minimum(nearest_enemy[rows], np.min(distance[:, enemy_columns], axis=1))
        if np.any(own_columns):
            nearest_own[rows] = np.minimum(nearest_own[rows], np.min(distance[:, own_columns], axis=1))
        hit = np.any(distance <= CONTACT_DISTANCE, axis=1)
        if np.any(hit):
            local_rows = np.flatnonzero(hit)
            columns = np.argmin(distance[local_rows], axis=1)
            global_rows = rows[local_rows]
            first_hit[global_rows] = indexes[columns]
            first_owner[global_rows] = owners[columns]
            active[global_rows] = False

        still_rows = rows[active[rows]]
        out = entered[still_rows] & (
            (x[still_rows] < PLAY_X_MIN) | (x[still_rows] > PLAY_X_MAX) | (y[still_rows] < PLAY_Y_MIN)
        )
        if np.any(out):
            out_rows = still_rows[np.flatnonzero(out)]
            exits[out_rows] = True
            active[out_rows] = False
        # 不能为了省几十个粗代理步而在 0.35 m/s 提前停下：慢速旋进路线
        # 仍可能在后半段贴到守壶。对照恢复公式同样以 0.01 m/s 为终止量级。
        active[still_rows[speed[still_rows] <= stop_speed_mps]] = False

    return BatchPrediction(
        shots=shots.copy(), first_hit_index=first_hit, first_hit_owner=first_owner,
        exits_play=exits, stop_points=np.stack((x, y), axis=1),
        nearest_enemy=nearest_enemy, nearest_own=nearest_own,
    )


def attack_score(
    prediction: BatchPrediction,
    *,
    protected_opponent_indices: Sequence[int] = (),
    must_clear_index: int | None = None,
    chain_entry_indices: Sequence[int] = (),
) -> np.ndarray:
    score = -np.minimum(prediction.nearest_enemy * 10.0, 50.0)
    score[prediction.first_hit_owner == "opponent"] += 100.0
    score[prediction.first_hit_owner == "self"] -= 150.0
    score[prediction.exits_play] -= 60.0
    score[prediction.nearest_own < CONTACT_DISTANCE + 0.04] -= 30.0
    # 前五手的对方自由防守区壶不能作为攻击目标。粗代理的首撞判断有近似误差，
    # 因此这里只做极强降级、而不物理删除候选；最终是否犯规仍由严格 PhysX 的
    # 多摩擦序列规则检查决定，避免误伤一条实际上只是擦边且最终合法的路线。
    if protected_opponent_indices:
        protected = np.isin(prediction.first_hit_index, np.asarray(tuple(protected_opponent_indices), dtype=np.int32))
        score[protected] -= 10000.0
    # 指定“必须清出界”的目标敌壶时，直接首撞目标优先；若目标被己方壶遮住，
    # 则也保留“先撞紧邻目标的己方壶”的连锁入射种子，交给严格 PhysX 判断是否
    # 真能完成一撞/二撞，而不是被普通的“先撞己方”规则提前删掉。
    if must_clear_index is not None:
        score[prediction.first_hit_index == int(must_clear_index)] += 20000.0
        if chain_entry_indices:
            chain = np.isin(prediction.first_hit_index, np.asarray(tuple(chain_entry_indices), dtype=np.int32))
            score[chain] += 500.0
    return score


def conservative_parent_indices(
    prediction: BatchPrediction,
    *,
    risk_radius_m: float = 0.45,
    minimum_count: int = 48,
    protected_opponent_indices: Sequence[int] = (),
    must_clear_index: int | None = None,
    chain_entry_indices: Sequence[int] = (),
) -> np.ndarray:
    """保守地选择要局部细分的连续参数区域。

    不能只保留“粗代理已经判为撞到敌壶”的路线，否则近似误差会漏掉窄缝。
    任何距敌壶不超过 risk_radius_m 的路径都保留；若数量不足，再按攻击评分
    补足。这个函数允许假阳性，但目标是不漏掉值得严格 PhysX 复核的路线。
    """

    score = attack_score(
        prediction, protected_opponent_indices=protected_opponent_indices,
        must_clear_index=must_clear_index, chain_entry_indices=chain_entry_indices,
    )
    near_enemy = np.flatnonzero(prediction.nearest_enemy <= float(risk_radius_m))
    order = np.argsort(-score)
    selected: List[int] = []
    seen = set()
    # 先取风险通道；按离敌方最近优先，以控制后续严格搜索规模。
    for index in near_enemy[np.argsort(prediction.nearest_enemy[near_enemy])]:
        value = int(index)
        if value not in seen:
            seen.add(value)
            selected.append(value)
    for index in order:
        value = int(index)
        if len(selected) >= minimum_count:
            break
        if value not in seen:
            seen.add(value)
            selected.append(value)
    return np.asarray(selected, dtype=np.int32)
