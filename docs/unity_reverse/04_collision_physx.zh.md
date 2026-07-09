# 碰撞与 PhysX 总览

这页只放当前碰撞线的结论和阅读入口。旧的长过程文档已归档到：

```text
docs/archive/unity_reverse_superseded_20260709/04_collision_entry.zh.md
```

## 当前结论

我们不是完全不知道 Unity 碰撞机制。已经确认的大方向：

```text
Unity PhysX 4.1 / WebGL wasm
fixed timestep = 0.01s
contact generation = PCM
friction type = patch friction
solver iterations = 6 / 1
stone material = Bouncy, friction 0.6, restitution 1.0, combine Multiply
ice material = Ice, friction 0.02
formal stone runtime constraints = FreezeRotationX | FreezeRotationZ
formal stone collider = runtime convex MeshCollider
```

但是本地 pyphysx replay 还不是 Unity 首次碰撞帧的字段级 native-state 复刻。当前 best：

```text
unique-role current best:
  active RMSE ~= 3.86cm
  target in-play RMSE ~= 11.32cm

per-sample entrance-state oracle:
  active RMSE ~= 1.35cm
  target in-play RMSE ~= 1.48cm
  7 / 7 in-play pair 双终点进 2cm

visible-feature leave-one-out correction:
  active RMSE ~= 5.22cm
  target in-play RMSE ~= 30.98cm
  0 / 7 双终点进 2cm
```

所以，2cm oracle 只能证明缺口在入口 native state / contact-instance 状态，不是可直接训练的通用公式。

## 证据链

1. 单一全局参数不成立：`friction/restitution/radius/contactOffset/solver/lock_upright` 等扫描都不能把 target 拉进 2cm。
2. 尾段滑行不是主因：从本地 `0.02s/0.20s` snapshot 重跑 target tail，只调 `vx/vy` 可把 endpoint 压到毫米级。
3. 首帧冲量差很小但足够放大：需要约 `0.49 Ns` row 级修正，约本地主冲量 `2.35%`。
4. 最坏样本 `12003` 的 contact-frame 差约 `4.98deg`，接近 64 边 cooked hull 一个侧面步长。
5. `12005` 需要 `handoff_w_offset=-0.44rad/s` 才闭合，但全局 w offset 失败，说明它是 tangent/angular/contact cache 代理。

## 阅读入口

- 几何和 cooked hull：[`12_physx_convex_cooking.zh.md`](12_physx_convex_cooking.zh.md)
- contact generation 细节：[`05_physx_contact_generation.zh.md`](05_physx_contact_generation.zh.md)
- solver row 细节：[`06_physx_solver.zh.md`](06_physx_solver.zh.md)
- native state 是否一致：[`13_physx_native_state_equivalence.zh.md`](13_physx_native_state_equivalence.zh.md)

## 下一步

不要继续用 endpoint 大网格蒙参数。碰撞线的下一步是：

```text
1. 抓 Unity runtime 首次碰撞帧 native state。
2. 用 dump 出来的字段构造本地 trace-driven pyphysx/C++ replay。
3. 先比较 0.02s 碰后 active/target linear/angular velocity。
4. 速度对齐后再看 endpoint。
```

如果 0.02s 速度不对，继续查 `ContactBuffer`、friction anchor/cache、solver rows 和 shape local pose。
