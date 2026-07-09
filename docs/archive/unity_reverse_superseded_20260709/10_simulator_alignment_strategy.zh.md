# 模拟器对齐策略

这页回答一个核心工程问题：不能在一个结构性不准的本地模拟器上训练，那么下一步怎么把误差压下去。

## 结论

不要用“终点数据拟合版”当最终训练环境。最终训练模拟器必须分层验收：

```text
1. 单壶无碰撞运动：按 Unity 代码公式复现，必须先对齐。
2. 扫冰与随机摩擦：按 Midline/Hogline2 门控和 Unity RNG 复现；没有 seed 时验证分布，不验证单次轨迹。
3. 碰撞：单独攻 PhysX，不能混在终点拟合里糊过去。
4. 规则/状态机：按已恢复的 DCP/AutoDCP Update 和 SendGameState 实现。
```

训练时使用两个模拟器：

```text
reference simulator:
  直接翻译 wasm/IL2CPP 恢复公式，慢一点也可以，用作真值参考。

fast training simulator:
  为 RL/MCTS 加速，必须持续和 reference simulator + Unity 采样对齐。
```

只有 fast simulator 通过验收门槛后，才允许进入大规模 self-play。

## 2026-07-08：先冻结扫冰的训练结论

当前第一阶段可以完全不扫冰，训练动作空间先固定为：

```text
BESTSHOT(v, h, w)
SWEEP = 0
```

理由是 no-sweep 单壶无碰撞链路已经接近可训练标准，而 sweep 的 socket 生效时序仍会引入额外不确定性。受控样本上的当前结果：

```text
BESTSHOT -> MOTIONINFO 位置 RMSE：约 1.89 cm
MOTIONINFO -> endpoint no-sweep 原始 RMSE：约 3.24 cm
加入 no-sweep residual correction 后：
  in-sample RMSE：约 2.11 cm
  grouped-CV RMSE：约 2.30 cm
重复同一 BESTSHOT 的 Unity 自然离散度：约 2.16-2.20 cm
```

因此，在没有 `RANDSEED` 的普通 socket 样本里，严格要求每一次单发都小于 `2cm`
并不现实；Unity 自身随机摩擦已经给确定性点预测带来约 `2.2cm` 的下限。更合理的验收口径是：

```text
1. sweep=0；
2. 单壶、无碰撞；
3. 分布/交叉验证 RMSE 在 2cm 左右；
4. 对重复动作的预测误差不明显超过 Unity 自身随机离散度。
```

当前可直接使用的文件：

```text
tools/reverse/infer_unity_sample_residuals.py
tools/reverse/fit_nosweep_residual_correction.py
tools/reverse/nosweep_residual_correction.py
config/unity_nosweep_residual_correction.controlled.json
data/calibration/unity_nosweep_residual_correction_controlled_report.json
```

扫冰的增益确实存在：在受控直线样本里，`sweep=8/10/12` 会让同一出手大约多走
`0.9m-1.4m` 量级。但这个增益可以先由投壶参数本身覆盖一部分，而且扫冰当前误差主要来自
命令到达帧、Midline/Hogline2 门控和随机摩擦耦合。为了先得到一个可信训练环境，扫冰应放到
no-sweep 模型稳定之后再单独做。

## 为什么现在还有误差

当前误差来源不是“完全不知道 Unity 物理”，而是这些层还没全部闭环：

```text
1. 随机摩擦：
   Unity 每个 FixedUpdate 会抽 Random.Range(-0.0002, 0.0002)。
   没有 AutoDCP RANDSEED 时，单次轨迹无法 bit-level 对齐，只能对齐分布或从 seed 入口 replay。

2. 扫冰时序：
   普通 socket 模式里 AI 收到 MOTIONINFO 后再发 SWEEP，有网络/调度延迟；
   AutoDCP record 模式则在 Midline trigger 后从文件读 SWEEP，更适合验证无网络延迟版本。

3. release 和 trigger：
   BESTSHOT 到刚体初态、Midline/Hogline2 首次 overlap tick、stop 阈值都要逐项锁死。

4. 碰撞：
   正式石壶使用 Unity PhysX + 运行时生成 convex MeshCollider。
   我们已经恢复了大量 PhysX contact/solver 分支，并用 pyphysx 做了本地 baseline；
   当前大误差主要不能再简单归因于“公式未知”。旧 controlled collision 样本确实有复用风险，
   但 2026-07-08 的 unique-role 样本已经证明：active/target 都不复用时，本地 probe 仍有
   约 10cm 级 target RMSE。剩余重点是 exact convex cooking/contact manifold、初始 yaw/rotation、
   接触 tick/solver impulse 和 MOTIONINFO 后 RNG 摩擦序列；managed material timing 已由后续
   小网格弱化为非主因。

5. 当前 build 没有 AutoGame scene：
   代码里有 AutoDCP record，但本 WebGL BuildSettings 没打包 AutoGame/FastGame。
   因此普通 UI 不会直接给出 .save/RANDSEED/TRACE。
```

## 验收门槛

### A. 出手映射

目标：`BESTSHOT(v, h, w)` 到 Unity 刚体初态完全一致。

证据：

```text
BESTSHOT -> release body state
release body state -> Midline MOTIONINFO
```

做法：

```text
1. 用正式 socket no-sweep 样本覆盖 v/h/w 网格；
2. 本地 reference simulator 从 BESTSHOT 起跑；
3. 对比 Midline MOTIONINFO，不先看终点；
4. 若误差在中线前已经出现，优先修 release/坐标/trigger。
```

### B. 单壶无碰撞尾段

目标：从 `MOTIONINFO` 起跑到 `POSITION`，在无扫冰、无碰撞情况下对齐。

没有 `RANDSEED` 时不要要求单次 bit-level 一致；应重复同一动作采样，比较 Unity endpoint 分布和本地随机摩擦分布。
拿到 AutoDCP `.save` 后，使用 `RANDSEED` 从 `BESTSHOT` 整段 replay，`rng-skip=0`。

### C. 扫冰

目标：扫冰改变的是有效摩擦，不是终点线性偏移。

当前训练第一阶段先冻结 `SWEEP=0`。扫冰不进入 no-sweep 模型的验收门槛；后续需要时再作为
单独增强模块验证。

证据：

```text
same BESTSHOT + sweep distance grid
MOTIONINFO timing
Hogline2 前后 sweep 生效/失效边界
```

验收：

```text
1. sweep=0 先过；
2. sweep 小/中/大分别过；
3. high-sweep outlier 必须解释为时序/随机/边界问题，不能用多项式硬拟合。
```

### D. 碰撞

目标：把碰撞从“混合误差”里拆出来单独验证。

最小样本集：

```text
1. 静止目标壶，正碰；
2. 静止目标壶，偏心碰；
3. 双壶均运动；
4. 靠近 house/边界的碰撞；
5. 多壶连锁，但最后再做。
```

对比不只看终点，还要看碰后短时间的两壶速度/角速度/位置。否则终点误差会把摩擦和碰撞混在一起。
旧 `unity_controlled_samples_20260707.jsonl` 只适合定位误差来源；正式验收必须用
`config/unity_fresh_collision_manifest_20260708.json` 里的 one-shot fresh-page 样本，
并重新生成 fresh PhysX probe。

2026-07-08 之后的当前状态：

```text
不再主动拉起 Unity 采样；先用已有 unique-target / unique-role 数据做离线逆向。

已由资产/反编译确认：
  - 正式比赛石壶均为 ExtendedColliders3D 运行时生成的 256 面 convex MeshCollider；
  - ExtendedColliders3D.centre=(0,0,0)，rotation=(0,0,0)，不同正式 stone index 未发现碰撞体尺寸差异；
  - 正式比赛石壶 Rigidbody 序列化值: mass=19.1，drag=0，angularDrag=0.05，
    constraints=0，collisionDetection=0；序列化 inertiaTensor=(1,1,1)，inertiaRotation=identity；
  - `CurlingStoneNew.Start` 运行时会设置 `centerOfMass=Vector3.zero`，
    `Rigidbody.constraints=80`，即 `FreezeRotationX | FreezeRotationZ`，yaw 仍自由；
  - Ice/Bouncy 材质、PhysicsManager solver=6/1、fixed timestep=0.01s、contactOffset=0.01
    与前文资产结果一致；
  - Plane 是静态 MeshCollider / triangle mesh，不是 PxPlane；world normal=(0,1,0)，因此冰面没有倾斜。

已由 pyphysx 离线 probe 弱化：
  - combine mode = Multiply；
  - Ice friction = 0.02；
  - solver iterations = 6/1；
  - stop threshold、center height、contact offset、scene flags 不是 10cm 主因；
  - handoff angular velocity 在协议坐标映射后保持正号更好；翻符号没有改善；
  - handoff y-offset=-0.005m、custom inertia、center_height/contactOffset 联动只能把
    部分旧 unique-role 网格候选降到约 9cm-10cm，刷新后的可复现 current_best
    仍是 target RMSE 约 11.32cm，远不是 2cm 解；
  - handoff_extra 与毫米级 y-offset 刷新小网格的最佳为 `+5mm/-5mm`，target RMSE
    也只能从约 11.32cm 降到 10.27cm；
  - `FreezeRotationX|FreezeRotationZ` 已按 z-up 映射为 PhysX `LOCK_ANGULAR_X/Y` 复跑，
    0.02s 横向角速度确实归零，但 target RMSE 仍约 11.37cm；
  - handoff friction 常数与 handoff velocity scale 扫描不能解释误差；
  - pre-collision active material friction=0 会变差，不符合当前样本。

2026-07-08 runtime console 进一步提供了新的 handoff 证据：

```text
Unity 控制台会逐 tick 打印 b2Vec2 velocity。
对纯滑行壶，丢掉第一条速度后按 x/y += v * 0.01 积分，可把最终 POSITION 对到约 1mm。
对碰撞壶，Curling stop 前仍有明显残速，说明这里就是 Newfrictionstep 退出、转入 PhysX 的边界。
```

已落地工具：

```text
tools/reverse/analyze_unity_console_trajectory.py
tools/reverse/merge_console_handoff_into_samples.py
```

因此下一轮 controlled collision 采样不应再只保存 sampler JSONL；必须同时保存 runtime probe
`console.log`，再合并出显式 `handoff_state`。这样可以把“MOTIONINFO 到接触 tick 之间的
线速度/位置误差”从碰撞误差里剥离。

2026-07-08 18:10 又完成了一轮干净重连后的正常四局制采样：

```text
日志目录:
  log/unity_fourgame_20260708_1810/

输入:
  player1.out.log
  player2.out.log
  browser_console_slice.log

解析:
  console_trajectory_summary.json
  shot_count = 64
  纯滑行/自然停壶 = 10
  Curling stop 时仍有明显速度的 handoff = 54

派生保守碰撞样本:
  data/calibration/unity_fourgame_1810_console_collision_samples_replay_w_20260708.jsonl
  sample_count = 36

当前 best PhysX 参数复跑:
  data/calibration/unity_physx_fourgame_1810_console_replay_w_current_best_20260708.json
  active_rmse_m = 0.0387
  target_in_play_rmse_m = 0.1553
  combined_rmse_m = 0.0903
  target_cleared_count = 21 / 36
```

这轮不能直接作为参数定标集：它是正常四局对战，包含多体碰撞、清壶、可能的边界/二次接触，
而 `build_console_collision_samples.py` 只能从终局变化里抽“看起来像一目标”的保守样本。
但它的误差结构和 unique-role / unique-target 受控样本一致：显式 handoff 后，active 多数在
1cm-4cm，target 仍可到 10cm 级以上。新的证据继续指向 contact/cooked hull/首帧冲量，
而不是 release 到 Newfrictionstep 退出这一段滑行公式。

仍未过门槛：
  - 8 条 unique-role：刷新后 current_best target RMSE 仍约 11.32cm；
  - 36 条 unique-target：最佳 target RMSE 仍约 16.6cm；
  - 36 条四局制显式 handoff 派生样本：target in-play RMSE 约 15.5cm；
  - 目标是 in-play target 和 active endpoint 都进入 2cm 级，当前远未达到。

2026-07-09 的离线参数 oracle 又补了一条关键证据：

```text
工具:
  tools/reverse/analyze_collision_parameter_oracle_floor.py

输入:
  已有 unique-role probe/grid JSON，共 75 个 probe 文件、1697 组 result sets。

结果:
  target-only per-sample oracle:
    RMSE ~= 0.02148m
    over_2cm = 2 / 7

  active+target pair oracle:
    pair RMSE floor ~= 0.02206m
    pair over_2cm = 3 / 7
    active 和 target 都分别小于 2cm = 3 / 7

  全局同一参数最好:
    target_in_play_RMSE 仍约 9.28cm
```

解释：如果每条样本都允许偷偷换一套互相矛盾的参数，endpoint 才能勉强接近 2cm；
但同一套全局参数解释不了全部碰撞。这说明当前大误差不是“PhysX 框架没逆向清楚”，
也不像单个 restitution/friction/radius 常数没调准，而是碰撞那一帧 Unity native PhysX
接收到的完整状态还没有和本地 pyphysx 证明一致。

2026-07-09 又把 `Shape.set_local_pose()` 接进
`tools/reverse/probe_physx_collision_alignment.py`，专门检查 shape wrapper/local pose
是否能作为统一解释：

```text
identity local pose + handoff_y=-0.005:
  target_in_play_RMSE ~= 12.42cm

shape local x/y/z in {-5mm, 0, +5mm}:
  best target_in_play_RMSE ~= 12.28cm

shape local yaw in {-0.049087, 0, +0.049087} rad:
  best target_in_play_RMSE ~= 12.36cm

加入这些结果后，oracle:
  target-only RMSE 仍为 2.1479cm，没有改善；
  active+target pair floor 只从约 2.280cm 小幅到 2.206cm。
```

所以“所有石壶共同存在一个简单 local offset/yaw”不是 10cm 主误差源；shape wrapper
仍要证明，但重点应转向 cooked stream/topology/contact manifold 或每壶/每次碰撞的
runtime rotation/cache，而不是继续扫共同 local pose。

同日又对最硬坏样本 `12003` 做了单样本 state perturbation oracle：

```text
样本:
  12003 collision_headon_y6p2_v4
  target 终点位移约 3.31m

网格:
  radius in {0.146, 0.150, 0.155}
  handoff_x/y_offset in {-5mm, 0, +5mm}
  handoff_v_scale in {0.98, 1.00, 1.02}
  active_yaw/target_yaw in {-0.049087, 0, +0.049087}

结果:
  正常材质路径下 target 最好仍约 8.84cm；
  全局 oracle 里 12003 的最好 target 约 4.93cm，来自 preactive0 这类非正式材质路径；
  加入这 729 组 result sets 后，总 oracle 下限没有变化。
```

这说明 `12003` 不是现有 handoff/yaw/radius 状态扰动可以救回来的样本。它更像首次
contact manifold / cooked stream / solver impulse 与 Unity native 不一致，而不是
终点摩擦或普通初态小偏移。

同日又专门把 `OnCollisionEnter` 材质改写时序参数化：

```text
新增参数:
  --material-switch-mode = pre-step-distance / post-step-distance / never

候选:
  baseline: first contact 使用 0.6/0.6
  dynamic=0, static=0.6，再按距离切回
  dynamic=0, static=0，再按距离切回
  never switch

结果:
  dynamic=0, static=0.6 与 baseline 完全等价；
  dynamic/static 都为 0 且 post-step 才切回会明显变差；
  never switch 会导致 active 或 target 误差灾难性增大；
  19 个材质时序候选最好仍是 baseline 等价路径，target RMSE 约 12.42cm；
  加入全部材质时序候选后，总 oracle 下限不变。
```

因此 first-contact 材质时序不是当前 10cm 误差的主解释。更合理的剩余方向是：
first contact manifold、cooked stream/contact topology、solver impulse/cache，而不是继续
在 managed `OnCollisionEnter` 的 0/0.6 时序上打转。

又用 `tools/reverse/analyze_collision_impulse_residual.py` 从 0.02s snapshot 反推了
Unity 终点所需的早期 target 速度/冲量修正：

```text
current_best_refresh:
  endpoint RMSE ~= 11.32cm
  required delta_v mean ~= 0.0366m/s
  required delta_v ~= early target speed 的 3.5%
  normal delta_v RMSE ~= 0.0328m/s
  tangent delta_v RMSE ~= 0.0324m/s
  mean equivalent impulse ~= 0.70 Ns
  max equivalent impulse ~= 1.76 Ns
  dominant components: tangent 3 / normal 3 / mixed 1

material_baseline:
  endpoint RMSE ~= 12.42cm
  required delta_v mean ~= 0.0452m/s
  dominant components: tangent 3 / normal 3 / mixed 1
```

最硬坏样本 `12003` 在 current_best_refresh 下：

```text
endpoint error ~= 24.57cm
required delta_v ~= 0.0919m/s ~= early target speed 的 7.23%
tail distance scale ~= 0.966
tail direction delta ~= +3.71 deg
normal delta_v ~= -0.0445m/s
tangent delta_v ~= +0.0804m/s
equivalent impulse ~= 1.76 Ns
  dominant component = tangent
```

这说明剩余误差不是一个 restitution 标量，也不是单纯法线冲量大小问题；切向冲量、
接触点、摩擦行、角速度耦合都有参与。下一步应围绕 Unity native contact manifold /
solver row 的实际输出，而不是继续 endpoint 参数搜索。

随后新增 `tools/reverse/analyze_collision_pair_impulse_residual.py`，把同样的 endpoint
反推扩展到 active/target 双方，检查误差是否像“缺了一个等大反向 pair impulse”：

```text
data/calibration/unity_collision_pair_impulse_residual_refresh_20260709.json

0.02s pair classification:
  pair_impulse_like = 0 / 7
  non_closing_pair  = 2 / 7
  pair_check_weak   = 5 / 7

target delta_v RMSE ~= 0.04612m/s
pair closure fraction mean ~= 0.762
```

这个结果要谨慎读：多数样本 active 在 0.02s 后很快停住，active tail 太短，用终点反推
active early velocity 会被放大，所以 pair 闭合不能当强证据。但 target 侧很稳定：
硬坏样本 `12003` 的 target required delta_v 从 `0.02s` 到 `0.2s` 只从
`0.09190m/s` 变到 `0.09474m/s`，方向修正约 `3.7deg -> 4.0deg`；`12004/12005/12007`
也呈同样稳定趋势。这说明 target 误差不是停壶尾段慢慢漂出来的，而是在碰后最早几帧
速度方向/大小已经错了。可疑层进一步收窄到首次 contact manifold / solver row /
contact cache，而不是 endpoint tail friction。

同日又新增 `tools/reverse/analyze_collision_early_velocity_sensitivity.py`，对
current_best_refresh 做 0.02s target early velocity 的有限差分敏感度。它检查一个全局
handoff 位置/速度偏差、target 位置偏差、active/target yaw、radius、contactOffset、
centerHeight 是否能解释早期速度缺口：

```text
data/calibration/unity_collision_early_velocity_sensitivity_refresh_20260709.json

baseline required delta RMSE per component ~= 0.03261m/s
unconstrained least-squares residual     ~= 0.02186m/s
plausible-clipped residual               ~= 0.03628m/s

unconstrained largest parameters:
  center_height ~= 213.93m      (plausible x21393)
  target_yaw    ~= 0.8497 rad   (plausible x17.0)
  active_yaw    ~= -0.7650 rad  (plausible x15.3)
  active_w      ~= +0.947 rad/s (plausible x9.47)
  radius        ~= +0.0282m     (plausible x2.82)
```

合理范围裁剪后不但没有改善，反而比 baseline 更差。因此“统一的初态小偏移/几何小偏移”
也基本排除；剩余更像 per-contact runtime state，包括 PCM contact points、friction
patch/cache、solver row 或 Unity runtime cooked stream 细节。

同日又新增 `tools/reverse/analyze_collision_impulse_feasibility.py`，把 target 早期
delta-v 换算成等效冲量，并分解到 contact normal / tangent。这个检查不是把残差当成
真实单次接触冲量，而是看“Unity 与本地 solve 的差值”更像哪类 solver row：

```text
data/calibration/unity_collision_impulse_feasibility_refresh_20260709.json

ok rows = 7
classification:
  friction_row_or_cache_suspect = 3
  normal_row_plausible          = 3
  mixed_contact_manifold_suspect= 1

residual cone:
  outside residual cone under mu=0.36 = 4 / 7
  outside residual cone under mu=0.60 = 4 / 7

normal sign:
  Unity needs more normal = 3
  Unity needs less normal = 4

impulse RMSE:
  normal ~= 0.627 Ns
  tangent ~= 0.619 Ns
```

逐样本看，`12003/12005/12002` 是切向主导，甚至用 `mu=0.60` 的宽松摩擦锥也解释不了；
它们更像 friction anchors/cache、tangent basis、contact point 或 patch friction row
不一致。`12004/12007/12006` 则是法向主导，更像 normal row、restitution、
separation bias 或 contact normal 不一致。`12000` 是 normal/tangent 混合。

这进一步说明：剩余误差不是一个全局摩擦系数、恢复系数、半径或 yaw 可以一次性修掉的。
要把 target RMSE 压到 2cm，必须拿到首次 stone-stone `ContactBuffer` 和
`SolverContactHeader/Point/Friction` 实例；否则只能在不同样本族之间互相牺牲。

随后补跑了同一 current_best 参数、但 snapshot 加密到每 `0.01s` 的本地 replay：

```text
data/calibration/unity_physx_collision_probe_unique_role_current_best_step_snapshots_20260709.json
data/calibration/unity_collision_local_impulse_trace_20260709.json

local main target impulse:
  main interval = 0.00s-0.01s, 7 / 7
  local target impulse mean ~= 19.31 Ns
  local target impulse RMSE ~= 19.81 Ns

Unity endpoint-inferred residual:
  required impulse mean ~= 0.70 Ns
  required impulse RMSE ~= 0.88 Ns
  residual / local main impulse mean ~= 3.5%
  Unity-implied normal scale mean ~= 0.983
  Unity-implied normal scale RMSE from 1 ~= 0.033
  Unity-implied tangent sign flip = 1 / 7
  same dominant axis = 3 / 7
```

这条证据把误差源又往下压了一层：本地 PhysX 的主碰撞 tick 是 `0.00s-0.01s`，
active/target 的水平动量变化几乎等大反向，说明“是否发生碰撞、碰撞帧、主法向冲量量级”
大体是对的。当前 10cm 终点误差来自首帧 `ContactBuffer/SolverContact` 里约 `1%-7%`
的 row 级差异。法向主导样本需要查 normal、separation bias、restitution 或 normal row；
切向主导样本需要查 contact point、tangent basis、friction anchors/cache 和 patch friction row。
其中 `12003` 最扎眼：本地 target tangent 冲量约 `-0.463 Ns`，Unity implied 约 `+1.073 Ns`，
直接翻符号；`12004/12007` 则主要像 normal row 比本地少约 `5.5%`。

随后又扫了 `frictionOffsetThreshold`，检查是否只是 friction anchors 的全局距离阈值没对齐：

```text
data/calibration/unity_physx_collision_probe_unique_role_current_best_friction_offset_refresh_20260709.json

frictionOffsetThreshold=0.001:
  target RMSE ~= 12.60cm
  12003 target error ~= 26.52cm

frictionOffsetThreshold=0.005/0.01/0.02/0.04/0.08/0.12:
  endpoint 完全相同
  target RMSE ~= 11.32cm
  12003 target error ~= 24.57cm
```

因此 `frictionOffsetThreshold` 不是当前缺失杠杆。剩余更像具体 contact manifold /
friction anchor/cache 实例或 solver row 字段不同，而不是一个全局阈值常数没扫到。

又新增 `tools/reverse/analyze_collision_tail_replay_oracle.py`，直接从本地 snapshot
重建 target-only pyphysx 尾段，验证误差是不是后续滑行造成的：

```text
data/calibration/unity_collision_tail_replay_oracle_002s_20260709.json

snapshot = 0.02s:
  baseline target-only tail vs local full replay RMSE ~= 3.06cm
  local full replay vs Unity RMSE ~= 11.32cm
  只改 target 水平 vx/vy 的 tail oracle vs Unity RMSE ~= 0.09cm
  oracle over 2cm = 0 / 7
  oracle 所需 delta-v RMSE ~= 0.0398m/s
  oracle delta-v 分量: normal 3 / tangent 3 / mixed 1

data/calibration/unity_collision_tail_replay_oracle_020s_20260709.json

snapshot = 0.20s:
  baseline target-only tail vs local full replay RMSE ~= 2.29cm
  local full replay vs Unity RMSE ~= 11.32cm
  只改 target 水平 vx/vy 的 tail oracle vs Unity RMSE ~= 0.05cm
  oracle over 2cm = 0 / 7
  oracle 所需 delta-v RMSE ~= 0.0397m/s
  oracle delta-v 分量: normal 3 / tangent 4
```

这条证据把尾段滑行降级为非主因：只要 target 在碰后早期拿到正确的水平线速度，
后面的 pyphysx 支撑/滑行已经能自然落到 Unity endpoint。剩余主缺口就是首次
stone-stone solve 输出给 target 的 `vx/vy`，也就是 `ContactBuffer`、contact point、
normal/tangent row、friction anchor/cache、solver impulse 这些行级状态。

把 tail oracle 需要的 `vx/vy` 修正投回首帧 contact normal/tangent frame 后：

```text
data/calibration/unity_collision_solver_row_delta_from_tail_oracle_20260709.json

endpoint before RMSE ~= 11.32cm
endpoint after tail-oracle RMSE ~= 0.09cm
平均需要改的 target 冲量 ~= 0.49 Ns
约为本地主碰撞冲量的 2.35%
implied normal scale mean ~= 0.992
impulse angle delta abs mean ~= 0.96 deg

分类:
  normal_row_magnitude_or_separation_bias = 3
  friction_row_contact_point_or_cache = 2
  tangent_sign_flip_contact_basis_or_cache = 1
  mixed_contact_manifold = 1

12003:
  local N/T ~= 24.27 / -0.46 Ns
  Unity-implied N/T ~= 23.82 / +1.31 Ns
  等效冲量方向需要转约 +4.25 deg

12004:
  local N/T ~= 20.17 / -0.41 Ns
  Unity-implied N/T ~= 19.60 / -0.11 Ns

12007:
  local N/T ~= 14.36 / -2.39 Ns
  Unity-implied N/T ~= 13.98 / -2.29 Ns
```

`0.20s` tail oracle 重跑出的 row-delta 也稳定：平均需要改 `0.50 Ns`，
约本地主冲量 `2.4%`，分类为 normal 3 / tangent 4。结论是：误差不是碰撞整体错位，
也不是尾段滑行；它是首次 contact solver row 的 2%-8% 小偏差，其中最坏样本属于
切向基/摩擦缓存/接触点方向错误。

随后用 `tools/reverse/analyze_collision_row_correction_models.py` 检查能否靠一个全局
row 修正补丁解决：

```text
data/calibration/unity_collision_row_correction_models_20260709.json

per_sample_oracle:
  endpoint RMSE ~= 0.09cm
  over 2cm = 0 / 7

global_full_2x2_linear:
  endpoint RMSE ~= 10.24cm
  over 2cm = 7 / 7

global_nt_scale_plus_rotation_term:
  endpoint RMSE ~= 10.59cm
  over 2cm = 7 / 7

global_uniform_scale_rotation:
  endpoint RMSE ~= 10.61cm
  over 2cm = 7 / 7

global_rotation_only:
  endpoint RMSE ~= 11.28cm
  over 2cm = 6 / 7
```

`0.20s` 版本也一样：per-sample oracle 约 `0.05cm`，但最宽松的全局
`2x2` contact-frame 线性变换仍约 `10.22cm`。这基本排除了“调一个统一的
restitution/friction/法线角/冲量比例”能进 2cm 的路线；缺口是样本级 contact
manifold/cache/solver row 实例，而不是一个全局标量。

又用 `tools/reverse/analyze_contact_frame_quantization.py` 把这些 row-delta 和 formal
cooked hull 的 64 边侧面法线对齐：

```text
data/calibration/unity_collision_contact_frame_quantization_20260709.json

formal cooked hull:
  side face count = 64
  side normal step = 5.625 deg
  half step = 2.8125 deg
  world radius - apothem ~= 0.17mm

整体:
  required angle delta abs mean ~= 0.96 deg
  required angle delta abs max ~= 4.25 deg
  implied impulse 到最近 side-face normal 的平均距离 ~= 1.10 deg

12003:
  center-line angle ~= -85.34 deg
  local impulse world angle ~= -86.44 deg
  nearest local side-face normal ~= -87.19 deg
  Unity-implied impulse world angle ~= -82.18 deg
  nearest implied side-face normal ~= -81.56 deg
  required angle delta ~= +4.25 deg ~= 0.76 个 side step
```

这把 `12003` 的性质又收紧了一步：本地冲量贴近一个侧面法线，Unity-implied 冲量贴近
相邻侧面法线。它不像材质常数或 restitution，而像 PCM manifold / contact feature /
friction anchor cache 在相邻 hull feature 间选了不同的一侧。

随后把 `probe_physx_collision_alignment.py` 扩展为可直接使用 recovered formal mesh：

```text
新增参数:
  --stone-geometry ring / formal-recovered
  --formal-stone-mesh D:\esp\tmp\curling_reverse_il2cpp\stone_extendedcollider_mesh_256.json

data/calibration/unity_collision_stone_geometry_input_audit_20260709.json

current-best inflated scale:
  ring target RMSE ~= 11.3233cm
  formal-recovered target RMSE ~= 11.3233cm
  delta = 0

formal physical scale + 0.292m handoff:
  ring target RMSE ~= 12.6463cm
  formal-recovered target RMSE ~= 12.0754cm
  improvement ~= 0.5710cm
```

解释：本地 probe 现在已经不是“没有把 512 顶点 formal mesh 送进 pyphysx cooking”。
在 current-best 尺度下，formal recovered mesh 和旧 ring 点云完全等价；在 formal 尺度下，
它只带来毫米级改善，仍远离 2cm。因此几何输入点云不是 10cm 主因，剩余应继续查
runtime cooked stream byte-level、shape wrapper/local pose、ContactBuffer 和 solver row。

为了确认这不是一个静态 hull 相位或 actor yaw 常数没设对，又做了只读本地 feature-phase
审计：

```text
data/calibration/unity_collision_feature_phase_audit_20260709.json

common shape-local yaw:
  best 12003 target error ~= 20.41cm
  global target RMSE ~= 12.36cm

12003 fine shape-local yaw:
  best target error ~= 20.46cm

12003 active/target actor yaw +/-11.25deg:
  best target error ~= 20.43cm

12003 stone-faces sweep:
  best target error ~= 19.29cm
```

所以 `12003` 的相邻侧面现象不是“统一旋转 hull/actor 一下”能解决的静态相位问题。
它仍然指向运行时 contact manifold、friction anchor/cache 或 solver row 实例差异。

不过 reset rotation/yaw 不能完全降级。又对 `12003` 做了宽范围 active/target yaw 粗扫和
局部细化：

```text
data/calibration/unity_collision_rotation_reset_audit_20260709.json

wide yaw result sets: 487
best target:
  active_yaw ~= -14.06 deg
  target_yaw ~= 104.06 deg
  target error ~= 1.75cm
  active error ~= 6.88cm

best pair:
  active_yaw ~= -19.69 deg
  target_yaw ~= 98.44 deg
  pair RMSE ~= 3.41cm
  active error ~= 4.35cm
  target error ~= 2.07cm

both endpoints <= 2cm: 0
pair RMSE <= 2cm: 0

target-yaw-only per-sample oracle over all unique-role samples:
  target RMSE ~= 5.37cm
  pair RMSE ~= 4.79cm
  target > 2cm: 12004, 12005, 12007

hard-sample dual-yaw coarse grids:
  12003 best pair RMSE ~= 3.41cm
  12004 best pair RMSE ~= 4.47cm
  12007 best pair RMSE ~= 5.57cm

serialized stone prefab rotation:
  data/calibration/unity_stone_prefab_rotation_audit_20260709.json
  formal stone count = 80
  unique local rotations = 1
  max serialized yaw = 0deg

deterministic active yaw integration:
  data/calibration/unity_collision_integrated_active_yaw_audit_20260709.json
  source = BESTSHOT -> observed MOTIONINFO -> handoff
  signs tested = +integrated, -integrated
  best integrated target RMSE ~= 16.30cm
  baseline target RMSE ~= 11.32cm
```

解释：大 yaw 是真实 contact-feature lever，能把 `12003` 的 target 从 `24.6cm` 拉到
`1.75cm`；但它不能让 active/target 双壶同时进 2cm。全样本 target-yaw-only oracle
和 `12004/12007` 双 yaw 粗扫也没有闭合。资产层 80 个正式 stone 的 serialized yaw
都是 0，所以它不是“不同 stone prefab 初始 yaw 不同”。因此 reset rotation/yaw 应继续作为
runtime-state/contact-feature 缺项追踪，但不能把它当成已经解决碰撞误差的单一答案。
把 recovered motion 从 BESTSHOT 积到 handoff 的 deterministic active yaw 接入后反而变差，
说明 wide-yaw 也不是简单漏掉 active 壶出手后的累计自旋相位。

同日又检查了重力/冰面支撑 contact：

```text
证据:
  Unity formal stone useGravity=true；
  Unity PhysicsManager gravity=(0,-9.81,0)；
  pyphysx Scene z gravity=-9.81。

current_best:
  0.02s physx z mean ~= 0.124657m
  0.02s physx vz mean ~= -0.1962m/s
  target RMSE ~= 11.32cm（current_best_refresh）

center_height=0.115:
  0.02s physx z mean ~= 0.115001m
  0.02s physx vz mean ~= -0.00001m/s
  target RMSE ~= 11.32cm

target/active pre-settle grid:
  center_height=0.1276: no-settle 仍是 global target RMSE 最优；12003 最好仍约 24cm。
  center_height=0.115: no-settle 仍是 global target RMSE 最优；12003 仍约 25cm。

disable_stone_gravity:
  target RMSE ~= 18.33m
```

解释：重力/冰面支撑是必须的；禁用会直接失真。但把垂直下落速度消掉并不能改善 target
endpoint，加入这些候选后 oracle 下限也不变。预先 settle target/active 来制造 stone-rink
支撑 warm-start/cache 也不能降低全局 target RMSE。因此 `0.02s` 的竖直下落/支撑状态和
冰面支撑缓存都不是 10cm 主误差源，剩余仍指向 stone-stone contact manifold / solver row。

仍不能靠猜的未知项：
  - Unity runtime convex MeshCollider cooking 后的实际 hull 顶点、face、margin 与 shape wrapper；
    当前已由输入几何和 `summarize_physx_cropped_hull_path.py` 的 wasm/PhysX 源码对照确认
    会走 OBB cropped hull；离线 pyphysx Unity-flags raw hull 已得到
    `128 vertices / 66 polygons / 384 polygon indices`，topology/BigConvexData/mass-inertia
    也已复刻，但还没证明 Unity formal runtime stream 与这份离线结果字节级一致；
  - 资源序列化 `m_ImplicitTensor=true`，且运行时 AddComponent<MeshCollider>() /
    `sharedMesh/convex` rebuild 已确认会触发 Rigidbody 重新计算惯量；world-scale formal
    hull 的推荐 probe 惯量已由 PhysX 公式推出为 radial=0.178810612362、
    vertical=0.189222883199，但 unique-role 定向 replay 仍为 target RMSE 约 12.65cm，
    剩余是 shape scale/local pose 是否确实等于该候选，以及 contact handoff/stream 顺序；
  - OnCollisionEnter 材质时序已做小网格：first-contact 完全 0 摩擦会变差，dynamic=0/static=0.6
    与 baseline 等价，不能解释 10cm 主误差；
  - 重力/冰面支撑已做小网格：禁用重力会米级失真；消掉 0.02s 竖直速度也不能改善 target RMSE；
  - target/active 支撑 pre-settle 已做小网格：no-settle 仍是最优，不能靠支撑 warm-start/cache 进 2cm；
  - 静态 feature-phase 已做小网格：shape-local yaw、actor yaw、shape-local xyz、stone-faces
    都不能把 `12003` 拉到 2cm；最好仍约 `19.29cm`；
  - formal mesh 输入已做 A/B：current-best 尺度下 recovered 512 顶点 formal mesh 与旧 ring
    点云 endpoint 完全相同；formal 尺度下只改善 `0.57cm` target RMSE，仍约 `12.08cm`；
  - 宽 reset-yaw 已做单样本网格：`12003` target 可到 `1.75cm`，但最佳 pair RMSE
    仍约 `3.41cm`；全样本 target-yaw-only oracle 仍约 `5.37cm` target RMSE，
    `12004/12007` 双 yaw 粗扫也停在 `4.47cm/5.57cm` pair RMSE，说明 rotation/yaw
    是重要缺项但不是单独闭环；资产层 80 个正式 stone 的 serialized yaw 都是 0，
    因此不是 prefab 初始 yaw 差异；deterministic BESTSHOT->handoff active-yaw 接入后
    target RMSE 反而到 `16.30cm`，也不是简单累计自旋相位；
  - MOTIONINFO 到接触 tick 间真实 RNG friction 序列和离散接触 tick；
  - PyPhysX 使用的 convex cooking 与 Unity WebGL 内置 PhysX cooking 是否完全同参。
  - 若走注入路线，还需要确认 wasm table index、函数签名和内存布局，才能稳定抓到指定函数参数。
  - PhysX 首次 contact manifold：接触点、法线、穿透/分离量、normal/friction impulse；
  - 目标壶碰后前几个 physics tick 的真实速度/角速度。当前终点误差显示，target 坏样本多半在
    首帧冲量方向/大小已经偏掉，而不是停壶尾段慢慢漂掉。
```

把这个缺口表述成验收条件，就是：

```text
必须证明 Unity 在首次 stone-stone contact solve 那一帧喂给 PhysX 的 native state，
与本地 pyphysx 构造的 state 在以下维度逐项一致：

1. active/target Transform position、rotation、scale；
2. active/target Rigidbody velocity、angularVelocity、mass、COM、inertia tensor、constraints；
3. PxShape local pose、geometry scale、contactOffset/restOffset、material；
4. cooked convex mesh stream，包括 vertices / polygons / indices / GAUS / VALE 顺序；
5. 首次 contact manifold 的 normal、contact points、separation 和 solver impulse。
```

现在只能证明其中一部分，不能宣称完整 native state 一致；这就是“文档里 PhysX 很详细”
但 endpoint 仍大误差的直接原因。

2026-07-09 又把这个证明题单独拆成字段级审计文档：

```text
docs/unity_reverse/13_physx_native_state_equivalence.zh.md
data/calibration/unity_physx_native_state_equivalence_audit_20260709.json
```

关键结论更明确：历史 current-best probe 用 `RigidStatic.create_plane` 代表冰面，而
Unity 正式冰面是静态 `MeshCollider` / triangle mesh；这一个字段足以否定“旧 probe
完整 native state 已经一模一样”。2026-07-09 已扩展 pyphysx binding，新增
`Shape.create_triangle_mesh_from_points`，并给 probe 加了
`--rink-geometry unity-plane-mesh`。A/B 结果为：

```text
data/calibration/unity_physx_collision_probe_unique_role_rink_mesh_currentbest_winding_20260709.json
active RMSE ~= 3.86cm
target RMSE ~= 12.83cm
```

也就是说，冰面 triangle mesh 严格性要保留，但它不是 10cm 主误差源。formal stone
runtime cooked stream、shape local pose/scale、contact manager cache、首个
ContactBuffer 和 solver impulses 仍没有运行时快照。所以下一步不是继续 endpoint
参数搜索，而是补 native-state 抓取，尤其是首次 stone-stone contact manifold / solver rows。
同一审计还接入了 handoff threshold / placement 刷新网格：接触入口调早 `5mm` 加
protocol-y `-5mm` 只把 target RMSE 改到约 `10.27cm`。这说明 Newfrictionstep 到 PhysX
入口边界有贡献，但它不是主缺口，也不能替代 ContactBuffer / SolverContact 实例抓取。
另外，Unity runtime 的 `FreezeRotationX|FreezeRotationZ` 已做对应本地复跑：
`--lock-upright` 后横滚/俯仰角速度归零，best target RMSE 仍约 `11.37cm`。所以最终
reference simulator 应保留锁轴，但继续压误差的主线仍是 stone-stone contact manifold、
friction anchors/cache 和 solver rows。

同日又把 rebuilt pyphysx 的 contact report 打开并接进 probe：

```text
data/calibration/unity_physx_collision_probe_unique_role_contact_report_current_best_20260709.json
data/calibration/unity_collision_contact_report_vs_row_delta_20260709.json
```

这一步给出了本地 PhysX 的真实 `ContactPairPoint`，不是 endpoint 反推。8 条 unique-role
样本的 active-target 第一帧 contact 都在 `0.01s`。最硬坏样本 `12003` 中，本地 contact
report 的 target 侧冲量角度为 `-87.19deg`，Unity endpoint 反推的等效 target 冲量角度为
`-82.21deg`，差 `+4.98deg`，接近 64 边 cooked hull 的一个侧面步长 `5.625deg`。
所以接下来要对齐的不是尾段滑行，而是 Unity 首帧 contact manifold / feature 选择 /
friction anchor-cache / solver row 实例。

同日又做了 handoff x/y 反事实。单看最硬坏样本 `12003`，把主动壶进入本地 PhysX
前的位置改成 `x=-2cm,y=0`，active/target endpoint error 可到约 `1.93cm/3.16cm`。
这说明碰撞入口 pose 的厘米级差异足以改变首帧 contact feature。但全 unique-role 样本
统一 `y=0`、扫 `x=-3cm..+3cm` 后，target RMSE 最优仍是 baseline `x=0m` 的
`11.32cm`；`x=-0.005m` 只改善 active RMSE，target RMSE 反而约 `11.50cm`。
所以它不是一个全局坐标偏置，而是继续指向每个碰撞实例的 native pose/contact
manifold/cache 是否和 Unity 一致。
把这条线扩成 per-sample handoff x/y oracle 后，target RMSE 从 `11.32cm` 降到
`1.48cm`，active RMSE 到 `1.35cm`。这个最新汇总不再只是 x/y：`12003` 需要
微小 `handoff_v_scale=1.005`，`12007` 需要 diagnostic target reset offset，
`12004/12006` 由 handoff x/y 闭合，`12005` 由 handoff angular velocity 诊断闭合。
7 条 in-play target pair 全部双终点同时小于 `2cm`：
`12000/12002/12003/12004/12005/12006/12007`。所以 reconstructed entrance native state
是真实大源头；但它还是 per-sample oracle，不是可直接泛化到训练环境的完整公式。
如果只看 active endpoint，入口状态 oracle 能让 8 条 active 全部小于 `2cm`，
active RMSE 约 `0.61cm`。这把误差来源进一步拆开：active 端主要是入口状态重建，
pair objective 需要额外的角速度/切向状态才能闭合。
`12005` 是关键证据：入口 `vx/vy` 偏移与 active/target yaw 小网格都没有改善；
`handoff_w_offset=-0.44rad/s` 可把 active/target 压到 `1.77cm/1.37cm`。这个量级远大于
可见的 `motioninfo.w ~= 0.0037rad/s`，所以它不是一个已经恢复的真实管理层公式，而是
指向 active-side angular/tangent native state 或 contact row / friction cache / manifold
中仍未对齐的状态。同 pose 的 `w=0` 与 `w=-0.44` contact report 中，第一帧 contact
time、contact count、normal、separation 都不变，0.02s 速度/角速度分配改变；因此这一步
更像 tangent/angular row 代理，不是 normal/contact point 数量变化。全样本统一扫
`handoff_w_offset` 不能闭合：最佳约 `-0.5rad/s`，target RMSE 仍约 `10.94cm`，
7 条 in-play pair 仍超过 `2cm`。所以训练模拟器不能简单加一个全局角速度常数；更合理的
路线是把它看作接触实例级 tangent/angular 状态缺口，后续用 contact/row 特征或局部校正建模。

为了检查这种 oracle 能不能直接变成训练公式，新增
`tools/reverse/analyze_collision_oracle_generalization.py` 做了 leave-one-out 泛化审计。
结果很差：当前最好模型 `headon_linear` 只用 `target_before_y/requested_v0` 预测入口修正，
复跑 pyphysx 后 active RMSE 约 `5.22cm`、target RMSE 约 `30.98cm`，7 条 in-play pair
里 `0` 条双终点小于 `2cm`。加入左右偏碰、approach normal/tangent 等可见特征也没有改善。
这条结果的含义很直接：per-sample oracle 证明“缺的是 native/contact 实例状态”，
但不能当作 fast training simulator 的通用修正层。训练前必须先走 native-state dump/replay
或拿到更大样本集做独立验证。

当前离线快照显示：target 的最终位移方向基本延续 0.02s 碰后速度方向，坏样本不是停壶后
“慢慢漂歪”，而是碰撞最初几帧传给 target 的速度方向/大小已经偏了几度或几个百分点。
这会在 3m-4m 滑行距离上放大成 10cm 级终点误差。因此下一步要继续挖 contact/cooking/首帧
冲量，而不是用终点残差硬拟合。

若先想降低人工刷新成本，可以先跑
`config/unity_unique_target_collision_batch_manifest_20260708.json`：每页 12 发，
target index 不复用，用来判断 target hidden state 是否就是主误差源。
验收统一看 `tools/reverse/summarize_collision_alignment.py` 输出的
`all_in_play_targets_within_threshold`、`failed_in_play_sample_ids` 和
`same_session_target_reuse_detected`，不要再人工挑几条 probe row 下结论。

### E. 规则状态机

目标：本地训练环境的 `GO/GAMESTATE/POSITION/SCORE/SETSTATE` 和 Unity 主路径一致。

规则错会让策略学错局面价值，即使物理单步很准也没用。

## 当前可执行路线

1. 先把 `recovered_curling_motion.py` 当 reference simulator，而不是直接把 fast env 当真值。
2. 对现有 no-collision 样本做分段误差报告：release -> Midline、Midline -> stop、stop -> POSITION。
3. 为同一 `BESTSHOT` 重复采样，估计 Unity 随机摩擦导致的自然方差，区分“不可 bit-match 的随机差”和“模拟器结构错”。
4. 第一阶段训练只开放 no-sweep 动作，用 `config/unity_nosweep_residual_correction.controlled.json`
   做 endpoint 残差校正，并用 grouped-CV 监控是否仍在 `2cm` 左右。
5. 尝试进入 `GameSceneDebug`：当前包打包了 Debug scene，主菜单按钮只是 inactive；可通过
   `SendMessage("SceneControl", "mLoadScence", "GameSceneDebug")` 或局部 patch 暴露按钮验证是否有额外调试输出。
6. 若要拿 AutoDCP `.save`，需要：
   - 找到包含 `Assets/Scenes/AutoGame.unity` 的 build；或
   - 注入/改造当前 build，让某个已打包 scene 挂上 AutoDCP；或
   - 放弃 `.save`，改用重复采样 + 已恢复 RNG 分布验证。
7. 运行时注入探针已落在 `tools/reverse/unity_webgl_runtime_probe.js`。它可先用于旁路记录
   WebSocket、Emscripten FS、WASM instance/memory/table；函数级 hook 等确认签名后再逐个启用。
8. 碰撞模块不要急着并入大规模训练；先跑 unique-target batch，若还不够再用 fresh-page
   小样本把 PhysX 接触/solver 工程化验证。

## 训练准入线

在以下条件前，不应把本地模拟器当最终训练环境：

```text
1. no-sweep/no-collision 在受控样本上达到 2cm 左右，并接近重复采样随机下限；
2. sweep 暂不作为第一阶段准入项；后续启用扫冰前再要求分布误差可解释；
3. 两壶碰撞样本至少覆盖 fresh-page 正碰/偏碰，并通过短时状态或 endpoint 2cm 验证；
4. 规则状态机和 Unity socket 日志一致；
5. fast simulator 对 reference simulator 有自动回归测试。
```

如果某一层还没过，训练仍然可以做，但只能作为预训练/候选策略搜索，最终必须回 Unity oracle 筛选。
