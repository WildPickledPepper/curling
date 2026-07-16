# Unity 反推归档

这里保存“严格本地模拟器如何从 Unity 行为反推出来”的完整研究证据。它不参与日常训练或交付运行；当前可运行实现位于 [../../local_simulator/](../../local_simulator/README.md)。

| 目录 | 内容 |
| --- | --- |
| `source/reverse/` | 反推、回放、碰撞审计与 PhysX 资产分析脚本。 |
| `source/calibration/` | Unity 浏览器探针、采样器、会话控制与拟合脚本。 |
| `source/analysis/` | 反推期间的分析工具。 |
| `evidence/config/` | 采样构型、批次计划和实验配置。 |
| `evidence/data/` | Unity 采样结果、校准数据与统计结果。 |
| `evidence/log/` | 浏览器探针、会话握手、逐 tick 事件与运行日志。 |
| `docs/` | 反推账本、碰撞对齐报告与已废弃文档。 |
| `tests/` | 仅用于验证反推结论的历史测试。 |
| `compatibility_shims/` | 旧模块名兼容入口；当前代码请改从 `local_simulator` 导入。 |

`local_simulator/runtime_support/` 内保留了一份运行所需的最小反推方程源码；`local_simulator/assets/` 内保留严格 PhysX 回放必需的冰面网格和 runtime hull 证据。因此可交付模拟器不依赖本目录。
