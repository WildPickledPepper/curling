# 论文到训练决策映射

## 总体路线

当前最稳的路线不是继续裸 DQN/PPO，而是：

1. 用 tactic library / 当前模型产生初始候选。
2. 用连续动作搜索在候选附近 refinement。
3. 搜索时显式考虑执行噪声和擦冰。
4. 把搜索结果蒸馏回模型。
5. 用历史模型池和多类型对手避免过拟合固定对手。
6. 官方服务器恢复后优先做物理校准。

## 决策依据表

| 训练/工程决策 | 主要依据 | 对当前代码的含义 |
|---|---|---|
| 保留搜索蒸馏，不盲目裸 RL | AlphaGo Zero、AlphaZero、KR-DL-UCT | `train_search_distill.py` 是正确主线 |
| tactic 只做初始候选，最终允许连续偏移 | KR-UCT、KR-DL-UCT、Hammer Shot | `continuous_shot_search.py` 应继续加强 |
| 搜索目标用分布/期望加风险，而不是单点无噪声最优 | KR-UCT、Hammer Shot | 每个候选多 rollout，记录均值/方差 |
| value 从标量升级到得分分布 `[-8, 8]` | AlphaGo Zero、KR-DL-UCT | 下一代模型加 value distribution head |
| 最后一壶单独提高搜索预算 | Hammer Shot、KR-UCT hammer analysis | end 最后一壶可用更高 candidates/rollouts |
| 不把擦冰当后处理，纳入动作 | KR-UCT sweeping 讨论、Hammer Shot 局限、比赛协议 | 4D action `(v0,h0,w0,sweep)` 是必要方向 |
| 建立 opponent pool / 历史模型池 | NFSP、Digital Curling NFSP | 训练时随机打 random/scripted/old model/search oracle |
| 先后手分开评估 | Digital Curling NFSP、Hammer Shot | evaluation 报 first/second 或 hammer/non-hammer |
| 官方服务器恢复后先校准，不先大训 | KR-UCT、KR-DL-UCT、MCTS Survey | 采集固定 shot 的落点均值/协方差 |
| 暂不做复杂状态抽象 | Elastic MCTS、当前项目风险 | 状态抽象优先级低于物理和连续搜索 |

## 近期优先级

1. 做一次更大样本的 refined evaluation，确认本地 `+2.0` 左右平均分是否稳定。
2. 给 evaluation trace 增加候选动作、搜索均值/方差、sweep 距离、最终得分。
3. 把最后一壶识别出来，单独提高 local search budget。
4. 设计下一代训练标签：`state -> tactic distribution + continuous delta + score distribution`。
5. 准备官方服务器 calibration 脚本：固定 `(v,h,w,sweep)` 多次发球并记录落点。

## 当前判断

现在最该强化的是“可信搜索老师”，不是急着堆更复杂网络。只要本地物理还粗，模型越大越容易学到代理服务器的偏差；等官方校准数据回来，再把网络容量和自我博弈规模提上去。

