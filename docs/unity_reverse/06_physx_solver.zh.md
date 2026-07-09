# PhysX 接触约束与 Solver

记录 Px1DConstraint 排查、contact finalization、single-pair 和 4-wide patch contact solver 的结构与公式。

> 原长文档已封存：[`UNITY_REVERSE_ENGINEERING.zh.2026-07-07.archive.md`](../archive/UNITY_REVERSE_ENGINEERING.zh.2026-07-07.archive.md)。以后维护以本目录子文档为准。

这条线后来确认是通用 `Px1DConstraint` 行约束准备路径，不是石壶 contact point 的主结构。

继续拆 `func71272` 后，已经能把内部 helper 粗分出来：

```text
func71150 f_ofad
  初始化/清空 Dy::ThreadContext 一类的 contact/constraint 临时缓存，
  预分配 512/128 容量的数组区。

func71197 f_jhad
  扩容并拷贝 32-byte float records，底层来源标注为 PsArray.h。

func71174 f_mgad
  `Px1DConstraint` rows 的 preprocessRows。80-byte 输入 row 精确对应
  `PxConstraintDesc.h::Px1DConstraint`：offset 76 是 flags，offset 78 是 solveHint。
  它先按 solveHint 插入排序，再把 KEEPBIAS row 的 geometricError 复制到 forInternalUse，
  接着用两个 body 的 sqrtInvInertia 计算 angular row，最后按 solveHint 高/低 byte
  做 orthogonalize / diagonalize 分组处理。

func71175 f_ngad
  对小批量 `Px1DConstraint` row 做 3x3/四元数式迭代正交化，含 5 次迭代、
  sqrt、1e3/2e6 阈值。对应 PhysX 里的 diagonalize / orthogonalize 稳定化，
  不是冰壶专用公式。

func71176 f_ogad
  最终 1D constraint row block writer。它写入 48-byte header 和逐行 constraint：
  无 articulation 时每 row 96 byte，extended/articulation 时每 row 160 byte。
  对照 PhysX 4.1，这个尺寸精确对应 `DySolverConstraint1D.h` 里的
  `SolverConstraint1DHeader` / `SolverConstraint1D` / `SolverConstraint1DExt`，
  而不是 `SolverContactPoint`。`65535` 是 `PxSolverConstraintDesc::NO_LINK`。

func71177 f_pgad
  单 block fallback：先调用动态 constraint shader 填最多 12 个 80-byte `Px1DConstraint` row，
  再调用 func71176 写成最终 1D solver constraint block。
```

80-byte 输入 row 现在已经不是未知 blob，而是 `Px1DConstraint`：

```text
offset 0   linear0.xyz
offset 12  geometricError
offset 16  angular0.xyz
offset 28  velocityTarget
offset 32  linear1.xyz
offset 44  minImpulse
offset 48  angular1.xyz
offset 60  maxImpulse
offset 64  mods.spring.stiffness / mods.bounce.restitution
offset 68  mods.spring.damping / mods.bounce.velocityThreshold
offset 72  forInternalUse
offset 76  flags
offset 78  solveHint
```

`func71176` 的输出字段也能命名到 PhysX 1D row 结构级别：

```text
l[6]      = desc.constraint，分配出的 constraint block 指针
l[11]     = desc.constraintLengthOver16
header[0] = type，普通 row 为 `DY_SC_TYPE_RB_1D`，extended row 为 `DY_SC_TYPE_EXT_1D`
header[1] = count，后续 1D rows 数量
row[0..2] / row[4..6]   = lin0 / lin1
row[8..10] / row[12..14] = ang0 / ang1
row[3] / row[7]         = constant / unbiasedConstant
row[11] / row[15]       = velMultiplier / impulseMultiplier
row[16..18]             = ang0Writeback
row[20..23]             = minImpulse / maxImpulse / appliedForce / flags
extended row 追加 deltaVA / deltaVB，用于 articulation impulse response
input row 的 flags 和 bounce/spring 位会决定 restitution、bias 和 drive 公式分支
```

其中一个关键分支已经能读出物理含义：

```text
if inputRow[38] & 1:
  使用 inputRow[16], inputRow[17], inputRow[7], inputRow[3] 计算 restitution/bias 项
  若 inputRow[38] & 2，则走另一套缩放公式
else:
  使用 row effective mass 的倒数，并根据输入 flags 判断 bounce/threshold 分支
```

`func71176` 里原先标出的两处 `call_indirect` 已经能和 PhysX 4.1 对上：
它们不是普通 `Rigidbody` 的必经 vtable，而是 articulation/link 分支里的
`Articulation::getImpulseResponse`。`65535` 对应 PhysX 的
`PxSolverConstraintDesc::NO_LINK`；当 `linkIndexA/linkIndexB` 都是 `NO_LINK`
时，`func71176` 选择 96-byte `SolverConstraint1D` row，并直接用
`PxSolverBodyData` 计算 unit response。只有任一端不是 `NO_LINK` 时，才切到
160-byte `SolverConstraint1DExt` row，并通过 articulation vtable 计算对应 link 的响应。

普通刚体分支的公式层含义已经明确：

```text
resp0 = |lin0|^2 * invMass0 * linearScale0 + |ang0|^2 * angularScale0
resp1 = |lin1|^2 * invMass1 * linearScale1 + |ang1|^2 * angularScale1
unitResponse = resp0 + resp1
recipResponse = unitResponse <= minRowResponse ? 0 : 1 / unitResponse

非 spring 行:
  velMultiplier     = -recipResponse
  impulseMultiplier = 1
  若 restitution 条件成立:
    constant = unbiasedConstant = recipResponse * restitution * (-normalVel)
  否则:
    constant         = recipResponse * (velocityTarget - geometricError * recipDt)
    unbiasedConstant = recipResponse * (velocityTarget - internalBias * recipDt)
```

`func71169 f_hgad` 也已对上普通刚体的 `PxSolverBodyData::projectVelocity`：

```text
projectVelocity(lin, ang) =
  bodyData.linearVelocity.dot(lin) + bodyData.angularVelocity.dot(ang)
```

项目 dump 里能看到 Unity/ROS/BioIK 的通用 Joint 类型定义，但这些是库类型；
当前已恢复的冰壶石正式对象仍是 `Rigidbody + MeshCollider`，没有证据表明正式比赛
石壶碰撞依赖 joints 或 articulation。也就是说，`func71174/71175/71176/71177`
这条线把通用 1D constraint row 准备公式挖出来了，但它不是石壶接触点求解的核心缺口。
真正影响石壶碰撞的是 contact finalization：`func71103/func70963`
如何把 contact patches 写成 `SolverContactHeader` / `SolverContactPoint` /
`SolverContactFriction`。这一层现在也已经从“入口已知”推进到“核心字段和公式已知”。

`func71103` 的前半段精确对应 PhysX 4.1 的
`DyContactPrep.cpp::createFinalizeSolverContacts(...)`：

```text
func71103 / createFinalizeSolverContacts
  -> func71234 f_uiad = extractContacts
     从 PxsContactManagerOutput 抽取 normal、point、separation、
     materialFlags、maxImpulse、staticFriction、dynamicFriction、
     restitution、targetVel，并读取 invMass / invInertia scale。
  -> func71233 f_tiad = getFrictionPatches
     从上一帧 friction cache 恢复未 broken 的 friction anchors。
  -> func71216 f_ciad = createContactPatches
     按 normal/material/restitution/friction 把 contact 合并成 patches。
  -> func71217 f_diad = correlatePatches
     把 contact patches 和 friction patches 关联。
  -> func71218 f_eiad = growPatches
     按 correlationDistance / frictionOffsetThreshold 生成或扩展 friction anchors。
  -> reserveBlockStreams
  -> setupFinalizeSolverConstraints
```

`func70963` 对应 `DyContactPrep4.cpp::createFinalizeSolverContacts4(...)`，是 4 个
contact pair 的 batched path。它的前半段对每个 pair 重复上面的
`extractContacts/getFrictionPatches/createContactPatches/correlatePatches/growPatches`
流程，随后按 `SolverContactHeader4`、`SolverFrictionSharedData4`、
`SolverContactBatchPointBase4/Dynamic4`、`SolverContactFrictionBase4/Dynamic4`
计算 block stream 大小。若 4-pair batch 不可处理，PhysX 会回落到
`func71103` 的 single-pair path。

single-pair 普通刚体路径的输出结构已经能命名：

```text
SolverContactHeader  // wasm 32-bit build 中为 64 bytes
  type
  flags
  numNormalConstr
  numFrictionConstr
  angDom0 / angDom1
  invMass0 / invMass1
  staticFriction / dynamicFriction / dominance0 / dominance1
  normal / minAppliedImpulseForFriction
  broken / frictionBrokenWritebackByte / shapeInteraction

SolverContactPoint   // 48 bytes
  raXn
  rbXn
  velMultiplier
  biasedErr
  unbiasedErr
  maxImpulse

SolverContactFriction // 64 bytes
  normalXYZ_appliedForceW
  raXnXYZ_velMultiplierW
  rbXnXYZ_biasW
  targetVel
```

`func71104 f_udad` 已对上 `DyContactPrepShared.h::constructContactConstraint(...)`，
也就是逐接触点 normal constraint 的核心公式。它对每个 contact point 做：

```text
point = contact.point
normal = contact.normal
ra = point - bodyFrame0.p
rb = point - bodyFrame1.p
raXn = cross(ra, normal)
rbXn = cross(rb, normal)
raXnSqrtInertia = invSqrtInertia0 * raXn
rbXnSqrtInertia = invSqrtInertia1 * rbXn

unitResponse =
  invMass0 * dominance0 * |normal|^2
  + angDom0 * dot(raXnSqrtInertia, raXnSqrtInertia)
  + invMass1 * dominance1 * |normal|^2
  + angDom1 * dot(rbXnSqrtInertia, rbXnSqrtInertia)

velMultiplier = unitResponse > 0 ? 1 / unitResponse : 0
penetration = contact.separation - restDistance
scaledBias = velMultiplier * max(maxPenBias, penetration * invDt * 0.8)

如果 restitution > 0 且相对法向速度低于 bounceThreshold：
  targetVelocity += restitution * (-relativeNormalVelocity)

biasedErr   = targetVelocity * velMultiplier - scaledBias
unbiasedErr = targetVelocity * velMultiplier - max(scaledBias, 0)
maxImpulse  = contact.maxImpulse
```

`func71105 f_vdad` 是 `SolverContactFriction` 行的构造 helper。它为每个 friction
anchor 写两条切向约束：

```text
t0 = relativeLinearVelocity 去掉 normal 分量后的归一化方向
如果 t0 太小，fallback 到 normal 和坐标轴构造出的垂直方向
t1 = cross(normal, t0)

每个 anchor:
  ra/rb = body0/body1 anchor 旋转到世界
  error = (ra + bodyFrame0.p) - (rb + bodyFrame1.p)

每个 tangent:
  raXn = cross(ra, tangent)
  rbXn = cross(rb, tangent)
  response = invMass terms + angular response terms
  velMultiplier = response > 0 ? 0.8 / response : 0
  bias = dot(tangent, error) * invDt
  targetVel = dot(contact.targetVel, tangent) - relativeTangentVelocity
```

`func71173 f_lgad` 是接触/摩擦 helper 里调用的 impulse response 计算：普通刚体时直接用
`PxSolverBodyData` 的 invMass 和 sqrtInvInertia 计算线/角速度响应；如果 link index
不是 `65535`，才切到 articulation 的 `getImpulseResponse` 间接调用。正式冰壶石没有
articulation，因此主路径是普通刚体分支。

继续往 solver 迭代阶段追，`SolverContactPoint` / `SolverContactFriction` 被消费的
核心函数也已经定位到 wasm 函数：

```text
func71035 f_dbad
  对应 patch friction 的 solveContact 动态-动态主循环。
  用于 stone-stone 这类两端都是普通 Rigidbody 的接触。

func71036 f_ebad
  对应 patch friction 的 solveContact_BStatic 主循环。
  用于 stone-rink / stone-wall 这类 body1 为 static/kinematic 的接触。

func71041 f_jbad
  solveContactConcludeBlock 动态-动态 wrapper。
  先调用 func71035，再把 SolverContactPoint.biasedErr 替换成 unbiasedErr，
  并清空 friction appliedForce。

func71044 f_mbad
  solveContact_BStaticConcludeBlock 静态 body1 wrapper。
  先调用 func71036，再做同样的 conclude 处理。
```

`func71035` 的字段偏移和 `DySolverConstraints.cpp::solveContact(...)` 对得上：

```text
PxSolverConstraintDesc:
  desc.bodyA / desc.bodyB
  desc.constraint
  desc.constraintLengthOver16

SolverContactHeader:
  offset 0   type
  offset 2   numNormalConstr
  offset 3   numFrictionConstr
  offset 4   angDom0
  offset 8   angDom1
  offset 12  invMass0
  offset 16  staticFriction
  offset 20  dynamicFriction
  offset 24  dominance0
  offset 28  dominance1
  offset 32  normal.xyz
  offset 48  invMass1

SolverContactPoint, 48 bytes:
  float[0..2]  raXn
  float[4..6]  rbXn
  float[8]     velMultiplier
  float[9]     biasedErr
  float[10]    unbiasedErr
  float[11]    maxImpulse

SolverContactFriction, 64 bytes:
  float[0..2]  tangent normal
  float[3]     appliedForce
  float[4..6]  raXt
  float[7]     velMultiplier
  float[8..10] rbXt
  float[11]    bias
  float[12]    targetVel
```

动态-动态 normal contact 的实际迭代公式可以写成：

```text
old = appliedForce[i]
normalVel =
  dot(normal, linVel0) + dot(raXn, angVel0)
  - dot(normal, linVel1) - dot(rbXn, angVel1)

delta = max(biasedErr - velMultiplier * normalVel, -old)
newApplied = min(old + delta, maxImpulse)
delta = newApplied - old

linVel0 += normal * invMass0 * delta
linVel1 -= normal * invMass1 * delta
angVel0 += raXn * angDom0 * delta
angVel1 -= rbXn * angDom1 * delta
```

这一点在 `func71035` 中表现为：

```text
point[8]  = velMultiplier
point[9]  = biasedErr
point[11] = maxImpulse
forceBuffer[i] = min(maxImpulse, old + max(biasedErr - velMultiplier*normalVel, -old))
```

动态-动态 friction 行随后使用同一个 contact patch 累计出的 normal impulse：

```text
normalImpulseSum = sum(newApplied normal impulses in this patch)
staticLimit  = staticFriction  * normalImpulseSum
dynamicLimit = dynamicFriction * normalImpulseSum

old = friction.appliedForce
tangentVel =
  dot(tangent, linVel0) + dot(raXt, angVel0)
  - dot(tangent, linVel1) - dot(rbXt, angVel1)

candidate = old - velMultiplier * (bias - targetVel + tangentVel)

if abs(candidate) > staticLimit:
  newApplied = clamp(candidate, -dynamicLimit, dynamicLimit)
  broken = true
else:
  newApplied = candidate

delta = newApplied - old
用 tangent / raXt / rbXt 把 delta 写回两端线速度和角速度
```

`func71036` 是同一公式的静态 body1 版本：没有 body1 的速度项和写回项，只更新 body0。
这对 stone-rink 和 stone-wall 很关键：冰面/墙不吸收速度，所有冲量只改动石壶的线速度和角速度。

4-pair batch solver 的消费端也已经继续往下对到了 wasm。`func70963`
生成的 `SolverContactHeader4` / block stream 不是另一套物理模型，而是后续 4-wide
SIMD contact solver 的输入：

```text
func70917 f_pwzc
  对应 DySolverConstraintsBlock.cpp::solveContact4_Block(...)
  动态-动态 4-pair block solver。
  contact stride = 144 bytes，对应 SolverContactBatchPointDynamic4。
  同时读取/写回 bodyA 和 bodyB 的线速度、角速度。

func70919 f_rwzc
  对应 DySolverConstraintsBlock.cpp::solveContact4_StaticBlock(...)
  静态 body1 4-pair block solver。
  contact stride = 96 bytes，对应 SolverContactBatchPointBase4。
  只读取/写回 bodyA，适合 stone-rink / stone-wall 这类 static body1。

func70920 f_swzc
  对应 solveContactPreBlock_Conclude(...)
  先调用 func70917，再执行 concludeContact4_Block(dynamic)。

func70921 f_twzc
  对应 solveContactPreBlock_ConcludeStatic(...)
  先调用 func70919，再执行 concludeContact4_Block(static)。
```

`func70917` 的开头从 `desc[0..3].bodyA/bodyB` 读取 4 个 pair 的 body，
然后把 4 个 pair 的 `linearVelocity/angularState` 转置成 Vec4 lanes。
这与 PhysX 源码里的 `PX_TRANSPOSE_44` 完全对应。它随后按
`SolverContactHeader4` 读取：

```text
numNormalConstr / numFrictionConstr
appliedForces[numNormalConstr]        // Vec4，每个 lane 是一个 pair
SolverContactBatchPointDynamic4[]
optional maxImpulses[numNormalConstr]
SolverFrictionSharedData4
frictionAppliedForce[numFrictionConstr]
SolverContactFrictionDynamic4[]
```

动态-动态 4-wide normal 迭代公式和 single-pair 的 `func71035` 一样，
只是每个变量都是 4-lane Vec4：

```text
relVel =
  dot(normal, linVel0) - dot(normal, linVel1)
  + dot(raXn, angVel0) - dot(rbXn, angVel1)

delta = biasedErr - velMultiplier * relVel
delta = max(delta, -oldApplied)
newApplied = min(oldApplied + delta, maxImpulse)
delta = newApplied - oldApplied

linVel0 += normal * invMass0 * delta
linVel1 -= normal * invMass1 * delta
angVel0 += raXn * angDom0 * delta
angVel1 -= rbXn * angDom1 * delta
```

4-wide friction 也和 single-pair 一样，先用本 patch 的累计 normal impulse
给出 static/dynamic friction limit，然后在两个 tangent rows 上迭代：

```text
staticLimit  = staticFriction  * accumulatedNormalImpulse
dynamicLimit = dynamicFriction * accumulatedNormalImpulse

tangentVel =
  dot(tangent, linVel0) - dot(tangent, linVel1)
  + dot(raXt, angVel0) - dot(rbXt, angVel1)

candidate = oldApplied - scaledBias - velMultiplier * tangentVel

if abs(candidate) > staticLimit:
  newApplied = clamp(candidate, -dynamicLimit, dynamicLimit)
  broken = true
else:
  newApplied = candidate
```

`func70919` 是同一公式的静态 body1 版本：少掉 bodyB 的速度项和写回项。
这和 `func71036` 对 single-pair static contact 的作用完全一致。`func70920/70921`
的 conclude 部分则把 normal contact 里的 `biasedErr` 改成下一阶段使用的
`biasedErr - scaledBias`，并把 friction row 的 `scaledBias` 重置成
`targetVelocity`。在 wasm 里它表现为 144-byte 或 96-byte stride 上的
`a[23]-=a[19]`、`a[22]-=a[18]`、`c[6]=c[10]`、`c[7]=c[11]`
这类字段拷贝/替换。

因此 `func70963/createFinalizeSolverContacts4` 的求解端公式已经不再是未知：
它写出的 block stream 进入 `func70917/70919`，公式上等价于把 4 个 single-pair
patch contact 并排求解。剩余难点不是“4-wide 使用了另一种碰撞物理”，而是
把 `SolverContactHeader4`、`SolverContactBatchPoint*4`、
`SolverContactFriction*4` 的每个字段完整工程化翻译，并继续追上游
`func70574/func70576/func70030/func70051` 如何生成 contact 点。

`func70963` 的 batch field layout 也已经不再是纯未知。对照 PhysX 4.1
`DySolverContact4.h` 与 `DyContactPrep4.cpp::setupFinalizeSolverConstraints4(...)`，
32-bit wasm 下的 block stream 结构为：

```text
SolverContactHeader4                         // 192 bytes
Vec4 appliedNormalForces[numNormalConstr]    // 每个 Vec4 的 xyzw = 4 个 pair
SolverContactBatchPointBase4/Dynamic4[]      // static 96 bytes, dynamic 144 bytes
optional Vec4 maxImpulse[numNormalConstr]
SolverFrictionSharedData4                    // 128 bytes, 仅 numFrictionConstr > 0 时
Vec4 frictionAppliedForce[numFrictionConstr]
SolverContactFrictionBase4/Dynamic4[]        // static 96 bytes, dynamic 144 bytes
```

其中 `SolverContactHeader4` 字段为：

```text
offset 0    type
offset 1    numNormalConstr
offset 2    numFrictionConstr
offset 3    flag                              // bit0 = eHAS_MAX_IMPULSE
offset 4    flags[4]                          // 每个 pair 的 force-threshold 等 flags
offset 8    numNormalConstr0..3               // 4 个 pair 各自真实 normal contact 数
offset 12   numFrictionConstr0..3             // 4 个 pair 各自真实 friction row 数
offset 16   restitution
offset 32   staticFriction
offset 48   dynamicFriction
offset 64   invMass0D0
offset 80   invMass1D1
offset 96   angDom0
offset 112  angDom1
offset 128  normalX
offset 144  normalY
offset 160  normalZ
offset 176  shapeInteraction[4]
```

`SolverContactBatchPoint*4` 和 `SolverContactFriction*4` 的偏移也已经固定：

```text
SolverContactBatchPointBase4, 96 bytes:
  0 raXnX, 16 raXnY, 32 raXnZ,
  48 velMultiplier, 64 scaledBias, 80 biasedErr

SolverContactBatchPointDynamic4, 144 bytes:
  Base4 + 96 rbXnX, 112 rbXnY, 128 rbXnZ

SolverFrictionSharedData4, 128 bytes:
  0 broken, 16 frictionBrokenWritebackByte[4],
  32 normalX[2], 64 normalY[2], 96 normalZ[2]

SolverContactFrictionBase4, 96 bytes:
  0 raXnX, 16 raXnY, 32 raXnZ,
  48 scaledBias, 64 velMultiplier, 80 targetVelocity

SolverContactFrictionDynamic4, 144 bytes:
  Base4 + 96 rbXnX, 112 rbXnY, 128 rbXnZ
```

`func70963` 的写入逻辑也能和源码逐项对齐：

```text
1. 读取 4 个 PxSolverContactDesc，判断 isDynamic。
   只要任一 pair 的 body1 是 dynamic，就用 Dynamic4 结构；
   只有 4 个 pair 全是 static/kinematic body1 时才用 Base4 结构。

2. 读取 4 个 body 的 linearVelocity/angularVelocity、invMass、sqrtInvInertia、
   bodyFrame0/bodyFrame1，并转置成 Vec4 lanes。

3. 对每个 friction patch index：
   totalContacts = max(clampedContacts0..3)
   写 header 与 appliedNormalForces，并把较少 contact 的 pair 用 0 padding。

4. 对每个 contact row：
   point/targetVel/separation/maxImpulse 从 4 个 ContactPoint 合并成 Vec4；
   ra = point - bodyFrame0.p，rb = point - bodyFrame1.p；
   raXn/rbXn 乘 sqrtInvInertia 后写入 BatchPoint；
   velMultiplier、scaledBias、biasedErr 用和 single-pair 相同的 response/restitution 公式计算。

5. 对每个 friction anchor：
   anchorCount 每个 pair 最多 2 个；
   若 material flag 有 eDISABLE_FRICTION，则该 pair 的 friction row 数为 0；
   若 eIMPROVED_PATCH_FRICTION 且 anchorCount == 2，static/dynamic friction 系数乘 0.5；
   每个 anchor 写两条 tangent row，因此 numFrictionConstr = maxAnchorCount * 2。
```

normal row 的字段可以进一步写成：

```text
normalX/Y/Z = transpose(contactBase[0..3].normal)
relNorVel = dot(normal, linVel0) - dot(normal, linVel1)

对每个 contact row:
  pointX/Y/Z = transpose(con0..con3.point)
  targetVelX/Y/Z = transpose(con0..con3.targetVel)
  separation = Vec4(con0..con3.separation)

  ra = point - bodyFrame0.p
  rb = point - bodyFrame1.p

  rawRaXn = cross(ra, normal)
  rawRbXn = cross(rb, normal)

  delAngVel0 = sqrtInvInertia0 * rawRaXn
  delAngVel1 = sqrtInvInertia1 * rawRbXn

  unitResponse =
    invMass0D0
    + angDom0 * dot(delAngVel0, delAngVel0)
    + invMass1D1
    + angDom1 * dot(delAngVel1, delAngVel1)   // dynamic body1 时

  vrel =
    relNorVel
    + dot(rawRaXn, angVel0)
    - dot(rawRbXn, angVel1)

  velMultiplier = unitResponse > 0 ? 1 / unitResponse : 0
  penetration = separation - restDistance
  scaledBias = max(maxPenBias, penetration * invDt * 0.8) * velMultiplier

  若 restitution 条件成立:
    scaledBias = 0
    targetVelocity = velMultiplier * vrel * restitution
  否则:
    scaledBias = -scaledBias
    targetVelocity = 0

  biasedErr = targetVelocity + scaledBias
              - (vrel - dot(contact.targetVel, normal)) * velMultiplier
```

写入 `SolverContactBatchPointBase4/Dynamic4` 时，结构体字段名叫
`raXnX/raXnY/raXnZ` 和 `rbXnX/rbXnY/rbXnZ`，但实际存的是
`sqrtInvInertia * cross(r, n)` 后的 solver-space 角速度响应向量。
这和 single-pair path 里的 `raXnSqrtInertia/rbXnSqrtInertia` 是同一层含义。

friction row 的写入也能明确到公式级：

```text
vrelTangentCandidate = relativeLinearVelocity - normal * relNorVel

如果 |vrelTangentCandidate|^2 > 0.0001:
  t0 = normalize(vrelTangentCandidate)
否则:
  t0 = normal 的稳定垂直 fallback

t1 = cross(normal, t0)

SolverFrictionSharedData4:
  broken = false
  frictionBrokenWritebackByte[0..3] = desc[i].frictionPtr + patchWritebackIndex * sizeof(FrictionPatch)
  normal[0] = t0
  normal[1] = t1
```

对每个 friction anchor，`func70963` 写两条 row：`f0` 对应 `t0`，
`f1` 对应 `t1`。每条 row 的公式相同：

```text
ra = rotate(bodyFrame0.q, frictionPatch.body0Anchors[index])
rb = rotate(bodyFrame1.q, frictionPatch.body1Anchors[index])
error = (bodyFrame0.p + ra) - (bodyFrame1.p + rb)

rawRaXt = cross(ra, tangent)
rawRbXt = cross(rb, tangent)

delAngVel0 = sqrtInvInertia0 * rawRaXt
delAngVel1 = sqrtInvInertia1 * rawRbXt

response =
  invMass0D0
  + angDom0 * dot(delAngVel0, delAngVel0)
  + invMass1D1
  + angDom1 * dot(delAngVel1, delAngVel1)   // dynamic body1 时

velMultiplier = response > 0 ? 0.8 / response : 0

vrel =
  dot(tangent, linVel0) + dot(rawRaXt, angVel0)
  - dot(tangent, linVel1) - dot(rawRbXt, angVel1)

target = dot(contact.targetVel, tangent) - vrel
bias = dot(tangent, error) * invDt

row.targetVelocity = -target * velMultiplier
row.scaledBias = (bias - target) * velMultiplier
row.velMultiplier = velMultiplier
row.raXn = delAngVel0
row.rbXn = delAngVel1   // dynamic body1 时
```

如果某个 lane 的 anchor 数不足当前 `j`，`maxImpulseScale` 会把该 lane 的 tangent
向量和 `velMultiplier` 归零；这就是 4 个 pair contact/friction 数不一致时的 padding
机制。`contactID == 0xffff` 时，friction row 的 target velocity 使用该 patch 的
`contactBase.targetVel` fallback，否则使用对应 contact 的 `targetVel`。

这说明 `func70963` 剩余的“batch field layout”已经缩小为更细的工程化工作：
把 `DyContactPrep4.cpp` 里 normal row 与 friction row 的每个 Vec4 写入偏移完整转成
本地结构体即可；它的尺寸、顺序、padding、dynamic/static 分支和主要字段含义已经对上。

同时排除了一条容易误读的支线：`func70937/func70941/func70942/func70947`
属于 `DySolverPFConstraints.cpp` / `DySolverControlPF.cpp` 的 Coulomb/PF 分支。
这些函数也实现 contact/friction 求解，但当前 Unity 资源 `PhysicsManager.frictionType = 0`
选的是 patch friction，不是 Coulomb 1D/2D，因此它们不是正式比赛主路径。

`func71272` 附近的上游流程要拆成两类，不应混在一起：

```text
contact finalization lane
  -> 读取 body/core 数据和 contact manager flags
  -> extractContacts 写入 ThreadContext.mContactBuffer
  -> getFrictionPatches 复用上一帧未 broken 的 friction anchors
  -> createContactPatches 按 material/restitution/friction/normal 合并 contact patch
  -> correlatePatches / growPatches 复用或生成 friction patch
  -> contact[15]/[11] 先填入 +/-Infinity sentinel
  -> 4 个 pair 走 func70963/createFinalizeSolverContacts4
  -> single pair 走 func71103/createFinalizeSolverContacts
  -> 写出 SolverContactHeader / SolverContactPoint / SolverContactFriction

generic 1D constraint lane
  -> constraint shader 生成最多 12 个 80-byte Px1DConstraint rows
  -> func71174/preprocessRows 排序、KEEPBIAS 处理、sqrtInvInertia、正交化
  -> func71176/SetupSolverConstraint 写出 SolverConstraint1D header 和 rows
```

这说明 `func71272` 附近同时有 contact task 和通用 constraint row prep 相关代码，
不能把所有 constraint 字样都误读成石壶接触点公式。剩余不确定处主要在
`func70574/func70576/func70030` 内部各个 inlined PhysX 模板如何进一步还原成干净代码，
以及 `func70963` 写出的 4-wide batch normal/friction row 如何逐偏移落成本地结构体。`func71103` 的 single-pair
contact finalization 已经能映射到 PhysX 的 `SolverContactHeader` /
`SolverContactPoint` / `SolverContactFriction` 字段和核心公式；`func71035/func71036`
又把 single-pair patch contact 的迭代冲量公式对到了 wasm；`func70917/func70919`
则把 4-wide block path 的动态/静态迭代公式也对到了 wasm。接触点生成的宏观流程已经不是未知：
它是 PhysX PCM + GJK/EPA + SAT/mesh midphase，再进入 patch friction contact solver，
不是冰壶项目自写二维闭式公式。

这比“只有 PhysX 字符串”更进一步：已经定位到 narrowphase 表、关键 shape contact generator、
contact finalization 表、manifold refresh/contact reduction/ContactBuffer 写入、
single-pair contact constraint 写出公式、single-pair 和 4-wide
solver 迭代公式，以及一条通用 1D constraint row 准备链。但它仍是 PhysX 通用求解器的数据结构，
不是冰壶专用闭式碰撞公式。要完全复现碰撞，需要继续把
`func70574/func70576/func70030`、`func70051` 和 `func70963` 的 normal/friction row 写入落成结构化代码，
或者用标准 PhysX 近似参数加样本验证。

这说明 PhysX 并不是完全“看不见”。更准确地说：正式碰撞求解已经进入 Unity/PhysX native wasm，
并且具体任务函数已经定位，但这些函数是数百到上千行的低层 contact/constraint 求解代码，
包含 contact patch、body data、constraint descriptor、batch/partition 等结构，距离可直接写进
本地模拟器的简洁“石壶碰撞公式”还有一层艰苦翻译。

我们已经足够构建很好的无碰撞 rollout 模拟器。对多壶碰撞，single-pair 的
normal/friction 约束写出与迭代公式、4-wide batch solver 的迭代公式都已经不再是黑箱；
convex-convex 的 face/edge 裁剪候选点生成也已经对到 PhysX 源码；stone-rink 的
triangle SAT、active edge、deferred contacts、edge/vertex cache 和 patch reduction
也已经对到源码规则。现在还不足以保证精确复现多壶碰撞后的速度/角速度转移，是因为这些
通用 PhysX 模板还没有完整落成本地可运行代码，`Plane` 使用的
`unity default resources:10209` 已经能定位为 Unity 内置 Plane/`New-Plane.fbx`
路径，但具体顶点顺序、三角形索引顺序和运行时 PhysX cooking 结果还没直接导出；
动态生成 convex MeshCollider 的 cooking 前 mesh、setter 顺序和 `RecalculateNormals`
已经锁定，但在 WebGL build 里的最终 cooked convex hull 结果，以及
restitution/friction combine 的运行细节仍需要碰撞样本或更深层 Unity/PhysX 行为验证。

因此当前正确边界是：碰撞半径、质量、材质、全局 PhysX 配置、narrowphase 表地址和关键
shape contact 函数号已经可恢复；没有再发现正式比赛路径里可替代 PhysX 的 C# 碰撞公式。
逐接触点 normal/friction constraint 的 single-pair 写出与 single/batch 迭代公式已经能对到
PhysX 源码和 wasm，convex-convex 候选点生成、convex-mesh triangle 接触生成和
mesh patch reduction 也已经对到源码级规则，但仍不是完整本地碰撞引擎；
除非继续把 `func70532/func70533/func70030/func70051` 以及 contact finalization 的
`func70963` normal/friction row 写入等落成可读模型，否则训练环境仍应先用近似碰撞并用
正碰/偏碰样本验证误差。

2026-07-08 的 pyphysx baseline 进一步说明：参数层面已经排除了 dt、坐标轴、plane
contactOffset、常见 scene flags、center height、contact offset、maxDepenetrationVelocity、
单一 restitution 等解释。旧 controlled collision 数据的主要问题是连续复用目标壶且没有记录
rotation/完整刚体状态；它不是最终 2cm 验收集。下一轮应以 fresh-page one-shot
collision 样本重新验证 pyphysx/工程化 PhysX 路径。
