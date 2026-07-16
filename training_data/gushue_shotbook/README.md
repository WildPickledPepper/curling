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
