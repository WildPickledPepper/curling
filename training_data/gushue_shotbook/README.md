# Team Gushue 逐手壶谱原始库

这不是人工编写的战术案例集，而是 World Curling / CurlIT 发布的比赛原始记录。
每张 `Game - Shot by Shot` 页面都按投壶顺序给出当时的壶位图、比分变化、投壶类型、旋转方向和评分。它是把“真实壶面”映射为战术局面的证据底座。

## 已下载范围

| 赛事 | Team Gushue 身份 | 原始内容 |
| --- | --- | --- |
| 2022 世界男子锦标赛 | 加拿大 | 官方完整 Results Book + 对局逐手图 |
| 2023 世界男子锦标赛 | 加拿大 | 官方完整 Results Book + 对局逐手图 |
| 2024 世界男子锦标赛 | 加拿大 | 官方完整 Results Book + 对局逐手图 |

`source_results_books/` 保存官方完整 PDF；不要修改。

`gushue_games/` 是从完整 PDF 中无损切出的 Team Gushue 单场逐手图。一个 PDF 对应一场比赛，且只含该场的 `Game - Shot by Shot` 页。

`gushue_game_index.csv` 是机器可读索引：年份、对手、淘汰/循环赛阶段、原始页码和切出文件名都在这里。

`extracted_text/` 是完整图册的文本层。它包含每手显示的 `Draw`、`Guard`、`Take-out`、`Hit and Roll`、`Raise`、`Clearing` 等记录，便于先筛选，再回看对应的壶位图。

## 坐标提取

`extract_stone_coordinates.py` 直接从 PDF 里取出每个小盘面的内嵌图，不对整页做 OCR。
一页是一个 End，通常有 16 个小盘面；每个小盘面是一次投壶结束后的场上状态。

- 实心红、黄圆：当前仍在场的壶；黄壶内部的蓝色十字是该黄壶的绘制组成，**不能据此删壶**；
- 空心红、黄圆：前一位置残影，**不算在场壶**；
- 小盘面最上、最下边缘的成排小壶：尚未投出的计数，**不算在场壶**；
- 壶中心贴近上方 back line 仍视为在场；代码只剔除顶边未投壶计数，不把 back-line 壶误删。

代码不会只看颜色：必须是实心圆面积占自身包围框至少 50% 的色块；这会剔除内部白色、只画外圈的“上一位置残影”。
- 官方图册的 End 视角上下交替：壶在上方的页直接读取，壶在下方的页先作 **180° 旋转**；
  所有输出最终都统一为“壶在上方”的坐标系。原点是按钮，`+x` 向统一视角右侧，`+y` 向前方守壶/起滑线方向；单位为米。

运行：

```powershell
python training_data\gushue_shotbook\extract_stone_coordinates.py
```

输出在 `coordinates/gushue_stone_states.jsonl`：一行是一手后的完整壶面，保留来源比赛、End、手数、红黄队伍、原始 PDF 页码和每颗壶的图像/米制坐标。`coordinates/extraction_audit.json` 给出总数和过滤规则。

每一手还会检查“活壶数相对上一手不能净增超过一颗”。少数图例相互贴近、难以自动区分的状态不删除，但会标成 `quality_status=needs_manual_review`，并写入 `coordinates/manual_review_states.json`。自动归纳战术树时只使用 `auto_pass` 状态。

还可运行 `python training_data\gushue_shotbook\render_coordinate_qa.py` 生成原图叠图抽检页：绿色十字必须落在每颗被保留的实心壶中心，不能落在空心残影或蓝叉壶上。

日常验收无需人工逐图看：运行 `python training_data\gushue_shotbook\validate_coordinate_pixels.py`。它会重新从官方 PDF 抽出小盘面，并逐壶比较保存的原始连通像素 SHA-256；`pixel_component_difference=0` 才算提取记录与原图像素完全一致。这个检查验证的是“坐标记录没有偏离原图”；战术是否合理仍由后续的状态树和 PhysX 反击验证。

该坐标系是“统一后的官方图表坐标系”，尚未硬绑定本项目 PhysX 的场地原点；策略层可以直接用相对按钮的壶型，真正调用 PhysX 时再由适配层统一转换。

## 后续讨论只读的逐手状态表

运行：

```powershell
python training_data\gushue_shotbook\build_structured_shotbook.py
```

它把已经提取的坐标与官方逐手文字合并为两个不需要再打开 PDF 的文件：

- `coordinates/gushue_structured_shots.jsonl`：每一手的投壶方、投手、官方叫球、旋转方向、完成度、是否后手、当局前后比分、出手后所有壶的坐标和分区，以及双方壶数变化。
- `coordinates/gushue_structured_ends.jsonl`：每局的先后手、实际下一局后手、该局得分和累计比分，以及是否提前结束。
- `coordinates/gushue_structured_games.jsonl`：每场比赛的最终比分、胜方和按局汇总的进程。

默认会剔除被物理连续性检查标成 `needs_manual_review` 的状态；原始坐标仍保留在 `gushue_stone_states.jsonl` 供追溯。若确实要研究这些原图状态，才显式加 `--include-review-states`。剔除点之后的第一条记录会把 `transition_observed_from_immediately_previous_shot=false`，且不计算壶数变化，避免跨过缺口伪造一次“单手变化”。

这些表包含战术复盘所需的公开信息。它们不声称恢复 PDF 没有记录的内容，例如真实初速度、扫冰输入、逐 tick 摩擦、壶的 yaw 或每次碰撞的精确先后次序。

## 安全重建（不覆盖现有结果）

`rebuild_coordinates_parallel.py` 会按比赛并行提取，并默认写入 `coordinates/recovery_candidate.jsonl`，不覆盖当前 `gushue_stone_states.jsonl`。先用小样本测速，例如：

```powershell
python training_data\gushue_shotbook\rebuild_coordinates_parallel.py --limit-games 2 --workers 2
```

只有候选文件通过像素和物理连续性核验后，才应人工确认替换正式结果。

在任何全量候选重建前，先运行规则回归测试：

```powershell
python training_data\gushue_shotbook\validate_extraction_rules.py
```

该测试直接读取两处曾误判的官方小盘面，要求蓝色标记的有效黄壶被保留，并要求局面壶数分别连续为 `1→2→3` 和 `0→1→2`。失败时不得启动或采纳全量候选。

## 重新生成索引和单场文件

在 `DCCourse` 根目录执行：

```powershell
python training_data\gushue_shotbook\build_gushue_game_index.py
```

已存在 `extracted_text/` 时，脚本只需要 `pypdf`；若文本层缺失，才需要 Poppler 的
`pdftotext` 重新生成。当前环境已验证可运行。

## 这批资料怎样进入策略系统

不要直接从图册抄一个固定坐标。每条学习样本应是：

```text
出手前壶面 + 比分/局数/先后手/当前第几壶
    → Team Gushue 实际这一手的类型和出手后壶面
    → 由人工或规则标注为“争两分、转两翼、清中、处理掩护壶、偷分、blank”等局面
```

连续的 `v/h/w` 仍由本项目路径求解器处理；这个壶谱库只提供经过真实高水平比赛验证的离散布局目标和分支。

## 来源

- [2022 World Men's Championship Results Book](https://curlit.com/PDF/WMCC2022_ResultsBook.pdf)
- [2023 World Men's Championship Results Book](https://curlit.com/PDF/WMCC2023_ResultsBook.pdf)
- [2024 World Men's Championship Results Book](https://curlit.com/PDF/WMCC2024_ResultsBook.pdf)

文件保留来源链接和原始页码，便于随时回到官方资料核验，不把推断误写成 Team Gushue 的私有战术。
