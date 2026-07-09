# 碰撞入口、任务图与接触表

记录正式碰撞/触发行为、PhysX 模块证据、任务图、contact finalization 表和 narrowphase 表定位。

> 原长文档已封存：[`UNITY_REVERSE_ENGINEERING.zh.2026-07-07.archive.md`](../archive/UNITY_REVERSE_ENGINEERING.zh.2026-07-07.archive.md)。以后维护以本目录子文档为准。

## 已恢复的碰撞/触发行为

`CurlingStoneNew` 字段：

```csharp
public bool mCollision;      // 0x10
public bool allowSweep;      // 0x11
private Rigidbody rb;        // 0x14
private Vector3 origin_postion; // 0x18
public AudioSource source;   // 0x24
```

`CurlingStoneNew.OnCollisionEnter` 对应 wasm `func61030`。它会把碰撞对象的 tag/name
与两个字符串比较；metadata 解析后已经能命名为 `Stone` 和 `Wall`。

碰到 `Stone` 时：

```text
mCollision = true
GetComponent<Collider>().material.dynamicFriction = 0.6
GetComponent<Collider>().material.staticFriction = 0.6
如果 source != null，则 source.Play()
```

碰到 `Wall` 时还会额外：

```text
Rigidbody.velocity = Vector3.zero
Rigidbody.angularVelocity = Vector3.zero
stone.GameObject.SetActive(false)
```

这意味着多壶和墙体行为不是纯 `Newfrictionstep`；Unity collision callback 会改变
碰撞体材质/对象状态，并且一旦 `mCollision` 置位，自定义单壶 stepping 路径就会停止。

## RESET/出手路径的状态重置证据

2026-07-08 继续反编译 `DCP.HandleMessage` / `DCP_HumanVSAI.HandleMessage`
的 `RESETSTATE/RESETPOSITION/BESTSHOT` 周边逻辑后，当前可确认：

```text
f_nlbc  = UnityEngine.GameObject.SetActive
f_aubc  = UnityEngine.Transform.set_position_Injected
f_vbva  = UnityEngine.Rigidbody.set_velocity
f_ybva  = UnityEngine.Rigidbody.set_angularVelocity
f_lbva  = UnityEngine.PhysicMaterial.set_dynamicFriction
f_mbva  = UnityEngine.PhysicMaterial.set_staticFriction
```

正式出手路径会把 active stone 的 PhysicMaterial `dynamicFriction/staticFriction`
都置为 `0.0`，随后设置 Rigidbody 速度/角速度。`OnCollisionEnter(Stone)`
再把碰撞壶材质摩擦置回 `0.6/0.6`。

`RESETSTATE/RESETPOSITION` 路径会 `SetActive`、写 `Transform.position`，
并清 `Rigidbody.velocity/angularVelocity`，也会清 `CurlingStoneNew.mCollision`。
但在已检查的 reset 主路径附近没有看到 `Transform.set_rotation`、
`Transform.set_localRotation` 或 `Transform.SetPositionAndRotation`。因此受控采样如果
连续复用同一个 stone index，只重置平面位置而不重置三维姿态，是一个真实风险。
这会让凸 MeshCollider 的接触流形携带前一次样本的姿态历史。

`CurlingStoneNew.OnTriggerEnter` 对应 `func61031`。它会切换 `allowSweep`，
并调用与 `Midline` / `Hogline2` 相关的 controller 方法。

现在已确认的两个 trigger：

```text
Midline  -> allowSweep = true，然后按当前 scene 调 controller 的 motion-info 处理
Hogline2 -> allowSweep = false
```

`OnTriggerEnter` 同样按 scene name 分发。`recordedGame == false` 时发送真实 `MOTIONINFO`；
`recordedGame == true` 时普通 `DCP/FastDCP/HumanVsAI` 跳过发送，`AutoDCP` 改为从记录文件读取：

```text
FastGame:
  if !FastDCP.recordedGame:
      FastDCP.SendMotionInfo()

AutoGame:
  if AutoDCP.recordedGame:
      AutoDCP.ReadMotionInfoFromRecord()
  else:
      AutoDCP.SendMotionInfo()

HumanVsAI:
  if !DCP_HumanVSAI.recordedGame:
      DCP_HumanVSAI.SendMotionInfo()

default DCP:
  if !DCP.recordedGame:
      DCP.SendMotionInfo()
```

另一个 trigger 类 `CrossLineEvent.OnTriggerEnter` 也已经解析。它只用于切相机：

```text
if collider.gameObject.name == "Hogline1":
    GameObject.Find("CameraControl").GetComponent<CameraControl>().SendMessage("SwitchCamera", 3)

if collider.gameObject.name == "Hogline2":
    GameObject.Find("CameraControl").GetComponent<CameraControl>().SendMessage("SwitchCamera", 4)
```

所以 `CrossLineEvent` 不是物理或判罚核心。

全局查找 `OnTriggerEnter`/`OnCollisionEnter` 后，正式物理相关类只有：

```text
CrossLineEvent.OnTriggerEnter
CurlingStoneNew.OnCollisionEnter
CurlingStoneNew.OnTriggerEnter
MotionTestStone.OnTriggerEnter
MotionTestStone.OnCollisionEnter
```

还有一个 `MotionTestStone` 测试类，里面有两个碰撞辅助公式：

```text
Lambda1(m1, m2, u, e, v, theta)
  = m1*m2*u*(e + 1)*v*cos(theta) / (m1 + m2)

Lambda2(m1, m2, u, e, v, theta)
  = sin(theta)*v / (3/m1 + 3/m2)
```

构造函数默认值：

```text
u = 0.1
e = 1.0
m = 19.1
R = 0.145
```

但是恢复出的 `MotionTestStone.OnCollisionEnter` 并没有调用这些公式，而且正式比赛壶类是
`CurlingStoneNew`。所以这些 helper 是开发者碰撞实验的有用证据，不是比赛多壶碰撞路径。

更进一步，资产检查显示 `MotionTestStone` 只挂在 `level1` 的测试壶上；正式比赛场景的 16
个石壶挂的是 `CurlingStoneNew + CrossLineEvent + ExtendedColliders3D`。因此这些 Lambda
不是正式比赛多壶碰撞路径。

## 碰撞侧剩余未知与 PhysX 深挖


### 4. 多壶碰撞细节

冰壶对象不是纯自定义物理。`CurlingStoneNew` 有：

```csharp
public bool mCollision;
public bool allowSweep;
private Rigidbody rb;
private void OnCollisionEnter(Collision collision);
private void OnTriggerEnter(Collider collider);
```

`CurlingStoneNew.OnCollisionEnter` 的 `Stone`/`Wall` 分支已经命名。另一个碰撞 helper
`MotionTestStone` 类还含有 `Lambda1`、`Lambda2`、`m1`、`m2`、`u`、`e`、`m`、`R`。
但 `MotionTestStone` 只挂在 level1 的测试石壶上；正式比赛石壶挂的是
`CurlingStoneNew + CrossLineEvent + ExtendedColliders3D`，且 `MotionTestStone.OnCollisionEnter`
本身也没有调用 `Lambda1/Lambda2` 改写速度。

现在已恢复的碰撞几何与 PhysX 设置：

```text
stone MeshCollider: ExtendedColliders3D runtime generated cylinder
stone collider material: Bouncy
stone local collision radius: about 0.14375m
stone formal-scene world collision radius: about 0.140875m
stone MeshCollider convex: true
stone cylinder faces: 256
stone generated mesh: 512 vertices, 3060 indices, 1020 triangles, flipFaces=true
stone Rigidbody mass: 19.1
stone Rigidbody drag/angularDrag: 0 / 0.05
stone Rigidbody collisionDetection: 0 for formal stones
stone Rigidbody serialized constraints: 0
stone runtime constraints: 80  // CurlingStoneNew.Start sets FreezeRotationX | FreezeRotationZ, yaw remains free
stone serialized centerOfMass: (0, 0, 0)
stone runtime centerOfMass: Vector3.zero
stone serialized inertiaTensor: (1, 1, 1)
stone serialized inertiaRotation: identity
global solver iterations: 6
global solver velocity iterations: 1
default contact offset: 0.01
bounce threshold: 0.05
default max depenetration velocity: 10
solver type: 0
broadphase type: 0
contacts generation: 1
contact pairs mode: 0
adaptive force: false
enhanced determinism: false
improved patch friction: false
default PhysicsMaterial: None
```

`m_InertiaTensor=(1,1,1)` 是资源序列化值；运行时 `ExtendedColliders3D.Awake()` 生成 convex
`MeshCollider` 后已经确认会触发 Rigidbody mass properties sync。因此 solver 最终惯量
不应直接取序列化 `(1,1,1)`，而应来自 runtime cooked convex shape 自动重算。

2026-07-08 追加恢复了 `CurlingStoneNew.Start`，对应 wasm `func61028`。它在运行时做了三件
和碰撞强相关的初始化：

```text
rb = GetComponent<Rigidbody>()
rb.centerOfMass = Vector3.zero
rb.constraints = 80
GetComponent<Collider>().material.dynamicFriction = 0.0
```

其中 `constraints=80` 按 Unity `RigidbodyConstraints` 枚举解释为
`FreezeRotationX | FreezeRotationZ`，也就是锁住横滚/俯仰，只允许绕竖直轴 yaw。
这修正了此前“运行时仍是 constraints=0”的误读。`centerOfMass` 用到的 `Vector3` 静态对象
与 `OnCollisionEnter(Wall)` 清 `velocity/angularVelocity` 时相同，因此这里可按
`Vector3.zero` 处理。

2026-07-08 已进一步确认 `ExtendedColliders3D.Awake` 的 wasm 映射：

```text
ExtendedColliders3D.Awake
  method pointer 12126
  wasm function $f59928
  decompile file D:\esp\tmp\curling_reverse_il2cpp\dcmp_funcs\func59928.dcmp
```

`func59928` 的业务层调用只有：

```text
GameObject.AddComponent<MeshCollider>()
Collider.set_enabled(...)
MeshCollider.set_sharedMesh(generateMesh(false))
MeshCollider.set_convex(...)
Collider.set_isTrigger(...)
Collider.set_material(...)
Object.Destroy(this)
```

同一路径没有调用 `Rigidbody.set_mass`、`Rigidbody.set_inertiaTensor`、
`Rigidbody.set_inertiaTensorRotation`、`Rigidbody.ResetCenterOfMass` 或
`Rigidbody.ResetInertiaTensor`。所以当前可锁死的是：“业务 C# 层没有显式改惯量”；
native 层的 `sharedMesh/convex` rebuild 则会隐式更新 attached Rigidbody mass properties。

2026-07-08 又把这一步固化成可复查脚本：

```powershell
python tools\reverse\summarize_rigidbody_mass_writes.py
```

该脚本用 `script.json -> wasm_table_map.json -> build.dcmp` 三源交叉解析，避免把
`ScriptMethod.Address` 误当成 `d_[index]` 元数据槽。当前输出中的质量属性写入为：

```text
UnityEngine.Rigidbody.set_mass
  RosSharp.Urdf.UrdfInertial.Create

UnityEngine.Rigidbody.set_inertiaTensor
UnityEngine.Rigidbody.set_inertiaTensorRotation
UnityEngine.Rigidbody.ResetCenterOfMass
UnityEngine.Rigidbody.ResetInertiaTensor
  RosSharp.Urdf.UrdfInertial.ImportInertiaData / UpdateRigidBodyData

UnityEngine.Rigidbody.set_centerOfMass
  RosSharp.Urdf.UrdfInertial.Create / UpdateRigidBodyData
  CurlingStoneNew.Start
```

也就是说：正式石壶业务路径只显式调用
`CurlingStoneNew.Start -> Rigidbody.set_centerOfMass(Vector3.zero)`；`set_mass`、
`set_inertiaTensor`、`set_inertiaTensorRotation`、`ResetCenterOfMass`、
`ResetInertiaTensor` 全部没有落到 `CurlingStoneNew`。这些命中集中在
`RosSharp.Urdf.UrdfInertial.*`，属于 URDF 车体/机器人导入逻辑，不是正式比赛石壶。
所以当前可以锁死的是：**COM 被 C# 层在 Start 写成 zero；stone mass/inertia tensor
没有被 C# 业务层显式覆盖。**native 层继续追完后，又可以锁死：
runtime convex `MeshCollider` rebuild 会调用 attached Rigidbody 的 mass-properties
sync；最终 inertia tensor 来自 cooked convex shape 自动重算，而不是 C# 业务层显式写入。

继续从 Unity internal-call 注册表往 native 层追，Rigidbody mass properties 的自动/显式
开关已经可以命名，而且字段名来自 Unity 自己的 Rigidbody 序列化函数：

```text
a[85]  = m_ImplicitCom
a[100] = m_ImplicitTensor

UnityEngine.Rigidbody::set_centerOfMass_Injected
  table ptr 129366 -> func82515 -> func73033
  func73033: a[85] = 0;  写 COM；同步到 PxRigidBody 的 CMassLocalPose；调用 f_abdd

UnityEngine.Rigidbody::set_inertiaTensor_Injected
  table ptr 129370 -> func82519 -> func73032
  func73032: a[100] = 0; 写 inertia tensor；调用 f_abdd

UnityEngine.Rigidbody::set_inertiaTensorRotation_Injected
  table ptr 129368 -> func82517 -> func73031
  func73031: a[100] = 0; 写 inertia rotation

UnityEngine.Rigidbody::ResetCenterOfMass
  table ptr 129375 -> func82524
  func82524: a[85] = 1; 调用 f_abdd

UnityEngine.Rigidbody::ResetInertiaTensor
  table ptr 129376 -> func82525
  func82525: a[100] = 1; 调用 f_abdd

func73082 / func73083 / func73084
  反序列化/传输字段 m_ImplicitCom    -> a + 85
  反序列化/传输字段 m_ImplicitTensor -> a + 100
```

`func73058` 的 Rigidbody native 初始化分支也把 `a[85]=1`、`a[100]=1`，并写入默认
COM `(0,0,0)` 与 inertia `(1,1,1)`。`tools/reverse/inspect_unity_assets.py`
读取 `data.unity3d` 后，82 个 `Curling stone*` Rigidbody 均能看到
`m_ImplicitCom=true`、`m_ImplicitTensor=true`。

`CurlingStoneNew.Start` 调用的是显式 `set_centerOfMass(Vector3.zero)`，所以它会把
`m_ImplicitCom` 关掉，COM 不再跟随后续 collider/cooked hull 自动重算。石壶没有显式调用
`set_inertiaTensor*` 或 `ResetInertiaTensor`，因此 `m_ImplicitTensor=true` 目前仍是最强
证据。`f_abdd` 会在 `m_ImplicitCom | m_ImplicitTensor` 为真时走
`PxRigidBodyExt::setMassAndUpdateInertia`；如果 COM 已显式锁定，Unity 会把当前 COM
作为 `massLocalPose` 传下去，让 PhysX 在固定 COM 下更新惯量。

2026-07-08 再把 `MeshCollider.sharedMesh/convex` 的 native rebuild 链路固化成脚本：

```powershell
python tools\reverse\summarize_meshcollider_rebuild_mass_sync.py
```

当前输出确认：

```text
MeshCollider.set_sharedMesh func82533 calls slot[37]: yes
MeshCollider.set_convex helper func72947 calls slot[37]: yes
slot[37] -> func72951
rebuild func72951 convex path calls f_pjdd: yes
shape attach func73283 calls f_abdd(e): yes
f_abdd calls f_eqcd/setMassAndUpdateInertia: yes
```

也就是说，`MeshCollider` rebuild 是否触发 `f_abdd` 已经不是未知。正式石壶当前推论为：
COM 已锁 zero；`m_ImplicitTensor=true` 保留；convex MeshCollider 建好后会按 rebuilt
PhysX shape 重算 inertia。剩余真正未知是那时参与计算的 cooked convex shape 精确数据，
以及由它得到的最终 inertia tensor 数值。

`build.wasm` 明文字符串中还能看到 Unity 内置 PhysX 模块证据，例如：

```text
./physx/source/physx/src/NpPhysics.cpp
./physx/source/physx/src/NpScene.cpp
PxScene.collide
PxScene.solve
PxRigidBody
PxMaterial
PxsDynamics.solverStart
PxsDynamics.solverSetupSolve
PxsDynamics.createFinalizeContacts
PxsContext.contactManagerDiscreteUpdate
PxsCCD.cpp
DyTGSContactPrep.cpp
PxInitExtensions failed
```

这进一步说明正式多壶碰撞不是 C# 层自写 `Lambda1/Lambda2` 求解，而是 Unity 3D Physics/PhysX
在 native wasm 层处理，C# 层只在 `OnCollisionEnter` 后设置 `mCollision`、改材质摩擦和处理 Wall 分支。
需要注意：wasm 里编进了 TGS/CCD 等 PhysX 相关代码字符串，但资源里的 `PhysicsManager`
显示 `solverType = 0`，因此项目实际使用的应是默认 solver 类型；这些字符串只能证明模块存在，
不能反推比赛场景启用了对应选项。

2026-07-08 runtime probe 的浏览器控制台日志提供了独立运行时证据：Unity 每个 FixedUpdate
会打印 `b2Vec2 velocity`。纯滑行壶的速度序列能积分到最终 `POSITION`；发生碰撞/边界事件时，
`Curling stop` 前最后一条速度仍然可能有 `0.26m/s - 1.52m/s`。这说明 `Curling stop`
不是“速度自然降为 0”的通用日志，而是 `mCollision` 或边界状态让单壶 `Newfrictionstep`
路径退出，随后由 PhysX/墙处理接管。该日志现在可通过
`tools/reverse/analyze_unity_console_trajectory.py` 提取 handoff 位置和线速度。

本轮进一步从字符串引用追到了 PhysX 任务图。相关地址不是普通 C 字符串起点，而是 task/vtable
元数据块；块内的函数表项可以映射回 wasm 函数。已经定位到的关键任务：

```text
PxsDynamics.solverStart
  metadata 3151016 -> table[8] 120557 -> func71248  // 1143 行

PxsDynamics.solverEnd
  metadata 3152020 -> table[8] 120566 -> func71257

PxsDynamics.solverSetupSolve
  metadata 3152088 -> table[8] 120569 -> func71259  // 467 行

PxsDynamics.solverConstraintPartition
  metadata 3152236 -> table[8] 120575 -> func71263

PxsDynamics.createForceChangeThresholdStream
  metadata 3152452 -> table[8] 120584 -> func71269

PxsDynamics.createFinalizeContacts
  metadata 3152788 -> table[8] 120587 -> func71272  // 1194 行

PxsDynamics.preIntegrate
  metadata 3152868 -> table[8] 120590 -> func71273  // 62 行

PxsContext.contactManagerDiscreteUpdate
  metadata 3134996 -> table[8] 120204 -> func70739  // 1065 行
```

这些条目现在可以用 `tools/reverse/resolve_physx_task_metadata.py` 从 `build.wat`
和 `wasm_table_map.json` 直接复现；同一批 metadata block 的前几个 word 是公共 task/vtable
入口，`table[8]` 对应具体 task body。`func71265` 是 dynamics solver 任务图调度函数：
它创建并串接 `createForceChangeThresholdStream`、`solverEnd`、`solverSetupSolve`、
`solverConstraintPartition`、`solverStart` 等 task。`func71202` 负责按 contact manager 分块创建
`PxsDynamics.createFinalizeContacts` 与 `PxsDynamics.preIntegrate` 任务。
