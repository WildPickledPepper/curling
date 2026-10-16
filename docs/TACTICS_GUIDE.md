# 战术库与因果研究导航

## 先区分目标候选与因果结论

目前能用的是历史状态分类、语义目标、当前角色绑定和 PhysX 验收接口。NWNHT 观察数据的两条因果路线均未通过隔离保留集：当前没有据此发布已证明有优势的固定先手策略边。原因及区间见 [停止报告](../training_data/nwnht_curling/causal_state_machine/CAUSAL_ROUTE_STOP_REPORT.md)。

## 按工作目的找入口

| 目的 | 代码 / 文档 | 输入 → 输出 |
| --- | --- | --- |
| 当前壶面选择语义目标 | `load_semantic_goal_mdp()` | `K + 按钮原点壶面` → 当前状态、同 K 的目标、回退及对手回应后的状态分布。 |
| 绑定具体目标合同 | `instantiate_recommendation()`、`instantiate_goal_contracts()` | 当前盘面 + 已选语义目标 → 当前角色、终态落区/清壶要求。 |
| 已有战术合同求解 | `semantic_contract_physx_bridge.py` | 完整合同 → 现有放置、单清、双清或混合碰撞搜索及验收。 |
| GoalState 候选与回退 | [goal_state_tactics](../planning_proxy/goal_state_tactics/README.md) | 当前本地壶面 → 按优先级绑定的候选、终态门和末壶反击要求。 |
| 新的已采样终态反求 | [shot_solver](../training_research/SOLVER_GUIDE.md) | 实际初始场景 + 显式终态 `selection` → `v/h/w` 或未找到。 |
| 旧正式先手状态机 | `first_player_strategy.py`、[迭代日志](../planning_proxy/STATE_MACHINE_ITERATION_LOG.md) | 保留原生产入口及其失败记录，没有被此次维护自动替换。 |
| 重建/审计因果数据 | [causal_state_machine](../training_data/nwnht_curling/causal_state_machine/ARTIFACT_STATUS.md) | 原 SQLite → `S_K → U_K → S_(K+1)`、效果标签和评估工件。 |

## 最小语义推荐

```python
from planning_proxy.tactical_library_strategy import load_semantic_goal_mdp

planner = load_semantic_goal_mdp()
result = planner.recommend(k=8, board=[
    {"owner": "opponent", "x_m": 0.15, "y_m": 0.20},
    {"owner": "opponent", "x_m": 0.55, "y_m": 0.60},
])
print(result["state_id"])
print(result["primary_goal"])
```

读取 `recommendation_status` 和每条目标的证据状态；缺少支持时保留 `SEARCH_REQUIRED`，不要自行补成固定安全动作。历史坐标和角色不能直接当成当前物理壶号。

使用本地坐标的 GoalState CLI：

```powershell
python -m planning_proxy.goal_state_tactics.cli --board-json planning_proxy/fixtures/actual_final_defence_smoke.json --own-throw-number 6 --active-stone-index 10
```

这个命令只提出目标，不执行投壶。复杂合同还可能包含匿名壶数量、控分关系和对手末壶反击，不能只翻译一个落点给新反求器后就宣布整个合同通过。新 `shot_solver` 接受逐壶终态和首碰/碰撞对约束；完整合同的额外条件仍使用 [原合同接口](../planning_proxy/goal_state_tactics/PATH_PLANNER_CONTRACT.md) 复核。

## PPO 与下一步接线

队友 PPO 是离散战术选择器，旧代码用手写库产生具体出手，见 [PPO 审查](../training_research/04_teammate_ppo_review.md)。新的目标搜索不要求重新训练 PPO；接线时应把战术翻译成当前壶的目标与约束，再搜索并验收。现有模块不等于所有 PPO 战术已自动适配，更不能把当前终态采样成绩当作整场胜率。

当前值得补齐的是可执行反事实证据：同一真实壶面尝试多个可达目标、记录完整终态、对手反应和终局结果。它对应停止报告提出的下一阶段方向，不是本次文档整理已经完成的新实验。
