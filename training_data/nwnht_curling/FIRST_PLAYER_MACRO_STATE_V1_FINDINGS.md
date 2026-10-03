# 先手宏观状态机 v1：当前候选部署结构

结论：当前离散层采用 47 个状态，而不是旧版 43/51 个未收敛平面簇。

状态为 `FIRST_Kk_MACRO`：先手第 `k=1..8` 次出手加一个可解释宏观壶形。它不读取比分、局号、胜负或控分意图；本地规则由运行时根据 `k` 验收。

| K | 节点数 | 当前可出现的宏观壶形 |
| --- | ---: | --- |
| K1 | 1 | `EMPTY` |
| K2 | 5 | `EMPTY`、`GUARD_EXCHANGE`、`OPPONENT_HOUSE_THREAT`、`OWN_HOUSE_CONTROL`、`LOW_SUPPORT_SEARCH_REQUIRED` |
| K3 | 6 | `GUARD_EXCHANGE`、`OPPONENT_CENTRE_SHELL`、`OWN_CENTRE_SHELL`、`OPPONENT_HOUSE_THREAT`、`OWN_HOUSE_CONTROL`、`LOW_SUPPORT_SEARCH_REQUIRED` |
| K4–K8 | 各 7 | `CROWDED_HOUSE_SEARCH_REQUIRED`、`GUARD_EXCHANGE`、`OPPONENT_CENTRE_SHELL`、`OWN_CENTRE_SHELL`、`OPPONENT_HOUSE_THREAT`、`OWN_HOUSE_CONTROL`、`LOW_SUPPORT_SEARCH_REQUIRED` |

总计：`1 + 5 + 6 + 5 × 7 = 47` 个节点，7,675 条历史两手转移边。

## 运行时含义

- `EMPTY`、`GUARD_EXCHANGE`、`OPPONENT_HOUSE_THREAT`、`OWN_HOUSE_CONTROL`：离散策略树可以直接给出宏观战术目标。
- `OPPONENT_CENTRE_SHELL`、`OWN_CENTRE_SHELL`、`CROWDED_HOUSE_SEARCH_REQUIRED`：离散层只说明结构；具体穿门、撞击链、raise/runback 由严格 PhysX 搜索。
- `LOW_SUPPORT_SEARCH_REQUIRED`：同一个 `Kk × 原始宏观形态` 在公开数据中少于 250 条，被合并为回退状态；该回退入口本身可以低于 250 条，但不从稀少样本学习确定战术。

## 数据支持

- 四人赛完整且壶色归属无冲突的局：10,873。
- 每局八个先手决策：86,984 条样本。
- K8 中高密度营内缠斗为 4,389 条、对方营内威胁为 3,655 条，说明把末手前复杂壶面单独交给 PhysX 不是罕见回退，而是主路径之一。

这仍不是“已证明最优”的策略树：每个宏观节点的目标、失败回退、本地规则合法性和末手反击韧性还需接严格 PhysX 验证。
