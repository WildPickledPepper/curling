# Unity 逆向工程笔记

这是维护入口。原来的超长单文件已经原样封存，后续请优先维护 `docs/unity_reverse/` 下的子文档。

> 封存原文：[`archive/UNITY_REVERSE_ENGINEERING.zh.2026-07-07.archive.md`](archive/UNITY_REVERSE_ENGINEERING.zh.2026-07-07.archive.md)

## 子文档

1. [`unity_reverse/00_overview_assets.zh.md`](unity_reverse/00_overview_assets.zh.md)：包结构、Unity 对象参数、全局常量、数据结构、核心函数索引、Ghidra 过程。
2. [`unity_reverse/01_single_stone_motion.zh.md`](unity_reverse/01_single_stone_motion.zh.md)：`Newfrictionstep`、`fsimp`、速度分段、运行时物理循环。
3. [`unity_reverse/02_protocol_sweep_input.zh.md`](unity_reverse/02_protocol_sweep_input.zh.md)：Unity/协议坐标、MOTIONINFO、扫冰、BESTSHOT/SWEEP/POSITION 输入。
4. [`unity_reverse/03_rules_state_records.zh.md`](unity_reverse/03_rules_state_records.zh.md)：规则阈值、每壶结束状态机、SendGameState、AutoDCP 记录/回放。
5. [`unity_reverse/04_collision_entry.zh.md`](unity_reverse/04_collision_entry.zh.md)：碰撞/触发路径、PhysX 任务图、contact/finalization 表、narrowphase 表。
6. [`unity_reverse/05_physx_contact_generation.zh.md`](unity_reverse/05_physx_contact_generation.zh.md)：PhysX convex-convex / convex-mesh 接触点生成、cache、reduction、ContactBuffer。
7. [`unity_reverse/06_physx_solver.zh.md`](unity_reverse/06_physx_solver.zh.md)：PhysX contact finalization、Px1DConstraint 排查、single-pair 和 4-wide solver。
8. [`unity_reverse/07_unknowns_training_toolchain.zh.md`](unity_reverse/07_unknowns_training_toolchain.zh.md)：剩余未知、训练优先级、实用结论、当前逆向边界、模拟器修正、数据一致性检查。
9. [`unity_reverse/08_resampling_plan.zh.md`](unity_reverse/08_resampling_plan.zh.md)：重采样计划、`.save` record 归档、socket JSONL 采样流程。
10. [`unity_reverse/09_record_file_storage.zh.md`](unity_reverse/09_record_file_storage.zh.md)：`.save`、`RANDSEED`、`TRACE`、`AutoGame/rank.csv` 的逻辑路径与 WebGL IndexedDB 落盘位置。
11. [`unity_reverse/10_simulator_alignment_strategy.zh.md`](unity_reverse/10_simulator_alignment_strategy.zh.md)：本地模拟器对齐、误差分层、训练准入线。
11. [`unity_reverse/04_collision_physx.zh.md`](unity_reverse/04_collision_physx.zh.md)：碰撞/PhysX 兼容导航页。

## 维护约定

- 以后新增逆向结论先写入对应子文档。
- 这个入口文件只维护目录和阅读路径。
- 封存原文只作为历史快照，不再继续维护。
- 如果某个子文档继续变长，再按同样方式拆分，并在这里更新目录。

## 建议阅读路径

训练模拟器优先读：`01_single_stone_motion` -> `02_protocol_sweep_input` -> `03_rules_state_records` -> `07_unknowns_training_toolchain`。

碰撞保真优先读：`00_overview_assets` -> `04_collision_entry` -> `05_physx_contact_generation` -> `06_physx_solver` -> `07_unknowns_training_toolchain`。
