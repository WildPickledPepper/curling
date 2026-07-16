# 冰壶 AI 训练研究

这里记录基于严格本地模拟器的训练思路、决策和实验，不存放可直接交付的模拟器代码。

## 当前结论

主路线是：**战术候选 → 带随机摩擦的连续动作搜索 → 搜索蒸馏策略/价值网络 → 对手池自对弈**。

当前不扫冰；扫冰在协议与物理验证完成前不进入训练动作空间。

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
| [decision_log.md](decision_log.md) | 每次关键取舍的简短、可追溯记录。 |

## 资料入口

- 已收集的论文与精读：[`../references/papers/game_ai_strategy/`](../references/papers/game_ai_strategy/README.md)
- 严格模拟器：[`../local_simulator/`](../local_simulator/README.md)

## 记录规则

1. 已验证事实、文献结论、待验证假设必须分开写。
2. 任何训练结果必须写明模拟器版本、是否扫冰、对手池、样本量及先后手拆分。
3. 旧粗糙代理的胜率或分数不能作为当前严格模拟器的性能结论。
