# 从头审查：初始化凸包的实际输入差异（2026-10-02）

本页保存修复前证据。顶点输入及其自然烹饪数值输出现已修复，见 [初始化凸包输入修复](stone_cooking_input_repair_20261002.md)。旧机器报告绑定历史生产源码，当前版本使用新的修复验证脚本。

本次从初始化重新检查内部数据，不以完成帧 P/Q/v/w 一致反推所有内部计算一致。当前最早**已直接观察**的差异在正式冰壶凸包烹饪的顶点输入，发生在第一次 Reset 和释放之前。建场及更早的网格读取/生成调用尚未穷尽比较，不能称它为全程序已证明的首条分歧指令。

## 实际入参

Unity 原始 Wasm SHA256 为 `cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81`。直接包装 `f72908`，从其实际读取的上下文 +4 获取 PxConvexMeshDesc，并读出原始点缓冲区。16 次正式冰壶调用的 512 个顶点全部逐位相同。对应调用 ID 为 131、142、153、164、175、186、197、208、219、230、241、252、263、274、285、296。

本地通过 Frida Stalker 在默认生产路径第一次 `_make_stone` 执行期间，只读采集原生调用入参。CP39 RVA `0x926b0`、`0x9aaa0`、`0x9b070` 的参数 1 均直接携带同一顶点数据的 Win64 PxConvexMeshDesc。这三份原生缓冲区与 Python 实际传入的数组逐位相同，因此差异不是只在 Python 层观察到的。

两边 count=512、stride=12、flags=2、vertexLimit=255、quantizedCount=255 相同。但是 1,536 个顶点分量中 **1,020 个原始 float32 字不同**。首个差异为顶点 0 的 X：

- Unity 第一个顶点为 `(0, 1, 1.25)`，位值 `00000000 3f800000 3fa00000`。
- 本地第一个顶点为 `(1.25, 1, 0)`，位值 `3fa00000 3f800000 00000000`。

本地来源已通过源码和实际原生内存对应到 `local_simulator/assets/stone_extendedcollider_mesh_256.json → _formal_stone_points → Y-up 转换 → pybind → 原生 descriptor`。这里只确认输入不同，不凭对称外形推断交换轴就能修复。即使对数据做 X/Z 交换，仍有 632 个分量不同；该离线比较仅说明两组输入不是简单逐位轴交换关系，没有用于实现补偿。

## 后续数据为何能够一致

Unity `f72915` 的 16 次正式冰壶输出均为 128 顶点、66 面，原始输出缓冲区相同；它们与本地烹饪输出的顶点顺序、面法线不同。本地现有生产路径随后导入从 Unity 采集的凸包 feature buffer，并重建 BigConvex 数据。导入后的 **4,008 字节 feature buffer、BigConvex samples/valencies/adjacency 三组缓冲区均与当前 Unity 内存逐字节一致**。这是明确使用已采集的固定几何资产，不是烹饪内部计算已经对齐的证明。

而凸包头的 4 个数值仍未被现有导入替换。本次首次 Reset 的 PCM 入口（table120119、resetSerial1、resetPhysicsStep1）直接确认：

- `mCenterOfMass.x`：Unity `b32d9c27`，本地 `321e8a27`。
- `mCenterOfMass.y`：Unity `b29e56f4`，本地 `32b494a6`。
- `mCenterOfMass.z`：Unity `32a00860`，本地 `31ef9e3d`。
- `mInternal.mExtents.x`（Unity 凸包头 +52）：Unity `3f8dd3db`，本地 `3f8dd3dc`。

这里的凸包质心属于网格烹饪数据，与 Rigidbody 通过 Start 设置的零质心不是同一个字段。没有把头部差异造成的影响臆测为某个轨迹误差，也没有修改这些字段或生产资产。

## 观察器验证与复查

两次新 Unity 采样都保留所有被包装函数的原始正文，源/插桩哈希核验通过。与基线比较，256 次 Reset core 采样、1,562 次摩擦记录、1,563 对密集 setter 的共有物理字段、协议终局物理结果全部相同。额外 bridge 输入字段只在旧 release-setter manifest 下采集，不把新观察器未采集的字段混作数值差异。

本地 Python 被动包装与普通初始化的双方凸包、16 只冰壶的初始状态原始字及质量信息一致；原生 Stalker 采样后的最终凸包也与普通生产路径一致。生产代码未改动。此前当前样本双方每个完成帧的 52,000 个状态字检查重新通过，说明初始化内部差异与该样本帧末轨迹一致可以同时成立。

复查：

```powershell
python analysis_input/verify_startup_geometry_audit_20261002.py --suffix _inputs_v2
```

机器结果及证据 SHA256 见 `startup_geometry_audit_verified_20261002_inputs_v2.json`。主要原始文件：

- Unity：`unity_startup_geometry_audit_capture_20261002_inputs_v2/logs/unity_runtime_probe_20261002_184502/events.jsonl`。
- 原生：`native_startup_cooker_inputs_20261002/calls.json`；各条记录保存函数 RVA、descriptor 地址及全部 pointBits。
- 本地烹饪前/导入后：`native_startup_geometry_audit_20261002.json`。
- 同次实际观察器、manifest：Unity 采样目录中的 `observer_source.js`、`capture_manifest.json`。
- 原始反编译：`pcm_functions_20261001/f72908.wat`、`f72915.wat`。
- 原生调用入口指令：`native_cooker_input_entry_disassembly_20261002.json`。

接下来应沿 Unity 的实际点缓冲区来源继续向前追踪网格读取/生成、轴布局和 float32 写入，找到这一输入差异的产生位置。暂未比较全部 PxCookingParams、烹饪分支和每个计算中间值；当前没有依据宣称交换轴、替换某个常量或某项烹饪开关已还原机制。
