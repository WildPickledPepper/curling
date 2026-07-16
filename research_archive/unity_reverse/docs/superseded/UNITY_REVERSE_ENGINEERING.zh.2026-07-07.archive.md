# Unity 逆向工程笔记

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
- `collisionDetection = 0 or 1`
- local scale 约为 `(0.115, 0.115, 0.115)`

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
size = (2.5, 2.0, 2.5)
cylinderFaces = 256
cylinderCapTop = true
cylinderCapBottom = true
cylinderTaperTop = (1, 1)
cylinderTaperBottom = (1, 1)
flipFaces = true
```

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
```

如果按 Unity 内置 Plane 的 10x10 XZ 面计算，冰面碰撞区域约为：

```text
world size ~= 49.98m x 9.9568m
surface y  ~= 14.3048m
```

这和四周墙 `bound1..bound4` 围出的赛道范围、以及石壶世界中心 `y ~= 14.4324`
和石壶半高 `0.115m` 能对上：石壶底面约在 `14.3174m`，距离冰面约 `0.0126m`，
与默认 contact offset `0.01m` 同量级。

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

我在仓库外临时安装过一套 Ghidra 工具链：

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

## `Newfrictionstep` 做了什么

从 `$f59956` 恢复出的高层结构：

1. 如果角速度接近 0，就把输入角速度夹到 `0.01`。
2. 从输入 `b2Vec2` 计算 `|v|`。
3. 如果 `|v| <= 0.01`，返回零速度、零角速度。
4. 否则构造 `MyParams(vx, vy, w, r1, r2)`，初始 `r1 = r2 = 0.125`。
5. 反复调用 `fsimp(0, PI/2, 1e-5, param, type, i)` 积分力/力矩 kernel。
6. 正角速度和负角速度有不同分支。
7. 近似按下面方式更新速度：

```text
vx += steptime * 10 * ax
vy += steptime * 10 * ay
angle += steptime * 20 * angular_acc / 0.399475
```

函数体里还能看到这些硬常量：

- 加速度分母里质量实际按 `19` 处理。
- `R = 0.125`
- `K = 0.2`
- `PI = 3.1416`
- 积分上界 `PI / 2 = 1.5708`
- 积分精度 `1e-5`

更细的 WAT 检查显示，`Newfrictionstep` 每步会调用 `fsimp` 40 次。调用按三组参数副本组织，使用 `type = 1/2/3` 和不同 kernel index：

```text
group A:
  type 1: i = 1, 5, 6
  type 2: i = 1, 5, 6
  type 3: i = 1, 2, 7, 8

group B:
  type 1: i = 1, 2, 3, 4, 5, 6
  type 2: i = 1, 2, 3, 4, 5, 6
  type 3: i = 1, 2, 3, 4, 5, 6, 7, 8

group C:
  type 1: i = 2, 3, 7
  type 2: i = 2, 3, 7
  type 3: i = 2, 3, 4, 5
```

`Newfrictionstep` 中其余常量也揭示了带状几何：

- `0.122 = R - DR / 2`
- `0.128 = R + DR / 2`
- `0.0244 = K * (R - DR / 2)`
- `0.0256 = K * (R + DR / 2)`
- `0.025 = K * R`
- `6.2832 = 2 * PI`
- `12.5664 = 4 * PI`
- `1900 = 100 * 19`

所以这个模型不是简单拟合出来的经验曲线，而是一个带有内/外 running-band 半径和湿摩擦项的环带积分摩擦模型。

## 已恢复的 `fsimp` 语义

对大函数来说，WABT 的 `wasm-decompile` 比 Ghidra 更可读：

```powershell
$wabt = "$env:TEMP\curling_wabt_tools\wabt-1.0.41\bin"
& "$wabt\wasm-decompile.exe" "$env:TEMP\curling_reverse_il2cpp\build.wasm" `
  -o "$env:TEMP\curling_reverse_il2cpp\build.dcmp"

D:\anaconda3\python.exe tools\reverse\extract_decompiled_wasm_func.py `
  "$env:TEMP\curling_reverse_il2cpp\build.dcmp" `
  "$env:TEMP\curling_reverse_il2cpp\dcmp_funcs" `
  func59955 func59956
```

反编译名对应关系：

- `func59955 = fsimp`
- `func59956 = Newfrictionstep`
- `f_avh = sin`
- `f_zuh = cos`
- `f_rwac = atan`
- `f_wxec = pow`

`fsimp(a, b, eps, param, type, i)` 先算梯形估计，然后不断把区间减半，并使用：

```text
T_new = (T_old + step * midpoint_sum) / 2
S_new = (4 * T_new - T_old) / 3
stop when abs(S_new - S_prev) < eps
```

其中：

```text
vx = param.a
vy = param.b
w  = param.c
r1 = param.d
r2 = param.e
s  = sin(x)
c  = cos(x)
```

dispatch table 为：

| type | i | integrand 形状 |
| ---: | ---: | --- |
| 1 | 1 | `sin(atan((vx + s*w*r2) / (vy + c*w*r2))) + sin(atan((vx + s*w*r2) / (vy - c*w*r2)))` |
| 1 | 2 | `sin(atan((s*w*r1 - vx) / (vy + c*w*r1))) + sin(atan((s*w*r1 - vx) / (vy - c*w*r1)))` |
| 1 | 3 | `((vx + s*w*r1)^2 + (vy + c*w*r1)^2) * sin(atan((vx + s*w*r1) / (vy + c*w*r1)))` |
| 1 | 4 | `((vx + s*w*r1)^2 + (vy - c*w*r1)^2) * sin(atan((vx + s*w*r1) / (vy - c*w*r1)))` |
| 1 | 5 | `((s*w*r2 - vx)^2 + (vy + c*w*r2)^2) * sin(atan((s*w*r2 - vx) / (vy + c*w*r2)))` |
| 1 | 6 | `((s*w*r2 - vx)^2 + (vy - c*w*r2)^2) * sin(atan((s*w*r2 - vx) / (vy - c*w*r2)))` |
| 1 | 7 | `sin(atan((vx + s*w*r2) / (vy - c*w*r2)))` |
| 2 | 1..7 | 与 `type=1` 相同，但最外层 `sin(atan(...))` 变为 `cos(atan(...))`。第 3..6 项仍保留局部速度平方乘子。 |
| 3 | 1 | `sin(x + PI/2 - atan((vx + s*w*r2) / (vy + c*w*r2)))` |
| 3 | 2 | `sin(x + PI/2 + atan((vx + s*w*r2) / (vy - c*w*r2)))` |
| 3 | 3 | `sin(PI/2 - x + atan((s*w*r1 - vx) / (vy + c*w*r1)))` |
| 3 | 4 | `sin(PI/2 - x - atan((s*w*r1 - vx) / (vy - c*w*r1)))` |
| 3 | 5 | `((vx + s*w*r1)^2 + (vy + c*w*r1)^2) * sin(x + PI/2 - atan((vx + s*w*r1) / (vy + c*w*r1)))` |
| 3 | 6 | `((vx + s*w*r1)^2 + (vy - c*w*r1)^2) * sin(x + PI/2 + atan((vx + s*w*r1) / (vy - c*w*r1)))` |
| 3 | 7 | `((s*w*r2 - vx)^2 + (vy + c*w*r2)^2) * sin(PI/2 - x + atan((s*w*r2 - vx) / (vy + c*w*r2)))` |
| 3 | 8 | `((s*w*r2 - vx)^2 + (vy - c*w*r2)^2) * sin(PI/2 - x - atan((s*w*r2 - vx) / (vy - c*w*r2)))` |

这基本消除了 `fsimp` 的不确定性。还需要严谨验证的是翻译到本地代码后的符号约定，而不是 dispatch 结构本身。

## 已恢复的 `Newfrictionstep` 汇编逻辑

反编译出的 `func59956` 显示有三个速度区间：

```text
speed = sqrt(vx^2 + vy^2)
if speed <= 0.01: return (0, 0, 0)
if abs(angle) <= 1e-6: angle_input = 0.01

vx_abs = abs(vx)
vy_abs = abs(vy)
w_abs = abs(angle_input)
```

返回更新为：

```text
out.vx    = vx + steptime * 10 * ax
out.vy    = vy + steptime * 10 * ay
out.angle = angle_input + steptime * 20 * torque / 0.399475
```

定义：

```text
I(type, i; r1, r2) = fsimp(0, PI/2, 1e-5, MyParams(vx_abs, vy_abs, w_abs, r1, r2), type, i)
F2 = friction * 100 / (2 * PI)
F4 = friction * 100 / (4 * PI)
T2 = friction * 1900 / (2 * PI)
T4 = friction * 1900 / (4 * PI)
```

### 速度 `>= 1.5`

使用 `r1 = r2 = R`。

```text
ax_base = K / 19 * (I(1,5) + I(1,6))
ay      = F2 * I(2,1) + K / 19 * (I(2,5) + I(2,6))

if angle_input > 0:
  ax     = ax_base - F2 * I(1,1)
  torque = T2 * R * (I(3,2) - I(3,1)) + K*R * (I(3,8) - I(3,7))
else:
  ax     = F2 * I(1,1) - ax_base
  torque = T2 * R * (I(3,1) - I(3,2)) + K*R * (I(3,7) - I(3,8))
```

### 速度 `1.0..1.5`

使用 `r1 = R - DR/2 = 0.122`，`r2 = R + DR/2 = 0.128`。

```text
ax_wet_low  = 0.1 / 19 * (I(1,3) + I(1,4))
ax_wet_high = 0.1 / 19 * (I(1,5) + I(1,6))
ay = F4 * (I(2,1) + I(2,2))
   + 0.1 / 19 * (I(2,3) + I(2,4))
   + 0.1 / 19 * (I(2,5) + I(2,6))

if angle_input > 0:
  ax = F4 * (I(1,2) - I(1,1)) + ax_wet_high - ax_wet_low
  torque = T4 * (0.128 * (I(3,2) - I(3,1)) + 0.122 * (I(3,4) - I(3,3)))
         + 0.0244 * (I(3,6) - I(3,5))
         + 0.0256 * (I(3,8) - I(3,7))
else:
  ax = F4 * (I(1,1) - I(1,2)) + ax_wet_low - ax_wet_high
  torque = T4 * (0.128 * (I(3,1) - I(3,2)) + 0.122 * (I(3,3) - I(3,4)))
         + 0.0244 * (I(3,5) - I(3,6))
         + 0.0256 * (I(3,7) - I(3,8))
```

### 速度 `< 1.0`

使用 `r1 = r2 = R`。

```text
ay = K / 19 * I(2,3) + F2 * (I(2,2) + I(2,7))

if angle_input > 0:
  ax     = F2 * (I(1,2) - I(1,7)) - K / 19 * I(1,3)
  torque = T2 * R * (I(3,2) - I(3,3) + I(3,4)) - K*R * I(3,5)
else:
  ax     = K / 19 * I(1,3) + F2 * (I(1,7) - I(1,2))
  torque = K*R * I(3,5) + T2 * R * (I(3,3) - I(3,2) - I(3,4))
```

这意味着单壶、无碰撞模型已经基本能从二进制恢复出来。剩余工作是实现并用 Unity trace 样本验证。

第一版独立 Python 翻译在：

- `tools/reverse/recovered_curling_motion.py`

它目前放在 `tools/reverse/` 下，直到用 Unity trace 验证完、Unity 坐标符号约定彻底锁定。

## 已恢复的运行时物理循环

`DCP_HumanVSAI.FixedUpdate` 对应 wasm `func60124`。关键物理路径是：

1. 检查游戏是否激活、是否正在出手、`movingCurling` 是否存在、壶是否还没报告碰撞。
2. 读取当前 `Rigidbody` 的 velocity/angular velocity。
3. 把 Unity 轴转换成 `Newfrictionstep` 使用的 `b2Vec2`。
4. 调用：

```text
Newfrictionstep(friction, vec, angle, 0.001)
```

5. 把返回的 `speed` 转回 Unity `Rigidbody.velocity` 和 `Rigidbody.angularVelocity`。

时间尺度需要区分两层：

```text
Unity TimeManager.Fixed_Timestep = 0.01 seconds
Newfrictionstep steptime argument = 0.001
Newfrictionstep velocity update = old_v + steptime * 10 * acceleration
```

所以每个 Unity `FixedUpdate` tick 是 `0.01s`；`steptime = 0.001` 经函数内部 `*10`
缩放后，对线速度正好产生 `0.01s` 量级的增量。文档和代码里提到 `0.001` 时，应理解为
`Newfrictionstep` 参数，而不是 Unity 调度周期。

更精确的入口条件是：

```text
playersReady == true
shot == true
movingCurling != null
movingCurling.GetComponent<CurlingStoneNew>().mCollision == false
gameOver == false
recordedGame == false
```

其中最重要的是 `mCollision == false`。一旦 `CurlingStoneNew.OnCollisionEnter` 把 `mCollision`
置为 true，`FixedUpdate` 就跳过自定义 `Newfrictionstep` 单壶积分。这说明碰撞后的速度/角速度演化
不再由 `CurlingMotion.Newfrictionstep` 直接控制，而是交给 Unity `Rigidbody`/PhysX 的碰撞求解和后续刚体运动。

已恢复的 friction 参数：

```text
noise = Random.Range(-0.0002, 0.0002)

if Sweep.isSweeping:
    friction = 0.0006 + noise
else:
    friction = 0.0010 + noise
```

这是对早期模型的重要修正。`SWEEP_EFFECT = 0.4` 在代码里体现为：

```text
0.0010 * (1 - 0.4) = 0.0006
```

所以扫冰不是在出手后追加一个位移，而是在 `Sweep.isSweeping` 激活期间降低每个 Unity
`FixedUpdate` tick 中 `Newfrictionstep` 使用的摩擦。

随机项也意味着，终点匹配应按统计方式评估，或者控制 Unity 随机状态。确定性本地模拟器可以先用平均摩擦，但高保真 replay 需要逐步复现随机扰动：

```text
no sweep: friction in [0.0008, 0.0012]
sweep:    friction in [0.0004, 0.0008]
```

RNG 调用点已经全局反查：

```text
DCP_HumanVSAI.FixedUpdate -> Random.Range(-0.0002, 0.0002)
FastDCP.FixedUpdate       -> Random.Range(-0.0002, 0.0002)
AutoDCP.FixedUpdate       -> Random.Range(-0.0002, 0.0002)
DCP.FixedUpdate           -> Random.Range(-0.0002, 0.0002)
MotionTest.FixedUpdate    -> Random.Range(-0.0002, 0.0002)  // test scene
```

这一层已经从 C# wrapper 继续追到 Unity native internal-call 注册表。`UnityEngine.Random` 的相关
C# wrapper：

```text
UnityEngine.Random.Range(float, float) -> wasm func54300
UnityEngine.Random.InitState(int)      -> wasm func54299
UnityEngine.Random.get_seed()          -> wasm func54303
```

这些 wrapper 先通过 internal-call resolver 取 native function pointer：

```text
Range:     f_vkb(317095) -> "UnityEngine.Random::Range(System.Single,System.Single)"
InitState: f_vkb(333563) -> "UnityEngine.Random::InitState(System.Int32)"
get_seed:  f_vkb(347302) -> "UnityEngine.Random::get_seed()"
```

继续解析 internal-call 注册表后，已经恢复出实际 native wasm 函数：

```text
UnityEngine.Random::InitState -> table 129032 -> func82199
UnityEngine.Random::Range     -> table 129033 -> func82200
UnityEngine.Random::get_value -> table 129035 -> func82202
UnityEngine.Random::get_seed  -> table 129036 -> func82203
```

RNG 状态是 4 个 `uint32`。`InitState(seed)` 的状态初始化为：

```text
s0 = uint32(seed)
s1 = uint32(int32(s0) * 1812433253 + 1)
s2 = uint32(int32(s1) * 1812433253 + 1)
s3 = uint32(int32(s2) * 1812433253 + 1)
```

每次取随机数时：

```text
old0 = s0
old3 = s3
s0, s1, s2 = s1, s2, s3
x = uint32(old0 ^ (old0 << 11))
s3 = uint32(old3 ^ ((x >> 8) ^ x) ^ (old3 >> 19))
raw = s3
```

`Random.value` 使用：

```text
(raw & 0x7fffff) / 8388607
```

WAT 原始常量是：

```text
f32.const 0x1.000002p-23  // 约等于 1 / 8388607
```

`Random.Range(float min, float max)` 在 wasm 中按 f32 执行：

```text
t = Random.value
return min * t + (1 - t) * max
```

这个表达式和常见的 `min + t * (max - min)` 在分布上等价，但非对称区间下不保证逐 bit 完全相同。
对当前摩擦噪声 `Range(-0.0002, 0.0002)` 来说，分布仍是对称均匀扰动。

已经把这部分落成可执行原型：

```text
tools/reverse/recovered_unity_random.py
tools/reverse/recovered_curling_motion.py --unity-seed <seed>
tests/test_recovered_unity_random.py
```

例如 `RANDSEED=1` 的初始状态为：

```text
0x00000001, 0x6c078966, 0x714acb3f, 0xdbffe6dc
```

前 3 个 `Range(-0.0002, 0.0002)` 输出为：

```text
-0.00019987385894637555
-0.00010970510629704222
-0.0000723935299902223
```

`tools/reverse/recovered_curling_motion.py` 现在也能直接用该 RNG 生成 Unity 同款摩擦：

```powershell
D:\anaconda3\python.exe tools\reverse\recovered_curling_motion.py --vx 1 --vy 2 --angle 5 --unity-seed 1
```

第一步 dry friction 为：

```text
0.001 + (-0.00019987385894637555) = 0.0008001261410536245
```

也就是说，比赛代码层没有自写 RNG；它调用 Unity 引擎内置 RNG，但该 WebGL build 里的具体 native
实现已经可以本地复刻。当前训练实现的做法应调整为：

```text
1. 快速训练：可以继续用 0 噪声或普通均匀噪声加速；
2. 可复现训练/验证：使用 recovered_unity_random.py 按 RANDSEED 逐 tick 生成摩擦噪声；
3. Unity 对齐：AutoDCP 记录中有 RANDSEED 时，优先用该 seed 做 bit-level replay 验证。
```

唯一发现的 `UnityEngine.Random.InitState(seed)` 调用在 `AutoDCP.HandleMessage`。
它和记录回放有关：

```text
AutoDCP.recordedGame == false:
    INIParser.WriteValue(..., "RANDSEED", UnityEngine.Random.seed)

AutoDCP.recordedGame == true:
    seed = Convert.ToInt32(recordLoader.ReadValue(..., "RANDSEED", "0"))
    UnityEngine.Random.InitState(seed)
```

没有在 `DCP_HumanVSAI`、`DCP`、`FastDCP` 的 match start/FixedUpdate 路径中发现统一
`Random.InitState`。因此普通比赛 endpoint replay 应按随机过程处理；AutoDCP 录像回放
如果有 `RANDSEED` 字段，则可以复现 Unity RNG 序列。

## 已恢复的 Unity/协议坐标公式

这些公式来自 Unity 代码，不是样本拟合。

`DCP_HumanVSAI.SendMotionInfo` 对应 wasm `func60096`。它发送移动壶状态时使用：

```text
protocol_x  = teePosition.z - unity_position.z + 2.375
protocol_y  = teePosition.x - unity_position.x + 4.88
protocol_vx = -unity_velocity.z
protocol_vy = -unity_velocity.x
protocol_w  = unity_angularVelocity.y
```

`DCP_HumanVSAI.GetCurrentTrace` 对应 wasm `func60072`。它保存的是同一个坐标系，但没有协议偏移：

```text
trace_x = teePosition.z - unity_position.z
trace_y = teePosition.x - unity_position.x
```

对于 body 数组，顺序取决于 `firstShot`：

```text
firstShot == 0:
  body[4*i + 0], body[4*i + 1] = blue stone i trace_x, trace_y
  body[4*i + 2], body[4*i + 3] = red  stone i trace_x, trace_y

firstShot != 0:
  body[4*i + 0], body[4*i + 1] = red  stone i trace_x, trace_y
  body[4*i + 2], body[4*i + 3] = blue stone i trace_x, trace_y
```

`DCP_HumanVSAI.HandleHumanShot` 对应 wasm `func60092`。出手时 Unity 设置为：

```text
velocity = clamp(velocity, 0.0001, 6.0)
position = clamp(position, -2.23, 2.23)
rotation = clamp(rotation, -15.7, 15.7)

stone_list = (pGameState.WhiteToMove == 0) ? mBlueBalls : mRedBalls
stone_index = floor(pGameState.ShotNum * 0.5)
stone = stone_list[stone_index]

stone.transform.position.z = stone.transform.position.z - position
stone.rigidbody.velocity = (velocity, 0, 0)
stone.rigidbody.angularVelocity = (0, rotation, 0)
movingCurling = stone
shot = true
```

符号和 `SendMotionInfo` 能对上：正 Unity `velocity.x` 会变成负的协议 `motion_vy`；正 Unity `angularVelocity.y` 会变成正的协议 `motion_w`。

## 已恢复的 MOTIONINFO 尾段映射

官方协议的 `MOTIONINFO` 消息现在可以作为恢复物理 kernel 的验证锚点。`MOTIONINFO` 在移动壶到达中线时给出状态：

```text
motion_x, motion_y, motion_vx, motion_vy, motion_w
```

使用独立恢复模型 `tools/reverse/recovered_curling_motion.py` 时，最好的尾段 replay 约定是：

```text
x += motion_vx * 0.01
y += motion_vy * 0.01
speed = Newfrictionstep(0.001, (motion_vx, motion_vy), motion_w, 0.001)
```

换句话说，公共协议坐标可以直接积分尾段：

```text
sx = +1, sy = +1, sw = +1
position dt = 0.01 seconds
Newfrictionstep steptime parameter = 0.001
```

验证探针是：

```text
tools/reverse/probe_unity_tail_mapping.py
```

使用平均干摩擦、不复现 Unity RNG 的 no-sweep 经验验证结果：

```text
first 3 rows, dt=0.010: RMSE 0.0488 m, MAE 0.0450 m, max 0.0638 m
first 3 rows, dt=0.009: RMSE 1.4597 m
first 3 rows, dt=0.011: RMSE 1.5485 m
first 10 rows, dt=0.010: RMSE 0.0468 m, MAE 0.0419 m, max 0.0833 m
```

这强烈说明：对中线 `MOTIONINFO` 之后的无碰撞、无扫冰 rollout 来说，恢复出的 `Newfrictionstep` 公式和协议尾段坐标约定是正确的。剩余厘米级残差与已恢复的逐步摩擦随机噪声以及 Unity/JSON 四舍五入一致。

## 已恢复的扫冰流程

用户侧扫冰请求路径为：

```text
HumanInputController.OnSweepButtonClicked -> DCP_HumanVSAI.HandleHumanSweep
```

`HumanInputController.OnSweepButtonClicked`：

- 只有 `isHumanTurn` 为 true 时才生效；
- 读取 `sweepDistanceInput`；
- 如果输入为空或无法解析，默认用 `1.0`；
- 调用 `OnSweepRequested(distance)`。

`DCP_HumanVSAI.HandleHumanSweep(distance)`：

- 要求 `movingCurling != null`；
- 要求 `movingCurling.GetComponent<CurlingStoneNew>().allowSweep == true`；
- 记录请求距离日志；
- 设置场景里的 `Sweep` component：

```text
Sweep.isSweeping = true
Sweep.sweepDistance = distance
```

`Sweep` 对应 wasm `func60750..func60753`。字段为：

```text
sweepSpeed:    float  // default 2.0
movementDist:  float  // default 0.25
isSweeping:    bool
sweepDistance: float
isMovingFor:   bool   // default true
target:        GameObject
offset:        Vector3
sumnewZ:       float
```

`Sweep.Sweeper` 在 `FixedUpdate` 中调用，并读取 `Time.deltaTime` 来让视觉扫刷围绕目标壶移动。
在固定物理帧里它通常等于本帧物理时间，但函数调用名本身是 `Time.get_deltaTime`。恢复出的振荡逻辑是：

```text
direction = isMovingFor ? +2 : -2
sumnewZ += Time.deltaTime * sweepSpeed * movementDist * direction

if sumnewZ > movementDist:
    isMovingFor = false
elif sumnewZ < -movementDist:
    isMovingFor = true

sweeper.position = target.position + offset + (0, 0, sumnewZ)
```

停止逻辑也在 `Sweep.Sweeper` 中。现在已经用 `tools/reverse/resolve_metadata_refs.py`
把 metadata slot 解析回了字符串名，因此这个窗口不是匿名判断：

```text
target.position.x < Hogline2.position.x
target.position.x < Midline.position.x + sweepDistance
```

如果任一条件失败，Unity 清除：

```text
Sweep.isSweeping = false
Sweep.sweepDistance = 0
```

这意味着 `sweepDistance` 控制场景里的 `Sweep.isSweeping` 标志保持多久；它不是摩擦的连续倍增/倍减系数。

资产层也验证了这两个 trigger 是普通 `BoxCollider(isTrigger=true)`。正式场景里典型坐标为：

```text
Hogline1.x ~= 3.695
Midline.x  ~= 14.58
Hogline2.x ~= 25.57
```

因此 `SWEEP distance` 的实际窗口可以近似写成：

```text
start: moving stone hits Midline
end:   moving_stone.x >= min(Midline.x + sweepDistance, Hogline2.x)
max physical sweep window ~= 25.57 - 14.58 = 10.99 m
```

也就是说，`distance` 再大也不会让扫冰越过 `Hogline2`。

`Sweep.FixedUpdate` 根据当前 scene name 找不同 controller/sweeper target：

```text
FastGame  -> GameObject.Find("FastDCP").GetComponent<FastDCP>().movingCurling
AutoGame  -> GameObject.Find("AutoDCP").GetComponent<AutoDCP>().movingCurling
HumanVsAI -> GameObject.Find("DCP_HumanVSAI").GetComponent<DCP_HumanVSAI>().movingCurling
default   -> GameObject.Find("DCP").GetComponent<DCP>().movingCurling
```

对应 byte offsets 分别是：

```text
FastDCP.movingCurling      // 0xD4 = 212
AutoDCP.movingCurling      // 0xF0 = 240
DCP_HumanVSAI.movingCurling // 0x104 = 260
DCP.movingCurling          // 0xE8 = 232
```

所以扫刷 target 就是当前运动壶。

此外，`Sweep.FixedUpdate` 会根据当前运动壶和 `Hogline2` 的 Unity `position.x` 比较来开关
扫刷 Renderer：

```text
sweeperRenderer.enabled = movingCurling.position.x < Hogline2.position.x
```

对本地模拟器的实际含义：

- 请求扫冰控制低摩擦模式持续多久；
- 活跃扫冰期间摩擦大小固定在约 `0.0006`，不与请求距离成比例；
- 是否允许扫冰由 `CurlingStoneNew.allowSweep` 控制，而它由 trigger zone 切换。

## 已恢复的出手输入映射

`DCP_HumanVSAI.HandleHumanShot` 对应 wasm `func60092`。输入 clamp 为：

```text
velocity:          [0.0001, 6.0]
horizontal offset: [-2.23, 2.23]
rotation:          [-15.7, 15.7]
```

它用下面方式从蓝/红壶列表里选当前壶：

```text
stone_index = floor(current_shot_index * 0.5)
```

然后：

- 用请求的 horizontal offset 放置选中的壶；
- 用请求的 `velocity` 设置 `Rigidbody.velocity`；
- 用请求的 `rotation` 设置 `Rigidbody.angularVelocity`；
- 标记 `movingCurling` 和出手进行中状态。

Unity 内部 `Vector3` 轴约定已经通过 `HandleHumanShot` 和 `SendMotionInfo` 对上；公共协议尾段约定也已经锁定：`motion_x/y/vx/vy/w` 可以直接用 `position dt = 0.01` 和 `Newfrictionstep(..., steptime = 0.001)` replay。

### 正式 BESTSHOT 协议入口

正式比赛/机器人 socket 入口不是 `HandleHumanShot`，而是各 controller 的 `HandleMessage`：

```text
DCP.HandleMessage            -> wasm func61066
DCP_HumanVSAI.HandleMessage  -> wasm func60060
FastDCP.HandleMessage        -> wasm func60175
AutoDCP.HandleMessage        -> wasm func60864
```

`DCP`、`DCP_HumanVSAI` 和 `FastDCP` 的 `BESTSHOT` 分支已经逐行对过，核心释放逻辑一致。消息会先做：

```text
Regex.Replace(message, "[\s]+", " ").Trim().Split(' ')
```

然后要求消息所属玩家颜色等于当前 `pGameState.Player`。`BESTSHOT` 参数读取为：

```text
BESTSHOT velocity horizontal_offset rotation
```

注意：C# 数组对象在 wasm 里有对象头，所以反编译中看到的 `command[5]、command[6]、command[7]`
实际对应 split 后的第 1、2、3 个参数。

正式协议入口的 clamp 是：

```text
velocity:          if velocity < 0.0001 then 1.0; if velocity > 6.0 then 6.0
horizontal offset: [-2.23, 2.23]
rotation:          [-15.7, 15.7]
```

这和人类 UI 的 `HandleHumanShot` 不完全一样：人类 UI 的速度下限是 `0.0001`，正式 `BESTSHOT`
入口会把低于 `0.0001` 的速度改成 `1.0`。课程文档里写的 `0 <= v0 <= 6` 在 Unity release
实现中更准确应理解为：正常非负速度会原样进入，极小/负数异常速度会被保护性改成 `1.0`。

正式 `BESTSHOT` 的刚体释放流程是：

```text
stone_list = (pGameState.WhiteToMove == 0) ? mBlueBalls : mRedBalls
stone_index = floor(pGameState.ShotNum * 0.5)
stone = stone_list[stone_index]

stone.SetActive(true)
stone.rigidbody.position.z = stone.rigidbody.position.z - horizontal_offset
stone.collider.material.staticFriction = 0.0
stone.collider.material.dynamicFriction = 0.0
stone.rigidbody.velocity = (velocity, 0, 0)
stone.rigidbody.angularVelocity = (0, rotation, 0)
movingCurling = stone
shot = true
```

这里新增确认了一点：出手瞬间，当前运动壶的 `Collider.material` 摩擦被置为 `0.0/0.0`。
随后如果撞到其他壶，`CurlingStoneNew.OnCollisionEnter` 会把材质摩擦改回 `0.6/0.6`，并把
`mCollision = true`，从而停止自定义 `Newfrictionstep` 单壶积分，转入 Unity PhysX 碰撞路径。

### 正式 SWEEP 协议入口

`SWEEP` 分支同样在 `DCP`、`DCP_HumanVSAI`、`FastDCP` 中确认。消息形式为：

```text
SWEEP distance
```

生效条件是：

```text
消息玩家颜色 == 当前 pGameState.Player
movingCurling.GetComponent<CurlingStoneNew>().allowSweep == true
```

满足条件后，Unity 执行：

```text
GameObject.Find("Broom").GetComponent<Sweep>().isSweeping = true
Sweep.sweepDistance = parsed_distance
```

如果 `distance` 解析失败，会打印 `distance invalid`；反编译路径仍会把本地临时 float 写入
`sweepDistance`，实际等价于不要依赖非法输入。训练/比赛代码应始终发送合法浮点数。

结合前面 `FixedUpdate` 中恢复出的摩擦逻辑，`SWEEP distance` 的物理含义不是直接“多滑
distance 米”，而是打开低摩擦模式，直到 `Sweep.FixedUpdate` 根据运动壶和请求距离关闭扫冰。

### POSITION / RESETPOSITION 坐标入口

`POSITION` 分支会把协议中的 16 个壶坐标写回内部 `body` 数组。转换式是：

```text
body_x = protocol_x - 2.375
body_y = protocol_y - 4.88
```

这和 `SendMotionInfo`、`GetCurrentTrace` 的坐标公式闭合：

```text
protocol_x = trace_x + 2.375
protocol_y = trace_y + 4.88
```

`DCP.HandleMessage` 里还存在 `RESETPOSITION` 和 `RESETSTATE` 分支。它们主要用于课程平台/调试重置，
不是正式比赛 AI 的常规动作；但从逆向角度看，`RESETPOSITION` 使用的坐标转换同样是上面的
`-2.375/-4.88`。

### READY / NAME / RESET 类协议

这批分支已经确认不会改写主物理公式：

```text
NAME / CONNECTNAME
  -> 记录玩家名、更新等待界面显示

READYOK / READYOKNAME / READYOKCONNECTNAME
  -> 按 Player1/Player2 设置 player1Ready/player2Ready

RESETSTATE
  -> 调 ResetState 类逻辑，主要服务课程平台/调试重置

RESETPOSITION
  -> 当前玩家合法时，把传入坐标按 -2.375/-4.88 写入 body，准备重设局面
```

`READY/NAME` 影响的是开始前握手和 UI；`RESET*` 是外部调试/平台控制入口。它们不改变
`BESTSHOT/SWEEP` 到刚体释放、`Newfrictionstep`、扫冰摩擦和停壶状态机这些主比赛物理路径。

### 经验 BESTSHOT 到 MOTIONINFO 探针

这一节只应当作为验证/备用方案。权威 release mapping 已经从 `HandleMessage` 的正式
`BESTSHOT` 分支和 `HandleHumanShot` 的 UI 分支恢复；数据拟合不是主来源，也不应该成为主模拟器设计。

辅助工具：

```text
tools/reverse/probe_action_to_motioninfo.py
```

它拟合一个小的二次最小二乘模型：

```text
BESTSHOT(v0, h0, w0) -> MOTIONINFO(x, y, vx, vy, w)
```

在 `data/calibration/no_sweep_200.jsonl` 上，使用 190 条 in-play no-sweep 样本：

```text
motion_x:  RMSE 0.000107
motion_y:  RMSE 0.005249
motion_vx: RMSE 0.000045
motion_vy: RMSE 0.001221
motion_w:  RMSE 0.000428
final_x:   RMSE 0.024141
final_y:   RMSE 0.032637
```

粗略关系：

```text
motion_x ~= h0 + 2.346 plus spin curl before the middle line
motion_vy / v0 ~= -0.629
motion_w / w0 ~= 0.337
motion_vx / w0 ~= 0.010
```

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

## 已恢复的规则阈值

`DCP_HumanVSAI.GetStoneState` 对应 wasm `func60070`。它使用固定规则阈值：

```text
side bounds:       -2.23 < x < 2.23
valid y range:     -4.735 < y < 39.475
near hog/guard y:  -2.015, 0.145, 5.645
house radius:      sqrt(x*x + y*y) < 2.015
center line touch: abs(x) <= 0.145
```

对应 enum 已从 `dump.cs` 恢复：

```csharp
STATE_RINK = 1
STATE_PLAYAREA = 2
STATE_FREEGUARD = 4
STATE_HOUSE = 8
```

`AutoDCP`、`DCP`、`DCP_HumanVSAI`、`FastDCP` 的 `GetStoneState` 都映射到同一个
wasm 函数 `$f60070`，所以这组区域阈值是所有正式 controller 共用的。

`DCP_HumanVSAI.IsTouchingCenterLine` 对应 wasm `func60071`，精确为：

```text
abs(x) <= 0.145
```

`DCP_HumanVSAI.IsAllCurlingStoped` 对应 wasm `func60089`。它遍历两边壶列表，只要有任意活跃壶满足：

```text
velocity.x^2 + velocity.y^2 + velocity.z^2 > 0.000001
```

就返回 false。所以 Unity 的停止检查是平方速度阈值 `1e-6`，不是 `Newfrictionstep` 内部使用的 `0.01` 线速度 cutoff。

`DCP_HumanVSAI.UpdateState` / `DCP.UpdateState` 还包含 R7/中线相关的规则修正逻辑。
已确认字段：

```text
GameStateEx.ShotNum     // 0x08
GameStateEx.WhiteToMove // 0x18
GameStateEx.body        // 0x1C
GameStateEx.Player      // 0x20
```

`UpdateState` 每次会把 Unity 场景里的活跃壶位置写回 `GameStateEx.body`。写入坐标使用 tee 偏移：

```text
body_x = teePosition.z - stone.position.z
body_y = teePosition.x - stone.position.x
```

如果壶不活跃，或写回后不在有效保留区域：

```text
-2.23 < body_x < 2.23
-2.015 < body_y < 5.645
```

Unity 会把对应 `body` 槽清零，把壶移动回初始/备用位置，并 `SetActive(false)`。
所以出界/无效壶不是只在最终计分时忽略，而是在 `UpdateState` 中被写回、清零、失活。

关键条件能读出：

```text
只在 ShotNum >= 2 后进入检查；
按 ShotNum % 2 的同色/同队 parity 扫描既有壶；
候选壶位置要求：
    0.145 < y < 5.645
   -2.23 < x < 2.23
    sqrt(x*x + y*y) >= 2.015
中心线接触判断：
    abs(x) <= 0.145
```

当检测到相关违规时：

```text
DCP/DCP_HumanVSAI 会调用 SetStonesByBody(...) 回滚/重设 body；
非人类选择路径会发送 "CENTERLINE_VIOLATION" 给对应 Client；
HumanVsAI 且人类是被违规方时，调用 HumanInputController.ShowCenterlineViolationPanel(...)
让人类选择 keep/reset。
```

这段规则对单壶 rollout 不影响，但对完整比赛状态 replay 和训练环境的规则层很重要。

`CENTERLINE_CHOICE` 的正式 socket 分支也已经确认：

```text
CENTERLINE_CHOICE RESET
  -> 清 waitingForCenterlineChoice 和 timeout
  -> 把 r7BackupBodyState 复制回 GameStateEx.body
  -> 保存 lastBodyState
  -> SetStonesByBody(r7BackupBodyState)
  -> SendGameState()
  -> Invoke(SendGoCommand, 16.0)

CENTERLINE_CHOICE KEEP
  -> 清 waitingForCenterlineChoice 和 timeout
  -> 保留当前 GameStateEx.body
  -> 清掉当前备份引用
  -> SendGameState()
  -> Invoke(SendGoCommand, 16.0)
```

`DCP/FastDCP/DCP_HumanVSAI` 的主行为一致；`FastDCP` 额外会在处理后把
`Time.timeScale` 设回 `1.0`。该消息只有在 `waitingForCenterlineChoice == true`
且消息玩家等于 `centerlineViolatedTeam` 时才会生效。超时未回复时，`Update` 路径默认按
`KEEP` 继续。

`DCP_HumanVSAI.GetScore` 对应 wasm `func60074`。它不是调用 Unity 物理，而是直接读取
`GameStateEx.body` 计分。恢复出的逻辑：

```text
blue/even slots: body index 0,2,4,...
red/odd slots:   body index 1,3,5,...

忽略 x 和 y 同时接近 0 的空槽；
只考虑 house 内壶：sqrt(x*x + y*y) <= 2.015；
先找偶数槽最近距离 f；
再找奇数槽最近距离 g；

if f < g:
    score = 偶数槽中 distance < g 的壶数
elif f > g:
    score = - 奇数槽中 distance < f 的壶数
else:
    score = 0

if firstShot == 1:
    score = -score
```

所以 Unity 的局分是标准“谁最近，数到对方最近壶为止”的冰壶计分；符号最后会按先后手/颜色视角翻转。

## 已恢复的每壶结束状态机

正式比赛的“这一壶什么时候结束、什么时候轮到下一方、什么时候计分”不在单壶物理
`FixedUpdate` 里，而在各 controller 的 `Update` 里完成：

```text
DCP.Update       -> wasm func61097
FastDCP.Update   -> wasm func60201
AutoDCP.Update   -> wasm func60908
```

`DCP_HumanVSAI` 的普通比赛路径与上面同源，但还混有人类 UI 和 trace replay 分支；训练环境优先模拟
`DCP/FastDCP/AutoDCP` 的正式 AI-vs-AI 主路径即可。

主状态流已经能读成下面的伪代码：

```text
if !gameOver:
    Dispatch queued socket messages

if waitingForCenterlineChoice:
    centerlineChoiceTimeout += Time.unscaledDeltaTime
    if timeout reached:
        default to KEEP
        waitingForCenterlineChoice = false
        centerlineChoiceTimeout = 0
        if !recordedGame:
            SendGameState()
            Invoke(SendGoCommand, delay)

if shot && movingCurling != null:
    current_stone = stone_list[floor(ShotNum * 0.5)]
    if distance(current_stone.position, release_origin) > 1.0
       and current_stone.velocity.sqrMagnitude < 0.000001:
        log "Curling stop"
        current_stone.collider.material.staticFriction = 0.6
        current_stone.collider.material.dynamicFriction = 0.6
        Sweep.isSweeping = false

        if IsAllCurlingStoped():
            shot = false
            ShotNum += 1
            if recordedGame:
                SetStonesByBody(record_body)

            if ShotNum == 16:
                UpdateState()
                score[End] = GetScore()
                SendGameState()
                choose first shot for next end from score sign
                ShotNum = 0
                End += 1
                UpdateScoreBoard()
                if End < totalGame:
                    ResetStones()
                    UpdateState()
                    SendGameState()
                    SendGoCommand/NewGame after delay
                else:
                    SendTotalScore()
                    deactivate all stones
                    gameOver = true
            else:
                WhiteToMove ^= 1
                UpdateState()
                if !waitingForCenterlineChoice && !recordedGame:
                    SendGameState()
                    Invoke(SendGoCommand, delay)
```

关键细节：

- 当前壶必须从释放点实际移动超过 `1m`，才会进入“停壶收尾”判断。这避免释放前或刚激活时的零速度误判。
- 单壶停止阈值和全场停止阈值都是 `velocity.sqrMagnitude < 1e-6` 这一量级。
- 停壶后会强制关闭 `Sweep.isSweeping`，并把当前壶 collider 摩擦改回 `0.6/0.6`。
- 非第 16 壶时只翻转 `WhiteToMove`、调用 `UpdateState`、广播局面、延迟发下一次 `GO`。
- 第 16 壶时先 `UpdateState`，再 `GetScore` 写入 `score[End]`，再根据本局得分决定下一局先后手。
- `FastDCP` 的中线选择超时约为 `1s`；`DCP` 路径约为 `5s`。正式训练环境可以把它抽象成
  “CENTERLINE_CHOICE 未回复时默认 KEEP”。

`SendGoCommand` 行为也已确认。它会先清空 `movingCurling`，然后按当前 `WhiteToMove/Player`
给当前方 client 发送 `GO`，最后清掉 `shot` 并打开出手超时计数。`DCP_HumanVSAI` 如果轮到人类，
不会发 socket `GO`，而是打开 `HumanInputController` 的输入面板；这属于 UI 分支。

`Dispatch` 只是在 `Update` 里从 socket message queue 取消息并调用对应 `HandleMessage`：

```text
queue.TryDequeue(out message) -> HandleMessage(message)
```

因此本地训练环境的最小规则层可以不复刻线程/队列，只需要按同样顺序处理：

```text
BESTSHOT/SWEEP/CENTERLINE_CHOICE messages
-> physics rollout
-> stop check
-> UpdateState
-> GetScore if ShotNum == 16
-> SendGameState-equivalent observation
-> next GO/action request
```

## 已恢复的 SendGameState 协议

`SendGameState` 是 Unity 每次广播局面给 AI 的主出口：

```text
DCP.SendGameState       -> wasm func61069
FastDCP.SendGameState   -> wasm func60177
AutoDCP.SendGameState   -> wasm func60866
DCP_HumanVSAI.SendGameState -> wasm func60063
```

它主要发三类文本消息：

```text
POSITION x1 y1 x2 y2 ... x16 y16
SCORE score
SETSTATE ShotNum End Player WhiteToMove
```

`POSITION` 使用 `GameStateEx.body` 的规则坐标再加回协议偏移：

```text
if body_x == 0 and body_y == 0:
    send "0 0"
else:
    send_x = body_x + 2.375
    send_y = body_y + 4.88
```

`SETSTATE` 的前三个整数来自 `GameStateEx.ShotNum`、`GameStateEx.End`、`GameStateEx.Player`，
最后一个布尔/整数来自 `GameStateEx.WhiteToMove`。在 `DCP` 的特殊总局数分支里，
当 `totalGame == 7` 时第三项会发送 `-1`，这是平台/赛制控制分支，不影响单壶物理。

`SCORE` 只在完成一局或需要同步比分时发送。`FastDCP/DCP` 会对两个 client 发送相反视角的 score：
一方收到 `score`，另一方收到 `-score`。这解释了为什么 Unity 内部 `GetScore` 的符号还会再经过
先后手/玩家视角处理，不能把 socket 里某一方收到的 `SCORE` 直接当作全局绝对分。

## AutoDCP 记录/回放格式

`AutoDCP` 是唯一明确支持记录和复现随机种子的 controller。它的相关字段为：

```text
recordedGame      // 是否回放已有记录
recordParser      // 当前写记录的 INIParser
recordLoader      // 回放读取的 INIParser
autoGameRecorder  // AutoGame 总记录/排名相关 INIParser
```

每壶使用一个 section，section 名由当前局和当前壶拼成：

```text
section = End.ToString("D2") + ShotNum.ToString("D2")
```

例如第 0 局第 3 壶是 `0003`。`SendGameState` 每次还会写：

```text
[LASTSTATE]
LASTSTATE = section
```

每个 section 中已经确认的 key：

```text
BESTSHOT = BESTSHOT velocity horizontal_offset rotation
RANDSEED = UnityEngine.Random.seed
SWEEP    = SWEEP distance
POSITION = POSITION ...
SCORE    = SCORE ...
SETSTATE = SETSTATE ShotNum End Player WhiteToMove
```

`BESTSHOT` 分支在 `recordedGame == false` 时，先把原始 `BESTSHOT v h w` 写入当前 section。
释放刚体之后，它会立刻写：

```text
RANDSEED = UnityEngine.Random.seed
```

`recordedGame == true` 时，`BESTSHOT` 分支会从同一个 section 读取 `RANDSEED`，然后执行：

```text
UnityEngine.Random.InitState(Convert.ToInt32(RANDSEED))
```

因此 AutoGame 回放模式不是“重放每一帧轨迹”，而是用同样动作、同样 sweep、同样 Unity RNG seed
重新跑物理。

`AutoDCP.ReadMotionInfoFromRecord` 这个名字比较误导。它不是读取 `MOTIONINFO` 数值；实际逻辑是：

```text
section = End.ToString("D2") + ShotNum.ToString("D2")
sweep_message = recordLoader.ReadValue(section, "SWEEP", " ")
fake_player = "Player" + (pGameState.Player + 1)
HandleMessage((fake_player, sweep_message))
```

这个函数在 `CurlingStoneNew.OnTriggerEnter(Midline)` 的 AutoGame recorded 分支调用。
也就是说，壶过中线后，Unity 从记录文件取本壶的 `SWEEP` 命令，再走正式 `SWEEP` 协议入口。
这与普通比赛中 AI 在收到 `MOTIONINFO` 后自行发 `SWEEP` 的流程等价。

这给训练验证一个很好的方向：如果我们能生成或捕获 AutoGame 记录文件，就能得到
`BESTSHOT + RANDSEED + SWEEP` 的可复现实验，而不必依赖只含终点的数据盲猜摩擦噪声。

AutoDCP 的历史读取函数也已经对上：

```text
ReadPosition -> 读取 section/POSITION，写回 body 坐标
ReadState    -> 读取 section/SETSTATE，写回 ShotNum/End/Player/WhiteToMove
ReadBestshot -> 读取 section/BESTSHOT，伪造成 Player 消息并调用 HandleMessage
ReadTrace    -> 读取 section/TRACE，填充 lTrace
ReadScore    -> 读取 section/SCORE，写回 score
```

`TRACE` 是历史播放/可视化用的轨迹列表，不是正式 AI 交互里必需的物理输入。真正复现出手的核心仍然是
`BESTSHOT + RANDSEED + SWEEP`。

AutoDCP 还有一个会影响运行速度但不改变物理公式的静态设置：

```text
AutoDCP.timescale = 16.0
Awake -> Time.timeScale = AutoDCP.timescale
```

所以 AutoGame 自动赛程默认把 Unity 时间加速到 `16x`。这会影响真实等待时间和 `Invoke` 延迟，
但 `FixedUpdate` 中每个物理 tick 仍然调用同一个 `Newfrictionstep(..., 0.001)` 和同一个随机摩擦逻辑。
本地训练环境应复现固定 tick 的物理序列，不应把 `timescale=16` 当成新的摩擦或速度参数。

AutoDCP 的记录目录按 scene name 选择：

```text
GameScene       -> Records/8Games/
GameScene4Games -> Records/4Games/
FastGame        -> Records/4Games/
AutoGame        -> Records/4Games/
```

自动赛程结束时会更新 `AutoGame/rank.csv`，字段头为：

```text
团队名称,团队排名,小组积分,备注
```

这部分是赛程/排名外壳；目前没有证据显示它改写 `Newfrictionstep`、扫冰摩擦、碰撞材质或规则阈值。

## 目前还不知道什么

逆向已经显著缩小未知范围，但还有几项没有完全恢复。

### 1. 每个 kernel 的干净生产级代数实现

`fsimp` dispatch table 和 `Newfrictionstep` 汇编逻辑已经恢复到公式层，并翻译成了独立 Python 原型。仍缺的是更快、经过审计的生产实现，可能用 C++/NumPy/Numba，供训练 rollout 使用。

这很重要，因为 running-band 项里一个符号错误，在低旋转 shots 上可能看起来不明显，但在大 curl 和重扫冰 shots 上会放大。

### 2. 剩余 controller/回放/握手状态语义

重要的 Unity/协议轴映射已经从 `HandleHumanShot`、`SendMotionInfo`、`GetCurrentTrace` 中恢复：

```text
protocol_x  = teePosition.z - unity_position.z + 2.375
protocol_y  = teePosition.x - unity_position.x + 4.88
protocol_vx = -unity_velocity.z
protocol_vy = -unity_velocity.x
protocol_w  = unity_angularVelocity.y
```

metadata-use-to-string resolver 已经补上：`FastGame`、`AutoGame`、`HumanVsAI`、
`DCP`、`FastDCP`、`AutoDCP`、`DCP_HumanVSAI`、`Midline`、`Hogline2`、
`Stone`、`Wall` 这些关键对象名已经能从 wasm 里的 `d_[index]` 精确解析。

已经确认 `FastDCP + 212`、`AutoDCP + 240`、`DCP_HumanVSAI + 260`、`DCP + 232`
都指向各 controller 的 `movingCurling` 字段。全局 `OnTriggerEnter`/`OnCollisionEnter`
也已经查过：正式物理相关 trigger 基本集中在 `CurlingStoneNew` 与 `CrossLineEvent`，
`MotionTestStone` 是 level1 测试路径。

本轮已经补上 `UpdateState` 的 body 写回/出界清零逻辑、`GetScore` 的完整计分公式、
每壶结束状态机、`SendGameState` 主协议、`SendGoCommand` 行为，以及 AutoDCP 的
`BESTSHOT/RANDSEED/SWEEP/POSITION/SCORE/SETSTATE` 记录格式。因此“计分边界”、
“扫冰/中线 trigger”、“每壶何时推进”、“AutoGame 如何复现随机种子”和 AutoDCP
默认 `Time.timeScale=16` 都已明确；剩余主要是 UI、网络握手、自动赛程外壳和少数 controller 状态标志。

### 3. 随机性控制

`FixedUpdate` 每个 Unity fixed tick（`0.01s`）都会给 friction 加：

```text
Random.Range(-0.0002, 0.0002)
```

现在已经恢复了该 WebGL build 的 `UnityEngine.Random` native 实现，并落成
`tools/reverse/recovered_unity_random.py`。`AutoDCP.HandleMessage` 支持用 `RANDSEED`
记录/恢复 Unity RNG；`DCP_HumanVSAI`、`DCP`、`FastDCP` 没看到统一 `Random.InitState`。
因此剩余未知已经缩小为：

```text
1. 普通比赛模式的 Unity 初始 RNG state 是否可从外部固定；
2. 普通比赛模式若不能固定初始 state，是否需要把每局初始 seed 作为隐变量估计；
3. 是否要把 recovered RNG 接进 fast_curling_env，还是只在 Unity 对齐验证时启用。
```

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

### PhysX 4.1 源码交叉定位

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
这条线后来确认是通用 `Px1DConstraint` 行约束准备路径，不是石壶 contact point 的主结构。

继续拆 `func71272` 后，已经能把内部 helper 粗分出来：

```text
func71150 f_ofad
  初始化/清空 Dy::ThreadContext 一类的 contact/constraint 临时缓存，
  预分配 512/128 容量的数组区。

func71197 f_jhad
  扩容并拷贝 32-byte float records，底层来源标注为 PsArray.h。

func71174 f_mgad
  `Px1DConstraint` rows 的 preprocessRows。80-byte 输入 row 精确对应
  `PxConstraintDesc.h::Px1DConstraint`：offset 76 是 flags，offset 78 是 solveHint。
  它先按 solveHint 插入排序，再把 KEEPBIAS row 的 geometricError 复制到 forInternalUse，
  接着用两个 body 的 sqrtInvInertia 计算 angular row，最后按 solveHint 高/低 byte
  做 orthogonalize / diagonalize 分组处理。

func71175 f_ngad
  对小批量 `Px1DConstraint` row 做 3x3/四元数式迭代正交化，含 5 次迭代、
  sqrt、1e3/2e6 阈值。对应 PhysX 里的 diagonalize / orthogonalize 稳定化，
  不是冰壶专用公式。

func71176 f_ogad
  最终 1D constraint row block writer。它写入 48-byte header 和逐行 constraint：
  无 articulation 时每 row 96 byte，extended/articulation 时每 row 160 byte。
  对照 PhysX 4.1，这个尺寸精确对应 `DySolverConstraint1D.h` 里的
  `SolverConstraint1DHeader` / `SolverConstraint1D` / `SolverConstraint1DExt`，
  而不是 `SolverContactPoint`。`65535` 是 `PxSolverConstraintDesc::NO_LINK`。

func71177 f_pgad
  单 block fallback：先调用动态 constraint shader 填最多 12 个 80-byte `Px1DConstraint` row，
  再调用 func71176 写成最终 1D solver constraint block。
```

80-byte 输入 row 现在已经不是未知 blob，而是 `Px1DConstraint`：

```text
offset 0   linear0.xyz
offset 12  geometricError
offset 16  angular0.xyz
offset 28  velocityTarget
offset 32  linear1.xyz
offset 44  minImpulse
offset 48  angular1.xyz
offset 60  maxImpulse
offset 64  mods.spring.stiffness / mods.bounce.restitution
offset 68  mods.spring.damping / mods.bounce.velocityThreshold
offset 72  forInternalUse
offset 76  flags
offset 78  solveHint
```

`func71176` 的输出字段也能命名到 PhysX 1D row 结构级别：

```text
l[6]      = desc.constraint，分配出的 constraint block 指针
l[11]     = desc.constraintLengthOver16
header[0] = type，普通 row 为 `DY_SC_TYPE_RB_1D`，extended row 为 `DY_SC_TYPE_EXT_1D`
header[1] = count，后续 1D rows 数量
row[0..2] / row[4..6]   = lin0 / lin1
row[8..10] / row[12..14] = ang0 / ang1
row[3] / row[7]         = constant / unbiasedConstant
row[11] / row[15]       = velMultiplier / impulseMultiplier
row[16..18]             = ang0Writeback
row[20..23]             = minImpulse / maxImpulse / appliedForce / flags
extended row 追加 deltaVA / deltaVB，用于 articulation impulse response
input row 的 flags 和 bounce/spring 位会决定 restitution、bias 和 drive 公式分支
```

其中一个关键分支已经能读出物理含义：

```text
if inputRow[38] & 1:
  使用 inputRow[16], inputRow[17], inputRow[7], inputRow[3] 计算 restitution/bias 项
  若 inputRow[38] & 2，则走另一套缩放公式
else:
  使用 row effective mass 的倒数，并根据输入 flags 判断 bounce/threshold 分支
```

`func71176` 里原先标出的两处 `call_indirect` 已经能和 PhysX 4.1 对上：
它们不是普通 `Rigidbody` 的必经 vtable，而是 articulation/link 分支里的
`Articulation::getImpulseResponse`。`65535` 对应 PhysX 的
`PxSolverConstraintDesc::NO_LINK`；当 `linkIndexA/linkIndexB` 都是 `NO_LINK`
时，`func71176` 选择 96-byte `SolverConstraint1D` row，并直接用
`PxSolverBodyData` 计算 unit response。只有任一端不是 `NO_LINK` 时，才切到
160-byte `SolverConstraint1DExt` row，并通过 articulation vtable 计算对应 link 的响应。

普通刚体分支的公式层含义已经明确：

```text
resp0 = |lin0|^2 * invMass0 * linearScale0 + |ang0|^2 * angularScale0
resp1 = |lin1|^2 * invMass1 * linearScale1 + |ang1|^2 * angularScale1
unitResponse = resp0 + resp1
recipResponse = unitResponse <= minRowResponse ? 0 : 1 / unitResponse

非 spring 行:
  velMultiplier     = -recipResponse
  impulseMultiplier = 1
  若 restitution 条件成立:
    constant = unbiasedConstant = recipResponse * restitution * (-normalVel)
  否则:
    constant         = recipResponse * (velocityTarget - geometricError * recipDt)
    unbiasedConstant = recipResponse * (velocityTarget - internalBias * recipDt)
```

`func71169 f_hgad` 也已对上普通刚体的 `PxSolverBodyData::projectVelocity`：

```text
projectVelocity(lin, ang) =
  bodyData.linearVelocity.dot(lin) + bodyData.angularVelocity.dot(ang)
```

项目 dump 里能看到 Unity/ROS/BioIK 的通用 Joint 类型定义，但这些是库类型；
当前已恢复的冰壶石正式对象仍是 `Rigidbody + MeshCollider`，没有证据表明正式比赛
石壶碰撞依赖 joints 或 articulation。也就是说，`func71174/71175/71176/71177`
这条线把通用 1D constraint row 准备公式挖出来了，但它不是石壶接触点求解的核心缺口。
真正影响石壶碰撞的是 contact finalization：`func71103/func70963`
如何把 contact patches 写成 `SolverContactHeader` / `SolverContactPoint` /
`SolverContactFriction`。这一层现在也已经从“入口已知”推进到“核心字段和公式已知”。

`func71103` 的前半段精确对应 PhysX 4.1 的
`DyContactPrep.cpp::createFinalizeSolverContacts(...)`：

```text
func71103 / createFinalizeSolverContacts
  -> func71234 f_uiad = extractContacts
     从 PxsContactManagerOutput 抽取 normal、point、separation、
     materialFlags、maxImpulse、staticFriction、dynamicFriction、
     restitution、targetVel，并读取 invMass / invInertia scale。
  -> func71233 f_tiad = getFrictionPatches
     从上一帧 friction cache 恢复未 broken 的 friction anchors。
  -> func71216 f_ciad = createContactPatches
     按 normal/material/restitution/friction 把 contact 合并成 patches。
  -> func71217 f_diad = correlatePatches
     把 contact patches 和 friction patches 关联。
  -> func71218 f_eiad = growPatches
     按 correlationDistance / frictionOffsetThreshold 生成或扩展 friction anchors。
  -> reserveBlockStreams
  -> setupFinalizeSolverConstraints
```

`func70963` 对应 `DyContactPrep4.cpp::createFinalizeSolverContacts4(...)`，是 4 个
contact pair 的 batched path。它的前半段对每个 pair 重复上面的
`extractContacts/getFrictionPatches/createContactPatches/correlatePatches/growPatches`
流程，随后按 `SolverContactHeader4`、`SolverFrictionSharedData4`、
`SolverContactBatchPointBase4/Dynamic4`、`SolverContactFrictionBase4/Dynamic4`
计算 block stream 大小。若 4-pair batch 不可处理，PhysX 会回落到
`func71103` 的 single-pair path。

single-pair 普通刚体路径的输出结构已经能命名：

```text
SolverContactHeader  // wasm 32-bit build 中为 64 bytes
  type
  flags
  numNormalConstr
  numFrictionConstr
  angDom0 / angDom1
  invMass0 / invMass1
  staticFriction / dynamicFriction / dominance0 / dominance1
  normal / minAppliedImpulseForFriction
  broken / frictionBrokenWritebackByte / shapeInteraction

SolverContactPoint   // 48 bytes
  raXn
  rbXn
  velMultiplier
  biasedErr
  unbiasedErr
  maxImpulse

SolverContactFriction // 64 bytes
  normalXYZ_appliedForceW
  raXnXYZ_velMultiplierW
  rbXnXYZ_biasW
  targetVel
```

`func71104 f_udad` 已对上 `DyContactPrepShared.h::constructContactConstraint(...)`，
也就是逐接触点 normal constraint 的核心公式。它对每个 contact point 做：

```text
point = contact.point
normal = contact.normal
ra = point - bodyFrame0.p
rb = point - bodyFrame1.p
raXn = cross(ra, normal)
rbXn = cross(rb, normal)
raXnSqrtInertia = invSqrtInertia0 * raXn
rbXnSqrtInertia = invSqrtInertia1 * rbXn

unitResponse =
  invMass0 * dominance0 * |normal|^2
  + angDom0 * dot(raXnSqrtInertia, raXnSqrtInertia)
  + invMass1 * dominance1 * |normal|^2
  + angDom1 * dot(rbXnSqrtInertia, rbXnSqrtInertia)

velMultiplier = unitResponse > 0 ? 1 / unitResponse : 0
penetration = contact.separation - restDistance
scaledBias = velMultiplier * max(maxPenBias, penetration * invDt * 0.8)

如果 restitution > 0 且相对法向速度低于 bounceThreshold：
  targetVelocity += restitution * (-relativeNormalVelocity)

biasedErr   = targetVelocity * velMultiplier - scaledBias
unbiasedErr = targetVelocity * velMultiplier - max(scaledBias, 0)
maxImpulse  = contact.maxImpulse
```

`func71105 f_vdad` 是 `SolverContactFriction` 行的构造 helper。它为每个 friction
anchor 写两条切向约束：

```text
t0 = relativeLinearVelocity 去掉 normal 分量后的归一化方向
如果 t0 太小，fallback 到 normal 和坐标轴构造出的垂直方向
t1 = cross(normal, t0)

每个 anchor:
  ra/rb = body0/body1 anchor 旋转到世界
  error = (ra + bodyFrame0.p) - (rb + bodyFrame1.p)

每个 tangent:
  raXn = cross(ra, tangent)
  rbXn = cross(rb, tangent)
  response = invMass terms + angular response terms
  velMultiplier = response > 0 ? 0.8 / response : 0
  bias = dot(tangent, error) * invDt
  targetVel = dot(contact.targetVel, tangent) - relativeTangentVelocity
```

`func71173 f_lgad` 是接触/摩擦 helper 里调用的 impulse response 计算：普通刚体时直接用
`PxSolverBodyData` 的 invMass 和 sqrtInvInertia 计算线/角速度响应；如果 link index
不是 `65535`，才切到 articulation 的 `getImpulseResponse` 间接调用。正式冰壶石没有
articulation，因此主路径是普通刚体分支。

继续往 solver 迭代阶段追，`SolverContactPoint` / `SolverContactFriction` 被消费的
核心函数也已经定位到 wasm 函数：

```text
func71035 f_dbad
  对应 patch friction 的 solveContact 动态-动态主循环。
  用于 stone-stone 这类两端都是普通 Rigidbody 的接触。

func71036 f_ebad
  对应 patch friction 的 solveContact_BStatic 主循环。
  用于 stone-rink / stone-wall 这类 body1 为 static/kinematic 的接触。

func71041 f_jbad
  solveContactConcludeBlock 动态-动态 wrapper。
  先调用 func71035，再把 SolverContactPoint.biasedErr 替换成 unbiasedErr，
  并清空 friction appliedForce。

func71044 f_mbad
  solveContact_BStaticConcludeBlock 静态 body1 wrapper。
  先调用 func71036，再做同样的 conclude 处理。
```

`func71035` 的字段偏移和 `DySolverConstraints.cpp::solveContact(...)` 对得上：

```text
PxSolverConstraintDesc:
  desc.bodyA / desc.bodyB
  desc.constraint
  desc.constraintLengthOver16

SolverContactHeader:
  offset 0   type
  offset 2   numNormalConstr
  offset 3   numFrictionConstr
  offset 4   angDom0
  offset 8   angDom1
  offset 12  invMass0
  offset 16  staticFriction
  offset 20  dynamicFriction
  offset 24  dominance0
  offset 28  dominance1
  offset 32  normal.xyz
  offset 48  invMass1

SolverContactPoint, 48 bytes:
  float[0..2]  raXn
  float[4..6]  rbXn
  float[8]     velMultiplier
  float[9]     biasedErr
  float[10]    unbiasedErr
  float[11]    maxImpulse

SolverContactFriction, 64 bytes:
  float[0..2]  tangent normal
  float[3]     appliedForce
  float[4..6]  raXt
  float[7]     velMultiplier
  float[8..10] rbXt
  float[11]    bias
  float[12]    targetVel
```

动态-动态 normal contact 的实际迭代公式可以写成：

```text
old = appliedForce[i]
normalVel =
  dot(normal, linVel0) + dot(raXn, angVel0)
  - dot(normal, linVel1) - dot(rbXn, angVel1)

delta = max(biasedErr - velMultiplier * normalVel, -old)
newApplied = min(old + delta, maxImpulse)
delta = newApplied - old

linVel0 += normal * invMass0 * delta
linVel1 -= normal * invMass1 * delta
angVel0 += raXn * angDom0 * delta
angVel1 -= rbXn * angDom1 * delta
```

这一点在 `func71035` 中表现为：

```text
point[8]  = velMultiplier
point[9]  = biasedErr
point[11] = maxImpulse
forceBuffer[i] = min(maxImpulse, old + max(biasedErr - velMultiplier*normalVel, -old))
```

动态-动态 friction 行随后使用同一个 contact patch 累计出的 normal impulse：

```text
normalImpulseSum = sum(newApplied normal impulses in this patch)
staticLimit  = staticFriction  * normalImpulseSum
dynamicLimit = dynamicFriction * normalImpulseSum

old = friction.appliedForce
tangentVel =
  dot(tangent, linVel0) + dot(raXt, angVel0)
  - dot(tangent, linVel1) - dot(rbXt, angVel1)

candidate = old - velMultiplier * (bias - targetVel + tangentVel)

if abs(candidate) > staticLimit:
  newApplied = clamp(candidate, -dynamicLimit, dynamicLimit)
  broken = true
else:
  newApplied = candidate

delta = newApplied - old
用 tangent / raXt / rbXt 把 delta 写回两端线速度和角速度
```

`func71036` 是同一公式的静态 body1 版本：没有 body1 的速度项和写回项，只更新 body0。
这对 stone-rink 和 stone-wall 很关键：冰面/墙不吸收速度，所有冲量只改动石壶的线速度和角速度。

4-pair batch solver 的消费端也已经继续往下对到了 wasm。`func70963`
生成的 `SolverContactHeader4` / block stream 不是另一套物理模型，而是后续 4-wide
SIMD contact solver 的输入：

```text
func70917 f_pwzc
  对应 DySolverConstraintsBlock.cpp::solveContact4_Block(...)
  动态-动态 4-pair block solver。
  contact stride = 144 bytes，对应 SolverContactBatchPointDynamic4。
  同时读取/写回 bodyA 和 bodyB 的线速度、角速度。

func70919 f_rwzc
  对应 DySolverConstraintsBlock.cpp::solveContact4_StaticBlock(...)
  静态 body1 4-pair block solver。
  contact stride = 96 bytes，对应 SolverContactBatchPointBase4。
  只读取/写回 bodyA，适合 stone-rink / stone-wall 这类 static body1。

func70920 f_swzc
  对应 solveContactPreBlock_Conclude(...)
  先调用 func70917，再执行 concludeContact4_Block(dynamic)。

func70921 f_twzc
  对应 solveContactPreBlock_ConcludeStatic(...)
  先调用 func70919，再执行 concludeContact4_Block(static)。
```

`func70917` 的开头从 `desc[0..3].bodyA/bodyB` 读取 4 个 pair 的 body，
然后把 4 个 pair 的 `linearVelocity/angularState` 转置成 Vec4 lanes。
这与 PhysX 源码里的 `PX_TRANSPOSE_44` 完全对应。它随后按
`SolverContactHeader4` 读取：

```text
numNormalConstr / numFrictionConstr
appliedForces[numNormalConstr]        // Vec4，每个 lane 是一个 pair
SolverContactBatchPointDynamic4[]
optional maxImpulses[numNormalConstr]
SolverFrictionSharedData4
frictionAppliedForce[numFrictionConstr]
SolverContactFrictionDynamic4[]
```

动态-动态 4-wide normal 迭代公式和 single-pair 的 `func71035` 一样，
只是每个变量都是 4-lane Vec4：

```text
relVel =
  dot(normal, linVel0) - dot(normal, linVel1)
  + dot(raXn, angVel0) - dot(rbXn, angVel1)

delta = biasedErr - velMultiplier * relVel
delta = max(delta, -oldApplied)
newApplied = min(oldApplied + delta, maxImpulse)
delta = newApplied - oldApplied

linVel0 += normal * invMass0 * delta
linVel1 -= normal * invMass1 * delta
angVel0 += raXn * angDom0 * delta
angVel1 -= rbXn * angDom1 * delta
```

4-wide friction 也和 single-pair 一样，先用本 patch 的累计 normal impulse
给出 static/dynamic friction limit，然后在两个 tangent rows 上迭代：

```text
staticLimit  = staticFriction  * accumulatedNormalImpulse
dynamicLimit = dynamicFriction * accumulatedNormalImpulse

tangentVel =
  dot(tangent, linVel0) - dot(tangent, linVel1)
  + dot(raXt, angVel0) - dot(rbXt, angVel1)

candidate = oldApplied - scaledBias - velMultiplier * tangentVel

if abs(candidate) > staticLimit:
  newApplied = clamp(candidate, -dynamicLimit, dynamicLimit)
  broken = true
else:
  newApplied = candidate
```

`func70919` 是同一公式的静态 body1 版本：少掉 bodyB 的速度项和写回项。
这和 `func71036` 对 single-pair static contact 的作用完全一致。`func70920/70921`
的 conclude 部分则把 normal contact 里的 `biasedErr` 改成下一阶段使用的
`biasedErr - scaledBias`，并把 friction row 的 `scaledBias` 重置成
`targetVelocity`。在 wasm 里它表现为 144-byte 或 96-byte stride 上的
`a[23]-=a[19]`、`a[22]-=a[18]`、`c[6]=c[10]`、`c[7]=c[11]`
这类字段拷贝/替换。

因此 `func70963/createFinalizeSolverContacts4` 的求解端公式已经不再是未知：
它写出的 block stream 进入 `func70917/70919`，公式上等价于把 4 个 single-pair
patch contact 并排求解。剩余难点不是“4-wide 使用了另一种碰撞物理”，而是
把 `SolverContactHeader4`、`SolverContactBatchPoint*4`、
`SolverContactFriction*4` 的每个字段完整工程化翻译，并继续追上游
`func70574/func70576/func70030/func70051` 如何生成 contact 点。

`func70963` 的 batch field layout 也已经不再是纯未知。对照 PhysX 4.1
`DySolverContact4.h` 与 `DyContactPrep4.cpp::setupFinalizeSolverConstraints4(...)`，
32-bit wasm 下的 block stream 结构为：

```text
SolverContactHeader4                         // 192 bytes
Vec4 appliedNormalForces[numNormalConstr]    // 每个 Vec4 的 xyzw = 4 个 pair
SolverContactBatchPointBase4/Dynamic4[]      // static 96 bytes, dynamic 144 bytes
optional Vec4 maxImpulse[numNormalConstr]
SolverFrictionSharedData4                    // 128 bytes, 仅 numFrictionConstr > 0 时
Vec4 frictionAppliedForce[numFrictionConstr]
SolverContactFrictionBase4/Dynamic4[]        // static 96 bytes, dynamic 144 bytes
```

其中 `SolverContactHeader4` 字段为：

```text
offset 0    type
offset 1    numNormalConstr
offset 2    numFrictionConstr
offset 3    flag                              // bit0 = eHAS_MAX_IMPULSE
offset 4    flags[4]                          // 每个 pair 的 force-threshold 等 flags
offset 8    numNormalConstr0..3               // 4 个 pair 各自真实 normal contact 数
offset 12   numFrictionConstr0..3             // 4 个 pair 各自真实 friction row 数
offset 16   restitution
offset 32   staticFriction
offset 48   dynamicFriction
offset 64   invMass0D0
offset 80   invMass1D1
offset 96   angDom0
offset 112  angDom1
offset 128  normalX
offset 144  normalY
offset 160  normalZ
offset 176  shapeInteraction[4]
```

`SolverContactBatchPoint*4` 和 `SolverContactFriction*4` 的偏移也已经固定：

```text
SolverContactBatchPointBase4, 96 bytes:
  0 raXnX, 16 raXnY, 32 raXnZ,
  48 velMultiplier, 64 scaledBias, 80 biasedErr

SolverContactBatchPointDynamic4, 144 bytes:
  Base4 + 96 rbXnX, 112 rbXnY, 128 rbXnZ

SolverFrictionSharedData4, 128 bytes:
  0 broken, 16 frictionBrokenWritebackByte[4],
  32 normalX[2], 64 normalY[2], 96 normalZ[2]

SolverContactFrictionBase4, 96 bytes:
  0 raXnX, 16 raXnY, 32 raXnZ,
  48 scaledBias, 64 velMultiplier, 80 targetVelocity

SolverContactFrictionDynamic4, 144 bytes:
  Base4 + 96 rbXnX, 112 rbXnY, 128 rbXnZ
```

`func70963` 的写入逻辑也能和源码逐项对齐：

```text
1. 读取 4 个 PxSolverContactDesc，判断 isDynamic。
   只要任一 pair 的 body1 是 dynamic，就用 Dynamic4 结构；
   只有 4 个 pair 全是 static/kinematic body1 时才用 Base4 结构。

2. 读取 4 个 body 的 linearVelocity/angularVelocity、invMass、sqrtInvInertia、
   bodyFrame0/bodyFrame1，并转置成 Vec4 lanes。

3. 对每个 friction patch index：
   totalContacts = max(clampedContacts0..3)
   写 header 与 appliedNormalForces，并把较少 contact 的 pair 用 0 padding。

4. 对每个 contact row：
   point/targetVel/separation/maxImpulse 从 4 个 ContactPoint 合并成 Vec4；
   ra = point - bodyFrame0.p，rb = point - bodyFrame1.p；
   raXn/rbXn 乘 sqrtInvInertia 后写入 BatchPoint；
   velMultiplier、scaledBias、biasedErr 用和 single-pair 相同的 response/restitution 公式计算。

5. 对每个 friction anchor：
   anchorCount 每个 pair 最多 2 个；
   若 material flag 有 eDISABLE_FRICTION，则该 pair 的 friction row 数为 0；
   若 eIMPROVED_PATCH_FRICTION 且 anchorCount == 2，static/dynamic friction 系数乘 0.5；
   每个 anchor 写两条 tangent row，因此 numFrictionConstr = maxAnchorCount * 2。
```

normal row 的字段可以进一步写成：

```text
normalX/Y/Z = transpose(contactBase[0..3].normal)
relNorVel = dot(normal, linVel0) - dot(normal, linVel1)

对每个 contact row:
  pointX/Y/Z = transpose(con0..con3.point)
  targetVelX/Y/Z = transpose(con0..con3.targetVel)
  separation = Vec4(con0..con3.separation)

  ra = point - bodyFrame0.p
  rb = point - bodyFrame1.p

  rawRaXn = cross(ra, normal)
  rawRbXn = cross(rb, normal)

  delAngVel0 = sqrtInvInertia0 * rawRaXn
  delAngVel1 = sqrtInvInertia1 * rawRbXn

  unitResponse =
    invMass0D0
    + angDom0 * dot(delAngVel0, delAngVel0)
    + invMass1D1
    + angDom1 * dot(delAngVel1, delAngVel1)   // dynamic body1 时

  vrel =
    relNorVel
    + dot(rawRaXn, angVel0)
    - dot(rawRbXn, angVel1)

  velMultiplier = unitResponse > 0 ? 1 / unitResponse : 0
  penetration = separation - restDistance
  scaledBias = max(maxPenBias, penetration * invDt * 0.8) * velMultiplier

  若 restitution 条件成立:
    scaledBias = 0
    targetVelocity = velMultiplier * vrel * restitution
  否则:
    scaledBias = -scaledBias
    targetVelocity = 0

  biasedErr = targetVelocity + scaledBias
              - (vrel - dot(contact.targetVel, normal)) * velMultiplier
```

写入 `SolverContactBatchPointBase4/Dynamic4` 时，结构体字段名叫
`raXnX/raXnY/raXnZ` 和 `rbXnX/rbXnY/rbXnZ`，但实际存的是
`sqrtInvInertia * cross(r, n)` 后的 solver-space 角速度响应向量。
这和 single-pair path 里的 `raXnSqrtInertia/rbXnSqrtInertia` 是同一层含义。

friction row 的写入也能明确到公式级：

```text
vrelTangentCandidate = relativeLinearVelocity - normal * relNorVel

如果 |vrelTangentCandidate|^2 > 0.0001:
  t0 = normalize(vrelTangentCandidate)
否则:
  t0 = normal 的稳定垂直 fallback

t1 = cross(normal, t0)

SolverFrictionSharedData4:
  broken = false
  frictionBrokenWritebackByte[0..3] = desc[i].frictionPtr + patchWritebackIndex * sizeof(FrictionPatch)
  normal[0] = t0
  normal[1] = t1
```

对每个 friction anchor，`func70963` 写两条 row：`f0` 对应 `t0`，
`f1` 对应 `t1`。每条 row 的公式相同：

```text
ra = rotate(bodyFrame0.q, frictionPatch.body0Anchors[index])
rb = rotate(bodyFrame1.q, frictionPatch.body1Anchors[index])
error = (bodyFrame0.p + ra) - (bodyFrame1.p + rb)

rawRaXt = cross(ra, tangent)
rawRbXt = cross(rb, tangent)

delAngVel0 = sqrtInvInertia0 * rawRaXt
delAngVel1 = sqrtInvInertia1 * rawRbXt

response =
  invMass0D0
  + angDom0 * dot(delAngVel0, delAngVel0)
  + invMass1D1
  + angDom1 * dot(delAngVel1, delAngVel1)   // dynamic body1 时

velMultiplier = response > 0 ? 0.8 / response : 0

vrel =
  dot(tangent, linVel0) + dot(rawRaXt, angVel0)
  - dot(tangent, linVel1) - dot(rawRbXt, angVel1)

target = dot(contact.targetVel, tangent) - vrel
bias = dot(tangent, error) * invDt

row.targetVelocity = -target * velMultiplier
row.scaledBias = (bias - target) * velMultiplier
row.velMultiplier = velMultiplier
row.raXn = delAngVel0
row.rbXn = delAngVel1   // dynamic body1 时
```

如果某个 lane 的 anchor 数不足当前 `j`，`maxImpulseScale` 会把该 lane 的 tangent
向量和 `velMultiplier` 归零；这就是 4 个 pair contact/friction 数不一致时的 padding
机制。`contactID == 0xffff` 时，friction row 的 target velocity 使用该 patch 的
`contactBase.targetVel` fallback，否则使用对应 contact 的 `targetVel`。

这说明 `func70963` 剩余的“batch field layout”已经缩小为更细的工程化工作：
把 `DyContactPrep4.cpp` 里 normal row 与 friction row 的每个 Vec4 写入偏移完整转成
本地结构体即可；它的尺寸、顺序、padding、dynamic/static 分支和主要字段含义已经对上。

同时排除了一条容易误读的支线：`func70937/func70941/func70942/func70947`
属于 `DySolverPFConstraints.cpp` / `DySolverControlPF.cpp` 的 Coulomb/PF 分支。
这些函数也实现 contact/friction 求解，但当前 Unity 资源 `PhysicsManager.frictionType = 0`
选的是 patch friction，不是 Coulomb 1D/2D，因此它们不是正式比赛主路径。

`func71272` 附近的上游流程要拆成两类，不应混在一起：

```text
contact finalization lane
  -> 读取 body/core 数据和 contact manager flags
  -> extractContacts 写入 ThreadContext.mContactBuffer
  -> getFrictionPatches 复用上一帧未 broken 的 friction anchors
  -> createContactPatches 按 material/restitution/friction/normal 合并 contact patch
  -> correlatePatches / growPatches 复用或生成 friction patch
  -> contact[15]/[11] 先填入 +/-Infinity sentinel
  -> 4 个 pair 走 func70963/createFinalizeSolverContacts4
  -> single pair 走 func71103/createFinalizeSolverContacts
  -> 写出 SolverContactHeader / SolverContactPoint / SolverContactFriction

generic 1D constraint lane
  -> constraint shader 生成最多 12 个 80-byte Px1DConstraint rows
  -> func71174/preprocessRows 排序、KEEPBIAS 处理、sqrtInvInertia、正交化
  -> func71176/SetupSolverConstraint 写出 SolverConstraint1D header 和 rows
```

这说明 `func71272` 附近同时有 contact task 和通用 constraint row prep 相关代码，
不能把所有 constraint 字样都误读成石壶接触点公式。剩余不确定处主要在
`func70574/func70576/func70030` 内部各个 inlined PhysX 模板如何进一步还原成干净代码，
以及 `func70963` 写出的 4-wide batch normal/friction row 如何逐偏移落成本地结构体。`func71103` 的 single-pair
contact finalization 已经能映射到 PhysX 的 `SolverContactHeader` /
`SolverContactPoint` / `SolverContactFriction` 字段和核心公式；`func71035/func71036`
又把 single-pair patch contact 的迭代冲量公式对到了 wasm；`func70917/func70919`
则把 4-wide block path 的动态/静态迭代公式也对到了 wasm。接触点生成的宏观流程已经不是未知：
它是 PhysX PCM + GJK/EPA + SAT/mesh midphase，再进入 patch friction contact solver，
不是冰壶项目自写二维闭式公式。

这比“只有 PhysX 字符串”更进一步：已经定位到 narrowphase 表、关键 shape contact generator、
contact finalization 表、manifold refresh/contact reduction/ContactBuffer 写入、
single-pair contact constraint 写出公式、single-pair 和 4-wide
solver 迭代公式，以及一条通用 1D constraint row 准备链。但它仍是 PhysX 通用求解器的数据结构，
不是冰壶专用闭式碰撞公式。要完全复现碰撞，需要继续把
`func70574/func70576/func70030`、`func70051` 和 `func70963` 的 normal/friction row 写入落成结构化代码，
或者用标准 PhysX 近似参数加样本验证。

这说明 PhysX 并不是完全“看不见”。更准确地说：正式碰撞求解已经进入 Unity/PhysX native wasm，
并且具体任务函数已经定位，但这些函数是数百到上千行的低层 contact/constraint 求解代码，
包含 contact patch、body data、constraint descriptor、batch/partition 等结构，距离可直接写进
本地模拟器的简洁“石壶碰撞公式”还有一层艰苦翻译。

我们已经足够构建很好的无碰撞 rollout 模拟器。对多壶碰撞，single-pair 的
normal/friction 约束写出与迭代公式、4-wide batch solver 的迭代公式都已经不再是黑箱；
convex-convex 的 face/edge 裁剪候选点生成也已经对到 PhysX 源码；stone-rink 的
triangle SAT、active edge、deferred contacts、edge/vertex cache 和 patch reduction
也已经对到源码规则。现在还不足以保证精确复现多壶碰撞后的速度/角速度转移，是因为这些
通用 PhysX 模板还没有完整落成本地可运行代码，`Plane` 使用的
`unity default resources:10209` 已经能定位为 Unity 内置 Plane/`New-Plane.fbx`
路径，但具体顶点顺序、三角形索引顺序和运行时 PhysX cooking 结果还没直接导出；
动态生成 convex MeshCollider 的 cooking 前 mesh、setter 顺序和 `RecalculateNormals`
已经锁定，但在 WebGL build 里的最终 cooked convex hull 结果，以及
restitution/friction combine 的运行细节仍需要碰撞样本或更深层 Unity/PhysX 行为验证。

因此当前正确边界是：碰撞半径、质量、材质、全局 PhysX 配置、narrowphase 表地址和关键
shape contact 函数号已经可恢复；没有再发现正式比赛路径里可替代 PhysX 的 C# 碰撞公式。
逐接触点 normal/friction constraint 的 single-pair 写出与 single/batch 迭代公式已经能对到
PhysX 源码和 wasm，convex-convex 候选点生成、convex-mesh triangle 接触生成和
mesh patch reduction 也已经对到源码级规则，但仍不是完整本地碰撞引擎；
除非继续把 `func70532/func70533/func70030/func70051` 以及 contact finalization 的
`func70963` normal/friction row 写入等落成可读模型，否则训练环境仍应先用近似碰撞并用
正碰/偏碰样本验证误差。

### 5. 协议入口状态位和异常分支

公共动作到 Unity 刚体释放的主路径已经恢复：

```text
BESTSHOT velocity horizontal_offset rotation
  -> Rigidbody.velocity = (velocity, 0, 0)
  -> Rigidbody.angularVelocity = (0, rotation, 0)
  -> Rigidbody.position.z -= horizontal_offset

SWEEP distance
  -> Sweep.isSweeping = true
  -> Sweep.sweepDistance = distance

POSITION x1 y1 ... x16 y16
  -> body_x = x - 2.375
  -> body_y = y - 4.88
```

正式 socket `BESTSHOT` 的速度异常下限也已经确认：`velocity < 0.0001` 时会被改成 `1.0`。
这不同于人类 UI 分支的 `0.0001` 下限。

剩余未知已经不是“动作参数怎么变成速度/角速度”，而是少量 controller 状态位和异常分支：

```text
1. READYOK/NAME/CONNECTNAME 的 UI 显示和联网等待细节；
2. RESETSTATE/RESETPOSITION 的外部平台重置细节；
3. AutoDCP 进程重启、文件复制和排名输出的完整自动赛程细节。
```

这些分支会影响通信流程和回放，但不会改变已经恢复出的主出手物理入口。

### 6. 已恢复但仍需工程化实现的规则层

`GetStoneState`、`IsAllCurlingStoped`、`GetCurrentTrace`、`UpdateState` 和 `GetScore`
的核心公式已经恢复；`DCP/FastDCP/AutoDCP.Update` 的每壶结束状态机也已经恢复到主路径。
停止阈值、出界/失活清零、house 半径、局分计算、`SendGameState` 时机都可直接实现。
剩余不是公式未知，而是要把这些规则无歧义地落到本地训练环境里，并用 Unity 样本验证：

```text
1. DCP_HumanVSAI 的人类 UI 分支是否完全可以从训练环境里剥离；
2. AutoDCP 进程重启/文件复制/排名输出分支的完整自动赛程细节；
3. 本地训练是否需要完全复现 socket queue/timeout，还是只保留同步 step API。
```

## 训练角度的未知项优先级

对训练来说，未知项的重要性不同：

1. 最高优先级：把 `Newfrictionstep + fsimp` 精确翻译到足够可用的单壶无碰撞 rollout，实现以上恢复公式。
2. 最高优先级：把扫冰实现为“持续时间门控的低摩擦 stepping”，并包含逐步随机 friction。
3. 高优先级：把已恢复的 `Update/SendGameState/SendGoCommand` 状态机落成本地训练规则层。
4. 高优先级：利用 AutoGame `RANDSEED` 和已恢复 RNG 生成可复现实验；快速训练可继续用均匀噪声采样。
5. 中优先级：验证或近似 Unity PhysX 的石壶-石壶/石壶-冰面碰撞；若追求更高保真，把已恢复的 convex-convex 候选点生成、convex-mesh triangle SAT/deferred contact/cache/reduction，以及 `func70963` 的 normal/friction row 写入落成本地结构体。
6. 中优先级：继续恢复 UI/网络握手/自动赛程状态位，尤其是 READY/NAME/RESET/排名输出分支。
7. 低优先级：精确 UI、网络、计分显示、上传、人类输入细节。

## 实用结论

Unity 模拟器不是不可知黑箱。关键运动模型已经可恢复到足以指导本地模拟器：

- 我们可以匹配 Unity 使用的精确常量。
- 我们可以复现同样的 `Newfrictionstep` 结构。
- 我们已经可以从 no-sweep 的协议 `MOTIONINFO` 尾段 replay 到 endpoint，使用平均干摩擦时 RMSE 约 5 cm。
- `BESTSHOT/SWEEP/POSITION/MOTIONINFO` 主协议入口已经从代码恢复，不需要靠数据蒙。
- 每壶结束、下一壶 `GO`、一局结束计分、`POSITION/SCORE/SETSTATE` 同步的主状态机已经恢复。
- AutoDCP 记录格式和 `RANDSEED` 回放方式已经恢复，可以作为可复现实验入口。
- AutoGame 默认 `Time.timeScale=16` 已确认；这是自动赛程加速，不是新物理参数。
- `UnityEngine.Random.Range/InitState/get_value/get_seed` 的 native wasm 实现已经恢复，并已接入 recovered 物理原型。
- `MotionTestStone` 碰撞 helper 已确认是测试路径，正式碰撞仍是 Unity PhysX；石壶 `ExtendedColliders3D.generateVerticesAndTriangles` 的 cylinder mesh 已恢复：512 vertices、3060 indices、1020 triangles、上下 cap 中点交替 ear triangulation、`flipFaces=true`，正式场景 world radius 约 `0.140875m`；`Awake/generateMesh` 的 internal-call 已确认会设置 `Collider.enabled`、`MeshCollider.sharedMesh`、`MeshCollider.convex`、`Collider.isTrigger`、`Collider.material`，并在 mesh 生成后调用 `Mesh.RecalculateNormals`，但没有显式写 `MeshCollider.cookingOptions`。PhysX solver task 已定位到 `func71248/func71257/func71259/func71263/func71269/func71272/func71273`，contact manager 更新为 `func70739`，PCM narrowphase 表为 `4117968`，关键 shape contact 为 `func70574/func70576/func70577/func70030`；convex-convex/box-convex 的 face/edge SAT、reference/incident polygon 裁剪、face-vertex/vertex-face/edge-edge 候选点生成已经对到源码级规则；stone-rink 的 triangle face/poly face/active edge SAT、deferred contact、edge/vertex cache、patch 合并与 reduction 也已经对到源码级规则；`Plane` MeshCollider 的 `m_Convex=false`、`m_CookingOptions=30`、`m_Material=Ice`、`m_Mesh=unity default resources:10209` 已恢复。`ContactPoint/ContactBuffer` 的 64-byte/4112-byte 布局也已固定。contact finalization 表已定位到 `func71103/createFinalizeSolverContacts` 与 `func70963/createFinalizeSolverContacts4`，并确认 `frictionType=0` 走 PhysX `ePATCH` 分支。`func71103` 的 single-pair normal/friction constraint 已经对到 `SolverContactHeader`、`SolverContactPoint`、`SolverContactFriction` 和 `func71104/func71105/func71173` helper；`func70963` 的 4-wide block stream 顺序和 `SolverContactHeader4`、`SolverContactBatchPoint*4`、`SolverFrictionSharedData4`、`SolverContactFriction*4` 尺寸已经对到 PhysX；`func71035/func71036` 已对到 patch contact solver 的动态-动态/静态 body1 迭代冲量公式；`func70917/func70919` 已对到 4-wide block solver 的动态-动态/静态 body1 迭代冲量公式，`func70920/func70921` 是对应 conclude wrapper；另一路 `func71174/func71175/func71176` 已确认是 `Px1DConstraint` 通用行约束准备路径，不应再误当成石壶 contact point 主路径。
- 剩余难点是把 23 个 kernel 函数、Simpson 积分器和已恢复 RNG 接入更快的生产代码；碰撞侧则是把已恢复的 PhysX 接触/solver 规则工程化，并直接导出或重建 Plane 内置 mesh 的索引顺序与 convex cooking 后几何。

推荐下一步：

1. 保留 `tools/reverse/recovered_curling_motion.py` 作为参考模型，并把它移植成更快的训练实现。
2. 直接实现已恢复的 `HandleMessage/Update/SendGameState` 和坐标变换公式，而不是从数据拟合 release 行为。
3. 解析剩余 controller 方法语义，重点是握手、重置、AutoDCP 自动赛程/排名输出分支。
4. 把 `--unity-seed` 摩擦噪声入口接到 AutoDCP `BESTSHOT + RANDSEED + SWEEP` replay/校准流程。
5. 在信任本地模拟器做战术 self-play 前，补充碰撞验证样本；必要时把已恢复的 PhysX convex-convex/convex-mesh 接触生成、`func70051` reduction 和 `func70963` 写出的 4-wide normal/friction rows 工程化实现，并锁死 Plane 内置 mesh 顶点。

## 当前逆向边界

稳定工具链为：

1. 对 `build.wasm` 和 `global-metadata.dat` 使用 Il2CppDumper。
2. 用 `script.json` 把 IL2CPP 方法映射到 dynCall method pointer ID。
3. 通过 wasm indirect function table 解析 dynCall ID。
4. 检查对应 WAT 函数。
5. 用 `tools/reverse/resolve_metadata_refs.py` 把 WABT 反编译里的 `f_xkb(address)` 和
   `d_[index]` 映射回字符串、类型和泛型方法。
6. 用 `tools/reverse/resolve_wasm_calls.py` 把 WABT 反编译里的调用别名，如 `f_kwjc`，
   映射回 `DCP_HumanVSAI.SendMotionInfo` 这类 IL2CPP 方法名。
7. 用 `tools/reverse/resolve_decompiled_string_refs.py` 把 WABT 反编译里的
   `f_vkb(309480)` 这类 wasm 线性内存字符串指针解析成
   `UnityEngine.MeshCollider::set_sharedMesh(UnityEngine.Mesh)` 等 internal-call 名称。
8. 用 `tools/reverse/list_decompiled_native_calls.py` 为 PhysX native wasm 函数列出
   `f_xxx -> funcNNNNN` 调用链，方便继续追非 IL2CPP 的低层 helper。
9. 用 `tools/reverse/inspect_unity_assets.py` 检查 Unity 资源里的 tag、PhysicsManager、
   Rigidbody、`ExtendedColliders3D` 动态 MeshCollider 参数，以及 Plane/Wall/Line
   collider 的 material、mesh PPtr、convex/cooking options；该工具也会递归计算
   Transform world matrix，用来核对 Plane/stone/wall 的真实世界位置和缩放。
10. 用 `tools/reverse/list_icall_registrations.py` 解析 `f_vvrd(name, functionPointer)`，
   把 Unity native internal-call 注册项映射到 wasm table function。
11. 用 `tools/reverse/find_decompiled_function_by_line.py` 从巨大 `build.dcmp` 行号反查所在
   wasm-decompile 函数，方便追 PhysX 字符串引用。
12. 用 `tools/reverse/recovered_unity_random.py` 本地复刻当前 WebGL build 的
    `UnityEngine.Random`。
13. 用 `tools/reverse/resolve_physx_task_metadata.py` 从 WAT data segment 读取 PhysX
    task metadata/vtable/function-table block，并把 table index 映射回 `funcNNNNN`。
14. 用 `tools/reverse/scan_wat_function_pointer_runs.py` 扫描 WAT data segment 中的
    连续 wasm function pointer，用来找静态函数表。
15. 用 `tools/reverse/find_physx_pcm_contact_table.py` 从 WAT 线性内存中扫描 PhysX
    7x7 contact method table，定位 `g_ContactMethodTable` 与 `g_PCMContactMethodTable`。
16. 用 NVIDIA PhysX 4.1 源码交叉定位 wasm 中的 `createFinalizeMethods`、
    `createFinalizeMethods4`、`createContactPatches`、`correlatePatches` 和
    `PxFrictionType` 枚举。
17. 用 `tools/reverse/find_physx_solver_vtables.py` 辅助扫描 PhysX solver vtable
    形状；本轮用它排查了 solver 表候选，并结合函数体确认 `func70937/70941/70942/70947`
    是 Coulomb/PF 支线，不是当前 patch friction 主路径。
18. 用 PhysX 4.1 的 `DySolverConstraintsBlock.cpp` 交叉确认
    `func70917/func70919/func70920/func70921`，把 4-wide patch contact block solver
    的动态/静态迭代公式和 conclude wrapper 对回 wasm。
19. 用 `tools/reverse/physx_contact4_layout.py` 生成 WebGL 32-bit 下
    `SolverContactHeader4`、`SolverContactBatchPoint*4`、`SolverFrictionSharedData4`
    和 `SolverContactFriction*4` 的 size/offset 表，避免后续手工数字段出错。
20. 用 `tools/reverse/physx_contact_buffer_layout.py` 生成 WebGL 32-bit 下
    `Gu::ContactPoint` 和 `Gu::ContactBuffer` 的 size/offset 表，确认 narrowphase
    写出的 contact 如何进入 contact finalization。
21. 用 `tools/reverse/recovered_extended_collider_mesh.py` 复原
    `ExtendedColliders3D.generateVerticesAndTriangles(...)` 的 cylinder mesh 生成规则，
    输出石壶 MeshCollider cooking 前的 vertices/triangles。

本 build 里的 metadata slot 关系是：

```text
address = 3705984 + 4 * d_index
```

例子：

```powershell
$base = Join-Path $env:TEMP 'curling_reverse_il2cpp'
D:\anaconda3\python.exe tools\reverse\resolve_metadata_refs.py `
  (Join-Path $base 'il2cpp_out\script.json') `
  (Join-Path $base 'dcmp_funcs\func60752.dcmp') `
  (Join-Path $base 'dcmp_funcs\func61030.dcmp') `
  (Join-Path $base 'dcmp_funcs\func61031.dcmp')

D:\anaconda3\python.exe tools\reverse\resolve_wasm_calls.py `
  (Join-Path $base 'il2cpp_out\script.json') `
  (Join-Path $base 'wasm_table_map.json') `
  (Join-Path $base 'build.dcmp') `
  (Join-Path $base 'dcmp_funcs\func61031.dcmp')
```

Cpp2IL 能把这个项目作为 WebAssembly 解析，并找到相同的 code/metadata registration 地址，但它的 IL recovery 目前会在导入的 WebGL 函数上中止，例如 `env.SetIMEText` 没有关联函数体。这意味着我们可以可靠恢复名字、常量、结构体、函数映射和 WAT 级行为，但不能不经手工反编译或更重的 Ghidra 工作流就拿到整个物理类的干净 C# 伪代码。

`fsimp` 特别难干净反编译，因为它把很多 force kernel 内联进嵌套的 `br_table` switch 后面。它仍然能识别为 `Newfrictionstep` 使用的 Simpson 积分器，并且 `Newfrictionstep` 调用它时参数为：

```text
fsimp(0, PI / 2, 1e-5, param, type, i)
```

## 本轮对模拟器的修正

本轮发现并修复了一个具体 calibration bug：

- `sweep_200.jsonl` 把 sweep 存成 `requested_sweep_distance`。
- `tools/calibration/fit_unity_samples.py` 之前只读取 `requested_sweep`。
- 修复前，所有官方 sweep 样本都被归一化成 `sweep = 0`。

同时也收紧了 fast simulator，使 `unity_landing_v2` calibration 会检查 calibrated sweep range。否则，一个只在某个 sweep 范围拟合的 calibration 可能被静默用于支持范围之外。

新的拟合文件：

- `config/unity_physics_calibration.json`

它现在是 `fast_curling_env.py` 优先加载的第一个 calibration 文件。

## 数据一致性检查

用以下数据重新拟合 `config/unity_physics_calibration.json` 后：

- `data/calibration/no_sweep_200.jsonl`
- `data/calibration/sweep_200.jsonl`

对 390 条可用样本做确定性 landing replay，结果为：

| bucket | RMSE total |
| --- | ---: |
| all samples | `0.1164 m` |
| sweep `0` | `0.0406 m` |
| sweep `2` | `0.0384 m` |
| sweep `4` | `0.0396 m` |
| sweep `6` | `0.0462 m` |
| sweep `8` | `0.0565 m` |
| sweep `10` | `0.3087 m` |
| sweep `12` | `0.2682 m` |

总误差 90 分位数约为 `0.0946 m`，但有一个 high-sweep outlier 约 `1.55 m`。这说明：

- no-sweep 和中等 sweep 与修正后的模拟器一致；
- high sweep 不能被简单 endpoint polynomial 很好表示；
- 逆向模型解释了原因：sweep 改变的是有效摩擦，因此把 sweep 当成线性出手后位移在结构上是错的。
