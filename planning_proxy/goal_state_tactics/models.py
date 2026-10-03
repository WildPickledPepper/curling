"""战术层交给路径规划器的终局约束数据契约。

历史 NWNHT 快照没有同色壶跨帧 id，因此历史抽取阶段绝不能把某颗历史壶
伪造成固定 slot。``StoneSelector`` 先以几何角色描述壶；运行时 binder 再在
当前 PhysX 棋盘上解析为实际 slot。目标区域均为范围而非精确点。
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal


Owner = Literal["self", "opponent"]
Disposition = Literal["OUT_OF_PLAY", "SURVIVE", "IN_REGION"]
RankBy = Literal["closest_to_button", "frontmost", "backmost", "leftmost", "rightmost"]
LastReplyPolicy = Literal["REQUIRE_SEARCH_RECORD", "REQUIRE_NO_COUNTERPLAY"]


@dataclass(frozen=True)
class CircleRegion:
    """一个以米为单位的可接受终局圆区。"""

    region_id: str
    centre_x: float
    centre_y: float
    radius_m: float

    def __post_init__(self) -> None:
        if not self.region_id:
            raise ValueError("region_id 不能为空")
        if self.radius_m <= 0.0:
            raise ValueError("目标区域半径必须为正")

    def to_json(self) -> dict[str, object]:
        return {
            "region_id": self.region_id,
            "shape": "circle",
            "centre": [self.centre_x, self.centre_y],
            "radius_m": self.radius_m,
        }


@dataclass(frozen=True)
class StoneSelector:
    """在运行时棋盘上选择一颗壶的几何角色，不携带历史或 PhysX 固定 id。"""

    selector_id: str
    owner: Owner
    source_region: str
    rank_by: RankBy
    rank: int = 1

    def __post_init__(self) -> None:
        if not self.selector_id:
            raise ValueError("selector_id 不能为空")
        if self.rank < 1:
            raise ValueError("rank 从 1 开始")
        if not self.source_region:
            raise ValueError("source_region 不能为空")

    def to_json(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class StoneConstraint:
    """一个关键壶的终局去留或落点范围要求。"""

    selector: StoneSelector
    disposition: Disposition
    final_region: CircleRegion | None = None
    required: bool = True

    def __post_init__(self) -> None:
        if self.disposition == "IN_REGION" and self.final_region is None:
            raise ValueError("IN_REGION 必须提供 final_region")
        if self.disposition != "IN_REGION" and self.final_region is not None:
            raise ValueError("只有 IN_REGION 可以携带 final_region")

    def to_json(self) -> dict[str, object]:
        return {
            "selector": self.selector.to_json(),
            "disposition": self.disposition,
            "final_region": None if self.final_region is None else self.final_region.to_json(),
            "required": self.required,
        }


@dataclass(frozen=True)
class OccupancyConstraint:
    """对一个终局区域内某方壶数量的约束，处理匿名或连撞后不可追踪的壶。"""

    owner: Owner
    region: CircleRegion
    min_count: int = 0
    max_count: int | None = None

    def __post_init__(self) -> None:
        if self.min_count < 0:
            raise ValueError("min_count 不能为负")
        if self.max_count is not None and self.max_count < self.min_count:
            raise ValueError("max_count 不能小于 min_count")

    def to_json(self) -> dict[str, object]:
        return {
            "owner": self.owner,
            "region": self.region.to_json(),
            "min_count": self.min_count,
            "max_count": self.max_count,
        }


@dataclass(frozen=True)
class GoalState:
    """一条可由连续规划器验证的终局棋盘约束边。

    ``expected_own_after_state`` 和 ``expected_after_reply_state`` 都是离散
    棋盘状态 id，不是保证；出手后必须按真实 PhysX 棋盘重新分类。
    """

    transition_id: str
    priority: int
    source_state: str
    expected_own_after_state: str
    expected_after_reply_state: str | None
    stone_constraints: tuple[StoneConstraint, ...] = ()
    occupancy_constraints: tuple[OccupancyConstraint, ...] = ()
    forbidden_outcomes: tuple[str, ...] = ()
    fallback_transition_ids: tuple[str, ...] = ()
    require_last_reply_search: bool = False
    last_reply_policy: LastReplyPolicy = "REQUIRE_SEARCH_RECORD"
    evidence_status: Literal["HISTORICAL_TEMPLATE", "PHYSX_VALIDATED"] = "HISTORICAL_TEMPLATE"
    notes: str = ""
    schema: str = field(default="goal_state_tactics_v0", init=False)

    def __post_init__(self) -> None:
        if not self.transition_id:
            raise ValueError("transition_id 不能为空")
        if self.priority < 1:
            raise ValueError("priority 从 1 开始")
        if not self.source_state or not self.expected_own_after_state:
            raise ValueError("source_state 和 expected_own_after_state 不能为空")
        selector_ids = [item.selector.selector_id for item in self.stone_constraints]
        if len(selector_ids) != len(set(selector_ids)):
            raise ValueError("同一 GoalState 不可对同一个 selector 重复施加约束")
        if self.transition_id in self.fallback_transition_ids:
            raise ValueError("GoalState 不能把自己列为回退")
        if not self.require_last_reply_search and self.last_reply_policy != "REQUIRE_SEARCH_RECORD":
            raise ValueError("未要求末壶搜索的 GoalState 不能声明 REQUIRE_NO_COUNTERPLAY")

    def to_json(self) -> dict[str, object]:
        return {
            "schema": self.schema,
            "transition_id": self.transition_id,
            "priority": self.priority,
            "source_state": self.source_state,
            "expected_own_after_state": self.expected_own_after_state,
            "expected_after_reply_state": self.expected_after_reply_state,
            "stone_constraints": [item.to_json() for item in self.stone_constraints],
            "occupancy_constraints": [item.to_json() for item in self.occupancy_constraints],
            "forbidden_outcomes": list(self.forbidden_outcomes),
            "fallback_transition_ids": list(self.fallback_transition_ids),
            "require_last_reply_search": self.require_last_reply_search,
            "last_reply_policy": self.last_reply_policy,
            "evidence_status": self.evidence_status,
            "notes": self.notes,
        }
