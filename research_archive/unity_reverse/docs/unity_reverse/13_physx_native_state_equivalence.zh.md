# PhysX Native State 等价性审计

旧长版已归档：

```text
docs/archive/unity_reverse_superseded_20260709/13_physx_native_state_equivalence.zh.md
```

这页回答一个问题：

```text
Unity 在 stone-stone 碰撞那一帧喂给 PhysX 的完整 native state，
是否已经和本地 pyphysx 构造的 state 一模一样？
```

## 结论

没有证明，而且现有证据反证“当前本地 replay 已经一模一样”。

高层机制已经很清楚：PCM、patch friction、solver、材质、fixed timestep、Rigidbody 标量、convex cooking 大路径都已恢复。2026-07-09 的 stream capture 已经抓到 stone-stone `createFinalizeSolverContacts.after` 的 `ContactBuffer / FrictionPatch / SolverContactHeader / SolverContactPoint / SolverContactFriction`，并且 Unity raw normal row 与按 PhysX 源码从 `ContactBuffer + PxSolverBodyData` 反算的 row 只差 `4.45e-7` 量级。

2026-07-09 17:12 的 runtime hull capture 又把缺口向前推了一层：
`readyForFieldDiff=true` 且 `readyForContactGenerationDiff=true`，PCM 入口的
shape GeometryUnion、transform、cache/contactBuffer、solver/writeback 边界都已经抓到。

所以当前缺口不再是“finalizer row 公式未知”，也不再是
`solveContactConcludeBlock` 单对 body delta 公式未知，更不是普通 endpoint 样本不够。

2026-07-09 晚上新增的 direct PCM 审计把此前 “Unity 2 contacts / 本地 3-4 contacts”
分叉进一步拆开：

```text
1. 本地 pyphysx Python pose 传参曾有实锤错误：
   pyphysx caster 要 [w,x,y,z]，旧 replay 传了 [x,y,z,w]。
2. 修正四元数顺序并使用 Unity 原生坐标 + Unity raw PCM-after cache 后，
   本地 refreshContactPoints 保留 2 点，invalidate_BoxConvex=false。
3. 继续用 immediate-mode PxGenerateContacts 仍会得到 3 点或 0 点；源码原因是
   NpImmediateMode.cpp 会重新分配 PCM manifold，只拷 mRelativeTransform / contacts /
   warm indices，漏拷 mQuatA / mQuatB，导致后续路径不等价 Unity scene。
4. 绕过 immediate wrapper，直接调用和 Unity scene 一样的 g_PCMContactMethodTable
   后，local direct PCM contact_count=2，normal 与 Unity 一致，两个 separation
   只差约 7e-8m。
5. 同一 capture 中，把 direct PCM contacts 喂进 `ContactBuffer + PxSolverBodyData`
   row 重构器后，raw-vs-direct normal-row 最大差约 `5.86e-5`。
```

对应证据：

```text
data/calibration/unity_pcm_refresh_invalidate_audit_20260709.json
data/calibration/unity_direct_pcm_vs_immediate_audit_20260709.json
data/calibration/unity_direct_pcm_solver_row_bridge_20260709.json

Unity:
  count = 2
  separations = 0.009429097175598145, 0.009273719973862171
  normal0 = [-0.9891765117645264, -1.95383673684546e-08, 0.14673064649105072]

local direct scene-style PCM:
  count = 2
  separations = 0.009429019875824451, 0.009273648262023926
  normal0 = [-0.9891765117645264, -1.95383673684546e-08, 0.14673064649105072]

local immediate PxGenerateContacts:
  count = 3 in local/BigConvex cases, or 0 in hull-only patched case

direct PCM -> solver row bridge:
  max contact delta ~= 7.73e-8
  max direct-vs-Unity computed row delta ~= 5.84e-5
  max raw-vs-direct computed row delta ~= 5.86e-5
  bridge_closed_at_contact_prep_precision = true
```

当前最重要的结论：`PxGenerateContacts` immediate probe 不是 Unity scene narrowphase
的等价替身。后续本地碰撞 replay 要使用 scene-style PCM cache 路径，至少要保留
`mQuatA / mQuatB`、`mRelativeTransform`、contacts、warm-start indices 和
同一 `g_PCMContactMethodTable` 调用边界。现在 contact generation 的首个
stone-stone cached manifold 和 normal-row 准备链已经对到 Unity。下一步是把 direct PCM /
Unity cache 语义接回完整碰撞 replay，验证 post-solve 速度和 endpoint 是否自然收敛到 2cm。

2026-07-10 的前半段 runtime capture 又把 `BESTSHOT -> first PCM entrance` 单独拆了出来。
这轮不是 endpoint 盲采，而是同时抓：

```text
socket:
  RESETPOSITION / RESETSTATE / BESTSHOT / MOTIONINFO / POSITION

sliding trace:
  UnityEngine.Random.Range(-0.0002, 0.0002) 每次返回值

native PCM:
  PxcPCMContactConvexConvex before/after
  transform0 / transform1
  PxCache / PersistentContactManifold
  ContactBuffer count
```

对应文件：

```text
log/unity_runtime_probe_20260710_012403/events.jsonl
log/unity_runtime_probe_20260710_012403/front_half_pcm_summary.json
data/calibration/front_half_pcm_samples_20260710_012534.jsonl
data/calibration/front_half_pcm_replay_compare_20260710.json
data/calibration/front_half_threshold_replay_audit_20260710.json

tools/calibration/launch_front_half_pcm_probe.py
tools/calibration/run_front_half_pcm_sampler.py
tools/reverse/front_half_pcm_replay.py
tools/reverse/summarize_front_half_pcm_capture.py
tools/reverse/compare_front_half_pcm_replay.py
tools/reverse/audit_front_half_threshold_replay.py
unity_front_half_sim.py
tests/test_unity_front_half_sim.py
config/front_half_pcm_probe_20260710.json
```

关键结果：

```text
6 / 6 个 BESTSHOT 都抓到 first PCM
6 / 6 个 BESTSHOT 都抓到 first nonzero-contact PCM

用真实 Random.Range 摩擦序列重放 BESTSHOT -> first-contact:
  active x/y RMSE ~= 0.01128m
  active x/y mean error ~= 0.00874m
  active x/y max error ~= 0.02194m

clean 正碰速度 spot-check:
  local precontact vx ~= +0.000275, vy ~= -0.796006, w ~= +0.183981
  Unity solver body vx ~= +0.000268, vy ~= -0.794515, w ~= +0.177870
  delta ~= 0.000007 / -0.001491 / +0.006111

正碰:
  first-any PCM == first-contact PCM
  contact_count = 2

擦边:
  first-any PCM 可能 contact_count = 0
  需要继续等到 first-contact PCM
  contact_count = 4
```

这说明前半段滑行的位置推进已经不是 10cm 级误差来源。`Random.Range` 调用数在这轮里
直接对应滑行 tick 主序列，`stride=1` 就能把 first-contact active x/y 推到厘米级。

进一步的 self-stop 审计不再使用 Unity first-contact 时间截断，而是让本地 replay
按 active-target 中心距阈值自行停止：

```text
threshold = 2R + 2*contactOffset
R = 0.140875m
contactOffset = 0.01m
threshold = 0.30175m

data/calibration/front_half_threshold_replay_audit_20260710.json

observed Unity first-contact center distance:
  mean ~= 0.29805m
  max  ~= 0.30017m

self-stop replay，离散 FixedUpdate tick:
  active x/y RMSE ~= 0.00905m
  active x/y max error ~= 0.02194m
  mean abs step delta vs Unity first-contact ~= 0.50 fixed tick
  reached threshold = 5 / 6

MOTIONINFO -> self-stop replay，离散 FixedUpdate tick:
  active x/y RMSE ~= 0.001061m
  active x/y mean error ~= 0.001009m
  active x/y max error ~= 0.001734m
  reached threshold = 6 / 6
```

这条证据比单纯“拿 Unity 时间截断”更接近训练模拟器：本地已经能用物理接触壳
`2R + 2*contactOffset` 在离散 tick 切到 first PCM entrance。从 `MOTIONINFO` 起算时，
6 条平移状态全部进 2mm；因此前半段剩余缺口不是 tick 相位或位置公式，而是需要把
hidden yaw / actor pose 作为完整状态传入后续 scene-style PCM。

剩余最明显的不等价是 hidden orientation：

```text
target yaw:
  seq0 ~= 0
  seq1 ~= +0.02684 rad
  seq2 ~= -0.08315 rad
  seq3 ~= +0.10943 rad
  seq4 ~= -0.33360 rad
  seq5 ~= +0.32271 rad

active inferred initial-yaw offset:
  max abs ~= 1.26601 rad
```

这些 yaw 不是 socket `POSITION` 能看到的字段。受控 sampler 的 `RESETPOSITION`
只保证 x/y，不证明 Rigidbody/shape quaternion 被清零；同一 active stone 重复使用时，
Unity native quaternion 显示姿态会继承/累积。因此当前的 first-PCM native-state
等价性重点已经从“摩擦公式未知”转到：

```text
1. 本地 game state 必须持续跟踪 stone quaternion/yaw，不只跟踪 x/y。
2. debug reset 样本不能当成“姿态清零”的证据。
3. 逐字段比较时必须区分 first-any PCM 与 first-contact PCM。
4. 完整 replay 要把 active/target 的 native quaternion 一起喂给 scene-style PCM / solver。
```

这里已经有反编译级别的生命周期证据，不再只是从样本猜测：

```text
DCP.SetStonesByBody -> func61068
DCP.ResetStones     -> func61078

func61068:
  按 body x/y 激活或失活既有 stone GameObject；
  只调用 Transform.position 写入，没有写 Transform.rotation。

func61078:
  把既有 stone 移回 origin position 并 SetActive(false)；
  同样没有写 quaternion/rotation。
```

所以 hidden yaw 的正确处理不是拟合一个 yaw 偏置，而是保存每个编号石壶的历史姿态。
`unity_front_half_sim.py` 已按这个语义实现：冷启动才清 yaw；协议位置 reset 默认只改
x/y 和静止速度；碰撞结束后由持久 Scene 把新的 pose/velocity 回写到同一 actor 槽。

同源 17:12 样本的完整 Scene replay 现状：

```text
data/calibration/unity_physx_collision_probe_native13000_pcm_hull_runtime_posefix_20260709.json
data/calibration/unity_direct_pcm_scene_replay_gap_20260709.json

active endpoint error ~= 0.00840m
target endpoint error ~= 0.10087m

local Scene first contact:
  contact_count = 4
  separation ~= -0.00691m

Unity/direct PCM first cached manifold:
  contact_count = 2
  separation ~= +0.00943m / +0.00927m
```

这说明：公式链条已经被推到很深，但完整 pyphysx Scene 从头跑仍没有进入
Unity 的同一 PCM/cache 状态；它一开始就走 fresh/local manifold，导致 target endpoint
仍有 10cm 级误差。

2026-07-09 晚上又把这个结论接进了完整 Scene 代码，而不是只停留在 direct PCM 探针：

```text
tools/reverse/probe_physx_collision_alignment.py
  新增 --unity-runtime-feature-mode hull / hull-bigconvex
  新增 --unity-runtime-feature-events / --unity-runtime-feature-line
  formal-recovered mesh 改为未缩放 z-up 顶点 + PxMeshScale [x,z,y]

tools/calibration/launch_unity_probe_browser.py
  native nested raw 默认开启，避免漏抓 BigConvex pointed arrays

tools/calibration/decode_runtime_probe_events.py
tools/reverse/extract_physx_native_solver_state.py
  现在会显式报告 BigConvex samples / valencies / adjacentVerts 三组 raw arrays 是否完整
```

最小 smoke 证据：

```text
data/calibration/unity_physx_collision_probe_sample84_runtime_feature_smoke_20260709.json
data/calibration/unity_physx_collision_probe_sample84_runtime_feature_immediate_20260709.json

active / target runtime patch:
  hull old_buffer_size 4776 -> new_buffer_size 4008, ok=true
  BigConvex samples=3072 / valencies=512 / adjacent=384, ok=true

但 full Scene 第一帧 local immediate contact 仍是 fresh 4 contacts：
  contact_count = 4
  first separation ~= -0.047685m
  manifold a_indices/b_indices 来自本地 fresh generation
```

所以现在不是“runtime hull patch 没接进完整 Scene”。这条代码通道已经打通。
剩余分叉仍然在完整 Scene 的 first-frame entrance state：pose / 时机 / target 初始状态 /
PCM pair cache 生命周期与 Unity 不同。本地如果从 Unity after-cache raw 进入，可以稳定输出
Unity 的 2-contact manifold；但从 fresh/before 状态进入仍会生成本地 4-contact manifold。

2026-07-09 继续把这个分叉又拆掉两层，得到当前最具体的误差来源：

```text
tools/reverse/probe_physx_collision_alignment.py
  新增 --unity-runtime-feature-coordinate pyphysx-zup / unity-native
  新增 --handoff-center-distance

data/calibration/unity_physx_collision_probe_native13000_runtime_feature_zup_rebuilt_20260709.json
data/calibration/unity_physx_collision_probe_native13000_runtime_feature_zup_interpdist_20260709.json
data/calibration/unity_physx_collision_probe_native13000_runtime_feature_zup_interpdist_contactreport_20260709.json
```

第一，Unity runtime `Gu::ConvexHullData` 的 4008 bytes 是 Unity/PhysX native xyz
坐标语义，不能原样塞进本地 z-up Scene。必须只转换有坐标含义的字段：

```text
polygons.plane normal: x,y,z -> x,z,y
hullVertices:          x,y,z -> x,z,y
topology/index streams: facesByEdges8 / facesByVertices8 / vertexData8 不变
BigConvexRawData:      从换轴后的 runtime hull 重新 rebuild
```

对照结果：

```text
旧路径：Unity raw hull 原样 patch 到 z-up Scene + synthetic BigConvex
  active error ~= 0.20025m
  target error ~= 4.43507m

新路径：runtime hull 换轴 + 从换轴后 hull rebuild BigConvex
  active error ~= 0.00716m
  target error ~= 0.08409m
```

第二，剩余 8cm 主要来自 handoff 入口时机。Unity first PCM 抓到的 active-target
中心距是：

```text
Unity native/z-up relative p:
  [-0.2898406982, 0.0242385864, 0]
  center distance ~= 0.2908524358m

本地离散 first <= 2R handoff:
  [-0.2839365005, 0.0233149529, 0]
  center distance ~= 0.2848921258m
```

这 5.96mm 的入口中心距差，会把本地 Scene 从接近 Unity 的浅 separation
推成另一组 first-contact manifold。把 MOTIONINFO -> handoff 按 Unity 中心距线性插值后：

```text
handoff source = interpolated_center_distance
handoff step   = 1159.24610183877
handoff x,y    = (2.3516829521, 5.4899161590)
handoff v,w    = (0.0002691213, -0.7938470066), 0.1860218273

full Scene endpoint:
  active error ~= 0.00481m
  target error ~= 0.00575m
  combined RMSE ~= 0.00530m
```

active yaw 也不需要手填 Unity 抓到的常数才能闭合。同一配置下改用
`--active-yaw-source integrated-precontact`：

```text
data/calibration/unity_physx_collision_probe_native13000_runtime_feature_zup_interpdist_integratedyaw_20260709.json

integrated yaw:
  release -> MOTIONINFO ~= 0.0264301344rad
  MOTIONINFO -> handoff ~= 0.2233496193rad
  total ~= 0.2497797536rad = 14.3113deg

best local sign:
  active-yaw-integral-sign = -1
  active error ~= 0.00474m
  target error ~= 0.00612m
```

这条证据非常关键：在同一 native sample 上，碰撞公式、solver、runtime hull/BigConvex
和 handoff 入口距离同时对齐后，完整 Scene replay 已经进入 1cm 内。此前 10cm
不是 PhysX 碰撞公式未知，而是完整 Scene 喂给 PCM 的入口 state 不同。

仍需注意：`enable_immediate_contact_probe` 里的 PxGenerateContacts wrapper 仍会报
4 contacts；这不是 Scene 内部 PCM 的等价证据。新的 endpoint 5mm 级闭合来自完整
pyphysx Scene 自己的 simulate/contact report 路径，不能再用 immediate wrapper 的 4 点
作为“Scene 未对齐”的直接结论。

把这个 5mm 配置直接套到旧的 12 条 endpoint-only controlled collision 样本上，不能
直接泛化到 2cm：

```text
data/calibration/unity_physx_collision_probe_controlled12_runtime_feature_zup_interpdist_integratedyaw_20260709.json

best over active-yaw-integral-sign +/-1:
  active RMSE ~= 0.03540m
  target in-play RMSE ~= 0.28492m
  combined RMSE ~= 0.19386m
```

这个负结果不推翻 native13000 的闭合；它说明旧 endpoint 样本缺少每个 shot 自己的
first PCM entrance state。`handoff-center-distance=0.2908524358m` 是 native13000
抓到的那一帧，不是所有碰撞场景的通用真值。下一步泛化必须从运行时抓/推导每个
collision 的 first PCM pose、relative transform、yaw、target state，而不是把单样本
中心距硬套到全部训练样本。

2026-07-10 离线合龙把这条路推广到前半段 clean capture，没有再采 Unity：

```text
tools/reverse/export_front_half_pcm_entrance_truth.py
tools/reverse/build_front_half_explicit_handoff_samples.py
tools/reverse/probe_physx_collision_alignment.py

data/calibration/front_half_pcm_entrance_truth_20260710.json
data/calibration/front_half_explicit_handoff_samples_localvel_20260710.jsonl
data/calibration/front_half_explicit_handoff_collision_replay_localvel_targetsettle_sweep_20260710.json
```

关键改动不是调物理参数，而是把 Unity first-contact PCM 入口的每条样本 pose/yaw
显式喂给完整 pyphysx Scene：

```text
active handoff:
  x/y/yaw = Unity firstPcmWithContacts.before transform0
  vx/vy/w = BESTSHOT + captured Random.Range 前半段重放
  vz = -0.0981m/s，用于补齐进入 solver 前的重力一帧

target:
  x/y = reset_position，与 Unity first-contact transform1 一致到 1e-14m 量级
  yaw = Unity firstPcmWithContacts.before transform1
  target 先加入 Scene 并 settle >= 0.01s，再加入 active
```

A/B 结果非常明确：

```text
fresh local Scene，target 和 active 在 handoff 同时加入:
  active RMSE ~= 5.15cm
  target in-play RMSE ~= 25.64cm
  combined RMSE ~= 17.52cm

target 先存在 0.01s 后再加入 active:
  active RMSE ~= 1.12cm
  target in-play RMSE ~= 4.13cm
  combined RMSE ~= 2.88cm

target settle 0.01 / 0.02 / 0.05 / 0.10s:
  结果基本平台，best 0.05s 只到 combined ~= 2.87cm
```

逐样本看，14000 从 target 50.6cm 误差降到 1.5cm；14004 约 2.2cm；
14005 约 4.6cm；主要剩余离群是 14002，target 约 6.3cm。这个结果说明：

```text
已排除：
  PhysX 碰撞公式未知
  Unity runtime hull / BigConvex 未接入
  单纯漏掉 active/target yaw
  单纯漏掉 solver body 竖直速度

当前未闭合：
  target/stone 已在 Unity Scene 中存在的生命周期和 contact cache
  first-any PCM -> first-contact PCM 之间的 pair cache / manifold warm-start
  本地从 fresh Scene 进入时 contact_count 和 Unity 不一致的样本
```

对应 contact report 对比：

```text
sample 14000:
  Unity first-contact: 0 -> 2 contacts
  local fresh:         1 -> 2 contacts
  target pre-exists:   endpoint 恢复到 1.5cm

sample 14002:
  Unity first-contact: 0 -> 2 contacts
  local fresh:         4 -> 4 contacts
  target pre-exists:   target 仍约 6.3cm

sample 14004 / 14005:
  Unity first-contact: 0 -> 4 contacts
  local fresh:         4 -> 4 contacts
  endpoint 已在 2cm 到 5cm 档位
```

所以当前结论是：前半段 `MOTIONINFO -> first PCM entrance` 的平移推进已经毫米级，
完整 Scene 尾段也不再是 10cm 级；剩余要复刻的不是公式，而是 target/contact
lifecycle 和 2-contact 样本的 pair cache 状态。更准确的本地实现应保留稳定的
stone GameObject/Rigidbody/shape 身份：已投出的 target 持续留在 Scene，待投 active
在出手时按 Unity 的 `SetActive(true)` 语义启用；reset 只搬位置并保留 quaternion。
绝不能在 first-PCM handoff 临时新建 active/target 两个 actor。

Scene/cache 的合龙顺序固定为：

```text
1. 一局只建一个 pyphysx Scene；16 个 stone 槽保持稳定 actor/shape identity。
2. inactive stone 禁用 simulation shape；出手时启用同一 shape，写 release pose/v/w/material。
3. 每个 0.01s tick 先用 Newfrictionstep 写 active velocity，再 scene.simulate(0.01)。
4. 让 broadphase/PCM 自己创建 first-any/first-contact pair，不手工灌 fresh cache。
5. 碰撞回调把材质切回 0.6 并停用 custom sliding；Scene 继续跑到全场静止。
6. 把每个 actor 的 x/y/quaternion/velocity 回写到持久状态；reset 不清 quaternion。
```

验收必须逐层通过：first-PCM pose/velocity -> contact count/normal/point/separation ->
0.02s writeback velocity -> 双壶 endpoint。只有这四层都对齐，才允许接入训练主循环。

### 2026-07-10：exact first-PCM native entry 的 scalar 等价性已通过

此前“exact pose 仍会得到 4 contacts”的结论属于默认 x64 SSE PhysX，不可继续作为 Unity
native state 缺失的证据。保持所有 native 输入不变，仅将 PhysX 编译为
`PX_SIMD_DISABLED` scalar 后端，六条 Unity first-contact call 的结果均闭合：

```text
contact count:                 6 / 6 match
local point / normal / pen:    max component delta = 5.960464477539063e-08
full manifold generation:      scalar result equals Unity after-manifold raw
```

也就是说，在 **exact Unity first-PCM entrance** 边界，当前已知的 transform、hull、BigConvex、
cache、params 与 scalar PhysX 机制足以复现 Unity；剩余未闭合的层级上移为“从协议/持久场景自然
推进到该 exact entrance 的 tick、hidden yaw 与历史生命周期”，而非 PCM contact formula。
证据：`tools/reverse/audit_scalar_pcm_backend.py` 和
`data/calibration/scalar_pcm_backend_audit_20260710.json`。

### 2026-07-10：第二次 PCM 的真实 cache 生命周期已对齐

为排除“本地 Scene 只是恰好在首帧生成两点”的假象，受控 `14000` 正碰额外抓取了连续的
`PxcPCMContactConvexConvex` 调用。原始日志是
`log/unity_runtime_probe_20260710_p4_second_pcm/unity_runtime_probe_20260710_233626/events.jsonl`。
第二次调用入口并没有保留上一帧的完整 contact points：Unity 的 `numContacts` 和
`numWarmStartPoints` 都回到 0，然而 feature-index 数组仍为 `a=[8,209,43]`、`b=[81]`；函数返回后
再次稳定产生两个 contacts。

同一 pose 下的 scalar 复验给出严格的反事实：灌入 Unity call 1 after 的完整 manifold 会得到
3 contacts；灌入 Unity call 2 before 的 task-local cache 则得到 2 contacts，两个 separation 与
Unity call 2 after 完全相同。因此差异不是 hull、GJK、PCM 公式或 pose，而是本地 Scene 此前错误
保留了完整 manifold。scalar pyphysx 已改为每个 convex-convex Scene PCM 调用前清空 contact points、
relative transform 与 warm-start count，同时保留 feature-index bytes，模拟 Unity 的 task-local
重建步骤。

复跑 `MOTIONINFO -> local-contact` 后四条自然到达样本的 contact count `4/4` 一致，
证据为 `data/calibration/persistent_scene_motioninfo_local_contact_after_pcm_lifecycle_20260710.json`。
后续误差审计不得再把 PCM cache 作为待猜参数；剩余边界是 hidden yaw、solver writeback 与碰撞后
连续 Scene 姿态。

### 2026-07-10 持久 Scene 前半段实装结果

上述第 1 至第 3 步已经落地，不再只是计划：

```text
unity_front_half_physx.py
tools/reverse/audit_persistent_scene_front_half.py
data/calibration/persistent_scene_front_half_state_audit_20260710.json
data/calibration/persistent_scene_motioninfo_front_half_state_audit_20260710.json
data/calibration/persistent_scene_front_half_contact_audit_20260710.json
```

后端保留同一 Scene 和 actor/shape identity；inactive 时关闭 simulation shape，reset
只改位置并保留完整 quaternion；出手后每 tick 先写 `Newfrictionstep` 结果再
`scene.simulate(0.01)`。用 0.30175m physical PCM shell 自停：

```text
BESTSHOT -> shell:
  6 / 6 reached
  active position RMSE ~= 1.159mm
  max                  ~= 1.350mm

MOTIONINFO -> shell:
  6 / 6 reached
  active position RMSE ~= 0.767mm
  max                  ~= 0.934mm
```

样本 14000 的 cold-actor BESTSHOT replay 同时把 entrance yaw 对到约
`1.23e-4rad`，水平 `vx/vy` 对到 `1e-7m/s` 量级，`w` 对到 `1.5e-4rad/s`
量级。这足以说明前半段主公式已经闭合，但不能把 first-PCM 完整 native pose 标成逐位
等价：PCM support feature 恰好落在很窄的边界时，远小于训练终点容差的入口微差也可能
改变 manifold 数量。

审计显式把 active yaw 置零时，后四条所需起始 yaw 为历史量而不是拟合参数；正式后端
不置零，而是从同一 actor quaternion 继续。MOTIONINFO 协议本身只有 x/y/vx/vy/w，
所以脱离整局历史时不可能单靠五个字段唯一恢复 orientation。

必须保留一个边界结论：physical PCM shell 和 local Scene contact report 不是同一验收项。
同一持久 Scene 的 local-contact 审计只有 4 / 6 在现有 Unity 噪声流结束前产出报告；
其中 Unity 2-contact 的正碰仍由本地生成 4 contacts，而 Unity 4-contact 的两条能匹配
数量。2026-07-10 的逐字段 A/B 已把样本 14000 的原因继续缩到 first-PCM pose：

```text
tools/reverse/audit_first_pcm_pose_feature_boundary.py
data/calibration/first_pcm_pose_feature_boundary_audit_20260710.json

yaw=0:                              4 contacts
补齐历史 yaw，剩余 yaw 差约 1.33e-7rad: 4 contacts
只补 Unity quaternion:              4 contacts
只补 Unity native Z（横向 38.146um）: 4 contacts
只补 Unity native Y（竖直 0.954um）: 2 contacts
只把本地冰面下移 1 ULP:             2 contacts
只把本地冰面下移 2 ULP:             4 contacts
只补 Unity native position:          2 contacts
补完整 Unity pose:                   2 contacts
```

在补齐历史 yaw 后，本地 native Y 比 Unity 高 `9.5367431640625e-7m`，恰好是该 world
高度的一个 float32 ULP；native Z / protocol X 另差 `-3.814697265625e-5m`。单独补 native Y，
同一 Scene、actor、PCM cache、runtime hull/BigConvex 和 solver 就立即生成 2 contacts；
单独补 native Z 或 quaternion 都仍是 4 contacts：

```text
normal     = [0.9891765118, 1.95e-8, -0.1467306465]
separation = 0.0167143047 / 0.0165289175m
```

normal 与 Unity 闭合；再补横向位置后 separation 也闭合到约 `1e-8m`。这严格证明的是
**样本 14000** 的 4-vs-2 由 first-PCM 竖直支撑高度跨过 feature 边界触发，不能直接外推到
其余五条样本。更上游的冰面 A/B 也只对 14000 建立了因果：不注入 active pose，只把
本地 ice actor 下移一个 ULP，active 会自然落到 Unity native Y 并生成 2 contacts；下移
两个 ULP 又回到 4 contacts。

### 2026-07-10 六样本分层审计表

统一审计见：

```text
tools/reverse/audit_first_pcm_ice_ulp_multisample.py
data/calibration/first_pcm_ice_ulp_multisample_audit_20260710.json
```

其中 `Unity tick` 列使用捕获的 Random.Range 序列、补齐每条样本的历史 yaw，并固定目标壶
Unity native pose；`exact pose` 列再把主动壶完整 native pose 也替换为 Unity 值。因而该表
用于定位最早分叉，不代表生产模拟器可以依赖 oracle。

| 样本 | Unity contacts | BESTSHOT 到 PCM shell 位置误差 | Unity first-contact tick 的本地结果 | exact Unity pose + fresh PCM | first contact 前 PCM 调用 | 最早未对齐环节 |
|---|---:|---:|---|---|---:|---|
| 14000 | 2 | 1.350mm | 4；native Y 高 0.954um，横向差 38.147um | 2 | 0 | first-PCM 石壶-冰面支撑高度；下移 1 ULP 可闭合 |
| 14001 | 2 | 1.280mm | 4；水平 pose 已逐位相同，native Y 高 0.954um | 4 | 0 | exact pose 进入 PCM 后的 support/feature/manifold 点选择 |
| 14002 | 2 | 1.169mm | 0；主动壶沿 native X 落后 10.445mm，表现为一 tick 相位差 | 4 | 0 | 先有 handoff/tick 分叉；强制 exact pose 后仍有 PCM feature 分叉 |
| 14003 | 4 | 1.264mm | 4 | 4 | 4 | contact count、normal、separation 已闭合；只剩生产历史 yaw 要自然继承 |
| 14004 | 4 | 1.277mm | 0；主动壶沿 native X 落后 10.437mm，表现为一 tick 相位差 | 2 | 8 | handoff/tick 与 pre-contact PCM manifold 生命周期两层都未闭合 |
| 14005 | 4 | 0.076mm | 4 | 4 | 3 | contact count、normal、separation 已闭合；只剩生产历史 yaw 要自然继承 |

逐样本 exact-pose direct PCM 的 contact 数为：

```text
Unity:                    [2, 2, 2, 4, 4, 4]
local fresh PCM:          [2, 4, 4, 4, 2, 4]
local + Unity before raw: [2, 4, 4, 4, 2, 4]
```

三个 narrow-phase 参数已逐字段相同：`contactDistance=0.02`、
`meshContactMargin=0.01`、`toleranceLength=1`。当前本地 runtime hull SHA16 为
`7c5429592f144782`；从该 hull 重建的 BigConvex 三组数组 SHA16 分别为
`ec18837768a60ec7 / ccf344e149137aea / d382b34acd8d58c6`，与 Unity 捕获哈希一致。
所以 14001/14002/14004 不能再归因于“4008 字节 hull 没灌进去”或 BigConvex 数组内容不同。

另一方面，把 2048 字节 `before manifoldWindowRaw` 作为 seed 灌给本地 direct PCM 没有改变
三条失败结果。这只排除了“复制一段 raw cache 就能修好”的简单方案；不能证明完整 Scene
cache 对象、ConvexHullData 头部微差、feature ID、pair 创建/刷新顺序已经等价。当前最窄的
剩余范围就是这组 PCM 入口内部状态，再叠加 14002/14004 的一 tick handoff 相位。

## 当前误差

### 2026-07-11：确认 Random.Range 与物理 step 不是一一对应

六组 P6 同源重放给出了一个可直接复现的时相因果：14002/14004 的 Unity
`firstPcmWithContacts` 都发生在最后一条 `sliding.random_range.friction` 之后。旧本地把每条
Random.Range 强制绑定一次 `Scene.simulate(0.01)`，在摩擦序列结束时直接退出，因此少执行了一帧
fixed physics，造成两个样本本地没有 stone-stone contact。

这不是 PCM、hull 或 material 参数问题。将 Unity 已捕获的 first-PCM pose 直接放入本地 scalar
Scene，并且只额外调用一次 `Scene.simulate(0.01)`，14002 得到 2 contacts，14004 得到 4 contacts，
与 Unity 的 contact count 一致。生产前半段现已把该 trailing physics step 编码为明确规则：它不消费
额外 RNG，也不再运行 `Newfrictionstep`。

修复后六组均自然进入接触；剩余 P6 target 终点误差集中在 14002 `55.633mm`、14004 `39.006mm`。
它们的 first-contact entrance quaternion/yaw 与 Unity 仍有显著差异，故下一层是 collision
writeback 后的持久 yaw/friction 状态，而不是 contact 是否发生。

```text
unique-role current best:
  active RMSE ~= 3.86cm
  target in-play RMSE ~= 11.32cm

per-sample entrance-state oracle:
  active RMSE ~= 1.35cm
  target in-play RMSE ~= 1.48cm
  7 / 7 in-play pair 双终点进 2cm

visible-feature correction leave-one-out:
  active RMSE ~= 5.22cm
  target in-play RMSE ~= 30.98cm
  0 / 7 双终点进 2cm
```

解释：如果每条样本都单独改 hidden entrance/native-state proxy，可以把现有样本压到 2cm；但用可见特征无法泛化这些修正，所以它不是训练用通用公式。

## 13000 同样本审计

2026-07-09 后续补了一条同 shot 的桥接样本。当前以 14:55 with-writeback run
为准，不再混用旧 solvecontact endpoint：

```text
data/calibration/unity_native_solver_collision_probe_20260709_withwriteback.jsonl
data/calibration/unity_physx_collision_probe_native13000_withwriteback_bestgeom_20260709.json
data/calibration/unity_collision_upstream_mismatch_audit_20260709.json
tools/reverse/summarize_collision_upstream_mismatch.py

sample 13000:
  v0 = 3.4
  h0 = 0
  w0 = 0
  target stone 8 reset to (2.375, 5.2)
```

用当前 best 几何参数复跑本地 pyphysx 后：

```text
local active endpoint error ~= 2.29cm
local target endpoint error ~= 19.87cm
```

2026-07-09 继续给本地 pyphysx 补了 `PxGenerateContacts` immediate-mode 探针：

```text
D:\esp\tmp\curling_pyphysx\src\pyphysx.cpp
pyphysx.generate_contacts_between(...)

data/calibration/unity_physx_collision_probe_native13000_immediate_contact_20260709.json
```

这个探针在本地同一套 actor/shape/pose 上直接吐 PhysX raw contact generation 结果，
因此不再只依赖 post-step `ContactPairPoint`。最新字段级差异修正了旧的
normal-angle 结论：normal 方向已经贴合，首个明确分叉是 contact 数量和 separation：

```text
local pyphysx immediate pre_step t=0.00:
  contact_count = 4
  target-side normal angle ~= -2.812468deg
  separation ~= -0.00152m

local pyphysx first ContactPairPoint report:
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

这比上一版结论更强：local 侧已经有 raw contact generation，不只是 report-layer。
当前最高优先级误差源是
`contact generation / manifold reduction / exact first-collision-frame timing / cooked hull or contact cache parity`，
不是 `friction/restitution`，也不是 `ContactBuffer -> solver row` 或 solver consume 公式。

针对性反证：把本地从简化 ring/cylinder 换成恢复出的 formal collider mesh 后，
并没有消除 `4 vs 2` 的 contact-count 分叉：

```text
data/calibration/unity_physx_collision_probe_native13000_immediate_formal_contact_20260709.json

formal mesh local active endpoint error ~= 1.50cm
formal mesh local target endpoint error ~= 17.53cm
formal mesh immediate contact_count = 4
formal mesh target-side normal angle ~= -5.62deg
```

所以当前不能简单说“换成这个 recovered formal mesh 就等价 Unity cooked hull”。
它略微改善 endpoint，但 normal 反而偏离 Unity 的 `-2.8125deg`，contact 数量仍不对。

另一个针对性反证是只把 handoff 边界提前到 `2R + 2*contactOffset`：

```text
data/calibration/unity_physx_collision_probe_native13000_immediate_handoff_extra001_20260709.json

handoff_extra = 0.01
local active endpoint error ~= 6.39cm
local target endpoint error ~= 40.74cm
first immediate contact_count = 1
first immediate separation ~= +0.00668m
first immediate target-side normal angle ~= 0deg
```

这说明问题也不是一个标量 handoff threshold。提前切入会让 separation 变正，
但 contact manifold / normal / endpoint 全部变差；必须一起对齐 first-frame pose、
PCM/contact cache 和 cooked hull/local pose。

2026-07-09 又补了一个更直接的 bodyFrame 回灌实验：

```text
tools/reverse/probe_unity_finalizer_pose_contacts.py
data/calibration/unity_finalizer_pose_contact_replay_20260709.json

Unity firstStoneStone finalizer:
  relative body0-body1 distance xz ~= 0.289936m
  active bodyFrame yaw ~= 12.818889deg
  contact_count = 2
  separations ~= +0.00859m / +0.00838m
  target-side normal angle ~= -2.812503deg

local PxGenerateContacts, fed Unity finalizer relative bodyFrame pose:
  ring geometry, zero yaw: contact_count = 4
  ring geometry, Unity yaw cases: contact_count = 3
  formal recovered mesh, zero yaw: contact_count = 4
  formal recovered mesh, Unity yaw cases: contact_count = 3
```

这条证据把“只是本地 handoff 位置/姿态没切准”进一步降级了：即使拿
Unity finalizer 的相对 bodyFrame 姿态去问本地 PhysX，本地也回不到 Unity 的
2-contact manifold。因此当前“cooked hull”问题不是重新找离线输入点云，而是要证明
Unity 运行时真正参与 contact generation 的 `PxShape / PxConvexMeshGeometry / shape.localPose /
PCM persistent manifold cache` 和本地是否逐字段一致。

2026-07-09 17:12 的 runtime hull dump 已经证明第一处字段级分叉：

```text
raw events:
  log/unity_runtime_probe_20260709_171257/events.jsonl

endpoint trigger:
  data/calibration/unity_native_pcm_hull_runtime_probe_20260709_171257.jsonl

native report:
  data/calibration/unity_physx_native_solver_state_pcm_hull_runtime_20260709_171257.json

runtime hull diff:
  data/calibration/unity_runtime_hull_vs_pyphysx_diff_20260709_171257.json
  data/calibration/pyphysx_cooked_stone_hull_probe_unity_flags_rebuilt_native_runtime_20260709.json
  data/calibration/unity_runtime_hull_vs_pyphysx_native_runtime_diff_20260709.json
  tools/reverse/compare_unity_runtime_hull_to_pyphysx.py
```

本轮 capture 质量：

```text
rowCount = 132
stone_stone rows = 8
PxcPCMContactConvexConvex before/after = 6 / 6
readyForFieldDiff = true
readyForContactGenerationDiff = true
```

Unity stone-stone PCM 两端 shape 的运行时 hull：

```text
geometryType = eCONVEXMESH
scale = (0.1127000079, 0.1150000021, 0.1127000079)
nbHullVertices = 128
nbPolygons = 66
nbEdges = 192
vertexRefCount = 384
runtime buffer bytes = 4008
```

和本地 rebuilt pyphysx hull 对比：

```text
Unity runtime sha16 = 7c5429592f144782
local rebuilt sha16 = fc08aa00c31b708a
byteEqual = false
byteDiffCount = 2318 / 4008

polygons / hullVertices / facesByEdges8 / facesByVertices8 / vertexData8 全部不 byte-level 相同。
```

随后给本地 pyphysx 补 native `Gu::ConvexHullData` dump 后，进一步排除了
“只是 Python 重建脚本错了”的可能：

```text
local native pyphysx runtime hull:
  nbHullVertices = 128
  nbPolygons = 66
  nbEdges = 192
  runtime buffer bytes = 4776
  sha16 = fe22499e9fa9f563

extra local segment:
  verticesByEdges16 = 768 bytes

Unity runtime bytes = 4008
local native bytes = 4776
byteEqual = false
byteDiffCount = 2984
```

也就是说，本地 PhysX 真正进入 PCM 的 native hull buffer 就已经和 Unity 不一样；
本地还多了 `verticesByEdges16`/GRB edge layout，而 Unity WebGL 这份 runtime hull
没有这段。

同时，几何集合基本一致：

```text
nearest vertex max distance ~= 4.8429e-7 local hull units
side plane angle-set max error ~= 6.03e-5 deg after phase alignment
```

2026-07-09 又做了一个更窄的合龙实验，不再重采 endpoint，而是直接把 Unity 抓到的
4008 字节 runtime hull buffer 灌进本地 pyphysx shape：

```text
external pyphysx patch interface:
  Shape.patch_convex_mesh_runtime_hull_data_for_unity(...)
  Shape.patch_convex_mesh_big_convex_raw_data_for_unity(...)
  Shape.create_convex_mesh_from_points_with_scale(...)

probe:
  tools/reverse/probe_unity_runtime_hull_patch_contacts.py

report:
  data/calibration/unity_runtime_hull_patch_contact_ab_20260709.json
```

这次本地 shape 构造已经改成更接近 Unity 的状态：

```text
raw mesh input = stone_extendedcollider_mesh_256.json 的 512 顶点
PxMeshScale = (0.1127000079, 0.1150000021, 0.1127000079)
quantize_input = false
gpu_compatible = false
```

A/B 结果：

```text
Unity 真值:
  contact_count = 2
  separation = +0.009429097 / +0.009273720

local native 4776 bytes / GRB layout:
  contact_count = 4
  separation range = +0.008100420 .. +0.009458765

local patched Unity 4008 bytes / no-GRB layout, hull-only:
  patch ok = true
  contact_count = 0
```

这个结果很关键：它证明 `Gu::ConvexHullData` runtime hull buffer 所在层确实是分叉层，
但也证明“只灌 4008 字节 hull buffer”还不充分。原因是本地 shape 仍保留自己 cook 出来的
`BigConvexRawData` / support map / vertex valency arrays；这些数组和被替换后的 Unity
hull 拓扑不配套时，local `PxGenerateContacts` 甚至不再产生 contact。

2026-07-09 随后补了 runtime-hull 版 BigConvex 重建，不再等待下一次
Unity pointed-array capture：

```text
tool:
  tools/reverse/rebuild_bigconvex_from_runtime_hull.py

report:
  data/calibration/unity_runtime_bigconvex_rebuild_20260709.json

local self-check:
  samples diff = 0 / 3072 bytes
  valencies diff = 0 / 512 bytes
  adjacent_vertices diff = 0 / 384 bytes
```

这一步说明 `BigConvexRawData.mSamples / mValencies / mAdjacentVerts`
不再是黑盒：从 runtime hull 的 polygons、facesByEdges8、vertexData8 可以按 PhysX
`BigConvexDataBuilder` 路径重建，并且在本地 native hull 上字节级对上 pyphysx dump。

把 Unity 4008-byte hull 和这三段重建数组一起喂回本地 A/B 后：

```text
report:
  data/calibration/unity_runtime_hull_plus_rebuilt_bigconvex_contact_ab_20260709.json
  data/calibration/unity_runtime_hull_plus_rebuilt_bigconvex_pcm_pose_contact_ab_20260709.json

Unity 真值:
  contact_count = 2
  separation = +0.009429097 / +0.009273720

local native 4776/GRB:
  contact_count = 4

Unity 4008/no-GRB hull-only:
  contact_count = 0

Unity 4008/no-GRB + rebuilt BigConvex:
  contact_count = 4
  separation range = +0.008100420 .. +0.009444088

同样切到 PCM-after transform pose:
  contact_count = 4
```

这组结果当时把问题收窄到 `PxcPCMContactConvexConvex` contact generation 层；
但 2026-07-09 晚上的 direct scene-style PCM 审计进一步证明，`4/0 contacts`
主要是本地 immediate wrapper 调用边界不等价。保留旧 A/B 的意义是：
它证明静态 `Gu::ConvexHullData + BigConvexRawData` 必须和 cache 语义一起看，
不能只替换某一段 buffer。

```text
Unity raw PCM-after cache + Unity native transform:
  audit_seeded_pcm_refresh:
    refreshContactPoints 2 -> 2
    invalidate_BoxConvex = false

direct scene-style g_PCMContactMethodTable:
  contact_count = 2
  separation 与 Unity 只差约 7e-8m

direct PCM -> ContactBuffer + PxSolverBodyData:
  raw-vs-direct normal-row max delta ~= 5.86e-5

immediate PxGenerateContacts:
  local/BigConvex = 3 contacts
  hull-only = 0 contacts
```

因此当前最早可证明的分叉点不是 solver，也不是材质、半径或质量；
旧的 `PxGenerateContacts` 分叉也已降级为 probe artifact。contact prep row 桥接也已闭合。
现在要做的是把 direct scene-style PCM 的 2-contact ContactBuffer 和 Unity cache/warm-start
语义接回完整碰撞 replay，继续验证 0.02s 速度和 endpoint。

## 为什么不是继续调参数

已弱化的方向：

```text
friction / restitution / combine mode
fixed timestep
contactOffset / restOffset / frictionOffsetThreshold
solver iterations / scene flags
lock-upright constraints
formal mesh 输入点云
离线 cooked hull topology / BigConvexData
统一 handoff-x/y 偏移
统一 handoff_w_offset
宽范围 yaw / integrated active yaw
target/active support pre-settle
```

这些方向有些会改善单样本，但不能作为一套全局参数把 active 和 target 都压进 2cm。

## 最强证据

1. 尾段滑行不是主因：从本地 `0.02s/0.20s` snapshot 只调 target 水平 `vx/vy`，endpoint 可到毫米级。
2. 缺口在首次碰撞输出：需要约 `0.49 Ns` row 级修正，约本地主冲量 `2.35%`。
3. `12003` 本地 contact report 冲量角度约 `-87.19deg`，Unity-implied 约 `-82.21deg`，差 `+4.98deg`，接近 64 边 hull 一个侧面步长。
4. `12005` 用 `handoff_w_offset=-0.44rad/s` 可闭合，但全局 w offset 失败，说明它是 contact-instance tangent/angular 代理。
5. visible-feature leave-one-out correction 失败，说明 oracle 不是简单经验公式。
6. `13000` with-writeback 同 shot 桥接样本中，normal 方向已经匹配；旧本地 pyphysx
   immediate raw contact 的 4-contact 分叉已经被 direct PCM 审计解释为 wrapper artifact。
7. `20260709_171257` runtime hull capture 证明 Unity 和本地 rebuilt 的几何集合几乎一致，
   但 runtime feature buffer 不 byte-level 等价；这解释了为什么“公式都对”仍会出现 manifold 分叉。
8. 本地 native `Gu::ConvexHullData` dump 证明差异不是 Python 重建误差：本地 native 是
   4776 bytes，Unity runtime 是 4008 bytes，本地多出 768 bytes 的 `verticesByEdges16`。
9. direct PCM solver-row bridge 证明：本地 direct PCM 两个 contact 进入同一
   `PxSolverBodyData` 后，normal row 与 Unity raw row 只差 `5.86e-5`；剩余不是 row 公式。
10. 同源 17:12 完整 Scene replay 证明：即使四元数顺序修正，本地从头跑仍在 first contact
    生成 4 点/负 separation，target endpoint 仍约 10.09cm；剩余是 Scene 状态集成。

## 怎么改成一样

短期要做 trace-driven replay，并把本地 replay 切到 Unity scene 等价路径：

```text
1. native dump 已完成；首个 cached stone-stone manifold 的 direct PCM contact 和 normal row 已对齐。
2. 所有 pyphysx pose 数组统一按 `[w,x,y,z]` 传四元数。
3. 本地碰撞 replay 不再把 immediate `PxGenerateContacts` 当等价入口；
   改用 direct scene-style `g_PCMContactMethodTable` wrapper 和 Unity raw PCM cache。
4. 接回完整 replay 后，先比较 0.02s 碰后 linear/angular velocity。
5. 若速度一致，再看 endpoint；若速度分叉，优先比完整 Scene 的 PxSolverBody 初值、
   PCM cache 生命周期、warm-start force buffer、friction patch anchors 和 writeback。
```

只有 trace-driven replay 对齐后，才能继续把 dump 字段替换成公式。

当前已经补上第一步的 WebGL runtime hook，入口在：

```text
tools/reverse/unity_webgl_runtime_probe.js
```

推荐用启动脚本自动安装 hook：

```powershell
python tools\calibration\launch_unity_probe_browser.py --physx-native-hooks
```

手动浏览器 console 也可以调用：

```javascript
__curlingProbe.installPhysXNativeHooks({
  maxDumpsPerHook: 16,
  armMs: 2000,
  includeRawBytes: true,
  argWindowBytes: 8192
})
```

它不是 endpoint 采样工具，而是 native state 抓取工具。默认策略是：

```text
1. 先 hook stone-stone PCM: PxcPCMContactConvexConvex。
2. 一旦这个函数触发，自动 armed 约 2 秒。
3. 对 PxcPCMContactConvexConvex / PxcPCMContactConvexMesh 保存 exact PCM 输入：
   shape0/shape1 GeometryUnion、transform0/1、NarrowPhaseParams、Cache、ContactBuffer。
4. 在 armed 窗口内继续 dump contact finalization / solver-row writer 的参数指针窗口。
5. 导出 physx.native.before / physx.native.after 事件。
```

2026-07-09 追加的 PCM 入口 dump 不是重新抓 endpoint，也不是重做离线 cooked hull；
它直接对准 `pcmContactConvexConvex(shape0, shape1, transform0, transform1, params, cache, contactBuffer, ...)`
这一层。这里的 `cache` 是 `Gu::Cache / PxCache`，能看到：

```text
mCachedData
mCachedSize
mPairData
mManifoldFlags
PersistentContactManifold candidate:
  mNumContacts
  mCapacity
  mNumWarmStartPoints
  mAIndice / mBIndice
  mContactPoints pointer
```

因此下一次 runtime 抓取后，判断标准不是“终点像不像”，而是：

```text
data/calibration/unity_physx_native_solver_state_withwriteback_20260709.json
captureReadiness.readyForContactGenerationDiff == true

重点字段：
  pcmContactRows[].pcmInputs.shape0/shape1.decoded
  pcmContactRows[].pcmInputs.transform0/transform1
  pcmContactRows[].pcmInputs.narrowPhaseParams
  pcmContactRows[].pcmInputs.cache.decoded
  pcmContactRows[].pcmInputs.contactBuffer.candidate
```

旧的 `log/unity_runtime_probe_20260709_145532/events.jsonl` 重解码后显示：

```text
PxcPCMContactConvexConvex before/after = 6 / 6
readyForFieldDiff = true
readyForContactGenerationDiff = false
```

这说明旧 capture 已足够证明 solver/writeback，但还没有记录 PCM 入口的 exact
shape/cache/manifold 字段；这正是下一次运行要补的最小缺口。

解码：

```powershell
python tools\calibration\decode_runtime_probe_events.py log\unity_runtime_probe_...\events.latest.json
```

`*.summary.json` 里重点看：

```text
physx_native_counts
physx_contact_candidates
physx_contact_candidate_examples
```

`physx_contact_candidate_examples` 会列出候选 `ContactBuffer` 的首个 contact，
包括 normal、point、separation、friction、restitution。第一轮对齐就从这些字段和本地
pyphysx 同一帧的 contact report 开始比。

2026-07-09 已完成一次无限局运行时抓取。原始事件：

```text
log/unity_runtime_probe_20260709_113402/events.collision_pause_snapshot.json
```

压缩报告：

```text
data/calibration/unity_physx_native_contactbuffers_20260709.json
tools/reverse/extract_physx_native_contactbuffers.py
```

solver-state 审计报告：

```text
data/calibration/unity_physx_native_solver_state_20260709.json
tools/reverse/extract_physx_native_solver_state.py
```

这次抓到：

```text
PxcPCMContactConvexConvex calls = 4067
PxcPCMContactConvexMesh calls   = 83223
createFinalizeSolverContacts   = 80899
native before/after dumps      = 96 / 96

plausible ContactBuffer candidates = 84
stone-stone finalizer candidates   = 8
stone-stone narrowphase candidates = 15
stone-rink finalizer candidates    = 11
stone-rink narrowphase candidates  = 16
```

首个干净的 stone-stone finalizer ContactBuffer：

```text
normal      = (-0.9977886081, ~0, 0.0664669424)
point       = (-69.3740921, 14.5347843, 54.1385155)
separation  = 0.0160543937 m
friction    = 0.3600000143 / 0.3600000143
restitution = 1
```

同一帧的 `PxSolverContactDesc / FrictionPatch / PxSolverConstraintDesc` 也已经能从旧快照里恢复到指针和尺寸级：

```text
PxSolverContactDesc.invMassScales = 1 / 1 / 1 / 1
body0/body1 = 124621376 / 124621344
data0/data1 = 36211024 / 36210912
contactsPtr = 313859104
frictionPtr = 313720656
frictionCount = 1

Dy::FrictionPatch:
  broken = 0
  materialFlags = 0
  anchorCount = 1
  restitution = 1
  staticFriction / dynamicFriction = 0.3600000143 / 0.3600000143

PxSolverConstraintDesc[0]:
  linkIndexA/B = 65535 / 65535
  bodyADataIndex/bodyBDataIndex = 3 / 2
  constraintPtr = 313873504
  constraintLengthOver16 = 16
  expectedConstraintBytes = 256
```

`256 bytes` 正好对应 `64-byte SolverContactHeader + 48-byte SolverContactPoint +
16-byte applied force buffer + 2 * 64-byte SolverContactFriction`。因此
stone-stone 这一帧已经不是“摩擦有没有生成”的未知：`anchorCount=1`，理论上就是两条切向 friction row。

同一报告还把 `bodyFrame0/1` 和 `PxSolverBodyData` preview 解出来了：

```text
bodyFrame0.p = (-69.5303192, 14.4197845, 54.1532516)
bodyFrame1.p = (-69.2337952, 14.4197845, 54.1257439)

data0.linearVelocity = (0.2265774, -0.0981000, -0.0075694)
data1.linearVelocity = (~0, -0.0981000, ~0)
invMass0/1 = 0.0523560196
```

用这些字段按 `DyContactPrepShared::constructContactConstraint` 反算首个 normal row：

```text
relativeNormalVelocity ~= -0.22394605
velMultiplier ~= 9.53539771
penetration/separation = 0.01605439
bounce = false
biasedErr ~= -10.11138766
```

这意味着旧快照中前几条 stone-stone finalizer 仍是 contact-distance 内的预接触帧，
不是主 normal impulse 已经生效的碰撞帧。8 条 stone-stone finalizer 里 `biasedErr`
都为负，不能拿来验证真正冲量差。当时的下一步是延长 capture 或直接抓
raw solver row / force buffer；这个目标后来由 streamed event-sink 采样补上。

但这次旧快照的限制也很明确：当时只展开了一层 nested pointer，`desc->constraint`
没有被二级 dereference，所以 `SolverContactHeader/Point/Friction` 的 raw bytes 还不在
`events.collision_pause_snapshot.json` 里。`tools/reverse/unity_webgl_runtime_probe.js`
随后已经更新，后续 streamed 采样在 `extraDumps` 里直接保存了
`desc->constraint` raw bytes。

`tools/reverse/extract_physx_native_solver_state.py` 也已经同步更新：若 `extraDumps`
包含 `constraintWindow`，报告会解码真实 `SolverContactHeader / SolverContactPoint /
SolverContactFriction`，并生成 `rawVsComputedNormalRow`。这个字段曾是查误差源的
分水岭：

```text
rawVsComputedNormalRow 近 0:
  ContactBuffer/bodyData -> solver row 这一步一致，继续查 solver iteration / batch path。

rawVsComputedNormalRow 明显非 0:
  Unity 喂给 solver 的 bodyFrame/bodyData/contact/friction patch 与本地 replay 仍有字段差，
  回到 cooked hull 姿态、contact cache、shape pose 或 handoff state。
```

2026-07-09 13:25 的 streamed event-sink 版本已经完成这一步，并把分水岭推过了
finalizer row 公式：

```text
raw events:
  log/unity_runtime_probe_20260709_132549/events.jsonl

sampler endpoint:
  data/calibration/unity_native_solver_collision_probe_20260709_streamed_convexconvex_arm.jsonl

solver-state report:
  data/calibration/unity_physx_native_solver_state_convexconvex_arm_20260709.json
```

这次 `PxcPCMContactConvexConvex` 只负责 arm，`PxcPCMContactConvexMesh` 只在 armed
窗口内观察，避免冰面支撑接触抢光 solver dump 额度。结果：

```text
source events = 799
createFinalizeSolverContacts rows = 188
stone_stone rows = 4
constraintCapture.raw_available = 188

first stone-stone after row:
  ContactBuffer.numContacts = 2
  FrictionPatch.anchorCount = 1
  SolverContactHeader.numNormalConstr = 2
  SolverContactHeader.numFrictionConstr = 2
  static/dynamic friction = 0.3600000143
  restitution = 1

raw row vs computed row:
  header normal delta = (0, 0, 0)
  max abs normal-row delta ~= 4.45e-7
```

这说明 `ContactBuffer + PxSolverBodyData -> SolverContactHeader/Point/Friction`
这一步已经基本闭合。下一步不是继续猜 row 参数，而是抓 solver consume/writeback
前后的 `PxSolverConstraintDesc.bodyA/bodyB` 可变速度窗口。

这条证据把材质 combine 和 friction patch 是否存在都从未知项里拿掉了。剩余要比的是：

```text
1. 本地 pyphysx 在同类碰撞帧生成的 normal / point / separation 是否一致。
2. Unity 的 `createFinalizeSolverContacts` 输入 bodyFrame / bodyData / ContactBuffer 是否和本地 pyphysx 一致。
3. Unity 真正冲量帧的 256/304 字节 constraint block 里的 normal/friction row 是否和本地 pyphysx 一致。
4. 若 row 一致，再查 solver 迭代或 batch/库版本差异；若 row 不一致，回到 bodyData、shape pose、
   friction anchors 和 contact point 生成。
```

当前 hook 的关键 table 入口：

```text
120118 func70576 PxcPCMContactConvexConvex
120587 func71272 PxsDynamics.createFinalizeContacts
120379 func70963 createFinalizeSolverContacts4
120487 func71103 createFinalizeSolverContacts
120346 func71040 solveContactBlock
120348 func71043 solveContact_BStaticBlock
120349 func70916 solveContact4Block
120350 func70918 solveContact4StaticBlock
120352 func71042 solveContactBlockWithWriteback
120354 func71045 solveContact_BStaticBlockWithWriteback
120355 func70922 solveContact4BlockWithWriteback
120356 func70923 solveContact4StaticBlockWithWriteback
120358 func71041 solveContactConcludeBlock
120360 func71044 solveContact_BStaticConcludeBlock
120361 func70920 solveContact4ConcludeBlock
120362 func70921 solveContact4StaticConcludeBlock
```

这些事件先解决“Unity 到底给 PhysX 喂了什么”和“solver row 实际写出了什么”。
如果抓到的 ContactBuffer / solver rows 和本地 pyphysx 输入一致但输出仍不一致，才继续查
PhysX 库版本 / batch path / compiler fast-math 差异；如果输入已经不一致，就回到 shape pose、
contact cache、friction patch 或 handoff state。

2026-07-09 已经把 single-pair finalizer row 这一层基本闭合：

```text
data/calibration/unity_physx_native_solver_state_convexconvex_arm_20260709.json

stone-stone rowCount = 4
raw SolverContactHeader/Point/Friction 可用
Unity raw row vs 本地按 ContactBuffer + PxSolverBodyData 重构 row:
  normal-row 最大差约 4.45e-7
```

同日继续抓 `solveContactConcludeBlock` 前后：

```text
data/calibration/unity_physx_native_solver_state_solvecontact_20260709.json
data/calibration/unity_physx_solvecontact_writeback_summary_20260709.json

solveContactConcludeBlock paired before/after = 5
changed pairs = 1
最大 body preview delta ~= 0.008657
call 3 before 时 bodyA/bodyB 已经约为 -0.784 / +0.779 m/s
```

同一份 capture 继续用 `tools/reverse/replay_solver_consume_delta.py` 做了离线重放：

```text
data/calibration/unity_physx_solvecontact_replay_delta_20260709.json

solveContactConcludeBlock:
  replayed pairs = 5
  max bodyA/bodyB error ~= 5.96e-8

solveContact_BStaticConcludeBlock:
  replayed pairs = 105
  max bodyA error ~= 7.45e-9
```

因此 single-pair solver consume / writeback 公式已经闭合。当前不能把 conclude wrapper
当作“完整首次碰撞前后”，但原因不是公式没挖出来，而是主冲量已经在进入某些 conclude
call 前发生。下一步等价性证明要比较更早父 wrapper 前的 `PxSolverBody` / row / bodyData，
找到本地 pyphysx 生成的 pre-solve native state 和 Unity 的差异。

2026-07-09 14:55 的补采已经抓到父级 with-writeback 边界：

```text
log/unity_runtime_probe_20260709_145532/events.jsonl
data/calibration/unity_physx_native_solver_state_withwriteback_20260709.json
data/calibration/unity_physx_solver_consume_writeback_summary_20260709.json
data/calibration/unity_physx_solver_consume_replay_delta_withwriteback_20260709.json

captureReadiness.readyForFieldDiff = true
withWritebackPairCount = 108

solveContactBlockWithWriteback:
  before = 5
  after = 5
  changed pairs = 2
  main writeBack impulse ~= 12.271674
  replay max error ~= 5.96e-8

solveContact_BStaticBlockWithWriteback:
  before = 49
  after = 49
  changed pairs = 49
  replay max error ~= 7.45e-9
```

这证明主 solve + body writeback 边界已经抓到，且 Unity raw row 离线重放能贴住
after body window。剩余等价性问题收窄为：Unity 进入 solver 前的 native state
和本地 pyphysx 构造的 native state 是否逐字段相同，尤其是 ContactBuffer、FrictionPatch、
PxSolverBody 初值、first collision frame 和 contact cache/anchor。

2026-07-09 的干净 runtime 试跑补充了一条重要证据：

```text
controlled sampler:
  RESETPOSITION target index 8 -> (2.375, 5.2)
  BESTSHOT 3.4 0 0
  Unity final active = (2.3408, 5.4852)
  Unity final target = (2.4856, 3.8950)
  collision_observed = true

hook summary before arm-strategy fix:
  CurlingStoneNew.OnCollisionEnter = 1
  PxcPCMContactConvexConvex = 0
  PxcPCMContactConvexMesh = 42
  createFinalizeSolverContacts = 42
```

这说明“只看 `PxcPCMContactConvexConvex` 调用数就能判断石壶碰撞发生”这个假设不稳定。
后续试跑又证明，让 `PxcPCMContactConvexMesh` 触发 arm 会被 stone-rink 支撑接触刷爆日志。
当前策略是：`PxcPCMContactConvexConvex` 负责 arm，`PxcPCMContactConvexMesh` 和
finalizer/solver row 只在 armed 窗口内 dump；stone-stone 归类由 `ContactBuffer`
材质、法线、`FrictionPatch` 和 body state 决定。

### 2026-07-11：`SetActive` 不是单一 shape flag，且不能以 remove/add 代替

前文的 `func61068/func61078` 已确认 Unity 在 GameObject 层按 `SetActive(true/false)` 管理既有 stone；
这一事实不足以直接推出 native PhysX actor 的精确状态。为避免把该层遗漏成“新问题”，对 14000 的
同一 persistent Scene 做了受控 A/B：基线只关闭 `SIMULATION_SHAPE`；反事实则对 inactive stone
执行 `removeActor`，出手时对同一 actor 执行 `addActor`。其余 pose、quaternion、hull、BigConvex、
material、fixed tick 与 Unity task-local PCM cache hook 均不变。

```text
shape-flag 基线：      body order target -> active，2 contacts，contact x 约 -69.726m
remove/add 反事实：    body order active -> target，4 contacts，底部 contact x 约 -69.718m
Unity runtime：        2 contacts，contact x 约 -69.717m
```

所以 body/shape registration order 是切向 contact point 的真实敏感字段，不是摩擦参数；但单独复刻
actor 成员资格会改变 full-manifold reduction 为四点，仍不等价于 Unity。当前未导出的 native 状态被
精确限定为 `ShapeInteraction` / contact-manager 的创建或复用顺序，以及其关联 PCM cache 的
pointer、flags、feature bytes。下一步必须从同一 runtime call 抓这些字段，不再用 endpoint、摩擦
或 actor add/remove 行为猜测。详细执行与数值见 14 号计划文档的 2026-07-11 `SetActive` A/B 小节。

同日的既有日志重解码已经把其中一部分“未导出字段”闭合。14000 Unity 的
`PxsContactManager::mNpUnit` 为 `flags=611, statusFlags=2, edgeIndex=2, index=1,
transformCache=(12,9), npIndex=8, frictionPatchCount=0`；关闭本地 contact-modify callback 后，
本地 `flags/statusFlags/edgeIndex` 也为 `611/2/2`，但仍是 `index=2, transformCache=(9,1),
npIndex=16, frictionPatchCount=1`。产物为
`data/calibration/p5_14000_workunit_state_audit_20260711.json`。

这里最重要的纠正是：本地旧 `flags=737` 中的 `eMODIFIABLE_CONTACT` 并非 Unity 状态，完全由
本地 callback/filter shader 引入；它已在 binding 中改成“callback 关闭则不写 pair flag”。这消除了
一个已证明的本地污染源，但尚未消除 ContactBuffer 的切向偏移。剩余需比较的是 cache slot 所指
transform 内容与 pair 注册/刷新顺序，而不是把这些 index 数值当作可拟合参数。

紧接着的入口复验已经证明：slot 编号不同不等于 transform 不同，两个 slot 被 PCM 实际读取的
position/quaternion 内容与 Unity 对应入口一致。把 local active 的剩余 `2.8418e-5rad` yaw 差精确
注入 active -> target 反事实后，contact count 仍是 4；该微小角状态不是 2-contact/4-contact 分叉。

还要保留一个防止回归的解码结论：不可把某个简化 probe 输出理解成
`Gu::Cache.cachedData == null`。已归档的六条 Unity first-contact raw cache 均有有效
`cachedDataPtr`，而 `func70576` 在函数入口就解引用 `cache[0]`。真正已对齐的 lifecycle 是
`numContacts=0`、`numWarmStartPoints=0`，同时保留 feature-index bytes；这一点已经在 P4 的 scalar
复验中逐字段验证。故 cache 指针空/非空不再是待追未知项。

现有证据只留下一个结构性边界：Unity `SetActive` 形成的 ShapeInteraction/contact-manager
创建或 refresh 顺序。本地仅关闭 shape 时得到 `target -> active` 的 2 contacts；remove/add actor
时得到 `active -> target` 的 4 contacts；Unity 则是 `active -> target` 的 2 contacts。后续只比较
pair registration/manager refresh 调用序，不能把 slot 编号、yaw 或摩擦作为自由参数调节。

材质时序也已完成独立复验：滑行时 active material 保持 `0`，仅在预测进入 PCM shell 的 tick 前恢复
到 `0.6`，同时关闭 local contact-modify callback，首 solver 的两条 ContactBuffer 都得到 Unity 原始值
`staticFriction=dynamicFriction=0.3600000143`，且 work-unit flags 为 `611`。这既消除了 callback
带来的 `eMODIFIABLE_CONTACT` 污染，又不改变 2-contact 数。该修复没有消除约 8.5mm 的切向 point
偏移，故 material/friction 已从未知项中退出；唯一待解决的是 pair lifecycle。

### 2026-07-11 更正：first-contact 不是 PCM cache reset 造成的

此前 local binding 为审计 Unity task 入口加入了一个可选 wrapper：每次 convex-convex call 前执行
`LargePersistentContactManifold::clearManifold()`，保留 feature bytes 而清零 contact/warm-start 数。
这不是 scalar PhysX 的默认行为，故不能凭它与 Unity 的某一帧 cache 视图相似就认定为机制等价。

在保持 `active -> target` role、壳层 `0.6 x 0.6` material 和关闭 modify callback 的前提下，六条
controlled shot 做了 task-cache reset 开/关 A/B；两边 first-contact count 都是：

```text
14000..14005 = 4, 2, 2, 4, 4, 4
```

所以 cache reset、warm-start 和 allocator feature residue 已从 **首帧** 的根因候选中排除。它们仍是
碰撞后多 tick 演进的审计项，但不能解释 Unity 2-contact 与 local 4-contact 的首次差异。现阶段没有
任何允许生产代码写入 Unity cache/feature bytes 的结论；同时也不能因此重新审计已经由 scalar
direct-PCM 闭合的几何/dispatch 字段。下一步只反查 `GameObject.SetActive` 到 native PhysX 的 actor、
shape 与 ShapeInteraction 启停链，找出为何本地 remove/add 虽复刻 `active -> target` RigidID 顺序，
仍未复刻 Unity 新建 pair 的 2-contact work-unit。

## 最少要抓的字段

```text
active / target:
  global pose
  rotation / yaw
  linearVelocity / angularVelocity
  mass / COM / inertia tensor
  constraints / sleep state / solver iteration counts

PxShape:
  local pose
  geometry scale
  contactOffset / restOffset
  material pointer / filter data
  convex mesh pointer

stone cooked stream:
  vertices / polygons / indices
  bounds
  mass / inertia / COM
  GAUS / VALE / SUPM byte order

rink:
  triangle mesh vertices / indices
  local pose / scale
  material

contact:
  work-unit body / shape order
  ShapeInteraction / contact-manager pointer and creation-or-refresh state
  persistent contact cache
  friction patches / anchors
  ContactBuffer normal / points / separation
  solver rows
  normal and friction applied impulses
```

## 机器报告

主报告：

```text
data/calibration/unity_physx_native_state_equivalence_audit_20260709.json
```

生成：

```powershell
D:\esp\tmp\curling_pyphysx_conda\python.exe tools\reverse\summarize_physx_native_state_equivalence.py
```

当前机器结论：

```text
strong_identity_proven = false
```

### 2026-07-11：高层 `SetActive` 顺序已与本地一致，剩余是组件 native side effect

`data/calibration/unity_setactive_pair_lifecycle_20260711.json` 从一次受控 14000 runtime capture 确认：
target 8 在 `RESETPOSITION` 后启用，active 0 在 `BESTSHOT` 后启用，随后 Unity 新建的 manager 直接生成
2-contact finalizer。该顺序已经等于本地 `target -> active`，故 RigidID/高层 actor insertion order 不再
解释持久 Scene 的 2/4 分叉。仍未证明的是 GameObject 启停期间 Collider/Rigidbody component callback 对
native `ShapeInteraction`、broadphase 或 contact-manager 的精确副作用；下一轮只抓这些 callback 的原生
对象和 table slot，不重开已闭合的 geometry、PCM、cache 或 solver 字段。

后续受控 capture 已把“table slot”进一步区分为两个方向：`MeshCollider` 的 type 20 / vtable 3221476
在 disable 时走 slot 24 `func73275`，而 enable 不走该 slot，而是由 `func79987 -> func79992/79993` 的
activation queue 用 `component[1]` 的 registry descriptor slot 3 dispatch。故完整 native identity 尚未证明，
但剩余字段已收敛为该 registry descriptor 的 handler pointer，而不是任意 PhysX 参数或接触几何。

### 2026-07-11 更正：negative-key MeshCollider 不经过 descriptor registry

运行时证据 `log/unity_runtime_probe_20260711_133844/events.jsonl` 显示，target/active MeshCollider 的
`component[1]` 分别是负 key `-124` 与 `-140`；同一时刻 `func80110` 的 resolver provider/table index globals
都是 `0`。其反编译分支在负 key 且 provider 为空时直接返回 `0`，没有 registry fallback。故上一段把
MeshCollider enable 归到 descriptor slot 3 的推论不成立，已由本段取代。

当前仅保留一个可证伪的对象级未知：negative-key MeshCollider 的专用 native activation bridge 如何改变
physics-side registration/state。后续静态反查以 `func73275 -> func73773` 的 disable event 及其对称 enable
call site 为起点；无需再采 Unity endpoint，也不能据此重开已排除的 hull、PCM、cache、摩擦或 solver 分叉。

### 2026-07-11：negative-key MeshCollider bridge 的实际 callback 已确定

静态调用链已从 `f_lced` 的 event mask 一直跟到 flush consumer `func73761/f_zbed`：它遍历 GameObject
component list，并以两个 activation bit 调 component vtable slot 44。MeshCollider vtable `3221476` 的
slot 44 是 `func73295/f_bkdd`，其 active 分支按严格顺序调用：

```text
MeshCollider slot44 f_bkdd
  -> slot43 func72952/f_wwcd: transform/shape refresh
  -> slot42 func72949/f_twcd: collider runtime refresh
  -> f_jjdd -> f_xidd: attached Rigidbody mass-properties sync dispatch
```

这修正了“未知 registry descriptor handler”的旧表述。剩余未知不再是 Wasm 的 activation 公式，而是
本地 pyphysx 在同一 persistent actor/shape identity 上能否重现该 lifecycle 之后的**原生状态结果**。
下一份审计必须比较 callback 后、first PCM 前的 actor/shape core、flags、sleep state、mass/COM/inertia
和 manager creation state；发现最早字段分叉后再修改本地 Scene。

Rigidbody vtable `3222248` 的数据段在 slot 43 后结束，没有 slot 44。因此 `f_zbed` 不会把完整
GameObject component array 都当作 activation callback 调用；它只遍历 participant 子表。不存在尚待反查的
Rigidbody 独立 slot44 路径，Rigidbody 的相关 mass sync 已包含在 MeshCollider callback 内。

### 2026-07-11：local post-activation pose 的必要性已 A/B 证伪

`PersistentPhysxFrontHalfScene` 在 `SIMULATION_SHAPE` 启用后重写一次 actor pose。去掉它的受控
six-shot replay 会让 14000 在 step `1` 对旧 broadphase pose 发生 `4` contacts，active 到真实
first-PCM entrance 的距离为 `26.98m`；保留时 14000 在 step `1560` 得到 `2` contacts。证据为
`persistent_scene_sequence_activation_bridge_baseline_20260711.json` 与
`persistent_scene_sequence_activation_bridge_no_postpose_20260711.json`。

此写入是对 Unity `f_wwcd` transform-refresh 语义的本地最小适配，不是额外的 Unity Transform setter，
也不是当前 persistent Scene 2/4 分叉的候选根因。后续状态审计必须在保留该适配的 baseline 上进行。

### 2026-07-11：activation 实测只命中 f_wwcd 分支，f_twcd 尚待直接观测

新的受控 14000 capture 对 table `122045/func73295` 的唯一 runtime call 参数为 `(component, 1, 0, 0)`。
`f_bkdd` 在该分支只调 vtable slot 43 `f_wwcd`，并不调 slot 42 `f_twcd`；其 component 192B 与
collider-backend 320B before/after raw window 均相同。这否定了“每次 SetActive 都必然直接执行
f_wwcd + f_twcd + mass sync”的强表述。

后续只需同时 hook slot43 的 table `122156` 与 slot42 的 table `122155`，确认它们在同一受控状态转换中
各自的真实调用时刻和参数；在此之前，不把 `f_twcd` 的静态可达性当作已发生的 runtime side effect。
