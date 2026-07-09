# PhysX Native State 等价性审计

这页专门回答一个证明题：

```text
Unity 在 stone-stone 碰撞那一帧喂给 PhysX 的完整 native state，
是否已经证明和本地 pyphysx 构造的 state 一模一样？
```

## 结论

现在不能证明。更严格地说，当前证据已经反证这条强命题：

```text
Unity first-contact native state == local pyphysx native state
```

原因不是“PhysX 机制完全未知”。我们已经恢复了很多高层和中层事实：PCM contact
路径、patch friction、固定步长、材质、Rigidbody 标量参数、MeshCollider cooking
flags、convex-convex / convex-mesh contact 入口、solver row 布局和主要公式。

但“完整 native state 一模一样”要求更高。它要求 `PxScene`、`PxRigidDynamic`、
`PxShape`、`PxConvexMesh`、`PxTriangleMesh`、`PxsContactManager`、`ContactBuffer`
和 solver row 的实际运行时字段逐项一致。我们还没有抓到这些字段的完整快照。

历史 current-best probe 还有一个直接的非等价点：Unity 正式冰面是静态
`MeshCollider` / triangle mesh，而本地当时用的是 `RigidStatic.create_plane`。
2026-07-09 已扩展 pyphysx binding，并在 `probe_physx_collision_alignment.py`
里加入 `--rink-geometry unity-plane-mesh`，可以用 Unity 内置 Plane 结构近似的
`10x10 / 200 triangles` 冰面做 A/B。这个 A/B 说明它不是主误差源，但也说明
“完整 native state 一模一样”仍不能只靠旧 probe 宣称。

## 怎么把 state 改成一样

不能靠继续给 endpoint 套一个残差补丁来宣布“一样”。正确做法是把本地 replay 的输入
改成 Unity 在那一帧真正喂给 PhysX 的字段，然后按层验证：

```text
第一层：trace-driven replay
  从 Unity runtime 抓 active/target/rink 的 PxRigidDynamic、PxShape、PxConvexMesh、
  PxTriangleMesh、material、pose、velocity、inertia、lock flags 和 contactOffset/restOffset。
  本地 pyphysx 或 C++ PhysX 不再重建这些字段，而是直接用 dump 出来的字段建 scene。

第二层：contact equivalence
  抓首次 stone-stone ContactBuffer / ContactPairPoint / solver row 或 applied impulses。
  先比较 0.02s 的碰后 linear/angular velocity，而不是先看最终 endpoint。

第三层：formula recovery
  如果 trace-driven replay 已经对齐，再反推这些字段是由哪段 Unity/PhysX/managed 代码生成的，
  把 runtime dump 逐步替换成公式。只有这一步完成，训练用模拟器才可以脱离 Unity。
```

所以“改成一样”的短期工程动作不是再调 `friction/restitution/radius/w_offset`，而是让
`probe_physx_collision_alignment.py` 增加一个 native-state 输入模式：从 Unity dump 的
字段构造 scene，并把 `0.00s -> 0.02s` 碰后速度作为第一验收门槛。endpoint 只能放在最后。

## 为什么不能用终点误差证明

如果 Unity 和本地 replay 在首次碰撞帧的 native state 真正逐字段一致，并且后续
PhysX 版本、scene flags、solver path、timestep 也一致，那么同一对刚体不应稳定产生
10cm 级 target endpoint 残差。当前证据是：

```text
unique-role current best:
  active RMSE ~= 3.86cm
  target in-play RMSE ~= 11.32cm

已有 probe 的逐样本 oracle:
  target-only oracle RMSE ~= 2.15cm
  active+target pair floor ~= 2.21cm

0.02s snapshot 反推:
  target 需要的早期 delta-v 均值 ~= 0.0366m/s
  约为碰后早期速度的 3.5%
  normal/tangent 分量都存在，不像单个 restitution 标量错误

active/target 双方 endpoint 反推:
  pair_impulse_like = 0 / 7
  non_closing_pair = 2 / 7
  pair_check_weak = 5 / 7
  target delta-v 在 0.02s-0.2s 间高度稳定

早期速度敏感度:
  合理范围内的全局 handoff/placement/yaw/radius/contactOffset 修正不能解释缺口
  无约束 least-squares 需要 213m 级 center_height 或 0.8rad 级 yaw 这类荒唐参数

冲量可行性分类:
  friction_row_or_cache_suspect = 3 / 7
  normal_row_plausible = 3 / 7
  mixed_contact_manifold_suspect = 1 / 7
  4 / 7 在 mu=0.60 的宽松残差摩擦锥外

本地 0.01s 主冲量 trace:
  7 / 7 的 target 主冲量都在 0.00s-0.01s
  本地 target 主冲量均值 ~= 19.31 Ns
  Unity 终点反推残差冲量均值 ~= 0.70 Ns
  残差 / 本地主冲量均值 ~= 3.5%
  Unity-implied normal scale mean ~= 0.983
  Unity-implied normal scale RMSE from 1 ~= 0.033
  Unity-implied tangent sign flip = 1 / 7
  dominant axis 一致 only 3 / 7

tail replay 反事实:
  从本地 0.02s snapshot 只重跑 target 尾段，baseline 可在约 3.06cm RMSE 内复现本地完整 replay；
  只允许改 target 的水平 vx/vy，有限差分 oracle 可把 Unity endpoint 压到约 0.09cm RMSE。
  所需 delta-v 分量为 normal 3 / tangent 3 / mixed 1。
  从 0.20s snapshot 做同一实验，baseline 约 2.29cm，oracle 约 0.05cm。
  所需 delta-v 分量为 normal 3 / tangent 4。
  所以主误差不在尾段滑行，而在 0.00s-0.02s 首次碰撞赋给 target 的水平线速度。

solver row delta:
  把 tail oracle 所需速度修正投回首帧 normal/tangent 冲量，平均只需改约 0.49 Ns，
  约为本地主碰撞冲量的 2.35%。
  分类为 normal-row 3、friction/contact/cache 2、tangent-sign-flip 1、mixed 1。
  最坏样本 12003 的 local N/T ~= 24.27 / -0.46 Ns；
  Unity-implied N/T ~= 23.82 / +1.31 Ns，等效冲量方向需转约 +4.25 deg。

global row correction:
  per-sample oracle 可到约 0.09cm RMSE；
  但最宽松的全局 2x2 contact-frame 线性变换仍约 10.24cm，7 / 7 超过 2cm。
  全局旋转、全局 N/T scale、统一 scale+rotation 也都在 10cm-12cm。
  所以不能靠一个统一参数补丁证明 native state 相同。

cooked-hull contact frame:
  formal cooked hull 是 64 边棱柱，side normal step = 5.625 deg。
  12003 的 local impulse world angle ~= -86.44 deg，贴近 side face -87.19 deg；
  Unity-implied impulse world angle ~= -82.18 deg，贴近相邻 side face -81.56 deg。
  它需要的 +4.25 deg 旋转约等于 0.76 个 side step。
  这更像相邻 hull feature / contact manifold / friction anchor cache 选择不同。

stone geometry input A/B:
  probe 已新增 --stone-geometry formal-recovered，可直接把 ExtendedColliders3D 恢复出的
  512 顶点 formal mesh 送入 pyphysx cooking。
  current-best inflated scale 下，formal-recovered 与旧 ring 点云 target/active RMSE 完全相同。
  formal physical scale + 0.292m handoff 下，formal-recovered 比 ring 只改善约 0.57cm target RMSE，
  但 target RMSE 仍约 12.08cm。
  因此“probe 没用 512 顶点 formal mesh 输入”不是 10cm 主误差源。

static feature-phase probes:
  common shape-local yaw: best 12003 ~= 20.41cm，global target RMSE 仍约 12.36cm。
  12003 fine shape-local yaw: best ~= 20.46cm。
  12003 active/target actor yaw +/-11.25deg: best ~= 20.43cm。
  12003 stone-faces sweep: best ~= 19.29cm。
  因此静态 hull 相位、actor yaw、简单 wrapper offset、输入 face count 都不能把 12003 压到 2cm。

wide reset-yaw probes:
  12003 active/target yaw 粗扫 + 局部细化共 487 个本地 result sets。
  best target error ~= 1.75cm，active error ~= 6.88cm。
  best pair RMSE ~= 3.41cm，对应 active ~= 4.35cm、target ~= 2.07cm。
  no tested yaw pair 让 pair RMSE 或 active+target 双终点同时小于 2cm。
  unique-role target-yaw-only per-sample oracle: target RMSE ~= 5.37cm，pair RMSE ~= 4.79cm。
  hard-sample dual-yaw: 12003/12004/12007 best pair RMSE ~= 3.41cm / 4.47cm / 5.57cm。
  serialized prefab rotation audit: 80 个正式 stone 只有 1 种 local rotation，max yaw = 0deg。
  deterministic BESTSHOT->handoff active-yaw integration: best target RMSE ~= 16.30cm，
  比 baseline 11.32cm 更差。
  因此大 yaw/rotation 是真实可疑 runtime state，但不是完整碰撞对齐解。

support pre-settle probes:
  target/active settle grid, center_height=0.1276: no-settle 仍是 global target RMSE 最优。
  target/active settle grid, center_height=0.115: no-settle 仍是 global target RMSE 最优。
  12003 在 settle 变体中最多仍约 24cm 级。
  因此冰面支撑 warm-start/cache 或竖直静置状态不是当前 10cm 主因。

handoff threshold / placement refinement:
  current-best local replay 在进入 PhysX 时，active/target 中心距已经按样本不同
  比 2R 小约 0.0002m-0.0104m。
  重新扫 handoff_extra 和毫米级 y offset 后，最佳为 handoff_extra=0.005m、
  handoff_y_offset=-0.005m。
  它把 target RMSE 从 11.32cm 降到 10.27cm，只改善约 1.05cm。
  因此接触入口时机/位置确实有贡献，但不能证明 native state 一致，也不是 2cm 解。

lock constraints:
  Unity 正式石壶运行时 constraints=80，即 FreezeRotationX|FreezeRotationZ，只允许 yaw。
  本地 z-up replay 把它映射为 PhysX LOCK_ANGULAR_X / LOCK_ANGULAR_Y。
  打开 lock-upright 后，0.02s target 横向角速度最大值为 0，说明锁轴确实生效。
  但 best target RMSE 仍约 11.37cm，和 baseline 11.32cm 同一水平。
  因此“本地 replay 没锁横滚/俯仰”不是 10cm 主误差源。

handoff x/y offset counterfactual:
  `12003` 单样本宽网格显示，若把主动壶进入本地 PhysX 前的位置改成
  `handoff_x_offset=-0.02m, handoff_y_offset=0m`，active/target endpoint error
  可降到约 `1.93cm / 3.16cm`，比 baseline 的 24cm 级 target 误差小很多。
  但把全 unique-role 样本统一扫 `y=0` 的 handoff-x 后，target RMSE 最优仍是
  `x=0m` 的 `11.32cm`；`x=-0.005m` 只让 active RMSE 更好，target RMSE 反而约
  `11.50cm`。所以这不是一个全局坐标常数漏设，而是样本级 first-contact native
  pose / manifold / cache 差异信号。

per-sample entrance-state oracle:
  最新汇总已不只是 x/y；它纳入 `12003` 的 `handoff_v_scale=1.005`、
  `12007` 的 diagnostic target reset offset、`12004/12006` 的 handoff x/y，
  以及 `12005` 的 handoff angular velocity 诊断。
  target RMSE 从 `11.32cm` 降到 `1.48cm`，active RMSE 降到 `1.35cm`；
  7 条 in-play target pair 全部双终点同时小于 `2cm`。
  这说明入口 native state 是主源头之一，但也说明原本的本地 native state 并不可能
  已经和 Unity 逐字段相同。
  `12005` 的闭合尤其关键：入口 `vx/vy` 偏移和 active/target yaw 小网格都没有改善，
  但 `handoff_w_offset=-0.44rad/s` 可把 active/target endpoint error 压到
  `1.77cm/1.37cm`。这个诊断偏移远大于可见 `motioninfo.w ~= 0.0037rad/s`，所以它
  更像缺失的 angular/tangent native state 或 contact-row/cache/manifold 状态，而不是
  已经恢复出的通用管理层公式。同 pose 的 contact report 对照中，`w=0` 与
  `w=-0.44` 的第一帧 contact time、contact count、normal、separation 都不变；
  改变的是 0.02s 的横向线速度和角速度分配。
  全样本统一扫 `handoff_w_offset` 不能闭合：全局最佳约 `-0.5rad/s`，target RMSE
  仍约 `10.94cm`，7 条 in-play pair 超过 `2cm`。所以它不是全局角速度常数。

visible-feature generalization:
  对上述 per-sample 入口状态 oracle 做了 leave-one-out 验证。用当前可见特征
  `target_before_y/requested_v0/glance/right/approach geometry` 去预测 oracle 修正，
  最好模型 `headon_linear` 仍只有 active RMSE `5.22cm`、target RMSE `30.98cm`，
  7 条 in-play pair 里 `0` 条双终点进 `2cm`。
  因此“现有样本能用 oracle 到 2cm”不能直接转成训练公式；它只是证明 native-state
  缺口存在，并且缺口是样本/contact-instance 级别。
```

所以终点误差不是证明 state 相同的证据，反而是一个反证信号：至少有某个
contact-relevant native 字段、运行时缓存、shape wrapper 或 local replay 构造方式还没对齐。
而且残差已经分裂成 normal-row 和 tangent/friction/cache 两类，不像单个全局常数错误。
主碰撞 tick 和冲量量级大体正确，剩余是首帧 contact/solver row 的几个百分点误差，
这个量级足以在 3m-4m 后续滑行中放大成 10cm 级 endpoint 偏差。
target-only tail replay 已经把后续滑行降级为非主因：从 `0.02s/0.20s` 本地 snapshot
开始，只调 target 水平线速度就能把 endpoint 压到毫米级。
进一步的 row-delta 报告显示，缺口不是整套碰撞完全错，而是首帧 solver row 的
`0.5 Ns` 量级差异；它同时包含 normal-row 与 tangent/friction/cache 两类。
全局 row-correction 模型的失败说明这些差异是 contact-instance 级别的，不是一个
统一 restitution、friction 或法线旋转常数。
contact-frame quantization 又把最坏样本 `12003` 和 64 边 cooked hull 的相邻侧面法线对上了：
本地冲量贴近一个侧面，Unity-implied 冲量贴近相邻侧面。
最硬坏样本 `12003` 的 implied tangent 冲量甚至相对本地翻符号，所以它优先指向
tangent basis、friction anchor/cache 或 contact point，而不是 restitution。
2026-07-09 又把本地 pyphysx binding 重编并打开 `PxSimulationEventCallback` contact report：
`unity_physx_collision_probe_unique_role_contact_report_current_best_20260709.json` 现在直接保存
active-target 的 `ContactPairPoint` normal、separation 和 impulse。结果进一步坐实：
`12003` 本地第一帧 contact report 的 target 侧冲量角度是 `-87.19deg`，而 Unity endpoint
反推的 target 冲量角度是 `-82.21deg`，差 `+4.98deg`，接近 64 边 cooked hull 的
一个侧面步长 `5.625deg`。这把嫌疑从“终点拟合误差”推进到首次 contact manifold
feature 选择、friction anchor/cache 或 Unity runtime shape rotation/cooked stream。
新增 stone geometry input 审计排除了一个实现缝隙：probe 现在可以直接使用
`ExtendedColliders3D` 恢复出的 512 顶点 formal mesh；在 current-best 尺度下，它和旧 ring
点云输出完全相同，formal 尺度下也只改善 `0.57cm` target RMSE，仍停在 `12.08cm`。
所以缺口不在“没有把 formal mesh 顶点送进 pyphysx cooking”。
新增 feature-phase 审计进一步排除了一个看似合理的几何解释：如果只是静态 hull 相位、
actor yaw 或简单拓扑面数错了，12003 应该能在这些离散 sweep 中出现 2cm 级谷底；实际最好
仍是 `19.29cm`。所以现在更像 Unity 运行时 contact manifold / friction anchor cache /
solver row 实例和本地 fresh scene 不同，而不是一个固定 shape phase 常数没设对。
新增 support pre-settle 审计又排除了“只是 target/active 在冰面上没有预热支撑接触缓存”
这个解释：预先让 target 或 active 在冰面上 settle，再开始碰撞，并没有降低全局 target RMSE；
在 `center_height=0.115` 的静止高度下也是如此。
新增 wide reset-yaw 审计则保留了一个重要线索：如果允许很大的 active/target yaw，`12003`
的 target endpoint 可以到 `1.75cm`，说明 reset rotation/yaw 确实会强烈改变 contact feature。
但同一组 yaw 下 active 仍约 `6.88cm`，最佳 pair RMSE 也只有 `3.41cm`，所以它不是单独的
2cm 级双壶解。把 target-yaw-only 放宽到全 unique-role 样本后，per-sample oracle 的
target RMSE 仍约 `5.37cm`，pair RMSE 仍约 `4.79cm`；对 `12004/12007` 再做 active/target
双 yaw 粗扫，最佳 pair RMSE 也分别只有 `4.47cm/5.57cm`。所以 reset rotation/yaw
是“缺运行时状态或 contact feature 代偿”的证据，不是“已经证明 native state 一致”的证据。
资产层又补了一条反证：`unity_stone_prefab_rotation_audit_20260709.json` 显示 80 个正式
`Curling stone*` 只有一种 near-identity local rotation，yaw 最大绝对值为 `0deg`。
因此 wide-yaw 改善不能解释成“不同编号/颜色的 prefab 初始 yaw 本来就不同”。
又把 `BESTSHOT -> MOTIONINFO -> handoff` 的可见旋转相位接入 probe：
`--active-yaw-source integrated-precontact`，并同时扫 `+/-` 积分符号。结果 best target
RMSE 反而从 baseline `11.32cm` 变差到 `16.30cm`。所以 wide-yaw 改善也不能简单解释成
“之前漏了 active 壶从出手到碰撞的累计自旋 yaw”。
又补了 handoff threshold / placement 审计：把 active/target 接触入口调早 `5mm`，并把
协议 y 平移 `-5mm`，只能把 target RMSE 从 `11.32cm` 降到 `10.27cm`。所以 handoff
边界确实不是完全无关，但它解释的是约 `1cm`，不是剩下的 `10cm`；这条线同样不能支撑
“Unity 和本地喂给 PhysX 的 native state 已经逐字段相同”。
再补锁轴审计：Unity 的 `FreezeRotationX|FreezeRotationZ` 是确定事实，current-best
确实没有默认打开；但本地打开 `--lock-upright` 并使用 cooked-hull 惯量后，target RMSE
仍约 `11.37cm`。这说明锁轴应该进入最终 reference simulator，但不是当前碰撞误差来源。
再补 handoff x/y 反事实：`12003` 用 `x=-2cm,y=0` 可以把 active/target 压到
`1.93cm/3.16cm`，说明碰撞入口位置确实足以改变首帧 contact feature；但全样本统一
`y=0`、只扫 x 的最佳 target RMSE 仍是 baseline `11.32cm`，不是一个统一坐标偏置。
这条证据把问题继续压到“每次碰撞实例的 native pose/contact manifold/cache 是否一致”，
而不是“已经能证明完整 native state 一模一样”。
把 handoff x/y 扩成 per-sample 入口状态 oracle 后，结论更定量：target RMSE 可降到
`1.48cm`，active RMSE 可降到 `1.35cm`，7/7 in-play target pair 双终点进 `2cm`。
`12003` 由微小 `handoff_v_scale=1.005` 闭合，`12007` 由 diagnostic target reset
offset 闭合，`12005` 由 `handoff_w_offset=-0.44rad/s` 闭合。
这说明 reconstructed entrance native state 是大误差来源之一，也反过来说明原来的
本地 replay 入口状态不可能已经和 Unity 逐字段相同。
这一步已经把现有 in-play 样本控制到 2cm，但控制手段是 per-sample 诊断入口状态；
它不能直接宣布训练用模拟器已经恢复通用真公式。
`12005` 的 0.20s tail oracle 曾显示需要约 `0.107m/s` 的 active 速度修正，在接触坐标系中
主要是 tangent 侧约 `-1.99 Ns`。现在 `handoff_w_offset` 能闭合它，进一步说明缺口优先
指向 active-side angular/tangent native state 或 contact-row/cache，而不是后段滑行。

## 等价性清单

| 维度 | Unity 状态 | 本地 pyphysx 状态 | 当前判断 |
| --- | --- | --- | --- |
| fixed timestep | `0.01s` | probe `dt=0.01s` | 已对齐 |
| gravity | `(0,-9.81,0)`，石壶 `useGravity=true` | z-up 场景 `-9.81`，未禁用重力 | 主 probe 已对齐 |
| contact generation | `contactsGeneration=1`，PCM | pyphysx scene 默认包含 PCM | 大路径对齐 |
| friction type | `frictionType=0`，patch friction | probe 走默认 patch friction | 大路径对齐 |
| solver iterations | `6/1` | probe 设置 `6/1` | 已对齐 |
| Rigidbody scalar | mass `19.1`、drag `0`、angularDrag `0.05` | probe 设置对应值 | 大部分对齐 |
| constraints | `FreezeRotationX | FreezeRotationZ`，yaw 自由 | lock-upright replay 映射为 PhysX `LOCK_ANGULAR_X/Y`，可把横向角速度压到 0 | 已验证映射，非主因 |
| COM | `CurlingStoneNew.Start` 写 `centerOfMass=Vector3.zero` | probe 默认 body COM / 可设惯量 | COM 高置信，tensor 仍依赖 shape |
| inertia tensor | Unity runtime MeshCollider rebuild 后隐式更新 | 离线 hull 推导 `radial=0.178810612362 / vertical=0.189222883199` | 公式已推，runtime shape 未逐字段证明 |
| stone material | Bouncy，friction/restitution/Combine 已恢复 | probe 可设置 `0.6/1.0/Multiply` | 大体对齐 |
| material timing | OnCollisionEnter 是否首帧前后切换 | 已做 pre/post/never 小网格 | 已弱化为非主因 |
| stone convex cooking flags | `eCOMPUTE_CONVEX`，`vertexLimit=255`，`quantizedCount=255`，`qi=false/gpu=false` | rebuilt pyphysx 可按这些 flags 离线 cook | flags 对齐，runtime stream 未直接证明 |
| formal cooked hull | Unity formal stone runtime `PxConvexMesh` | 离线 cook 为 `128 vertices / 66 polygons / 384 indices` | 强推断，不是 byte-level 证明 |
| shape local pose/scale | Unity `PxShape` wrapper 的真实 local pose / scale | probe 默认 identity，已扫 common offset/yaw、actor yaw、stone-faces | 静态相位/offset 已排除为 2cm 解，但 wrapper 未直接抓取 |
| rink geometry | 静态 `MeshCollider` triangle mesh | probe 支持旧 `PxPlane` 和 `unity-plane-mesh` | 近似可跑，精确 stream 未导出 |
| rink cooked mesh | Unity default Plane mesh，经 cooking options=30 | 本地 10x10 Plane mesh A/B 已跑 | 非主因，但未 byte-level 证明 |
| handoff pose/velocity | Unity true Newfrictionstep -> PhysX 入口帧 | 已用 console handoff、handoff_extra 和毫米级 y offset 扫描；最佳仍约 10.27cm target RMSE | 部分验证，不是 2cm 解 |
| contact manager cache | Unity 场景中 pair/cache/friction anchors 的运行时状态 | fresh pyphysx scene，默认无历史 cache | 未证明 |
| first ContactBuffer | Unity PCM 输出的 normal/point/separation/material | 未抓取，只能从 endpoint/0.02s 反推 | 缺核心证据 |
| solver rows/impulses | Unity `SolverContact*` 行和 applied impulses | 公式/布局已恢复，但实例未抓取；本地主冲量 trace 只证明 0.00s-0.01s 主冲量量级正确，残差分类仍指向 normal-row 与 friction/cache 两类 | 缺核心证据 |

## 已经排除或弱化的方向

这些方向不能再当成主解释：

```text
1. 单纯 dt 错误：dt=0.009/0.011 会米级失真，正确路径固定为 0.01s。
2. 完全禁用重力：target RMSE 会到十几米，说明支撑接触必须存在。
3. 消掉 0.02s 竖直速度：center_height=0.115 后 target RMSE 仍约 11.32cm。
4. OnCollisionEnter 首帧完全 0 摩擦：会变差；dynamic=0/static=0.6 与 baseline 等价。
5. 只换 cooked-hull 推导惯量：formal geometry + cooked inertia target RMSE 仍约 12.65cm。
6. common shape-local x/y/z/yaw 小偏移：没有把 target RMSE 拉到 2cm。
7. `PxPlane` vs triangle-mesh 冰面：`unity-plane-mesh` A/B 后 target RMSE 约 `12.83cm`，
   比 current-best-refresh `11.32cm` 更差，因此冰面几何不是 10cm 主因。
8. `frictionOffsetThreshold`：`0.005/0.01/0.02/0.04/0.08/0.12` 的 endpoint 完全相同，
   target RMSE 都是 `11.32cm`；`0.001` 反而变差到 `12.60cm`，所以它不是当前缺口主因。
9. 单靠 endpoint 反推一个“缺失 pair impulse”：多数样本 active tail 太短，闭合检查弱；
   target 端修正却在多个 snapshot 上稳定，说明问题在碰后最早几帧，而不是后续尾段漂移。
10. 静态 feature phase：共同 shape-local yaw、12003 fine shape-local yaw、active/target actor yaw、
    shape-local xyz、stone-faces 扫描都不能把硬坏样本 `12003` 拉到 2cm；最好仍约 `19.29cm`。
11. formal mesh 输入：`--stone-geometry formal-recovered` 已直接使用 512 顶点 recovered mesh；
    current-best 尺度下与旧 ring 点云 endpoint 完全相同，formal 尺度下也只改善 `0.57cm`
    target RMSE，仍约 `12.08cm`，不是 10cm 主因。
12. target/active 支撑 pre-settle：预先 settle target、active 或两者，`center_height=0.1276`
    和 `0.115` 两组网格都没有改善全局 target RMSE；no-settle 仍是最优。
13. 宽范围 reset yaw：可把 `12003` 的 target 降到 `1.75cm`，但 active 仍约 `6.88cm`；
    最佳 pair RMSE 约 `3.41cm`，没有双终点同时小于 `2cm` 的 yaw pair。全样本
    target-yaw-only oracle 仍有 `5.37cm` target RMSE，`12004/12007` 双 yaw 粗扫也
    分别停在 `4.47cm/5.57cm` pair RMSE。资产层 80 个正式 stone 的 serialized yaw
    都是 0，所以它不是 prefab 初始 yaw 差异。BESTSHOT 到 handoff 的 deterministic active
    yaw 积分接入 probe 后 target RMSE 变差到 `16.30cm`，所以也不是简单漏掉累计自旋相位。
14. handoff threshold / placement：把接触入口调早 `5mm` 并加 `-5mm` protocol-y offset
    是当前小网格最优，但 target RMSE 仍约 `10.27cm`；它只比 baseline 改善约 `1.05cm`，
    因此不能证明碰撞帧 native state 已经和本地 replay 一模一样。
15. lock-upright / Rigidbody constraints：Unity runtime 锁住横滚/俯仰是确定事实；本地
    `--lock-upright` 后 `0.02s` target 横向角速度最大值为 0，但 target RMSE 仍约
    `11.37cm`，所以自由横滚/俯仰不是当前 10cm 主误差源。
16. 本地 ContactPairPoint dump：`--enable-contact-report` 已能抓 active-target 首次接触。
    8 条样本第一帧 contact 都在 `0.01s`；`12003` 本地 contact report 冲量角度
    `-87.19deg`，Unity-implied 冲量角度 `-82.21deg`，差 `+4.98deg`。所以现在最强证据
    指向 Unity 首帧 contact manifold / feature / cache 与本地不同，而不是后段滑行。
17. 统一 handoff-x 常数：全样本 `y=0`、x 从 `-3cm` 到 `+3cm` 的 sweep 中，target RMSE
    最优仍是 `x=0m` 的 `11.32cm`；`x=-0.005m` 虽把 active RMSE 从 `3.86cm`
    降到 `2.72cm`，但 target RMSE 升到 `11.50cm`。单样本 `12003` 的
    `x=-2cm,y=0` 能到 `1.93cm/3.16cm`，这只能说明局部碰撞实例敏感，不能说明存在
    一个全局偏移能补齐 native state。
18. per-sample 入口状态 oracle：纳入 handoff x/y、`handoff_v_scale`、target reset
    offset 和 handoff angular velocity 诊断后，target RMSE 降到 `1.48cm`，
    active RMSE `1.35cm`，7 条 in-play target pair 全部双终点同时小于 `2cm`。
    active-only 计分时 8 条 active 全部小于 `2cm`，active RMSE 约 `0.61cm`。
    这说明入口 native state 是实源头之一；若原始 replay 已经逐字段等价，这些
    per-sample 入口扰动不该成为主解释变量。
19. `12005` 残差类型：入口 `vx/vy` 偏移和 active/target yaw 小网格都没有改善；
    `handoff_w_offset=-0.44rad/s` 可把 active/target 压到 `1.77cm/1.37cm`。
    因为可见 `motioninfo.w` 只有约 `0.0037rad/s`，这个闭合项应解释为
    active-side angular/tangent native state 或 contact-row/friction-cache/manifold 代理，
    而不是一个已经恢复的通用管理层角速度公式。contact report 对照没有改变第一帧
    normal/separation/contact count，进一步排除 normal row 或接触点数量是这一步的主因。
    全局 `handoff_w_offset` 最好仍有 `10.94cm` target RMSE 和 7 条 bad pair，排除
    “统一角速度常数”。
20. 可见特征预测 oracle 修正失败：`tools/reverse/analyze_collision_oracle_generalization.py`
    做 leave-one-out 后，最好模型是 `headon_linear`，active RMSE `5.22cm`、
    target RMSE `30.98cm`，7 条 in-play pair 里没有一条双终点进 `2cm`。
    这说明现在缺的不是一个可从 `v/y/左右偏碰` 直接读出的简单经验公式。
```

## 真正需要的证明

要证明 native state 一样，最少要拿到碰撞那一帧的这些数据：

```text
1. active / target:
   global pose、linear/angular velocity、mass、COM、inertia tensor、
   solver iteration counts、maxDepenetrationVelocity、lock flags、sleep state、reset 后 rotation/yaw。

2. active / target PxShape:
   local pose、geometry type、convex mesh pointer、geometry scale、
   contactOffset、restOffset、material、filter data。

3. formal stone cooked stream:
   CVXM/CLHL、vertices、polygons、indices、bounds、mass/inertia/COM、
   SUPM/GAUS/VALE 顺序和 byte-level 内容。

4. rink:
   PxTriangleMesh 或 cooked mesh 的顶点/三角形/scale/local pose/material。

5. contact manager:
   persistent contact cache、friction patches/anchors、pair age、fresh/broken 标志。

6. 首次 stone-stone contact 输出:
   normal、contact points、separation、material fields、maxImpulse、
   SolverContactHeader / SolverContactPoint / SolverContactFriction、
   normal/friction applied impulses。

本地侧现在已能导出 `PxContactPairPoint`，但这只证明本地选了什么 contact normal/points。
要完成等价证明，还必须在 Unity runtime 抓到同一帧的 ContactBuffer 或 solver rows。
```

只有这些字段逐项一致，才可以说“Unity 喂给 PhysX 的完整 native state 和本地 replay
一模一样”。现在我们只能说：高层配置和许多公式已经对齐，但 contact-relevant runtime
state 还没完成证明。

## 最短路线

接下来不要再靠 endpoint 大网格蒙参数。最快路径是：

```text
1. 保留 triangle-mesh 冰面 A/B，不再把它当主线。
   pyphysx binding 已在 `D:\esp\tmp\curling_pyphysx` 中扩出
   `Shape.create_triangle_mesh_from_points`，并已安装到
   `D:\esp\tmp\curling_pyphysx_conda`。probe 可用：

   ```powershell
   D:\esp\tmp\curling_pyphysx_conda\python.exe tools\reverse\probe_physx_collision_alignment.py `
     --rink-geometry unity-plane-mesh ...
   ```

   当前输出：

   ```text
   data/calibration/unity_physx_collision_probe_unique_role_rink_mesh_currentbest_winding_20260709.json
   active RMSE ~= 3.86cm
   target RMSE ~= 12.83cm
   ```

2. 运行时 hook formal stone 的 PxShape / PxConvexMeshGeometry。
   目标不是再导等待页装饰 hull，而是比赛石壶 active/target 的 shape local pose、
   scale、material、filter、convex mesh stream。静态 yaw/offset/faces sweep 已经不能解释
   12003，所以这里要抓的是 runtime 字段，而不是继续猜固定相位。

3. hook 首次 stone-stone contact 的 ContactBuffer 或 solver rows。
   只要拿到 normal、points、separation、normal/friction impulse，
   就能判断误差来自 contact manifold、friction row、inertia/pose，还是 handoff 状态。

4. 本地 replay 的验收先看 0.02s 碰后速度/角速度。
   如果这里对齐，终点还偏，再查碰后滑行随机摩擦；如果这里不对齐，就继续查 contact native state。
```

## 机器审计报告

对应摘要脚本：

```powershell
D:\esp\tmp\curling_pyphysx_conda\python.exe tools\reverse\summarize_physx_native_state_equivalence.py
```

输出：

```text
data/calibration/unity_physx_native_state_equivalence_audit_20260709.json
```

这个报告把每个 native-state 字段标成 `matched`、`mostly_matched`、
`binding_available_not_main_cause`、`inferred_not_captured` 或
`missing_required_proof` 等状态。
以后每补一个 hook 或 local replay 修正，就更新这张表，而不是笼统说“PhysX 已经很详细”。
