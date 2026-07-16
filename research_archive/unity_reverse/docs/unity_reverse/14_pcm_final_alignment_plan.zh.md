# PCM 最终对齐执行计划

更新时间：2026-07-11

## 目标

在不重新采样、不拟合碰撞参数的前提下，复现 Unity/PhysX 从 first PCM entrance 到
stone-stone contact、solver writeback 和双壶终点的完整过程。最终验收不是某一条样本
出现相同 contact 数，而是六条 `14000~14005` 样本逐层通过，并能说明每个修正对应的
真实 native 字段或调用语义。

## 当前基线

```text
BESTSHOT -> physical PCM shell:
  6 / 6 reached
  position RMSE = 1.159mm
  max error     = 1.350mm

MOTIONINFO -> physical PCM shell:
  6 / 6 reached
  position RMSE = 0.767mm
  max error     = 0.934mm

Unity contact counts:          [2, 2, 2, 4, 4, 4]
local exact-pose direct PCM:   [2, 4, 4, 4, 2, 4]
scalar exact-pose direct PCM:  [2, 2, 2, 4, 4, 4]
```

已确认相等：

- active/target exact native transform 可逐字段注入；
- `contactDistance=0.02`、`meshContactMargin=0.01`、`toleranceLength=1`；
- 4008 字节 runtime hull，SHA16=`7c5429592f144782`；
- BigConvex samples/valencies/adjacency，SHA16 分别为
  `ec18837768a60ec7 / ccf344e149137aea / d382b34acd8d58c6`；
- solver 公式与已捕获 ContactBuffer 的 row 重放路径。

已发现但尚未解释完的差异：

- 本地旧代码的 convex scale X/Z 少一个 float32 ULP；已经改为 Unity 精确值，但
  `14001` 仍为 4 contacts，因此它是真差异但不是主因；
- `ConvexHullData.centerOfMass` 与 Unity 不同；
- `ConvexHullData.mInternal.mRadius` 本地为 `1.1080279350`，Unity 为
  `1.1080278158`；
- `14002/14004` 在 Unity first-contact tick 前约落后一帧，即约 10.44mm；
- 14001/14002 即使强制 exact pose 仍是 4 而不是 2；14004 exact pose 为 2 而
  Unity 为 4。

边界校正（2026-07-11）：上述“scalar exact-pose direct PCM”是把 Unity 已捕获的
入口 transform、hull 和 task-local cache 直接交给 `PxcPCMContactConvexConvex` 的验收；它证明
**PCM 公式和离线入口状态可等价**。它不是持久 `PxScene` 中 contact-manager/work-unit 的等价证明。
当前最早的持久 Scene 分叉已在样本 14000 的 solver-facing `ContactBuffer` 观察到，两个 contact
point 相对 Unity 横移约 `8.5--8.7mm`；后续所有 P5/P6 结论必须明确说明属于哪一层，禁止把
direct-PCM 的成功外推成完整碰撞链成功。

## 执行约束

1. 不启动 Unity，不新增采样；只有现有日志缺失不可替代字段时才重新评估。
2. 不扫描摩擦、半径、恢复系数、contact offset 或 solver 参数。
3. 一次只修改一个已证明不一致的 native 字段或调用语义。
4. 每次修改先验 `14001`；只有 `14001` 闭合后才外推到其他样本。
5. contact 数相同不算完成；normal、point、separation、writeback 和 endpoint 必须继续验收。
6. 不把 oracle pose、oracle cache 或样本专用修正接入训练代码。

## 执行步骤

### P0 固化六样本基线

状态：已完成

产物：

```text
tools/reverse/audit_first_pcm_ice_ulp_multisample.py
data/calibration/first_pcm_ice_ulp_multisample_audit_20260710.json
```

退出条件：六条样本的自然 replay、exact pose、fresh cache、Unity before-cache 结果均已
保存；文档不再把 14000 的 1 ULP 结论外推到全体样本。

### P1 建立 14001 PCM 入口逐字段差异表

状态：已完成

比较边界：Unity `PxcPCMContactConvexConvex call 7 before` 对本地
`exact-pose direct PCM before`。

字段组：

```text
PxTransform active/target
PxConvexMeshGeometryLL scale/rotation/flags
ConvexHullData 完整头部
runtime hull 与 BigConvex 指向的数据
NarrowPhaseParams
Gu::Cache / LargePersistentContactManifold
GeometryUnion 构造路径与 contact method table 入口
```

产物：

```text
tools/reverse/compare_first_pcm_native_entry.py
data/calibration/first_pcm_native_entry_diff_14001_20260710.json
```

退出条件：所有可见字段被标成 `equal` 或 `different`；无法导出的字段有明确名称和所属
C++ 类型，不再使用“可能还有某些状态”的笼统描述。

结果：40 个可见字段中只有 4 项不同，即两只壶各自的
`ConvexHullData.centerOfMass` 与 `ConvexHullData.mInternal`。完整差异表已生成：

```text
data/calibration/first_pcm_native_entry_diff_14001_20260710.json
```

### P2 定位并修复第一个有效分叉语义

状态：已完成

结论：分叉不是某个 Unity native 字段。将同一份 Unity exact pose、runtime hull、
BigConvex、narrow-phase 参数和 before-manifold raw 同时输入 PhysX 4.1.1 时，x64 SSE
后端在 `generateFullContactManifold(...)` 内产生四点；Unity WebGL 的 scalar 后端只产生
其中两个底部点。`addBatchManifoldContacts(...)` 没有删点，分叉发生在其之前的
`generatedContacts(...)` 裁剪计算。

```text
SSE exact-pose direct PCM:     [2, 4, 4, 4, 2, 4]
scalar exact-pose direct PCM:  [2, 2, 2, 4, 4, 4]
Unity:                         [2, 2, 2, 4, 4, 4]
```

`14001` 在 scalar 后端的两个 local contact 与 Unity after-cache contact 的字段逐位相同。
这证明 4008-byte hull、cache、姿态和公式已经足够；必须使用 scalar PhysX，不能把
x64 SSE 的 PhysX 当作 Unity WebGL 的等价后端。

产物：

```text
tools/reverse/audit_scalar_pcm_backend.py
data/calibration/scalar_pcm_backend_audit_20260710.json
```

### P3 外推验证 14002/14004

状态：已完成

同一 scalar 后端未按样本分支，六条 exact-pose 输入全部通过：contact count 全匹配，
local point / normal / penetration 的最大分量差为 `5.960464477539063e-08`，即 float32
一 ULP 量级。验收见 `scalar_pcm_backend_audit_20260710.json`。

### P4 对齐 first-contact tick 与 PCM 生命周期

状态：已完成。

P4 的验收边界已经满足：`MOTIONINFO -> PCM shell` 为 6/6、位置 RMSE
`0.194mm`；exact native entrance 下 scalar PCM 为 6/6 float32-ULP 对齐；既有
hidden-yaw 历史能自然到达 local-contact 的四条样本 contact count 为 4/4 一致；第二次
PCM 的 task-local cache 重建也已用 Unity 运行时 raw bytes 验证。跨局 quaternion 与
碰撞后姿态不是 P4 的 tick/cache 缺口，归入 P5/P6。

只处理已确认的时间/历史问题：

```text
14002: first-contact handoff 约差 1 tick
14004: first-contact handoff 约差 1 tick，且 Unity 有 8 次 pre-contact PCM 调用
14003: Unity 有 4 次 pre-contact PCM 调用
14005: Unity 有 3 次 pre-contact PCM 调用
```

最新 scalar 持久 Scene 审计：4/6 在现有噪声窗口内自然到达 local contact，四条的 contact
count 均与 Unity 一致。active entrance position RMSE 为 `0.205mm`，target position RMSE 为
`0.00099mm`；14002/14004 的未到达仍由跨局 hidden yaw 历史决定。此前 14000/14001 的
“2 变 3/4”已经确认是本地完整 manifold 留存导致，不能再归因于 first-contact feature boundary。
下一步只处理持久 actor 的真实 quaternion/yaw 和 solver writeback，禁止退回调参。

2026-07-10 已额外排除 custom sliding kernel：从 Unity 抽出的 `func59956`
`Newfrictionstep` Wasm 原函数逐 tick 消费六条相同噪声流，与 Python 翻译的最大差仅
`vx=1.73e-18`、`vy/w=2.22e-16`。因此剩余一 ULP 高度、横向微差和 14002/14004 的
tick 差发生在“velocity 写入 Rigidbody 后的 scalar PhysX Scene 积分/接地接触”，不是
随机摩擦、fsimp 或 Python 数学库。证据：

2026-07-10 进一步核对采样顺序：六条样本是同一连续 session，0/1 号壶交替出手，8 号壶
反复被 Reset。Unity 的 Reset 仅重置二维 position，完整 quaternion 会保留；但现有
`front_half_pcm_samples` 的 reset/after 记录只含二维位置，没有每个 reset 边界的
`PxTransform.q`。因此 P4 的执行顺序固定为：先让本地 16 壶 Scene 无姿态注入地连续复放，
每帧以真实的首个 stone-stone PCM/report 定义 first-contact tick，并与已抓到的 Unity
first-PCM `P/Q/v/w` 比较；若连续复放在某个 reset 后首次分叉，缺口就精确是该 reset 边界
未记录的 Unity quaternion，而不是再调位置、摩擦或 contact 参数。

首次连续审计已完成，产物：

```text
tools/reverse/audit_persistent_scene_sequence.py
data/calibration/persistent_scene_sequence_audit_20260710.json
```

它证明本地 Reset 前后所有被跟踪 actor 的 quaternion 差严格为 `0`。第一处跨 shot 历史
失配不在 Reset：14000 的 cold active 在 first-contact 前仍只差 `3.82e-5m` / `8.69e-5rad`，
但该微差使 local scalar Scene 产生 4 contacts；将它继续推进到静止后，14001 的 target 8 号壶
入口 quaternion 已差 `0.00810`。同时 14001 的 fresh active 只差 `1.74e-5`。故下一项只应
解决 14000 的 first-contact 前接地 tick / micro-pose，之后再验证 collision writeback；不能把
后续 yaw 发散误判成 Reset 或滑行公式问题。

2026-07-10 已完成冰面 runtime 捕获，证据为：

```text
log/unity_runtime_probe_20260710_194111/events.jsonl
data/calibration/unity_runtime_ice_triangle_mesh_20260710_final.json
```

`PxcPCMContactConvexMesh` 里的 Unity `Gu::TriangleMesh` 已逐字段读出：`121` 个顶点、
`200` 个三角形、16-bit index（`mFlags=2`）；`mVertices/mTriangles` 的 SHA-256 分别为
`01a7fde6b4c13248053bbbccff5df80f5f4b88e2634d370cf588dbd5336f84ee` 和
`643fd5c9d59918e837fd9295e74c431602ed0ca5d100fa51dfa7ad75dec90856`。geometry 的 scale
是 `(4.99799156, 1.01600003, 0.99568027)`，pose 是
`(-85.98600006, 14.30478477, 55.56601715)`，二者 rotation 都是 identity。

这同时否定了“本地普通 10x10 网格已经完全等价”：两者覆盖范围相同，但 world center 相差
`(-7.60858, 0, +1.41602)m`，顶点 float32 相位最高差 `6.10e-5m`，且三角形 face set/顺序并不相同。
最初的“直接重 cook”审计确实失败过：当时把 runtime 顶点先乘非均匀 scale、再加 world translation 后，
把这份已经 cooked 的 triangle 顺序交给本地 cooker；结果 BVH34 变成 116 nodes，14000 active yaw
误差从 `8.69e-5rad` 变成 `1.60e-4rad`。失败的原因不是 Unity `mTriangles` 不能借用，而是错误地改变了
其 native vertex frame 后才 cooking；该 world-baked 接入已撤回，不能作为训练代码。

2026-07-10 随后完成了“一次 cooking”路径的字段审计，产物：

```text
tools/reverse/audit_runtime_ice_cooked_equivalence.py
data/calibration/runtime_ice_cooked_equivalence_audit_20260710.json
```

这里的关键修正不是调参：旧本地实现把非均匀 scale 和 world translation 烘进顶点后再 cooking；
Unity 则是对内置 `New-Plane.fbx` 的原始 `[-5,5]` 顶点先 cooking，再在
`PxTriangleMeshGeometry` 上保留 `PxMeshScale=(4.99799156, 1.01600003, 0.99568027)`，并把
static actor pose 设为 `(-85.98600006, 14.30478477, 55.56601715)`。新审计保持 runtime 捕获的
原始顶点 frame，不烘焙 scale/pose，并直接复用 Unity 的 `Gu::TriangleMesh.mTriangles` 作为本地
cooking 输入，得到：

```text
Unity BVH34:                    100 nodes, initData=4, quantized, 1600 bytes
旧 reconstructed / BVH34:       116 nodes, 1856 bytes
post-cook arrays re-cook / BVH34: 116 nodes, 1856 bytes
source + scale + pose once / BVH34: 100 nodes, 1600 bytes
```

因此“先把 world 坐标烘进顶点”的路径已被明确排除；Unity 的 vertex frame、`mTriangles`、
`PxMeshScale`、static pose、BV4 node count 与 node buffer 尺寸均已对齐。source-once 的本地 cooked
`mTriangles` 现在是 `200/200` 行一致，公共前缀也是 200。这个结果仍**不能**标记 cooked mesh
完成：Unity 的 `mFaceRemap` 与完整 `BV4Tree.mNodes` 没有被现有 runtime capture 导出，因此 local
1600 bytes 的内容尚未能逐字节比较。剩余缺口已从 cooking 输入与 triangle order 收缩到 face remap
和 BV4 raw node bytes。

2026-07-10 21:30 的补抓已完成最后两块 runtime 真值：

```text
log/unity_runtime_probe_20260710_213035/events.jsonl
data/calibration/unity_runtime_ice_triangle_mesh_20260710_213035_v3.json
```

新的 probe 一次性读取了 `mFaceRemap`（800 bytes）及 `BV4Tree.mNodes`（100 x 16 = 1600 bytes）。
本地 source-once 重新 cooking 后的 BV4 node buffer SHA-256 已与 Unity 同为
`583e42fad1dce2329c9b09c781cab101bfb11ebc7ea04d9f5237729c006cd929`；vertices、16-bit
triangles、BV4 nodes 三者均逐字节相等。local cooker 的 face-remap 是恒等映射，而 Unity 保存的是
source-face permutation；该表不参与碰撞力，但影响 contact report 的 internal face ID，因此已通过
窄 pyphysx 接口直接覆写为 Unity 的 200 项真值。最终审计：

```text
vertices raw bytes:  equal
triangles raw bytes: equal
faceRemap raw bytes: equal
BV4 mNodes raw bytes: equal
```

证据：`data/calibration/runtime_ice_cooked_equivalence_audit_20260710.json` 的
`acceptance.cookedIceEquivalent=true`。至此 **ice cooked object 已完全对齐**，不再是 P4 的未知项。

另有本地后端约束：Unity WebGL 的 stone-stone PCM 要使用 scalar PhysX 才能和 Unity contact
生成一致；该 scalar 构建由于 `PX_SIMD_DISABLED` 不能执行 BVH34，因此默认可执行 Scene 是 BVH33。
把正确的 non-uniform `PxMeshScale` 接入这个 BVH33 fallback 后，多壶持续 Scene 会在本地
pyphysx 的 scaled-triangle-mesh pair 路径异常退出。单壶可连续跑过 1800 tick，故这不是 source
mesh 缺失或滑行公式差异，而是本地 binding/backend 的限制。source-once 目前只作为 cooked
equivalence 审计，不得接入训练或宣称 P4 已闭合。

因此 P4 的剩余问题不再包括 mesh/cooking/冰面接触几何，只剩 **连续 Scene 的 first-contact
tick、hidden yaw 与 PCM cache 生命周期**。14000 在 target collision pair 被临时关闭、活动壶仍在完整
Unity ice mesh 上推进至 PCM shell 时，step `1559` 的 active native position 已逐分量等于 Unity；
yaw 仍差 `-1.23025e-4rad`。下一步只允许追这条 angular-state/tick 链，不得再修改冰面几何。

scalar backend 的限制仍需明确保留：Unity WebGL stone-stone PCM 要使用 scalar PhysX；该构建不能
执行 BVH34 traversal，因此可执行前半段使用 BVH33 fallback，但 PCM shell 后必须交给已经通过 P2/P3
的 scalar direct PCM。完整 six-shot persistent-shell 审计脚本
`tools/reverse/audit_unity_source_front_half_shell.py` 尚未稳定产出表，P4 不能因 ice cooked object
完成而提前标记完成。
离线解析器为 `tools/reverse/extract_runtime_ice_triangle_mesh.py`；它只接受带
`triangleMeshRuntime` 的新捕获，避免把旧版将 geometryType=5 误作 convex 的日志当作真值。

```text
tools/reverse/audit_newfrictionstep_wasm_rollout.py
tools/reverse/run_newfrictionstep_wasm_rollout.js
data/calibration/newfrictionstep_wasm_rollout_audit_20260710.json
```

产物：

```text
data/calibration/persistent_scene_front_half_contact_scalar_audit_20260710.json
```

2026-07-10 晚间复验：`PersistentPhysxFrontHalfScene` 默认冰面已改为 `unity-source-once`，不再
走 hand-reconstructed plane；scalar Scene 使用可执行的 BVH33 fallback，而 source/scale/cooked
输入保持 Unity 真值。六样本在此入口上的结论是：

```text
BESTSHOT natural Scene first-contact: 14000/14001/14003/14005 = 4/6 reached
14000/14001 natural contact count:    2 / 2
14003/14005 natural contact count:    4 / 4
MOTIONINFO -> PCM shell position:     6/6 reached, RMSE 0.194 mm, max 0.290 mm
exact entrance pose -> scalar PCM:    6/6 contact count/normal/separation float32-ULP 对齐
```

`14002/14004` 的旧 10.44 mm first-contact miss 已定位为用 BESTSHOT 公式替代 Unity 实际写入
Rigidbody 的 `MOTIONINFO`：两条初始纵向速度差约 `5e-4 m/s`，一千余 tick 后累积为厘米级距离。
这不是 PhysX contact 的未知参数。改用日志里的 MOTIONINFO 后，所有 active position 都进入亚毫米范围。

剩余真实状态缺口只有两项，均不能用样本专用 pose 注入冒充完成：

1. 首条 `14000` 在 MOTIONINFO 前已有未记录的 active hidden yaw。local cold-yaw=0 的 entrance
   yaw 比 Unity 少 `0.0246336728 rad`；该差异首条即存在，不能由后续 Reset 补出。
2. 后续 0/1 号壶交替出手，Reset 保留 quaternion；起始 yaw 由前一碰撞 solver writeback 产生。
   初始 yaw 未锚定时，14000 settle 后本地 0 号壶 yaw 约 `0.21521 rad`，14002 所需历史入口量约
   `0.22189 rad`，故还须由 P5 对 Unity 碰撞后 writeback 真值逐字段校验。

因此 P4 的前半段（Unity MOTIONINFO 到 PCM shell、scalar PCM manifold）已闭合；最终持久生命周期
验收仍需补记录每个 MOTIONINFO 起点的 active `PxTransform.q`，以及碰撞后 `0.01s/settled` 的
active/target `PxTransform.q`。这不是 endpoint 采样或参数拟合，而是当前日志唯一缺失的 native
state 边界。
### P5 solver writeback 验收

状态：机制边界已完成；Scene 数值 writeback 仍在验收。

#### 2026-07-11：X/Z solver inertia 已对齐，剩余为 entrance yaw/friction

`hybrid_p6_endpoint_14000_20260711.json` 以 no-oracle 连续 Scene 跑同一条
14000。它直接证明此前的本地 `FreezeRotationX/Z` 不等价于 Unity 的 solver 输入：
上游 PhysX `DyRigidBodyToSolverBody.cpp` 对 lock flag 只清角速度，源码明确保留
`sqrtInvInertia` 的 X/Z 列；而 Unity raw `PxSolverBodyData.sqrtInvInertia` 在同一
first finalizer 边界只保留 yaw 轴。

将本地 mass-space inertia 改为 `[0, 0.1892229261, 0]` 后，normal row 从：

```text
local old: velMultiplier = 3.93984 / 3.94536
Unity:     velMultiplier = 9.43222 / 9.46369
local new: velMultiplier = 9.43216 / 9.46370
```

五轮 position-solve 的前两条 normal force 也逐轮贴合 Unity；因此这不是惯量拟合，
而是将 Unity runtime native state 写入 `unity_front_half_physx.py`。该修复把
14000 的 target endpoint error 从 `38.804mm` 降到 `33.484mm`。

此后 first finalizer 仍有一个精确的上游差异：active quaternion 约差
`1.23e-4 rad`，第一条 friction row 的 `targetVelocity` 约差 `1.57e-3m/s`。
normal/contact/solver-row 公式不再是分叉；下一步仅审计
`Newfrictionstep -> angular velocity write -> PhysX yaw integration` 的调用相位，
并以 Unity raw first-finalizer pose 为验收，禁止扫描摩擦、反弹或 contact 参数。

最新入口/出口分界验证：给 14000 的 MOTIONINFO 起始壶注入从 Unity entrance 反推的唯一 hidden
yaw `0.0246336728 rad` 后，本地 first PCM entrance yaw 与 Unity 只差 `1.924e-7 rad`，且
Scene 自然产生 2 contacts。让该局继续自然静止，0 号壶的 local yaw 为 `0.20000967 rad`；下一条
14002 从其 Unity entrance 反推的 MOTIONINFO 起始 yaw 为 `0.24637914 rad`，相差
`0.04636947 rad`。因此分叉已经被严格放在：first PCM 之后的 solver writeback、接触后 Scene
推进或两者之间，而不在 motion、ice cooked object 或 PCM manifold 生成。

后续只比较 Unity `solveContact` writeback 后的 body linear/angular velocity、`PxTransform.q`，再在
`0.01s` 与静止边界比较同一字段；不搜索摩擦、反弹或姿态参数。

已完成 Unity 首条 writeback 的确定性解码，产物为
`tools/reverse/audit_unity_solver_writeback.py` 与
`data/calibration/unity_solver_writeback_14000_audit_20260710.json`。它以 finalize constraint pointer、
shapeInteraction 与两只 solver-body pointer 三元组定位 `solveContactBlockWithWriteback call 2`，得到：

```text
Unity active written linear/angular: (0.73831134, 0.00001802, -0.01018930) / wy=0.36808948
Unity target written linear/angular: (0.05149376, 0.00001855,  0.00992249) / wy=0.18375860
```

本地已用 scalar pyphysx 的 pair-specific `PxContactModifyCallback` 将 dynamic-dynamic contact 设为
Unity raw 的 `0.36/0.36`，而 stone-ice 仍保持 custom sliding 的 frictionless material；同时在
PCM shell tick 前唤醒 target，匹配 Unity solver data 的 `bodyState=1`。

2026-07-10 的单一受控 `14000` 重采样已抓到连续六次真实
`PxcPCMContactConvexConvex` 调用，原始证据保存在
`log/unity_runtime_probe_20260710_p4_second_pcm/unity_runtime_probe_20260710_233626/events.jsonl`。
关键第二次调用说明 Unity 不是把第一次 after 的完整两点 manifold 原样续用：

```text
call 1 after:  numContacts=2, numWarmStartPoints=1, a=[8,209,43], b=[81]
call 2 before: numContacts=0, numWarmStartPoints=0, a=[8,209,43], b=[81]
call 2 after:  numContacts=2, separation 与本地 scalar 逐 float32 相同
```

所以 Unity 在每次 task-local PCM 调用前重建 manifold：清空 contact points、相对变换与
warm-start count，但保留 feature-index 字节。此前本地 Scene 错把 call 1 after 的完整两点
manifold 直接留到 call 2，才会在相同 pose 下生成 3 contacts。将同一规则接入 scalar pyphysx
Scene 后，`MOTIONINFO -> local-contact` 的四条自然到达样本 contact count 为 `4/4` 一致，
active entrance position RMSE 为 `0.205mm`；该修复没有改变冰面滑行路径。

这项结论由 `unity_front_half_physx.py` 的显式生命周期开关和
`data/calibration/persistent_scene_motioninfo_local_contact_after_pcm_lifecycle_20260710.json`
复验。P5 只继续比较 solver writeback、hidden yaw 与碰撞后持久姿态，不再搜索 PCM cache 参数。

最后一次同 tick 审计还补齐了本地 rigid-body 的真实 solver 输入：mass=`19.1kg`、
solver iterations=`6/1`、max depenetration=`10` 与 Unity 一致；Unity
`sqrtInvInertia.y=2.29886317` 对应的 `Iy=0.1892229261` 已写入本地。以 Unity 14000
第二次 PCM 的 pose/contact 为边界，本地 scalar Scene 也生成相同的 2 contacts 与
separation；其 high-level writeback 仍有 mm/s 级残差，是同 tick stone-ice 多约束
BVH33/BVH4 执行顺序的整场积分问题，而非 stone-stone 的 SolverContact 行公式。

P5 的退出条件已经满足：Unity raw `ContactBuffer + PxSolverBodyData` 经
`replay_solver_consume_delta.py` 重放到 `solveContactBlockWithWriteback` 后的 body
linear/angular writeback 为 float 精度；direct scalar PCM 生成的同一 ContactBuffer 也能
构造同一 normal/friction rows。证据见
`data/calibration/unity_solver_writeback_14000_audit_20260710.json`、
`data/calibration/front_half_pcm_solver_state_20260710.json` 与
`data/calibration/unity_direct_pcm_solver_row_bridge_20260709.json`。

范围校正（2026-07-11）：这里的“退出条件”仅指 **给定 raw ContactBuffer、solver body 和
constraint row 后的单约束公式/写回边界**。它不等价于“连续 Scene 的切向 friction state 已完全
对齐”。P6 六组重放已显示 14001 后出现首个 target yaw 分叉，故 P5 的整场数值 writeback 验收仍需
继续，以 14001 Unity/local first-finalizer friction row 和 post-writeback yaw 为下一证据。

完整 Scene 同时处理冰面约束并跑到静止后的双壶终点，仍只在 P6 验收；不得用 P5 的 raw-row
成功替代 P6 的 2cm endpoint 门槛。

### P6 双壶终点与训练接入门槛

状态：执行中，尚未通过。

#### 2026-07-11：修正脚本/物理时相，六组均已自然进入接触

此前 P6 将“一次 `Random.Range` 摩擦调用”错误等同于“一次 `Scene.simulate(0.01)`”。对
14002/14004，Unity 在最后一次摩擦调用之后仍会执行一帧固定物理：不再运行
`Newfrictionstep`，只推进 PhysX。旧本地缺这帧，故两个样本分别漏掉 `2-contact` 与
`4-contact` 接触，表现为米级终点错误。

这是直接因果验证，不是调参：将两壶摆到已经抓到的 Unity first-PCM pose 后，且只补这一帧
`Scene.simulate(0.01)`，14002 立即产生 2 contacts 和非零碰撞冲量，14004 立即产生 4 contacts。
对应生产修复位于 `unity_front_half_physx.py::_run_to_first_contact`：摩擦序列结束且仍未收到
stone-stone report 时，只追加一个不消费 RNG、不调用自定义滑行公式的 physics-only trailing step。

证据与可复现审计：

```text
tools/reverse/audit_hybrid_p6_endpoint_sixshot.py
data/calibration/hybrid_p6_endpoint_sixshot_20260711.json
18 passed, 44 subtests passed
```

该修复后，六组均已产生本地 stone-stone contact：

| 样本 | first-contact 数 | trailing physics step | active 终点误差 | target 终点误差 | 当前判断 |
|---|---:|---|---:|---:|---|
| 14000 | 2 | 否 | 1.638mm | 2.007mm | 通过本样本 |
| 14001 | 1 | 否 | 9.176mm | Unity 已出界，本地仍在场 | 出界生命周期未对齐 |
| 14002 | 2 | 是 | 10.175mm | 55.633mm | 目标壶切向/yaw 状态未对齐 |
| 14003 | 4 | 否 | 无可靠真值 | 无可靠真值 | 原 Unity sampler timeout，不能计入 P6 误差 |
| 14004 | 4 | 是 | 18.610mm | 39.006mm | 目标壶切向/yaw 状态未对齐 |
| 14005 | 4 | 否 | 10.449mm | 11.676mm | 通过本样本 |

可靠 Unity `POSITION` 的五条中，active 均小于 20mm，RMSE 为 11.366mm；四条仍在场 target
的 RMSE 为 34.485mm，故 P6 仍不通过。

此前记录的单条 `14000 target=33.484mm` 不得再作为 P6 证据：它误把 2026-07-10 早期六组会话的
摩擦序列与后一次受控运行的终点配对，二者的 `MOTIONINFO` 不同。历史文件保留以便审计，但已由
同源六组结果取代。

#### 当前最早剩余分叉

时相修复后，不再有 14002/14004 的漏碰；剩余误差已明确落在碰撞切向状态的持久链。逐字段对比
first-contact entrance yaw：

```text
14000: active -0.000028rad, target  0.000000rad
14001: active -0.000023rad, target +0.007340rad  <- 首个可观测 target 分叉
14002: active -0.023539rad, target -0.009645rad
14004: active -0.156669rad, target -0.498750rad
14005: active +0.117902rad, target -0.396512rad
```

因此不能再把 14002/14004 的终点归因于 contact count、hull 或摩擦参数。下一条证据任务是比较
14001 第一笔 stone-stone `createFinalizeSolverContacts` 的 Unity/local friction rows 和
writeback yaw；本地对应 trace 已保存为：

```text
data/calibration/local_14001_first_contact_trace_20260711.json
```

#### 2026-07-11：PCM 参数顺序敏感性反事实（诊断，不是生产根因结论）

此前 P1/P2/P4 已分别排除了 `PxConvexMeshGeometryLL`、runtime hull/BigConvex、exact
transform、NarrowPhaseParams 及 task-local cache 清空语义；因此不应重复搜索
`localPose`、scale 或 cache feature 字节。对 14000 的同一 second-finalizer transform 做了
以下 scalar direct-PCM 反事实：

```text
Unity 调用顺序 active -> target: contact x = -69.7170258 / -69.7175980
本地 Scene 顺序 target -> active: contact x = -69.7257614 / -69.7261047
```

两种顺序的法线只差符号，separation 保持同量级；但 PCM 的 full-manifold/reduction 不是交换律，
接触点可沿切向移动约 `8.8mm`，其量级足以解释第一条 `Dy::SolverContactFriction.targetVelocity`
的 `1.57e-3m/s` 差。因此“pair 参数顺序”是一个已证实的**敏感方向**。

但这不是 P6 的生产根因结论：P4 已记录 local Scene 在 Unity solver-facing tick 前会产生 early
PCM/contact report，且 Scene 内的 cache/work-unit 生命周期与 standalone direct PCM 不同。将 direct
反事实硬接到 Scene 会使 early call 变成四点，不能作为修复，也不能改变训练/P6 代码。该实验已撤回；
保留结论仅用于后续同相位 native row 审计。

下一步仍遵循既定 P5：以 14001 第一笔 Unity/local 同相位
`createFinalizeSolverContacts` 为边界，逐字段比较 ContactBuffer、friction row 和 writeback yaw；
在该边界证明最早分叉后，才允许改变 Scene pair/work-unit 路径。

该比较已于 2026-07-11 完成，产物：

```text
tools/reverse/audit_p5_14001_same_phase.py
data/calibration/p5_14001_same_phase_audit_20260711.json
```

自动按两个 body-frame position 配对后，local finalizer sequence `2` 与 Unity stone-stone row
`9` 的 position squared error 为 `0`。结果表明 14001 不是新的 solver 分叉：

```text
active entrance yaw: Unity 0.0358946185, local 0.0358716004, delta -0.0000230181 rad
target entrance yaw: Unity 0.0268390436, local 0.0341789896, delta +0.0073399461 rad
first friction targetVelocity delta: -0.0087128505 m/s
```

也就是说，14001 的 friction row 差发生前，target quaternion 已经带着 14000 collision 后的
`0.00734rad` 历史偏差进入 solver；不得把它误判成 14001 的独立 friction/solver 参数缺口。
P5 的最早未闭合边界回退为 **14000 first solver-facing ContactBuffer 的切向 contact point**，及其
随后造成的 target angular writeback。下一项只比较该 14000 边界的 Scene work-unit/contact generation
语义，禁止用 14001 的 endpoint 或 yaw 反向拟合。

对应 14000 审计已经完成：

```text
tools/reverse/audit_p5_14000_contactbuffer.py
data/calibration/p5_14000_contactbuffer_audit_20260711.json
```

它自动匹配到 Unity stone-stone row `0` 与 local finalizer sequence `2`，两个 body-frame position
的 squared error 为 `0`。进入 solver 前的姿态差为：

```text
active yaw delta = -0.0000282132 rad
target yaw delta = -0.00000000000529 rad
```

但同一 ContactBuffer 的两个 world contact point 已在切向横移：

```text
point 0 local - Unity = (-8.735657mm, 0, +1.300812mm)
point 1 local - Unity = (-8.506775mm, 0, +1.258850mm)
separation delta       = +0.3725um / +0.0680um
first friction targetVelocity delta = -0.0015719235m/s
```

因此 `Dy::SolverContactFriction` 的差是 ContactBuffer 杠杆臂的下游结果，不能改 friction 或
writeback 参数来修。当前最窄的未知项是：持久 Scene 的 contact-manager/pair work-unit 如何在同一
transform、hull、参数与 task-local cache 生命周期下进入不同的 convex-convex full-manifold
reduction 路径。下一 probe 必须读取该 work-unit 的 body/shape order、cache pointer/size/flags 与
contact-manager creation/refresh 边界；不再新增 endpoint 采样。

#### 2026-07-11：`SetActive` Scene 成员资格 A/B（已证实敏感，但不是修复）

13 号文档的反编译已证明 Unity 对未上场壶调用 `SetActive(false)`，出手时再启用同一
GameObject；这不等价于仅关闭 `SIMULATION_SHAPE`。因此以 14000 做了一个严格的本地反事实：不改
stone actor、shape、pose、hull、材质、tick 或 cache-lifecycle hook，只将 inactive actor 从
`PxScene` 移除，并在出手时把**同一个 actor**重新加入 Scene。

```text
仅关闭 simulation shape（当前生产基线）：
  finalizer body order = target -> active
  solver-facing manifold = 2 contacts
  contact x = -69.7257614 / -69.7261047

移除并重加同一 actor（SetActive membership A/B）：
  finalizer body order = active -> target
  solver-facing manifold = 4 contacts
  两个底部 contact x = -69.7175980 / -69.7180557

Unity：
  2 contacts
  contact x = -69.7170258 / -69.7175980
```

这给出两个确定事实：Scene 注册历史会改变 native work-unit 的 body order；body order 的变化足以
把切向位置从约 `8.8mm` 差异拉到亚毫米量级。与此同时，它把流形从 Unity 的 2 点变成 4 点，故
“remove/add actor”不能进入生产后端，更不能当作 P6 修复。它反而缩小了唯一未知：Unity 的
`SetActive` 同时如何创建/复用 `ShapeInteraction`、contact-manager 和其 PCM cache，而本地
`removeActor/addActor` 没有复刻其中的 native 生命周期。

该 A/B 仅以 `set_active_scene_membership=True` 的默认关闭实验开关存在于
`unity_front_half_physx.py`，不改变训练或 P6 基线路径。下一步只读抓取同一 14000 solver-facing
call 的 work-unit body/shape order、interaction/contact-manager 指针、cache 地址/flags/feature bytes，
并与 Unity runtime hook 的同字段逐项比较；字段不齐前不得继续改 Scene 注册或 solver 代码。

#### 2026-07-11：work-unit 字段已从既有日志解出

上述“下一步”不需要重新启动 Unity。`createFinalizeSolverContacts` 的既有
`shapeInteractionWindow` 已含有 `ShapeInteraction.mManager`，其后是完整的 wasm32
`PxsContactManager::mNpUnit`；本地 finalizer trace 也已增加相同字段的只读导出。可复现审计为：

```text
tools/reverse/audit_p5_14000_workunit_state.py
data/calibration/p5_14000_workunit_state_audit_20260711.json
```

在关闭本地 `PxContactModifyCallback` 后，14000 的关键字段为：

| 字段 | Unity | local | 结论 |
|---|---:|---:|---|
| `PxcNpWorkUnit.flags` | 611 | 611 | 已一致 |
| `statusFlags` | 2 | 2 | 已一致 |
| `edgeIndex` | 2 | 2 | 已一致 |
| `frictionPatchCount` | 0 | 1 | 不一致 |
| contact-manager `index` | 1 | 2 | 不一致 |
| `transformCache0/1` | 12 / 9 | 9 / 1 | 不一致 |
| `mNpIndex` | 8 | 16 | 不一致 |

旧本地默认值为 `flags=737`，比 Unity 多 `128`，即 `eMODIFIABLE_CONTACT`。来源不是 Unity，
而是本地为了把 active 壶的预碰撞 `0` 摩擦强行改成 `0.36` 所加的 contact-modify callback；更早的
filter shader 即使 callback 被关闭也无条件写该 bit。现已修正 binding，使 callback 关闭时不再设置
`eMODIFIABLE_CONTACT`，并在审计中验证 flags 从 `737` 收敛到 Unity 的 `611`。

这不是“调材质”的结论。正式 `BESTSHOT` 的 active 预碰撞摩擦确实是 `0`，直接全程改为 `0.6`
会让 14000 在原噪声窗口内不再进入同一碰撞。因此还不能仅凭 flags 一致就把“关闭 callback”接入
production；下一步要先用 runtime `OnCollisionEnter` 与 first finalizer 的时序，复刻 Unity 从 `0` 到
`0.6` 的真实切换边界。

`transformCache0/1` 不是自由参数：源码显示 narrowphase 直接用它们索引 `PxsTransformCache` 读取
两端 transform，`mNpIndex` 则索引/重排 contact-manager output。数值编号不同本身不说明 pose 错，
但它与 local `target -> active`、Unity `active -> target` 的 work-unit 顺序一致，证明两端的
`ShapeInteraction` 注册/刷新顺序尚未等价。当前唯一允许的下一步是比较这些 cache slot **指向的
transform 内容**及 pair registration/refresh 调用顺序；不能把编号硬写成 Unity 的 12、9、8。

#### 2026-07-11：cache slot 内容和微小 yaw 均已排除，不能把 probe 字段误读为新机制

随后针对同一 14000 first PCM 入口做了两项只读/单变量复验：

1. `transformCache0/1` 虽然编号不同，但其被 PCM 实际读取的两个 `PxTransform` 的 position 与
   quaternion 内容和 Unity 对应入口一致；差异只在 storage slot 与 pair 的角色顺序，不能把
   `12/9`、`9/1` 当作需要手填的物理参数。
2. local active quaternion 相对 Unity 还差约 `2.8418e-5rad`。在 active -> target 的
   membership 反事实中，把初始 yaw 精确补上后仍生成 4 contacts；因此这点角差是真实入口差，
   但不是 2-contact -> 4-contact 的主因。

中途曾把 Wasm probe 的某一条 cache 视图误读为 `cachedData=null` 的 fresh cache。这个解释已撤回：
原始 Unity cache truth 对六条 first-contact call 都清楚记录了有效的 `cachedDataPtr`，而且
`func70576` 入口立即解引用 `cache[0]`；空指针不可能走到正常 contact generation。P4 已证实的
真实语义仍是：每次调用前 `numContacts=0`、`numWarmStartPoints=0`，但 feature-index bytes 保留。
本地也已经按这一 task-local cache 重建语义处理。之后不得再把“cache 指针是否为空”列作未知项。

所以当前剩余边界进一步收紧为：在 transform 内容、hull、scalar PCM、task-local cache reset 及
`flags/status/edge` 已一致后，Unity `SetActive` 所形成的 `ShapeInteraction/contact-manager`
**创建或 refresh 顺序**为何能得到 `active -> target` 的 2-contact work-unit；本地两个可复现替代
路径分别得到 `target -> active` 的 2 contacts，或 `active -> target` 的 4 contacts。下一 probe 只需
读取/比对 pair 注册和 manager refresh 的真实调用顺序，不能再扫描摩擦、cache 指针或 yaw。

#### 2026-07-11：首 solver 的材质切换已可无 callback 复现

为把已确认的 `eMODIFIABLE_CONTACT` 本地污染从生产路径中移除，做了一个单变量 14000 A/B：
滑行阶段仍令 active material 为 `0`；仅在预测本 tick 进入 PCM shell 时，将 active material 恢复为
`0.6`，并关闭 contact-modify callback。结果为：

```text
local ContactBuffer static/dynamic friction: 0.36 / 0.36（两点均逐位等于 Unity）
local PxcNpWorkUnit.flags:                   611（逐位等于 Unity）
local contact count:                         2
```

这证明 Unity 第一笔 solver 的 `0.36` 不需要也不应由本地 `eMODIFY_CONTACTS` 伪造；它可由真实的
`0.6 x 0.6` material-combine 在 first PCM tick 前得到。审计脚本和结果：

```text
tools/reverse/audit_p5_14000_material_transition.py
data/calibration/p5_14000_material_transition_audit_20260711.json
```

同一次运行的 contact point 仍为约 `-69.72584/-69.72618m`，并未收敛到 Unity 的
`-69.71703/-69.71760m`。因此材质/callback 问题已经闭合，不能再作为切向点误差的解释；正式路径
应在 pair lifecycle 闭合后采用此 material-transition 语义，而不是继续保留 callback 覆盖。

#### 2026-07-11：pair lifecycle 专用 runtime probe 已就绪，采集 14000--14005

现有日志只在 `PxcPCMContactConvexConvex` / finalizer 时看到已存在的 manager，不能区分它在本 tick
之前是新建、注册，还是 refresh。源码与 Wasm `func70739` 已逐字段对齐：它是
`PxsCMDiscreteUpdateTask`，task wasm32 偏移 `+28/+32/+36/+40/+44/+48` 分别是
`cmArray / PxsContactManagerOutput[] / Gu::Cache[] / count / dt / PxsContext`。

probe 现会在该 task 的 before/after 逐项导出每条 manager 的：

```text
contactManager pointer
rigidCore0/1, shapeCore0/1
flags, statusFlags, frictionPatchCount
index, transformCache0/1, edgeIndex, mNpIndex
同 task-index 的 PxsContactManagerOutput 与 Gu::Cache
```

实现和启动器为：

```text
tools/reverse/unity_webgl_runtime_probe.js
tools/calibration/launch_pair_lifecycle_probe.py
```

它只 hook `PxsContext.contactManagerDiscreteUpdate`、`PxcPCMContactConvexConvex` 与
`createFinalizeSolverContacts`，以 `always` 模式保存 `14000--14005` 每条从出手、首碰撞到静止的
manager 时间线；每个 hook 上限为 18000，足以覆盖完整六条受控 shot。控制 sampler 仍会保存每条
MOTIONINFO、first PCM 与 final POSITION，故这次同时补齐此前终点缺失/timeout 的样本记录。
它不写 Wasm 内存；验收判据不是 contact 数，而是找出目标 stone-pair 的 manager 首次出现时刻及其
`taskIndex/mNpIndex` 是否属于 new-list 或 refresh-list，再与本地 shape-flag 路径的等价时间线逐项
比较。只有得到这个首个不同事件，才改 Scene 生命周期。

首轮启动即时暴露了采集配置问题，而非物理问题：全局 `always` 同时把每一帧 stone-rink
`createFinalizeSolverContacts` 的 2KB pointer windows 写入；14000 尚未完成时日志已约 763MB。该
partial log `log/unity_runtime_probe_20260711_113930/` 已保留、不删除，但不作为完整样本证据。probe
已改为分层策略：

```text
PxsContext.contactManagerDiscreteUpdate: 常驻，只保留 arg0 128B 与解码后的 task/manager 小字段
PxcPCMContactConvexConvex:              仅 arm，不导出重复 hull/BigConvex raw
createFinalizeSolverContacts:           只在 PCM arm 后短窗导出
```

这保留了“manager 首次进入 narrowphase task”的唯一必要时间线，同时避免以大量静态 hull/ice row
淹没六条结果。重启后才开始正式的 14000--14005 采集。

第一次正式运行还验证了控制协议的真实轮次：14000 由 Player1 的 0 号壶完成并已写入
`data/calibration/front_half_pcm_samples_20260711_114916.jsonl`，但下一回合轮到 Player2 的 1 号壶，
原计划中每条 `active_index=0` 与协议奇偶性冲突，sampler 在 14001 前主动退出。已修正 runner，
可用 `--start-index 1` 从 14001 恢复，并让 `ControlledSceneSampler` 按当前玩家的真实 0/1 parity
选择 active 壶；不会覆盖已保存的 14000。与此同时 finalizer hook 现只保留
`bodyState0=bodyState1=1` 的 dynamic-dynamic contact（stone-rink 为 1/2 或其他组合），进一步剔除
无关冰面行。修复均通过 JS/Python 语法检查与 18 个单元测试。

#### 2026-07-11：六条 manager creation 时间线已抓到，创建/refresh 二分已结束

最终六条记录由 14000 的保留 raw log 与 14001--14005 的续跑日志组成：

```text
data/calibration/unity_pair_lifecycle_timeline_20260711.json
tools/reverse/extract_pair_lifecycle_timeline.py
```

每条均在首个 dynamic-dynamic finalizer 前第一次出现在 `PxsCMDiscreteUpdateTask`，且共同的首次状态为：

```text
taskIndex                       = 1
PxcNpWorkUnit.flags             = 611
statusFlags / frictionPatchCount= 0 / 0
transformCache0/1               = 12 / 9
edgeIndex                       = 2
mNpIndex                        = 0x80000008  (new-list, slot 8)
Gu::Cache                       = manifold, numContacts=0, warmStart=0
```

`mNpIndex` 的最高位是 PhysX `NEW_CONTACT_MANAGER_MASK`；因此这不是 old-list 的 refresh，也不是
上一帧 persistent pair 的复用。Unity 在每一条 controlled shot 都是“新建 ShapeInteraction/contact-manager
-> register 到 new narrowphase list -> first PCM -> finalizer”的同一生命周期。manager pool 地址会在
三个对象间复用，`managerIndex` 随对象为 `1/0/2` 轮换，但这些不是自由参数。

这消除了最后一个二义性：此前计划中的“找出创建或 refresh”已完成，结果确定为 **创建**。接下来本地
只比较该新建 pair 的 `shapeCore0/1` 与 stone slot 角色：Unity 的 first task 已固定为
`active -> target`、cache `(12,9)`；本地 shape-flag 路径已知为 `target -> active`。不得再调用 Unity
采样、不得再改 cache/friction/yaw；只允许在本地 Scene 的 shape/actor 注册顺序上修复角色顺序，再以
14000 的 2-contact ContactBuffer 验收。

六样本最终验收仍为：

```text
active endpoint error <= 0.02m
target endpoint error <= 0.02m
正确复现 Unity cleared/out-of-play 生命周期
每条样本具有可靠 Unity final POSITION
```

只有 P0~P6 全部完成，才允许把本地模拟器标记为可用于碰撞策略训练。

#### 2026-07-11：task-cache clear A/B 已否证，首帧 2/4 分叉不来自 cache 生命周期

为避免把本地 probe 的包装行为误当 Unity 机制，`PersistentPhysxFrontHalfScene` 现把
`set_scene_pcm_unity_cache_lifecycle_enabled()` 暴露为显式开关。该开关为此前观测到
`numContacts=0 / numWarmStartPoints=0` 后加入的 task-cache reset 假设；启用时，wrapper 会在每次
convex-convex PCM 调用前执行 `clearManifold()`。它不是 PhysX 默认路径，因此必须单独证伪。

同一持久 Scene、同一 14000--14005 输入、同一 `active -> target` RigidID 顺序、同一壳层 material
恢复及关闭 callback 的 A/B 结果如下：

```text
task-cache reset 开启：  14000..14005 = 4, 2, 2, 4, 4, 4 contacts
task-cache reset 关闭：  14000..14005 = 4, 2, 2, 4, 4, 4 contacts
```

证据：

```text
tools/reverse/audit_persistent_scene_sequence.py
data/calibration/persistent_scene_sequence_lifecycle_audit_20260711.json
data/calibration/persistent_scene_sequence_native_cache_audit_20260711.json
```

因此首个 ContactBuffer 的 2/4 分叉**不是** `clearManifold()`、warm-start 或 cache pool 复用造成；
它们只可能影响首碰后的持续流形。此前把未初始化 feature bytes 当作 first-contact 主因的推测在此撤回。

这项否证**不重新打开** `PxConvexMeshGeometry`、scale/localPose、contact distance、hull/BigConvex 或
contact method table：P1/P2/P4 的 scalar direct-PCM 已经逐字段/逐样本闭合了这些层。结合本节已抓到的
Unity new-list 事实，唯一剩余边界仍是 `GameObject.SetActive(false/true)` 落到 Unity native PhysX 后的
精确 actor/shape/interaction 启停语义。本地 `remove_actor/add_actor` 只复现了 RigidID 使其成为
`active -> target`，却没有复现 Unity 的完整生命周期，故得到 4 contacts。后续只允许反查这条 native
SetActive 调用链及其创建 ShapeInteraction/contact-manager 的时序；不得通过灌入 feature bytes、缓存
内容或重扫已排除的几何字段来伪造 2 contacts。

#### 2026-07-11：`SetActive` 的 engine 调用链已定位到组件启停队列，尚未等同于 remove/add actor

为避免继续把本地 `Scene.remove_actor/add_actor` 误称为 Unity `SetActive`，已从 internal-call 注册表
反查到 engine 侧的实际入口：

```text
UnityEngine.GameObject::SetActive      Wasm table 129063 -> func82227
func82227                              -> func80192
enable                                 -> func80190
disable                                -> func80191
两支                                  -> func80182 (hierarchy/component activation)
                                       -> func79992 (flush 23 个组件回调队列)
```

`func80182` 会递归处理子层级，并按组件类别把既有 component 排入 23 个 activation queue；启用侧调用
`func79987` 入队，随后 `func79992/79993` 通过 component vtable callback 执行。禁用侧则经同一
hierarchy dispatcher 走相应的停用 callback。这里没有任何“直接 delete/recreate PxActor”的证据，
也没有只切 `SIMULATION_SHAPE` 的证据。

因此现有 Unity runtime 结果与本地 A/B 的正确解释是：Unity 的 GameObject 启停保留 stone identity，
但会通过 Collider/Rigidbody 所在的 component callback 更新 native physics state；本地 remove/add 仅巧合
复刻了 RigidID 角色顺序，未复刻该 callback 的 actor/shape/interaction 更新。下一步的最小工作是把
stone 的 MeshCollider/Rigidbody 在 `func79992` 中实际落到哪个 native callback、该 callback 是否
register/unregister shape 或只更新 broadphase 标志反查出来。此前的 hull/cache/摩擦/yaw 路线均不得重开。

为拿到这一条尚缺的对象级证据，probe 已新增**手动 opt-in** 的
`__curlingProbe.installGameObjectActivationHook()`：只 hook table `129063`，记录每次
`GameObject.SetActive` 的 GameObject pointer、布尔值和 128-byte 前/后窗口；不调用 Unity API，
不改 Wasm 内存，不自动启动浏览器或采样。它须与既有 `PxsCMDiscreteUpdateTask` hook 同时开启，
才可把某个 stone 的 activation event 和随后 new-list contact-manager 关联。实现：
`tools/reverse/unity_webgl_runtime_probe.js`。在没有这份 activation-to-native 关联证据之前，
不得把本地任一种 actor add/remove 或 shape-flag 变体接入 P6/训练路径。

#### 2026-07-11：受控 runtime component capture 已完成，启用与停用 dispatch 已分开

本轮由 watcher 自动进入无限局、准备和开始，随后 `controlled_scene_sampler.py` 自动完成
`RESETPOSITION -> RESETSTATE -> BESTSHOT` 的单一 14000 碰撞。原始日志和摘要：

```text
log/unity_runtime_probe_20260711_130633/events.jsonl
data/calibration/setactive_component_single_shot_20260711.jsonl
data/calibration/unity_setactive_component_pair_lifecycle_20260711.json
```

runtime 时间线确认 target 在 reset 的 call 28 启用、active 在 BESTSHOT 后的 call 36 启用；first
contact-manager 仍是 `new-list / slot 8 / flags 611 / transformCache [12,9]`，first finalizer 为 2 contacts。
两颗石壶都有 7 个 native component。其 type 20 的 vtable 为 `3221476`，与 00 号文档已经确认的
`MeshCollider` vtable 完全一致；它的停用 callback 是 table `122025 -> func73275`。`func73275` 会进入
`func73773` 的 engine physics-scene dispatch 路径，故 MeshCollider 已从“可能的组件”收紧为实际会影响
native physics registration 的组件。

同时这次反编译修正了一个关键边界：

```text
SetActive(true):  func80190 -> func80182(g=true) -> func79987 入 23 个队列
                  -> func79992/func79993 -> registry(component[1]) 的 descriptor slot[3]
SetActive(false): func80191 -> func80182(g=false) -> component vtable slot[24]
                  -> MeshCollider 为 func73275
```

因此本轮从 vtable 读到的 `func73275` 只证明 **停用** callback，不能错误当作启用时的 PhysX 调用。
剩余唯一的对象级未知已精确为：MeshCollider 的 `component[1]` type key 在 activation registry 中解析出的
descriptor 及其 slot 3 handler。下一步只读取该 key/descriptor/handler table index 并反查对应 Wasm 函数；
不重新采样 endpoint，不改 hull、PCM、cache、摩擦或 solver。

#### 2026-07-11：首次受控 activation-to-manager 时间线，已排除高层启用顺序

受控单样本 `14000` 已在不改 Unity 内存的条件下完整跑通。证据为
`log/unity_runtime_probe_20260711_122659/events.jsonl`，机器摘要为
`data/calibration/unity_setactive_pair_lifecycle_20260711.json`。时间线中的关键事件是：

```text
RESETPOSITION 后：target stone 8  SetActive(true)  call 51
BESTSHOT 后：      active stone 0 SetActive(true)  call 59
随后：             first PxsCMDiscreteUpdateTask -> new-list manager -> 2-contact finalizer
```

这与本地 persistent Scene 的高层 `target -> active` 启用顺序相同。因此“壶在 Scene 中注册的先后
顺序”不再是候选根因，也不能再试图通过交换 addActor 次序来修复 2/4 分叉。该 capture 的 128-byte
managed GameObject 窗口尚不足以识别其中 Collider/Rigidbody 的 native callback；probe 已扩展为同时
读取 `m_CachedPtr`、native component-entry 列表和每个 component 的 vtable activation slot。下一次
同一受控样本只需抓这一份 callback 映射，然后从真实 table index 反查其 Wasm 实现及 PhysX 调用。

## 状态更新规则

- 每完成一步，先更新本文件的状态和证据路径，再进入下一步。
- 若 A/B 不改变 contact 数，记录为“真实差异、非主因”，继续比较下一个入口字段。
- 若发现更早分叉，后续步骤保持待执行，计划退回该层修复。
- 英文归档不更新；只维护中文子文档。

#### 2026-07-11 更正：MeshCollider 不走通用 registry descriptor slot 3

随后的一次同样受控的 runtime capture（`log/unity_runtime_probe_20260711_133844/events.jsonl`，摘要
`data/calibration/unity_setactive_resolver_pair_lifecycle_20260711.json`）读取了 component key 及
`func80110` 所依赖的 resolver globals。target/active 的 MeshCollider（type 20）key 分别为 `-124`、`-140`，
而 resolver provider 与 table index 均为 `0`。按 `func80110` 的实际分支，负 key 在 resolver 为空时直接
返回 `0`，不会 fallback 到此前假定的 `f_hknd` registry lookup。因此上一节将 MeshCollider 启用归为
“registry descriptor slot 3 handler”的表述已被证伪，保留仅作历史记录。

这轮也确认 `func80183` 只是释放 23 个 queue 的临时内存，不能作为启用 callback。下一步改为沿
MeshCollider 自身的 native negative-key bridge 反查：从 `func73275 -> func73773` 的停用事件分支及其
对应启用分支，找实际更新 native physics state 的函数。该结论不需要新的 endpoint 采样，也不重开
hull、PCM、cache、摩擦或 solver 假设。

#### 2026-07-11：MeshCollider 的实际 activation flush 已静态闭合

该反查现已完成。`func73773/f_lced` 将 GameObject 的 activation 位写入 engine event mask；
`func73761/f_zbed` 消费 `4702216/4702220` 两个 activation mask，并对 GameObject 的 component list
调用 vtable slot 44。MeshCollider vtable `3221476` 的相关项逐字解码为：

```text
slot 42 -> func72949 / f_twcd
slot 43 -> func72952 / f_wwcd
slot 44 -> func73295 / f_bkdd

f_bkdd(activeSelf, activeInHierarchy, 0)
  -> 两个 active bit 都为真时：slot43 f_wwcd，再 slot42 f_twcd
  -> 状态下降时：按 bit 组合调用相应的同一组 slot
```

`f_wwcd` 读取既有 collider shape、Transform 和 attached Rigidbody，走 `f_kjdd` 的 transform 比较/更新；
必要时调用 `f_ajdd` 写入 shape-side transform。`f_twcd` 刷新 collider runtime state，最后经
`f_jjdd -> f_xidd` 对 attached Rigidbody 做既有的 mass-properties sync 分派。故 Unity `SetActive`
不是 `removeActor/addActor`，也不只是 `SIMULATION_SHAPE` flag，而是**保持 actor/shape identity 的
shape refresh + activation event + wake/sleep/mass-sync 生命周期**。

这将下一步收敛成可逐字段验证的本地任务：在本地 `activate_stationary/start_motioninfo` 完成后，导出
actor core、shape core、shape flags、sleep/wake、mass/COM/inertia 及 contact-manager 创建前状态；与 Unity
同一 `SetActive` 后、first PCM 前的原生窗口对齐。只有发现第一处不同字段，才改
`PersistentPhysxFrontHalfScene`；不能根据这条函数链直接猜测 add/remove 次序或重扫 endpoint。

补充核验：Rigidbody vtable `3222248` 在 slot 43 后已结束，并无 slot 44；所以 `f_zbed` 遍历的不是
GameObject 的完整 7-component 数组，而是 activation-participant 子表。Rigidbody 没有另一条独立的
slot44 activation callback；其 physics-side mass sync 已由 MeshCollider 的 `f_twcd -> f_jjdd -> f_xidd`
附带触发。故不能把 Rigidbody 再列为第二个生命周期未知项。

#### 2026-07-11：post-activation pose 是本地 transform-refresh 适配，不是候选根因

以相同六条连续 session 做了唯一开关 A/B：保留本地 `SIMULATION_SHAPE` 启用后的第二次 pose 写入时，
14000 在 step `1560` 首碰并有 `2` contacts，六条均能自然到达 first contact；去掉该写入时，14000
在 step `1` 就以 `4` contacts 撞上 disabled 期间的旧 broadphase pose，active 距真实 entrance `26.98m`。
证据：

```text
data/calibration/persistent_scene_sequence_activation_bridge_baseline_20260711.json
data/calibration/persistent_scene_sequence_activation_bridge_no_postpose_20260711.json
```

原因是 scalar pyphysx 对 disabled `SIMULATION_SHAPE` 的 actor pose 写入不会立即刷新 broadphase；Unity
`f_wwcd` 则在 `f_twcd` 前执行专用 transform/shape refresh。本地第二次 pose 是这条 refresh 的必要适配，
不是额外 Unity setter，也不是 2/4-contact 根因，后续 baseline 必须保留它。

#### 2026-07-11：`OnOverlapCreatedTask` runtime 证据闭合了 Unity 的创建输入与预分配 identity

本节不再从 endpoint 或 manager 编号猜测创建顺序。新的单一 `14000` 受控日志已经在真实
`Sc::Scene::OnOverlapCreatedTask`（table `120736` / `func71504`）读取 task 的三组预分配数组。
此前 probe 把 task 的 `+40/+44/+48` 错误命名成 touch 输出；按 `ScScene.cpp` 的真实布局，它们分别是
`PxsContactManager**`、`ShapeInteraction**`、`ElementInteractionMarker**`。probe 字段名已修正，旧日志仍由
解析器兼容读取。

```text
原始日志： log/overlap_created_probe_20260711_160604/
             unity_runtime_probe_20260711_160605/events.jsonl
解析器：   tools/reverse/extract_overlap_created_timeline.py
产物：     data/calibration/overlap_created_timeline_20260711.json
```

真实 stone-stone overlap 的输入和紧随其后的 task 状态为：

```text
OnOverlapCreatedTask 输入 volume 顺序： target -> active
预分配 contact manager：             275165968
预分配 ShapeInteraction：            278002840
first PxsCMDiscreteUpdateTask：       3 个 manager 中 taskIndex=1
taskIndex=1 manager 指针：            275165968（与预分配指针相同）
work-unit：                           flags=611, status=0, frictionPatchCount=0
                                     transformCache=(12,9), edgeIndex=2,
                                     mNpIndex=0x80000008（new-list）
随后 first finalizer：               2 contacts
```

源码与运行时一致：`OnOverlapCreatedTask` 先把 broadphase 的 `volume1/volume0` 传给
`createRbElementInteraction`，`createShapeInteraction` 再按 dynamic rigid ID 排为 solver-facing 的
`active -> target`。因此 Unity 的真实路径不是“按启用先后直接 addActor”，也不是“broadphase 输入本身
就是 active -> target”。本地 `shape-flag` 路径只复现了 2 contacts 而 body role 仍反向；本地
`remove/add` 路径只复现了 body role 而变成 4 contacts。两者都不能替代 Unity 的这条已捕获创建路径。

这也排除了一个笼统说法：不能再把未知描述为“Unity 的 broadphase pair 输入顺序”。该输入已经捕获。
尚未对齐的是本地在相同创建边界上如何形成 **同一 solver-facing work-unit 以及其首次
`PxcDiscreteNarrowPhasePCM` 实际读取的 transform-cache/cache 状态**。下一步不再调用 Unity：只在本地
scalar PhysX 的 `PxcDiscreteNarrowPhasePCM(context, workUnit, cache, output)` 边界导出该三元组，并同上述
Unity `taskIndex=1` 状态逐字段比较。只有找到第一个不同字段，才修改本地 activation bridge。

#### 2026-07-11：本地函数级 trace 证实 8.5mm 偏移的上游因果

为避免再从 finalizer 或 endpoint 倒推，本地 scalar PhysX 增加了只读的
`PxcDiscreteNarrowPhasePCM(context, workUnit, cache, output)` callback。它直接导出 work-unit、两条
`PxsTransformCache` 的实际 transform、`NarrowPhaseParams`、`Gu::Cache` 与输出；不修改任何
PhysX 内存。实现涉及本地审计构建 `PxcNpBatch.cpp` 和 pyphysx 绑定，生产训练接口不调用它。

同一 `14000` 的 `remove/add actor` 分支（这是此前唯一能得到 `active -> target` 的本地反事实）在
**真实函数入口**的 first convex-convex 状态为：

```text
workUnit: flags=611, status=0, geom=(convex,convex), new-list
local transform-cache IDs: 2 / 1          （Unity 为 12 / 9；编号本身不是可手填参数）
local active P - Unity PCM P: (-30.517578125um, 0, 0)
local active yaw - Unity PCM yaw: -0.000302781346rad
local PCM output: 4 contacts
```

接着只在最后一个本地 fixed tick 前补入上述**已测量**的 X/yaw 差，不改变 hull、cache、材质、solver、
manager flag 或任何碰撞参数。新 trace 验证实际送入 `PxcDiscreteNarrowPhasePCM` 的 position 三分量均为
`0` 差，quaternion 最大分量差 `1.49e-8`；同一个 local Scene 的输出立即变为 `2 contacts`，两点位置为：

```text
(-69.71715546, 14.30478477, 54.16677475)
(-69.71759796, 14.30478477, 54.16381073)
```

这与 Unity 的 2-contact 分支一致，且证实此前约 `8.5mm` 的 solver-facing 切向点误差是这个
micro-pose 分叉的**下游**，不是独立的 hull、PCM cache、friction 或 SolverContact 公式问题。
完整证据：

```text
data/calibration/p5_14000_narrowphase_pose_causality_20260711.json
tools/reverse/summarize_p5_14000_narrowphase_pose_causality.py
```

范围必须严格限定：此处的补偿是 oracle **诊断**，绝不能进入训练后端。因此私有 Scene lifecycle
尚未以生产方式闭合，但未知项已从“如何得到某个神秘 2-contact manager”收缩为：
**本地 activation bridge 在 active->target 路径中，哪一次 actor/shape transform-cache 写入或 fixed-step
相位导致这 `30.5um / 0.000303rad` 没有自然与 Unity 相同。** 下一步只沿
`activate_stationary/start_bestshot -> transform cache refresh -> first fixed simulate` 比较本地状态，目标是
无 oracle 使该函数入口逐字段相等；不得把测得的修正量硬编码。

#### 2026-07-11 更正：微 pose 差不是 `SetActive` 独有；完整闭合需两条链同时成立

紧接着把同一 `14000` 的两个本地路径按真正 `PxcDiscreteNarrowPhasePCM` 入口复核：

```text
shape-flag only（solver-facing target -> active）：
  active P - Unity = (-30.517578125um, 0, 0)
  active yaw - Unity = -0.000302781346rad
  output = 2 contacts（但切向 point 仍偏）

remove/add actor（solver-facing active -> target）：
  active P - Unity = (-30.517578125um, 0, 0)
  active yaw - Unity = -0.000302781346rad
  output = 4 contacts

Unity：
  active -> target + Unity exact PCM transform
  output = 2 contacts
```

因此前一节不能把全部微 pose 差归因于 private `SetActive`：它在两条本地路径中相同，发生在更早的
`Newfrictionstep` 速度写入后、local scalar PhysX 与冰面接触的连续推进。`SetActive`/pair lifecycle
仍是另一条独立且必要的链：它决定 local Scene 是 `target -> active / 2 points`，还是
`active -> target / 4 points`。要生产闭合，必须同时满足：

1. 前半段自然将 active PCM transform 对到 Unity，消除 `30.5um / 0.000303rad`；
2. 不用 oracle 复现 Unity 的 `active -> target` 新 pair 生命周期，同时仍保留 2-contact reduction。

所以后续禁止把“补精确 pose 后得到 2 contacts”误写成 lifecycle 已完成；它只证明两条链的耦合方式。
下一项先审计二者共同经过的 scalar Scene stone-ice 推进路径（runtime ice 的 midphase/BVH traversal 与
transform-cache 写入），不重新打开已排除的 hull、PCM 公式、cache feature 或 solver 参数。

#### 2026-07-11：标准单壶采样完成；active 的首次 `Start` 已逐 API 解码

本轮已改回标准浏览器启动器，不使用 proxy。受控 `14000` 已完整完成并保留原始证据：

```text
log/unity_standard_probe_20260711/unity_runtime_probe_20260711_145542/events.jsonl
data/calibration/mesh_collider_bridge_standard_single_shot_20260711.jsonl
data/calibration/mesh_collider_bridge_timeline_20260711.json
```

`SetActive` 时间线给出了一个必须区分的事实：target stone 8 的 call 30 启用会进入
`MeshCollider.slot44 -> slot43(transform refresh)`；active stone 0 曾在 call 4、22 被停用，随后在
call 38 启用时**不**进入 slot42/43/44，而是紧接着第一次执行
`CurlingStoneNew.Start`（table 10894 / `func61028`）。这不是 hook 漏记：三个 slot 都已同时安装，
全局 bridge 记录只有 target 的两条。

`func61028` 里四个 `f_vkb` 字符串指针已从 Wasm data segment 直接解为 Unity API：

```text
mCollision / allowSweep = false
rb = GetComponent<Rigidbody>()
origin_position = rb.position
rb.centerOfMass = Vector3.zero
rb.constraints = 80  // FreezeRotationX | FreezeRotationZ
GetComponent<Collider>().material.dynamicFriction = 0
```

因此 `Start` 不是隐含的 shape/contact-manager 注册调用。local Scene 原本已经使用 X/Z angular lock，
`BESTSHOT` 也会在出手时把 active 的材质摩擦置为零；但 cooker 默认留下了约 `1e-9` 的 COM 浮点残值。
现已在 `_make_stone()` 显式执行 `set_center_of_mass_local_pose(identity at zero)`，本地审计为严格
`(0,0,0)`。这是一项真实 native 对齐修正，但它不可能单独造成 8.5mm 的切向 contact-point 平移。

所以本轮没有重开 hull、cache、PCM、friction 或 solver 假设：已排除的 `Start` 写入已闭合；剩余边界仍是
**已有 Collider 的 Unity-native activation/pair registration 历史**。下一步只比较该 history 进入
`createShapeInteraction` 前的 actor/shape registration state，不能把 `Start` 或 COM 当作 P6 的根因。

#### 2026-07-11：控制协议的 reset 预演化与本地强制 sleep 已做反证

标准 sampler 在 `RESETPOSITION -> RESETSTATE` 后固定等待 `0.2s` 才发 `BESTSHOT`
（`controlled_scene_sampler.py --reset-settle-seconds=0.2`）。新日志也确实在 target 的
call 30 `SetActive(true)` 与 active 的 call 38 之间记录到 42 次
`PxsContext.contactManagerDiscreteUpdate`，每次 `dt=0.01`，并有一次 target 的 stone-ice
`OnCollisionEnter`。这说明本地旧审计只用 `settle_steps=1` 是一个真实的**时相差异**，必须单独验证，
但不能直接假定它是根因。

同一条 `14000` 做了两组只改生命周期时相的离线 A/B：

```text
A: settle_steps=1,  reset 后强制 sleep（旧基线）
B: settle_steps=20, reset 后自然保持 wake（匹配 sampler 的 0.2s）

first-contact step:             1560 / 1560
first-contact count:            2 / 2
active/target entrance P/Q/v/w: 完全相同
first report 两个 point:        完全相同
```

因此 target 在出手前的 0.2s ice 预演化、以及 local `put_to_sleep()` 的时机都不是当前
8.5mm solver-facing ContactBuffer 切向偏移的主因。`reset_positions()` 仅保留
`force_sleep_after_reset` 诊断开关，默认仍为旧行为；不得把 20 tick 或不睡眠作为训练修复。
剩余边界继续收缩到：**两端已有 shape 的 Scene interaction 注册记录如何决定新
active-target pair 的 contact-manager/work-unit 内部顺序和 full-manifold reduction 输入。**

#### 2026-07-11：已定位 interaction 的唯一创建 task；等待一次窄运行时证据

从 Unity Wasm task-name data 和 `ScNPhaseCore.cpp` 源码交叉定位到：

```text
OnOverlapCreatedTask table 120736 -> func71504
func71504 -> func71692 (f_kabd)
func71692 -> Sc::NPhaseCore::createRbElementInteraction / createShapeInteraction
```

这正是 broadphase overlap 被正式变成 `ShapeInteraction + PxsContactManager` 的边界，比现有
`PxsContext.contactManagerDiscreteUpdate` 更早。现已在
`tools/reverse/unity_webgl_runtime_probe.js` 增加只读 `installOverlapCreatedHook()`；它会记录 task 的
`NPhaseCore`、每个 overlap 的两个 volume、pair data 和三组输出位。启动器新增
`--overlap-created-hook`，`launch_pair_lifecycle_probe.py` 默认携带该参数。

此 hook 不写 Wasm 内存、不改变 filter、cache、shape 或 solver。现有日志没有此 task 的 before/after，
所以不能从旧 JSON 事后推导；下一次只需一条受控 `14000`，即可将 Unity overlap pair 的实际创建顺序
和本地 `Sc::NPhaseCore::createShapeInteraction` 的输入逐项比对。通过前不能把 actor add/remove、
sleep 时机或 pair index 当作修复。

#### 2026-07-11：首次 `func73295` runtime hook 更正了 activation 分支假设

受控 14000 runtime capture `log/mesh_collider_activation_probe_20260711/unity_runtime_probe_20260711_140850/events.jsonl`
实际命中一次 MeshCollider `func73295/f_bkdd`，参数为 `(component, 1, 0, 0)`。按函数体，这会只调用
slot 43 `f_wwcd` 后返回，**不会**调用 slot 42 `f_twcd`。同次 before/after 的 192-byte component window
和 320-byte collider-backend window 均无字节变化。

因此上一节把“SetActive active 分支必然按 slot43 后 slot42 执行”作为 runtime 结论是不准确的；它仅是
`f_bkdd` 的一个静态条件分支。当前已确认的事实是：SetActive 路径至少触发 `f_wwcd`，但 `f_twcd` / mass
sync 是否由其它直接 call site 在同一状态转换中触发尚未记录。下一 probe 只 hook table `122156/f_wwcd`
与 `122155/f_twcd` 的直接调用，不更改任何本地 Scene 参数或重开 endpoint 采样。

#### 2026-07-11：14000 启用对象已映射，slot44 不是活动壶的完整边界

同一份受控运行的 sampler 明确指定 `active_index=0`、`target_index=8`，因此可将 runtime
`SetActive` 事件精确对应为：

```text
call 30: target stone 8, MeshCollider=313234928
         -> 命中 func73295(slot44), args=(component, 1, 0, 0)
         -> 只转入 func72952(slot43/f_wwcd)

call 38: active stone 0, MeshCollider=313086576
         -> 同样 SetActive(true)，但未命中 func73295(slot44)
```

原始证据：

```text
log/mesh_collider_activation_probe_20260711/
  unity_runtime_probe_20260711_140850/events.jsonl
data/calibration/mesh_collider_activation_single_shot_20260711.jsonl
```

目标壶 slot43 调用前后，已导出的 `192B MeshCollider component` 与 `320B collider backend` 均逐字节不变；
这与源码一致：`f_wwcd` 的可见工作是计算 transform 是否变化，再通过其内部虚调用把刷新提交给更深层的
physics bridge。因此“slot44 未改本体字节”不能解释为没有 native effect。

这次采样已经否定一个错误简化：活动壶并非必然经 `slot44` 进入物理刷新。为观察其真实分支，probe 已扩为
同时只读 hook `slot43/f_wwcd` 与 `slot42/f_twcd`，分别记录两颗壶的 component/backend 前后状态；它不改变
Wasm 内存、hull、PCM cache、材质或任何本地 Scene 参数。此前采样仍保留，且在直接调用这两个入口前不能把
“活动壶没有 slot44”误写成“活动壶没有 Collider refresh”。

本地侧同步新增 `PersistentPhysxFrontHalfScene.activation_audit_state()`；它在不改变 Scene 的前提下导出
actor pose/velocity/sleep、mass/COM/inertia、lock flags、shape simulation/local pose/contact offset、material
及 in-scene 状态。该接口已在 scalar pyphysx 环境做 JSON 序列化复验，供下一份 runtime bridge 日志逐字段
比较，不能用于向训练代码灌入 Unity oracle。

#### 2026-07-11：历史文档回查收敛了共同 micro-pose 的边界

对 `01_single_stone_motion`、`05_physx_contact_generation`、`06_physx_solver`、`08_sampling_runtime_records`
和 `13_physx_native_state_equivalence` 的回查确认：这不是一个尚未记录的自由方向。

```text
Unity fixed tick:
  Newfrictionstep(..., 0.001)
  -> 写 Rigidbody linear/angular velocity
  -> PhysX fixed simulate(0.01)
  -> 读回 P / Q / v / w
```

其中 `Newfrictionstep` Wasm 与 Python 翻译已逐 tick 对齐；旧的 14000 "native Y 高一个 ULP" A/B
严格证明 PCM 对石壶-冰面支撑高度的微差敏感，但它是较早 two-stone 入口边界，不能直接套为当前
16 壶 `active -> target` 生命周期的生产修复。当前 source-level trace 的共同差是 active PCM 输入
`X=-30.517578125um`、`yaw=-0.000302781346rad`，且同时存在于 shape-flag 与 remove/add 两条本地
pair 路径；故它不由 SetActive 单独造成。

同一 14000 的本地 fast-midphase/BVH33 A/B 也没有改变这组 first-PCM 输入差或 4-contact 输出，
因此不能把简单切换本地 BVH 路径当作修复。历史中已存在 `PxcPCMContactConvexMesh` 61 组 before/after
记录及 stone-rink static-solver 路径定义；下一步只复用这些记录和本地函数级 trace，对比末个
fixed tick 的 stone-ice narrowphase 输入、static constraint/writeback 与 transform-cache 更新，定位第一处
P/Q 分叉。不得重开 hull、PCM 参数、摩擦扫描或把 oracle micro-pose 写入训练后端。

#### 2026-07-11：暂停实验后的全链路证据盘点

本节只整理既有中文文档和已保存报告，不引入新的采样或参数实验。目的不是重述所有历史过程，
而是严格区分“已在对应边界闭合”与“不能由该结论外推的 Scene 层”。

| 层级 | 已闭合或已反证的事实 | 仍未证明的内容 |
|---|---|---|
| 协议/脚本时序 | `BESTSHOT` 的 SetActive、材质置零、velocity/omega 写入；`FixedUpdate` 的 `Newfrictionstep -> simulate(0.01)`；14002/14004 的 trailing physics step 都已由 runtime/受控 A/B 确认。 | 一次 fixed step 内 Unity 与本地 stone-ice solver/task 的精确执行顺序。 |
| 自定义滑行 | Wasm `Newfrictionstep` 对同一噪声流逐 tick 对齐，非 Python 数学或 RNG 分叉。 | 写回 Rigidbody 后，PhysX 读取 velocity/omega、解 stone-ice 约束并积分 quaternion 的中间状态。 |
| 石壶/冰面几何 | stone runtime hull、BigConvex、Unity ice vertices/triangles/faceRemap/BV4 均有字段或 byte 级真值；source-once cooking 已验证。 | 本地 scalar Scene 的可执行 BVH33 fallback 与 Unity WebGL 运行时 stone-ice task 的逐 tick native 等价性。不能把 cooked object 相同外推成整场 traversal/solve 顺序相同。 |
| direct scalar PCM | exact Unity entrance 下六条 contact count、point、normal、separation 均到 float32 ULP；SSE/scalar 分叉已解释。 | 这不证明持久 `PxScene` 的 work-unit 角色、cache 和 transform-cache 写入等价。 |
| PCM cache | task-local `numContacts/warmStart` 清零、feature bytes 保留已验证；clearManifold 开/关 A/B 排除它作为首帧 2/4 根因。 | 首碰后的多 tick cache/anchor 演进仍属 P6，但不能再解释 first ContactBuffer。 |
| solver | ContactBuffer 到 normal/friction row、single-pair dynamic/static consume 与 with-writeback 都可用 Unity raw 重放到 float 精度；mass、solver iteration、yaw inertia 和第一笔材质切换已校正。 | 连续 Scene 在 stone-ice 与 stone-stone 多约束间的实际 pre-solve body state、batch 排序和写回时相。 |
| SetActive/pair | Unity 每 shot 都由 new-list 创建 manager；overlap 输入是 `target -> active`，solver-facing work-unit 为 `active -> target`；高层启用顺序、component activation 链和本地 post-pose refresh 的必要性均已确认。 | 本地如何以保持 actor/shape identity 的方式形成 Unity 同样的 `active -> target` 且 2-contact 的新 pair。remove/add 与 shape-flag 各只复现一半。 |
| micro-pose | 本地真实 `PxcDiscreteNarrowPhasePCM` 入口相对 Unity 差 `X=-30.517578125um`、`yaw=-0.000302781346rad`；仅作 oracle 诊断时补齐会把 active->target 本地输出从 4 点变为 2 点。 | 这两个差在 shape-flag 和 remove/add 路径中相同，故其来源不是 SetActive/pair lifecycle 独有；必须在最后的 stone-ice fixed step 向上定位。 |

由此，原问题“本地激活壶时哪一次 position/quaternion/transform-cache refresh 少了”必须拆为两条
不可互相替代的证据链：

```text
A. common micro-pose chain
   Newfrictionstep write
   -> last stone-ice narrowphase / static constraint solve
   -> body linear/angular writeback
   -> pose integration
   -> PxsTransformCache consumed by first stone-stone PCM

B. private pair lifecycle chain
   existing actor/shape activation state
   -> broadphase overlap
   -> ShapeInteraction / contact-manager creation
   -> work-unit role order and first full-manifold reduction
```

链 A 的输出决定那 `30.5um / 0.000303rad` 是否自然消失；链 B 的输出决定相同 pose 下是否成为
Unity 的 `active -> target / 2 contacts`。两条都必须闭合，不能用 A 的 oracle pose 冒充 B 完成，
也不能用 B 的 actor add/remove 冒充 A 完成。

下一步只允许按下列已有或可由既有日志提取的边界逐项对照：

1. 最后一个 pre-contact fixed tick 的 active Rigidbody 写入后 `v/w`，以及它进入 stone-ice
   `PxcPCMContactConvexMesh` 时的 transform-cache 内容。
2. 同 tick 的 static contact `ContactBuffer`、`solveContact_BStaticBlockWithWriteback` 前后
   `PxSolverBody` 线/角速度，以及 pose integration 后 actor `P/Q`。
3. 该 actor `P/Q` 从 actor core 写入 `PxsTransformCache` 的调用点和时序；这是链 A 中唯一仍未
   逐字段观测的 refresh 边界。
4. 独立地读取 active/target ShapeInteraction 创建后的 shape/rigid role、manager/work-unit，验证链 B。

在第 1--3 项没有找到第一处差异前，禁止把“activation hook 未命中 slot44”、BVH toggle、sleep/settle、
cache clear、材质 callback、hull 或 contact 参数重新列为候选修复。

当前执行约束与证据状态统一见：
`docs/unity_reverse/15_persistent_scene_alignment_ledger.zh.md`。

#### 2026-07-11：A0-min 更正，actor-to-cache refresh 已排除

随后以受控 `14000` 在首次 dynamic-dynamic manager（`flags=611`、cache `(12,9)`）只读抓取两端
`PxsRigidCore.body2World` 和紧随其后的 `PxcPCMContactConvexConvex` 输入 transform。两对 `q/p` 逐 float
相同，审计为：

```text
tools/reverse/audit_a0_actor_core_cache.py
data/calibration/a0_actor_core_cache_14000_audit_20260711.json
```

因此上文第 3 项不再是当前未知：Unity 没有在 actor core 已正确的前提下漏写或晚写
`PxsTransformCache`。本地相对 Unity 的 `30.5um / 0.000303rad` 必须在 actor core 形成之前追踪，
即最后一次 stone-ice static writeback 或 pose integration；不得再把 activation/cache refresh 作为该
micro-pose 的候选修复。pair lifecycle 链仍独立保留。
