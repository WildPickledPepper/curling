# 单壶运动模型

记录 `Newfrictionstep`、`fsimp`、速度分段和 Unity 运行时物理循环。

> 原长文档已封存：[`UNITY_REVERSE_ENGINEERING.zh.2026-07-07.archive.md`](../archive/UNITY_REVERSE_ENGINEERING.zh.2026-07-07.archive.md)。以后维护以本目录子文档为准。

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

继续看 `func59955` 的循环尾部可以确认：wasm 里没有看到固定迭代次数上限。
循环每轮会：

```text
p = S_prev
l = T_old
midpoint_sum = sum(integrand(a + step*(k + 0.5)))
T_new = (l + step*midpoint_sum) * 0.5
S_new = (4*T_new - l) / 3
step *= 0.5
intervals <<= 1
continue while abs(S_new - p) >= eps
```

`tools/reverse/recovered_curling_motion.py` 中的 `FSIMP_SAFETY_MAX_ITERATIONS = 24`
只是本地防止异常参数挂死的保护，不是 Unity 代码里的物理常量。当前测试用一组代表参数
检查 22 个 integrand 都能在该保护上限前收敛。

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

因此唯一支持的 integrand 是 `type=1` 的 7 个、`type=2` 的 7 个、`type=3`
的 8 个，一共 22 个。`func59955` 里能看到第二套相似的 `br_table` label，
那是自适应 Simpson 循环中对同一批 integrand 的 midpoint 累加展开，不是额外的第 23
个 kernel。

这基本消除了 `fsimp` 的不确定性。还需要严谨验证的是翻译到本地代码后的符号约定和 rollout 端采样误差，而不是 dispatch 结构本身。

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
6. 随后的 Unity 物理步用刚写入的 Rigidbody velocity 推进位置。

这意味着本地 replay 的单 tick 顺序应是：

```text
speed = Newfrictionstep(friction, (vx, vy), w, 0.001)
vx, vy, w = speed
x += vx * 0.01
y += vy * 0.01
```

早期 probe 曾用“先用旧速度推进位置，再更新摩擦速度”的顺序；按 `FixedUpdate`
反编译修正后，第一条 no-sweep 尾段平均摩擦误差从约 `5.19cm` 降到约 `3.53cm`。

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

这个分支里的 `recordedGame` 字段已经和 AutoDCP dump 的 `0x54` 偏移对上，即 wasm
中的 `a[84]:ubyte`。`RANDSEED` 写入/读取发生在刚体释放之后，但早于下一次
`FixedUpdate` 摩擦噪声消耗，因此从 AutoDCP `BESTSHOT` 整段 replay 时不需要
额外 `rng-skip`。

没有在 `DCP_HumanVSAI`、`DCP`、`FastDCP` 的 match start/FixedUpdate 路径中发现统一
`Random.InitState`。因此普通比赛 endpoint replay 应按随机过程处理；AutoDCP 录像回放
如果有 `RANDSEED` 字段，则可以复现 Unity RNG 序列。
