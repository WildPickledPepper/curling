# 研究归档

这里存放不再参与当前交付路径、但对后续研究仍有参考价值的历史代码、模型和文档。

## legacy_proxy_training

这是本地严格 PhysX 模拟器完成前的旧训练路线。它依赖已经移除的
`fast_curling_env.py`、`paper_curling_sim.py` 和 `curling_sweep.py`，因此**不能直接运行**。

仍值得继承的思路：

- 以整盘壶位、壶次、先后手和当前得分构造局面状态；
- 先手与后手分策略；
- 按 early / middle / late / hammer 区分决策；
- 先选离散战术，再细化连续 `BESTSHOT` 参数；
- 使用多种对手、自对弈、交换先后手评测，以及候选模型晋级门槛。

不能复用为结论的部分：旧代理物理、旧模型权重、旧本地胜率，以及旧扫冰近似。它们只适合作为重建严格训练路线时的设计参考。

目录：

| 目录 | 内容 |
| --- | --- |
| `legacy_proxy_training/code/` | 旧训练、搜索、机器人与本地竞技场入口 |
| `legacy_proxy_training/tools/` | 旧评测与策略分析脚本 |
| `legacy_proxy_training/tests/` | 旧代理物理测试 |
| `legacy_proxy_training/models/` | 旧搜索蒸馏模型与 smoke 权重 |
| `legacy_proxy_training/docs/` | 旧训练方法、策略分析和代理物理说明 |

## unity_reverse

这是严格 PhysX 模拟器的 Unity 反推过程归档。源码、采样构型、约 10 GB 的
原始记录、日志、文档和历史测试均已移至
[unity_reverse/README.md](unity_reverse/README.md)。它们不参与当前运行；交付入口仍是
[`../local_simulator/`](../local_simulator/README.md)。
