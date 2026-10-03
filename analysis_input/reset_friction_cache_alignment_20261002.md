# Reset 接触、摩擦约束与缓存逐位检查（2026-10-02）

**历史快照：**下面是无条件 pose 写回与 FPU guard 修复之前的结果。第 2 步缓存和第 6 步输出分歧现已修复；最新见 [第一次 Reset 完整逐位闭合](reset_complete_alignment_20261002.md)，42 步及自然休眠逐位通过。

本轮按真实调用修正两处材质生命周期：`CurlingStoneNew.Start` 只将动态摩擦写为 0；Reset 保留已有材质状态；`OnCollisionEnter(Stone)` 对实际碰撞双方恢复 0.6/0.6。**状态输出的首个分叉仍在第一次 Reset 第 6 步。新增内部采样发现，第 2 步的摩擦缓存输入已经不同，不能再把前 5 步的状态输出一致称作内部链条全部一致。**

## 修复依据

- 反编译 `f61028` 明确执行 `f32557` 获取 Collider material，随后 `f32511(..., 0, ...)`，只写 dynamicFriction。新运行采样也记录该 Start 调用及嵌套写入；启动时已执行 Start 的组件与实测 roster 的约束 80 对应。Unity Reset 静态接触的约束头 offset 16/20 实测为 static=0.012 / dynamic=0；旧本地为 0.012 / 0.012。
- `f61066` 的正式出手分支将 active 的两种摩擦置零；Reset 的 pose/activation 操作不会恢复所有壶的材质。此前本地 `deactivate` 和 `activate_stationary` 无条件恢复 0.6/0.6，现按 native 生命周期保留。
- `f61030` 的 Stone 碰撞分支恢复接收组件自己的两种摩擦。此前本地只恢复 active，默认所有 target 已是 0.6 掩盖了遗漏。修正 Start 后，必须同时处理实际接触的 target；现通过真实 stone--stone report 对双方恢复，数值已相同则不重复写入。新增实际 PhysX 接触测试覆盖双方与随后 Reset 的材质保留。

## 内部逐位边界

完整验证在 [reset_internal_alignment_verified_20261002.json](reset_internal_alignment_verified_20261002.json)，复查脚本为 [verify_reset_internal_alignment_20261002.py](verify_reset_internal_alignment_20261002.py)。

1. 第一 Reset 第 1～6 步，双方 PCM 输入的两个 P/Q 共 84 个浮点字一致；30 个输出接触点的 normal/separation/point 共 210 个字一致，顺序也一致。内部面编号尚未在该检查中闭合。
2. 两侧接触约束头的全部数值字段一致；native 64 位指针使 header 比 wasm 长 16 字节，指针和未参与算术的填充不作为物理值比较。
3. 六帧的全部 5 条 normal row，共 360 个浮点字一致。前 5 帧的 4 条 friction row 所有参与算术的字段一致。
4. 第 6 帧的 friction row 首先在锚点相关角响应、速度乘数、bias/targetVelocity 字段出现差异；随后 Q、水平线速度及角速度输出分叉。竖直速度仍逐位一致。
5. 再向前追，Unity `f71103` 调 `f71233/getFrictionPatches` 时，第 1～6 帧 cachePtr/count 都为 0/0。Native 对应 finalizer 入口 RVA `0xdcf30` 的 descriptor +160/+168 在第 1 帧为 0/0，第 2～6 帧是非空指针/count=1。原生反汇编 `0xdd022`/`0xdd032` 直接读取这些字段，随后进入旧 patch 复用分支。

因此当前 **首个已观察到的 Reset 内部输入分叉是第 2 步摩擦缓存复用入口**，不是第 6 步 PCM 几何计算。第一帧的缓存为空一致，后续约束输出在第 6 帧才体现缓存历史差异。不能据此宣称所有更早启动/烹饪指令均已对齐。

## 证据与插桩有效性

- Unity 原始 wasm SHA256：`cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81`；native CP39：`2564abec4fa3f358e67259b105c4b88d49eae28510611c8a0e2f11b7671888df`。
- Unity 有效采样：`unity_reset_internal_first_case_20261002`、`unity_reset_anchors_first_case_20261002`、`unity_reset_contact_prep_first_case_20261002`。验证原函数体迁移后逐字节不变；三次的 256 个 Reset core frame、1,562 次摩擦记录、终局物理字段均与基线相同。
- Native 有效采样：`native_reset_anchors_steps1_6_20261002`、`native_reset_friction_prep_steps1_6_20261002`。两次分别 30/36 个完整调用，调用栈可靠、无丢失、无未完成；全部 42 步输出与未插桩运行相同。
- 两次额外 pose/cache 采样虽然完成正式出手与摩擦记录，但缺少 Reset solver 窗口：`unity_reset_pose_cache_first_case_20261002`、`unity_reset_pose_cache_bounded_first_case_20261002`。**它们不用于 Reset 的通过判定，也不能用“没有 pose 事件”证明 Unity 没调用 setter。** 该窗口缺失原因尚未确认。

## 回归及尚未闭合项

28 项测试通过。12 枪受校准回放完成，11005 原有 1,023 次 setter 保持逐位相同；首次石壶接触后的输出发生预期变化，因此不宣称旧 1,022 tick 整份输出保持相同。活动壶端点 RMSE 从约 0.206 mm 降到 0.038 mm，目标壶从约 2.919 mm 降到 0.073 mm。这只验证两处材质修复的效果，不证明摩擦缓存清除机制或碰后链条已还原；该回放仍使用已记录的释放姿态/摩擦输入。

还缺少 Unity 清除 work-unit frictionData/frictionCount 的具体写入者、调用条件及原生等价操作。`f71272` 会从 work-unit +36/+42 读入 descriptor +136/+140，并在 finalization 后写回；已定位两端字段，但清除发生在这些边界之间的哪一个上游调用尚未闭合。下一步应对这两个 work-unit 字段做定点写入跟踪，同时检查调用者与 scene flag，不能直接添加经验清缓存或从端点改善推断原因。

```powershell
python analysis_input/verify_reset_internal_alignment_20261002.py
& 'C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python39_64/python.exe' analysis_input/sample_reset_internal_trace_20261002.py --output analysis_input/native_reset_start_friction_internal_fixed_20261002.json
& 'C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python39_64/python.exe' -m unittest local_simulator.tests.test_unity_stone_registration local_simulator.tests.test_unity_reset_settling local_simulator.tests.test_unity_shape_refresh local_simulator.tests.test_strict_simulator local_simulator.tests.test_recovered_stone_mass local_simulator.tests.test_recovered_transform_scale
```
