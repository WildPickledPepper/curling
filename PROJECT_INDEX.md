# DCCourse 项目索引

更新：2026-10-03。这个文件只做导航与保留分类；**不会移动、删除或覆盖任何文件**。
目录中存在其他会话的改动时，先以本索引定位，再只修改明确属于当前任务的源文件。

## 先从这里进入

| 目的 | 打开位置 | 说明 |
|---|---|---|
| 模拟器、预测计时与精度证据 | `local_simulator/README.md`、`analysis_input/README.md` | 当前物理主线及验证范围；原始采样留在本地。 |
| 看策略状态机与当前结论 | `planning_proxy/STATE_MACHINE_ITERATION_LOG.md` | 状态机、求解器、失败反例与撤回记录的唯一连续日志。 |
| 本地开发/解释器/平台入口 | `planning_proxy/DEVELOPMENT_RUNBOOK.md` | Python ABI、PhysX 扩展、PowerShell、课程平台与对战平台边界。 |
| 修改正式先手逻辑 | `planning_proxy/first_player_strategy.py`、`planning_proxy/evaluate_vs_teammate_ppo.py` | 先读迭代日志；未完成证据门槛时不得加入新生产状态边。 |
| 看严格物理与粗代理 | `planning_proxy/strict_refine.py`、`planning_proxy/analytic_proxy.py`、`local_simulator/` | 粗代理只生成/排序候选；严格 PhysX 才认证。 |
| 看真实 fallback 与实验报告 | `planning_proxy/RUNS_INDEX.md`、`planning_proxy/runs/` | `runs/` 有大量历史报告，先按索引找，不要按文件名猜结论。 |
| 课程平台运行 | `planning_proxy/server_linux_cp39_physx_state_machine_20260721_direct/README_课程Notebook_Linux_CP39.md` | Linux CP39 包；不与对战平台根目录混用。 |

## 目录分类

### A. 当前运行源码：日常开发优先看

| 位置 | 分类 | 作用 |
|---|---|---|
| `planning_proxy/` | 正式策略与求解源码 | 状态机、候选生成、严格回放、测试、诊断、打包工具的主目录。 |
| `local_simulator/` | 正式严格模拟器 | PhysX 运行时、加载器、规则环境和物理资产。 |
| `AIRobot.py`、`tools/protocol/` | 对战协议入口 | 课程机器人通信基类及协议。 |
| `planning_proxy/tests/` | 回归测试 | 规则、状态语义与物理桥接检查。 |
| `planning_proxy/fixtures/` | 小型固定盘面 | 可复现的局部物理/合同测试输入。 |

### B. 当前研究资产：有用，但不能直接提交

| 位置 | 分类 | 使用边界 |
|---|---|---|
| `planning_proxy/diagnostics/` | 离线诊断 | 定位 fallback、覆盖和耗时；默认不改变正式选择器。 |
| `planning_proxy/solver_benchmark/` | 求解器基准 | 验证等价性、耗时与召回；不代表对局胜率。 |
| `planning_proxy/docs/strategy/` | 策略研究文档 | 已从规划器顶层归位；是历史战术与设计材料，不等于当前验收结论。 |
| `planning_proxy/goal_state_tactics/`、`planning_proxy/tactical_library_strategy/` | 战术角色与历史语义 | 只能给当前盘面提供候选角色，不能直接按历史坐标提交。 |
| `planning_proxy/STATE_MACHINE_ITERATION_LOG.md` | 实验证据账本 | 生产改动前必须补齐正例、反例、完整续局、种子和耗时。 |
| `planning_proxy/STATE_MACHINE_RECOVERY_20260718.md` | 历史恢复背景 | 旧结论必须与当前日志交叉核对，不能当作当前版本胜率。 |
| `training_research/` | 对手、训练和研究代码 | PPO/aggressive 主要用于离线验收，不是线上状态机依赖。 |
| `training_data/` | 历史壶谱数据 | 用于抽取局面/战术角色，不是正式物理裁决。 |
| `unity_planner.jsonl` | Unity 实战日志 | 当前真实平台失败与回退的首要来源。 |

### C. 发布/部署副本：只在对应平台打包时使用

这些目录是某一时刻复制出去的发布副本，**不是主源码**。日常修复请先改 A 类源文件，再用对应打包脚本生成新包。

| 位置 | 面向平台 | 状态 |
|---|---|---|
| `planning_proxy/submission/`、`planning_proxy/submission_direct/` | 对战平台提交副本 | 保留；避免与主源码双向修改。 |
| `planning_proxy/archive/deployment_directories/server_py313_physx_state_machine_20260721/` | Windows CP313 服务端 | 已归档的历史发布包。 |
| `planning_proxy/server_linux_cp39_physx_state_machine_20260721_direct/` | 课程 Notebook Linux CP39 | 当前课程平台参考包。 |
| `planning_proxy/archive/deployment_directories/server_linux_cp39_physx_state_machine_20260721_backhand_draw/` | 课程 Notebook 旧变体 | 已归档；不作为默认课程包。 |
| `planning_proxy/archive/deployment_directories/teammate_state_machine_package_20260721/` | 队友独立包 | 已归档的对外分发快照。 |
| `planning_proxy/archive/deployment_directories/teammate_opponent_package_20260719/` | 队友对手包 | 已归档的对外分发快照。 |
| `planning_proxy/archive/deployment_snapshots_20260721/` | 压缩发布物 | 已归档的上传/回滚快照；不要在压缩包内改代码。 |

### D. 资料与外部基线：保留，不进入当前运行路径

| 位置 | 作用 |
|---|---|
| `references/`、`images/`、`notebooks/`、`tacticslib/` | 课程资料、图像、Notebook 与战术参考。 |
| `external_research/` | 外部开源/论文复现材料。 |
| `数字冰壶单机版_win/` | Unity 单机版；需要采样或 UI 对照时才打开。 |
| `research_archive/` | 历史反推、旧模型、旧日志，约 9.9GB；不属于当前运行路径。 |

### E. 归档候选：当前不删除

下列内容不是“无用”，而是**不应占据日常视线、也不能未经确认删除**的候选：

| 位置/模式 | 原因 | 建议标签 |
|---|---|---|
| `planning_proxy/runs/` 的未索引旧报告 | 历史实验产物多，跨版本结论不能直接复用。 | `历史证据` |
| `__pycache__/`、`*.pyc` | 可再生成缓存。 | `可清理缓存` |
| `archive/platform_probe_20260724/` | 已移动的平台探测/安装包快照。 | `部署探测留档` |
| `archive/third_party_and_model_snapshots/` | 已移动的外部和阶段性压缩快照。 | `历史压缩包` |
| `planning_proxy/archive/deployment_snapshots_20260721/` | 已移动的版本化发布压缩快照。 | `历史发布物` |

在人工确认用途、校验哈希并备份前，不移动、不删除这些文件。若未来需要瘦身，应先建立 `archive/manifest.json`，逐项记录原路径、哈希、保留原因和恢复方式。

## 体积概览（2026-07-24）

| 区域 | 约占用 | 结论 |
|---|---:|---|
| `research_archive/` | 9.86GB | 最大历史资料区。 |
| `training_data/` | 2.87GB | 历史壶谱数据。 |
| `planning_proxy/` | 245MB，其中 `runs/` 146MB | 当前代码和报告都在这里；先用报告索引。 |
| `training_research/` | 159MB | 训练/对手研究。 |
| `数字冰壶单机版_win/` | 169MB | Unity 对照程序。 |
| `local_simulator/` | 31MB | 当前严格物理运行时。 |

## 简单规则

1. 改策略：只从 `planning_proxy/` 主源码开始，不在发布副本中改。
2. 查失败：先看 `unity_planner.jsonl`、`STATE_MACHINE_ITERATION_LOG.md` 和 `RUNS_INDEX.md`。
3. 新实验：脚本放 `planning_proxy/diagnostics/`，报告写 `planning_proxy/runs/`，再向迭代日志登记结论。
4. 新发布：从主源码打包；发布目录和压缩包只作产物。
5. 清理：先更新本文件和清单，再进行任何移动或删除。

## Git 保存范围（2026-10-03）

Git 保存主源码、必需的 PhysX/数学运行时、小型测试夹具、分析脚本与验收报告。
Unity 原始日志、完整 Wasm/WAT、训练 artifacts、发布副本及压缩快照保留在本地，由忽略规则排除。
原有文件归位已按 SHA-256 核验，见 `archive/manifest.json`；两份策略文档同时保留已有内容修订，原版本仍可从 Git 历史恢复。
未跟踪文件的整理前盘点见 `analysis_input/repository_inventory_20261003.json`，约 9.05 GB；这是未跟踪内容的体积，不是整个工作区的总占用。
