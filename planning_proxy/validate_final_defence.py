#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用严格 PhysX 检查防御球形能否扛住对方最后一颗反击。

这不是“我方壶摆得像不像目标阵型”的检查，而是反过来问：对方最后一颗壶在
筛过的直线、旋进和先撞我方壶的路线中，是否能

1. 停入按钮区（石头中心距离大本营中心不超过一颗壶半径）；或
2. 停得比我方任何在场壶都更靠中心。

任一严格 PhysX 摩擦序列出现上述情况，就将该候选视为反例。若没有反例，只能
说明“在本轮有限但偏进攻的反击搜索中暂时守住”，不能误称数学上的全空间保证。
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import HOUSE_X, HOUSE_Y, STONE_R, StrictCurlingEnd  # noqa: E402
from local_simulator.runtime_loader import install_bundled_pyphysx  # noqa: E402
from planning_proxy.analytic_proxy import (  # noqa: E402
    ProxyStone, calibrate_force_lookup, calibrate_from_recovered_formula, make_initial_candidates,
    simulate_batch,
)
from planning_proxy.strict_refine import BoardStone, Candidate, evaluate_one, local_candidates_for_parent, make_position  # noqa: E402


ACTIVE_INDEX = 15  # 对方的最后一颗；静止壶使用 1,3,5,...，避免占用它。
DEFAULT_OUTPUT = ROOT / "planning_proxy" / "runs" / "final_defence_validation.json"
CENTRE_GUARD = (HOUSE_X, 7.15)


@dataclass(frozen=True)
class DefenceFixture:
    name: str
    stage: str
    description: str
    stones: tuple[BoardStone, ...]


def _own_stones(points: Sequence[tuple[float, float]]) -> tuple[BoardStone, ...]:
    return tuple(BoardStone(2 * offset + 1, "self", x, y) for offset, (x, y) in enumerate(points))


# 坐标刻意不是完全对称的“教学摆盘”：所有壶间距大于一个壶直径，且红圈壶
# 前后错开。这样失败时才更接近真实的策略缺口，而不是摆盘重叠造成的伪失败。
DEFENCE_FIXTURES: tuple[DefenceFixture, ...] = (
    DefenceFixture(
        "双红圈错层", "一颗已有壶后的补第二红圈壶",
        "最低层基线：两颗己方红圈壶，未额外放前方保护壶。",
        _own_stones(((2.10, 4.52), (2.72, 5.15))),
    ),
    DefenceFixture(
        "左侧三角", "两颗已有壶后的左侧保护",
        "两颗错层红圈壶，加左前方保护壶。",
        _own_stones(((2.10, 4.52), (2.72, 5.15), (1.92, 6.12))),
    ),
    DefenceFixture(
        "右侧三角", "两颗已有壶后的右侧保护",
        "两颗错层红圈壶，加右前方保护壶。",
        _own_stones(((2.10, 4.52), (2.72, 5.15), (2.83, 6.12))),
    ),
    DefenceFixture(
        "三红圈错层", "两颗已有壶后的第三红圈壶",
        "三颗红圈壶彼此错开；它代表重得分、轻入口封锁的候选。",
        _own_stones(((2.00, 4.70), (2.68, 4.45), (2.80, 5.20))),
    ),
    DefenceFixture(
        "左侧外壳", "三颗已有壶后的左侧加壳",
        "三颗错层红圈壶加左前方保护壶，用于第八颗的高保守选择。",
        _own_stones(((2.00, 4.70), (2.68, 4.45), (2.80, 5.20), (1.92, 6.12))),
    ),
    DefenceFixture(
        "右侧外壳", "三颗已有壶后的右侧加壳",
        "三颗错层红圈壶加右前方保护壶，用于第八颗的高保守选择。",
        _own_stones(((2.00, 4.70), (2.68, 4.45), (2.80, 5.20), (2.83, 6.12))),
    ),
    # 下列是实际先手路线的正向验证盘：第一颗中线守壶仍在。前面的六组
    # 保留为“中线守壶已被拆掉时不能继续自欺欺人”的负例。
    DefenceFixture(
        "中线守壶加双红圈", "实际先手基线",
        "中线守壶仍在，两颗红圈壶错层；检验单守壶是否已足以封住末手旋进。",
        _own_stones((CENTRE_GUARD, (2.10, 4.52), (2.72, 5.15))),
    ),
    DefenceFixture(
        "中线守壶加左三角", "实际先手的左侧防线",
        "中线守壶、两颗红圈壶和左侧保护壶同时在场。",
        _own_stones((CENTRE_GUARD, (2.10, 4.52), (2.72, 5.15), (1.92, 6.12))),
    ),
    DefenceFixture(
        "中线守壶加右三角", "实际先手的右侧防线",
        "中线守壶、两颗红圈壶和右侧保护壶同时在场。",
        _own_stones((CENTRE_GUARD, (2.10, 4.52), (2.72, 5.15), (2.83, 6.12))),
    ),
    DefenceFixture(
        "中线守壶加左外壳", "第八颗后的左侧高保守防线",
        "中线守壶、三颗错层红圈壶与左侧外壳同时在场。",
        _own_stones((CENTRE_GUARD, (2.00, 4.70), (2.68, 4.45), (2.80, 5.20), (1.92, 6.12))),
    ),
    DefenceFixture(
        "中线守壶加右外壳", "第八颗后的右侧高保守防线",
        "中线守壶、三颗错层红圈壶与右侧外壳同时在场。",
        _own_stones((CENTRE_GUARD, (2.00, 4.70), (2.68, 4.45), (2.80, 5.20), (2.83, 6.12))),
    ),
    # 以上红圈错层盘都会给对方留下中心空位。以下是下一轮应重点寻找的
    # “中心锚”方向：我方先占按钮附近，对手必须清锚且自己滚入才可能反超。
    DefenceFixture(
        "中心锚加中线守壶", "中心锚基线",
        "我方一颗壶占按钮，中线守壶保留；检验单门能否阻止直线或旋进清锚。",
        _own_stones((CENTRE_GUARD, (HOUSE_X, HOUSE_Y))),
    ),
    DefenceFixture(
        "中心锚加左门", "中心锚的单侧保护",
        "按钮锚、中线守壶和左前方门壶同时在场。",
        _own_stones((CENTRE_GUARD, (HOUSE_X, HOUSE_Y), (1.92, 6.12))),
    ),
    DefenceFixture(
        "中心锚加双门", "中心锚的双侧保护",
        "按钮锚、中线守壶、左右两个前方门壶同时在场。",
        _own_stones((CENTRE_GUARD, (HOUSE_X, HOUSE_Y), (1.92, 6.12), (2.83, 6.12))),
    ),
    # 中心锚双门的包络边界。先分别扰动一个角色，避免在一次测试中混入多个
    # 变量；通过快筛的边界才进入九序列复核。
    DefenceFixture(
        "双门范围_锚左", "中心锚左边界",
        "中心锚向左偏 13.5 cm，其余角色取基准位置。",
        _own_stones((CENTRE_GUARD, (2.24, HOUSE_Y), (1.92, 6.12), (2.83, 6.12))),
    ),
    DefenceFixture(
        "双门范围_锚右", "中心锚右边界",
        "中心锚向右偏 13.5 cm，其余角色取基准位置。",
        _own_stones((CENTRE_GUARD, (2.51, HOUSE_Y), (1.92, 6.12), (2.83, 6.12))),
    ),
    DefenceFixture(
        "双门范围_锚前", "中心锚前边界",
        "中心锚向来壶方向偏 13 cm，其余角色取基准位置。",
        _own_stones((CENTRE_GUARD, (HOUSE_X, 5.01), (1.92, 6.12), (2.83, 6.12))),
    ),
    DefenceFixture(
        "双门范围_锚后", "中心锚后边界",
        "中心锚向大本营后方偏 13 cm，其余角色取基准位置。",
        _own_stones((CENTRE_GUARD, (HOUSE_X, 4.75), (1.92, 6.12), (2.83, 6.12))),
    ),
    DefenceFixture(
        "双门范围_守壶左", "中线守壶左边界",
        "中线守壶向左偏 12.5 cm，其余角色取基准位置。",
        _own_stones(((2.25, 7.15), (HOUSE_X, HOUSE_Y), (1.92, 6.12), (2.83, 6.12))),
    ),
    DefenceFixture(
        "双门范围_守壶右", "中线守壶右边界",
        "中线守壶向右偏 12.5 cm，其余角色取基准位置。",
        _own_stones(((2.50, 7.15), (HOUSE_X, HOUSE_Y), (1.92, 6.12), (2.83, 6.12))),
    ),
    DefenceFixture(
        "双门范围_守壶微左", "中线守壶左侧窄范围",
        "中线守壶只向左偏 5 cm，用于寻找仍可接受的横向容差。",
        _own_stones(((2.325, 7.15), (HOUSE_X, HOUSE_Y), (1.92, 6.12), (2.83, 6.12))),
    ),
    DefenceFixture(
        "双门范围_守壶微右", "中线守壶右侧窄范围",
        "中线守壶只向右偏 5 cm，用于寻找仍可接受的横向容差。",
        _own_stones(((2.425, 7.15), (HOUSE_X, HOUSE_Y), (1.92, 6.12), (2.83, 6.12))),
    ),
    DefenceFixture(
        "双门范围_门外张", "双门外张边界",
        "左右门壶同时向外、向前张开。",
        _own_stones((CENTRE_GUARD, (HOUSE_X, HOUSE_Y), (1.82, 6.42), (2.93, 6.42))),
    ),
    DefenceFixture(
        "双门范围_门内收", "双门内收边界",
        "左右门壶同时向内、向后收窄。",
        _own_stones((CENTRE_GUARD, (HOUSE_X, HOUSE_Y), (2.08, 5.92), (2.67, 5.92))),
    ),
    # 三壶残局不能同时保存中线守壶和双门，因此单列检验“锚 + 双门”的取舍。
    DefenceFixture(
        "三壶中心锚加宽双门", "三壶残局的宽双门",
        "按钮锚加左右外侧门壶；舍弃中线守壶，换取两侧旋进线都被遮挡。",
        _own_stones(((HOUSE_X, HOUSE_Y), (1.92, 6.12), (2.83, 6.12))),
    ),
    DefenceFixture(
        "三壶中心锚加窄双门", "三壶残局的窄双门",
        "按钮锚加左右内收门壶；门缝接近一颗壶的直径，专门检验对方能否穿窄缝或撞门滚入。",
        _own_stones(((HOUSE_X, HOUSE_Y), (2.08, 5.92), (2.67, 5.92))),
    ),
    DefenceFixture(
        "三壶中心锚加左内盖", "三壶残局的左错位内盖",
        "中线守壶、按钮锚和左前方错位内圈盖壶；避免三颗壶落在同一条直线。",
        _own_stones((CENTRE_GUARD, (HOUSE_X, HOUSE_Y), (2.05, 5.18))),
    ),
    DefenceFixture(
        "三壶中心锚加右内盖", "三壶残局的右错位内盖",
        "中线守壶、按钮锚和右前方错位内圈盖壶；作为左内盖的镜像验证。",
        _own_stones((CENTRE_GUARD, (HOUSE_X, HOUSE_Y), (2.70, 5.18))),
    ),
)


def _closest_to_centre_indices(prediction, *, count: int, require_hit: bool) -> list[int]:
    """从粗代理取对方最危险的父区域。

    ``require_hit=False`` 取可能直接旋进中心的路线；``True`` 只取先撞到我方
    壶的路线，防止漏掉“撞开守壶后自己滚进中心”的反击。
    """

    centre_distance = np.hypot(prediction.stop_points[:, 0] - HOUSE_X, prediction.stop_points[:, 1] - HOUSE_Y)
    if require_hit:
        eligible = np.flatnonzero(prediction.first_hit_index >= 0)
    else:
        eligible = np.flatnonzero((prediction.first_hit_index < 0) & ~prediction.exits_play)
    order = eligible[np.argsort(centre_distance[eligible])]
    return [int(value) for value in order[:count]]


def _parents_for_opponent(board: Sequence[BoardStone], *, direct_count: int, impact_count: int) -> tuple[list[dict], dict]:
    params = calibrate_from_recovered_formula()
    lookup = calibrate_force_lookup()
    proxy_board = [ProxyStone(stone.index, stone.owner, stone.x, stone.y) for stone in board]
    initial = simulate_batch(
        make_initial_candidates(velocity_count=7, lateral_count=41, spin_count=15),
        proxy_board, params, force_lookup=lookup, dt=0.02,
    )
    direct = _closest_to_centre_indices(initial, count=direct_count, require_hit=False)
    impact = _closest_to_centre_indices(initial, count=impact_count, require_hit=True)
    selected = list(dict.fromkeys(direct + impact))
    direct_set = set(direct)
    rows = [{
        "bestshot": [float(value) for value in initial.shots[index]],
        # 这不是“容易/困难”的最终判断；它只记录反击是否需要先撞现有壶，供
        # 同候选族、同预算下的后续难度比较使用。
        "replyFamily": "DIRECT_OR_DRAW" if index in direct_set else "IMPACT_OR_RUNBACK",
    } for index in selected]
    return rows, {
        "initialCandidateCount": int(len(initial.shots)),
        "directParentCount": len(direct),
        "impactParentCount": len(impact),
        "totalParentCount": len(rows),
    }


def _seed_is_safe(
    final_distances: dict[int, float], own_indices: set[int], opponent_indices: set[int],
) -> tuple[bool, str, float | None, float | None]:
    """按真实终局双方所有存活壶判断末手反击是否得手。

    静态模板只有己方壶；实战终局还可能有上一手未清干净的敌壶。因此不能只
    看第 16 手是否比己方更近，而要把它与所有既有敌壶一起纳入计分侧比较。
    """

    active_distance = final_distances.get(ACTIVE_INDEX)
    opponent_distances = [
        distance for index, distance in final_distances.items() if index in opponent_indices
    ]
    own_distances = [distance for index, distance in final_distances.items() if index in own_indices]
    own_closest = min(own_distances) if own_distances else None
    opponent_closest = min(opponent_distances) if opponent_distances else None
    if active_distance is None and opponent_closest is None:
        return True, "对方最后一颗出界，且没有残留敌方得分壶", None, own_closest
    if active_distance is not None and active_distance <= STONE_R:
        return False, "对方最后一颗进入按钮区", active_distance, own_closest
    if own_closest is None:
        return False, "我方壶被全部清空，而对方壶留在场内", opponent_closest, None
    if opponent_closest is not None and opponent_closest < own_closest:
        return False, "对方（末手或残留壶）比我方最近壶更靠中心", opponent_closest, own_closest
    return True, "对方未取得中心优势", opponent_closest, own_closest


def evaluate_fixture(
    fixture: DefenceFixture,
    environment: StrictCurlingEnd,
    *, direct_count: int,
    impact_count: int,
    physics_seeds: Sequence[int],
    stop_on_first_counterexample: bool,
) -> dict:
    parents, coarse_metadata = _parents_for_opponent(
        fixture.stones, direct_count=direct_count, impact_count=impact_count,
    )
    position = make_position(fixture.stones)
    own_indices = {stone.index for stone in fixture.stones if stone.owner == "self"}
    opponent_indices = {ACTIVE_INDEX} | {stone.index for stone in fixture.stones if stone.owner == "opponent"}
    seen: set[tuple[float, float, float]] = set()
    strict_count = 0
    counterexamples: list[dict] = []
    button_counterexample_count = 0
    stable_counterexample_count = 0
    direct_counterexample_count = 0
    impact_counterexample_count = 0
    best_opponent_distance = math.inf
    largest_centre_advantage = 0.0
    for rank, row in enumerate(parents, 1):
        for candidate in local_candidates_for_parent(row, rank, seen):
            strict_count += 1
            result = evaluate_one(
                environment, candidate, fixture.stones, position, physics_seeds,
                shot_index=15, active_index=ACTIVE_INDEX,
            )
            seed_results = [
                _seed_is_safe(distances, own_indices, opponent_indices)
                for distances in result.final_center_distance_by_index
            ]
            breaches = []
            for seed_index, (safe, reason, enemy_distance, own_distance) in enumerate(seed_results):
                if enemy_distance is not None:
                    best_opponent_distance = min(best_opponent_distance, enemy_distance)
                if enemy_distance is not None and own_distance is not None:
                    largest_centre_advantage = max(largest_centre_advantage, own_distance - enemy_distance)
                if not safe:
                    breaches.append({
                        "physicsSeed": int(physics_seeds[seed_index]),
                        "reason": reason,
                        "opponentFinalDistanceM": enemy_distance,
                        "ownClosestDistanceM": own_distance,
                    })
            if breaches:
                if any(item["reason"] == "对方最后一颗进入按钮区" for item in breaches):
                    button_counterexample_count += 1
                if len(breaches) == len(physics_seeds):
                    stable_counterexample_count += 1
                reply_family = str(row["replyFamily"])
                if reply_family == "DIRECT_OR_DRAW":
                    direct_counterexample_count += 1
                else:
                    impact_counterexample_count += 1
                counterexamples.append({
                    "bestshot": [candidate.v0, candidate.h0, candidate.w0],
                    "parentRank": candidate.parent_rank,
                    "replyFamily": reply_family,
                    "breachSeedCount": len(breaches),
                    "seedCount": len(physics_seeds),
                    "breaches": breaches,
                })
                # 只适合快速找明显漏洞；默认测完整个筛过的反击集合，以区分
                # 偶发漏洞与稳定可复现的对方破局路线。
                if stop_on_first_counterexample:
                    break
        if stop_on_first_counterexample and counterexamples:
            break
    return {
        "fixture": asdict(fixture), "coarse": coarse_metadata,
        "strictCandidateCount": strict_count, "screenedSafe": not counterexamples,
        "counterexampleCandidateCount": len(counterexamples),
        "stableCounterexampleCandidateCount": stable_counterexample_count,
        "buttonCounterexampleCandidateCount": button_counterexample_count,
        "directCounterexampleCandidateCount": direct_counterexample_count,
        "impactCounterexampleCandidateCount": impact_counterexample_count,
        "bestOpponentDistanceM": None if not math.isfinite(best_opponent_distance) else best_opponent_distance,
        "largestOpponentCentreAdvantageM": largest_centre_advantage,
        # 前 20 条足够复现最危险输入，避免长跑报告无限膨胀。
        "counterexamples": counterexamples[:20],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", action="append", choices=[item.name for item in DEFENCE_FIXTURES], help="只测指定球形；可重复传入。")
    parser.add_argument("--direct-parents", type=int, default=3, help="粗筛中保留几条最接近中心的直进/旋进父区域。")
    parser.add_argument("--impact-parents", type=int, default=3, help="粗筛中保留几条先撞我方壶的父区域。")
    parser.add_argument("--physics-seeds", type=int, default=3, help="每条对方反击路线严格复核的摩擦序列数。")
    parser.add_argument("--stop-on-first-counterexample", action="store_true", help="只用于快速找漏洞；默认完整统计反击成功次数。")
    parser.add_argument("--seed", type=int, default=20260716)
    parser.add_argument(
        "--board-json", type=Path, default=None,
        help="真实第八颗落定后的壶面 JSON 数组。元素为 index/owner/x/y，可选 yaw；slot 15 留给对手末手。提供后只验证该实际壶面。",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def load_actual_final_board(path: Path) -> DefenceFixture:
    """读取实际第八颗终局，供与基准模板不同的每个构型单独反击验收。"""

    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("--board-json 必须是壶对象数组")
    stones = tuple(
        BoardStone(
            index=int(item["index"]), owner=str(item["owner"]), x=float(item["x"]), y=float(item["y"]),
            enabled=bool(item.get("enabled", True)), yaw=float(item.get("yaw", 0.0)),
        )
        for item in raw
        if isinstance(item, dict) and bool(item.get("enabled", True))
    )
    if not stones:
        raise ValueError("--board-json 没有有效静止壶")
    if any(stone.owner not in {"self", "opponent"} for stone in stones):
        raise ValueError("--board-json 的 owner 只能是 self 或 opponent")
    if any(not 1 <= stone.index < ACTIVE_INDEX for stone in stones):
        raise ValueError("--board-json 的静止壶 index 必须在 1..14；slot 15 保留给对手末手")
    if len({stone.index for stone in stones}) != len(stones):
        raise ValueError("--board-json 的 stone index 不能重复")
    if not any(stone.owner == "self" for stone in stones):
        raise ValueError("--board-json 至少需要一颗己方壶")
    return DefenceFixture(
        name=f"实际终局:{path.stem}", stage="第八颗落定后的真实壶面",
        description="由 --board-json 提供；包含残留壶与 yaw 后逐条搜索对手第十六手。", stones=stones,
    )


def main() -> None:
    args = parse_args()
    if min(args.direct_parents, args.impact_parents, args.physics_seeds) < 1:
        raise SystemExit("父区域数和摩擦序列数都必须至少为 1")
    if args.board_json is not None and args.fixture is not None:
        raise SystemExit("--board-json 与 --fixture 不能同时使用")
    try:
        chosen = (load_actual_final_board(args.board_json),) if args.board_json is not None else tuple(
            item for item in DEFENCE_FIXTURES if args.fixture is None or item.name in args.fixture
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"无法读取实际终局壶面：{exc}") from exc
    install_bundled_pyphysx()
    environment = StrictCurlingEnd(seed=args.seed, training_fast=True)
    started = time.perf_counter()
    reports = []
    for index, fixture in enumerate(chosen):
        seeds = [args.seed + index * 100_003 + offset * 7919 for offset in range(args.physics_seeds)]
        report = evaluate_fixture(
            fixture, environment,
            direct_count=args.direct_parents, impact_count=args.impact_parents,
            physics_seeds=seeds, stop_on_first_counterexample=args.stop_on_first_counterexample,
        )
        reports.append(report)
        state = "暂未发现反例" if report["screenedSafe"] else "发现反例"
        print(f"{fixture.name}: {state}；严格候选 {report['strictCandidateCount']} 条")
        if report["counterexamples"]:
            print("  ", report["counterexamples"][0])
    payload = {
        "scope": "strict PhysX screened final-opponent reply; no sweeping; not a mathematical proof over continuous inputs",
        "criteria": {
            "buttonRadiusM": STONE_R,
            "centreAdvantage": "the closest of the final opponent stone and every surviving old opponent stone must not be smaller than the closest surviving self stone",
        },
        "physicsSeedsPerCandidate": args.physics_seeds,
        "stopOnFirstCounterexample": bool(args.stop_on_first_counterexample),
        "reports": reports,
        "elapsedSeconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"report={args.output}")


if __name__ == "__main__":
    main()
