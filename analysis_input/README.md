# Unity 对齐与预测证据索引

更新：2026-10-03。主代码在 `../local_simulator/`；逆向原则见 `../AGENTS.md`。

## 当前预测与加速

- `prediction_driver_repair_20261003.md`：真实 FixedUpdate/Update 调度、摩擦随机消费及自然停止。
- `prediction_clock_validation_20261003.json`：原始 WAT 对照 2,580 帧，步数与时钟字段逐位比较。
- `prediction_optimization_manifest_20261003.json`：优化源文件/DLL 哈希、编译选项与证据路径。
- `prediction_optimization_comparison_20261003.json`：五场景所有 16 个对象逐步状态、随机消费、材质/活动/睡眠标记，16,135,300 字节一致。
- `prediction_acceleration_timing_20261003.json`：同进程交替运行参考/加速路径各十轮，最终结果一致，中位加速 1.60–2.12 倍。
- `prediction_optimization_tests_20261003.stdout.txt`：Windows CP39 的 49 项回归输出。

这些结果分别验证时钟计算、优化等价性和已有 Unity 采样窗口；不能推导未知随机种子、真实时间输入或未采样内部阶段全部一致。

## 历史对齐与局部窗口

- `local_partial_validation_20261003.md` 及同名目录的报告：本地已有采样的逐份核对范围与未覆盖项。
- `case12000_wall_repair_20261003.md`：墙碰撞回调、速度清零与停用。
- `case12009_cos_repair_20261003.md`：积分余弦计算。
- `case12004_stop_material_repair_20261002.md`：自然停止与摩擦恢复。
- `sample11009_cache_repair_20261002.md`：目标冰面持久缓存。
- `scheduler_functions_20261003/` 与 `pcm_functions_20261001/`：函数级 WAT 与提取清单；完整模块保留本地。

## 保存与复查

本目录 `.gitignore` 只纳入分析代码、文档、小型 JSON 报告和函数级反汇编。
超过 2 MB 的原始数值转储、完整 Unity 二进制、采样日志、临时执行文件和大型搜索函数仍在原路径，没有删除。
`repository_inventory_20261003.json` 保存整理前未跟踪文件的路径与体积盘点。
报告中的原始证据路径可能指向这些本地文件；克隆仓库可以运行随包测试夹具，重新审计完整 Unity 采样需取得报告指定的原始数据。

复现预测计时：从仓库根目录运行 CP39 Python 的 `-m local_simulator.examples.benchmark_prediction_acceleration`。
物理回归：`python -m unittest discover -s local_simulator/tests -p "test_*.py"`。
分析脚本开头记录输入路径/参数，运行前应检查所需本地 Unity 文件是否存在。
