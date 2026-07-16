# 当前状态、未知项与训练策略

这页是训练决策入口。旧的长版未知项文档和模拟器策略文档已归档：

```text
docs/archive/unity_reverse_superseded_20260709/07_unknowns_training_toolchain.zh.md
docs/archive/unity_reverse_superseded_20260709/10_simulator_alignment_strategy.zh.md
```

## 一句话结论

第一阶段可以训练 `SWEEP=0` 的单壶无碰撞策略；`shot/MOTIONINFO -> first PCM shell`
已经在持久 pyphysx Scene 中达到毫米级。碰撞模块仍不能并入大规模训练，因为本地 Scene
进入 shell 后生成的 contact feature/cache 还没有和 Unity 字段级一致。

## 已经稳定的部分

```text
单壶运动:
  - `Newfrictionstep` 和 `fsimp` 主公式已恢复。
  - fixed timestep = 0.01s。
  - clean capture 的 Random.Range 主序列已确认每 tick 一次。
  - MOTIONINFO 到 first PCM 的离散自停位置 RMSE ~= 1.06mm，max ~= 1.73mm。
  - 持久 Scene 中 BESTSHOT 到 PCM shell 的 x/y RMSE ~= 1.16mm。
  - 持久 Scene 中 MOTIONINFO 到 PCM shell 的 x/y RMSE ~= 0.77mm。

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

最重要的剩余项不是高层 PhysX 机制或首次碰撞帧字段抓取，而是把已知字段由本地整局
状态自然生成出来：

```text
已经闭合:
  Newfrictionstep / Random.Range tick 主序列
  2R + 2*contactOffset 的 first-PCM 离散边界
  stable actor 内从 BESTSHOT/MOTIONINFO 推到 PCM shell 的 position/velocity/yaw 积分
  reset 保留完整 quaternion 的本地生命周期实现
  runtime hull / scene-style direct PCM / solver-row 公式
  Unity runtime first-PCM pose/contact/cache/row 的抓取链

待生成而不是待猜:
  上一发碰撞后写回的正确 quaternion/yaw；前半段会保留它，但碰撞尾段尚未对齐
  Unity 2-contact 与本地 4-contact 的最早 feature/cache 分叉
  local Scene 的 first-any / first-contact pair cache 与 Unity raw cache 等价性
  完整 Scene 的 0.02s writeback 和双壶 endpoint
```

`SetStonesByBody(func61068)` 和 `ResetStones(func61078)` 已证明位置 reset 不写 rotation，
所以 yaw 必须作为整局持久状态，而不能从每条 socket POSITION 样本重新设为零。

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
1. 一局只创建一个 pyphysx Scene，保留 16 个 stable actor/shape identity。
2. reset 只搬 x/y、停速度并保留 quaternion；已投 target 持续存在。
3. active 出手时启用同一 shape，每 tick 写 Newfrictionstep 速度后 simulate(0.01)。
4. 前三项已由 `unity_front_half_physx.py` 落地并通过 6 条 PCM-shell 状态验收。
5. 下一关只比较 local/Unity first-contact 的 feature/cache/contact fields，再验收
   0.02s writeback 和 endpoint；不要回头重拟合前半段位置。
```

## 当前可用文件

```text
单壶:
  tools/reverse/recovered_curling_motion.py
  tools/reverse/replay_bestshot_seeded.py
  tools/reverse/front_half_pcm_replay.py
  unity_front_half_sim.py
  unity_front_half_physx.py
  tools/reverse/audit_persistent_scene_front_half.py
  data/calibration/front_half_threshold_replay_audit_20260710.json
  data/calibration/persistent_scene_front_half_state_audit_20260710.json

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
