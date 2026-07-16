# 采样、记录文件与运行时探针

旧的重采样计划、记录文件路径、运行时注入探针长文档已合并到这里：

```text
docs/archive/unity_reverse_superseded_20260709/08_resampling_plan.zh.md
docs/archive/unity_reverse_superseded_20260709/09_record_file_storage.zh.md
docs/archive/unity_reverse_superseded_20260709/11_runtime_injection_probe.zh.md
```

## 当前结论

现在不需要继续普通 socket 采样。已有样本足够证明：

```text
1. 单壶 no-sweep 可做训练第一阶段。
2. 2026-07-09 17:12 已补到首次碰撞帧 PCM/native state。
   当前不是缺 endpoint 样本，而是本地 replay 的 cooked runtime feature bundle 不等价。
3. 普通四局或无限模式不会自动给出 AutoDCP `.save` / `RANDSEED`。
```

后续如果再打开 Unity，目标必须是抓运行时 native 字段，不是多收 endpoint。
运行一次碰撞只是为了触发 hook。

2026-07-09 的 hull-only patch A/B 已经证明：

```text
local 4776/GRB hull:
  contact_count = 4

patched Unity 4008/no-GRB hull-only:
  contact_count = 0

Unity 真值:
  contact_count = 2
```

2026-07-09 后续已经从 runtime hull 重建出 BigConvex 三段数组，并通过本地
native byte-level 自校验：

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

但 `Unity 4008/no-GRB + rebuilt BigConvex` 的 A/B 结果仍是本地 4 个 contact，
不是 Unity 的 2 个：

```text
report:
  data/calibration/unity_runtime_hull_plus_rebuilt_bigconvex_contact_ab_20260709.json
  data/calibration/unity_runtime_hull_plus_rebuilt_bigconvex_pcm_pose_contact_ab_20260709.json

Unity:
  contact_count = 2

local 4776/GRB:
  contact_count = 4

Unity 4008/no-GRB hull-only:
  contact_count = 0

Unity 4008/no-GRB + rebuilt BigConvex:
  contact_count = 4

同样切到 PCM-after transform pose:
  contact_count = 4
```

所以后续再采不是“再扔更多壶”，也不是单纯再抓 BigConvex arrays，而是一个更窄的
native dump / replay：

```text
PxCache / PersistentContactManifold raw state
feature anchors / aIndices / bIndices / warm-start point
PCM refresh/reduce 进入 ContactBuffer 前后的 contact manifold
```

`tools/reverse/unity_webgl_runtime_probe.js` 仍会在下一次 `PxcPCMContactConvexConvex`
事件里 dump BigConvex pointed arrays；但它现在是交叉验证字段，不再是最小阻塞项。
如果确实再开 Unity，采完后可直接跑：

```powershell
D:\esp\tmp\curling_pyphysx_conda\python.exe tools\reverse\probe_unity_runtime_hull_patch_contacts.py ^
  --events log\unity_runtime_probe_YYYYMMDD_HHMMSS\events.jsonl ^
  --output data\calibration\unity_runtime_hull_patch_contact_ab_YYYYMMDD_HHMMSS.json
```

脚本会自动检查 `bigConvexRawDataArrays` 是否存在：

```text
不存在：只能复现旧结论，hull-only 仍不闭合。
存在：自动追加 unity_4008_no_grb_plus_bigconvex case。
```

## `.save` 和 RANDSEED

Unity 代码里 AutoDCP 支持：

```text
BESTSHOT
RANDSEED
SWEEP
POSITION
SCORE
SETSTATE
TRACE
```

但是当前 WebGL build 没有打包可直接进入的 `AutoGame/FastGame` 主路径。普通 UI 的四局制和无限模式不会自然生成我们想要的 `.save` 文件。

WebGL 逻辑落盘位置通常在浏览器 IndexedDB / Emscripten FS 下，但当前包没有在普通模式暴露 AutoDCP record 入口，所以“找不到 `.save`”不是路径没扫全，而是模式没开。

## 运行时 probe 能抓什么

现有工具：

```text
tools/reverse/unity_webgl_runtime_probe.js
tools/calibration/launch_unity_probe_browser.py
tools/calibration/decode_runtime_probe_events.py
tools/reverse/export_cooked_hull_from_probe_events.py
```

已经能帮助抓：

```text
WebSocket 收发
console trajectory
Emscripten FS 行为
WASM memory/table 基础信息
部分 PhysX cooking hook 事件
PhysX native hook 事件：
  ContactBuffer 生成入口
  contact finalization task
  single-pair / 4-wide solver contact row 写出入口
```

当前等待页抓到的 cooked hull 已被尺寸判据排除为正式比赛石壶，不能直接接进训练。

## 当前主线：抓 native state

目标不是终点采样，而是抓 Unity 在碰撞帧喂给 PhysX 的中间态：

```text
ContactBuffer:
  normal / point / separation
  maxImpulse
  staticFriction / dynamicFriction / restitution
  targetVel
  internalFaceIndex1

friction cache / patch:
  old anchors
  correlation / grow patch 后的 anchors
  broken/writeback 状态

solver rows:
  SolverContactHeader
  SolverContactPoint
  SolverContactFriction
  4-wide batch row 的 normal / friction 写出缓冲
```

已经接入的 WebGL table hook：

```text
120118 func70576 PxcPCMContactConvexConvex        signature iiiiiiiii
120119 func70577 PxcPCMContactConvexMesh          signature iiiiiiiii
120204 func70739 PxsContext.contactManagerDiscreteUpdate signature vi
120587 func71272 PxsDynamics.createFinalizeContacts       signature vi
120379 func70963 createFinalizeSolverContacts4    signature iiiifffffi
120487 func71103 createFinalizeSolverContacts     signature iiiifffffii
120346 func71040 solveContactBlock                signature viii
120348 func71043 solveContact_BStaticBlock        signature viii
120349 func70916 solveContact4Block               signature viii
120350 func70918 solveContact4StaticBlock         signature viii
120352 func71042 solveContactBlockWithWriteback   signature viii
120354 func71045 solveContact_BStaticBlockWithWriteback signature viii
120355 func70922 solveContact4BlockWithWriteback  signature viii
120356 func70923 solveContact4StaticBlockWithWriteback signature viii
120358 func71041 solveContactConcludeBlock        signature viii
120360 func71044 solveContact_BStaticConcludeBlock signature viii
120361 func70920 solveContact4ConcludeBlock       signature viii
120362 func70921 solveContact4StaticConcludeBlock signature viii
```

`PxcPCMContactConvexConvex` 被调用时，probe 会自动把 native capture 武装一小段时间，
随后只抓这段时间内的 finalizer / solver row / solver consume 入口，避免日志先被冰面
支撑接触填满。`PxcPCMContactConvexMesh` 不再触发 arm，只在 armed 窗口内观察。

推荐启动方式：

```powershell
python tools\calibration\launch_unity_probe_browser.py --physx-native-hooks --stream-events --stream-no-store --no-poll-events --physx-native-max-dumps 128 --physx-native-arm-ms 5000 --physx-native-window-bytes 2048
```

这会预注入 probe，并在 WebAssembly table 捕获后自动执行：

```javascript
__curlingProbe.scanAndHookFS()
__curlingProbe.installPhysXNativeHooks({
  maxDumpsPerHook: 16,
  armMs: 2000,
  includeRawBytes: true,
  includeNestedRawBytes: false,
  argWindowBytes: 8192,
  solverConstraintBytes: 4096,
  solverDescRecords: 4,
  solverBodyBytes: 256
})
```

如果不是用启动脚本，而是手动把 probe 粘到浏览器 console，也可以直接运行上面的
JavaScript。

然后只需要在页面里触发一次明确的石壶-石壶碰撞。启动脚本会持续保存：

```text
log/unity_runtime_probe_YYYYMMDD_HHMMSS/events.latest.json
log/unity_runtime_probe_YYYYMMDD_HHMMSS/events.final.json
```

手动 console 场景下，结束后导出：

```javascript
__curlingProbe.downloadEvents("physx_native_state_events.json")
```

本地解码：

```powershell
python tools\calibration\decode_runtime_probe_events.py path\to\physx_native_state_events.json
```

重点看 summary 里的：

```text
physx_native_counts
physx_contact_candidates
physx_contact_candidate_examples
```

原始 JSON 里的关键事件：

```text
physx.native.capture_armed
physx.native.before
physx.native.after
```

每个 `physx.native.before/after` 都会保存参数指针窗口、前若干 `u32/f32` 预览、完整 raw bytes
以及参数结构里的嵌套指针预览。若某个窗口正好是 `Gu::ContactBuffer`，会按已知布局直接给出
`contactBufferCandidate`。

2026-07-09 后，`createFinalizeSolverContacts` 还会额外保存 `extraDumps`：

```text
PxSolverContactDesc:
  descPtr / contactsPtr / frictionPtr / contactForcesPtr
  numContacts / frictionCount / body/data 指针

PxSolverConstraintDesc:
  bodyA/bodyB
  linkIndexA/B
  constraintPtr
  constraintLengthOver16
  writeBackPtr

constraintWindow:
  直接从 desc->constraint dump SolverContactHeader/Point/Friction raw bytes

frictionWindow:
  直接从 frictionPtr dump Dy::FrictionPatch raw bytes

contactBufferWindow / data0Window / data1Window:
  直接 dump Gu::ContactBuffer 和两端 PxSolverBodyData raw bytes

solveContact* consume hooks:
  直接 dump PxSolverConstraintDesc.constraint
  同时 dump bodyA/bodyB 的 raw bytes，用来比较 solver 前后速度写回
```

`solveContact*` 这里包含三类 wrapper：普通 block、conclude block、with-writeback block。
`func71035/71036/70917/70919` 本体不是 table-exported，不能用 table hook 直接包住；
但它们的父 wrapper 已经由 `tools/reverse/trace_wasm_callers_from_wat.py` 从
`build.wat + wasm_table_map.json` 反查确认。

`tools/reverse/extract_physx_native_solver_state.py` 会优先读取这些精确二级
dump，而不是只靠旧的 pointer scan。若 `constraintWindow.rawBytes` 存在，报告会直接解出：

```text
SolverContactHeader
SolverContactPoint.normalRows[]
appliedNormalForces[]
SolverContactFriction.frictionRows[]
writeBack f32[]
rawVsComputedNormalRow
```

报告顶部还有 `captureReadiness`，以后判断一次 Unity 运行是否“抓够了”只看这个 gate：

```text
readyForFieldDiff = true
```

它要求同一次 capture 同时具备：

```text
stone-stone createFinalizeSolverContacts.after:
  contactBufferWindow
  frictionWindow
  data0Window / data1Window
  raw SolverContactHeader/Point/Friction

solveContact*WithWriteback:
  before / after rows
  bodyAWindow / bodyBWindow
  raw solver rows / writeBackWindow
```

旧的两份 2026-07-09 capture 现在已经明确：

```text
unity_physx_native_solver_state_convexconvex_arm_20260709.json:
  finalizer 字段齐
  withWritebackPairCount = 0
  readyForFieldDiff = false

unity_physx_native_solver_state_solvecontact_20260709.json:
  finalizer 字段齐
  只抓到 conclude，不是 with-writeback
  withWritebackPairCount = 0
  readyForFieldDiff = false
```

2026-07-09 14:55 的 Unity runtime probe 已补上这一块：

```text
data/calibration/unity_physx_native_solver_state_withwriteback_20260709.json

withWritebackPairCount = 108
readyForFieldDiff = true

solveContactBlockWithWriteback:
  before = 5
  after = 5
  withConstraintRaw = 10
  withBodyWindows = 10
  withWriteBackWindow = 10

solveContact_BStaticBlockWithWriteback:
  before = 49
  after = 49
  withConstraintRaw = 98
  withBodyWindows = 98
  withWriteBackWindow = 98
```

其中 `rawVsComputedNormalRow` 是 Unity raw solver row 减去我们按 PhysX 源码从
`ContactBuffer + PxSolverBodyData` 反算出的 row。2026-07-09 的 stream 版本已经让
`constraintCapture.raw_available = 188`，stone-stone after row 的最大差约 `4.45e-7`。
后续成功标准改为：把这次 Unity pre-solve native state 和本地 pyphysx 同 shot 的
pre-solve native state 做逐字段差异表，而不是再采 endpoint。

2026-07-09 的 `solveContactConcludeBlock` 试抓结果：

```text
data/calibration/unity_physx_native_solver_state_solvecontact_20260709.json
data/calibration/unity_physx_solvecontact_writeback_summary_20260709.json

solveContactConcludeBlock paired before/after = 5
changed pairs = 1
最大 bodyA/bodyB preview delta ~= 0.008657
writeBack preview 没变
```

这说明 conclude wrapper 不是完整主冲量写回边界；下一轮应优先用新增的
`solveContactBlockWithWriteback` / `solveContact_BStaticBlockWithWriteback`
和 4-wide with-writeback hooks。

14:55 这轮已经抓到了完整 with-writeback 边界：

```text
data/calibration/unity_physx_solver_consume_writeback_summary_20260709.json
data/calibration/unity_physx_solver_consume_replay_delta_withwriteback_20260709.json

pairedCount = 378

solveContactBlockWithWriteback:
  pairs = 5
  changed pairs = 2
  main writeBack impulse ~= 12.271674
  replay max error ~= 5.96e-8

solveContact_BStaticBlockWithWriteback:
  pairs = 49
  changed pairs = 49
  replay max error ~= 7.45e-9
```

普通 `solveContactBlock` 单独重放会有 0.08 量级 body-window 误差；这不是主公式失败，
而是它不是完整写回边界。判断 solver 闭合要看 `*WithWriteback` 和 conclude wrapper。

这里的目标已经不是继续验证 solver 公式。`ContactBuffer + PxSolverBodyData -> solver row`
和 single-pair consume/writeback 已经闭合。with-writeback hooks 现在的用途是抓主冲量发生前的
完整入口状态，然后和本地 pyphysx 逐字段比：

```text
PxSolverBody / PxSolverBodyData 初值
ContactBuffer normal / point / separation
FrictionPatch cache / anchors
solver rows / applied force buffer
body writeback 前后速度
first collision frame timing
```

2026-07-09 的同 shot `13000` 最新 with-writeback 审计已经证明分叉在上游，
但不是旧报告里写的 normal 方向分叉。后续本地 pyphysx 已补
`pyphysx.generate_contacts_between(...)` immediate-mode 探针，可以在本地同一套
actor/shape/pose 上直接吐 raw contact generation 结果。最新结论是 normal 方向匹配，
首个可见分叉在 contact count / separation / manifold reduction：

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

针对性验证 `formal-recovered` collider mesh 也没有消除这个分叉：

```text
data/calibration/unity_physx_collision_probe_native13000_immediate_formal_contact_20260709.json

formal mesh target endpoint error ~= 17.53cm
formal mesh immediate contact_count = 4
formal mesh target-side normal angle ~= -5.62deg
```

所以现在不是继续采 endpoint，也不是再调 solver 参数；下一步是把 Unity finalizer 的
pose/bodyFrame 转成本地坐标后回灌给 immediate contact generator，或继续挖 Unity
PCM/contact cache/cooked hull 的运行时状态。

这个 bodyFrame 回灌实验已经补上：

```text
tools/reverse/probe_unity_finalizer_pose_contacts.py
data/calibration/unity_finalizer_pose_contact_replay_20260709.json

Unity finalizer:
  contact_count = 2
  separations ~= +0.00859m / +0.00838m
  target-side normal angle ~= -2.812503deg

local PxGenerateContacts using Unity finalizer relative bodyFrame:
  ring zero-yaw = 4 contacts
  ring Unity-yaw cases = 3 contacts
  formal zero-yaw = 4 contacts
  formal Unity-yaw cases = 3 contacts
```

因此后续 runtime probe 的最小目标不是再拿 endpoint，也不是再试 yaw，而是抓
`shapeInteraction` 背后的运行时 shape/collider/cache 字段：

```text
PxShape localPose
PxConvexMeshGeometry / convexMesh pointer / scale
PCM manifold/contact cache anchors
internalFaceIndex -> hull polygon mapping
```

2026-07-09 已把这个目标落进 WebGL probe 的 exact PCM 入口 dump：

```text
tools/reverse/unity_webgl_runtime_probe.js

PxcPCMContactConvexConvex / PxcPCMContactConvexMesh extraDumps:
  shape0 / shape1 GeometryUnion
  transform0 / transform1 PxTransform
  Gu::NarrowPhaseParams
  Gu::Cache / PxCache
  cache.cachedData PersistentContactManifold candidate
  Gu::ContactBuffer before/after
```

对应解析器：

```powershell
D:\esp\tmp\curling_pyphysx_conda\python.exe tools\reverse\extract_physx_native_solver_state.py ^
  log\unity_runtime_probe_YYYYMMDD_HHMMSS\events.jsonl ^
  --output data\calibration\unity_physx_native_solver_state_withwriteback_20260709.json
```

报告里新增的判断字段：

```text
captureReadiness.readyForContactGenerationDiff
pcmContactCounts
pcmContactRows[].pcmInputs.cache.decoded
pcmContactRows[].pcmInputs.contactBuffer.candidate
```

旧的 14:55 with-writeback capture 重解码结果是：

```text
readyForFieldDiff = true
readyForContactGenerationDiff = false
```

这说明旧数据已经足够做 solver/writeback 字段级审计，但还不能回答
`PxGenerateContacts fresh cache` 和 Unity `PCM cached manifold` 是否一致。
下一次运行只需要补这块，不需要再做 endpoint 盲采。

2026-07-09 17:12 已经补上这块，不再需要继续普通重采样：

```text
raw events:
  log/unity_runtime_probe_20260709_171257/events.jsonl

controlled endpoint trigger:
  data/calibration/unity_native_pcm_hull_runtime_probe_20260709_171257.jsonl

native state report:
  data/calibration/unity_physx_native_solver_state_pcm_hull_runtime_20260709_171257.json

runtime hull diff:
  data/calibration/unity_runtime_hull_vs_pyphysx_diff_20260709_171257.json
  data/calibration/pyphysx_cooked_stone_hull_probe_unity_flags_rebuilt_native_runtime_20260709.json
  data/calibration/unity_runtime_hull_vs_pyphysx_native_runtime_diff_20260709.json
```

这轮抓到：

```text
rowCount = 132
stone_stone rows = 8
PxcPCMContactConvexConvex before/after = 6 / 6
PxcPCMContactConvexMesh before/after = 61 / 61
readyForFieldDiff = true
readyForContactGenerationDiff = true
```

触发样本：

```text
sample_id = 13000
active shot = BESTSHOT 3.4 0.0 0.0
target stone 8 reset = (2.375, 5.2)
collision_observed = true

final active = (2.3409, 5.4787)
final target = (2.4785, 3.9729)
target move ~= 1.23146m
```

最关键的新增字段是 `PxcPCMContactConvexConvex.pcmInputs.shape0/shape1` 里的
runtime `Gu::ConvexHullData` buffer：

```text
geometryType = eCONVEXMESH
scale = (0.1127000079, 0.1150000021, 0.1127000079)
nbHullVertices = 128
nbPolygons = 66
nbEdges = 192
vertexRefCount = 384
runtime buffer bytes = 4008
```

对比报告显示：Unity runtime hull 与本地 rebuilt pyphysx hull 的几何点集基本一致，
但 `polygons / hullVertices / facesByEdges8 / facesByVertices8 / vertexData8` 的
byte-level feature 顺序不一致。后续不需要再采 endpoint；应该改本地 pyphysx 的
native dump/load/replay，让 `PxGenerateContacts` 的输入 feature/cache 和 Unity 一样。

本地 native pyphysx dump 后结论更强：

```text
Unity runtime hull = 4008 bytes
local native pyphysx runtime hull = 4776 bytes
local extra segment = verticesByEdges16, 768 bytes
```

这说明差异不是 Python 重建脚本造成的；本地真正进入 PhysX PCM 的 hull runtime buffer
已经和 Unity WebGL 的 buffer 不等价。

对应审计文件：

```text
data/calibration/unity_collision_upstream_mismatch_audit_20260709.json
tools/reverse/summarize_collision_upstream_mismatch.py
```

旧的 `events.collision_pause_snapshot.json` 只抓到 `constraintPtr` 和 `FrictionPatch`
预览，没有二级展开 `desc->constraint`；完整 `constraintWindow` 来自后续
streamed event-sink 采样。

旧快照的 8 条 stone-stone finalizer 都是正 separation 且反算 `biasedErr < 0`，
更像 contact-distance 预接触帧，不是主冲量帧。后续 with-writeback hook 已经解决
主 solve/writeback 边界；现在要保留 finalizer/contact-cache 信息，是为了判断 Unity
为什么把同类 contact manifold 压成 2 个点，而本地 immediate 和 report 都是 4 个点。

2026-07-09 后续试跑确认：`CurlingStoneNew.OnCollisionEnter=1` 且 sampler 的
`collision_observed=true` 时，`PxcPCMContactConvexConvex` 调用计数不一定可靠。
但让 `PxcPCMContactConvexMesh` 触发 arm 会被 stone-rink 支撑接触刷爆日志额度。
当前策略是：`PxcPCMContactConvexConvex` 负责 arm，`PxcPCMContactConvexMesh` 只在
armed 窗口内 dump；stone-stone 归类交给 `ContactBuffer`、材质、法线和
`FrictionPatch`。

## 2026-07-10 前半段 capture

这轮采样已经足够支撑 `BESTSHOT -> first PCM entrance` 分析，当前不需要继续打开 Unity
重采。

干净日志：

```text
log/unity_runtime_probe_20260710_012403/events.jsonl
log/unity_runtime_probe_20260710_012403/front_half_pcm_summary.json
data/calibration/front_half_pcm_samples_20260710_012534.jsonl
data/calibration/front_half_pcm_replay_compare_20260710.json
```

工具：

```text
tools/calibration/launch_front_half_pcm_probe.py
tools/calibration/run_front_half_pcm_sampler.py
tools/reverse/summarize_front_half_pcm_capture.py
tools/reverse/compare_front_half_pcm_replay.py
config/front_half_pcm_probe_20260710.json
```

采到的证据：

```text
6 / 6 BESTSHOT 有 first PCM
6 / 6 BESTSHOT 有 first nonzero-contact PCM
sliding.random_range.friction = 8111 条
physx.native.before = 1089 条
physx.native.after = 1089 条
```

采后结论：

```text
用 Unity runtime 的 Random.Range 摩擦序列重放到 first-contact:
  active x/y RMSE ~= 1.13cm
  mean ~= 0.87cm
  max ~= 2.19cm

用本地 self-stop 物理阈值 `2R + 2*contactOffset = 0.30175m` 自行停止：
  使用离散 FixedUpdate tick，不做几何插值
  active x/y RMSE ~= 0.905cm
  max ~= 2.19cm
  平均比 Unity first-contact 早 ~= 0.50 fixed tick
  reached threshold = 5 / 6

从协议 MOTIONINFO 状态继续到同一 self-stop 边界：
  active x/y RMSE ~= 0.106cm
  max ~= 0.173cm
  reached threshold = 6 / 6

所以当前不需要再靠 endpoint 增加样本量。
前半段中线后位置推进已经达到毫米级；剩余主问题是 hidden quaternion/yaw 和
first-contact native state 是否完整传给本地 scene-style PCM/solver。
```

注意区分两个边界：

```text
first-any PCM:
  第一次进入 PxcPCMContactConvexConvex，擦边样本可能 contactBuffer.count = 0。

first-contact PCM:
  第一次 after contactBuffer.count > 0。后续对齐碰撞入口必须用这个边界。
```

这轮还暴露了一个 sampling 注意事项：`RESETPOSITION` 只证明 x/y 被重置，不证明
Rigidbody/shape quaternion 被清零。后续若使用 debug reset 样本，必须把 native
quaternion/yaw 当作真值字段保存和回放，不能默认目标壶姿态为 0。

2026-07-10 后续未再采样，只用上述日志做离线 explicit-handoff replay。新增产物：

```text
tools/reverse/export_front_half_pcm_entrance_truth.py
tools/reverse/build_front_half_explicit_handoff_samples.py
tools/reverse/front_half_pcm_replay.py
tools/reverse/audit_front_half_threshold_replay.py

data/calibration/front_half_pcm_entrance_truth_20260710.json
data/calibration/front_half_threshold_replay_audit_20260710.json
data/calibration/front_half_explicit_handoff_samples_20260710.jsonl
data/calibration/front_half_explicit_handoff_samples_localvel_20260710.jsonl
data/calibration/front_half_explicit_handoff_collision_replay_fullvel_20260710.json
data/calibration/front_half_explicit_handoff_collision_replay_localvel_20260710.json
data/calibration/front_half_explicit_handoff_collision_replay_localvel_contactreport_20260710.json
data/calibration/front_half_explicit_handoff_collision_replay_localvel_targetsettle_20260710.json
data/calibration/front_half_explicit_handoff_collision_replay_localvel_targetsettle_sweep_20260710.json
```

离线结论：

```text
1. 只把 Unity first-contact pose/yaw 喂给 fresh local Scene 还不够：
   active RMSE ~= 5.15cm
   target in-play RMSE ~= 25.64cm

2. target 壶先加入 Scene 并 settle >= 0.01s 后，再把 active 放到 handoff：
   active RMSE ~= 1.12cm
   target in-play RMSE ~= 4.13cm

3. target settle 0.01 / 0.02 / 0.05 / 0.10s 基本平台；
   这不是继续调参，而是证明 target actor 生命周期/contact cache 是真实机制差异。
```

因此当前仍然不需要再采 endpoint。下一步应在本地模拟器结构上复现 Unity 的 actor
生命周期：所有 16 个石壶长期存在于同一个 Scene 中，发球前 reset pose/velocity，
而不是每条碰撞样本在 first PCM handoff 才新建 active/target 两个 actor。

## 如果以后必须再采样

采样必须服务于一个明确问题：

```text
单壶 RNG:
  需要 RANDSEED 或重复同一 BESTSHOT 的分布。

扫冰:
  需要记录 SWEEP 到达帧、Midline/Hogline2 状态和 sweep distance。

碰撞:
  需要 fresh scene / fresh page。
  需要 active/target 碰前碰后短时状态。
  重点抓 native ContactBuffer / solver rows。
```

不要再做只保存最终 `POSITION` 的碰撞采样；那会继续把 contact 和尾段滑行混在一起。

## 用户手动点页面时的最小流程

```text
1. 进入四局或无限模式。
2. 等脚本连接两个 player。
3. 点准备和开始。
4. 每发只跑一个明确 case。
5. 每发结束后清场或 fresh page。
6. 保存 socket log、browser console、probe events。
```

2026-07-09 当前建议命令：

```powershell
python tools\calibration\launch_unity_probe_browser.py `
  --physx-native-hooks `
  --stream-events `
  --stream-no-store `
  --no-poll-events `
  --physx-native-max-dumps 192 `
  --physx-native-arm-ms 8000 `
  --physx-native-window-bytes 2048 `
  --physx-native-solver-constraint-bytes 4096 `
  --physx-native-solver-desc-records 8 `
  --physx-native-solver-body-bytes 256 `
  --interval 0.5
```

无限模式比四局更适合这个任务，因为我们只需要一次短的石壶-石壶碰撞窗口。

但当前阶段不建议继续做普通 endpoint 采样。主线是 native-state hook。
