# 修复初始化凸包输入（2026-10-02）

已修复 [从头审查](startup_geometry_audit_20261002.md) 找到的正式冰壶凸包输入差异。默认碰撞网格改为当前 Unity `f72908` 实际接收的固定 512 顶点资产，保存原始顺序与 float32 位值，替代旧重建圆柱。没有交换轴猜测、重算圆周坐标、调整烹饪数值参数或额外写入凸包质心/内部几何参数。

生产修改为 `local_simulator/unity_physx.py` 的 `DEFAULT_FORMAL_STONE_MESH` 和新资产 `local_simulator/assets/unity_stone_convex_input_512.json`。原重建网格保留，可显式指定用于历史诊断。资产是固定碰撞网格输入，并非烹饪输出、某一帧位姿或求解结果；它包含 Unity 二进制哈希、实际函数、16 次调用 ID、日志哈希及完整点缓冲区哈希。生成脚本 `build_actual_stone_cooking_input_20261002.py` 直接从运行记录解码原始字，不使用几何公式。

## 实际计算验证

Unity `f72908` 的 16 次输入与修复后 CP39 RVA `0x926b0`、`0x9aaa0`、`0x9b070` 原生 descriptor 全部逐位一致：512 顶点、1,536 个分量，count512、stride12、flags2、vertexLimit255、quantizedCount255。

在现有 runtime hull 导入函数调用**之前**读取本地烹饪输出，并与 Unity `f72915` 输出及第一 Reset PCM 入口的实际内存核对：

- 128 个顶点及全部面/拓扑数值段合计 4,008 字节一致：polygons1,320、hullVertices1,536、facesByEdges384、facesByVertices384、vertexData384。
- AABB、网格质心和 internal 共 13 个 float32 字一致，原先 4 个头部差异由正常烹饪自然消除。
- BigConvex samples、valencies、adjacency 原始数组一致。
- 导入后完整运行时 feature buffer 4,008 字节也一致；原生 Stalker 与无 Stalker 运行的最终凸包一致。

这里确认了实测输入和数值输出边界，不把边界一致称作每条烹饪指令已对照。现有 feature 导入保留：本地烹饪的预导入布局仍额外包含 768 字节 GPU 边数组，Unity 布局没有这一段。两侧公共几何字段全部一致，导入后布局一致；`PxCookingParams/buildGPUData` 的实际生成分支尚未核对，因此未宣称整个烹饪内部链闭合。

## 状态回归

从正常初始化、Reset、BESTSHOT 开始，不注入位姿或求解输出，重跑样本11000：

- 新的被动包装采样与无包装采样双方 3,362 个完成帧、87,412 个状态字一致。
- 新采样与修复前生产版本的释放状态及全部 3,362 帧状态一致。
- 直接与现有 Unity 双冰壶完成帧记录比较，第1–2,000帧、52,000个P/Q/v/w原始字仍完全一致，包含双方最终静止。
- 34 项原有检查通过；新增真实 Unity 烹饪输出回归通过，共35项。新测试在既有凸包导入前检查原生自然输出，导入操作不能掩盖其失败。

这些状态结论仍限于 Windows CP39、样本11000及同一已记录摩擦输入；不能推广成内部 RNG、协议计算、所有出手参数和其他 ABI 已闭合。

## 可复查证据

```powershell
python analysis_input/verify_stone_cooking_input_repair_20261002.py
& 'C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python39_64/python.exe' -m unittest local_simulator.tests.test_unity_stone_cooking
```

机器报告 `stone_cooking_input_repair_verified_20261002.json` 记录当前生产代码、输入资产、二进制和所有原始证据 SHA256。原始 Unity Wasm SHA256 为 `cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81`；CP39 内核为 `7c31ced1773023e552391645e42040c9f3694d513805bc8b95ef0f8bc737bd38`，本轮未修改内核。

新原生证据：`native_startup_cooker_input_fixed_20261002/calls.json`、`native_startup_geometry_input_fixed_20261002.json`、`native_stone_input_fixed_plain_20261002.json`、`native_stone_input_fixed_wrapped_20261002.json`。修复前同名 audit 证据、旧网格和 Unity 采样都保留，未被新结果覆盖。旧 verifier 绑定历史生产 SHA；当前修复应使用上面的新 verifier。
