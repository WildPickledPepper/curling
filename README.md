# Curling AI Workspace

当前可交付的本地物理模拟器在 [local_simulator/README.md](local_simulator/README.md)。它包含严格 PhysX 后端、固定局面策略树自对弈样例、已锁定的运行时依赖，以及复现验证所需的关键物理资产。

## 目录说明

| 目录 | 是否当前使用 | 用途 |
| --- | --- | --- |
| `local_simulator/` | 是 | 当前交付：严格本地模拟器、运行时、样例与测试。 |
| `tools/protocol/`、`AIRobot.py` | 是 | 与数字冰壶服务通信的课程机器人基类。 |
| `tacticslib/`、`notebooks/` | 是 | 后续研究训练策略时要参考的课程战术与教学实现。 |
| `数字冰壶单机版_win/` | 按需 | Unity 单机版；仅在需要重新采样或对照时使用。 |
| `references/`、`images/` | 保留 | 课程资料与图像资产。 |
| `research_archive/` | 否（研究留档） | 历史代码、模型、反推证据与文档；不属于当前运行路径。 |

## 归档内容

- [research_archive/unity_reverse/](research_archive/unity_reverse/README.md)：反推严格本地模拟器时的源码、采样计划、原始 Unity 数据/日志、实验文档和测试。约 10 GB，仅在需要重新审计或继续反推时使用。
- [research_archive/legacy_proxy_training/](research_archive/legacy_proxy_training/README.md)：严格模拟器出现前的粗糙代理训练代码、旧模型与旧报告。代码依赖已移除的旧代理，不能直接运行；其中的训练思路可作为重建 PPO/MCTS 训练管线的参考。

根目录不再提供旧训练脚本或旧物理代理的运行入口。新训练应直接基于 `local_simulator/` 进行。
