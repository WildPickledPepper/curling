# 03 精读：NFSP: Deep Reinforcement Learning from Self-Play in Imperfect-Information Games

## 论文定位

NFSP 研究的是不完美信息博弈中的自我博弈学习。数字冰壶本身是完美信息游戏，双方石头都可见，但这篇仍然有价值，因为它解决了一个更普遍的问题：在多智能体自我博弈中，单纯学习 best response 容易振荡，如何学习更稳定的平均策略并接近 Nash equilibrium。

对我们项目来说，NFSP 的直接启发是 opponent pool 和 average strategy。我们不应该只训练“打败当前对手”的策略，否则模型很可能只会克制 random/scripted，而不是形成稳健战术。

## 背景细读

虚拟博弈 Fictitious Play 的思想是：每个玩家对对手历史平均策略做最佳响应。对于某些博弈类别，平均策略可以收敛到 Nash equilibrium。

NFSP 把这个思想神经网络化。每个 agent 有两个网络：

- `Q(s, a | theta_Q)`：强化学习网络，学习对其他玩家平均策略的 best response。
- `Pi(s, a | theta_Pi)`：监督学习网络，模仿自己历史 best response 行为，形成 average policy。

它还维护两个记忆池：

- `M_RL`：强化学习 replay memory，通常是循环缓冲，保存近期 transition。
- `M_SL`：监督学习 reservoir memory，保存历史 best response 的 `(s, a)`，用 reservoir sampling 避免只记近期策略。

行为策略是混合策略：

```text
sigma = eta * best_response + (1 - eta) * average_policy
```

其中 `eta` 是 anticipatory parameter。它让 agent 偶尔执行 best response，从而产生监督数据，同时大部分时间按平均策略行动，使训练分布更平滑。

## 方法细读

NFSP 的训练循环：

1. 每局开始，以概率 `eta` 选 best response 策略，否则选 average policy。
2. 与其他 NFSP agent 对局。
3. 所有 transition 存入 `M_RL`。
4. 如果当前执行的是 best response，则把 `(s, a)` 存入 `M_SL`。
5. 用 `M_RL` 训练 Q 网络。
6. 用 `M_SL` 训练 average policy 网络。

论文强调两个稳定性技巧：

1. Reservoir sampling。

   如果监督记忆只保存最近窗口，average policy 会变成“近期策略”，不再是真正历史平均，容易震荡。

2. Anticipatory dynamics。

   如果 agent 永远只执行 average policy，就没有 best response 行为数据可训练平均策略。如果永远执行 best response，又会像普通 DQN 一样在多智能体环境中振荡。混合策略在两者之间折中。

## 实验细读

论文主要在 Leduc Hold'em 和 Limit Texas Hold'em 上评估。

Leduc Hold'em 中：

- NFSP 的 exploitability 随训练下降，逐步接近 Nash equilibrium。
- 网络规模越大，最终 exploitability 越低。
- 去掉 reservoir sampling 或使用滑动窗口监督记忆，会明显损害稳定性甚至发散。
- anticipatory parameter 太大也会导致性能停滞。

与 DQN 对比：

- DQN 的贪心策略高度可 exploitable。
- 即使额外训练一个网络去观察 DQN 的平均行为，也不能像 NFSP 那样稳定接近均衡。
- 关键原因是 DQN 自我博弈产生的状态分布变化剧烈且集中，NFSP 的平均策略让数据分布更平滑。

Limit Texas Hold'em 中：

- NFSP 不依赖人工抽象，直接从原始输入学习。
- 最终策略接近当时强扑克程序的水平，但不是完全超过。

## 对数字冰壶的可迁移点

1. 我们需要 opponent pool。

   当前如果只对 random 或 scripted 评估，模型会过拟合这些弱对手。训练池至少应包含：

   - random tactic
   - scripted tactic
   - 当前模型
   - 历史模型快照
   - 搜索 oracle

2. 保存历史策略，而不是只保留最新版。

   NFSP 的 reservoir memory 对应到我们这里，可以是历史模型快照池和历史搜索样本池。训练时随机抽对手或抽旧样本，减少策略振荡。

3. 平均策略比单一 best response 更稳。

   冰壶中某些局面如果只追求克制当前对手，可能学出冒险打法。比赛环境未知时，应优先选择 robust policy。

4. exploitability 思路可以改造成“被对手池剥削程度”。

   我们无法精确计算冰壶 Nash exploitability，但可以用强对手池分别评估模型被不同风格击败的概率，作为近似指标。

## 不能直接照搬的地方

NFSP 原文用于不完美信息扑克，动作空间较小且离散。数字冰壶是连续动作物理游戏，核心难点不是 hidden information，而是：

- 连续动作搜索。
- 模拟器误差。
- 执行噪声。
- 多壶长程策略。

因此 NFSP 不应替代 KR-UCT/连续搜索，而应作为训练组织方式：对手池、平均策略、历史样本稳定化。

## 对当前项目的决策

短期可以实现：

- 训练时随机从 `model/` 中加载历史快照作为对手。
- 每次产生新模型后保留快照，不覆盖唯一文件。
- evaluation 增加对旧模型和搜索 oracle 的对战项。

中期可以实现：

- 建立 `replay_buffer/search_distill/`，保存多个版本搜索样本。
- 训练时混合近期样本和 reservoir 样本。
- 加入 strategy diversity 统计，观察 tactic 分布是否塌缩。

## 一句话结论

NFSP 告诉我们：自我博弈不是只训练最强 best response，而是要管理“当前最佳响应”和“历史平均策略”的关系。对冰壶项目，最现实的落地是历史模型池和混合对手训练。

