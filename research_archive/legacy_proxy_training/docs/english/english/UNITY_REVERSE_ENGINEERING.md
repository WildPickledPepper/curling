# Unity Reverse Engineering Notes

This note records what we can recover from the bundled official Unity/WebGL
curling simulator and what it means for a local training simulator.

## Package Shape

The local competition client is a Unity WebGL + IL2CPP build:

- `数字冰壶单机版_win/数字冰壶单机版/curling_server.exe`
- `数字冰壶单机版_win/数字冰壶单机版/web/Build/build.data.gz`
- `数字冰壶单机版_win/数字冰壶单机版/web/Build/build.wasm.gz`
- `数字冰壶单机版_win/数字冰壶单机版/web/Build/build.framework.js.gz`
- Unity version found in the asset bundle: `2022.3.62f2c1`
- IL2CPP metadata version: `31`

`curling_server.exe` is mainly the local server/bridge. Its config is in
`conf/config.ini`:

```ini
HttpPort = 9007
TcpPort = 7788
ConnectHost = "127.0.0.1"
CurlingServerHost = "http://127.0.0.1:8084"
RobotPython = "./resource"
```

## Recovered Unity Object Parameters

From Unity asset/type-tree inspection:

### PhysicMaterial

`Ice`:

- `dynamicFriction = 0.02`
- `staticFriction = 0.02`
- `bounciness = 0`
- `frictionCombine = 2`
- `bounceCombine = 2`

`Bouncy`:

- `dynamicFriction = 0.6`
- `staticFriction = 0.6`
- `bounciness = 1`
- `frictionCombine = 2`
- `bounceCombine = 2`

### Stone Rigidbody

Typical curling stone objects (`Curling stone blue*`, `Curling stone red*`):

- `mass = 19.1`
- `drag = 0`
- `angularDrag = 0.05`
- `useGravity = true`
- `isKinematic = false`
- `collisionDetection = 0 or 1`
- local scale around `(0.115, 0.115, 0.115)`

## Recovered Game Physics Constants

The following constants are embedded in both `DCP_HumanVSAI` and
`Assets.CurlingMotion`:

```csharp
PI = 3.1416
R = 0.125
DR = 0.006
FAI = 2
K = 0.2
STONEINFO_NEWFRICTION = 1
SWEEP_EFFECT = 0.4
```

These line up with the paper-style dry/wet curling friction model already
described in `docs/CURLING_PHYSICS_MODEL_ANALYSIS.md`.

## Recovered Data Structures

From `dump.cs`:

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
    public b2Vec2 v;   // 0x0
    public double angle; // 0x10
}
```

## Recovered Core Functions

`Assets.CurlingMotion` contains the local motion model:

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

Il2CppDumper maps these methods to dynCall method pointer IDs `12132..12155`.
The wasm indirect function table maps those IDs to real wasm functions:

| C# method | method pointer | wasm function |
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

The called math helpers were identified from wasm bodies:

- `$f5979 = cos`
- `$f5980 = sin`
- `$f54019 = atan`
- `$f56754 = pow`

## Ghidra Pass

I also installed a temporary Ghidra toolchain outside the repo:

- Ghidra `12.1.2` official build: can run headless, but has no native wasm
  loader.
- `ghidra-wasm-plugin` `v2.4.0`: provides a WebAssembly loader, but is built
  for Ghidra `12.0` and crashes on Ghidra `12.1.2`.
- Ghidra `12.0` official build + the wasm plugin: successfully imports
  `build.wasm`.
- JDK `21` is required by modern Ghidra; the system Java 17 is not enough.

The wasm import completed and saved, although full auto-analysis hit the
1800-second timeout. That was still enough to decompile the small
`CurlingMotion` kernel functions. The reusable scripts are:

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

Important limitation: Ghidra's wasm table/symbol handling is not fully reliable
for this Unity build. The small kernels decompile correctly, but the
`Newfrictionstep` address/name mapping can collide with adjacent IL2CPP
wrappers. For `Newfrictionstep`, use the WAT body `$f59956` as the authoritative
source. The Ghidra pass is still useful for the `fdx/fwx/fdy/fwy/fda/fwa`
formulas because those are compact and decompile cleanly.

With `MyParams(vx, vy, w, r1, r2)`, the first recovered kernels match the
expected running-band geometry. For example, WAT inspection gives:

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

The wet-friction kernels multiply similar directional terms by squared local
contact speed, which is consistent with the recovered `FAI = 2` exponent.

## What `Newfrictionstep` Does

The high-level structure recovered from `$f59956`:

1. If angular speed is near zero, it clamps the angular speed input to `0.01`.
2. It computes `|v|` from the input `b2Vec2`.
3. If `|v| <= 0.01`, it returns zero velocity and zero angle.
4. Otherwise it builds `MyParams(vx, vy, w, r1, r2)` with `r1 = r2 = 0.125`.
5. It repeatedly calls `fsimp(0, PI/2, 1e-5, param, type, i)` to integrate
   the force/torque kernels.
6. It has separate branches for positive and negative angular speed.
7. It updates velocity approximately as:

```text
vx += steptime * 10 * ax
vy += steptime * 10 * ay
angle += steptime * 20 * angular_acc / 0.399475
```

Other hard constants seen in the body:

- `mass` is effectively handled as `19` in the acceleration division.
- `R = 0.125`
- `K = 0.2`
- `PI = 3.1416`
- integration upper bound `PI / 2 = 1.5708`
- integration epsilon `1e-5`

More detailed WAT inspection shows that `Newfrictionstep` calls `fsimp` 40
times per step. The calls are grouped around three parameter copies and use
`type = 1/2/3` with different kernel indices:

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

The remaining constants in `Newfrictionstep` also reveal the band geometry:

- `0.122 = R - DR / 2`
- `0.128 = R + DR / 2`
- `0.0244 = K * (R - DR / 2)`
- `0.0256 = K * (R + DR / 2)`
- `0.025 = K * R`
- `6.2832 = 2 * PI`
- `12.5664 = 4 * PI`
- `1900 = 100 * 19`

So the model is not just a fitted empirical curve. It is a ring/band integral
friction model with explicit inner/outer running-band radii and wet-friction
terms.

## Recovered `fsimp` Semantics

WABT `wasm-decompile` can decompile the real wasm functions more readably than
Ghidra for the large methods:

```powershell
$wabt = "$env:TEMP\curling_wabt_tools\wabt-1.0.41\bin"
& "$wabt\wasm-decompile.exe" "$env:TEMP\curling_reverse_il2cpp\build.wasm" `
  -o "$env:TEMP\curling_reverse_il2cpp\build.dcmp"

D:\anaconda3\python.exe tools\reverse\extract_decompiled_wasm_func.py `
  "$env:TEMP\curling_reverse_il2cpp\build.dcmp" `
  "$env:TEMP\curling_reverse_il2cpp\dcmp_funcs" `
  func59955 func59956
```

The decompiled names map as:

- `func59955 = fsimp`
- `func59956 = Newfrictionstep`
- `f_avh = sin`
- `f_zuh = cos`
- `f_rwac = atan`
- `f_wxec = pow`

`fsimp(a, b, eps, param, type, i)` first computes a trapezoidal estimate, then
keeps halving the interval and applies:

```text
T_new = (T_old + step * midpoint_sum) / 2
S_new = (4 * T_new - T_old) / 3
stop when abs(S_new - S_prev) < eps
```

With:

```text
vx = param.a
vy = param.b
w  = param.c
r1 = param.d
r2 = param.e
s  = sin(x)
c  = cos(x)
```

the dispatch table is:

| type | i | integrand shape |
| ---: | ---: | --- |
| 1 | 1 | `sin(atan((vx + s*w*r2) / (vy + c*w*r2))) + sin(atan((vx + s*w*r2) / (vy - c*w*r2)))` |
| 1 | 2 | `sin(atan((s*w*r1 - vx) / (vy + c*w*r1))) + sin(atan((s*w*r1 - vx) / (vy - c*w*r1)))` |
| 1 | 3 | `((vx + s*w*r1)^2 + (vy + c*w*r1)^2) * sin(atan((vx + s*w*r1) / (vy + c*w*r1)))` |
| 1 | 4 | `((vx + s*w*r1)^2 + (vy - c*w*r1)^2) * sin(atan((vx + s*w*r1) / (vy - c*w*r1)))` |
| 1 | 5 | `((s*w*r2 - vx)^2 + (vy + c*w*r2)^2) * sin(atan((s*w*r2 - vx) / (vy + c*w*r2)))` |
| 1 | 6 | `((s*w*r2 - vx)^2 + (vy - c*w*r2)^2) * sin(atan((s*w*r2 - vx) / (vy - c*w*r2)))` |
| 1 | 7 | `sin(atan((vx + s*w*r2) / (vy - c*w*r2)))` |
| 2 | 1..7 | Same cases as `type=1`, but the outer `sin(atan(...))` becomes `cos(atan(...))`. For cases 3..6 the local speed-squared multiplier remains. |
| 3 | 1 | `sin(x + PI/2 - atan((vx + s*w*r2) / (vy + c*w*r2)))` |
| 3 | 2 | `sin(x + PI/2 + atan((vx + s*w*r2) / (vy - c*w*r2)))` |
| 3 | 3 | `sin(PI/2 - x + atan((s*w*r1 - vx) / (vy + c*w*r1)))` |
| 3 | 4 | `sin(PI/2 - x - atan((s*w*r1 - vx) / (vy - c*w*r1)))` |
| 3 | 5 | `((vx + s*w*r1)^2 + (vy + c*w*r1)^2) * sin(x + PI/2 - atan((vx + s*w*r1) / (vy + c*w*r1)))` |
| 3 | 6 | `((vx + s*w*r1)^2 + (vy - c*w*r1)^2) * sin(x + PI/2 + atan((vx + s*w*r1) / (vy - c*w*r1)))` |
| 3 | 7 | `((s*w*r2 - vx)^2 + (vy + c*w*r2)^2) * sin(PI/2 - x + atan((s*w*r2 - vx) / (vy + c*w*r2)))` |
| 3 | 8 | `((s*w*r2 - vx)^2 + (vy - c*w*r2)^2) * sin(PI/2 - x - atan((s*w*r2 - vx) / (vy - c*w*r2)))` |

This removes most of the previous uncertainty around `fsimp`. What still needs
careful validation is not the dispatch shape, but the sign conventions after
translation into local code.

## Recovered `Newfrictionstep` Assembly

The decompiled `func59956` shows three speed bands:

```text
speed = sqrt(vx^2 + vy^2)
if speed <= 0.01: return (0, 0, 0)
if abs(angle) <= 1e-6: angle_input = 0.01

vx_abs = abs(vx)
vy_abs = abs(vy)
w_abs = abs(angle_input)
```

The return update is:

```text
out.vx    = vx + steptime * 10 * ax
out.vy    = vy + steptime * 10 * ay
out.angle = angle_input + steptime * 20 * torque / 0.399475
```

Let:

```text
I(type, i; r1, r2) = fsimp(0, PI/2, 1e-5, MyParams(vx_abs, vy_abs, w_abs, r1, r2), type, i)
F2 = friction * 100 / (2 * PI)
F4 = friction * 100 / (4 * PI)
T2 = friction * 1900 / (2 * PI)
T4 = friction * 1900 / (4 * PI)
```

### Speed `>= 1.5`

Uses `r1 = r2 = R`.

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

### Speed `1.0..1.5`

Uses `r1 = R - DR/2 = 0.122`, `r2 = R + DR/2 = 0.128`.

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

### Speed `< 1.0`

Uses `r1 = r2 = R`.

```text
ay = K / 19 * I(2,3) + F2 * (I(2,2) + I(2,7))

if angle_input > 0:
  ax     = F2 * (I(1,2) - I(1,7)) - K / 19 * I(1,3)
  torque = T2 * R * (I(3,2) - I(3,3) + I(3,4)) - K*R * I(3,5)
else:
  ax     = K / 19 * I(1,3) + F2 * (I(1,7) - I(1,2))
  torque = K*R * I(3,5) + T2 * R * (I(3,3) - I(3,2) - I(3,4))
```

This means the single-stone no-collision model is now mostly recoverable from
the binary. The remaining work is implementation and validation against Unity
trace samples.

The first standalone Python translation is:

- `tools/reverse/recovered_curling_motion.py`

It intentionally lives under `tools/reverse/` until it is validated against
Unity traces and the Unity-axis sign convention is locked down.

## Recovered Runtime Physics Loop

`DCP_HumanVSAI.FixedUpdate` maps to wasm `func60124`. Its important physics
path is:

1. Check that the game is active, a shot is in progress, `movingCurling` exists,
   and the stone has not reported a collision.
2. Read the current `Rigidbody` velocity/angular velocity.
3. Convert the Unity axes into the `b2Vec2` used by `Newfrictionstep`.
4. Call:

```text
Newfrictionstep(friction, vec, angle, 0.001)
```

5. Convert the returned `speed` back into Unity `Rigidbody.velocity` and
   `Rigidbody.angularVelocity`.

The recovered friction argument is:

```text
noise = Random.Range(-0.0002, 0.0002)

if Sweep.isSweeping:
    friction = 0.0006 + noise
else:
    friction = 0.0010 + noise
```

This is an important correction to the earlier model. `SWEEP_EFFECT = 0.4`
appears as:

```text
0.0010 * (1 - 0.4) = 0.0006
```

So sweep does not add a post-shot displacement. It lowers the friction used by
each 0.001-second `Newfrictionstep` while the sweep animation/state is active.

The random term also means endpoint matching should be evaluated statistically
or with the Unity random state controlled. A deterministic local simulator can
use the mean friction first, but high-fidelity replay needs the per-step random
perturbation:

```text
no sweep: friction in [0.0008, 0.0012]
sweep:    friction in [0.0004, 0.0008]
```

The Unity RNG call sites are now globally resolved:

```text
DCP_HumanVSAI.FixedUpdate -> Random.Range(-0.0002, 0.0002)
FastDCP.FixedUpdate       -> Random.Range(-0.0002, 0.0002)
AutoDCP.FixedUpdate       -> Random.Range(-0.0002, 0.0002)
DCP.FixedUpdate           -> Random.Range(-0.0002, 0.0002)
MotionTest.FixedUpdate    -> Random.Range(-0.0002, 0.0002)  // test scene
```

The only discovered `UnityEngine.Random.InitState(seed)` call is in
`AutoDCP.HandleMessage`, and it is tied to recorded-game replay:

```text
AutoDCP.recordedGame == false:
    INIParser.WriteValue(..., "RANDSEED", UnityEngine.Random.seed)

AutoDCP.recordedGame == true:
    seed = Convert.ToInt32(recordLoader.ReadValue(..., "RANDSEED", "0"))
    UnityEngine.Random.InitState(seed)
```

No shared `Random.InitState` call was found in the `DCP_HumanVSAI`, `DCP`, or
`FastDCP` match-start/FixedUpdate paths. Ordinary match endpoint replay should
therefore be treated as stochastic; AutoDCP recorded replay can reproduce the
Unity RNG sequence when the record contains `RANDSEED`.

## Recovered Unity/Protocol Coordinate Formulas

These formulas are recovered from Unity code, not fitted from samples.

`DCP_HumanVSAI.SendMotionInfo` maps to wasm `func60096`. It sends the moving
stone state using:

```text
protocol_x  = teePosition.z - unity_position.z + 2.375
protocol_y  = teePosition.x - unity_position.x + 4.88
protocol_vx = -unity_velocity.z
protocol_vy = -unity_velocity.x
protocol_w  = unity_angularVelocity.y
```

`DCP_HumanVSAI.GetCurrentTrace` maps to wasm `func60072`. It stores the same
coordinate system without the protocol offset:

```text
trace_x = teePosition.z - unity_position.z
trace_y = teePosition.x - unity_position.x
```

For body arrays, the order depends on `firstShot`:

```text
firstShot == 0:
  body[4*i + 0], body[4*i + 1] = blue stone i trace_x, trace_y
  body[4*i + 2], body[4*i + 3] = red  stone i trace_x, trace_y

firstShot != 0:
  body[4*i + 0], body[4*i + 1] = red  stone i trace_x, trace_y
  body[4*i + 2], body[4*i + 3] = blue stone i trace_x, trace_y
```

`DCP_HumanVSAI.HandleHumanShot` maps to wasm `func60092`. The release-time
Unity setup is:

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

The signs line up with `SendMotionInfo`: positive Unity `velocity.x` becomes
negative protocol `motion_vy`, and positive Unity `angularVelocity.y` becomes
positive protocol `motion_w`.

## Recovered MOTIONINFO Tail Mapping

The official protocol's `MOTIONINFO` message is now usable as a validation
anchor for the recovered physics kernel. `MOTIONINFO` provides the moving stone
state when it reaches the middle line:

```text
motion_x, motion_y, motion_vx, motion_vy, motion_w
```

Using the standalone recovered model in
`tools/reverse/recovered_curling_motion.py`, the best tail replay convention is:

```text
x += motion_vx * 0.01
y += motion_vy * 0.01
speed = Newfrictionstep(0.001, (motion_vx, motion_vy), motion_w, 0.001)
```

In other words, the public protocol coordinates can be integrated directly for
tail replay:

```text
sx = +1, sy = +1, sw = +1
position dt = 0.01 seconds
friction-kernel dt = 0.001 seconds
```

The validation probe is:

```text
tools/reverse/probe_unity_tail_mapping.py
```

Empirical no-sweep results with mean dry friction and no Unity RNG replay:

```text
first 3 rows, dt=0.010: RMSE 0.0488 m, MAE 0.0450 m, max 0.0638 m
first 3 rows, dt=0.009: RMSE 1.4597 m
first 3 rows, dt=0.011: RMSE 1.5485 m
first 10 rows, dt=0.010: RMSE 0.0468 m, MAE 0.0419 m, max 0.0833 m
```

This strongly indicates that the recovered `Newfrictionstep` formulas and the
protocol tail coordinate convention are correct for no-collision, no-sweep
rollouts after the middle-line `MOTIONINFO` event. The remaining centimeter-
scale residual is consistent with the recovered per-step friction noise and
possible Unity/JSON rounding.

## Recovered Sweep Flow

The user-facing sweep request path is:

```text
HumanInputController.OnSweepButtonClicked -> DCP_HumanVSAI.HandleHumanSweep
```

`HumanInputController.OnSweepButtonClicked`:

- only works when `isHumanTurn` is true;
- reads `sweepDistanceInput`;
- defaults to `1.0` if the input is empty or unparsable;
- invokes `OnSweepRequested(distance)`.

`DCP_HumanVSAI.HandleHumanSweep(distance)`:

- requires `movingCurling != null`;
- requires `movingCurling.GetComponent<CurlingStoneNew>().allowSweep == true`;
- logs the requested distance;
- sets the scene `Sweep` component:

```text
Sweep.isSweeping = true
Sweep.sweepDistance = distance
```

`Sweep` maps to wasm `func60750..func60753`. Its fields are:

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

`Sweep.Sweeper` uses `Time.fixedDeltaTime` and moves the visual sweeper around
the target stone while `isSweeping` is true. The recovered oscillation is:

```text
direction = isMovingFor ? +2 : -2
sumnewZ += Time.fixedDeltaTime * sweepSpeed * movementDist * direction

if sumnewZ > movementDist:
    isMovingFor = false
elif sumnewZ < -movementDist:
    isMovingFor = true

sweeper.position = target.position + offset + (0, 0, sumnewZ)
```

The stopping logic is also in `Sweep.Sweeper`. With
`tools/reverse/resolve_metadata_refs.py`, the metadata slots now resolve to named
scene objects, so the window is no longer anonymous:

```text
target.position.x < Hogline2.position.x
target.position.x < Midline.position.x + sweepDistance
```

If either check fails, Unity clears:

```text
Sweep.isSweeping = false
Sweep.sweepDistance = 0
```

This means `sweepDistance` gates how long the scene `Sweep.isSweeping` flag
stays true; it is not used as a continuous multiplier on friction.

`Sweep.FixedUpdate` selects the target controller by scene name:

```text
FastGame  -> GameObject.Find("FastDCP").GetComponent<FastDCP>().movingCurling
AutoGame  -> GameObject.Find("AutoDCP").GetComponent<AutoDCP>().movingCurling
HumanVsAI -> GameObject.Find("DCP_HumanVSAI").GetComponent<DCP_HumanVSAI>().movingCurling
default   -> GameObject.Find("DCP").GetComponent<DCP>().movingCurling
```

The corresponding byte offsets are:

```text
FastDCP.movingCurling       // 0xD4 = 212
AutoDCP.movingCurling       // 0xF0 = 240
DCP_HumanVSAI.movingCurling // 0x104 = 260
DCP.movingCurling           // 0xE8 = 232
```

So the sweeper target is the currently moving stone.

`Sweep.FixedUpdate` also toggles the sweeper renderer by comparing the moving
stone and `Hogline2` in Unity `position.x`:

```text
sweeperRenderer.enabled = movingCurling.position.x < Hogline2.position.x
```

The practical result for the local simulator is:

- requested sweep controls how long the lower-friction mode remains active;
- the friction magnitude during active sweep is fixed around `0.0006`, not
  proportional to the requested distance;
- sweep eligibility is gated by `CurlingStoneNew.allowSweep`, which is toggled
  by trigger zones.

## Recovered Shot Input Mapping

`DCP_HumanVSAI.HandleHumanShot` maps to wasm `func60092`. The input clamps are:

```text
velocity:          [0.0001, 6.0]
horizontal offset: [-2.23, 2.23]
rotation:          [-15.7, 15.7]
```

It selects the current stone from the blue/red stone list using roughly:

```text
stone_index = floor(current_shot_index * 0.5)
```

Then it:

- positions the selected stone at the release location with the requested
  horizontal offset;
- sets `Rigidbody.velocity` from the requested `velocity`;
- sets `Rigidbody.angularVelocity` from the requested `rotation`;
- marks `movingCurling` and shot-in-progress state.

The exact Unity internal `Vector3` axis convention is still being verified, but
the public protocol tail convention is now locked down for `MOTIONINFO` replay:
`motion_x/y/vx/vy/w` can be used directly with position `dt = 0.01` and
`Newfrictionstep(..., steptime = 0.001)`.

### Empirical BESTSHOT To MOTIONINFO Probe

The release-to-middle-line mapping is not fully reverse-engineered yet, but the
existing calibration data already makes it highly predictable. The helper:

```text
tools/reverse/probe_action_to_motioninfo.py
```

fits a small quadratic least-squares model from:

```text
BESTSHOT(v0, h0, w0) -> MOTIONINFO(x, y, vx, vy, w)
```

On `data/calibration/no_sweep_200.jsonl`, using 190 in-play no-sweep rows:

```text
motion_x:  RMSE 0.000107
motion_y:  RMSE 0.005249
motion_vx: RMSE 0.000045
motion_vy: RMSE 0.001221
motion_w:  RMSE 0.000428
final_x:   RMSE 0.024141
final_y:   RMSE 0.032637
```

The useful coarse relationships are:

```text
motion_x ~= h0 + 2.346 plus spin curl before the middle line
motion_vy / v0 ~= -0.629
motion_w / w0 ~= 0.337
motion_vx / w0 ~= 0.010
```

This section should be treated as validation/fallback only. The authoritative
release mapping is the Unity formula in `HandleHumanShot`; data fitting is not
the primary source of truth and should not be the main simulator design.

## Recovered Collision/Trigger Behavior

`CurlingStoneNew` fields are:

```csharp
public bool mCollision;      // 0x10
public bool allowSweep;      // 0x11
private Rigidbody rb;        // 0x14
private Vector3 origin_postion; // 0x18
public AudioSource source;   // 0x24
```

`CurlingStoneNew.OnCollisionEnter` maps to wasm `func61030`. It checks the
collided object's tag/name against two strings, which now resolve to `Stone` and
`Wall`.

For `Stone` collisions it:

```text
mCollision = true
Rigidbody.drag = 0.6
Rigidbody.angularDrag = 0.6
```

For `Wall` collisions it also:

```text
Rigidbody.velocity = Vector3.zero
Rigidbody.angularVelocity = Vector3.zero
stone.GameObject.SetActive(false)
```

This means multi-stone and wall behavior is not purely from `Newfrictionstep`;
Unity collision callbacks change the `Rigidbody` state and stop the custom
single-stone stepping path once `mCollision` is set.

`CurlingStoneNew.OnTriggerEnter` maps to `func61031`. It toggles
`allowSweep`, and also calls controller methods associated with hogline,
centerline, and other rule triggers.

The two confirmed triggers are:

```text
Midline  -> allowSweep = true, then dispatches motion-info handling by scene
Hogline2 -> allowSweep = false
```

`OnTriggerEnter` also dispatches by scene name:

```text
FastGame  -> FastDCP.SendMotionInfo()
AutoGame  -> AutoDCP.recordedGame ? AutoDCP.ReadMotionInfoFromRecord() : AutoDCP.SendMotionInfo()
HumanVsAI -> DCP_HumanVSAI.SendMotionInfo()
default   -> DCP.SendMotionInfo()
```

The separate `CrossLineEvent.OnTriggerEnter` class is also resolved. It only
switches cameras:

```text
if collider.gameObject.name == "Hogline1":
    GameObject.Find("CameraControl").GetComponent<CameraControl>().SendMessage("SwitchCamera", 3)

if collider.gameObject.name == "Hogline2":
    GameObject.Find("CameraControl").GetComponent<CameraControl>().SendMessage("SwitchCamera", 4)
```

So `CrossLineEvent` is not the physics or rule-penalty core.

There is also a `MotionTestStone` test class with two collision helper formulas:

```text
Lambda1(m1, m2, u, e, v, theta)
  = m1*m2*u*(e + 1)*v*cos(theta) / (m1 + m2)

Lambda2(m1, m2, u, e, v, theta)
  = sin(theta)*v / (3/m1 + 3/m2)
```

Its constructor defaults are:

```text
u = 0.1
e = 1.0
m = 19.1
R = 0.145
```

However, the recovered `MotionTestStone.OnCollisionEnter` does not call these
formulas, and the competition stone class used by `DCP_HumanVSAI` is
`CurlingStoneNew`. So these helpers are useful evidence about the developer's
collision experiments, but they are not currently proven to be the competition
multi-stone collision path.

## Recovered Rule Thresholds

`DCP_HumanVSAI.GetStoneState` maps to wasm `func60070`. It uses fixed rule
thresholds:

```text
side bounds:       -2.23 < x < 2.23
valid y range:     -4.735 < y < 39.475
near hog/guard y:  -2.015, 0.145, 5.645
house radius:      sqrt(x*x + y*y) < 2.015
center line touch: abs(x) <= 0.145
```

`DCP_HumanVSAI.IsTouchingCenterLine` maps to wasm `func60071` and is exactly:

```text
abs(x) <= 0.145
```

`DCP_HumanVSAI.IsAllCurlingStoped` maps to wasm `func60089`. It iterates both
stone lists and returns false if any active stone has:

```text
velocity.x^2 + velocity.y^2 + velocity.z^2 > 0.000001
```

So Unity's stop check is a squared-speed threshold of `1e-6`, not the
`0.01` linear speed cutoff used inside `Newfrictionstep`.

`DCP_HumanVSAI.UpdateState` / `DCP.UpdateState` also contain R7/centerline rule
correction logic. Confirmed fields:

```text
GameStateEx.ShotNum     // 0x08
GameStateEx.WhiteToMove // 0x18
GameStateEx.body        // 0x1C
GameStateEx.Player      // 0x20
```

The readable conditions are:

```text
enter this check only after ShotNum >= 2;
scan existing stones by ShotNum % 2 parity;
candidate stone position must satisfy:
    0.145 < y < 5.645
   -2.23 < x < 2.23
    sqrt(x*x + y*y) >= 2.015
centerline touch is:
    abs(x) <= 0.145
```

When the related violation is detected:

```text
DCP/DCP_HumanVSAI call SetStonesByBody(...) to roll back/reset body state;
non-human-choice paths send "CENTERLINE_VIOLATION" to the relevant Client;
HumanVsAI calls HumanInputController.ShowCenterlineViolationPanel(...)
when the human is the violated player, allowing keep/reset.
```

This does not affect single-stone rollouts, but matters for full match-state
replay and the rule layer of a training environment.

## What We Still Do Not Know

The reverse pass has reduced the unknowns, but several items are still not
fully recovered.

### 1. Exact Clean Algebra For Every Kernel

The `fsimp` dispatch table and `Newfrictionstep` assembly are now recovered at
formula level and translated into a standalone Python prototype. What is still
missing is a faster audited production translation, likely C++/NumPy/Numba, for
training-speed rollout.

This matters because one sign error in the running-band terms can look small
on low-spin shots but become large on curls and sweep-heavy shots.

### 2. Remaining Rule Trigger And Controller Method Semantics

The important Unity/protocol axis mapping is now recovered from
`HandleHumanShot`, `SendMotionInfo`, and `GetCurrentTrace`:

```text
protocol_x  = teePosition.z - unity_position.z + 2.375
protocol_y  = teePosition.x - unity_position.x + 4.88
protocol_vx = -unity_velocity.z
protocol_vy = -unity_velocity.x
protocol_w  = unity_angularVelocity.y
```

The metadata-use-to-string resolver is now in place. The key names `FastGame`,
`AutoGame`, `HumanVsAI`, `DCP`, `FastDCP`, `AutoDCP`, `DCP_HumanVSAI`,
`Midline`, `Hogline2`, `Stone`, and `Wall` can now be resolved directly from
the wasm `d_[index]` slots.

`FastDCP + 212`, `AutoDCP + 240`, `DCP_HumanVSAI + 260`, and `DCP + 232` are
now confirmed to be each controller's `movingCurling` field. What remains is
whether rule triggers beyond `Midline` and `Hogline2` are handled in other
functions, plus the full call chain for more controller-side rule methods.

### 3. Randomness Control

`FixedUpdate` adds `Random.Range(-0.0002, 0.0002)` to friction every
`0.001`-second step. `AutoDCP.HandleMessage` can record/restore Unity RNG
through `RANDSEED`, but no shared `Random.InitState` call was found in
`DCP_HumanVSAI`, `DCP`, or `FastDCP`. The remaining unknown is not whether a
seed call exists in those paths, but:

```text
1. whether ordinary match-mode Unity initial RNG state can be fixed externally;
2. whether the local simulator should replicate UnityEngine.Random exactly;
3. whether training should use mean friction, sampled friction, or an empirical noise model.
```

### 4. Multi-Stone Collision Details

The stone objects are not pure custom physics. `CurlingStoneNew` has:

```csharp
public bool mCollision;
public bool allowSweep;
private Rigidbody rb;
private void OnCollisionEnter(Collision collision);
private void OnTriggerEnter(Collider collider);
```

`CurlingStoneNew.OnCollisionEnter` now has named `Stone` and `Wall` branches.
There is also another collision helper class with `Lambda1`, `Lambda2`, `m1`,
`m2`, `u`, `e`, `m`, and `R`. That means stone-stone interactions may mix Unity
PhysX collision solving with custom callback logic.

We have enough to build a good no-collision rollout simulator. We do not yet
have enough to guarantee exact multi-stone post-collision velocity/angular
velocity transfer, because the detailed PhysX contact solver behavior, contact
geometry, and restitution/friction combine behavior still need collision traces
or deeper Unity/PhysX validation.

### 5. Server Action To Physics Input Mapping

The public action is roughly `(velocity, horizontal offset, rotation, sweep)`.
The physics core takes:

```csharp
Newfrictionstep(double friction, b2Vec2 vec, double angle, double steptime)
```

The input clamps and Unity release setup are now recovered from
`HandleHumanShot`:

```text
velocity -> Rigidbody.velocity.x
position -> subtract from selected stone transform.position.z
rotation -> Rigidbody.angularVelocity.y
```

What remains is not the formula itself, but confirming every external protocol
entry point routes through this exact path in all game modes.

### 6. Stop/Out-Of-Play/Rule Thresholds

We have method names such as `GetStoneState`, `IsAllCurlingStoped`,
`GetCurrentTrace`, `UpdateState`, and scoring functions, but not all readable
logic. For training, this matters less than motion/collision at first, but it
matters for exact game-state replay and final scoring edge cases.

## Practical Unknowns By Priority

For training, the unknowns are not equal:

1. Highest priority: translate `Newfrictionstep + fsimp` exactly enough for
   single-stone no-collision rollouts, using the recovered formulas above.
2. Highest priority: implement sweep as duration-gated low-friction stepping
   with per-step random friction.
3. High priority: recover controller method semantics and remaining rule
   triggers such as stop, out-of-play zones, and scoring edges.
4. High priority: recover RNG seeding or model endpoint noise statistically.
5. Medium priority: validate or approximate Unity PhysX stone-stone collision.
6. Medium priority: prove whether any custom collision helper is active in the
   competition scene, or only test code.
7. Lower priority: exact UI, networking, scoring display, upload, and human
   input details.

## Practical Conclusion

The Unity simulator is not an unknowable black box. The important motion model
is recoverable enough to guide a local simulator:

- We can match the exact constants used by Unity.
- We can reproduce the same `Newfrictionstep` structure.
- We can already replay no-sweep protocol tails from `MOTIONINFO` to endpoint
  within about 5 cm RMSE using mean dry friction.
- The remaining hard part is translating the 23 kernel functions and Simpson
  integrator into faster production code, then validating release-time action
  mapping, sweep duration, randomness, and collisions against Unity traces.

Recommended next step:

1. Keep `tools/reverse/recovered_curling_motion.py` as the reference model and
   port it to a faster implementation for training.
2. Implement the recovered `HandleHumanShot` and coordinate-transform formulas
   directly, rather than fitting release behavior from data.
3. Resolve the remaining controller method semantics and rule triggers.
4. Add collision validation samples before trusting the simulator for tactical
   self-play.

## Current Reverse-Engineering Boundary

The stable toolchain is:

1. Use Il2CppDumper on `build.wasm` and `global-metadata.dat`.
2. Use `script.json` to map IL2CPP methods to dynCall method pointer IDs.
3. Resolve dynCall IDs through the wasm indirect function table.
4. Inspect the resulting WAT functions.
5. Use `tools/reverse/resolve_metadata_refs.py` to map WABT-decompiled
   `f_xkb(address)` and `d_[index]` references back to strings, types, and
   generic methods.
6. Use `tools/reverse/resolve_wasm_calls.py` to map WABT-decompiled call aliases
   such as `f_kwjc` back to IL2CPP method names such as
   `DCP_HumanVSAI.SendMotionInfo`.

The metadata slot relation in this build is:

```text
address = 3705984 + 4 * d_index
```

Example:

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

Cpp2IL can parse this project as WebAssembly and finds the same code/metadata
registration addresses, but its IL recovery currently aborts on imported WebGL
functions such as `env.SetIMEText` having no associated function body. That
means we can reliably recover names, constants, structs, function mapping, and
WAT-level behavior, but not clean C# pseudocode for the whole physics class
without manual decompilation or a heavier Ghidra workflow.

`fsimp` is especially hard to cleanly decompile because it inlines many of the
force kernels behind nested `br_table` switches. It is still recognizable as
the Simpson integrator used by `Newfrictionstep`, and `Newfrictionstep` calls it
with:

```text
fsimp(0, PI / 2, 1e-5, param, type, i)
```

## Simulator Corrections From This Pass

This pass found and fixed one concrete calibration bug:

- `sweep_200.jsonl` stores sweep as `requested_sweep_distance`.
- `tools/calibration/fit_unity_samples.py` only read `requested_sweep`.
- Before the fix, all official sweep samples were normalized as `sweep = 0`.

The fast simulator was also tightened so `unity_landing_v2` calibration checks
the calibrated sweep range. Without this, a calibration fitted on one sweep
range could be silently used outside support.

The new fitted file is:

- `config/unity_physics_calibration.json`

It is now the first calibration file loaded by `fast_curling_env.py`.

## Data Consistency Check

After refitting `config/unity_physics_calibration.json` on:

- `data/calibration/no_sweep_200.jsonl`
- `data/calibration/sweep_200.jsonl`

the deterministic landing replay against 390 usable samples gives:

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

The 90th percentile total error is about `0.0946 m`, but there is one high
sweep outlier around `1.55 m`. This suggests:

- no-sweep and moderate sweep are consistent with the corrected simulator;
- high sweep is not well represented by a simple endpoint polynomial;
- the reverse-engineered model supports why: sweep changes effective friction,
  so treating sweep as a linear post-shot distance is structurally wrong.
