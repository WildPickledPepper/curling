# 未知项、训练优先级与工具链

记录非碰撞侧剩余未知、训练优先级、实用结论、逆向边界、模拟器修正和数据一致性检查。

> 原长文档已封存：[`UNITY_REVERSE_ENGINEERING.zh.2026-07-07.archive.md`](../archive/UNITY_REVERSE_ENGINEERING.zh.2026-07-07.archive.md)。以后维护以本目录子文档为准。

## 目前还不知道什么

逆向已经显著缩小未知范围，但还有几项没有完全恢复。

### 误差来源交底表

现在不应再把厘米级残差笼统说成“Unity 公式未知”。按证据拆开看：

```text
已确定，不应继续当未知：
  - teePosition：Start() 中明确取 GameObject.Find("Terminal").transform.position
  - release_x/release_y：来自 origin_postion 与 Terminal world position 的坐标差
  - BESTSHOT 主映射：velocity -> -protocol_vy，horizontal_offset -> protocol_x 偏移，rotation -> w
  - 固定步长：Unity fixed tick 为 0.01s，错误 dt=0.009/0.011 会退化到米级
  - 单 tick 顺序：FixedUpdate 先 Newfrictionstep/set_velocity，随后物理步用新速度推进位置
  - 干摩擦随机项形式：base + Random.Range(-0.0002, 0.0002)
  - AutoDCP seed 回放：recordedGame 写/读同一 section 的 RANDSEED
  - MOTIONINFO 触发：Midline trigger overlap，不是 Midline 中心线数学穿越

仍会造成残差的真实来源：
  - 普通 JSON 样本没有 RANDSEED，缺逐 tick Unity 随机摩擦序列
  - 只从 MOTIONINFO replay 时，缺出手到中线前已经消耗的 RNG 次数
  - MOTIONINFO 是 OnTriggerEnter/FixedUpdate 离散帧读数，有一帧级触发时刻误差
  - sweep window 公式已经恢复，但 socket `SWEEP` 命令到达 Unity 的帧延迟还需验证
  - 碰撞场景仍需要把 PhysX contact/solver 规则工程化后做金标准验证
```

`AutoDCP.HandleMessage` 的当前证据是：`recordedGame` 位于 `0x54`，wasm 里对应
`a[84]:ubyte`；`recordedGame == false` 时写 `BESTSHOT` 和 `RANDSEED`，
`recordedGame == true` 时读 `RANDSEED` 并 `Random.InitState(seed)`。`ReadTrace`
也已确认是每 32 个 float 一帧的历史轨迹流，可用于逐帧验证，但不是正式动作输入。

### 1. 每个 kernel 的干净生产级代数实现

`fsimp` dispatch table 和 `Newfrictionstep` 汇编逻辑已经恢复到公式层，并翻译成了独立 Python 原型。`tests/test_recovered_curling_motion.py`
现在还用官方 no-sweep 样本锁住 `MOTIONINFO` 尾段 replay：`dt=0.010`
约 3-4cm，`dt=0.009/0.011` 为米级错误。因此剩余缺口不是尾段坐标符号或 timestep，
而是更快、经过审计的生产实现，可能用 C++/NumPy/Numba，供训练 rollout 使用。
这里的“慢”是工程问题：精确原型每个 `0.001s` 摩擦步会调用多个自适应 Simpson
积分，一条尾段常有上千步；再套一层摩擦参数搜索时，`--limit 1 --iterations 6`
也会到十秒量级。尝试把整个大分支 Python 函数直接交给 Numba JIT，首次编译开销超过
反向探针可接受范围；手写纯 Python scalar 版本也没有实测变快，因此已撤掉该实验。
后续如果要把精确公式放进训练内循环，应该走 C++/Rust 扩展、分 kernel 编译，或者把它作为
teacher 生成校准表/蒸馏数据，而不是直接用现在的可读 Python 原型硬跑大规模 rollout。
`fsimp` 自适应 Simpson 的循环规则也已经钉住：wasm 中没有固定迭代上限，按
`abs(S_new - S_prev) < eps` 停止；Python 原型里的 24 次上限只是本地防挂保护。
需要强调：`dt=0.009/0.011` 的米级误差是反证测试，证明错误 timestep 不可接受；
不是我们容忍正确 replay 有米级误差。正确 `dt=0.010` 的厘米级残差继续用
`tools/reverse/probe_tail_residual_sources.py` 追踪。第一条 no-sweep 样本在平均摩擦下
误差约 `0.035264m`，给该样本拟合一个等效常数摩擦后降到 `0.010024m`，
说明普通采样缺少 `RANDSEED`/逐 tick friction noise 是主要边界之一。要达到 bit-level
一致，需要采集或读取 AutoDCP `RANDSEED`，并用 recovered Unity RNG 逐 tick replay。
当前工作区和单机版目录里没有发现现成 AutoDCP record/ini 录像文件；已有
`no_sweep_200.jsonl` / `sweep_200.jsonl` 主要是 endpoint 校准数据，不含可复现 seed。
`tools/reverse/probe_tail_residual_sources.py` 已经接入 `--unity-seed`、`--rng-skip`
和 `--sweeping`，因此拿到 AutoDCP record 后，可以直接把 `RANDSEED` 接进尾段验证。
尚未完全消掉的未知是：如果只从中线 `MOTIONINFO` 开始 replay，需要知道出手到中线期间
已经消耗了多少次 `Random.Range(-0.0002, 0.0002)`；整段从 `BESTSHOT` 开始 replay
则不需要跳过。
本轮又补了 `tools/reverse/replay_bestshot_seeded.py` 和
`tools/reverse/probe_bestshot_release_constants.py`：前者从正式 `BESTSHOT` 映射生成协议初态，
后者用 no-sweep `MOTIONINFO` 样本检查几何常数。现在 `Start()` 赋值链已经确认：

```text
origin_postion = mBlueBalls[0].transform.position
terminal       = GameObject.Find("Terminal")
teePosition    = terminal.transform.position

release_x ~= 2.3506
release_y ~= 32.4768
```

`MOTIONINFO` 触发点也不是 Midline 中心，而是 `CurlingStoneNew.OnTriggerEnter`
第一次进入名为 `Midline` 的 trigger box 时调用 `SendMotionInfo()`。因此几何阈值约为：

```text
midline_center_y ~= 21.3342
midline_trigger_y ~= 21.3342 + stone_radius(0.140875) + trigger_half_width(0.0735)
                  ~= 21.548575
```

用这些代码/资产几何默认值验证前 10 条 no-sweep 样本：

```text
state_rmse ~= 0.0947
pos_rmse   ~= 0.0202
```

小范围搜索可把位置 RMSE 降到约 `1.5cm`，但剩余误差不应再归因于
`teePosition` 未知；主要边界是普通采样缺少真实 `RANDSEED`、trigger 回调发生在
离散 fixed step 上，以及 velocity/angular velocity 对逐 tick 摩擦随机序列很敏感。

这很重要，因为 running-band 项里一个符号错误，在低旋转 shots 上可能看起来不明显，但在大 curl 和重扫冰 shots 上会放大。

### 2. 剩余 controller/回放/握手状态语义

重要的 Unity/协议轴映射已经从 `HandleHumanShot`、`SendMotionInfo`、`GetCurrentTrace` 中恢复：

```text
protocol_x  = teePosition.z - unity_position.z + 2.375
protocol_y  = teePosition.x - unity_position.x + 4.88
protocol_vx = -unity_velocity.z
protocol_vy = -unity_velocity.x
protocol_w  = unity_angularVelocity.y
```

metadata-use-to-string resolver 已经补上：`FastGame`、`AutoGame`、`HumanVsAI`、
`DCP`、`FastDCP`、`AutoDCP`、`DCP_HumanVSAI`、`Midline`、`Hogline2`、
`Stone`、`Wall` 这些关键对象名已经能从 wasm 里的 `d_[index]` 精确解析。

已经确认 `FastDCP + 212`、`AutoDCP + 240`、`DCP_HumanVSAI + 260`、`DCP + 232`
都指向各 controller 的 `movingCurling` 字段。全局 `OnTriggerEnter`/`OnCollisionEnter`
也已经查过：正式物理相关 trigger 基本集中在 `CurlingStoneNew` 与 `CrossLineEvent`，
`MotionTestStone` 是 level1 测试路径。

本轮已经补上 `UpdateState` 的 body 写回/出界清零逻辑、`GetScore` 的完整计分公式、
每壶结束状态机、`SendGameState` 主协议、`SendGoCommand` 行为，以及 AutoDCP 的
`BESTSHOT/RANDSEED/SWEEP/POSITION/SCORE/SETSTATE/TRACE` 记录格式。因此“计分边界”、
“扫冰/中线 trigger”、“每壶何时推进”、“AutoGame 如何复现随机种子”和 AutoDCP
默认 `Time.timeScale=16` 都已明确；剩余主要是 UI、网络握手、自动赛程外壳和少数 controller 状态标志。

### 3. 随机性控制

`FixedUpdate` 每个 Unity fixed tick（`0.01s`）都会给 friction 加：

```text
Random.Range(-0.0002, 0.0002)
```

现在已经恢复了该 WebGL build 的 `UnityEngine.Random` native 实现，并落成
`tools/reverse/recovered_unity_random.py`。`AutoDCP.HandleMessage` 支持用 `RANDSEED`
记录/恢复 Unity RNG；`DCP_HumanVSAI`、`DCP`、`FastDCP` 没看到统一 `Random.InitState`。
因此剩余未知已经缩小为：

```text
1. 普通比赛模式的 Unity 初始 RNG state 是否可从外部固定；
2. 普通比赛模式若不能固定初始 state，是否需要把每局初始 seed 作为隐变量估计；
3. 是否要把 recovered RNG 接进 fast_curling_env，还是只在 Unity 对齐验证时启用。
```

### 4. 多壶碰撞细节

详见 [`04_collision_physx.zh.md`](04_collision_physx.zh.md)，核心内容见 `12_physx_convex_cooking` / `04_collision_entry` / `05_physx_contact_generation` / `06_physx_solver`。

#### 2026-07-08 cooked hull 运行时抓取更新

`func72915/f_lvcd` 的运行时 hook 已成功，wasm table index 为 `122108`。
在四局制等待连接页面，即使没有 socket 连接、没有开始对局，进入场景后 Unity
也会创建若干 convex `MeshCollider` 并触发 PhysX cooking。本次稳定输出：

```text
log/unity_runtime_probe_20260708_225950/events.latest.json
data/calibration/unity_cooked_hulls_20260708_225950.json
```

关键结果：

```text
1_0/2_0/3_0/4_0:
  129 vertices / 254 polygons / 762 indices
  hash=0aac2338ce35d813

unnamed companion hull:
  99 vertices / 158 polygons / 510 indices
  hash=957070e591b9f7ce
```

但尺寸判据已经排除这批 hull 是正式比赛石壶：

```powershell
python tools\reverse\analyze_cooked_hull_identity.py
```

正式石壶期望 sorted extents 约 `(0.230000, 0.281750, 0.281750)`；本次最佳候选
`1_0/2_0/3_0/4_0` 为 `(0.083596, 0.159256, 0.159977)`，最大相对误差约 `0.637`。
所以当前结论应改为：hook/导出链路有效，但等待页不连接/不开局抓到的主要是
等待页/机器人/装饰相关 convex mesh；正式石壶 cooked hull 仍需单独导出或离线复刻。
短期不应把 `data/calibration/unity_cooked_hulls_20260708_225950.json` 直接接进碰撞训练。

formal stone 的离线状态已固化：

```powershell
python tools\reverse\summarize_formal_stone_cooking_status.py
```

输出：

```text
data/calibration/formal_stone_cooking_status_20260708.json
```

该报告确认：正式石壶 source mesh 是 `512` 个 unique vertices / `1020` triangles，
世界 sorted extents 为 `(0.230000, 0.281750, 0.281750)`，`512` 个 support-extreme
vertices 超过 `vertexLimit=255`，所以 Unity flags 下必走
`expandHullOBB -> convexHullCrop`。

2026-07-08 晚间已补齐构建链并重编 pyphysx：

```text
Visual Studio Community 2026 已有：cl 19.50、MSBuild 18
新增：scoop cmake 4.3.4、ninja 1.13.2
重编 wheel：D:\esp\tmp\curling_pyphysx\dist\pyphysx-0.2.5-cp38-cp38-win_amd64.whl
```

重编后的 binding 已暴露 `quantize_input/gpu_compatible`，并能跑 Unity flags：

```powershell
D:\esp\tmp\curling_pyphysx_conda\python.exe tools\reverse\dump_pyphysx_cooked_convex_hull.py `
  --output data\calibration\pyphysx_cooked_stone_hull_probe_unity_flags_rebuilt_raw_20260708.json `
  --include-binding-default-control `
  --include-raw-convex-data
```

结果为 `128 raw vertices / 66 convex polygons / 384 polygon indices / 252 rendered triangles`，
polygon 直方图为 `64:2, 4:64`，即两个 64 边 cap 加 64 个侧面四边形；
世界 radial mean 约 `0.140875m`；同时导出了 `PxConvexMesh.getMassInformation()`：
单位密度质量约 `9.801714`，local COM 近似 0，local inertia 对角主值约
`(7.089887, 7.645298, 7.089887)`。旧的非 raw 输出
`data/calibration/pyphysx_cooked_stone_hull_probe_unity_flags_rebuilt_20260708.json`
仍保留。
binding 默认 `qi1/gpu1` 控制组仍是 `64 unique vertices / 124 triangles`，只能当负对照。

同一 raw hull 的 contact topology 已由离线脚本重建：

```powershell
python tools\reverse\analyze_pyphysx_raw_hull_topology.py
```

输出：

```text
data/calibration/pyphysx_raw_hull_topology_20260708.json
V=128, F=66, E=192, V-E+F=2
edge classes = top_ring:64, bottom_ring:64, vertical:64
facesByEdges8 complete = true
facesByVertices8 complete = true
vertex face valency = 3 for all vertices
world radius - side apothem ~= 0.000169705m
```

所以 256 面石壶被 cooked 成 64 面棱柱这件事本身已经可离线复刻；
64 面离散化带来的顶点半径/侧面 apothem 差只有 `0.17mm`，不能解释厘米级碰撞误差。

2026-07-09 又把 `BigConvexData` 的 `VALE/GAUS` 离线复刻：

```powershell
python tools\reverse\analyze_pyphysx_bigconvex_data.py
```

输出：

```text
data/calibration/pyphysx_bigconvex_data_20260709.json
VALE: nbVerts=128, nbAdjVerts=384, valency_hist={3:128}
GAUS: subdiv=16, nbSamples=1536, sampleBytes=3072
brute-force support validation errors = 0
```

因为 `128 > gaussMapLimit=32`，正式离线 hull 必然需要 BigConvexData。现在
`VALE/GAUS` 的算法内容已经能按 PhysX 4.1 源码重建；剩余不是“不知道 support
数据怎么计算”，而是 Unity formal stone 的 `CVXM/SUPM/GAUS/VALE` stream
字节顺序是否与本地复刻完全一致。

把 rebuilt Unity flags 接进既有 unique-role 碰撞 probe 后，旧补偿几何
`radius=0.146, center_height=0.1276` 的 target RMSE 约 `11.32cm`；formal
`radius=0.140875, center_height=0.115` 即使把 handoff threshold 对齐到
`0.292m`，target RMSE 仍约 `12.08cm`。因此当前缺口不再是 pyphysx 不能跑
Unity flags，也不再是离线 `PxConvexMesh` 的 polygons/indices/topology/BigConvexData 完全拿不到；
而是 Unity runtime formal stone 的 shape scale/local pose/contact handoff、
runtime cooked stream 字节顺序是否与离线 PhysX 4.1 raw hull/BigConvexData 逐项一致。

#### 2026-07-08 碰撞对齐交底

本轮把 Unity collision 样本接到本地 CPU PhysX 4.1/`pyphysx` 后，已经排除和确认了一批
关键项：

```text
已确认：
  - Unity fixed timestep 必须用 0.01s；误用 0.001s 会把高速目标壶误差放大到几十厘米。
  - protocol 坐标必须先转换到 Unity 水平坐标系再进 PhysX。
  - pyphysx plane shape 默认 contactOffset=0.02，Unity PhysicsManager 是 0.01；
    探针已补为 0.01，但它不是最终大误差主因。
  - PhysicsManager: solverIterations=6，solverVelocityIterations=1，
    bounceThreshold=0.05，defaultContactOffset=0.01，maxDepenetrationVelocity=10。
  - scene flag `ENABLE_PCM` 和其它常见 scene flags 对当前 83 号高速样本几乎无影响。
  - center height、contact offset、frictionOffsetThreshold、maxDepenetrationVelocity、
    lock upright、半径小范围/大范围改动都不能把全样本压到 2cm。
  - 碰前 active dynamicFriction=0 不是主因：全样本 target RMSE 约 24.1cm，
    与默认 23.9cm 基本一致；active staticFriction 也置 0 反而会把 78 号干净正碰打坏到约 9cm。
  - 单一全局 restitution 也不成立；全局最佳仍约 20cm 级 target RMSE。
```

当前最重要的发现是：受控 collision 样本很可能携带了“跨样本 stone 状态历史”。
这个判断现在有可复跑报告：

```powershell
python tools\reverse\analyze_collision_sample_carryover.py
```

默认输出：

```text
data/calibration/unity_collision_state_carryover_report_20260708.json
```

证据链如下：

```text
1. reset 路径确认清 position、velocity、angularVelocity、mCollision；
2. reset 主路径附近未见 rotation reset；
3. controlled sampler 连续复用 target index：
   - target2: sample78 -> sample80 -> sample82
   - target3: sample79 -> sample81 -> sample83
4. 对所有复用 target 的样本，server_position_before_reset 里该 target 的二维位置仍是 0；
   因此二维位置看起来是被清干净的，问题更可能在 rotation/contact history/native contact stream 等二维外状态。
5. 默认 e=1/半径真实值下，target2 正碰误差随复用次数增大：
   sample78 target error = 0.649cm
   sample80 target error = 5.654cm
   sample82 target error = 17.585cm
6. sample83 是 target3 两次碰撞/清出界后的高速样本，默认目标误差 68.070cm；
   它可以被降低 restitution、改 convex vertexLimit 或改 yaw 部分补偿，
   但这些补偿会破坏其它样本，说明不是一个干净的全局物理常数。
7. restitution 细扫里即使允许每个样本挑自己的最佳 e，10 个 in-play target 里仍有
   9 个大于 2cm；全局最佳 target RMSE 仍约 21cm。
```

补充扫了一遍 `build.data.gz`/`build.wasm.gz` 字符串：能找到
`RESETPOSITION`、`RESETSTATE`、`BESTSHOT`、`MOTIONINFO`、`SWEEP`，
但没有找到 `RESETROT`、`SETROT`、`ROTATION` 这类 socket/debug 命令。
所以目前不能指望已有协议显式清 rotation；fresh page 或注入新 debug 入口更现实。

所以目前不能把 `unity_controlled_samples_20260707.jsonl` 里的碰撞样本直接当作“每条都应
2cm 对齐”的金标准。它们适合暴露误差来源，但不适合作为最终碰撞标定集。下一轮采样应至少满足：

```text
必须项：
  - 每个 collision 场景 fresh scene / fresh page，或显式 reset rotation；
  - 每次只跑一个 collision case，避免 target stone 继承上一 case 的姿态/材质历史；
  - 记录 active/target 的三维 rotation、velocity、angularVelocity，至少在碰撞前后各一次；
  - 对 y5.2/y6.2/y8、v3.4/v4.0、左右擦碰分别重复 3-5 次，用于区分随机摩擦和系统误差。

最好项：
  - 如果能拿到 AutoDCP RANDSEED/save，记录出手到碰撞前 RNG 消耗；
  - 如果协议无法回传 rotation，则用 fresh scene 保证初始 rotation 可由 prefab 决定；
  - 对 wall/cleared 样本单独建模，不混入 in-play endpoint RMSE。
```

在当前证据下，碰撞侧还差的不是“PhysX 公式完全未知”，而是“Unity 运行时接触状态的初始条件
没有被采样完整”。这也是为什么局部参数能把某个样本调到 2cm，但全局会立刻破坏其它样本。

#### 2026-07-08 追加：unique-target / unique-role 离线诊断

随后补了两组更干净的 socket 样本，但当前阶段不再主动拉起 Unity 继续采样：

```text
unique-target:
  data/calibration/unity_unique_target_collision_samples_20260708.jsonl
  3 批 x 12 条；每批 target index 不复用。

unique-role:
  data/calibration/unity_unique_role_collision_samples_20260708_r00.jsonl
  8 条；active index 和 target index 都不复用。
```

这两组样本把前一轮“目标壶复用污染”的猜测进一步拆开：

```text
unique-target:
  same_session_target_reuse_detected = false
  same_session_active_reuse_detected = true
  默认 PhysX probe target RMSE 约 17.2cm。

unique-role:
  same_session_target_reuse_detected = false
  same_session_active_reuse_detected = false
  默认 PhysX probe target RMSE 约 13.2cm。
```

因此，active/target 复用不是唯一主因；即使完全不复用壶编号，当前本地 PhysX 复现仍达不到
2cm。新的 `probe_physx_collision_alignment.py` 已加入这些诊断参数：

```text
--inertia-model solid-cylinder/thin-shell/pyphysx-default/custom
--inertia-radial / --inertia-vertical
--handoff-friction
--handoff-v-scale
--handoff-x-offset / --handoff-y-offset
--stone-faces
--angular-sign
```

已排除或弱化的项：

```text
1. Rigidbody mass 只 set_mass 不设 inertia tensor 是代码缺口；
   但补 solid-cylinder/thin-shell 惯量后只改善毫米级，不是 10cm 主因。
2. handoff_friction 在 0.0008..0.0012 扫描，全局最佳仍是 0.001。
3. handoff_v_scale 在 0.94..1.06 扫描，全局最佳仍是 1.0。
4. handoff_extra 与毫米级 y-offset 的刷新小网格最佳为 `+5mm/-5mm`，
   只能把 target RMSE 从约 `11.32cm` 降到 `10.27cm`，不是 2cm 解。
5. center_height 从 0.115 扫到 0.135，只带来毫米级变化。
6. stop threshold 从近似完全静止到 0.05m/s 早停，终点几乎不变。
7. Ice friction 最佳仍是 0.02；combine mode 明确是 Multiply，Average/Min/Max 会米级变差。
8. active/target/both 的 pre-collision material friction 置 0 会明显变差；
   unique-role target RMSE 约 20.8cm，不符合 Unity 当前样本。
9. scene flags（PCM、disable contact cache、stabilization 等）只带来毫米级变化。
10. 正式 stone 的 `ExtendedColliders3D.centre/rotation` 已确认全为 0；不同 stone index
   没发现局部 collider 偏移或尺寸差异。
11. 正式 stone 的 `collisionDetection=0`，CCD 不是比赛路径主因。
12. Plane world normal=(0,1,0)，冰面没有可解释该误差的倾斜。
13. protocol -> Unity frame 后 handoff angular velocity 保持正号更好；`--angular-sign=-1`
   没有改善。
14. `FreezeRotationX|FreezeRotationZ` 已按 z-up replay 映射到 PhysX `LOCK_ANGULAR_X/Y`；
   打开 `--lock-upright` 后 0.02s target 横向角速度归零，但 target RMSE 仍约 `11.37cm`。
   因此最终模拟器要保留锁轴，但它不是 10cm 主误差源。
15. `ExtendedColliders3D.Awake -> $f59928` 已确认只 Add/配置 MeshCollider 并 Destroy 脚本；
    它没有显式调用 Rigidbody mass/inertia/center-of-mass 相关 API。
16. `CurlingStoneNew.Start -> $f61028` 已确认会把正式石壶 `centerOfMass` 写成
    `Vector3.zero`，并把 `Rigidbody.constraints` 设为 `80`
    (`FreezeRotationX | FreezeRotationZ`)；因此碰撞模拟不应再按完全自由旋转刚体处理。
17. `tools/reverse/summarize_rigidbody_mass_writes.py` 三源交叉扫描确认：
    全局 `set_mass`、`set_inertiaTensor`、`set_inertiaTensorRotation` 和 Reset 命中集中在
    `RosSharp.Urdf.UrdfInertial.*` / `Car/base_link` 路径，不是正式比赛石壶路径；
    正式石壶只显式写 `centerOfMass=Vector3.zero`。
18. Rigidbody native 层已确认 `a[85]=m_ImplicitCom`、`a[100]=m_ImplicitTensor`
    （字段名来自 `func73082/73083/73084`）。`set_centerOfMass` 会把
    `m_ImplicitCom` 清 0，`ResetCenterOfMass` 会置 1；`set_inertiaTensor*`
    会把 `m_ImplicitTensor` 清 0，`ResetInertiaTensor` 会置 1。正式石壶资源里
    `m_ImplicitCom=true`、`m_ImplicitTensor=true`，`CurlingStoneNew.Start` 又把
    COM 显式锁为 zero，但没有关 `m_ImplicitTensor`。继续追 `MeshCollider`
    native vtable 后已确认：`set_sharedMesh/set_convex -> slot[37] func72951 ->
    convex 分支 func73283 -> f_abdd(e)`，因此 runtime rebuild 会调用
    `PxRigidBodyExt::setMassAndUpdateInertia`。world-scale formal hull 的最终
    tensor 已由 `analyze_pyphysx_scaled_mass_properties.py` 推出；剩余未知是
    Unity runtime 当时输入的 shape wrapper/local pose/scale 是否确实等于该候选。
```

当前最强的残余信号：

```text
1. 有效半径从 0.140875 提到约 0.146~0.155 会改善一部分，
   但 8 条 unique-role 的 target RMSE 仍约 10cm 级，36 条 unique-target 仍约 16.6cm。
2. 2026-07-09 的参数 oracle 横扫了已有 75 个 unique-role probe 文件、1697 组 result sets。
   如果每条样本都允许从已扫参数中偷偷挑一套最优参数，target-only oracle 的 RMSE
   也只是约 2.15cm，仍有 2/7 个 in-play target 大于 2cm；同时要求 active 和 target
   都对齐时，只有 3/7 条能双双进入 2cm。
3. 每条样本的 oracle 最优参数互相矛盾：有的要 radius=0.150/0.155/0.160，
   有的要 convex_vertex_limit=32，有的要 active_yaw=0.049087，有的要 handoff_v_scale=1.02。
   这不是一个全局 PhysX 常数没调好，而是样本级输入状态/contact manifold 缺项。
4. 单个全局参数组仍停在 10cm 级；刷新后的 current_best target RMSE 约 `11.32cm`。
   这说明不能把当前误差解释为“还差一个 friction/restitution/radius 标量”。
5. 使用 `stone_faces=128/256`、handoff x/y offset、center height、contactOffset 和 custom inertia
   组合搜索可以解释几毫米到约 1cm，但刷新后的可复现 current_best 仍是：
     active RMSE ~= 3.86cm
     target RMSE ~= 11.32cm
     combined RMSE ~= 8.23cm
   不能当作 2cm 解。
   后续 handoff_extra / y-offset 刷新小网格的最优 `+5mm/-5mm` 也只把 target RMSE
   降到约 `10.27cm`，进一步确认接触入口位置不是主缺口。
6. `Shape.set_local_pose()` 已接入 `probe_physx_collision_alignment.py`。
   共同 shape local x/y/z 偏移在 `{-5mm, 0, +5mm}` 的小网格只把 target RMSE
   从约 12.42cm 改到约 12.28cm；共同 shape local yaw 只到约 12.36cm。
   因此简单共同 local offset/yaw 不是主因，不能靠这个把误差压到 2cm。
7. 对最硬坏样本 `12003` 单独扫 `radius/handoff_x/y/vscale/active_yaw/target_yaw`
   共 729 组状态扰动，正常材质路径下 target 最好仍约 8.84cm；全局 oracle 里
   该样本最好 target 约 4.93cm，来自 `preactive0` 这类非正式材质路径。
   因此 12003 不是已有状态扰动轴能修的样本。
8. `OnCollisionEnter` 材质切换时序已参数化并跑 19 个候选：
   `dynamic=0/static=0.6` 与 baseline 等价；`dynamic/static=0` 且 post-step
   才切回会明显变差；never switch 会灾难性变差。加入这些候选后总 oracle 下限不变。
   因此 first-contact managed 材质时序不是 10cm 主误差源。
9. `analyze_collision_impulse_residual.py` 用 0.02s snapshot 反推早期 target 速度修正：
   current_best_refresh 下平均需要 `0.0366m/s` 的 delta_v（约 early target speed 的 `3.5%`），
   等效冲量平均约 `0.70 Ns`、最大约 `1.76 Ns`；但主导分量不是单一方向，
   7 条里 tangent 3、normal 3、mixed 1。最硬坏样本 `12003` 是 tangent 主导，
   需要约 `0.0919m/s` delta_v，其中切向 `0.0804m/s`、法向 `-0.0445m/s`。
10. `analyze_collision_impulse_feasibility.py` 把 target 等效冲量分解到 contact normal/tangent：
    7 条有效样本里 `friction_row_or_cache_suspect=3`、`normal_row_plausible=3`、
    `mixed_contact_manifold_suspect=1`；其中 4/7 即使用 `mu=0.60` 的宽松残差摩擦锥也在锥外。
    这说明误差已经分成 normal-row 与 friction/cache 两类，不能靠一个全局常数修掉。
11. `analyze_collision_local_impulse_trace.py` 对同一 current_best 本地 replay 加密到 0.01s：
    7/7 条有效样本的 target 主冲量都发生在 `0.00s-0.01s`，本地主冲量均值约 `19.31 Ns`；
    Unity 终点反推残差冲量均值约 `0.70 Ns`，也就是本地主冲量的 `3.5%`。
    Unity-implied normal scale 均值约 `0.983`，相对 1 的 RMSE 约 `0.033`；但有 1/7 条
    tangent 冲量翻符号。因此主碰撞 tick 和主法向冲量量级大体正确，剩余是首帧
    contact/solver row 的几个百分点误差，尤其是 tangent basis/friction anchor/cache。
12. `analyze_collision_tail_replay_oracle.py` 从本地 `0.02s/0.20s` snapshot 重建
    target-only pyphysx 尾段。baseline tail 能在 `3.06cm/2.29cm` RMSE 内复现本地完整 replay；
    如果只允许调 target 水平 `vx/vy`，有限差分 oracle 可把 Unity endpoint 压到
    `0.09cm/0.05cm` RMSE，且 7/7 都小于 `2cm`。因此尾段滑行不是主误差源；
    主缺口是首次碰撞后 target 拿到的水平线速度。`0.02s` 的 oracle delta-v 分量仍是
    normal 3 / tangent 3 / mixed 1，和前面的 row 级分类吻合。
13. `analyze_collision_solver_row_delta.py` 把 tail oracle 的速度修正投回首帧
    normal/tangent 冲量：endpoint 从 `11.32cm` 压到 `0.09cm` 只需平均改 `0.49 Ns`，
    约本地主碰撞冲量的 `2.35%`。分类为 normal-row 3、friction/contact/cache 2、
    tangent-sign-flip 1、mixed 1。最坏样本 `12003` 的本地 N/T 约 `24.27/-0.46 Ns`，
    Unity-implied 约 `23.82/+1.31 Ns`，切向直接翻符号。
14. `analyze_collision_row_correction_models.py` 检查全局 row 补丁是否能解决问题：
    per-sample oracle 可到 `0.09cm`，但最宽松的全局 `2x2` contact-frame 线性变换仍约
    `10.24cm`，7/7 超过 `2cm`；全局旋转、N/T scale、统一 scale+rotation 也都在
    `10cm-12cm`。因此不能靠一个统一 restitution/friction/法线角/冲量比例进 2cm。
15. `analyze_contact_frame_quantization.py` 把 row-delta 和 cooked hull 侧面法线对齐：
    formal cooked hull 是 64 边棱柱，side normal step `5.625deg`。`12003` 的本地冲量
    world angle 约 `-86.44deg`，贴近 side face `-87.19deg`；Unity-implied 冲量约
    `-82.18deg`，贴近相邻 side face `-81.56deg`。这把 `12003` 指向相邻 hull feature /
    contact manifold / friction anchor cache 选择差异。
16. `summarize_collision_feature_phase_audit.py` 已排查静态 hull/actor phase：
    共同 shape-local yaw 只能把 `12003` 拉到约 `20.41cm`，单样本 fine shape-local yaw
    最好约 `20.46cm`，active/target actor yaw `+/-11.25deg` 最好约 `20.43cm`，
    stone-faces sweep 最好约 `19.29cm`。因此 `12003` 的相邻侧面现象不是一个固定 yaw、
    简单 shape wrapper offset 或输入 face count 能修掉的静态几何问题。
17. `probe_physx_collision_alignment.py` 已新增 `--stone-geometry formal-recovered`，可直接把
    `ExtendedColliders3D` 恢复出的 512 顶点 formal mesh 送入 pyphysx cooking；
    `summarize_collision_stone_geometry_input_audit.py` 显示 current-best 尺度下 recovered mesh
    与旧 ring 点云 endpoint 完全相同，formal 尺度下也只改善约 `0.57cm` target RMSE，
    仍约 `12.08cm`。因此“没用 formal 512 顶点输入”不是 10cm 主因。
18. `summarize_collision_rotation_reset_audit.py` 保留了 reset rotation/yaw 线索：
    对 `12003` 做宽范围 active/target yaw 粗扫和局部细化后，target 最好可到 `1.75cm`，
    但 active 仍约 `6.88cm`；最佳 pair RMSE 约 `3.41cm`，没有 yaw pair 让双终点同时
    小于 `2cm`。全 unique-role 样本的 target-yaw-only per-sample oracle 仍为
    `5.37cm` target RMSE / `4.79cm` pair RMSE；`12004/12007` 双 yaw 粗扫也分别停在
    `4.47cm/5.57cm` pair RMSE。`summarize_stone_prefab_rotation_audit.py` 又确认资产里
    80 个正式 stone 只有一种 near-identity local rotation，max yaw 为 `0deg`，所以
    wide-yaw 不是 prefab 初始 yaw 差异；`--active-yaw-source integrated-precontact`
    把 BESTSHOT 到 handoff 的 deterministic active yaw 接进 probe 后，best target RMSE
    反而到 `16.30cm`，比 baseline `11.32cm` 更差，所以也不是简单漏掉累计自旋相位。
    它仍是重要 runtime-state/contact-feature 缺项，但不是单独闭环。
19. `summarize_collision_support_contact.py` 已排查重力/冰面支撑：Unity formal stone
    和 pyphysx 都使用重力；禁用 stone gravity 会让 target RMSE 到 `18m` 级，说明支撑 contact
    必须存在；把 center height 改为 `0.115` 可把 0.02s 竖直速度从 `-0.196m/s`
    消到近 0，但 target RMSE 仍约 `11.32cm`。新增 target/active pre-settle 网格后，
    `center_height=0.1276` 和 `0.115` 两组都是 no-settle 全局最优，`12003` 仍在 24cm
    级附近。因此垂直下落、冰面支撑 warm-start/cache 都不是 10cm 主因。
20. 从 probe snapshot 看，target 的最终位移方向基本延续 0.02s 碰后速度方向；
   坏样本不是后段滑行随机漂歪，而是碰撞最初几帧的 target 速度方向/大小已经不一致。
21. 这说明错误不像一个全局材质常数或 restitution 标量，更像 exact convex cooking/contact manifold、
   tangent basis/friction cache、normal row/separation bias、runtime mass properties 或样本级碰撞前隐藏状态差异。
22. rebuilt pyphysx 已打开 `PxSimulationEventCallback`，`probe_physx_collision_alignment.py`
   新增 `--enable-contact-report`，可保存 active-target 的本地 `ContactPairPoint` normal /
   separation / impulse。`unity_collision_contact_report_vs_row_delta_20260709.json` 显示：
   8 条 unique-role 的第一帧 active-target contact 都在 `0.01s`；`12003` 本地 contact report
   target 冲量角度为 `-87.19deg`，Unity-implied target 冲量角度为 `-82.21deg`，差
   `+4.98deg`，接近 64 边 cooked hull 的一个侧面步长。现在最强嫌疑已经压到
   Unity 首帧 contact manifold/feature/cache 或 solver row 实例。
23. handoff x/y 反事实进一步说明这不是全局坐标常数：`12003` 单样本宽网格中
   `handoff_x_offset=-0.02m, handoff_y_offset=0m` 可把 active/target endpoint error
   降到约 `1.93cm/3.16cm`，但全 unique-role 样本统一 `y=0` 扫 x 后，target RMSE
   最优仍是 `x=0m` 的 `11.32cm`；`x=-0.005m` 只改善 active，target 反而约 `11.50cm`。
   因此厘米级入口 pose 对 contact feature 很敏感，但不能当作一个统一偏移补丁；它仍指向
   样本级 first-contact native pose/manifold/cache 未证一致。
24. per-sample 入口状态 oracle：
   最新 `data/calibration/unity_collision_handoff_xy_oracle_20260709.json` 已纳入
   `12003` 的微小 `handoff_v_scale=1.005`、`12007` 的 diagnostic target reset offset，
   `12004/12006` 的 handoff x/y 细化，以及 `12005` 的 handoff angular velocity
   诊断。target RMSE 从 `11.32cm` 降到 `1.48cm`，active RMSE 降到 `1.35cm`，
   7 条 in-play target pair 全部双终点同时小于 `2cm`：
   `12000/12002/12003/12004/12005/12006/12007`。这说明入口 native state 重建确实是
   主源头；但它是 per-sample oracle，不是已经恢复出通用公式。
25. `12005` 的闭合方式很有指向性：
   入口 `vx/vy` 偏移粗网格和 active/target yaw 小网格都没有改善；但
   `handoff_w_offset=-0.44rad/s` 可把 active/target endpoint error 压到
   `1.77cm/1.37cm`。该偏移远大于样本可见 `motioninfo.w ~= 0.0037rad/s`，所以不能
   直接解释成“Unity 真的有一个简单管理层 w 公式没加”；它更像缺了 active-side
   angular/tangent native state，或 PhysX contact row / friction cache / manifold 中
   和角速度耦合的状态。同 pose 的 contact report 对照显示第一帧 contact time 仍是
   `0.01s`、contact count 仍是 4、normal 和 separation 不变；变化集中在 0.02s
   active/target 横向速度和 angular velocity，因此优先指向 tangent/angular row，
    不是 normal/contact-point 数量。全样本统一扫 `handoff_w_offset` 也不能闭合：
    全局最佳约 `-0.5rad/s`，target RMSE 仍约 `10.94cm`，7 条 in-play pair 超过 `2cm`。
    因此 `-0.44rad/s` 不是全局角速度常数。
26. 可见特征无法泛化 per-sample oracle：
   `tools/reverse/analyze_collision_oracle_generalization.py` 对入口状态 oracle 做了
   leave-one-out 验证。最好模型 `headon_linear` 的复跑结果仍是 active RMSE 约
   `5.22cm`、target RMSE 约 `30.98cm`，7 条 in-play pair 里 `0` 条双终点进 `2cm`。
   所以当前 2cm 结果只能读成 native-state proxy 证据，不能读成训练模拟器可用的
   通用碰撞公式。
```

这也回答了“PhysX 逆向已经很详细，为什么仍有大误差”：现在详细的是机制和外壳参数，
但还没有证明碰撞那一帧 Unity 喂给 native PhysX 的完整状态和本地 pyphysx 完全一致。
要证明“一模一样”，至少要逐项闭环：

```text
active/target:
  Transform position / rotation / localScale
  Rigidbody linearVelocity / angularVelocity
  Rigidbody mass / centerOfMass / inertiaTensor / inertiaTensorRotation
  Rigidbody constraints / drag / angularDrag / sleep state

shape:
  PxShape local pose / geometry scale / contactOffset / restOffset
  cooked convex mesh vertices / polygons / indices / GAUS / VALE byte order
  material pointer and combine mode at first contact solve

contact frame:
  contact tick number
  contact normal / points / separation
  normal impulse / friction impulse / solver warm-start/cache state
```

目前已证明的是 mass、COM、constraints、材质大方向、solver/dt、离线 cooked hull/topology/
BigConvexData/inertia 公式；尚未证明的是 runtime shape wrapper/local pose、formal
stone cooked stream 字节级一致性、首次 contact manifold/impulse，以及 reset 后三维
rotation/cache 是否完全一致。

下一步不应再靠“数据蒙参数”。每次只消一个未知项，必须给出证据来源；优先逆向/复现：

```text
1. Unity runtime convex MeshCollider cooking 后的实际 hull 顶点/face/scale；现在
   256 面双圈输入会超过 `vertexLimit=255`，且
   `tools/reverse/summarize_physx_cropped_hull_path.py` 已把
   `func72908 -> func72910 -> func72915` 的 wasm/PhysX 源码证据固化，
   因此 OBB cropped hull 路径不再是未知，剩余是 crop 后的精确输出；
2. `MeshCollider` rebuild 触发 inertia 重算已确认；继续查 cropped convex shape
   的精确顶点/面/plane/indices 与由它导出的 inertia tensor；
3. OnCollisionEnter 材质切换已经通过小网格弱化为非主因；若继续查，只应围绕
   native contact stream 是否已在材质改写前固定，而不是再做 endpoint 调参；
4. MOTIONINFO 到接触 tick 之间的 Random.Range 消耗和摩擦序列；
5. pyphysx rebuilt Unity-flags raw `PxConvexMesh`/BigConvexData 与 Unity WebGL runtime
   shape 封装之间的 scale/local pose、runtime cooked stream 顺序一致性、
   mass-property 差异；
6. 静态 shape yaw / actor yaw / stone-faces 已不能解释 `12003`，下一步若继续查几何，
   必须抓 runtime ContactBuffer 或 cooked stream 字段，而不是继续 endpoint 相位网格；
7. reset 路径未见 rotation reset；宽 yaw 可把 12003 target 降到 1.75cm，但不能双壶闭合，
   所以应优先抓 runtime Transform.rotation / Rigidbody.rotation，而不是只靠 POSITION；
8. unique-role 已避免 active/target 编号复用，
   但 reset 后三维姿态是否完全可控仍不是 socket POSITION 能证明的量。
```

已从 PhysX 4.1 源码和 wasm 字符串进一步确认的 cooking 边界：

```text
PxConvexMeshDesc 默认 vertexLimit=255，quantizedCount=255；
PxCookingParams 默认 convexMeshCookingType=eQUICKHULL；
areaTestEpsilon = 0.06 * scale.length^2；
planeTolerance = 0.0007；
meshPreprocessParams = 0，meshWeldTolerance = 0，gaussMapLimit = 32；
WebGL build.wasm 中能看到 QuickHullConvexHullLib / ConvexHullBuilder / Cooking::cookConvexMesh 字符串；
重编后的本地 pyphysx 可传 Unity flags，并已通过 `Shape.get_convex_mesh_data()`
导出离线 `PxConvexMesh` raw vertices/polygons/indices/mass；剩余不是本地 raw hull
无法导出，而是 Unity runtime formal stone 是否与该离线结果一致。
```

所以 cooking 不是完全黑箱；`func72915/f_lvcd` 的运行时 hook 已经把 Unity
实际 cook 出来的 `PxConvexMeshDesc.points/polygons/indices` 导出到：

```text
data/calibration/unity_cooked_hulls_20260708_225950.json
```

这一步确认了 hook/导出链路有效，但等待页导出的 `1_0/2_0/3_0/4_0`
和 `99 vertices / 158 polygons / 510 indices` companion hull 经尺寸判据排除，
不能视为正式石壶 collision hull。后续逆向不应再围绕 QuickHull flags 蒙参数，
而应专门恢复 `ExtendedColliders3D` formal stone 那次 runtime shape：要么抓到
formal stone 的 `func72915` desc 和 shape local pose/scale，要么用 rebuilt pyphysx
的 `128 vertices / 66 polygons / 384 indices` 结果作为离线对照，再解析
`func72927 / ConvexMeshBuilder::save()` 写出的 `CVXM/CLHL` stream 中的
byte-level vertexData/facesByEdges/facesByVertices、GAUS/SUPM/VALE 顺序和
mass/inertia 信息。

为降低人工成本，之前补过两套 no-sweep collision 采样计划：

```text
最干净：config/unity_fresh_collision_manifest_20260708.json
  - 36 个 one-shot plan，每发刷新页面。

优先实验：config/unity_unique_target_collision_batch_manifest_20260708.json
  - 3 个 batch plan，每页 12 发；
  - 同一 batch 内 target index 显式分配为 2..13，不复用目标壶。
```

当前这轮不再主动拉起 Unity 继续采样；已有 unique-target / unique-role 数据已经足够说明：
单纯避免 target/active 编号复用不能把误差降到 2cm。因此后续工作重心回到
convex cooking / runtime mass properties / contact solve 首帧细节，而不是继续扩大终点样本量。

2026-07-08 追加了一个运行时注入探针：

```text
tools/reverse/unity_webgl_runtime_probe.js
```

它的定位是“旁路取证”，不是改比赛逻辑。当前能记录：

```text
WebAssembly.instantiate / instantiateStreaming 捕获的 instance、memory、table；
createUnityInstance 的配置和返回对象；
WebSocket send/recv；
Emscripten FS 的 writeFile/readFile/mkdir/unlink/syncfs；
若 table index 和函数签名可用，可 opt-in 记录指定 wasm 函数入口参数。
```

这条路线最适合继续确认 `.save/RANDSEED/TRACE` 是否真的写入虚拟文件系统，以及在不改
Unity 物理的前提下抓运行时证据。它不能自动读出所有 C# 字段；函数级 hook 还需要逐个确认
wasm table index、签名和参数内存布局。

同时新增了统一验收脚本：

```powershell
python tools\reverse\summarize_collision_alignment.py `
  --samples <采样.jsonl> `
  --probe <probe_physx_collision_alignment 输出.json> `
  --output <summary.json>
```

旧样本基线输出 `data/calibration/unity_collision_alignment_summary_20260708.json`：

```text
full_in_play_pass_count = 1 / 10
failed_in_play_sample_ids = [80, 82, 83, 84, 85, 86, 87, 88, 89]
target_rmse_m = 0.239327...
same_session_target_reuse_detected = true
all_in_play_targets_within_threshold = false
```

这份报告就是下一轮 unique-target / fresh one-shot 的对照基线。


### 5. 协议入口状态位和异常分支

公共动作到 Unity 刚体释放的主路径已经恢复：

```text
BESTSHOT velocity horizontal_offset rotation
  -> Rigidbody.velocity = (velocity, 0, 0)
  -> Rigidbody.angularVelocity = (0, rotation, 0)
  -> Rigidbody.position.z -= horizontal_offset

SWEEP distance
  -> Sweep.isSweeping = true
  -> Sweep.sweepDistance = distance

POSITION x1 y1 ... x16 y16
  -> body_x = x - 2.375
  -> body_y = y - 4.88
```

正式 socket `BESTSHOT` 的速度异常下限也已经确认：`velocity < 0.0001` 时会被改成 `1.0`。
这不同于人类 UI 分支的 `0.0001` 下限。

剩余未知已经不是“动作参数怎么变成速度/角速度”，而是少量 controller 状态位和异常分支：

```text
1. READYOK/NAME/CONNECTNAME 的 UI 显示和联网等待细节；
2. RESETSTATE/RESETPOSITION 的外部平台重置细节；
3. AutoDCP 进程重启、文件复制和排名输出的完整自动赛程细节；
4. 如何进入 AutoDCP 记录入口：当前 WebGL BuildSettings 没有 `AutoGame`/`FastGame` scene，
   因此普通 UI 路径不会生成 `.save`。
```

这些分支会影响通信流程和回放，但不会改变已经恢复出的主出手物理入口。

### 6. 已恢复但仍需工程化实现的规则层

`GetStoneState`、`IsAllCurlingStoped`、`GetCurrentTrace`、`UpdateState` 和 `GetScore`
的核心公式已经恢复；`DCP/FastDCP/AutoDCP.Update` 的每壶结束状态机也已经恢复到主路径。
停止阈值、出界/失活清零、house 半径、局分计算、`SendGameState` 时机都可直接实现。
剩余不是公式未知，而是要把这些规则无歧义地落到本地训练环境里，并用 Unity 样本验证：

```text
1. DCP_HumanVSAI 的人类 UI 分支是否完全可以从训练环境里剥离；
2. AutoDCP 进程重启/文件复制/排名输出分支的完整自动赛程细节；
3. 当前 build 缺 AutoGame/FastGame scene 时，是否寻找另一份 build，还是注入/改造当前场景挂载 AutoDCP；
4. 本地训练是否需要完全复现 socket queue/timeout，还是只保留同步 step API。
```

## 训练角度的未知项优先级

对训练来说，未知项的重要性不同：

1. 最高优先级：第一阶段冻结 `SWEEP=0`，只把 no-sweep 单壶无碰撞 rollout 和 residual correction 做到 `2cm` 左右。
2. 最高优先级：把 `Newfrictionstep + fsimp` 精确翻译到足够可用的单壶无碰撞 rollout，实现以上恢复公式。
3. 高优先级：把已恢复的 `Update/SendGameState/SendGoCommand` 状态机落成本地训练规则层。
4. 高优先级：如果拿到包含 AutoGame scene 的 build 或成功注入 AutoDCP，利用 `.save` 里的
   `RANDSEED` 和已恢复 RNG 生成可复现实验；当前 build 普通 UI 不会直接产出该 record。
5. 中优先级：验证或近似 Unity PhysX 的石壶-石壶/石壶-冰面碰撞；若追求更高保真，把已恢复的 convex-convex 候选点生成、convex-mesh triangle SAT/deferred contact/cache/reduction，以及 `func70963` 的 normal/friction row 写入落成本地结构体。
6. 中优先级：把扫冰实现为“Midline/Hogline2 门控的低摩擦 stepping”，并包含逐步随机 friction；
   socket 对战还要考虑 `MOTIONINFO -> SWEEP` 消息延迟，AutoDCP `.save` 可验证无网络延迟版本。
7. 中优先级：继续恢复 UI/网络握手/自动赛程状态位，尤其是 READY/NAME/RESET/排名输出分支。
8. 低优先级：精确 UI、网络、计分显示、上传、人类输入细节。

## 2026-07-08 no-sweep 校正与训练取舍

扫冰可以放到最后做。第一版训练环境先固定 `SWEEP=0`，目标不是还原所有战术动作，而是先得到一个
可信的投壶模型：

```text
动作：BESTSHOT(v, h, w)
环境：单壶、无碰撞、无扫冰
验收：endpoint RMSE 约 2cm，并且不明显超过 Unity 重复采样的自然离散度
```

当前受控样本结果：

```text
BESTSHOT -> MOTIONINFO 位置 RMSE：约 0.0189m
MOTIONINFO -> endpoint no-sweep 原始 RMSE：约 0.0324m
no-sweep residual correction 后 in-sample RMSE：约 0.0211m
no-sweep residual correction 后 grouped-CV RMSE：约 0.0230m
重复动作的 Unity endpoint 自然离散度：约 0.0216-0.0220m
```

这说明当前 no-sweep 误差已经基本碰到“普通 socket 无 `RANDSEED`”的随机下限。若要强行要求
每一发都 `<=2cm`，必须拿到 seed/逐 tick 随机摩擦序列；否则更合理的是用分布误差和交叉验证
作为准入线。

本轮新增的 no-sweep 工具：

```text
tools/reverse/infer_unity_sample_residuals.py
tools/reverse/fit_nosweep_residual_correction.py
tools/reverse/nosweep_residual_correction.py
tests/test_nosweep_residual_correction.py
config/unity_nosweep_residual_correction.controlled.json
```

历史 `no_sweep_200.jsonl` 仍可作为压力测试；它的尾段原始 RMSE 约 `0.0333m`，但噪声更宽，
不适合作为第一阶段严格验收门槛。第一阶段训练建议用受控 no-sweep 数据锁定模型，再用旧数据做外部 sanity check。

## 实用结论

Unity 模拟器不是不可知黑箱。关键运动模型已经可恢复到足以指导本地模拟器：

- 我们可以匹配 Unity 使用的精确常量。
- 我们可以复现同样的 `Newfrictionstep` 结构。
- 我们已经可以从 no-sweep 的协议 `MOTIONINFO` 尾段 replay 到 endpoint，使用平均干摩擦时 RMSE 约 3-4 cm。
- 受控 no-sweep 样本加入 residual correction 后，grouped-CV RMSE 约 `2.30cm`，已经接近无 `RANDSEED`
  条件下 Unity 重复采样的自然离散度。
- `BESTSHOT/SWEEP/POSITION/MOTIONINFO` 主协议入口已经从代码恢复，不需要靠数据蒙。
- 每壶结束、下一壶 `GO`、一局结束计分、`POSITION/SCORE/SETSTATE` 同步的主状态机已经恢复。
- AutoDCP 记录格式和 `RANDSEED` 回放方式已经恢复，可以作为可复现实验入口。
- 当前 WebGL BuildSettings 没有 `AutoGame`/`FastGame` scene；这解释了普通无限模式/四局对战采样没有
  `.save` 和 `RANDSEED`，不是 watcher 漏了路径。
- AutoGame 默认 `Time.timeScale=16` 已确认；这是自动赛程加速，不是新物理参数。
- `UnityEngine.Random.Range/InitState/get_value/get_seed` 的 native wasm 实现已经恢复，并已接入 recovered 物理原型。
- `MotionTestStone` 碰撞 helper 已确认是测试路径，正式碰撞仍是 Unity PhysX；石壶 `ExtendedColliders3D.generateVerticesAndTriangles` 的 cylinder mesh 已恢复：512 vertices、3060 indices、1020 triangles、上下 cap 中点交替 ear triangulation、`flipFaces=true`，正式场景 world radius 约 `0.140875m`；`Awake/generateMesh` 的 internal-call 已确认会设置 `Collider.enabled`、`MeshCollider.sharedMesh`、`MeshCollider.convex`、`Collider.isTrigger`、`Collider.material`，并在 mesh 生成后调用 `Mesh.RecalculateNormals`，但没有显式写 `MeshCollider.cookingOptions`。PhysX solver task 已定位到 `func71248/func71257/func71259/func71263/func71269/func71272/func71273`，contact manager 更新为 `func70739`，PCM narrowphase 表为 `4117968`，关键 shape contact 为 `func70574/func70576/func70577/func70030`；convex-convex/box-convex 的 face/edge SAT、reference/incident polygon 裁剪、face-vertex/vertex-face/edge-edge 候选点生成已经对到源码级规则；stone-rink 的 triangle face/poly face/active edge SAT、deferred contact、edge/vertex cache、patch 合并与 reduction 也已经对到源码级规则；`Plane` MeshCollider 的 `m_Convex=false`、`m_CookingOptions=30`、`m_Material=Ice`、`m_Mesh=unity default resources:10209` 已恢复。`ContactPoint/ContactBuffer` 的 64-byte/4112-byte 布局也已固定。contact finalization 表已定位到 `func71103/createFinalizeSolverContacts` 与 `func70963/createFinalizeSolverContacts4`，并确认 `frictionType=0` 走 PhysX `ePATCH` 分支。`func71103` 的 single-pair normal/friction constraint 已经对到 `SolverContactHeader`、`SolverContactPoint`、`SolverContactFriction` 和 `func71104/func71105/func71173` helper；`func70963` 的 4-wide block stream 顺序和 `SolverContactHeader4`、`SolverContactBatchPoint*4`、`SolverFrictionSharedData4`、`SolverContactFriction*4` 尺寸已经对到 PhysX；`func71035/func71036` 已对到 patch contact solver 的动态-动态/静态 body1 迭代冲量公式；`func70917/func70919` 已对到 4-wide block solver 的动态-动态/静态 body1 迭代冲量公式，`func70920/func70921` 是对应 conclude wrapper；另一路 `func71174/func71175/func71176` 已确认是 `Px1DConstraint` 通用行约束准备路径，不应再误当成石壶 contact point 主路径。
- 剩余难点是把 22 个 `fsimp` integrand、Simpson 积分器和已恢复 RNG 接入更快的生产 rollout 代码；碰撞侧则是把已恢复的 PhysX 接触/solver 规则工程化，并直接导出或重建 Plane 内置 mesh 的索引顺序与 convex cooking 后几何。2026-07-08/09 新增的 [`12_physx_convex_cooking.zh.md`](12_physx_convex_cooking.zh.md) 已经把石壶 256 面 runtime mesh、PhysX 4.1 QuickHull/OBB partial hull 分支、rebuilt pyphysx Unity-flags raw `PxConvexMesh` dump、192-edge contact topology 和 BigConvexData `VALE/GAUS` 记录下来；当前最重要的结构性未知是 Unity runtime stone shape 的 scale/local pose、runtime cooked stream 顺序与离线复刻是否一致、最终 inertia，而不是继续追加 socket 样本。

推荐下一步：

1. 保留 `tools/reverse/recovered_curling_motion.py` 作为参考模型，并把它移植成更快的训练实现。
2. 第一阶段训练固定 `SWEEP=0`，接入 `tools/reverse/nosweep_residual_correction.py` 的受控校正配置。
3. 直接实现已恢复的 `HandleMessage/Update/SendGameState` 和坐标变换公式，而不是从数据拟合 release 行为。
4. 解析剩余 controller 方法语义，重点是握手、重置、AutoDCP 自动赛程/排名输出分支。
5. 若能拿到包含 AutoGame scene 的 build，或通过注入让当前 build 进入 AutoDCP，则采集 `.save`
   record，用 `parse_autodcp_record.py` 抽 `RANDSEED`，再用
   `probe_tail_residual_sources.py --unity-seed --rng-skip` 验证尾段；若从 `BESTSHOT`
   整段 replay，则用 `replay_bestshot_seeded.py` 并把 `rng-skip` 固定为 `0`。
6. 在信任本地模拟器做战术 self-play 前，补充碰撞验证样本；必要时把已恢复的 PhysX convex-convex/convex-mesh 接触生成、`func70051` reduction 和 `func70963` 写出的 4-wide normal/friction rows 工程化实现，并锁死 Plane 内置 mesh 顶点。

## 当前逆向边界

稳定工具链为：

1. 对 `build.wasm` 和 `global-metadata.dat` 使用 Il2CppDumper。
2. 用 `script.json` 把 IL2CPP 方法映射到 dynCall method pointer ID。
3. 通过 wasm indirect function table 解析 dynCall ID。
4. 检查对应 WAT 函数。
5. 用 `tools/reverse/resolve_metadata_refs.py` 把 WABT 反编译里的 `f_xkb(address)` 和
   `d_[index]` 映射回字符串、类型和泛型方法。
6. 用 `tools/reverse/resolve_wasm_calls.py` 把 WABT 反编译里的调用别名，如 `f_kwjc`，
   映射回 `DCP_HumanVSAI.SendMotionInfo` 这类 IL2CPP 方法名。
7. 用 `tools/reverse/resolve_decompiled_string_refs.py` 把 WABT 反编译里的
   `f_vkb(309480)` 这类 wasm 线性内存字符串指针解析成
   `UnityEngine.MeshCollider::set_sharedMesh(UnityEngine.Mesh)` 等 internal-call 名称。
8. 用 `tools/reverse/list_decompiled_native_calls.py` 为 PhysX native wasm 函数列出
   `f_xxx -> funcNNNNN` 调用链，方便继续追非 IL2CPP 的低层 helper。
9. 用 `tools/reverse/inspect_unity_assets.py` 检查 Unity 资源里的 tag、PhysicsManager、
   Rigidbody、`ExtendedColliders3D` 动态 MeshCollider 参数，以及 Plane/Wall/Line
   collider 的 material、mesh PPtr、convex/cooking options；该工具也会递归计算
   Transform world matrix，用来核对 Plane/stone/wall 的真实世界位置和缩放。
10. 用 `tools/reverse/list_icall_registrations.py` 解析 `f_vvrd(name, functionPointer)`，
   把 Unity native internal-call 注册项映射到 wasm table function。
11. 用 `tools/reverse/find_decompiled_function_by_line.py` 从巨大 `build.dcmp` 行号反查所在
   wasm-decompile 函数，方便追 PhysX 字符串引用。
12. 用 `tools/reverse/recovered_unity_random.py` 本地复刻当前 WebGL build 的
    `UnityEngine.Random`。
13. 用 `tools/reverse/resolve_physx_task_metadata.py` 从 WAT data segment 读取 PhysX
    task metadata/vtable/function-table block，并把 table index 映射回 `funcNNNNN`。
14. 用 `tools/reverse/scan_wat_function_pointer_runs.py` 扫描 WAT data segment 中的
    连续 wasm function pointer，用来找静态函数表。
15. 用 `tools/reverse/find_physx_pcm_contact_table.py` 从 WAT 线性内存中扫描 PhysX
    7x7 contact method table，定位 `g_ContactMethodTable` 与 `g_PCMContactMethodTable`。
16. 用 NVIDIA PhysX 4.1 源码交叉定位 wasm 中的 `createFinalizeMethods`、
    `createFinalizeMethods4`、`createContactPatches`、`correlatePatches` 和
    `PxFrictionType` 枚举。
17. 用 `tools/reverse/find_physx_solver_vtables.py` 辅助扫描 PhysX solver vtable
    形状；本轮用它排查了 solver 表候选，并结合函数体确认 `func70937/70941/70942/70947`
    是 Coulomb/PF 支线，不是当前 patch friction 主路径。
18. 用 PhysX 4.1 的 `DySolverConstraintsBlock.cpp` 交叉确认
    `func70917/func70919/func70920/func70921`，把 4-wide patch contact block solver
    的动态/静态迭代公式和 conclude wrapper 对回 wasm。
19. 用 `tools/reverse/physx_contact4_layout.py` 生成 WebGL 32-bit 下
    `SolverContactHeader4`、`SolverContactBatchPoint*4`、`SolverFrictionSharedData4`
    和 `SolverContactFriction*4` 的 size/offset 表，避免后续手工数字段出错。
20. 用 `tools/reverse/physx_contact_buffer_layout.py` 生成 WebGL 32-bit 下
    `Gu::ContactPoint` 和 `Gu::ContactBuffer` 的 size/offset 表，确认 narrowphase
    写出的 contact 如何进入 contact finalization。
21. 用 `tools/reverse/recovered_extended_collider_mesh.py` 复原
    `ExtendedColliders3D.generateVerticesAndTriangles(...)` 的 cylinder mesh 生成规则，
    输出石壶 MeshCollider cooking 前的 vertices/triangles。
22. 用 `tools/reverse/dump_pyphysx_cooked_convex_hull.py` 从 rebuilt pyphysx 暴露的
    `Shape.get_convex_mesh_data()` 导出同一石壶 mesh 的 cooked convex hull raw 报告。
    当前输出
    `data/calibration/pyphysx_cooked_stone_hull_probe_unity_flags_rebuilt_raw_20260708.json`，
    证明 PhysX Unity-flags cooking 会把 512 顶点/1020 三角的 256 面石壶改写成
    `128` vertices / `66` polygons / `384` polygon indices / `252` rendered triangles，
    polygon 直方图为 `64:2, 4:64`，也就是离线 cooked hull 是 64 面棱柱；
    并给出单位密度 mass/inertia/local COM。它是离线 PhysX 4.1 raw hull 证据，
    但仍不等于 Unity runtime formal stone 的 shape scale/local pose 和 cooked stream
    内部块已经逐项匹配。
23. 用 `tools/reverse/analyze_pyphysx_raw_hull_topology.py` 把 raw hull 转成
    contact topology：`V=128, F=66, E=192`，`facesByEdges8[384]` 和
    `facesByVertices8[384]` 都完整，每个顶点邻接 3 个 face；top/bottom/vertical
    三类边各 64 条。输出
    `data/calibration/pyphysx_raw_hull_topology_20260708.json`。这说明离线拓扑层
    已经不是黑箱；剩余要验证的是 Unity formal stone `CLHL` 字节顺序、GAUS/VALE
    字节顺序和 shape 包装。
24. 用 `tools/reverse/analyze_pyphysx_bigconvex_data.py` 复刻 BigConvexData：
    `VALE` 为 `128` 个顶点、`384` 个 adjacent verts、所有顶点 valency 都是 `3`；
    `GAUS` 为 `subdiv=16`、`nbSamples=1536`、`3072` sample bytes，且所有
    sample 都通过 brute-force support 校验。输出
    `data/calibration/pyphysx_bigconvex_data_20260709.json`。这说明 support/hill-climbing
    数据的算法内容已经可复现；剩余只需 Unity formal stream 做字节级一致性证明。
25. 用 `tools/reverse/analyze_pyphysx_scaled_mass_properties.py` 把 raw cooked hull
    的单位密度 mass/inertia 按 PhysX 4.1 `scaleInertia` 和
    `setMassAndUpdateInertia(single mass)` 缩放到正式 Rigidbody mass=19.1。
    当前 world-scale formal hull 推荐接入 z-up probe 的惯量为
    `inertia_radial=0.178810612362`、`inertia_vertical=0.189222883199`，输出
    `data/calibration/pyphysx_scaled_mass_properties_20260709.json`。这说明惯量公式
    不再需要靠 endpoint 拟合；剩余是 Unity runtime shape wrapper 是否等于该输入。

本 build 里的 metadata slot 关系是：

```text
address = 3705984 + 4 * d_index
```

例子：

```powershell
$base = Join-Path $env:TEMP 'curling_reverse_il2cpp'
D:\anaconda3\python.exe tools\reverse\resolve_metadata_refs.py `
  (Join-Path $base 'il2cpp_out\script.json') `
  (Join-Path $base 'dcmp_funcs\func60752.dcmp') `
  (Join-Path $base 'dcmp_funcs\func61030.dcmp') `
  (Join-Path $base 'dcmp_funcs\func61031.dcmp')

D:\anaconda3\python.exe tools\reverse\resolve_wasm_calls.py `
  (Join-Path $base 'il2cpp_out\script.json') `
  (Join-Path $base 'wasm_table_map.json') `
  (Join-Path $base 'build.dcmp') `
  (Join-Path $base 'dcmp_funcs\func61031.dcmp')
```

Cpp2IL 能把这个项目作为 WebAssembly 解析，并找到相同的 code/metadata registration 地址，但它的 IL recovery 目前会在导入的 WebGL 函数上中止，例如 `env.SetIMEText` 没有关联函数体。这意味着我们可以可靠恢复名字、常量、结构体、函数映射和 WAT 级行为，但不能不经手工反编译或更重的 Ghidra 工作流就拿到整个物理类的干净 C# 伪代码。

`fsimp` 特别难干净反编译，因为它把很多 force kernel 内联进嵌套的 `br_table` switch 后面。它仍然能识别为 `Newfrictionstep` 使用的 Simpson 积分器，并且 `Newfrictionstep` 调用它时参数为：

```text
fsimp(0, PI / 2, 1e-5, param, type, i)
```

## 本轮对模拟器的修正

本轮发现并修复了一个具体 calibration bug：

- `sweep_200.jsonl` 把 sweep 存成 `requested_sweep_distance`。
- `tools/calibration/fit_unity_samples.py` 之前只读取 `requested_sweep`。
- 修复前，所有官方 sweep 样本都被归一化成 `sweep = 0`。

同时也收紧了 fast simulator，使 `unity_landing_v2` calibration 会检查 calibrated sweep range。否则，一个只在某个 sweep 范围拟合的 calibration 可能被静默用于支持范围之外。

新的拟合文件：

- `config/unity_physics_calibration.json`

它现在是 `fast_curling_env.py` 优先加载的第一个 calibration 文件。

## 数据一致性检查

用以下数据重新拟合 `config/unity_physics_calibration.json` 后：

- `data/calibration/no_sweep_200.jsonl`
- `data/calibration/sweep_200.jsonl`

对 390 条可用样本做确定性 landing replay，结果为：

| bucket | RMSE total |
| --- | ---: |
| all samples | `0.1164 m` |
| sweep `0` | `0.0406 m` |
| sweep `2` | `0.0384 m` |
| sweep `4` | `0.0396 m` |
| sweep `6` | `0.0462 m` |
| sweep `8` | `0.0565 m` |
| sweep `10` | `0.3087 m` |
| sweep `12` | `0.2682 m` |

总误差 90 分位数约为 `0.0946 m`，但有一个 high-sweep outlier 约 `1.55 m`。这说明：

- no-sweep 和中等 sweep 与修正后的模拟器一致；
- high sweep 不能被简单 endpoint polynomial 很好表示；
- 逆向模型解释了原因：sweep 改变的是有效摩擦，因此把 sweep 当成线性出手后位移在结构上是错的。
