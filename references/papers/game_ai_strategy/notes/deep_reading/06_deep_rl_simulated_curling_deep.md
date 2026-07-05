# 06 精读：Deep Reinforcement Learning in Continuous Action Spaces: Simulated Curling

## 论文定位

这篇论文把 AlphaGo Zero 式策略价值网络、KR-UCT 连续搜索和数字冰壶结合起来，是最接近我们项目目标的完整系统论文。它最终在数字冰壶比赛中获胜，说明“神经网络学全局结构 + 连续搜索精修动作”这条路线在冰壶上是可行的。

## 方法总览

论文方法可概括为：

1. 用参考程序生成监督数据，先训练 policy-value network。
2. 用网络输出离散动作先验和局面价值。
3. 在实际决策时，使用 KR-DL-UCT 从离散动作初始化，进入连续动作空间搜索。
4. 自我博弈生成 `(state, search_policy, score_distribution)` 继续训练。
5. 多 end 策略用 winning percentage table 把单 end 得分分布转化为整场胜率目标。

这套方案不是纯强化学习，也不是纯搜索，而是混合系统。

## 网络结构细读

输入表示：

- 将冰壶石头位置映射到 `32x32` 空间图。
- 用多个 feature map 表示己方石、对方石、投壶数等信息。

网络主体：

- 一层卷积。
- 九个残差块。
- 不使用 pooling，避免丢失位置精度。

policy head：

- 输出 `32 x 32 x 2` 的动作分布。
- 其中 32x32 是离散化位置/动作网格，2 是顺/逆时针旋转。

value head：

- 输出 `[-8, 8]` 共 17 个得分结果的概率分布，而不是单一标量。

这一点非常值得我们学：冰壶一 end 的结果天然是分布，尤其存在 execution uncertainty。预测分布比预测均值更能服务风险决策。

## 连续动作搜索细读

论文的 KR-DL-UCT 结合了：

- policy network 产生初始动作候选。
- kernel regression 在连续动作邻域共享价值。
- progressive widening 控制扩展。
- value network 替代手工 rollout，加快模拟。

搜索中：

- 根状态从 policy 分布采样若干动作。
- 选择动作时使用 KR-UCT 风格的 UCB。
- 扩展时在选中动作附近采样新动作，探索连续空间。
- 新状态不做长 rollout，而是直接用 value network 输出得分分布。

这正好对应我们可以做的升级：让模型提供候选，搜索做本地优化，value 头减少 rollout 成本。

## 学习流程细读

监督学习阶段：

- 使用参考程序 AyumuGAT'16 的约 40 万 state-action pairs。
- policy 学参考程序动作。
- value 不直接用最终胜负，而使用 d-depth simulation 和 bootstrapping 降低高方差。
- loss 是 policy cross-entropy + value cross-entropy + L2。

自我博弈阶段：

- 用 KR-DL-UCT 产生搜索策略 `pi` 和得分分布 `z`。
- 训练网络拟合 `(pi, z)`。
- 样本从最近自我博弈历史中均匀抽取。

多 end 策略：

- 冰壶不是只优化当前 end 得分。
- 论文构建 WP table，输入为剩余 end 数和当前分差，输出胜率。
- 用单 end 得分分布和 WP table 计算动作的整场胜率。

## 实验细读

论文使用比赛模拟器，假设冰面固定，不考虑显式擦冰，并加入非对称高斯噪声。

主要设置：

- 自我博弈每壶搜索 400 simulations。
- 连续搜索参数如 `C=0.1`、`k=20`。
- 与多个数字冰壶程序对战，包括 AyumuGAT、Jiritsukun 等。

结果：

- 监督学习加 KR 搜索已经能击败一些基线。
- 自我博弈强化后的 KR-DRL-MES 表现更强。
- 对 JiritsukunGAT'16 等程序胜率很高。
- 论文系统赢得 GAT-2018。

## 对我们项目的直接启发

1. 我们当前 MLP 版是轻量替代，不是最终形态。

   如果 CPU 约束强，MLP 可以继续用。但如果状态表达开始复杂，应该考虑小型 CNN 或 set/attention 模型。32x32 CNN 的优势是能学空间关系，缺点是 CPU 成本更高。

2. 得分分布比标量 value 更重要。

   我们下一代模型可以输出 17 类 score distribution。这样最后一壶或落后局面可以选择高方差搏命 shot，而领先局面可以选择稳健 shot。

3. 搜索应由网络初始化。

   论文不是全空间乱搜，而是从 policy network 输出开始。我们可以先用 tactic policy top-k 作为近似 policy network 初始化。

4. 官方物理校准仍是前提。

   论文用的是高保真比赛模拟器和已知噪声。我们的 `fast_curling_env.py` 只是粗代理，所以当前搜索提升只能证明本地环境有效。

5. 擦冰是我们和论文的差异点。

   论文实验不考虑显式 sweeping。我们比赛协议有 `SWEEP`，因此 sweep 应进入动作维度。当前已实现 4D 动作，但需要真实校准。

## 建议实施路线

短期：

- 保持当前 `search_distill + local continuous search`。
- 训练数据中加入连续 refinement 的最终动作。
- evaluation 输出 sweep 使用率和最终分差。

中期：

- 模型增加 value distribution head。
- 用本地搜索结果蒸馏 `(state, tactic_distribution, continuous_delta, score_distribution)`。
- 对最后一壶单独提高搜索预算。

长期：

- 官方服务器恢复后采集物理样本，重新拟合 local simulator。
- 引入 WP table，把不同 end、分差、先后手纳入目标。

## 一句话结论

这篇论文基本给出了我们项目的“完整版蓝图”：监督冷启动、搜索改进、自我博弈蒸馏、连续动作优化、得分分布价值。我们现在做的是它的 CPU 轻量版，下一步应优先补 value distribution 和物理校准。

