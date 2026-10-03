# 当前模拟器与 Unity 对齐检查（2026-09-29）

## 范围和方法

初始阶段是当前 Windows CP39 模拟器对历史 Unity 原始采样的离线回放。后续为同一组12条计划补录了 Unity 原生边界，并修改了生产模拟器的**默认关闭**的精确发射开关及原有诊断角速度投影函数；没有改物理参数或覆盖用户已有改动。不覆盖 CP313/Linux。

- 解释器：`C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe`。
- 扩展：`local_simulator/runtime/pyphysx/_pyphysx.cp39-win_amd64.pyd`。
- 扩展 SHA256：`2564abec4fa3f358e67259b105c4b88d49eae28510611c8a0e2f11b7671888df`。
- 采样目录：`research_archive/unity_reverse/evidence/data/calibration/extended_collision_validation_20260715_ordered/`。
- 输入：`collision_unique_targets_batch_r03.jsonl` 与同目录 `collision_unique_targets_batch_r03_orientation.json`。
- 事件：`research_archive/unity_reverse/evidence/log/extended_collision_validation_20260715_ordered/collision_unique_targets_batch_r03/unity_runtime_probe_20260715_125420/events.jsonl`。
- 审计逻辑：`research_archive/unity_reverse/source/reverse/audit_hybrid_p6_endpoint_sixshot.py`。在进程内适配旧 CP38 加载段，改由当前 runtime_loader 加载 CP39，导入当前 `local_simulator.unity_physx`；保留原有回放和统计逻辑，使用 `native-pyphysx`、`--require-orientation-truth`，显式提供输入与输出路径。没有更改归档脚本。
- 使用记录的初始朝向和摩擦序列，不注入 Unity 碰后状态。此条件比只有 POSITION/BESTSHOT 的普通对战协议更强。

输出：`simulator_alignment_20260929_cp39.json`。

## 本次结果

12 条配置，7 条实际接触；12 条都有朝向证据，无不可靠终点来源。7 条接触样本均完成静止结算。全部12条本地终点与历史 `collision_unique_targets_batch_r03_endpoint_strict_native.json` 完全一致。

整体投掷壶：9条可计算距离，RMSE 7.739 mm、平均4.565 mm、最大19.976 mm。
整体目标壶：12条，RMSE 2.499 mm、平均1.174 mm、最大8.278 mm。
整体统计含5条未接触样本，不能全部称作碰撞精度。Unity 清除的3条投掷壶不计算距离；本审计不证明清除/出界规则完全一致。

| 样本 | 类型 | 投掷壶误差 mm | 目标壶误差 mm |
|---|---|---:|---:|
|12002|深碰左侧|0.379|0.701|
|12006|反向弧线左到右|1.046|1.007|
|12007|反向弧线右到左|0.342|1.101|
|12008|高旋左到右|9.523|0.354|
|12009|高旋右到左|4.438|1.144|
|12010|左侧偏心碰撞|5.312|8.278|
|12011|右侧偏心碰撞|19.976|1.495|

## 剩余问题：证据等级

1. **本次复现**：偏心/高旋碰后终点仍有毫米到约2厘米残差。仅终点回放不能断言本批每条的第一分叉位置，需要对最差样本逐帧对齐后再归因。
2. **此次复测的相近构型**：C133/C134 wide-right 的被撞壶在 C03 求解入口 P/v/w/q 为数值零差；首次写回后的线速度差分别为0.002089/0.002656 m/s、角速度差分别为0.009991/1.062073 rad/s，终点误差6.866/11.848 mm。当前 CP39 回放结果与归档报告一致。投掷壶在入口位置有11.749/23.483 mm差，可能涉及阶段比较；这里仅将“被撞壶从求解写回开始分叉”视为直接证据。C133/C134 是 wide-right glance，不能直接替代12011远距离偏心构型的逐帧归因。
3. **此次复测的连续姿态影响**：左分裂同一份12条 Unity摩擦记录，在当前 CP39 环境中沿用本地连续姿态时，投掷壶平均19.238 mm、被撞壶平均32.266 mm，最大被撞壶155.266 mm。明确重置双方姿态时，对应平均0.494/1.731 mm，被撞壶最大8.534 mm。后者是独立重置姿态诊断，不是连续协议的精度估计。与历史文档中连续模式15.566/37.459 mm、最大176.284 mm的统计不同；这些旧数不能覆盖此次复测结果。
4. **输入可观测性限制**：POSITION不提供完整姿态/物理历史；相同随机种子不保证相同随机消费序列。严格摩擦/朝向回放成绩不能直接外推到在线对战。
5. **历史协议问题、此次未复测**：旧扫冰大偏差与请求是否及时生效有关，不可当作已证明的全局摩擦参数偏差。不能宣称所有真实生效扫冰已验证。

历史归因来源：`research_archive/unity_reverse/docs/unity_reverse/15_persistent_scene_alignment_ledger.zh.md` 和 `16_rng_evidence_inventory.zh.md`。

## 现有采样覆盖与下一步

- 12008、12010、12011：已有同场12条的原始 `samples`、`events.jsonl` 摩擦流、A10重置朝向清单及终点；当前回放通过。该批事件流只有摩擦和A10类探针，**没有** C03/C04 求解器帧，因此无法只凭这批材料确定每条的首个分叉。12008另有 C120/C126 high-curl 专项静态和接触记录，但属于另一轮运行，不能把该帧直接配到当前12008的摩擦与历史状态。
- 对12011又检查了 C116、C117、C118、C119、C120 多轮同构型采样对应的 `events.jsonl`：各轮 C03/C04 帧数均为0；其中仅最终 ordered 批次含12条A10朝向事件。现存这些记录仍可用于终点分布与摩擦敏感性分析，但无法建立12011当前批次的原生首次求解写回对照。
- C133/C134：已有完整 Unity摩擦、重置朝向、C03首求解帧与本地对照；当前 CP39 已重新回放，并重新计算首帧差异。输出 `simulator_alignment_c133_20260929_cp39.json`、`simulator_alignment_c134_20260929_cp39.json` 以及两份 `_first_frame_20260929.json`。复跑适配器为 `replay_archived_unity_audit_cp39.py`。
- 双壶左分裂：已有同场12条记录及摩擦流，当前 CP39 分别回放连续姿态和重置姿态。输出 `simulator_alignment_split_left_persistent_20260929_cp39.json` 与 `simulator_alignment_split_left_reset_20260929_cp39.json`。因归档回放脚本依赖旧CP38和目录布局，本次在进程内选择当前 runtime_support 和当前CP39模块，保留原始样本/摩擦回放逻辑；没有修改归档脚本。

下一步可先利用 C133/C134 已有的 ContactBuffer 和 solver rows 进一步比较写回差异；对于12011/12010，应先在现有档案中继续查找**同一轮**更深探针，不能将另一构型直接类推。没有证据前不拟合全局摩擦或角冲量补偿。

## 12011 的首次可观测分叉范围（本轮追加）

重新读取 ordered 批次原始 `events.jsonl`，按第12条 A10 release 后的摩擦事件计数，与当前模拟器同一摩擦流的逐步回放对齐：

| 检查点 | Unity 记录 | 当前本地回放 | 判断 |
| --- | --- | --- | --- |
| 中线 MOTIONINFO | 第322次摩擦；`(x,y,vx,vy,w)=(2.3506,21.5126,0.0001,-2.7848,0.0038)`，协议四位小数 | 第322步 `(2.3506011963,21.5125403545,0.0001280629,-2.7847905159,0.0037784546)` | 各字段均能舍入到Unity协议值。位置差约0.060mm，受四位小数精度限制，不能据此宣称真正精确数值相同。 |
| 首次壶间回调/本地接触 | Unity第910次摩擦有两次 `CurlingStoneNew.OnCollisionEnter`；另第1次是初始石头/冰面回调 | 本地首个壶间接触也在第910步，4个接触点 | 接触时序一致。 |
| 回调中的碰前相对速度 | 第910次回调 `arg1` 的32位浮点偏移28/32/36处为 `(-1.5999035835,0,+0.0001092708)` | 本地 `beforeScene` 线速度 `(1.5999035835,0,-0.0001092398)` | 该三元组与本地速度相反，纵向数值相同，横向绝对差约`3.10e-8 m/s`。将其解释为Unity碰前相对速度属于布局推断；回调自身没有导出完整石头姿态或求解器写回。 |
| 终点 | Unity投掷壶 `(1.5025,5.6621)`、被撞壶 `(2.9241,8.6630)` | 本地投掷壶 `(1.5218811,5.6572623)`、被撞壶 `(2.9226799,8.6625343)` | 投掷壶误差19.976mm，被撞壶1.495mm。 |

目前能定位到的最后共同锚点是第910步的接触时序和近乎一致的相对速度；第一个明确不一致的观测是停稳后的终点。第322步中线状态对齐，使“碰前运动速度大幅跑偏”缺少证据。可能的第一分叉仍包括碰前未记录的微小位置/姿态差被碰撞放大，以及碰撞接触/求解/结算本身。该轮 Unity 数据没有碰前完整 P/Q，也没有 C03/C04 求解器帧；无法证明第一次数值不相等恰在第910步，更不能断言就是求解器某条冲量行。`simulator_alignment_12011_motion_anchor_20260929.json` 保存了本次加探针回放的标准终点审计；逐步中线值来自本次进程内只读插桩输出。

## 12011 同输入 C03/C04 专项复测：根因已收窄（覆盖上一节的采样限制）

上一节描述的是**旧档案**的数据限制。随后用相同12条投掷计划和逐次强制复用的旧摩擦流，仅针对12011补录了 Unity 原生状态，见 `unity_12011_first_solver_poll_long_20260929/`。新日志含12条A10、21538条摩擦、1条C03、40条C04；摩擦逐项与旧档案一致，12008/12010/12011的Unity终点也与旧档案一致。新日志不是另一条轨迹的类比。

本地逐帧回放：`trace_12011_local_collision_tail.py`；原始输出 `simulator_alignment_12011_local_tail_20260929.json` 和 `_precontact.json`；本地首帧对照 `simulator_alignment_12011_first_frame_20260929.json`。C04 frame 0 对齐本地第899步，frame 11 对齐本地第910步（首个接触时刻），frame 12 对齐本地接触后的下一次 simulate，frame 13 对齐随后的首次显著冲量。C04 的 `tickSerial` 在这些 frame 之间并非递增，不能直接当成物理步序号。

| 物理阶段 | 对齐观测 | 结论 |
| --- | --- | --- |
| 第899步 / C04 frame 0 | 本地投掷壶 native X 比 Unity 高 `7.62939453125e-6 m`（此量级的单精度一 ULP）；投掷壶姿态分量已差约 `1e-6`；线速度 X 完全相同。 | **第一处现有精确帧可观测差异在碰撞前**。不能声称它最早于第899步发生；更早没有同精度Unity逐步姿态。 |
| 第910步 / C04 frame 11 | 投掷壶X仍差 `7.62939453125e-6 m`，纵向速度相同；目标壶尚未动。 | 接触时序正确；小状态差持续进入碰撞。 |
| C04 frame 12 / 本地 first_writeback | 目标壶位置精确相同；投掷壶X差 `7.62939453125e-6 m`，姿态约`1e-6`量级。 | 首次求解写回并未产生厘米级分叉。旧 `audit_c04_local_first_frame.py` 的 active entry 0.177m 是把 C03 的更早 `coresBeforeSolve` 与本地第910步误当同相位比较，不能用作误差。 |
| C04 frame 13 / 本地下一步 | 目标壶线速度X差 `0.0004322 m/s`、角速度Y差 `0.0108567 rad/s`；投掷壶线速度X反向差`0.0004323 m/s`。 | 首次明显动力学差异在这一接触冲量之后。 |
| 停稳 | 原样回放投掷壶误差 `19.9757 mm`、目标壶 `1.4945 mm`。 | 偏心擦碰对微米级碰前状态高度敏感。 |

做了三组**仅用于因果验证的Unity状态注入**，均保持原12条计划、摩擦流及本地碰撞求解器不变：

- 在C04 frame 0 对应的第899步，只将投掷壶姿态和位置设为Unity精确状态，终点投掷壶误差从19.976mm降到`0.04175mm`，目标壶仍有`1.103mm`误差。
- 同时设位置、姿态、线速度、角速度，投掷壶误差`0.04175mm`，目标壶误差`0.04472mm`；见 `simulator_alignment_12011_trace_audit_20260929_frame12_none_pre_all.json`。在 frame 12 全状态注入也得到约`0.0475/0.0447mm`，交叉验证同一结论。
- 只修正第899步的X位置，投掷壶仍差`20.124mm`；只有初始A10原生四元数精确注入，仍差`18.166mm`。不能把这一结果简化为“加一个位置偏移”或“只修正A10”。

**归因与边界**：对12011，当前大误差由碰前单精度P/Q/微小角速度差进入高敏感擦碰并放大；在精确碰前状态下，本地尾段PhysX与Unity终点能到约0.05mm。因此没有证据支持调全局石头摩擦/冲量参数，也不能把C133/C134的求解器问题套到这一条。注入实验使用了本次捕获的Unity内部状态，只证明因果和尾段一致性，**不是**独立预测修复；普通在线协议不提供这个P/Q状态。生产模拟器未做基于12011的硬编码补偿。要使未知投掷也稳定消除同类厘米级误差，需要在碰前状态传播达到Unity逐位等价（包括姿态和角速度）或将擦碰类输出作为不确定结果处理，而非拟合单条终点。

## 12011 发射到首碰的逐写入归因（覆盖前述“碰前状态来源未知”）

新增同一次 Unity release 的 A12 密集探针：`unity_12011_dense_setter_bridge_20260929/`，记录首次 reset angular setter 后的910条每帧 `PxTransform`、线/角速度 getter、脚本角速度 setter 和 native bridge 的角速度写入。仍使用与历史12枪逐值相同的21538条摩擦值；`verify_12011_collision_causality.py` 对事件数和旧样本终点做断言。

从**第一处不等值**到放大，现可精确分层：

| 边界 | 本地旧实现 | Unity 实测 / 不可再分的代码点 |
| --- | --- | --- |
| BESTSHOT 发射位置 | X `-96.8541946411`、Y `14.4197845459` | X `-96.8542022705`、Y `14.4323997498`。`start_bestshot` 复用 `start_motioninfo` 的贴冰面 `_horizontal_position`；既使用 ResetPosition 的 X 基准，也没有发射高差 `12.615204mm`。12枪的 native 发射 X/Y 相同。 |
| 第2帧起竖直写入 | 保留上帧自由落体 `v.y`；第3次 getter 为 `-0.1962m/s` | Unity 第3次 getter 仍为 `-0.0981m/s`，位置每帧只降 `0.000981m`。对应 `step_custom_sliding` / 训练快路径的 `custom_sliding_zero_vertical_setter`，应在每次 Scene 之前写 `0`。这不是调重力。 |
| 每次角速度 native setter | 默认 tilt-only 近似；旧 full-projection helper 把 native quaternion Z 反号 | Unity `func72559/f73035` 的锁轴投影是 `q.rotate(maskXZ(q^-1.rotate([0,wy,0])))`，使用**未反号**的 native pose。第1次 Unity bridge 为 `[-8.79851747e-15, 0.0099680442363, 1.32731071e-9]`；修正后的 helper 三分量逐值相同。 |
| 发射四元数来源 | 离线审计从 `activeYaw` 重新构造四元数 | 同次 A10 native quaternion 与该重构相差数个 float32 ULP；yaw 标量不足以保存历史 tilt/舍入。严格离线对齐使用朝向清单已有的 A10 quaternion，在线模拟仍需维护原生姿态历史，不能用 Unity 真值注入。 |

用生产实现的三个可选语义（`emulate_unity_bestshot_release_pose=True`、`custom_sliding_zero_vertical_setter=True`、`emulate_unity_native_angular_setter_rotation=True` 且 tilt-only=False），加上**离线诊断专用**的 A10 native quaternion，12011 的910个碰前 `PxTransform.p` 全部逐值一致；前7次 bridge 的完整 X/Y/Z 逐值一致。第8次 bridge X 首次差 `2.77555756156e-17rad/s`，第12帧 quaternion 出现短暂1 ULP差，第19帧石头-冰面接触反馈的竖直速度相差 `3.57627868652e-6m/s`。这些比旧20mm分叉小许多；碰后终点误差投掷壶 `0.04175mm`、目标壶 `0.04472mm`，已小于 Unity 终点四位小数的单坐标半格 `0.05mm`。在当前终点精度下，不能再把这约0.04mm解释为另一个可验证的碰撞参数误差。

单项 A/B 说明它们不是一个可任意替换的“误差补偿”：精确发射 P/Q 后仍用旧 tilt-only setter，误差约 `17.945mm`；再使用修正的锁轴投影但仍保留本地竖直速度，投掷壶已约 `0.045mm`、目标壶仍约 `1.186mm`；补上零竖直写入后两者才同落到 `0.05mm` 以下。这将投掷壶主分叉限定在角速度 native 写入，将目标壶剩余分叉限定在发射后前十余帧的竖直写入/落冰时序。终点响应非线性，不能把这些误差当作线性可加项。

**不可误用的验收边界**：不注入 A10 quaternion 时，同三个真实代码开关使12011为 `0.370/1.108mm`，较旧 `19.976/1.495mm` 明显收敛，但12枪投掷壶 RMSE `7.739 -> 17.521mm`，其中12008高旋 `9.523 -> 52.292mm`；即便每枪使用 A10 真值，并对齐高旋 reset 的角速度投影，该批 RMSE 仍为 `5.295mm`，12008仍差 `14.403mm`。所以这些新语义没有设为训练默认，不能把12011已闭合外推为全局Unity等价。本轮没有修改训练默认或发射物理参数。

### 12008 高旋退化的首个同输入分叉（后续补证）

补抓同一批第9枪（release serial 18）的1282条原生 setter，见 `unity_12008_dense_setter_bridge_20260929/`，同样复用21538条旧摩擦值。此前“新投影在高旋下本身不通用”的说法不成立：Unity 发射 reset setter 的脚本输入为 `[0,3.1400001049,0]`，native bridge 为 `[1.378452907e-12,3.1399991512,4.181176223e-7]`，使用 A10 姿态的新投影**逐分量复现**；旧 tilt-only 路径第一帧 X 约 `-4.095e-7`，明显不对。模拟器 `start_motioninfo` 原先在发射 reset 仍直接写 `[0,w,0]`，现已让 opt-in full-projection 模式在这一步也使用同一 native setter。

但这是**同一物理公式、不同浮点计算图**的问题。第2次滑行写入前，使用 A10 诊断姿态的本地与Unity getter `P/Q/v/w` 已逐分量相同；摩擦 noise 相同，recovered `Newfrictionstep` 得到的脚本 `wy=3.1206440925598145` 也相同。仅 native 锁轴 wrapper 的结果不同：Unity bridge `wy=3.1206445693969727`，本地简化的两次 `PxQuat::rotate` 投影给出 `3.120643138885498`，差 `-1.430511474609375e-6rad/s`。将**Unity 自己的**第2帧 pose 和脚本输入直接送进该 helper，差值仍存在，故这不是 A10 四元数重建、随机流、滑行算法或接触求解造成的第一分叉；它就在 native angular setter 的浮点运算次序/中间四元数组合内。

对同次1282步逐条套用 helper，完整 XYZ 只在1059步逐值吻合；高旋将剩余桥接 ULP 差积累到碰前姿态和终点。Unity `build.wasm.gz` 的实际 `func[73035]` 反汇编确认，其锁轴分支先通过两路原生姿态读取构造中间四元数，再以展开的 `f32.mul/add/sub` 次序做投影；当前 helper 直接对 `get_global_pose().q` 调代数化简后的 `PxQuat::rotate`，**不具备逐位等价的操作顺序**。因此通用的是锁轴投影的几何语义，不是现有 helper 的浮点实现。12008 的52.292mm/14.403mm退化不得作为“旧 tilt-only 更正确”的证据，也不得把简化 helper 提升为生产默认。后续精确修复需要按 `func[73035]` 的两个姿态源和 f32 运算次序重写 helper，不能按终点拟合补偿量。

复现与校验：

```powershell
& 'C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe' analysis_input/trace_12011_local_collision_tail.py --a10-all --production-alignment
& 'C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe' analysis_input/verify_12011_collision_causality.py
& 'C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe' -m unittest local_simulator.tests.test_strict_simulator
```

### 角速度 setter 的逐位修复与验收（更新）

已完成上段所说的源级修复。新增只读 getter 捕获 `unity_12008_two_pose_setter_20260929/` 证明：`func[73035]` 第一姿态源是 Unity 场景 Transform 的世界四元数，第二姿态源对这批冰壶是单位四元数；此前直接使用 PhysX body pose 不完全等价。首次 reset setter 和首次滑行 setter 使用原始发射四元数；之后 Unity 的 Transform 四元数等于 PhysX body 四元数按 float32 平方、求和、平方根、逐分量除法归一化。后续 1281/1281 次四元数全分量逐位相同，前两次不归一化。

`local_simulator/unity_physx.py` 的 opt-in full-projection 路径现按 `func[73035]` 的 float32 加减乘法次序计算 `q^-1.rotate -> 锁X/Z -> q.rotate`，并按上述同步规则选取姿态。将 Unity 捕获的 Transform 四元数和脚本角速度送入该函数，高旋样例 1283/1283 次 XYZ 桥接角速度逐位相同；用本地重建 Transform 源同样 1283/1283 次相同。旧的 12011 密集捕获用相同规则复核 911/911 次相同。`local_simulator/tests/test_strict_simulator.py` 固化了高旋 ULP 案例与同步规则。

完整轨迹不能由此宣称等价：A10 真值+生产对齐开关下，12枪投掷壶 RMSE 由修前 `5.295mm` 降至 `4.724mm`；12008 终点误差由 `14.403mm` 降至 `13.058mm`，12011 为 `0.0475mm`。剩余高旋误差发生在整体状态传播/碰撞链路中，**不是**这次已逐位验收的锁轴投影算法。该模式仍未设为训练默认。

可复测：`C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe analysis_input/verify_unity_angular_setter_projection.py`。

**求解器默认更新**：本地 `local_simulator/unity_physx.py` 已将精确投影改为默认，旧 tilt-only 仅可显式指定；`StrictCurlingEnd` 的无目标出手也已禁止在精确模式下误入仍使用旧 setter 的原生快循环。上段“仍未设为训练默认”是修复中途的历史状态，不再适用于当前主目录的逆向求解器；独立交付包未修改。本机单次无目标高旋出手：精确 Python/PhysX 路径约 `0.366s`，旧原生路径约 `0.072s`。

### 当前残差分层（同一12枪、记录的重置yaw与摩擦流）

新 `trace_12011_local_collision_tail.py --exact-setter-only --trace-sample-id 12000` 隔离“只修角速度”效果：投掷壶9个可比终点 RMSE `3.804mm`、目标壶12个 RMSE `2.472mm`。12008为`0.805/0.174mm`，12009为`3.830/0.198mm`，12010为`5.182/8.288mm`，12011为`9.289/1.275mm`。此配置并未修发射高度/竖直setter，也未注入A10完整native四元数。

`--production-alignment --trace-sample-id 12000` 同时打开精确投影、Unity发射位置/高度和零竖直setter（无A10完整四元数注入）：投掷壶 RMSE `4.870mm`、目标壶 `2.443mm`。12011收敛到`0.048/0.043mm`；但12008变为`13.058/0.325mm`，12010仍为`5.173/8.309mm`。因此不能仅以12011的闭合把发射/竖直两项立即提升为全局默认；12008的该回归和12010的碰撞残差需要同一轨迹的首次分叉证据。两组 RMSE 都是固定历史yaw与摩擦的校准对比，不是未知场景的盲测精度。

### BESTSHOT 发射写入顺序修正（随后核查）

Unity A12 的12008、12011首次角速度 setter 前 native `P.y=14.43239974975586`；旧 `start_bestshot` 却先让 `start_motioninfo` 在贴冰高度完成 setter 与 shape 激活，最后才抬高 `P.y`。现将 BESTSHOT 的 native release P 作为 `start_motioninfo` 的初始/重复 pose 写入，确保 setter 前已在发射高度；普通 MOTIONINFO 路径不变。真实 PyPhysX 12008 首 setter 前 P 精确为 `[-96.85420227050781,14.43239974975586,54.424400329589844]`，与 Unity A12 一致；16 项测试通过。

此顺序修正**不是**12008残差根因：同样无A10完整四元数注入的12枪回归，12008仍为`13.058/0.325mm`，12011仍为`0.048/0.043mm`。整批投掷壶 RMSE `4.870175 -> 4.869420mm`；仅12007终点有可见变化（active `0.413 -> 0.322mm`、target `1.131 -> 1.333mm`）。已证实的是首次setter的发射位置与写入先后，不是 Unity 的全部 SetActive/shape 内部顺序；不得用这次修正解释尚未定位的13mm误差。
