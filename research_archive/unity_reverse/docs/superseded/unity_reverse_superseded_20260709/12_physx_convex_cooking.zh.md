# PhysX Convex Cooking 与石壶碰撞体

记录石壶 `ExtendedColliders3D` 生成的 MeshCollider 在进入 PhysX contact generation 之前，可能被 convex cooking 改写成什么几何。这个文档只维护 cooking/cooked hull 证据；PCM/GJK/SAT 接触点生成见 [`05_physx_contact_generation.zh.md`](05_physx_contact_generation.zh.md)，solver 见 [`06_physx_solver.zh.md`](06_physx_solver.zh.md)。

## 已确定

石壶运行时由 `ExtendedColliders3D.Awake/generateMesh` 创建 MeshCollider。资产和反编译证据一致：

```text
ExtendedColliders3D:
  type = 5 cylinder
  convex = true
  isTrigger = false
  material = Bouncy
  size = (2.5, 2.0, 2.5)
  cylinderFaces = 256
  caps = (True, True)
  flipFaces = true

场景 transform:
  local scale = (0.115, 0.115, 0.115)
  world scale ~= (0.1127, 0.115, 0.1127)
  local radius = 1.25 * 0.115 = 0.143750
  world radius ~= 1.25 * 0.1127 = 0.140875
```

`tools/reverse/recovered_extended_collider_mesh.py` 复原出的 cooking 前网格为：

```text
vertices = 512
indices = 3060
triangles = 1020
side triangles = 512
cap triangles = 508
```

导出的临时文件保留在：

```text
D:\esp\tmp\curling_reverse_il2cpp\stone_extendedcollider_mesh_256.json
```

不要删这个文件；后续离线 cooking dump 会反复用它。

2026-07-08 继续把“是否必进 cropped hull”固化成脚本：

```powershell
python tools\reverse\summarize_stone_quickhull_path.py
```

当前输出要点：

```text
raw vertices = 512
unique vertices = 512
y levels = [-1.0, 1.0]
radius range = 1.25 .. 1.25
support-extreme vertices = 512
PxConvexMeshDesc.vertexLimit = 255
```

这里的 `support-extreme vertices=512` 是几何侧证据：对每个顶点取一个接近其径向角度、
并用极小 y 分量区分上下圈的 support direction，该点都是唯一极值点。因此这不是
“512 个 mesh 点里有很多内部点可以直接丢掉”，而是一个上下两圈都在凸包边界上的
256 边棱柱。结合 Unity flags 已确认没有 `eQUANTIZE_INPUT`，PhysX QuickHull 在
`fillConvexMeshDesc()` 后如果仍保留原始 hull，会触发 `Cooking::cookConvexMeshInternal`
的 `desc.points.count >= 256` 失败检查。因此正式石壶应走：

```text
QuickHullConvexHullLib::createConvexHull
  -> expandHullOBB          # 因为未启用 ePLANE_SHIFTING
  -> mCropedConvexHull
  -> fillConvexMeshDescFromCroppedHull
```

所以 `mCropedConvexHull` 是否发生已经不应再当主要未知；剩余是 OBB crop 后实际
输出的顶点、面、plane、indices 和 mass/inertia 数值。

## Unity MeshCollider runtime 证据

`ExtendedColliders3D` 里能看到脚本层行为：运行时 `AddComponent<MeshCollider>`，然后设置 `sharedMesh` 和 `convex`。为了确认这两个 setter 到 Unity native 层实际改了什么，已经追到 wasm internal-call 注册表：

```text
UnityEngine.MeshCollider::set_sharedMesh -> table ptr 129385 -> func82533
UnityEngine.MeshCollider::set_convex     -> table ptr 129386 -> func82534
```

`set_convex` 的调用链：

```text
func82534
  f_ognd(a)                # C# object -> native MeshCollider*
  f_rwcd(native, b != 0)   # 真正设置 convex

func72947 / f_rwcd
  if a[80]:ubyte != b and dirty flag enabled:
    f_djld(a)
  a[80]:byte = b
  if collider attached to scene/object:
    call virtual dirty/rebuild callback
```

因此 `a[80]` 基本可以钉为 MeshCollider 的 `convex` 布尔位。

`set_sharedMesh` 的调用链：

```text
func82533
  f_ognd(a)                # C# object -> native MeshCollider*
  f_ovnd(mesh)             # Mesh C# object -> native Mesh*
  a[21]:int = mesh_native  # 写入 sharedMesh 指针
  if changed:
    f_djld(a)
    call virtual dirty/rebuild callback
```

这个 setter 路径里没有看到显式写 `m_CookingOptions` 或 PhysX convex flags。也就是说，石壶运行时碰撞体的脚本层已确认会进入 “有 mesh + convex=true” 的 cooking/rebuild 路径；但 cooking options 更可能来自 MeshCollider native 默认值、Unity 版本默认策略，或 rebuild/cook 函数内部映射，而不是 `ExtendedColliders3D` 自己设置。

继续追 native MeshCollider 初始化和字段读写后，`m_CookingOptions` 的默认值已经可以钉住：

```text
func72956 / f_axcd     # MeshCollider native 初始化/reset 路径
  a[36]:long@4 = 128849018910L
  a[80]:byte = 0
  a[140]:byte = 1

128849018910L = 0x1e0000001e
低 32 位 = 30
高 32 位 = 30
```

所以新建 MeshCollider 的 native 字段里，`a[36]` 与旁边缓存字段 `a[37]` 都被初始化为 `30`，`a[80]` 初始化为 `false`。`ExtendedColliders3D` 只调用 `set_convex(true)`，没有看到任何修改 `m_CookingOptions` 的脚本层或 native setter，因此石壶 runtime MeshCollider 的 `m_CookingOptions=30` 现在是高置信结论。

字段名也能从 Unity 序列化/传输函数里交叉验证：

```text
func72959 / f_dxcd
  f_fxkd(..., 39519, ..., a + 80, 0)        # m_Convex
  c.a = a[36]
  f_fxkd(..., 71909, ..., c, 8388608)       # m_CookingOptions
  a[36] = c.a
  f_fxkd(..., 136988, 220012, a + 84, 0)    # m_Mesh

func72960 / f_excd
  f_yykd(..., a + 80, 39519, ...)           # m_Convex
  c[2] = a[36]
  f_vrnd(..., c + 8, 71909, ...)            # m_CookingOptions
  a[36] = c[2]
  if (f_cykd(b, 3)) { a[36] = a[36] | 16 }  # 老版本/缺字段兼容路径补 UseFastMidphase
```

对应字符串地址已经在 wasm data 段确认：

```text
39519  -> m_Convex
71909  -> m_CookingOptions
136988 -> m_Mesh
```

真正触发 shape/cooked mesh 创建的是 `func72950`。这个函数会读取 `a[21]` 的 mesh 指针、`a[80]` 的 convex 布尔位和 `a[36]` 的 cooking options，并把它们传给全局物理管理器 `4679096[0]` 的 vtable 第 11 项：

```text
func72950 / f_uwcd
  f = a[21]:int                  # sharedMesh native pointer
  ...
  b = a[36]:int                  # m_CookingOptions
  e = a[80]:ubyte                # convex
  call_indirect(4679096[0], f, e, b, ..., (manager[0])[11])

  # 另一条 rebuild 分支也一致
  call_indirect(4679096[0], f, a[80]:ubyte, a[36]:int, ..., (manager[0])[11])
```

这说明 `m_CookingOptions=30` 不是只存在于序列化字段里，而是实际参与了 MeshCollider shape/cooked mesh 创建。另一个 mesh 预载/缓存路径 `func78763` 也会用硬编码 `30` 调同一个 manager vtable 第 11 项，进一步印证 Unity 2022.3.62f2c1 这一版的默认 cooking options 就是 30。

Unity C# 侧枚举定义来自 UnityCsReference：

```text
MeshColliderCookingOptions.None                 = 0
InflateConvexMesh                               = 1  # obsolete
CookForFasterSimulation                         = 2
EnableMeshCleaning                              = 4
WeldColocatedVertices                           = 8
UseFastMidphase                                 = 16
```

因此：

```text
m_CookingOptions = 30 = 2 + 4 + 8 + 16
```

也就是默认开启 `CookForFasterSimulation`、`EnableMeshCleaning`、`WeldColocatedVertices`、`UseFastMidphase`，不开启已废弃的 `InflateConvexMesh`。

## Unity 到 PhysX cooking 入口

`func72950` 里的全局物理管理器已经继续解析到具体 vtable：

```text
func73790 / f_cded
  a = f_igsd(4, 41, 16, 300)
  a[0] = 3221824
  f_gbsc(a)                         # 4679096[0] = a

3221824 vtable:
  [11] = table 122182 -> $f72989 -> func72989

func72989 / f_hycd
  return f_zkdd(mesh, convex, cookingOptions, out, extra, 0)

func73319 / f_zkdd
  现场构造 PxCookingParams
  现场构造 PxConvexMeshDesc / PxSimpleTriangleMesh
  convex=true 时走 PxConvexMeshDesc 分支
```

`func73319` 里已经能把 Unity cooking options 和 PhysX 参数对上：

```text
PxCookingParams:
  areaTestEpsilon = 0.06 * scale.length * scale.length
  planeTolerance  = 0.0007
  convexMeshCookingType = QUICKHULL
  buildGPUData = false
  gaussMapLimit = 32

  EnableMeshCleaning 打开时:
    meshPreprocessParams 不写 eDISABLE_CLEAN_MESH

  EnableMeshCleaning 关闭时:
    meshPreprocessParams 写 eDISABLE_CLEAN_MESH

  UseFastMidphase 打开时:
    midphaseDesc = BVH34, numPrimsPerLeaf = 4

  UseFastMidphase 关闭时:
    midphaseDesc = BVH33, meshSizePerformanceTradeOff = 0.55
    CookForFasterSimulation 打开 -> meshCookingHint = eSIM_PERFORMANCE
    CookForFasterSimulation 关闭 -> meshCookingHint = eCOOKING_PERFORMANCE
```

注意：`midphaseDesc` 和 triangle mesh preprocess 主要影响非 convex triangle mesh。石壶走的是 `convex=true` 分支；PhysX 4.1 源码里 convex cooking 实际使用的是 `areaTestEpsilon`、`planeTolerance`、`buildGPUData`、`gaussMapLimit` 和 `PxConvexMeshDesc.flags/vertexLimit/quantizedCount`。

石壶 convex 分支构造出的 `PxConvexMeshDesc` 更关键：

```text
func73319 convex=true:
  desc.points.stride = 12
  desc.points.data   = Unity 预处理后的 vertex buffer
  desc.points.count  = h

  g[53]:int = 16711682 = 0x00ff0002
    low16  = 0x0002 -> PxConvexFlag::eCOMPUTE_CONVEX
    high16 = 0x00ff -> vertexLimit = 255

  g[108]:short = 255 -> quantizedCount = 255
```

所以石壶 runtime convex cooking 现在可以确认：

```text
PxConvexFlag::eCOMPUTE_CONVEX              = on
PxConvexFlag::eCHECK_ZERO_AREA_TRIANGLES   = off
PxConvexFlag::eQUANTIZE_INPUT              = off
PxConvexFlag::eGPU_COMPATIBLE              = off
PxConvexFlag::ePLANE_SHIFTING              = off
PxConvexFlag::eFAST_INERTIA_COMPUTATION    = off
PxConvexFlag::eSHIFT_VERTICES              = off
vertexLimit                                = 255
quantizedCount                             = 255
buildGPUData                               = false
```

下游调用也已经定位：

```text
func73319
  f_fwcd(..., PxCookingParams*) -> 创建 vtable=3219996 的 physx::Cooking 包装对象
  convex 分支 call vtable[8]

3219996 vtable:
  [8] = table 122118 -> $f72928 -> func72928

func72928:
  f_wvcd(...)        # 生成 cooked convex 数据
  call_indirect(..., 2, cookedData, insertionCallback, ...)
```

继续向下追后，`f_wvcd` 和 PhysX 源码可以对上：

```text
func72926 / f_wvcd
  校验 PxConvexMeshDesc::isValid()
  若 desc.flags 带 eCOMPUTE_CONVEX:
    调 hullLib vtable[2]
    调 hullLib vtable[3]
  f_aucd(cookedOut, desc, gaussMapLimit=32, validateOnly=0, hullLib)

func72878 / f_aucd
  对应 PhysX ConvexMeshBuilder::build(desc, gaussMapLimit, validateOnly, hullLib)
  内部先 gather points / indices / polygons
  再 hullBuilder.init(..., hullLib)
  再 computeMassInfo(...)
  若 hull vertex 数超过 gaussMapLimit=32，则 computeGaussMaps()
  validateOnly=false 时 computeInternalObjects()
```

`func72927` 是相邻的 cooked convex 序列化路径，会写出 `CVXM/CLHL/SUPM/GAUS` 等块；这和 PhysX cooked convex mesh 数据结构吻合。真正还没完全拆开的，是 `hullLib` / QuickHull 的具体输出和最终 cooked hull 内容。

`hullLib` 对象也已经定位到：

```text
func72905 / f_bvcd
  构造 QuickHullConvexHullLib
  a[0] = 3217816
  a[1] = PxConvexMeshDesc*
  a[2] = PxCookingParams*
  a[8] = QuickHull 内部对象

3217816 vtable:
  [2] = table 122107 -> $f72908 -> func72908 -> createConvexHull()
  [3] = table 122108 -> $f72915 -> func72915 -> fillConvexMeshDesc()
  [4] = table 122109 -> $f72914 -> edge/face helper
```

这意味着 Unity wasm 里不是一个黑箱“某个碰撞函数”，而是标准 PhysX 4.1 QuickHull cooking 链路。现在最关键的未知已经从 QuickHull 参数收缩到：把导出的 cooked hull desc 映射回 Unity/PxShape 的 local pose、scale 和复合 collider 关系。

## PhysX 4.1 cooking 分支

PhysX 4.1 源码位置：

```text
D:\esp\tmp\curling_physx_41\physx\include\cooking\PxConvexMeshDesc.h
D:\esp\tmp\curling_physx_41\physx\include\cooking\PxCooking.h
D:\esp\tmp\curling_physx_41\physx\source\physxcooking\src\Cooking.cpp
D:\esp\tmp\curling_physx_41\physx\source\physxcooking\src\convex\QuickHullConvexHullLib.cpp
```

关键常量和默认值：

```text
PxConvexMeshDesc.vertexLimit default = 255
PxConvexMeshDesc.quantizedCount default = 255
PxCookingParams.planeTolerance default = 0.0007
PxCookingParams.areaTestEpsilon default = 0.06 * scale.length^2
PxCookingParams.convexMeshCookingType default = eQUICKHULL
PxCookingParams.buildGPUData default = false
PxConvexFlag::ePLANE_SHIFTING default = off
```

源码层面的处理逻辑已经确认：

```text
Cooking::cookConvexMeshInternal
  if eCOMPUTE_CONVEX:
    hullLib->createConvexHull()
    如果返回 eSUCCESS 或 ePOLYGONS_LIMIT_REACHED，继续 fillConvexMeshDesc()
    ePOLYGONS_LIMIT_REACHED 不是失败，只是 condition 记录超限

QuickHullConvexHullLib::createConvexHull
  buildHull()
  if ePOLYGONS_LIMIT_REACHED 或 eVERTEX_LIMIT_REACHED:
    if ePLANE_SHIFTING:
      expandHull()
    else:
      expandHullOBB()

expandHullOBB()
  1. 从当前 QuickHull visible faces 收集 expandPlanes
  2. fillConvexMeshDescFromQuickHull(convexDesc)
  3. computeOBBFromConvex(convexDesc, sides, obbTransform)
  4. 用这个 OBB 构造初始 ConvexHull
  5. 最多取 256 个候选 plane:
       k = c->findCandidatePlane(planeTolerance, epsilon)
       c = convexHullCrop(c, expandPlanes[k], planeTolerance)
       如果 crop 后 vertices > vertexLimit，则回退到上一个 hull 并停止
  6. mCropedConvexHull = c
```

所以 256 面石壶不是“理想圆柱直接进求解器”。一旦 cooked hull 触发顶点/面限制，
PhysX 会使用一个由 OBB 裁剪出的 partial hull。这个 cropped hull **不是**简单盒子；
它是“从 OBB 起步，再按 QuickHull 生成的面逐步切割出来的 partial hull”。具体输出
依赖 QuickHull 面序、`findCandidatePlane()` 选择和 `convexHullCrop()` 的浮点细节，
所以当前还不能用半径/高度手写一个固定多边形来替代。Unity wasm 里也有对应错误/警告文本：

```text
Couldn't create a Convex Mesh from source mesh "%s" within the maximum polygons limit (256).
The partial hull will be used...
```

这条证据解释了为什么只用二维圆盘半径或理想 256 面圆柱，很难把碰撞误差压到 2cm。

## wasm cropped-hull 证据脚本

2026-07-08 又把 `createConvexHull -> expandHullOBB -> fillConvexMeshDesc`
这条链路固化成可复跑脚本：

```powershell
python tools\reverse\summarize_physx_cropped_hull_path.py
```

这个脚本读取：

```text
D:\esp\tmp\curling_reverse_il2cpp\build.dcmp
D:\esp\tmp\curling_physx_41\physx\source\physxcooking\src\convex\QuickHullConvexHullLib.cpp
D:\esp\tmp\curling_physx_41\physx\source\physxcooking\src\convex\ConvexHullUtils.cpp
D:\esp\tmp\curling_physx_41\physx\source\physxcooking\src\Cooking.cpp
```

当前输出的关键证据：

```text
stone flags = 0x0002
ePLANE_SHIFTING = false
eGPU_COMPATIBLE = false
expected expand path = f_gvcd / expandHullOBB

func72908 / f_evcd / createConvexHull:
  L3434123  getNbHullVerts <= vertexLimit 时不 expand
  L3434131  flags & 32 时走 f_fvcd / expandHull
  L3434128  flags 不含 32 时走 f_gvcd / expandHullOBB
  L3434138  flags & 128 是 GPU compatible 后备分支

func72910 / f_gvcd / expandHullOBB:
  L3434624  f_jvcd(a, n + 16)              # fillConvexMeshDescFromQuickHull
  L3434625  复制 desc.flags
  L3435466  maxplanes = min(256, expandPlanes.size)
  L3435560  candidate plane 选择逻辑
  L3435574  convexHullCrop 对应的大栈内联块
  L3436117  c.vertices > vertexLimit 时回退
  L3436147  flags & 128 是 GPU per-face limit 分支
  L3436248  a[9] = c                       # mCropedConvexHull = c

func72915 / f_lvcd / fillConvexMeshDesc:
  L3436590  if (a[9]) 进入 cropped hull 路径
  L3436653  b.g = 4                        # indices.stride
  L3436656  b.a = 12                       # points.stride
  L3436657  b.d = 20                       # polygons.stride
  L3436765  else f_jvcd(a, b)              # 非 cropped QuickHull 路径
```

这一步把“是否进入 cropped hull”从推理结论提升成了 wasm/源码双重证据。
因此后续不应再把 `stone_faces`、`vertexLimit` 或 `eGPU_COMPATIBLE` 当成大网格参数去蒙；
真正剩下的是把 `a[9]` 指向的 cropped hull 或 `func72915` 写回的
`points/polygons/indices` 导出来。

## cooked hull 导出抓取点

Unity 最终 `PxConvexMeshDesc` 几何已经能从运行时直接导出；最短抓取点如下。
辅助定位工具：

```powershell
python tools\reverse\summarize_cooked_hull_capture_points.py
```

当前结论：优先 hook `func72915 / f_lvcd` 返回后，读取第二个参数指向的
`PxConvexMeshDesc` 前 36 字节。这个 desc 已经是 cropped hull 写回后的结果，
不需要先解析完整 `CVXM/CLHL` stream。

```text
+0  u32 points.stride    = 12
+4  u32 points.data      = vertsOut
+8  u32 points.count     = numVertices

+12 u32 polygons.stride  = 20
+16 u32 polygons.data    = polygonsOut
+20 u32 polygons.count   = numPolygons

+24 u32 indices.stride   = 4
+28 u32 indices.data     = indicesOut
+32 u32 indices.count    = numIndices
```

抓到这三组数组就能得到 Unity 真值：

```text
points.data    -> points.count * 12 bytes, PxVec3 顶点
polygons.data  -> polygons.count * 20 bytes, PxHullPolygon，含 plane 和 indexBase
indices.data   -> indices.count * 4 bytes, PxU32 顶点索引
```

### 2026-07-08 运行时抓取结果

在四局制等待连接页面，不需要 socket 连接、不需要开始对局；进入该场景后
Unity 会创建若干 convex `MeshCollider`，`func72915/f_lvcd` 会被调用。
本次 hook 的 wasm table index 为 `122108`，抓取日志为：

```text
log/unity_runtime_probe_20260708_225950/events.latest.json
```

稳定导出文件：

```text
data/calibration/unity_cooked_hulls_20260708_225950.json
```

导出命令：

```powershell
python tools\reverse\export_cooked_hull_from_probe_events.py `
  log\unity_runtime_probe_20260708_225950\events.latest.json `
  -o data\calibration\unity_cooked_hulls_20260708_225950.json
```

本次共抓到 `14` 个 cooked hull desc，其中 `8` 个唯一几何。关键项如下：

```text
event 113/117/121/125:
  source mesh = 1_0, 2_0, 3_0, 4_0
  vertices=129, polygons=254, indices=762
  extents=(0.083596, 0.159256, 0.159977)
  hash=0aac2338ce35d813

event 115/119/123/127:
  source mesh 未由 Unity warning 打印
  vertices=99, polygons=158, indices=510
  extents=(0.023931, 0.152456, 0.157076)
  hash=957070e591b9f7ce

base_link_0:
  vertices=129, polygons=254, indices=762
  extents=(0.159229, 0.159977, 0.083596)
  hash=0ee365a79abbc1f0

base_link_1:
  vertices=130, polygons=255, indices=766
  extents=(0.606739, 0.159373, 0.083618)
  hash=95886646ab4821cb

base_link_2:
  vertices=130, polygons=254, indices=764
  extents=(0.610349, 0.159913, 0.492628)
  hash=5fca89a703de03b5

base_link_3:
  vertices=130, polygons=255, indices=766
  extents=(0.612593, 0.158413, 0.083551)
  hash=d7dd908b0bc18300
```

重要解释：

```text
1. 1_0/2_0/3_0/4_0 的 129 点 hull 是同一套几何，但尺寸不匹配正式石壶。
2. 每个 129 点 hull 后面还出现一个重复的 99 点 hull；这说明等待页确实触发了多次
   convex cooking，但不能据此推出正式石壶是这两套 hull 的复合体。
3. Unity 控制台同时打印：
   Couldn't create a Convex Mesh from source mesh "1_0"... partial hull will be used
   这与 PhysX `vertexLimit=255` 和 cropped hull 路径完全一致。
```

但随后做了尺寸自检，结论必须修正：这批等待页 cooked hull **不能**当成正式比赛石壶
collision hull。辅助判据工具：

```powershell
python tools\reverse\analyze_cooked_hull_identity.py
```

输出：

```text
data/calibration/unity_cooked_hull_identity_20260708_225950.json
```

正式石壶 `ExtendedColliders3D` 的期望世界尺寸来自资产解析：

```text
radius_world ~= 0.14087501
height_world = 0.23
sorted extents ~= (0.230000, 0.281750, 0.281750)
```

而等待页抓到的最佳候选 `1_0/2_0/3_0/4_0` 为：

```text
sorted extents=(0.083596, 0.159256, 0.159977)
max relative error ~= 0.637
match=False
```

因此当前更严谨的解释是：

```text
1. `func72915` hook 和 desc 导出机制有效，能拿到真实 cooked convex desc。
2. 四局等待页不连接/不开局时抓到的是等待页或机器人/装饰相关 convex mesh，
   不是已经证明的正式比赛石壶碰撞 hull。
3. `base_link_*` 名称明显属于 URDF/机器人路径，也不能混进正式石壶碰撞模型。
4. 正式石壶 cooked hull 仍需从 `ExtendedColliders3D` 生成的比赛 stone MeshCollider
   创建时刻导出，或离线复刻 PhysX OBB crop 得出；不能把本次 `1_0/99点`
   几何接进 `probe_physx_collision_alignment.py`。
```

`func72926 / f_wvcd` 是调用者侧的二级抓取点：它在 `call_indirect(d, f, (d[0])[3])`
后检查 `f[2] >= 256`，这里的 `f[2]` 就是 `desc.points.count`。如果此时
`points.count < 256`，才继续进入 `f_aucd / ConvexMeshBuilder::build`。

`func72927 / f_xvcd` 是更晚的完整 cooked stream 抓取点：它会写 `CVXM/CLHL`，
并继续写 bounds、mass/inertia/COM、GAUS/SUPM/VALE 等。这个路径信息更完整，
但要解析 stream；若目标只是拿 hull 几何，`func72915` 的 desc 更短。

## cooked hull 字段级布局

新增工具：

```powershell
python tools\reverse\physx_convex_layouts.py
```

这个工具按 Unity WebGL / wasm32 的 32-bit 指针布局打印 PhysX 4.1 convex 相关结构偏移，用来和 `func72915/func72927` 对照。当前确认的关键结构：

```text
PxBoundedData32:
  +0  u32 stride
  +4  u32 data
  +8  u32 count

PxConvexMeshDesc32:
  +0   PxBoundedData points
  +12  PxBoundedData polygons
  +24  PxBoundedData indices
  +36  u16 flags
  +38  u16 vertexLimit
  +40  u16 quantizedCount
  sizeof = 44

PxHullPolygon:
  +0   float plane[4]
  +16  u16 mNbVerts
  +18  u16 mIndexBase
  sizeof = 20

Gu::HullPolygonData:
  +0   PxPlane mPlane
  +16  u16 mVRef8
  +18  u8  mNbVerts
  +19  u8  mMinIndex
  sizeof = 20

Gu::ConvexHullData, wasm32:
  +0   CenterExtents mAABB
  +24  PxVec3 mCenterOfMass
  +36  PxBitAndWord mNbEdges
  +38  u8 mNbHullVertices
  +39  u8 mNbPolygons
  +40  ptr mPolygons
  +44  ptr mBigConvexRawData
  +48  InternalObjectsData mInternal
  sizeof = 64

ConvexMeshBuilder, wasm32:
  +0   ConvexPolygonsBuilder hullBuilder
  +44  Gu::ConvexHullData mHullData
  +108 ptr mBigConvexData
  +112 float mMass
  +116 PxMat33 mInertia
  sizeof = 152
```

这解释了 `func72927` 的读法：

```text
(f[7])[18]:ushort  -> ConvexHullData.mNbEdges, byte offset 36
(f[7])[38]:ubyte   -> ConvexHullData.mNbHullVertices
(f[7])[39]:ubyte   -> ConvexHullData.mNbPolygons

f[7]                -> ConvexMeshBuilder.hullBuilder.mHull
                       指向 builder + 44，也就是 builder.mHullData
f[27]               -> ConvexMeshBuilder.mBigConvexData
f[28]               -> ConvexMeshBuilder.mMass
f + 116             -> ConvexMeshBuilder.mInertia
```

`func72876 / f_ytcd` 是 `ConvexMeshBuilder` 构造 helper。它把 `hullBuilder.mHull` 设为 `a+44`，并把惯量矩阵初始化成单位阵。`4575657221408423936 = 0x3f80000000000000`，按小端解释就是两个 float：`0.0, 1.0`，正好对应 `mMass=0` 后接 identity inertia 的第一项。

也更正一个容易误读的点：`func72915` 里的

```text
b.g = 4
```

不是 `PxConvexMeshDesc.flags=4`，而是 `indices.stride = sizeof(PxU32)`。`PxConvexMeshDesc.flags` 在 byte offset 36；`func72915` 填的是 desc 的 `points/polygons/indices` 三个 `PxBoundedData`，也就是前 36 字节。

### `func72915` 的两条输出路径

`func72915 = QuickHullConvexHullLib::fillConvexMeshDesc()`，内部按是否存在 `mCropedConvexHull` 分两条路径。

**1. cropped hull 路径**

PhysX 源码：

```text
fillConvexMeshDescFromCroppedHull(outDesc)
  indicesOut  = mOutMemoryBuffer
  polygonsOut = mOutMemoryBuffer + indicesBufferSize
  vertsOut    = mOutMemoryBuffer + indicesBufferSize + facesBufferSize

  outDesc.indices  = { stride=4,  data=indicesOut,  count=numIndices }
  outDesc.points   = { stride=12, data=vertsOut,    count=numVertices }
  outDesc.polygons = { stride=20, data=polygonsOut, count=numPolygons }
  swapLargestFace(outDesc)
```

wasm 对应：

```text
a[9] != 0                       # mCropedConvexHull 存在
h = alloc(indices + polygons + vertices + 12)
l = h + indicesBufferSize       # polygonsOut
o = memcpy(l + facesBufferSize) # vertsOut

b.a/b.b/b.c = points.stride/data/count
b.d/b.e/b.f = polygons.stride/data/count
b.g/b.h/b.i = indices.stride/data/count
```

cropped hull 的 `edges` 会按 facet 分组；每个 facet 生成一个 `PxHullPolygon`，`plane` 来自 cropped facet，`mIndexBase` 指向 `indicesOut` 中该面的起点。随后 `swapLargestFace()` 把顶点数最多的面换到第 0 个 polygon，并重排 index buffer。

**2. 非 cropped QuickHull 路径**

`func72913 = fillConvexMeshDescFromQuickHull()`。它统计 visible faces 和 index 数，然后分配一个临时 buffer：

```text
indices           = base
vertices          = base + indicesBufferSize
polygons          = base + indicesBufferSize + verticesBufferSize
mFaceTranslateTable = base + indicesBufferSize + verticesBufferSize + facesBufferSize
translateTable    = base + indicesBufferSize + verticesBufferSize + facesBufferSize + faceTranslationTableSize
```

输出 desc：

```text
desc.points   = { stride=12, data=vertices, count=numVertices }
desc.indices  = { stride=4,  data=indices,  count=numIndices }
desc.polygons = { stride=20, data=polygons, count=numFacesOut }
```

这个路径同样把最大面写成第 0 个 polygon，并用 `mFaceTranslateTable` 记录输出 face 到 QuickHull 内部 face 的映射。这个顺序会继续影响 `createEdgeList()` 里的 edge/face 邻接表。

### runtime buffer 与 CLHL stream 顺序不同

`ConvexHullBuilder::copy()` 生成 runtime `Gu::ConvexHullData` 额外数据时，内存顺序是：

```text
mPolygons[nbPolygons]              # Gu::HullPolygonData, 20 bytes each
hullVertices[nbHullVertices]       # PxVec3, 12 bytes each
facesByEdges8[nbEdges * 2]         # 每条边相邻的两个面
facesByVertices8[nbHullVertices*3] # 每个顶点最多三个相邻面，用于 PCM
verticesByEdges16[nbEdges * 2]     # 只有 GRB bit set 时存在
vertexData8[sum polygon vertex counts]
```

但 `ConvexHullBuilder::save()` 写 `CLHL` cooked stream 时，顺序是：

```text
u32 nbHullVertices
u32 nbEdgesWithGrbBit
u32 nbPolygons
u32 nbVertexRefs
float hullVertices[nbHullVertices * 3]
Gu::HullPolygonData polygons[nbPolygons]
u8 vertexData8[nbVertexRefs]
u8 facesByEdges8[nbEdges * 2]
u8 facesByVertices8[nbHullVertices * 3]
u16 verticesByEdges16[nbEdges * 2] # 只有 GRB bit set 时存在
```

`func72927` 对应的是 stream 顺序，不是 runtime pointer 后面的内存顺序。后面如果解析 `CVXM/CLHL`，必须按 stream 顺序；如果从运行时 `ConvexHullData.mPolygons` 指针往后扫，则必须按 runtime buffer 顺序。

### GAUS / BigConvexRawData

当 hull 顶点数超过 `gaussMapLimit=32` 时，`ConvexMeshBuilder::build()` 会调用 `computeGaussMaps()`，`func72927` 会在 `CVXM` 中写出 `SUPM/GAUS/VALE`。32-bit 下：

```text
Gu::Valency:
  +0 u16 mCount
  +2 u16 mOffset
  sizeof = 4

Gu::BigConvexRawData:
  +0  u16 mSubdiv
  +2  u16 mNbSamples
  +4  ptr mSamples
  +8  u32 mNbVerts
  +12 u32 mNbAdjVerts
  +16 ptr mValencies
  +20 ptr mAdjacentVerts
  sizeof = 24
```

`GAUS` 不是另一套物理模型，而是大凸包 support vertex / hill-climbing 加速数据。GJK/PCM 查找 support point 时会使用它；因此如果真实 Unity cooked hull 顶点数大于 32，这个块也属于“要复刻”的几何输入。

### `func72878` / `func72926` 与质量属性

`func72926 = f_wvcd` 对应 `Cooking::cookConvexMeshInternal` 周围的 wrapper。它先做 `PxConvexMeshDesc::isValid()` 同构校验，然后：

```text
if desc.flags has eCOMPUTE_CONVEX:
  hullLib->createConvexHull()
  hullLib->fillConvexMeshDesc()

func72878 / f_aucd(
  ConvexMeshBuilder* builder,
  PxConvexMeshDesc* desc,
  gaussMapLimit=32,
  validateOnly=false,
  hullLib
)
```

`func72878` 对上 `ConvexMeshBuilder::build()`：

```text
loadConvexHull(desc, hullLib)
  gather points
  gather indices
  gather polygons
  hullBuilder.init(...)
  computeMassInfo(desc.flags & eFAST_INERTIA_COMPUTATION)

computeBoundsAroundVertices(...)
if mHullData.mNbHullVertices > gaussMapLimit:
  computeGaussMaps()
if !validateOnly:
  computeInternalObjects()
```

这点很重要：cooked hull 不只决定 contact generation 的 reference face、incident face、edge witness 和 support point；它还会进入 `computeMassInfo()`，产生 PhysX convex mesh 的单位密度质量、惯量张量和 local COM。除非 Unity 后面显式覆盖 Rigidbody inertia，否则“我们本地 hull 和 Unity cooked hull 不一致”会同时造成：

```text
1. 接触点/法线不一致；
2. solver 里 angular impulse 使用的 inertia 不一致；
3. 碰后角速度、旋转带来的二次接触误差继续放大。
```

### CVXM 整体写出顺序

`func72927` 对应 `ConvexMeshBuilder::save()` 这一路 cooked stream。忽略 `f_wazc/f_xazc` 写的 chunk header 后，payload 级顺序是：

```text
CVXM:
  u32 serialFlags = 0
  CLHL:
    u32 nbHullVertices
    u32 nbEdgesWithGrbBit
    u32 nbPolygons
    u32 nbVertexRefs
    float hullVertices[nbHullVertices * 3]
    Gu::HullPolygonData polygons[nbPolygons]
    u8 vertexData8[nbVertexRefs]
    u8 facesByEdges8[nbEdges * 2]
    u8 facesByVertices8[nbHullVertices * 3]
    u16 verticesByEdges16[nbEdges * 2]  # 只有 GRB bit set 时存在

  float zeroGeomEpsilon
  float boundsMin[3]
  float boundsMax[3]
  float mass
  float inertia[9]
  float centerOfMass[3]

  float gaussMapFlag
  if gaussMapFlag > 0:
    SUPM / GAUS:
      u32 subdiv
      u32 nbSamples
      u8 samples[nbSamples * 2]
      VALE:
        u32 nbVerts
        u32 nbAdjVerts
        u32 maxValencyCount
        compressed valencyCounts[nbVerts]  # StoreIndices；按 maxValencyCount 选择 8/16 bit
        u8 adjacentVerts[nbAdjVerts]

  float internal.radius
  float internal.extents[3]
```

工具输出里的 `CVXM cooked stream order` 是 payload-level sketch，不包含各 chunk header 的实际字节数；用于字段顺序校验，不可直接当文件绝对偏移。

## pyphysx 离线 dump

新增工具：

```powershell
D:\esp\tmp\curling_pyphysx_conda\python.exe tools\reverse\dump_pyphysx_cooked_convex_hull.py
```

脚本默认尝试匹配 Unity wasm 里恢复出的 flags：

```text
eCOMPUTE_CONVEX = on
eQUANTIZE_INPUT = off
eGPU_COMPATIBLE = off
vertexLimit = 255
quantizedCount = 255
```

2026-07-08 晚间已补齐本机 C++ 构建链，不需要重新安装 Visual Studio：

```text
已有:
  Visual Studio Community 2026
  cl.exe 19.50.35721
  MSBuild 18.0.5

新装:
  scoop install ninja  -> 1.13.2
  scoop install cmake  -> 4.3.4
```

随后用 `D:\esp\tmp\curling_pyphysx` 里的本地改动源码重编 wheel：

```powershell
cmd /v:on /c 'call D:\MicrosoftVisualStudio\18\Community\VC\Auxiliary\Build\vcvars64.bat >nul && set "PATH=D:\esp\tmp\curling_pyphysx_conda\Scripts;!PATH!" && D:\esp\tmp\curling_pyphysx_conda\python.exe -m pip wheel . -w dist --no-build-isolation --no-deps -v --config-settings=cmake.build-type=Release --config-settings=cmake.args="-G;Ninja"'

D:\esp\tmp\curling_pyphysx_conda\python.exe -m pip install --force-reinstall --no-deps D:\esp\tmp\curling_pyphysx\dist\pyphysx-0.2.5-cp38-cp38-win_amd64.whl
```

重编后的 docstring 已确认暴露：

```text
create_convex_mesh_from_points(...,
                               quantized_count=255,
                               vertex_limit=255,
                               quantize_input=True,
                               gpu_compatible=True)
```

随后继续扩展本地 binding，新增 `Shape.get_convex_mesh_data()`，直接从
`PxConvexMesh` 读出 raw vertices、polygons、index buffer、local bounds、
`isGpuCompatible()` 和 `getMassInformation()`。这比 `get_shape_data()` 的
渲染用 triangle soup 更接近 PhysX cooked hull 本体。

因此本机 pyphysx 已经可以跑 Unity recovered flags：

```powershell
D:\esp\tmp\curling_pyphysx_conda\python.exe tools\reverse\dump_pyphysx_cooked_convex_hull.py `
  --output data\calibration\pyphysx_cooked_stone_hull_probe_unity_flags_rebuilt_raw_20260708.json `
  --include-binding-default-control `
  --include-raw-convex-data
```

关键输出：

```text
detail variant = q255_v255_qi0_gpu0
input vertices = 512
raw PxConvexMesh vertices = 128
raw PxConvexMesh polygons = 66
raw polygon index_count = 384
polygon histogram = 2 faces with 64 vertices + 64 faces with 4 vertices
top/bottom vertices = 64 + 64
top angle step ~= 5.625 deg
rendered triangles from polygons = 252
local bounds = [-1.25, -1, -1.25] .. [1.25, 1, 1.25]
mesh scale = [1, 1, 1]
mesh scale rotation xyzw = [0, 0, 0, 1]
is_gpu_compatible = false
unit-density mass ~= 9.80171394
local COM ~= [9e-09, 2e-08, 7e-09]
local inertia rows ~= [
  [7.08988714, 0, 0],
  [0, 7.64529800, 0],
  [0, 0, 7.08988714]
]
world radial mean ~= 0.140875m
binding_flag_support = true
```

旧的非 raw 报告仍保留：

```text
data/calibration/pyphysx_cooked_stone_hull_probe_unity_flags_rebuilt_20260708.json
```

2026-07-08 进一步把 raw hull 转成 contact-relevant topology：

```powershell
python tools\reverse\analyze_pyphysx_raw_hull_topology.py
```

输出：

```text
data/calibration/pyphysx_raw_hull_topology_20260708.json

V = 128
F = 66
E = 192
V - E + F = 2

edge classes:
  top_ring = 64
  bottom_ring = 64
  vertical = 64

facesByEdges8 complete = true
facesByVertices8 complete = true
vertex face valency = 3 for all 128 vertices

runtime extra buffer = 4008 bytes
CLHL payload excluding chunk header = 4024 bytes
```

这个报告按 PhysX 4.1 `ConvexHullBuilder::createEdgeList()` / `calculateVertexMapTable()`
的结构重建了：

```text
vertexData8[384]
facesByEdges8[192 * 2]
facesByVertices8[128 * 3]
edgeData16_by_vertex_ref[384]  # builder 临时 face->edge 映射；非 GRB runtime 不写出
```

因此 topology 层现在可以说清楚：离线 raw hull 是一个 manifold convex hull，
每条边恰好两个邻接面，每个顶点恰好三个邻接面，PCM/convex-convex 需要的
`facesByEdges8` 和 `facesByVertices8` 都可从 raw polygon/index buffer 重建。
但如果要做 **字节级一致**，还要拿 formal stone 的 Unity `CLHL` stream 证明
face/edge 排序与本地重建顺序完全一致。

另一个关键数值：64 边棱柱的顶点半径与侧面 apothem 在世界尺度只差约
`0.000169705m`，也就是 `0.17mm`。所以当前碰撞中用 `0.146m` 补偿几何才略好
的现象，不能归因于“256 面被裁成 64 面造成有效半径少了几厘米”；这个离散化误差
本身太小。

2026-07-09 继续复刻 `BigConvexData` 的 `VALE/GAUS`：

```powershell
python tools\reverse\analyze_pyphysx_bigconvex_data.py
```

输出：

```text
data/calibration/pyphysx_bigconvex_data_20260709.json
```

触发条件：

```text
gaussMapLimit = 32
nbHullVertices = 128
128 > 32, so BigConvexData is required
```

`VALE` 结果：

```text
nbVerts = 128
nbAdjVerts = 384 = nbEdges * 2
maxValencyCount = 3
valency histogram = {3: 128}
compressed valency count bytes = 1 byte each
```

`GAUS` 结果：

```text
density/subdiv = 16
nbSamples = 6 * 16 * 16 = 1536
sample bytes = 3072
unique sampled support vertices = 120
brute-force support validation errors = 0
```

payload 尺寸，不含 `SUPM/GAUS/VALE` chunk header：

```text
GAUS = 3080 bytes   # u32 subdiv + u32 nbSamples + 3072 sample bytes
VALE = 524 bytes    # u32 nbVerts + u32 nbAdjVerts + u32 maxValencyCount
                    # + 128 one-byte valency counts + 384 adjacent verts
GAUS + VALE = 3604 bytes
```

这个脚本按 `BigConvexDataBuilder::computeValencies()` 与
`BigConvexDataBuilder::precompute(density=16)` 复刻。`GAUS` 的每个 min/max sample
都用 brute-force 点积重新检查：sample 指向的顶点确实是对应 cubemap 方向的 support
顶点。因此 `GAUS/VALE` 的**算法内容**现在已经不是黑箱。仍需 Unity formal-stone
`CVXM/SUPM/GAUS/VALE` stream 的原因，只是为了证明 face/edge/adjacent/sample 的
**字节级顺序**和本地复刻完全一致。

2026-07-09 继续把 raw hull 的单位密度质量/惯量按 PhysX 4.1 公式缩放到正式
Unity 尺度：

```powershell
python tools\reverse\analyze_pyphysx_scaled_mass_properties.py
```

输出：

```text
data/calibration/pyphysx_scaled_mass_properties_20260709.json
```

该脚本复刻的是 PhysX 源码中的三段：

```text
PxMassProperties(const PxGeometry&), eCONVEXMESH branch
PxMassProperties::scaleInertia(identity scaleRotation)
PxRigidBodyExt::setMassAndUpdateInertia(single mass)
```

也就是说，它不是用碰撞终点拟合出来的参数，而是从 raw `PxConvexMesh`
的 `getMassInformation()`、Unity shape scale 和 Rigidbody mass=19.1 推出来的
mass-space inertia。当前三组候选：

```text
raw mesh identity:
  radial ~= 13.8156291029
  vertical ~= 14.8979242530

Unity localScale=(0.115,0.115,0.115):
  radial ~= 0.182711694886
  vertical ~= 0.197025048246

Unity formal worldScale=(0.112700008,0.115,0.112700008):
  radial ~= 0.178810612362
  vertical ~= 0.189222883199
```

其中最后一组对应正式场景尺寸：

```text
radius_x/z ~= 1.25 * 0.112700008 = 0.14087501m
height_y   ~= 2.0  * 0.115       = 0.23m
```

接入现有 z-up `probe_physx_collision_alignment.py` 时，参数应写成：

```text
--radius 0.14087501 --height 0.23 --inertia-model custom \
--inertia-radial 0.178810612362 --inertia-vertical 0.189222883199
```

这里的轴约定需要注意：raw Unity mesh 是 `x/z` 水平径向、`y` 竖直；现有 probe
构造的是 z-up 石壶，所以要把 raw mesh 的 `diag_x/diag_z` 平均值传给
`inertia_radial`，把 raw mesh 的 `diag_y` 传给 `inertia_vertical`。

保留的 binding 默认对照：

```text
data/calibration/unity_physx_collision_probe_unique_role_current_best_rebuilt_binding_default_control_20260708.json

运行参数:
--quantize-input --gpu-compatible

detail variant = q255_v255_qi1_gpu1
cooked unique vertices = 64
cooked triangles = 124
```

这个对照只说明一件事：`qi1/gpu1` 会把石壶 cooked hull 压到 64 个唯一顶点。它不是 Unity 真值，因为 Unity wasm 已确认 `eQUANTIZE_INPUT` 和 `eGPU_COMPATIBLE` 都没有开启。

重编后也同步更新了 `tools/reverse/probe_physx_collision_alignment.py`：默认路径会传
`quantize_input=false / gpu_compatible=false`，只有显式加

```text
--quantize-input --gpu-compatible
```

才跑旧控制组。

用既有 unique-role 样本做定向 replay 后，结果如下：

```text
旧 current_best 几何 + rebuilt Unity flags:
  data/calibration/unity_physx_collision_probe_unique_role_current_best_rebuilt_unityflags_20260708.json
  active RMSE ~= 3.86cm
  target RMSE ~= 11.32cm

旧 current_best 几何 + binding 默认 qi1/gpu1:
  data/calibration/unity_physx_collision_probe_unique_role_current_best_rebuilt_binding_default_control_20260708.json
  active RMSE ~= 3.78cm
  target RMSE ~= 10.80cm

formal radius=0.140875m + rebuilt Unity flags + handoff threshold 对齐到 0.292m:
  data/calibration/unity_physx_collision_probe_unique_role_formal_geometry_rebuilt_unityflags_handoff292_20260708.json
  active RMSE ~= 3.20cm
  target RMSE ~= 12.08cm

formal radius=0.14087501m + rebuilt Unity flags + PhysX 推导 cooked-hull inertia:
  data/calibration/unity_physx_collision_probe_unique_role_formal_geometry_cooked_inertia_20260709.json
  active RMSE ~= 3.33cm
  target RMSE ~= 12.65cm
```

所以 pyphysx binding 已经不是当前阻塞点。新的交底是：formal source mesh 和 Unity flags 可以离线 cook 出 `128 vertices / 66 polygons / 384 polygon indices / 252 rendered triangles` 的 raw `PxConvexMesh`，结构上就是 `64` 面棱柱：两个 64 边 cap 加 64 个侧面四边形；其 contact topology 为 `192` 条 unique edges，`facesByEdges8/facesByVertices8` 都能重建且自洽；`BigConvexData` 的 `VALE/GAUS` 也能离线复刻并通过 support 校验；world-scale cooked-hull inertia 也能由 PhysX `scaleInertia` 推出 `radial=0.178810612362 / vertical=0.189222883199`，且定向 replay 已证明单独替换这组惯量不会把 target 误差压下去。直接把 formal 半径接进现有 probe 没有把碰撞压到 2cm，反而说明 **Unity runtime shape scale/local pose/contact handoff、Unity 实际 cooked stream 的字节级顺序是否与离线 PhysX 4.1 完全一致** 仍有未对齐项。

## 当前未知

已经从未知项里移出的结论：

```text
1. Unity 运行时生成的石壶 MeshCollider 继承默认 m_CookingOptions=30。
2. m_CookingOptions=30 在 Unity C# 枚举层等于 2+4+8+16。
3. m_CookingOptions 会被 func72950 实际传入 shape/cooked mesh 创建入口，不是无效字段。
4. Unity convex 分支的 PxConvexMeshDesc flags 只有 eCOMPUTE_CONVEX。
5. 石壶 runtime MeshCollider 没有启用 eQUANTIZE_INPUT。
6. 石壶 runtime MeshCollider 没有启用 eGPU_COMPATIBLE。
7. vertexLimit=255，quantizedCount=255，buildGPUData=false。
8. 重编后的 pyphysx binding 已能传 `quantize_input=false/gpu_compatible=false`；formal source mesh 在该路径下得到 `128 vertices / 66 polygons / 384 polygon indices / 252 rendered triangles` 的 raw `PxConvexMesh` dump，并已导出单位密度 mass/inertia/local COM。
9. `func72915` 填的是 `PxConvexMeshDesc.points/polygons/indices`；其中 `b.g=4` 是 `indices.stride=4`，不是 flags。
10. `func72927` 的 `CLHL` 头部和 `ConvexHullData` 计数字段已经对上：`mNbEdges` byte offset 36，`mNbHullVertices` byte offset 38，`mNbPolygons` byte offset 39。
11. runtime `ConvexHullData` 后续 buffer 顺序与 `CLHL` cooked stream 顺序不同，解析时不能混用。
12. `ConvexMeshBuilder` wasm32 布局已对上：`mHullData` offset 44，`mBigConvexData` offset 108，`mMass` offset 112，`mInertia` offset 116。
13. `func72878` 会在 `loadConvexHull()` 内调用 `computeMassInfo()`；cooked hull 数值会影响单位密度质量、惯量和 local COM。
14. `func72927` 的 `CVXM` payload 顺序已对上 `ConvexMeshBuilder::save()`：`CLHL -> bounds -> mass/inertia/COM -> GAUS flag/SUPM/GAUS/VALE -> internal objects`。
15. runtime `MeshCollider.sharedMesh/convex` rebuild 已确认会触发 attached Rigidbody
    的 mass-properties sync：slot[37] 是 `func72951`，convex 分支走 `func73283`，
    并调用 `f_abdd(e)`；`f_abdd` 会在 `m_ImplicitTensor=true` 时调用
    `f_eqcd / PxRigidBodyExt::setMassAndUpdateInertia`。
16. `func72908/createConvexHull` 到 `func72910/expandHullOBB` 再到
    `func72915/fillConvexMeshDesc` 的 wasm 分支已由
    `tools/reverse/summarize_physx_cropped_hull_path.py` 固化：非
    `ePLANE_SHIFTING` 下走 `f_gvcd`，`f_gvcd` 最终写 `a[9]=c`，
    `f_lvcd` 在 `a[9]!=0` 时走 cropped hull desc 输出。
17. Unity cooked hull 的 desc 级导出机制已经由运行时 hook 验证：
    `func72915/f_lvcd` 的 wasm table index 为 `122108`，返回后读第二参数
    `PxConvexMeshDesc.points/polygons/indices` 三组 `PxBoundedData`。
    本次四局制等待页日志为 `log/unity_runtime_probe_20260708_225950`，
    稳定导出文件为 `data/calibration/unity_cooked_hulls_20260708_225950.json`。
18. `tools/reverse/analyze_cooked_hull_identity.py` 已把本次等待页抓到的
    `1_0/2_0/3_0/4_0` 和 formal stone `ExtendedColliders3D` 尺寸作比对：
    正式石壶期望 sorted extents 约 `(0.230000, 0.281750, 0.281750)`，
    而 `1_0` hull 为 `(0.083596, 0.159256, 0.159977)`，最大相对误差约
    `0.637`。因此这批 hull 不能视作正式比赛石壶 cooked hull。
19. binding 默认 `qi1/gpu1` 控制组仍为 `64 vertices / 124 triangles`，只用于证明旧结果不是 Unity flags 真值。
20. `tools/reverse/summarize_formal_stone_cooking_status.py` 已把 formal stone
    当前 cooking 状态固化到 `data/calibration/formal_stone_cooking_status_20260708.json`：
    formal mesh 为 `512` 个 unique vertices、`1020` 个 triangles，世界 sorted extents
    为 `(0.230000, 0.281750, 0.281750)`，`512` 个 support-extreme vertices
    超过 `vertexLimit=255`，因此必须走 cropped path。rebuilt pyphysx raw 报告
    为 `128 vertices / 66 polygons / 384 polygon indices`，polygon 直方图是
    `64:2, 4:64`，即两个 64 边 cap 加 64 个侧面四边形。当前阻塞点不是输入、
    flags 或 pyphysx binding，而是正式 Unity runtime shape 的 scale/local pose、
    Unity cooked stream 的 byte-level face/edge/GAUS/VALE 顺序是否与离线
    PhysX 4.1 复刻完全一致。
21. `tools/reverse/analyze_pyphysx_raw_hull_topology.py` 已从 raw `PxConvexMesh`
    重建 contact topology：`V=128, F=66, E=192, V-E+F=2`，
    edge 类型为 `top_ring=64, bottom_ring=64, vertical=64`，
    `facesByEdges8[384]` 和 `facesByVertices8[384]` 都完整，每个顶点邻接
    3 个 face。runtime extra buffer 预计 `4008` bytes，`CLHL` payload
    不含 chunk header 为 `4024` bytes。64 边棱柱的世界顶点半径与侧面
    apothem 只差 `0.17mm`，不能解释厘米级碰撞半径补偿。
22. `tools/reverse/analyze_pyphysx_bigconvex_data.py` 已按 PhysX 4.1 源码复刻
    formal stone 离线 raw hull 的 `BigConvexData`：因为 `128 > gaussMapLimit=32`，
    `mBigConvexData` 必须存在；`VALE` 为 `128` 个顶点、`384` 个 adjacent verts、
    所有顶点 valency 都是 `3`；`GAUS` 为 `subdiv=16`、`nbSamples=1536`、
    `3072` 个 sample byte。所有 cubemap sample 均通过 brute-force support
    校验，说明 `VALE/GAUS` 的算法内容可离线复刻。
23. `tools/reverse/analyze_pyphysx_scaled_mass_properties.py` 已按 PhysX 4.1
    `PxMassProperties::scaleInertia` 和
    `PxRigidBodyExt::setMassAndUpdateInertia(single mass)` 把 raw hull 的单位密度
    mass/inertia 缩放到 Unity 正式 world scale。推荐接入现有 z-up probe 的参数为
    `--inertia-radial 0.178810612362 --inertia-vertical 0.189222883199`。
    这组数是从 cooked hull 和 Rigidbody mass=19.1 推导，不是 endpoint 拟合。
```

还没有完全钉死的项：

```text
1. 正式比赛石壶 `ExtendedColliders3D` 生成的 MeshCollider cooked hull 还没有从
   Unity runtime 直接导出；等待页 `1_0/2_0/3_0/4_0` 和 `base_link_*`
   几何经尺寸判据排除，不可当作 stone collision hull。
2. pyphysx 离线 raw dump 已给出 `128 vertices / 66 polygons / 384 polygon indices`
   以及单位密度 mass/inertia/local COM；topology 层也已给出 `192` 条 unique edges
   和完整 `facesByEdges8/facesByVertices8`；world-scale mass-space inertia 也已按
   PhysX 公式推出。但它仍是本地 PhysX 4.1 对 formal mesh 的离线复刻，还没有证明
   Unity runtime formal stone 的 cooked hull/CLHL 顺序与它逐项一致。shape local pose、
   runtime scale、contact handoff 仍需核对。
3. `func72927` cooked stream 写出位置已定位，但还没有完整导出并解析 formal stone
   的 `CVXM/CLHL/SUPM/GAUS/VALE` stream；因此 byte-level face/edge ordering、
   adjacent/sample ordering 还需要用 Unity formal stream 证明。
4. Unity Rigidbody 的 COM 已由 `CurlingStoneNew.Start` 显式写成 `Vector3.zero`，并且
   native `set_centerOfMass` 会把 `m_ImplicitCom`（native offset `a[85]`）清 0；
   COM 不应再视为 cooked hull 自动值。`m_ImplicitTensor`（native offset `a[100]`）
   已从 `func73082/73083/73084` 字段名和资源抽取中确认：正式石壶资源为 true，
   业务层也没有 `set_inertiaTensor*` 把它关掉。rebuild 触发 `f_abdd /
   PxRigidBodyExt::setMassAndUpdateInertia` 也已经确认；在 world-scale formal hull
   假设下，最终 tensor 已由 `analyze_pyphysx_scaled_mass_properties.py` 给出。惯量侧
   剩余未知不再是公式，而是 Unity runtime shape wrapper 是否确实等于该 world-scale
   formal hull。
5. Unity 是否在 cooked convex mesh 创建后还有额外缓存、scale 烘焙或 shape geometry
   包装细节影响 contact。当前碰撞 probe 用 formal `0.140875m` 半径反而比旧
   `0.146m` 补偿几何更差，说明这个 scale/contact 半径问题必须继续追。
```

其中第 2/3 项最影响碰撞对齐。contact generation 和 solver 公式已经挖得很深；现在离线 hull/topology/BigConvexData/mass-inertia 算法内容都已复刻，剩下要证明的是 Unity runtime 里 formal stone 的 shape 包装和 cooked stream 顺序是否完全一致。

## 下一步路线

优先级按“能减少结构性未知”的强度排序：

1. **拿到正式石壶 runtime shape 封装，而不是只拿 triangle dump**
   现在 flags 和 desc 级几何都已明确：`eCOMPUTE_CONVEX`、
   `vertexLimit=255`、`quantizedCount=255`、`buildGPUData=false`、
   `eQUANTIZE_INPUT=false`、`eGPU_COMPATIBLE=false`，且运行时 hook 已验证能导出
   `vertices / polygons / planes / indices`。但等待页抓到的 `1_0/99点/base_link`
   不是 formal stone 尺寸。pyphysx 离线结果已经给出 Unity flags 下的
   `128 vertices / 66 polygons / 384 polygon indices / 252 rendered triangles`
   对照，topology 也已重建到 `192` 条 unique edges 和完整
   `facesByEdges8/facesByVertices8`，`VALE/GAUS` 也已按源码复刻并通过 support
   校验；下一步不是再蒙 hull 参数，而是确认 `ExtendedColliders3D` formal stone
   在 Unity runtime 中的 shape scale/local pose、runtime cooked stream 字节顺序
   是否逐项匹配这份离线 `PxConvexMesh`，并把已推导出的 automatic inertia/tensor
   接入 probe 做验证。

   当前离线状态报告：

   ```powershell
   python tools\reverse\summarize_formal_stone_cooking_status.py
   ```

   输出：

   ```text
   data/calibration/formal_stone_cooking_status_20260708.json
   ```

   这个报告把 formal stone mesh 512 个极点、Unity flags、rebuilt pyphysx
   `qi0/gpu0` 的 128 顶点/66 面 raw hull、192 边 contact topology、
   VALE/GAUS support 数据、world-scale cooked-hull inertia，以及碰撞 probe 的
   剩余误差放在同一个状态表里。

2. **Unity wasm 侧继续拆 cooked stream / shape 创建输出**
   目标从“导出 cropped hull”改为“补全 shape 包装和 cooked stream 细节”。两条具体路线：

   ```text
   A. hook MeshCollider/PxShape 创建附近，记录 shape local pose、scale、material、filter data。
   B. 在 func72927 / ConvexMeshBuilder::save 附近导出 CVXM/CLHL bytes 后离线解析，
      校验 byte-level edge/face ordering、vertexData、GAUS/SUPM/VALE 顺序和最终
      mass/inertia 相关数据。
   ```

   现在离线 `PxConvexMesh` raw 数据、topology、BigConvexData 和 mass/inertia 已拿到，
   `func72915` desc 导出链路也已验证；差的是 formal stone 那次 Unity runtime 调用、
   shape 层封装，以及更晚 cooked stream 的 byte-level 内部数据。

3. **把 cooked hull 和自动惯量接入碰撞 probe**
   只有拿到 formal stone cooked hull 后，才能替换当前
   `probe_physx_collision_alignment.py` 里的理想圆柱/半径近似；在确认 shape transform 后，
   再重跑已有 unique-role / four-game collision replay。若 target RMSE 明显下降，说明误差主因就是 hull cooking/compound shape；若仍不降，再继续追 contact cache、solver warm start 和首次 contact manifold。2026-07-09 的 managed material timing 小网格已弱化为非主因。

4. **只做定向验证，不做大采样**
   当前不需要重新采样。只有当 cooked hull、质量/惯量或 shape 包装出现无法从 wasm/PhysX 源码判断的二选一问题时，才做极少量定向采样或运行时注入验证。
