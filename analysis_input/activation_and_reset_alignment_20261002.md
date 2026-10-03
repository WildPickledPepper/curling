# 登记与 Reset 逐位修复（2026-10-02）

**历史阶段记录：**本页的第 6 步分歧已修复。最新见 [第一次 Reset 完整逐位闭合](reset_complete_alignment_20261002.md)：42 个求解器出口及自然休眠逐位通过，已推进到后续 BESTSHOT 释放位姿。

本轮按实测调用修改了生产后端。`Sc::RigidSim` 的 40 次正式壶登记输入，共 **1,400 个数值字逐位一致**；全新场景第一次 Reset 的 16 个位置输入，共 **48 个数值字一致**。该目标壶前 5 个物理步的 P/Q/线速度/角速度输出，共 **65 个数值字一致**。**第 6 个物理步的求解输出仍有差异，整条链未完成。**

这些结论分别验证具体边界，不能用它们证明所有启动函数、质量烹饪中间值、接触缓存都已一致，也不能把此前 11005 的活动壶局部序列当作全场景连续前缀。当前第 6 步是这次完整 Reset 输出采样的首个分歧；内部接触准备/缓存是否更早分歧，须继续采样。

## 实际调用与修复依据

Unity 原始 wasm SHA256 为 `cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81`。共同登记边界为 Unity `f71726` / 本地 CP39 模块 RVA `0x214bd0`，比较 `ScRigidCore` 参数 2 的 35 个数值字；不同 ABI 的指针、填充和保留标志不混作数值对齐。

- 首次登记时，Unity 使用默认 P/Q、单位逆惯量和角速度上限 3.14。此前本地提前写入世界位置、倾角、计算惯量和上限 100。现在先登记，再同步属性，后续上限按实测恢复为 20。
- 反编译和运行时共同确认 `f73018` 更换 PhysX 刚体。单枪样本 11000 中，首次目标启用 callId 460 → 登记 callId 466；首次释放 callId 492 → 登记 callId 495，组件保存的 actor 指针均发生变化。此前本地复用旧 actor，现在启用时创建新 actor，保留组件的 Transform，恢复默认质量/手动惯量及已执行 Start 的约束。
- 通过 Reset 前 16 次 Transform 写入、原生 GameObject 的组件成员、Rigidbody 组件与首次 actor 的对应关系，直接恢复了协议壶号与初始登记顺序。该映射及首次 Reset 前的组件约束存在 `local_simulator/assets/unity_startup_body_roster.json`，没有从终点推测壶号或约束。
- Reset 的非空位置实测写入高度为 `14.43239974975586`，空槽写入固定停放位置 `(-96.85420227050781,14.43239974975586,54.174400329589844)`。Unity 接着执行重力积分、落冰接触并自然休眠。本地此前直接放在贴冰高度 `14.419784545898438` 并强制休眠；现在恢复实测放置输入，推进正常 PhysX 步直到其自然休眠，不注入实测休眠姿态。

## 验证和剩余差异

[登记逐位报告](activation_registration_fixed_20261002.json)覆盖 16 次首次登记、24 次重新启用，1,400/1,400。原生被动采样共 116 次调用，无丢失、无未完成调用。12 枪原有端点结果与汇总保持相同；11005 的 1,023 次活动壶 setter 及 1,022 个 tick 的输入/输出保持相同。恢复 Reset 下落后，被撞壶的微小姿态和速度发生变化，因此没有宣称整份场景状态回归不变。

[Reset 逐位报告](reset_settling_verified_20261002.json)使用全新生产场景，不注入 yaw、quaternion 或摩擦记录。它验证 48 个位置输入、前 5 步 65 个状态输出字，并记录第 6 步 Q、线速度和角速度的两侧原始位值。休眠及后续帧仍未闭合。下一处需要直接比较第 6 步接触准备、PCM/摩擦缓存、约束输入和求解中间值；尚未确认具体内部指令差异。

Unity 新插桩使用逐字节不变的原始函数体转发；两份单枪采样的 1,562 次摩擦记录与原基线相同，终局字段相同。测试共 27 项通过，包含独立实测 fixture 的首次登记与 Reset 前 5 步测试。此前不完整的批量 Reset 导出没有用于通过判定。

```powershell
python analysis_input/verify_activation_registration_fixed_20261002.py
python analysis_input/verify_reset_settling_fixed_20261002.py
& 'C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python39_64/python.exe' analysis_input/sample_reset_settling_fixed_20261002.py
& 'C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python39_64/python.exe' -m unittest local_simulator.tests.test_unity_stone_registration local_simulator.tests.test_unity_reset_settling local_simulator.tests.test_unity_shape_refresh local_simulator.tests.test_strict_simulator local_simulator.tests.test_recovered_stone_mass local_simulator.tests.test_recovered_transform_scale
```

具体事件路径、函数索引、调用编号、字段偏移、程序与证据哈希均在对应 JSON 报告及 roster 资产中。
