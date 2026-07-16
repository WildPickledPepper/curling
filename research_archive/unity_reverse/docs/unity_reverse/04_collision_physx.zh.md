# 碰撞与 PhysX 总览

这页只放当前碰撞线的结论和阅读入口。旧的长过程文档已归档到：

```text
docs/archive/unity_reverse_superseded_20260709/04_collision_entry.zh.md
```

## 当前结论

我们不是完全不知道 Unity 碰撞机制。已经确认的大方向：

```text
Unity PhysX 4.1 / WebGL wasm
fixed timestep = 0.01s
contact generation = PCM
friction type = patch friction
solver iterations = 6 / 1
stone material = Bouncy, friction 0.6, restitution 1.0, combine Multiply
ice material = Ice, friction 0.02
formal stone runtime constraints = FreezeRotationX | FreezeRotationZ
formal stone collider = runtime convex MeshCollider
```

2026-07-09 运行时 native probe 又确认了 finalizer 层材质：

```text
stone-stone createFinalizeSolverContacts:
  staticFriction ~= 0.3600000143
  dynamicFriction ~= 0.3600000143
  restitution = 1

stone-rink createFinalizeSolverContacts:
  staticFriction ~= 0.0120000001
  dynamicFriction ~= 0.0120000001
  restitution = 0
```

这正好对应 Multiply combine：`0.6*0.6=0.36`、`0.6*0.02=0.012`。
所以材质 combine 已经不是当前 10cm 级碰撞误差主嫌。

同一轮 raw snapshot 进一步恢复了 single-pair finalizer 的 desc / friction patch：

```text
data/calibration/unity_physx_native_solver_state_20260709.json
data/calibration/unity_physx_native_solver_state_convexconvex_arm_20260709.json

首个 stone-stone createFinalizeSolverContacts.after:
  ContactBuffer.count = 1
  FrictionPatch.anchorCount = 1
  FrictionPatch.friction = 0.3600000143 / 0.3600000143
  PxSolverConstraintDesc.constraintLengthOver16 = 16
  expected constraint block = 256 bytes
```

`256 bytes` 正好对应 `SolverContactHeader + 1 normal row + normal force buffer +
2 friction rows`。后续 stream 采样已经直接抓到了 `desc->constraint` raw bytes，
并把 Unity raw row 与本地按 `ContactBuffer + PxSolverBodyData` 重构的 row 对到
`4.45e-7` 量级。因此 finalizer row 公式本身已经不是当前主嫌。

solver consume / body writeback 公式也已经用 Unity raw row 离线闭合：

```text
data/calibration/unity_physx_solvecontact_replay_delta_20260709.json
data/calibration/unity_physx_solver_consume_replay_delta_withwriteback_20260709.json

solveContactConcludeBlock replay max error ~= 5.96e-8
solveContact_BStaticConcludeBlock replay max error ~= 7.45e-9
solveContactBlockWithWriteback replay max error ~= 5.96e-8
solveContact_BStaticBlockWithWriteback replay max error ~= 7.45e-9
```

所以 `func71035/71036` 的公式不是当前主嫌。旧 hook 抓到的
`solveContactConcludeBlock` 显示主速度跳变在进入某些 conclude call 前已经存在；
2026-07-09 14:55 的 runtime probe 已补上 `solveContactBlockWithWriteback` 等父 wrapper，
并且抓到了主 solve 写回边界。现在要做的不是继续猜 solver 公式，而是把这份 Unity
pre-solve `PxSolverBody` / row / bodyData 和本地 pyphysx 同 shot 生成的 native state
逐字段对齐。

同日又补了一条同 shot 桥接样本 `13000`。注意：旧的 solvecontact endpoint
和 14:55 with-writeback endpoint 不能混着比，当前审计已经切到 with-writeback run：

```text
data/calibration/unity_native_solver_collision_probe_20260709_withwriteback.jsonl
data/calibration/unity_physx_collision_probe_native13000_immediate_contact_20260709.json
data/calibration/unity_collision_upstream_mismatch_audit_20260709.json
tools/reverse/summarize_collision_upstream_mismatch.py
```

这条样本是 `v0=3.4, h0=0, w0=0, target 8 at (2.375,5.2)`。用当前 best 几何
复跑本地 pyphysx 后，在这个 with-writeback run 的 endpoint 下：

```text
active endpoint error ~= 2.29cm
target endpoint error ~= 19.87cm
```

这次最新字段级结论修正了旧结论：normal 方向已经匹配，首个分叉在
contact generation / manifold reduction，而不是 solver 公式：

```text
local pyphysx immediate pre_step t=0.00:
  contact_count = 4
  target-side normal angle ~= -2.812468deg
  separation ~= -0.00152m

local pyphysx first ContactPairPoint:
  contact_count = 4
  normal angle ~= -2.812468deg
  impulse norm ~= 15.156 Ns
  separation ~= -0.00152m

Unity createFinalizeSolverContacts.after:
  contact_count = 2
  target-side candidate normal angle ~= -2.812503deg
  separation ~= +0.00859m / +0.00838m

Unity solveContactBlockWithWriteback:
  positive normal-force sum ~= 12.811 Ns
```

这组结果曾经把最高优先级推到 contact generation/cache parity；但 2026-07-09 晚上的
direct scene-style PCM 审计修正了判断：这里的 `4 contacts` 来自本地
`PxGenerateContacts` immediate wrapper 的缓存复制语义，不等价 Unity scene narrowphase。
formal collider mesh 的旧探针结果仍保留作反例：

```text
data/calibration/unity_physx_collision_probe_native13000_immediate_formal_contact_20260709.json

formal mesh active error ~= 1.50cm
formal mesh target error ~= 17.53cm
formal mesh immediate contact_count = 4
formal mesh target-side normal angle ~= -5.62deg
```

这说明“直接换 recovered formal mesh”还不能复刻 Unity cooked hull/contact manifold。

随后用 Unity finalizer 里已经抓到的相对 `bodyFrame0/bodyFrame1` 做了回灌实验：

```text
tools/reverse/probe_unity_finalizer_pose_contacts.py
data/calibration/unity_finalizer_pose_contact_replay_20260709.json

Unity finalizer:
  contact_count = 2
  separation ~= +0.00859m / +0.00838m
  target-side normal angle ~= -2.812503deg

local immediate PxGenerateContacts fed Unity finalizer relative bodyFrame pose:
  ring geometry = 4 contacts at zero yaw, 3 contacts at Unity yaw cases
  formal recovered mesh = 4 contacts at zero yaw, 3 contacts at Unity yaw cases
```

随后把 Unity raw PCM-after cache、Unity native transform/quaternion 顺序修正后，
绕过 immediate wrapper，直接调用 Unity scene 同一层的 `g_PCMContactMethodTable`：

```text
data/calibration/unity_pcm_refresh_invalidate_audit_20260709.json
data/calibration/unity_direct_pcm_vs_immediate_audit_20260709.json

local direct scene-style PCM:
  contact_count = 2
  normal 与 Unity 一致
  separation 与 Unity 只差约 7e-8m
```

再把 direct PCM contacts 喂进同一 capture 的 `ContactBuffer + PxSolverBodyData`
row 重构器：

```text
tools/reverse/compare_direct_pcm_to_solver_rows.py
data/calibration/unity_direct_pcm_solver_row_bridge_20260709.json

unity_contact_count = 2
direct_contact_count = 2
max contact delta ~= 7.73e-8
max direct-vs-Unity computed row delta ~= 5.84e-5
max raw-vs-direct computed row delta ~= 5.86e-5
bridge_closed_at_contact_prep_precision = true
```

所以单一 17:12 样本的 contact generation 和 contact prep/normal row 已经闭合到数值
精度内。2026-07-10 的完整 Scene A/B 又确认，样本 14000 在补齐历史 yaw 后，只需把
first-PCM native Y 下调一个 float32 ULP（`0.953674um`）到 Unity 值，同一
cache/hull/solver 就从 4 点变成 2 点；单独补 `38.146um` 横向差仍为 4 点。

但后续六样本审计否定了把这条规律全局化：exact Unity pose 下本地 contact 数为
`[2,4,4,4,2,4]`，Unity 为 `[2,2,2,4,4,4]`。14001/14002/14004 的分叉仍位于 PCM
support/feature/manifold 入口内部状态；14002/14004 还叠加 first-contact 一 tick 相位差。
因此不能把“只修冰面高度”写成全局下一步，也不能重新扫描摩擦、半径或 solver 参数。

把同源 17:12 样本按修正后的四元数顺序重跑完整 pyphysx Scene：

```text
data/calibration/unity_physx_collision_probe_native13000_pcm_hull_runtime_posefix_20260709.json
data/calibration/unity_direct_pcm_scene_replay_gap_20260709.json

endpoint:
  active error ~= 0.84cm
  target error ~= 10.09cm

local Scene first contact report:
  contact_count = 4
  separation ~= -0.00691m

Unity / direct PCM:
  contact_count = 2
  separation ~= +0.00943m / +0.00927m
```

这就是当前最硬的剩余差异：单帧 direct PCM/contact-prep 已闭合，但完整 Scene
从头跑时仍然走 fresh/local PCM 路径，在首次接触帧生成 4 个穿透 contact。
因此目标不是继续调半径/摩擦，而是把 PCM cache 生命周期、first collision timing、
warm-start force buffer、friction anchors 和 pre-solve `PxSolverBody` 初值接进 replay。

但是本地 pyphysx replay 还不是 Unity 首次碰撞帧的字段级 native-state 复刻。当前 best：

```text
unique-role current best:
  active RMSE ~= 3.86cm
  target in-play RMSE ~= 11.32cm

per-sample entrance-state oracle:
  active RMSE ~= 1.35cm
  target in-play RMSE ~= 1.48cm
  7 / 7 in-play pair 双终点进 2cm

visible-feature leave-one-out correction:
  active RMSE ~= 5.22cm
  target in-play RMSE ~= 30.98cm
  0 / 7 双终点进 2cm
```

所以，2cm oracle 只能证明缺口在入口 native state / contact-instance 状态，不是可直接训练的通用公式。

## 证据链

1. 单一全局参数不成立：`friction/restitution/radius/contactOffset/solver/lock_upright` 等扫描都不能把 target 拉进 2cm。
2. 尾段滑行不是主因：从本地 `0.02s/0.20s` snapshot 重跑 target tail，只调 `vx/vy` 可把 endpoint 压到毫米级。
3. 首帧冲量差很小但足够放大：需要约 `0.49 Ns` row 级修正，约本地主冲量 `2.35%`。
4. 最坏样本 `12003` 的 contact-frame 差约 `4.98deg`，接近 64 边 cooked hull 一个侧面步长。
5. `12005` 需要 `handoff_w_offset=-0.44rad/s` 才闭合，但全局 w offset 失败，说明它是 tangent/angular/contact cache 代理。
6. `13000` with-writeback 同 shot 审计显示 normal 方向已经贴合；旧 immediate probe 的
   contact count/separation 分叉已被 direct PCM 审计解释为 wrapper 假差异。
7. `20260709_171257` 同 capture 桥接显示：direct PCM contact 接入 row 重构后，
   raw solver row 只差约 `5.86e-5`，所以 contact prep 也不是剩余主嫌。
8. 同源 17:12 完整 Scene replay 仍有 `target error ~= 10.09cm`，本地 first contact
   是 4 点/负 separation；这把剩余缺口锁定在 Scene 状态集成，而不是单帧 PCM 或 solver 公式。

## 阅读入口

- 几何和 cooked hull：[`12_physx_convex_cooking.zh.md`](12_physx_convex_cooking.zh.md)
- contact generation 细节：[`05_physx_contact_generation.zh.md`](05_physx_contact_generation.zh.md)
- solver row 细节：[`06_physx_solver.zh.md`](06_physx_solver.zh.md)
- native state 是否一致：[`13_physx_native_state_equivalence.zh.md`](13_physx_native_state_equivalence.zh.md)

## 下一步

不要继续用 endpoint 大网格蒙参数。碰撞线的下一步是：

```text
1. 本地 replay 统一修正 pyphysx 四元数数组顺序：[w,x,y,z]。
2. 用 direct scene-style PCM 替换 immediate PxGenerateContacts 作为 contact 等价入口。
3. 把 Unity raw PCM cache / direct PCM ContactBuffer 接入完整碰撞 replay 或等价的 trace-driven solver。
4. 比较 0.02s 碰后 active/target linear/angular velocity。
5. 速度对齐后再看 endpoint 是否进 2cm。
```

如果 direct PCM 的 ContactBuffer 一致但 0.02s 速度仍不对，优先查完整 Scene replay 的
pre-solve `PxSolverBody` 初值、PCM cache 生命周期、warm-start force buffer 和 friction anchors。
目前 `13000` 已经把第一优先级推到 trace-driven replay：Unity 侧已经有
`solveContactBlockWithWriteback` 的 pre-solve body/row、ContactBuffer、FrictionPatch anchors、
PxSolverBodyData 和 body writeback 窗口；17:12 之后的 PCM 入口 dump/direct replay 已经证明
首个 cached manifold 的 contact generation 与 contact prep 都可与 Unity 对齐。

当前已有这些运行时压缩/提取报告：

```text
data/calibration/unity_physx_native_contactbuffers_20260709.json
data/calibration/unity_physx_native_solver_state_20260709.json
data/calibration/unity_physx_native_solver_state_convexconvex_arm_20260709.json
data/calibration/unity_physx_native_solver_state_solvecontact_20260709.json
```

早期 ContactBuffer 报告来自 `log/unity_runtime_probe_20260709_113402/events.collision_pause_snapshot.json`；
后续 solver row / solveContact 报告来自同日 streamed event-sink 采样。raw log 只留本地，
小报告用于和本地 pyphysx / trace-driven replay 对比。
