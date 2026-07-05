# 06 Deep RL in Continuous Action Spaces: Simulated Curling

## 这篇解决什么问题

这篇把 AlphaGo 式 policy-value network 和 KR-UCT 连到数字冰壶。它承认纯离散动作网络不适合冰壶，因为很小的动作变化会导致结果巨大差异；但纯连续搜索又太慢。因此采用“网络学全局结构，搜索做连续精修”的框架。

## 方法拆解

网络输入是离散化后的冰壶状态特征图，论文中使用 32x32 位置网格，不做 pooling 以保留空间精度。网络输出两部分：

- policy head：动作分布。
- value head：最终得分分布，范围是 `[-8, 8]`。

训练分两段：

- 监督学习：用参考程序生成约 40 万个 state-action 样本。value 不只靠最终结果，而是用 d-depth simulation 和 bootstrapping 降低随机回报方差。
- 自我博弈强化学习：每步用 KR-DL-UCT 搜索，得到搜索策略分布和价值目标，再训练网络拟合。

KR-DL-UCT 的思想是：网络先给动作候选和价值评估，KR-UCT 在连续空间里围绕候选搜索，最后把搜索后的策略再投影回网络。

## 实验和结论

论文报告训练后的程序超过已有带手工特征的程序，并赢得国际数字冰壶比赛。对我们最有用的不是冠军结论，而是工程流程：先 imitation/reference bootstrapping，再 self-play search distillation，最后在线用搜索增强。

## 对我们数字冰壶的启发

我们现在的 search-distill 已经是这篇的简化版，但缺三块：

- value head 应从单标量升级到得分分布，至少能区分小胜和大胜。
- 动作应从 tactic index 扩展到 tactic + continuous refinement。
- 训练对手应从随机对手升级到模型池/平均策略，否则策略会对随机局面过拟合。

CPU 可行路线：不做大 CNN，继续用向量特征 + MLP；重点先实现连续微调搜索和更真实模拟，而不是堆网络。

## 局限

论文使用高保真模拟器和大量数据。我们目前本地代理很粗糙，不能直接相信模拟成绩。应先做官方物理校准，再把这套 pipeline 扩大。

