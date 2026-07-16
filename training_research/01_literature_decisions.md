# 文献筛选后的训练取舍

> 详细逐段结论见 [05_detailed_literature_to_system_spec.md](05_detailed_literature_to_system_spec.md)。本页只保留最终决策，避免把“论文事实”和“我们的工程取舍”混写。

## 选择的主方法：搜索蒸馏

采用 KR-DL-UCT 的结构思想：搜索负责在当前局面找更好的一手，网络学习搜索后的策略分布与结果分布。原因是冰壶同时具有连续动作、随机执行和长程对抗；裸 PPO/DQN 要直接从稀疏终局回报中学会这些内容，样本效率不适合当前严格模拟器的计算成本。

## 组件取舍

| 组件 | 结论 | 来源 |
| --- | --- | --- |
| 连续动作根节点搜索 | 现在做 | KR-UCT：相邻动作必须共享估值，按执行不确定性与置信下界选球。 |
| 策略 + 得分分布价值网络 | 第二阶段做 | KR-DL-UCT：网络提供候选和局面估值，搜索提供训练标签。 |
| 先后手 / hammer 状态 | 从 P0 数据 schema 就做 | Digital Curling NFSP 分别训练 sente/gote；KR-DL-UCT 还输入当前得分者与出壶数。 |
| 历史模型池 / 混合对手 | 搜索老师稳定后做 | NFSP：减少只克制当前对手造成的振荡，历史样本使用 reservoir 思路。 |
| 最后一壶专用高预算 | 从 P0 开始单独标记，P3 接 WP | Hammer Shot：最后一壶没有后续响应，适合集中搜索预算；但真正的冒险选择要由全场 WP 决定。 |
| 全局深 MCTS | 暂缓 | 严格模拟器成本高，先验证根节点连续搜索是否严格优于固定战术库。 |
| 纯 PPO / 纯 DQN | 不作为主线 | 连续动作、随机物理、自对弈非平稳性使其早期成本过高。 |
| 显式扫冰训练 | 暂缓 | 当前非扫冰交付范围。 |

## 核心文献

- KR-UCT：`references/papers/game_ai_strategy/notes/deep_reading/05_kr_uct_curling_deep.md`
- KR-DL-UCT：`references/papers/game_ai_strategy/notes/deep_reading/06_deep_rl_simulated_curling_deep.md`
- Digital Curling NFSP：`references/papers/game_ai_strategy/notes/deep_reading/07_digital_curling_nfsp_deep.md`
- Hammer Shot：`references/papers/game_ai_strategy/notes/deep_reading/08_hammer_shots_curling_deep.md`
