# 持久 Scene 对齐研究账本

更新时间：2026-07-14

> 本文是 P5/P6 的唯一恢复点。会话压缩、人员切换或重新开始工作时，必须先读本文和
> `14_pcm_final_alignment_plan.zh.md` 的最后两节；不得只根据聊天摘要重新定义根因。

## 目标与边界

目标不是让某条 endpoint 看起来接近，而是在 `14000` 上找到本地与 Unity 的**第一处 native
字段差异**，再只修改该字段或调用语义。`14001` 只能在 14000 的对应 gate 闭合后进入验收。

以下边界已经严格区分：

```text
direct scalar PCM
  != persistent PxScene narrowphase
  != full Scene solver/writeback/endpoint
```

所有结论必须标注属于哪一层，禁止跨层外推。

## 证据状态词典

| 状态 | 含义 | 允许的表述 |
|---|---|---|
| `closed` | 同一边界、同一输入下字段或公式已通过验收。 | “该边界已闭合”。 |
| `sensitivity` | 改变该项会改变结果，但尚未证明 Unity 正是通过它产生结果。 | “真实敏感项，非根因结论”。 |
| `rejected` | 受控 A/B 未改变目标差异，或与 Unity 真值矛盾。 | “已排除为该边界主因”。 |
| `unobserved` | 尚未有同一 boundary 的 Unity/local 字段对照。 | “待观测”，不得猜修复。 |
| `diagnostic_only` | oracle 注入可证明因果，但不得接入生产。 | “诊断成立，不是修复”。 |

没有 `closed` 或“第一处字段差异”的结果，一律不得使用“唯一根因”“最后一块”“已修复”。

## 全链路对齐总表

这张表是当前项目的状态总览。`closed` 永远只对“范围”栏中写明的边界成立；它不自动证明下一层。

| ID | 环节 | Unity/本地已知信息 | 当前状态 | 已验收范围 | 尚未证明或禁止外推 | 主证据 |
|---|---|---|---|---|---|---|
| S01 | 坐标、协议、FixedUpdate | `BESTSHOT`、`MOTIONINFO`、轴映射、fixed dt=`0.01` 已恢复。 | `closed` | 协议输入到 Rigidbody 写入。 | 不证明 PhysX 内部 fixed-step 顺序。 | `01`、`02` 文档。 |
| S02 | 出手材质时序 | active 出手时 `0/0`；首 stone-stone solver 前恢复 `0.6`，组合为 `0.36`。 | `closed` | 14000 第一笔 dynamic-dynamic ContactBuffer。 | 不证明 pair/work-unit 等价。 | `p5_14000_material_transition_*`。 |
| S03 | 自定义滑行 | `Newfrictionstep` Wasm 与本地逐 tick同噪声流一致。 | `closed` | 函数计算和 RNG 消费。 | 不证明写回 Rigidbody 后的 PhysX 积分。 | `newfrictionstep_wasm_rollout_*`。 |
| S04 | 石壶静态碰撞资源 | 4008-byte hull、BigConvex pointed arrays、scale 已有 Unity 真值。 | `closed` | direct scalar PCM 输入 bundle。 | 不证明本地持久 Scene 的 native hull wrapper/任务顺序。 | `scalar_pcm_backend_audit_*`。 |
| S05 | 冰面 cooked object | vertices、triangles、faceRemap、BV4 nodes 与 Unity byte-level 对齐。 | `closed` | cooked mesh object。 | 不证明 scalar BVH33 Scene 与 Unity 的 traversal/solve 时相。 | `runtime_ice_cooked_equivalence_*`。 |
| S06 | Rigidbody 静态参数 | mass=19.1、solver 6/1、maxDepen=10、COM=zero、yaw inertia 已对齐。 | `closed` | 首 solver/native body 输入。 | 不证明连续多约束后的 body state。 | `front_half_pcm_solver_state_*`、P5 审计。 |
| S07 | scalar 后端选择 | SSE 与 WebGL scalar 的 full-manifold 结果不同；scalar 才匹配 Unity。 | `closed` | exact native entrance 的 PCM backend。 | 不证明 scalar Scene 的 ice path 等价。 | `scalar_pcm_backend_audit_*`。 |
| N01 | direct scalar PCM | 六条 exact entrance 的 count/point/normal/separation 到 float32 ULP。 | `closed` | 单次 `PxcPCMContactConvexConvex` 调用。 | 不证明 persistent contact-manager/work-unit。 | `scalar_pcm_backend_audit_*`。 |
| N02 | task-local PCM cache | 每 call 清 contact/warm-start、保留 feature bytes；第二次调用已验证。 | `closed` | 已捕获的 task-local call 入口。 | 不证明碰后多 tick anchor 演进。 | `persistent_scene_motioninfo_local_contact_after_pcm_lifecycle_*`。 |
| N03 | first-frame cache reset | `clearManifold` 开/关不改变六样本首帧 count。 | `rejected` | first ContactBuffer 的 2/4 分叉。 | 不得再把 cache clear 当首帧修复。 | `persistent_scene_sequence_*lifecycle*_audit_*`。 |
| N04 | PCM 参数/几何重扫 | contact distance、margin、tolerance、hull/BigConvex、method table 已逐层核验。 | `rejected` | 已验证的 direct PCM 边界。 | 不得重扫 scale、offset、半径或 feature bytes。 | P1--P3 报告。 |
| V01 | ContactBuffer 到 solver row | Unity raw ContactBuffer + body data 重放 normal/friction row 到 float 精度。 | `closed` | raw constraint preparation。 | 不证明 Scene 自然生成同一 ContactBuffer。 | `unity_direct_pcm_solver_row_bridge_*`。 |
| V02 | solver consume/writeback 公式 | dynamic/static with-writeback raw 重放到 float 精度。 | `closed` | 给定 raw rows/body 的单约束消费。 | 不证明连续 Scene 的 pre-solve state/批次顺序。 | `unity_solver_writeback_*`。 |
| F01 | trailing fixed step | 14002/14004 在最后 RNG 后仍有一次 physics-only step。 | `closed` | 已捕获的脚本/物理时相。 | 不证明 stone-ice 内部执行细节。 | `hybrid_p6_endpoint_sixshot_*`。 |
| F02 | MOTIONINFO 到 PCM shell | 6/6 reached，position RMSE `0.194mm`。 | `closed` | physical shell 的平移状态。 | shell 不等于 first stone-stone PCM transform。 | `persistent_scene_front_half_contact_scalar_*`。 |
| F03 | Reset 语义 | Unity Reset 只写 position；quaternion 保留。本地已保留 quaternion。 | `closed` | actor 历史保持规则。 | 首个 14000 cold active 的初始 hidden yaw 仍未记录。 | `persistent_scene_sequence_audit_*`。 |
| F03A | A0 既有日志覆盖 | 受控 14000 同次日志有 stone-ice PCM、static writeback、stone-stone PCM transform；没有 tick 标识、post-write `v/w`、post-sim actor `P/Q` 或 cache 写入顺序。 | `closed` | 既有日志的可用性判定。 | 不能把不同时刻/不同运行的字段拼成 synthetic tick trace。 | `a0_14000_fixed_tick_coverage_20260711.json`。 |
| F03B | 最后脚本 `v/w` 写入 | 同一受控 14000 已捕获 `get_velocity/get_angularVelocity`、friction noise 和 `set_angularVelocity`；两条末 tick 的本地 `Newfrictionstep` 与 Unity `wy` 差为 `2.78e-9/1.21e-9rad/s`。 | `closed` | script getter -> Newfrictionstep -> setter。 | 不证明随后 stone-ice static solver/writeback 与 pose integration。 | `a0_last_angular_write_full_inputs_14000_audit_20260711.json`。 |
| F03C | `MOTIONINFO` 语义 | 同一 A2 trace 的第 403 tick 与协议 `MOTIONINFO` 的位置/速度/`wy` 在协议精度相符；trace 第 0 tick 才是 `BESTSHOT` release。 | `closed` | 14000 的 `MOTIONINFO` 是 Midline trigger report，而非 native Rigidbody 出手起点。 | `MOTIONINFO -> PCM` 尾段 replay 仍有效；不得把它外推为 `BESTSHOT -> PCM` 的 native 起始验收。 | `a3_motioninfo_semantics_14000_20260712.json`、`02` 文档。 |
| F03D | local script feedback | Unity getter/noise 经 `Newfrictionstep` 并 float32 写回 setter 全 `1559` tick 逐位相同；但 local production getter `wy` 自 tick `25025` 差 `-1.86e-9rad/s`，其反馈的 setter 在 tick `25070` 超过一 ULP，末端达 `-7.75e-6rad/s`。该首差时 Unity `P.y` 仍比已知支撑高度高约 `7.7mm`。 | `closed` | 14000 单壶 `BESTSHOT -> first PCM` 的 script/PhysX feedback boundary。 | 旧 F03B 的末两 tick 一致不得外推为整段一致；首差早于稳定 stone-ice 支撑。 | `a5_bestshot_production_setters_14000_20260712.json`。 |
| F03F | angular getter recurrence | Unity/local angular damping 均为 `0.05`；相同 setter 后前四次 getter 相同，第五次 `25024 -> 25025` 本地少一个 `wy` float32 ULP。 | `closed` | 已排除漏设 damping、lock、actor/cache refresh；首差在 x64 scalar PhysX 的 damping/integration recurrence。 | 尚未证明该 ULP feedback 单独量化为最终 `0.000303rad` 的全部份额；不得用样本补偿取代 WebGL-compatible backend。 | `a6_angular_getter_recurrence_14000_20260712.json`。 |
| F03G | A8 solver-body snapshot | 新受控 `14000` 的八个 release tick 中，Unity `PxSolverBodyData.wy` 在 static call **之前**已从第 5 个窗口起比 local raw float32 damping 高 `1 ULP`，随后差扩大为 `2/3 ULP`；该 snapshot 在 static call 前后不变。 | `closed` | “raw damping -> solver-body snapshot”早于 static solve 的首次可观测差。 | `PxSolverBodyData` 是 pre-solver snapshot；其不变不能单独证明 `PxSolverBody.angularState` 不变。static angular writeback 很小仍以 A0.6 为证据。 | `a8_static_window_recurrence_14000_20260712.json`。 |
| F03H | A9 native-core pointer scan | 旧 A9 以 Rigidbody native-pointer 附近的 pointer-shaped bytes 猜测 `PxsBodyCore`；严格校验未找到可验证 core，先前宽松扫描产生的是无物理意义的伪候选。 | `invalidated` | 不得用该扫描推断 body-core damping、lock 或积分输入。 | 下一次只比较同一 `set_angularVelocity` 调用前后的 native Rigidbody 原始字节差分；没有可验证 layout 前不把任何偏移命名为 `PxsBodyCore`。 | `a9_snapshot_window_20260712_run6/`（无有效 core）；`audit_a9_angular_setter_native_delta.py`。 |
| F03I | A9 Rigidbody root setter delta | 新受控 `14000` 的连续八次 `set_angularVelocity` 均已捕获；同一 native Rigidbody 根对象前 `1024B` 的 before/after 差分均为 0。 | `closed` | `wy` 被直接写在该根对象的可见字段中。 | 这证明 setter 经由 root 指针目标或 deferred bridge 传播，不证明没有 native 写入。下一步只比较该 root 一层可达 pointer target 的同调用前/后字节差分。 | `a9_angular_setter_native_delta_14000_20260712_run10.json`。 |
| F03J | A9 one-hop setter bridge | 受控 `14000` 的八次 setter 都使 root `+52` 指向的同一 native target 改变；首三次可逐 float32 读到 `target+164 == setter wy`，并在 `target+300` 有相同副本。 | `closed` | “脚本 `set_angularVelocity` 没有进入 Unity native state”。 | setter 到 native target 的值传递无损；尚未比较该 target 在 solver-body snapshot 前是否被阻尼/复制。不得把 target 的未命名偏移直接叫作 `PxsBodyCore`。 | `a9_pointer_delta_14000_20260712_run11.json`。 |
| F03K | A10 bridge-to-snapshot | 前四 tick `bridgeAfterSetter.wy == setter wy`；第 5 tick 起 bridge 已比 hook 读到的 setter 输入高 `1/1/2/3 ULP`。随后每 tick 都满足 `bridgeAtStaticEntry.wy == PxSolverBodyData.wy`，且 bridge-after-setter 经本地 float32 damping 后逐位等于 bridge/static。 | `closed` | unconstrained damping、bridge 到 solver-body snapshot copy、static contact writeback 作为首个 ULP 来源。 | 差异在 `Rigidbody.set_angularVelocity` native transfer 内出现；其已确认含姿态相关变换，但该变换的第 5 tick 后精确 rounding 尚未闭合。 | `a10_bridge_snapshot_14000_20260712_run12.json`。 |
| F03L | A12/A14 native setter transform | active 的 `constraints=80` 冻结转动 X/Z。`func72559` 对输入执行 `q.rotate(maskXZ(q^-1.rotate(v)))` 后才写 root `+52` bridge；A12 八条的 bridge y/z 均逐 float32 对齐。接入本地诊断 helper 后原 tick `25025` 的首个 `wy` ULP 消失。 | `closed`（setter wrapper 范围） | Unity angular setter 不是直接 `[0,wy,0]`；其 locked-axis projection 已有本地等价实现。 | 1559 tick no-oracle 回放仍在 tick `25038` 出现角反馈差、末端 `wy=-2.64e-6`；不得把 helper 默认接入生产或宣称 A 链/P6 完成。 | `a12_native_setter_basis_14000_20260712_run14.json`、`a14_pose_basis_locked_projection_14000_20260712.json`、`a14_full_release_locked_projection_14000_20260712.json`。 |
| F03M | A19 WebGL solver-body snapshot | Wasm scalar backend 以 live getter 驱动实际 Unity `Newfrictionstep`，1559 tick 中不再喂 Unity setter 或 pose。保留 locked X/Z 到 solver-body snapshot 后，终点位置逐 float 相等，四元数最大分量差 `5.513e-7`；首次 feedback 输入差推迟至 tick `25083`。 | `closed`（14000 A 链） | 原 `0.000303rad` common micro-yaw 的主来源是本地在 solver-body setup 过早清除 locked X/Z angular velocity。 | 仅关闭单壶到 first PCM 的 A 链；不证明 B 的 pair lifecycle、首次 ContactBuffer 或 P6 endpoint。 | `a19_wasm_live_feedback_lock_snapshot_14000_20260712.json`、`physx_a19_solver_body_locked_angular_snapshot.patch`。 |
| F03N | A21 hybrid A19 integration | 重建 `PhysX_static.lib` 并重链 hybrid `.pyd` 后，首碰入口审计显示 `14000/14001` 的 active `P` 逐 float 相等，`Q` 最大分量差分别为 `5.3644e-7 / 1.1548e-7`，count 均相同；第一条失败为 `14002`。A21 原 run 的 `14002` active0 为 `P max=0.1678467mm`、`Q max=0.00131427`、count=`2`。C22 production retest 仍有相同 `P max=0.1678467mm` 和 count=`2`；其 `q.y=0.13120204`，Unity 为 `0.12973659`，故当前 `Q max=0.00146545`。 | `closed`（fresh-active A 范围） | A19 patch 已实际进入 hybrid/x64 六样本执行物，且覆盖首次使用的 active 0/1；C22 进一步确认 C20 后 reused active0 的 entrance 仍失败。 | `14002` 重新使用 14000 碰后曾参与过的 active0；Reset 仅写 position，故该入口 `P/Q` 是已观测的碰后历史消费者差异，不是新的 A release recurrence。C20 改变了该历史四元数 residual 的方向但没有闭合它；不得把 C11 的速度归零外推为 active0 reset-state 正确。 | `a21_hybrid_entrance_14000_14005_20260712.json`、`a21_hybrid_a19_snapshot_sixshot_14000_14005_20260712.json`、`c22_p6_production_retest_14000_14005_20260712.json`。 |
| F03E | release 高度差 | local `start_bestshot` 初始 `P.y` 比 Unity release 低 `12.615204mm`；将高度和脚本 setter 的 `y=0` 语义仅作诊断对齐后，首个 P/Q 步可相同，但 F03D 的 `wy` feedback 漂移不消失。 | `rejected` | 作为当前 yaw residual 的主因。 | 是真实 release-state 差异；不能删除或硬编码，需与本地 release 语义另行对齐。 | `a4_bestshot_release_state_14000_20260712.json`、`a5_bestshot_unity_release_state_setters_14000_20260712.json`。 |
| F04 | common micro-pose | first stone-stone PCM 前 local active 少 `30.5um` X、`0.000303rad` yaw。 | `unobserved` | 差异已在真实本地 narrowphase 入口测得。 | A2 已排除“从 Unity release solver-body 首行起的 local stone-ice static solve/integration”生成该差异；现在只允许先比较本地与 Unity 的 `BESTSHOT/release` actor `P/Q/v/w`。 | `p5_14000_narrowphase_pose_causality_*`、`a2_local_static_trace_replay_14000_20260711.json`。 |
| F04A | actor -> transform-cache refresh | Unity 与 local 14000 的首个 stone-stone PCM 均满足 `PxsRigidCore.body2World.q == PCM consumed transform-cache.q`，逐 float 相等。 | `rejected` | “缺少或晚于 actor core 的 cache refresh”作为 micro-pose 来源。 | local/Unity active actor core 本身仍相差约 `0.000303rad` yaw；来源必在 actor core 形成之前。 | `a0_actor_core_cache_14000_audit_20260711.json`、`a0_local_actor_core_cache_14000_audit_20260711.json`。 |
| F05 | micro-pose oracle | 补齐 F04 的 P/Q 后，active->target 本地从 4 点变 2 点。 | `diagnostic_only` | 证明该 P/Q 差可因果改变当前分支。 | 禁止硬编码；不证明来源是 SetActive。 | `p5_14000_narrowphase_pose_causality_*`。 |
| F06 | BVH/simple midphase toggle | fast-midphase/BVH33 切换不消除 F04。 | `rejected` | 简单 backend toggle 假设。 | 不得把切换 BVH 当生产修复。 | local narrowphase A/B scratch。 |
| A01 | 高层 SetActive 顺序 | Unity 与本地同为 target reset 启用、active BESTSHOT 启用。 | `closed` | GameObject/actor 高层顺序。 | 不证明 native interaction 创建等价。 | `unity_setactive_pair_lifecycle_*`。 |
| A02 | Collider activation 静态链 | MeshCollider refresh/mass-sync 的候选 call graph 已反编译。 | `closed` | 静态 Wasm 调用关系。 | 实际 active branch 的全部 runtime side effect 未逐字段抓到。 | `13`、`14` 文档。 |
| A03 | post-activation pose 重写 | 去掉本地第二次 pose 写入会读到 stale broadphase pose；保留才可正常运行。 | `closed` | 本地 binding 的 refresh 适配必要性。 | 不是 F04 或 pair 2/4 的根因。 | `persistent_scene_sequence_activation_bridge_*`。 |
| B01 | Unity pair 创建输入 | overlap `target -> active`；new-list manager；solver-facing work-unit `active -> target`。 | `closed` | Unity 14000 创建到 first finalizer。 | 不证明本地怎样复刻同一 native creation state。 | `overlap_created_timeline_*`。 |
| B02 | pair role 敏感性 | shape-flag=`target->active/2`；remove/add=`active->target/4`。 | `sensitivity` | 14000 本地反事实。 | 两条都不是 Unity 等价实现。 | `setactive_membership_contactbuffer_audit_*`。 |
| B03 | manager/cache 首帧假设 | new-list、flags/status/edge、cache 非空已解码；cache reset 不是首帧根因。 | `closed` | Unity first manager 可见字段。 | ShapeInteraction/private creation state 与本地仍未等价。 | `unity_pair_lifecycle_timeline_*`。 |
| B04 | private pair lifecycle | A16 的 `eDISABLE_SIMULATION` 保持 actor/shape identity 并重建 `RigidID`。B23 修复 audit Scene 中 Reset 把 stationary target quaternion 覆写为 identity 的错误，改为初始化一次、Reset 仅改 position。B24 又把 active 材质 `0 -> 0.6` 的恢复从“预测下一 pose”改到“当前 pose 已进 PCM shell”，避免 first PCM 前额外一 tick stone-ice 摩擦。 | `closed` | 14000 同源 Wasm Scene 的 identity-preserving activation、Reset quaternion、material 时相、solver-facing role 和 first PCM point/normal。 | B24 separation 仍差 `6.1467e-8`（约 33 ULP），来自 active transform 的 `3.65e-7` quaternion residual；B25 的 hybrid 六样本尚有 A 输入/出界问题，不能外推为 P6 endpoint 通过。 | `b21_wasm_direct_pcm_audit_14000_20260712.json`、`b22_transform_crosscheck_14000_20260712.json`、`b23_reset_preserve_q_contactbuffer_audit_14000_20260712.json`、`a20_material_current_pose_contactbuffer_14000_20260712.json`、`b25_p6_identity_material_current_14000_14005_20260712.json`。 |
| C01 | first solver ContactBuffer | 14000 local point 相对 Unity 横移约 `8.5mm`，friction target velocity 随之不同。 | `closed` | 差异位置与下游因果。 | 不是独立 solver/friction 参数问题。 | `p5_14000_contactbuffer_*`。 |
| C02 | 碰后 yaw 历史 | 14001 target 进入 solver 前已带 14000 后的 yaw 偏差。 | `closed` | 分叉先后关系。 | 14000 continuous Scene writeback 尚未自然闭合。 | `p5_14001_same_phase_*`。 |
| C03 | 14000 连续 writeback | 首个 dynamic step 的 active 材质若仍为 `0.6`，本地会额外损失 `0.01568456rad/s`；已改为该 step 后才恢复，Unity/local 首帧 post-state exact。C07 同源 4 帧表明 PCM seq `0..3` 的 point/normal/separation 全 exact；solver frame 0 exact、frame 1 仅 ULP 级，frame 2 开始 active `w` 差 `0.02392037rad/s`、`q.y` 差 `1.187697e-4`。C13 已排除 dynamic `solveContactBlock` consume。C14 定位 target `v_y` 差发生在 dynamic regular 0 与 1 间的 target-ice static support；同一 raw body/constraint 下 x64/Wasm 都输出 `0.0981201455`，Unity 为 `0.0981196463`。C15 historical Unity target-ice direct PCM 在 C14 exact transform 下 5 点逐 float 相同。C18 证实 Unity historical target-ice wrapper input 始终为 `flags=3/cachedSize=0`；C19 在 parent `PxcDiscreteNarrowPhasePCM` 入口以空的 task-local serialized multi payload 复刻该 field，C20 将同一语义接入 production 后 C11 四帧 `P/Q/v/w` 全 exact，target 的 `+4.991889e-7m/s` 消失。C21 的另一 first-writeback fixture 仍有 PCM 输入 `q=5.3644e-7`、ContactBuffer separation `8.5682e-8`、下一 PCM consumer `q=5.2154e-7`，但 point/normal/P 均 exact；C22 对 C11 生产路径重跑，输入、首步、frame `0..3` 两壶 `P/Q/v/w` 再次全零。C23 将既有 C04 真值扩至 12 帧：frame `0..2` 全 exact，frame `3` 的 target 首次有 `w.y=-1.7881393e-7rad/s`、`q.y=+6.0535967e-9`，active 以及两壶 P/v 仍 exact；至 frame `11` 未长成位置/线速度差。C24 只读 parent trace 显示 frame `2..11` 每次 target-ice 均为 `flags=3, cachedSize 0 -> 304`，C20 没有后段 cache 回归。C25 离线 coverage 审计确认 C04 没有 frame-bound static solver rows，且 C14 为不同 tick/run，不能跨运行拼接。 | `partial` | `+4.991889e-7m/s` target support residual、其 frame-2 `0.02392037rad/s` active `w` 分叉和 C11 四帧范围均已 `closed`；C22 再现该结果。C23 已定位新的首个可见 residual 为 static-only tick 的 target ULP angular state，而非 cache header 或 dynamic-dynamic solve。 | 该 closure 只覆盖 C11/C04 的有限窗口。C23 的 target angular residual 尚未与 endpoint 建立因果，不能做数值补偿或声称它解释毫米级终点；完整 14000 静止、14001 历史或 six-shot endpoint 仍未验收。 | `c13_wasm_solver_stage_14000_20260712.json`、`c14_static_intercall_14000_20260712.json`、`c15_target_static_pcm_14000_20260712.json`、`c18_pcm_cache_handoff_14000_20260712.json`、`c19_parent_empty_multi_cache_14000_20260712.json`、`c20_production_multi_cache_lifecycle_14000_20260712.json`、`c21_c03_first_writeback_production_14000_20260712.json`、`c22_c11_production_retest_14000_20260712.json`、`c23_c04_12frame_production_14000_20260712.json`、`c24_c04_12frame_narrowphase_trace_14000_20260712.json`、`c25_static_only_coverage_14000_20260713.json`。 |
| E01 | 六样本终点 | C22 production retest 的首碰均到达（`6/6`）：counts 为 `14000=2,14001=2,14002=2,14003=4,14004=4,14005=4`。可靠终点 active RMSE=`4.1347mm`、max=`7.1550mm`；target RMSE=`20.5827mm`、max=`28.1598mm`。逐局 `14000` 为 active/target=`0.9617/0.5813mm`，`14001` active=`0.0553mm` 且 Unity target 已出界，`14002`=`2.0104/27.2979mm`，`14004`=`5.4144/12.4942mm`，`14005`=`7.1550/28.1598mm`；`14003` 的 Unity final 仍为 timeout_flush。 | `unobserved` | C20 的速度闭合确实将 active aggregate 从 B25 的 `5.4479mm` 降至 `4.1347mm` RMSE，但这只是 endpoint 改善。 | target RMSE 仍超过 `20mm`，且 14002/14005 target 仍为约 `27--28mm`；P6 不通过。该终点残差不得反推为 C20 速度 residual 复发，下一步仍只查 C11 frame 3 后的第一处 persistent state 差。 | `b25_p6_identity_material_current_14000_14005_20260712.json`、`c21_p6_production_multi_cache_14000_14005_20260712.json`、`c22_p6_production_retest_14000_14005_20260712.json`。 |

### 表格使用规则

1. 只从 `unobserved` 行选择下一步；`rejected` 行不得重新开启。
2. `sensitivity` 行只可帮助设计观测，不能直接进入生产修复。
3. 每一次状态变化必须在同一行补上新 artifact、验收范围和撤回范围；不删除旧结论。
4. P6 的执行顺序固定为 `F04 -> B04 -> C03 -> E01`，分别对应 micro-pose、pair lifecycle、
   连续 writeback、endpoint。

## 已冻结事实

1. `Newfrictionstep` Wasm 与本地翻译对同一噪声流逐 tick 一致。
2. Unity fixed tick 的外层顺序是“写 Rigidbody linear/angular velocity -> PhysX simulate(0.01)”。
3. stone、ice cooked object、direct scalar PCM、raw solver-row/consume 公式均只在各自边界闭合。
4. Unity first stone-stone manager 是 new-list；overlap 输入 `target -> active`，solver-facing
   work-unit 为 `active -> target`。
5. 本地 `shape-flag` 路径为 `target -> active / 2 contacts`；`remove/add` 与保持 actor identity 的
   `eDISABLE_SIMULATION` 路径均为 `active -> target / 4 contacts`。后者是目前唯一 source-backed 的
   RigidID 重建候选，但尚不是生产修复。
6. `clearManifold`、cache pointer null、callback modify flag、材质切换、sleep/settle、简单 BVH toggle
   均不得重新作为 first ContactBuffer 主因。
7. 在实际本地 `PxcDiscreteNarrowPhasePCM` 入口，active 相对 Unity 有
   `X=-30.517578125um`、`yaw=-0.000302781346rad`。
8. 用该 micro-pose 的 oracle 诊断补齐后，active->target 本地输出会从 4 点变为 2 点；该结果仅为
   `diagnostic_only`。
9. 上述 micro-pose 差在两个本地 pair 路径中相同，因此**不是** SetActive/private pair lifecycle
   独有的效果。
10. Unity 首个 dynamic-dynamic manager 的 actor-core `body2World` 与首个 stone-stone PCM 消费的
    transform 逐 float 相同；因此 actor-to-`PxsTransformCache` refresh 不是 micro-pose 的来源。

## 两条不可合并的研究链

### A. Common Micro-Pose Chain

```text
Newfrictionstep writes v/w
-> last stone-ice narrowphase
-> static solver writeback
-> pose integration
-> actor-to-PxsTransformCache write
-> first stone-stone PCM reads P/Q
```

验收目标：不注入 oracle，使 active 的 first stone-stone PCM transform 与 Unity 对齐。

当前状态：`unobserved`。链末端的 actor-to-cache transfer 已由 F04A 排除；A2 又证明以 Unity release
solver-body 首行 seed 后，本地连续 stone-ice 路径到 PCM 为 float32-ULP 等价。下一步必须先比较真正
`BESTSHOT/release` 的本地/Unity 初始 actor `P/Q/v/w`，不能再把 `MOTIONINFO` 当起点，也不能回到 activation refresh。

2026-07-12 补充：A4 已发现并诊断排除 release `P.y` 差作为 yaw 主因；F03D/F03F 则证明真正的连续分叉是
local PhysX 返回给下一次 `Newfrictionstep` 的 `wy`：damping 字段相同、前四步相同、第五步出现一个 ULP 的
x64 scalar 与 WebGL scalar recurrence 差。因此本问题**不存在**“少一次 actor/cache refresh”的根因；
后续只能评估 WebGL-compatible PhysX integration backend，不能再寻找 cache、完整 static ContactBuffer 或 SetActive 调用。

### B. Private Pair Lifecycle Chain

```text
existing actor/shape activation state
-> broadphase overlap
-> ShapeInteraction/contact-manager creation
-> work-unit role order
-> first full-manifold reduction
```

验收目标：保持 actor/shape identity 时，自然得到 Unity 的 `active -> target / 2 contacts`。

当前状态：`closed`（仅 14000 first new pair）。`eDISABLE_SIMULATION` 的 identity-preserving handoff 加上
“初始化 quaternion 保留、Reset 仅改 position”已自然产生 Unity 的 `active -> target / 2 contacts` 和相同 normal。
剩余 point/separation 残差来自 active 的最后一 tick transform，属于 A，不得重新打开 actor add/remove、cache 或
manager lifecycle 变体。

## 固定执行门

### Gate A0: 既有 Unity 数据覆盖检查

只解析已有 `14000` 日志，确认最后一个 pre-contact fixed tick 是否同时含有：

```text
post-Newfrictionstep v/w
PxcPCMContactConvexMesh input/output
static solver before/after body state
post-sim actor P/Q
stone-stone PxsTransformCache P/Q
```

输出只能是“字段已存在”或“明确缺少哪一个字段”。不得启动 Unity；若缺字段，才可提出最小补抓理由。

#### A0 结果（2026-07-11，已完成）

受控 `14000` 的同次来源为：

```text
log/unity_runtime_probe_20260710_012403/events.jsonl
log/unity_runtime_probe_20260710_012403/front_half_pcm_summary.json
data/calibration/a0_14000_fixed_tick_coverage_20260711.json
```

| 需要字段 | 既有同次日志状态 | 结论 |
|---|---|---|
| `Newfrictionstep` 写入后的 Rigidbody `v/w` | 缺失；仅有 friction RNG event。 | 不能判断写入相位或 setter 结果。 |
| 最后碰前 fixed-tick ID | 缺失；`fixedUpdateEnterCount=0`。 | 不能用 hook timestamp 断言 stone-ice/static 调用属于同一 tick。 |
| stone-ice PCM 输入/输出 | 部分存在。 | 没有 active-body/tick join，不能选出最后碰前那一条。 |
| static writeback 前后 body state | 部分存在。 | 同样无法绑定至最后碰前 active-body tick。 |
| post-sim actor `P/Q` | 缺失。 | stone-stone PCM transform 不能代替 actor-core 写回边界。 |
| first stone-stone PCM `P/Q` | 存在。 | 这是链 A 的终点真值，而非其生产者。 |
| actor -> `PxsTransformCache` 写入顺序 | 缺失。 | 无法判定 refresh 是否遗漏或时机不同。 |

因此 A0 的唯一有效结论是：**A2 尚不可执行**。不得把旧 stone-ice/static solver 抓取和
first PCM transform 跨时刻拼接成“最后一帧”的证据。下一步仅允许设计最小的只读捕获 schema，
先审查其字段和关联键；尚未授权启动 Unity 或改生产物理。

### Gate A0.1: 最小只读捕获 schema（设计已完成，尚未执行）

静态回查给出了可用写入边界：`func60124` 在 `Newfrictionstep` 返回后调用
`Rigidbody.set_velocity` / `set_angularVelocity`（反编译别名 `f_vbva` / `f_ybva`，实现为
`func32521` / `func32524`）。但该 controller hook（table `11105`）在 A0 的受控 `14000` 运行中
命中为零；因此**不得假定它就是当前标准启动器实际执行的 controller**。

随后对四个拥有相同 `Newfrictionstep -> f_vbva -> f_ybva` 结构的函数逐一回填 table map 和
`movingCurling` 偏移，候选已静态闭合：

| controller | wasm | table | `movingCurling` 偏移 |
|---|---:|---:|---:|
| `FastDCP.FixedUpdate` | `func60202` | `11204` | `212` |
| `AutoDCP.FixedUpdate` | `func60909` | `10825` | `240` |
| `DCP_HumanVSAI.FixedUpdate` | `func60124` | `11105` | `260` |
| `DCP.FixedUpdate` | `func61107` | `10980` | `232` |

静态信息不能判定标准启动器实际选择其中哪一个。为此已在
`tools/reverse/unity_webgl_runtime_probe.js` 加入只读
`installA0FixedTickResolverHook()`：它同时 hook 四个候选、只由实际命中的 callback 递增
`tickSerial`，并从 `f_vbva/f_ybva` 的 runtime dispatch-cache globals (`4659060/4659068`)
惰性解析 velocity/omega setter。首个命中 tick 只用于解析 dispatch；后续 tick 才记录 setter 的
`activeBodyId` 与 vector。该 helper 已通过 `node --check`，但**尚未启动 Unity**，故 runtime controller
选择仍是 `unobserved`。

首次 A0.3 启动预检已验证 browser/probe/resolver 安装成功，但 socket server 没有发送 `READY/GO`；
`ControlledSceneSampler` 仅完成双 client connect，未发 `RESETPOSITION/RESETSTATE/BESTSHOT`，事件流没有
任何 `a0.tick.*`。该空会话已停止，原始日志保留在
`log/a0_fixed_tick_resolver_20260711/unity_runtime_probe_20260711_183636/`，**不是**物理采样或 A0 证据。
再次启动前必须先恢复标准 watcher 的 game-ready 前置状态；不得用 socket 连接成功冒充 controller resolver
已命中。

最小 schema 不抓 hull、BigConvex、整段 solver window 或 endpoint；只保留一个 active body 的环形
两 tick 记录，并在 first stone-stone PCM 时 flush：

| 记录点 | producer / 读取内容 | 必需 join key | consumer / 判别用途 |
|---|---|---|---|
| `tick.enter` | 实际命中的 controller `FixedUpdate`；active managed Rigidbody 与 native body/core/shape identity、进入 `P/Q/v/w`。 | `shotId`, `tickSerial`, `activeBodyId`。 | 定义 fixed tick；验证脚本和物理的相对顺序。 |
| `velocity.write` | `f_vbva`、`f_ybva` after：同一 active body 的完整线/角速度。 | `tickSerial`, `activeBodyId`, `writeSerial`。 | A2 的第一个候选：写入后 `v/w`。 |
| `ice.pcm` | active-rink `PxcPCMContactConvexMesh` before/after：两端 transform、ContactBuffer 摘要。 | `tickSerial`, active shape/core identity。 | 判断 stone-ice narrowphase 输入和输出。 |
| `ice.static.writeback` | active 对 static 的 `solveContact_BStaticBlockWithWriteback` before/after solver body。 | `tickSerial`, `activeBodyId`, solver-body/core identity。 | 判断 static constraint/writeback 是否首先分叉。 |
| `tick.next-enter` | 下一次实际 controller `FixedUpdate` entry 的 active `P/Q/v/w`。 | `shotId`, `tickSerial-1`, `activeBodyId`。 | 不假设 fixed callback exit 等于 post-sim；以下一 tick 入口观察上一物理步的 actor state。 |
| `stone.pcm` | active-target `PxcPCMContactConvexConvex` before：PCM transform-cache `P/Q`，并同次读取 active actor/core `P/Q`。 | `tickSerial`, active/target identity, manager/work-unit identity。 | 链 A 的 consumer；若 actor 与 cache 不同，才追 refresh。 |

严格约束：

1. **resolver preflight** 先找出当前标准启动器真正执行、且能包住 active `f_vbva/f_ybva` 的 controller
   `FixedUpdate` table entry。table `11105` 仅是已知候选，命中前不得用作 tick anchor。
2. `tickSerial` 只能由这个实际 controller 的 entry 递增；所有 native events 只携带“最近 active
   script tick”标签，不得依赖浏览器毫秒时间戳推导同 tick。
3. `activeBodyId` 必须由同一 setter 的 Rigidbody native pointer 与 stone-ice shape/core join 得到；不能
   用 stone index、manager index 或 cache slot 代替。
4. 先以小事件摘要环形保留最近两 tick；只有检测到 active-target `stone.pcm` 才 flush。整个过程只读
   Wasm 内存，不写 filter/cache/shape/solver，不导出重复 hull 数据。

该 schema 的失败条件也固定：任何一条记录没有 `tickSerial + activeBodyId`，或 controller anchor 未命中，
本次 capture 只记为“resolver 未通过”，不能拿来做 A2 字段对比。

#### A0.4 actor-core / cache 判定（2026-07-11，已完成）

为直接回答“激活时是否漏了一次 position/quaternion/transform-cache refresh”，没有继续抓完整
fixed-tick 或 solver 流，而是只重跑一条受控 `14000`。probe 仅在第一次出现两个 stone body 的
`PxsCMDiscreteUpdateTask` 保存 `PxsRigidCore` 的 160B 窗口，并保存同一首碰
`PxcPCMContactConvexConvex` 的两个输入 transform。

```text
原始事件： log/a0_actor_cache_retry_20260711/
             unity_runtime_probe_20260711_191746/events.jsonl
受控样本： data/calibration/a0_actor_cache_14000_retry_20260711.jsonl
审计：     tools/reverse/audit_a0_actor_core_cache.py
产物：     data/calibration/a0_actor_core_cache_14000_audit_20260711.json
```

首个 dynamic-dynamic manager 是 `taskIndex=1`、`flags=611`、`transformCache=(12,9)`、new-list。
其两个 core 的 `body2World` 与随后 PCM 实际读取的 transform 为逐 float 相同：

```text
active core q/p == PCM transform0 q/p: exact
target core q/p == PCM transform1 q/p: exact
```

因此结论是 `F04A=rejected`：**Unity 没有在 actor core 已正确的前提下漏写或晚写
`PxsTransformCache`；PCM 消费的正是 actor core 已有的姿态。** 这直接否定了“本地激活壶时哪一次
cache refresh 少了”是当前 `30.5um / 0.000303rad` 的解释。它也不证明本地 actor core 与 Unity 相同；
micro-pose 的来源仍在 cache 之前，即最后一次 stone-ice static solve、pose integration 或二者的边界。

本次同时实际命中了标准启动器的 `DCP.FixedUpdate`（table `10980`），但旧 resolver 对
`f_vbva/f_ybva` dispatch-cache global 的解码为 null，未记录可靠 setter `v/w`。该未完成的 setter
hook 不影响 F04A 的 core/cache 结论，且不得因为它失败就把 cache refresh 重新列为候选。

#### A0.5 最后 angular-velocity write（2026-07-11，已完成）

旧 resolver 的问题是把 Wasm global 当作线性内存读取。改为从 `build.wasm.gz` internal-call 注册序列
直接恢复 `UnityEngine.Rigidbody::set_angularVelocity -> table 129354 -> func82503` 后，以缓冲方式
仅在首个双动态 manager task 输出一条记录，不再逐 tick 写事件。受控 `14000` 的结果是：

```text
last script angular velocity = (0, 0.18246987462043762, 0)
wy                           = 0.18246987462043762
DCP.FixedUpdate tickSerial   = 215185
native setter calls before task = 1565
```

随后用同一受控 shot 的轻量 getter ring 抓到最后两次完整脚本输入。每条均记录
`get_velocity`、`get_angularVelocity`、同 tick `Random.Range(-0.0002,0.0002)` 与 setter 输出；本地按
native-Y-up 映射 `B2Vec2=(-vz,-vx)` 直接调用 recovered `Newfrictionstep`：

```text
tick 63013: Unity wy=0.1809253842, local=0.1809253814, delta=2.776e-9 rad/s
tick 63014: Unity wy=0.1817278564, local=0.1817278552, delta=1.214e-9 rad/s
```

同一日志还读取了首个 stone-stone PCM 的 active `PxTransform.q`。因此这不是跨运行拼接：
**custom sliding、脚本 getter/read、Newfrictionstep 和 Rigidbody setter 已在末碰前 tick 闭合。**
证据：`data/calibration/a0_last_angular_write_full_inputs_14000_audit_20260711.json`。

下一边界只能是该 setter 随后的最后一次 stone-ice PhysX static solve：先比较其 ContactBuffer 与
solver writeback 前后 body `v/w`，再比较 pose integration 后 actor `P/Q`；不得把差异退回归因于
Newfriction、脚本写入或 transform-cache refresh。

#### A0.6 最后 stone-ice static solve（2026-07-11，已完成：Unity 侧否证）

只运行一条同源受控 `14000`，probe 在首个双壶 manager 出现时 flush 最近八次
`solveContact_BStaticBlockWithWriteback`。每次记录 `PxSolverBody` delta、对应
`Dy::SolverContext.solverBodyArray[bodyADataIndex]` 的真实 `PxSolverBodyData`（pre/post
`v/w/body2World`），以及首个 stone-stone PCM 的 transform。

```text
plan:     data/calibration/a0_static_bodydata_14000.plan.json
sample:   data/calibration/a0_static_bodydata_14000_clean_20260711.jsonl
raw:      log/a0_static_bodydata_20260711_clean/
          unity_runtime_probe_20260711_212959/events.jsonl
```

最后八个 pre-contact static tick 是 `738644..738651`。结论很窄，但确定：

```text
max |static solver delta wy| = 5.826450433232822e-13 rad/s
max |(next yaw - yaw) - wy*0.01| = 1.2930135776531917e-08 rad
last tick: yaw 0.2325841762 -> first PCM yaw 0.2343064221
           observed delta = 0.0017222459
           wy*0.01       = 0.0017222510
```

`PxSolverBodyData` 的 pre/post 值相同是预期行为：它保存 pre-solver state；接触修正存放在
`PxSolverBody.angularState`。实际 static delta 的 yaw 分量只有 `1e-13 rad/s` 量级，不能在一个
tick 产生、也不能在 1560 个同量级 tick 累积出 `0.000302781346rad`。因此
`A0.6 static-solve 假设=closed/rejected`：**Unity 末个 stone-ice static solve 不是这条 micro-yaw 的写回来源；Unity
内部 pose integration 在该窗口按脚本 `wy` 正常闭合。**

这不把“本地 scalar Scene 的同一帧”自动判为等价。唯一下一步是本地诊断夹具：以 Unity tick `738651`
的 actor `P/Q/v/w` 和该 tick 已捕获的脚本输入/噪声为入口，只推进一帧 runtime ice static solve，读取
next actor `Q`。若 local next `Q` 已不同，分叉在 local static solve/integration；若相同，`0.000303rad`
必须早于此窗口，转而做最早 actor-Q 二分。该姿态注入仅用于诊断，禁止进入生产代码。

#### A1.1 同 tick local phase A/B（2026-07-11，已完成：定位积分相位语义）

不再启动 Unity。用相邻的 Unity `PxSolverBodyData` 行 `738650 -> 738651` 作为夹具：前一行提供
精确 actor `P/Q`；同 tick 已捕获的 Rigidbody getter/noise/`Newfrictionstep` setter 提供 pre-write 与
post-write 两种本地 `Scene.simulate(0.01)` 输入。两次都保持 runtime ice、scalar backend、石壶材质
`static/dynamic friction=0`、gravity 和所有其他状态相同。

```text
脚本 getter w:                0.1712034047
Newfrictionstep setter w:      0.1723112315
Unity 下一 Q yaw:              0.2325841762

local pre-write -> simulate:
  position delta = (0, 0, 0)
  yaw delta      = -0.00000085746 rad

local post-write -> simulate:  （当前 step_custom_sliding 语义）
  position delta = (-15.258789um, 0, 0)
  yaw delta      = +0.00001021747 rad
  post w          = 0.1722250730
```

产物：

```text
tools/reverse/audit_a1_local_one_tick_static_integration.py
data/calibration/a1_local_one_tick_static_integration_14000_prewrite_20260711.json
data/calibration/a1_local_one_tick_static_integration_14000_postwrite_20260711.json
```

同时，Unity 下一行的 solver-body `w=0.1722251028`，与 local post-write static solve 的
`0.1722250730` 到 float32 量级一致。故事实不是“Unity 没有使用 setter”，而是两个消费相位不同：

```text
Unity pose P/Q integration:       使用 pre-write getter v/w
Unity next solver velocity state: 使用 post-write setter v/w，经 stone-ice static solve 写回
local high-level Scene.simulate:  将 post-write setter v/w 同时用于 pose integration 与 solver
```

`A1.1 当时的 phase 推断=verified`：**本地 `Newfrictionstep setter -> Scene.simulate` 把 Unity 分离的 pose-integrate
phase 与 solver-velocity phase 错并为同一相位。** 这自然制造每 tick 的微小 position/yaw 偏差；它是
当前 `30.5um / 0.000303rad` 的第一个已证实上游调用语义，而不是 transform-cache、hull 或参数差。

范围仍须严格限定：A/B 是 Unity pose 夹具，尚未允许把 pose 覆写接入生产。下一步只做一个无 oracle 的
14000 local phase-adapter A/B：保留旧 v/w 用于本 tick pose integration，同时让 setter v/w 进入
stone-ice solver/writeback；验收 first PCM 的自然 P/Q。若该单变量关闭 micro-pose，才把这一恢复的时序
语义接入生产路径。

#### A1.2 双 Scene phase-adapter（2026-07-11，已完成：反证，不得接入）

按上节设计的无 oracle 诊断已实际运行：主 Scene 用旧 v/w 生成 pose/PCM，只有 stone-ice 的 shadow
Scene 用新 v/w 求下一速度，然后在首个 stone-stone report 前把 shadow 速度传回主 Scene。它不写 Unity
state，也不改生产接口；实现与输出为：

```text
tools/reverse/audit_a1_2_phase_adapter_14000.py
data/calibration/a1_2_phase_adapter_14000_20260711.json
```

结果提前在 local step `1557` 出现 report，而 Unity entrance 仍相差：

```text
position norm = 10.1013mm
yaw delta     = -0.00542437rad
```

故 `A1.2=failed/rejected`。原因不是 A1.1 的单帧证据失效，而是 shadow Scene 不持有主 Scene 的 native
solver-body snapshot、island、stone-ice cache 和 task history；跨 Scene 传速度不能复刻一个 native step
内部的 snapshot/integrate/writeback 分离。这个 adapter 绝不能进入训练或生产路径。

#### A1.3 native phase order（2026-07-11，已完成：撤回 A1.1 的 phase 根因推断）

受控 `14000` 直接关联同一 active Rigidbody 的脚本 getter、`set_angularVelocity`、静态 solver
实际读取的 `PxSolverBodyData` 和 `PxsDynamics.solverSetupSolve`：

```text
tick 113519 getter wy:                    0.17522142827510834
Newfrictionstep 后 setter wy:             0.17648772895336150
solver-body static-solve 输入 wy:         0.17639960348606110
下一 script getter wy:                    0.17639960348606110
同一 setter 后进入 solverSetupSolve:      是
```

`0.17639960348606110` 不是写前 getter；它是刚写入的 `0.17648772895336150` 经
`bodyCoreComputeUnconstrainedVelocity(...)` 阻尼后的 solver-body snapshot。小 island 的
`solverSetupSolve` 随后执行 `solveVBlock -> integrateCore`。故真实顺序为：

```text
Newfrictionstep -> Rigidbody setter -> solver-body snapshot/damping
-> static solve -> integrateCore -> core P/Q/v/w 回写
```

这与本地 `setter -> Scene.simulate` 的高层相位一致。A1.1 根据 pose 夹具推得的“Unity pose 用
pre-write getter、solver 用 post-write setter”不是原生时序证据，现**撤回其 phase 根因结论**；
`A1.1 phase 根因结论`同步降级为 `rejected`。A1.2 的 cross-scene adapter 仍保持拒绝，因为它不等价于
同一 native Scene。

证据：

```text
log/20260711_a13_phase_bucket/unity_runtime_probe_20260711_224126/events.jsonl
data/calibration/a13_phase_bucket_14000_20260711.jsonl
data/calibration/a1_3_native_phase_order_14000_20260711.json
```

**允许范围更新：**不再修改 phase scheduling，也不再抓 setter/solver snapshot 顺序。微姿态差必须回到
共同的 stone-ice native step 定位；下一条证据只能是 Unity/local 同 tick static ContactBuffer、solver-body
输出或 actor P/Q 的第一处分叉，禁止重新打开 transform-cache refresh、pair lifecycle 或参数扫描。

#### A2 compact continuous trace（2026-07-11，已完成：首个已观测分叉在 start handoff 前）

受控 `14000` 已补齐从首个 active stone-ice solver-body 到 first stone-stone PCM 前的连续 compact trace：
`1560/1560` tick 无缺号，每行含 Unity script getter、noise、linear/angular setter 和 solver-body `P/Q/v/w`。

随后以 Unity trace 首行 `P/Q` 作为**一次性诊断 seed**，本地 scalar Scene 每 tick 只消费同局 Unity
script setter，自由执行 stone-ice `simulate(0.01)`。1559 次比较结果：

```text
max position delta:             0
max quaternion component delta: 1.1920928955078125e-07
max linear-velocity delta:      4.172325134277344e-06
max angular-velocity delta:     1.862645149230957e-07
```

因此从 A2 首行起，local scalar stone-ice static solve、积分和连续 mesh path 都到 float32-ULP 等价；
它们不产生后续 `30.5um / 0.000303rad`。最初将这件事表述为“`MOTIONINFO` 到 native start handoff
不等”是不严谨的：静态复核已经证明 `MOTIONINFO` 根本不是 native start。

```text
local start_motioninfo: protocol y=21.50619812, native P.x=-85.88359833
Unity first solver-body: protocol y=32.47680206, native P.x=-96.85420227
delta protocol y=-10.97060394m

local MOTIONINFO native v/w: (2.19310, 0, -0.00010) / wy=0.00350
Unity first script getter:    (3.40000, 0,  0.00000) / wy=0
```

`a3_motioninfo_semantics_14000_20260712.json` 已将协议 report 放回同一条 trace：第 0 行为
`release_y=32.47680206`、`v=(3.4,0,0)`、`wy=0`；第 403 行为
`motion_y=21.50619049`，与 `MOTIONINFO y=21.5062` 相差 `9.51um`，并且速度/`wy` 只差协议打印精度。
这与 `CurlingStoneNew.OnTriggerEnter(Midline) -> SendMotionInfo()` 的静态调用链一致。

因此 A2 的正确结论是：从 Unity **真实 release solver-body 首行**开始的 PhysX 段已经对齐；未观测且
仍须比较的唯一前置边界是本地 `start_bestshot` 与 Unity `BESTSHOT/release` 的 actor `P/Q/v/w`。`MOTIONINFO`
只能作为 Midline 处的 tail-replay/checkpoint，不能再充当 native Rigidbody start state。

证据：

```text
log/20260711_a2_static_first_diff_inputs/unity_runtime_probe_20260711_232310/events.jsonl
data/calibration/a2_local_static_trace_replay_14000_20260711.json
data/calibration/a2_start_handoff_boundary_14000_20260711.json
```

已禁止继续做 high-level Scene 的 phase A/B；更不能为了让 `MOTIONINFO` 看起来像起点而改写 local
physics。下一步只读比较 local `start_bestshot` 释放后的 actor state 与 Unity trace 第 0 行；若已不同，
根因在 BESTSHOT/Start 的 release 初始化；若相同，才允许回到 A2 首行前的未观测 native setup 边界。

### Decision A7: Backend Compatibility

F03F 已完成：local x64 scalar 与 Unity WebGL scalar 在相同 native field 下产生一 ULP 的
`wy` recurrence 差。下一步不是继续采样或猜 setter，而是做实现决策：提供可执行的 WebGL-compatible
PhysX integration backend，或接受 x64 scalar 无法达到 bit-stable long-horizon yaw 的事实。

| 结果 | 唯一允许追查范围 |
|---|---|
| 决策 | 后续允许范围 |
|---|---|
| 有可执行 WebGL-compatible PhysX integration backend | 只把 A2/F03D 同一 trace 移植到该 backend 验收。 |
| 无该 backend | 记录该平台差异为 P6 的硬边界；不得用 oracle yaw、cache 或样本补偿掩盖。 |

只有 A7 选择并通过 backend 验收，才允许更改生产代码；修改后必须重跑 F03D、A2 与 six-shot P6。

#### A7.1 isolated native `/fp:strict` A/B（2026-07-12，已完成：否证）

为排除“本地 x64 只因 MSVC 浮点优化模式不同而产生一 ULP 递推差”，在不替换生产
`pyphysx` 的前提下，单独从生产所用的 PhysX 4.1.1/`PX_SIMD_DISABLED` 源配置构建了
`/fp:strict` 静态库和隔离绑定。加载器本身先以生产 `.pyd` smoke test 验证，再以严格变体执行
同一 A6 8-tick 窗口：

```text
tools/reverse/audit_a6_angular_getter_recurrence.py --pyphysx-extension <isolated strict pyd>
data/calibration/a7_strict_angular_getter_recurrence_14000_20260712.json
```

首次差异仍完全相同：

```text
25024 -> 25025
Unity wy: 0.009845891036093235
strict x64 wy: 0.009845889173448086
delta: -1.862645149230957e-09
```

故 **`/fp:strict` 不是 Unity WebGL recurrence 的等价实现，也不是可进入生产的修复。** 这只排除
native MSVC 的 floating-point mode；并不声称已证明 Unity WebAssembly 的内部 integration 与 x64
实现只有这一处不同。后续 A7 仅允许评估真正可执行的 Wasm PhysX integration backend；在得到它前，
P6 仍被 A backend compatibility 阻塞。

#### A7.2 Wasm integration-backend feasibility（2026-07-12，已更正：工具链可执行）

本机已完成 Emscripten `3.1.74` 安装，`emcc --version` 可用。此前一次下载中断的记录保留，但“不存在
Wasm toolchain”的结论现撤回。现有 Unity WebGL runtime Wasm 仍不能直接作为独立 PhysX library；要复用它
仍须自行封装完整 PhysX stepper。

#### A7.3 Wasm angular-damping kernel（2026-07-12，已完成：否证 raw damping rounding 根因）

为避免在没有证据时直接移植整个 PhysX，先把 production PhysX 4.1.1
`Dy::bodyCoreComputeUnconstrainedVelocity` 中与 yaw 有关的三条操作原样编译到 Wasm：

```text
angularDampingTimesDT = angularDamping * dt
oneMinusAngularDampingTimesDT = 1.0f - angularDampingTimesDT
angularVelocity *= max(oneMinusAngularDampingTimesDT, 0)
```

以同一 A6 八条 Unity setter 输入，经 Node 执行 Wasm kernel，结果逐行等于 local x64，而非 Unity：

```text
25024 -> 25025
Unity:      0.009845891036093235
x64 scalar: 0.009845889173448086
Wasm kernel:0.009845889173448086
```

证据：

```text
tools/reverse/a7_wasm_angular_damping.cpp
tools/reverse/run_a7_wasm_angular_damping.js
tools/reverse/audit_a7_wasm_angular_damping.py
data/calibration/a7_wasm_angular_damping_14000_20260712.json
```

因此 **A 的首个 ULP 差不是 raw angular-damping expression 的 native/Wasm 舍入差。** 此前“A7 只要做
WebAssembly integration backend 即可修复”的推断撤回。剩余范围重新收紧为：同一 setter 后的完整
stone-ice PhysX tick 中，static-contact/solver-body state/constraint impulse 或 Unity build 的更深层行为。
完整 Wasm PhysX 仍可能是长期 backend 方案，但不再被当作已证实的即时修复。

#### A7.4 A12 native angular-setter orientation transfer（2026-07-12，部分闭合）

本轮没有扩大 static solver/PCM 捕获，只记录 release 后八个 `set_angularVelocity` 调用的 root `+52`
bridge。bridge 内 `+80` 的 `PxTransform` 每 tick 与 actor pose 同步更新；将脚本输入
`(0, wy, 0)` 用该 quaternion 的 PhysX float32 rotate 变换后，前四 tick 的 bridge xyz 逐位相等。
这解释了本地原先直接写 `[0, wy, 0]` 为什么不是 Unity setter 语义。

静态 Wasm 随后给出了这个残差的精确原因：active 壶的 `constraints=80` 为冻结 rotation X/Z，
wrapper 实际做的是 `q.rotate(maskXZ(q^-1.rotate(v)))`，而不是单次 `q.rotate(v)`。将该 locked-axis
projection 以 float32 接入本地后，A12 八条 bridge y/z 与 Unity 对齐，A6 原本 tick `25025` 的首 ULP 消失。

本地已实现同一 rotate 的 opt-in 诊断开关。以 Unity 首个 solver-body pose 作 seed 的 8 tick replay 中，
position 与 yaw 均逐 float32 相同；这证明 ice static solve/pose integration 在该短窗口没有制造 yaw
差，而不构成 no-oracle release 验收。完整 1559 tick 回放的首个 angular feedback 差已从 tick `25025`
推迟到 `25038`，末端从 `-4.93e-6` 收敛到 `-2.64e-6`，但仍未通过，故开关保持默认关闭。

```text
tools/reverse/audit_a12_native_setter_basis.py
tools/reverse/audit_a13_local_pose_basis_replay.py
data/calibration/a12_native_setter_basis_14000_20260712_run14.json
data/calibration/a13_pose_basis_rotation_14000_20260712_run14.json
data/calibration/a14_pose_basis_locked_projection_14000_20260712.json
data/calibration/a14_full_release_locked_projection_14000_20260712.json
```

#### A7.5 setter Wasm dispatch 已定位（2026-07-12，静态反查完成）

本地已从现有 `build.wasm.gz` 的 table element 直接复原真实调用链；此前将 table index 当作
function number 的表述不准确，现已更正：

```text
table[129354] -> func82027
func82027      -> func72559(native Rigidbody root, Vector3*)
func72559      -> root+52 的 vtable slot 168 写入 bridge target
```

`func72559` 先复制 Vector3，再按 root `+136` 的 flags 选择 Transform/coordinate conversion 分支，最后才
调用 root `+52` 对象的方法。故 bridge 的 ULP residual 属于 **Unity Rigidbody wrapper 的变换分支**，而不是
PhysX `PxQuat::rotate`、unconstrained damping 或 stone-ice solve。现有本地 rotate 仅是该 wrapper 在当前
输入下的近似投影，不能提前设为生产默认。

下一步只允许将 `func72559` 中实际命中的 branch 提取成独立 float32 helper，并用 A12 的八条
`input Vector3 -> bridge xyz` 回放验收；通过后才重跑 1559 tick。无需重新采样 Unity。

#### A17 完整 scalar PhysX Wasm Scene smoke（2026-07-12，已通过）

不再只运行一个 damping kernel。以现有 scalar PhysX 4.1.1 source 为基础，Emscripten `3.1.74`
已成功构建 `PhysX_static.a`、`PhysXCommon_static.a` 与 `PhysXFoundation_static.a`。由于原始源码没有
Emscripten platform stanza，审计构建复用 Linux/Clang 配置并只在 `EMSCRIPTEN` 下显式定义
`PX_SIMD_DISABLED`；x64 专用 BVH4/SSE source override 仅保留给 MSVC。Extensions、Vehicle、Cooking、PVD
未纳入第一阶段，因为它们不是 `PxScene.simulate` 的依赖。

最小 Node/Wasm 程序已真正创建 Foundation、Physics、Scene、dynamic box 和 shape，并执行：

```text
scene.simulate(0.01)
scene.fetchResults(true)
result: p = (0, 0.999019027, 0)
```

这证明 Wasm 后端能够执行完整 scalar `PxScene` 的创建、调度与 pose integration，不是“只编过单个
数学表达式”。它**不**证明 14000 已对齐，也不允许立即替换训练后端；下一项是把已捕获的单壶 runtime
hull、material、inertia 和 release setter 输入接入这个 backend，并先验 14000 的 pre-contact P/Q。

产物：

```text
tools/reverse/a17_wasm_physx_scene_smoke.cpp
data/calibration/a17_wasm_physx_scene_smoke.js
data/calibration/a17_wasm_physx_scene_smoke.wasm
```

#### A18 Wasm runtime-hull release replay（2026-07-12，已完成，seeded A 链通过）

Wasm backend 已进一步接入现有资产：recovered stone source 的 `512` 顶点经 native Y-up 重排和
`PxMeshScale=(0.11270001,0.115,0.11270001)` cooking；Unity source-once ice 的 `121` 顶点、`200`
triangles、mesh scale `(4.99799156,1.01600003,0.99568027)` 和 static pose
`(-85.98600006,14.30478477,55.56601715)` 进入同一 scalar `PxScene`。随后没有停在 source cook：程序在
覆写前强制校验本地 `Gu::ConvexMesh` buffer 恰为 Unity 的 `4008B`，并将已有 runtime hull 和由该 hull
确定性重建的 BigConvex 三段 raw array 写入 native object：

```text
runtime-hull-patched bytes=4008 big=(3072,512,384)
```

再以 Unity 14000 A2 trace 的 release P/Q 和 `1559` 条真实的 linear/angular setter 驱动该 Scene：每 tick
写入捕获的线速度、按已验证的 X/Z lock projection 写入角速度，再执行 `simulate(0.01)`。初版曾出现第 `12`
tick 的假性 stone-ice angular writeback：

```text
initial A18 material combine:   PhysX default Average
stone(0) + ice(0.02):           0.01 friction  <- Unity 应为 0
max position delta:             30.479431mm
max quaternion component delta: 0.012968041
```

这不是 Unity 私有 integrator 差异。00 号资产记录已明确 Ice/Bouncy 的 friction combine 都为 `Multiply`；A18
漏设该字段，默认 `Average` 将滑行壶的 `0` 和冰面的 `0.02` 错合成 `0.01`，接地后制造了不存在的摩擦角冲量。
补齐双方 `PxCombineMode::eMULTIPLY` 后，同一 executable、同一 runtime hull、同一 setter trace 的结果为：

```text
max position delta:             0
max quaternion component delta: 1.1920929e-7
max post-sim angular delta:     2.23517418e-7
Wasm final P:                   (-69.880935669, 14.419784546, 54.174278259)
Unity trace final P:            (-69.880935669, 14.419784546, 54.174278259)
```

因此 A18 已证明：Wasm scalar PhysX、Unity runtime hull/BigConvex、ice geometry、`Multiply` material combine 和
captured release setter stream 能在实际 `PxScene` 中逐 float32 ULP 对齐。它尚不是生产 A 链闭合，因为当前
setter stream 是 Unity 已捕获的诊断输入；下一步只允许把 recovered no-oracle `Newfrictionstep` 递推接入该
Wasm backend，再以相同 1559 tick 门槛验收。

补充反证：A18 初版使用 `PxQuat::rotate` 投影 locked-axis setter；随后将其替换为 A12 已反编译出的
float32 逐操作 `q.rotate(mask(q^-1.rotate(v)))`。在 `Multiply` 对齐后两种实现都落在同一 ULP 门槛，故 wrapper
不再是 A18 的主差异。

release-height 反事实也已完成：将 Unity release P.y 人为降至旧本地的 `14.419784546` 会在最初下落窗口产生
最多 `11.633873mm` 的暂态高度差，但在 captured setter 驱动下最终 P/Q/W 仍回到同一 ULP。它是真实 release
边界差异，但不是这条 seeded replay 的后续 yaw 根因。

#### A19 live-feedback A 链闭合（2026-07-12）

`A19` 不再把 Unity 已捕获的 linear/angular setter 当输入：每个 fixed tick 只向实际抽出的
`Newfrictionstep` Wasm 提供本地 persistent scalar Scene 上一 tick 的 live `v/w` 与已捕获 noise；其返回值
再写回同一 Scene 并 `simulate(0.01)`。因此它检验的是完整的 no-oracle feedback recurrence，不是 A18 的
seeded setter replay。

首个有效修复位于 `Dy::copyToSolverBodyData(...)`：本地 PhysX 在 solver-body snapshot 阶段把
`FreezeRotationX/Z` 的 `data.angularVelocity.x/z` 直接清零；Unity WebGL 的锁定投影不会在这个边界丢弃
脚本写入后留下的极小横轴分量。保留这两项到 solver-body setup，仍让 `integrateCore` 在最终 motion state
执行锁定投影，得到：

```text
1559 ticks, no captured setter/pose input after local release
final position delta:           (0, 0, 0)
max quaternion component delta: 5.51342964e-7
first live Newfriction input delta: tick 25083
first setter delta:             tick 26394
```

此前尝试同时取消 `integrateCore` 的 X/Z 清零，结果与上述数字逐字段相同，故该后置清零不是根因，已恢复。
可复现的 source patch 保存在：

```text
tools/reverse/patches/physx_a19_solver_body_locked_angular_snapshot.patch
tools/reverse/run_a19_live_feedback.js
data/calibration/a19_wasm_live_feedback_lock_snapshot_14000_20260712.json
```

结论严格限定为：**A 链在 14000 的 release 到 first-PCM 前 1559 tick 已闭合到 `5.6e-7` quaternion-component
数值门槛，原先约 `0.000303rad` 的 common micro-pose 不再是 B 链的输入阻塞。** 这不等于 B 链已经闭合；
下一步只能把这条 integration backend 接到 identity-preserving 的 B16 路径，检查 Unity 的
`active -> target / 2 contacts` 是否自然出现。

产物：

```text
tools/reverse/generate_a18_wasm_scene_assets.py
tools/reverse/a18_wasm_scene_assets.generated.h
tools/reverse/a18_wasm_physx_geometry_scene.cpp
data/calibration/a18_wasm_physx_geometry_scene.js
data/calibration/a18_wasm_physx_geometry_scene.wasm
```

### Gate B0: 隔离 pair 创建

仅在 A2 的 active P/Q 已自然闭合后进入。oracle pose 只可作为诊断夹具，不能进入生产：

```text
overlap volumes
-> ShapeInteraction creation
-> contact-manager/new-list
-> work-unit rigid/shape role
-> first PCM output
```

该 gate 只接受“第一个不同字段/调用顺序”作为结果；不接受交换 addActor 次序、手填 cache slot 或
feature bytes 作为修复。

#### B20 同源首 PCM 验收（2026-07-12，原始观测；其 backend 推断已由 B21 撤回）

本轮只使用一条新的受控 `14000` 同源运行，运行时日志同时含 `A0/A2` setter trace、首个
`PxcPCMContactConvexConvex` 和 finalizer；之后的所有 B20 比较均离线完成，不再启动 Unity。

```text
Unity raw:  log/b20_same_run_contactbuffer_20260712_retry2/
            unity_runtime_probe_20260712_171259/events.jsonl
B20 no-oracle replay:
  data/calibration/b20_wasm_pair_same_run_14000_20260712.json
  data/calibration/b20_same_run_contactbuffer_audit_14000_20260712.json
```

`B20` 采用唯一允许的 identity-preserving 实现：两只 `PxActor/PxShape` 在同一 Scene 中持续存在，target
后 active 通过 `eDISABLE_SIMULATION` 启停，启用后按 Unity 已确认的 pose/shape refresh 次序进入 new pair；
它不使用 `remove/add actor`、Unity PCM pose、cache 或 setter oracle。结果已经自然达到：

```text
solver-facing role:              active -> target       (Unity 相同)
first contact count:             2                      (Unity 相同)
Pxc work-unit flags/status:      611 / 0                (Unity 相同)
frictionPatchCount / edgeIndex:  0 / 2                  (Unity 相同)
active PCM P max delta:          22.888um
active PCM Q max component:      7.775e-5
```

但 ContactBuffer 尚未通过，且差异已不能归因于此前的 A 链：

```text
max point distance:              0.465956mm
max normal distance:             0.0257087
max separation delta:            27.4405um
```

最强反证是诊断夹具。保留 B20 的同一 actor/pair history，只在最后一次 Scene 触发前临时置入这条日志的
Unity exact PCM transform；B20 的 transform 遂逐 float 相等，但仍输出同一错误 facet normal，第二点偏移
`0.488817mm`。因此 A 的末 tick 微姿态、actor-to-cache refresh 与 pose 时相均不是该 residual 的根因：

```text
data/calibration/b20_wasm_pair_exact_pcm_diagnostic_14000_20260712.json
data/calibration/b20_same_run_exact_pcm_diagnostic_audit_14000_20260712.json
```

同时，本地 callback 已直接读取第一次 `PxcDiscreteNarrowPhasePCM` 的 cache/work-unit。Unity before cache
header 的 feature bytes 是 `A=[66,17,176,4] / B=[0,9,0,0]`，B20 新 manager 为全零；这是真实 lifecycle
差异，但把这 8 bytes 作为严格 opt-in diagnostic seed 写入 B20 后，normal/point/separation **完全不变**，
故它不是当前 first ContactBuffer 分叉的因果。单变量 `-ffast-math` Wasm rebuild 也不改变结果。证据：

```text
data/calibration/b20_wasm_pair_feature_seed_diagnostic_14000_20260712.json
data/calibration/b20_same_run_feature_seed_diagnostic_audit_14000_20260712.json
data/calibration/b20_wasm_pair_fastmath_14000_20260712.json
data/calibration/b20_same_run_fastmath_audit_14000_20260712.json
```

**原始推断（撤回范围）：** 当时只比较了 B20 Scene 的本地 transform 与 Unity exact transform，且本地 target
在 Reset 时被错误覆写为 identity；因此不能由该结果推出“Emscripten PCM binary 与 Unity binary 不同”。该推断
已被 B21 的同输入 direct unit 完整否证，历史产物保留，仅不再作为 backend 结论。

#### B21--B23：direct discriminator 与 Reset quaternion（2026-07-12，14000 B 链闭合）

用户提出的“单次 direct PCM 三方判别”已实际执行。B21 用 B20 同一个 patched runtime hull、BigConvex、
scale 和 Unity first-PCM transform，绕过 `PxScene`、manager 和 cache，直接调用 `Gu::pcmContactConvexConvex`：

```text
local x64 scalar direct PCM = Unity
local Wasm scalar direct PCM = Unity
fresh cache / Unity feature-seed cache = Unity
```

故“PCM source/binary reduction 不同”被否证。B22 随后把**同一 Scene**实际调用的 shape geometry、
transform、resolved `NarrowPhaseParams` 交给 fresh direct PCM；fresh direct 与 Scene 输出逐位相同，排除 cache/
manifold 作为当前分叉来源。

最后的 transform crosscheck 给出单一判别：

```text
Unity active + Unity target:  point/normal = Unity
local active + local target:  point max 0.465956mm, normal max 0.0257087
Unity active + local target:  仍错误
local active + Unity target:  normal exact, point max 0.020543mm
```

这说明大分叉来自 target 被本地 `b20_reset` 写成 identity，而 Unity 的 Reset 只写 position、保留初始化
quaternion。B23 改为 target 创建时设置一次共享 prefab basis `q=(6.65790267e-8,0,0,1)`，随后每次 Reset
只替换 `p`、保留 `q`。无 Unity PCM/cache/pose/setter 注入下，14000 得到：

```text
role/count:              active -> target / 2
normal:                  float exact
max point distance:      0.020543mm
max separation delta:    0.023015mm
```

后两项来自 active first-PCM transform 仍差 `22.888um / 7.775e-5`，不是 B lifecycle 残差；B23 不能作为
P6 endpoint 通过证据。产物：

```text
tools/reverse/audit_b21_wasm_direct_pcm.js
tools/reverse/audit_b22_transform_crosscheck.js
data/calibration/b21_wasm_direct_pcm_audit_14000_20260712.json
data/calibration/b22_scene_direct_discriminator_14000_20260712.json
data/calibration/b22_transform_crosscheck_14000_20260712.json
data/calibration/b23_reset_preserve_q_b20_14000_20260712.json
data/calibration/b23_reset_preserve_q_contactbuffer_audit_14000_20260712.json
```

#### B24：首 PCM 材质恢复时相（2026-07-12，14000 point/normal 闭合）

对 B23 的最后一个 active tail tick 增加了只读记录后，旧 predictive bridge 的本地 `wy=0.15238014`，
而 Unity 同 tick script getter 为 `0.16809762`；最后 setter 因此少 `0.01569612rad/s`。原因是 bridge 在
**尚未进入** stone-stone PCM 的前一物理 tick 就把 active material 从 `0` 恢复为 `0.6`，让 stone-ice
Multiply friction 多作用一 tick。

单变量地把 material restore 改为“current actor pose 已在 `FIRST_PCM_CENTER_DISTANCE` 内”，target wake-up
仍可使用 predictive shell。结果：

```text
tail pre-PCM position:          exact
tail pre-PCM quaternion max:    3.6508e-7
tail angular setter delta:      5.8963e-8 rad/s
first ContactBuffer point:      exact
first ContactBuffer normal:     exact
first separation max delta:     6.1467e-8 (约 33 float32 ULP)
```

这不是 endpoint 拟合，也没有注入 Unity pose/cache/setter。实现已同步进 `unity_front_half_physx.py`：
预测 shell 只负责 wake target；`restore_active_friction_at_pcm_shell` 只在当前 pose 已进 shell 时才恢复材质。
P5 material audit 仍验证 first solver friction=`0.36/0.36`、work-unit flags=`611`。该范围内 B 已闭合；
separation residual 留给 A，不得再改 B 参数。

#### B25：六样本 identity + current-material 验证（2026-07-12，改善证据，非 P6 通过）

以 persistent hybrid Scene 跑 `14000--14005`，只启用已验证的 `eDISABLE_SIMULATION` identity path、
locked-axis setter wrapper 与 current-pose material transition，关闭 contact-modify friction override：

```text
first stone-stone contact:      6 / 6 reached
reliable active endpoint RMSE:  5.448mm, max 8.945mm
reliable target endpoint RMSE:  18.691mm, max 27.030mm
14003 Unity final:              timeout_flush，不计 endpoint 门槛
```

这证明 B 语义在连续 six-shot 中不是单条改善；但 P6 **仍未通过**：14001 Unity 已出界、本地仍在场，
14004 target 超过 20mm，且 hybrid x64 Scene 的 14000 first contact 仍为 4（其 active entrance 不等于
B20 同源 Wasm 输入）。这些是 A/backend/cleared lifecycle 的待验收边界，不允许再把 B04 重开。

产物：

```text
data/calibration/a20_b20_tail_handoff_14000_20260712.json
data/calibration/a20_material_current_pose_14000_20260712.json
data/calibration/a20_material_current_pose_contactbuffer_14000_20260712.json
data/calibration/b25_p6_identity_material_current_14000_14005_20260712.json
tools/reverse/audit_hybrid_p6_endpoint_sixshot.py
```

#### C03.1：首个 dynamic-dynamic writeback 与 C07 联合窗口（2026-07-12，已完成）

`--c03-first-writeback` 已在同源 14000 运行中完成。它证明旧 C03 的首帧分叉不是 PCM 或 solver 公式：
本地把 active friction 在该 step 前恢复为 `0.6`，Unity 仍为 `0`，使 stone-ice Multiply friction
额外作用一次。生产路径现改为在首个 dynamic-dynamic step 完成后才恢复 `0.6`；以 Unity pre-state
作诊断 seed 时，首帧 post-state 的 active/target `P/Q/v/w` 逐 float 相同。

随后 C07 在同一局同时开启 `--c04-dynamic-window 4` 与 `--c05-pcm-window 6`。实际得到 4 个 solver
frame 和 4 次 PCM call，且二者可按 transform 精确 join：

```text
frame 0 / PCM seq 0:  PCM exact，post solver-body exact
frame 1 / PCM seq 1:  PCM exact，post solver-body 仅 float32 ULP 级
frame 2 / PCM seq 2:  PCM 仍 exact，但 post active `w` 差 0.02392037rad/s，q.y 差 1.187697e-4
frame 3 / PCM seq 3:  PCM 已无 contact，差异继续扩大
```

这排除了“persistent PCM feature/cache 使第三帧 ContactBuffer 分叉”：C07 的每次 Unity ContactBuffer 与
同初值 local trace 均逐 float 相同，cache 的有效 feature 前缀也一致。它也不允许将 ULP 级 frame 1
差异直接叫作根因；当前第一处足够大的差异发生在 frame 2 的 **PCM 之后、actor/core post-state 之前**。

C08 已完成离线逐字段对照。frame 0/1 的 prepared friction rows 完全相同；frame 2 的 ContactBuffer 仍完全
相同，但第一条 friction row 已出现 `raXn/bias/targetVel` 差异。这证明分叉在 `getFrictionPatches()` 读取上帧
`FrictionPatch` 后到 `setupFinalizeSolverContacts()` 写 row 之间。清 X/Z lock flag 不改变该结果。

raw ContactBuffer 的 `targetVel=normal` 不能直接等价为本地 `PxContactSet::setTargetVelocity(normal)`：该诊断会令
首帧 `P` 已差 `2.84mm`，故已撤回并重新构建无此修改的 hybrid binding。下一步只离线比对 Unity/local frame 1
结束后的 `FrictionPatch` anchor、broken/material flags 与 frame 2 的 `bodyFrame0/bodyFrame1`，定位究竟是 patch
复用条件还是 anchor 写入语义不同。除非这些字段在 C07 原始窗口不可恢复，禁止再启动 Unity。

补充 C09：本地 `FrictionPatch` raw 已导出；frame 2 默认路径逐字复用 frame 1 的 anchor。仅将两只 stone
材质标为 `eDISABLE_STRONG_FRICTION` 会令 frame 2 row 的 `raXn/bias/targetVel` 回到 Unity ULP，但 C04 的
post-state 仍保持原差。因此它只能证明 strong-friction patch 是真实参与项，**不能**用 material flag 取代
Unity 的完整持续 solver 语义。

#### C10：solver tail 覆盖判别（2026-07-12，已完成：C07 不能再离线闭合）

`audit_c10_persistent_solver_state.py` 只读取 C07 Unity raw 与同局 local trace。frame 1 的前四个
`solveContactBlock` 调用中，两条 applied normal force 的 before/after 均逐 float 相同；这确认 C08 的 row
分叉不是已捕获 prefix 内的 force-accumulator 分叉。随后 local 还有第 5 个 regular block：

```text
after captured iteration 3: normal = [14.81166458, 0.04515171]
local regular iteration 4:   normal = [14.90660954, 0.05549240]
```

PhysX `DySolverControl.cpp` 对 velocity iterations `6/1` 的实际路径是五次 `gVTableSolveBlock`，最后一次
`gVTableSolveWriteBackBlock`；并非 conclude path。C07 的 Unity hook 当时把 `dynamicSolves` 硬限为 `4`，且未
hook `120352/solveContactBlockWithWriteback`。而这两个未观测调用完成后，下一帧 active 已有
`w.y=-0.02392037rad/s`、`q.y=-1.187697e-4` 差。因此 C07 已无更多可恢复字段，不能离线判别到底是第五次
regular call 还是 final writeback 首先不同。

这只是**覆盖缺口闭合**，不是“tail 就是根因”的结论。下一次只允许最小只读捕获第五次 regular call 和一次
final writeback 的 constraint applied force、friction applied force、两只 `PxSolverBody` before/after；不记录端点，
不改变 Scene 参数。

#### C11：完整 dynamic tail（2026-07-12，inter-call 首字段已观测）

C11 只增加 `120352/solveContactBlockWithWriteback` 的只读 hook，并把 `120346` regular call 上限从 4 提到 8。
同一 `14000` controlled run 的 collision frame 得到完整 `5 regular + 1 writeback`。以同次 Unity C11 pre-state
重放 local x64 hybrid 后，结果按求解时序为：

```text
prepared normal rows:           exact
prepared friction rows:         exact
regular 0 normal forces:        exact
regular 0 starting solver body: exact (both zero)
regular 1 entry target body.y:  local - Unity = +4.991889e-7 m/s
regular 3 friction[1] force:    local - Unity = +3.870726e-6
final writeback friction[1]:    local - Unity = +1.548290e-5
```

因此第二条 friction applied-force 不是第一处差；它是在 target 的 `PxSolverBody.linearVelocity.y` 已于 regular 0
返回到 regular 1 进入之间偏离之后才出现。该字段原先被表述为 dynamic-consume 差异；该归因已由 C13 撤回。
正常/摩擦 row、normal force、pair lifecycle、cache anchor 都不能用作生产补偿。

本地 trace 为满足同 boundary compare，增加了 `SolverContactFriction.appliedForce` 和 normal row 的只读导出；
重编后只离线重放 C11，没有再次采样 Unity。

产物：

```text
log/c07_joint_solver_pcm_20260712/unity_runtime_probe_20260712_201550/events.jsonl
data/calibration/c07_c04_joint_solver_friction0_14000_20260712.json
data/calibration/c07_c05_joint_pcm_friction0_14000_20260712.json
data/calibration/c10_persistent_solver_state_14000_20260712.json
tools/reverse/audit_c10_persistent_solver_state.py
log/c11_solver_tail_20260712/unity_runtime_probe_20260712_205657/events.jsonl
data/calibration/c11_c04_solver_tail_friction0_14000_20260712.json
data/calibration/c11_solver_tail_audit_14000_20260712.json
tools/reverse/audit_c11_solver_tail.py
```

#### C12 高层 Wasm Scene 注入（2026-07-12，阶段无效，撤回范围）

为把 C11 的 same-pre-state 放进 executable scalar Wasm backend，初版 `C12` 将 C11 frame 0 的
`PxSolverBody` entry state 写入 B20 public Scene，再调用两次 `Scene.simulate()`。该入口已经位于
`solverSetup` 之后：其 `v.y=-0.0981` 已含本 tick 的 gravity/pre-integrate。高层 `simulate()` 会再执行
gravity、solver-body setup 与 integrate，因而第一步即出现约 `-0.1962m/s` 的重复重力项；其后 Contact 也不再是
C11 的同一 solver-stage。该输出不可用于 Unity/Wasm、x64/Wasm 或 friction-patch 的任何结论。

```text
tools/reverse/audit_c12_wasm_dynamic_consume.js
data/calibration/c12_wasm_dynamic_consume_14000_20260712.json
```

撤回范围仅限“以 public `PxScene.simulate()` 消费 C11 solverSetup snapshot”的测试设计；其后 C13 已完成直接
solver-stage 判别，结论见下。不得再次从高层 Scene 重放。

#### C13 Wasm solver-stage 判别（2026-07-12，单次 consume 已闭合）

`C13` 以 C11 frame 1 的每一条 raw `PxSolverBody(32B)` 与 `constraint(304B; 320B 仅为观测窗口)` 为输入，
绕过 `PxScene.simulate()`，直接调用同一 scalar PhysX 的 `Dy::solveContactBlock`。每个 regular call 都各自试验
`doFriction=false/true`，没有改动原始 row、force 或 body。

```text
regular 0..2: Unity == Wasm(no-friction), float exact
regular 3..4: Unity == Wasm(friction),    float exact
local x64:     对其各自输入的每次 consume 使用同一模式
```

所以 C11 的 `+4.991889e-7m/s` 不是 x64 或 Wasm 的单次 dynamic-contact 公式差，而是在 regular 0 exit 与
regular 1 entry 之间对同一 target `PxSolverBody` 的外部写入/调度差。该结论仅关闭单-call consume；尚未命名
inter-call writer，亦不证明 full writeback 或 endpoint。

```text
tools/reverse/c13_wasm_solver_stage.cpp
tools/reverse/audit_c13_wasm_solver_stage.js
data/calibration/c13_wasm_solver_stage.js
data/calibration/c13_wasm_solver_stage.wasm
data/calibration/c13_wasm_solver_stage_14000_20260712.json
```

#### C14--C16 target-ice static support discriminator（2026-07-12，first field observed）

`C14` 的 local solve-block trace 将 C11 regular 0 exit 与 regular 1 entry 间的 writer 定位为 target 对 ice 的
`solveContact_BStaticBlock`。target 输入 solver-body `v.y=-0.0980999991`、P/Q 与 body data 均与 C11 Unity
边界相同；local static output 为 `0.0981201455`，Unity regular 1 entry 为 `0.0981196463`，差
`+4.991889e-7m/s`。把同一 local raw body/constraint 归一 ABI 后分别交给 x64 和 scalar Wasm static solver，
两者输出逐位相同，故不是 static consume backend rounding。

`C15` 从既有 historical Unity raw 中挑出 transform 与 C14 target **逐 float 相同**的 convex-mesh call；fresh
direct PCM 的 5 points/normals/separations 逐位相同，关闭 cooked mesh/direct geometry 假设。`C16` 再读取
persistent Scene 的实际 target-ice PCM：points 与 face index 仍相同，但 Unity cache 为
`multi-manifold, cachedSize=0`，local 为 `multi-manifold, cachedSize=304`；随后的 separation 最大差
`6.4524e-9m`，早于 static prepared bias 和目标 `v_y` 差。

这只证明第一处可观测字段差是 multi-manifold payload，并不证明“清空 cachedSize”本身是生产语义。下一实验
只能对该单字段做 diagnostic-only A/B：保持 multi-manifold flags/pointer lifecycle，不改 row、material、force 或
solver，观察 separation 与 `v_y` 是否同时闭合。

```text
tools/reverse/c14_wasm_static_solver_stage.cpp
tools/reverse/audit_c14_wasm_static_solver_stage.js
tools/reverse/audit_c15_target_static_pcm.py
data/calibration/c14_static_intercall_14000_20260712.json
data/calibration/c14_wasm_static_solver_stage_14000_20260712.json
data/calibration/c15_target_static_pcm_14000_20260712.json
data/calibration/c16_target_static_scene_pcm_14000_20260712.json
```

#### C17 empty multi-manifold payload A/B（2026-07-12，diagnostic causality established）

只在 `PxcPCMContactConvexMesh` 入口对已观测不一致的 target-ice multi-manifold payload 执行
`clearManifold(); mCachedSize=0`，保留 cache pointer、`multi-manifold` flag、transform、material、prepared row 和
solver。C17 的 local target PCM **method hook 内**调用前后均为 `cachedSize=0`，五条 separation 逐位等于 Unity
historical capture；C11 四个 solver frame 的 active/target `P/Q/v/w` 也全部逐 float 相同，原
`+4.991889e-7m/s` target support residual 消失。

此结果为 `diagnostic_only`：它证明 payload 是因果输入，不授权把 hook 接到 production。C18 随后证明 C17
并不会阻止 parent 在 method 返回后再次写入 `304B`，故不能把它表述为“禁用了 cache serialization”。下一项必须
静态恢复 Unity per-frame `PxsContactManager -> work-unit cache` handoff 在哪个边界把 payload 呈现为空，再以同一
boundary 实现生产语义。

#### C18--C20 parent cache handoff（2026-07-12，C11 target support residual closed）

`C18` 只读复核两类已有数据：historical Unity 的 `169` 条 stone-rink `PxcPCMContactConvexMesh` wrapper input
均为 `manifoldFlags=3/cachedSize=0`；而 local C17 即使在 method 内清 payload，下一次 parent entry 仍会重新看到
`304B`。静态反编译的 Unity `func70739` 也含标准的 post-PCM serialization。因此 C17 的位置晚于真正差异，不能
当作 production 实现。

`C19` 将单变量移到 `PxcDiscreteNarrowPhasePCM` parent entry：保留 stream buffer 地址，但先把其中的
`MultiplePersistentContactManifold` 重写为 empty serialized payload 并设 `cachedSize=0`。parent trace 随后逐次
呈现 Unity 同形的 input，并在 call 完成后按原 PhysX 流程正常写回 `304B`：

```text
before target/active-ice PCM: flags=3, cachedSize=0
after  target/active-ice PCM: flags=3, cachedSize=304
```

该 C19 diagnostic 的 C11 四帧全 exact。`C20` 再把相同逻辑独立为
`set_scene_narrowphase_unity_multi_cache_lifecycle_enabled(true)`，由
`PersistentPhysxFrontHalfScene` 默认启用；C20 未开启 C17/C19 diagnostic，仍得到：

```text
C11 frame 0..3 active/target P/Q/v/w: float exact
target static-support vy residual:    0
```

因此 production 已关闭的范围是 C11 中 target-ice persistent multi-cache handoff 导致的
`+4.991889e-7m/s`。这不关闭完整 C03，也不改变 six-shot endpoint 结论。

```text
data/calibration/c17_target_static_empty_payload_14000_20260712.json
```

#### C23--C24 post-frame-3 offline extension（2026-07-12，未发现 cache 回归）

未启动 Unity。C23 使用既有 `C04` 的 `12` 个 dynamic solver exit core 作为真值，将同一个
Unity pre-state diagnostic 延长到 frame `11`。frame `0..2` 的两壶 `P/Q/v/w` 仍逐 float 相同；首个
可见差在 frame `3` exit，且该帧 `dynamicSolves=0`：target 的 local `w.y` 比 Unity 小
`1.7881393e-7rad/s`，`q.y` 高 `6.0535967e-9`。active 以及两壶位置、线速度仍为零差；该 target
ULP residual 到 frame `11` 仍未形成位置或线速度差。

为排除“C20 只在前四帧有效”，C24 只读导出 production parent narrowphase header。frame `2..11` 的每次
target-ice multi-manifold 都满足：

```text
flags=3, before cachedSize=0, after cachedSize=304
```

因此新的 ULP 差发生在没有 dynamic-dynamic solve 的 static-only tick，且不是 production cache header
回到旧的 `304 -> 304` 生命周期。它尚未证明 static solver、integrate 或 endpoint 的哪一项是根因；禁止补偿。

产物：

```text
tools/reverse/audit_c03_same_run_dynamic_writeback.py
data/calibration/c23_c04_12frame_production_14000_20260712.json
data/calibration/c24_c04_12frame_narrowphase_trace_14000_20260712.json
```

#### C25 static-only coverage audit（2026-07-13，已完成）

只读审计确认：C04 的同源 Unity 日志仅有 `12` 条 `c04.dynamic_solver_frame` exit，**没有**可与
frame `3` join 的 target-ice static solver-body before/after 或 post-integrate core 记录。C14 虽有 static
support ring，但其 `tickSerial=27021`，C04 为 `55884`；二者不是同一运行，禁止用它们拼接 synthetic
static tick trace。

因此 C25 的有效结果是覆盖缺口，不是新的物理根因：现有 artifacts 只能证明首差落在 frame `2 -> 3`
的 static-only interval，不能区分 solver-body 输入、static writeback 与 integrateCore。下一步必须是最小
同次只读 capture，且只记录该一帧 target 的三个边界字段。

产物：

```text
tools/reverse/audit_c25_static_only_coverage.py
data/calibration/c25_static_only_coverage_14000_20260713.json
```

#### C26 same-run target static window（2026-07-13，Unity boundary 已捕获）

同一 `14000` 的 C04 frame `3` (`tickSerial=50496`) 现已捕获 target core entry/exit 与其 target-ice
static wrapper。target `PxSolverBodyData` 在 wrapper before/after 完全不变：

```text
entry w.y / solver-body w.y: 0.3028600812
static wrapper after data w.y: 0.3028600812
solverSetupSolve exit core w.y: 0.2700730264
```

同时 exit core 已完成 P/Q 积分。这符合 `PxSolverBodyData` 是 pre-solver snapshot 的既有语义；它把当前
残差进一步限定在 static solve 的 internal angular state/consume 到 `integrateCore` 的区间，**不**证明任一
内部字段已与 local 不同。由于本轮 `--stream-no-store` 未保存完整 noise，不能直接给 local 做同输入 replay。

产物：

```text
log/c26_target_static_20260713/unity_runtime_probe_20260713_002100/events.jsonl
data/calibration/c26_target_static_14000_20260713.jsonl
```

#### C27 same-window local replay（2026-07-13，target residual 反证；active 子阶段不可外推）

以 C26 同次 `c03.first_dynamic_writeback` 的 Unity core pre-state重建本地 diagnostic Scene，并以当前 production
C20 binding 跑 C04 四个窗口。target 在 frame `0..3` 的 `P/Q/v/w` 均逐 float 相同，故旧 C23 的 target
`w.y=-1.7881393e-7` residual 不再出现在当前 production 路径。该结论不依赖 empty-cache diagnostic，关闭该
开关后同样成立。

同一回放的 active 在 frame `3` 出现 `w.y=0.02554227rad/s`。但 C26 的四个 solverSetupSolve record 都共享
`tickSerial=50496`，是一次 simulate 内的子阶段；C27 只能按完整 `Scene.simulate` 取样，不能证明它的第四个
完整步与 Unity 第四个内部 setup 是同一 phase。该 active 数值仅是 scheduler-alignment 缺口，不能提升为 native
字段差异或修复目标。

#### C28 local intra-tick phase map（2026-07-13，已完成：首次 active 字段差收紧）

在 scalar PhysX 的 `PxsDynamics.solverSetupSolve` 顺序入口/退出加入只读快照，并给每个 local solve block 标记
所属 outer phase。C26 同源 four-frame fixture 与 C28 的 phase `1..4` 一一对应；phase `1..3` 的 active/target
退出 `P/Q/v/w` 均逐 float 相同，故 C27 的 fourth-step 比较不是 scheduler 错配。

第一处 active 差异出现在 phase `4` 的**入口**：Unity active `q.y=0.12013883888721466`，local 为
`0.12013885378837585`，相差约一个 float32 ULP；该 phase 的 active `v/w` 与 target 的完整 `P/Q/v/w` 仍相同。
phase `4` 仅剩 static-contact blocks；其退出后 active 变为 `w.y` 差 `0.0255422741rad/s`、`q.y` 差
`1.26801431e-4`，target 仍逐 float 相同。因此该大差异是 static constraint consume 对 phase-entry active
quaternion 微差的放大，**不是** active0 release state、C20 target speed residual 或 endpoint 证据。

这只关闭“C27 是否比较了错误 phase”的疑问；尚未证明该 ULP 来自 quaternion transfer/normalization，还是它只与
同 phase static constraint row 的另一未记录字段共同出现。下一步只允许以 phase-4 entry 的 Unity `q` 为单变量
diagnostic oracle，或离线对照该 phase 的 active-ice constraint row；两者均不得进入生产。

产物：

```text
data/calibration/c28_local_solver_setup_phase_map_14000_20260713.json
log/c26_target_static_20260713/unity_runtime_probe_20260713_002100/events.jsonl
```

#### C29 phase-4 active quaternion oracle（2026-07-13，diagnostic_only）

对 C28 phase `4` 前的 local active quaternion 单独执行 float32 normalize：其 length-squared 为
`1.000000238418579`，inverse-length 为 `0.9999998807907104`；输出四个 float32 bit 与 Unity phase-4 entry
完全相同。只在该边界临时置入 Unity q、其余 position/velocity/target 均保持 local 值后，phase `4` 的
active/target post-state `P/Q/v/w` 全部逐 float 相同。

因此 C28 的 `0.0255422741rad/s` active angular residual 是这一次 quaternion normalization 缺失的因果下游。
该 oracle 禁止进入生产；它尚未证明 Unity 实际调用点，也未验收 `14000` 完整 settle 或 `14002` Reset 前的
active0 history。此前“FrictionPatch 跨局残留是 14002 根因”只能保留为 history-sensitive hypothesis，不得提升。

产物：

```text
data/calibration/c29_phase4_active_q_oracle_14000_20260713.json
```

#### C30 source-backed quaternion-normalization boundary（2026-07-13，setter 时序排除；unobserved）

本条是只读源码审计，边界严格为 C28 的 phase-3 `solverSetupSolve` exit 到 phase-4 entry；单变量仅为该
间隔内可见的 Unity locked-axis `set_angularVelocity` 调用 `func72559` 与本地对应调用链，未改 Unity 采样、
local Scene 或生产路径。

同次 C26 的 phase `1..4` enter/exit 全部保持 `lastAngularWriteSerial=1564`，所以 setter 发生在 phase-1
之前，而非 phase-3 exit 与 phase-4 entry 之间。它可解释进入这组 phase 前的角速度输入，但时间上不能成为
C29 所需的 between-phase producer；以下 setter 审计仅保留为调用链排除证据。
`D:/esp/tmp/func72559.wat` 的**直接函数体**没有 `f32.sqrt` 或 `f32.div`，函数只用当前 orientation
投影输入角速度，最后通过虚调用写入一个三浮点 velocity。该直接函数体没有 body quaternion store，也没有能
产生 C29 `inverseLength=0.9999998807907104` 的规范化运算。local 对应的
`NpRigidDynamic::setAngularVelocity -> Scb::Body::setAngularVelocity -> Sc::BodyCore::setAngularVelocity`
同样只写 angular velocity。

更正范围：`func72559` 的 helper/virtual target 尚未逐个反编译；但 C26 的 serial 时序已足以将整个 setter
调用发生时间排除出 C30 boundary，故不再把它列为 between-phase producer。它不改变 C29 的因果诊断，更不
授权将 normalize 接入生产。反编译 `120569 -> f71259` 还确认每个 `solverSetupSolve` 内都调用
`f71198 / integrateCore`，后者对应 `DyBodyCoreIntegrator.h::integrateCore` 的 `result.getNormalized()`；C28
phase-3 exit 的 Unity/local q 逐 float 相同，说明这一次 normalize 是双方共有的第一遍。Unity 仅在其返回后、
下一次 `f71259` 调入前多一遍标准 float32 normalize。C30 的主问题因此收紧为外层 Scene
completion/synchronization 调用链，状态仍为 `unobserved`。

同日继续按 runtime table map 而非 numeric 函数号回查：实际已 hook 的 public endpoint 是
`129354 -> $f82503 -> $f73035`。`f73035` 在 locked-axis 分支通过 native-object vtable slot `28` 将当前 pose
读到 stack scratch，做 `q.rotate(maskXZ(q^-1.rotate(v)))` 投影，再通过 slot `42` 传入三浮点 angular velocity。
其自身没有 `body2World.q` store 或 reciprocal-length 运算。这把 C30 收紧为两个尚未解析的虚调用 target：slot
`28` 的 pose-read 与 slot `42` 的 angular-velocity write。不得把旧 numeric `func72559` 单独当作 table endpoint，
也不得据“wrapper 没有 sqrt”提前宣布 setter 链完全排除；C30 主状态仍为 `unobserved`。

实验记录：

```text
boundary: phase-3 solverSetupSolve exit -> phase-4 solverSetupSolve entry (14000 active0)
single variable: func72559 / local setAngularVelocity path only
expected discriminator: setter 是否含 q normalize 或 body-q write
artifact path: data/calibration/c30_quaternion_normalization_source_audit_14000_20260713.json
scope: read-only source audit; no Unity resampling; no production normalize
```

#### C30.1 phase-4 q oracle settle extension（用户请求，diagnostic_only；已完成）

用户要求先量化“手动补齐真值”对完整尾段的可见影响。本实验沿用 C29 的**唯一**写入：仅在 local phase-4
entry 将 active0 q 写为同源 Unity 四个 float32；不写 p/v/w/target/参数，随后在同一 isolated C03 pair
diagnostic fixture 内继续到 local settle。它只量化该已证明局部因果对 local tail endpoint 的位移，不能证明
Unity endpoint 已闭合，也不能授权生产改动。

```text
boundary: C29 phase-4 entry -> isolated local 14000 pair settle
single variable: active0 quaternion set to Unity phase-4 entry only
expected discriminator: oracle/no-oracle settle endpoint delta；phase-4 float-exact closure 必须保持
artifact path: data/calibration/c30_1_phase4_q_oracle_settle_14000_20260713.json
scope: diagnostic_only; no production path, no Unity sampling, no lifecycle/material/cache/endpoint fitting change
```

采用 C29 同一 fixture（active friction `0.0`）分别运行 no-oracle 与单 q-oracle；两条都在 `346` 个
post-C04 steps 后 settle。oracle 的 phase-4 active/target `P/Q/v/w` 仍全部逐 float 相同；但完整 isolated
pair tail 中 active0 final position 仅改变
`( +0.0004425049, 0, +0.0000228882 ) m`，范数 `0.0004430964 m`（`0.443 mm`），target8 final position不变。

它是已证明的**第一处 native 字段差**和 phase-4 static-contact angular residual 的唯一因果上游，但仅在本
isolated fixture 内显示亚毫米 endpoint leverage。该夹具不是完整 persistent 14000/六-shot endpoint，故不得据此
把它排除为当前约 `2.7 cm` residual 的主因；其真实 full-path leverage 仍为 `unobserved`。此结论仍为
`diagnostic_only`；它不授权把 oracle 或无条件 normalize 接入生产。

产物：

```text
data/calibration/c30_1_phase4_q_oracle_settle_14000_20260713.json
data/calibration/c30_1_phase4_q_oracle_settle_baseline_friction0_14000_20260713.json
data/calibration/c30_1_phase4_q_oracle_settle_oracle_friction0_14000_20260713.json
```

#### C31 progressive truth-fill coverage（用户请求，已授权只读采样；待执行）

用户要求按上游顺序逐节点回填 Unity 真值、每步都算完整 settle endpoint，并用累积 endpoint 改变量划分主次。
现有真值已覆盖 release `1559` ticks 与 post-contact phase `0..3`，但没有到静止的连续两壶 core checkpoints；
不得从 endpoint 反推中间状态。因此仅新增一个 long-window 只读 capture：first stone-stone manager 出现后，记录
`solverSetupSolve` 的 active0/target8 decoded `P/Q/v/w` entry/exit；不存 raw memory、constraint、cache、
contacts 或任何生产状态修改。

```text
boundary: first 14000 stone-stone dynamic solver frame -> local/Unity pair reaches quiet (or 2048 frames)
single variable: observation coverage only
expected discriminator: enough same-run Unity checkpoints to run cumulative truth-fill endpoint waterfall
artifact path: data/calibration/c31_compact_core_truth_14000_20260713.json
scope: read-only Unity capture; no physics, lifecycle, cache, material, endpoint fitting, or production modification
```

采样完成：同次 `14000` 取得 `1024` 个 compact frame，active/target 在约 frame `400` 前已静止。以
frame `0` 同源 core 输入的 isolated local tail，最终 endpoint active/target 误差为 `0.722/1.650mm`；frame `1`
是本运行首个 solver divergence，active `w.y` 差 `0.0230753rad/s`。但只在 frame `2` entry 写入两壶 Unity
`P/Q/v/w` 会使下一帧 active angular difference 增至 `0.0303319rad/s`，target endpoint error 反而变为
`6.554mm`。这不是“负贡献”，而是证明四字段不是完整 PhysX state：该节点仍缺 active-ice PCM/manifold、
constraint/internal angular state 与 contact lifecycle history，禁止用该写入作主次结论。

当前有效/无效的真值瀑布行均已固化为：

```text
data/calibration/c31_truth_fill_waterfall_14000_20260713.json
```

#### C31.1 same-run angular-only waterfall retry（2026-07-13，diagnostic_only；部分完成）

首次 C31.1 启动没有连上并非 Unity/protocol 故障：watcher 以标题包含 `curling` 选窗，误把含
`curling_pyphysx` 标签的 VS Code 当成浏览器。现已收紧为优先且只接受 `Unity WebGL Player` 标题（浏览器缺少
该前缀时才接受带 Chrome/Edge/Chromium 的 `curling` 标题），重跑后 sampler 成功回传，取得 C04 `0..15`
compact core，以及同次 frame-1 的 static writeback（两个有效 dynamic-to-static solver descriptors）。

这个 retry 再次说明 endpoint **必须按同一 Unity run 成组**：它的 Unity endpoint 为 active/target
`(2.3409,5.4854)/(2.4851,3.9001)`，与早先 C31 capture 的最终点不同，因此两次 waterfall 绝不作数值相加。
retry 中 frame-0 exit 两壶仍 exact，frame-1 exit 的首个物理分叉仍为 active angular state，
`max |Δw|=0.0220451504rad/s`。

为避免 C31 的不完整 `P/Q/v/w` 覆盖破坏 PCM/manifold history，本轮只在下一个 C04 entry 调用 body angular
velocity setter；不写 P/Q/v、不清 cache、不改材料。结果如下（同 run isolated tail settle，单位 mm）：

| 累积回填至节点 | active endpoint error | target endpoint error | 相对 baseline target 改善 | 结论 |
|---|---:|---:|---:|---|
| 无回填（frame-0 exact baseline） | 0.188 | 5.319 | — | 基线 |
| frame-2 entry 仅 active `w` 真值 | 0.565 | 4.778 | 0.541 | 首个 active angular split 对 target 有真实但有限的尾段杠杆 |
| frame-2..15 每帧仅 active `w` 真值 | 0.382 | 4.778 | 0.541 | 额外 later active `w` 回填没有新增 target 改善 |
| 再加入 frame-3..15 target `w` 真值 | 0.382 | 4.778 | 0.000 incremental | target angular state 不是此窗口独立主因 |

因此该 run 中，frame-1 active angular residual 已确认有 `0.541mm` target endpoint contribution（baseline 的
`10.17%`），但 active endpoint 同时变差，表明静态接触的 P/Q/v、constraint/PCM hidden state 仍未一起闭合。
它是 `partial_only` 的因果量化，不是可接入 production 的修复。下一 gate 只允许解码并比对同次两个 frame-1
static solver descriptor 与 local static solve trace；完成前禁止把 angular oracle 变成生产补偿。

```text
data/calibration/c31_frame1_static_bundle_retry_14000_20260713.jsonl
log/c31_frame1_static_bundle_retry_20260713/unity_runtime_probe_20260713_111312/events.jsonl
data/calibration/c31_truth_fill_waterfall_retry_14000_20260713.json
data/calibration/c31_retry_truth_fill_active_w_entry2_14000_20260713.json
data/calibration/c31_retry_truth_fill_active_w_2_15_14000_20260713.json
data/calibration/c31_retry_truth_fill_active_target_w_2_15_14000_20260713.json
```

#### R01 historical RNG evidence reclassification（2026-07-13，已完成）

先前采样不会删除或改写，但自此按 RNG 可复现性分为 `R0_replay_grade`、`R1_same_run_boundary`、
`R2_input_conditioned` 与 `R3_statistical_only`。其中只有 R0（完整 per-tick friction 流，或记录的
`RANDSEED + draw start`）可进入未来“单次 endpoint 毫米级”验收；C03/C11/C31 等同 run checkpoint 保留
native boundary 定位资格；无 seed/noise/raw-log 绑定的旧 P6 endpoint 汇总降为残差分布/回归趋势，不得再作
跨 run 绝对误差。完整清单及迁移协议见：

```text
docs/unity_reverse/16_rng_evidence_inventory.zh.md
data/calibration/rng_evidence_inventory_20260713.json
```

#### C36 fixed-friction manifest closure（2026-07-13，C31.1 解释撤回范围已闭合）

`Random.InitState` 仅固定 global RNG 的一个时刻，不能隔离其它 Unity 路径的随机消费。C33/C35 的同 seed repeat 在第
`22` 个 DCP friction draw 分叉，故此前 C31/C31.1 所谓 frame-1 active `w` 首差及其 `0.541mm` angular-only tail
杠杆，**只适用于当时那一对 RNG 不同的 run，不能再解释为 local static solver 缺失**。

新 C36 fixture 按 C33 捕获的完整 `1562` 项 DCP friction manifest 回放；两次 fresh browser 都完整消费且没有耗尽，
endpoint、C04 frame `0..3` decoded core 完全一致。将其中一次 truth 输入当前 local same-run replay：frame-0 exact，
frame-1 起最大差 `1.847743988e-6 rad/s`，到 frame-3 仍是 ULP 级。因此 C31 的 static hidden-state gate 已关闭：
当前 production local path 在这个可严格复现 fixture 中没有可测的静态 solver 首差；禁止把旧 angular oracle 或
`0.541mm` 回填结论转成 production 补偿。

完整 C26 640-byte capture 仍保留为结构证据：两个 37×16 static descriptors 的 solver-body 物理字段跨 fresh run
一致；raw byte 差异是 pointer/尾部工作区，审计器明确报告而不把它纳入 `P/Q/v/w` 误差。后续严格验收应以 C36
manifest fixture 取代 seed gate，以 endpoint + exposed boundary core 为准。

```text
tools/reverse/audit_c36_manifest_replay.py
data/calibration/c36_manifest_replay_audit_14000_20260713.json
data/calibration/c37_manifest_local_static_phase_map_14000_20260713.json
```

#### C39 strict-manifest C03 前端 truth-fill waterfall（2026-07-13，主因已缩至最后 handoff）

在同一 C36 `1562`-draw manifest 下，从真实 `BESTSHOT` 生产路径跑到 C03 dynamic-pair 前。baseline 的 active
C03 entry residual 仅为 `P=45.776μm`、`q=1.13994e-5`、`v=2.384e-7m/s`、`w=1.38581e-6rad/s`；target 则已是
machine-zero。这个量级在碰撞中被放大，baseline final error 为 active `0.630mm`、target `4.226mm`。

按上游→下游的累计真值补齐（每行保留之前字段，只有 C03 pre-solver diagnostic fixture 写真值）如下。单位均为最终
endpoint 的 mm；这张表是**因果排名**，不是允许进 production 的补偿表。

| 累计补齐至 C03 entry | active error | target error | 相对 baseline target 改善 | 判定 |
|---|---:|---:|---:|---|
| 无 | 0.630 | 4.226 | — | production strict-manifest baseline |
| active `P` | 0.322 | 0.022 | 4.203 | **绝对主因：最后 handoff 的 active pose** |
| + active `q` | 0.962 | 0.022 | 0.000 | 与其它字段有非线性耦合，不能单独当修复 |
| + active `v` | 1.008 | 0.022 | 0.000 | 无 target 独立杠杆 |
| + active `w` | 0.036 | 0.022 | 0.000 | active 终点的第二层关键耦合项 |
| 再依次 + target `P/q/v/w` | 0.036 | 0.022 | 0.000 | target entry 已严格对齐，无独立贡献 |

全量 C03 truth 后的 active/target `0.036/0.022mm` 也与 C38 post-C04 truth settle 相符。这同时解释了为何旧 C31
angular-only waterfall 不可靠：它把 RNG 不同所造成的整个前端 pose residual 错投影为 static-solver angular residual。
下一 gate 不再解 C26 static descriptor；只检查最后一轮 `Newfrictionstep -> Rigidbody setter -> pre-sim pose` 的
active `P/q/w` 写入语义，先消除 `45.776μm` pose residual，再重跑此 strict fixture。

#### C41/C42 release-height 单因子反证（2026-07-13，非 production 修复）

将历史观测到的 Unity release native `P.y` 差 `+12.615203857mm` **仅**在 local `BESTSHOT` release 注入，随后仍按同一
C36 `1562`-draw manifest、正常 DCP/PhysX 路径推进。它不是 C39 active `P` residual 的来源：C03 前 active 的
`P`、`v` 逐值不变，只有 `q.y` 改 `+5.2154064e-8`、`w.y` 改 `+1.0430813e-7rad/s`；baseline endpoint 从
active/target `0.630/4.226mm` 变为 `0.668/4.226mm`，没有改善目标壶误差。

更关键的是，该微小 `q/w` 变化令“仅补 active `P`”从 target `0.022mm` 跳回 `4.222mm`；补 `P+q` 后立即恢复
`0.022mm`。这不是把 release height 提升为根因，反而证明碰撞入口在该 fixture 的分支敏感性：waterfall 中单字段的
非单调结果只能作**条件贡献**，最终 production 修复必须对齐完整的 last setter/pre-sim `P/q/w`，不能用高度或 endpoint
拟合替代。

```text
tools/reverse/audit_c39_manifest_front_half_waterfall.py
data/calibration/c42a_manifest_handoff_baseline_14000_20260713.json
data/calibration/c42b_manifest_release_y_14000_20260713.json
```

#### C44--C48 release setter 语义闭环与拒绝（2026-07-13，R0）

C40 同一 manifest 的 `1561` 行 Unity A2 trace 证明：把 Unity 每 tick getter/noise 直接喂给 recovered
`Newfrictionstep` 并在 setter 边界转 `float32` 后，linear 与 yaw setter **逐值相同**；函数本身不是 `45.776μm`
残差来源。用完全相同的 C39 16-stone/hybrid scene 回授实际 local getter 时，首个 yaw getter ULP 在 tick `118351`
（trace index `18`）出现，末端累积为 `1.56e-6rad/s`；这与 C40 “Unity pose + Unity setter”静态 replay 的首个
stone-ice divergence（同 tick 的 `v.y=4.1723e-6m/s`）一致。

曾被单独试验的 Unity release `P.y` 与每 tick `linearVelocity.y=0` 不能拆开解释：提高 release `Y` 后若仍保留 local
vertical velocity，会立即产生 `0.0981m/s` setter 错配；两者一起使用可把 release 初段 horizontal setter 压到
`~1e-11`，但 C48 端到端反而为 active/target `0.952/4.226mm`，比 C39 baseline 更差。因此二者都保留为
**diagnostic-only** 开关，禁止并入 production；它们没有解释横向 C03 pose residual。

在 **C36 单一 fixture** 内可严格下结论的是：前端 residual 的首个可观测来源是落地后 stone-ice static PhysX 反馈的
ULP 级差，而非 RNG、`Newfrictionstep` 算法、release height 或 vertical setter。此时继续做单字段补偿没有物理意义；
下一轮若要追求 sub-mm production，应比较 Unity/local 的 contact/solver 输入并以多 manifest 分布验收为准。

```text
tools/reverse/audit_a5_bestshot_production_setters.py
data/calibration/c44_c40_strict_setter_feedback_audit_14000_20260713.json
data/calibration/c47_c40_release_y_zero_vertical_setter_audit_14000_20260713.json
data/calibration/c48_manifest_release_y_zero_vertical_waterfall_14000_20260713.json
```

#### C49--C51 raw-RNG R0 分布前测（2026-07-13，C36 tail 结论撤回为单 fixture）

新的 raw-RNG 样本不再尝试以 global seed 对齐；每一条 runtime log 都保存自己的完整 DCP friction 流、C03，以及 C50/C52
额外的 C04 `0..3`（C52 也保存 C05 PCM cache/contact window）。C03 前端切片必须按事件顺序排除发生在
`first_stone_task` 已 arm 之后的 tail draw：C49 排除 1 条、C50/C52 排除 0 条。完成该切片后，三个 raw-RNG 样本的
C03 active `P` 均逐值对齐，`q/v/w` 只有 float ULP 级；这确认随机输入和 BESTSHOT-to-C03 前端路径可按 shot 严密对齐。

但 C50 用 Unity C04 truth 输入 local tail 后，frame 1 主壶 `w` 已差 `0.00604759rad/s`，frame 2 两壶 `v` 各约
`0.0012m/s`；最终仍差 active/target `1.839/3.957mm`。对照 C36 同一 C04-truth tail 的 `0.036/0.022mm`，**撤回**
“C03/C04 之后已普遍闭合”的外推：它只对 C36 的接触状态成立，不得用于所有 RNG manifest。

当前五个 R0 fixture 的 production endpoint 为：C36 `0.630/4.226mm`、C49 `0.361/5.437mm`、C50 `1.323/3.957mm`、
C52 `0.556/0.831mm`、C54 `1.135/3.907mm`（active/target）。已有四条带 C04 的 fixture：C36 在 frame 1 后仅 ULP 差且 tail
`0.036/0.022mm`；C50 从 frame 1 分叉、tail `1.839/3.957mm`；C52 frame 0--1 exact、frame 2 才分叉、tail
`1.676/0.351mm`；C54 的 C04 `0..3`（含全部 static blocks）逐字段对齐、tail `0.051/0.058mm`。C04-tail 范围为 active `0.036..1.839mm`、target `0.022..3.957mm`；C49 缺 C04，显式标记缺失，
不能插补。因此分布验收尚未通过，也尚不能把均值当作精度结论。C52 已完成的前 3 次 stone--stone PCM 对照中，
contact count、warm-start indices、normal、point、separation 均逐值相同；第 4 次才随着 frame-2 local dynamic
writeback 偏离而偏离。因此 PCM/cache 生成不是 C52 的首因。C53/C54 已把下钻点进一步改为 C04 dynamic calls
之间的 static writer；不能再重开 RNG、release 或 PCM 几何假设。

将同一 fixture 的 production endpoint、累计 C03 `P/q/v/w` truth diagnostic 和 C04-truth tail 并列后，贡献排序为：

| fixture | production active/target (mm) | C03 truth 后 (mm) | C04 truth tail (mm) | 当前主次 |
| --- | ---: | ---: | ---: | --- |
| C36 | 0.630 / 4.226 | 0.036 / 0.022 | 0.036 / 0.022 | C03 前端 handoff |
| C49 | 0.361 / 5.437 | 0.347 / 5.437 | 缺失 | C03 后下游，尚未捕获 C04 |
| C50 | 1.323 / 3.957 | 1.839 / 3.957 | 1.839 / 3.957 | C04 static inter-call 分叉 |
| C52 | 0.556 / 0.831 | 1.676 / 0.351 | 1.676 / 0.351 | C04 static inter-call 分叉 |
| C54 | 1.135 / 3.907 | 0.051 / 0.058 | 0.051 / 0.058 | C03 前端 handoff |

表中 truth 仅为 waterfall 诊断，不得进入 production。它说明“继续压量”的优先级不能用一个全局补偿决定：C03
front handoff 是 C36/C54 的高收益项；C50/C52 必须先抓到 C04 static batch 的首个 writer；C49 需要补采 C04 后
才可分类。

```text
tools/reverse/audit_c51_r0_distribution_summary.py
data/calibration/c51_r0_distribution_summary_20260713.json
log/c49_r0_distribution_a_20260713/unity_runtime_probe_20260713_121705/events.jsonl
log/c50_r0_distribution_b_20260713/unity_runtime_probe_20260713_122040/events.jsonl
log/c52_r0_distribution_c_20260713/unity_runtime_probe_20260713_123014/events.jsonl
```

```text
tools/reverse/audit_c39_manifest_front_half_waterfall.py
data/calibration/c39_manifest_front_half_waterfall_14000_20260713.json
```

#### C53 C04 solver consume 首分叉（2026-07-13，R0，C50/C52）

把 C04 的 Unity native descriptor 与 local trace 对齐到“finalizer prepare → 5 次 regular solve → final
writeback”后，C50 frame 1 与 C52 frame 2 呈现同一模式：prepare 行不是缺失状态。normal/friction 行虽不满足
逐字节相等，但只有浮点末位差（例如 C52 normal `rbXn.z` 差 `1.67e-16`，friction normal 的 `y` 差
`4.26e-14`）；regular iteration 0 的输出也为 `~1e-15`。

差异的时序尤其重要：C52 的 iteration 0 pair solve 输出仍只有 `~1e-15` 差，但 iteration 1 **进入前** target
solver-body `v.y` 已差 `4.165e-6m/s`；C50 亦在 iteration 1 进入前出现 active `v.y=5.364e-6m/s` 差。随后 pair
iteration 只传播并放大该已存在的状态，最后 C52 active `w.y` 差 `9.10e-3rad/s`、C50 差
`2.623e-3rad/s`。这解释了 C50/C52 后续毫米 tail，而没有授权把任何 Unity truth 写回 production。

**更正归因：** `dynamicSolves` 之间并非只有 dynamic--dynamic pair 调用，PhysX 会穿插 stone--ice static
blocks。C13/C14 已证明同一类现象的 pair consume 本身可闭合，而 first difference 正是发生在 pair iteration 0
exit 到 iteration 1 entry。因此 C53 不能把问题称为 dynamic solver arithmetic；它将首因收紧为 **C04 同帧
inter-call static-contact writer（active/target--ice 的 prepare/solve/writeback）**。RNG、release、PCM/cache
生成、外部 rigid-core handoff 与 finalizer 缺字段仍被排除；但本轮尚没有 C50/C52 同次 static block 的 Unity
before/after，不能把旧 C14 cache 结论直接外推。禁止 endpoint 拟合、额外真值注入或无依据摩擦补偿。

C54 已验证 static batch 的 descriptor 顺序为 `0=active--ice`、`1=target--ice`。据此仅作**时序推断**：C50
在 regular iteration 1 entry 的首个 `>=1e-6` 差为 pair `bodyA(active).linear.y`，候选 writer 是 descriptor 0；
C52 首差为 pair `bodyB(target).linear.y`，候选 writer 是 descriptor 1。这个映射只决定下一次 capture 的优先
descriptor，不能替代 C50/C52 同次 Unity static before/after，也不能进入 production 修改。

```text
tools/reverse/audit_c53_c04_first_divergence.py
data/calibration/c53_c50_c04_frame1_solver_audit_14000_20260713.json
data/calibration/c53_c52_c04_frame2_solver_audit_14000_20260713.json
```

#### C54 inter-call static block runtime capture（2026-07-13，R0，采集能力验证）

runtime hook 现把每个 C04 frame 的 dynamic/static regular block 与两类 writeback 共用 `solveSequence`：
`dynamic 0, static 1, dynamic 2, ... dynamic 8, dynamic-writeback 10, static-writeback 11`。static batch 有两个
descriptor，分别为 active--ice 与 target--ice；每个 descriptor 都保存 raw constraint window、solver-body data
before/after，且采集默认关闭。

独立 raw-RNG C54 样本完成了 1560 条本 shot friction draw 与 C04 `0..3`，四帧 active/target `P/Q/v/w`
全严格对齐（唯一是 frame 1 target `w.x=2.12e-39` subnormal）。因此这个样本是 C54 hook 的有效覆盖和一个已闭合
分支，**不是** C50/C52 静态 writer 已修复的证据。随后试图用 C50 的已记录 friction manifest 获取同一分叉，但三次
会话均停在 UI/protocol 入口、没有形成 `c03` 或 `c04`，全部标为无效连接日志，不可参与分布或根因判断。

`audit_c54_intercall_static_blocks.py` 已将该 capture 自动 join 到 local interleaved trace：4 frames × 5
regular static calls × active/target 两 descriptor 共 `40` 条 before/after compare，最大 local-minus-Unity 为
`4.7644e-44`，没有 `1e-6` 级差。这严格关闭 C54 正常分支的 static batch，并固定了 C50/C52 分叉时唯一可接受的
报告格式：`frame / regularIteration / descriptorIndex / localSequence / first differing solver-body or force field`。

同一 C54 的 production BESTSHOT-to-settle 仍为 active/target `1.135/3.907mm`；仅以 C03 `P/q/v/w` truth
diagnostic 累积补齐后成为 `0.051/0.058mm`，与 C04 tail 相符。因此此 fixture 的主误差在 **C03 前端 handoff**，
不是已严格闭合的 C04 static batch；这也再次禁止只依据 production endpoint 把 C04 误称为通用根因。

后续以 C50 的 `1560` 条 DCP friction manifest 重进同一 shot 时，先后发现两项采集前置缺口：HTML loading bar
消失时 Unity 仍可能停在 native splash，且 C54 必须显式同时开启 C04 window。修复这两个采集时序/配置后，C54k 获得
完整 `12` 个 C04 frame、C03 以及全 manifest 应用的有效运行时记录。但它**没有复现原 C50 的分叉**：C50 原始 frame 1
dynamic pair 在 iteration 1 entry 已有 `5.3644e-6` 的 `bodyA.linear.y` 差，C54k 同位点仅约 `1.74e-16`。这严格说明
“逐 tick friction 值相同”不足以冻结该 shot 的完整运行时分支；仍有 friction 之外的全局 RNG 消耗或运行时前置状态未锁定。

把 C54k 的 static block 与既有 C50 local trace 比较，最早可观测差在 `frame 0 / regularIteration 0 / descriptor 0`
的 `after.normalForce[0]`，local-minus-Unity 为 `-6.83069e-5`（首 `>=1e-6`）；但它未传导成原 C50 的 frame-1
dynamic-pair 首分叉，故**不得**将 descriptor 0 提升为 C50 根因，也不得把 C54k 加入 R0 误差分布。它只证明今后要取得
原始 split branch，必须冻结完整 RNG/state 前缀，而非只回放 DCP friction manifest。

#### C55 complete RNG/state-prefix inventory（2026-07-13，R0 C55b）

为排除“未记录的 Unity RNG 消耗”，C55b 从 hook 安装（早于 protocol `BESTSHOT`）到首个 C04 frame 同时记录
`UnityEngine.Random.InitState/Range/value/get_seed`。有效 shot 取得 `12` 个 C04 frame 和 `1562` 条 friction Range；
非 friction Range、`Random.value`、`get_seed`、`InitState` 的观测数全部为 `0`。因此在这段**已覆盖的 Unity Random
internal-call 窗口**，不存在可解释分叉的其它 Unity Random 消耗；它不排除 hook 安装前已建立的状态，或其它未恢复 RNG API。

C55b 也不是 C50 原 branch：其首 `>=1e-6` 差已在 C04 frame 1 的 regular iteration 0 **after** 出现，
`bodyA.linearDelta.x` local-minus-Unity=`+2.297401e-3 m/s`，下一 iteration entry 保持该差；这早于 C50 的
iteration-1 entry `bodyA.linear.y=+5.364418e-6`。故 C55b 是“iteration-0 dynamic split”类别，不能用于给 C50
descriptor 排因。下一项只允许采集一条同口径 full-RNG **non-split** R0 对照，再按 protocol、controller 写入、C03 input、
C04 regular iteration 顺序找第一处状态不同。

C55c 是同口径独立复验：仍为 `1562` 条 friction、其它已 hook Unity Random 调用均为零，且首差同样出现在
iteration 0 after（`bodyA.linearDelta.x=+2.462089e-3 m/s`）。因此当前 full-RNG 两样本均落入早分叉类；它们只能
共同排除“此窗口漏记的 Unity Random.Range/value/get_seed/InitState”，尚未构成 split/non-split 前缀对照。

watcher 已补齐且默认不影响普通采样：仅 `--recover-in-match` 才识别等待室左下蓝色“主菜单”，并且每个会话最多
执行一次恢复，防止从主菜单进入无限局制后的正常等待室被再次误退回。

```text
tools/reverse/unity_webgl_runtime_probe.js
tools/calibration/launch_unity_probe_browser.py
tools/calibration/unity_ui_watcher.py
tools/reverse/audit_c54_intercall_static_blocks.py
log/c54_r0_intercall_static_20260713/unity_runtime_probe_20260713_124335/events.jsonl
data/calibration/c54_c04_tail_settle_14000_20260713.json
data/calibration/c54_intercall_static_blocks_14000_20260713.json
log/c54k_c50_manifest_intercall_static_20260713/unity_runtime_probe_20260713_131936/events.jsonl
data/calibration/c54k_c50_intercall_static_blocks_14000_20260713.json
data/calibration/c54k_c50_c04_frame1_solver_audit_14000_20260713.json
log/c55b_full_rng_prefix_20260713/unity_runtime_probe_20260713_132450/events.jsonl
data/calibration/c55b_rng_state_prefix_14000_20260713.json
data/calibration/c55b_c04_tail_settle_14000_20260713.json
data/calibration/c55b_c04_frame1_solver_audit_14000_20260713.json
log/c55c_full_rng_prefix_20260713/unity_runtime_probe_20260713_132749/events.jsonl
data/calibration/c55c_rng_state_prefix_14000_20260713.json
data/calibration/c55c_c04_window_14000_20260713.json
data/calibration/c55c_c04_frame1_solver_audit_14000_20260713.json
```

产物：

```text
data/calibration/c30_quaternion_normalization_source_audit_14000_20260713.json
data/calibration/c30_wasm_solver_setup_source_20260713/func71259.dcmp
```

产物：

```text
data/calibration/c27_local_same_window_14000_20260713.json
data/calibration/c27_local_same_window_production_14000_20260713.json
```

#### C25 active0 history PCM supplemental capture（2026-07-13，采样覆盖，非本 gate 验收）

用户请求的受控 `14000 -> 14001 -> 14002` 运行已完成；`14002` 复用 `active0`。滚动 PCM hook 捕获
`11` 次正 stone-stone PCM：`14000` 为 seq `0..4`，`14001` 为 `6..8`，`14002` 为 `10..12`。
其中 `14002` 首个 PCM 前 active transform 为
`P=(-72.67115784,14.41978455,54.17440033)`、
`q=(6.541684e-8,0.186013296,1.238456e-8,0.982547283)`，并自然得到 2 contacts。

本轮 launcher 使用 `--stream-no-store`，没有保存可供本地 `Newfrictionstep` replay 的完整逐 tick noise；
因此本地同计划 replay 在 step 0 耗尽输入，不能把其 endpoint 输出视为物理对照。该捕获只增加 Unity PCM
history 真值，不改变 C23/C24 的 static-only 判别范围，也不授权重开 A/B 或作 endpoint 拟合。

产物：

```text
log/c25_active0_history_clean_20260713/unity_runtime_probe_20260713_001021/events.jsonl
data/calibration/c25_active0_history_clean_14000_14002.jsonl
data/calibration/c25_active0_history_local_replay_20260713.json
```

## 不可违反的工作协议

1. 每次实验先写一条记录：`boundary`、`single variable`、`expected discriminator`、`artifact path`、`scope`。
2. 每次实验最多改变一个已经被证明不一致的字段或调用语义。
3. oracle 只能进入 `diagnostic_only` 测试夹具，不能进入 `unity_front_half_physx.py` 的生产路径。
4. 任何新发现先更新本账本的状态，再讨论下一步；历史结论若被推翻，保留原记录并加“撤回范围”。
5. 禁止因为 endpoint、contact count 或单个 A/B 有改善，就提升为根因结论。
6. P14 只记录证据和计划；本账本记录“现在允许做什么”。两者冲突时，以本账本的 gate 为准。

## C57：同场景 12 构型 × 3 次冷启动的 collision matrix（2026-07-13，已完成）

### 正确的实验边界

本轮不是“每一球重启 Unity”。共有三个独立 Unity 进程 session（`r00/r01/r02`）；每个 session 在同一
无限模式场景中连续执行相同的 12 个构型。相邻 shot 只经 `RESETSTATE` 清场、换入该构型的主动/目标石，
不重启浏览器、不重置该 Unity 进程的全局 RNG。三个 session 之间才冷启动 Unity。目标石使用 `2..13`
不同 slot，避免同一 scene object 的残余生命周期混入构型比较。

每个 session 分别保存完整 front-half friction trace（`14995..15583` 条，未触及 `50000` 上限），并用
同一条 session trace 做 production local 的 no-oracle endpoint replay：不注入 Unity 的姿态、速度、
cache 或碰撞后状态。

产物：

```text
data/calibration/unity_collision_batch_matrix_20260713/
  collision_unique_targets_batch_r00.jsonl
  collision_unique_targets_batch_r01.jsonl
  collision_unique_targets_batch_r02.jsonl
  *_endpoint.json
  progress.jsonl
log/unity_collision_batch_matrix_20260713/
  collision_unique_targets_batch_r00/.../events.jsonl
  collision_unique_targets_batch_r01/.../events.jsonl
  collision_unique_targets_batch_r02/.../events.jsonl
data/calibration/unity_collision_batch_matrix_drainfix_20260713/
  collision_unique_targets_batch_r01.jsonl
  collision_unique_targets_batch_r02.jsonl
  *_endpoint.json
```

初版在 sampler 收到第 12 球最终 `POSITION` 后立即杀 browser，造成每批**最后一球**的 streamed friction
trace 没有完全落盘：`r01` 仅 `1180` tick、`r02` 仅 `640` tick。它们不能用于 local replay；不是物理上的
“未碰撞”。采样器已有正确 Unity 终点，但本地输入被截断。已在 batch runner 中加入 `8 s` drain，并重跑完整的
`r01/r02` 两个 12 球 session；最终表使用原完整 `r00` 加 drain-fixed `r01/r02`。三条右宽擦碰均在
第 `1236` tick 进入 local contact，初版的“右宽擦碰 1/3 碰撞分支”结论撤回。

### 结果（长度单位均为 mm）

`Unity 主动石分叉` 是同一构型跨三个 Unity 冷启动的最大两两终点距离；`本地主动石误差` 是三个 session
逐次相对本次 Unity 的终点误差。目标石若为“清出 3/3”，表示 Unity 三次都将其移出场地；当前 local
replay 尚未匹配该移出状态，故不伪造一个位置误差。`碰撞分支` 是 local 是否进入与 Unity 对应的首次
stone-stone contact。

| 构型 | Unity 主动石分叉 | Unity 目标石分叉/状态 | 本地主动石误差（三次） | 本地目标石最大误差 | 碰撞分支 |
| --- | ---: | --- | --- | ---: | --- |
| 正碰 y5.2, v3.4 | 15.8 | 227.2 | 0.37, 0.03, 1.58 | 0.00 | 3/3 |
| 正碰 y5.2, v4.0 | 46.5 | 清出 3/3 | 0.55, 0.02, 0.02 | —（清出状态未匹配） | 3/3 |
| 正碰 y6.2, v3.4 | 12.6 | 154.6 | 0.05, 0.04, 2.45 | 0.04 | 3/3 |
| 正碰 y6.2, v4.0 | 32.9 | 清出 2/3 | 0.27, 0.69, 0.39 | 0.01 | 3/3 |
| 正碰 y8.0, v3.4 | 13.3 | 135.8 | 0.80, 3.14, 2.35 | 0.05 | 3/3 |
| 正碰 y8.0, v4.0 | 17.8 | 58.6 | 0.54, 104.89, 0.46 | 0.44 | 3/3 |
| 左目标擦碰 | 29.8 | 72.0 | 25.58, 0.26, 2.15 | 0.08 | 3/3 |
| 右目标擦碰 | 50.1 | 105.2 | 38.21, 14.39, 1.38 | 0.08 | 3/3 |
| 左带旋擦碰 | 15.5 | 51.8 | 5.61, 15.51, 5.63 | 0.05 | 3/3 |
| 右带旋擦碰 | 13.8 | 18.9 | 1.09, 3.50, 8.06 | 0.03 | 3/3 |
| 左宽擦碰 | 19.6 | 清出 3/3 | 18.34, 5.35, 5.55 | —（清出状态未匹配） | 3/3 |
| 右宽擦碰 | 2.3 | 13.3 | 1.64, 0.41, 3.50 | 0.01 | 3/3 |

### 允许的结论与禁止的外推

- 本轮证明：local 三次都进入了 Unity 对应的碰撞分支；`右宽擦碰 1/3` 是初版最后一球 trace 截断导致的
  假象，已撤回。右宽擦碰补跑后的主动/目标误差分别为 `0.41..3.50 mm`、`0.01..5.34 mm`。
- 但全域仍不是毫米级：`y8,v4` 正碰的主动石有一次 `104.89 mm`，左右目标擦碰也分别出现 `25.58 mm`、
  `38.21 mm` 主动石误差；左宽擦碰最大 `18.34 mm`。这些是完整 trace 下的真实 local-vs-Unity endpoint
  差，不能归为采样截断。
- Unity 自身对同一输入、跨冷启动的分叉仍不小：主动石为 `2.3..50.1 mm`，目标石可到 `227.2 mm`。这说明
  任何后续“分布交付”必须按构型给出 Unity 的经验分布，不能用一个统一毫米阈值替代。
- 因而此前的“代表性正碰已达毫米级”只能作为该已覆盖子域的结论；本矩阵不支持宣称**全碰撞构型的最终落点分布**
  已可交付。

### C58：对 `>20 mm` endpoint 的只读交接 A/B（2026-07-13，诊断完成）

用户接受约 `10 mm` 的 Unity 分叉背景，要求仅追查 `>20 mm` 的异常。C57 complete-trace matrix 中三条被选为
discriminator：`y8,v4,r01`（active `104.89 mm`、target `441.52 mm`）、左目标擦碰 r00（`25.58/84.22 mm`）和
右目标擦碰 r00（`38.21/80.88 mm`）。所有 A/B 都复用**同一份完整 Unity friction trace**和同一 reset sequence，
不向本地注入 Unity 碰撞后真值；因此是归因实验，不是 endpoint 拟合。

| local 交接语义 | y8,v4 active/target | 左目标擦碰 active/target | 右目标擦碰 active/target |
| --- | --- | --- | --- |
| 当前 production replay | 104.89 / 441.52 | 25.58 / 84.22 | 38.21 / 80.88 |
| contact-friction override（不作 PCM material transition） | **3.40** / 64.07 | 26.19 / 85.62 | **18.17** / 66.06 |
| SetActive interaction refilter + material transition | 104.89 / 441.52 | **4.81 / 7.24** | 38.21 / 80.88 |
| refilter + contact-friction override | **3.40** / 64.07 | **4.75 / 4.56** | **18.17** / 66.06 |
| 上行再延后 target wake 至当前 PCM shell | 无变化 | 无变化 | 无变化 |

（单位：mm；粗体表示降入用户认可的约 `20 mm` 以内。）

允许的结论：

1. `y8,v4` 和右目标擦碰的大**主动石**误差来自 local 的 `PCM-shell material transition` / contact-friction
   恢复语义；这是可复现、可消除的交接问题，不是 Unity 分布本身。
2. 左目标擦碰来自 `SetActive` 后没有等价重建 actor/shape interaction；加入 refilter 后主动/目标均降至
   `5 mm` 左右。
3. 右目标擦碰和 `y8,v4` 的**目标石**仍为 `64..66 mm`，且对 refilter、contact friction 和 wake timing 均不敏感。
   它们属于首个 dynamic--dynamic solve 之后的 target tail/state 差异，尚未定位到单一 source 字段；不得把现有
   A/B 选项直接提升为 production 修复。

产物：

```text
data/calibration/diagnostic_r00_{contact_override,wake_pcm,refilter,membership,refilter_contact_override,refilter_override_wakecurrent}_20260713.json
data/calibration/diagnostic_r01_{contact_override,wake_pcm,refilter_contact_override,refilter_override_wakecurrent}_20260713.json
```

### C59--C70：长批次完整随机流与目标石首帧 writeback 定位（2026-07-13，已定位，未修复）

为避免 C04 逐帧观测与全量 friction stream 同时采集时产生大量单事件 HTTP 请求，probe 改为保留原始
时间戳的 `128` 条有序批发送；sink 逐条写回 JSONL。C69/C70 的 12 组 friction 长度分别为
`[1561,1236,1445,1155,1259,1021,1333,1337,1383,1383,1236,1237]` 和
`[1560,1236,1445,1156,1261,1022,1335,1338,1384,1380,1235,1236]`，均完整，故可与 local
无真值注入 replay 配对。

目标石 7 同时被 `y8,v3.4` 和 `y8,v4.0` 使用；C03 增加 active horizontal-speed 下限后，`1.2 m/s`
只捕获后者。C70 的 `y8,v4.0` 是高误差样本：active/target endpoint 为 `3.48/65.04 mm`。

| C04 首个 dynamic solver frame | active | target |
| --- | --- | --- |
| entry P/v/Q | position 逐 float 对齐；线速度仅 Z 差 `0.00014 mm/s`；Q norm 差 `5.73e-5` | position 差 `0.0076 mm`，其余可忽略 |
| entry -> exit position 差 | `0.207 mm` | `0.184 mm` |
| exit transverse velocity（local - Unity） | `+21.021 mm/s` | **`-18.666 mm/s`** |
| exit angular-y（local - Unity） | `-0.29520 rad/s` | **`-0.32149 rad/s`** |

这把 `65.04 mm` 的 target endpoint 残差严格前移到**首个 dynamic--dynamic solver frame 的切向冲量/角速度
writeback**：不是 RNG stream 截断，不是 reset 后 refilter，也不是碰后很晚的 ice tail。C69 的温和样本还显示
另一条真实但次级的历史量：同一 entry 处 Unity active yaw 为 `-0.28846rad`，local 为 `-0.00010rad`；只以
真值替换这一个 entry yaw 的诊断将 target endpoint 从 `13.14` 降至 `9.01 mm`。因此 reset “保留 quaternion”
的语义本身已正确；缺的是此前碰撞 writeback 后 local quaternion 的精确复刻，且它不是 C70 高分叉的唯一根因。

产物：

```text
data/calibration/c69_y8v4_target7_speed_filtered_c04_entrance_20260713.json
data/calibration/c70_y8v4_target7_speed_filtered_c04_entrance_20260713.json
data/calibration/c70_y8v4_target7_first_frame_compare_20260713.json
tools/reverse/audit_c04_local_first_frame.py
```

下一步只允许比较 C70 frame-0 的 Unity dynamic constraint/body writeback 与 local 相同 first-contact step 的
solver输入/输出；不得按 endpoint 反调摩擦、反弹或 yaw。

### C71--C73：4-wide dynamic solver 采集门槛（2026-07-13，进行中）

原 C04 只钩 `solveContactBlock`，但目标石高分叉的 island 实际走 `solveContact4Block` /
`solveContact4BlockWithWriteback`。现已将两者纳入同一只读 C03/C04 窗口。C71 完整记录到 `5` 个
regular dynamic solve 与 `1` 个 writeback，且全批 friction stream 完整；本地同一持久 Scene 的 first-contact
step 也能只在该步打开 trace，得到 `1/15/1` 个 finalizer/regular/writeback local 记录。

但 C71 的 `127.51 mm` target 样本不能用来判定 solver 本体：其 C04 entry active yaw 为 `0.37530rad`，
local 为 `0.32719rad`，已有约 `0.048rad` 的历史 quaternion 输入差；其 contact normal/constraint 差是
该上游差的合法后果。相反，C72 的 entry yaw 差仅 `2.44e-6rad`，同样完整地捕获 4-wide trace，最终
active/target 仅 `0.23/2.13 mm`。这再次证明不能把任一高 endpoint 直接归因给 solver。

`C73` 因重钩子 session 超过有效采集窗口被显式停止，未纳入任何 endpoint 或分布统计。

当前可接受的 solver 判别样本必须同时满足：

```text
1. 12 组 friction stream 完整；
2. C04 的 5 regular + 1 writeback 完整；
3. C04 entry active/target P、水平 v、yaw/Q 均与 local first-contact trace 对齐；
4. target endpoint 仍 > 20 mm。
```

产物：

```text
data/calibration/c71_y8v4_target7_dynamic4_c04_20260713/
data/calibration/c71_y8v4_target7_local_first_contact_solver_20260713.json
data/calibration/c72_y8v4_target7_dynamic4_c04_20260713/
tools/reverse/audit_p6_targeted_first_contact_solver_trace.py
```

## Unity 受控采样连接协议

这不是物理实验的一部分，但它是所有 runtime probe 的固定前置流程。不得再把浏览器 WebSocket、
采样器 TCP socket 和临时 idle supervisor 混为一谈。

```text
1. 启动 probe launcher：只负责拉起可见浏览器和安装只读 hook。
2. 立即启动 ControlledSceneSampler：它是唯一的两槽 protocol client；默认重试等待 180 秒，
   在尚未开放 protocol server 时不退出、不另起连接器。
3. 用户在浏览器中点击“无限模式”。无限模式开放 `127.0.0.1:7788` 后，sampler 自动连接、
   CONNECTKEY、READYOK、RESETSTATE、BESTSHOT。
4. sampler 收到 GO 后自行发射计划中的 shot；不要再另起 idle_socket_supervisor，也不要手动发 BESTSHOT。
5. 采样结束后先 dry-run 清理器，再以 `--stop` 结束该 session 的 sampler、launcher 和 browser 子进程。
```

执行约束：

- launcher 的 Python parent 可作为后台进程启动；验收是 Playwright 浏览器本身必须 `headless=False` 并
  `page.bring_to_front()`，用户能看到并点击“无限模式”；
- sampler 应使用 Python 3.10+（本机为 `C:/Users/PickledPepper/scoop/apps/python313/current/python.exe`），
  因为它使用 `argparse.BooleanOptionalAction`；
- `localtest:0` 仅由 `ControlledSceneSampler --use-reset` 自动派生；浏览器 URL 仍使用
  `connectkey=localtest`；
- 同一轮采样只允许一个 sampler 持有两条 socket。`idle_socket_supervisor.py` 仅用于无 shot 的
  server health check，不能与 sampler 并发运行。

清理器只按 session 的 `--log-root` 和 sampler `--output-file` 精确匹配，不会扫描或结束其它项目的
Python 进程：

```powershell
& 'C:/Users/PickledPepper/scoop/apps/python313/current/python.exe' tools/calibration/stop_unity_probe_session.py `
  --log-root log/a8_static_window_20260712 `
  --sampler-output data/calibration/a8_static_window_14000_20260712.jsonl

& 'C:/Users/PickledPepper/scoop/apps/python313/current/python.exe' tools/calibration/stop_unity_probe_session.py `
  --log-root log/a8_static_window_20260712 `
  --sampler-output data/calibration/a8_static_window_14000_20260712.jsonl `
  --stop
```

## C78--C96：首碰零摩擦交接已修复；残余为第二 tick 的数值分叉（2026-07-14）

### 已进入 production 的确定性修复

C04 直接观测证明：石--石**第一个 dynamic solver frame**使用 `0/0` 静/动摩擦；其后的正常接触为
`0.36/0.36`。此前 local 把 `0.36/0.36` 从第一帧起持续使用，因而把一个已知的时序事实误建模成了
“调一个全局摩擦参数”。现 production 路径仅在首个进入 PCM shell 的 `Scene.simulate(dt)` 前临时改为
`0/0`，该步结束立即恢复 `0.36/0.36`。

这个修复不是 endpoint 拟合：它由 C04 solver frame 的 Unity 真值约束，并已回归通过
`tests.test_unity_front_half_sim` 与 `tests.test_fast_curling_env`（10/10）。把 pair friction 永久置零的
C79 A/B 已证实会破坏目标石（target RMSE 约 `196 mm`），因此明确禁止。

### 同一场景 12 构型 × 3 冷启动的最新 production 回归

使用 C86 `r00/r01` 与 C87 `r02`；每个 session 内连续执行 12 个构型，session 间才冷启动。
下列为本地相对该次 Unity 的 target endpoint 误差（mm；`clear` 表示 Unity 清出场地，不能伪造成坐标误差）。

| 构型 | r00 | r01 | r02 | 当前判定 |
| --- | ---: | ---: | ---: | --- |
| 正碰 y5.2, v3.4 | 0.5 | 0.8 | 1.6 | 稳定毫米级 |
| 正碰 y5.2, v4.0 | clear | clear | clear | 清出状态，未作位置比较 |
| 正碰 y6.2, v3.4 | 1.2 | 0.3 | 0.9 | 稳定毫米级 |
| 正碰 y6.2, v4.0 | clear | 6.0 | 7.3 | 可接受 |
| 正碰 y8.0, v3.4 | 4.1 | 2.0 | 2.6 | 稳定毫米级 |
| 正碰 y8.0, v4.0 | 9.8 | **481.4** | 10.2 | r01 极端分支 |
| 左目标擦碰 | 25.4 | 6.1 | 12.7 | 存在尾部 |
| 右目标擦碰 | 6.6 | 76.3 | 5.3 | r01 极端分支 |
| 左带旋擦碰 | 3.8 | 42.6 | 6.6 | r01 极端分支 |
| 右带旋擦碰 | 0.4 | 34.1 | 129.7 | session 尾部 |
| 左宽擦碰 | 75.4 | clear | clear | 构型分支/清出混合 |
| 右宽擦碰 | 61.4 | 38.5 | 17.5 | 仍有系统尾部 |

因此“标准正碰已经毫米级”仍成立；但这张完整构型表不支持宣称全构型 endpoint 分布已验收。

### RNG 已闭合，不再是这批残差的解释

C90/C91 的 runtime hook 在完整 batch 中未见 friction 之外的 `Random.Range` 或 `Random.value` 调用。
C92 修正 hook 后保存的完整 friction manifest 能精确重现 r01 的矩阵，包括 `y8,v4` target 的
`481.4383 mm` 分支。此前 C89 因 hook 没有写出 manifest friction event 而无效，不能引用。

结论是：在当前受控序列中，已记录的 friction stream 足以重放该分支；不能再把它笼统归为“每次全局 RNG
不同、所以无法对齐”。

### 已定位到的剩余误差层级

以 C96 的 r01 `y8,v3.4` 为判别样本：首个 C04 dynamic frame 与 local 对齐到约 `4e-6`，同帧 static
intercall 也仅约 `7e-5`；故首碰接触生成、首帧零摩擦交接与 static--dynamic 顺序已不是主因。

但在其后的第二个 physics tick，给定首碰 entry yaw 真值后，前 3 次 regular solver iteration 仍只差
`0.00021` 量级，到第 4 次即放大到约 `0.0147`，并持续影响 writeback 和随后冰面尾迹。对应的 friction
force 差约 `0.01345`，而静摩擦上限约 `7.16`，远未触及 clamp；**“静摩擦阈值/夹紧切换导致分叉”这一旧猜测
撤回**。现在唯一被证据支持的表述是：极微小的 solver 递推/浮点状态差在第 4 次迭代开始被放大。

同一 C96 中，Unity 在碰后停止时 yaw 为 `0.263467`，local 为 `0.247283`，差约 `0.016184 rad`；该差恰与
下一投 `y8,v4` 的 r01 入射 yaw 差同量级，足以解释其随后 `481 mm` 的分叉。初始 yaw 真值注入仍不能消掉
这段碰后差，因此 quaternion 不是唯一漏字段，而是这段 solver/tail 数值分叉的可观测结果和向下游传播通道。

隔离检查过的 A7 strict 标量构建缺少当前 production 依赖的 multi-cache lifecycle 接口，不能替换现有
运行时；直接切换会丢失已对齐的 cache/SetActive 语义，故该路线排除为生产修复。

产物：

```text
data/calibration/c86_timed_zero_pair_friction_3sessions_20260714/
data/calibration/c87_timed_zero_pair_friction_r02_20260714/
data/calibration/c92_r01_manifest_validated_20260714/
data/calibration/c96_r01_y8v3_compact64_bg_20260714/
data/calibration/c96_y8v3_r01_second_tick_trace_20260714.json
data/calibration/c96_y8v3_r01_yawtruth_second_tick_trace_20260714.json
data/calibration/c96_y8v3_r01_yawtruth_second_tick_dynamic_20260714.json
data/calibration/c96_y8v3_r01_yawtruth_second_tick_static_20260714.json
```

### C97：Wasm 单次 solver consume 复验（2026-07-14，已完成）

复用已有的 `c13_wasm_solver_stage`，对 C96 r01 `y8,v3.4` 的第二 tick 五个 Unity raw
`PxSolverBody(32B)` / constraint window 逐次直接调用 scalar Wasm `Dy::solveContactBlock`。结果为逐 float
完全一致：regular `0..2` 必须 `doFriction=false`，regular `3..4` 必须 `doFriction=true`。这也解释了第 4
次 regular 才出现非零 friction force，但不等于 friction clamp：它是该 tick 内既有的 solver phase 切换。

因此，C96 的本地--Unity 差异不能归因于 x64/Wasm 的**单次** pair solver 公式、摩擦开关时相或摩擦上限；
它必定发生在 local Scene 把 body/constraint 送入 regular 0 之前，或在相邻 regular call 之间由其它
constraint/调度路径写入 solver state。C99 随后已使用现有 C53 trace 的 raw body window 缩小该边界。

产物：

```text
data/calibration/c97_y8v3_r01_wasm_second_tick_solver_20260714.json
```

### C99：second-tick role mapping 修正与 regular-0 entry（2026-07-14，已完成）

C53 的 `--swap-local-bodies` 比较器原先漏掉“交换 descriptor 时 contact normal 反向”，从而也漏掉
`ra×n/rb×n` 的反号。该脚本已修正并在 C96 r01 `y8,v3.4` 第二 tick 重跑；它只影响诊断显示，不触碰
production simulation。

结果：regular-0 entry 的两份 local `PxSolverBody` 前 `32B`（按 role 交换）与 Unity wasm window 前 `32B`
逐字节一致。constraint 的 raw bytes 不可跨 wasm32/x64 直接比较，但解码字段仍有极小物理差：首个 normal
row 的 `ra×n` 最大约 `3.64e-6`，首个 friction normal 最大约 `5.96e-8`。它在 regular-0 exit 已产生 target
angular-y `1.23575e-4 rad/s` 差，随后才在 regular-3 的 friction phase 放大。

故“第 0 次 pair solve 的 body 输入不一致”排除；目前最早的可观测 source 是第二 tick 的 contact
finalization 几何 row，而不是 solver consume 或摩擦阈值。

产物：

```text
tools/reverse/audit_c53_c04_first_divergence.py
data/calibration/c99_y8v3_r01_second_tick_dynamic_rolefix_20260714.json
```

### C100--C102：second-tick PCM pose 与单 ULP A/B（2026-07-14，诊断完成，未进入 production）

C100 在本地只读地保留了 first-contact 后第二 tick 的 PCM trace。pair PCM 的 active pose 与 Unity C04
frame-1 entry 的位置和 yaw 对齐；但 stationary target 的 native X 为 `-72.3774032593`，Unity 为
`-72.3773956299`，相差一个 float32 ULP（`7.629e-6 m`）。active quaternion 的 Y 相同，但 W 比 Unity
低一个 float32 ULP（`5.960e-8`）。这些量会进入下一 tick 的 contact finalization，因而足以解释
`ra×n`/normal 的首个微差；但尚不等于已找到可泛化的 setter 语义。

为防止把单样本真值补偿误写入 production，做了两个全历史 replay 的 diagnostic-only A/B：

| A/B | 对 regular-0 及后续的结果 | 结论 |
| --- | --- | --- |
| C101：每次 ResetState 后 stationary target native X `+1` float32 ULP | target pose 对到 Unity；target angular-y 初始差由 `1.236e-4` 降到 `7.23e-5 rad/s`，但 normal 差反而由约 `6e-8` 扩至 `1.7e-6`，后续 friction 放大仍在 | 不是通用 target pose 修复 |
| C102：首碰后 active quaternion W `+1` float32 ULP | regular-0/3/4 误差基本不变 | 不是 quaternion W 单字段修复 |

因此当前不允许把任一 ULP 偏置接入 `unity_front_half_physx.py`。C100 也确认 local PCM trace 只能提供
本地 ContactBuffer；C93 未开启 Unity C05 PCM window，尚不能直接比较 Unity pair ContactBuffer。

产物：

```text
data/calibration/c100_y8v3_r01_second_tick_pcm_20260714.json
data/calibration/c101_y8v3_r01_target_x_ulpplus1_20260714.json
data/calibration/c101_y8v3_r01_target_x_ulpplus1_dynamic_20260714.json
data/calibration/c102_y8v3_r01_active_qw_ulpplus1_20260714.json
data/calibration/c102_y8v3_r01_active_qw_ulpplus1_dynamic_20260714.json
```

### C103：首次 Unity C05 PCM 补采启动失败（2026-07-14，无效，不纳入统计）

为取得上述 Unity pair ContactBuffer，batch runner 已增加 `--c05-pcm-window` 透传；随后以相同 r01
friction manifest 启动 12 构型 session。浏览器导航被本地 WebGL host `127.0.0.1:9007` 拒绝，采样器只
停在等待无限模式 socket，未收到任何 shot。该 session 已按精确 log/output 路径停止；没有完整 sample、
friction stream 或 endpoint，故 C103 无效且不纳入任何分布。

### C104：r01 C05 PCM window 重采（2026-07-14，已完成，仍是诊断）

恢复本机 `curling_server.exe` 后，以同一 r01 friction manifest、同一 12 构型计划重新采集；browser 的
C05 window 已记录 `12` 条 post-contact convex--convex PCM 调用。当前判别构型 `y8,v3.4,t06` 的前两条
分别对应 C04 frame `0/1`：frame-1 pair 的 Unity transform 与 C04 core entry 一致、ContactBuffer count 为
`2`。按 body role 反向后，Unity/local pair normal 的最大差约 `8.94e-8`，排除了毫米/厘米级的二次 PCM
分支错误。

该 hook 的 ContactBuffer world-point preview 不能直接作为最终比较字段（buffer 在调用后被下游覆盖）；应使用
C05 记录的 wasm manifold raw 与 local 已转换到 wasm32 layout 的 manifold raw 解码 local-point/penetration。
因此 C104 完成了真值采集，但尚未授权 production 改动，也不把该次 endpoint audit 用作分布回归。

产物：

```text
data/calibration/c104_r01_y8v3_pcm_window_20260714/
log/c104_r01_y8v3_pcm_window_20260714/
```

### C105--C107：PCM 语义闭合、Reset timing 与全局原点反证（2026-07-14，已完成；无 production 改动）

C105 新增了按 `PersistentContactManifold` 真实语义解码 wasm raw 的只读比较器。它不直接比较
role-reversed pair 的字节：Unity 是 `active -> stationary`，本地是 `stationary -> active`；contact normal
存于 B 的局部坐标，比较时先转回 world 再反向。对 C104/C100 的 frame-1：

| 字段 | 最大差 | 结论 |
| --- | ---: | --- |
| pair PCM 输入 active position | `0m` | active 入口已经对齐 |
| pair PCM 输入 stationary position | `7.6293945e-6m` | 差异在 PCM 之前已存在 |
| world normal | `5.19e-8` | pair PCM 未形成大分叉 |
| stationary-side contact point / penetration | `7.63e-6m` / `7.68e-6m` | 基本是上游 pose 差的传递 |

因此 C99 的 `ra×n` 微差来源从“pair PCM backend/cache”收紧为 **stationary target 在第二 tick pair 入口前的
pose producer**；不得继续改 pair PCM、feature bytes 或 friction threshold。

C106 改变本地 Reset 后的 settle count（`1 -> 0`，不注入真值）。target 的 native X 仍为
`-72.3774032593`，故该 ULP 不是本地这一个 reset settle tick 自行产生。C107 曾把**冰面网格与所有
body 共用的** `protocol_y -> world_x` float32 原点提升一 ULP；虽然 y=8 的 target 因而对上 Unity，历史中的
active 在当前 shot 入口立即偏到 `15.26µm / 0.01567rad`。这个 production patch 已撤回。C107 只能否证
“把观测到的 y=8 float32 endpoint 直接当作全局原点”，不能否证 managed setter 在更高精度表达式后才落入
native float32 的可能性；该区分由 C108 闭合。

产物：

```text
tools/reverse/audit_c105_pcm_manifold_semantics.py
tools/reverse/audit_p6_targeted_first_contact_solver_trace.py  # 新增 reset timing diagnostic-only 开关
data/calibration/c105_y8v3_r01_pcm_manifold_semantics_20260714.json
data/calibration/c106_y8v3_r01_reset_settle0_20260714.json
data/calibration/c107_y8v3_r01_exact_native_origin_trace_20260714.json
data/calibration/c107_y8v3_r01_exact_native_origin_pcm_compare_20260714.json
```

### C108--C109：Reset position 的 managed 精度语义闭合并接入生产（2026-07-14，已完成）

C108 在 fresh Unity page 内先让 sampler 接入，再进入无限模式，避免空会话；两次单 shot 分别抓到 target
首次进入 `PxcPCMContactConvexMesh`（target--ice）的 native `PxTransform`。这是 target 首次可见的
static-contact consumer，早于 stone--stone C04：

| protocol y | 首个 static PCM native X | 本地旧 reset X | C04 target X | 结论 |
| ---: | ---: | ---: | ---: | --- |
| `6.2` | `-70.5774002075` | `-70.5774002075` | 相同 | 原映射已命中 |
| `8.0` | `-72.3773956299` | `-72.3774032593` | `-72.3773956299` | 在 static support 前已存在 `+7.6293945µm` |

两行并不需要一个错误的全局 float32 原点：它们共同约束了 hidden managed X base 的区间。以
`-64.377398` 在 Python double 中完成 `base - protocol_y`、仅在 `PxRigidDynamic.set_global_pose` 时落为
float32，正好同时产生上述两个 Unity native 值；若直接把 base 改为 y=8 的 float32 endpoint，y=6.2 会错一
ULP，这正是 C107 的失败原因。

production 已新增 `UNITY_NATIVE_POSITION_X_BASE`，仅供 stone managed-position 写入与反解使用；已验证的
ice mesh `UNITY_NATIVE_ORIGIN_X` 保持不变。C109 用**同一 r01 的 12 条 Unity 输入、同一 RNG manifest**作
严格 A/B（除该一行映射外无差别）：

| 指标 | 修复前 | 修复后 | 变化 |
| --- | ---: | ---: | ---: |
| active endpoint RMSE | `34.396mm` | `20.349mm` | `-40.8%` |
| target endpoint RMSE | `155.609mm` | `46.916mm` | `-69.9%` |
| target endpoint max | `481.438mm` | `126.414mm` | `-73.7%` |

同一修复下，前五条（均为 head-on）为 active RMSE `0.717mm`、target RMSE `3.538mm`。这证明该位置写入
误差是当前主因之一，且修复没有扰动 y=6.2；余下的大尾部集中在 glancing/curl/wide，尚不能宣称全构型完成。

产物：

```text
tools/reverse/audit_c108_target_static_pose_timeline.py
data/calibration/c108b_y8v3_r01_target_static_timeline_20260714.json
data/calibration/c108c_y6p2v3_r01_target_static_timeline_20260714.json
data/calibration/c109_y8v3_r01_managed_position_base_solver_20260714.json
data/calibration/c109_r01_all12_pre_position_base_endpoint_20260714.json
data/calibration/c109_r01_all12_managed_position_base_endpoint_20260714.json
```

### C110：fresh Unity 全 12 构型回归（2026-07-14，session 1/3 已完成）

修复 batch runner 的协议编排：sampler 必须在 browser 进入 infinite mode 前启动，并以 `5s` poll 回到其
`15s` handshake/reconnect 判定；否则 TCP 虽已连通，自动 UI 已开始空对局，永远没有 `GO`。两个空会话
`c110/c110b/c110c` 没有发出 `BESTSHOT`、样本文件均为空，已排除；`c110d` 是第一条有效 fresh session。

它在**一个 Unity 进程内连续**完成 12/12，随后用该 session 自己的 friction stream 无真值注入回放：

| 分组 | 可比较落点数 | RMSE | max |
| --- | ---: | ---: | ---: |
| head-on | 11 | `4.482mm` | `10.508mm` |
| glancing / curl / wide | 11 | `14.283mm` | `42.799mm` |
| 全部 active | 12 | `4.229mm` | `8.888mm` |
| 全部 target | 10 | `15.002mm` | `42.799mm` |

head-on 六构型均已在 `0.01--10.51mm`；非正碰中最大的残差是 `glance_right_curl_in` target `42.80mm`，
说明 C109 修复已泛化到正碰和多数斜碰，但仍需用独立 Unity restart 区分该尾部是 Unity session 分布还是
local contact producer。

产物：

```text
data/calibration/c110d_fresh_r01_positionbase_20260714/
log/c110d_fresh_r01_positionbase_20260714/
tools/calibration/run_unity_collision_batch_matrix.py  # sampler-before-browser + 5s handshake poll
```

### C111--C112：三次 fresh Unity restart 的 12 构型泛化（2026-07-14，已完成）

在 C110 r01 之外，C111 r02 与 C112 r00（同构型、不同 target slot 分配）也各完成 12/12；三次全局
local endpoint RMSE 分别为：

| fresh session | active RMSE | target RMSE |
| --- | ---: | ---: |
| r01 | `4.229mm` | `15.002mm` |
| r02 | `4.442mm` | `19.488mm` |
| r00（不同 slot） | `4.110mm` | `19.558mm` |

跨 restart 的 Unity 自身落点范围远大于本地误差：例如 y=6.2/v4 target 的 Unity range 为 `4095.7mm`，wide-left
target 为 `3490.8mm`，而本地对应最大误差仅 `10.5mm` / `58.9mm`。最敏感的 curl-right target 在 r01 出现
`42.80mm` 本地误差，但 Unity 跨重启 target range 为 `223.6mm`；它落在 Unity 分布内，不能作为本地未闭合的
确定性 defect。y=8/v3（此前位置 producer 的判别样本）三次 local target 最大误差 `6.2mm`，Unity restart range
`14.2mm`。

结论：C109 的 managed-position 修复已在 head-on、glancing、curl、wide 和不同 slot 的三次 fresh session 中泛化；
当前 endpoint 残差没有发现一条同时满足“跨 restart 稳定 >20mm”且“落在 Unity 自身 spread 外”的样本。因此停止
继续压缩 deterministic pose ULP，交付层应把剩余差异作为 Unity session 分布而非本地确定性误差。

产物：

```text
data/calibration/c111_fresh_r02_positionbase_20260714/
data/calibration/c112_fresh_r00_positionbase_20260714/
log/c111_fresh_r02_positionbase_20260714/
log/c112_fresh_r00_positionbase_20260714/
```

### C113：交付前二维分布外审计（2026-07-14，通过）

`tools/reverse/audit_restart_endpoint_distribution.py` 对 C110--C112 的 23 个有效 body/configuration
组合执行了比 RMSE 更严格的判定：Unity 清场 `(0,0)` 不视作物理 endpoint；其余项必须同时满足
“三次均可见、三次 local error 均 >`20mm`、local endpoint 在 Unity 二维 restart envelope 外 >`20mm`”才会被
列为需继续修复的确定性 candidate。结果为 `candidateCount=0`、`accepted=true`。

这满足当前目标的完整性条件：修复后已覆盖所有 12 构型和三次 fresh Unity restart；没有遗漏的、可被现有
真值区分为本地 deterministic defect 的尾部。剩余差异归入被观测到的 Unity session distribution。

产物：

```text
tools/reverse/audit_restart_endpoint_distribution.py
data/calibration/c113_restart_endpoint_distribution_audit_20260714.json
```

### C120--C122：扩展构型批量重放的验收前提修正（2026-07-14）

对新增 high-curl / long-offset 构型的同场 Unity 批次，不能把仅含 `RESETPOSITION`、`BESTSHOT` 和
friction stream 的记录直接当作逐行独立 endpoint 真值。`RESETPOSITION` 的已闭合语义是**只改位置、保留
Rigidbody quaternion**；而协议 `POSITION` 不携带 quaternion。故本地从上一条自身碰后状态继续，Unity 则从
上一条 Unity 碰后状态继续；一旦两者已有微小姿态差，高旋的 native angular setter 会放大该差，后续 endpoint
的几十厘米差不能归因于该行的碰撞模型。

这不是给本地补 endpoint 真值，也不是把连续场景降级为 fresh scene，而是补齐严格重放本来就需要的**上游状态**。
`tools/reverse/audit_hybrid_p6_endpoint_sixshot.py` 现支持 `--orientation-manifest` 和
`--require-orientation-truth`：manifest 对每个 sample 提供 active/target 的 reset yaw；缺失时报告会标
`strictEndpointComparable=false`，不得进入毫米级 aggregate。C122 的旧单条 high-curl 报告正因此被重新标注为
非严格值（缺 stone `0,10` 的 reset yaw），其 `266mm/87mm` 不能再作为本地确定性 endpoint 残差。

独立 fresh high-curl C120-12008 的完整 friction replay 则仍给出 active `13.4mm`、target `3.5mm`，说明该
构型并未证实存在数十厘米级的单条碰撞方程偏差。下一次“同场 12 构型”验收必须在每次 `RESETPOSITION` 后抓取
参与 stone 的 native quaternion（或等价 yaw），并与同次 friction stream 一起作为 R0 输入；否则只能报告统计/
非严格结果。

### C122：纠正错误的 angular setter quaternion 包装（2026-07-14）

C122 的 live C04 窗口直接给出了 DCP 的最后一次角速度 setter：脚本写入为纯 world-Y
`[0, 0.145769387..., 0]`。旧本地实现把这个值再次按当前 quaternion 投影；该 A/B 在同一
1280 次 friction stream 的最后一步得到 `w=0.125660`，而 Unity 为 `0.145624`。关闭该二次投影后，
本地为 `0.145635`，同时线速度也与 Unity C04 frame 18 对齐。

因此 `PersistentPhysxFrontHalfScene` 及 endpoint audit 的默认路径已改为直接写
`[0, speed.angle, 0]`；`--unity-native-angular-setter-wrapper` 只保留为历史 A/B。该修正使 C122
目标壶 endpoint 从旧的非严格 `86.9mm` 降到 `0.423mm`。主壶仍有残差，原因已缩小为首次接触报告出现后、
实际冲量发生前的 stone--ice angular-friction 过渡；不能以调一个全局摩擦系数代替该阶段语义。

### C125--C127：native angular setter 的最终语义更正（2026-07-14）

C122 把 A9 中**脚本层** `speed.angle=[0, wy, 0]` 与 native setter 的实际输入混为一谈，故“直接
world-Y”为过渡性结论，现已撤销。C127 在 fresh Unity 的 A8/A9 前八 tick 窗口中确认：脚本纯 Y 写入经过
native bridge 后仍保留一个随刚体 tilt 变化的微小 X/Z 分量；但它**不**随累计 yaw 旋转。第一 tick 的证据为：

| 层级 | angular vector |
| --- | --- |
| 脚本 `speed.angle` | `[0, 3.13115262985, 0]` |
| Unity native bridge | `[0, 3.13115262985, 4.169381782e-7]` |

正确复现为：从当前 quaternion 分解出 yaw，保留其余 tilt quaternion；只将 world-Y 按该 tilt 映射成 native
angular vector。它既不是 direct-Y，也不是旧的“完整 quaternion 再投影”。生产默认已改为
`emulate_unity_native_angular_setter_tilt_only=True`；direct-Y 和
`--unity-native-angular-setter-wrapper` 都只允许作为历史 A/B。

在同一份完整 C126 friction stream 上，直写 Y 的 active endpoint 误差为 `198.364mm`，tilt-only 降至
`11.808mm`；target 由 `1.107mm` 降至 `0.425mm`。随后没有复用该会话的 C127 fresh high-curl 盲验证得到
active `7.173mm`、target `0.502mm`。因此首个碰撞前已有的约 `1.024mrad` yaw 偏差已被消除，剩余 active
误差是毫厘到一厘米量级的中段 setter/getter feedback 残差，不再是碰撞前姿态主因。

对 C120 的 12 行同场批次（仍缺每次 reset yaw，故只作非严格趋势）也有一致改善：target RMSE
`7.311mm -> 6.367mm`，active RMSE `54.202mm -> 52.868mm`，active mean
`31.966mm -> 25.173mm`。不能以这组 non-strict aggregate 宣称完整验收；严格验收仍须带 orientation manifest。

产物：

```text
data/calibration/c126_highcurl_a2_c04_20260714/endpoint_default_tilt.json
data/calibration/c127_highcurl_early_static_20260714/endpoint_default_tilt.json
data/calibration/c120_extended_r03_drain60_20260714/collision_unique_targets_batch_r03_endpoint_tilt_only_all12.json
```

### C128--C131：带 reset-yaw 真值的三次 fresh 12 构型严格验收（2026-07-14，通过）

此前同场批次缺 `RESETPOSITION` 保留的 quaternion，故只能做 non-strict 趋势。C128 首先验证了这一缺口：
12 次 release 事件均能关联到协议 reset，但旧 native-root 路径未解出 quaternion，整轮明确作废为严格证据。
C129 修正为读取已由 A9 验证的 native bridge `Rigidbody root +52 -> bridge +80 PxTransform`；每次
`BESTSHOT` 的第一条 angular setter 之前均得到 active quaternion。新增
`tools/reverse/build_a10_fresh_target_orientation_manifest.py` 把这些 active yaw 生成 manifest。

验收设计是三个彼此 fresh 的 Unity session（r01/r02/r00），每 session 12 个 head-on、glancing、curl、
wide 构型；target index `2..13` 在 session 内各只使用一次、此前未参与任何 shot，故其 factory identity yaw=0
是设计真值；反复使用的 active `0/1` 则每枪使用 A10 真值。三个 manifest 均以
`--require-orientation-truth` 运行，全部 `12/12 strictEndpointComparable` 且 `12/12 reachedFirstContact`：

| fresh session | active RMSE / mean / max | target RMSE / mean / max | strict rows |
| --- | ---: | ---: | ---: |
| r01 / C129 | `4.660 / 1.520 / 16.123 mm` | `9.982 / 4.386 / 29.079 mm` | `12/12` |
| r02 / C130 | `2.814 / 1.101 / 9.626 mm` | `7.831 / 4.303 / 21.661 mm` | `12/12` |
| r00 / C131 | `0.307 / 0.238 / 0.578 mm` | `3.591 / 1.806 / 10.251 mm` | `12/12` |
| 合计 | `3.148 / 0.953 / 16.123 mm`（36） | `7.621 / 3.527 / 29.079 mm`（28 非清场 target） | `36/36` |

唯一两条超过 `20mm` 的 target 残差均是 `glance_wide_right`：r01 `29.079mm`、r02 `21.661mm`，r00 同构型
仅 `1.104mm`。三次 Unity target endpoint 本身最大相隔 `235.704mm`，且两次 local 偏差方向不同；因此它没有构成
跨 restart 稳定、同向的本地 deterministic defect。保持为 Unity session distribution 的尾部监控项，不得再用单次
>20mm 直接判定本地碰撞模型错误。

产物：

```text
data/calibration/c129_active_yaw_r01_20260714/endpoint_strict_yaw.json
data/calibration/c130_strict_yaw_r02_r00_20260714/endpoint_strict_r02.json
data/calibration/c131_strict_yaw_r00_20260714/endpoint_strict_r00.json
tools/reverse/build_a10_fresh_target_orientation_manifest.py
```

### C133--C134：wide-right 尾差的 C03 solver-boundary 复核（2026-07-14）

为避免把 Unity 的同场分布误判为本地 defect，对 `glance_wide_right` 追加了 two fresh C04 windows。C132 因
READY 前 protocol socket 被服务端关闭而未产生任何 sample，已清理且不计入证据；C133/C134 均完整 `12/12`
strict，native selector 固定为 target13 的 `(-70.077398, 53.7300015)`。

复核同时修正了 `audit_c04_local_first_frame.py` 的边界选择：C04 的 frame 0 可能只是 first dynamic island，
早于真正 stone--stone PCM 消费一 tick。审计现在优先使用 manager-validated
`c03.first_dynamic_writeback.manager.coresBeforeSolve -> coresAfterSolverSetup`，并把 `q` 与 `-q` 视为同一
orientation。此前报告的 C04-entry `11.7mm` active 位差属于错相位比较，不能作为主因。

在正确 C03 entry，target 的 `P/v/w/q` 对 Unity 均为数值零差；差异从首个 solver writeback 的切向角速度
产生：C133 target `|Δv|=0.002089m/s`、`|Δw|=0.009991rad/s`，endpoint `6.866mm`；C134
`|Δv|=0.002656m/s`、`|Δw|=1.062073rad/s`，endpoint `11.848mm`。这说明 wide-right 的 remaining tail 确在
instance-specific 的 stone--stone tangential/angular solver 输出，而不在 reset yaw、碰前位置、或 angular setter。

但它尚不授权全局修正：同一 production code 下两次 writeback residual 的量级不同，且 endpoint 都在 `12mm`
内；把该单帧 `w` 差折成全局摩擦/角冲量补偿会伤害已经严格闭合的其余 35 条。若将来出现跨 fresh session
稳定同向的 >20mm endpoint，唯一允许的下一步是抓取该实例的 ContactBuffer / friction rows / solver bodies 做
row-level 对照；禁止从当前两条 C03 `w` 残差直接拟合生产参数。

产物：

```text
data/calibration/c133_wide_right_c04_20260714/c03_first_contact_wide_right.json
data/calibration/c134_wide_right_c04_r01_20260714/c03_first_contact_wide_right.json
tools/reverse/audit_c04_local_first_frame.py
```

### C140--C142：双壶左右分裂的连续朝向归因（2026-07-15）

右分裂的完整 12 局同场 friction-manifest 重放确认：`RESETPOSITION` 只复位位置和速度，**不复位石头
quaternion**。同一份 Unity friction stream 下，把每局石头朝向复位会使原始 r08 的 far branch 消失；所以它
不是“第二次碰撞”的独立缺陷，而是跨局保留朝向进入首个斜碰后被放大的临界分叉。生产连续模式已保持本地自身的
朝向历史；并行模式则只允许明确的 fresh-state `--reset-all-stone-rotations`，不再把互相独立的 worker 伪装成
连续 Unity 场景。

左分裂的独立 Unity A/B 给出同一结论。连续朝向重放时 active / 被撞壶平均误差为 `15.566 / 37.459mm`
（被撞壶 max `176.284mm`）；同一 friction、双方每局都复位朝向后降至 `0.494 / 3.461mm`
（被撞壶 max `8.534mm`）。故此前约 `2cm` 的左分裂均值不是可安全写入全局碰撞参数的偏置；强加该补偿会伤害
已经闭合的 fresh-state 轨迹。

产物：

```text
data/calibration/unity_split_manifest_rotation_ab_20260715/left_r03/
data/calibration/unity_split_manifest_rotation_ab_20260715/left_r03/left_session_reset_orientation_replay.json
tools/reverse/replay_manifest_collision_session.py
```

### C143--C145：扫冰守壶的协议生效状态与训练路径（2026-07-15）

对 s2/s6 守壶执行了严格 A/B：两端复用同一 Unity friction stream，且每局都复位全部石头朝向。若本地仅依据
`SWEEP distance` 假设即时生效，被撞壶平均误差为 s2 `178.6mm`、s6 `288.1mm`。Unity browser log 表明 8 次
请求中仅前两次进入 Unity handler，且 handler 紧贴 `Curling stop`；其余六次未投递到 Unity。因此此批实际
physics-effective sweep 均为 false。把这一**观测到的协议生效状态**输入本地后，误差为：

| 构型 | active mean | 被撞壶 mean / max |
| --- | ---: | ---: |
| s2 | `0.105mm` | `0.930 / 1.710mm` |
| s6 | `0.091mm` | `0.547 / 0.646mm` |

这不是把所有扫冰全局关掉：`tools/reverse/derive_protocol_sweep_effect_manifest.py` 从 Unity browser log 导出逐 shot
生效清单；`sample_local_collision_distribution.py`、完整 session replay 与并行 batch runner 均支持
`--sweep-effect-manifest`。进一步的严格 s4/s8 sweep-glance A/B 也确认同一 socket 语义：即时请求模型的
active / target 平均误差为 `106.046 / 110.991mm`，协议实际生效模型为 `2.755 / 0.442mm`。因此无清单时生产/
训练默认 `--sweep-request-policy protocol-late`，即请求不影响当前 slide；只有 direct/native sweep API 或未来有
明确 Unity handler-before-slide 证据时，才显式使用 `--sweep-request-policy assume-effective` 或 manifest 的
`effective=true` entry。

训练用 fresh-state 并行模式新增 `--compact-training-output`，移除仅用于调试的 PhysX 指针快照；同一 8 条样本在
4 worker 下由 `6.296s` 降至 `2.516s`，并且顺序/并行 JSONL 的 SHA-256 完全一致。命令形态：

```powershell
D:\esp\tmp\curling_pyphysx_conda\python.exe tools/reverse/run_local_simulation_batch.py `
  --plan-file <fresh_plan.json> --output-file <train.jsonl> --workers 4 `
  --reset-all-stone-rotations --compact-training-output `
  --sweep-effect-manifest <unity_protocol_sweep_effects.json> `
  --python D:\esp\tmp\curling_pyphysx_conda\python.exe
```

产物：

```text
data/calibration/sweep_guard_rotation_timing_ab_20260715/unity_protocol_sweep_effects.json
data/calibration/sweep_guard_rotation_timing_ab_20260715/local_protocol_effect_replay.json
tools/reverse/derive_protocol_sweep_effect_manifest.py
tools/reverse/sample_local_collision_distribution.py
tools/reverse/run_local_simulation_batch.py
```

## 当前唯一允许的动作

```text
Action: 生产保持 tilt-only native angular setter；连续协议保留本地 quaternion history，fresh 训练才允许
`--reset-all-stone-rotations` 并行。socket 扫冰默认 `protocol-late`，禁止仅凭请求距离假设即时生效；effect manifest
只在有逐 shot Unity 证据时用于覆盖默认。禁止注入全局摩擦补偿。禁止恢复完整 quaternion 二次投影；禁止把
direct-Y 当生产语义；禁止用全局摩擦常数、C107 全局原点改动或 C101/C102 的单 ULP pose 偏置掩盖已通过的链路。
```

## 恢复提示

新会话的第一条工作提示应为：

```text
Read docs/unity_reverse/15_persistent_scene_alignment_ledger.zh.md first.
Use the tilt-only native angular setter. Strict batch endpoint acceptance requires reset-yaw truth;
direct-Y and full-quaternion wrapper are A/B diagnostics only.
```
