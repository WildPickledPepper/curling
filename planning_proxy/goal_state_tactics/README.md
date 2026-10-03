# 终局约束战术模块

本目录与 `planning_proxy/tactical_library_strategy/` 独立。旧目录保留其“宏观意图
→ 单点候选”的实验性启发式；本目录实现新的模块边界：

```text
当前棋盘 -> GoalState（战术模块）
当前棋盘 + GoalState -> v/h/w 或当前预算内未找到（路径规划模块）
```

`GoalState` 是一条按优先级排序的状态转移边，不是出手参数，也不是一个精确的
终局棋盘。它可以同时指定：

- 以几何角色选出的关键壶必须出界、保留或落入一个范围；
- 匿名壶在关键区域的数量约束；
- 不可接受的结果；
- 真实出手后预期分类到的离散状态，以及失败回退边。

NWNHT 壶位帧没有同色壶的持久 id，因此历史工件只能产生 `StoneSelector`（如
“营内离按钮最近的对方壶”），不能输出历史固定壶号。运行时 binder 才将选择器
解析为当前 PhysX 棋盘中的 slot。

`HISTORICAL_TEMPLATE` 仅表示由公开历史壶位抽取；必须通过本地严格 PhysX 的
可达性和规则检查后，才可标记为 `PHYSX_VALIDATED`。两者都不等同于已证明胜率。

运行时入口为 `propose_goal_states(board, own_throw_number)`。它会把 NWNHT 的
按钮中心坐标转换为本地 `HOUSE_X/HOUSE_Y`，并输出已绑定当前壶 slot 的
`BoundStoneConstraint`。精细 draw/guard 边含窄圆形终局区；双飞边只要求当前
选出的两颗对方营内壶出界，不会捏造唯一的出手壶滚位。

若前两层在当前候选生成阶段都没有可绑定目标，模块最后会给出 `HISTORICAL_ZONE_FALLBACK`：它按阶段带、中心
控制和双方营内层从历史中取一个约 0.6m 网格的目标圆区。该层只用于缩小 PhysX
搜索范围，**不**承诺唯一下一精细状态，也不附加硬营内数量约束。

路径规划器返回每条摩擦种子的最终壶位后，使用 `accept_bound_goal` 统一验收；
`solve_with_fallback` 依序尝试候选，只有规划器返回合法稳定解才停止。回调必须把
“终局门拒绝”和“在当前算法/候选覆盖/计算预算内未找到”分开记录；后者**不等于物理
无解**。这样“首选双飞当前未命中 -> 单清或旋进回退”不是文字约定，而是调用方可直接
执行的控制流，同时允许未来在更大预算或更强反解器下重试首选边。

第 8 手（先手的最后一壶）生成的每个 GoalState 都带有
`require_last_reply_search=true`。这不是假定任何普通三角或侧壳天然安全；调用方必须
实际运行 `planning_proxy.validate_final_defence` 对每条我方 PhysX 终局种子逐条进行
对手最后一壶反击搜索，再用 `receipt_from_final_defence_reports` 生成与这些终局壶面
指纹绑定的 `LastReplySearchReceipt`。默认 K8 边要求搜索真实完成；发现反例会作为
反击难度证据保留，不自动等同于本手无效，因为先手目标可以是逼迫高难度末壶而非保证
对手绝不取分。空搜索、报告对应另一壶面或搜索错误都会拒绝。只有显式标为
`REQUIRE_NO_COUNTERPLAY` 的安全声明才会因反例被拒绝；当前历史 K8 模板没有这种认证。
任何通过默认门的状态也只能称为“当前预算内完成末壶反击筛查”，不能称为绝对安全终局。
若筛查使用“找到第一条反例即停止”，反例数只能说明“至少存在这些反例”，不能用于比较
两条候选哪个更难；难度排序必须使用同一候选族、同一预算且完整跑完的反击搜索。

`python -m planning_proxy.goal_state_tactics.validate_k8_single_clear_reply` 是一个完整的
代表性反例：它从支持度 797 的 K8“对方单壶 → 单清”历史边出发，先证明指定候选能
跨三条我方摩擦种子清壶，再逐条筛查对手末壶。该夹具发现反例，故展示的是**拒绝错误
安全声明、并记录末壶反击的能力，不是声称该历史边或所有单清策略无效。

`python -m planning_proxy.goal_state_tactics.validate_k8_anchor_zone_reply` 则验证一个不同
类型的高支持位置边：已有按钮锚后，历史上常补前方红圈壶。当前有界反击搜索同样找到
反例；因此它也仍是“待 PhysX 筛查的历史目标圆区”，不是已认证防线。

`python -m planning_proxy.goal_state_tactics.validate_k8_guarded_single_clear_reply` 验证
“中线守壶挡住直线、绕守壶清按钮敌壶”的历史碰撞边。它在当前反解器中可达，但末壶
反击仍能破局；因此中线守壶只能作为搜索与战术结构的一部分，绝不能被称为安全盾牌。

`python -m planning_proxy.goal_state_tactics.validate_k8_same_state_zone_alternatives` 是真正
同一当前壶面内的多候选实验：按钮锚局面同时反解三个历史区域候选。默认只作早停筛查；
加 `--complete-reply-search` 才会在同一预算下输出局部末壶压力排序。

最小调用示例：

```powershell
python -m planning_proxy.goal_state_tactics.cli `
  --board-json planning_proxy/runs/current_board.json `
  --own-throw-number 6 --active-stone-index 10
```

输入的每颗壶为 `{"index": 4, "owner": "opponent", "x": 2.2, "y": 4.9}`；
坐标必须是本地 PhysX 坐标，`owner` 只能为 `self` 或 `opponent`。输出的
`bound_stone_constraints` 已使用实际 slot，连续规划器可以直接验收这些终局约束。

完整的路径层返回格式、预算失败语义，以及第 8 手对手末壶搜索的两阶段验收流程见
[PATH_PLANNER_CONTRACT.md](PATH_PLANNER_CONTRACT.md)。
