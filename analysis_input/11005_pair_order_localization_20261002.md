# 2026-10-02：11005 壶间碰撞分歧定位到刚体排序与参考面选择

后续已完成[生产生命周期修复及验收](11005_lifecycle_fix_20261002.md)：下文保留修复前定位记录；当前 12 枪角色顺序与 11005 首碰几何已闭合，剩余差异进入求解约束。

## 定位结论

首次壶间碰撞（物理步 1022、角速度写入 ordinal 1023）已经追到 `createShapeInteraction` 的动态刚体排序入口。两侧传入此函数的角色顺序都为活动壶、目标壶；**输入的 RigidID 大小关系相反**，使同一个排序规则产生相反的 solver-facing 接触对。

| 实际字段/调用 | Unity | 本地 CP39 native |
| --- | --- | --- |
| 活动壶 RigidID | 16 | 3 |
| 目标壶 RigidID | 1 | 9 |
| 排序函数 | Wasm `f71700` | module RVA `0x236ed0` |
| 比较 | `16 >= 1`，保持 | RVA `0x236f65` 比较 `3 >= 9`，交换 |
| 构造函数收到的角色 | 活动壶、目标壶 | 目标壶、活动壶 |
| 首次 PCM 的角色 | 活动壶、目标壶 | 目标壶、活动壶 |

Unity 同一次捕获在 ordinal 0/2 的壶—冰创建调用与 ordinal 1023 的壶间创建调用中，分别验证了目标/活动 ShapeSim 身份。`ShapeSim +4 -> ActorSim`，排序实际读取 `ActorSim +48`。本地实际读取 `ShapeSim +8 -> ActorSim +0x58`，同时采集 bodyCore 姿态，以首次 PCM 的位置逐位核对角色。

Unity 的排序输出进入 `f71680` 构造函数；本地经过 `0x23dc00`，进入 `0x27c630`。两侧构造函数实参都验证了上述排序结果。输入编号属于真实生命周期产生的状态，不能硬写成 16/1 或交换高层 addActor 顺序来代替该调用链。

## 接触法线为何在后续出现不同

两侧真实 GJK 都返回状态 `4`，均进入完整接触面生成。它们选中的两个物理面一致：目标壶面索引 37，活动壶面索引 17；但最终参考面相反。

| 实际裁剪实参 | Unity `f70076` | 本地 `0x3cab40` |
| --- | --- | --- |
| 参考面 | 目标壶面 37 | 活动壶面 17 |
| 另一面 | 活动壶面 17 | 目标壶面 37 |

用本次捕获的输入与实际 witness 查询返回值，按反编译 `f70077` 的原始 float32 运算顺序重放参考面比较。两个得分都为 **`0.9997755289077759`**，`f32.ge` 返回真，选择第二颗壶的面。重放中，两次 witness 查询的法线/最近点输入均与实际运行记录逐位相同，随后裁剪函数的两个面指针及角色顺序也完全对应实际记录。

本地实际汇编在 `0x3c861e` 执行 `comiss`，随后 `setae`；真实裁剪调用的返回地址为 `0x3c868f`，证明它走了该 `>=` 分支，也选第二颗壶的面。本地比较的两个得分尚未直接采样，不能把 Unity 的相等得分写成本地运行事实。

因此，已闭合的链条是：**排序入口的 RigidID 大小关系不同 → 接触对顺序相反 → 实际参考面角色不同 → PCM 接触法线不同 → 不同法线进入求解约束。** 两侧选中的面法线/plane 原始值相同，只是参考/另一面的角色交换；完整数值见验收 JSON。

## 修复涉及的代码与范围

本地 `local_simulator/unity_physx.py` 默认 `emulate_unity_setactive_no_sim=False`。初始化预先把所有壶加入 Scene；`deactivate()` 默认关闭 shape 的 simulation 标志并休眠，保留 actor simulation 的注册历史。`activate_stationary()` / `start_motioninfo()` 仅在上述选项开启时才恢复 actor 的 `DISABLE_SIMULATION` 状态。

此次真实排序采样已经证明，当前路径生成的 RigidID 角色关系与 Unity 不同。生产修复应从这些 actor 启停/注册生命周期函数着手，自然形成相同的排序关系，再验收实际 PCM 入口和参考面；此次定位没有修改正式物理实现。

目标壶更早的 quaternion/速度历史、solver lock flags 仍有已记录差异。它们是独立的待对齐输入；本次不能宣称启停生命周期已经完全还原，或仅修正排序就会完成整段轨迹对齐。

## 验收与证据

- [collision_pair_sort_verified_20261002.json](collision_pair_sort_verified_20261002.json)：排序、GJK、参考面实参、调用地址和证据哈希。
- [verify_collision_pair_sort_20261002.py](verify_collision_pair_sort_20261002.py)：完整验收脚本。
- [reference_face_compare_replay_20261002.json](reference_face_compare_replay_20261002.json)、[原运算重放脚本](replay_reference_face_compare_20261002.py)。
- [Unity 创建链/PCM 原始事件](unity_11005_pair_registration_20261002/logs/unity_runtime_probe_20261002_111917/events.jsonl)。
- [本地实际物理步的可靠函数调用记录](native_stone_pair_sort_interceptor_20261002/calls.json)。
- [Unity 排序反编译](pcm_functions_20261001/f71700.wat)、[Unity 参考面计算](pcm_functions_20261001/f70077.wat)、[本地参考面计算汇编](native_full_manifold_20261002.asm)。

三次 Unity 插桩捕获均与原捕获的 15,580 个摩擦值、1,023 组 setter 前后物理字段、40 帧求解入口/出口及 12 个样本终点一致。本地 isolated PCM 查询与实际物理步的接触几何相同；三份可靠 Interceptor 报告的正式轨迹结果行和聚合值均未改变。Stalker 发现记录仅用于函数地址发现，其不可靠嵌套关系未用于结论。

Unity Wasm SHA-256：`cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81`。

本地 native SHA-256：`2564abec4fa3f358e67259b105c4b88d49eae28510611c8a0e2f11b7671888df`。

```powershell
& 'D:\anaconda3\python.exe' analysis_input/replay_reference_face_compare_20261002.py
& 'D:\anaconda3\python.exe' analysis_input/verify_collision_pair_sort_20261002.py
```
