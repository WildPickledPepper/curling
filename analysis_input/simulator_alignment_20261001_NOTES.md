# 2026-10-01：沿实际调用链定位 PCM 输入缩放差异

后续状态：2026-10-02 已接入实时形状刷新与原生姿态写回，原第 488 次 setter 分叉已消除；当前验收范围见 [修复记录](simulator_alignment_20261002_FIX.md)。本文保留当日机制还原阶段的证据与未完成项。

## 已确认结果

11005 的分歧窗口已从接触结果追到实际形状输入和 Unity 的缩放计算。该窗口中双方接触查询的原生姿态相同，但凸包几何的 X/Z 缩放不同：

| 输入 | Unity | 本地固定值 |
| --- | --- | --- |
| X/Z 缩放 | `0.11270000040531158`，`0x3de6cf42` | `0.11270000785589218`，`0x3de6cf43` |
| Y 缩放 | `0.11500000208616257` | 同左 |

使用隔离查询场景补齐这处已观察输入，ordinal 486、487、488 的六个接触点、法线、分离距离和 face ID 全部逐位相同。主物理场景未采用该修正，其整批轨迹/终点仍与诊断基线相同。因此这是同输入 PCM 的闭合验证，不能表述成完整轨迹已对齐。

全批运行显示活动壶缩放随投掷改变，共四种 X/Z 浮点值；目标壶仍保持初始值。不能把常量统一减一个 ULP。

## 真实生产路径

通过实际内存写入定位到 `f70398`，再沿形状创建的上游调用追到：

```text
f72951  collider 几何构建
  f72950  取得凸包与缩放
    f78119  读取 Transform 层级并取得世界旋转
      f78120  将世界旋转从旋转/缩放矩阵中剥离
        f78121  从层级的局部 TRS 构建世界旋转/缩放矩阵
    输出矩阵对角元素 [0, 4, 8] -> xyz scale
  f73283 -> f73282
    虚调用 f72573  创建 PhysX shape
      f70398  复制输入 PxGeometry
```

捕获到的冰壶层级只有自身与一个父节点：

- 自身局部 scale 为三个 `0.11500000208616257`。
- 父节点 quaternion 为 `[0,0,0,1]`，scale 为 `[0.9800000190734863,1,0.9800000190734863]`。
- 自身 quaternion 随历史状态变化。没有通过终点误差拟合这些输入。

`f78121` 以实际指令顺序构建并逐层相乘矩阵；`f78120` 再乘以逆世界 quaternion 对应的矩阵；`f72950` 读取最终矩阵对角线。这些浮点操作在当前 quaternion 下产生多个相邻 f32 结果。实现中每次乘法/加减都必须单独舍入到 f32，点积为 `a + (b + c)`。没有取列向量长度，也没有用平方根估算缩放。

## 已移植与核验

`local_simulator/runtime_support/tools/reverse/recovered_transform_scale.py` 已实现上述已观察层级的计算，尚未接入实时形状刷新。范围是单个无旋转、正缩放的父节点，不能将其当作任意 Transform 层级的完整实现。

从原始 Unity Wasm 提取 `f78119/f78120/f78121`，只重定位直接调用函数索引，数值指令保持原样；需要同步层级的辅助函数设为 trap，离线重放显式提供已经同步的层级输入。

| 核验 | 结果 |
| --- | --- |
| 原始 Wasm 函数重放 | 138 次调用的 1,242 个矩阵浮点字段逐位一致 |
| 本地 Python 移植 | 同一 138 次调用的全部矩阵字段逐位一致 |
| 矩阵 -> f72950 -> shape 输入 | 23 次形状创建的三个缩放字段逐位一致 |
| 插桩透明性 | 六次相关捕获均保持 12 次终点、15,580 次摩擦输入、1,023 对 setter 状态一致 |
| Windows 原生 PCM 跟踪 | 213 次 Interceptor 调用，调用栈完整、无丢弃；轨迹保持基线一致 |
| 独立回归 fixture | 11 组去重的原始 Unity quaternion/矩阵输出 |
| 相关单元测试 | 18 项通过 |

形状构建捕获中只有 23 次根调用：一个形状已在首个 pending release 生效前创建。矩阵重放核验只覆盖日志实际包含的 138 次调用；该数量不应写成 24 次完整创建均被捕获。

## 证据与复现

原始 Unity Wasm SHA256：
`cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81`。

当前 Windows CPython 3.9 原生模块 SHA256：
`2564abec4fa3f358e67259b105c4b88d49eae28510611c8a0e2f11b7671888df`。

- 总体验证：`pcm_internal_trace_verified_20261001.json`。
- 输入补齐查询：`c131_matched_geometry_input_20261001.json`。
- 本地基线：`c131_full-q_pcm_direct_verified_20261001.json`。
- Unity 原始几何/内部调用：`unity_11005_pcm_internal_calls_20261001/`。
- PCM 候选点选择：`unity_11005_pcm_candidate_calls_20261001/`。
- 原生可靠调用跟踪：`native_pcm_interceptor_20261001/calls.json`。
- 形状内存写：`unity_geometry_writers_20261001/`。
- 原始 shape 创建调用者：`unity_geometry_producer_20261001/`。
- Transform 层级、矩阵与形状输入原始调用：`unity_transform_scale_calc_trace_20261001/logs/unity_runtime_probe_20261001_233057/events.jsonl`。
- 提取函数哈希：`unity_transform_scale_kernel_20261001.json`。
- 原始函数重放结果：`transform_scale_kernel_verified_20261001.json`。
- Python 移植/生产链核验：`recovered_transform_scale_verified_20261001.json`。
- 可携带的测试 fixture：`../local_simulator/tests/fixtures/unity_transform_scale_20261001.json`。

在项目根目录执行：

```powershell
& 'D:\Node_js\node.exe' analysis_input/verify_transform_scale_kernel.js
& 'C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe' analysis_input/verify_recovered_transform_scale.py
& 'C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe' -m unittest local_simulator.tests.test_recovered_transform_scale local_simulator.tests.test_strict_simulator
```

重新插桩可用 `instrument_geometry_writes.py --trace-functions 72573 72951 72950 78119 78120 78121 --geometry-root-functions 72951 72573 --output <新路径>.wasm`；必须重新执行原有透明性验收，不能覆盖已留存的运行。

## 下一处需要直接补证与实现

1. 追踪 Rigidbody 物理姿态写回 Transform 后的实际局部 quaternion。当前移植输入是捕获的局部 Transform；不能无证据地用 yaw 重构或用任意时刻的 PhysX quaternion 替代它。
2. 接入 SetActive/collider 构建时的 shape 缩放刷新。当前绑定可创建带 scale 的凸包，也可克隆既有凸包，但克隆接口没有新 scale 参数，且未暴露 `PxShape::setGeometry`。需要补充安全的原生接口或按实际创建路径重建形状，保留已还原的 runtime hull/BigConvex 数据和 actor 状态。
3. 用本地计算的 Transform 与 scale 运行原有诊断批次，再从首个未对齐的原生状态继续追踪。不得在线注入捕获的 Unity scale/quaternion，也不得以终点改善替代内部一致性验收。

尚未修改训练默认、实时碰撞体或现有原生模块。完整端到端对齐尚未完成；本次新增的是已还原、可复算、经过原始输出验证的缩放计算及其证据链。
