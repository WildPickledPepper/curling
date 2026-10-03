# 释放后的首个已确认分叉：第二帧线速度竖直分量（2026-10-02）

本报告保存修复前检查。第二帧差异现已修复，连续状态比较通过前 525 帧；新边界及验证见 [竖直速度修复记录](release_vertical_repair_20261002.md)。

样本 11000，第一次 Reset 后直接使用当前默认生产路径执行 `BESTSHOT 3.4 0 0`。没有注入 Unity 的释放 Q/P、速度输出或滑行结果。两侧使用同一组已记录的摩擦随机输入；这一控制不代表随机数发生器状态已经闭合。

当前连续状态比较已推进为：

`Reset 放置 → 42 个求解出口 → 自然休眠 → 释放 P/Q、线速度/角速度写入 → 第一帧滑行速度写入 → 第一帧物理求解与 fetch/位姿写回 → 第二帧线速度构造/写入首次不同`

前段依据 [Reset 完整记录](reset_complete_alignment_20261002.md)。本次追加比较释放及第一帧两个 setter 前后各 13 个 P/Q/线速度/角速度原始字，以及第一帧 solver 出口和第二帧 setter 入口的 13 个字，均一致。这里的逐位结论对应这些连续状态边界；未宣称滑行公式中每个 f64 算术中间值都已逐指令审计。

## 原始运行证据

第一枪协议 release serial=2，密集 ordinal=1 是释放时角速度 setter，ordinal=2 是第一帧滑行，ordinal=3 是第二帧滑行。线速度 setter 发生在角速度 setter 之前，因此它的原始 row.ordinal 比对应密集 ordinal 小一；不能直接把两种编号混用。

第二帧的 Unity `f73034` 调用 ID=115（密集 ordinal=3）：

- setter 前：两侧 13 个状态字全部一致，竖直速度都是 `0xbdc8e8a7`，即 `-0.09809999912977219`。
- Unity 线速度输入：`[0x40590b4d, 0x00000000, 0xb5ce9e9d]`。
- Native 线速度输入：`[0x40590b4d, 0xbdc8e8a7, 0xb5ce9e9d]`。
- 只差 native 世界 Y 分量。setter 后仍只有这一个状态字不同。此后高度和物理轨迹的差异是后续传播，不属于更早分叉。

源码依据来自同一目标原始二进制：表 11105 对应 `DCP_HumanVSAI.FixedUpdate` 的 `f60124`。函数正文 byte offset=837 包含 `local.get 1; i32.const 0; i32.store offset=124`，明确把构造出的速度向量中间分量写成正零；随后复制到参数向量，正文 byte offset=874 调用 `f32521`。实际链为 `f60124 → f32521 → 表129352/f82501 → f73034`。`f73034` 读取这一输入后调用实际刚体 setter。

本地 `step_custom_sliding` 则执行 `0.0 if self.custom_sliding_zero_vertical_setter else float(current["vz"])`，而默认 `custom_sliding_zero_vertical_setter=False`，沿用上一帧竖直速度。第一帧的原值本来就是正零，所以该差异直到第二帧才显现。本次只检查并记录原因，未修改生产实现。

## 观察器校验与版本

- Unity 原始 wasm SHA256：`cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81`。
- 本次插桩 wasm SHA256：`91851f5bd2f507d0c397e98c611784307ca805b31bc7689c6cfaba317390bbb6`。
- Native CP39 SHA256：`7c31ced1773023e552391645e42040c9f3694d513805bc8b95ef0f8bc737bd38`。
- 51 个选中函数的实际原始正文逐字节保留；其余函数正文也未改变。probe 只读取 setter 前后内存。
- 与原始基线相比，256 个 Reset core frame、1,562 次摩擦输入记录和终局物理字段全部一致。
- Native 内部追踪与未开启追踪版本的释放状态、全部 setter 记录和前四帧输出完全一致。
- 第一份释放采样因窗口条件提前排除了启动注册，缺少 Reset core frame；没有用它证明完整观察器等价。补采修正只读窗口，完整校验通过。

## 复查和证据

运行 `python analysis_input/verify_first_release_chain_20261002.py`。

- [逐位结果、函数字节偏移及全部证据 SHA256](first_release_chain_verified_20261002.json)。
- [完整 Unity 运行记录](unity_first_release_chain_complete_capture_20261002/logs/unity_runtime_probe_20261002_162622/events.jsonl)。
- [Native 原始 setter 与内部求解记录](native_first_release_chain_traced_20261002.json)。
- [Native 未开启内部追踪记录](native_first_release_chain_untraced_20261002.json)。
- [FixedUpdate 反编译](pcm_functions_20261001/f60124.wat)、[托管桥接](pcm_functions_20261001/f82501.wat)、[原生入口](pcm_functions_20261001/f73034.wat)。

结论限于当前样本、默认配置与 Windows CP39。第二帧以后的状态不再作为连续闭合段；后续碰撞及其他出手参数仍需修复这一差异后继续串行比较。
