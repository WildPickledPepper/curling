# 当前状态、未知项与训练策略

这页是训练决策入口。旧的长版未知项文档和模拟器策略文档已归档：

```text
docs/archive/unity_reverse_superseded_20260709/07_unknowns_training_toolchain.zh.md
docs/archive/unity_reverse_superseded_20260709/10_simulator_alignment_strategy.zh.md
```

## 一句话结论

第一阶段可以训练 `SWEEP=0` 的单壶无碰撞策略；碰撞模块还不能并入大规模训练，因为本地 pyphysx 还没有证明和 Unity 首次碰撞帧 native state 字段级一致。

## 已经稳定的部分

```text
单壶运动:
  - `Newfrictionstep` 和 `fsimp` 主公式已恢复。
  - fixed timestep = 0.01s。
  - 普通 socket 样本没有 RANDSEED，单次 bit-level 对齐不现实。

协议和坐标:
  - `BESTSHOT(v,h,w)` 到协议坐标的主映射已恢复。
  - `MOTIONINFO` 是 Midline trigger 离散帧，不是数学线穿越。
  - `SWEEP` 受 Midline/Hogline2 和 socket 到达帧影响。

规则:
  - 每壶结束状态、`POSITION`、`SCORE`、`GAMESTATE`、AutoDCP 记录格式已恢复。
```

## 训练优先级

1. 先冻结扫冰：

```text
BESTSHOT(v, h, w)
SWEEP = 0
```

2. 单壶无碰撞先过验收：

```text
无 RANDSEED 时看分布和 grouped-CV。
普通样本 endpoint 2cm 左右已经接近 Unity 随机摩擦下限。
不要要求每一发都 bit-level 小于 2cm。
```

3. 碰撞暂不进入训练主循环：

```text
current pyphysx:
  active RMSE ~= 3.86cm
  target in-play RMSE ~= 11.32cm

per-sample oracle:
  active RMSE ~= 1.35cm
  target in-play RMSE ~= 1.48cm

oracle 泛化失败:
  leave-one-out best target RMSE ~= 30.98cm
  0 / 7 双终点进 2cm
```

这说明当前 2cm 是“每条样本知道隐藏修正”的诊断结果，不是训练用通用碰撞公式。

## 现在还缺什么

最重要的未知不是高层 PhysX 机制，而是首次碰撞帧的运行时字段：

```text
active / target:
  pose, rotation, linearVelocity, angularVelocity
  mass, COM, inertia tensor
  constraints, sleep state, solver iteration counts

shape:
  local pose, scale, contactOffset, restOffset
  cooked convex mesh pointer / byte stream
  material pointer and combine mode

contact:
  PCM ContactBuffer
  contact normal / points / separation
  friction anchors/cache
  SolverContact rows and applied impulses
```

没有这些字段，终点误差会把 contact、tail friction、RNG 和 endpoint 残差混在一起。

## 不要再优先做的事

```text
1. 不要继续扫单个全局 friction/restitution/radius。
2. 不要把 per-sample oracle 当训练环境。
3. 不要再做没有 runtime native state 的大规模 endpoint 拟合。
4. 不要把扫冰混进当前碰撞对齐问题。
```

这些方向已经被现有报告弱化。继续做只会堆更多相互矛盾的候选参数。

## 接下来最短路径

```text
1. 做 trace-driven collision replay：
   Unity runtime dump -> 本地 pyphysx/C++ scene。

2. 验收顺序：
   first contact fields -> 0.02s 碰后速度 -> endpoint。

3. 如果 trace-driven replay 对齐：
   再把 dump 字段逐步替换成公式。

4. 如果 trace-driven replay 不对齐：
   继续查 ContactBuffer / solver row / friction cache / cooked stream。
```

## 当前可用文件

```text
单壶:
  tools/reverse/recovered_curling_motion.py
  tools/reverse/replay_bestshot_seeded.py
  tools/reverse/fit_nosweep_residual_correction.py
  config/unity_nosweep_residual_correction.controlled.json

碰撞:
  tools/reverse/probe_physx_collision_alignment.py
  tools/reverse/summarize_physx_native_state_equivalence.py
  tools/reverse/analyze_collision_oracle_generalization.py
  data/calibration/unity_physx_native_state_equivalence_audit_20260709.json
```

## 训练准入线

```text
单壶 no-sweep:
  可以先用于训练。
  验收看 2cm 左右分布误差和交叉验证。

扫冰:
  暂缓。
  等 no-sweep 稳定后单独做。

碰撞:
  暂缓进入训练。
  至少要让 trace-driven replay 的 0.02s 碰后速度对齐，再谈 endpoint 2cm。
```
