# 总览与 Unity 资产参数

记录包结构、Unity 对象参数、全局常量、数据结构、核心函数索引和 Ghidra 过程。

> 原长文档已封存：[`UNITY_REVERSE_ENGINEERING.zh.2026-07-07.archive.md`](../archive/UNITY_REVERSE_ENGINEERING.zh.2026-07-07.archive.md)。以后维护以本目录子文档为准。


这份文档记录我们目前能从官方打包的 Unity/WebGL 数字冰壶模拟器里恢复出什么，以及这些结论对本地训练模拟器意味着什么。

## 包结构

本地竞赛客户端是一个 Unity WebGL + IL2CPP 构建：

- `数字冰壶单机版_win/数字冰壶单机版/curling_server.exe`
- `数字冰壶单机版_win/数字冰壶单机版/web/Build/build.data.gz`
- `数字冰壶单机版_win/数字冰壶单机版/web/Build/build.wasm.gz`
- `数字冰壶单机版_win/数字冰壶单机版/web/Build/build.framework.js.gz`
- 资源包里识别到的 Unity 版本：`2022.3.62f2c1`
- IL2CPP metadata 版本：`31`

`curling_server.exe` 主要是本地服务器/桥接程序。配置在 `conf/config.ini`：

```ini
HttpPort = 9007
TcpPort = 7788
ConnectHost = "127.0.0.1"
CurlingServerHost = "http://127.0.0.1:8084"
RobotPython = "./resource"
```

### BuildSettings 场景列表

`tools/reverse/inspect_unity_assets.py` 现在会直接解析 `globalgamemanagers` 里的
`BuildSettings` raw data。当前 WebGL 包实际打包的场景是：

```text
0: Assets/Scenes/MenuScene.unity
1: Assets/Scenes/MotionTestScene.unity
2: Assets/Scenes/GameScene.unity
3: Assets/Scenes/GameScene4Games.unity
4: Assets/Scenes/GameSceneNoLimit.unity
5: Assets/Scenes/GameSceneDebug.unity
6: Assets/Scenes/HumanVsAI.unity
```

因此这版包里没有 `Assets/Scenes/AutoGame.unity`，也没有 `FastGame.unity`。
`AutoDCP`、`AutoGame`、`FastGame` 等字符串和方法确实存在于 IL2CPP 代码/metadata 中，
但当前 WebGL BuildSettings 没把对应 AutoGame/FastGame 场景打进去。这个结论解释了为什么
普通无限模式和普通四局/八局 UI 路径不会产生 AutoDCP `.save`。

当前 asset inventory 还能看到：

```text
level0: ScenesController=1
level1: MotionTest=1, MotionTestStone=1
level2: DCP=1, ScenesController=1, WaitMenuControl=1
level3: DCP=1, ScenesController=1, WaitMenuControl=1
level4: DCP=1, ScenesController=1, WaitMenuControl=1
level5: DCP=1, ScenesController=1, WaitMenuControl=1
level6: AIBattleController=1, DCP_HumanVSAI=1, HumanInputController=1, ScenesController=1, UrlParamReader=1, WaitMenuControl=1
```

没有任何已打包 scene 里挂着 `AutoDCP` 或 `FastDCP` GameObject。`ReadRecord` 和
`StartHisGame` 按钮在 DCP/HumanVsAI 场景里存在，但 GameObject 默认 inactive；真正的
AutoDCP `Start()` 绑定逻辑在代码里存在，却没有当前包内可加载的 AutoGame scene 来承载。

主菜单按钮的 persistent `Button.onClick` 也已经从 raw MonoBehaviour 里解析出来：

```text
BtnFinalContest       -> SceneControl.mLoadScence("GameScene")
BtnDebug Contest      -> SceneControl.mLoadScence("GameSceneDebug")      // GameObject inactive
BtnFastGame           -> SceneControl.mLoadScence("FastGame")            // GameObject inactive, scene not in BuildSettings
BtnHumanVsAI          -> SceneControl.mLoadScence("HumanVsAI")
BtnNoLimit Contest    -> SceneControl.mLoadScence("GameSceneNoLimit")
BtnPreliminaryContest -> SceneControl.mLoadScence("GameScene4Games")
BtnMotionTest         -> SceneControl.mLoadScence("MotionTestScene")
```

`ScenesController.mLoadScence` 对应 wasm `func60729`，函数体本质上就是
`UnityEngine.SceneManagement.SceneManager.LoadScene(sceneName)`。所以 `GameSceneDebug`
虽然按钮隐藏，但 scene 本身在包里；后续可以尝试用 WebGL `SendMessage("SceneControl",
"mLoadScence", "GameSceneDebug")` 或局部 patch 主菜单按钮来进入 Debug 场景。`FastGame`
则不同：按钮和字符串存在，但 scene 没打包，直接 load 会失败。

## 已恢复的 Unity 对象参数

来自 Unity asset/type-tree 检查。

### PhysicMaterial

`Ice`：

- `dynamicFriction = 0.02`
- `staticFriction = 0.02`
- `bounciness = 0`
- `frictionCombine = 2`
- `bounceCombine = 2`

`Bouncy`：

- `dynamicFriction = 0.6`
- `staticFriction = 0.6`
- `bounciness = 1`
- `frictionCombine = 2`
- `bounceCombine = 2`

### 冰壶 Rigidbody

典型冰壶对象（`Curling stone blue*`、`Curling stone red*`）：

- `mass = 19.1`
- `drag = 0`
- `angularDrag = 0.05`
- `useGravity = true`
- `isKinematic = false`
- `collisionDetection = 0`（正式比赛石壶）；`level1` 的测试红壶为 `1`
- `constraints = 0`
- 序列化 `m_CenterOfMass = (0, 0, 0)`
- 序列化 `m_InertiaTensor = (1, 1, 1)`
- 序列化 `m_InertiaRotation = (0, 0, 0, 1)`
- 序列化 `m_ImplicitCom = true`
- 序列化 `m_ImplicitTensor = true`
- local scale 约为 `(0.115, 0.115, 0.115)`

注意：`m_InertiaTensor=(1,1,1)` 是资源里保存的默认字段值，不等于最终 solver
必然使用这个惯量。因为同一个 Rigidbody 还序列化了 `m_ImplicitTensor=true`，
Unity/PhysX 在 collider shape 建好后允许按 shape 自动更新惯量。后续已确认
runtime MeshCollider rebuild 会触发 Rigidbody mass-properties sync；真正剩下的是
这一步使用的是哪一个 cooked hull，以及其质量属性的具体数值。

2026-07-08 继续追到 Rigidbody native setter 和序列化函数后，COM 与惯量的自动/显式
字段已经能命名：

```text
a[85]  = m_ImplicitCom
a[100] = m_ImplicitTensor

set_centerOfMass_Injected -> func82515 -> func73033: a[85] = 0
ResetCenterOfMass         -> func82524:              a[85] = 1
set_inertiaTensor*        -> func82517/func82519:   a[100] = 0
ResetInertiaTensor        -> func82525:              a[100] = 1
Rigidbody native init     -> func73058:              a[85] = 1, a[100] = 1

func73082/73083/73084 反序列化字段名：
  m_ImplicitCom    -> a + 85
  m_ImplicitTensor -> a + 100
```

所以 `CurlingStoneNew.Start` 显式写 `centerOfMass=Vector3.zero` 后，COM 已经不应再按
cooked hull 自动重算；但它没有调用 `set_inertiaTensor*`，资源里的
`m_ImplicitTensor=true` 也没有被 C# 业务层关掉。当前更精确的结论是：正式石壶
运行时是“COM 锁为 zero，inertia 仍走 implicit/shape 自动计算”。`MeshCollider`
rebuild 是否调用 mass-properties sync 也已钉住：`set_sharedMesh/set_convex ->
slot[37] func72951 -> convex 分支 func73283` 会对 attached Rigidbody 调 `f_abdd`。
剩余要追的是这一步看到的 cooked convex shape 到底是什么，以及由它导出的
inertia tensor 数值。

### 冰壶动态 MeshCollider

场景里石壶根对象没有直接序列化一个普通 `MeshCollider` 组件。真正的石壶碰撞体由
`ExtendedColliders3D` 脚本在 `Awake()` 里运行时创建：

```text
GameObject.AddComponent<MeshCollider>()
Collider.enabled = enabled
MeshCollider.sharedMesh = generateMesh(...)
MeshCollider.convex = properties.convex
MeshCollider.isTrigger = properties.isTrigger
MeshCollider.material = properties.material
Destroy(this)
```

`ExtendedColliders3D` 挂在正式比赛石壶上，和 `CurlingStoneNew`、`CrossLineEvent` 同时存在。
`MotionTestStone` 只出现在 level1 的测试石壶上，不是正式比赛石壶路径。

已恢复的石壶 `ExtendedColliders3D.properties`：

```text
colliderType = 5                 // Cylinder
convex = true
isTrigger = false
material = Bouncy
centre = (0, 0, 0)
rotation = (0, 0, 0)
size = (2.5, 2.0, 2.5)
cylinderFaces = 256
cylinderCapTop = true
cylinderCapBottom = true
cylinderTaperTop = (1, 1)
cylinderTaperBottom = (1, 1)
flipFaces = true
```

对 `build.data.gz` 里 82 个 `Curling stone*` 的 `ExtendedColliders3D` 组件去重后，`centre`、
`rotation`、`size`、`cylinderFaces`、`flipFaces` 和 `material` 都一致；当前没有发现不同 stone
index 使用不同碰撞体尺寸或局部偏移。

这批 setter 已经从 wasm 里的 `f_vkb(...)` 字符串指针反查到 Unity internal-call 名：

```text
f_cdva -> UnityEngine.Collider::set_enabled(System.Boolean)
f_hdva -> UnityEngine.MeshCollider::set_sharedMesh(UnityEngine.Mesh)
f_idva -> UnityEngine.MeshCollider::set_convex(System.Boolean)
f_edva -> UnityEngine.Collider::set_isTrigger(System.Boolean)
f_gdva -> UnityEngine.Collider::set_material(UnityEngine.PhysicMaterial)
```

`Awake()` 会调用 `generateMesh(false)`，也就是把 `properties` 生成的局部 mesh
直接赋给 `MeshCollider.sharedMesh`，不额外烘入 GameObject Transform；这一段没有看到
`MeshCollider.cookingOptions` setter，因此运行时石壶的 cooking 选项目前只能按 Unity
默认 runtime MeshCollider 行为处理，不能把 `Plane.m_CookingOptions=30` 直接套到石壶上。

2026-07-08 继续把 `ExtendedColliders3D.Awake` 映射到 wasm 后，调用链已经能固定到：

```text
ExtendedColliders3D.Awake
  method pointer 12126 -> wasm $f59928 / dcmp_funcs/func59928.dcmp

func59928 只调用：
  GameObject.AddComponent<MeshCollider>()
  Collider.set_enabled(...)
  MeshCollider.set_sharedMesh(generateMesh(false))
  MeshCollider.set_convex(...)
  Collider.set_isTrigger(...)
  Collider.set_material(...)
  Object.Destroy(this)
```

在 `Awake/generateMesh/generateVerticesAndTriangles` 这条业务脚本路径里没有看到：

```text
Rigidbody.set_mass
Rigidbody.set_inertiaTensor
Rigidbody.set_inertiaTensorRotation
Rigidbody.ResetCenterOfMass
Rigidbody.ResetInertiaTensor
```

因此可确认的是：`ExtendedColliders3D.Awake` 这条 MeshCollider 创建路径没有显式改
Rigidbody mass/inertia。另一路 `CurlingStoneNew.Start` 会把正式石壶
`centerOfMass` 写成 `Vector3.zero`，但没有写 `mass`、`inertiaTensor`、
`inertiaTensorRotation` 或 Reset。native 层继续追完后，runtime convex
`MeshCollider` rebuild 已确认会隐式重算 attached Rigidbody 的 mass properties：

```text
MeshCollider vtable base 3221476
slot[37] -> func72951 / f_vwcd
slot[38] -> func72948 / f_swcd

set_sharedMesh func82533 -> call slot[37]
set_convex     func72947 -> call slot[37]
func72951      -> convex 分支调用 f_pjdd / func73283
func73283      -> f_qjdd 找 attached Rigidbody，再调用 f_abdd(e)
f_abdd         -> 在 m_ImplicitCom | m_ImplicitTensor 为真时调用 f_eqcd
```

可复查脚本：

```powershell
python tools\reverse\summarize_meshcollider_rebuild_mass_sync.py
```

所以“是否重算惯量”已经不是未知；剩余是 cooked convex shape 的精确顶点/面/plane/indices
以及由 PhysX `setMassAndUpdateInertia` 得到的最终惯量数值。

`generateMesh(...)` 的 Unity API 序列也已经从 internal-call 字符串确认：

```text
new Mesh() / Mesh::Internal_Create
Object.SetName(mesh, "Extended Colliders 3D Mesh")
generateVerticesAndTriangles(...)
Mesh.SetArrayForChannel<Vector3>(vertices)
Mesh.SetIndicesImpl(... MeshTopology.Triangles ...)
Mesh.RecalculateNormalsImpl(MeshUpdateFlags.Default)
```

继续把 `generateVerticesAndTriangles(...)` 拆开后，正式石壶 cylinder mesh 的原始输入为：

```text
local mesh vertices = 2 * cylinderFaces = 512
local mesh indices  = side 6*256 + top cap (3*256-6) + bottom cap (3*256-6)
                   = 3060 indices = 1020 triangles

top ring:
  vertex i = (cos(2*pi*i/256)*1.25, +1.0, sin(2*pi*i/256)*1.25)

bottom ring:
  vertex i+256 = (cos(2*pi*i/256)*1.25, -1.0, sin(2*pi*i/256)*1.25)

side triangles before flipFaces:
  [top_i, bottom_i, top_next]
  [top_next, bottom_i, bottom_next]

top/bottom caps:
  不是简单 fan 从 0 开始，而是从当前 ring index list 的中点开始，
  交替向两侧 remove center 做 ear triangulation。

flipFaces:
  最后对每个 triangle 交换前两个 index。
```

结合石壶自身 `localScale = (0.115, 0.115, 0.115)`，不考虑父级缩放时：

```text
local collision radius ~= 2.5 * 0.115 / 2 = 0.14375 m
local collision height ~= 2.0 * 0.115     = 0.23 m
```

但正式赛道层级还有父级 Transform，`inspect_unity_assets.py` 现在会递归计算 world matrix。
正式场景中石壶的典型 `worldScale ~= (0.1127, 0.115, 0.1127)`，所以真实世界碰撞半径约为：

```text
world collision radius ~= 1.25 * 0.1127 = 0.140875 m
world collision height ~= 2.0 * 0.115   = 0.23 m
```

这解释了为什么规则层仍使用略大的阈值 `0.145m`：它接近未乘父级缩放的半径，
并给实际 PhysX 半径约 `0.140875m` 留了一点规则判断余量。

### Tag 和 PhysicsManager

`TagManager` 中的自定义 tag：

```text
Wall
Rink
Stone
```

因此石壶的 `m_Tag = 20002` 对应 `Stone`，边界 `bound1..bound4` 的 `m_Tag = 20000`
对应 `Wall`，冰面 `Plane` 的 `m_Tag = 20001` 对应 `Rink`。

资产层再次确认了正式场景中的几何类型：

```text
stone:
  runtime generated convex MeshCollider
  ExtendedColliders3D cylinder, 256 faces

rink Plane:
  static MeshCollider(m_IsTrigger=false)
  注意：对象名叫 Plane，但 PhysX 几何不是 PxPlane，而是 triangle mesh
  m_Convex = false
  m_CookingOptions = 30
  m_Material = Ice
  m_Mesh = unity default resources:10209
  local position = (2204.17, -109, -20.083)
  local rotation ~= (0, 0.707107, 0)
  local scale = (200.787, 40, 40)

bound1..bound4:
  BoxCollider(m_IsTrigger=false)

Midline / Hogline1 / Hogline2:
  BoxCollider(m_IsTrigger=true)

Terminal:
  CapsuleCollider(m_Enabled=false)
  local position ~= (31.37, 17.931, 55.2551)
  local scale ~= (0.15, 0.1, 0.15)
```

`Plane` 的 `MeshCollider.m_Mesh` 指向 `unity default resources:10209`，不是项目
`sharedassets*.assets` 里可直接读出的 mesh object。当前 UnityPy 能稳定恢复这个
PPtr、材质和 cooking options，但不能直接从 bundle 里 dump 出内置 mesh 顶点。
WebGL 字符串里也出现了 `New-Plane.fbx`；Unity 官方 primitive 说明里，Plane 是本地
XZ 平面、边长 10，并包含 200 个三角形。因此它基本可以按 Unity 内置 Plane mesh
理解，但在没有从 Unity default resources 或运行时 PhysX cooking 数据导出前，
“Plane 的具体顶点顺序/三角形索引顺序”仍列为尚未完全锁死的几何细节。
另外，`Plane.m_CookingOptions=30` 是静态冰面 `MeshCollider` 的序列化值；
正式石壶的 `MeshCollider` 是运行时 `AddComponent` 生成，`Awake/generateMesh`
里没有看到 `MeshCollider.cookingOptions` 写入，因此不能把冰面的 cooking 选项
直接套到石壶上。

这次还补了父子 Transform 的 world matrix 计算，解释了为什么 Plane 的 local transform
看起来离谱。以 level1 为例：

```text
Plane local position = (2204.17, -109, -20.083)
Plane local scale    = (200.787, 40, 40)

Plane world position = (14.014, 14.3048, 55.566)
Plane world scale    = (4.998, 1.016, 0.99568)
Plane world normal   = (0, 1, 0)
```

如果按 Unity 内置 Plane 的 10x10 XZ 面计算，冰面碰撞区域约为：

```text
world size ~= 49.98m x 9.9568m
surface y  ~= 14.3048m
```

这和四周墙 `bound1..bound4` 围出的赛道范围、以及石壶世界中心 `y ~= 14.4324`
和石壶半高 `0.115m` 能对上：石壶底面约在 `14.3174m`，距离冰面约 `0.0126m`，
与默认 contact offset `0.01m` 同量级。

正式场景的 release/trigger 几何还恢复出：

```text
Curling stone blue0 initial local position ~= (3.21, 17.9324, 55.28)
Midline local position ~= (14.58, 17.94, 55.23)
Hogline1 local position ~= (3.695, 17.94, 55.2)
Hogline2 local position ~= (25.57, 17.94, 55.2)
CameraHouse local position ~= (-70.74, 22.03, 53.87)   // 带场景整体平移的正式 level
Terminal local position ~= (31.37, 17.931, 55.2551)
Terminal local scale ~= (0.15, 0.1, 0.15)
```

正式 level 会整体平移，因此世界坐标会出现 `-100` 左右的偏移；协议公式使用的
`teePosition` 与石壶 `Transform.position` 需要在同一坐标系里相减。`Start()` 中已经确认：

```text
origin_postion = mBlueBalls[0].transform.position
terminal       = GameObject.Find("Terminal")
teePosition    = terminal.transform.position
```

因此 release 几何要用 world 坐标差，而不是直接拿 local 坐标相减。`MOTIONINFO`
的 `stop_y` 还要考虑 Midline trigger box 与石壶 collider 的首次 overlap，
详见 [`02_protocol_sweep_input.zh.md`](02_protocol_sweep_input.zh.md)。

`TimeManager` 中已恢复的全局时间步长：

```text
Fixed_Timestep = 0.01
Maximum_Allowed_Timestep = 0.33
Maximum_Particle_Timestep = 0.33
timeScale = 1.0
```

这点很重要：Unity `FixedUpdate` 的调度周期是 `0.01s`。代码里传给
`Newfrictionstep` 的 `steptime = 0.001` 是该函数自己的参数，不是 Unity 的 fixed timestep。

`PhysicsManager` 中已恢复的全局设置：

```text
gravity = (0, -9.81, 0)
bounceThreshold = 0.05
defaultContactOffset = 0.01
defaultSolverIterations = 6
defaultSolverVelocityIterations = 1
sleepThreshold = 0.005
defaultMaxAngularSpeed = 3.14
defaultMaxDepenetrationVelocity = 10
frictionType = 0
solverType = 0
broadphaseType = 0
contactsGeneration = 1
contactPairsMode = 0
autoSyncTransforms = false
simulationMode = 0
enableAdaptiveForce = false
enableEnhancedDeterminism = false
improvedPatchFriction = false
enableUnifiedHeightmaps = true
queriesHitBackfaces = false
queriesHitTriggers = true
fastMotionThreshold = 3.402823e38
worldSubdivisions = 8
invokeCollisionCallbacks = true
reuseCollisionCallbacks = true
defaultMaterial = None
```

## 已恢复的游戏物理常量

以下常量同时嵌在 `DCP_HumanVSAI` 和 `Assets.CurlingMotion` 中：

```csharp
PI = 3.1416
R = 0.125
DR = 0.006
FAI = 2
K = 0.2
STONEINFO_NEWFRICTION = 1
SWEEP_EFFECT = 0.4
```

这些常量和 `docs/CURLING_PHYSICS_MODEL_ANALYSIS.md` 里已经描述过的干/湿摩擦冰壶模型能对上。

## 已恢复的数据结构

来自 `dump.cs`：

```csharp
public struct b2Vec2 {
    public double x; // 0x0
    public double y; // 0x8
}

public struct MyParams {
    public double vx; // 0x0
    public double vy; // 0x8
    public double w;  // 0x10
    public double r1; // 0x18
    public double r2; // 0x20
}

public struct speed {
    public b2Vec2 v;     // 0x0
    public double angle; // 0x10
}
```

## 已恢复的核心函数

`Assets.CurlingMotion` 包含本地运动模型：

```csharp
private static double fdx1(double x, MyParams param);
private static double fdx2(double x, MyParams param);
private static double fdx3(double x, MyParams param);
private static double fwx1(double x, MyParams param);
private static double fwx2(double x, MyParams param);
private static double fwx3(double x, MyParams param);
private static double fwx4(double x, MyParams param);
private static double fdy1(double x, MyParams param);
private static double fdy2(double x, MyParams param);
private static double fdy3(double x, MyParams param);
private static double fwy1(double x, MyParams param);
private static double fwy2(double x, MyParams param);
private static double fwy3(double x, MyParams param);
private static double fwy4(double x, MyParams param);
private static double fda1(double x, MyParams param);
private static double fda2(double x, MyParams param);
private static double fda3(double x, MyParams param);
private static double fda4(double x, MyParams param);
private static double fwa1(double x, MyParams param);
private static double fwa2(double x, MyParams param);
private static double fwa3(double x, MyParams param);
private static double fwa4(double x, MyParams param);
private static double fsimp(double a, double b, double eps, MyParams param, int type, int i);
public static speed Newfrictionstep(double friction, b2Vec2 vec, double angle, double steptime);
```

Il2CppDumper 将这些方法映射到 dynCall method pointer ID `12132..12155`。wasm 间接函数表再把这些 ID 映射到真正的 wasm 函数：

| C# 方法 | method pointer | wasm 函数 |
| --- | ---: | ---: |
| `fdx1` | `12132` | `$f59933` |
| `fdx2` | `12133` | `$f59934` |
| `fdx3` | `12134` | `$f59935` |
| `fwx1` | `12135` | `$f59936` |
| `fwx2` | `12136` | `$f59937` |
| `fwx3` | `12137` | `$f59938` |
| `fwx4` | `12138` | `$f59939` |
| `fdy1` | `12139` | `$f59940` |
| `fdy2` | `12140` | `$f59941` |
| `fdy3` | `12141` | `$f59942` |
| `fwy1` | `12142` | `$f59943` |
| `fwy2` | `12143` | `$f59944` |
| `fwy3` | `12144` | `$f59945` |
| `fwy4` | `12145` | `$f59946` |
| `fda1` | `12146` | `$f59947` |
| `fda2` | `12147` | `$f59948` |
| `fda3` | `12148` | `$f59949` |
| `fda4` | `12149` | `$f59950` |
| `fwa1` | `12150` | `$f59951` |
| `fwa2` | `12151` | `$f59952` |
| `fwa3` | `12152` | `$f59953` |
| `fwa4` | `12153` | `$f59954` |
| `fsimp` | `12154` | `$f59955` |
| `Newfrictionstep` | `12155` | `$f59956` |

从 wasm 函数体里识别出的数学辅助函数：

- `$f5979 = cos`
- `$f5980 = sin`
- `$f54019 = atan`
- `$f56754 = pow`

## Ghidra 逆向过程

我在仓库外安装过一套 Ghidra/IL2CPP/WABT 工具链。注意：这些目录是后续逆向需要反复复用的
工作资产，不应清理。

当前关键目录：

```text
D:\esp\tmp\curling_reverse_il2cpp
  build.wat
  build.dcmp
  build.wasm
  data.unity3d
  wasm_table_map.json
  il2cpp_out\script.json
  il2cpp_out\dump.cs
  dcmp_funcs\*.dcmp

D:\esp\tmp\curling_ghidra12_project
D:\esp\tmp\curling_ghidra_tools
D:\esp\tmp\curling_physx_41
D:\esp\tmp\curling_pyphysx_conda
```

工具链概况：

- Ghidra `12.1.2` 官方版：可以 headless 运行，但没有原生 wasm loader。
- `ghidra-wasm-plugin` `v2.4.0`：提供 WebAssembly loader，但它是为 Ghidra `12.0` 构建的，在 Ghidra `12.1.2` 上会崩。
- Ghidra `12.0` 官方版 + wasm plugin：可以成功导入 `build.wasm`。
- 现代 Ghidra 需要 JDK `21`；系统自带 Java 17 不够。

wasm 导入和保存成功了，虽然完整 auto-analysis 跑到 1800 秒超时。即便如此，它已经足够反编译较小的 `CurlingMotion` kernel 函数。可复用脚本如下：

```powershell
D:\anaconda3\python.exe tools\reverse\extract_wasm_table_map.py `
  "$env:TEMP\curling_reverse_il2cpp\build.wat" `
  "$env:TEMP\curling_reverse_il2cpp\wasm_table_map.json"

& "$env:TEMP\curling_ghidra_tools\ghidra_12.0_PUBLIC\support\pyghidraRun.bat" `
  -H "$env:TEMP\curling_ghidra12_project" CurlingWasm `
  -process build.wasm -noanalysis `
  -scriptPath "$env:TEMP\curling_ghidra_tools\ghidra_12.0_PUBLIC\Ghidra\Extensions\ghidra-wasm-plugin\ghidra_scripts" `
  -postScript ghidra_il2cpp_wasm_export.py `
  "$env:TEMP\curling_reverse_il2cpp\il2cpp_out\script.json" `
  "$env:TEMP\curling_reverse_il2cpp\ghidra_curlingmotion_export.md" `
  "$env:TEMP\curling_reverse_il2cpp\wasm_table_map.json"
```

重要限制：Ghidra 对这个 Unity 构建的 wasm table/symbol 处理并不完全可靠。小 kernel 能正确反编译，但 `Newfrictionstep` 的地址/名字映射可能和相邻 IL2CPP wrapper 撞在一起。因此 `Newfrictionstep` 应以 WAT 函数体 `$f59956` 为权威来源。Ghidra 仍然适合看 `fdx/fwx/fdy/fwy/fda/fwa` 这批公式，因为它们很短，反编译也干净。

令 `MyParams(vx, vy, w, r1, r2)`，最先恢复出的 kernel 与预期的 running-band 几何一致。例如 WAT 检查给出：

```text
fdx1:
  A = vx + sin(x) * w * r2
  B1 = vy + cos(x) * w * r2
  B2 = vy - cos(x) * w * r2
  return sin(atan(A / B1)) + sin(atan(A / B2))

fdx2:
  A = sin(x) * w * r1 - vx
  B1 = vy + cos(x) * w * r1
  B2 = vy - cos(x) * w * r1
  return sin(atan(A / B1)) + sin(atan(A / B2))

fdx3:
  A = vx + sin(x) * w * r2
  B = vy - cos(x) * w * r2
  return sin(atan(A / B))
```

湿摩擦 kernel 会把类似方向项乘以局部接触速度平方，这和已恢复的 `FAI = 2` 指数一致。
