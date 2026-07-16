#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""严格 PhysX 检查：中线守壶能替后方错层得分壶挡住多少对方撞击。

这不是末手“能否赢分”的验证，而是专门回答一个更基础的问题：对方攻击中线
守壶后方、靠近大本营的己方壶时，能把它们撞到什么程度。

默认保留白盒粗筛中能直接碰到后方壶、以及先碰中线守壶的两类父路线；之后
每条父路线在严格 PhysX 中展开 3×3×3 局部参数，并跨多条摩擦序列回放。输出会分别报告：

* 后方壶最少还能留下几颗；
* 任一后方壶最大位移；
* 后方壶离开大本营、离开内圈、物理出界各发生多少次；
* 哪条对方输入造成最坏结果。

它是“中线守壶作为缓冲层”的压力测试；不取代全局对局验证，也不声称遍历了
连续输入空间。
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import (  # noqa: E402
    HOUSE_R, HOUSE_X, HOUSE_Y, STONE_R, StrictCurlingEnd,
)
from local_simulator.runtime_loader import install_bundled_pyphysx  # noqa: E402
from planning_proxy.analytic_proxy import (  # noqa: E402
    ProxyStone, calibrate_force_lookup, calibrate_from_recovered_formula,
    make_initial_candidates, simulate_batch,
)
from planning_proxy.strict_refine import Candidate, local_candidates_for_parent  # noqa: E402


GUARD = (2.375, 7.150)
INNER_R = 0.610 + STONE_R
ACTIVE_INDEX = 15


@dataclass(frozen=True)
class ShieldFixture:
    name: str
    description: str
    # Guard is slot 1; the two rear stones are slots 3 and 5.  The active
    # opponent stone uses slot 15, so no historical identity is overwritten.
    stones: tuple[tuple[int, float, float], ...]

    @property
    def guard_index(self) -> int:
        return 1

    @property
    def rear_indices(self) -> tuple[int, ...]:
        return tuple(index for index, _x, _y in self.stones if index != self.guard_index)


FIXTURES: dict[str, ShieldFixture] = {
    "保护期_中线后方单红圈": ShieldFixture(
        "保护期_中线后方单红圈",
        "我方第二颗已停在中线守壶后方红圈；对应全局第 4 手、保护期仍有效时，对方试图绕过守壶直接攻击它。",
        ((1, *GUARD), (3, 2.280, 4.700)),
    ),
    "保护期_中线后方单红圈_镜像": ShieldFixture(
        "保护期_中线后方单红圈_镜像",
        "上述局面的左右镜像，避免把单侧绕壶难度误当成普遍结论。",
        ((1, *GUARD), (3, 2.470, 4.700)),
    ),
    "中线后方双红圈": ShieldFixture(
        "中线后方双红圈",
        "中线守壶后方是一对左右、前后错开的红圈壶；对应当前先手策略的左布局。",
        ((1, *GUARD), (3, 2.280, 4.700), (5, 2.670, 5.180)),
    ),
    "中线后方双红圈_镜像": ShieldFixture(
        "中线后方双红圈_镜像",
        "与“中线后方双红圈”左右镜像；用于避免只在单侧得到结论。",
        ((1, *GUARD), (3, 2.470, 4.700), (5, 2.080, 5.180)),
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", choices=tuple(FIXTURES), action="append", default=None)
    parser.add_argument("--parent-count", type=int, default=12, help="保留多少条粗筛中可直击后方或先碰守壶的父路线。")
    parser.add_argument("--physics-seeds", type=int, default=3, help="每条严格候选使用几条摩擦序列。")
    parser.add_argument("--seed", type=int, default=20260716)
    parser.add_argument(
        "--shot-index", type=int, default=5,
        help="对方从第六次全局投壶起可正常清中线守壶；默认 5。若填 1 或 3，会额外标出自由防守区违规路线。",
    )
    parser.add_argument(
        "--output", type=Path,
        default=ROOT / "planning_proxy" / "runs" / "centre_guard_shield_stress.json",
    )
    return parser.parse_args()


def _representative_rows(prediction, indices: np.ndarray, *, limit: int) -> list[dict[str, Any]]:
    """从一类粗筛命中里抽横向/旋转不同的代表父路线。"""

    ordered = indices[np.argsort(prediction.nearest_enemy[indices])]
    rows: list[dict[str, Any]] = []
    bins: set[tuple[int, int]] = set()
    for index in ordered:
        v0, h0, w0 = (float(value) for value in prediction.shots[int(index)])
        key = (round(h0 / 0.12), 1 if w0 >= 0.0 else -1)
        if key in bins and len(rows) < max(2, limit // 2):
            continue
        bins.add(key)
        rows.append({"bestshot": [v0, h0, w0]})
        if len(rows) >= limit:
            break
    return rows


def _parents_that_can_hit_rear(fixture: ShieldFixture, *, params, lookup, count: int) -> tuple[list[dict[str, Any]], dict[str, int]]:
    # 从攻击方视角，场上的我方壶均视为 opponent。这里不要预设“中线守壶
    # 一定先被撞”：对方也可能绕过它，直接攻击后方红圈壶。
    proxy_board = [ProxyStone(index, "opponent", x, y) for index, x, y in fixture.stones]
    prediction = simulate_batch(make_initial_candidates(), proxy_board, params, force_lookup=lookup, dt=0.02)
    rear_hits = np.flatnonzero(np.isin(prediction.first_hit_index, np.asarray(fixture.rear_indices, dtype=np.int32)))
    guard_hits = np.flatnonzero(prediction.first_hit_index == fixture.guard_index)
    if not len(rear_hits) and not len(guard_hits):
        raise RuntimeError("粗筛未找到可接近后方壶或中线守壶的路线；请检查坐标或代理参数")

    # 两类路线都留：直接绕过守壶打后方，以及先撞守壶后可能形成的传力链。
    rear_limit = max(1, (count + 1) // 2)
    guard_limit = max(1, count - rear_limit)
    rows = _representative_rows(prediction, rear_hits, limit=rear_limit) if len(rear_hits) else []
    existing = {tuple(round(float(value), 6) for value in row["bestshot"]) for row in rows}
    for row in (_representative_rows(prediction, guard_hits, limit=guard_limit) if len(guard_hits) else []):
        key = tuple(round(float(value), 6) for value in row["bestshot"])
        if key not in existing:
            existing.add(key)
            rows.append(row)
    # 某一类去重后不足时，从另一类补齐。
    for group in (rear_hits, guard_hits):
        for row in (_representative_rows(prediction, group, limit=count) if len(group) else []):
            key = tuple(round(float(value), 6) for value in row["bestshot"])
            if key not in existing:
                existing.add(key)
                rows.append(row)
            if len(rows) >= count:
                break
        if len(rows) >= count:
            break
    return rows, {
        "coarseCandidateCount": int(len(prediction.shots)),
        "coarseFirstHitRearCount": int(len(rear_hits)),
        "coarseFirstHitGuardCount": int(len(guard_hits)),
        "parentCount": int(len(rows)),
    }


def _position(fixture: ShieldFixture) -> list[float]:
    values = [0.0] * 32
    for index, x, y in fixture.stones:
        values[2 * index] = float(x)
        values[2 * index + 1] = float(y)
    return values


def _initial_by_index(fixture: ShieldFixture) -> dict[int, tuple[float, float]]:
    return {index: (x, y) for index, x, y in fixture.stones}


def _is_free_guard_legal_for_guard(state: dict[str, Any]) -> bool:
    if not bool(state.get("enabled", False)):
        return False
    x, y = float(state["x"]), float(state["y"])
    # Guard must remain on centre line, inside free guard zone, and fully outside house.
    return abs(x - HOUSE_X) <= STONE_R + 1e-6 and y >= HOUSE_Y - 1e-6 and math.hypot(x - HOUSE_X, y - HOUSE_Y) > HOUSE_R + STONE_R


def _simulate_candidate(
    environment: StrictCurlingEnd,
    fixture: ShieldFixture,
    candidate: Candidate,
    *,
    physics_seed: int,
    shot_index: int,
) -> dict[str, Any]:
    # The attacker uses slot 15. Old self stones keep their slots/yaw=0.
    environment.seed = int(physics_seed) - ACTIVE_INDEX * 7919
    environment.scene.reset_positions(_position(fixture), yaw_overrides={index: 0.0 for index in range(16)})
    environment.shot_number = ACTIVE_INDEX
    result = environment.play((candidate.v0, candidate.h0, candidate.w0))
    states = result["states"]
    guard_state = states[fixture.guard_index]
    legal = True if shot_index > 4 else _is_free_guard_legal_for_guard(guard_state)
    initial = _initial_by_index(fixture)
    rear: list[dict[str, Any]] = []
    for index in fixture.rear_indices:
        state = states[index]
        enabled = bool(state.get("enabled", False))
        if enabled:
            distance = math.hypot(float(state["x"]) - HOUSE_X, float(state["y"]) - HOUSE_Y)
            displacement = math.hypot(float(state["x"]) - initial[index][0], float(state["y"]) - initial[index][1])
        else:
            distance = None
            displacement = None
        rear.append({
            "index": index,
            "enabled": enabled,
            "x": None if not enabled else float(state["x"]),
            "y": None if not enabled else float(state["y"]),
            "distanceToCentreM": distance,
            "displacementM": displacement,
            "inHouse": bool(enabled and distance is not None and distance <= HOUSE_R + STONE_R),
            "inInnerRing": bool(enabled and distance is not None and distance <= INNER_R),
        })
    return {
        "legal": legal,
        "contact": bool(result.get("contact", False)),
        "firstContactTargets": [int(index) for index in result.get("firstContactTargets", [])],
        "clearedSlots": [int(value) for value in result.get("cleared", [])],
        "rear": rear,
        "guard": {
            "enabled": bool(guard_state.get("enabled", False)),
            "x": None if not bool(guard_state.get("enabled", False)) else float(guard_state["x"]),
            "y": None if not bool(guard_state.get("enabled", False)) else float(guard_state["y"]),
            "legalInProtectedPeriod": _is_free_guard_legal_for_guard(guard_state),
        },
    }


def _compact_outcome(outcome: dict[str, Any]) -> dict[str, Any]:
    return {
        "legal": outcome["legal"],
        "firstContactTargets": outcome["firstContactTargets"],
        "clearedSlots": outcome["clearedSlots"],
        "guard": outcome["guard"],
        "rear": outcome["rear"],
    }


def run_fixture(
    fixture: ShieldFixture, *, params, lookup, environment: StrictCurlingEnd,
    seeds: Iterable[int], parent_count: int, shot_index: int,
) -> dict[str, Any]:
    started = time.perf_counter()
    rows, coarse = _parents_that_can_hit_rear(fixture, params=params, lookup=lookup, count=parent_count)
    seen: set[tuple[float, float, float]] = set()
    cases: list[dict[str, Any]] = []
    for parent_rank, row in enumerate(rows, 1):
        for candidate in local_candidates_for_parent(row, parent_rank, seen):
            outcomes = [
                _simulate_candidate(environment, fixture, candidate, physics_seed=int(seed), shot_index=shot_index)
                for seed in seeds
            ]
            legal_outcomes = [outcome for outcome in outcomes if outcome["legal"]]
            # 一条只在幸运摩擦序列中不犯规的路线，不应被当成“对方可稳定
            # 使用的合法反击”。保护期检查时要求每条复核序列都合法。
            if len(legal_outcomes) != len(outcomes):
                continue
            rear_remaining = [sum(bool(item["enabled"]) for item in outcome["rear"]) for outcome in legal_outcomes]
            rear_in_house = [sum(bool(item["inHouse"]) for item in outcome["rear"]) for outcome in legal_outcomes]
            rear_in_inner = [sum(bool(item["inInnerRing"]) for item in outcome["rear"]) for outcome in legal_outcomes]
            displacements = [
                float(item["displacementM"])
                for outcome in legal_outcomes for item in outcome["rear"]
                if item["displacementM"] is not None
            ]
            cases.append({
                "bestshot": [candidate.v0, candidate.h0, candidate.w0],
                "parentRank": candidate.parent_rank,
                "legalSeedCount": len(legal_outcomes),
                "rearRemainingByLegalSeed": rear_remaining,
                "rearInHouseByLegalSeed": rear_in_house,
                "rearInInnerRingByLegalSeed": rear_in_inner,
                "worstRearRemaining": min(rear_remaining),
                "worstRearInHouse": min(rear_in_house),
                "worstRearInInnerRing": min(rear_in_inner),
                "maxRearDisplacementM": max(displacements, default=None),
                "outcomes": [_compact_outcome(outcome) for outcome in outcomes],
            })
    # “清后方壶多”是最坏，其次“仍在场但离开大本营多”，再比较最大位移。
    cases.sort(key=lambda row: (
        int(row["worstRearRemaining"]),
        int(row["worstRearInHouse"]),
        int(row["worstRearInInnerRing"]),
        -(float(row["maxRearDisplacementM"]) if row["maxRearDisplacementM"] is not None else 99.0),
    ))
    worst = cases[0] if cases else None
    return {
        "fixture": fixture.name,
        "description": fixture.description,
        "initialGuard": {"index": fixture.guard_index, "x": GUARD[0], "y": GUARD[1]},
        "initialRearStones": [
            {"index": index, "x": x, "y": y}
            for index, x, y in fixture.stones if index != fixture.guard_index
        ],
        "shotIndex": shot_index,
        "scope": "opponent routes that white-box predicts can directly hit rear stones or enter through the centre guard; strict PhysX local refinement; no sweeping",
        "coarse": coarse,
        "strictCandidateCount": len(cases),
        "worstLegalGuardFirstAttack": worst,
        "topAttacks": cases[:12],
        "elapsedSeconds": time.perf_counter() - started,
    }


def main() -> int:
    args = parse_args()
    if args.parent_count < 1 or args.physics_seeds < 1 or not 0 <= args.shot_index < 16:
        raise SystemExit("--parent-count、--physics-seeds 必须为正，--shot-index 必须在 0..15")
    install_bundled_pyphysx()
    params = calibrate_from_recovered_formula()
    lookup = calibrate_force_lookup()
    seeds = [int(args.seed) + 104729 * offset for offset in range(args.physics_seeds)]
    environment = StrictCurlingEnd(seed=seeds[0], training_fast=True)
    selected = args.fixture or list(FIXTURES)
    reports = []
    for name in selected:
        report = run_fixture(
            FIXTURES[name], params=params, lookup=lookup, environment=environment,
            seeds=seeds, parent_count=args.parent_count, shot_index=args.shot_index,
        )
        reports.append(report)
        worst = report["worstLegalGuardFirstAttack"]
        if worst is None:
            summary = "未找到合法首撞守壶路线"
        else:
            summary = "后方最少留 %d，最少在营内 %d，最大位移 %s m" % (
                worst["worstRearRemaining"], worst["worstRearInHouse"],
                "—" if worst["maxRearDisplacementM"] is None else "%.3f" % worst["maxRearDisplacementM"],
            )
        print("%s | 严格候选=%d | %s | %.2fs" % (
            name, report["strictCandidateCount"], summary, report["elapsedSeconds"],
        ), flush=True)
    payload = {
        "schema": "centre_guard_shield_stress_v1",
        "scope": "strict PhysX stress test of attacks against stones behind the centre guard, including direct bypass and guard-first chains; finite search, not a proof over continuous inputs",
        "physicsSeeds": seeds,
        "reports": reports,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print("report=%s" % args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
