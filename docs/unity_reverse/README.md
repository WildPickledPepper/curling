# Unity 逆向文档入口

这个目录只保留当前需要维护的短文档。旧长版已归档到：

```text
docs/archive/unity_reverse_superseded_20260709/
```

以后更新结论时，优先改这里的短版；原始 probe 细节放在 `data/calibration/*.json` 和
`tools/reverse/*.py` 里，不再把大段历史过程复制进多个文档。

## 当前读法

训练和决策先读：

```text
07_unknowns_training_toolchain.zh.md
13_physx_native_state_equivalence.zh.md
```

碰撞逆向先读：

```text
04_collision_physx.zh.md
12_physx_convex_cooking.zh.md
13_physx_native_state_equivalence.zh.md
```

单壶、协议、规则先读：

```text
01_single_stone_motion.zh.md
02_protocol_sweep_input.zh.md
03_rules_state_records.zh.md
```

## 活跃文档

1. [`00_overview_assets.zh.md`](00_overview_assets.zh.md)：Unity 包结构、资产参数、PhysicsManager、关键函数索引。
2. [`01_single_stone_motion.zh.md`](01_single_stone_motion.zh.md)：`Newfrictionstep`、`fsimp`、单壶无碰撞运动。
3. [`02_protocol_sweep_input.zh.md`](02_protocol_sweep_input.zh.md)：协议坐标、`BESTSHOT`、`MOTIONINFO`、`SWEEP`、`POSITION`。
4. [`03_rules_state_records.zh.md`](03_rules_state_records.zh.md)：规则、每壶结束状态、计分、AutoDCP 记录格式。
5. [`04_collision_physx.zh.md`](04_collision_physx.zh.md)：碰撞总览、证据链、下一步。
6. [`05_physx_contact_generation.zh.md`](05_physx_contact_generation.zh.md)：PhysX contact generation 源码级细节。
7. [`06_physx_solver.zh.md`](06_physx_solver.zh.md)：PhysX solver row、constraint、冲量公式细节。
8. [`07_unknowns_training_toolchain.zh.md`](07_unknowns_training_toolchain.zh.md)：当前结论、剩余未知、训练策略。
9. [`08_sampling_runtime_records.zh.md`](08_sampling_runtime_records.zh.md)：采样、`.save`、WebGL 存储、运行时 native-state probe。
10. [`12_physx_convex_cooking.zh.md`](12_physx_convex_cooking.zh.md)：石壶 convex cooking、cooked hull、质量属性。
11. [`13_physx_native_state_equivalence.zh.md`](13_physx_native_state_equivalence.zh.md)：Unity native state 与本地 pyphysx state 是否一致。

## 维护规则

- 短文档写结论、证据位置和下一步，不再贴完整历史日志。
- 详细数值以 `data/calibration/*.json` 为准；文档只写关键数字。
- 新 probe 先写工具和报告路径，再写一句结论。
- 如果一段话同时出现在两个文档里，只保留在最贴近主题的文档，其他地方改成链接。
- 训练决策只看 `07` 和 `13`，避免被旧实验过程带偏。

## 关键报告

```text
data/calibration/unity_physx_native_state_equivalence_audit_20260709.json
data/calibration/unity_collision_handoff_xy_oracle_20260709.json
data/calibration/unity_collision_oracle_generalization_20260709.json
data/calibration/unity_collision_angular_handoff_diagnostic_20260709.json
data/calibration/formal_stone_cooking_status_20260708.json
```

## 关键工具

```text
tools/reverse/probe_physx_collision_alignment.py
tools/reverse/summarize_physx_native_state_equivalence.py
tools/reverse/summarize_collision_handoff_xy_oracle.py
tools/reverse/analyze_collision_oracle_generalization.py
tools/reverse/summarize_collision_angular_handoff_diagnostic.py
tools/reverse/dump_pyphysx_cooked_convex_hull.py
tools/reverse/analyze_pyphysx_raw_hull_topology.py
tools/reverse/analyze_pyphysx_bigconvex_data.py
tools/reverse/analyze_pyphysx_scaled_mass_properties.py
```
