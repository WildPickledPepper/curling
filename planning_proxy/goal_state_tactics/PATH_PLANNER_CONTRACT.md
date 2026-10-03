# 战术模块与路径规划器的对接契约

这份契约的目标是让两层各做一件事：战术模块选择**希望终局变成什么样**，路径规划器
在严格 PhysX 中寻找使其发生的 `v/h/w`。战术模块不反解路径；规划器不把“第一个能打
到的点”当战术选择。

## 1. 战术层输出

调用：

```python
proposal_set = propose_goal_states(board, own_throw_number, active_stone_index=active_slot)
```

`proposal_set.proposals` 已按优先级排序。每一条 `ProposedGoal` 含：

- `goal.transition_id`：状态机的一条边；
- `goal.source_state`：本手前的离散状态；
- `goal.expected_own_after_state`：我方本手落定后应重新分类到的状态；
- `goal.expected_after_reply_state`：历史观察到的对手答复后状态分布的最高项，**不是保证**；
- `bound_stone_constraints`：本局实际 slot 的出界/保留/圆区落点约束；
- `goal.occupancy_constraints`：匿名壶数量约束；
- `goal.fallback_transition_ids`：该条失败后允许尝试的后续边；
- `goal.require_last_reply_search`：仅第 8 手为真，表示还不能直接称为终局。

`HISTORICAL_TEMPLATE` 表示公开历史位置的模板，不能解释为因果最优或已验证胜率。

## 2. 路径层对每条边的返回

路径层必须对每个尝试的 `transition_id` 返回下列四类之一，而不是只返回 `None`：

| 状态 | 含义 | 可否把该条标为失败 |
| --- | --- | --- |
| `ACCEPTED` | 找到参数；所有摩擦种子终局都满足规则和 GoalState | 可以，进入下一阶段 |
| `NOT_FOUND_WITHIN_CURRENT_SEARCH_BUDGET` | 当前算法、候选生成、时间/算力预算内未找到 | 可暂时回退，但**不能**写成物理无解 |
| `REJECTED_BY_GOAL_GATE` | 模拟了候选，但至少一个严格终局约束未满足 | 可以回退；保留失败约束 |
| `SEARCH_ERROR` | 输入、仿真或搜索器异常 | 不能伪装成战术结论；记录后按运行策略决定是否降级 |

Python 接口对应 `SearchAttempt`；旧式回调返回 `None` 时会被规范化为
`NOT_FOUND_WITHIN_CURRENT_SEARCH_BUDGET`。

建议路径层直接调用 `solve_strict_goal_with_fallback`，并把每条严格 PhysX 求解结果包成
`StrictGoalSolution(payload, final_boards, rule_legal)`。这样路径层返回了参数也不能跳过
终局门或第 8 手反击门；函数会在当前边因几何/规则/搜索完整性被拒绝后自动尝试下一条
GoalState。默认 K8 策略遇到已记录的对手反击不会自动回退，反击强度应交给战术比较层。

一个 `ACCEPTED` 的路径层结果至少必须携带：

```text
transition_id
v/h/w
rule_legal
final_boards[physics_seed]  # 每条种子的稳定终局；每颗壶含 index/owner/x/y/yaw/enabled
```

调用 `accept_bound_goal(final_boards, ..., rule_legal=...)` 复核，而不是只依据规划器自报
成功。任何一条种子违规，整条边都不能接受。

## 3. 第 8 手的额外两阶段门

第 8 手的 `ACCEPTED` 只表示“我方这颗壶到达目标”；它仍不是防守终局。流程必须是：

```text
GoalState
  -> 严格 PhysX 反解我方出手
  -> 对每条我方终局种子做几何/规则验收
  -> 对每条终局壶面运行 validate_final_defence 的对手末壶搜索
  -> receipt_from_final_defence_reports 绑定报告与终局壶面
  -> accept_bound_goal(..., last_reply_receipt=receipt) 最终放行或回退
```

`LastReplySearchReceipt` 对每个终局壶面计算指纹。以下任一种情况均拒绝：

- 未提交末壶搜索；
- 报告数量没有覆盖我方每条 PhysX 种子终局；
- 报告中的 `fixture.stones` 与待验收终局壶面不一致；
- 严格反击候选数为零；
- 搜索错误。

默认 `REQUIRE_SEARCH_RECORD` 允许 `COUNTERPLAY_FOUND` 通过第 8 手门，但把反例数量、
路线和种子完整保留给后续的难度比较；这符合“让对手面对高难度末壶”而非“保证对手不能
得分”的目标。`SCREENED_NO_COUNTERPLAY_WITHIN_CURRENT_SEARCH_BUDGET` 仍不叫 `SAFE`：它
仅说明当前筛过的对手直进、旋进和撞击路线中未发现反例。只有未来有独立证据的结构才可
显式设为 `REQUIRE_NO_COUNTERPLAY`，此时任一反例才会拒绝终局。

## 4. 回退与重试

调用方按 `proposal_set.proposals` 的顺序执行。`NOT_FOUND_WITHIN_CURRENT_SEARCH_BUDGET`
和 `REJECTED_BY_GOAL_GATE` 都可以让本回合尝试下一条边；但前者应保留在日志中，以便
未来增加预算、改善候选覆盖或升级反解器后重新尝试同一主边。不得把“当前反解失败”倒灌
成“该战术在物理上不存在”。

如果所有历史目标边都未通过，返回的应该是“当前目标集合未获解”及完整尝试记录，而
不是声称已证明对手必胜或该局面不存在可行走法。

## 5. K8 的反击压力排序

当同一实际棋盘生成的多条 K8 候选都已完成**相同预算、完整**末壶筛查时，先调用
`screen_all_strict_goals`，再将所有通过几何/规则/搜索完整性门的结果交给
`rank_k8_proposal_set_by_reply_pressure`。它以同一次 `GoalProposalSet.runtime_core_state` 为
边界，允许同一壶面的 collision/core/zone 候选共同比较；低层工具
`rank_same_state_k8_by_reply_pressure` 仅适合来源标签也相同的候选。排序键为：

1. 不先撞壶的直接/旋进反击比例；
2. 按钮反例比例；
3. 全部反例比例；
4. 跨摩擦种子稳定反例比例。

历史支持度只在上述四项完全相同才作 tie-break。不同源状态、不同棋盘、早停反例报告
或不同候选族/预算不得混在一起排序；该函数会拒绝前两类输入，调用方必须负责统一后两类
实验条件。这是“末壶压力”的局部 PhysX 代理，不是胜率模型。
