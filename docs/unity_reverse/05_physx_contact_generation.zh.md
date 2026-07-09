# PhysX 接触点生成

记录 PhysX 4.1 对照下的 convex-convex、convex-mesh、triangle SAT、contact cache、reduction 和 ContactBuffer。

> 原长文档已封存：[`UNITY_REVERSE_ENGINEERING.zh.2026-07-07.archive.md`](../archive/UNITY_REVERSE_ENGINEERING.zh.2026-07-07.archive.md)。以后维护以本目录子文档为准。

## PhysX 4.1 源码交叉定位

我把 NVIDIA PhysX `4.1` 源码浅克隆到临时目录，对照了 wasm 里的函数表和反编译体：

```text
%TEMP%/PhysX-4.1-source
branch: 4.1
commit: a2c0428acab643e60618c681b501e86f7fd558cc
```

关键源码位置：

```text
physx/include/PxSceneDesc.h
physx/source/lowleveldynamics/src/DyDynamics.cpp
physx/source/lowleveldynamics/src/DyContactPrep.cpp
physx/source/lowleveldynamics/src/DyContactPrep4.cpp
physx/source/lowleveldynamics/src/DyContactPrepPF.cpp
physx/source/lowleveldynamics/src/DyContactPrep4PF.cpp
physx/source/lowleveldynamics/src/DyFrictionCorrelation.cpp
physx/source/lowlevel/common/src/pipeline/PxcContactMethodImpl.cpp
```

这次一个重要修正是：之前看到的 `4118616/4118628` 不是 narrowphase shape contact
generator 表，而是 `createFinalizeContacts_Parallel` 里按 `frictionType` 选择的
contact constraint finalization 表。

`build.wat` data table 解析结果：

```text
createFinalizeMethods4[frictionType]  // 4 个 contact pair 的 batched path
  address 4118616
  [0] func70963 = createFinalizeSolverContacts4
  [1] func71107 = createFinalizeSolverContacts4Coulomb1D wrapper
  [2] func71109 = createFinalizeSolverContacts4Coulomb2D wrapper

createFinalizeMethods[frictionType]   // 单 pair fallback path
  address 4118628
  [0] func71103 = createFinalizeSolverContacts
  [1] func70964 = createFinalizeSolverContactsCoulomb1D wrapper
  [2] func70966 = createFinalizeSolverContactsCoulomb2D wrapper
```

Unity 资源里的 `PhysicsManager.frictionType = 0`，而 PhysX `PxFrictionType` 的枚举顺序为：

```text
0 = ePATCH
1 = eONE_DIRECTIONAL
2 = eTWO_DIRECTIONAL
```

所以正式比赛碰撞最终走的是默认 patch friction：

```text
4-pair batch: func70963 / createFinalizeSolverContacts4
single pair:  func71103 / createFinalizeSolverContacts
```

`func71107/func71109/func70964/func70966` 这些 Coulomb 1D/2D wrapper 编进了 wasm，
但当前工程配置不会选它们；不能把它们当作正式比赛路径。

结合资产中的 collider 类型、`PxsContext.contactManagerDiscreteUpdate` 的反编译体和
PhysX `PxcContactMethodImpl.cpp`，已经把真正的 narrowphase function table 定位出来。
`func70739` 中的两处表访问是：

```text
legacy contact table:
  address 4117760
  expression: (type0 * 28 + type1 * 4 + 4117760)[0]

PCM contact table:
  address 4117968
  expression: (type0 * 28 + type1 * 4 + 4117968)[0]

material method table:
  address 4118208
  expression: (type0 * 28 + type1 * 4 + 4118208)[0]
```

其中 `28 = 7 * 4`，对应 PhysX 的 7 种 `PxGeometryType`：

```text
0 SPHERE
1 PLANE
2 CAPSULE
3 BOX
4 CONVEXMESH
5 TRIANGLEMESH
6 HEIGHTFIELD
```

用 `tools/reverse/find_physx_pcm_contact_table.py` 可以复现：

```powershell
D:\anaconda3\python.exe tools\reverse\find_physx_pcm_contact_table.py `
  $env:TEMP\curling_reverse_il2cpp\build.wat `
  $env:TEMP\curling_reverse_il2cpp\wasm_table_map.json `
  --min-func 70000 --max-func 70600 --min-score 130 `
  --address-min 4117600 --address-max 4118300
```

为了日常核对冰壶相关路径，新增了更窄的摘要工具：

```powershell
D:\esp\tmp\curling_pyphysx_conda\python.exe tools\reverse\summarize_physx_contact_paths.py
```

当前输出的关键项：

```text
Unity relevant choice:
  contactsGeneration=1 -> pcm_contact
  frictionType=0 -> patch

stone_vs_stone:
  CONVEXMESH x CONVEXMESH
  pcm_contact    = 120118 $f70576 func70576
  legacy_contact = 120100 $f70558 func70558
  material       = 120123 $f70594 func70594

stone_vs_rink_mesh:
  CONVEXMESH x TRIANGLEMESH
  pcm_contact    = 120119 $f70577 func70577
  legacy_contact = 120101 $f70559 func70559
  material       = 120124 $f70592 func70592

stone_vs_wall_box:
  BOX x CONVEXMESH
  pcm_contact    = 120116 $f70574 func70574
  legacy_contact = 120098 $f70556 func70556
  material       = 120123 $f70594 func70594
```

`func70739` 也能直接证明表选择逻辑：`contactsGeneration` 非零时查 `4117968`
的 PCM 表；非 PCM 分支才查 `4117760` 的 legacy 表。资源里 `PhysicsManager.contactsGeneration=1`，
所以正式比赛石壶不走 legacy `func70558/70559/70556`，而是走 PCM
`func70576/70577/70574`。

注意：本地 `pyphysx.Scene(scene_flags=[])` 不是“禁用 PCM”。pyphysx 的 `Scene` 构造从
`PxSceneDesc` 默认值开始，而 PhysX 4.1 的默认 `PxSceneDesc.flags` 已包含
`eENABLE_PCM`。因此当前 pyphysx 碰撞 probe 的主要结构性偏差不是 PCM 开关，而是
convex cooking binding 不能传入 Unity 已恢复的 `quantize_input=false / gpu_compatible=false`。

扫描会同时找出 legacy 表 `4117760` 和 PCM 表 `4117968`，两者都是 PhysX 源码表形状的满分匹配。
`g_PCMContactMethodTable` 的关键行如下：

```text
stone vs stone
  convex MeshCollider vs convex MeshCollider
  -> PxcPCMContactConvexConvex
  -> table[CONVEXMESH][CONVEXMESH] = 120118 $f70576 = func70576

stone vs rink Plane
  convex MeshCollider vs static MeshCollider / triangle mesh
  -> PxcPCMContactConvexMesh
  -> table[CONVEXMESH][TRIANGLEMESH] = 120119 $f70577 = func70577
  注意不是 PxcPCMContactPlaneConvex

stone vs wall
  convex MeshCollider vs BoxCollider
  -> PxcPCMContactBoxConvex
  -> table[BOX][CONVEXMESH] = 120116 $f70574 = func70574

stone vs Midline/Hogline
  BoxCollider trigger
  -> OnTriggerEnter 规则路径，不产生普通碰撞约束
```

这次还确认了 `PxcInvalidContactPair` 在这个 build 中是 `func70548`。PhysX 源码里
`DYNAMIC_CONTACT_REGISTRATION(x)` 静态展开为 `PxcInvalidContactPair`，所以 heightfield
相关项在静态表中也是 `func70548`，不是实际 heightfield 接触函数；这解释了为什么一开始按
heightfield contact function 去扫表会失败。

抽取后的函数规模：

```text
func70574 = PxcPCMContactBoxConvex / pcmContactBoxConvex path       // 680 行
func70576 = PxcPCMContactConvexConvex / pcmContactConvexConvex path // 1599 行
func70577 = PxcPCMContactConvexMesh wrapper                         // 115 行
func70030 = Gu::PCMContactConvexMesh shared mesh midphase body      // 218 行
func70548 = PxcInvalidContactPair                                  // 4 行
func70594 = ordinary material method                               // 14 行
func70592 = mesh material method                                   // 26 行
```

`func70577` 内部会设置 convex/mesh scaling、AABB、PCM margin，然后调用 `func70030`
继续处理 `Gu::PCMContactConvexMesh(...)`；这和 PhysX 4.1 的
`GuPCMContactConvexMesh.cpp` 对应。`func70574/func70576` 中能看到和 PhysX 源码一致的
PCM 结构：`CalculatePCM...Margin`、`projectBreakingThreshold = minMargin * 0.8`、
`refreshContactPoints(...)`、`invalidate_BoxConvex(...)`、GJK/EPA 接触生成，以及
`0.999775` 这类法线相似度阈值。

## contactDistance / restDistance

`PxcNpBatch.cpp::checkContactsMustBeGenerated(...)` 已确认 narrowphase 传入 contact
generator 的距离参数为两边 per-shape contact distance 之和：

```text
context.mNarrowPhaseParams.mContactDistance =
  context.mContactDistance[shape0TransformCache] +
  context.mContactDistance[shape1TransformCache]
```

而 `ScShapeSim::updateContactDistance(...)` 中每个 shape 的值是：

```text
contactDistance[index] = getContactOffset() + inflation + angularInflation
angularInflation = |angularVelocity| * dt * boundsRadius
```

当前正式比赛石壶资源显示 `collisionDetection=0`，也就是没有证据走 CCD / speculative CCD
主路径；因此常规 stone-stone 接触的主项就是两边 `contactOffset` 相加。全局
`defaultContactOffset=0.01` 时，stone-stone 的接触提前量主项约为 `0.02m`。如果本地
probe 改 `contact_offset`，实际是在改 `mContactDistance`，从而改变 GJK/EPA/SAT
什么时候开始生成 contact。

`restDistance` 是另一条低层输入：`ScShapeInteraction` 会把两边 `restOffset` 相加后写入
contact manager。当前资源和 probe 默认都按 `restOffset=0` 处理，所以它不是现有
10cm 级误差的首要嫌疑；但如果后续发现 Unity shape 包装层改了 restOffset，它会进入
solver 的 penetration/bias 项，而不是改变 contact generator 的表选择。

继续往下拆后，shape contact generator 的内部 helper 已经能对到 PhysX 源码层级：

```text
func70532
  BoxConvex 的 fullContactsGenerationBoxConvex 主体。
  对应 GuPCMContactBoxConvex.cpp 调用的 fullContactsGenerationBoxConvex(...)
  以及 GuPCMContactGenBoxConvex.cpp 里的 generateFullContactManifold(...)。

func70533
  ConvexConvex 的 generateOrProcessContactsConvexConvex/fullContactsGenerationConvexConvex 主体。
  对应 GuPCMContactConvexConvex.cpp 的 generateOrProcessContactsConvexConvex(...)
  与 fullContactsGenerationConvexConvex(...)。

func70517
  按 feature type 计算/插值 contact point。
  `br_table(g - 1)` 分支对应点、边、三角形/多边形等 feature。

func70518 / func69905
  边-边、三角形/多边形裁剪和退化 fallback。
  源码层面对应 generateFullContactManifold(...) 里 SAT/face/edge 路径下的
  witness feature 选择与 generatedContacts(...) 相关逻辑。

func70525
  support/witness polygon index 查询。
  反编译里会在 hull face normal 数组上做最大 dot product；有 scale/特殊路径时转到 func70527。
```

`func70532/func70533` 里能看到源码里的核心判据：

```text
replaceBreakingThreshold = minMargin * 0.05
fullContactGen = dot(oldLocalNormal, output.normal) < 0.707106781 或 contact 数减少
doOverlapTest = GJK/EPA 退化时切到 SAT/overlap fallback
法线相似度阈值约 0.999775
```

这说明石头-石头、石头-墙这两类碰撞的接触点生成不是简单二维刚体碰撞，而是：

```text
PersistentContactManifold refresh
  -> GJK penetration
  -> 必要时 EPA penetration
  -> GJK/EPA 退化时 SAT overlap / face-edge fallback
  -> 根据 witness face/edge 生成 full contact manifold
  -> reduce/add batch manifold contacts
  -> 写入 ContactBuffer
```

stone-stone 的 `pcmContactConvexConvex` 主路径现在可以明确写成：

```text
pcmContactConvexConvex(shapeConvex0, shapeConvex1)
  -> 读取两个 PxConvexMeshGeometryLL 的 hullData / scale
  -> contactDist = params.mContactDistance
  -> curRTrans = transform1^-1 * transform0
  -> convexMargin0/1 = CalculatePCMConvexMargin(...)
  -> minMargin = min(convexMargin0, convexMargin1)
  -> projectBreakingThreshold = minMargin * 0.8
  -> manifold.refreshContactPoints(aToB, projectBreakingThreshold, contactDist)
  -> 如果 contact 丢失，或 manifold.invalidate_BoxConvex(...):
       manifold.setRelativeTransform(...)
       构造 ConvexHullV / SupportLocal
       gjkPenetration(...)
       generateOrProcessContactsConvexConvex(...)
     否则:
       worldNormal = manifold.getWorldNormal(transform1)
       manifold.addManifoldContactsToContactBuffer(...)
```

`generateOrProcessContactsConvexConvex(...)` 里已经对上的关键分支是：

```text
GJK_NON_INTERSECT:
  返回 false，没有 contact。

GJK_CONTACT:
  addManifoldPoint(...)，加入一个 GJK witness contact。

EPA_CONTACT:
  epaPenetration(...)，成功则加入 penetration contact。

GJK_DEGENERATE 或 EPA 失败:
  doOverlapTest = true，切到 SAT / full contact generation。

fullContactGen:
  old normal 与新 normal 夹角过大，阈值 dot < 0.707106781；
  或 refresh 后 contact 数少于 initialContacts。
```

full contact generation 不是只取一个最近点，而是先用 `testFaceNormal(...)`
检查两边 polyData 的 face normal，再必要时用 `testEdgeNormal(...)` 做 edge axis。
最终根据 `POLYDATA0 / POLYDATA1 / EDGE` 选择 reference polygon 和 incident polygon，
调用 `generatedContacts(...)` 做裁剪，并把 contact 翻转到统一方向后进入
`addBatchManifoldContacts(...)`。这意味着 stone-stone 的碰撞接触点同样依赖 hull face、
edge witness、上一帧 manifold cache 和 contact reduction，而不是一个固定“圆盘撞圆盘”
闭式结果。

继续对照 `GuPCMContactGenBoxConvex.cpp` 后，`generateFullContactManifold(...)`
的候选点生成规则已经可以写到源码级：

```text
testFaceNormal(polyData0, polyData1)
  -> 遍历 polyData0 的所有 polygon plane
  -> 把 face normal 变换到另一 shape 空间
  -> 分别把两个 convex 投影到该轴
  -> 若 min1 > max0 + contactDist 或 min0 > max1 + contactDist:
       该轴是 separating axis，返回 false
  -> 否则按 overlap 更新最小穿透轴、feature index 和 POLYDATA0/POLYDATA1 状态

testEdgeNormal(polyData0, polyData1)
  -> 先用 buildPartialHull(...) 在互相 support point 附近裁出候选边
  -> 对两边候选边两两做 cross product，得到 edge-edge SAT axis
  -> 跳过近零轴
  -> 用同样的 projection/contactDist 规则判断分离或更新最小穿透轴
  -> 若 edge axis 更优，则状态变成 EDGE
```

`generateFullContactManifold(...)` 有两条主路径：

```text
doOverlapTest = true:
  先跑两次 testFaceNormal，分别测试 A 的面法线和 B 的面法线。
  初始不一定跑 edge test；如果 face 路径生成不出 contact，再 retry testEdgeNormal。
  按 POLYDATA0 / POLYDATA1 / EDGE 选择 reference/incident face。

doOverlapTest = false:
  由 GJK/EPA 输出的 normal 与 closest point 选 witness polygon。
  tolerance = clamp(margin, toleranceLength * 1e-2, toleranceLength * 5e-2)
  调用 getWitnessPolygonIndex(...) 分别找两边最合适的 face。
  比较 reference face normal 与 incident face normal 谁更贴近接触法线，
  再决定哪边当 reference，必要时翻转 contact。
```

`generatedContacts(...)` 本身是 reference polygon 对 incident polygon 的裁剪。
它先构造一个把接触法线当作 Z 轴的局部坐标系，把两个多边形投影到 reference face 的
2D 平面，然后生成三类候选 contact：

```text
1. incident vertices inside reference polygon
   incident 顶点变到 reference plane；
   若 z < referenceDistance + contactDist 且 2D 点在 reference polygon 内：
     localPointA = incident 顶点
     localPointB = incident 顶点沿 contact normal 投影到 reference face
     localNormalPen = (contactNormal, z - referenceDistance)

2. reference vertices inside incident polygon
   reference 顶点沿 contact normal 投影到 incident plane；
   若投影距离 t <= contactDist 且 2D 点在 incident polygon 内：
     localPointA = 投影到 incident face 的点
     localPointB = reference 顶点
     localNormalPen = (contactNormal, t)

3. reference edge 与 incident edge 的 2D 线段交点
   用 signed2DTriArea(...) 判断两条 2D 线段相交；
   交点再插值回 3D；
   若 penetration <= contactDist，则加入候选 contact。
```

`contains(...)` 使用 XY 平面的 ray crossing 判断点是否在多边形内，并带 bounding min/max
提前排除；`signed2DTriArea(...)` 是线段相交和插值参数的核心小函数。
因此 contact 候选点的来源已经不是未知：它来自 face-vertex、vertex-face、
edge-edge 三类裁剪结果。剩下的工程难点是把这套通用 convex hull 裁剪、scale、
contact reduction 和 manifold cache 完整翻成我们自己的本地实现。

石头-冰面三角网格路径也进一步收窄了：

```text
func70030 = Gu::PCMContactConvexMesh(...)
  -> 设置 convexTransform / meshTransform
  -> multiManifold.invalidate(curTransform, minMargin)
  -> replaceBreakingThreshold = minMargin * 0.05
  -> computeHullOBB(...)
  -> Midphase::intersectOBB(meshData, hullOBB, callback, true)
  -> flushCache()
  -> generateLastContacts()
  -> processContacts(GU_SINGLE_MANIFOLD_CACHE_SIZE, false)
  -> addManifoldContactsToContactBuffer(...)

func70050
  初始化 PCMConvexVsMeshContactGenerationCallback / contact generation state。

func70056
  每个 triangle 的 processTriangle 路径。
  对应 PCMConvexVsMeshContactGeneration::processTriangle(...)：
  triangle 顶点变到 convex local space，计算三角形法线，背面剔除，
  再调用 generateTriangleFullContactManifold(...)。

func70054
  flushCache / generateLastContacts 类路径，把延迟的边/顶点/三角形接触刷新出来。

func70051
  MultiplePersistentContactManifold::addManifoldContactPoints / processContacts 类路径。
  反编译中反复出现最多 6/3 contact 的缓存尺寸分支，对应 PhysX 对 convex/sphere/capsule
  manifold contact 的 reduce/add batch 逻辑。
```

继续对照 PhysX 4.1 后，这条 mesh 路径可以更具体地拆成：

```text
pcmContactConvexMesh(shapeConvex, shapeMesh)
  -> 读取 PxConvexMeshGeometryLL / PxTriangleMeshGeometryLL
  -> getPCMConvexData(...) 得到 convex hull 的 PolygonalData 与 hullAABB
  -> CalculatePCMConvexMargin(hullData, scale, toleranceLength, GU_PCM_MESH_MANIFOLD_EPSILON)
  -> 构造 ConvexHullV 和 SupportLocalImpl
  -> PCMContactConvexMesh(polyData, polyMap, minMargin, hullAABB, shapeMesh, ...)

PCMContactConvexMesh(...)
  -> curTransform = meshTransform.transformInv(convexTransform)
  -> 如果 multiManifold.invalidate(curTransform, minMargin):
       replaceBreakingThreshold = minMargin * 0.05
       multiManifold.mNumManifolds = 0
       computeHullOBB(hullAABB, contactDistance, world0, world1, meshScaling)
       Midphase::intersectOBB(meshData, hullOBB, blockCallback, true)
       blockCallback.flushCache()
       blockCallback.mGeneration.generateLastContacts()
       blockCallback.mGeneration.processContacts(6, false)
     否则:
       projectBreakingThreshold = minMargin * 0.8
       multiManifold.refreshManifold(aToB, projectBreakingThreshold, contactDist)
  -> multiManifold.addManifoldContactsToContactBuffer(contactBuffer, meshTransform)
```

`PCMMeshContactGenerationCallback::processHit` 的行为也能对上 `func70030`
里的 indirect callback：midphase 每命中一个三角形，先做 OBB/triangle 测试，
再根据 mesh scaling 调整顶点 winding，读取 `extraTrigData` 里的 convex edge flags，
把三角形塞进 16 个一组的 `TriangleCache`。cache 满时进入
`processTriangleCache<16>`，这就是 `func70050/func70056` 周围那组函数的意义。
这个 callback 还有一个重要细节：`doTest(...)` 会先跑
`intersectTriangleBox(hullOBB, v0, v1, v2)`，只有和 hull OBB 相交的三角形才进入
cache；如果 mesh scaling 会翻转法线，代码会交换 `v1/v2` 的 winding。

`PCMConvexVsMeshContactGeneration::processTriangle` 的接触生成步骤是：

```text
v0/v1/v2 = triangle vertices
n = normalize(cross(v1-v0, v2-v0))
dist = dot(hullCenterMesh, n) - dot(v0, n)
if dist < 0: backface culling

locV0/locV1/locV2 = meshToConvex.transform(v0/v1/v2)
localTriMap = SupportLocalImpl<TriangleV>(localTriangle)
generateTriangleFullContactManifold(...)

若生成了 contact:
  把 inactive edges 写进 edge cache
  把三个 vertex 写进 vertex cache
  addContactsToPatch(patchNormal, previousNumContacts)
```

`generateTriangleFullContactManifold(...)` 现在也能进一步拆开。它不是把三角形当
无限平面，而是对 triangle 与 convex hull 做三类 SAT：

```text
testTriangleFaceNormal(...)
  用 triangle normal 做分离轴。
  min0=max0=dot(triangleNormal, triangle.verts[0])
  polyMap->doSupport(triangleNormal, min1, max1)

testPolyFaceNormal(...)
  遍历 convex hull 的所有 polygon plane。
  identity scale 时直接用 polygon plane normal；
  非 identity scale 时把 plane normal 转到 shape space 并归一化。
  每个 axis 都做 projection/contactDist 分离测试，并记录最小 overlap 的 face。

testPolyEdgeNormal(...)
  只使用 triFlags 标记为 active 的三角形边。
  对 active triangle edge 与 convex polygon edge 做 cross product。
  跳过近零轴，并用 triangle normal 做方向剔除。
  通过 projection/contactDist 测试分离轴，必要时把状态切成 EDGE。
```

状态分支如下：

```text
status == POLYDATA0:
  最小轴是 triangle normal。
  选 convex hull 中最贴近 triangle normal 的 polygon 作为 incident polygon；
  调 generatedTriangleContacts(...)，patchNormal = triangle normal。

status == POLYDATA1:
  最小轴是 convex polygon face normal。
  若 dot(-minNormal, triangleNormal) > 0.707106781:
    仍用 triangle normal 生成 generatedTriangleContacts(...)。
  否则 defer：把 triangleIndex、featureIndex、triFlags、三个顶点和三个顶点索引
    写入 mDeferredContacts，等 generateLastContacts() 再处理。

status == EDGE:
  根据 minNormal 重新找 convex reference polygon；
  用 generatedPolyContacts(...) 生成 contact，patchNormal = -convexFaceNormal。
```

`generatedTriangleContacts(...)` 和 `generatedPolyContacts(...)` 都会把 reference
polygon/triangle 投到以 contact normal 为 Z 轴的 2D 平面，再产生三类 contact：

```text
1. incident 顶点落在 reference polygon/triangle 内；
2. reference 顶点投影到 incident triangle/polygon 内；
3. reference edge 与 incident edge 的 2D 线段交点。
```

其中 triangle 内点判断会用 barycentric coordinate。单个 triangle/polygon
超过 `GU_MESH_CONTACT_REDUCTION_THRESHOLD = 16` 个候选点时，会先用
`SinglePersistentContactManifold::reduceContacts(...)` 裁到
`GU_SINGLE_MANIFOLD_SINGLE_POLYGONE_CACHE_SIZE = 4` 个。

`generateLastContacts()` 会处理延迟的 poly-face contact，并用 barycentric coordinate
判断新 contact 是否落在已缓存的顶点附近；阈值为：

```text
upperBound = 0.97
lowerBound = 1 - upperBound = 0.03
```

如果 contact 接近某个 triangle vertex，而该 vertex 已在 `mVertexCache` 中出现过，
就丢弃该 contact。处理 deferred triangle 前还会检查三条边：

```text
edge 01: triFlags 有 ETD_CONVEX_EDGE_01，或 CachedEdge(ref0, ref1) 不存在
edge 12: triFlags 有 ETD_CONVEX_EDGE_12，或 CachedEdge(ref1, ref2) 不存在
edge 20: triFlags 有 ETD_CONVEX_EDGE_20，或 CachedEdge(ref2, ref0) 不存在
```

三个条件都成立才会真正调用 `generatePolyDataContactManifold(...)`。
这就是相邻三角形去重的关键：inactive edge 进入 `mEdgeCache`，三个顶点进入
`mVertexCache`，后处理时避免在共享边/共享顶点重复生成相同接触。

`addContactsToPatch()` 先把同一三角形/patch 里超过 4 个的 contact 用
`SinglePersistentContactManifold::reduceContacts(...)` 裁到 4 个，再按
`replaceBreakingThreshold^2` 去重，并把 patch normal 转到 mesh local space。

`processContacts(6, false)` 的后处理流程已经能对上源码：

```text
prioritizeContactPatches()
  按 patch 最大穿透深度排序，深的排前面。

refineContactPatchConnective(...)
  把法线夹角 5 度以内的 patches 连接起来，阈值 mAcceptanceEpsilon = 0.996。

reduceManifoldContactsInDifferentPatches(...)
  不同 patch 间按 replaceBreakingThreshold 去重。

addManifoldContactPoints(...)
  每个 SinglePersistentContactManifold 最多保留 6 个 convex contacts。
  如果 manifold 数量不够，会优先保留更深的 patch。

addManifoldContactsToContactBuffer(...)
  contact.normal = manifold.getWorldNormal(meshTransform)
  contact.point = meshTransform.transform(localPointB)
  contact.separation = localNormalPen.w
  contact.internalFaceIndex1 = triangle face index
```

继续把 `func70051` 拆开后，几个子 helper 也已经能命名：

```text
func69975 f_jmyc
  对应 SinglePersistentContactManifold::reduceBatchContactsConvex(...)
  用于 convex hull，每个 SinglePersistentContactManifold 最多保留 6 个 contact。
  石壶本体是 convex MeshCollider，因此这是 stone-rink/stone-stone 里最相关的 reduction 分支。

func69976 f_kmyc
  对应 SinglePersistentContactManifold::reduceBatchContactsCapsule(...)
  最多保留 3 个 contact。正式石壶不是 capsule，此分支主要用于排除误读。

func69978 f_mmyc
  对应 SinglePersistentContactManifold::refreshContactPoints(...)
  用旧 manifold contact 在新相对位姿下重新投影，若平方距离超过
  projectBreakingThreshold^2 就删除该 contact，否则更新 localNormalPen.w / separation。

func69979 f_nmyc
  对应 MultiplePersistentContactManifold::addManifoldContactsToContactBuffer(...)
  把 manifold 中保留下来的 contact 写入 ContactBuffer：
    normal = getWorldNormal(meshTransform)
    point = meshTransform.transform(localPointB)
    separation = localNormalPen.w
    internalFaceIndex1 = mFaceIndex
```

`Gu::ContactBuffer` 这一层的结构也已经对到 PhysX 4.1。WebGL 32-bit 下每个
`Gu::ContactPoint` 是 64 byte，`ContactBuffer` 最多放 64 个 contact：

```text
ContactPoint, 64 bytes:
  offset 0   normal.xyz
  offset 12  separation
  offset 16  point.xyz
  offset 28  maxImpulse
  offset 32  targetVel.xyz
  offset 44  staticFriction
  offset 48  materialFlags
  offset 50  forInternalUse
  offset 52  internalFaceIndex1
  offset 56  dynamicFriction
  offset 60  restitution

ContactBuffer:
  offset 0     contacts[64]
  offset 4096  count
  offset 4100  pad[3]
  total size   4112 bytes
```

这和 wasm 里常见的 `contactBase + (index << 6)` 写入模式一致。
`tools/reverse/physx_contact_buffer_layout.py` 可以重新打印这些 size/offset，
避免后续把 `separation`、`internalFaceIndex1` 和 friction/restitution 字段看串。

`func69975/reduceBatchContactsConvex` 的 6 点选择规则也不是普通排序：

```text
1. 先选 localPointB 到原点距离最大的 contact。
2. 再选离第 1 个 contact 最远的 contact。
3. 用这两个点和第 1 个 contact normal 构造一条横向分离轴。
4. 在该轴两侧各选距离最大的 contact；若都在同侧，则重新选另一侧代表点。
5. 剩余两个名额给未选择 contact 中 penetration 最深的两个。
```

同一三角形 patch 内早一层的 `SinglePersistentContactManifold::reduceContacts(...)`
最多裁到 4 点；跨 patch 进入 single manifold 后，convex 分支再最多裁到 6 点。
这两级 reduction 是不同的：前者避免单个 polygon 产生过多候选点，后者控制最终
single manifold 的 solver contact 数量。

这里的 `reduceContacts(...)` 不是随机裁剪：它先保留最深点，再选离最深点最远的点，
再选相对这条线两侧距离最大的点，最多组成 4 点代表集。这解释了为什么碰撞结果会依赖
三角网格接触 patch、上一帧 manifold cache、三角形邻接/edge flags 和 contact reduction，
不能被一个简单二维圆盘-平面/圆盘-圆盘公式完全替代。

因此现在的状态不是“找不到碰撞入口”，而是“入口、表地址、函数号、manifold refresh、
contact reduction、ContactBuffer 写入和 convex-convex 候选点裁剪规则都已定位；
仍需把 PhysX 通用 PCM/GJK/mesh midphase 和后续 constraint solver 翻译成工程化模型”。对训练来说，
如果只需要可用本地模拟器，仍可以先近似；如果要极限对齐 Unity，就要继续结构化
`func70574/func70576/func70030` 的接触候选生成代码、4-wide batch 的 `func70963`，
以及 single-pair path 里已经定位出的 `func71103/func71104/func71105/func71173`。
`func71174/func71175/func71176`
