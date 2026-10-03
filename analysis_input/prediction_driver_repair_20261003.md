# 自主预测的摩擦消费与 Update 调度修复

## 结论与实现

修复 `StrictCurlingEnd.play` 的外层驱动，`inverse_spin_shot` 通过此入口自动使用新路径。调用者只提供出手、场景和本地种子即可预测。自由滑行和有目标场景都走 `local_simulator/unity_prediction.py`，不再由水平速度 <=0.01、5000 项预生成噪声的长度或旧原生批量循环决定自定义滑行的结束。

链条：帧时钟推进 → 每个到期固定步检查控制器/碰撞/启用门 → 门通过才抽一次摩擦并执行原有滑行 setter → PhysX → 原有碰撞回调与姿态写回 → 下一固定步；本帧固定步耗尽后才执行控制器 Update 的停止检查。

`UnityPredictionClock` 按原始 f79750 与 f77913 的顺序执行。帧增量与最大增量比较用 f64；timeScale 乘法按 f32 舍入后提升到 f64；固定时间用 f64 逐次加上提升后的 f32 固定步长，不用近似除法取整。默认独立预测选择可复现的饱和帧输入：timeScale=96、最大帧间隔=.33、固定步长=.01、初始累计时间零。每手种子仍采用原有本地策略 `seed+shot_number*7919`，这不是对未知 Unity 全局种子的推断。

`UnityPredictionDriver` 惰性抽取 RNG。第一次 Stone 进入事件后，后续固定步不再抽取；Wall 停用后也不再抽取。物理尾段继续执行。自然停止只在 Update 边界按位于缓存起点一米以外、活动壶三维速度平方 < f32(1e-6) 判断；按 dynamic/static 的原始顺序恢复 .6，然后按 f61089 对启用壶的三维线速度平方检查，全部 <= f32(1e-6) 才清除出手进行标志。这里没有用角速度或 .01 替代原条件。

流耗尽及帧输入耗尽会报错；步数预算耗尽返回未完成，预测入口会拒绝将其报告为已静止。结果包含实际固定步数、随机抽取数、Update 数、最终 RNG 状态和时钟状态，便于复查。

原有提供 `friction_noises` 的 Scene 首碰回放 API 保留为录制输入回放；它们的输入窗口长度不能作为自主预测调度的证明。`training_fast` 参数保留兼容性，但该预测入口不再使用缺少 Update 边界的旧批量循环。

## 直接证据

- 原始 Wasm：`analysis_input/unity_20260930.wasm`，SHA256 `cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81`。当前服务器压缩构建解压后与此相同。
- 原始控制器：`scheduler_functions_20261003/f61107.wat`（FixedUpdate，原表索引10980）、`f61097.wat`（Update，原表索引10970）、`f61089.wat`（全部停止检查）、`f61094.wat`（Awake 明确设置 infinite 模式 timeScale=96）。碰撞回调为原始 f61030。
- 时钟：同目录 `f79750.wat`（帧时间）、`f77913.wat`（是否开始下一个固定步）、`f80140.wat`（TimeManager 单例）；提取清单/哈希为同目录 `manifest.json`。固定步/最大增量的序列化设置另见 `research_archive/unity_reverse/docs/unity_reverse/00_overview_assets.zh.md` 的 TimeManager 记录。
- 实际直接调用跟踪：`prediction_schedule_unity_v4_20261003/logs/unity_runtime_probe_20261003_201831/events.jsonl`。timeScale setter 依次收到16、4、96；活动控制器在 FixedCount176186 的 Update 后进入出手状态，随后3168次实际 Range 调用，到 FixedCount179354 的 Update 前仍进行中，Update 后清除 +236。下游 FixedUpdate 继续进入但不再抽取。
- 插桩：`prediction_schedule_calls_20261003.json`。f61097、f61107、f54300、f54557 原始函数体逐字节保留，原入口变为参数/返回值转发 thunk。patched SHA256 `8b964d6853d5fb7775f39fc3c620c2b9cc16ce8c9ad0f6320f3ba8e55cae8daf`。
- **插桩的计时无扰动未证明**：本次没有修改 RNG/时钟状态，但日志开销可能改变浏览器帧间隔。修正后的 `observer_manifest.json` 明确记录此限制；不能把日志中的批次大小推广为所有机器/所有帧恒为3168。

## 验收

1. `verify_prediction_clock_20261003.py` 用 wasmtime 执行提取出的原始 WAT 函数，保持原算术与访存，仅去除类型引用以组成独立可执行模块。6种 timeScale、2580帧（含饱和、短帧、随机间隔、零增量及临界值），固定步调用次数一致；frameTime@80、fixedTime@32、timeOffset@208 每帧 f64 字节一致。报告 `prediction_clock_validation_20261003.json`。
2. `test_unity_natural_stop.py` 新增自主驱动回归：停止由引擎时钟和状态决定，不读取摩擦输入长度；12004 的释放及4000完成步、两壶共416104状态字节全部一致。2506步满足停止速度条件但尚无 Update，继续抽取至3168；Update 后从3169开始不再抽取，后续832步状态仍一致。输入生成器若多抽一次即失败。
3. `test_unity_target_activation.py` 新增实际碰撞消费回归：1561–1563实际状态字一致，1562步进入碰撞后不再多抽一次，即使没有执行 Update。
4. `test_unity_wall_collision.py` 新增墙碰自主驱动回归：12000 的全部已采到 live actor 状态与启用身份一致；1879步后停用门阻止继续抽取。
5. `python -m unittest discover -s local_simulator/tests -v`：Windows CP39，48项全部通过，含活动壶停止但其他壶仍移动时保持进行标志、只恢复材料的分支。原有完整轨迹/内部窗口回归保留。
6. `verify_autonomous_prediction_20261003.py`：自由滑行、首碰、墙碰、高旋4场景各跑2次，同种子与时钟的终态字节哈希及计数/RNG状态全部复现；持久 Scene 连续16手全部完成。报告 `autonomous_prediction_validation_20261003.json`。此项是本地重复性检查，不冒充 Unity 同输入逐位验证。

## 结论范围

本次闭合的是运行、非暂停、captureFramerate=0、非扫冰预测入口的时钟计算及消费门，以上 Unity 数值窗口全部通过。完整浏览器 PlayerLoop、暂停/单步/captureFramerate 路径及扫冰控制不在本次实现范围。

**全部随机输入相同还需要调用时钟输入相同**，才能要求后续轨迹逐位相同。原始代码直接表明帧间隔和释放时的固定时间余量会决定停止 Update 在哪个固定步之后发生。独立预测使用明确固定的时钟策略；复现某次实机运行时，可向 driver 提供实际帧间隔及释放边界的 TimeManager 初始状态。未知的随机状态、帧时钟或未采到的历史不会补造，也不会据此宣称任意实机运行全链路100%一致。
