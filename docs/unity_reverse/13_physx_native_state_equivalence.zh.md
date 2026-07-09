# PhysX Native State 等价性审计

旧长版已归档：

```text
docs/archive/unity_reverse_superseded_20260709/13_physx_native_state_equivalence.zh.md
```

这页回答一个问题：

```text
Unity 在 stone-stone 碰撞那一帧喂给 PhysX 的完整 native state，
是否已经和本地 pyphysx 构造的 state 一模一样？
```

## 结论

没有证明，而且现有证据反证“已经一模一样”。

高层机制已经很清楚：PCM、patch friction、solver、材质、fixed timestep、Rigidbody 标量、convex cooking 大路径都已恢复。但字段级等价要求更高，需要 `PxRigidDynamic`、`PxShape`、`PxConvexMesh`、`PxTriangleMesh`、contact cache、`ContactBuffer` 和 solver rows 的运行时字段逐项一致。我们还没有抓到这些完整字段。

## 当前误差

```text
unique-role current best:
  active RMSE ~= 3.86cm
  target in-play RMSE ~= 11.32cm

per-sample entrance-state oracle:
  active RMSE ~= 1.35cm
  target in-play RMSE ~= 1.48cm
  7 / 7 in-play pair 双终点进 2cm

visible-feature correction leave-one-out:
  active RMSE ~= 5.22cm
  target in-play RMSE ~= 30.98cm
  0 / 7 双终点进 2cm
```

解释：如果每条样本都单独改 hidden entrance/native-state proxy，可以把现有样本压到 2cm；但用可见特征无法泛化这些修正，所以它不是训练用通用公式。

## 为什么不是继续调参数

已弱化的方向：

```text
friction / restitution / combine mode
fixed timestep
contactOffset / restOffset / frictionOffsetThreshold
solver iterations / scene flags
lock-upright constraints
formal mesh 输入点云
离线 cooked hull topology / BigConvexData
统一 handoff-x/y 偏移
统一 handoff_w_offset
宽范围 yaw / integrated active yaw
target/active support pre-settle
```

这些方向有些会改善单样本，但不能作为一套全局参数把 active 和 target 都压进 2cm。

## 最强证据

1. 尾段滑行不是主因：从本地 `0.02s/0.20s` snapshot 只调 target 水平 `vx/vy`，endpoint 可到毫米级。
2. 缺口在首次碰撞输出：需要约 `0.49 Ns` row 级修正，约本地主冲量 `2.35%`。
3. `12003` 本地 contact report 冲量角度约 `-87.19deg`，Unity-implied 约 `-82.21deg`，差 `+4.98deg`，接近 64 边 hull 一个侧面步长。
4. `12005` 用 `handoff_w_offset=-0.44rad/s` 可闭合，但全局 w offset 失败，说明它是 contact-instance tangent/angular 代理。
5. visible-feature leave-one-out correction 失败，说明 oracle 不是简单经验公式。

## 怎么改成一样

短期要做 trace-driven replay：

```text
1. 从 Unity runtime dump 首次碰撞帧 native state。
2. 本地 pyphysx/C++ 直接用 dump 字段构造 scene。
3. 先比较 0.02s 碰后 linear/angular velocity。
4. 再比较最终 endpoint。
```

只有 trace-driven replay 对齐后，才能继续把 dump 字段替换成公式。

当前已经补上第一步的 WebGL runtime hook，入口在：

```text
tools/reverse/unity_webgl_runtime_probe.js
```

浏览器里调用：

```javascript
__curlingProbe.installPhysXNativeHooks({
  maxDumpsPerHook: 16,
  armMs: 2000,
  includeRawBytes: true,
  argWindowBytes: 8192
})
```

它不是 endpoint 采样工具，而是 native state 抓取工具。默认策略是：

```text
1. 先 hook stone-stone PCM: PxcPCMContactConvexConvex。
2. 一旦这个函数触发，自动 armed 约 2 秒。
3. 在 armed 窗口内 dump contact finalization / solver-row writer 的参数指针窗口。
4. 导出 physx.native.before / physx.native.after 事件。
```

当前 hook 的关键 table 入口：

```text
120118 func70576 PxcPCMContactConvexConvex
120587 func71272 PxsDynamics.createFinalizeContacts
120379 func70963 createFinalizeSolverContacts4
120487 func71103 createFinalizeSolverContacts
```

这些事件先解决“Unity 到底给 PhysX 喂了什么”和“solver row 实际写出了什么”。
如果抓到的 ContactBuffer / solver rows 和本地 pyphysx 输入一致但输出仍不一致，才继续查
PhysX 库版本 / batch path / compiler fast-math 差异；如果输入已经不一致，就回到 shape pose、
contact cache、friction patch 或 handoff state。

## 最少要抓的字段

```text
active / target:
  global pose
  rotation / yaw
  linearVelocity / angularVelocity
  mass / COM / inertia tensor
  constraints / sleep state / solver iteration counts

PxShape:
  local pose
  geometry scale
  contactOffset / restOffset
  material pointer / filter data
  convex mesh pointer

stone cooked stream:
  vertices / polygons / indices
  bounds
  mass / inertia / COM
  GAUS / VALE / SUPM byte order

rink:
  triangle mesh vertices / indices
  local pose / scale
  material

contact:
  persistent contact cache
  friction patches / anchors
  ContactBuffer normal / points / separation
  solver rows
  normal and friction applied impulses
```

## 机器报告

主报告：

```text
data/calibration/unity_physx_native_state_equivalence_audit_20260709.json
```

生成：

```powershell
D:\esp\tmp\curling_pyphysx_conda\python.exe tools\reverse\summarize_physx_native_state_equivalence.py
```

当前机器结论：

```text
strong_identity_proven = false
```
