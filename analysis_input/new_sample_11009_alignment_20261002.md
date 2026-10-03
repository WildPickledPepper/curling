# 新样例 11009：出手坐标已暴露分叉

后续状态：该出手坐标差异已修复，实际运行入口核验为 f61066；下文初步引用的 f60092 是同类函数，不能作为此样例的实际入口证据。当前结果见 [出手坐标修复记录](bestshot_offset_repair_20261002.md)，最早剩余状态差异在第 1383 个物理步的目标冰壶。

2026-10-02，用全新 Unity 页面跑另一组输入：`BESTSHOT 3.4 0.2 1.57`，主冰壶 0，目标冰壶 11，目标协议坐标 `(2.655, 6.8)`。没有前序投壶历史，没有注入位姿、四元数、速度或求解器输出。Unity 使用自然随机数；模拟器重放捕获到的 1383 个真实摩擦随机返回值。

**没有完美对齐。最早观察到的状态分叉就在 BESTSHOT 出手位置设置，尚未进入第一帧物理步。**

| 出手时主冰壶原生 `position.z` | float32 位 | 数值 |
| --- | --- | --- |
| Unity | `0x4257e5c9` | 53.97439956665039 |
| 当前模拟器 | `0x4257e5ca` | 53.974403381347656 |

相差 1 ULP，约 `3.814697265625e-6`。出手时两只冰壶的 P/Q/v/w 共 26 个 float32 字，25 个相同，仅该位置字不同；目标冰壶完整 13 字与模拟器自然 Reset 后的状态相同。第一帧完成状态已经带着这个差异，连续比较的 3000 帧均有差异。不能用后面碰撞、终点误差来替代这个更早分叉。

实际反编译链条在 `pcm_functions_20261001/f60092.wat:319` 附近：`f32544` 读取 Rigidbody 位置，将 Z 的 `f32.load` 与参数 `p2` 横向偏移做 `f32.sub`，写回位置向量，再调用 `f32546`。当前模拟器 `start_bestshot` 则经 `local_initial_state` 生成协议坐标，再计算 `float32(UNITY_NATIVE_ORIGIN_Z - release.x)`。两条计算路径不同。此轮未修改生产实现；要修复时应继续采样位置 getter 返回值及偏移解析结果，按实际输入与 f32 运算顺序实现。

本次也运行了原始 Wasm 对照：相同计划、相同实际摩擦返回值，1384 组 setter 前后采样的位姿、getter 输出和 setter 输入相同，最终协议位置相同。原始函数体与插桩副本逐字节核验通过。这个对照验证了已观察轨迹及结果没有被本轮插桩改变，不证明内部 RNG 状态相同。

原始 Wasm SHA256：`cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81`。

生产 `unity_physx.py` SHA256：`e20aaccc1f641fe7236108807dfc35e2d28ccc2ffbb8048f7d09400e071ddbb0`。CP39 内核 SHA256：`7c31ced1773023e552391645e42040c9f3694d513805bc8b95ef0f8bc737bd38`。

证据与复现：

- `new_sample_11009_plan_20261002.json`：输入。
- `unity_new_sample_11009_capture_20261002/logs/unity_runtime_probe_20261002_190058/events.jsonl`：Unity 实际运行数据，出手最早状态为 `normalizeCandidate.121708` enter，随后 `DCP.FixedUpdate.boundary` solverSerial 0；物理完成边界 1–3000。
- `unity_new_sample_11009_control_20261002/logs/unity_runtime_probe_20261002_190444/events.jsonl`：原始 Wasm 对照。
- `native_new_sample_11009_20261002.json`：模拟器正常构造、Reset、出手和 3000 步原始状态。
- `new_sample_11009_verified_20261002.json`：逐位差异、版本与全部证据文件哈希。
- `sample_new_case_20261002.py` 与 `verify_new_sample_11009_20261002.py`：采样和核验脚本。

本结论是新样例最早已观察到的出手状态差异。此轮没有逐位采样所有更早的解析、构造、cooking、Reset 内部操作，不能据此宣称那些内部操作全部一致。旧样例 11000 的通过结果仍限于旧样例；它的横向偏移为 0，没有检验本次非零偏移路径。
