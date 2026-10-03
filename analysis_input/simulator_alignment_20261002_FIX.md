# 2026-10-02：修复 11005 第 488 次 native setter 分叉

## 结果与验收条件

在与原始捕获相同的初始原生 quaternion、摩擦流和已对齐的发射/竖直写入条件下，11005 的全部 1,023 次原始位置、四元数和 native 角速度 setter 输出均逐位一致。原第 488 次输出分叉已消除。

ordinal 486/487/488 的接触查询直接使用实际物理场景中的修复后形状，其点、法线、分离距离和 face ID 全部与 Unity 相同。没有再构造读取 Unity scale 的隔离查询形状。

12 次投掷实际形状中的 scale 均由当前本地姿态计算，并与捕获逐位一致。源代码不读取采样日志或按 sample ID 选择 scale。

现有密集捕获到 ordinal 1023 截止，不能据此声称下一处分叉在 1024，也不能据此声称碰后轨迹已完全一致。

## 正式实现

- `local_simulator/unity_physx.py` 在 `activate_stationary` / `start_motioninfo` 放置姿态后，沿已观察的 MeshCollider 创建路径计算 scale 并重建形状。未改变 actor 身份、材质、质量、惯量或速度。
- scale 相同时共享既有已恢复的凸包；不同时重新创建带 scale 的形状并应用同一 runtime hull / BigConvex 数据。复制形状局部姿态、偏移与 flags，最后替换 attachment。
- 原生 Y-up 模拟步现执行已观察的 `f72606` f32 平方模、平方根、倒数和逐分量乘法，写回真实 body quaternion。与 Transform 读取时归一化分开。
- 训练的前半段和结算路径在需要该写回时使用同一逐步入口；旧原生批量循环尚未包含该写回，不能让默认正确路径绕过它。原有速度数字不应作为当前默认结算路径的新基准。
- `emulate_unity_transform_scale_refresh` 与 `emulate_unity_body_pose_writeback` 默认启用；Legacy Z-up 不执行这两项 Y-up 语义。历史运行可显式关闭两项，新修复不依赖诊断包装层。

审计器的旧碰后/结算循环也已路由到当前正式模拟步；诊断包装层不会再次重复归一化。`c131_production_geometry_pose_fix_20261002.json` 是中间记录，最终应使用下方 `all_steps` 报告。

## 自动核验与证据

- 最终重放：`c131_production_geometry_pose_fix_all_steps_20261002.json`。
- 最终验收：`11005_geometry_fix_verified_20261002.json`，包括原始日志、模块和源文件哈希。
- 验收脚本：`verify_11005_geometry_fix_20261002.py`。
- Unity 原始对照：`unity_11005_step486_pcm_20261001/logs/unity_runtime_probe_20261001_215740/events.jsonl`。
- 缩放机制、原始函数与 1,242 字段复算证据：`simulator_alignment_20261001_NOTES.md`。
- 原始函数来源 SHA256：`cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81`。
- 实际 PhysX 形状回归：`../local_simulator/tests/test_unity_shape_refresh.py`。11 个捕获姿态下，实际 scale 与捕获一致，凸包 vertices/polygons/index buffer 未变，body 原始状态未变，每个 body 仍只附着一个形状。
- f72606 写回测试使用独立捕获的源/目标 quaternion。另有结算路径测试确保需要写回时不进入旧批量循环。

测试：完整本地模拟器测试集 22 项通过；随后新增的结算路径回归和两项形状/写回回归共 3 项通过（23 个不同测试均已通过）。

在项目根目录复现：

```powershell
& 'C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe' analysis_input/verify_11005_geometry_fix_20261002.py
& 'C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe' -m unittest discover -s local_simulator/tests -p 'test_*.py'
```

## 尚未闭合的范围

1. 11005 碰后终点仍有活动壶 `1.766 mm`、目标壶 `35.595 mm` 残差。此次修复的成功依据是输入、接触生成与 setter 输出的内部一致性，不能以终点残差变化解释全部碰撞机制。
2. 两处 Unity angular getter 与读取本地 raw angular 的微小差异仍留在验收 JSON 中（ordinal 466/482）；它们没有造成这批 native setter 输出分叉，但不应把“setter 与 P/Q 已匹配”写成全部 getter 字段匹配。
3. 只使用重置 yaw 时，原生 quaternion 从 ordinal 1 就与捕获不同。不同输入对照见 `c131_live_geometry_fix_from_reset_yaw_20261002.json`、`11005_geometry_fix_reset_yaw_control_20261002.json`。它没有使用新增的 A10 quaternion 覆盖，也没有注入 Unity scale 或碰后状态，但不能宣称逐位对齐。在线保留完整姿态历史仍是独立工作。
4. 后续检查已完成首次壶间 PCM 与求解入口/出口采样：第 1,022 次物理步、ordinal 1023 写入后，PCM 接触法线已不同。进一步追到真实刚体 RigidID 排序与参考面选择分歧，见 [排序定位证据](11005_pair_order_localization_20261002.md)。actor 启停生命周期和目标壶输入历史仍需对齐。
# 后续首碰生命周期修复

2026-10-02 后续结果见 [11005_lifecycle_fix_20261002.md](11005_lifecycle_fix_20261002.md)：保留下文原第 488 次写入修复记录，新的 RigidID 生命周期修复已使 12 枪实际首碰角色顺序一致，11005 两个接触几何逐位一致；剩余为同一首碰帧的求解约束与目标壶输入历史差异。
