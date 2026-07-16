# 当前模型策略模式分析

## 结论摘要

- 当前策略不是单一打法，而是“进营/占位 + 旋进 + 保护/清障”的混合策略。
- 先手和后手差异明显：先手是无 hammer 的约束局，目标更偏“控中线、逼对手只拿 1 分或偷分”；后手拥有最后一壶，目标更偏“保持通道、制造 2 分以上机会、最后一壶单独优化”。
- 当前本地策略偏向在 house 内累计优势，`draw/occupy` 与 `curl_draw` 占比很高；takeout 类动作主要在后手早盘、落后或局面拥挤时出现。
- 擦冰主要绑定 draw/curl/freeze 类动作，guard/takeout 大多不擦，符合当前搜索假设；后手 hammer 阶段擦冰率最高，说明最后一壶对距离控制更敏感。
- 但它还没有完整学出现实冰壶里“有 hammer 更常打边路/角卫、无 hammer 控中线”的空间布局模式。这里应视为本地代理物理和战术库限制下的模式，不是最终比赛策略。

## 调研依据

- 真实冰壶基础策略：有 hammer 时通常更积极，目标是 2 分或更多，常把壶分散到边路并保持四尺区通道；无 hammer 时更保守，常把局面导向中线，控制四尺区入口，目标是偷分或逼对方只拿 1 分。
- 比分会改变策略：落后时需要更多 guard、come-around、raise 等高方差进攻；领先时应减少给对手藏壶和打大分的机会。
- 数字冰壶论文路线：KR-DL-UCT 强调“神经网络给候选 + 连续动作搜索”；NFSP 数字冰壶论文强调先手/后手策略差异，需要分开统计或建模；hammer-shot 论文强调最后一壶不能只最大化期望分，而应按剩余局数和分差最大化 winning percentage。
- 对我们项目的翻译：当前最合理的策略层不是一个平均策略，而是按 `side x phase x score_bucket` 切换的模式控制器，再由连续搜索在 `(v0, h0, w0, sweep)` 上微调。

## 总体表现

| 视角 | Games | Avg score | Win rate | Loss rate | Top groups |
| --- | ---: | ---: | ---: | ---: | --- |
| 先手 | 80 | 2.325 | 86.2% | 13.8% | draw 37.0%, guard 31.7%, curl_draw 29.7%, freeze 0.8%, raise_push 0.5%, takeout 0.3% |
| 后手 | 80 | 3.150 | 93.8% | 6.2% | draw 45.2%, curl_draw 24.4%, guard 17.7%, takeout 5.8%, freeze 4.8%, raise_push 2.2% |

## 分阶段战术模式

### 先手

| 阶段 | 战术组占比 | 擦冰率 | 平均搜索估值 | 预算模式 |
| --- | --- | ---: | ---: | --- |
| early | draw 61.9%, guard 21.2%, curl_draw 15.6%, raise_push 0.6%, takeout 0.6% | 35.0% | 2.228 | {'normal': 160} |
| middle | guard 37.5%, curl_draw 31.7%, draw 28.7%, freeze 1.2%, raise_push 0.4%, takeout 0.4% | 45.4% | 2.958 | {'normal': 240} |
| late_setup | guard 38.1%, curl_draw 33.8%, draw 26.2%, freeze 1.2%, raise_push 0.6% | 42.5% | 3.676 | {'normal': 80, 'late': 80} |
| final_without_hammer | curl_draw 43.8%, draw 33.8%, guard 22.5% | 48.8% | 3.908 | {'late': 80} |

### 后手

| 阶段 | 战术组占比 | 擦冰率 | 平均搜索估值 | 预算模式 |
| --- | --- | ---: | ---: | --- |
| early | draw 48.1%, curl_draw 17.5%, takeout 16.9%, guard 8.8%, freeze 6.9%, raise_push 1.9% | 30.0% | 2.569 | {'normal': 160} |
| middle | draw 37.1%, guard 24.2%, curl_draw 24.2%, freeze 7.1%, takeout 3.8%, raise_push 3.8% | 51.7% | 2.844 | {'normal': 240} |
| late_setup | draw 50.0%, curl_draw 28.1%, guard 18.8%, freeze 1.9%, raise_push 0.6%, takeout 0.6% | 50.0% | 3.184 | {'normal': 80, 'late': 80} |
| hammer | draw 53.8%, curl_draw 31.2%, guard 13.8%, raise_push 1.2% | 58.8% | 3.525 | {'hammer': 80} |

## 目前可归纳的策略模式

| 模式 | 触发条件 | 当前统计特征 | 战术含义 | 后续改进 |
| --- | --- | --- | --- | --- |
| 无 hammer 开局控场 | 先手 early | draw 61.9%, guard 21.2%, curl_draw 15.6% | 模型倾向先占 house/中路，再保留 guard 或旋进余地 | 增加显式 center guard / top-four 控制特征，避免只会早早进营 |
| 无 hammer 领先防守 | 先手 leading_1/2plus | guard 分别 42.4%/52.8% | 当前把“领先”理解为封路和保护 | 真实冰壶领先常需要更 clean 的局面，后续要加入风险惩罚和对手双飞机会评估 |
| 无 hammer 落后抢分 | 先手 trailing | draw+curl 超过 95%，少量 takeout | 通过进营和旋进制造得分点 | 应提高 raise_push/freeze 候选占比，落后时需要更高方差打法 |
| 有 hammer 开局清通道 | 后手 early | takeout 16.9%，guard 8.8% | 后手比先手明显更愿意清除威胁，少打 guard | 增加边路/角卫布局，否则多分能力可能不足 |
| 有 hammer 中后盘建优势 | 后手 middle/late_setup | draw 37.1%/50.0%，curl_draw 24.2%/28.1% | 逐步把最终一壶可得分局面做厚 | 训练标签中显式记录“当前最佳壶数量”和“可清障通道” |
| Hammer 收官 | 后手 hammer | draw+curl 85.0%，擦冰 58.8% | 最后一壶主要变成距离和线路控制问题 | 单独接入 winning percentage 目标和更高预算连续优化 |

## 按局势切换

下面是按当前 house 内即时分数粗分的战术组倾向。注意这不是整局真实胜率，只是当前局面快照。

### 先手

| 当前局势 | 战术组占比 |
| --- | --- |
| tied | draw 76.2%, curl_draw 23.8% |
| leading_1 | guard 42.4%, curl_draw 36.4%, draw 19.1%, freeze 1.3%, raise_push 0.8% |
| leading_2plus | guard 52.8%, draw 26.7%, curl_draw 20.5% |
| trailing_2plus | draw 60.9%, curl_draw 34.8%, takeout 4.3% |
| trailing_1 | draw 61.3%, curl_draw 34.9%, freeze 1.9%, raise_push 0.9%, takeout 0.9% |

### 后手

| 当前局势 | 战术组占比 |
| --- | --- |
| trailing_1 | draw 45.9%, curl_draw 28.5%, takeout 13.0%, freeze 8.2%, raise_push 2.9%, guard 1.4% |
| trailing_2plus | draw 60.2%, curl_draw 16.3%, takeout 10.2%, raise_push 6.1%, freeze 4.1%, guard 3.1% |
| leading_1 | draw 42.2%, guard 31.4%, curl_draw 21.1%, freeze 4.9%, raise_push 0.5% |
| leading_2plus | draw 38.0%, guard 32.7%, curl_draw 28.0%, raise_push 0.7%, freeze 0.7% |

## 对训练和搜索的含义

1. 后续模型最好显式拆分或条件化先手/后手策略。虽然 state 已包含 `player_is_init`，但从统计看两种模式差异足够大，值得考虑 separate head 或 side-specific calibration。
2. 最后一壶需要独立目标。后手 hammer 不应只最大化当前 end 期望分，长期应接入 winning percentage table；领先保守、落后搏高方差。
3. 训练标签应记录 `phase`、`score_bucket`、`budget`、`group`、`sweep` 和最终搜索估值分布。这样能避免模型只学一个平均策略，把先手布局和后手收官混在一起。
4. 搜索可以按模式调参：无 hammer early 保留更多 center guard / freeze / draw 候选；有 hammer early 增加边路和清通道候选；late/hammer 增加 takeout/raise_push 和连续探索预算。
5. 当前策略最大的可疑点是“领先时 guard 偏多、后手边路模式不足”。这可能来自本地 mock physics、战术库候选覆盖或单 end 期望分目标，官方服务器恢复后必须重新校准。
6. 当前统计仍基于本地 mock physics。官方服务器恢复后，应重新跑同一脚本生成 official-calibrated strategy report。

## 下一步具体做法

1. 保持当前 `search_distill + continuous refinement` 主线，但训练数据增加模式字段：`side`、`phase`、`score_bucket`、`group`、`sweep_rate`、`search_mean/std`。
2. 做一个轻量策略门控器：先根据 `side/phase/score_bucket` 调整候选战术先验，再交给模型和连续搜索；这比直接大训一个平均模型更稳。
3. 给后手 hammer 单独做搜索目标：短期用“期望分 + 方差/搏命系数”，长期用 WP table。
4. 补空间特征：中心线是否被堵、四尺区通道是否开放、边路是否有可利用 guard、对手是否有双飞机会。
5. 继续保留先手/后手分开评估，不再只看总胜率。

## 参考资料

- Local notes: `references/papers/game_ai_strategy/notes/deep_reading/05_kr_uct_curling_deep.md`
- Local notes: `references/papers/game_ai_strategy/notes/deep_reading/06_deep_rl_simulated_curling_deep.md`
- Local notes: `references/papers/game_ai_strategy/notes/deep_reading/07_digital_curling_nfsp_deep.md`
- Local notes: `references/papers/game_ai_strategy/notes/deep_reading/08_hammer_shots_curling_deep.md`
- Granite Curling Club strategy: https://curlingseattle.org/strategy
- USA Curling basic strategy handout mirror: https://southshorecurling.com/wp-content/uploads/2013/03/USA_Curling-basic_curling_strategy.pdf
- Hammer-shot paper: https://www.ijcai.org/Proceedings/16/Papers/086.pdf
- KR-DL-UCT paper page: https://proceedings.mlr.press/v80/lee18b.html
