# NWNHT 公开壶谱复盘：CAN vs SWE

- 比赛：Ford World Men's Curling Championship 2017，2017-04-09 18:00:00，match_id=1076
- 最终比分：CAN 4 – 2 SWE
- 数据：NWNHT/curling 随附 SQLite；壶位为上游自动解析坐标。叫球/评分和壶位是事实记录，最后一列的战术意图是我们的保守归纳。
- 对照原则：[Team Gushue 公开战术树](../../planning_proxy/docs/strategy/05_Team_Gushue公开战术树_证据版.md)。

## 第 1 局

- 后手：CAN；本局得分：CAN 0，SWE 0；累计：CAN 0，SWE 0。
- 壶色归属：red→CAN，yellow→SWE（由连续壶面新增壶与投手队伍反推）。
- 逐手覆盖：16/16 手，完整。

| 手 | 出手方 / 投手 | 官方叫球（评分） | 出手后检测壶数 | 营内暂时得分 | 观察到的离散目标 |
| --- | --- | --- | --- | --- | --- |
| 1 | SWE / SUNDGREN C | Draw（4） | CAN 0, SWE 1 | SWE 暂得 1（最近 0.68 m） | 落营或前场落点 |
| 2 | CAN / WALKER G | Take-out（4） | CAN 1, SWE 0 | CAN 暂得 1（最近 1.72 m） | 清除/处理对方壶 |
| 3 | SWE / SUNDGREN C | Take-out（4） | CAN 0, SWE 1 | 营内无壶 | 清除/处理对方壶 |
| 4 | CAN / WALKER G | Take-out（4） | CAN 1, SWE 0 | CAN 暂得 1（最近 0.88 m） | 清除/处理对方壶 |
| 5 | SWE / WRANAA R | Take-out（4） | CAN 0, SWE 1 | SWE 暂得 1（最近 0.97 m） | 清除/处理对方壶 |
| 6 | CAN / GALLANT B | Take-out（4） | CAN 1, SWE 0 | CAN 暂得 1（最近 1.65 m） | 清除/处理对方壶 |
| 7 | SWE / WRANAA R | Take-out（4） | CAN 0, SWE 1 | SWE 暂得 1（最近 1.64 m） | 清除/处理对方壶 |
| 8 | CAN / GALLANT B | Take-out（2） | CAN 0, SWE 0 | 营内无壶 | 清除/处理对方壶 |
| 9 | SWE / ERIKSSON O | Draw（4） | CAN 0, SWE 1 | SWE 暂得 1（最近 1.36 m） | 落营或前场落点 |
| 10 | CAN / NICHOLS M | Take-out（4） | CAN 1, SWE 0 | CAN 暂得 1（最近 1.53 m） | 清除/处理对方壶 |
| 11 | SWE / ERIKSSON O | Take-out（4） | CAN 0, SWE 1 | SWE 暂得 1（最近 1.82 m） | 清除/处理对方壶 |
| 12 | CAN / NICHOLS M | Take-out（4） | CAN 1, SWE 0 | 营内无壶 | 清除/处理对方壶 |
| 13 | SWE / EDIN N | Take-out（4） | CAN 0, SWE 1 | SWE 暂得 1（最近 0.95 m） | 清除/处理对方壶 |
| 14 | CAN / GUSHUE B | Take-out（4） | CAN 1, SWE 0 | CAN 暂得 1（最近 0.74 m） | 清除/处理对方壶 |
| 15 | SWE / EDIN N | Take-out（4） | CAN 0, SWE 1 | SWE 暂得 1（最近 1.27 m） | 清除/处理对方壶 |
| 16 | CAN / GUSHUE B | Clearing（4） | CAN 0, SWE 0 | 营内无壶 | 清场，降低复杂度 |

第 1 局：本局 blank；后手没有拿分，后手权保留。 叫球结构：清除类 14 手、守壶类 0 手、draw 2 手。 这局明显优先降低壶数；与“后手局面不利时可清场/blank”分支相符。

## 第 2 局

- 后手：CAN；本局得分：CAN 1，SWE 0；累计：CAN 1，SWE 0。
- 壶色归属：red→CAN，yellow→SWE（由连续壶面新增壶与投手队伍反推）。
- 逐手覆盖：16/16 手，完整。

| 手 | 出手方 / 投手 | 官方叫球（评分） | 出手后检测壶数 | 营内暂时得分 | 观察到的离散目标 |
| --- | --- | --- | --- | --- | --- |
| 1 | SWE / SUNDGREN C | Draw（3） | CAN 0, SWE 1 | SWE 暂得 1（最近 0.16 m） | 落营或前场落点 |
| 2 | CAN / WALKER G | Front（4） | CAN 1, SWE 1 | SWE 暂得 1（最近 0.15 m） | 前场占位/守壶 |
| 3 | SWE / SUNDGREN C | Guard（3） | CAN 1, SWE 2 | SWE 暂得 1（最近 0.15 m） | 前场守壶，制造掩护 |
| 4 | CAN / WALKER G | Take-out（0） | CAN 2, SWE 2 | SWE 暂得 1（最近 1.60 m） | 清除/处理对方壶 |
| 5 | SWE / WRANAA R | Draw（3） | CAN 2, SWE 3 | SWE 暂得 2（最近 0.59 m） | 落营或前场落点 |
| 6 | CAN / GALLANT B | Double Take-out（2） | CAN 2, SWE 2 | SWE 暂得 2（最近 0.60 m） | 双飞，压低场上壶数 |
| 7 | SWE / WRANAA R | Guard（1） | CAN 2, SWE 3 | SWE 暂得 3（最近 0.59 m） | 前场守壶，制造掩护 |
| 8 | CAN / GALLANT B | Double Take-out（2） | CAN 3, SWE 2 | CAN 暂得 1（最近 1.18 m） | 双飞，压低场上壶数 |
| 9 | SWE / ERIKSSON O | Take-out（4） | CAN 2, SWE 3 | SWE 暂得 3（最近 1.38 m） | 清除/处理对方壶 |
| 10 | CAN / NICHOLS M | Hit and Roll（3） | CAN 3, SWE 2 | SWE 暂得 1（最近 1.61 m） | 撞击后滚到新位置 |
| 11 | SWE / ERIKSSON O | Draw（4） | CAN 3, SWE 3 | SWE 暂得 2（最近 1.12 m） | 落营或前场落点 |
| 12 | CAN / NICHOLS M | Draw（3） | CAN 4, SWE 2 | CAN 暂得 1（最近 0.89 m） | 落营或前场落点 |
| 13 | SWE / EDIN N | Take-out（4） | CAN 3, SWE 3 | SWE 暂得 2（最近 0.78 m） | 清除/处理对方壶 |
| 14 | CAN / GUSHUE B | Take-out（4） | CAN 4, SWE 2 | CAN 暂得 1（最近 0.98 m） | 清除/处理对方壶 |
| 15 | SWE / EDIN N | Take-out（4） | CAN 3, SWE 3 | SWE 暂得 2（最近 0.69 m） | 清除/处理对方壶 |
| 16 | CAN / GUSHUE B | Take-out（4） | CAN 4, SWE 2 | CAN 暂得 1（最近 0.94 m） | 清除/处理对方壶 |

第 2 局：CAN 有后手并拿到 1 分。 叫球结构：清除类 8 手、守壶类 3 手、draw 4 手。 需要结合逐手壶面判断是哪一次碰撞改变了局势，不能仅从叫球名称下结论。

## 第 3 局

- 后手：SWE；本局得分：CAN 0，SWE 1；累计：CAN 1，SWE 1。
- 壶色归属：red→CAN，yellow→SWE（由连续壶面新增壶与投手队伍反推）。
- 逐手覆盖：16/16 手，完整。

| 手 | 出手方 / 投手 | 官方叫球（评分） | 出手后检测壶数 | 营内暂时得分 | 观察到的离散目标 |
| --- | --- | --- | --- | --- | --- |
| 1 | CAN / WALKER G | Front（4） | CAN 1, SWE 0 | 营内无壶 | 前场占位/守壶 |
| 2 | SWE / SUNDGREN C | Front（4） | CAN 1, SWE 1 | 营内无壶 | 前场占位/守壶 |
| 3 | CAN / WALKER G | Front（4） | CAN 2, SWE 1 | 营内无壶 | 前场占位/守壶 |
| 4 | SWE / SUNDGREN C | Draw（3） | CAN 2, SWE 2 | SWE 暂得 1（最近 1.56 m） | 落营或前场落点 |
| 5 | CAN / GALLANT B | Draw（4） | CAN 3, SWE 2 | CAN 暂得 1（最近 0.45 m） | 落营或前场落点 |
| 6 | SWE / WRANAA R | Double Take-out（2） | CAN 2, SWE 3 | CAN 暂得 1（最近 0.44 m） | 双飞，压低场上壶数 |
| 7 | CAN / GALLANT B | Take-out（4） | CAN 3, SWE 2 | CAN 暂得 2（最近 0.45 m） | 清除/处理对方壶 |
| 8 | SWE / WRANAA R | Hit and Roll（2） | CAN 2, SWE 3 | CAN 暂得 2（最近 0.45 m） | 撞击后滚到新位置 |
| 9 | CAN / NICHOLS M | Guard（4） | CAN 3, SWE 3 | CAN 暂得 2（最近 0.45 m） | 前场守壶，制造掩护 |
| 10 | SWE / ERIKSSON O | Promotion Take-out（2） | CAN 2, SWE 3 | CAN 暂得 1（最近 0.45 m） | 借己方壶完成清除 |
| 11 | CAN / NICHOLS M | Guard（4） | CAN 3, SWE 3 | CAN 暂得 1（最近 0.45 m） | 前场守壶，制造掩护 |
| 12 | SWE / ERIKSSON O | Clearing（4） | CAN 2, SWE 2 | CAN 暂得 2（最近 0.45 m） | 清场，降低复杂度 |
| 13 | CAN / GUSHUE B | Guard（1） | CAN 3, SWE 2 | CAN 暂得 2（最近 0.44 m） | 前场守壶，制造掩护 |
| 14 | SWE / EDIN N | Take-out（4） | CAN 2, SWE 3 | SWE 暂得 1（最近 0.75 m） | 清除/处理对方壶 |
| 15 | CAN / GUSHUE B | Hit and Roll（4） | CAN 3, SWE 2 | CAN 暂得 2（最近 0.87 m） | 撞击后滚到新位置 |
| 16 | SWE / EDIN N | Draw（4） | CAN 3, SWE 3 | SWE 暂得 1（最近 0.09 m） | 落营或前场落点 |

第 3 局：SWE 有后手并拿到 1 分。 叫球结构：清除类 4 手、守壶类 6 手、draw 3 手。 需要结合逐手壶面判断是哪一次碰撞改变了局势，不能仅从叫球名称下结论。

## 第 4 局

- 后手：CAN；本局得分：CAN 1，SWE 0；累计：CAN 2，SWE 1。
- 壶色归属：red→CAN，yellow→SWE（由连续壶面新增壶与投手队伍反推）。
- 逐手覆盖：16/16 手，完整。

| 手 | 出手方 / 投手 | 官方叫球（评分） | 出手后检测壶数 | 营内暂时得分 | 观察到的离散目标 |
| --- | --- | --- | --- | --- | --- |
| 1 | SWE / SUNDGREN C | Front（4） | CAN 0, SWE 1 | 营内无壶 | 前场占位/守壶 |
| 2 | CAN / WALKER G | Front（4） | CAN 1, SWE 1 | 营内无壶 | 前场占位/守壶 |
| 3 | SWE / SUNDGREN C | Draw（3） | CAN 1, SWE 2 | SWE 暂得 1（最近 0.46 m） | 落营或前场落点 |
| 4 | CAN / WALKER G | Draw（2） | CAN 2, SWE 1 | CAN 暂得 1（最近 0.73 m） | 落营或前场落点 |
| 5 | SWE / WRANAA R | Hit and Roll（4） | CAN 1, SWE 3 | SWE 暂得 2（最近 0.24 m） | 撞击后滚到新位置 |
| 6 | CAN / GALLANT B | Double Take-out（4） | CAN 2, SWE 0 | 营内无壶 | 双飞，压低场上壶数 |
| 7 | SWE / WRANAA R | Guard（2） | CAN 2, SWE 2 | SWE 暂得 1（最近 0.53 m） | 前场守壶，制造掩护 |
| 8 | CAN / GALLANT B | Hit and Roll（0） | CAN 2, SWE 2 | SWE 暂得 1（最近 0.85 m） | 撞击后滚到新位置 |
| 9 | SWE / ERIKSSON O | Draw（3） | CAN 2, SWE 3 | SWE 暂得 2（最近 0.59 m） | 落营或前场落点 |
| 10 | CAN / NICHOLS M | Raise（4） | CAN 3, SWE 3 | CAN 暂得 1（最近 0.81 m） | 推进己方壶 |
| 11 | SWE / ERIKSSON O | Promotion Take-out（4） | CAN 2, SWE 4 | SWE 暂得 3（最近 0.85 m） | 借己方壶完成清除 |
| 12 | CAN / NICHOLS M | Hit and Roll（3） | CAN 3, SWE 3 | CAN 暂得 1（最近 0.78 m） | 撞击后滚到新位置 |
| 13 | SWE / EDIN N | Take-out（4） | CAN 3, SWE 4 | SWE 暂得 3（最近 0.82 m） | 清除/处理对方壶 |
| 14 | CAN / GUSHUE B | Raise（4） | CAN 4, SWE 4 | CAN 暂得 1（最近 1.04 m） | 推进己方壶 |
| 15 | SWE / EDIN N | Draw（4） | CAN 4, SWE 5 | SWE 暂得 1（最近 0.32 m） | 落营或前场落点 |
| 16 | CAN / GUSHUE B | Raise（2） | CAN 5, SWE 5 | CAN 暂得 1（最近 1.04 m） | 推进己方壶 |

第 4 局：CAN 有后手并拿到 1 分。 叫球结构：清除类 2 手、守壶类 3 手、draw 4 手。 需要结合逐手壶面判断是哪一次碰撞改变了局势，不能仅从叫球名称下结论。

## 第 5 局

- 后手：SWE；本局得分：CAN 0，SWE 1；累计：CAN 2，SWE 2。
- 壶色归属：red→CAN，yellow→SWE（由连续壶面新增壶与投手队伍反推）。
- 逐手覆盖：16/16 手，完整。

| 手 | 出手方 / 投手 | 官方叫球（评分） | 出手后检测壶数 | 营内暂时得分 | 观察到的离散目标 |
| --- | --- | --- | --- | --- | --- |
| 1 | CAN / WALKER G | Front（4） | CAN 1, SWE 0 | 营内无壶 | 前场占位/守壶 |
| 2 | SWE / SUNDGREN C | Draw（3） | CAN 1, SWE 1 | SWE 暂得 1（最近 0.47 m） | 落营或前场落点 |
| 3 | CAN / WALKER G | Draw（3） | CAN 2, SWE 1 | SWE 暂得 1（最近 0.46 m） | 落营或前场落点 |
| 4 | SWE / SUNDGREN C | Draw（4） | CAN 2, SWE 2 | SWE 暂得 1（最近 0.46 m） | 落营或前场落点 |
| 5 | CAN / GALLANT B | Draw（4） | CAN 2, SWE 2 | SWE 暂得 2（最近 0.46 m） | 落营或前场落点 |
| 6 | SWE / WRANAA R | Raise（4） | CAN 3, SWE 3 | SWE 暂得 2（最近 0.46 m） | 推进己方壶 |
| 7 | CAN / GALLANT B | Promotion Take-out（3） | CAN 3, SWE 2 | SWE 暂得 1（最近 0.49 m） | 借己方壶完成清除 |
| 8 | SWE / WRANAA R | Take-out（4） | CAN 2, SWE 3 | SWE 暂得 1（最近 0.49 m） | 清除/处理对方壶 |
| 9 | CAN / NICHOLS M | Promotion Take-out（4） | CAN 3, SWE 1 | CAN 暂得 2（最近 0.63 m） | 借己方壶完成清除 |
| 10 | SWE / ERIKSSON O | Double Take-out（2） | CAN 2, SWE 2 | CAN 暂得 1（最近 0.63 m） | 双飞，压低场上壶数 |
| 11 | CAN / NICHOLS M | Hit and Roll（3） | CAN 3, SWE 1 | CAN 暂得 1（最近 0.63 m） | 撞击后滚到新位置 |
| 12 | SWE / ERIKSSON O | Take-out（4） | CAN 2, SWE 2 | SWE 暂得 2（最近 0.84 m） | 清除/处理对方壶 |
| 13 | CAN / GUSHUE B | Double Take-out（4） | CAN 3, SWE 1 | CAN 暂得 1（最近 0.64 m） | 双飞，压低场上壶数 |
| 14 | SWE / EDIN N | Draw（3） | CAN 3, SWE 2 | SWE 暂得 1（最近 0.45 m） | 落营或前场落点 |
| 15 | CAN / GUSHUE B | Take-out（4） | CAN 4, SWE 1 | CAN 暂得 2（最近 0.43 m） | 清除/处理对方壶 |
| 16 | SWE / EDIN N | Take-out（4） | CAN 3, SWE 2 | SWE 暂得 1（最近 0.20 m） | 清除/处理对方壶 |

第 5 局：SWE 有后手并拿到 1 分。 叫球结构：清除类 6 手、守壶类 1 手、draw 5 手。 需要结合逐手壶面判断是哪一次碰撞改变了局势，不能仅从叫球名称下结论。

## 第 6 局

- 后手：CAN；本局得分：CAN 0，SWE 0；累计：CAN 2，SWE 2。
- 壶色归属：red→CAN，yellow→SWE（由连续壶面新增壶与投手队伍反推）。
- 逐手覆盖：16/16 手，完整。

| 手 | 出手方 / 投手 | 官方叫球（评分） | 出手后检测壶数 | 营内暂时得分 | 观察到的离散目标 |
| --- | --- | --- | --- | --- | --- |
| 1 | SWE / SUNDGREN C | Draw（4） | CAN 0, SWE 1 | SWE 暂得 1（最近 0.56 m） | 落营或前场落点 |
| 2 | CAN / WALKER G | Front（4） | CAN 1, SWE 1 | SWE 暂得 1（最近 0.57 m） | 前场占位/守壶 |
| 3 | SWE / SUNDGREN C | Guard（2） | CAN 1, SWE 2 | SWE 暂得 1（最近 0.57 m） | 前场守壶，制造掩护 |
| 4 | CAN / WALKER G | Take-out（4） | CAN 2, SWE 2 | CAN 暂得 1（最近 1.15 m） | 清除/处理对方壶 |
| 5 | SWE / WRANAA R | Take-out（4） | CAN 1, SWE 3 | SWE 暂得 1（最近 0.86 m） | 清除/处理对方壶 |
| 6 | CAN / GALLANT B | Take-out（4） | CAN 2, SWE 2 | CAN 暂得 1（最近 1.73 m） | 清除/处理对方壶 |
| 7 | SWE / WRANAA R | Take-out（4） | CAN 1, SWE 3 | SWE 暂得 1（最近 1.82 m） | 清除/处理对方壶 |
| 8 | CAN / GALLANT B | Draw（4） | CAN 2, SWE 3 | CAN 暂得 1（最近 1.30 m） | 落营或前场落点 |
| 9 | SWE / ERIKSSON O | Double Take-out（2） | CAN 1, SWE 3 | CAN 暂得 1（最近 1.31 m） | 双飞，压低场上壶数 |
| 10 | CAN / NICHOLS M | Draw（4） | CAN 2, SWE 3 | CAN 暂得 2（最近 1.31 m） | 落营或前场落点 |
| 11 | SWE / ERIKSSON O | Hit and Roll（3） | CAN 1, SWE 4 | SWE 暂得 1（最近 0.44 m） | 撞击后滚到新位置 |
| 12 | CAN / NICHOLS M | Take-out（4） | CAN 2, SWE 3 | CAN 暂得 2（最近 0.68 m） | 清除/处理对方壶 |
| 13 | SWE / EDIN N | Double Take-out（4） | CAN 0, SWE 4 | SWE 暂得 2（最近 1.53 m） | 双飞，压低场上壶数 |
| 14 | CAN / GUSHUE B | Take-out（4） | CAN 1, SWE 3 | CAN 暂得 1（最近 1.71 m） | 清除/处理对方壶 |
| 15 | SWE / EDIN N | Clearing（4） | CAN 0, SWE 2 | 营内无壶 | 清场，降低复杂度 |
| 16 | CAN / GUSHUE B | Through（-1） | CAN 0, SWE 2 | 营内无壶 | 上游未归类的叫球 |

第 6 局：本局 blank；后手没有拿分，后手权保留。 叫球结构：清除类 9 手、守壶类 2 手、draw 3 手。 需要结合逐手壶面判断是哪一次碰撞改变了局势，不能仅从叫球名称下结论。

## 第 7 局

- 后手：CAN；本局得分：CAN 0，SWE 0；累计：CAN 2，SWE 2。
- 壶色归属：red→CAN，yellow→SWE（由连续壶面新增壶与投手队伍反推）。
- 逐手覆盖：16/16 手，完整。

| 手 | 出手方 / 投手 | 官方叫球（评分） | 出手后检测壶数 | 营内暂时得分 | 观察到的离散目标 |
| --- | --- | --- | --- | --- | --- |
| 1 | SWE / SUNDGREN C | Front（4） | CAN 0, SWE 1 | 营内无壶 | 前场占位/守壶 |
| 2 | CAN / WALKER G | Draw（3） | CAN 1, SWE 1 | CAN 暂得 1（最近 1.18 m） | 落营或前场落点 |
| 3 | SWE / SUNDGREN C | Take-out（4） | CAN 0, SWE 2 | SWE 暂得 1（最近 0.89 m） | 清除/处理对方壶 |
| 4 | CAN / WALKER G | Take-out（4） | CAN 1, SWE 1 | CAN 暂得 1（最近 0.81 m） | 清除/处理对方壶 |
| 5 | SWE / WRANAA R | Take-out（4） | CAN 0, SWE 2 | SWE 暂得 1（最近 0.54 m） | 清除/处理对方壶 |
| 6 | CAN / GALLANT B | Take-out（4） | CAN 1, SWE 1 | CAN 暂得 1（最近 0.85 m） | 清除/处理对方壶 |
| 7 | SWE / WRANAA R | Take-out（2） | CAN 0, SWE 1 | 营内无壶 | 清除/处理对方壶 |
| 8 | CAN / GALLANT B | Clearing（4） | CAN 0, SWE 0 | 营内无壶 | 清场，降低复杂度 |
| 9 | SWE / ERIKSSON O | Draw（3） | CAN 0, SWE 1 | SWE 暂得 1（最近 0.40 m） | 落营或前场落点 |
| 10 | CAN / NICHOLS M | Take-out（4） | CAN 1, SWE 0 | 营内无壶 | 清除/处理对方壶 |
| 11 | SWE / ERIKSSON O | Take-out（4） | CAN 0, SWE 1 | SWE 暂得 1（最近 1.55 m） | 清除/处理对方壶 |
| 12 | CAN / NICHOLS M | Take-out（4） | CAN 1, SWE 0 | CAN 暂得 1（最近 1.45 m） | 清除/处理对方壶 |
| 13 | SWE / EDIN N | Take-out（4） | CAN 0, SWE 1 | SWE 暂得 1（最近 1.36 m） | 清除/处理对方壶 |
| 14 | CAN / GUSHUE B | Take-out（4） | CAN 1, SWE 0 | CAN 暂得 1（最近 1.52 m） | 清除/处理对方壶 |
| 15 | SWE / EDIN N | Take-out（4） | CAN 0, SWE 1 | SWE 暂得 1（最近 1.39 m） | 清除/处理对方壶 |
| 16 | CAN / GUSHUE B | Clearing（4） | CAN 0, SWE 0 | 营内无壶 | 清场，降低复杂度 |

第 7 局：本局 blank；后手没有拿分，后手权保留。 叫球结构：清除类 13 手、守壶类 1 手、draw 2 手。 这局明显优先降低壶数；与“后手局面不利时可清场/blank”分支相符。

## 第 8 局

- 后手：未能由完整末手确认；本局得分：CAN 0，SWE 0；累计：CAN 2，SWE 2。
- 壶色归属：red→CAN，yellow→SWE（由连续壶面新增壶与投手队伍反推）。
- 逐手覆盖：15/16 手，不完整；本局不下完整战术结论。

| 手 | 出手方 / 投手 | 官方叫球（评分） | 出手后检测壶数 | 营内暂时得分 | 观察到的离散目标 |
| --- | --- | --- | --- | --- | --- |
| 1 | SWE / SUNDGREN C | Front（4） | CAN 0, SWE 1 | 营内无壶 | 前场占位/守壶 |
| 2 | CAN / WALKER G | Front（4） | CAN 1, SWE 1 | 营内无壶 | 前场占位/守壶 |
| 3 | SWE / SUNDGREN C | Front（4） | CAN 1, SWE 2 | 营内无壶 | 前场占位/守壶 |
| 4 | CAN / WALKER G | Draw（3） | CAN 2, SWE 2 | CAN 暂得 1（最近 0.86 m） | 落营或前场落点 |
| 5 | SWE / WRANAA R | Raise（4） | CAN 2, SWE 3 | CAN 暂得 1（最近 0.05 m） | 推进己方壶 |
| 6 | CAN / GALLANT B | Clearing（4） | CAN 2, SWE 2 | CAN 暂得 1（最近 0.04 m） | 清场，降低复杂度 |
| 7 | SWE / WRANAA R | Draw（0） | CAN 2, SWE 3 | CAN 暂得 1（最近 0.05 m） | 落营或前场落点 |
| 8 | CAN / GALLANT B | Hit and Roll（4） | CAN 3, SWE 2 | CAN 暂得 1（最近 0.05 m） | 撞击后滚到新位置 |
| 9 | SWE / ERIKSSON O | Hit and Roll（2） | CAN 2, SWE 3 | CAN 暂得 1（最近 0.04 m） | 撞击后滚到新位置 |
| 10 | CAN / NICHOLS M | Hit and Roll（4） | CAN 3, SWE 2 | CAN 暂得 2（最近 0.05 m） | 撞击后滚到新位置 |
| 11 | SWE / ERIKSSON O | Double Take-out（4） | CAN 1, SWE 2 | SWE 暂得 1（最近 1.07 m） | 双飞，压低场上壶数 |
| 12 | CAN / NICHOLS M | Double Take-out（2） | CAN 1, SWE 0 | 营内无壶 | 双飞，压低场上壶数 |
| 13 | SWE / EDIN N | Raise（3） | CAN 1, SWE 2 | SWE 暂得 2（最近 0.32 m） | 推进己方壶 |
| 14 | CAN / GUSHUE B | Double Take-out（2） | CAN 2, SWE 1 | SWE 暂得 1（最近 0.04 m） | 双飞，压低场上壶数 |
| 15 | SWE / EDIN N | Take-out（4） | CAN 1, SWE 2 | SWE 暂得 2（最近 0.04 m） | 清除/处理对方壶 |

第 8 局：上游库没有完整的 16 手记录（或最后一手没有投手信息）。比分栏仍可作为赛果参考，但不能据此判成 blank、偷分或末手战术。

## 第 9 局

- 后手：CAN；本局得分：CAN 2，SWE 0；累计：CAN 4，SWE 2。
- 壶色归属：red→CAN，yellow→SWE（由连续壶面新增壶与投手队伍反推）。
- 逐手覆盖：16/16 手，完整。

| 手 | 出手方 / 投手 | 官方叫球（评分） | 出手后检测壶数 | 营内暂时得分 | 观察到的离散目标 |
| --- | --- | --- | --- | --- | --- |
| 1 | SWE / SUNDGREN C | Front（4） | CAN 0, SWE 1 | 营内无壶 | 前场占位/守壶 |
| 2 | CAN / WALKER G | Draw（4） | CAN 1, SWE 1 | CAN 暂得 1（最近 0.46 m） | 落营或前场落点 |
| 3 | SWE / SUNDGREN C | Front（3） | CAN 1, SWE 2 | CAN 暂得 1（最近 0.46 m） | 前场占位/守壶 |
| 4 | CAN / WALKER G | Draw（4） | CAN 2, SWE 2 | CAN 暂得 2（最近 0.45 m） | 落营或前场落点 |
| 5 | SWE / WRANAA R | Raise（0） | CAN 2, SWE 3 | CAN 暂得 2（最近 0.45 m） | 推进己方壶 |
| 6 | CAN / GALLANT B | Clearing（4） | CAN 2, SWE 1 | CAN 暂得 2（最近 0.46 m） | 清场，降低复杂度 |
| 7 | SWE / WRANAA R | Raise（4） | CAN 1, SWE 3 | CAN 暂得 1（最近 0.42 m） | 推进己方壶 |
| 8 | CAN / GALLANT B | Clearing（4） | CAN 3, SWE 1 | CAN 暂得 2（最近 0.42 m） | 清场，降低复杂度 |
| 9 | SWE / ERIKSSON O | Draw（3） | CAN 3, SWE 2 | SWE 暂得 1（最近 0.04 m） | 落营或前场落点 |
| 10 | CAN / NICHOLS M | Take-out（2） | CAN 3, SWE 1 | CAN 暂得 2（最近 0.42 m） | 清除/处理对方壶 |
| 11 | SWE / ERIKSSON O | Draw（4） | CAN 3, SWE 2 | SWE 暂得 1（最近 0.32 m） | 落营或前场落点 |
| 12 | CAN / NICHOLS M | Raise（3） | CAN 4, SWE 1 | CAN 暂得 2（最近 0.10 m） | 推进己方壶 |
| 13 | SWE / EDIN N | Draw（2） | CAN 4, SWE 2 | CAN 暂得 1（最近 0.10 m） | 落营或前场落点 |
| 14 | CAN / GUSHUE B | Double Take-out（4） | CAN 4, SWE 1 | CAN 暂得 3（最近 0.10 m） | 双飞，压低场上壶数 |
| 15 | SWE / EDIN N | Double Take-out（3） | CAN 4, SWE 2 | SWE 暂得 1（最近 0.66 m） | 双飞，压低场上壶数 |
| 16 | CAN / GUSHUE B | Draw（4） | CAN 5, SWE 2 | CAN 暂得 1（最近 0.37 m） | 落营或前场落点 |

第 9 局：CAN 有后手并拿到 2 分。 叫球结构：清除类 5 手、守壶类 2 手、draw 6 手。 需要结合逐手壶面判断是哪一次碰撞改变了局势，不能仅从叫球名称下结论。

## 第 10 局

- 后手：未能由完整末手确认；本局得分：CAN 0，SWE 0；累计：CAN 4，SWE 2。
- 壶色归属：red→CAN，yellow→SWE（由连续壶面新增壶与投手队伍反推）。
- 逐手覆盖：16/16 手，不完整；本局不下完整战术结论。

| 手 | 出手方 / 投手 | 官方叫球（评分） | 出手后检测壶数 | 营内暂时得分 | 观察到的离散目标 |
| --- | --- | --- | --- | --- | --- |
| 1 | CAN / WALKER G | Draw（4） | CAN 1, SWE 0 | CAN 暂得 1（最近 0.20 m） | 落营或前场落点 |
| 2 | SWE / SUNDGREN C | Front（4） | CAN 1, SWE 1 | CAN 暂得 1（最近 0.20 m） | 前场占位/守壶 |
| 3 | CAN / WALKER G | Wick / Soft Peeling（4） | CAN 1, SWE 1 | CAN 暂得 1（最近 0.20 m） | 轻碰/软 peel，调整而非硬清 |
| 4 | SWE / SUNDGREN C | Front（4） | CAN 1, SWE 2 | CAN 暂得 1（最近 0.20 m） | 前场占位/守壶 |
| 5 | CAN / GALLANT B | Clearing（4） | CAN 1, SWE 1 | CAN 暂得 1（最近 0.20 m） | 清场，降低复杂度 |
| 6 | SWE / WRANAA R | Front（4） | CAN 1, SWE 2 | CAN 暂得 1（最近 0.20 m） | 前场占位/守壶 |
| 7 | CAN / GALLANT B | Clearing（4） | CAN 1, SWE 1 | CAN 暂得 1（最近 0.20 m） | 清场，降低复杂度 |
| 8 | SWE / WRANAA R | Draw（2） | CAN 1, SWE 1 | CAN 暂得 1（最近 0.20 m） | 落营或前场落点 |
| 9 | CAN / NICHOLS M | Clearing（4） | CAN 1, SWE 1 | CAN 暂得 1（最近 0.19 m） | 清场，降低复杂度 |
| 10 | SWE / ERIKSSON O | Draw（4） | CAN 1, SWE 2 | CAN 暂得 1（最近 0.20 m） | 落营或前场落点 |
| 11 | CAN / NICHOLS M | Take-out（1） | CAN 2, SWE 2 | CAN 暂得 2（最近 0.20 m） | 清除/处理对方壶 |
| 12 | SWE / ERIKSSON O | Draw（2） | CAN 2, SWE 3 | CAN 暂得 1（最近 0.05 m） | 落营或前场落点 |
| 13 | CAN / GUSHUE B | Double Take-out（4） | CAN 3, SWE 1 | CAN 暂得 3（最近 0.05 m） | 双飞，压低场上壶数 |
| 14 | SWE / EDIN N | Freeze（0） | CAN 3, SWE 2 | CAN 暂得 1（最近 0.05 m） | 上游未归类的叫球 |
| 15 | CAN / GUSHUE B | Clearing（4） | CAN 4, SWE 1 | CAN 暂得 4（最近 0.05 m） | 清场，降低复杂度 |
| 16 | 未知 / 未知 | 未记录（-） | CAN 0, SWE 0 | 营内无壶 | 上游未归类的叫球 |

第 10 局：上游库没有完整的 16 手记录（或最后一手没有投手信息）。比分栏仍可作为赛果参考，但不能据此判成 blank、偷分或末手战术。
