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

## 已排除

```text
1. “pyphysx 不能 cook Unity flags”不是阻塞点。
2. “没有把 512 顶点 formal mesh 送进 pyphysx”不是 10cm 主因。
3. 单独替换 cooked-hull inertia 不能把 collision target RMSE 压到 2cm。
4. formal radius=0.140875m 直接接入当前 replay 仍约 12cm target RMSE。
```

这说明剩余误差更可能在 runtime shape local pose/scale、正式 cooked stream 字节级差异、contact manifold/cache 或 handoff native state，而不是“石壶大形状完全没恢复”。

## 仍未证明

```text
1. Unity runtime formal stone 的 PxConvexMesh stream 是否 byte-level 等于离线 cook。
2. PxShape local pose / scale 是否与本地默认 identity 完全一致。
3. Runtime rebuild 后 Rigidbody inertia tensor 是否逐字段等于离线推导。
4. 首次 contact 选择的是哪组 hull feature。
```

这些字段需要 runtime dump，而不是 endpoint 拟合。

## 关键工具和报告

```text
tools/reverse/dump_pyphysx_cooked_convex_hull.py
tools/reverse/analyze_pyphysx_raw_hull_topology.py
tools/reverse/analyze_pyphysx_bigconvex_data.py
tools/reverse/analyze_pyphysx_scaled_mass_properties.py
tools/reverse/summarize_formal_stone_cooking_status.py

data/calibration/formal_stone_cooking_status_20260708.json
data/calibration/pyphysx_raw_hull_topology_20260708.json
data/calibration/pyphysx_bigconvex_data_20260709.json
data/calibration/pyphysx_scaled_mass_properties_20260709.json
```
