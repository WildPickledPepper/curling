# PhysX Convex Cooking 与石壶碰撞体

旧版包含大量源码摘录和 wasm 过程，已归档：

```text
docs/archive/unity_reverse_superseded_20260709/12_physx_convex_cooking.zh.md
```

这页只保留当前结论。

## 已确定

正式比赛石壶的碰撞体不是手写 primitive，而是运行时生成的 convex `MeshCollider`。

```text
source mesh:
  ExtendedColliders3D.generateVerticesAndTriangles
  512 unique vertices
  1020 triangles
  world sorted extents ~= (0.230000, 0.281750, 0.281750)
  world radius ~= 0.140875m

Unity cooking flags:
  compute convex
  vertexLimit = 255
  quantizedCount = 255
  quantize_input = false
  gpu_compatible = false
```

因为 source mesh 有 512 个 support-extreme vertices，超过 `vertexLimit=255`，Unity/PhysX 会走 cropped hull 路径。

## 本地离线 cook 结果

重编 pyphysx 后，用 Unity flags 离线 cook 得到：

```text
raw vertices = 128
convex polygons = 66
polygon indices = 384
rendered triangles = 252
topology = 64 边棱柱
faces = 2 个 64 边 cap + 64 个侧面四边形
edges = 192
```

`BigConvexData` 也已离线复刻：

```text
VALE:
  nbVerts = 128
  nbAdjVerts = 384
  valency = 3 for all vertices

GAUS:
  subdiv = 16
  nbSamples = 1536
  support validation errors = 0
```

world-scale mass properties 已推导：

```text
mass = 19.1kg
radial inertia ~= 0.178810612362
vertical inertia ~= 0.189222883199
COM ~= zero
```

## 2026-07-09 运行时 hull dump

这次不是再用 endpoint 猜参数，而是在 Unity WebGL 运行中直接抓
`PxcPCMContactConvexConvex` 入口两端 shape 的 `Gu::ConvexHullData` runtime buffer。

```text
raw events:
  log/unity_runtime_probe_20260709_171257/events.jsonl

solver/native report:
  data/calibration/unity_physx_native_solver_state_pcm_hull_runtime_20260709_171257.json

Unity runtime hull vs local rebuilt diff:
  data/calibration/unity_runtime_hull_vs_pyphysx_diff_20260709_171257.json
  tools/reverse/compare_unity_runtime_hull_to_pyphysx.py

local native pyphysx runtime hull dump:
  data/calibration/pyphysx_cooked_stone_hull_probe_unity_flags_rebuilt_native_runtime_20260709.json
  data/calibration/unity_runtime_hull_vs_pyphysx_native_runtime_diff_20260709.json
```

Unity 运行时 shape 已确定为：

```text
geometryType = eCONVEXMESH
scale = (0.1127000079, 0.1150000021, 0.1127000079)
scaleRotation = identity
meshFlags = 1
gpuCompatible = false

ConvexHullData:
  nbHullVertices = 128
  nbPolygons = 66
  nbEdges = 192
  vertexRefCount = 384
  runtime buffer bytes = 4008
```

这 4008 字节 runtime buffer 的布局也已确认：

```text
polygons          offset 0     bytes 1320
hullVertices      offset 1320  bytes 1536
facesByEdges8     offset 2856  bytes 384
facesByVertices8  offset 3240  bytes 384
vertexData8       offset 3624  bytes 384
```

先用 public `PxConvexMesh` 字段在 Python 侧重建本地 runtime buffer 时，重要结论是：

```text
Unity runtime hull buffer sha16 = 7c5429592f144782
local rebuilt hull buffer sha16 = fc08aa00c31b708a
byteEqual = false
byteDiffCount = 2318 / 4008

segment diffs:
  polygons          550 bytes differ
  hullVertices      967 bytes differ
  facesByEdges8     332 bytes differ
  facesByVertices8  181 bytes differ
  vertexData8       288 bytes differ
```

2026-07-09 随后给本地 pyphysx 补了 native `Gu::ConvexHullData` dump。这个结果更强：

```text
local native pyphysx runtime hull:
  nbHullVertices = 128
  nbPolygons = 66
  nbEdges = 192
  buffer bytes = 4776
  sha16 = fe22499e9fa9f563

local native layout:
  polygons          offset 0     bytes 1320
  hullVertices      offset 1320  bytes 1536
  facesByEdges8     offset 2856  bytes 384
  facesByVertices8  offset 3240  bytes 384
  verticesByEdges16 offset 3624  bytes 768
  vertexData8       offset 4392  bytes 384
```

Unity runtime 的同一层是 4008 bytes，且没有 `verticesByEdges16` 这段：

```text
Unity runtime bytes = 4008
local native bytes = 4776
byteEqual = false
byteDiffCount = 2984
extra local segment:
  verticesByEdges16 = 768 bytes
```

因此这不是 Python 重建脚本制造的假差异；本地 PhysX 进入 PCM 的 native hull runtime
buffer 与 Unity WebGL 进入 PCM 的 native hull runtime buffer 真的不等价。

但这不是“大形状错了”。几何集合几乎相同：

```text
nearest Unity vertex -> local vertex:
  max distance ~= 4.8429e-7 local hull units
  RMS distance ~= 1.8328e-7 local hull units

64 个侧面法线集合在整体相位对齐后：
  max angle error ~= 6.03e-5 deg
  RMS angle error ~= 2.78e-5 deg
```

所以第一处真正分叉是 cooked hull 的 runtime feature 顺序 / adjacency table /
`vertexData8` 相位，以及本地额外存在的 `verticesByEdges16`/GRB edge layout，而不是半径、
质量、摩擦或 solver 公式。PCM contact generation 会用 polygon、vertex、edge adjacency
和 cache 做 feature pair / manifold reduction；同一组几何点，如果 feature 编号和邻接表不同，
本地就可能生成 4 个 contact，而 Unity 生成 2 个 contact。

2026-07-09 的 hull-only patch A/B 又把这个结论收紧了一步：

```text
tool:
  tools/reverse/probe_unity_runtime_hull_patch_contacts.py

report:
  data/calibration/unity_runtime_hull_patch_contact_ab_20260709.json

local shape setup:
  raw 512-point ExtendedCollider mesh
  PxMeshScale = (0.1127000079, 0.1150000021, 0.1127000079)
  quantize_input = false
  gpu_compatible = false
```

结果：

```text
Unity:
  contact_count = 2
  separation = +0.009429097 / +0.009273720

local native 4776 bytes / GRB layout:
  contact_count = 4
  separation range = +0.008100420 .. +0.009458765

local patched Unity 4008 bytes / no-GRB hull-only:
  patch ok = true
  contact_count = 0
```

解释：4008 字节 `Gu::ConvexHullData` runtime buffer 属于真实分叉层，但单独覆盖它不够。
PhysX convex-convex PCM 还会用 `BigConvexRawData` 的 support vertex map、valencies、
adjacent vertices，以及 persistent manifold/cache 的 feature anchors。若 hull buffer 换成
Unity 的，而 BigConvex/support-map 仍是本地 cook 的，本地 contact generation 会变成
不自洽状态，结果从 4 点变成 0 点，而不是 Unity 的 2 点。

2026-07-09 后续补齐了本地实验接口：

```text
pyphysx Shape:
  create_convex_mesh_from_points_with_scale(...)
  patch_convex_mesh_runtime_hull_data_for_unity(...)
  patch_convex_mesh_big_convex_raw_data_for_unity(...)

local BigConvex expected sizes:
  samples = 3072 bytes
  valencies = 512 bytes
  adjacent vertices = 384 bytes
```

2026-07-09 随后新增了 runtime-hull 版 BigConvex 重建器：

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

也就是说，`BigConvexRawData` 的三段 pointed arrays 已经可以从 runtime hull 的
polygons、facesByEdges8、vertexData8 按 PhysX 源码重建；它不再是主要黑盒。

用这个重建结果再跑 A/B：

```text
report:
  data/calibration/unity_runtime_hull_plus_rebuilt_bigconvex_contact_ab_20260709.json
  data/calibration/unity_runtime_hull_plus_rebuilt_bigconvex_pcm_pose_contact_ab_20260709.json

Unity:
  contact_count = 2
  separation = +0.009429097 / +0.009273720

local native 4776/GRB:
  contact_count = 4

Unity 4008/no-GRB hull-only:
  contact_count = 0

Unity 4008/no-GRB + rebuilt BigConvex:
  contact_count = 4

同样切到 PCM-after transform pose:
  contact_count = 4
```

这组 A/B 当时仍走 `PxGenerateContacts` immediate-mode 探针，所以它暴露的是
“静态 hull/BigConvex + immediate wrapper”不等价 Unity scene，而不是最终证明
Unity contact generator 仍未知。

2026-07-09 晚上的 direct scene-style PCM 审计已经把这层重新合上：

```text
data/calibration/unity_pcm_refresh_invalidate_audit_20260709.json
data/calibration/unity_direct_pcm_vs_immediate_audit_20260709.json

Unity raw PCM-after cache + Unity native transform
  refreshContactPoints: 2 -> 2
  invalidate_BoxConvex = false

local direct g_PCMContactMethodTable:
  contact_count = 2
  normal 与 Unity 一致
  separation 与 Unity 只差约 7e-8m

local immediate PxGenerateContacts:
  仍会出现 3 contacts 或 hull-only 0 contacts
```

因此最新结论不是“继续等待 BigConvex capture”，也不是“继续手调 cooked hull 直到
immediate probe 变成 2 点”。静态 cooked feature bundle 仍然重要，尤其影响 fresh-cache
和后续无 seed 的泛化；但当前首个 cached stone-stone manifold 的 2-contact 分叉，主要来自
本地 replay 调用边界和 cache 语义，而不是 Unity runtime hull 几何集合本身。

2026-07-09 晚上已经把 runtime feature patch 接进完整 `probe_physx_collision_alignment.py`：

```text
--unity-runtime-feature-mode hull-bigconvex
--unity-runtime-feature-events log/unity_runtime_probe_20260709_171257/events.jsonl
--synthetic-bigconvex data/calibration/unity_runtime_bigconvex_rebuild_20260709.json

active / target:
  ConvexHullData runtime buffer: 4776 -> 4008, ok=true
  BigConvex arrays: samples=3072, valencies=512, adjacent=384, ok=true
```

这证明完整 Scene 代码里已经可以灌入 Unity runtime hull + BigConvex。可是同一
full Scene smoke test 的 first immediate contact 仍是 fresh 4 点，且 separation 是负穿透。
因此当前不能再把 10cm 级误差归咎为“hull patch 没接上”；要继续查 first-frame pose /
target 初始状态 / pair cache 生命周期。

随后确认了一个更细的几何语义坑：Unity runtime `ConvexHullData` 4008 bytes 是
Unity/PhysX native xyz/y-up 坐标语义；而完整 pyphysx replay 的 formal mesh 已经被放进
z-up shape frame。旧 full Scene smoke 虽然 patch 返回 `ok=true`，但其实是把 native xyz
hull 原样塞进 z-up Scene。

当前正确接法是：

```text
Unity runtime hull -> pyphysx z-up:
  polygons.plane normal: x,y,z -> x,z,y
  hullVertices:          x,y,z -> x,z,y
  facesByEdges8 / facesByVertices8 / vertexData8: 保持 index bytes 不变

BigConvexRawData:
  不再直接复用 Unity native/synthetic 原数组；
  从换轴后的 runtime hull 用 subdiv=16 重新 rebuild samples / valencies / adjacentVerts。
```

对应证据：

```text
data/calibration/unity_physx_collision_probe_native13000_runtime_feature_unitynative_old_20260709.json
data/calibration/unity_physx_collision_probe_native13000_runtime_feature_zup_rebuilt_20260709.json
data/calibration/unity_physx_collision_probe_native13000_runtime_feature_zup_interpdist_20260709.json

raw hull 原样 patch 到 z-up Scene:
  active error ~= 0.20025m
  target error ~= 4.43507m

hull 换轴 + BigConvex 从换轴 hull 重建:
  active error ~= 0.00716m
  target error ~= 0.08409m

再把 handoff 插值到 Unity first PCM 中心距 0.2908524358m:
  active error ~= 0.00481m
  target error ~= 0.00575m
```

所以 convex/cooking 侧的当前结论是：几何集合、拓扑和 BigConvex 重建已经足够支持
1cm 内 replay；剩余泛化问题转到“如何为每个 shot 得到 Unity 同步的 first PCM entrance
pose/yaw/center distance/cache lifecycle”，而不是继续猜 cooked hull 参数。

同一 native13000 样本还验证了 active yaw 可以由现有运动积分近似得到，而不是必须手填
Unity 抓到的常数：

```text
data/calibration/unity_physx_collision_probe_native13000_runtime_feature_zup_interpdist_integratedyaw_20260709.json

integrated-precontact yaw ~= 0.2497797536rad
best local sign = -1
active error ~= 0.00474m
target error ~= 0.00612m
```

但把同一个 handoff 中心距直接套到旧的 12 条 endpoint-only controlled collision 样本，
target RMSE 仍约 28.5cm：

```text
data/calibration/unity_physx_collision_probe_controlled12_runtime_feature_zup_interpdist_integratedyaw_20260709.json
```

这说明 native13000 的 first PCM entrance state 不能当作所有样本的固定规则；旧样本缺
运行时 first PCM pose/relative transform，所以只能用于 endpoint 粗验证，不能用于证明
入口 state 已泛化闭合。

## 已排除

```text
1. “pyphysx 不能 cook Unity flags”不是阻塞点。
2. “没有把 512 顶点 formal mesh 送进 pyphysx”不是 10cm 主因。
3. 单独替换 cooked-hull inertia 不能把 collision target RMSE 压到 2cm。
4. formal radius=0.140875m 直接接入当前 replay 仍约 12cm target RMSE。
5. 石壶几何顶点集合本身不是主因；Unity 和本地顶点/侧面法线集合已经基本重合。
6. Unity runtime hull / BigConvex 不是未知黑盒；关键是坐标语义必须和本地 Scene frame 一致。
```

这说明剩余误差更可能在“每个样本如何重建 Unity first PCM entrance state”，而不是
“石壶大形状完全没恢复”，也不是单独的 BigConvex support-map 黑盒。

## 仍未闭合

```text
1. 把 handoff-center-distance / target pose 从 Unity runtime 抓取结果推广到普通训练样本。
2. 用新的 runtime raw 默认采样抓真实 BigConvex pointed arrays，验证与 z-up rebuild 是否一致。
3. 验证 integrated-precontact yaw 在更多 collision 样本上是否稳定，不再依赖手填 Unity yaw。
4. 为更多碰撞样本抓 first PCM entrance state，不能再只靠 endpoint-only 旧样本拟合。
5. 最后再把这个入口-state 重建方法接入训练用本地模拟器。
```

这些字段继续走 runtime native dump 和 trace-driven replay，不再用 endpoint 参数拟合。

## 关键工具和报告

```text
tools/reverse/dump_pyphysx_cooked_convex_hull.py
tools/reverse/analyze_pyphysx_raw_hull_topology.py
tools/reverse/analyze_pyphysx_bigconvex_data.py
tools/reverse/analyze_pyphysx_scaled_mass_properties.py
tools/reverse/summarize_formal_stone_cooking_status.py
tools/reverse/compare_unity_runtime_hull_to_pyphysx.py
tools/reverse/probe_unity_runtime_hull_patch_contacts.py

data/calibration/formal_stone_cooking_status_20260708.json
data/calibration/pyphysx_raw_hull_topology_20260708.json
data/calibration/pyphysx_bigconvex_data_20260709.json
data/calibration/pyphysx_scaled_mass_properties_20260709.json
data/calibration/unity_runtime_hull_vs_pyphysx_diff_20260709_171257.json
data/calibration/pyphysx_cooked_stone_hull_probe_unity_flags_rebuilt_native_runtime_20260709.json
data/calibration/unity_runtime_hull_vs_pyphysx_native_runtime_diff_20260709.json
data/calibration/unity_runtime_hull_patch_contact_ab_20260709.json
```
