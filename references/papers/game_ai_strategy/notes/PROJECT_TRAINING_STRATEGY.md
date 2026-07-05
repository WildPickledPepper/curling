# 对本项目的训练策略建议

## 总结判断

我们现在不该继续盲目 socket-DQN。论文共同指向的是一条更稳的路线：

1. 先有可信 forward model 或至少可校准代理。
2. 用搜索在局部状态产生强监督目标。
3. 用神经网络蒸馏搜索，获得快速在线策略。
4. 用对手池/平均策略做自我博弈，避免只克制随机对手。
5. 对连续动作和擦冰做局部优化，而不是只选离散战术。

## 当前代码处于哪一层

已有：

- `fast_curling_env.py`：粗略 forward model。
- `train_search_distill.py`：根搜索 + 策略价值蒸馏雏形。
- `search_distill_robot.py`：在线加载模型。
- `curling_sweep.py`：保守擦冰启发式。
- `continuous_shot_search.py`：围绕候选战术做小预算连续动作微调，动作包含 `(v0, h0, w0, sweep_distance)`。

缺口：

- 物理模型过粗，碰撞、擦冰、官方摩擦随机性都不可信。
- 已有本地连续 refinement，但仍依赖粗糙本地物理；官方物理校准前不能视为正式强度证明。
- 对手主要是随机/脚本，缺少 opponent pool。
- value 只是标量，不是得分分布。
- 已有初步 replay trace，仍缺可视化复盘。

## 下一阶段训练路线

### 阶段 1：校准和诊断

- 增加 replay 保存：每壶状态、候选动作、搜索均值/方差、最终落点、得分。
- 做 shot calibration 表：固定 `(v, h, w, sweep)` 多次执行，估计落点均值和协方差。
- 官方服务器恢复后，优先采集校准数据，不急着比赛训练。

### 阶段 2：连续动作搜索

在 tactic library 产生初始 shot 后，做局部搜索：

- 扰动 `v0`、`h0`、`w0`、`sweep_distance`。
- 每个候选多次模拟，估计期望得分和方差。
- 选 robust shot，不选无噪声最优 shot。
- 最后一壶采用 hammer-shot 专用优化，预算更高。

可先做轻量版 KR-UCT：不用完整树，只在根节点使用 kernel regression 共享相邻动作信息。

当前进展：已实现轻量根搜索版本，见 `continuous_shot_search.py`。它还不是完整 KR-UCT，但已经能在本地评估中把模型平均分从约 `+1.27` 提到约 `+2.04`。

### 阶段 3：蒸馏升级

训练样本从 `(state, tactic)` 升级到：

- `state`
- `candidate mask`
- `search policy distribution`
- `score distribution [-8, 8]`
- `continuous delta` 或最终 `(v, h, w, sweep)`

模型结构先保持 CPU 友好的 MLP，不急着 CNN。等物理可信后再考虑 32x32 空间图网络。

### 阶段 4：对手池与平均策略

训练对手池包含：

- random valid tactic
- scripted tactic
- 当前模型
- 历史模型快照
- 小预算搜索 oracle

每轮训练随机抽对手。保留历史策略池近似 NFSP 的 average strategy，避免模型只学会打当前版本自己。

## 对擦冰的策略

现在的 `curling_sweep.py` 是保守启发式，只解决“协议能用”。论文启发是：擦冰不应长期当后处理，而应进入动作搜索。

建议：

- 短期：默认只对 draw/curl/freeze 类动作启发式擦冰，guard/occupy/takeout 不擦。
- 中期：把 sweep 作为连续第 4 维加入根搜索。（已完成本地版。）
- 长期：用官方校准数据学习 `sweep_distance -> extra travel` 的真实映射。

## 验收指标

以后每次训练都至少报告：

- 对 random/scripted/current-old/search-oracle 的胜率和平均分。
- 先手/后手分开胜率。
- 最后一壶决策质量。
- tactic 分布，防止策略塌缩。
- sweep 使用率和使用后得分变化。
- 至少 10 局胜负 replay 可人工复盘。

这样训练才有科学闭环，不再是“跑了很久但不知道强在哪”。
