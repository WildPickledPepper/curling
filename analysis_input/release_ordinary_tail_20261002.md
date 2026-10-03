# 首次接触与普通物理尾段探查（2026-10-02）

后续已完成 [目标自然激活修复](target_natural_wake_repair_20261002.md)：原第 1561 帧分歧消除，样本 11000 双冰壶从第 1 帧至第 2000 帧的完成状态共 52,000 字相同，覆盖最终休眠。以下为修复前的历史探查；当前版本请运行 `verify_target_natural_wake_20261002.py`。

当前已观察分歧位于**第 1561 帧的目标冰壶唤醒**。本地 `step_custom_sliding` 用 `_reaches_pcm_shell_this_tick` 预测下一位置，提前调用目标 `wake_up()`。直接记录该调用确认目标由 sleeping=True 变为 False；同帧 Unity 目标 core 在求解入口、出口和下一次 DCP.FixedUpdate 入口保持原来的位置、四元数和零速度。本地已产生极小速度并推进四元数。尚未修改生产代码。

这里的结论来自实际函数调用与内存读取。没有根据终点误差选择开关，也没有用经验补偿修正结果。下一步需要直接记录 Unity 在第 1561–1562 帧的岛激活、目标 BodySim 纳入积分列表及唤醒调用，确定应恢复的真实生命周期；不能把距离判断开关本身视为还原出的内部机制。

## 同一时点的逐位结果

- 样本 11000，Windows CP39，全新默认生产场景，自然 Reset 后执行 BESTSHOT，使用同一记录摩擦输入。
- 主冰壶每个完成帧边界的 Pxyz/Qxyzw/vxyz/wxyz 共 13 个原始 float32 字，从第 1 帧到第 3362 帧连续相同，共 43,706 字。主冰壶在第 1603 帧休眠，后续记录仍相同。
- 第 1562 帧才出现第一次冰壶之间的接触回报；第 1561 帧仍在首次接触之前。之前把第 1022–1025 帧称为这个样本的“碰撞附近”不正确。
- 目标冰壶在此次新增窗口中的第一个已观察状态差异是第 1561 帧；第 1562 帧也不同。第 1563–3362 帧，两只冰壶的 26 个状态字均相同，共 46,800 字。该后段恢复一致不能消除前面的分歧，不能宣称双冰壶完整链条已闭合。
- 第 1561 帧目标四元数 Y：Unity `2c414a0a`，本地 `2c485f1c`；线速度 X：Unity `00000000`，本地 `ab0a7d0e`。本地两次显式 `wake_up()` 在第 1561、1562 帧。
- 第 1919 帧整帧完成后两边都将目标速度清零，最终位姿相同。最初拿 Unity 的求解器出口与本地 fetchResults 后状态比较，出现了伪差异；已用下一次 `DCP.FixedUpdate` 入口的直接内存读取纠正。

边界采样取实际 `table[10980] → f61107` 的 FixedUpdate 入口，对应上一物理步已收尾、下一步尚未施加重力及阻尼的 core 状态。求解器任务出口不能代替完整帧边界，尤其最后一个活动 actor 休眠、Unity 不再执行位姿写回时。`table[121708] → f72606` 的位姿规范化采样保留，用来观察活动 actor 的写回顺序。

## 碰撞回调的直接实现

原始 Wasm 中 `table[10896] → f61030`（CurlingStoneNew.OnCollisionEnter）的对应标签分支写入组件 `+16` 字节标志，随后调用 `f32511`、`f32512`，分别写入静态、动态摩擦 `0.6`。DCP.FixedUpdate `f61107` 在自定义滑行分支读取组件 `+16`；标志为真时跳过该段。此次实际摩擦记录停在第 1562 帧，此后直接普通物理推进的状态与 Unity 同时点采样一致。没有“低于 0.8 就停止滑行”的证据，也未据此实现阈值。

## 观测可靠性与复查

[验证脚本](verify_release_ordinary_tail_20261002.py) 与 [机器结果](release_ordinary_tail_verified_20261002.json)。运行：

```powershell
& 'C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe' analysis_input/verify_release_ordinary_tail_20261002.py
```

Unity 原始 Wasm SHA256 `cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81`；CP39 内核 SHA256 `7c31ced1773023e552391645e42040c9f3694d513805bc8b95ef0f8bc737bd38`；生产代码 SHA256 `d1af92f272aea36bcbe836ef48e5c5f6ec3d3a0e3ad071b90ac771ca03d9221d`。

新增 Unity 被动 observer 保留全部被包装的原始 Wasm 函数体。1562 条摩擦输入、256 条 Reset core 记录、1563 对密集 setter 数据及协议终点与原始基线相同。本地调用观测与原完整运行的释放状态、1562 帧输出、接触点及其他物理字段一致；只排除跨进程不同的 actor/shape 分配地址。带求解跟踪的前 256 帧普通尾段与不带跟踪运行的双方状态也逐字相同。

证据：

- `unity_release_tail_fixed_boundaries_20261002/logs/unity_runtime_probe_20261002_173246/events.jsonl`：双冰壶 core、实际任务顺序及下一 FixedUpdate 边界。
- `native_release_ordinary_tail_1800_20261002.json`：正常生产调用连续推进，不注入位姿、速度或求解输出。
- `native_release_target_wake_calls_20261002.json`：目标 wake_up 实际调用前后及睡眠状态。
- `pcm_functions_20261001/f61107.wat`、`f61030.wat`：原二进制反编译的 DCP.FixedUpdate 和碰撞回调。

范围限制：没有逐条证明全部算术中间值、内部 RNG 状态、此前每帧目标状态或所有样本相同。目标岛激活函数、协议坐标转换和字符串格式化、游戏状态切换仍须单独跟踪；最终坐标相同不替代这些内部检查。
