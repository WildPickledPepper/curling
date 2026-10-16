# 冰壶 AI 训练研究

队友应用入口：先看 [求解器使用指南](SOLVER_GUIDE.md)，直接调用 `BudgetedShotSolver` 或 `python -m training_research.shot_solver`。经验初值库和数学提案依赖已随包保留，三份实际采样输入可直接冒烟；下方保留此前研究路线与历史实验导航。

这里记录基于严格本地模拟器的训练思路、决策和实验，不存放可直接交付的模拟器代码。

## 当前结论

主路线是：**战术候选 → 带随机摩擦的连续动作搜索 → 搜索蒸馏策略/价值网络 → 对手池自对弈**。

当前不扫冰；扫冰在协议与物理验证完成前不进入训练动作空间。

2026-10-16 最新完成的可选 `full_augmented` 为 **684/704（97.16%）**，成功项全部严格不超过 10 秒，中位数约 0.205 秒；覆盖 306 个构型和 17 类标签，仍有 20 个漏解。它依赖离线学习权重，克隆后需按指南重建；额外 1024 题对照仍在运行。不依赖学习权重的 `wide_dfols` 为 681/704，其中 680 项严格不超过 10 秒，包含一次有证据的系统睡眠中断重跑。两者运行顺序与分区不同，未据此自动切换默认。见 [10 秒求解研究](solver_strategy_research_20261016.md) 和 [固定目录与验收证据](benchmarks/README.md)。

公开默认仍为 `baseline`，其 2026-10-04 历史完整复测为 **292/306（95.4%）**，成功中位数 2.806 秒，独立五种子全通过 237/292。不同配置与目录的成绩不能直接合并。历史实现与剩余任务见 [碰撞逆向求解优化](inverse_solver_optimization_20261004.md)。

首次阅读请先看：[训练路线总说明](训练路线总说明.md)。它用完整中文说明模拟器、搜索、模型分别做什么，以及 P0–P4 如何衔接。

## 文件导航

| 文件 | 用途 |
| --- | --- |
| [训练路线总说明.md](训练路线总说明.md) | **主入口**：完整说明训练思路、学习方式、阶段与验收条件。 |
| [00_scope_and_status.md](00_scope_and_status.md) | 已确认事实、边界与不应混入的旧结论。 |
| [01_literature_decisions.md](01_literature_decisions.md) | 文献筛选后的训练方法取舍。 |
| [02_target_training_system.md](02_target_training_system.md) | 目标训练闭环与最小可实施版本。 |
| [03_experiment_backlog.md](03_experiment_backlog.md) | 下一批实验、验收指标和优先级。 |
| [04_teammate_ppo_review.md](04_teammate_ppo_review.md) | 队友 PPO 版本的结构、优缺点及作为对手的接入方案。 |
| [05_detailed_literature_to_system_spec.md](05_detailed_literature_to_system_spec.md) | 文献逐项核对后形成的状态、标签、角色和验收规范。 |
| `p0_kernel_end_teacher.py` | P0.1 正式采集器：只采 end 最后五手，候选均继续推演至真实终局得分。 |
| `p0_kernel_benchmark.py` | P0.1 验收：同一固定局面、独立随机序列下比较 kernel 搜索与固定战术。 |
| [inverse_dataset/](inverse_dataset/README.md) | 当前加速模拟器批量造数据：局面/参数覆盖、完整终态、目标重标注、16×14 输入编码与分片续采。 |
| [旧双飞初值测试](inverse_solver_legacy_evaluation_20261004.md) | 旧公式/几何初值接入当前严格模拟器，与直线入口进行固定大核的 20 局对照。 |
| [有预算的双飞求解](inverse_initial_optimization_20261004.md) | 快速入口、缓存几何初值与预算迭代，可调用 API 默认十秒上限，含五秒/十秒配置的 40 局对照。 |
| [本地已知解调初值](inverse_initial_known_case_tuning_20261004.md) | 已纠正数据来源：原始正向采样的 6 个终态任务重新测试；历史构造 40 局和混合来源 27/26 局另作记录，默认原方法。 |
| [全部采样构型测试](inverse_sampled_suite_20261004.md) | 历史首轮：六批原始采样全部 306 个构型，单种子 208/306；数据来源、目标定义和鲁棒性范围。 |
| [98 个失败请求诊断](inverse_miss_diagnosis_20261004.md) | 历史分支修复与诊断：59 项无碰撞任务修复，形成 267/306 基线；其余 39 项做离线初值与粗细迭代对照。 |
| [碰撞逆向求解优化](inverse_solver_optimization_20261004.md) | 默认方案历史复测：其他构型经验初值、联合终态拟合、多初值和多尺度搜索；292/306，预算 10 秒。 |
| [10 秒求解研究](solver_strategy_research_20261016.md) | 可选搜索方案、704 题结果、难例实验、数据配对修正及尚未完成的回归。 |
| [固定目录与验收证据](benchmarks/README.md) | 可移植任务目录、704 题成功证据及复现方法；原始前向真值与逆向搜索结果分别保存。 |
| [decision_log.md](decision_log.md) | 每次关键取舍的简短、可追溯记录。 |

## 资料入口

- 已收集的论文与精读：[`../references/papers/game_ai_strategy/`](../references/papers/game_ai_strategy/README.md)
- 严格模拟器：[`../local_simulator/`](../local_simulator/README.md)

## 记录规则

1. 已验证事实、文献结论、待验证假设必须分开写。
2. 任何训练结果必须写明模拟器版本、是否扫冰、对手池、样本量及先后手拆分。
3. 旧粗糙代理的胜率或分数不能作为当前严格模拟器的性能结论。
