# 独立先手战术库策略

## 结论

`tactical_library_strategy/` 是与既有 `first_player_strategy.py` **完全并列**的新策略目录：旧策略没有被修改，也没有被自动替换。

它输入“先手第 K 次出手（K1..K8）+ 当前壶坐标”，输出：

1. `state_id`：47 个受支持宏观状态之一；
2. `current_goal`：本手要建立、保住或改变什么；
3. `primary_intent` 和 `alternative_intents`：交给粗代理/严格 PhysX 的离散候选；
4. `desired_next_state`：希望下一次先手出手前落到的状态；
5. `rule_constraint`、`require_strict_physx`、`require_last_reply_search`：不可跳过的验收门。

它不输出 `v/h/w`，也不执行旧策略的固定落点；因此可用作 A/B 对照、离线回放或新规划器的目标层，而不影响现有比赛提交包。

## 完整语义状态机（当前战术主线）

旧的 `plan_first_player_from_tactical_library()` 仍保留作 A/B 对照。数据驱动主线先保证完整的：

```text
K + 当前壶面
  -> 冻结的 v2 离散状态 S
  -> 同 K 的语义目标局面 G
  -> 对手回应后的 S_(K+1) 概率分布
  -> G 的可选细终点/动态绑定约束
```

`G_k` 与 `S_k` 使用同一个 K；它描述本手出完后希望出现的战术结果（新增/清除营内壶数量、
控分关系、宏观局面）。精细终点圆不是 G 是否存在的条件，而是实现 G 的子方案。对手回应不被
假设为唯一结果，因此保存的是 `P(S_(k+1) | S_k,G_k)`；下一次决策读取真实棋盘后重新分类。

调用完整语义状态机：

```python
from planning_proxy.tactical_library_strategy import load_semantic_goal_mdp

planner = load_semantic_goal_mdp()
result = planner.recommend(k=7, board=canonical_board)
```

它覆盖全部 95 个已识别状态，每个状态返回 `primary_goal` 和最多两个语义不同的回退 G；
`evidence_status` 区分五折稳定、部分跨折支持和低支持，不把存在候选写成胜利保证。

把已选 G 绑定为当前棋盘的最终局面合同：

```python
from planning_proxy.tactical_library_strategy import instantiate_recommendation

contract_plan = instantiate_recommendation(canonical_board, result)
```

合同给出当前盘面中需出界的动态角色、历史细落点圆、营内变化/控分验收条件，以及对手回应后的
`S_(K+1)` 分布。它不产生 `v/h/w`，也不把“当前搜索没找到”写成物理无解。

细落点不使用“该 G 全局最常见的圆”硬套当前棋盘。可在同一个 `S_k -> G_k` 的历史实现中检索
出手前几何最相近的案例，再把检索圆传给合同：

```python
from planning_proxy.tactical_library_strategy import (
    load_contextual_fine_retriever, contextual_regions_as_fine_options,
    instantiate_goal_contracts,
)

retrieval = load_contextual_fine_retriever().retrieve(canonical_board, result["primary_goal"])
contract = instantiate_goal_contracts(
    canonical_board, result["primary_goal"],
    fine_options_override=contextual_regions_as_fine_options(retrieval),
)
```

离线按比赛留出的比较中，该检索层对唯一新增出手壶终点的覆盖为 35.55%，同一批样本中全局细圆为
13.84%。这只是细终点预测覆盖，不是胜率、因果效应或 PhysX 可达证明。

对“零清壶 + 出手壶落入上下文圆”的合同，现已可接到既有的粗代理→严格 PhysX
Newton/MADS 求解器，并用每个摩擦种子的**完整终局棋盘**复核 `G_k`：

```python
from planning_proxy.tactical_library_strategy import solve_semantic_placement_contracts

attempts = solve_semantic_placement_contracts(
    canonical_board, contract["contracts"], own_throw_number=result["K"],
    physics_seeds=3, decision_budget_seconds=10.0,
)
```

只有 `CERTIFIED_SEMANTIC_CONTRACT` 才表示：落点圆、自由防守区合法性、完整 `G_k` 的营内变化、
控分和宏观形态都在所有已复核 PhysX 种子中成立。`NOT_FOUND_WITHIN_CURRENT_SEARCH_BUDGET`
只是当前预算/初值/算法下未找到路线，绝不是该 G 物理无解。清壶、hit-and-roll、双飞合同暂不会被
偷偷降级为 draw，仍等待各自的绑定碰撞终局验证器。

同一个已选 `S_k -> G_k` 下的多个**细圆替代方案**可以并行执行（不并行竞争不同 G，因而不改变战术排序）：

```python
from planning_proxy.tactical_library_strategy import solve_semantic_placement_contracts_parallel

attempts = solve_semantic_placement_contracts_parallel(
    canonical_board, contract["contracts"], own_throw_number=result["K"],
    physics_seeds=3, decision_budget_seconds=10.0, max_workers=3,
)
```

每个 worker 自己初始化粗代理和 PhysX 场景，先做大范围粗筛，再做 Newton/MADS 严格迭代；默认尽量做到
一候选一进程一核（同时限制 BLAS 线程为 1）。10 秒预算是**每个候选**的预算，因此三个圆在三核上约为
一轮预算的墙钟时间；返回结果仍按原始优先级排列，调用方取优先级最高的已认证候选。

清壶和双飞不再走“命中/出界就算成功”的旧口径：单清用粗代理给碰撞父分支、严格 PhysX MADS 细化；
双飞用独立双目标 MADS。两者均须验证被绑定敌壶实际出界、出手壶细圆（若合同有）、完整语义 `G_k`。
K8 的任一通过候选还会对每条己方 PhysX 终局运行有限的对手末壶严格反击筛查（直进/旋进父分支各一条、
碰撞父分支一条）；发现反例返回 `REJECTED_BY_OPPONENT_LAST_REPLY_SEARCH`，没有反例也只代表该固定反击预算
内暂未找到破局，绝不称绝对安全。

本地 PPO 对比可显式开启（默认不改变旧评测）：

```powershell
conda run -p D:\esp\tmp\curling_pyphysx_conda python planning_proxy\evaluate_vs_teammate_ppo.py `
  --proxy-team 0 --opponent ppo --semantic-tactical-library `
  --semantic-contract-budget-seconds 15 --semantic-max-workers 3
```

日志逐手写入 `semanticMdp`、检索圆、合同尝试与是否回退。一次失败的合同只会回退旧规划器；不能把回退后的对局结果
当成语义战术策略的胜率。

## 严格精细 G 子层（仅执行候选）

下列旧接口仍保留。它只返回五折共识且具有整盘谓词/细终点约束的 30 个严格 G；其余状态不代表
没有语义 G，只代表尚不能把语义 G 当作已验证的精细路径目标。

调用：

```python
from planning_proxy.tactical_library_strategy import load_goal_outcome_runtime_plan

planner = load_goal_outcome_runtime_plan()
result = planner.recommend(k=7, board=canonical_board)
```

`result["primary_goal"]` 的 `goal_state` 是可交给后续规划器尝试的严格目标：

- `terminal_board_predicate`：本手后双方营内层、控分关系和宏观形态必须满足的匿名整盘约束；
- `fine_goal_options`：出手壶终点圆区，或当前对方壶的动态清除绑定；
- `parent_action`：移出对方壶数量等战术结果；
- `primary_fold_count`、`backed_up_value_mean`：历史五折证据，而非胜利保证。

规划器必须同时满足整盘谓词与一个细约束；不能只完成“碰到/清掉一颗壶”就报告成功。若输出
`SEARCH_REQUIRED_NO_CROSS_FOLD_GOAL_OUTCOME_CONSENSUS`，表示没有足够稳定的 G，不得回退为默认清壶。

这里的 `canonical_board` 使用 NWNHT 按钮中心坐标：
`{"owner": "first"|"opponent", "x_m": ..., "y_m": ...}`。本地 PhysX 坐标的转换属于后续执行适配层；
不要混用两套坐标后直接把 G 交给求解器。

## 候选目标区域

`candidate_target_regions(board, own_throw_number)` 在战术计划之后给出不超过少量的几何候选：

- `STOP_REGION`：draw、guard 或碰后滚位希望停入的圆区；
- `STONE_CONTACT`：takeout、薄撞滚位等应首先瞄准的现有壶附近圆区。

它会排除与当前静止壶明显重叠的落位中心，并在保护期中线守壶场面只给绕守壶落位区；但不计算路径，也不能证明候选可达。

```python
from planning_proxy.tactical_library_strategy import candidate_target_regions

result = candidate_target_regions(board, own_throw_number=4)
for region in result.regions:
    print(region.region_id, region.target_kind, region.centre)
```

## 调用

```python
from planning_proxy.tactical_library_strategy import plan_first_player_from_tactical_library

plan = plan_first_player_from_tactical_library(board, own_throw_number=4)
print(plan.to_json())
```

或只查看状态：

```powershell
python planning_proxy\tactical_library_strategy\cli.py `
  --board board.json --own-throw-number 4
```

`board` 的每颗有效壶为 `{"index", "owner": "self"|"opponent", "x", "y"}`；坐标使用本地 PhysX 坐标。

## 实际接入原则

```text
战术库 plan
  -> 本地 FGZ/no-tick 过滤
  -> 按 primary + alternatives 构造少量 PhysX 目标候选
  -> 严格 PhysX 多摩擦序列验收
  -> K8 对每个真实终局再跑对方最后一壶反击搜索
```

- `DATA_SUPPORTED_*`：仅表示有通过双标签筛选的历史候选，仍需 PhysX。
- `ANTI_DEFAULT_CLEAR`：历史反证禁止把 `CLEARING` 当默认动作；它只可作为同池比较路线。
- `LOW_SUPPORT_SEARCH_REQUIRED`：不复用少样本动作。
- 任意 K8：`require_last_reply_search=True`。基准双门模板不是当前实际终局的安全证书。

历史候选统计来自 `nwnht_first_player_candidate_policy_v2_game_and_end.json`；打包环境未带训练数据时，模块用同版本的内置候选表回退。原始证据与细节见 [07_先手宏观战术树_数据支撑v0.md](../docs/strategy/07_先手宏观战术树_数据支撑v0.md)。
