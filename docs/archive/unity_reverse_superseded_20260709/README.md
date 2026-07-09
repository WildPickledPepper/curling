# Unity 逆向子文档目录

这是维护入口。原来的超长单文件已经原样封存，后续请优先维护本目录下的子文档。

> 封存原文：[`../archive/UNITY_REVERSE_ENGINEERING.zh.2026-07-07.archive.md`](../archive/UNITY_REVERSE_ENGINEERING.zh.2026-07-07.archive.md)

## 子文档

1. [`00_overview_assets.zh.md`](00_overview_assets.zh.md)：包结构、Unity 对象参数、全局常量、数据结构、核心函数索引、Ghidra 过程。
2. [`01_single_stone_motion.zh.md`](01_single_stone_motion.zh.md)：`Newfrictionstep`、`fsimp`、速度分段、运行时物理循环。
3. [`02_protocol_sweep_input.zh.md`](02_protocol_sweep_input.zh.md)：Unity/协议坐标、MOTIONINFO、扫冰、BESTSHOT/SWEEP/POSITION 输入。
4. [`03_rules_state_records.zh.md`](03_rules_state_records.zh.md)：规则阈值、每壶结束状态机、SendGameState、AutoDCP 记录/回放。
5. [`04_collision_entry.zh.md`](04_collision_entry.zh.md)：碰撞/触发路径、PhysX 任务图、contact/finalization 表、narrowphase 表。
6. [`05_physx_contact_generation.zh.md`](05_physx_contact_generation.zh.md)：PhysX convex-convex / convex-mesh 接触点生成、cache、reduction、ContactBuffer。
7. [`06_physx_solver.zh.md`](06_physx_solver.zh.md)：PhysX contact finalization、Px1DConstraint 排查、single-pair 和 4-wide solver。
8. [`07_unknowns_training_toolchain.zh.md`](07_unknowns_training_toolchain.zh.md)：剩余未知、训练优先级、实用结论、当前逆向边界、模拟器修正、数据一致性检查。
9. [`08_resampling_plan.zh.md`](08_resampling_plan.zh.md)：重采样计划、`.save` record 归档、socket JSONL 采样流程。
10. [`09_record_file_storage.zh.md`](09_record_file_storage.zh.md)：`.save`、`RANDSEED`、`TRACE`、`AutoGame/rank.csv` 的逻辑路径与 WebGL IndexedDB 落盘位置。
11. [`10_simulator_alignment_strategy.zh.md`](10_simulator_alignment_strategy.zh.md)：本地模拟器对齐、误差分层、训练准入线。
12. [`11_runtime_injection_probe.zh.md`](11_runtime_injection_probe.zh.md)：Unity WebGL 运行时注入探针、可采集信息、使用流程和边界。
13. [`12_physx_convex_cooking.zh.md`](12_physx_convex_cooking.zh.md)：石壶 MeshCollider convex cooking、cooked hull、PhysX 4.1 QuickHull/partial hull 证据。
14. [`13_physx_native_state_equivalence.zh.md`](13_physx_native_state_equivalence.zh.md)：首次碰撞帧 Unity native state 与本地 pyphysx state 是否逐字段一致的证明义务表。
15. [`04_collision_physx.zh.md`](04_collision_physx.zh.md)：碰撞/PhysX 兼容导航页。

## 维护约定

- 以后新增逆向结论先写入对应子文档。
- 这个入口文件只维护目录和阅读路径。
- 封存原文只作为历史快照，不再继续维护。
- 如果某个子文档继续变长，再按同样方式拆分，并在这里更新目录。

## 建议阅读路径

训练模拟器优先读：`01_single_stone_motion` -> `02_protocol_sweep_input` -> `03_rules_state_records` -> `07_unknowns_training_toolchain` -> `10_simulator_alignment_strategy`。

碰撞保真优先读：`00_overview_assets` -> `12_physx_convex_cooking` -> `04_collision_entry` -> `05_physx_contact_generation` -> `06_physx_solver` -> `07_unknowns_training_toolchain`。

## 常用离线工具

- `tools/reverse/summarize_physx_contact_paths.py`：从 wasm table 中汇总 stone-stone / stone-rink / stone-wall 的 PhysX contact 函数。
- `tools/reverse/physx_convex_layouts.py`：打印 wasm32 下 PhysX convex cooking / `ConvexHullData` / `CLHL` 的字段偏移和 buffer 顺序。
- `tools/reverse/dump_pyphysx_cooked_convex_hull.py`：rebuilt pyphysx cooked hull 对照 dump；当前 Unity-flags raw 输出为 `128` vertices / `66` polygons / `384` polygon indices / `252` rendered triangles，polygon 直方图 `64:2, 4:64`，并含单位密度 mass/inertia/local COM；binding 默认 `qi1/gpu1` 控制组仍为 `64` vertices / `124` triangles。
- `tools/reverse/analyze_pyphysx_raw_hull_topology.py`：从 raw `PxConvexMesh` 重建 contact topology；当前输出为 `V=128, F=66, E=192`，`facesByEdges8/facesByVertices8` 完整，三类边 `top_ring/bottom_ring/vertical` 各 64 条，报告为 `data/calibration/pyphysx_raw_hull_topology_20260708.json`。
- `tools/reverse/analyze_pyphysx_bigconvex_data.py`：按 PhysX 4.1 源码复刻 BigConvexData `VALE/GAUS`；当前 `VALE=128 verts / 384 adjacent verts / valency 3`，`GAUS=subdiv 16 / 1536 samples / 3072 sample bytes`，support 校验 0 错误，报告为 `data/calibration/pyphysx_bigconvex_data_20260709.json`。
- `tools/reverse/analyze_pyphysx_scaled_mass_properties.py`：按 PhysX 4.1 `scaleInertia` 和 `setMassAndUpdateInertia(single mass)` 把 raw cooked hull 的单位密度 mass/inertia 缩放到 Unity 正式 world scale；当前推荐 probe 参数为 `--inertia-radial 0.178810612362 --inertia-vertical 0.189222883199`，报告为 `data/calibration/pyphysx_scaled_mass_properties_20260709.json`。
- `tools/reverse/analyze_collision_parameter_oracle_floor.py`：横扫已有 unique-role 碰撞 probe/grid，计算“全局同一参数最好”和“每条样本单独挑参数”的理论下限；当前报告为 `data/calibration/unity_collision_parameter_oracle_floor_20260709.json`，用于判断误差是否还能靠单个全局 PhysX 参数解释。
- `tools/reverse/analyze_collision_oracle_hypotheses.py`：把 oracle winners 归因到 radius/yaw/handoff/topology/shape-local 等代理变量；当前报告为 `data/calibration/unity_collision_oracle_hypothesis_audit_20260709.json`，用于判断哪些 native-state 缺项最可疑。
- `tools/reverse/summarize_collision_material_timing.py`：汇总 `OnCollisionEnter` 材质时序候选 probe；当前报告为 `data/calibration/unity_collision_material_timing_audit_20260709.json`，用于判断 first-contact 材质切换是否能解释 10cm 误差。
- `tools/reverse/analyze_collision_impulse_residual.py`：用 probe 的 0.02s snapshot 反推 Unity 终点需要的早期 target 速度/冲量修正；当前报告为 `data/calibration/unity_collision_impulse_residual_20260709.json`，用于区分 normal impulse、tangent impulse 和接触点/角速度耦合。
- `tools/reverse/analyze_collision_pair_impulse_residual.py`：把 endpoint 反推扩展到 active/target 双方，检查所需早期速度修正是否像等大反向的 pair impulse；当前刷新报告为 `data/calibration/unity_collision_pair_impulse_residual_refresh_20260709.json`。结论是 target 修正在 0.02s-0.2s 间高度稳定，但多数样本 active tail 太短，pair 闭合不能当强证据；仍应优先抓 target 首次 ContactBuffer / solver rows。
- `tools/reverse/analyze_collision_early_velocity_sensitivity.py`：对 target 0.02s early velocity 做有限差分敏感度，检查全局 handoff/placement/yaw/radius/contactOffset/centerHeight 小偏移能否解释缺口；当前刷新报告为 `data/calibration/unity_collision_early_velocity_sensitivity_refresh_20260709.json`，合理范围裁剪后残差没有改善，进一步排除统一初态小偏移。
- `tools/reverse/analyze_collision_impulse_feasibility.py`：把 endpoint 反推的 target 早期冲量分解到 contact normal / tangent，并用摩擦锥做样本分类；当前刷新报告为 `data/calibration/unity_collision_impulse_feasibility_refresh_20260709.json`，结论是样本分裂为 normal-row、friction/cache 和 mixed 三类，因此不能再寄希望于单个全局参数。
- `tools/reverse/analyze_collision_local_impulse_trace.py`：从 0.01s 密集 snapshot 反推本地 PhysX 给 target 的主碰撞冲量，并与 Unity 终点反推残差对比；当前报告为 `data/calibration/unity_collision_local_impulse_trace_20260709.json`，结论是本地主冲量均值约 `19.3 Ns`、Unity 残差均值约 `0.70 Ns`，主误差是首帧 solver/contact row 的几个百分点，而不是碰撞事件整体错位。
- `tools/reverse/analyze_collision_tail_replay_oracle.py`：从本地 `0.02s/0.20s` snapshot 重建 target-only pyphysx 尾段，并用有限差分只调 target 水平 `vx/vy`；当前报告 `data/calibration/unity_collision_tail_replay_oracle_002s_20260709.json` 和 `data/calibration/unity_collision_tail_replay_oracle_020s_20260709.json` 显示，线速度 oracle 可把 endpoint 压到毫米级，说明主误差不在尾段滑行，而在首次碰撞输出给 target 的水平速度。
- `tools/reverse/analyze_collision_solver_row_delta.py`：把 tail oracle 的 target `vx/vy` 修正投回首帧 contact normal/tangent 冲量；当前报告为 `data/calibration/unity_collision_solver_row_delta_from_tail_oracle_20260709.json`，结论是 endpoint 从 `11.32cm` 压到 `0.09cm` 只需平均 `0.49 Ns` 的 row 级修正，约本地主冲量 `2.35%`，但分裂为 normal-row 与 friction/contact/cache 两类。
- `tools/reverse/analyze_collision_row_correction_models.py`：拟合全局 normal/tangent scale、统一旋转、scale+rotation、全局 2x2 等 row 补丁，并把预测修正跑回 pyphysx tail；当前报告为 `data/calibration/unity_collision_row_correction_models_20260709.json`，结论是只有 per-sample oracle 到 `0.09cm`，最宽松全局 2x2 仍约 `10.24cm`，不能靠统一参数进 2cm。
- `tools/reverse/analyze_contact_frame_quantization.py`：把 row-delta 需要的 contact-frame 角度变化和 formal cooked hull 的 64 边侧面法线对齐；当前报告为 `data/calibration/unity_collision_contact_frame_quantization_20260709.json`，结论是 `12003` 从贴近 side face `-87.19deg` 的本地冲量，变为贴近相邻 side face `-81.56deg` 的 Unity-implied 冲量，强指向相邻 hull feature/contact manifold/cache 差异。
- `tools/reverse/analyze_collision_contact_report_dump.py`：汇总 rebuilt pyphysx `--enable-contact-report` 的本地 `ContactPairPoint` normal/separation/impulse，并与 row-delta 对照；当前报告为 `data/calibration/unity_collision_contact_report_vs_row_delta_20260709.json`，结论是 8 条样本第一帧 contact 都在 `0.01s`，`12003` 本地 contact report 冲量角度 `-87.19deg`、Unity-implied `-82.21deg`，差 `+4.98deg`，进一步锁定首帧 contact manifold/feature/cache。
- `tools/reverse/summarize_collision_stone_geometry_input_audit.py`：汇总 generated ring 点云与 recovered formal 512 顶点 mesh 直接送入 pyphysx cooking 的 A/B；当前报告为 `data/calibration/unity_collision_stone_geometry_input_audit_20260709.json`，结论是 current-best 尺度下两者 endpoint 完全相同，formal 尺度下只改善 `0.57cm` target RMSE，几何输入点云不是 10cm 主因。
- `tools/reverse/summarize_collision_feature_phase_audit.py`：汇总 shape-local yaw、active/target actor yaw、shape-local xyz、stone-faces 等静态 feature-phase probe；当前报告为 `data/calibration/unity_collision_feature_phase_audit_20260709.json`，结论是硬坏样本 `12003` 最好仍约 `19.29cm`，静态 hull 相位/简单拓扑不是 2cm 解。
- `tools/reverse/summarize_collision_rotation_reset_audit.py`：汇总 `12003` 宽范围 active/target yaw、全样本 target-yaw-only oracle，以及 `12004/12007` 双 yaw 粗扫；当前报告为 `data/calibration/unity_collision_rotation_reset_audit_20260709.json`，结论是大 yaw 可把 `12003` target 降到 `1.75cm`，但全样本 target-yaw-only 仍约 `5.37cm` target RMSE，硬样本双 yaw best pair RMSE 为 `3.41/4.47/5.57cm`，reset rotation/yaw 是重要缺项但不是单独闭环。
- `tools/reverse/summarize_stone_prefab_rotation_audit.py`：汇总 `inspect_unity_assets.py` 输出中的正式 stone serialized local rotation；当前报告为 `data/calibration/unity_stone_prefab_rotation_audit_20260709.json`，结论是 80 个正式 stone 只有一种 near-identity local rotation，max yaw 为 `0deg`，所以 wide-yaw 改善不是 prefab 初始 yaw 差异。
- `tools/reverse/summarize_collision_integrated_active_yaw_audit.py`：汇总 `--active-yaw-source integrated-precontact` probe；当前报告为 `data/calibration/unity_collision_integrated_active_yaw_audit_20260709.json`，结论是把 BESTSHOT 到 handoff 的 deterministic active yaw 接入后 target RMSE 变差到 `16.30cm`，不是简单漏掉累计自旋相位。
- `tools/reverse/summarize_collision_handoff_threshold_audit.py`：汇总 handoff_extra 与毫米级 y-offset 刷新小网格；当前报告为 `data/calibration/unity_collision_handoff_threshold_audit_20260709.json`，结论是最佳 `+5mm/-5mm` 只把 target RMSE 从 `11.32cm` 降到 `10.27cm`，接触入口位置有贡献但不是 2cm 解。
- `tools/reverse/summarize_collision_handoff_xy_oracle.py`：汇总 handoff x/y、handoff_v_scale、target reset offset、handoff angular velocity 等入口状态反事实；当前报告为 `data/calibration/unity_collision_handoff_xy_oracle_20260709.json`，结论是 per-sample 入口状态 oracle 可把 target RMSE 降到 `1.48cm`、active RMSE 降到 `1.35cm`；7 条 in-play target pair 全部双终点进 `2cm`，active-only 时 8 条全进 `2cm`，其中 `12005` 由 `handoff_w_offset=-0.44rad/s` 诊断闭合。
- `tools/reverse/summarize_collision_angular_handoff_diagnostic.py`：专门汇总 `12005` handoff angular velocity 诊断、同 pose contact report A/B 和全局 `handoff_w_offset` 反证；当前报告为 `data/calibration/unity_collision_angular_handoff_diagnostic_20260709.json`，结论是 `-0.44rad/s` 可闭合 `12005`，但全局最佳 w offset 仍约 `10.94cm` target RMSE / 7 条 bad pair，因此它是 tangent/angular native-state 代理而非全局常数。
- `tools/reverse/analyze_collision_oracle_generalization.py`：对 per-sample 入口状态 oracle 做 leave-one-out 泛化审计；当前报告为 `data/calibration/unity_collision_oracle_generalization_20260709.json`，结论是最好可见特征模型 `headon_linear` 仍有 active RMSE 约 `5.22cm`、target RMSE 约 `30.98cm`，7 条 in-play pair 里 `0` 条双终点进 `2cm`，所以 oracle 不能直接当训练模拟器通用修正。
- `tools/reverse/summarize_collision_lock_constraints_audit.py`：汇总 Unity `FreezeRotationX|FreezeRotationZ` 对应的 pyphysx `--lock-upright` 复跑；当前报告为 `data/calibration/unity_collision_lock_constraints_audit_20260709.json`，结论是横向角速度可归零，但 target RMSE 仍约 `11.37cm`，锁轴不是 10cm 主因。
- `tools/reverse/summarize_collision_support_contact.py`：汇总重力/冰面支撑与 target/active pre-settle 诊断；当前报告为 `data/calibration/unity_collision_support_contact_audit_20260709.json`，结论是禁用重力会失真，但消掉竖直速度或预热支撑 contact/cache 都不能解释 10cm 碰撞误差。
- `tools/reverse/summarize_physx_native_state_equivalence.py`：把首次碰撞帧 native-state 等价性拆成字段级证明义务；当前报告为 `data/calibration/unity_physx_native_state_equivalence_audit_20260709.json`，结论是完整等价不但尚未证明，现有证据还反证强等价命题；pyphysx 已扩出 triangle mesh 和 contact report 入口，`unity-plane-mesh` A/B、handoff threshold、lock-upright 都不能闭合；入口状态 oracle 虽已把 7 条 in-play target pair 全部压进 `2cm`，但依赖 per-sample native-state proxy，说明至少还有 contact-instance native 字段或 cache/solver row 未恢复成通用公式。
- `tools/reverse/summarize_rigidbody_mass_writes.py`：解析 Rigidbody mass / COM / inertia / Reset 写入的真实 wasm 调用者，区分正式石壶和 URDF 无关路径。
- `tools/reverse/summarize_meshcollider_rebuild_mass_sync.py`：复查 `MeshCollider.sharedMesh/convex -> slot[37] -> func72951 -> func73283 -> f_abdd` 链路，确认 runtime convex rebuild 会触达 Rigidbody mass-properties sync。
- `tools/reverse/summarize_stone_quickhull_path.py`：读取已恢复石壶 mesh，证明 512 个输入点都是凸包极点并超过 `vertexLimit=255`，因此 Unity flags 下应走 PhysX OBB cropped hull 路径。
- `tools/reverse/summarize_physx_cropped_hull_path.py`：对照 Unity wasm `func72908/72910/72915` 与 PhysX 4.1 源码，固化 `createConvexHull -> expandHullOBB -> mCropedConvexHull -> cropped desc fill` 证据链。
- `tools/reverse/summarize_cooked_hull_capture_points.py`：打印导出 Unity 最终 cooked hull 的 wasm 抓取点；优先 hook `func72915/f_lvcd` 后的 `PxConvexMeshDesc.points/polygons/indices`。
- `tools/reverse/export_cooked_hull_from_probe_events.py`：从运行时 probe 的 `physx.cooked_hull.desc` 事件导出稳定 cooked hull JSON；当前等待页输出为 `data/calibration/unity_cooked_hulls_20260708_225950.json`，但该批 hull 已被尺寸判据排除为正式石壶。
- `tools/reverse/analyze_cooked_hull_identity.py`：把捕获 hull 的 extents 与 formal stone `ExtendedColliders3D` 期望尺寸对比，防止把等待页/机器人 cooked hull 误接进比赛石壶碰撞模型。
- `tools/reverse/summarize_formal_stone_cooking_status.py`：汇总 formal stone source mesh、Unity convex flags、cropped path 必然性、等待页 hull 排除、rebuilt pyphysx Unity-flags raw hull/topology/BigConvexData/mass-inertia dump 和碰撞 probe 剩余误差；当前输出为 `data/calibration/formal_stone_cooking_status_20260708.json`。
