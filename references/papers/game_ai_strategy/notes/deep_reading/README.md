# 精读总结索引

这一层是逐篇论文的较详细读书报告，区别于上一层短 notes。每篇都按“问题、方法、实验、对数字冰壶项目的可迁移点、风险/不能照搬处”来整理，目的是服务后续训练策略，而不是只复述摘要。

## 逐篇精读

- [01 AlphaZero 自我博弈](01_alphazero_self_play_deep.md)
- [02 AlphaGo Zero 无人类知识训练](02_alphago_zero_deep.md)
- [03 NFSP 不完美信息自我博弈](03_nfsp_self_play_deep.md)
- [04 Elastic MCTS 状态抽象](04_elastic_mcts_state_abstraction_deep.md)
- [05 KR-UCT 连续动作冰壶搜索](05_kr_uct_curling_deep.md)
- [06 KR-DL-UCT 数字冰壶深度强化学习](06_deep_rl_simulated_curling_deep.md)
- [07 数字冰壶 NFSP](07_digital_curling_nfsp_deep.md)
- [08 Hammer Shot 最后一壶动作选择](08_hammer_shots_curling_deep.md)
- [09 MCTS 方法综述](09_mcts_survey_deep.md)

## 当前对项目最关键的三篇

1. [05 KR-UCT 连续动作冰壶搜索](05_kr_uct_curling_deep.md)
2. [06 KR-DL-UCT 数字冰壶深度强化学习](06_deep_rl_simulated_curling_deep.md)
3. [08 Hammer Shot 最后一壶动作选择](08_hammer_shots_curling_deep.md)

它们直接支撑当前路线：tactic/model 给初始候选，连续搜索做局部 refinement，执行噪声和擦冰进入动作评价，最后一壶单独提高预算。

## 综合决策

- [论文到训练决策映射](PAPER_TO_TRAINING_DECISIONS.md)
