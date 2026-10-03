"""运行时战术提议器：当前棋盘 -> 已绑定的 GoalState 列表。

本模块不调用路径规划器。它将历史按钮中心坐标编译到本地 PhysX 坐标，并把
历史中的匿名几何角色绑定到当前棋盘的 slot。调用方依次将返回的目标交给
规划器；当前预算内未找到候选或严格验收失败时，调用方尝试下一条目标。前者不是
物理无解结论。
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from planning_proxy.competition_rules import HOUSE_R, HOUSE_X, HOUSE_Y, STONE_R
from training_data.nwnht_curling.causal_state_machine.build_causal_state_abstraction import state_key
from training_data.nwnht_curling.causal_state_machine.build_collision_goal_families import macro_collision_state
from training_data.nwnht_curling.causal_state_machine.build_zone_goal_fallbacks import compact_zone_state

from .models import CircleRegion, GoalState, OccupancyConstraint, StoneConstraint, StoneSelector


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_ROOT = PROJECT_ROOT / "training_data" / "nwnht_curling" / "causal_state_machine" / "artifacts"
FINE_EDGE_ARTIFACT = ARTIFACT_ROOT / "nwnht_goal_state_edges_v0.json"
COLLISION_FAMILY_ARTIFACT = ARTIFACT_ROOT / "nwnht_collision_goal_families_v2.json"
ZONE_FALLBACK_ARTIFACT = ARTIFACT_ROOT / "nwnht_zone_goal_fallbacks_v0.json"


@dataclass(frozen=True)
class BoundStoneConstraint:
    """已把几何角色绑定到本局真实 slot 的终局约束。"""

    role: str
    stone_index: int | None
    owner: str
    disposition: str
    final_region: CircleRegion | None = None

    def to_json(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "stone_index": self.stone_index,
            "owner": self.owner,
            "disposition": self.disposition,
            "final_region": None if self.final_region is None else self.final_region.to_json(),
        }


@dataclass(frozen=True)
class ProposedGoal:
    """一条可直接交给规划器的候选终局，附带历史证据而非胜率承诺。"""

    goal: GoalState
    bound_stone_constraints: tuple[BoundStoneConstraint, ...]
    proposal_kind: str
    support: int
    evidence_status: str
    observed_after_reply_distribution: tuple[dict[str, Any], ...]
    source_artifact_id: str

    def to_json(self) -> dict[str, Any]:
        return {
            "goal": self.goal.to_json(),
            "bound_stone_constraints": [item.to_json() for item in self.bound_stone_constraints],
            "proposal_kind": self.proposal_kind,
            "support": self.support,
            "evidence_status": self.evidence_status,
            "observed_after_reply_distribution": list(self.observed_after_reply_distribution),
            "source_artifact_id": self.source_artifact_id,
        }


@dataclass(frozen=True)
class GoalProposalSet:
    """当前状态及按优先级排序的 GoalState；空列表表示搜索保底策略。"""

    own_throw_number: int
    runtime_core_state: str
    runtime_collision_state: str
    proposals: tuple[ProposedGoal, ...]
    runtime_zone_state: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "own_throw_number": self.own_throw_number,
            "runtime_core_state": self.runtime_core_state,
            "runtime_collision_state": self.runtime_collision_state,
            "runtime_zone_state": self.runtime_zone_state,
            "proposals": [item.to_json() for item in self.proposals],
            "warning": "历史终局模板；必须由调用方进行本地规则检查、严格 PhysX 可达性与反击搜索。",
        }


def _stones(board: Iterable[object]) -> list[dict[str, Any]]:
    """标准化当前本地棋盘；只接受 runtime 所需坐标和壶 slot。"""

    result: list[dict[str, Any]] = []
    for item in board:
        if isinstance(item, Mapping):
            get = item.get
        else:
            get = lambda name, default=None: getattr(item, name, default)
        if not bool(get("enabled", True)):
            continue
        owner = str(get("owner"))
        if owner not in {"self", "opponent"}:
            raise ValueError("runtime board 的 owner 必须为 self 或 opponent")
        result.append({
            "index": int(get("index")), "owner": owner,
            "x": float(get("x")), "y": float(get("y")),
        })
    if len({stone["index"] for stone in result}) != len(result):
        raise ValueError("runtime board 的 stone index 不能重复")
    return result


def _historical_frame(board: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    """将本地绝对坐标翻译为 NWNHT 按钮中心规范坐标。"""

    return [
        {
            "owner": "first" if stone["owner"] == "self" else "opponent",
            "colour": "runtime",
            "x_m": float(stone["x"]) - HOUSE_X,
            "y_m": float(stone["y"]) - HOUSE_Y,
        }
        for stone in board
    ]


def runtime_states(board: Iterable[object], own_throw_number: int) -> tuple[list[dict[str, Any]], str, str]:
    if not 1 <= int(own_throw_number) <= 8:
        raise ValueError("own_throw_number 必须为 1..8")
    stones = _stones(board)
    historical = _historical_frame(stones)
    core = state_key(int(own_throw_number), historical)
    return stones, core, macro_collision_state(core)


def _load_json(path: Path) -> list[dict[str, Any]]:
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise RuntimeError(f"缺少战术工件: {path}") from error
    if not isinstance(parsed, list):
        raise RuntimeError(f"战术工件格式错误: {path}")
    return parsed


def _compile_region(normalized: dict[str, Any], region_id: str) -> CircleRegion:
    if normalized.get("shape") != "circle":
        raise ValueError("当前只支持圆形终局区域")
    return CircleRegion(
        region_id=region_id,
        centre_x=HOUSE_X + float(normalized["centre_x_m"]),
        centre_y=HOUSE_Y + float(normalized["centre_y_m"]),
        radius_m=float(normalized["radius_m"]),
    )


def _house_occupancy_constraints(after_own_occupancy: Mapping[str, Any]) -> tuple[OccupancyConstraint, ...]:
    """将历史终局的营内数量编译为本地 PhysX 可检查的结构约束。"""

    house = CircleRegion("house", HOUSE_X, HOUSE_Y, HOUSE_R + STONE_R)
    constraints: list[OccupancyConstraint] = []
    for historical_owner, runtime_owner in (("first", "self"), ("opponent", "opponent")):
        zones = after_own_occupancy.get(historical_owner, {})
        if not isinstance(zones, Mapping):
            raise ValueError("after_own_occupancy 必须按 owner 给出区域数量")
        count = sum(int(value) for name, value in zones.items() if str(name) == "button" or str(name).startswith("house_"))
        constraints.append(OccupancyConstraint(runtime_owner, house, min_count=count, max_count=count))
    return tuple(constraints)


def _rank(stones: Sequence[dict[str, Any]], rank_by: str) -> list[dict[str, Any]]:
    if rank_by == "closest_to_button":
        return sorted(stones, key=lambda item: math.hypot(float(item["x"]) - HOUSE_X, float(item["y"]) - HOUSE_Y))
    if rank_by == "frontmost":
        return sorted(stones, key=lambda item: -float(item["y"]))
    if rank_by == "backmost":
        return sorted(stones, key=lambda item: float(item["y"]))
    if rank_by == "leftmost":
        return sorted(stones, key=lambda item: float(item["x"]))
    if rank_by == "rightmost":
        return sorted(stones, key=lambda item: -float(item["x"]))
    raise ValueError(f"未知 rank_by: {rank_by}")


def _resolve_selector(selector: dict[str, Any], stones: Sequence[dict[str, Any]]) -> dict[str, Any] | None:
    owner = str(selector["owner"])
    candidates = [stone for stone in stones if stone["owner"] == owner]
    region = str(selector["source_region"])
    if region == "house":
        candidates = [
            stone for stone in candidates
            if math.hypot(float(stone["x"]) - HOUSE_X, float(stone["y"]) - HOUSE_Y) <= HOUSE_R + STONE_R
        ]
    elif region not in {"visible", "active_delivery"}:
        return None
    rank = int(selector["rank"])
    ordered = _rank(candidates, str(selector["rank_by"]))
    return ordered[rank - 1] if len(ordered) >= rank else None


def _fine_proposals(
    *, state: str, stones: Sequence[dict[str, Any]], active_stone_index: int | None,
    edges: Sequence[dict[str, Any]], limit: int, require_last_reply_search: bool,
) -> list[ProposedGoal]:
    result: list[ProposedGoal] = []
    matching = [
        edge for edge in edges
        if bool(edge.get("runtime_candidate")) and str(edge.get("source_state")) == state
    ]
    for edge in sorted(matching, key=lambda item: (-int(item["support"]), str(item["edge_id"])))[:limit]:
        region_data = edge.get("active_final_region")
        active_region = None if region_data is None else _compile_region(region_data, f"{edge['edge_id']}_active")
        constraints: list[StoneConstraint] = []
        bound: list[BoundStoneConstraint] = []
        if active_region is not None:
            active_selector = StoneSelector("active_delivery", "self", "active_delivery", "closest_to_button")
            constraints.append(StoneConstraint(active_selector, "IN_REGION", active_region))
            bound.append(BoundStoneConstraint("active_delivery", active_stone_index, "self", "IN_REGION", active_region))
        resolvable = True
        for raw in edge.get("stone_constraints_when_unambiguous", []):
            target = _resolve_selector(raw, stones)
            if target is None:
                resolvable = False
                break
            selector = StoneSelector(
                str(raw["selector_id"]), str(raw["owner"]), str(raw["source_region"]),
                str(raw["rank_by"]), int(raw["rank"]),
            )
            disposition = str(raw["required_disposition"])
            constraints.append(StoneConstraint(selector, disposition))
            bound.append(BoundStoneConstraint(selector.selector_id, int(target["index"]), str(target["owner"]), disposition))
        if not resolvable:
            continue
        own_after = edge["expected_own_after_states"][0]["state"]
        after_reply = edge["expected_after_reply_states"][0]["state"]
        goal = GoalState(
            transition_id=str(edge["edge_id"]), priority=1, source_state=state,
            expected_own_after_state=str(own_after), expected_after_reply_state=str(after_reply),
            stone_constraints=tuple(constraints),
            occupancy_constraints=_house_occupancy_constraints(edge["after_own_occupancy"]),
            forbidden_outcomes=("free_guard_zone_violation",),
            require_last_reply_search=require_last_reply_search,
            evidence_status="HISTORICAL_TEMPLATE",
            notes="精细终局边；出手后必须根据真实棋盘重新分类。" + (
                " 第 8 手必须完成对手最后一壶反击搜索后才能验收。" if require_last_reply_search else ""
            ),
        )
        result.append(ProposedGoal(
            goal=goal, bound_stone_constraints=tuple(bound), proposal_kind="FINE_TERMINAL_REGION",
            support=int(edge["support"]), evidence_status=str(edge["evidence_status"]),
            observed_after_reply_distribution=tuple(edge["expected_after_reply_states"]),
            source_artifact_id=str(edge["edge_id"]),
        ))
    return result


def _collision_proposals(
    *, collision_state: str, stones: Sequence[dict[str, Any]], families: Sequence[dict[str, Any]],
    max_pairs: int, require_last_reply_search: bool,
) -> list[ProposedGoal]:
    result: list[ProposedGoal] = []
    matching = [
        family for family in families
        if bool(family.get("runtime_candidate_for_physx_screen"))
        and str(family.get("source_collision_state")) == collision_state
    ]
    for family in sorted(
        matching,
        key=lambda item: (-int(item.get("dynamic_binding_request", {}).get("choose_count", 0)), -int(item["support"]), str(item["collision_family_id"])),
    ):
        request = family.get("dynamic_binding_request")
        if not isinstance(request, dict):
            continue
        available = [
            stone for stone in stones if stone["owner"] == "opponent"
            and math.hypot(float(stone["x"]) - HOUSE_X, float(stone["y"]) - HOUSE_Y) <= HOUSE_R + STONE_R
        ]
        choose_count = int(request["choose_count"])
        pair_order = sorted(
            itertools.combinations(available, choose_count),
            key=lambda pair: (
                min(math.hypot(float(item["x"]) - HOUSE_X, float(item["y"]) - HOUSE_Y) for item in pair),
                sum(math.hypot(float(item["x"]) - HOUSE_X, float(item["y"]) - HOUSE_Y) for item in pair),
            ),
        )
        for pair_rank, pair in enumerate(pair_order[:max_pairs], 1):
            constraints: list[StoneConstraint] = []
            bound: list[BoundStoneConstraint] = []
            for rank, stone in enumerate(pair, 1):
                selector = StoneSelector(f"opponent_house_set_{choose_count}_{pair_rank}_{rank}", "opponent", "house", "closest_to_button", rank)
                constraints.append(StoneConstraint(selector, "OUT_OF_PLAY"))
                bound.append(BoundStoneConstraint(selector.selector_id, int(stone["index"]), "opponent", "OUT_OF_PLAY"))
            own_after = family["observed_own_after_states"][0]["value"]
            after_reply = family["observed_after_reply_states"][0]["value"]
            goal = GoalState(
                transition_id=f"{family['collision_family_id']}|pair={pair_rank}", priority=1,
                source_state=collision_state, expected_own_after_state=str(own_after), expected_after_reply_state=str(after_reply),
                stone_constraints=tuple(constraints), forbidden_outcomes=("free_guard_zone_violation",),
                require_last_reply_search=require_last_reply_search,
                evidence_status="HISTORICAL_TEMPLATE",
                notes=(
                    f"多模态清壶家族：只约束选中的 {choose_count} 颗对方营内壶出界，不虚构出手壶唯一滚位。"
                    + (" 第 8 手必须完成对手最后一壶反击搜索后才能验收。" if require_last_reply_search else "")
                ),
            )
            result.append(ProposedGoal(
                goal=goal, bound_stone_constraints=tuple(bound), proposal_kind="COLLISION_PAIR_OUT",
                support=int(family["support"]), evidence_status=str(family["evidence_status"]),
                observed_after_reply_distribution=tuple(family["observed_after_reply_states"]),
                source_artifact_id=str(family["collision_family_id"]),
            ))
    return result


def _zone_proposals(
    *, zone_state: str, active_stone_index: int | None, fallbacks: Sequence[dict[str, Any]], limit: int,
    require_last_reply_search: bool,
) -> list[ProposedGoal]:
    result: list[ProposedGoal] = []
    matching = [item for item in fallbacks if str(item.get("source_zone_state")) == zone_state]
    for item in sorted(matching, key=lambda row: (-int(row["support"]), str(row["fallback_id"])))[:limit]:
        region = _compile_region(item["active_final_region"], f"{item['fallback_id']}_active")
        selector = StoneSelector("active_delivery", "self", "active_delivery", "closest_to_button")
        goal = GoalState(
            transition_id=str(item["fallback_id"]), priority=1, source_state=zone_state,
            expected_own_after_state=str(item["expected_own_after_states"][0]["state"]),
            expected_after_reply_state=str(item["expected_after_reply_states"][0]["state"]),
            stone_constraints=(StoneConstraint(selector, "IN_REGION", region),),
            forbidden_outcomes=("free_guard_zone_violation",),
            require_last_reply_search=require_last_reply_search,
            evidence_status="HISTORICAL_TEMPLATE",
            notes=(
                "第三层历史区域回退：后继状态仅为观测分布，不施加硬营内数量约束；当前 PhysX 搜索预算未找到时继续调用方保底策略，但不宣称物理无解。"
                + (" 第 8 手必须完成对手最后一壶反击搜索后才能验收。" if require_last_reply_search else "")
            ),
        )
        result.append(ProposedGoal(
            goal=goal,
            bound_stone_constraints=(BoundStoneConstraint("active_delivery", active_stone_index, "self", "IN_REGION", region),),
            proposal_kind="HISTORICAL_ZONE_FALLBACK", support=int(item["support"]),
            evidence_status=str(item["evidence_status"]),
            observed_after_reply_distribution=tuple(item["expected_after_reply_states"]),
            source_artifact_id=str(item["fallback_id"]),
        ))
    return result


def propose_goal_states(
    board: Iterable[object], own_throw_number: int, *, active_stone_index: int | None = None,
    fine_edges: Sequence[dict[str, Any]] | None = None,
    collision_families: Sequence[dict[str, Any]] | None = None,
    zone_fallbacks: Sequence[dict[str, Any]] | None = None,
    max_fine: int = 3, max_collision_pairs: int = 3, max_zone: int = 3,
) -> GoalProposalSet:
    """返回优先级和回退都已排好的终局约束；空结果由调用方走保底搜索。"""

    if max_fine < 0 or max_collision_pairs < 0 or max_zone < 0:
        raise ValueError("候选数量上限不能为负")
    stones, core_state, collision_state = runtime_states(board, own_throw_number)
    zone_state = compact_zone_state(core_state)
    fine = list(fine_edges) if fine_edges is not None else _load_json(FINE_EDGE_ARTIFACT)
    collisions = list(collision_families) if collision_families is not None else _load_json(COLLISION_FAMILY_ARTIFACT)
    zones = list(zone_fallbacks) if zone_fallbacks is not None else _load_json(ZONE_FALLBACK_ARTIFACT)
    # 碰撞目标优先于同一局面的静态落点，因其针对当前明确的对方营内双壶；
    # 两者都仅是待 PhysX 验证候选，并非已证明最优。
    final_throw_requires_reply_search = int(own_throw_number) == 8
    proposals = _collision_proposals(
        collision_state=collision_state, stones=stones, families=collisions, max_pairs=max_collision_pairs,
        require_last_reply_search=final_throw_requires_reply_search,
    )
    proposals.extend(_fine_proposals(
        state=core_state, stones=stones, active_stone_index=active_stone_index, edges=fine, limit=max_fine,
        require_last_reply_search=final_throw_requires_reply_search,
    ))
    proposals.extend(_zone_proposals(
        zone_state=zone_state, active_stone_index=active_stone_index, fallbacks=zones, limit=max_zone,
        require_last_reply_search=final_throw_requires_reply_search,
    ))
    ranked: list[ProposedGoal] = []
    ids = [proposal.goal.transition_id for proposal in proposals]
    for priority, proposal in enumerate(proposals, 1):
        fallback_ids = tuple(ids[priority:])
        ranked.append(replace(proposal, goal=replace(proposal.goal, priority=priority, fallback_transition_ids=fallback_ids)))
    return GoalProposalSet(
        own_throw_number=int(own_throw_number), runtime_core_state=core_state,
        runtime_collision_state=collision_state, proposals=tuple(ranked), runtime_zone_state=zone_state,
    )
