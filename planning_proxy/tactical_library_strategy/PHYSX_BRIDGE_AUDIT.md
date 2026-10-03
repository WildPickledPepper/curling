# v2 战术目标到既有 PhysX 反解器：最小闭环审计

## 结论

新 v2 战术 StatePlan 已能把一个有跨折证据的终局圆域，交给既有：

```text
连续粗代理初值搜索 -> 严格 PhysX -> Newton / MADS -> 多摩擦终局验收
```

的连续求解链。桥接代码位于 `physx_goal_bridge.py`；它不改旧
`first_player_strategy.py`、`ProxyMatchPlayer.choose()` 或比赛入口。

当前桥接范围刻意只包含 `ACTIVE_STONE_PLACEMENT` 的**净空落位**。碰撞、
双飞、raise、runback 等动作会返回
`REQUIRES_COLLISION_GOAL_CONSTRAINTS`，直到 v2 动作能够为它们给出关键壶的
去留/落点约束；它们绝不能被默认翻译成“清附近敌壶”。

## 已实际完成的一条严格 PhysX 冒烟（2026-07-17）

输入是 K1 空场，v2 跨折窄目标：

```text
state       = K1_V2_EMPTY_1
action      = nwnht_v2_tactical_action_5139a3bc43b11aba (BUTTON)
target      = local (2.378264, 5.288314), radius 0.173160m
precision   = NARROW_CROSS_FOLD_GOAL
```

在 3 条 PhysX 摩擦序列、40 秒总预算下，结果为：

```text
status                  CERTIFIED_CLEAR_PATH
coarse initial shots    425 (5 x 17 x 5)
strict physics calls    23
solver                  newton_clear_path
max landing error       0.038637m
mean landing error      0.030650m
free-guard legality     true
v/h/w                   (3.098602612, -2.207565327, 15.000629408)
```

这证明的仅是：该**一条**数据支持的 K1 目标，能被当前本地求解器从粗代理
初值反解并通过三序列的终局圆域与规则复验。它不证明按钮策略总体最优、不能
证明 42 个动作都可达、更不能证明最终胜率。

## 接口及失败语义

```text
K + local board
 -> RuntimeStatePlan
 -> CircleGoalRequest[主动作圆域, 同动作其他圆域, 备动作圆域]
 -> solve_clear_path_circle_requests(...)
 -> CERTIFIED_CLEAR_PATH 或逐条未命中记录
```

- `CERTIFIED_CLEAR_PATH`：每条配置摩擦序列均通过已有的规则、旧壶静止及圆域验收。
- `NOT_FOUND_WITHIN_BUDGET`：当前粗代理覆盖、Newton/MADS 和预算未找到已认证净空解；不是物理无解。
- `NOT_ATTEMPTED_BUDGET_EXHAUSTED`：前序按优先级请求耗尽总预算。
- `REQUIRES_COLLISION_GOAL_CONSTRAINTS`：本动作不是可以诚实降成净空 draw 的类型。

## 后续边界

1. 将 v2 碰撞动作补成“指定哪些当前壶移出/保留/进入范围”的终局谓词，再接现有 MADS 碰撞分支；
2. 为各类目标分别做少量代表性多摩擦 PhysX 夹具，而非大规模盲采样；
3. K8 每个通过的我方终局仍要接对手最后一壶反击搜索，普通守壶/三角不自动成为安全终局。
