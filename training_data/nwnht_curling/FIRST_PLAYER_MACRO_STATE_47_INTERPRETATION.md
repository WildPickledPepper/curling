# 先手宏观状态机：47 个节点分别代表什么

结论：47 个节点不是 47 个神秘坐标簇，而是 `先手第 K 次出手 × 可解释壶形关系`。同名壶形在不同 K 下保留为不同节点，因为剩余壶数不同；但它们的几何含义一致。

术语：

- **当前占分**：仅指此刻营内最近壶属于哪方，是几何事实，不是比赛比分。
- **中线壳**：一方同时有中线守壶和营内壶；它不是安全构型。
- **必须 PhysX**：离散层不继续细分通道、保护角度、raise/runback 接触链，必须由严格 PhysX 搜索具体方案。
- **低支持回退**：某个原始壶形在该 K 下少于 250 条样本；它能路由但没有独立策略结论。

## K1：先手第 1 次出手（总第 1 手）

| 节点 | n | 代表局面 | PhysX |
| --- | ---: | --- | --- |
| `FIRST_K1_EMPTY` | 10,873 | 空场，无可见壶。 | 否 |

## K2：先手第 2 次出手（总第 3 手）

| 节点 | n | 代表局面 | PhysX |
| --- | ---: | --- | --- |
| `FIRST_K2_EMPTY` | 313 | 前两手后场上无可见壶，多为壶被清出或未保留。 | 否 |
| `FIRST_K2_GUARD_EXCHANGE` | 2,775 | 营内无壶，双方至少一颗前场守壶；典型前场交换。 | 否 |
| `FIRST_K2_OPPONENT_HOUSE_THREAT` | 3,207 | 对方已有最近营内壶、当前占分；尚不构成中线壳。 | 否 |
| `FIRST_K2_OWN_HOUSE_CONTROL` | 4,378 | 己方已有最近营内壶、当前占分；尚不构成己方中线壳。 | 否 |
| `FIRST_K2_LOW_SUPPORT_SEARCH_REQUIRED` | 200 | 本手罕见的稀疏/混合形态，历史不足以单独学习。 | 是 |

## K3：先手第 3 次出手（总第 5 手）

| 节点 | n | 代表局面 | PhysX |
| --- | ---: | --- | --- |
| `FIRST_K3_GUARD_EXCHANGE` | 1,050 | 仍以守壶为主，营内为空。 | 否 |
| `FIRST_K3_OPPONENT_CENTRE_SHELL` | 303 | 对方中线守壶遮住其营内壶；结构存在，但样本刚过支持阈值。 | 是 |
| `FIRST_K3_OWN_CENTRE_SHELL` | 2,224 | 己方中线守壶与己方营内壶形成遮护关系。 | 是 |
| `FIRST_K3_OPPONENT_HOUSE_THREAT` | 3,855 | 对方最近营内壶占分，但没有达到“对方中线壳”的判据。 | 否 |
| `FIRST_K3_OWN_HOUSE_CONTROL` | 3,221 | 己方最近营内壶占分，但没有达到“己方中线壳”的判据。 | 否 |
| `FIRST_K3_LOW_SUPPORT_SEARCH_REQUIRED` | 220 | 空场、极稀疏或极早拥挤等少见组合的合并回退。 | 是 |

## K4：先手第 4 次出手（总第 7 手）

| 节点 | n | 代表局面 | PhysX |
| --- | ---: | --- | --- |
| `FIRST_K4_CROWDED_HOUSE_SEARCH_REQUIRED` | 1,459 | 可见壶至少 5 颗、其中至少 3 颗在营内；碰撞链丰富。 | 是 |
| `FIRST_K4_GUARD_EXCHANGE` | 884 | 守壶仍在前场，营内为空。 | 否 |
| `FIRST_K4_OPPONENT_CENTRE_SHELL` | 495 | 对方中线守壶加营内壶。 | 是 |
| `FIRST_K4_OWN_CENTRE_SHELL` | 1,328 | 己方中线守壶加营内壶。 | 是 |
| `FIRST_K4_OPPONENT_HOUSE_THREAT` | 3,201 | 对方当前营内最近壶占分。 | 否 |
| `FIRST_K4_OWN_HOUSE_CONTROL` | 3,231 | 己方当前营内最近壶占分。 | 否 |
| `FIRST_K4_LOW_SUPPORT_SEARCH_REQUIRED` | 275 | 罕见的空场、稀疏或未归入稳定宏观类的组合。 | 是 |

## K5：先手第 5 次出手（总第 9 手）

| 节点 | n | 代表局面 | PhysX |
| --- | ---: | --- | --- |
| `FIRST_K5_CROWDED_HOUSE_SEARCH_REQUIRED` | 2,228 | 多壶进营、接触与通道组合复杂。 | 是 |
| `FIRST_K5_GUARD_EXCHANGE` | 796 | 仍无营内壶的前场守壶结构。 | 否 |
| `FIRST_K5_OPPONENT_CENTRE_SHELL` | 536 | 对方中线守壶遮护营内壶。 | 是 |
| `FIRST_K5_OWN_CENTRE_SHELL` | 948 | 己方中线守壶遮护营内壶。 | 是 |
| `FIRST_K5_OPPONENT_HOUSE_THREAT` | 3,284 | 对方当前最近营内壶占分。 | 否 |
| `FIRST_K5_OWN_HOUSE_CONTROL` | 2,791 | 己方当前最近营内壶占分。 | 否 |
| `FIRST_K5_LOW_SUPPORT_SEARCH_REQUIRED` | 290 | 低样本壶形回退。 | 是 |

## K6：先手第 6 次出手（总第 11 手）

| 节点 | n | 代表局面 | PhysX |
| --- | ---: | --- | --- |
| `FIRST_K6_CROWDED_HOUSE_SEARCH_REQUIRED` | 2,884 | 多壶营内缠斗，离散层不判具体撞击链。 | 是 |
| `FIRST_K6_GUARD_EXCHANGE` | 631 | 营内为空、前场守壶存在。 | 否 |
| `FIRST_K6_OPPONENT_CENTRE_SHELL` | 507 | 对方中线壳。 | 是 |
| `FIRST_K6_OWN_CENTRE_SHELL` | 777 | 己方中线壳。 | 是 |
| `FIRST_K6_OPPONENT_HOUSE_THREAT` | 3,523 | 对方当前营内占分。 | 否 |
| `FIRST_K6_OWN_HOUSE_CONTROL` | 2,248 | 己方当前营内占分。 | 否 |
| `FIRST_K6_LOW_SUPPORT_SEARCH_REQUIRED` | 303 | 低样本壶形回退。 | 是 |

## K7：先手第 7 次出手（总第 13 手）

| 节点 | n | 代表局面 | PhysX |
| --- | ---: | --- | --- |
| `FIRST_K7_CROWDED_HOUSE_SEARCH_REQUIRED` | 3,588 | 高密度营内缠斗。 | 是 |
| `FIRST_K7_GUARD_EXCHANGE` | 518 | 营内为空、仍有前场守壶。 | 否 |
| `FIRST_K7_OPPONENT_CENTRE_SHELL` | 502 | 对方中线壳。 | 是 |
| `FIRST_K7_OWN_CENTRE_SHELL` | 561 | 己方中线壳。 | 是 |
| `FIRST_K7_OPPONENT_HOUSE_THREAT` | 3,533 | 对方当前营内占分。 | 否 |
| `FIRST_K7_OWN_HOUSE_CONTROL` | 1,834 | 己方当前营内占分。 | 否 |
| `FIRST_K7_LOW_SUPPORT_SEARCH_REQUIRED` | 337 | 低样本壶形回退。 | 是 |

## K8：先手第 8 次出手（总第 15 手）

| 节点 | n | 代表局面 | PhysX |
| --- | ---: | --- | --- |
| `FIRST_K8_CROWDED_HOUSE_SEARCH_REQUIRED` | 4,389 | 高密度营内缠斗；这是末手前常见主路径，非异常。 | 是 |
| `FIRST_K8_GUARD_EXCHANGE` | 336 | 营内为空、存在前场守壶。 | 否 |
| `FIRST_K8_OPPONENT_CENTRE_SHELL` | 433 | 对方中线壳。 | 是 |
| `FIRST_K8_OWN_CENTRE_SHELL` | 513 | 己方中线壳。 | 是 |
| `FIRST_K8_OPPONENT_HOUSE_THREAT` | 3,655 | 对方当前营内占分。 | 否 |
| `FIRST_K8_OWN_HOUSE_CONTROL` | 1,196 | 己方当前营内占分。 | 否 |
| `FIRST_K8_LOW_SUPPORT_SEARCH_REQUIRED` | 351 | 低样本壶形回退。 | 是 |

## 不应从这张表推出的结论

“己方中线壳”“己方营内控制”不等于安全；“对方营内威胁”也不自动等于清壶。表只给离散局面类型。下一步策略树必须为每个类型另写：当前目标、希望转成的下一宏观状态、失败回退，并由本地 PhysX 验证具体路径与最后一壶反击。
