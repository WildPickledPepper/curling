# 07 精读：A Game Strategy Model in the Digital Curling System Based on NFSP

## 论文定位

这篇论文尝试把 NFSP 和 KR-UCT 结合到数字冰壶中，目标是减少对大量人工监督数据和先验知识的依赖，同时让策略向 Nash equilibrium 靠近。它的实验和表述没有 KR-UCT、KR-DL-UCT 那么扎实，但提供了一个有用方向：冰壶训练不能只追求单一 best response，应考虑平均策略、对抗训练和 exploitability。

## 方法细读

论文把数字冰壶看作二人零和 extensive-form game。每个玩家有两个网络：

- 强化学习策略网络，用于拟合 best response。
- 监督学习网络，用于学习平均策略。

与 NFSP 原论文类似，它使用：

- reservoir sampling 保存平均策略数据。
- anticipatory dynamics 稳定自我博弈。
- 对先手和后手分别训练网络，因为两者策略差异很大。

输入表示：

- 冰壶 house 区域离散为 `32 x 32`。
- 输入包含己方石、对方石、投壶数等，总计 29 维抽象信息。

输出表示：

- KR-UCT 离散采样后的动作概率分布，维度为 `32 x 10 x 3`。
- 这里的 3 表示左旋、右旋、无旋。

网络：

- 7 层卷积。
- 不使用 pooling，以保留位置精度。

## 奖励机制细读

论文提出两类奖励：

1. SER，situation evaluation reward。

   每一轮根据 house 内石头分布做局面评价，并引入随轮次变化的权重。优点是 reward dense，收敛快。缺点是每壶局面并非独立，早期看似好的局面可能给后续留下风险。

2. FR，future reward。

   只有比赛结束或未来结果明确后回传收益。优点是更贴近整体目标，缺点是 reward sparse，收敛慢。

实验显示：

- SER 收敛更快，约 50 万轮后对 AI-simple 胜率稳定。
- FR 收敛慢，需要约 150 万轮，但最终胜率更高。

这和冰壶直觉一致：局部贪心能快速学会“看起来占优”，但长期策略需要延迟回报。

## 实验细读

论文比较了：

- DQN
- PPO
- 该方法

对手是国际数字冰壶比赛中的 AI-simple。论文报告：

- 该方法在相同训练迭代下胜率高于 DQN/PPO。
- SER 版最终胜率约 69.2%。
- FR 版最终胜率约 79.1%。
- 还与 KR-DL-UCT、KR-UCT 做了胜率对比，表中显示其对 KR-DL-UCT 和 KR-UCT 有较高胜率。
- 使用 exploitability 指标观察策略是否接近 Nash equilibrium，训练到 1000 万轮时 exploitability 降低。

需要谨慎的是，论文对一些实验细节描述不够充分，且胜率对比是否完全同等预算并不清楚。因此它更适合作为方向参考，不宜作为唯一证据。

## 对我们项目的可迁移点

1. 先手/后手要分开统计。

   冰壶后手优势明显。我们的 evaluation 不能只报总胜率，必须分 first/second 或 hammer/non-hammer。

2. 奖励要兼顾局部和长期。

   当前本地环境按 end 计分适合快速迭代，但如果比赛是多 end，总分差和剩余 end 必须进入状态和价值目标。

3. DQN/PPO 裸跑不是最优路线。

   论文也显示普通 DQN/PPO 在大连续动作空间中低效。我们之前的直觉一致：不应继续盲目 socket-DQN。

4. exploitability 可以转化为对手池评估。

   精确 Nash exploitability 对我们难算，但可以固定强对手池，记录模型是否容易被某类对手克制。

## 与 KR-DL-UCT 的关系

这篇更强调 NFSP 和平均策略，KR-DL-UCT 更强调连续搜索和策略价值网络。对我们的优先级：

1. 先做 KR-DL-UCT 式搜索蒸馏和连续动作优化。
2. 再加入 NFSP 式 opponent pool 和历史平均策略。
3. 最后再考虑 exploitability 近似指标。

## 一句话结论

这篇论文提醒我们：数字冰壶训练不能只看打败一个固定弱 AI 的胜率。我们要记录先后手、使用对手池、混合历史模型，并把局部 reward 与整局胜率目标分清楚。

