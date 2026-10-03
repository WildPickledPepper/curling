# 第一次 Reset 完整逐位闭合（2026-10-02）

本报告保存 Reset 闭合时的证据。后续释放与 BVH34 修复已继续推进，最新主石头连续状态边界到第 1561 帧结束，见 [BVH34 修复记录](release_bvh34_repair_20261002.md)。

当前结果：样本 11000 从 Reset 放置进入物理计算，**42 个求解器出口的 P/Q/线速度/角速度，共 546 个原始浮点字逐位一致**；第 42 步自然休眠后的位姿和零速度也一致。随后默认 BESTSHOT 的释放 P/Q 共 7 个字一致。释放后的 setter、第一滑行/物理步仍未完成串行逐位检查，不把已有局部回放当作这一段的闭合证明。

复查：`python analysis_input/verify_reset_complete_alignment_20261002.py`。完整结果见 [reset_complete_alignment_verified_20261002.json](reset_complete_alignment_verified_20261002.json)。旧 [摩擦缓存报告](reset_friction_cache_alignment_20261002.md)是本轮修复前的历史快照。

## 缓存分叉的实际调用链

定点内存写入观察记录：`f71272` 每步写回一个摩擦 patch；下一步 `f73070 -> f72606(rawPose, autowake=0) -> f71596 -> f71729 -> f71632` 清除 work-unit 的缓存。`f71632` 在 +42 写 count=0，并用 +32 的 i64 store 同时清掉 +36 的 frictionData 指针。第 2～8 步的调用链、清除写入及原始输入均有运行记录。f72606 输入的 7 个 P/Q 原始字与上一步求解器出口相同。

本地此前仅在归一化改变 Q 时调用 pose setter，因此数值未变时漏掉了接触交互更新。本轮改为每步调用实际 PhysX `setGlobalPose(rawPose, false)`，由原生实现归一化一次并清缓存。没有直接改写缓存字段。旧 Python 绑定只暴露默认 autowake=True，新增 [native_pose_writeback.py](../local_simulator/native_pose_writeback.py)通过已验证的 RigidDynamic vtable slot 19 调用缺失的参数，检查模块 SHA256 和实际函数入口。生产运行不依赖 Frida。

Native 对应链为 `0x1acb60 -> 0x1c3eb0 -> 0x215700 -> 0x2148d0 -> 0x240540 -> 0x2115d0`。最后一个函数清除 work-unit +0x48 的 frictionData 和 +0x52 的 count。修复后 actual prepare 入口 `0xdcf30` 的 descriptor +160/+168 在八步中均是 0/0。前八步约束头、全部 normal/friction 算术字段，以及五轮静态求解的每次入口/出口 delta 均逐位一致。

## 第 7 步非零极小数的实际计算

缓存修复后首次状态差异是角速度 X：Unity `0x8001b2e2`，本地 0。前面的约束与五轮求解一致。Native `0x2049c7` 入口采到的 bodyData 和 motionBody 原始字，代入 `0x204bdd～0x204c26` 实际矩阵乘加顺序，得到同一个 `0x8001b2e2`。其中角速度 Y 与 sqrtInvInertia 的乘积成为 subnormal；没有加入经验值。

原生入口的只读 STMXCSR 观察得到 `0x9fc0/0x9ff0`，FTZ/DAZ 两位都开启。反汇编显示 FPU guard 明确将 `0x9fc0` 写入保存槽，再 LDMXCSR。Unity 原始运行内存保留上述 subnormal。缺少 PhysX 原始构建目录，因此对已知 CP39 二进制中的 **51 处已解码 guard immediate** 做可复查修复：`0x9fc0 -> 0x1f80`，保留异常屏蔽及舍入模式，关闭 FTZ/DAZ；其他所有字节不变。修复后的运行时观察确认 FTZ/DAZ 关闭，42 步输出随之逐位通过。

- 修复脚本：[patch_physx_gradual_underflow_20261002.py](patch_physx_gradual_underflow_20261002.py)。
- 每处指令地址、原始字节与哈希：[native_gradual_underflow_patch_20261002.json](native_gradual_underflow_patch_20261002.json)。
- 原始内核备份：[native_kernel_before_gradual_underflow_20261002.pyd](native_kernel_before_gradual_underflow_20261002.pyd)。
- Unity wasm SHA256：`cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81`。
- 原 native CP39：`2564abec4fa3f358e67259b105c4b88d49eae28510611c8a0e2f11b7671888df`。
- 当前 native CP39：`7c31ced1773023e552391645e42040c9f3694d513805bc8b95ef0f8bc737bd38`。

## 休眠边界与下一段

第 42 步 Unity 的 solverSetupSolve.exit 尚有微小速度和当步 Q；fetch 的休眠处理随后清速度并保留上一帧 Q。Native Scene.simulate 返回值已过 fetch。最初将这两个不同边界直接比较，会报一个假分歧。现将 Native solver-setup 的出口数据与 Unity solver 出口比较，再将 Native fetch 后状态与 Unity 第 43 个 idle 入口比较，两处都逐位一致；不是强制 put_to_sleep，也未调整休眠阈值。

继续到 BESTSHOT 时发现默认仍用已静止的高度和 double 坐标转换，释放 X 差一个 ULP，Y 差约 12.6 mm。启用已有、来自实际释放记录的 native release pose 路径后，不注入 Unity Q/pose 的同一生产场景也得到完全相同的释放 P/Q。当前闭合边界是**第一次 Reset 自然休眠与接下来的释放位姿**，下一处未闭合的是释放 setter 及第一滑行/物理步。

## 验证范围

三份新增有效 Unity 插桩的全部 256 个 Reset core frame、1,562 次摩擦记录及终局物理字段均与原始基线一致。定点 store 保持类型、地址和值语义。Native 全 42 步只读追踪与同版本未插桩运行一致。

30 项测试通过，覆盖完整 Reset、极小非零值、自然休眠、无唤醒 pose setter、默认释放位姿及前面的登记/几何/材质修复。12 枪受校准回放完成：11005 的 1,023 对 setter 保持一致，端点汇总与材质修复后的基线完全相同；该回放仍注入记录的释放朝向和摩擦输入，不作为完整释放链的证据。

以上完整逐位验证适用于本次样本及已修复的 **Windows CP39 内核**。CP38/CP313 的 pose-setter 指令及算术常量已对照，但没有应用其 FTZ/DAZ 修复或宣称完整 Reset 逐位通过。Linux/未知内核需要显式 no-autowake 绑定，当前桥接拒绝未经验证的函数地址。其他 Reset 构型、启动/烹饪的所有中间值与全部释放后算术也没有因此自动获得逐位对齐结论。

```powershell
python analysis_input/verify_reset_complete_alignment_20261002.py
& 'C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python39_64/python.exe' -m unittest local_simulator.tests.test_unity_stone_registration local_simulator.tests.test_unity_reset_settling local_simulator.tests.test_unity_shape_refresh local_simulator.tests.test_strict_simulator local_simulator.tests.test_recovered_stone_mass local_simulator.tests.test_recovered_transform_scale
```
