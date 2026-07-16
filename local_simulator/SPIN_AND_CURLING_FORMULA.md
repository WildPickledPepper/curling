# 本地模拟器的旋球公式与代码

本文只说明当前交付的**非扫冰严格 PhysX 模拟器**怎样处理旋转（curl）。它回答四个问题：旋转输入是什么、为什么壶会横向弯、每个物理 tick 如何更新、碰撞后由谁继续计算。

> 一句话结论：本地模拟器不是用“画一条圆弧”模拟旋球。它在每个 `0.01 s` 的 Unity 固定 tick 内，按反推得到的 `CurlingMotion.Newfrictionstep` 计算壶底摩擦造成的横向加速度和扭矩，再把新速度写入 PhysX；第一次碰撞之后由 PhysX 刚体求解器处理碰撞后的运动。

## 1. 输入、输出与适用范围

一次出手是三个数：

```text
(v0, h0, w0)
```

- `v0`：出手速度；
- `h0`：横向瞄准偏移；
- `w0`：初始自转角速度。正负决定左右旋向，绝对值决定旋转强度。

旋球公式在“出手壶尚未第一次接触其他壶”的滑行段运行。它每 tick 输入当前 `(vx, vy, w)` 和该 tick 的摩擦 `μ`，输出下一 tick 的 `(vx', vy', w')`。

它**不**根据壶的初始朝向 `yaw` 人为改变弯曲方向；`yaw` 是刚体姿态，尤其会影响碰撞时的 PhysX 几何状态。滑行弯曲由自转 `w` 和冰面摩擦模型产生。

## 2. 每个 tick 的总更新式

Unity 固定物理步长是 `Δt = 0.01 s`。恢复出来的函数使用内部参数 `step = 0.001`，等价更新为：

```text
vx' = vx + 0.01 × ax
vy' = vy + 0.01 × ay
w'  = w  + 0.02 × torque / I

I = 0.399475
```

`ax` 是横向/纵向坐标系中的第一个加速度分量，`ay` 是另一个加速度分量，`torque` 是冰面对壶施加的扭矩。它们都不是固定常数，会随当前速度、自转、摩擦随机量和速度段变化。

## 3. 横向弯曲从哪里来

模型把壶底的接触面按角度 `θ` 积分。对接触面半径为 `r` 的一点，先构造局部相对滑动速度：

```text
u = |vx|, v = |vy|, ω = |w|
A 的两种形式：u + ω × r × sin(θ)，或 ω × r × sin(θ) - u
B 的两种形式：v + ω × r × cos(θ)，或 v - ω × r × cos(θ)
φ = atan(A / B)
```

代码会对正、负号对应的接触侧分别计算，并在 `θ ∈ [0, π/2]` 上以自适应 Simpson 积分求和。由于旋转让壶底两侧的相对滑动速度不对称，两侧摩擦相减后会留下横向分量 `ax`；这就是壶会弯的原因。摩擦同时产生扭矩，因此 `w` 也会逐步衰减或变化。

这不是简单的 `横向加速度 = c × w`：速度越低、旋转越高或摩擦不同，积分结果都会不同。

## 4. 三个速度段

函数按当前平面速度 `s = sqrt(vx² + vy²)` 切换公式：

| 速度段 | 接触半径/参数 | 含义 |
|---|---|---|
| `s ≥ 1.5` | `r1 = r2 = R = 0.125` | 高速滑行公式。 |
| `1.0 ≤ s < 1.5` | `r1 = R1`、`r2 = R2`，并加入 `WET_K` 项 | 中速过渡公式，左右有效接触半径不同。 |
| `0.01 < s < 1.0` | `r1 = r2 = R`，但使用低速积分组合 | 慢速阶段的公式。 |
| `s ≤ 0.01` | 速度与自转都置零 | 认为该壶已停止。 |

正旋、反旋使用镜像的 `ax` 和 `torque` 符号组合。因此同样的出手速度，改变 `w0` 的符号会让横向偏移镜像翻转。

## 5. 摩擦随机量

非扫冰时每个 tick 使用：

```text
μ = float32(0.001 + ε)
ε ∈ [-0.0002, +0.0002]
```

这里的 `ε` 来自 Unity 风格 RNG 序列。也就是说，即使 `(v0, h0, w0)` 完全一样，不同摩擦序列仍会产生一组落点，而不是唯一落点。严格回放可注入记录到的逐 tick 摩擦序列；训练/分布测试则应按相同分布重新采样。

## 6. 旋球公式和 PhysX 的交接

```text
出手 (v0, h0, w0)
        ↓
每 0.01 s：CurlingMotion 更新 vx / vy / w
        ↓
把更新后的线速度和角速度写入同一个 PhysX 壶
        ↓
PhysX 推进一步，检查是否首碰撞
        ↓
首碰撞前：继续 CurlingMotion
首碰撞后：停止主动旋球更新，PhysX 负责所有壶的碰撞、摩擦、旋转和静止
```

所以“旋球公式准确”只表示自由滑行的受控段准确；撞壶后的分裂、二次碰撞和最终停位，还取决于 PhysX 的碰撞形状、接触对、摩擦和 solver。

## 7. 实际运行的核心公式代码

当前交付运行的是编译版 `curling_new_friction_step`；它和下面这份 Python 反推实现使用相同的 `newfrictionstep` 数学。以下是实际入口函数，未做简化或改参数：

```python
def newfrictionstep(friction: float, vec: B2Vec2, angle: float, steptime: float) -> Speed:
    angle_input = ANGLE_FALLBACK if abs(angle) <= ANGLE_EPS else angle
    speed = math.sqrt(vec.x * vec.x + vec.y * vec.y)
    if speed <= 0.01:
        return Speed(B2Vec2(0.0, 0.0), 0.0)

    vx, vy, w = abs(vec.x), abs(vec.y), abs(angle_input)
    positive_spin = angle_input > 0.0
    f2 = friction * 100.0 / (2.0 * PI)
    f4 = friction * 100.0 / (4.0 * PI)
    t2 = friction * 1900.0 / (2.0 * PI)
    t4 = friction * 1900.0 / (4.0 * PI)

    if speed >= 1.5:
        p = MyParams(vx, vy, w, R, R)
        i11, i15, i16 = _i(p, 1, 1), _i(p, 1, 5), _i(p, 1, 6)
        i21, i25, i26 = _i(p, 2, 1), _i(p, 2, 5), _i(p, 2, 6)
        i31, i32, i37, i38 = _i(p, 3, 1), _i(p, 3, 2), _i(p, 3, 7), _i(p, 3, 8)
        ax_base = (i15 + i16) * K / MASS
        ay = f2 * i21 + (i25 + i26) * K / MASS
        if positive_spin:
            ax = ax_base - f2 * i11
            torque = t2 * R * (i32 - i31) + K * R * (i38 - i37)
        else:
            ax = f2 * i11 - ax_base
            torque = t2 * R * (i31 - i32) + K * R * (i37 - i38)

    elif speed >= 1.0:
        p = MyParams(vx, vy, w, R1, R2)
        values = {
            **{(1, i): _i(p, 1, i) for i in range(1, 7)},
            **{(2, i): _i(p, 2, i) for i in range(1, 7)},
            **{(3, i): _i(p, 3, i) for i in range(1, 9)},
        }
        ax_wet_low = (values[1, 3] + values[1, 4]) * WET_K / MASS
        ax_wet_high = (values[1, 5] + values[1, 6]) * WET_K / MASS
        ay = (f4 * values[2, 1] + f4 * values[2, 2]
              + (values[2, 3] + values[2, 4]) * WET_K / MASS
              + (values[2, 5] + values[2, 6]) * WET_K / MASS)
        if positive_spin:
            ax = f4 * values[1, 2] - f4 * values[1, 1] + ax_wet_high - ax_wet_low
            torque = (t4 * R2 * (values[3, 2] - values[3, 1])
                      + t4 * R1 * (values[3, 4] - values[3, 3])
                      + (values[3, 6] - values[3, 5]) * K * R1
                      + (values[3, 8] - values[3, 7]) * K * R2)
        else:
            ax = f4 * values[1, 1] - f4 * values[1, 2] + ax_wet_low - ax_wet_high
            torque = (t4 * R2 * (values[3, 1] - values[3, 2])
                      + t4 * R1 * (values[3, 3] - values[3, 4])
                      + (values[3, 5] - values[3, 6]) * K * R1
                      + (values[3, 7] - values[3, 8]) * K * R2)

    else:
        p = MyParams(vx, vy, w, R, R)
        i12, i13, i17 = _i(p, 1, 2), _i(p, 1, 3), _i(p, 1, 7)
        i22, i23, i27 = _i(p, 2, 2), _i(p, 2, 3), _i(p, 2, 7)
        i32, i33, i34, i35 = _i(p, 3, 2), _i(p, 3, 3), _i(p, 3, 4), _i(p, 3, 5)
        ay = i23 * K / MASS + f2 * (i22 + i27)
        if positive_spin:
            ax = f2 * (i12 - i17) - i13 * K / MASS
            torque = t2 * R * (i32 - i33 + i34) - K * R * i35
        else:
            ax = i13 * K / MASS + f2 * (i17 - i12)
            torque = K * R * i35 + t2 * R * (i33 - i32 - i34)

    return Speed(
        B2Vec2(vec.x + steptime * 10.0 * ax, vec.y + steptime * 10.0 * ay),
        angle_input + steptime * 20.0 * torque / INERTIA,
    )
```

上面 `_i`、`integrand`、`_local` 和自适应 Simpson 积分函数同样是公式的一部分；不要自行用常数替代。完整、可运行且作为唯一事实来源的实现是：

- [完整 Python 公式](runtime_support/tools/reverse/recovered_curling_motion.py)
- 编译版 C++ 公式源位于开发环境 `D:\esp\tmp\curling_pyphysx_hybrid\src\pyphysx.cpp`；交付包不依赖这个外部路径。
- [严格模拟器中的逐 tick 调用](unity_physx.py)

## 8. 最小可运行样例

下面样例不启动 PhysX，只计算一个 tick 的旋球速度更新，适合检查正/反旋或摩擦变化的直接影响。

```python
from local_simulator.runtime_support.tools.reverse.recovered_curling_motion import (
    B2Vec2, STEP, newfrictionstep, unity_friction,
)

# 非扫冰、不给随机扰动：mu = 0.001
mu = unity_friction(sweeping=False, noise=0.0)

# 同一速度下，比较正旋和反旋。
for w in (5.0, -5.0):
    after = newfrictionstep(mu, B2Vec2(x=0.10, y=3.20), w, STEP)
    print(f"w={w:+.1f} -> vx={after.v.x:.12f}, vy={after.v.y:.12f}, w_next={after.angle:.12f}")
```

从 `DCCourse` 根目录运行：

```powershell
& 'D:\esp\tmp\curling_pyphysx_conda\python.exe' local_simulator\examples\inspect_spin_step.py
```

## 9. 常见误解

1. **`w0` 不是初始 yaw。** `w0` 是“每秒转多快”；yaw 是壶此刻朝向。
2. **旋球公式不取代 PhysX。** 它负责首碰撞前的逐 tick 运动控制；碰撞与碰后滑行仍由 PhysX 负责。
3. **同一出手不必然同一落点。** 每 tick 的摩擦随机量不同，最终位置是分布。
4. **本文不等于扫冰模型。** 扫冰摩擦常量在源码中存在，但扫冰协议尚未纳入当前交付的严格训练范围。
