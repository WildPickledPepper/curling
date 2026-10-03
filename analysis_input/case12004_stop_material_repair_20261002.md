# 12004 自然停止分支正式修复（2026-10-02）

正式模拟器已补上自然停止时的材质恢复。12004 从出手到第 4000 步，两只冰壶的 P/Q/v/w 全部逐字节一致；原第 3169–3208 步的 40 个不同帧消失。此前通过的另外五次回放保持不变。六次回放、五种出手条件、21,000 个完成步及六次出手状态，共 2,184,624 字节全部一致，并覆盖休眠。

## 修改及内部依据

`local_simulator/unity_physx.py` 的 `_restore_unity_natural_stop_material` 实现原始 `DCP.Update / f61097` 的物理相关分支：有效滑行出手，按原 f32 运算顺序计算距 controller 原点的三维距离 > 1.0、三维速度平方和 < 1e-6，再按实际 setter 顺序恢复 dynamic/static 摩擦为 0.6/0.6，结束自定义滑行控制。

实际父调用也已补采到：`case12004_stop_controller_unity` 记录中，两次 `f32511/f32512` 的 `parentCallId` 均为 162，其父函数是 `f61097`。该调用入口的 controller +220/+224/+228 原点为 `(-96.85420227050781,14.43239974975586,54.174400329589844)`；原始 `f61095 Start` 从 blue0 初始 Transform 缓存这三个字段。BESTSHOT 横向偏移改变出手位置，不改变此缓存原点。

停止检查在自定义 setter 批次转入普通物理推进的边界执行；`step_custom_sliding` 和训练逐步循环在 `_simulate_custom_sliding_step` 中保持批次控制。不能每次 FixedUpdate 都检查：12004 从第 2506 步起已低于阈值，但目标实际继续执行 setter 到第 3168 步，然后才进入 Update。修复没有硬编码这个帧号，没有按输入流耗尽直接恢复，也没有注入采到的材质写入。Reset 和失活会清除旧出手上下文。

此 Scene API 的调用边界由调用方提供；这次没有新增 Unity 渲染时钟调度器、协议状态机或所有 controller 的完整 Update。字节一致结论限于已比较的出手及物理状态轨迹。

## 验证

- 当前正式代码使用普通回放驱动，不使用前一轮诊断驱动：六次完整回放全部通过。12004 第 3169 步五轮静态求解的共同约束头部、法向行、摩擦行计算字段、求解体输入及输出全部一致。
- 原有五次回放的出手及所比较完成状态与修复前完全相同。
- 新增固定 Unity 真值回归：出手及全部 4000 步逐字节比较，检查第 2506–3168 步没有提前恢复、第 3169 步实际接触系数为 0.012/0.012，并检查完整三维速度及距离条件。
- Windows CP39：`python -m unittest discover -s local_simulator/tests`，41 项通过。

复查完整生产回放：`python analysis_input/verify_case12004_stop_repair_20261002.py`。报告：`multi_case_validation_20261002/stop_material_repair_regression/report.json`。正式代码 SHA-256：`4073a71114da9f877784df5704a1e66e855b6119bace9eae239147c72ff52b83`。native 模块保持 `7c31ced1773023e552391645e42040c9f3694d513805bc8b95ef0f8bc737bd38`。

补采父调用的记录没有取得所请求的五个尾段边界，采集驱动明确报失败；只保留了第 3167 完成边界、第 3167/3168 求解退出、两次 setter 及父函数入口参数。该记录的完整滑行 setter/getter/pose、摩擦输入、原始函数体和最终协议结果已与未修改 Wasm 对照一致，但没有用于证明未采到的尾段。完整 4000 步真值与五轮求解比较沿用前一轮独立、完整、已验证未改变计算结果的采样；这一区别也写入验证报告。

前一轮定位与诊断回放保留在 `case12004_stop_material_cause_20261002.md` 及 `case12004_stop_material_cause_verified.json`，不覆盖其修复前事实。
