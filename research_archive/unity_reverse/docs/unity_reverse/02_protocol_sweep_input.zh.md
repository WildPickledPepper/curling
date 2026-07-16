# 协议、坐标与扫冰输入

记录 Unity/协议坐标映射、MOTIONINFO、扫冰流程和 BESTSHOT/SWEEP/POSITION 等入口。

> 原长文档已封存：[`UNITY_REVERSE_ENGINEERING.zh.2026-07-07.archive.md`](../archive/UNITY_REVERSE_ENGINEERING.zh.2026-07-07.archive.md)。以后维护以本目录子文档为准。

## 已恢复的 Unity/协议坐标公式

这些公式来自 Unity 代码，不是样本拟合。

`DCP_HumanVSAI.SendMotionInfo` 对应 wasm `func60096`。它发送移动壶状态时使用：

```text
protocol_x  = teePosition.z - unity_position.z + 2.375
protocol_y  = teePosition.x - unity_position.x + 4.88
protocol_vx = -unity_velocity.z
protocol_vy = -unity_velocity.x
protocol_w  = unity_angularVelocity.y
```

现在已经把正式 controller 的方法映射也对上：

```text
AutoDCP.SendMotionInfo        -> wasm func60903
DCP_HumanVSAI.SendMotionInfo  -> wasm func60096
AutoDCP.ReadPosition          -> wasm func60888
```

`AutoDCP.ReadPosition`/`DCP.HandleMessage` 的 `POSITION` 分支反向写入时使用：

```text
body_x = protocol_x - 2.375
body_y = protocol_y - 4.88
```

因此 `2.375/4.88` 是代码硬编码的协议原点偏移，不是数据拟合常数。

### release_x / release_y / MOTIONINFO 触发几何证据

资产层已经恢复正式场景中的关键坐标，并且 `Start()` 的赋值链已经确认：

```text
origin_postion = mBlueBalls[0].transform.position
terminal       = GameObject.Find("Terminal")
teePosition    = terminal.transform.position
```

也就是说，`teePosition` 已经不再是未知项；它取 `Terminal.transform.position`
的世界坐标。正式场景中典型 world 坐标为：

```text
origin stone center x ~= -96.8542
origin stone center z ~= 54.1744
Terminal center x     ~= -69.2574
Terminal center z     ~= 54.1500
Midline center x      ~= -85.7116
Midline trigger half width ~= 0.147 / 2
stone collider radius      ~= 0.140875
```

因此从 `BESTSHOT` 刚释放时的协议初态应按世界坐标差得到：

```text
release_x ~= 54.1500 - 54.1744 + 2.375 = 2.3506
release_y ~= -69.2574 - (-96.8542) + 4.88 = 32.4768
```

`MOTIONINFO` 不是在石头中心到达 `Midline` 中心时发送。`CurlingStoneNew.OnTriggerEnter`
对应 wasm `func61031`：当碰到的 collider 名字是 `Midline` 时，它设置 `allowSweep=true`
并立刻调用当前 controller 的 `SendMotionInfo()`；当碰到 `Hogline2` 时再把
`allowSweep=false`。因此 `MOTIONINFO` 对应的是石壶 collider 首次进入 Midline trigger
盒子的离散物理帧。

```text
midline_center_y ~= -69.2574 - (-85.7116) + 4.88 = 21.3342
trigger_y ~= midline_center_y + stone_radius + midline_half_width
          ~= 21.3342 + 0.140875 + 0.0735
          ~= 21.548575
```

官方 `no_sweep_200.jsonl` 里 `motion_y` 约为 `21.52`，比几何触发阈值略小，
这与 `FixedUpdate=0.01s` 离散步、触发回调时刻和缺真实随机摩擦序列一致。用恢复的
几何默认值在前 10 条 no-sweep 样本上验证：

```text
release_x=2.3506, release_y=32.4768, stop_y=21.548575
state_rmse ~= 0.0947
pos_rmse   ~= 0.0202
```

小范围搜索仍会把 `stop_y` 推到 `21.52` 左右、把位置 RMSE 降到约 `1.5cm`，
但这不应再解释为 `teePosition` 未知；更合理的解释是普通采样缺 `RANDSEED`，
并且 `MOTIONINFO` 是 trigger overlap 后某个离散帧的读数。

`DCP_HumanVSAI.GetCurrentTrace` 对应 wasm `func60072`。它保存的是同一个坐标系，但没有协议偏移：

```text
trace_x = teePosition.z - unity_position.z
trace_y = teePosition.x - unity_position.x
```

对于 body 数组，顺序取决于 `firstShot`：

```text
firstShot == 0:
  body[4*i + 0], body[4*i + 1] = blue stone i trace_x, trace_y
  body[4*i + 2], body[4*i + 3] = red  stone i trace_x, trace_y

firstShot != 0:
  body[4*i + 0], body[4*i + 1] = red  stone i trace_x, trace_y
  body[4*i + 2], body[4*i + 3] = blue stone i trace_x, trace_y
```

`DCP_HumanVSAI.HandleHumanShot` 对应 wasm `func60092`。出手时 Unity 设置为：

```text
velocity = clamp(velocity, 0.0001, 6.0)
position = clamp(position, -2.23, 2.23)
rotation = clamp(rotation, -15.7, 15.7)

stone_list = (pGameState.WhiteToMove == 0) ? mBlueBalls : mRedBalls
stone_index = floor(pGameState.ShotNum * 0.5)
stone = stone_list[stone_index]

stone.transform.position.z = stone.transform.position.z - position
stone.rigidbody.velocity = (velocity, 0, 0)
stone.rigidbody.angularVelocity = (0, rotation, 0)
movingCurling = stone
shot = true
```

符号和 `SendMotionInfo` 能对上：正 Unity `velocity.x` 会变成负的协议 `motion_vy`；正 Unity `angularVelocity.y` 会变成正的协议 `motion_w`。

## 已恢复的 MOTIONINFO 尾段映射

官方协议的 `MOTIONINFO` 消息现在可以作为恢复物理 kernel 的验证锚点。`MOTIONINFO` 在移动壶到达中线时给出状态：

```text
motion_x, motion_y, motion_vx, motion_vy, motion_w
```

使用独立恢复模型 `tools/reverse/recovered_curling_motion.py` 时，最好的尾段 replay 约定是：

```text
speed = Newfrictionstep(0.001, (motion_vx, motion_vy), motion_w, 0.001)
motion_vx, motion_vy, motion_w = speed
x += motion_vx * 0.01
y += motion_vy * 0.01
```

换句话说，公共协议坐标可以直接积分尾段：

```text
sx = +1, sy = +1, sw = +1
position dt = 0.01 seconds
Newfrictionstep steptime parameter = 0.001
```

验证探针是：

```text
tools/reverse/probe_unity_tail_mapping.py
```

使用平均干摩擦、不复现 Unity RNG 的 no-sweep 经验验证结果：

```text
first 3 rows, dt=0.010: RMSE 0.0338 m, MAE 0.0300 m, max 0.0460 m
first 3 rows, dt=0.009: RMSE 1.4753 m
first 3 rows, dt=0.011: RMSE 1.5294 m
first 10 rows, dt=0.010: RMSE 0.0332 m, MAE 0.0288 m, max 0.0630 m
```

这强烈说明：对中线 `MOTIONINFO` 之后的无碰撞、无扫冰 rollout 来说，恢复出的 `Newfrictionstep` 公式和协议尾段坐标约定是正确的。剩余厘米级残差与已恢复的逐步摩擦随机噪声以及 Unity/JSON 四舍五入一致。
现在这个结论已经有自动测试保护：`tests/test_recovered_curling_motion.py`
读取 `data/calibration/no_sweep_200.jsonl` 的第一条官方 no-sweep 样本，要求
`dt=0.010` 的尾段 replay 误差低于 `0.06m`，同时要求 `dt=0.009` 和 `dt=0.011`
都退化到米级误差。这里的米级误差是故意的反证测试，不是可接受误差；它用来证明错误 timestep
会立刻破坏 replay，从而锁住协议速度符号和 Unity position integration timestep。

为继续追 `dt=0.010` 下的厘米级残差，新增了残差来源探针：

```powershell
D:\anaconda3\python.exe tools\reverse\probe_tail_residual_sources.py `
  data\calibration\no_sweep_200.jsonl --limit 1 --iterations 10
```

第一条 no-sweep 样本结果为：

```text
base_err=0.035264
fitted_err=0.010024
fitted_friction=0.001003106
```

也就是说，用平均干摩擦 `0.001` 时误差约 `3.53cm`；如果只允许给这一条样本拟合一个
等效常数摩擦，误差能降到约 `1.00cm`。这支持当前判断：普通 no-sweep 采样文件没有
`RANDSEED`，缺少逐 tick Unity friction noise 序列，导致无法做到 bit-level replay。
要“分毫不差”，需要 AutoDCP 记录里的 `RANDSEED` 或直接采集每 tick 随机摩擦/状态。

这个探针比较慢是预期现象：它把恢复出的精确 `Newfrictionstep` 当内核，逐 `0.001s`
摩擦步做自适应 Simpson 积分，再外套摩擦搜索。它适合回答“误差来自哪里”，不适合作为
训练内循环。训练侧应使用蒸馏/表格化/编译实现，精确原型负责做少量 golden replay 和回归测试。

探针现在还支持 recovered Unity RNG 的逐 tick 摩擦序列：

```powershell
D:\anaconda3\python.exe tools\reverse\probe_tail_residual_sources.py `
  data\calibration\no_sweep_200.jsonl --limit 1 --unity-seed 12345 --rng-skip 0
```

这里 `--unity-seed` 对应 AutoDCP record 里的 `RANDSEED`。`--rng-skip` 是从出手到当前
`MOTIONINFO` 已经消耗掉的 fixed tick 随机摩擦次数；如果从 AutoDCP 的 `BESTSHOT`
起整段 replay，这个值应为 `0`，如果只从中线 `MOTIONINFO` 尾段 replay，则必须跳过前半段
已经用掉的 RNG draw。扫冰尾段可再加 `--sweeping`，但更严格的 sweep window 仍应由
`SWEEP distance` 和中线/前卫线触发位置共同决定。

为减少对 `rng-skip` 的依赖，现在又补了从 `BESTSHOT` 直接跑到中线触发位置的探针：

```powershell
D:\anaconda3\python.exe tools\reverse\replay_bestshot_seeded.py `
  --v0 2.7614464179441924 --h0 -0.3361462010994136 --w0 0.9701978439310928 `
  --release-x 2.3506 --release-y 32.4768 --stop-y 21.548575

D:\anaconda3\python.exe tools\reverse\probe_bestshot_release_constants.py `
  data\calibration\no_sweep_200.jsonl --limit 10 `
  --release-x-min 2.32 --release-x-max 2.38 --release-x-step 0.02 `
  --release-y-min 32.45 --release-y-max 32.55 --release-y-step 0.025 `
  --stop-y-min 21.50 --stop-y-max 21.58 --stop-y-step 0.02
```

`replay_bestshot_seeded.py` 使用从 Unity 代码恢复出的正式 socket 出手映射：

```text
initial_x  = release_x + horizontal_offset
initial_y  = release_y
initial_vx = 0
initial_vy = -velocity
initial_w  = rotation
```

这里 `release_x/release_y` 已经有代码/资产来源；`stop_y` 是 Midline trigger overlap
阈值，仍会受固定步离散回调影响。前 10 条 no-sweep 样本中，用几何默认值可得到
`pos_rmse≈0.0202m`；小范围搜索可把位置 RMSE 降到约 `0.015m`，但 velocity/angular
velocity 残差仍主要受缺真实 `RANDSEED` 影响。

## 已恢复的扫冰流程

用户侧扫冰请求路径为：

```text
HumanInputController.OnSweepButtonClicked -> DCP_HumanVSAI.HandleHumanSweep
```

`HumanInputController.OnSweepButtonClicked`：

- 只有 `isHumanTurn` 为 true 时才生效；
- 读取 `sweepDistanceInput`；
- 如果输入为空或无法解析，默认用 `1.0`；
- 调用 `OnSweepRequested(distance)`。

`DCP_HumanVSAI.HandleHumanSweep(distance)`：

- 要求 `movingCurling != null`；
- 要求 `movingCurling.GetComponent<CurlingStoneNew>().allowSweep == true`；
- 记录请求距离日志；
- 设置场景里的 `Sweep` component：

```text
Sweep.isSweeping = true
Sweep.sweepDistance = distance
```

`Sweep` 对应 wasm `func60750..func60753`。字段为：

```text
sweepSpeed:    float  // default 2.0
movementDist:  float  // default 0.25
isSweeping:    bool
sweepDistance: float
isMovingFor:   bool   // default true
target:        GameObject
offset:        Vector3
sumnewZ:       float
```

`.ctor` 和 `Start` 的常量也已经解码：

```text
Sweep..ctor:
  sweepSpeed   = 2.0
  movementDist = 0.25
  isMovingFor  = true

Sweep.Start:
  sumnewZ = 0
  target  = null
  offset  = (1.0, -0.1, 0.0)
```

`Sweep.Sweeper` 在 `FixedUpdate` 中调用，并读取 `Time.deltaTime` 来让视觉扫刷围绕目标壶移动。
在固定物理帧里它通常等于本帧物理时间，但函数调用名本身是 `Time.get_deltaTime`。恢复出的振荡逻辑是：

```text
direction = isMovingFor ? +2 : -2
sumnewZ += Time.deltaTime * sweepSpeed * movementDist * direction

if sumnewZ > movementDist:
    isMovingFor = false
elif sumnewZ < -movementDist:
    isMovingFor = true

sweeper.position = target.position + offset + (0, 0, sumnewZ)
```

停止逻辑也在 `Sweep.Sweeper` 中。现在已经用 `tools/reverse/resolve_metadata_refs.py`
把 metadata slot 解析回了字符串名，因此这个窗口不是匿名判断：

```text
target.position.x < Hogline2.position.x
target.position.x < Midline.position.x + sweepDistance
```

如果任一条件失败，Unity 清除：

```text
Sweep.isSweeping = false
Sweep.sweepDistance = 0
```

这意味着 `sweepDistance` 控制场景里的 `Sweep.isSweeping` 标志保持多久；它不是摩擦的连续倍增/倍减系数。

资产层也验证了这两个 trigger 是普通 `BoxCollider(isTrigger=true)`。正式场景里典型坐标为：

```text
Hogline1.x ~= 3.695
Midline.x  ~= 14.58
Hogline2.x ~= 25.57
```

因此 `SWEEP distance` 的实际窗口可以近似写成：

```text
start: moving stone hits Midline
end:   moving_stone.x >= min(Midline.x + sweepDistance, Hogline2.x)
max physical sweep window ~= 25.57 - 14.58 = 10.99 m
```

也就是说，`distance` 再大也不会让扫冰越过 `Hogline2`。

转成协议 `y` 坐标后，工具中固定为：

```text
midline_center_y  ~= 21.3342
midline_trigger_y ~= 21.548575
hogline2_y        ~= 10.3442

active sweep iff:
  protocol_y <= midline_trigger_y
  protocol_y > max(midline_center_y - sweepDistance, hogline2_y)
```

这里 `midline_trigger_y` 是石壶 collider 首次 overlap Midline trigger 的读数位置；
`midline_center_y` 则来自 `Sweep.Sweeper` 里直接比较 `target.position.x < Midline.position.x + sweepDistance`。
因此如果 `SWEEP` 命令能在 `MOTIONINFO` 触发后立刻进入 Unity，实际低摩擦窗口会比
请求的 `sweepDistance` 多出约 `midline_trigger_y - midline_center_y ~= 0.214m` 的前沿量。
这个规则已落成：

```text
tools/reverse/recovered_sweep_window.py
```

并接入尾段残差探针：

```powershell
D:\anaconda3\python.exe tools\reverse\probe_tail_residual_sources.py `
  data\calibration\sweep_200.jsonl --limit 3 --sweep-field requested_sweep_distance
```

注意：`sweep_200.jsonl` 中 `requested_sweep_distance=0` 的样本通常有
`sent_sweep=false`，这表示 Unity 没收到 `SWEEP 0`，不能模拟成零距离扫冰窗口。
此外 socket 采样是 AI 收到 `MOTIONINFO` 后再回 `SWEEP`，存在消息/帧延迟；AutoDCP
recorded replay 在 `OnTriggerEnter(Midline)` 里直接 `ReadMotionInfoFromRecord`，更适合验证
“无网络延迟”的 sweep window。

`Sweep.FixedUpdate` 根据当前 scene name 找不同 controller/sweeper target：

```text
FastGame  -> GameObject.Find("FastDCP").GetComponent<FastDCP>().movingCurling
AutoGame  -> GameObject.Find("AutoDCP").GetComponent<AutoDCP>().movingCurling
HumanVsAI -> GameObject.Find("DCP_HumanVSAI").GetComponent<DCP_HumanVSAI>().movingCurling
default   -> GameObject.Find("DCP").GetComponent<DCP>().movingCurling
```

对应 byte offsets 分别是：

```text
FastDCP.movingCurling      // 0xD4 = 212
AutoDCP.movingCurling      // 0xF0 = 240
DCP_HumanVSAI.movingCurling // 0x104 = 260
DCP.movingCurling          // 0xE8 = 232
```

所以扫刷 target 就是当前运动壶。

此外，`Sweep.FixedUpdate` 会根据当前运动壶和 `Hogline2` 的 Unity `position.x` 比较来开关
扫刷 Renderer：

```text
sweeperRenderer.enabled = movingCurling.position.x < Hogline2.position.x
```

对本地模拟器的实际含义：

- 请求扫冰控制低摩擦模式持续多久；
- 活跃扫冰期间摩擦大小固定在约 `0.0006`，不与请求距离成比例；
- 是否允许扫冰由 `CurlingStoneNew.allowSweep` 控制，而它由 trigger zone 切换。

## 已恢复的出手输入映射

`DCP_HumanVSAI.HandleHumanShot` 对应 wasm `func60092`。输入 clamp 为：

```text
velocity:          [0.0001, 6.0]
horizontal offset: [-2.23, 2.23]
rotation:          [-15.7, 15.7]
```

它用下面方式从蓝/红壶列表里选当前壶：

```text
stone_index = floor(current_shot_index * 0.5)
```

然后：

- 用请求的 horizontal offset 放置选中的壶；
- 用请求的 `velocity` 设置 `Rigidbody.velocity`；
- 用请求的 `rotation` 设置 `Rigidbody.angularVelocity`；
- 标记 `movingCurling` 和出手进行中状态。

Unity 内部 `Vector3` 轴约定已经通过 `HandleHumanShot` 和 `SendMotionInfo` 对上；公共协议尾段约定也已经锁定：`motion_x/y/vx/vy/w` 可以直接用 `position dt = 0.01` 和 `Newfrictionstep(..., steptime = 0.001)` replay。

### 正式 BESTSHOT 协议入口

正式比赛/机器人 socket 入口不是 `HandleHumanShot`，而是各 controller 的 `HandleMessage`：

```text
DCP.HandleMessage            -> wasm func61066
DCP_HumanVSAI.HandleMessage  -> wasm func60060
FastDCP.HandleMessage        -> wasm func60175
AutoDCP.HandleMessage        -> wasm func60864
```

`DCP`、`DCP_HumanVSAI` 和 `FastDCP` 的 `BESTSHOT` 分支已经逐行对过，核心释放逻辑一致。消息会先做：

```text
Regex.Replace(message, "[\s]+", " ").Trim().Split(' ')
```

然后要求消息所属玩家颜色等于当前 `pGameState.Player`。`BESTSHOT` 参数读取为：

```text
BESTSHOT velocity horizontal_offset rotation
```

注意：C# 数组对象在 wasm 里有对象头，所以反编译中看到的 `command[5]、command[6]、command[7]`
实际对应 split 后的第 1、2、3 个参数。

正式协议入口的 clamp 是：

```text
velocity:          if velocity < 0.0001 then 1.0; if velocity > 6.0 then 6.0
horizontal offset: [-2.23, 2.23]
rotation:          [-15.7, 15.7]
```

这和人类 UI 的 `HandleHumanShot` 不完全一样：人类 UI 的速度下限是 `0.0001`，正式 `BESTSHOT`
入口会把低于 `0.0001` 的速度改成 `1.0`。课程文档里写的 `0 <= v0 <= 6` 在 Unity release
实现中更准确应理解为：正常非负速度会原样进入，极小/负数异常速度会被保护性改成 `1.0`。

正式 `BESTSHOT` 的刚体释放流程是：

```text
stone_list = (pGameState.WhiteToMove == 0) ? mBlueBalls : mRedBalls
stone_index = floor(pGameState.ShotNum * 0.5)
stone = stone_list[stone_index]

stone.SetActive(true)
stone.rigidbody.position.z = stone.rigidbody.position.z - horizontal_offset
stone.collider.material.staticFriction = 0.0
stone.collider.material.dynamicFriction = 0.0
stone.rigidbody.velocity = (velocity, 0, 0)
stone.rigidbody.angularVelocity = (0, rotation, 0)
movingCurling = stone
shot = true
```

这里新增确认了一点：出手瞬间，当前运动壶的 `Collider.material` 摩擦被置为 `0.0/0.0`。
随后如果撞到其他壶，`CurlingStoneNew.OnCollisionEnter` 会把材质摩擦改回 `0.6/0.6`，并把
`mCollision = true`，从而停止自定义 `Newfrictionstep` 单壶积分，转入 Unity PhysX 碰撞路径。

### 正式 SWEEP 协议入口

`SWEEP` 分支同样在 `DCP`、`DCP_HumanVSAI`、`FastDCP` 中确认。消息形式为：

```text
SWEEP distance
```

生效条件是：

```text
消息玩家颜色 == 当前 pGameState.Player
movingCurling.GetComponent<CurlingStoneNew>().allowSweep == true
```

满足条件后，Unity 执行：

```text
GameObject.Find("Broom").GetComponent<Sweep>().isSweeping = true
Sweep.sweepDistance = parsed_distance
```

如果 `distance` 解析失败，会打印 `distance invalid`；反编译路径仍会把本地临时 float 写入
`sweepDistance`，实际等价于不要依赖非法输入。训练/比赛代码应始终发送合法浮点数。

结合前面 `FixedUpdate` 中恢复出的摩擦逻辑，`SWEEP distance` 的物理含义不是直接“多滑
distance 米”，而是打开低摩擦模式，直到 `Sweep.FixedUpdate` 根据运动壶和请求距离关闭扫冰。

### POSITION / RESETPOSITION 坐标入口

`POSITION` 分支会把协议中的 16 个壶坐标写回内部 `body` 数组。转换式是：

```text
body_x = protocol_x - 2.375
body_y = protocol_y - 4.88
```

这和 `SendMotionInfo`、`GetCurrentTrace` 的坐标公式闭合：

```text
protocol_x = trace_x + 2.375
protocol_y = trace_y + 4.88
```

`DCP.HandleMessage` 里还存在 `RESETPOSITION` 和 `RESETSTATE` 分支。它们主要用于课程平台/调试重置，
不是正式比赛 AI 的常规动作；但从逆向角度看，`RESETPOSITION` 使用的坐标转换同样是上面的
`-2.375/-4.88`。

### READY / NAME / RESET 类协议

这批分支已经确认不会改写主物理公式：

```text
NAME / CONNECTNAME
  -> 记录玩家名、更新等待界面显示

READYOK / READYOKNAME / READYOKCONNECTNAME
  -> 按 Player1/Player2 设置 player1Ready/player2Ready

RESETSTATE
  -> 调 ResetState 类逻辑，主要服务课程平台/调试重置

RESETPOSITION
  -> 当前玩家合法时，把传入坐标按 -2.375/-4.88 写入 body，准备重设局面
```

`READY/NAME` 影响的是开始前握手和 UI；`RESET*` 是外部调试/平台控制入口。它们不改变
`BESTSHOT/SWEEP` 到刚体释放、`Newfrictionstep`、扫冰摩擦和停壶状态机这些主比赛物理路径。

### 经验 BESTSHOT 到 MOTIONINFO 探针

这一节只应当作为验证/备用方案。权威 release mapping 已经从 `HandleMessage` 的正式
`BESTSHOT` 分支和 `HandleHumanShot` 的 UI 分支恢复；数据拟合不是主来源，也不应该成为主模拟器设计。

辅助工具：

```text
tools/reverse/probe_action_to_motioninfo.py
```

它拟合一个小的二次最小二乘模型：

```text
BESTSHOT(v0, h0, w0) -> MOTIONINFO(x, y, vx, vy, w)
```

在 `data/calibration/no_sweep_200.jsonl` 上，使用 190 条 in-play no-sweep 样本：

```text
motion_x:  RMSE 0.000107
motion_y:  RMSE 0.005249
motion_vx: RMSE 0.000045
motion_vy: RMSE 0.001221
motion_w:  RMSE 0.000428
final_x:   RMSE 0.024141
final_y:   RMSE 0.032637
```

粗略关系：

```text
motion_x ~= h0 + 2.346 plus spin curl before the middle line
motion_vy / v0 ~= -0.629
motion_w / w0 ~= 0.337
motion_vx / w0 ~= 0.010
```
