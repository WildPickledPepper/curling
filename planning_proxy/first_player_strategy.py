#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""先手中线控场策略的状态机。

这个模块只定义“这一颗壶要修复什么局面”，不自己假装计算碰撞。真正的
BESTSHOT 仍由白盒粗筛和严格 PhysX 产生。这样第七、第八颗不会变成写死的
坐标，而是根据对方刚刚拆掉的层来选择目标。

``shot_index`` 是全局零基投壶序号；本模块仅接受先手方自己的偶数序号
``0, 2, ..., 14``。
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Iterable, Mapping, Sequence

from planning_proxy.competition_rules import HOUSE_R, HOUSE_X, HOUSE_Y, STONE_R, is_in_free_guard_zone, touches_centre_line


INNER_RING_R = 0.610
GUARD_TARGET = (HOUSE_X, 7.15)
# 前后、左右都错开的一对红圈得分槽。镜像版本用于一侧被挡住时。
HOUSE_PAIR_LEFT = ((2.28, 4.70), (2.67, 5.18))
HOUSE_PAIR_RIGHT = ((2.47, 4.70), (2.08, 5.18))
# 第六/第七/第八颗用于保护直线入口的前方偏侧位置。
# 不是把“滚位”锁死到一个坐标。每侧给三个可接受的保护槽：靠前、靠中、
# 靠内。它们共同的几何要求是：位于两颗红圈壶前方、偏侧，且不和两颗得分
# 壶排成一条直线。严格层命中任一槽都可进入最终排序。
FRONT_GUARD_LEFT = ((1.82, 6.42), (1.92, 6.12), (2.08, 5.92))
FRONT_GUARD_RIGHT = ((2.93, 6.42), (2.83, 6.12), (2.67, 5.92))
EDGE_DEAD_LEFT = (0.195, 0.435)
EDGE_DEAD_RIGHT = (4.315, 4.555)


@dataclass(frozen=True)
class StrategyStone:
    index: int
    owner: str
    x: float
    y: float
    enabled: bool = True


@dataclass(frozen=True)
class DefenceShape:
    """下一颗壶可尝试达成的一种防御球形。

    ``active_targets`` 是本次出手壶的可接受终点集合；其余条件由场上既有壶
    与这颗新壶共同检查。多个 shape 是“或”关系：严格物理只要稳定达成其中
    一种，便可以作为候选解进入最终排序。
    """

    name: str
    description: str
    active_targets: tuple[tuple[float, float], ...]
    required_inner_count: int
    require_front_guard: bool = False
    require_centre_anchor: bool = False
    require_centre_guard: bool = False
    required_side_gate_count: int = 0
    # 仅当完整球形已通过“对方最后一颗反击”筛查时才为真。第八颗使用它
    # 作为提交门槛；此前各颗仍可把普通形状当作过渡层。
    certified_for_last_reply: bool = False

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "active_targets": [list(point) for point in self.active_targets],
            "required_inner_count": self.required_inner_count,
            "require_front_guard": self.require_front_guard,
            "require_centre_anchor": self.require_centre_anchor,
            "require_centre_guard": self.require_centre_guard,
            "required_side_gate_count": self.required_side_gate_count,
            "certified_for_last_reply": self.certified_for_last_reply,
        }

    @classmethod
    def from_json(cls, raw: Mapping[str, object]) -> "DefenceShape":
        points = tuple(
            (float(point[0]), float(point[1]))
            for point in raw.get("active_targets", [])
            if isinstance(point, (list, tuple)) and len(point) == 2
        )
        return cls(
            name=str(raw["name"]),
            description=str(raw["description"]),
            active_targets=points,
            required_inner_count=int(raw["required_inner_count"]),
            require_front_guard=bool(raw.get("require_front_guard", False)),
            require_centre_anchor=bool(raw.get("require_centre_anchor", False)),
            require_centre_guard=bool(raw.get("require_centre_guard", False)),
            required_side_gate_count=int(raw.get("required_side_gate_count", 0)),
            certified_for_last_reply=bool(raw.get("certified_for_last_reply", False)),
        )


@dataclass(frozen=True)
class FirstPlayerPlan:
    """一颗先手壶的战术目标。

    ``target_opponent_index`` 是需要重点处理的对方壶；它不是一律要求物理
    出界：前五次投壶中的普通自由防守区守壶只能被推到边缘废球带。
    """

    shot_index: int
    own_throw_number: int
    phase: str
    target_points: tuple[tuple[float, float], ...]
    target_opponent_index: int | None
    opponent_action: str
    rationale: str
    defence_shapes: tuple[DefenceShape, ...] = ()

    def to_json(self) -> dict:
        result = asdict(self)
        result["target_points"] = [list(point) for point in self.target_points]
        result["defence_shapes"] = [shape.to_json() for shape in self.defence_shapes]
        return result

    @classmethod
    def from_json(cls, raw: Mapping[str, object]) -> "FirstPlayerPlan":
        points = tuple((float(point[0]), float(point[1])) for point in raw.get("target_points", []) if isinstance(point, (list, tuple)) and len(point) == 2)
        return cls(
            shot_index=int(raw["shot_index"]),
            own_throw_number=int(raw["own_throw_number"]),
            phase=str(raw["phase"]),
            target_points=points,
            target_opponent_index=None if raw.get("target_opponent_index") is None else int(raw["target_opponent_index"]),
            opponent_action=str(raw["opponent_action"]),
            rationale=str(raw["rationale"]),
            defence_shapes=tuple(DefenceShape.from_json(shape) for shape in raw.get("defence_shapes", []) if isinstance(shape, Mapping)),
        )


def _as_stones(board: Iterable[object]) -> list[StrategyStone]:
    result: list[StrategyStone] = []
    for item in board:
        if isinstance(item, Mapping):
            result.append(StrategyStone(int(item["index"]), str(item["owner"]), float(item["x"]), float(item["y"]), bool(item.get("enabled", True))))
        else:
            result.append(StrategyStone(int(getattr(item, "index")), str(getattr(item, "owner")), float(getattr(item, "x")), float(getattr(item, "y")), bool(getattr(item, "enabled", True))))
    return [stone for stone in result if stone.enabled]


def distance_to_house(stone: StrategyStone) -> float:
    return math.hypot(stone.x - HOUSE_X, stone.y - HOUSE_Y)


def is_in_inner_ring(stone: StrategyStone) -> bool:
    return distance_to_house(stone) <= INNER_RING_R + STONE_R


def is_in_house(stone: StrategyStone) -> bool:
    return distance_to_house(stone) <= HOUSE_R + STONE_R


def is_edge_dead(stone: StrategyStone) -> bool:
    return (EDGE_DEAD_LEFT[0] <= stone.x <= EDGE_DEAD_LEFT[1]) or (EDGE_DEAD_RIGHT[0] <= stone.x <= EDGE_DEAD_RIGHT[1])


def _target_pair(stones: Sequence[StrategyStone]) -> tuple[tuple[float, float], tuple[float, float]]:
    """根据当前障碍选择左右镜像红圈布局。"""

    left_pressure = sum(1 for stone in stones if stone.owner == "opponent" and stone.x < HOUSE_X and not is_edge_dead(stone))
    right_pressure = sum(1 for stone in stones if stone.owner == "opponent" and stone.x > HOUSE_X and not is_edge_dead(stone))
    return HOUSE_PAIR_RIGHT if left_pressure > right_pressure else HOUSE_PAIR_LEFT


def _front_guard_targets(stones: Sequence[StrategyStone]) -> tuple[tuple[float, float], ...]:
    """保护壶落在与主要得分壶相反的一侧，避免三个己方壶排成一线。"""

    own_house = [stone for stone in stones if stone.owner == "self" and is_in_inner_ring(stone)]
    if own_house:
        mean_x = sum(stone.x for stone in own_house) / len(own_house)
        return FRONT_GUARD_RIGHT if mean_x <= HOUSE_X else FRONT_GUARD_LEFT
    return FRONT_GUARD_LEFT


def _unique_points(*groups: Sequence[tuple[float, float]]) -> tuple[tuple[float, float], ...]:
    """合并候选落点，同时保持声明这些落点时的优先顺序。"""

    result: list[tuple[float, float]] = []
    for group in groups:
        for point in group:
            if point not in result:
                result.append(point)
    return tuple(result)


def _defence_shapes(stones: Sequence[StrategyStone]) -> tuple[DefenceShape, ...]:
    """按己方当前在场壶数，给第六至第八颗生成可替代的防御球形。

    这些不是必须依次完成的待办项，而是交给搜索器的“或”目标。比如已经有
    两颗己方壶时，搜索器可以尝试补左侧三角、补右侧三角，或补第三颗错层
    红圈壶；严格 PhysX 中任一形状稳定成立即可通过战术检查。
    """

    own_count = sum(stone.owner == "self" and not is_edge_dead(stone) for stone in stones)
    pair = _target_pair(stones)

    if own_count <= 1:
        return (
            DefenceShape(
                "单壶_双红圈错层",
                "已有的一颗与新壶分别占红圈两侧，形成前后、左右错开的两颗得分壶。",
                pair,
                required_inner_count=2,
            ),
            DefenceShape(
                "单壶_左侧护门",
                "保留已有内圈锚点，新壶落在左前方偏侧，堵住一条直线击打入口。",
                FRONT_GUARD_LEFT,
                required_inner_count=1,
                require_front_guard=True,
            ),
            DefenceShape(
                "单壶_右侧护门",
                "保留已有内圈锚点，新壶落在右前方偏侧，堵住另一侧直线击打入口。",
                FRONT_GUARD_RIGHT,
                required_inner_count=1,
                require_front_guard=True,
            ),
        )

    if own_count == 2:
        return (
            DefenceShape(
                "双壶_左侧三角",
                "两颗已有壶作为底，第三颗落左前方，形成左偏的防御三角。",
                FRONT_GUARD_LEFT,
                required_inner_count=1,
                require_front_guard=True,
            ),
            DefenceShape(
                "双壶_右侧三角",
                "两颗已有壶作为底，第三颗落右前方，形成右偏的防御三角。",
                FRONT_GUARD_RIGHT,
                required_inner_count=1,
                require_front_guard=True,
            ),
            DefenceShape(
                "双壶_第三红圈错层",
                "不在中心堆壶，而是在红圈另一侧补第三颗错层得分壶。",
                pair,
                required_inner_count=3,
            ),
        )

    # 三颗及以上时不再执着于把壶都堆到中心。优先补左右任一侧的外壳；
    # 首选是已经经末手反击筛查的“中心锚＋中线守壶＋左右双门”。它需要
    # 四个相对角色；一手无法补齐时会自然不达标，搜索器再退到普通外壳/红圈
    # 后备候选，而不是伪造成功。
    return (
        DefenceShape(
            "三壶以上_中心锚双门",
            "优先完成中心锚、中线守壶与左右双门；它是目前唯一通过末手反击筛查的候选防线。",
            _unique_points(((HOUSE_X, HOUSE_Y),), FRONT_GUARD_LEFT, FRONT_GUARD_RIGHT),
            required_inner_count=1,
            require_centre_anchor=True,
            require_centre_guard=True,
            required_side_gate_count=2,
            certified_for_last_reply=True,
        ),
        DefenceShape(
            "三壶以上_左侧外壳",
            "在既有壶群左前方补保护壶，保持侧向通道被遮挡。",
            FRONT_GUARD_LEFT,
            required_inner_count=2,
            require_front_guard=True,
        ),
        DefenceShape(
            "三壶以上_右侧外壳",
            "在既有壶群右前方补保护壶，保持另一侧通道被遮挡。",
            FRONT_GUARD_RIGHT,
            required_inner_count=2,
            require_front_guard=True,
        ),
        DefenceShape(
            "三壶以上_红圈后备",
            "在不碰撞聚堆的前提下补一颗错层红圈壶，给最终计分留下后备。",
            pair,
            required_inner_count=3,
        ),
    )


def _priority_opponent(stones: Sequence[StrategyStone]) -> StrategyStone | None:
    """先处理红圈/大本营威胁；边缘废球不是当前主要目标。"""

    enemies = [stone for stone in stones if stone.owner == "opponent" and not is_edge_dead(stone)]
    if not enemies:
        return None
    return min(
        enemies,
        key=lambda stone: (
            0 if is_in_inner_ring(stone) else 1 if is_in_house(stone) else 2 if is_in_free_guard_zone(stone.x, stone.y) else 3,
            distance_to_house(stone),
        ),
    )


def _opponent_action(target: StrategyStone | None, shot_index: int) -> str:
    if target is None:
        return "none"
    if shot_index <= 4 and is_in_free_guard_zone(target.x, target.y):
        # 中线守壶在保护期内不能被撞离中线；普通守壶可被推到边缘，但不能出界。
        return "avoid_protected_centre_guard" if touches_centre_line(target.x) else "push_to_edge_dead"
    return "physical_clear"


def _has_front_guard(stones: Sequence[StrategyStone]) -> bool:
    return any(
        stone.owner == "self"
        and abs(stone.y - GUARD_TARGET[1]) <= 1.25
        and abs(stone.x - HOUSE_X) >= 0.20
        for stone in stones
    )


def _has_centre_anchor(stones: Sequence[StrategyStone]) -> bool:
    """是否已有一颗己方壶真正占住按钮附近。"""

    return any(stone.owner == "self" and distance_to_house(stone) <= 0.25 for stone in stones)


def _has_centre_guard(stones: Sequence[StrategyStone]) -> bool:
    """是否还保有第一颗建立的中线守壶，而不是只剩侧门壶。"""

    return any(
        stone.owner == "self"
        and abs(stone.x - GUARD_TARGET[0]) <= 0.25
        and abs(stone.y - GUARD_TARGET[1]) <= 0.60
        for stone in stones
    )


def _side_gate_count(stones: Sequence[StrategyStone]) -> int:
    """数出左右两个前方门中已有几个；同一颗壶不会重复计数。"""

    count = 0
    for targets in (FRONT_GUARD_LEFT, FRONT_GUARD_RIGHT):
        if any(
            stone.owner == "self"
            and min(math.hypot(stone.x - x, stone.y - y) for x, y in targets) <= 0.55
            for stone in stones
        ):
            count += 1
    return count


def _own_inner_count(stones: Sequence[StrategyStone]) -> int:
    return sum(1 for stone in stones if stone.owner == "self" and is_in_inner_ring(stone))


def _self_is_closest(stones: Sequence[StrategyStone]) -> bool:
    in_house = [stone for stone in stones if is_in_house(stone)]
    return bool(in_house) and min(in_house, key=distance_to_house).owner == "self"


def plan_first_player_turn(board: Iterable[object], shot_index: int) -> FirstPlayerPlan:
    """为先手方的下一颗壶生成可执行的战术意图。

    它处理的是“该补什么层”，不是直接输出物理输入。调用端将
    ``target_points`` 和 ``target_opponent_index`` 交给粗筛/严格 PhysX。
    """

    if not 0 <= int(shot_index) <= 14 or int(shot_index) % 2:
        raise ValueError("先手策略只接受我方的偶数全局投壶序号 0,2,...,14")
    stones = _as_stones(board)
    own_throw = int(shot_index) // 2 + 1
    target = _priority_opponent(stones)
    opponent_action = _opponent_action(target, int(shot_index))
    pair = _target_pair(stones)

    if own_throw == 1:
        return FirstPlayerPlan(int(shot_index), own_throw, "open_centre_guard", (GUARD_TARGET,), None, "none", "第一颗占中线守壶；之后的保护规则才有可利用的支点。")

    if own_throw == 2:
        target_point = pair[0]
        if opponent_action == "physical_clear":
            text = "对方第一颗已进大本营：优先物理清出，同时让出手壶尽量滚入第一红圈槽。"
        elif opponent_action == "push_to_edge_dead":
            text = "对方第一颗是受保护的普通自由防守区守壶：推入边缘废球带，不可打出界；出手壶争取第一红圈槽。"
        else:
            text = "对方中线守壶仍受保护，避免把它撞离中线；直接建立第一红圈得分壶。"
        return FirstPlayerPlan(int(shot_index), own_throw, "process_first_enemy_and_score", (target_point,), None if opponent_action == "avoid_protected_centre_guard" else (target.index if target else None), opponent_action, text)

    if own_throw == 3:
        return FirstPlayerPlan(int(shot_index), own_throw, "complete_staggered_house_pair", (pair[1],), target.index if target and opponent_action != "avoid_protected_centre_guard" else None, opponent_action, "保护期的最后一颗：优先补第二红圈壶，并与第一颗前后、左右错开；只有明显敌方得分威胁才顺带处理。")

    if own_throw in (4, 5):
        if target is not None:
            return FirstPlayerPlan(int(shot_index), own_throw, "reclaim_centre_or_clear_threat", (pair[0], pair[1]), target.index, "physical_clear", "保护期结束后，先处理对方上一颗仍有效的壶；若它已占红圈，则优先清出或重新取得最近壶。")
        if _own_inner_count(stones) < 2:
            return FirstPlayerPlan(int(shot_index), own_throw, "restore_second_scoring_stone", (pair[1],), None, "none", "己方红圈壶不足两颗，补另一侧得分层，不把壶堆在同一条直线上。")
        return FirstPlayerPlan(int(shot_index), own_throw, "maintain_centre_advantage", (pair[0],), None, "none", "当前中心层仍完整；用更靠中心或轻微错层的壶维持优势。")

    # 从第六颗开始，不再把滚位锁成一个固定点。根据己方现有 1/2/3 颗在场壶
    # 提供多个阵型；这些阵型是替代解，粗筛和严格 PhysX 都会把它们一起搜索。
    defence_shapes = _defence_shapes(stones)
    defence_targets = _unique_points(*(shape.active_targets for shape in defence_shapes))
    if own_throw == 6:
        return FirstPlayerPlan(
            int(shot_index), own_throw, "sixth_clear_and_choose_defence_shape", defence_targets,
            target.index if target else None, "physical_clear" if target else "none",
            "第六颗先处理对方第五颗；随后在当前壶数对应的多个防御形中任选一个稳定完成，而不是死守单一滚位。",
            defence_shapes,
        )

    # 第七、第八颗：上一颗对方有效壶仍是首先处理的对象；击打后的滚位由
    # “当前壶数对应的多个防御形”决定，而不是按一个固定坐标修补。
    target_index = target.index if target is not None else None
    target_action = "physical_clear" if target is not None else "none"
    return FirstPlayerPlan(
        int(shot_index), own_throw, "clear_then_choose_defence_shape", defence_targets,
        target_index, target_action,
        "先处理对方上一颗有效壶；再从与当前己方壶数匹配的多个防御形中，选择严格物理下最稳的一种。",
        defence_shapes,
    )


def tactical_coarse_score(stop_x: float, stop_y: float, first_hit_index: int, base_score: float, plan: FirstPlayerPlan) -> float:
    """给粗筛的轻量加分；严格 PhysX 仍负责真正的碰撞与终局排序。"""

    # 旧粗筛天生偏好“首撞敌方”。第七/八颗若只是补保护壶或红圈层，继续
    # 沿用它会把一条无意义的清外圈路线排在防守落点之前，因此此类回合改为
    # 纯落点优先并显式惩罚先撞任何已有壶。
    if plan.opponent_action == "none":
        score = -120.0 if int(first_hit_index) >= 0 else 0.0
    else:
        score = float(base_score)
    if plan.target_opponent_index is not None and int(first_hit_index) == plan.target_opponent_index:
        score += 250.0
    if plan.target_points:
        landing_error = min(math.hypot(stop_x - x, stop_y - y) for x, y in plan.target_points)
        score -= 45.0 * landing_error
    return score


def score_strict_outcome(
    final_states: Sequence[Mapping[str, object]],
    initial_board: Iterable[object],
    active_index: int,
    plan: FirstPlayerPlan,
) -> tuple[float, bool]:
    """给严格 PhysX 终局打先手战术分。

    分数只用于在已经合法、满足同一己方损失档的候选之间排序；它不放宽
    ``strict_refine`` 的自由防守区和出界安全约束。返回的布尔值是本轮主要
    目标是否在该摩擦序列下实现，供多种子取最差值。
    """

    initial = _as_stones(initial_board)
    owners = {stone.index: stone.owner for stone in initial}
    owners[int(active_index)] = "self"
    final: list[StrategyStone] = []
    for index, state in enumerate(final_states):
        if bool(state.get("enabled", False)):
            final.append(StrategyStone(index, owners.get(index, "unknown"), float(state["x"]), float(state["y"])))

    own = [stone for stone in final if stone.owner == "self"]
    enemy = [stone for stone in final if stone.owner == "opponent"]
    own_inner = sum(is_in_inner_ring(stone) for stone in own)
    own_closest = bool(own) and (not enemy or min(own + enemy, key=distance_to_house).owner == "self")
    guard_present = _has_front_guard(final)
    active = next((stone for stone in final if stone.index == int(active_index)), None)
    landing_error = math.inf if active is None or not plan.target_points else min(
        math.hypot(active.x - point[0], active.y - point[1]) for point in plan.target_points
    )

    target_ok = True
    if plan.target_opponent_index is not None:
        target = next((stone for stone in final if stone.index == plan.target_opponent_index), None)
        if plan.opponent_action == "physical_clear":
            target_ok = target is None
        elif plan.opponent_action == "push_to_edge_dead":
            target_ok = target is not None and is_edge_dead(target)

    landing_ok = not plan.target_points or (active is not None and landing_error <= 0.70)

    # 第六至第八颗的多个防御形是“或”关系。每一个都要求本次出手壶靠近
    # 它自己的落点槽，且场面满足它声明的内圈数/保护层条件。
    def shape_is_met(shape: DefenceShape) -> bool:
        if active is None or not shape.active_targets:
            return False
        shape_landing_error = min(math.hypot(active.x - point[0], active.y - point[1]) for point in shape.active_targets)
        return (
            shape_landing_error <= 0.70
            and own_inner >= shape.required_inner_count
            and (not shape.require_front_guard or guard_present)
            and (not shape.require_centre_anchor or _has_centre_anchor(final))
            and (not shape.require_centre_guard or _has_centre_guard(final))
            and _side_gate_count(final) >= shape.required_side_gate_count
        )

    matched_shapes = tuple(shape for shape in plan.defence_shapes if shape_is_met(shape))
    shapes_met = tuple(shape.name for shape in matched_shapes)
    if plan.defence_shapes:
        # 第八颗就是对方最后一颗前的最终布阵。此时普通三角只是“壶还在场”
        # 的描述，不能被当作已通过反击筛查的交付目标。
        goal_met = target_ok and bool(shapes_met) and (
            plan.own_throw_number < 8 or any(shape.certified_for_last_reply for shape in matched_shapes)
        )
    elif plan.phase == "open_centre_guard":
        goal_met = landing_ok
    elif plan.phase == "process_first_enemy_and_score":
        goal_met = target_ok and landing_ok
    elif plan.phase in {"clear_then_repair_closest_scoring_anchor", "reclaim_centre_or_clear_threat"}:
        goal_met = target_ok and own_closest and landing_ok
    elif plan.phase in {"clear_then_repair_second_inner_stone", "restore_second_scoring_stone", "complete_staggered_house_pair"}:
        goal_met = target_ok and own_inner >= 2 and landing_ok
    elif plan.phase in {"clear_then_repair_front_protector", "clear_then_reinforce_final_defence"}:
        goal_met = target_ok and own_closest and own_inner >= 2 and guard_present and landing_ok
    else:
        goal_met = landing_ok

    score = 0.0
    score += 240.0 if target_ok else -240.0
    score += 120.0 if own_closest else -120.0
    score += 55.0 * min(2, own_inner)
    score += 45.0 if guard_present else 0.0
    score += 65.0 if shapes_met else 0.0
    score += 260.0 if any(shape.certified_for_last_reply for shape in matched_shapes) else 0.0
    if math.isfinite(landing_error):
        score -= 70.0 * landing_error
    else:
        score -= 200.0
    return score, bool(goal_met)
