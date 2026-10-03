# NWNHT 公开壶谱复盘：CAN vs SWE

- 比赛：361° World Men's Curling Championship 2018，2018-04-06 08:30:00，match_id=1802
- 最终比分：CAN 5 – 6 SWE
- 数据：NWNHT/curling 随附 SQLite；壶位为上游自动解析坐标。叫球/评分和壶位是事实记录，最后一列的战术意图是我们的保守归纳。
- 对照原则：[Team Gushue 公开战术树](../../planning_proxy/docs/strategy/05_Team_Gushue公开战术树_证据版.md)。

## 第 1 局

- 后手：SWE；本局得分：CAN 0，SWE 3；累计：CAN 0，SWE 3。
- 壶色归属：red→CAN，yellow→SWE（由连续壶面新增壶与投手队伍反推）。
- 逐手覆盖：16/16 手，完整。

| 手 | 出手方 / 投手 | 官方叫球（评分） | 出手后检测壶数 | 营内暂时得分 | 观察到的离散目标 |
| --- | --- | --- | --- | --- | --- |
| 1 | CAN / WALKER G | Front（4） | CAN 1, SWE 0 | 营内无壶 | 前场占位/守壶 |
| 2 | SWE / SUNDGREN C | Front（4） | CAN 1, SWE 1 | 营内无壶 | 前场占位/守壶 |
| 3 | CAN / WALKER G | Front（4） | CAN 2, SWE 1 | 营内无壶 | 前场占位/守壶 |
| 4 | SWE / SUNDGREN C | Draw（4） | CAN 2, SWE 2 | SWE 暂得 1（最近 1.32 m） | 落营或前场落点 |
| 5 | CAN / GALLANT B | Double Take-out（2） | CAN 3, SWE 1 | 营内无壶 | 双飞，压低场上壶数 |
| 6 | SWE / WRANAA R | Clearing（4） | CAN 2, SWE 1 | 营内无壶 | 清场，降低复杂度 |
| 7 | CAN / GALLANT B | Draw（4） | CAN 3, SWE 1 | CAN 暂得 1（最近 0.88 m） | 落营或前场落点 |
| 8 | SWE / WRANAA R | Double Take-out（2） | CAN 2, SWE 2 | CAN 暂得 1（最近 0.87 m） | 双飞，压低场上壶数 |
| 9 | CAN / NICHOLS M | Guard（3） | CAN 3, SWE 2 | CAN 暂得 1（最近 0.87 m） | 前场守壶，制造掩护 |
| 10 | SWE / ERIKSSON O | Take-out（4） | CAN 2, SWE 3 | SWE 暂得 1（最近 1.16 m） | 清除/处理对方壶 |
| 11 | CAN / NICHOLS M | Take-out（0） | CAN 3, SWE 3 | SWE 暂得 1（最近 1.16 m） | 清除/处理对方壶 |
| 12 | SWE / ERIKSSON O | Raise（3） | CAN 3, SWE 4 | SWE 暂得 2（最近 1.24 m） | 推进己方壶 |
| 13 | CAN / GUSHUE B | Take-out（4） | CAN 4, SWE 3 | SWE 暂得 1（最近 1.24 m） | 清除/处理对方壶 |
| 14 | SWE / EDIN N | Draw（4） | CAN 4, SWE 4 | SWE 暂得 2（最近 1.10 m） | 落营或前场落点 |
| 15 | CAN / GUSHUE B | Draw（4） | CAN 5, SWE 4 | CAN 暂得 1（最近 0.66 m） | 落营或前场落点 |
| 16 | SWE / EDIN N | Double Take-out（4） | CAN 3, SWE 5 | SWE 暂得 2（最近 1.10 m） | 双飞，压低场上壶数 |

第 1 局：SWE 有后手并拿到 3 分。 叫球结构：清除类 7 手、守壶类 4 手、draw 4 手。 前场结构与营内落点同时出现，属于主动制造多层局面的样本。

## 第 2 局

- 后手：CAN；本局得分：CAN 1，SWE 0；累计：CAN 1，SWE 3。
- 壶色归属：red→CAN，yellow→SWE（由连续壶面新增壶与投手队伍反推）。
- 逐手覆盖：16/16 手，完整。

| 手 | 出手方 / 投手 | 官方叫球（评分） | 出手后检测壶数 | 营内暂时得分 | 观察到的离散目标 |
| --- | --- | --- | --- | --- | --- |
| 1 | SWE / SUNDGREN C | Draw（4） | CAN 0, SWE 0 | 营内无壶 | 落营或前场落点 |
| 2 | CAN / WALKER G | Front（4） | CAN 1, SWE 0 | 营内无壶 | 前场占位/守壶 |
| 3 | SWE / SUNDGREN C | Guard（4） | CAN 1, SWE 2 | SWE 暂得 1（最近 0.68 m） | 前场守壶，制造掩护 |
| 4 | CAN / WALKER G | Draw（4） | CAN 2, SWE 2 | SWE 暂得 1（最近 0.68 m） | 落营或前场落点 |
| 5 | SWE / WRANAA R | Clearing（4） | CAN 1, SWE 2 | SWE 暂得 1（最近 0.68 m） | 清场，降低复杂度 |
| 6 | CAN / GALLANT B | Front（4） | CAN 2, SWE 2 | SWE 暂得 1（最近 0.68 m） | 前场占位/守壶 |
| 7 | SWE / WRANAA R | Clearing（4） | CAN 1, SWE 2 | SWE 暂得 1（最近 0.68 m） | 清场，降低复杂度 |
| 8 | CAN / GALLANT B | Draw（4） | CAN 2, SWE 2 | SWE 暂得 1（最近 0.68 m） | 落营或前场落点 |
| 9 | SWE / ERIKSSON O | Promotion Take-out（4） | CAN 1, SWE 2 | SWE 暂得 1（最近 0.68 m） | 借己方壶完成清除 |
| 10 | CAN / NICHOLS M | Draw（0） | CAN 2, SWE 2 | SWE 暂得 1（最近 0.68 m） | 落营或前场落点 |
| 11 | SWE / ERIKSSON O | Raise（4） | CAN 1, SWE 3 | SWE 暂得 3（最近 0.17 m） | 推进己方壶 |
| 12 | CAN / NICHOLS M | Raise（3） | CAN 3, SWE 2 | CAN 暂得 1（最近 0.57 m） | 推进己方壶 |
| 13 | SWE / EDIN N | Hit and Roll（4） | CAN 2, SWE 3 | SWE 暂得 3（最近 0.23 m） | 撞击后滚到新位置 |
| 14 | CAN / GUSHUE B | Double Take-out（4） | CAN 3, SWE 1 | CAN 暂得 1（最近 1.52 m） | 双飞，压低场上壶数 |
| 15 | SWE / EDIN N | Double Take-out（4） | CAN 1, SWE 2 | SWE 暂得 2（最近 1.56 m） | 双飞，压低场上壶数 |
| 16 | CAN / GUSHUE B | Draw（4） | CAN 2, SWE 2 | CAN 暂得 1（最近 0.55 m） | 落营或前场落点 |

第 2 局：CAN 有后手并拿到 1 分。 叫球结构：清除类 4 手、守壶类 3 手、draw 5 手。 需要结合逐手壶面判断是哪一次碰撞改变了局势，不能仅从叫球名称下结论。

## 第 3 局

- 后手：SWE；本局得分：CAN 0，SWE 0；累计：CAN 1，SWE 3。
- 壶色归属：red→CAN，yellow→SWE（由连续壶面新增壶与投手队伍反推）。
- 逐手覆盖：16/16 手，完整。

| 手 | 出手方 / 投手 | 官方叫球（评分） | 出手后检测壶数 | 营内暂时得分 | 观察到的离散目标 |
| --- | --- | --- | --- | --- | --- |
| 1 | CAN / WALKER G | Front（4） | CAN 1, SWE 0 | 营内无壶 | 前场占位/守壶 |
| 2 | SWE / SUNDGREN C | Draw（3） | CAN 1, SWE 1 | SWE 暂得 1（最近 0.53 m） | 落营或前场落点 |
| 3 | CAN / WALKER G | Draw（4） | CAN 2, SWE 1 | SWE 暂得 1（最近 0.52 m） | 落营或前场落点 |
| 4 | SWE / SUNDGREN C | Draw（3） | CAN 1, SWE 2 | SWE 暂得 2（最近 0.52 m） | 落营或前场落点 |
| 5 | CAN / GALLANT B | Draw（3） | CAN 3, SWE 2 | SWE 暂得 1（最近 0.52 m） | 落营或前场落点 |
| 6 | SWE / WRANAA R | Clearing（4） | CAN 2, SWE 2 | SWE 暂得 1（最近 0.52 m） | 清场，降低复杂度 |
| 7 | CAN / GALLANT B | Guard（4） | CAN 3, SWE 2 | SWE 暂得 1（最近 0.53 m） | 前场守壶，制造掩护 |
| 8 | SWE / WRANAA R | Draw（4） | CAN 2, SWE 3 | SWE 暂得 3（最近 0.53 m） | 落营或前场落点 |
| 9 | CAN / NICHOLS M | Double Take-out（0） | CAN 3, SWE 3 | SWE 暂得 1（最近 0.53 m） | 双飞，压低场上壶数 |
| 10 | SWE / ERIKSSON O | Promotion Take-out（4） | CAN 2, SWE 3 | SWE 暂得 3（最近 1.03 m） | 借己方壶完成清除 |
| 11 | CAN / NICHOLS M | Double Take-out（4） | CAN 3, SWE 2 | SWE 暂得 1（最近 0.52 m） | 双飞，压低场上壶数 |
| 12 | SWE / ERIKSSON O | Take-out（4） | CAN 2, SWE 3 | CAN 暂得 1（最近 0.65 m） | 清除/处理对方壶 |
| 13 | CAN / GUSHUE B | Hit and Roll（3） | CAN 3, SWE 2 | CAN 暂得 2（最近 0.65 m） | 撞击后滚到新位置 |
| 14 | SWE / EDIN N | Promotion Take-out（4） | CAN 1, SWE 3 | SWE 暂得 2（最近 0.68 m） | 借己方壶完成清除 |
| 15 | CAN / GUSHUE B | Take-out（4） | CAN 2, SWE 1 | CAN 暂得 1（最近 0.38 m） | 清除/处理对方壶 |
| 16 | SWE / EDIN N | Clearing（4） | CAN 1, SWE 1 | 营内无壶 | 清场，降低复杂度 |

第 3 局：本局 blank；后手没有拿分，后手权保留。 叫球结构：清除类 6 手、守壶类 2 手、draw 5 手。 需要结合逐手壶面判断是哪一次碰撞改变了局势，不能仅从叫球名称下结论。

## 第 4 局

- 后手：SWE；本局得分：CAN 0，SWE 1；累计：CAN 1，SWE 4。
- 壶色归属：red→CAN，yellow→SWE（由连续壶面新增壶与投手队伍反推）。
- 逐手覆盖：16/16 手，完整。

| 手 | 出手方 / 投手 | 官方叫球（评分） | 出手后检测壶数 | 营内暂时得分 | 观察到的离散目标 |
| --- | --- | --- | --- | --- | --- |
| 1 | CAN / WALKER G | Front（3） | CAN 1, SWE 0 | 营内无壶 | 前场占位/守壶 |
| 2 | SWE / SUNDGREN C | Front（0） | CAN 1, SWE 1 | SWE 暂得 1（最近 1.59 m） | 前场占位/守壶 |
| 3 | CAN / WALKER G | Front（4） | CAN 2, SWE 0 | 营内无壶 | 前场占位/守壶 |
| 4 | SWE / SUNDGREN C | Draw（4） | CAN 2, SWE 2 | SWE 暂得 2（最近 0.19 m） | 落营或前场落点 |
| 5 | CAN / GALLANT B | Draw（4） | CAN 3, SWE 2 | SWE 暂得 1（最近 0.19 m） | 落营或前场落点 |
| 6 | SWE / WRANAA R | Clearing（4） | CAN 1, SWE 2 | SWE 暂得 1（最近 0.18 m） | 清场，降低复杂度 |
| 7 | CAN / GALLANT B | Guard（4） | CAN 2, SWE 2 | SWE 暂得 1（最近 0.18 m） | 前场守壶，制造掩护 |
| 8 | SWE / WRANAA R | Clearing（4） | CAN 1, SWE 2 | SWE 暂得 1（最近 0.18 m） | 清场，降低复杂度 |
| 9 | CAN / NICHOLS M | Guard（4） | CAN 2, SWE 2 | SWE 暂得 1（最近 0.18 m） | 前场守壶，制造掩护 |
| 10 | SWE / ERIKSSON O | Clearing（4） | CAN 1, SWE 2 | SWE 暂得 1（最近 0.18 m） | 清场，降低复杂度 |
| 11 | CAN / NICHOLS M | Take-out（4） | CAN 2, SWE 1 | SWE 暂得 1（最近 0.18 m） | 清除/处理对方壶 |
| 12 | SWE / ERIKSSON O | Double Take-out（0） | CAN 2, SWE 1 | SWE 暂得 1（最近 0.18 m） | 双飞，压低场上壶数 |
| 13 | CAN / GUSHUE B | Promotion Take-out（4） | CAN 3, SWE 0 | CAN 暂得 3（最近 0.65 m） | 借己方壶完成清除 |
| 14 | SWE / EDIN N | Double Take-out（4） | CAN 1, SWE 0 | CAN 暂得 1（最近 1.14 m） | 双飞，压低场上壶数 |
| 15 | CAN / GUSHUE B | Draw（4） | CAN 2, SWE 0 | CAN 暂得 2（最近 0.88 m） | 落营或前场落点 |
| 16 | SWE / EDIN N | Take-out（4） | CAN 1, SWE 1 | SWE 暂得 1（最近 1.00 m） | 清除/处理对方壶 |

第 4 局：SWE 有后手并拿到 1 分。 叫球结构：清除类 7 手、守壶类 5 手、draw 3 手。 需要结合逐手壶面判断是哪一次碰撞改变了局势，不能仅从叫球名称下结论。

## 第 5 局

- 后手：CAN；本局得分：CAN 0，SWE 0；累计：CAN 1，SWE 4。
- 壶色归属：red→CAN，yellow→SWE（由连续壶面新增壶与投手队伍反推）。
- 逐手覆盖：16/16 手，完整。

| 手 | 出手方 / 投手 | 官方叫球（评分） | 出手后检测壶数 | 营内暂时得分 | 观察到的离散目标 |
| --- | --- | --- | --- | --- | --- |
| 1 | SWE / SUNDGREN C | Draw（4） | CAN 0, SWE 1 | SWE 暂得 1（最近 0.35 m） | 落营或前场落点 |
| 2 | CAN / WALKER G | Front（4） | CAN 1, SWE 1 | SWE 暂得 1（最近 0.34 m） | 前场占位/守壶 |
| 3 | SWE / SUNDGREN C | Draw（4） | CAN 1, SWE 1 | SWE 暂得 1（最近 1.16 m） | 落营或前场落点 |
| 4 | CAN / WALKER G | Front（4） | CAN 2, SWE 2 | SWE 暂得 2（最近 0.33 m） | 前场占位/守壶 |
| 5 | SWE / WRANAA R | Clearing（4） | CAN 1, SWE 2 | SWE 暂得 2（最近 0.33 m） | 清场，降低复杂度 |
| 6 | CAN / GALLANT B | Hit and Roll（3） | CAN 2, SWE 1 | SWE 暂得 1（最近 0.61 m） | 撞击后滚到新位置 |
| 7 | SWE / WRANAA R | Clearing（4） | CAN 1, SWE 1 | SWE 暂得 1（最近 0.61 m） | 清场，降低复杂度 |
| 8 | CAN / GALLANT B | Front（4） | CAN 2, SWE 1 | SWE 暂得 1（最近 0.61 m） | 前场占位/守壶 |
| 9 | SWE / ERIKSSON O | Clearing（4） | CAN 1, SWE 1 | SWE 暂得 1（最近 0.61 m） | 清场，降低复杂度 |
| 10 | CAN / NICHOLS M | Front（4） | CAN 2, SWE 1 | SWE 暂得 1（最近 0.61 m） | 前场占位/守壶 |
| 11 | SWE / ERIKSSON O | Clearing（4） | CAN 1, SWE 1 | SWE 暂得 1（最近 0.61 m） | 清场，降低复杂度 |
| 12 | CAN / NICHOLS M | Draw（4） | CAN 2, SWE 1 | SWE 暂得 1（最近 0.61 m） | 落营或前场落点 |
| 13 | SWE / EDIN N | Hit and Roll（4） | CAN 1, SWE 1 | SWE 暂得 1（最近 0.61 m） | 撞击后滚到新位置 |
| 14 | CAN / GUSHUE B | Hit and Roll（3） | CAN 2, SWE 0 | CAN 暂得 1（最近 0.89 m） | 撞击后滚到新位置 |
| 15 | SWE / EDIN N | Take-out（4） | CAN 1, SWE 1 | SWE 暂得 1（最近 1.15 m） | 清除/处理对方壶 |
| 16 | CAN / GUSHUE B | Clearing（4） | CAN 1, SWE 0 | 营内无壶 | 清场，降低复杂度 |

第 5 局：本局 blank；后手没有拿分，后手权保留。 叫球结构：清除类 6 手、守壶类 4 手、draw 3 手。 需要结合逐手壶面判断是哪一次碰撞改变了局势，不能仅从叫球名称下结论。

## 第 6 局

- 后手：CAN；本局得分：CAN 1，SWE 0；累计：CAN 2，SWE 4。
- 壶色归属：red→CAN，yellow→SWE（由连续壶面新增壶与投手队伍反推）。
- 逐手覆盖：16/16 手，完整。

| 手 | 出手方 / 投手 | 官方叫球（评分） | 出手后检测壶数 | 营内暂时得分 | 观察到的离散目标 |
| --- | --- | --- | --- | --- | --- |
| 1 | SWE / SUNDGREN C | Draw（3） | CAN 0, SWE 1 | SWE 暂得 1（最近 0.30 m） | 落营或前场落点 |
| 2 | CAN / WALKER G | Front（4） | CAN 1, SWE 1 | SWE 暂得 1（最近 0.30 m） | 前场占位/守壶 |
| 3 | SWE / SUNDGREN C | Draw（4） | CAN 1, SWE 2 | SWE 暂得 2（最近 0.27 m） | 落营或前场落点 |
| 4 | CAN / WALKER G | Front（4） | CAN 2, SWE 2 | SWE 暂得 2（最近 0.27 m） | 前场占位/守壶 |
| 5 | SWE / WRANAA R | Clearing（4） | CAN 1, SWE 2 | SWE 暂得 2（最近 0.27 m） | 清场，降低复杂度 |
| 6 | CAN / GALLANT B | Front（4） | CAN 2, SWE 2 | SWE 暂得 2（最近 0.27 m） | 前场占位/守壶 |
| 7 | SWE / WRANAA R | Clearing（4） | CAN 1, SWE 2 | SWE 暂得 2（最近 0.27 m） | 清场，降低复杂度 |
| 8 | CAN / GALLANT B | Front（4） | CAN 2, SWE 2 | SWE 暂得 2（最近 0.27 m） | 前场占位/守壶 |
| 9 | SWE / ERIKSSON O | Clearing（4） | CAN 1, SWE 2 | SWE 暂得 2（最近 0.27 m） | 清场，降低复杂度 |
| 10 | CAN / NICHOLS M | Draw（3） | CAN 2, SWE 1 | SWE 暂得 1（最近 0.30 m） | 落营或前场落点 |
| 11 | SWE / ERIKSSON O | Take-out（2） | CAN 1, SWE 2 | SWE 暂得 2（最近 0.19 m） | 清除/处理对方壶 |
| 12 | CAN / NICHOLS M | Draw（4） | CAN 2, SWE 2 | CAN 暂得 1（最近 0.25 m） | 落营或前场落点 |
| 13 | SWE / EDIN N | Take-out（4） | CAN 1, SWE 2 | SWE 暂得 2（最近 0.53 m） | 清除/处理对方壶 |
| 14 | CAN / GUSHUE B | Draw（3） | CAN 2, SWE 2 | SWE 暂得 1（最近 0.55 m） | 落营或前场落点 |
| 15 | SWE / EDIN N | Take-out（2） | CAN 1, SWE 2 | SWE 暂得 2（最近 0.55 m） | 清除/处理对方壶 |
| 16 | CAN / GUSHUE B | Take-out（4） | CAN 2, SWE 1 | CAN 暂得 1（最近 0.93 m） | 清除/处理对方壶 |

第 6 局：CAN 有后手并拿到 1 分。 叫球结构：清除类 7 手、守壶类 4 手、draw 5 手。 前场结构与营内落点同时出现，属于主动制造多层局面的样本。

## 第 7 局

- 后手：SWE；本局得分：CAN 2，SWE 0；累计：CAN 4，SWE 4。
- 壶色归属：red→CAN，yellow→SWE（由连续壶面新增壶与投手队伍反推）。
- 逐手覆盖：16/16 手，完整。

| 手 | 出手方 / 投手 | 官方叫球（评分） | 出手后检测壶数 | 营内暂时得分 | 观察到的离散目标 |
| --- | --- | --- | --- | --- | --- |
| 1 | CAN / WALKER G | Front（4） | CAN 1, SWE 0 | 营内无壶 | 前场占位/守壶 |
| 2 | SWE / SUNDGREN C | Draw（2） | CAN 1, SWE 1 | SWE 暂得 1（最近 1.32 m） | 落营或前场落点 |
| 3 | CAN / WALKER G | Front（4） | CAN 2, SWE 1 | SWE 暂得 1（最近 1.33 m） | 前场占位/守壶 |
| 4 | SWE / SUNDGREN C | Draw（4） | CAN 2, SWE 2 | SWE 暂得 2（最近 0.57 m） | 落营或前场落点 |
| 5 | CAN / GALLANT B | Draw（4） | CAN 3, SWE 2 | SWE 暂得 1（最近 0.57 m） | 落营或前场落点 |
| 6 | SWE / WRANAA R | Double Take-out（2） | CAN 2, SWE 3 | SWE 暂得 1（最近 0.57 m） | 双飞，压低场上壶数 |
| 7 | CAN / GALLANT B | Front（4） | CAN 3, SWE 3 | SWE 暂得 1（最近 0.57 m） | 前场占位/守壶 |
| 8 | SWE / WRANAA R | Clearing（4） | CAN 2, SWE 3 | SWE 暂得 1（最近 0.57 m） | 清场，降低复杂度 |
| 9 | CAN / NICHOLS M | Front（4） | CAN 3, SWE 3 | SWE 暂得 1（最近 0.57 m） | 前场占位/守壶 |
| 10 | SWE / ERIKSSON O | Clearing（4） | CAN 2, SWE 3 | SWE 暂得 1（最近 0.57 m） | 清场，降低复杂度 |
| 11 | CAN / NICHOLS M | Draw（4） | CAN 3, SWE 3 | CAN 暂得 1（最近 0.28 m） | 落营或前场落点 |
| 12 | SWE / ERIKSSON O | Double Take-out（2） | CAN 2, SWE 4 | CAN 暂得 1（最近 0.28 m） | 双飞，压低场上壶数 |
| 13 | CAN / GUSHUE B | Guard（4） | CAN 3, SWE 4 | CAN 暂得 1（最近 0.29 m） | 前场守壶，制造掩护 |
| 14 | SWE / EDIN N | Draw（3） | CAN 3, SWE 5 | CAN 暂得 1（最近 0.23 m） | 落营或前场落点 |
| 15 | CAN / GUSHUE B | Draw（4） | CAN 4, SWE 4 | CAN 暂得 2（最近 0.22 m） | 落营或前场落点 |
| 16 | SWE / EDIN N | Take-out（0） | CAN 4, SWE 4 | CAN 暂得 2（最近 0.23 m） | 清除/处理对方壶 |

第 7 局：CAN 无后手却拿到 2 分，属于偷分。 叫球结构：清除类 5 手、守壶类 5 手、draw 6 手。 前场结构与营内落点同时出现，属于主动制造多层局面的样本。

## 第 8 局

- 后手：SWE；本局得分：CAN 0，SWE 1；累计：CAN 4，SWE 5。
- 壶色归属：red→CAN，yellow→SWE（由连续壶面新增壶与投手队伍反推）。
- 逐手覆盖：16/16 手，完整。

| 手 | 出手方 / 投手 | 官方叫球（评分） | 出手后检测壶数 | 营内暂时得分 | 观察到的离散目标 |
| --- | --- | --- | --- | --- | --- |
| 1 | CAN / WALKER G | Front（4） | CAN 1, SWE 0 | 营内无壶 | 前场占位/守壶 |
| 2 | SWE / SUNDGREN C | Front（4） | CAN 1, SWE 1 | 营内无壶 | 前场占位/守壶 |
| 3 | CAN / WALKER G | Front（4） | CAN 2, SWE 1 | 营内无壶 | 前场占位/守壶 |
| 4 | SWE / SUNDGREN C | Draw（4） | CAN 2, SWE 2 | SWE 暂得 1（最近 0.88 m） | 落营或前场落点 |
| 5 | CAN / GALLANT B | Draw（4） | CAN 3, SWE 2 | CAN 暂得 1（最近 0.37 m） | 落营或前场落点 |
| 6 | SWE / WRANAA R | Double Take-out（2） | CAN 2, SWE 3 | CAN 暂得 1（最近 0.36 m） | 双飞，压低场上壶数 |
| 7 | CAN / GALLANT B | Guard（4） | CAN 3, SWE 3 | CAN 暂得 1（最近 0.37 m） | 前场守壶，制造掩护 |
| 8 | SWE / WRANAA R | Clearing（4） | CAN 2, SWE 3 | CAN 暂得 1（最近 0.37 m） | 清场，降低复杂度 |
| 9 | CAN / NICHOLS M | Guard（3） | CAN 3, SWE 3 | CAN 暂得 1（最近 0.37 m） | 前场守壶，制造掩护 |
| 10 | SWE / ERIKSSON O | Raise（4） | CAN 3, SWE 4 | SWE 暂得 1（最近 0.19 m） | 推进己方壶 |
| 11 | CAN / NICHOLS M | Draw（4） | CAN 4, SWE 4 | SWE 暂得 1（最近 0.19 m） | 落营或前场落点 |
| 12 | SWE / ERIKSSON O | Promotion Take-out（4） | CAN 2, SWE 4 | CAN 暂得 1（最近 1.18 m） | 借己方壶完成清除 |
| 13 | CAN / GUSHUE B | Draw（4） | CAN 3, SWE 4 | CAN 暂得 2（最近 0.62 m） | 落营或前场落点 |
| 14 | SWE / EDIN N | Promotion Take-out（1） | CAN 3, SWE 4 | CAN 暂得 2（最近 0.63 m） | 借己方壶完成清除 |
| 15 | CAN / GUSHUE B | Draw（4） | CAN 4, SWE 4 | CAN 暂得 3（最近 0.63 m） | 落营或前场落点 |
| 16 | SWE / EDIN N | Draw（4） | CAN 4, SWE 5 | SWE 暂得 1（最近 0.23 m） | 落营或前场落点 |

第 8 局：SWE 有后手并拿到 1 分。 叫球结构：清除类 2 手、守壶类 5 手、draw 6 手。 前场结构与营内落点同时出现，属于主动制造多层局面的样本。

## 第 9 局

- 后手：CAN；本局得分：CAN 1，SWE 0；累计：CAN 5，SWE 5。
- 壶色归属：red→CAN，yellow→SWE（由连续壶面新增壶与投手队伍反推）。
- 逐手覆盖：16/16 手，完整。

| 手 | 出手方 / 投手 | 官方叫球（评分） | 出手后检测壶数 | 营内暂时得分 | 观察到的离散目标 |
| --- | --- | --- | --- | --- | --- |
| 1 | SWE / SUNDGREN C | Front（4） | CAN 0, SWE 1 | 营内无壶 | 前场占位/守壶 |
| 2 | CAN / WALKER G | Draw（4） | CAN 1, SWE 1 | CAN 暂得 1（最近 0.25 m） | 落营或前场落点 |
| 3 | SWE / SUNDGREN C | Draw（4） | CAN 1, SWE 2 | CAN 暂得 1（最近 0.25 m） | 落营或前场落点 |
| 4 | CAN / WALKER G | Draw（4） | CAN 2, SWE 2 | CAN 暂得 1（最近 0.25 m） | 落营或前场落点 |
| 5 | SWE / WRANAA R | Raise（2） | CAN 2, SWE 3 | CAN 暂得 1（最近 0.25 m） | 推进己方壶 |
| 6 | CAN / GALLANT B | Promotion Take-out（4） | CAN 2, SWE 1 | SWE 暂得 1（最近 0.53 m） | 借己方壶完成清除 |
| 7 | SWE / WRANAA R | Take-out（4） | CAN 1, SWE 2 | SWE 暂得 2（最近 0.53 m） | 清除/处理对方壶 |
| 8 | CAN / GALLANT B | Promotion Take-out（3） | CAN 2, SWE 1 | CAN 暂得 1（最近 1.53 m） | 借己方壶完成清除 |
| 9 | SWE / ERIKSSON O | Take-out（4） | CAN 1, SWE 2 | SWE 暂得 2（最近 1.40 m） | 清除/处理对方壶 |
| 10 | CAN / NICHOLS M | Draw（4） | CAN 2, SWE 2 | CAN 暂得 1（最近 0.43 m） | 落营或前场落点 |
| 11 | SWE / ERIKSSON O | Double Take-out（2） | CAN 1, SWE 3 | CAN 暂得 1（最近 0.42 m） | 双飞，压低场上壶数 |
| 12 | CAN / NICHOLS M | Draw（4） | CAN 2, SWE 2 | CAN 暂得 2（最近 0.42 m） | 落营或前场落点 |
| 13 | SWE / EDIN N | Hit and Roll（4） | CAN 1, SWE 3 | SWE 暂得 1（最近 0.90 m） | 撞击后滚到新位置 |
| 14 | CAN / GUSHUE B | Raise（3） | CAN 2, SWE 3 | CAN 暂得 2（最近 0.90 m） | 推进己方壶 |
| 15 | SWE / EDIN N | Double Take-out（4） | CAN 0, SWE 3 | SWE 暂得 2（最近 1.77 m） | 双飞，压低场上壶数 |
| 16 | CAN / GUSHUE B | Draw（4） | CAN 1, SWE 3 | CAN 暂得 1（最近 0.36 m） | 落营或前场落点 |

第 9 局：CAN 有后手并拿到 1 分。 叫球结构：清除类 4 手、守壶类 1 手、draw 6 手。 需要结合逐手壶面判断是哪一次碰撞改变了局势，不能仅从叫球名称下结论。

## 第 10 局

- 后手：SWE；本局得分：CAN 0，SWE 1；累计：CAN 5，SWE 6。
- 壶色归属：red→CAN，yellow→SWE（由连续壶面新增壶与投手队伍反推）。
- 逐手覆盖：16/16 手，完整。

| 手 | 出手方 / 投手 | 官方叫球（评分） | 出手后检测壶数 | 营内暂时得分 | 观察到的离散目标 |
| --- | --- | --- | --- | --- | --- |
| 1 | CAN / WALKER G | Front（4） | CAN 1, SWE 0 | 营内无壶 | 前场占位/守壶 |
| 2 | SWE / SUNDGREN C | Wick / Soft Peeling（4） | CAN 1, SWE 1 | 营内无壶 | 轻碰/软 peel，调整而非硬清 |
| 3 | CAN / WALKER G | Front（4） | CAN 2, SWE 1 | 营内无壶 | 前场占位/守壶 |
| 4 | SWE / SUNDGREN C | Wick / Soft Peeling（4） | CAN 2, SWE 2 | CAN 暂得 1（最近 1.08 m） | 轻碰/软 peel，调整而非硬清 |
| 5 | CAN / GALLANT B | Front（4） | CAN 3, SWE 2 | CAN 暂得 1（最近 1.08 m） | 前场占位/守壶 |
| 6 | SWE / WRANAA R | Clearing（4） | CAN 1, SWE 2 | CAN 暂得 1（最近 1.08 m） | 清场，降低复杂度 |
| 7 | CAN / GALLANT B | Front（4） | CAN 2, SWE 2 | CAN 暂得 1（最近 1.09 m） | 前场占位/守壶 |
| 8 | SWE / WRANAA R | Clearing（4） | CAN 1, SWE 2 | CAN 暂得 1（最近 1.09 m） | 清场，降低复杂度 |
| 9 | CAN / NICHOLS M | Front（4） | CAN 2, SWE 2 | CAN 暂得 1（最近 1.08 m） | 前场占位/守壶 |
| 10 | SWE / ERIKSSON O | Clearing（4） | CAN 1, SWE 2 | CAN 暂得 1（最近 1.08 m） | 清场，降低复杂度 |
| 11 | CAN / NICHOLS M | Front（4） | CAN 2, SWE 2 | CAN 暂得 1（最近 1.08 m） | 前场占位/守壶 |
| 12 | SWE / ERIKSSON O | Clearing（4） | CAN 1, SWE 2 | CAN 暂得 1（最近 1.08 m） | 清场，降低复杂度 |
| 13 | CAN / GUSHUE B | Front（4） | CAN 2, SWE 2 | CAN 暂得 1（最近 1.09 m） | 前场占位/守壶 |
| 14 | SWE / EDIN N | Clearing（4） | CAN 1, SWE 2 | CAN 暂得 1（最近 1.09 m） | 清场，降低复杂度 |
| 15 | CAN / GUSHUE B | Draw（3） | CAN 2, SWE 2 | CAN 暂得 2（最近 0.97 m） | 落营或前场落点 |
| 16 | SWE / EDIN N | Draw（4） | CAN 2, SWE 3 | SWE 暂得 1（最近 0.40 m） | 落营或前场落点 |

第 10 局：SWE 有后手并拿到 1 分。 叫球结构：清除类 5 手、守壶类 7 手、draw 2 手。 需要结合逐手壶面判断是哪一次碰撞改变了局势，不能仅从叫球名称下结论。
