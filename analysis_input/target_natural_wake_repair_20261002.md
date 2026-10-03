# 目标冰壶自然激活修复（2026-10-02）

第 1561 帧提前唤醒的分歧已修复。默认模拟和训练重放都删除了根据下一帧预测位置主动唤醒目标的行为，由 PhysX 的岛管理与活动刚体登记处理目标激活。

当前连续链条为：

`Reset 与自然休眠 → BESTSHOT → 自定义滑行 → 第1562帧目标岛激活与首次冰壶接触 → 碰撞回调 → 普通物理推进 → 双方最终休眠`

样本 11000、Windows CP39、同一记录摩擦输入下，主冰壶与目标冰壶每个完成帧的 Pxyz/Qxyzw/vxyz/wxyz，已从第 1 帧连续比较到第 2000 帧：**52,000 个 float32 原始字全部一致，没有已确认的新状态分叉**。主冰壶第 1603 帧休眠，目标第 1919 帧休眠，第 2000 帧包含双方静止后的状态。本次补采覆盖目标的整个释放后轨迹，不再以主冰壶一致代替双冰壶一致。

## 实际调用与修复依据

第 1561 帧，Unity 目标 BodySim 的活动数组索引为 `0xfffffffe`（-2），wake counter 为 0；求解入口目标线速度没有重力分量，帧结束状态仍保持不动。旧本地却调用 `wake_up()`，将其由睡眠转为活动，并产生提前一帧的微小速度与四元数推进。

新运行跟踪捕获第 1562 帧的真实路径：

`f71529 → f71557(targetBodySim, 1) → f71379(scene, targetBodySim)，返回后 f71555(targetBodySim)`

实际 call ID 为 253、254、255、256。`f71379` 和 `f71555` 的 parent 都是 `f71557`；`f71557` 的 parent 是岛任务 `f71529`。函数体反编译确认该任务从岛节点列表选择刚体；`f71557` 根据活动状态变化登记刚体并激活关联交互。采样中目标活动数组索引由 -2 变为 2，wake counter 仍为 0，之后该物理帧求解入口的目标 Y 速度才出现 `bdc8e8a7`（重力）。目标的显式唤醒函数 `f71572/f71573` 在该窗口没有调用。

`f71572` 的实际实现会将小于 0.4 的 wake counter 提高到 0.4，再标记岛节点。它与此次自然岛激活路径不同。因此不能通过把预测距离开关改成当前距离开关来宣称恢复了实际机制。

修复涉及 `local_simulator/unity_physx.py` 的普通模拟和 Python 训练循环；默认均不再额外调用目标 `wake_up()`。已有 `wake_target_at_current_pcm_shell=True` 保留为明确选择的人工唤醒诊断。旧原生批量循环内置距离唤醒，默认对齐路径不进入该循环；需要它的诊断路径仍明确选择人工唤醒。默认本来已因姿态写回使用 Python 步进。

## 验证与可靠性

[机器结果](target_natural_wake_verified_20261002.json) 与 [验证脚本](verify_target_natural_wake_20261002.py)：

```powershell
& 'C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe' analysis_input/verify_target_natural_wake_20261002.py
```

Unity observer 保留所有被包装函数的原始 Wasm 函数体。256 条 Reset core 记录、1562 条摩擦输入、1563 对密集 setter 数据、原始协议终点均与基线相同。本地带被动包装器的正常重放与无包装器重放，双方 3362 帧状态逐位相同；释放状态及原 1562 帧主冰壶状态也保持相同。

34 项测试通过：32 项原有检查，以及基于真实 Unity 第 1561–1563 帧记录的普通模拟、训练重放两项回归。测试从自然 Reset 开始推进，未注入修复帧的位姿、速度或求解输出。

关键证据：

- `unity_release_both_complete_activation_v2_20261002/logs/unity_runtime_probe_20261002_182449/events.jsonl`：完整双冰壶状态、实际活动登记调用与字段变化。
- `unity_release_both_complete_activation_v2_20261002/capture_manifest.json`：原始、插桩 Wasm 哈希及函数索引映射；`observer_source.js` 保存该次实际观察代码。
- `pcm_functions_20261001/f71529.wat`、`f71557.wat`、`f71379.wat`、`f71555.wat`、`f71572.wat`：原始二进制直接反编译。
- `native_release_natural_target_wake_20261002.json` 和 `native_natural_wake_unobserved_20261002.json`：默认生产路径双方状态及观测不变校验。
- `local_simulator/tests/fixtures/unity_target_activation_20261002.json`：原始 Unity 输入和完成帧输出，附来源哈希。

原始 Wasm SHA256 `cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81`；CP39 内核 SHA256 `7c31ced1773023e552391645e42040c9f3694d513805bc8b95ef0f8bc737bd38`。当前生产源码、插桩模块和全部证据哈希以机器结果为准。

未核对的后续环节是**协议坐标转换、字符串格式化和游戏状态切换的内部计算**。本记录确认这个样本的双冰壶物理状态轨迹；不据此宣称所有算术中间值、内部 RNG 状态、其他样本和 ABI 也已对齐。

早期无效目录 `unity_release_target_wake_internal_20261002`、`unity_release_both_complete_activation_20261002` 未通过数据数量校验，未用于结论；其日志保留。完整补采增大了导出等待时间，数值路径未改。
