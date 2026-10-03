# NWNHT 公开历史壶谱

这里的分析直接读取 `DCCourse/external_research/NWNHT_curling/curling-main/src/world_curling_ss.db`，不解析任何 PDF。

数据库含 2016–2019 年公开 CURLIT 壶谱的比赛、每局每手的叫球与评分、以及上游自动识别出的场上壶坐标。它适合用来复盘“高水平队在何种壶面下选择 guard/draw/take-out/blank”；不用于毫米级 PhysX 标定。

生成一场逐局复盘：

```powershell
python training_data\nwnht_curling\review_match.py --match-id 1076
```

`1076` 是 2017 世界男子锦标赛决赛：加拿大 Gushue 4–2 瑞典 Edin。输出会写到 `reviews/match_1076.md`。

报告每一手都分成三层：

1. 上游事实：出手队、投手、官方叫球、评分、出手后检测到的壶数及营内暂时得分；
2. 叫球对应的离散布局目标；
3. 一局结束后的保守归纳，并链接到项目已有的公开战术树。

壶位是公开项目的自动解析结果，重叠壶可能被漏检。因此它是复盘与归纳战术的证据，不应被误当作 Unity 的逐 tick 真值。

## Git 与本地生成资产

Git 保存研究源码、测试、复盘文档，以及 `causal_state_machine/artifacts/` 中三个默认运行资产：
状态分区 `nwnht_first_player_state_partition_v2.json`、语义计划 `nwnht_v2_universal_semantic_goal_mdp_v3_physx_admissible.json`、落点目标计划 `nwnht_v2_tactical_goal_outcome_value_v1.json`。
它们合计约 7 MB，供 `load_default()` 与固定历史局面回归使用；其余大型训练/估计中间产物留在本地并忽略。
原始公开数据库仍需按本文首段位置单独准备，克隆仓库不附带第三方数据库。

从仓库根目录验证：

```powershell
python -m unittest discover -s training_data/nwnht_curling/tests -p "test_*.py"
python -m unittest discover -s training_data/nwnht_curling/causal_state_machine/tests -p "test_*.py"
```
