# 09 精读：A Survey of Monte Carlo Tree Search Methods

## 论文定位

这是一篇 MCTS 综述，系统梳理了 MCTS 的基本算法、UCT、常见增强、适用场景和局限。它不是冰壶专用论文，但可以帮助我们判断哪些 MCTS 组件值得引入，哪些只是增加复杂度。

对当前项目最有用的部分是：MCTS 是 anytime、asymmetric、可少量领域知识启动的搜索框架，但基础版本通常不够，需要根据领域改造 tree policy、simulation policy、progressive widening、RAVE/AMAF、并行化等模块。

## 基础算法细读

MCTS 每次迭代包含四步：

1. Selection：从根节点按 tree policy 向下选择。
2. Expansion：在未完全展开的节点添加新子节点。
3. Simulation：从新节点用默认策略 rollout 到终局或截断点。
4. Backpropagation：把结果回传更新路径上的统计。

UCT 把多臂老虎机的 UCB 用到树搜索中。典型形式是：

```text
mean_reward + C * sqrt(log(parent_visits) / child_visits)
```

第一项 exploitation，第二项 exploration。`C` 需要按领域调参。

MCTS 的特点：

- Aheuristic：理论上不需要局面评估函数，只要能模拟终局。
- Anytime：预算越多通常越好，随时可中断。
- Asymmetric：把更多搜索放到有希望的分支。

这些特点解释了为什么它适合冰壶：我们有 forward model，局面评价手写困难，搜索预算有限但可以渐进改善。

## 常见增强细读

### Progressive Widening

连续或大动作空间中，不能一开始展开所有动作。Progressive widening 根据节点访问次数逐步增加可选动作数量。

对冰壶尤其重要，因为动作是连续的。KR-UCT 和 KR-DL-UCT 都是在这个问题上进一步改造。

### RAVE / AMAF

AMAF 的思想是：一次模拟中后面出现过的动作，也可以为前面类似状态提供信息。RAVE 是更常见的平滑版本。

对围棋这类“某步棋在哪个时机下都可能有价值”的游戏很有用。对冰壶是否有用要谨慎，因为 shot 的效果高度依赖局面和顺序。不过 tactic-level 的“takeout 某个石头”“guard 某条线”可能有部分共享价值。

### Progressive Bias / History Heuristic

把启发式评价加入 selection，随着访问次数增加逐渐减弱。适合有领域知识但不完全可信的场景。

对我们来说，tactic library 和模型先验可以作为 progressive bias，初期引导搜索，后期让模拟结果接管。

### Simulation Policy

默认随机 rollout 往往很差。许多强 MCTS 系统使用规则策略、学习策略、pattern 或历史启发式改善 rollout。

冰壶中 rollout 不能纯随机，否则后续壶不现实。我们至少要使用 scripted/model policy 作为 rollout policy。

### Transposition / Information Sharing

如果不同动作序列到达相同或相似状态，可以共享统计。冰壶中完全相同状态少见，但相似状态缓存可能有价值。

### Parallelisation

MCTS 容易并行，包括 root parallel、leaf parallel、tree parallel。当前 CPU 环境可以先做 root/candidate 并行评估，复杂 tree parallel 暂不急。

## 综述中的优缺点

优点：

- 不需要精确评估函数。
- 可以逐步加入领域知识。
- 适合复杂决策树和模拟可用的场景。
- anytime 特性适合比赛限时。

缺点：

- 需要大量模拟，forward model 慢时成本高。
- 随机 rollout 质量差会误导搜索。
- 参数敏感，例如 UCB 常数、rollout 长度、扩展策略。
- 大连续动作空间需要 progressive widening 或专门方法。
- 模拟器错误会被搜索放大。

最后一点对我们最关键：如果本地物理错，MCTS 会更努力地找到“本地物理漏洞”，不一定增强官方比赛表现。

## 对数字冰壶项目的组件选择

应该优先引入：

- Progressive widening 或局部连续候选扩展。
- 模型/tactic 先验作为 progressive bias。
- 多 rollout 估计执行噪声下的期望与风险。
- 强 rollout policy，而不是随机。
- 最后一壶更高预算搜索。

可以晚点引入：

- RAVE/AMAF。
- 状态抽象和 transposition。
- 复杂 tree parallel。
- MCTS-Solver 类确定胜负证明。

不建议：

- 直接对 4D 连续动作全空间普通 UCT。
- 只用一次无噪声模拟评价 shot。
- 用随机 rollout 做训练老师。

## 和当前实现的关系

当前 `continuous_shot_search.py` 更像 root-level stochastic local search，而不是完整 MCTS。但这符合当前阶段，因为：

- 官方物理还没校准，做深树风险高。
- CPU 预算有限。
- tactic library 已经提供合理初始动作。
- 先把单壶连续动作选好，收益最大。

下一步若要 MCTS 化，可以先做两层：

1. 我方当前 shot 连续搜索。
2. 对手下一 shot 用 scripted/model response。

再往后才做多壶树搜索。

## 一句话结论

MCTS 综述说明：搜索框架本身很强，但真正有效来自领域适配。对冰壶，我们最该优先做的是 progressive widening/连续动作扩展、强 rollout policy、噪声鲁棒评估和物理校准。

