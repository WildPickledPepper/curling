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
# 目标槽是允许存在摩擦/碰撞余量的区域，而不是任意进入大本营就算成功。
# 30cm 仍能给前方壶被带入营内留出缓冲，却不会把 40cm 以上的碰后漂移
# 误报为“定向滚位”。
DEFAULT_LANDING_REGION_RADIUS_M = 0.30
GUARD_TARGET = (HOUSE_X, 7.15)
# P1 是空场直线投壶，不应让“清敌/营内得分”的通用搜索把它推到大本营。
# 这组输入在严格 PhysX 空场、种子 0..8 下标定到 GUARD_TARGET：最大落点
# 误差 5.2 cm。P1 在线直接发送它；后续有壶的回合才进入连续候选搜索。
OPENING_CENTRE_GUARD_SHOT = (2.739, -0.0243, 0.0)
# 两颗内圈得分壶沿红圈对角分布，而不是挤在按钮附近或横向排成一排。壶心
# 离圆心约 0.49m，两个对角点相距约 0.99m：既保留内圈得分质量，又使从
# 上方直入的一次撞击不容易把两颗壶串成双飞。镜像版本用于一侧被挡住时，且
# P2 的第一颗总是落到相应一侧。
HOUSE_PAIR_LEFT = ((2.00, 5.20), (2.75, 4.56))
HOUSE_PAIR_RIGHT = ((2.75, 5.20), (2.00, 4.56))
# K1 中线守壶仍在、对手没有有效壶时，K2 不是空场直 draw。严格 PhysX 对
# 该绕壶通道标定出的第一红圈锚在此处；在线仍以区域而非精确点验收。
K2_AROUND_CENTRE_GUARD_ANCHOR = (1.932, 4.715)
# 对手清掉 K2 锚后若在侧前外环留下得分壶，K3 不能只尝试“滚到相反侧内圈”。
# 薄撞时，同侧前营控制槽也是独立的、可得分的后继状态：它保留了中线守壶
# 与一颗前营锚之间的遮挡关系。两个槽都是按大本营角色定义的镜像区域，在线
# 仍由严格 PhysX 决定当前碰撞实际可达哪一个，绝不把历史落点当作直接出手。
K3_CLEAR_LEFT_TO_RIGHT_INNER_ANCHOR = (2.535, 4.985)
K3_CLEAR_RIGHT_TO_LEFT_INNER_ANCHOR = (2.215, 4.985)
K3_CLEAR_LEFT_TO_LEFT_FRONT_ANCHOR = (1.800, 5.250)
K3_CLEAR_RIGHT_TO_RIGHT_FRONT_ANCHOR = (2.950, 5.250)
# K3 清掉侧前威胁后，原有中线守壶仍在时还应尝试回到它后方的恢复走廊。
# 这不是某局历史落点：它以按钮和中线角色定义，给严格 PhysX 的薄撞滚位
# 一段连续可达区域；最终仍必须清目标、成为最近壶并通过全部摩擦种子。
K3_GUARD_ALIGNED_RECOVERY_CORRIDOR = (
    (HOUSE_X, HOUSE_Y + 0.24),
    (HOUSE_X, HOUSE_Y - 0.02),
    (HOUSE_X - 0.155, HOUSE_Y + 0.12),
    (HOUSE_X + 0.155, HOUSE_Y + 0.12),
)
K5_CLEAR_LEFT_TO_LEFT_INNER_ANCHOR = (1.780, 5.330)
K5_CLEAR_RIGHT_TO_RIGHT_INNER_ANCHOR = (2.970, 5.330)
# K4 清侧守壶后，K5 无敌壶时采用历史主 G 的第二营内控制槽。当前第一
# 锚在左侧时，新壶仍落在左后控制位，而不是旧版右前 `(2.65, 4.855)`：
# 后者在 PPO 回放中被下一壶直接单清。左右仅作镜像，仍须严格 PhysX 验收。
K5_HISTORICAL_SECOND_LAYER_LEFT = (2.139136, 5.123235)
K5_HISTORICAL_SECOND_LAYER_RIGHT = (2.610864, 5.123235)
# K8 的可达降级终局：历史中的“清壶后两层营内”不可能由一颗壶完成时，
# 清威胁并让出手壶留在同侧**大本营外圈**、成为最近壶。该槽离按钮约
# 1.17m，不是内圈；它来自本地 PPO 轨迹上的严格三摩擦 hit-and-roll 与
# 末壶回复筛查，不被称作通用安全壳。
K8_CLEAR_LEFT_TO_LEFT_HOUSE_ROLL = (1.770, 5.880)
K8_CLEAR_RIGHT_TO_RIGHT_HOUSE_ROLL = (2.980, 5.880)
# NWNHT K8 赢方反推：当场上已经有己方前左（或镜像前右）壶、对手只剩
# 一枚营内威胁时，历史的高价值 G8 是单清后补齐另一侧前营壶，而不是清后
# 只留下出手壶。精细落点不能跨局写成固定全局点：严格 PhysX 在真实历史
# 夹具中显示出手壶自然停在被清目标的前方约 0.30m。因此以目标壶为参照
# 生成相对滚位，而完整“前左/前右各一壶”的盘面谓词仍是硬约束。
K8_FRONT_PAIR_ROLL_AHEAD_M = 0.30
K8_FRONT_PAIR_REGION_RADIUS_M = 0.35
HISTORICAL_BUTTON_RADIUS_M = 0.610
# K7 历史状态 ``OPPONENT_HOUSE_THREAT`` 的高支持 G：清掉唯一营内威胁，
# 再让出手壶停在历史控制细圆取得最近壶。该点不是泛化 draw；仅用于“无
# 己方内圈壶、两颗己方残壶、仍有中线锚”的窄残局。当前 PPO 轨迹已用
# 三摩擦 PhysX 认证其精确碰撞拓扑。
# K7_V2_OPPONENT_HOUSE_THREAT_81 的高支持细圆（已按本地按钮坐标反变换）。
# 它不是按钮：清掉唯一营内威胁后，出手壶停在这个前左控制槽即可成为最近壶。
K7_CLEAR_TO_HISTORICAL_CONTROL = (2.136679, 5.285392)
K7_CLEAR_TO_HISTORICAL_CONTROL_MIRROR = (2.613321, 5.285392)
# K6 历史主 G 的细圆。它与当前常见的对方内圈壶相交，因此不是净空 draw
# 目标；应作为 promote/raise 的碰后出手壶终点，并要求对方壶被推出原位。
K6_PROMOTE_TO_HISTORICAL_CONTROL = (2.567868, 5.307504)
# K4 的侧守壶清除滚位。该分支只用于“一内圈锚 + 中线守壶 + 对方单侧守壶”
# 的已回放构型：清守壶后出手壶停在同侧高外环，避免继续堆第二颗营内壶。
K4_CLEAR_LEFT_SIDE_GUARD_OUTER_ROLL = (1.500, 7.700)
K4_CLEAR_RIGHT_SIDE_GUARD_OUTER_ROLL = (3.250, 7.700)
# 第六/第七/第八颗用于保护直线入口的前方偏侧位置。
# 不是把“滚位”锁死到一个坐标。每侧给三个可接受的保护槽：靠前、靠中、
# 靠内。它们共同的几何要求是：位于两颗红圈壶前方、偏侧，且不和两颗得分
# 壶排成一条直线。严格层命中任一槽都可进入最终排序。
FRONT_GUARD_LEFT = ((1.82, 6.42), (1.92, 6.12), (2.08, 5.92))
FRONT_GUARD_RIGHT = ((2.93, 6.42), (2.83, 6.12), (2.67, 5.92))
# 第五颗处理前场侧守壶时，薄撞的自然滚位可能停在普通侧门槽的上方。
# 这不是“第三颗红圈壶”，而是清壶后仍保留压力的左/右前肩位。两侧仅是
# 状态机的镜像目标；每次实际提交仍须由严格 PhysX 认证。
FRONT_SHOULDER_LEFT = ((1.88, 6.98),)
FRONT_SHOULDER_RIGHT = ((2.87, 6.98),)
EDGE_DEAD_LEFT = (0.195, 0.435)
EDGE_DEAD_RIGHT = (4.315, 4.555)
# 这是策略层的“后方废球线”，不是 Unity 物理禁用边界。壶心越过该线后，
# 壶盘已完全不可能与大本营相交，不再计分，也不应继续被当作待清目标。
BACK_HOUSE_DEAD_Y = HOUSE_Y - HOUSE_R - STONE_R


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
    # 每个槽是圆形落点区域的中心；壶心进入该半径即算完成该防御角色。
    landing_region_radius_m: float = DEFAULT_LANDING_REGION_RADIUS_M
    require_front_guard: bool = False
    require_centre_anchor: bool = False
    require_centre_guard: bool = False
    # ``require_centre_guard`` 只描述终局存在中线守壶；若本手撞动了原守壶，
    # 出手壶本身也可能恰好落进该区域。需要保留既有屏风角色的合同应显式
    # 要求入局时那颗中线守壶仍在其原功能区，而不是让新壶冒充它。
    preserve_initial_centre_guard: bool = False
    required_side_gate_count: int = 0
    # 与 NWNHT 的 K8 全盘面谓词同义的营内扇区计数。它们不拿“两个己方
    # 壶都在营内”偷换“前左/前右各一壶”。
    required_own_front_left_count: int = 0
    required_own_front_right_count: int = 0
    max_opponent_house_count: int | None = None
    # 仅表示该**基准模板**曾通过离线的“对方最后一颗反击”筛查。它不等于
    # 当前真实壶面已经验收：残留敌壶、旧壶 yaw 和本手碰撞后的偏差都会改变
    # 反击路线，最终提交仍必须对实际终局重跑反击搜索。
    certified_for_last_reply: bool = False

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "active_targets": [list(point) for point in self.active_targets],
            "required_inner_count": self.required_inner_count,
            "landing_region_radius_m": self.landing_region_radius_m,
            "require_front_guard": self.require_front_guard,
            "require_centre_anchor": self.require_centre_anchor,
            "require_centre_guard": self.require_centre_guard,
            "preserve_initial_centre_guard": self.preserve_initial_centre_guard,
            "required_side_gate_count": self.required_side_gate_count,
            "required_own_front_left_count": self.required_own_front_left_count,
            "required_own_front_right_count": self.required_own_front_right_count,
            "max_opponent_house_count": self.max_opponent_house_count,
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
            landing_region_radius_m=float(raw.get("landing_region_radius_m", DEFAULT_LANDING_REGION_RADIUS_M)),
            require_front_guard=bool(raw.get("require_front_guard", False)),
            require_centre_anchor=bool(raw.get("require_centre_anchor", False)),
            require_centre_guard=bool(raw.get("require_centre_guard", False)),
            preserve_initial_centre_guard=bool(raw.get("preserve_initial_centre_guard", False)),
            required_side_gate_count=int(raw.get("required_side_gate_count", 0)),
            required_own_front_left_count=int(raw.get("required_own_front_left_count", 0)),
            required_own_front_right_count=int(raw.get("required_own_front_right_count", 0)),
            max_opponent_house_count=None if raw.get("max_opponent_house_count") is None else int(raw["max_opponent_house_count"]),
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
    # ``target_points`` 是多个可替代圆形落点区域的中心，不是必须精确命中的
    # 单点。碰撞滚位只要稳定进入其中任一区域即可。
    landing_region_radius_m: float = DEFAULT_LANDING_REGION_RADIUS_M
    defence_shapes: tuple[DefenceShape, ...] = ()
    # 这三个字段把原有“下一颗目标”提升为可供策略层直接消费的状态机边。
    # 物理求解器仍只需要 target_points / target_opponent_index。
    situation_type: str = ""
    strategy_type: str = ""
    desired_state_type: str = ""
    # ``None`` 表示由执行层依壶数决定可接受的一换一预算；非空时是这条
    # 状态转移的硬上限。它用于阻止“处理一颗敌壶”悄悄吞掉已建立的得分锚。
    max_own_cleared: int | None = None

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
            landing_region_radius_m=float(raw.get("landing_region_radius_m", DEFAULT_LANDING_REGION_RADIUS_M)),
            defence_shapes=tuple(DefenceShape.from_json(shape) for shape in raw.get("defence_shapes", []) if isinstance(shape, Mapping)),
            situation_type=str(raw.get("situation_type", "")),
            strategy_type=str(raw.get("strategy_type", "")),
            desired_state_type=str(raw.get("desired_state_type", "")),
            max_own_cleared=None if raw.get("max_own_cleared") is None else int(raw["max_own_cleared"]),
        )


@dataclass(frozen=True)
class FirstPlayerSituation:
    """先手回合的离散局面分类。

    类型只描述当前 end 内、当前壶面可观察到的结构；它不把比分、冰况或
    未公开的人类临场偏好伪装成确定规则。策略层因此可以立即选择“要做哪类
    事情”，而连续 ``v/h/w`` 仍交给白盒求解器。
    """

    shot_index: int
    own_throw_number: int
    situation_type: str
    strategy_type: str
    desired_state_type: str
    target_opponent_index: int | None
    opponent_action: str
    rationale: str

    def to_json(self) -> dict:
        return asdict(self)


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


def _front_house_sector_count(stones: Sequence[StrategyStone], owner: str, side: str) -> int:
    """按历史状态抽象计数前左/前右大本营扇区。

    这套扇区专门服务 K8 的完整 G8 合同：排除按钮小圆，要求在 T 线前，
    并区分左右。它不是 ``own_inner_count`` 的替代品。
    """

    sign = -1 if side == "left" else 1
    return sum(
        stone.owner == owner
        and HISTORICAL_BUTTON_RADIUS_M < distance_to_house(stone) <= HOUSE_R + STONE_R
        and stone.y >= HOUSE_Y
        and (stone.x - HOUSE_X) * sign > 0.0
        for stone in stones
    )


def _k8_front_pair_roll_target(target: StrategyStone, missing_side: str) -> tuple[float, float]:
    """为 K8 前营补双壶合同生成相对清壶滚位。

    敌壶已在目标侧时，出手壶应沿该侧向前滚过它；敌壶接近中线时，给出
    一个显式的侧向出口。完整前营扇区谓词会在严格终局再次约束这只是一个
    合理的 MADS 初始区域，而非用坐标代替目标盘面。
    """

    sign = 1.0 if missing_side == "right" else -1.0
    dx = float(target.x) - HOUSE_X
    if sign * dx > 0.20:
        x = float(target.x) + sign * 0.05
    else:
        x = HOUSE_X + sign * 0.70
    y = max(float(target.y) + K8_FRONT_PAIR_ROLL_AHEAD_M, HOUSE_Y + 0.35)
    return (x, y)


def is_tactically_dead_position(x: float, y: float) -> bool:
    """策略层的已清除/废球区：左右边缘，或完全越过大本营后沿。"""

    return (
        EDGE_DEAD_LEFT[0] <= float(x) <= EDGE_DEAD_LEFT[1]
        or EDGE_DEAD_RIGHT[0] <= float(x) <= EDGE_DEAD_RIGHT[1]
        or float(y) <= BACK_HOUSE_DEAD_Y
    )


def is_edge_dead(stone: StrategyStone) -> bool:
    """兼容旧名称：策略废球区不只包含左右边缘，也包含大本营后方。"""

    return is_tactically_dead_position(stone.x, stone.y)


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
    """按己方当前在场壶数，给第五至第八颗生成可替代的防御球形。

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


def _is_unreachable_side_enemy(stone: StrategyStone) -> bool:
    """识别仍 enabled、却已无法影响大本营的边线敌壶。

    ``is_edge_dead`` 同时服务己方壶数与高位守壶路径，不能把整个边线半平面
    都删掉。这里仅用于选择 *敌方主威胁*：壶心已经越过废球带内缘、且纵向
    位于大本营影响带时，既不能计分也不可能形成有效前场屏风；末手不应为了
    清它放弃得分或护门。
    """

    outside_side_lane = float(stone.x) < EDGE_DEAD_LEFT[0] or float(stone.x) > EDGE_DEAD_RIGHT[1]
    in_house_influence_band = HOUSE_Y - HOUSE_R - STONE_R <= float(stone.y) <= HOUSE_Y + HOUSE_R + STONE_R
    return bool(outside_side_lane and in_house_influence_band)


def _priority_opponent(stones: Sequence[StrategyStone]) -> StrategyStone | None:
    """先处理红圈/大本营威胁；边缘废球不是当前主要目标。"""

    enemies = [
        stone for stone in stones
        if stone.owner == "opponent" and not is_edge_dead(stone) and not _is_unreachable_side_enemy(stone)
    ]
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


def _threat_type(target: StrategyStone | None, shot_index: int) -> str:
    """把最高优先级敌壶归到互斥的、可解释的位置类别。"""

    if target is None:
        return "no_effective_enemy"
    if int(shot_index) <= 4 and is_in_free_guard_zone(target.x, target.y):
        return "protected_centre_guard" if touches_centre_line(target.x) else "protected_side_guard"
    if is_in_inner_ring(target):
        return "enemy_inner_threat"
    if is_in_house(target):
        return "enemy_house_threat"
    if is_in_free_guard_zone(target.x, target.y):
        return "enemy_free_guard"
    return "enemy_outer_threat"


def _front_side_hold_targets(
    stones: Sequence[StrategyStone], target: StrategyStone | None, own_throw: int,
) -> tuple[tuple[float, float], ...] | None:
    """识别 P5 的侧守壶对峙：清壶后保留高位前肩，而非硬滚到低侧门。

    这是按可观察几何分类的状态，而不是针对某一局 slot 写死的例外：己方已有
    三颗在场壶、没有红圈锚、同侧已有前场壶，敌方把有效守壶压在其内侧时，
    可行的薄撞常自然把出手壶留在该侧前肩。真正是否可提交仍由 PhysX 多种子
    求解器决定，失败会回退到其他分支。
    """

    # 目标是靠前、偏侧的大本营外环壶；它虽然已能计分，几何上与同侧前场
    # 壶形成窄薄撞。若目标仍在自由防守区，则应走保护规则分支，不混在这里。
    if int(own_throw) != 5 or target is None or not is_in_house(target) or target.y < HOUSE_Y + 1.25:
        return None
    own_live = [stone for stone in stones if stone.owner == "self" and not is_edge_dead(stone)]
    if len(own_live) < 3 or _own_inner_count(stones) != 0 or abs(target.x - HOUSE_X) < 0.22:
        return None
    side = -1 if target.x < HOUSE_X else 1
    same_side_front = any(
        stone.owner == "self"
        and (stone.x - HOUSE_X) * side >= 0.20
        and is_in_free_guard_zone(stone.x, stone.y)
        and stone.y >= target.y - 0.20
        for stone in stones
    )
    if not same_side_front:
        return None
    return FRONT_SHOULDER_LEFT if side < 0 else FRONT_SHOULDER_RIGHT


def classify_first_player_situation(board: Iterable[object], shot_index: int) -> FirstPlayerSituation:
    """把任意先手壶面映射到唯一的策略类型和下一目标壶型。

    分类优先级是规则合法性、敌方当前得分威胁、己方中心层缺口、最后三手的
    防御角色缺口。每一类均只输出离散意图；它不会跳过严格 PhysX 去承诺某条
    碰撞路线一定存在。
    """

    if not 0 <= int(shot_index) <= 14 or int(shot_index) % 2:
        raise ValueError("先手策略只接受我方的偶数全局投壶序号 0,2,...,14")
    stones = _as_stones(board)
    own_throw = int(shot_index) // 2 + 1
    target = _priority_opponent(stones)
    action = _opponent_action(target, int(shot_index))
    threat = _threat_type(target, int(shot_index))
    own_inner = _own_inner_count(stones)
    own_closest = _self_is_closest(stones)
    has_anchor = _has_centre_anchor(stones)
    has_guard = _has_centre_guard(stones)
    gates = _side_gate_count(stones)
    # “清一颗侧守壶即可保锚”的前提不是优先级恰好选中了守壶，而是场上
    # 确实只剩这一颗有效敌壶。若仍有第二颗有效敌壶，清一个目标并不能
    # 逻辑上推出下一个状态已安全，应交给后续的多威胁状态分类。
    opponent_live = sum(
        stone.owner == "opponent" and not is_edge_dead(stone)
        for stone in stones
    )
    target_index = None if target is None else target.index

    if own_throw == 1:
        return FirstPlayerSituation(
            int(shot_index), own_throw,
            "P1_EMPTY_SHEET", "PLACE_CENTRE_GUARD", "P2_CENTRE_GUARD_ESTABLISHED",
            None, "none", "空场第一颗只建立中线守壶；它是保护期内可利用的中路支点，而不是后方壶的护盾。",
        )

    if own_throw == 2:
        if threat == "protected_centre_guard":
            return FirstPlayerSituation(
                int(shot_index), own_throw,
                "P2_PROTECTED_CENTRE_GUARD", "AVOID_PROTECTED_GUARD_AND_DRAW_ANCHOR", "P3_FIRST_INNER_ANCHOR",
                None, action, "对方中线守壶仍受保护；不把它撞离中线，绕开它建立己方第一颗红圈锚。",
            )
        if threat == "protected_side_guard":
            return FirstPlayerSituation(
                int(shot_index), own_throw,
                "P2_PROTECTED_SIDE_GUARD", "PUSH_GUARD_TO_EDGE_AND_ROLL_IN", "P3_FIRST_INNER_ANCHOR",
                target_index, action, "普通自由防守区壶不能出界；将其推到边缘废球带，同时争取己方红圈锚。",
            )
        if threat in {"enemy_inner_threat", "enemy_house_threat"}:
            return FirstPlayerSituation(
                int(shot_index), own_throw,
                "P2_ENEMY_ALREADY_SCORING", "CLEAR_AND_ROLL_TO_INNER_ANCHOR", "P3_FIRST_INNER_ANCHOR",
                target_index, action, "敌方已占营内威胁；先清除或通过撞击取得更近的己方锚。",
            )
        return FirstPlayerSituation(
            int(shot_index), own_throw,
            "P2_NO_EFFECTIVE_ENEMY", "DRAW_FIRST_INNER_ANCHOR", "P3_FIRST_INNER_ANCHOR",
            None, "none", "对方没有有效主战壶；不为边缘废球浪费一颗，直接建立第一红圈锚。",
        )

    if own_throw == 3:
        if (
            target is not None
            and is_in_house(target)
            # 对方的侧营内壶即使略过 T 线仍可在清壶后留下最近壶；按 T 线
            # 切断会把这类局面错误降级为普通纯清，丢掉“清后滚入对侧内圈”
            # 的状态边。这里描述的是整个侧向营内威胁带，而非某个历史 y。
            and target.y >= HOUSE_Y - 0.60
            and own_inner == 0
            and has_guard
            and abs(target.x - HOUSE_X) >= 0.22
        ):
            side_label = "LEFT" if target.x < HOUSE_X else "RIGHT"
            return FirstPlayerSituation(
                int(shot_index), own_throw,
                f"P3_{side_label}_HOUSE_COUNTER_AFTER_K2_CLEAR", "CLEAR_AND_ROLL_TO_COUNTER_INNER_ANCHOR",
                f"P4_COUNTER_INNER_ANCHOR_{side_label}", target_index, "physical_clear",
                "对方已清掉我方 K2 锚但在侧前外环留下得分壶；清目标后把出手壶滚回相反侧按钮附近的内圈锚。",
            )
        if threat in {"enemy_inner_threat", "enemy_house_threat"} and not own_closest:
            return FirstPlayerSituation(
                int(shot_index), own_throw,
                "P3_ENEMY_HAS_CENTRE", "CLEAR_OR_OUTDRAW_TO_RETAKE_CENTRE", "P4_SELF_CLOSEST_ANCHOR",
                target_index, action, "对方比我方更近时，先夺回最近壶；不能只机械补第二颗红圈壶。",
            )
        if threat == "protected_side_guard":
            return FirstPlayerSituation(
                int(shot_index), own_throw,
                "P3_PROTECTED_SIDE_GUARD", "PUSH_EDGE_OR_BUILD_STAGGERED_PAIR", "P4_STAGGERED_INNER_PAIR",
                target_index, action, "保护期最后一手可把普通守壶推成边缘废球；若路径不稳，优先完成错层红圈对。",
            )
        if own_inner < 2:
            return FirstPlayerSituation(
                int(shot_index), own_throw,
                "P3_INNER_LAYER_MISSING", "BUILD_STAGGERED_INNER_PAIR", "P4_STAGGERED_INNER_PAIR",
                None, "none", "己方红圈层不足两颗；补另一侧、前后错开的壶，避免和已有锚排成直线。",
            )
        return FirstPlayerSituation(
            int(shot_index), own_throw,
            "P3_CENTRE_LAYER_PRESENT", "MAINTAIN_STAGGERED_ADVANTAGE", "P4_CENTRE_ADVANTAGE",
            None, "none", "已有最近壶与第二层；保留错层，不为无效外圈壶破坏结构。",
        )

    # 本比赛的自由防守区保护只覆盖全局第 1--5 壶。因此我方 P4
    # （全局第 7 壶）已经处于可击打阶段，但 P4 仍保留原来的“中心层
    # 修复”职责；从 P5 开始正式切到防御角色搜索。不能误把“第六壶”
    # 理解为双方各自的第六颗。
    if own_throw == 4:
        if threat in {"enemy_inner_threat", "enemy_house_threat"}:
            return FirstPlayerSituation(
                int(shot_index), own_throw,
                f"P{own_throw}_ENEMY_SCORING_THREAT", "CLEAR_AND_RECLAIM_CENTRE", "P6_CENTRE_ADVANTAGE",
                target_index, "physical_clear", "保护期结束后，营内敌壶是第一优先级；清除后再把出手壶滚到得分层。",
            )
        if own_inner == 1 and has_guard and opponent_live == 1 and threat == "enemy_free_guard":
            return FirstPlayerSituation(
                int(shot_index), own_throw,
                "P4_SINGLE_INNER_ANCHOR_OPPONENT_SIDE_GUARD", "CLEAR_SIDE_GUARD_AND_HOLD_OUTER_ROLL",
                "P5_SINGLE_INNER_ANCHOR_SIDE_GUARD_CLEARED", target_index, "physical_clear",
                "已有一颗内圈锚且对方只留下侧守壶；清守壶并把出手壶留在高外环，保留锚与中线支撑的后续转换空间。",
            )
        if own_inner == 0 and has_guard:
            # K3 的交换可能同时带走第一颗营内锚；这时不能把“没有第一层”
            # 误当成“缺第二层”。场外敌壶仍是实际绕行障碍，但不是本手的
            # 计分清除目标：应从中线守壶两侧反解一颗新的第一内圈锚。
            return FirstPlayerSituation(
                int(shot_index), own_throw,
                "P4_CENTRE_GUARD_ONLY_FIRST_ANCHOR_MISSING", "REBUILD_FIRST_INNER_ANCHOR_AROUND_CENTRE_GUARD",
                "P5_FIRST_INNER_ANCHOR_RESTORED", None, "none",
                "中线守壶仍在、己方营内层已清空且对方没有营内得分威胁；绕开当前前场壶重建第一内圈锚，不虚构第二层。",
            )
        if own_inner < 2:
            return FirstPlayerSituation(
                int(shot_index), own_throw,
                f"P{own_throw}_INNER_LAYER_DAMAGED", "RESTORE_STAGGERED_INNER_PAIR", "P6_TWO_INNER_LAYERS",
                None, "none", "己方两层红圈结构被拆；先补缺层而非继续向中心聚堆。",
            )
        return FirstPlayerSituation(
            int(shot_index), own_throw,
            f"P{own_throw}_CENTRE_ADVANTAGE", "MAINTAIN_OR_SELECTIVE_CLEAR", "P6_CENTRE_ADVANTAGE",
            target_index if threat != "no_effective_enemy" else None,
            "physical_clear" if threat != "no_effective_enemy" else "none",
            "己方中心层仍完整；只选择性处理有效敌壶，保留下一阶段可转换的己方壶。",
        )

    # K5 若仍保有一颗内圈锚和中线守壶、对手只是以高位侧守壶封路，不能
    # 退化为“只要清掉就行”的 pure-clear。当前壶面仍有两颗己方支撑，应
    # 清守壶并让出手壶停入任一高外环出口；两侧同时交给 PhysX，因为目标
    # 壶贴近中线时由其微小左右偏差指定唯一出口并不可靠。
    if (
        own_throw == 5
        and own_inner == 1
        and has_guard
        and opponent_live == 1
        and threat == "enemy_free_guard"
    ):
        return FirstPlayerSituation(
            int(shot_index), own_throw,
            "P5_SINGLE_INNER_ANCHOR_OPPONENT_SIDE_GUARD", "CLEAR_SIDE_GUARD_AND_HOLD_OUTER_ROLL",
            "P6_SINGLE_INNER_ANCHOR_SIDE_GUARD_CLEARED", target_index, "physical_clear",
            "已有内圈锚和中线守壶、对方仅以高位侧守壶封路；清守壶后停入任一高外环出口，保留原锚与中线支撑，禁止把该局面降级为纯清。",
        )

    # 第五至第八颗只接受“对方当前威胁 + 缺失防御角色”的组合类型。这样同一
    # 个壶面不会因程序调用路径不同而得到不同策略。
    own_live = sum(stone.owner == "self" and not is_edge_dead(stone) for stone in stones)
    # “没有己方壶”与“还留有一颗己方壶”不是同一个状态。后者可以把
    # 新壶视为第二个得分层；前者一手最多只能重新建立一个锚。过去把两者
    # 合并为 ONE_OWN，会让 K5--K8 在零己方壶壶面上声明一个至少需要两颗
    # 己方壶的 defence shape，因而从定义上不可能满足。
    role_suffix = (
        "ZERO_OWN" if own_live == 0 else
        "ONE_OWN" if own_live == 1 else
        "TWO_OWN" if own_live == 2 else
        "THREE_PLUS_OWN"
    )
    if own_live == 0:
        if threat != "no_effective_enemy":
            return FirstPlayerSituation(
                int(shot_index), own_throw,
                f"P{own_throw}_ENEMY_THREAT_ZERO_OWN", "CLEAR_THREAT_AND_RECLAIM_FIRST_ANCHOR",
                f"P{own_throw + 1}_FIRST_ANCHOR_RECLAIMED", target_index, "physical_clear",
                "场上已无己方有效壶：本手只能先清当前威胁并重新建立第一颗营内锚；"
                "不得把它伪装成补第二层或补护门。",
            )
        return FirstPlayerSituation(
            int(shot_index), own_throw,
            f"P{own_throw}_ZERO_OWN_NO_EFFECTIVE_ENEMY", "REBUILD_FIRST_INNER_ANCHOR",
            f"P{own_throw + 1}_FIRST_ANCHOR_REBUILT", None, "none",
            "场上已无己方有效壶且对方没有当前得分威胁：先重建一颗第一营内锚，"
            "不声明一手无法完成的双层结构。",
        )
    # 这条分支来自“先手 K8 得分”反推，不是从普通清壶规则猜出来的：
    # 当前已有一枚己方前侧营内壶、对手仅有一枚营内威胁，最有价值的 G8 是
    # 清威胁后补成左右前侧各一枚，并使对方营内为零。只在一颗敌方营内壶时
    # 启用，因为一颗壶不能诚实地承诺双清。
    own_front_left = _front_house_sector_count(stones, "self", "left")
    own_front_right = _front_house_sector_count(stones, "self", "right")
    own_house = sum(stone.owner == "self" and is_in_house(stone) for stone in stones)
    opponent_house = sum(stone.owner == "opponent" and is_in_house(stone) for stone in stones)
    # 一颗威胁已经落在 T 线之后时，出手壶从前场撞上它后的自然动量方向是
    # 向后（朝更小的 y）。此时强制它滚到“前营另一侧”会声明一个与碰撞
    # 几何矛盾的 G8：搜索再久也只能失败后退为纯清。若我方已有一枚营内
    # 得分壶，正确、可泛化的末手状态边是清威胁并把出手壶夺回按钮附近，
    # 形成两枚营内得分壶。这个分界只依赖当前目标相对 T 线的位置，并非
    # 某条历史轨迹的坐标或对手未来动作。
    if (
        own_throw == 8
        and target is not None
        and is_in_house(target)
        and opponent_house == 1
        and own_house >= 1
        and target.y < HOUSE_Y
    ):
        return FirstPlayerSituation(
            int(shot_index), own_throw,
            "P8_BACK_HOUSE_THREAT_RECLAIM_CENTRE",
            "TERMINAL_CLEAR_AND_RECLAIM_CENTRE_FROM_BACK_HOUSE_THREAT",
            "P8_TWO_SCORING_LAYERS_CENTRE_RECLAIM",
            target_index, "physical_clear",
            "唯一营内威胁已过 T 线；清壶后夺回按钮附近，保住现有营内锚形成两层得分，而不要求违反碰撞方向地滚到前营。",
        )
    if (
        own_throw == 8
        and target is not None
        and is_in_house(target)
        and opponent_house == 1
        and ((own_front_left >= 1 and own_front_right == 0) or (own_front_right >= 1 and own_front_left == 0))
    ):
        missing_side = "RIGHT" if own_front_left >= 1 else "LEFT"
        return FirstPlayerSituation(
            int(shot_index), own_throw,
            f"P8_SINGLE_HOUSE_THREAT_COMPLETE_FRONT_{missing_side}_PAIR",
            "TERMINAL_CLEAR_AND_COMPLETE_FRONT_HOUSE_PAIR",
            f"P8_CLEAR_THREAT_AND_FRONT_{missing_side}_PAIR_REPLY_SEARCH_REQUIRED",
            target_index, "physical_clear",
            "K8 历史先手得分的完整目标：清唯一营内威胁后，补齐另一侧前营壶，令前左/前右各一枚、对方营内为零；仍须由 PPO 最后一壶实际筛查。",
        )
    isolated_k8_outer_roll = (
        own_throw == 8
        and target is not None
        and is_in_house(target)
        and own_inner == 0
        and own_live == 2
        and (
            # 两颗己方残壶均已远离大本营；或 K7 抢回最近壶后 PPO 拆掉一颗，
            # 留下一颗外圈己壶和中线守壶。两者都不能一手造双内圈终局。
            all(
                stone.owner != "self" or math.hypot(stone.x - HOUSE_X, stone.y - HOUSE_Y) > HOUSE_R + 0.20
                for stone in stones
            )
            or (has_guard and sum(stone.owner == "self" and is_in_house(stone) for stone in stones) == 1)
        )
    )
    if isolated_k8_outer_roll:
        side_label = "LEFT" if target.x < HOUSE_X else "RIGHT"
        return FirstPlayerSituation(
            int(shot_index), own_throw,
            f"P8_{side_label}_HOUSE_THREAT_TWO_OWN_OUTER_ROLL",
            "TERMINAL_CLEAR_AND_HOLD_SIDE_HOUSE_ROLL",
            f"P8_{side_label}_HOUSE_ROLL_REPLY_SEARCH_REQUIRED",
            target_index, "physical_clear",
            "历史高价值终局要求清威胁后形成两层营内，但当前只有外圈/守壶角色，不能一手复刻；降级为清营内威胁并让出手壶停在同侧大本营外圈、成为最近壶。该真实终局仍须由对手最后一壶反击验证。",
        )
    if own_throw == 8 and has_anchor and has_guard and gates < 2:
        strategy = "CLEAR_THREAT_AND_COMPLETE_MISSING_GATE" if threat != "no_effective_enemy" else "COMPLETE_MISSING_GATE"
        return FirstPlayerSituation(
            int(shot_index), own_throw,
            "P8_FINAL_GATE_MISSING_" + role_suffix, strategy, "P8_REPLY_SEARCH_REQUIRED_CENTRE_GUARD_DOUBLE_GATE",
            target_index if threat != "no_effective_enemy" else None,
            "physical_clear" if threat != "no_effective_enemy" else "none",
            "第八颗已有中心锚和中线守壶但缺一侧门；优先补缺门。形成双门后只进入“需对真实终局重跑末手反击搜索”的候选池，不直接宣称安全。",
        )
    shoulder_targets = _front_side_hold_targets(stones, target, own_throw)
    if shoulder_targets is not None:
        side_label = "LEFT" if shoulder_targets == FRONT_SHOULDER_LEFT else "RIGHT"
        return FirstPlayerSituation(
            int(shot_index), own_throw,
            f"P5_{side_label}_FRONT_GUARD_CONTEST_NO_INNER", "CLEAR_AND_HOLD_FRONT_SHOULDER",
            f"P5_{side_label}_FRONT_SHOULDER_AFTER_CLEAR", target_index, "physical_clear",
            "己方尚无红圈锚但已有同侧前场壶；清掉内侧有效守壶后，允许出手壶留在高位前肩保持压力，不强迫它滚进低侧门。",
        )
    if (
        own_throw == 5
        and threat == "no_effective_enemy"
        and own_inner == 1
        and has_guard
        and own_live >= 3
    ):
        inner = next(stone for stone in stones if stone.owner == "self" and is_in_inner_ring(stone))
        side_label = "LEFT" if inner.x < HOUSE_X else "RIGHT"
        return FirstPlayerSituation(
            int(shot_index), own_throw,
            f"P5_ONE_INNER_{side_label}_ANCHOR_NO_ENEMY",
            "ADD_SECOND_STAGGERED_INNER_LAYER",
            f"P6_TWO_INNER_LAYERS_FROM_{side_label}_ANCHOR",
            None, "none",
            "K4 清侧守壶后对方没有有效壶；不只补泛化按钮区域，而是在已有内圈锚的对侧补第二错层内圈壶。",
        )
    if own_throw == 7 and own_house == 1 and own_closest and opponent_house == 0:
        return FirstPlayerSituation(
            int(shot_index), own_throw,
            "P7_SELF_SCORING_ONLY_EXTERNAL_OPPONENTS", "ADD_SECOND_SCORING_LAYER_WITH_EXTERNAL_OBSTACLES",
            "P8_TWO_SCORING_LAYERS_NO_ENEMY_HOUSE", None, "none",
            "己方已有最近得分壶、对方没有营内得分威胁；前场/边缘敌壶只作为绕行障碍，补反侧第二得分层而不是无收益清壶。",
        )
    if (
        own_throw == 6
        and target is not None
        and is_in_house(target)
        and own_inner == 1
        and has_guard
        and own_live >= 3
    ):
        return FirstPlayerSituation(
            int(shot_index), own_throw,
            "P6_ONE_INNER_ANCHOR_OPPONENT_HOUSE_COUNTER",
            "PROMOTE_TO_HISTORICAL_CONTROL",
            "P7_FIRST_CENTRE_CONTROL_AFTER_PROMOTE",
            target_index, "physical_displace",
            "同类历史 S6 的高价值边是新增己方营内层并夺回中心。历史细圆与当前对方内圈壶重叠，故本手应 promote/raise 把它推出原位，而不是伪装成净空 outdraw 或无条件清壶。",
        )
    if (
        own_throw == 7
        and target is not None
        and is_in_house(target)
        and own_inner == 0
        and own_live == 2
        and has_guard
    ):
        return FirstPlayerSituation(
            int(shot_index), own_throw,
            "P7_TWO_OUTER_OWN_SINGLE_HOUSE_THREAT", "CLEAR_AND_ROLL_TO_HISTORICAL_CONTROL",
            "P8_FIRST_HOUSE_CONTROL_AFTER_SINGLE_CLEAR", target_index, "physical_clear",
            "当前只剩两颗非内圈己方壶、对方一颗营内威胁且中线锚仍在；采用 K7 历史高支持边：清威胁并把出手壶滚进历史控制槽，先拿回最近壶，而不是只做宽松交换。",
        )
    if (
        own_throw == 7
        and target is not None
        and is_in_house(target)
        and own_house == 1
        and own_inner == 0
        and distance_to_house(target) >= 0.90
    ):
        return FirstPlayerSituation(
            int(shot_index), own_throw,
            "P7_ONE_OUTER_SELF_OUTER_ENEMY_HOUSE_THREAT", "CLEAR_OUTER_THREAT_AND_RECLAIM_CENTRE",
            "P8_TWO_SCORING_LAYERS_AFTER_OUTER_CLEAR", target_index, "physical_clear",
            "双方各有外层营内壶时，净空 outdraw 会把对方计分壶完整留在场上。先清唯一外层威胁并让出手壶夺回按钮附近，保留原锚形成两层得分。",
        )
    if (
        own_throw == 5
        and target is not None
        and is_in_inner_ring(target)
        and own_inner == 0
        and has_guard
        and _has_front_guard(stones)
        and abs(target.x - HOUSE_X) >= 0.20
    ):
        side_label = "LEFT" if target.x < HOUSE_X else "RIGHT"
        return FirstPlayerSituation(
            int(shot_index), own_throw,
            f"P5_{side_label}_INNER_THREAT_AFTER_SCREEN", "CLEAR_AND_RESTORE_SIDE_INNER_ANCHOR",
            f"P6_{side_label}_INNER_ANCHOR_RESTORED", target_index, "physical_clear",
            "K4 屏风仍在但内圈锚已被清、对方壶占住内圈；先清内圈威胁，并把出手壶滚回同侧红圈锚。",
        )
    if threat != "no_effective_enemy":
        return FirstPlayerSituation(
            int(shot_index), own_throw,
            f"P{own_throw}_ENEMY_THREAT_{role_suffix}", "CLEAR_THREAT_AND_ROLL_INTO_DEFENCE", f"P{own_throw}_DEFENCE_TRANSITION_{role_suffix}",
            target_index, "physical_clear", "第五颗以后，对方上一颗有效壶必须先被处理；滚位再按当前己方壶数补防御角色。",
        )
    return FirstPlayerSituation(
        int(shot_index), own_throw,
        f"P{own_throw}_NO_EFFECTIVE_ENEMY_{role_suffix}", "FILL_MISSING_DEFENCE_ROLE", f"P{own_throw}_DEFENCE_TRANSITION_{role_suffix}",
        None, "none", "对方只剩边缘或无效壶；不为清无效壶牺牲结构，直接补当前缺失的得分层或侧门。",
    )


def plan_first_player_turn(board: Iterable[object], shot_index: int) -> FirstPlayerPlan:
    """为先手方的下一颗壶生成可执行的战术意图。

    它处理的是“该补什么层”，不是直接输出物理输入。调用端将
    ``target_points`` 和 ``target_opponent_index`` 交给粗筛/严格 PhysX。
    """

    if not 0 <= int(shot_index) <= 14 or int(shot_index) % 2:
        raise ValueError("先手策略只接受我方的偶数全局投壶序号 0,2,...,14")
    # 先固化壶面，再分类。这样调用者即使传入的是 generator，也不会在分类时
    # 被消费掉，后续规划仍能看到同一份壶面。
    stones = _as_stones(board)
    situation = classify_first_player_situation(stones, int(shot_index))
    own_throw = int(shot_index) // 2 + 1
    target = _priority_opponent(stones)
    opponent_action = _opponent_action(target, int(shot_index))
    pair = _target_pair(stones)

    def make_plan(
        phase: str,
        target_points: tuple[tuple[float, float], ...],
        target_opponent_index: int | None,
        action: str,
        rationale: str,
        defence_shapes: tuple[DefenceShape, ...] = (),
        landing_region_radius_m: float = DEFAULT_LANDING_REGION_RADIUS_M,
        max_own_cleared: int | None = None,
    ) -> FirstPlayerPlan:
        """把物理层目标与唯一的离散状态机边一起交给调用端。"""

        return FirstPlayerPlan(
            int(shot_index), own_throw, phase, target_points, target_opponent_index,
            action, rationale, landing_region_radius_m, defence_shapes,
            situation.situation_type, situation.strategy_type, situation.desired_state_type, max_own_cleared,
        )

    if own_throw == 1:
        return make_plan("open_centre_guard", (GUARD_TARGET,), None, "none", "第一颗占中线守壶；之后的保护规则才有可利用的支点。")

    if own_throw == 2:
        target_point = (
            K2_AROUND_CENTRE_GUARD_ANCHOR
            if opponent_action == "none" and _has_centre_guard(stones) else pair[0]
        )
        if opponent_action == "physical_clear":
            text = "对方第一颗已进大本营：优先物理清出，同时让出手壶尽量滚入第一红圈槽。"
        elif opponent_action == "push_to_edge_dead":
            text = "对方第一颗是受保护的普通自由防守区守壶：推入边缘废球带，不可打出界；出手壶争取第一红圈槽。"
        else:
            text = "己方中线守壶仍在且对方无有效壶；绕开守壶进入已标定的第一红圈锚，不把它当作空场直 draw。"
        return make_plan("process_first_enemy_and_score", (target_point,), None if opponent_action == "avoid_protected_centre_guard" else (target.index if target else None), opponent_action, text)

    if own_throw == 3:
        if situation.strategy_type == "CLEAR_AND_ROLL_TO_COUNTER_INNER_ANCHOR":
            target_points = (
                (
                    K3_CLEAR_LEFT_TO_RIGHT_INNER_ANCHOR,
                    K3_CLEAR_LEFT_TO_LEFT_FRONT_ANCHOR,
                    *K3_GUARD_ALIGNED_RECOVERY_CORRIDOR,
                )
                if target is not None and target.x < HOUSE_X
                else (
                    K3_CLEAR_RIGHT_TO_LEFT_INNER_ANCHOR,
                    K3_CLEAR_RIGHT_TO_RIGHT_FRONT_ANCHOR,
                    *K3_GUARD_ALIGNED_RECOVERY_CORRIDOR,
                )
            )
            return make_plan(
                "clear_then_repair_closest_scoring_anchor", target_points,
                target.index if target else None, "physical_clear",
                "对手清掉 K2 锚后的反击：清其侧前得分壶；同时搜索相反侧内圈锚、同侧前营控制槽和中线守壶后方恢复走廊，选择当前严格物理下可达且仍为最近壶的后继状态。",
            )
        if situation.strategy_type == "CLEAR_OR_OUTDRAW_TO_RETAKE_CENTRE":
            return make_plan(
                "clear_then_repair_closest_scoring_anchor", (pair[0], pair[1]),
                target.index if target else None, "physical_clear",
                "对方已经是最近壶：本手先清掉该威胁，出手壶回到可争最近壶的红圈槽；不机械补第二颗壶。",
            )
        return make_plan("complete_staggered_house_pair", (pair[1],), target.index if target and opponent_action != "avoid_protected_centre_guard" else None, opponent_action, "保护期的最后一颗：优先补第二红圈壶，并与第一颗前后、左右错开；只有明显敌方得分威胁才顺带处理。")

    # S6：只剩中线自由防守区守壶，且唯一敌壶贴近中线的前营边缘。此时把
    # “绕开后 outdraw”当作唯一选择会放过一条更稳的单清滚位：从敌壶内侧
    # 留下一颗前营控制锚。横向威胁较远时该碰撞角会退化，仍交给 outdraw。
    # 这里的槽由当前威胁的左右方向生成，不依赖历史坐标或对手后续动作。
    if (
        own_throw == 6
        and target is not None
        and opponent_action == "physical_clear"
        and len([stone for stone in stones if stone.owner == "self"]) == 1
        and not any(stone.owner == "self" and is_in_house(stone) for stone in stones)
        and _has_centre_guard(stones)
        and is_in_house(target)
        and abs(target.x - HOUSE_X) <= 0.50
        # 只覆盖贴近前营边缘的威胁。更深的近中线壶仍有稳定 outdraw
        # 通道，不能用同一清壶滚位合同抢占它。
        and target.y >= HOUSE_Y + 1.10
    ):
        side = 1.0 if target.x >= HOUSE_X else -1.0
        front_control = (target.x - side * 0.17, target.y - 0.04)
        return make_plan(
            "sixth_clear_near_centre_front_house_threat", (front_control,), target.index,
            "physical_clear",
            "K6 单中线守壶对近中线前营威胁：优先清壶并把出手壶滚到威胁内侧前营控制槽；仅在该几何稳定时替代宽泛 outdraw。",
            landing_region_radius_m=0.32,
            max_own_cleared=0,
        )

    if own_throw == 4:
        if situation.strategy_type == "REBUILD_FIRST_INNER_ANCHOR_AROUND_CENTRE_GUARD":
            mirrored_anchor = (2.0 * HOUSE_X - K2_AROUND_CENTRE_GUARD_ANCHOR[0], K2_AROUND_CENTRE_GUARD_ANCHOR[1])
            return make_plan(
                "fourth_rebuild_first_anchor_around_centre_guard",
                (K2_AROUND_CENTRE_GUARD_ANCHOR, mirrored_anchor),
                None,
                "none",
                "第一营内锚被清空但中线守壶仍在：分别反解两侧绕守壶通道，提交当前严格 PhysX 下净空、入内圈且最稳的一侧。",
                landing_region_radius_m=0.35,
            )
        # 分类器只把“营内、正在计分的敌壶”定义为此时的必清威胁。此前把
        # 任意非废球敌壶都传成 physical_clear，会让 P4/P5_CENTRE_ADVANTAGE
        # 与其“选择性处理”的声明相矛盾，并退化成见壶就清。
        if situation.strategy_type == "CLEAR_AND_RECLAIM_CENTRE" and target is not None:
            return make_plan("reclaim_centre_or_clear_threat", (pair[0], pair[1]), target.index, "physical_clear", "保护期结束后，先处理对方上一颗仍有效的壶；若它已占红圈，则优先清出或重新取得最近壶。")
        if situation.strategy_type == "CLEAR_SIDE_GUARD_AND_HOLD_OUTER_ROLL":
            target_point = (
                K4_CLEAR_LEFT_SIDE_GUARD_OUTER_ROLL
                if target is not None and target.x < HOUSE_X else K4_CLEAR_RIGHT_SIDE_GUARD_OUTER_ROLL
            )
            return make_plan(
                "clear_side_guard_and_hold_outer_roll", (target_point,),
                target.index if target else None, "physical_clear",
                "单内圈锚不再与第二颗营内壶堆叠；清掉侧守壶后，出手壶留在同侧高外环，给下一手保留压力与转换余地。",
                landing_region_radius_m=0.15,
            )
        if _own_inner_count(stones) < 2:
            return make_plan("restore_second_scoring_stone", (pair[1],), None, "none", "己方红圈壶不足两颗，补另一侧得分层，不把壶堆在同一条直线上。")
        return make_plan("maintain_centre_advantage", (pair[0],), None, "none", "当前中心层仍完整；用更靠中心或轻微错层的壶维持优势。")

    if own_throw == 5 and situation.strategy_type == "CLEAR_SIDE_GUARD_AND_HOLD_OUTER_ROLL":
        return make_plan(
            "clear_side_guard_and_hold_outer_roll",
            (K4_CLEAR_LEFT_SIDE_GUARD_OUTER_ROLL, K4_CLEAR_RIGHT_SIDE_GUARD_OUTER_ROLL),
            target.index if target else None,
            "physical_clear",
            "K5 的近中线高位侧守壶同时反解左右高外环出口；严格 PhysX 必须清目标、保住已有锚和中线守壶，不能以纯清替代。",
            landing_region_radius_m=0.25,
            max_own_cleared=0,
        )

    # 从第五颗开始，不再把滚位锁成一个固定点。根据己方现有 1/2/3 颗在场壶
    # 提供多个阵型；这些阵型是替代解，粗筛和严格 PhysX 都会把它们一起搜索。
    if situation.strategy_type == "ADD_SECOND_SCORING_LAYER_WITH_EXTERNAL_OBSTACLES":
        existing_scoring = [stone for stone in stones if stone.owner == "self" and is_in_house(stone)]
        anchor = min(existing_scoring, key=distance_to_house)
        # 与当前最近壶错到按钮另一侧、略向后放置。目标由当前壶相对按钮的
        # 左右角色生成；外部敌壶仍完整保留给净空 PhysX 绕行验收。
        side = 1.0 if anchor.x <= HOUSE_X else -1.0
        second_layer_target = (HOUSE_X + side * 0.375, HOUSE_Y - 0.32)
        return make_plan(
            "seventh_add_second_scoring_layer_without_enemy_house_threat",
            (second_layer_target,), None, "none",
            "对方无营内得分壶时，保留现有最近壶并绕开外部壶，在其反侧补第二颗营内得分壶；不为前场壶放弃计分层。",
            landing_region_radius_m=0.35,
        )
    if situation.strategy_type == "CLEAR_OUTER_THREAT_AND_RECLAIM_CENTRE":
        return make_plan(
            "seventh_clear_outer_threat_and_reclaim_centre",
            ((HOUSE_X, HOUSE_Y),), target.index if target else None, "physical_clear",
            "清掉唯一外层营内威胁后，让出手壶夺回按钮近邻；原有外锚保留为第二得分层，而不是把威胁留给对手下一壶利用。",
            landing_region_radius_m=0.35,
        )
    if situation.strategy_type == "CLEAR_THREAT_AND_RECLAIM_FIRST_ANCHOR":
        return make_plan(
            "clear_then_reclaim_first_inner_anchor",
            (pair[0], pair[1]), target.index if target else None, "physical_clear",
            "当前没有任何己方有效壶：清掉唯一有效威胁后，出手壶必须成为新的最近营内锚。"
            "这只是从零壶面恢复第一层，下一手再按真实壶面分类，不能冒充完整防线。",
            landing_region_radius_m=0.35,
            max_own_cleared=0,
        )
    if situation.strategy_type == "REBUILD_FIRST_INNER_ANCHOR":
        return make_plan(
            "rebuild_first_inner_anchor_from_zero_own",
            (pair[0], pair[1]), None, "none",
            "当前没有任何己方有效壶；绕开场上障碍重建一颗第一营内锚，后续结构由下一轮真实状态重新决定。",
            landing_region_radius_m=0.35,
        )
    defence_shapes = _defence_shapes(stones)
    defence_targets = _unique_points(*(shape.active_targets for shape in defence_shapes))
    shoulder_targets = _front_side_hold_targets(stones, target, own_throw)
    if shoulder_targets is not None:
        side_label = "左" if shoulder_targets == FRONT_SHOULDER_LEFT else "右"
        shoulder_shape = DefenceShape(
            f"P5_{side_label}前肩清壶保留",
            "清除内侧有效侧守壶，出手壶保留在高位前肩；这是压力延续位，尚不把它称作最终安全防线。",
            shoulder_targets,
            required_inner_count=0,
            landing_region_radius_m=0.10,
            require_front_guard=True,
        )
        return make_plan(
            "fifth_clear_and_hold_front_shoulder", shoulder_targets,
            target.index if target else None, "physical_clear",
            "此类侧守壶对峙的已验证薄撞会停在高位前肩；先清目标，再把出手壶留在该压力位。",
            (shoulder_shape,), landing_region_radius_m=0.10,
        )
    if situation.strategy_type == "CLEAR_AND_RESTORE_SIDE_INNER_ANCHOR":
        target_point = (
            K5_CLEAR_LEFT_TO_LEFT_INNER_ANCHOR
            if target is not None and target.x < HOUSE_X else K5_CLEAR_RIGHT_TO_RIGHT_INNER_ANCHOR
        )
        anchor_shape = DefenceShape(
            "P5清内圈后同侧红圈锚",
            "清掉敌方内圈壶后，出手壶进入同侧红圈锚；保留 K4 的前场屏风继续限制直接入口。",
            (target_point,), required_inner_count=1, landing_region_radius_m=0.10, require_front_guard=True,
        )
        return make_plan(
            "fifth_clear_and_restore_side_inner_anchor", (target_point,),
            target.index if target else None, "physical_clear",
            "先清内圈敌壶，再以同侧红圈锚恢复得分层；不把普通侧壳称为终局安全。",
            (anchor_shape,), landing_region_radius_m=0.10,
        )
    if situation.strategy_type == "ADD_SECOND_STAGGERED_INNER_LAYER":
        inner = next(stone for stone in stones if stone.owner == "self" and is_in_inner_ring(stone))
        target_point = K5_HISTORICAL_SECOND_LAYER_LEFT if inner.x < HOUSE_X else K5_HISTORICAL_SECOND_LAYER_RIGHT
        return make_plan(
            "fifth_add_second_staggered_inner_layer", (target_point,), None, "none",
            "K5 将已有内圈锚扩展为历史主 G 的第二控制层；目标区域收紧，避免“都进营但下一手结构不同”的伪等价。",
            landing_region_radius_m=0.153234,
        )
    if situation.strategy_type == "PROMOTE_TO_HISTORICAL_CONTROL":
        return make_plan(
            "sixth_promote_to_historical_control", (K6_PROMOTE_TO_HISTORICAL_CONTROL,),
            target.index if target else None, "physical_displace",
            "K6 以碰撞 promote 实现历史 MDP 的中心控制：对方目标壶必须离开原位，出手壶进入历史控制细圆并成为最近壶；严格 PhysX 未找到时才允许回退。",
            landing_region_radius_m=0.163308,
        )
    if situation.strategy_type == "CLEAR_AND_ROLL_TO_HISTORICAL_CONTROL":
        target_point = (
            K7_CLEAR_TO_HISTORICAL_CONTROL
            if target is not None and target.x > HOUSE_X else K7_CLEAR_TO_HISTORICAL_CONTROL_MIRROR
        )
        return make_plan(
            "seventh_clear_and_roll_to_historical_control", (target_point,),
            target.index if target else None, "physical_clear",
            "K7 历史支持的精确状态转移：清唯一营内威胁，出手壶进入历史控制细圆并成为最近壶；后续仍由 PPO 第八码检验。",
            landing_region_radius_m=0.10,
        )
    if situation.strategy_type == "TERMINAL_CLEAR_AND_COMPLETE_FRONT_HOUSE_PAIR":
        existing_left = _front_house_sector_count(stones, "self", "left") >= 1
        missing_side = "right" if existing_left else "left"
        target_point = _k8_front_pair_roll_target(target, missing_side) if target is not None else (HOUSE_X, HOUSE_Y)
        pair_shape = DefenceShape(
            "K8清威胁后补齐前营双壶",
            "历史赢方 G8：对手营内归零，己方前左/前右各一壶。它只是严格 PhysX 的出手后盘面合同；PPO 第十六壶筛查尚未完成前，不称为安全终局。",
            (target_point,),
            required_inner_count=0,
            landing_region_radius_m=K8_FRONT_PAIR_REGION_RADIUS_M,
            required_own_front_left_count=1,
            required_own_front_right_count=1,
            max_opponent_house_count=0,
        )
        return make_plan(
            "terminal_clear_and_complete_front_house_pair", (target_point,),
            target.index if target else None, "physical_clear",
            "K8 不作单纯清壶：清唯一营内威胁，同时让出手壶补齐另一侧前营得分层；实际终局必须接受 PPO 最后一壶反击。",
            (pair_shape,), landing_region_radius_m=K8_FRONT_PAIR_REGION_RADIUS_M,
        )
    if situation.strategy_type == "TERMINAL_CLEAR_AND_RECLAIM_CENTRE_FROM_BACK_HOUSE_THREAT":
        return make_plan(
            "terminal_clear_and_reclaim_centre_from_back_house_threat", ((HOUSE_X, HOUSE_Y),),
            target.index if target else None, "physical_clear",
            "敌方唯一营内壶已过 T 线：以严格 PhysX 清掉目标，同时让出手壶停在按钮近邻并成为最近壶；已有营内锚保留为第二得分层。",
            landing_region_radius_m=0.35,
        )
    if situation.strategy_type == "TERMINAL_CLEAR_AND_HOLD_SIDE_HOUSE_ROLL":
        target_point = (
            K8_CLEAR_LEFT_TO_LEFT_HOUSE_ROLL
            if target is not None and target.x < HOUSE_X else K8_CLEAR_RIGHT_TO_RIGHT_HOUSE_ROLL
        )
        return make_plan(
            "terminal_clear_and_hold_side_house_roll", (target_point,),
            target.index if target else None, "physical_clear",
            "K8 当前无法一手复刻历史双营内高价值终局：清掉营内威胁后，出手壶必须停在同侧大本营外圈并成为最近壶；随后必须对真实壶面重跑对手最后一壶。",
            landing_region_radius_m=0.20,
        )
    if own_throw == 5:
        return make_plan(
            "fifth_clear_and_choose_defence_shape", defence_targets,
            target.index if target else None, "physical_clear" if target else "none",
            "第五颗时中线守壶早已可被对方击打；先处理当前有效威胁，再在当前壶数对应的多个防御形中任选一个稳定完成，而不是继续堆红圈。",
            defence_shapes,
        )

    # 第六至第八颗：上一颗对方有效壶仍是首先处理的对象；击打后的滚位由
    # “当前壶数对应的多个防御形”决定，而不是按一个固定坐标修补。
    target_index = target.index if target is not None else None
    target_action = "physical_clear" if target is not None else "none"
    return make_plan(
        "clear_then_choose_defence_shape", defence_targets,
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
        # 区域内不再因“没压到圆心”被惩罚；区域外才按到边界的距离扣分。
        score -= 45.0 * max(0.0, landing_error - plan.landing_region_radius_m)
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
    # “营内得分层”与“最内圈”不是同一个概念。K6 右侧清壶转移要求
    # 保住两颗可计分壶：旧的外侧锚可不在最内圈，不能因而把真实可行的
    # G6 误判为失败。
    own_house = sum(is_in_house(stone) for stone in own)
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
            # Unity 的 disabled 代表物理离开整张赛道；战术上的“清壶”还
            # 包含侧推到边缘废球带、或推过大本营后沿。两者都已不可能计分。
            target_ok = target is None or is_edge_dead(target)
        elif plan.opponent_action == "push_to_edge_dead":
            target_ok = target is not None and is_edge_dead(target)
        elif plan.opponent_action == "physical_displace":
            initial_target = next((stone for stone in initial if stone.index == plan.target_opponent_index), None)
            # promote/raise 的合同不要求目标出界，但必须真实离开原位；否则
            # 一个绕开目标的 draw 会被错误记成“促进”。0.20m 小于壶径，
            # 用于吸收坐标/摩擦误差，同时排除接近零位移的假碰撞。
            target_ok = bool(
                target is not None
                and initial_target is not None
                and math.hypot(target.x - initial_target.x, target.y - initial_target.y) >= 0.20
            )
            # K5 的唯一侧守壶若不能被跨摩擦稳定清出，不接受“只动了一点”的
            # 假位移。次级 G 必须把它横跨中线推到另一侧、且仍在大本营外；
            # 这会打开原侧通道，同时不把敌壶送成新的营内得分威胁。
            if plan.phase == "displace_side_guard_across_centre_and_hold_outer_roll":
                target_ok = target_ok and bool(
                    initial_target is not None
                    and not is_in_house(target)
                    and (initial_target.x - HOUSE_X) * (target.x - HOUSE_X) < -0.03
                )

    landing_ok = not plan.target_points or (active is not None and landing_error <= plan.landing_region_radius_m)

    # “清侧守壶并高位 hold”不是普通的一换一：它的目的正是让已有内圈锚
    # 和中线支撑继续组成两层结构。仅检查“没有己方壶被清出”不够，因为
    # 碰撞也可能把中线守壶拖进大本营、留下裸锚。此合同要求原角色在各个
    # 严格物理种子中仍停留在原来的功能区域。
    side_guard_support_preserved = True
    if plan.strategy_type == "CLEAR_SIDE_GUARD_AND_HOLD_OUTER_ROLL":
        final_by_index = {stone.index: stone for stone in final}
        for stone in initial:
            if stone.owner != "self":
                continue
            if _has_centre_guard((stone,)):
                after = final_by_index.get(stone.index)
                side_guard_support_preserved = side_guard_support_preserved and bool(
                    after is not None
                    and _has_centre_guard((after,))
                    and math.hypot(after.x - stone.x, after.y - stone.y) <= 0.35
                )
            if is_in_inner_ring(stone):
                after = final_by_index.get(stone.index)
                side_guard_support_preserved = side_guard_support_preserved and bool(
                    after is not None
                    and is_in_inner_ring(after)
                    and math.hypot(after.x - stone.x, after.y - stone.y) <= 0.35
                )

    # 这是比“终局仍存在任意中线守壶”更强的角色保持语义。即使新出手壶
    # 自己落进守壶带，也不能替代被本手撞开的原屏风。薄撞允许旧守壶在
    # 其屏风角色带内横移（与既有 side_guard 合同相同的 0.35m 容差）。
    initial_centre_guards = [
        stone for stone in initial
        if stone.owner == "self" and _has_centre_guard((stone,))
    ]
    final_by_index = {stone.index: stone for stone in final}
    initial_centre_guard_preserved = bool(initial_centre_guards) and all(
        (after := final_by_index.get(stone.index)) is not None
        and math.hypot(after.x - stone.x, after.y - stone.y) <= 0.35
        for stone in initial_centre_guards
    )

    # 第六至第八颗的多个防御形是“或”关系。每一个都要求本次出手壶靠近
    # 它自己的落点槽，且场面满足它声明的内圈数/保护层条件。
    def shape_is_met(shape: DefenceShape) -> bool:
        if active is None or not shape.active_targets:
            return False
        shape_landing_error = min(math.hypot(active.x - point[0], active.y - point[1]) for point in shape.active_targets)
        own_front_left = _front_house_sector_count(final, "self", "left")
        own_front_right = _front_house_sector_count(final, "self", "right")
        opponent_house = sum(stone.owner == "opponent" and is_in_house(stone) for stone in final)
        return (
            shape_landing_error <= shape.landing_region_radius_m
            and own_inner >= shape.required_inner_count
            and (not shape.require_front_guard or guard_present)
            and (not shape.require_centre_anchor or _has_centre_anchor(final))
            and (not shape.require_centre_guard or _has_centre_guard(final))
            and (not shape.preserve_initial_centre_guard or initial_centre_guard_preserved)
            and _side_gate_count(final) >= shape.required_side_gate_count
            and own_front_left >= shape.required_own_front_left_count
            and own_front_right >= shape.required_own_front_right_count
            and (shape.max_opponent_house_count is None or opponent_house <= shape.max_opponent_house_count)
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
    elif plan.phase == "fourth_rebuild_first_anchor_around_centre_guard":
        # 该状态只补第一层；要求本次出手后真正有一颗己方内圈壶，不能把
        # 经过前场但停在外环的净空球误报为完成恢复。
        goal_met = target_ok and own_inner >= 1 and landing_ok
    elif plan.phase in {"clear_then_reclaim_first_inner_anchor", "rebuild_first_inner_anchor_from_zero_own"}:
        # 零己方壶状态的一手上限就是重新建立第一颗最近营内锚。它不能被
        # defence shape 的“双层/护门”前置条件误判为无解，也不能被纯清
        # 偷换为没有得分层的状态。
        goal_met = target_ok and own_inner >= 1 and own_closest and landing_ok
    elif plan.phase == "clear_then_repair_outer_house_layer":
        # 完整双层/护门形若已被对手拆空，不能要求本手同时补回所有历史前置
        # 条件。这个显式修复合同仍须清掉当前威胁，并让出手壶进入已声明的
        # 大本营防御槽；下一手再由状态机补完整形。
        goal_met = target_ok and own_house >= 1 and landing_ok
    elif plan.phase in {"clear_then_repair_closest_scoring_anchor", "third_clear_and_roll_to_guard_aligned_recovery", "reclaim_centre_or_clear_threat", "terminal_clear_and_hold_side_house_roll", "terminal_clear_and_reclaim_centre_from_back_house_threat", "clear_side_guard_and_hold_outer_roll", "displace_side_guard_across_centre_and_hold_outer_roll", "sixth_promote_to_historical_control", "seventh_clear_and_roll_to_historical_control"}:
        goal_met = target_ok and own_closest and landing_ok
        if plan.phase in {
            "clear_side_guard_and_hold_outer_roll",
            "displace_side_guard_across_centre_and_hold_outer_roll",
        }:
            goal_met = goal_met and side_guard_support_preserved
        if plan.phase == "terminal_clear_and_reclaim_centre_from_back_house_threat":
            goal_met = goal_met and own_house >= 2
    elif plan.phase == "sixth_outdraw_single_house_threat":
        # K6 的一个独立状态边：己方只剩前场守壶、对方已有营内壶时，
        # 不把“必须清壶”误当成唯一动作。若能完全绕开旧壶并把新壶送到
        # 按钮近邻，己方成为最近壶，便把局面从单守壶转为可继续防守的
        # 营内锚。这里不依赖对手下一手，也不指向任何历史局面的坐标。
        goal_met = target_ok and own_closest and own_inner >= 1 and landing_ok
    elif plan.phase == "seventh_clear_outer_threat_and_reclaim_centre":
        goal_met = target_ok and own_closest and own_house >= 2 and landing_ok
    elif plan.phase == "sixth_clear_near_centre_front_house_threat":
        # K6 近中线前营威胁的明确状态边：必须清指定敌壶，自己留在大本营
        # 并取得最近壶；不能把一换一或仅把敌壶推开误报为已完成控制转换。
        goal_met = target_ok and own_closest and own_house >= 1 and landing_ok
    elif plan.phase == "fifth_clear_house_threat_roll_to_outer_anchor":
        # K5 的单中线守壶局面不能把清壶和滚位拆开：若唯一敌方营内壶被
        # 清出后，出手壶能够在同侧外层成为最近得分壶，就完成了从前场
        # 压力到第一颗营内锚的可恢复转移。合同不绑定任何历史盘面，只
        # 验收当前目标已失效、己方进入大本营并取得最近壶。
        goal_met = target_ok and own_house >= 1 and own_closest and landing_ok
    elif plan.phase == "seventh_outdraw_second_house_layer_behind_guard":
        # K7 若己方已经占住最近锚、对方外侧营内壶仍落后，清它并不是
        # 唯一的状态转移。净空补出由前场守壶遮护的第二营内层，能在不
        # 移动任何旧壶的前提下保留领先权和冗余。两层至少须实际分开，
        # 避免把同一碰撞线上的叠壶误计为第二得分点。
        scoring = [stone for stone in own if is_in_house(stone)]
        minimum_scoring_separation = min(
            (math.hypot(left.x - right.x, left.y - right.y)
             for index, left in enumerate(scoring) for right in scoring[index + 1:]),
            default=0.0,
        )
        goal_met = (
            target_ok and own_closest and own_house >= 2
            and minimum_scoring_separation >= 0.55 and landing_ok
        )
    elif plan.phase == "seventh_add_second_scoring_layer_without_enemy_house_threat":
        scoring = [stone for stone in own if is_in_house(stone)]
        minimum_scoring_separation = min(
            (math.hypot(left.x - right.x, left.y - right.y)
             for index, left in enumerate(scoring) for right in scoring[index + 1:]),
            default=0.0,
        )
        goal_met = (
            target_ok and own_closest and own_house >= 2
            and minimum_scoring_separation >= 0.55 and landing_ok
        )
    elif plan.phase in {"clear_then_repair_second_inner_stone", "restore_second_scoring_stone", "complete_staggered_house_pair"}:
        goal_met = target_ok and own_inner >= 2 and landing_ok
    elif plan.phase == "sixth_clear_right_threat_keep_two_layers":
        goal_met = target_ok and own_house >= 2 and landing_ok
    elif plan.phase == "eighth_raise_centre_guard_into_scoring_stack":
        # 已有两颗己方营内壶时，不执着于清左侧外圈敌壶；把中线守壶 raise
        # 入营并让新壶留在前方，形成三层得分栈，交给对方最后一壶反击验证。
        goal_met = own_house >= 3 and landing_ok
    elif plan.phase == "eighth_raise_guard_into_second_house_layer":
        # 己方已先占一颗营内壶、双方各有一颗前场守壶时，K8 的更稳终局可
        # 是 raise 己方守壶进入第二营内层，同时让出手壶留在对侧前方。两颗
        # 得分壶若仍贴成一团，会被最后一壶同线双清；因此这里把“营内双层”
        # 明确为两颗不同的得分层，而不把简单堆叠当作终局防线。
        scoring = [stone for stone in own if is_in_house(stone)]
        minimum_scoring_separation = min(
            (math.hypot(left.x - right.x, left.y - right.y)
             for index, left in enumerate(scoring) for right in scoring[index + 1:]),
            default=0.0,
        )
        # 三颗营内壶本身提供末手无法一次清空的冗余；只有两颗时才额外要求
        # 它们错层分离，避免把同线双壶误判为防线。
        goal_met = own_house >= 2 and (own_house >= 3 or minimum_scoring_separation >= 0.75) and landing_ok
    elif plan.phase == "eighth_complete_staggered_house_pair":
        # 末手前若对方无有效壶、己方只剩一枚营内锚和一枚前场守壶，优先在
        # 原锚同侧补一颗错层营内壶。它让 PPO 最后一壶即便能清前场守壶，
        # 仍无法把两个得分层同时拆掉。
        goal_met = own_house >= 2 and landing_ok
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
        score -= 70.0 * max(0.0, landing_error - plan.landing_region_radius_m)
    else:
        score -= 200.0
    return score, bool(goal_met)
