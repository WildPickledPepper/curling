# 本地局部 Unity 采样验收（2026-10-03）

按用户要求：已有局部采样可以作为验收依据，不要求每份日志都包含完整轨迹。没有抓到的字段不补造；只核对实际输入、调用阶段和实际输出。本轮没有新增 Unity 采样，没有修改生产物理。

盘点了 **352 份 events.jsonl，8082739215 字节**，其中 **253 份日志**已有数值窗口接入本轮核对。

原先只接入 81 份，是比较器支持范围过窄且验收提前停止，并非剩余日志不能使用。上一轮扩展到 222 份后也提前停止；本次从此前未核对的 130 份中，又增加 **31 份**。总计增加 **172 份此前未核对日志**；仍有 **99 份**没有接入数值比较，逐份保留实际事件类型及待处理原因，不能计入通过数量。

`remaining_capture_payload_review.json` 读取剩余日志实际 payload，保留每种事件的首次行号及字段结构。未核对项需逐项区分未完成适配器、缺少同一次调用输入/输出、只有安装或调度记录等情况，不按是否有完整轨迹排除整份日志。归档中存在 reset.rotation_restored 主动干预记录；局部同输入函数验算通过不等于原场景未经干预，也不证明串行前缀通过。

本轮已核对的范围全部逐位一致，没有确认新的分叉：

- **45 份局部轨迹日志，169,220 个 P/Q/v/w 状态，8,799,440 字节**。完整原生回放只使用同一布局、投掷和实测摩擦随机数；只比较 Unity 实际抓到的释放姿态、滑行前状态和完成边界。另核对 46,556 个活动对象成员集合。
- **74 份日志的 108,186 次滑行计算**：实测速度 getter 和摩擦随机数输入到脚本角速度 setter 输出，包含历史批次里的局部窗口。扫冰分支由原样例清单的 sent_sweep/requested.sweep 和实收命令核对。
- **212 份旧格式日志的 8,909 个 A0/A2 调用阶段窗口**：同一次实测速度 getter、同 tick 摩擦随机数到角速度 setter，另有 8,461 个窗口同时核对线速度 setter；全部逐位一致。这与前面的日志有重叠，不相加为独立日志数量。归档样例通过采集 session 时间、实际 BESTSHOT/Reset 浮点输入与原样例清单匹配扫冰分支；缺少证据时留空。
- **330 个实测 Transform 矩阵/正式冰壶惯量窗口**，当前生产函数输出逐位一致。只核对采到且满足已还原分支的函数；其他物体质量属性、缺失层级或输入字段单独记录。早期协议超时采集中的同输入函数验算不证明该采集的整场轨迹透明性。
- **54 份日志的 1,728 个初始冰壶构造器输入/输出窗口，60,480 个数值字**逐位一致。Unity f71726 与当前原生 RVA 0x214bd0 同边界比较；指针、填充位、其他对象和更早工厂步骤未算入。原生有/无插桩初始化状态一致。
- **121 份日志的 9,008 个 Reset 位置 setter 输入**，由实际协议输入调用当前生产放置计算，三项 float32 全部逐位一致；不包含 setter 内部、旋转、物理步及先前历史。
- **9 份日志的 114 次凸包/凸包 PCM（f70576）**：将实测完整凸包、姿态、参数及持久缓存输入当前原生函数，接触点数量、法线、距离、位置与 face index 全部逐位一致。缺少成对快照或输入数组的调用逐项留空；不含未初始化临时字段与先前场景历史。
- **105,112 次角速度投影**：使用实测 Transform 四元数和实测 setter 输入，两个内存输出位置都逐位一致。
- **107,304 次当前生产角速度设置路径**：使用实测刚体姿态和调用序号，核对两个内存输出。首次释放缺少约束分支证据的调用单独留空，不强套锁轴路径。
- **35 份日志的 8,960 个 Reset 求解器入口/出口核心状态**全部逐位一致。原生采集器另外跑了一次无插桩 Reset，所有逐步状态相同，实际自然休眠为第 42 步。
- 365 对姿态归一化输入/输出算术逐位一致。155,862 次 Unity getter 原始内存记录通过复制/不改写一致性检查；该数值仅是采样有效性检查。

这些数量包含同一案例的重复采集，不能解释为同样数量的独立投掷。局部函数通过也不自动证明此前整段场景历史通过。

**尚未宣称全部本地采样已通过。** 报告逐份保留了还需接入核对器的碰撞约束、求解器、PCM/缓存、几何等现成原始证据。历史批次的完整轨迹需要保留此前投掷与 Reset 历史，不能用新场景替代；它们已采到的函数窗口已经参与上面的函数验算。`unity_reset_core_bounded` 的 Reset 窗口只有空 cores，没有对应核心状态可比，但该日志的滑行窗口已经验算。

调用阶段必须一致：首次角速度缓存设置的 dense post 在 SetActive 前；f73018 重建 actor 时还会直接调用 f73035。它不能与 activation 完成后的 native releaseBits 混比。17 份旋转样例的这两个不同阶段数值不同，这不是相同边界的轨迹分叉，原始记录保存在 partial_trajectories.json。

结果：`local_partial_validation_20261003/report.json`。逐份路径、事件 SHA256、调用行号/序号、已比较范围、剩余证据均可复查；各函数范围分别保存在同目录下的 *_windows.json 和 reset_position_inputs.json。

复跑（仓库根目录）：

```powershell
D:\anaconda3\python.exe analysis_input/audit_all_local_partial_captures_20261003.py --reuse-inventory
D:\anaconda3\python.exe analysis_input/compare_local_motion_windows_20261003.py
D:\anaconda3\python.exe analysis_input/compare_local_partial_trajectories_20261003.py
D:\anaconda3\python.exe analysis_input/compare_local_reset_windows_20261003.py
D:\anaconda3\python.exe analysis_input/compare_legacy_motion_windows_20261003.py
D:\anaconda3\python.exe analysis_input/compare_local_geometry_numeric_windows_20261003.py
D:\anaconda3\python.exe analysis_input/compare_local_startup_windows_20261003.py
D:\anaconda3\python.exe analysis_input/compare_local_reset_position_inputs_20261003.py
D:\anaconda3\python.exe analysis_input/compare_local_pcm_windows_20261003.py
D:\anaconda3\python.exe analysis_input/summarize_local_partial_validation_20261003.py
D:\anaconda3\python.exe analysis_input/review_remaining_capture_payloads_20261003.py
D:\anaconda3\python.exe analysis_input/summarize_local_partial_validation_20261003.py
```

新增日志后，先运行 audit 脚本且不传 --reuse-inventory，重新扫描全部 events.jsonl。
