# 09 Survey of Monte Carlo Tree Search Methods

## 这篇解决什么问题

这是 MCTS 方法综述，价值在于给搜索算法变体做地图。它把 MCTS 分成选择、扩展、模拟、回传四阶段，并系统整理 UCT、RAVE、progressive widening、rollout policy、剪枝、并行化、非确定环境等增强。

## 方法拆解

标准 MCTS：

- Selection：从根节点沿树策略选择子节点，常用 UCB/UCT 平衡探索和利用。
- Expansion：遇到未完全展开节点时新增子节点。
- Simulation：从新节点 rollout 到终局或固定深度。
- Backpropagation：把结果沿路径回传更新访问次数和价值。

对我们最相关的变体：

- Progressive widening：动作空间太大或连续时，不一次性展开全部动作，而是随访问次数逐步增加候选动作。
- Domain rollout policy：随机 rollout 在复杂博弈中方差大，应使用脚本/启发式 rollout。
- Non-deterministic MCTS：随机转移下要对同一动作多次采样，不能把一次结果当确定。
- Parallel/root parallel：可用多进程或多线程跑独立搜索，最后合并根统计。

## 对我们数字冰壶的启发

我们需要的不是“完整大 MCTS”，而是定制小预算搜索：

- 根节点使用 tactic library 给候选动作，保证起点不是纯随机。
- 对每个候选动作做 progressive widening，连续扰动 `(v, h, w, sweep)`。
- rollout policy 用脚本/当前模型，而不是随机。
- 回传目标用得分分布或期望分。
- 搜索日志必须保存访问次数、均值、方差和最终选择，方便诊断模型为什么出某一壶。

## 局限

综述本身不解决冰壶连续物理问题。真正关键还得靠 KR-UCT、Delaunay Sampling 和模拟器校准。

