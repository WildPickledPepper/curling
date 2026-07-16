# 从文献到训练系统：逐项实施规范

> 目的：把论文中的可验证事实、我们采用的设计、暂不采用的部分严格分开。本文是 P0 重新开始采集前的约束，不是泛泛的综述。

## 先给结论

我们不应把“先手/后手”当成一个普通标记后随便混在数据里。训练样本必须同时包含：

1. **当前出手方**：这手是谁出；
2. **本 end 的 hammer 身份**：谁拥有最后一壶；
3. **当前谁在得分**：场上暂时是谁得分、多少分；
4. **第几手与剩余手数**：同一盘面在第 1 手与第 16 手的正确选择可完全相反；
5. **整场状态**：还剩几局、从当前出手方视角的总分差。

前三项解决“同一局面、先后手策略为什么不同”，后两项解决“领先保守、落后搏分为什么不同”。P0 只先训练单 end，但也必须把完整字段写入数据；未启用的整场字段明确写成默认值，不能缺失。

## 原文逐项核对

| 论文 | 原文做法 | 对本项目的硬约束 | 我们的取舍 |
| --- | --- | --- | --- |
| KR-UCT（IJCAI 2016） | 手写 shot generator 产生约 7–30 个起点；用执行误差作 kernel，让临近连续动作共享价值；一局搜索最多向前模拟 5 手；1600 samples；以 lower confidence bound 评估局面。 | 战术库只能当起点；不能把每个微调动作彼此孤立评估；随机扰动必须进入选球。 | P0 用根节点连续搜索，但必须升级为 kernel 共享 + 置信下界；当前“均值减 0.25×标准差”只是临时 smoke 规则，不能作为正式老师。 |
| KR-DL-UCT（PMLR 2018） | 状态含壶位置、**当前谁在得分**、出壶数、得分区占用；策略输出离散落点/旋转分布，价值输出 `[-8,8]` 的 17 类得分分布；自对弈标签是搜索策略 `π` 与得分分布 `z`；多 end 用剩余局数和分差查 WP。 | 训练标签不能只有“最终选中的一个动作”和标量均值；必须保存候选分布与完整 score histogram。 | 先用小模型和有限候选，不照搬 32×32 ResNet；但数据 schema 直接按 `state, π, continuous action, z` 设计。 |
| Digital Curling NFSP（2021） | 明确称 sente/gote 策略“完全不同”，为两角色分别使用 RL 与平均策略网络；状态为己方/对方壶、投壶数等；评测每组交换 sente/gote；短期局面奖励收敛快，终局回报最终更强。 | 不能只报一个混合胜率；先手和后手必须分别训练统计、分别验收。 | 不直接复制其四张网络：严格物理采样昂贵，先用共享表示 + 明确角色条件；同时保留两个角色的独立数据桶、独立指标。若共享模型出现角色串扰，再拆为双 policy head。 |
| NFSP（arXiv 2016） | 每个玩家有 best-response Q 网络和 average-policy 网络；RL transition buffer 与 SL reservoir 分开；只有 best-response 行为进入平均策略监督集；用 anticipatory mixture 稳定同时学习。 | “当前最强策略”不等于可部署平均策略；自对弈数据也不能只留最近几局。 | 早期不做 NFSP 双网络；保留对手池与历史样本 reservoir 思想，后续在自对弈阶段接入。 |
| Hammer Shot（IJCAI 2016） | 最后一壶用连续随机优化；目标是整场 WP 而非本局期望分。论文举例：最后一局落后 2 分时，稳定拿 1 分仍输，高方差拿 3 分反而合理。 | hammer 不能总用“均值最高”规则；目标函数必须看总分差和剩余 end。 | 单 end P0 先学 score distribution；P3 才把它接入 WP table。hammer 样本从 P0 起单独标记、加大搜索预算。 |
| AlphaZero（2017） | 搜索产生行动分布 `π`，终局产生结果 `z`，网络拟合两者；搜索不是只给一个 argmax 动作。 | 搜索蒸馏时，候选概率/访问量本身是训练信号。 | P0 记录根候选的归一化搜索权重；在完整 KR 搜索上线前，这个字段标为 provisional，不能伪称 MCTS visit policy。 |

### 关键原文位置

- KR-UCT：`references/papers/game_ai_strategy/extracted_text/05_kr_uct_continuous_action_curling_ijcai2016.txt`，方法与实验部分。执行模型采用重尾 Student-t；候选生成器、1600 samples、五手 rollout、LCB 均在实验设定中出现。
- KR-DL-UCT：`.../06_deep_rl_continuous_action_simulated_curling_pmlr2018.txt`，state representation、network training、self-play 与 multiple end 部分。
- Digital Curling NFSP：`.../07_digital_curling_nfsp_springer_open_2021.txt`，Methods 约第 1859–1862 页：分别训练 sente/gote，`32×32×3` 动作输出，SER/FR 对照以及每组 500 先手 + 500 后手的评测。
- 原始 NFSP：`.../03_nfsp_self_play_arxiv_1603.01121.txt`，第 3 节与 Algorithm 1：`MRL` circular buffer、`MSL` reservoir、best-response 行为才写入 `MSL`、anticipatory parameter `η`。
- Hammer Shot：`.../08_hammer_shots_curling_ijcai2016.txt`，目标函数与 WP table 部分。
- AlphaZero：`.../01_alphazero_self_play_arxiv_1712.01815.txt`，自对弈生成 `(s, π, z)` 的方法段。

## 我们的状态定义

所有状态一律转到“**当前出手方视角**”：当前出手方自己的壶为 `self`，对手壶为 `opponent`。这样相同空间关系可以共用样本；但绝不丢失角色字段。

```json
{
  "board": {
    "self": [{"id": 0, "x": 0.0, "y": 0.0, "yaw": 0.0, "inPlay": false}],
    "opponent": [{"id": 1, "x": 0.0, "y": 0.0, "yaw": 0.0, "inPlay": false}]
  },
  "turn": {
    "shotIndex": 0,
    "remainingShotsInEnd": 16,
    "isHammerSide": false,
    "isLastShotOfEnd": false,
    "houseLeader": "none",
    "houseScoreForSelf": 0
  },
  "match": {
    "endIndex": 0,
    "endsRemainingAfterThis": 0,
    "scoreDifferenceForSelf": 0,
    "mode": "single_end_p0"
  }
}
```

说明：

- `isHammerSide` 是“这支队本 end 是否拥有最后一壶”，不是“当前是不是最后一手”。
- `houseLeader`/`houseScoreForSelf` 是当前盘面暂时得分；若没有壶在 house，写 `none/0`。
- `match` 在 P0 固定为单 end，但字段必须存在，以免数据集与后续多 end 不兼容。
- yaw 对严格物理回放要保存；第一版策略网络可暂不把 yaw 输入，但不能从原始数据丢掉。

## 动作与老师标签

对每一条状态，保存而非只保存一个最终球：

```json
{
  "actionSpace": {"sweepEnabled": false, "parameters": ["v0", "h0", "w0"]},
  "rootCandidates": [
    {
      "tactic": "guard_left",
      "action": [3.2, -0.1, 0.0],
      "evaluationCount": 8,
      "scoreHistogram": {"-2": 1, "0": 3, "1": 4},
      "meanEndScoreForSelf": 0.25,
      "stdEndScore": 0.66,
      "lowerConfidenceBound": -0.16,
      "searchWeight": 0.31
    }
  ],
  "selectedAction": [3.2, -0.1, 0.0],
  "selectedCandidateIndex": 0,
  "targetScoreDistribution": {"-8": 0, "...": 0, "1": 4, "...": 0}
}
```

这里的正负分必须是**当前出手方视角**。否则一个共享模型会把“自己 +1 分”和“对手 +1 分”混成同一种标签。

正式 P0 的 `searchWeight` 应来自连续搜索的有效访问量/置信权重后归一化。它不是软最大化均值分；后者会把极窄、偶然成功的球错误地教给网络。

## 搜索老师的分层目标

### P0：单 end 根节点老师

目标不是“做完完整 MCTS”，而是验证一件可量化的事：连续搜索是否在同样预算下稳定优于固定战术库。

1. 由战术库给 7–30 个有意义的起点；
2. 每个实际执行结果以执行扰动 kernel 分摊给邻近意图动作；
3. 用有效样本数与均值构造探索分数，持续向未覆盖但有希望的局部扩展；
4. 当前壶之后继续按固定 rollout policy 交替模拟 `min(5, remainingShotsInEnd)` 手；若尚未到 end，则只允许使用一个事先固定、单独验证过的局面估值器；每个候选用该结果的 score histogram 估计 LCB；
5. 普通手按本 end score distribution 选球；hammer 另加预算与单独分组；
6. P0 仅产生数据，不训练网络。

### P1：搜索蒸馏

- policy：拟合 `searchWeight`，输出“优先从哪些战术/连续区域开始搜”；
- continuous head：拟合 selected action 或相对战术基点的连续修正；
- value：拟合 17 类 `targetScoreDistribution`，不只拟合一个平均分；
- 训练/验证按局面切分，且先手和后手各自保留验证集。

### P2：对手池与平均策略

当前策略不能只和“最新自己”下。对手池至少含 scripted、队友 PPO、历史检查点、小预算搜索。样本保留采用固定比例的近期数据与 reservoir 历史数据。这里借鉴 NFSP 的稳定性设计，不宣称已经实现 NFSP。

### P3：多 end 的 WP

给每个 end 后的得分 `k ∈ [-8,8]`，由 `WP(endsRemaining, scoreDifferenceForSelf + k, hammerNextEnd)` 取值，再按当前预测的 `P(k)` 加权：

```text
expectedWP = Σ_k P(k | state, action) × WP(nextStateAfterScore(k))
```

因此最后一壶不是“多拿期望分”就够；它是在当前比分下最大化 `expectedWP`。

## 角色处理：论文原法与我们的起步方案

数字冰壶 NFSP 的原法是 sente/gote 各自单独网络。那样最彻底，但在严格物理模拟成本下会近似把有效样本分成两半。

我们先采用下面的折中，且做消融验证：

| 方案 | 训练方式 | 优点 | 风险 | 是否先做 |
| --- | --- | --- | --- | --- |
| 共享编码器 + 角色字段 + 一个 policy head | 全部样本共训 | 样本效率最高 | 容易把先后手混淆 | 否，作为最低基线 |
| 共享编码器 + `isHammerSide` 条件 + **两个 policy head** | 两角色头分开更新，底层共享 | 既保留空间共性，也允许战术分化 | 实现稍多 | **是，推荐起步方案** |
| sente/gote 两套完整网络 | 两类数据完全分开 | 最贴近 NFSP 论文 | 样本效率最低 | 角色串扰显著时再做 |

无论用哪种模型，评测必须固定做四项：先手对固定对手、后手对固定对手、先手对历史池、后手对历史池。总胜率只作摘要，不能代替四项结果。

## 当前代码的状态与必须修改处

`p0_search_teacher.py` 当前仅是 smoke 原型，已经验证“复用 PhysX 场景、多条摩擦序列”这一工程路径，但**不能开始正式采集**，原因如下：

1. 没写入完整状态、hammer、当前 house 得分和 match 字段；
2. 只做固定小扰动并独立评估，尚未做 kernel 共享；
3. 目前的 `mean - riskPenalty × std` 不是有统计含义的 LCB；
4. 候选权重不是搜索访问分布；
5. 默认只做单 end，尚未形成先/后手分桶验收。
6. 当前候选只模拟了**这一壶**，随后就读取场上临时比分；它没有模拟对手响应及后续出壶，所以该数不是 end score，不能写作 `targetScoreDistribution`。

下一步不是盲跑，而是先把这六项补齐，并以 20–50 个固定局面做 P0 对照测试：固定战术库 vs 根节点连续搜索。通过后才采集大数据集。

## 评测门槛

P0 合格的最小证据：

1. 相同初始局面、相同总 rollout 预算；
2. 先/后手各至少一半局面，hammer 局面单列；
3. 每一局面用独立随机序列复测，不复用搜索时的随机序列；
4. 报告平均 end 分、score histogram、LCB、胜率/不败率；
5. 连续搜索相对固定战术库的提升要给置信区间；
6. 不能只挑有利局面，局面清单与随机种子在运行前固定。

## 不从论文照搬的东西

- 不把论文的数字冰壶噪声模型直接当作 Unity 的真实随机机制；我们的严格模拟器已对齐非扫冰物理，但 RNG 分布仍应以自己的采样为准。
- 不在 P0 训练显式扫冰；目前交付边界是非扫冰。
- 不上完整深树 MCTS；先用有验收的根节点连续搜索，避免算力耗在未经验证的深度上。
- 不把队友 PPO 或手写战术库当“真值老师”；它们是候选提案器/对手，严格搜索结果才是训练标签来源。
