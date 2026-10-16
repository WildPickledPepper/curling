# Curling AI：战术目标与出手求解

面向队友的主线是：**当前壶面 → 战术目标 → 出手参数搜索 → 完整物理终态验收**。队友 PPO 可以提供战术选择，历史战术库可以提供目标候选，求解器负责搜索 `BESTSHOT(v, h, w)`。

先看 [队友上手指南](docs/TEAM_GUIDE.md)，再按需要进入 [求解器应用](training_research/SOLVER_GUIDE.md) 或 [战术库导航](docs/TACTICS_GUIDE.md)。完整目录分类见 [PROJECT_INDEX.md](PROJECT_INDEX.md)。

## 当前能用到哪一步

| 部分 | 入口 | 当前边界 |
| --- | --- | --- |
| 完整终态目标反推出手 | [shot_solver.py](training_research/shot_solver.py) | 可直接调用 Python API 或 CLI；10 秒默认预算，未找到则返回空动作。 |
| 历史语义战术库 | [tactical_library_strategy](planning_proxy/tactical_library_strategy/README.md) | 读取当前状态，给出目标和回退；目标还要经过当前壶面绑定和物理验收。 |
| GoalState 合同与回退 | [goal_state_tactics](planning_proxy/goal_state_tactics/README.md) | 有角色绑定、终态门和末壶反击检查；复杂合同使用其原有桥接器。 |
| 因果策略研究 | [因果路线结论](training_data/nwnht_curling/causal_state_machine/CAUSAL_ROUTE_STOP_REPORT.md) | 保留集未证明优势，不能把历史目标候选称为已认证的因果制胜策略。 |
| PPO 对接与造数据 | [数据契约](training_research/inverse_dataset/README.md) | 局面/目标共用编码器；当前不要求先训练反推网络。 |
| 完整正向预测 | [local_simulator](local_simulator/README.md) | 给起始壶面和出手，完整推演至停止；当前应用范围为不扫冰。 |

2026-10-04 的本地原始采样测试：**292/306（95.4%）** 在单导航种子下找到解，14 个双飞构型全部通过；每局 10 秒预算，成功耗时中位数 **2.806 秒**。仍有 14 局未解出；找到的解在额外五种子全部通过为 **237/292**。这是指定采样集的搜索成绩，不是实战胜率或任意局面保证。见 [结果与范围](training_research/inverse_solver_optimization_20261004.md)。2026-10-16 的维护只整理入口与随包依赖，没有重新生成这一成绩。

## Windows 快速开始

推荐 **64 位 CPython 3.9**；在仓库根目录运行。若 `py -3.9` 不可用，请替换为自己的 Python 3.9 解释器。

```powershell
py -3.9 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-app.txt
.\.venv\Scripts\python.exe local_simulator/runtime/verify_native_runtime.py
.\.venv\Scripts\python.exe -m training_research.shot_solver --scene training_research/fixtures/sampled_goal_draw.json
```

原生扩展和应用需要的小型经验库已随仓库保留，运行上述样例不需要本机旧交接包、Unity 安装、PPO 权重或完整采样目录。`success=true` 时 `shot` 才是可提交的出手；`success=false` 表示当前预算内没找到，不等于物理无解。

批量测试可用随仓库保存的 [精简正向采样](training_research/datasets/forward_samples_20261004/README.md)：37,061 条、306 个构型，压缩约 4.03 MiB；求解输入与参照答案分别保存。

只看历史语义目标可运行以下代码，不会做 PhysX 搜索：

```python
from planning_proxy.tactical_library_strategy import load_semantic_goal_mdp
result = load_semantic_goal_mdp().recommend(k=1, board=[])
print(result["state_id"], result["primary_goal"])
```

## 协作与文件保存

日常修改主源码，不修改历史发布副本；改动要保留对应的目标、验收范围和回归结果。规则见 [AGENTS.md](AGENTS.md)。

- `training_research/`：新出手求解、样本构造、编码和搜索验收。
- `planning_proxy/`：策略、战术合同、既有 PhysX 桥接和完整对局评测。
- `training_data/nwnht_curling/`：历史壶谱分析和默认语义资产。
- `local_simulator/`：运行所需的模拟器与原生依赖。
- `runs/`、原始 Unity 采样、第三方数据库、训练权重、历史打包副本：本地证据或按需另行准备，不能把本地报告路径当成克隆后即有的文件。

当前维护不新增提交 Unity/PhysX 逆向分析过程资料。原有历史说明和逆向记录可从 Git 历史及已有证据索引追溯。
