# 队友上手指南

维护日期：2026-10-16。先跑应用，再按职责阅读源码。此次整理不提交新的 Unity 逆向分析脚本和采样；必要的物理运行依赖随应用保留。

## 三层接口

```text
当前实际壶面
  → PPO 战术选择 / 历史语义目标候选
  → 绑定当前壶的终态合同
  → 有预算的出手参数搜索
  → 完整 PhysX 终态、碰撞与规则验收
  → BESTSHOT 或当前预算未找到
```

PPO、历史统计和候选几何都不代替最终验收。已有战术合同桥接和新采样目标求解器是两套有明确边界的入口；不把它们描述成已经全部自动接通。

## 1. 准备环境

推荐 Windows x64 / CPython 3.9。下面的 `python` 必须来自该解释器，不能混用 Anaconda 中另一个 ABI：

```powershell
python -m pip install -r requirements-app.txt
python local_simulator/runtime/verify_native_runtime.py
```

自检应打印 `OK: bundled pyphysx native training loops are ready`。Windows CP38/CP313 的扩展也保留，但本轮应用和计时验收以 CP39 为准。Linux 的原生扩展需另行提供。

## 2. 跑出手求解器

```powershell
python -m training_research.shot_solver --scene training_research/fixtures/sampled_goal_draw.json
python -m training_research.shot_solver --scene training_research/fixtures/sampled_goal_collision.json
python -m training_research.shot_solver --scene training_research/fixtures/sampled_goal_double.json
```

这三个输入均来自已实际采样的构型和终态，没有把参照出手当成输入。默认每次 10 秒，成功要求一个搜索种子；完整结果和命令见 [求解器指南](../training_research/SOLVER_GUIDE.md)。

输出中 `success=true` 才读取 `shot=[v,h,w]`；失败时不能提交诊断里的 `best_effort_shot`。增加 `--required-seed-successes 3` 会要求三个搜索种子同时通过，耗时也计入同一预算；这与额外种子的独立测试应分开记录。

可选研究方案先安装 `requirements-solver-research.txt`，再传 `--search-profile wide_dfols`。其 704 题成绩为 681 个找到解、680 个严格不超过 10 秒；包括一次经核实的系统睡眠中断重跑，仍有 23 个漏解。默认方案没有切换，完整范围见 [研究记录](../training_research/solver_strategy_research_20261016.md)。输入与参照的 `record_id` 会跨文件重复，数据关联使用 [同名文件同行配对](../training_research/datasets/forward_samples_20261004/README.md)。

## 3. 看战术目标如何产生

先读 [战术库导航](TACTICS_GUIDE.md)。最快的纯 Python 示例：

```python
from planning_proxy.tactical_library_strategy import load_semantic_goal_mdp

planner = load_semantic_goal_mdp()
recommendation = planner.recommend(k=1, board=[])
print(recommendation["state_id"])
print(recommendation["primary_goal"])
```

三个默认语义 JSON 已随 Git 保留。重新训练或重建历史统计需要另行准备 NWNHT 原始数据库和中间产物。上下文精细检索也有额外工件依赖，不能把默认语义推荐可运行外推为所有历史研究脚本都无需数据。

## 4. 注意坐标与壶身份

| 接口 | 坐标 / 身份 |
| --- | --- |
| 新出手求解器、模拟器 | `x/y` 米；按钮 `(2.375,4.88)`；slot 保留实际投壶编号，`active_index` 为本次投壶编号。 |
| 历史语义状态 | `x_m/y_m` 为按钮中心原点；语义运行时使用其文档中的阵营字段。 |
| `canonical_board_to_local` | 接受 `owner=first/opponent`，映射为 `self/opponent`，再平移到本地按钮坐标；调用时保留实际 index。 |
| `goal_state_tactics` CLI | 本地 `index/owner/x/y`；`owner=self/opponent`。 |

新求解器只允许在场旧壶使用 `index < active_index`。阵营依投壶编号奇偶判定，不要把旧规划器的“slot 0 永远是本次壶”约定直接移植过来。给旧壶 yaw=0 是一项明确的输入假设，不能冒充已知真实朝向。

## 5. 验证与协作

不需要物理扩展的应用检查：

```powershell
python -m unittest discover -s training_research/tests -p "test_inverse_*.py"
python -m unittest training_research.tests.test_shot_solver_app training_research.tests.test_application_assets
python -m unittest discover -s training_data/nwnht_curling/causal_state_machine/tests -p "test_*.py"
```

不支持的 ABI 下原生检查会跳过；完整物理回归使用 [模拟器说明](../local_simulator/README.md) 的命令。原始数据库、全量采样缺失时，数据重建类测试可能跳过，不能把跳过算作通过。

改搜索：先保留完整目标与来源，用实际正向采样复测；改战术：保留候选、回退、完整终局与对手反击的证据。不要只从一次求解成功推导实战胜率，也不要把预算失败写成物理无解。

`runs/` 和 `.venv/` 不入 Git。日常从主源码改起，历史 ZIP、部署目录和大型采样不移动或删除。提交时明确区分代码改动、历史成绩和新复测成绩。
