# 当前模型策略模式分析

## 结论摘要

- 当前策略不是单一打法，而是“进营/占位 + 旋进 + 保护/清障”的混合策略。
- 先手和后手差异明显：先手更需要前中盘建立局面、后期防守保护；后手拥有最后一壶，末端更像 hammer-shot 优化问题。
- 当前本地策略偏向在 house 内累计优势，`draw/occupy` 与 `curl_draw` 占比很高；takeout 类动作只在落后或局面拥挤时出现。
- 擦冰主要绑定 draw/curl/freeze 类动作，guard/takeout 大多不擦，符合当前搜索假设。

## 总体表现

| 视角 | Games | Avg score | Win rate | Loss rate | Top groups |
| --- | ---: | ---: | ---: | ---: | --- |
| 先手 | 30 | 2.433 | 83.3% | 16.7% | draw 35.4%, guard 32.1%, curl_draw 30.4%, freeze 1.2%, raise_push 0.8% |
| 后手 | 30 | 3.133 | 93.3% | 6.7% | draw 41.7%, curl_draw 29.6%, guard 18.8%, freeze 4.6%, takeout 4.2%, raise_push 1.2% |

## 分阶段战术模式

### 先手

| 阶段 | 战术组占比 | 擦冰率 | 平均搜索估值 | 预算模式 |
| --- | --- | ---: | ---: | --- |
| early | draw 60.0%, guard 21.7%, curl_draw 18.3% | 40.0% | 2.225 | {'normal': 60} |
| middle | guard 34.4%, curl_draw 34.4%, draw 28.9%, freeze 1.1%, raise_push 1.1% | 48.9% | 3.022 | {'normal': 90} |
| late_setup | guard 41.7%, curl_draw 30.0%, draw 23.3%, freeze 3.3%, raise_push 1.7% | 43.3% | 3.653 | {'normal': 30, 'late': 30} |
| final_without_hammer | curl_draw 43.3%, draw 30.0%, guard 26.7% | 50.0% | 3.944 | {'late': 30} |

### 后手

| 阶段 | 战术组占比 | 擦冰率 | 平均搜索估值 | 预算模式 |
| --- | --- | ---: | ---: | --- |
| early | draw 46.7%, curl_draw 23.3%, takeout 11.7%, guard 8.3%, freeze 8.3%, raise_push 1.7% | 35.0% | 2.575 | {'normal': 60} |
| middle | draw 35.6%, curl_draw 28.9%, guard 25.6%, freeze 5.6%, takeout 3.3%, raise_push 1.1% | 54.4% | 2.778 | {'normal': 90} |
| late_setup | draw 41.7%, curl_draw 31.7%, guard 23.3%, raise_push 1.7%, freeze 1.7% | 48.3% | 3.233 | {'normal': 30, 'late': 30} |
| hammer | draw 50.0%, curl_draw 40.0%, guard 10.0% | 50.0% | 3.492 | {'hammer': 30} |

## 按局势切换

下面是按当前 house 内即时分数粗分的战术组倾向。注意这不是整局真实胜率，只是当前局面快照。

### 先手

| 当前局势 | 战术组占比 |
| --- | --- |
| tied | draw 80.0%, curl_draw 20.0% |
| leading_1 | curl_draw 39.0%, guard 36.4%, draw 19.5%, freeze 2.6%, raise_push 2.6% |
| leading_2plus | guard 57.6%, curl_draw 24.7%, draw 17.6% |
| trailing_2plus | draw 72.7%, curl_draw 27.3% |
| trailing_1 | draw 62.2%, curl_draw 35.1%, freeze 2.7% |

### 后手

| 当前局势 | 战术组占比 |
| --- | --- |
| trailing_1 | curl_draw 44.4%, draw 34.7%, takeout 11.1%, freeze 5.6%, raise_push 2.8%, guard 1.4% |
| trailing_2plus | draw 61.3%, curl_draw 16.1%, freeze 9.7%, takeout 6.5%, guard 3.2%, raise_push 3.2% |
| leading_1 | draw 44.6%, guard 32.4%, curl_draw 17.6%, freeze 5.4% |
| leading_2plus | draw 36.5%, curl_draw 33.3%, guard 30.2% |

## 对训练和搜索的含义

1. 后续模型最好显式拆分或条件化先手/后手策略。虽然 state 已包含 `player_is_init`，但从统计看两种模式差异足够大，值得考虑 separate head 或 side-specific calibration。
2. 最后一壶需要独立目标。后手 hammer 不应只最大化当前 end 期望分，长期应接入 winning percentage table；领先保守、落后搏高方差。
3. 训练标签应记录 `phase`、`score_bucket`、`budget` 和 `group`。这能避免模型只学一个平均策略，把先手布局和后手收官混在一起。
4. 搜索可以按模式调参：early 保留更多 draw/guard 候选，late/hammer 增加 takeout/raise_push 和连续探索预算。
5. 当前统计仍基于本地 mock physics。官方服务器恢复后，应重新跑同一脚本生成 official-calibrated strategy report。
