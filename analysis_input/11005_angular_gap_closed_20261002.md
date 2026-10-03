# 11005 角速度读取缺口修复（2026-10-02）

本轮修复的是此前第 466、482 次角速度读取差异，并补齐原始位模式检查发现的第 2 次线速度正负零差异。活动壶的已采样读取、P/Q 和角速度写入连续通过到第 1023 次。**这不等于整个场景已经对齐到第 1023 次**：目标壶在首个壶碰撞 PCM 入口的姿态仍有差异，尚未采到它最早出现的时刻。下一轮必须回溯目标壶的激活、Reset 后贴冰与休眠过程。

## 直接证据与修复依据

固定 Unity wasm SHA256：`cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81`。

角速度读取实际调用为 `f82502 → f73063 → table[121729] / f72661`。`f72661` 直接复制 Scb 的 `+296/+300/+304`，没有再次计算角速度。采样确认每次读取前后，核心值、缓冲值和 getter 输出的位模式一致，故差异已经在此前求解/积分阶段发生。

第 465 个物理步产生第 466 次 getter 输入。修复前，两侧 P/Q、线速度、角速度及求解器增量一致，但 `PxSolverBodyData.sqrtInvInertia` 的 9 个矩阵元素各差一个 ULP。Unity 活动壶的逆惯量 Y 为 `0x40a91cdc`（`5.284772872924805`），本地固定惯量的倒数为 `0x40a91cda`（`5.284771919250488`）。Unity 同一时刻目标壶也使用后者，因此不能把所有壶统一换成另一个常数。

实际重建链是 `f72951 → f73283 → f73060 → f72778 → f72776 → f72777`。Unity 在 attachShape 后按该形状的 float32 缩放重新计算质量属性。本地此前只重建了形状，遗漏质量同步。现恢复 `f72776` 的半迹、缩放及质量归一化表达式顺序，并在构造和形状重建时更新 Y 惯量。

约束同步 `f73070` 通过惯量冻结 X/Z；实测 Pxs 核心和求解器 `lockFlags` 都为 0。本地旧 X/Z 原生锁标志为 40，会擦掉实际角向求解增量，现改为 0，X/Z 惯量继续为 0。

原始位模式还发现释放速度 Z：Unity 为 `0x00000000`，本地为 `0x80000000`。BESTSHOT 路径（例如 `f60092/f60705`）显式将 native Y/Z 写为全零，再经 `f32521 → f82501 → f73034` 写入。现让 BESTSHOT 的协议到 native 坐标转换保留该正零；MOTIONINFO 的常规轴映射继续按其输入执行。

## 验证证据

- `unity_11005_mass_properties_v2_20261002/logs/unity_runtime_probe_20261002_133353/events.jsonl`：12 次释放中共 98 次质量重算。逐次验证实测缩放、质量、原始矩阵及最终惯量；98 次 `f69768` 的惯量旋转均为 identity。本次移植仅覆盖该正式壶模型、identity shape/scale rotation、显式零 COM 的实际路径。
- `extract_stone_mass_kernel_20261002.py`：抽出 `f72776` 的原始数值段和 `f72779/f69768/f72775`，保持运算指令、常数和顺序。`verify_stone_mass_properties_20261002.py` 对 98 次调用分别比较原始代码输出和生产移植输出，均逐位一致。内核与函数体哈希见 `unity_mass_numeric_kernel_20261002.json`。
- `native_getter_mass_fixed_465_20261002/calls.json`：原生模块 SHA256 `2564abec4fa3f358e67259b105c4b88d49eae28510611c8a0e2f11b7671888df`，RVA `0x2049c7` 的只读指令边界快照。修复后第 465 步完整数值输入及速度增量与 Unity 相同。112 字节 bodyData 仅 `+72` 的场景对象索引不同（Unity 15，本地 14），该索引由已有对象编排证据解释，不作为物理浮点值比较。
- `unity_11005_getter_setter_bits_20261002`：未修改 Unity wasm 的被动读取/写入位模式采样。读取范围为 ordinal 2–1023：线速度 2044 次、角速度 1022 次；写入范围为 ordinal 1–1023。
- `c131_getter_gap_closed_20261002.json`：生产修复后的连续回放；记录初始/Reset 姿态和摩擦，不注入释放后的 Unity 状态。
- `11005_angular_gap_verified_20261002.json`：自动验收结果、文件哈希和剩余场景差异。任意 getter/setter 位模式差异直接使验收失败；不再将 getter 差异作为不影响通过的附注。

两份成功的新 Unity 采样均与旧基线比较了完整摩擦序列、1023 对 setter、40 帧动态核心值和 12 枪终点，确认观测没有改变计算结果。第一次质量采样 `unity_11005_mass_properties_20261002` 因把每帧的 `f73070` 设为根、读取过多内存导致协议超时，**不得用于机制闭合或回归结论**；成功版本只以质量重算 `f73060` 为根，并缩小快照。

27 项模拟器测试通过；新增质量属性测试使用实际 Unity 输出 fixture，并检查真实 PhysX body 的激活惯量及原生锁标志。

## 当前串行边界

就活动壶已采样的链而言：释放输入 → 滑行读取/计算/写入 → 冰面求解与积分 → 下一次读取，原 466/482 缺口及第 2 次正负零缺口已闭合，已采样读取与写入连续通过至 1023。

就完整场景而言：目标壶在首次石头碰撞入口 quaternion 不同；其最早分叉尚未定位。不能据活动壶通过的读写序列，将整个场景的分叉点报为 1023，也不能把局部接触点相同当成完整姿态输入相同。后续应从目标壶激活/Reset 的原始 P/Q/v/w 开始采样，逐次比较贴冰求解、积分和休眠，找到首个真实分叉。

## 复现

```powershell
python analysis_input/extract_stone_mass_kernel_20261002.py
python analysis_input/verify_stone_mass_properties_20261002.py
python analysis_input/verify_11005_angular_gap_20261002.py
& 'C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe' -m unittest discover -s local_simulator/tests -p 'test_*.py' -q
```

原始代码内核验证使用研究环境的 `wasmtime`，生产模拟器没有增加这一依赖。
