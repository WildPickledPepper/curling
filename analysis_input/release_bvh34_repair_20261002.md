# 第 526 帧 BVH34 查询修复（2026-10-02）

当前进度以 [目标自然激活修复](target_natural_wake_repair_20261002.md) 为准：第 1561 帧目标提前唤醒已消除，样本 11000 双方完成状态连续通过第 2000 帧，覆盖最终休眠。下文的 BVH34 采样及验证脚本绑定的是当时生产版本。

生产默认 `ice_use_fast_midphase=True`，恢复 Unity 实际使用的 BVH34 网格查询。原注释称标量内核不能执行 BV4，但当前 CP39 二进制的反汇编和运行时调用都确认实现已经存在：`PCMContactConvexMesh 0x2e2880 → intersectOBB_BV4 0x347650 → BV4_OverlapBoxCB 0x3f69b0`。这次只修默认路径，未修改物理内核、角速度或接触法向量。

## 直接证据与修复

第 526 帧入口 P/Q/v/w 与 Unity 相同，实际角速度 setter 输出也相同。进一步读取该帧的惯量矩阵、PCM 中间接触和求解输入，发现最早的已观察差异在接触生成：BVH33 与 BVH34 的三角形处理顺序不同，接触归约后保存的法向量组合不同。

Unity `f69979` 和本地 `0x29d550` 的实际输入中，六个接触点坐标及距离相同，但旧本地有三个点使用 B 法向量，Unity 只有一个。实际 `f69979` 对六个法向量求和、旋转并归一化。因此旧本地最终 X/Z 法向量为 `a5800000/b0d2d7c0`，Unity 为 `a5d55556/b0d2d7eb`；该差异进入约束及求解。

恢复 BVH34 后，六个中间接触的 72 个浮点字、六个最终接触的 42 个浮点字全部相同。第 526 帧角速度 X 恢复为 Unity 的 `0x9a381bc6`，前 525 帧状态保持不变。默认冰面恢复出的 200 个三角形、200 项 face-remap、100 个 BVH34 节点原始字节也逐一与 Unity 资产核对相同。

## 当前连续链条

`Reset 42 步及自然休眠 → BESTSHOT 释放 → 滑行 → 第 1561 帧输出（首次冰壶接触之前）`

本次修复的历史验证从头连续比较主冰壶每帧 13 个 Pxyz/Qxyzw/线速度xyz/角速度xyz 原始字，至第 1561 帧共 **20,293 个字完全相同**。该 getter 采样本身未覆盖第 1562 帧输出，不能扩展为所有冰壶状态或每条内部运算已闭合。

后续已用实际写回及下一 FixedUpdate 入口补齐边界，见 [首次接触与普通尾段探查](release_ordinary_tail_20261002.md) 和 [新机器结果](release_ordinary_tail_verified_20261002.json)：主冰壶状态连续相同至第 3362 帧；首次冰壶接触是第 1562 帧。但新增目标冰壶观测发现第 1561 帧本地提前 `wake_up()`，因此双冰壶完整链条尚未闭合。

早期末帧补采目录 `unity_release_1562_1564_chain_capture_20261002`、`unity_release_1562_1564_writeback_capture_20261002` **无效，未用于结论**。后续 `unity_release_tail_fixed_boundaries_20261002` 已通过原始基线数量、完整 setter 序列及输出不变校验。

第 526 帧原函数体插桩、第 1022–1025 窗口插桩分别与原始基线核对：256 个 Reset core 帧、1562 个摩擦输入、1563 对密集 setter 前后数据、终点输出不变。原函数体保留；本地 Frida 观测无丢弃、无未完成调用，逐帧输出与不插桩运行相同。

32 项 unittest 通过，新增原始 Unity 第 526 帧回归及实际 BVH34 拓扑/节点检查。结果仅确认该样本及 CP39；不同 ABI 与其他样本应独立验证。

## 复查入口

- [机器验证结果](release_bvh34_repair_verified_20261002.json) 和 [验证脚本](verify_release_bvh34_repair_20261002.py)。运行 `python analysis_input/verify_release_bvh34_repair_20261002.py`。
- [完整默认场景运行](native_first_release_bvh34_full_20261002.json)。从 Reset 正常释放，不注入位姿、旋转或求解结果。
- [Unity 第 526 帧内部采样](unity_release_526_chain_capture_20261002/) 与 [修复后本地调用](native_release_526_bvh34_verified_20261002/calls.json)。
- [Unity 第 1022–1025 帧及完整 getter 序列](unity_release_1022_1025_chain_capture_20261002/)（该窗口不是样本 11000 的首次碰撞）。
- [独立 Unity 第 526 帧测试输入/输出](../local_simulator/tests/fixtures/unity_release_tick526_20261002.json)。

原始 Wasm SHA256：`cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81`。当前 CP39 内核 SHA256：`7c31ced1773023e552391645e42040c9f3694d513805bc8b95ef0f8bc737bd38`。代码、采样和报告哈希见机器验证结果。
