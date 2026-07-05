# 08 精读：Action Selection for Hammer Shots in Curling

## 论文定位

这篇论文专门研究冰壶每个 end 的最后一壶，也就是 hammer shot。它去掉了对手后续响应，只关注一个低维连续、随机、非凸优化问题：给定当前局面，最后一壶怎么选才能最大化胜率。

对我们项目非常有价值，因为最后一壶往往直接决定得分，而且与普通中盘 shot 的目标不同。论文还明确讨论了为什么不能只最大化期望得分 EP，而要根据比赛局势最大化 winning percentage WP。

## 问题细读

动作空间：

- 两个连续维度：角度 `theta` 和速度 `v`。
- 一个二元维度：旋转方向 turn。
- 论文不显式建模 sweeping，而是把 sweeping 的主要作用合并到执行噪声模型中。

转移模型：

- 用物理模拟器根据初速度、角度、旋转确定无噪声结果。
- 用执行模型把 intended shot 扰动为实际 shot。
- 执行误差服从重尾 Student-t 分布，参数调到接近奥运级人类投壶能力。

目标函数：

- 不是单纯本 end 期望分 EP。
- 而是根据剩余 end 数和当前分差，最大化整场 winning percentage。

论文举了很典型的例子：最后一局落后 2 分时，稳定拿 1 分没有意义，因为仍然输；20% 概率拿 3 分的高风险 shot 可能才是正确选择。

## 方法细读：Delaunay Sampling

论文改造了基于 Delaunay triangulation 的非凸优化方法，称为 Delaunay Sampling，简称 DS。

基本思想：

1. 先在连续动作空间中采样一些点。
2. 用 Delaunay triangulation 把动作空间划分为多个区域。
3. 每个区域根据面积和顶点得分计算权重。
4. 早期更关注大区域探索，后期更关注高分区域 exploitation。
5. 最后把 promising regions 当作多臂老虎机的 arms，用 UCB 再选择最终 shot。

区域权重形式体现了两个因素：

- 区域面积大，说明探索不足。
- 顶点得分高，说明附近可能有好 shot。

这很适合 hammer shot 的非凸热力图：好 shot 区域往往很小，被坏区域包围。

## 实验细读

数据：

- 使用 2010 温哥华冬奥男子和女子冰壶比赛的 hammer shot 局面。
- 参数调优集 397 个局面。
- 测试集 515 个局面。

比较方法：

- DS
- HOO
- PSO
- CMA-ES
- GPO
- 奥运人类选手实际结果

采样预算：

- DS 使用 500 到 3000 samples。
- 选择 shot 后用模拟采样估计 WP。
- 每个测试状态重复多次评估。

结果：

- 在所有相同采样预算下，DS 的平均 WP 显著高于其他优化算法。
- sample budget 越大，DS WP 越高，从约 0.4956 到 0.5343。
- 奥运选手实际 hammer shot 平均 WP 约 0.4893。
- DS 在预算 500 时不显著优于人类，但更高预算下显著优于人类。
- 仍有约 20% 局面中人类选择优于 DS。

论文也非常诚实地列出限制：

- 人类实际 shot 只观察一次，无法知道其 intended shot 的期望值。
- 执行模型可能与真实人类不完全一致。
- 手工记录的石头位置可能有误差。
- 物理模拟器不是真实冰面。

## 对我们项目的直接启发

1. 最后一壶应单独加预算。

   hammer shot 没有对手后续，不需要深树搜索，可以把预算集中到当前 shot 的连续优化。我们的机器人可以在最后一壶使用更大的 `--search-candidates` 和 `--search-rollouts`。

2. 目标应根据局势变换。

   领先时选低风险稳得分/保分 shot，落后时可能需要高方差搏命 shot。不能总最大化期望得分。

3. 选择 robust shot，不选窄缝极限 shot。

   论文中的例子显示，穿窄缝 draw 虽然无噪声得分高，但风险大；raise 可能更鲁棒。这和我们当前本地搜索要多 rollouts 完全一致。

4. Delaunay Sampling 可以作为最后一壶专用优化器。

   当前实现是局部扰动搜索。后续可以为 hammer shot 加一个更全局的二维/四维采样优化版本，尤其在候选库漏掉关键 shot 时有用。

## 擦冰相关

论文没有把 sweeping 作为显式动作，这一点与我们的比赛协议不同。论文承认 sweeping 除了降低误差，还能让石头走更远、减少 curl、改变末段轨迹。我们的动作空间应包含 sweep distance，而不是仅把它当噪声缩小。

因此对我们来说，hammer shot 优化空间应为：

```text
(v0, h0, w0, sweep_distance)
```

不过维度从 2D/turn 增到 4D 后，Delaunay triangulation 会更贵，短期可以在 tactic 候选附近做局部搜索，长期再考虑分层：先选 `(h, v, turn)`，再调 sweep。

## 一句话结论

最后一壶不是普通 shot。它应该用更高预算、按整场胜率而非期望分选择，并显式考虑执行噪声。我们当前 local continuous search 是起点，后续应增加 hammer-shot 专用策略。

