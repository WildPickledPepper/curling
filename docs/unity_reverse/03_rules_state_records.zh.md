# 规则、状态机与记录回放

记录规则阈值、每壶结束状态机、SendGameState，以及 AutoDCP 记录/回放格式。

> 原长文档已封存：[`UNITY_REVERSE_ENGINEERING.zh.2026-07-07.archive.md`](../archive/UNITY_REVERSE_ENGINEERING.zh.2026-07-07.archive.md)。以后维护以本目录子文档为准。

## 已恢复的规则阈值

`DCP_HumanVSAI.GetStoneState` 对应 wasm `func60070`。它使用固定规则阈值：

```text
side bounds:       -2.23 < x < 2.23
valid y range:     -4.735 < y < 39.475
near hog/guard y:  -2.015, 0.145, 5.645
house radius:      sqrt(x*x + y*y) < 2.015
center line touch: abs(x) <= 0.145
```

对应 enum 已从 `dump.cs` 恢复：

```csharp
STATE_RINK = 1
STATE_PLAYAREA = 2
STATE_FREEGUARD = 4
STATE_HOUSE = 8
```

`AutoDCP`、`DCP`、`DCP_HumanVSAI`、`FastDCP` 的 `GetStoneState` 都映射到同一个
wasm 函数 `$f60070`，所以这组区域阈值是所有正式 controller 共用的。

`DCP_HumanVSAI.IsTouchingCenterLine` 对应 wasm `func60071`，精确为：

```text
abs(x) <= 0.145
```

`DCP_HumanVSAI.IsAllCurlingStoped` 对应 wasm `func60089`。它遍历两边壶列表，只要有任意活跃壶满足：

```text
velocity.x^2 + velocity.y^2 + velocity.z^2 > 0.000001
```

就返回 false。所以 Unity 的停止检查是平方速度阈值 `1e-6`，不是 `Newfrictionstep` 内部使用的 `0.01` 线速度 cutoff。

`DCP_HumanVSAI.UpdateState` / `DCP.UpdateState` 还包含 R7/中线相关的规则修正逻辑。
已确认字段：

```text
GameStateEx.ShotNum     // 0x08
GameStateEx.WhiteToMove // 0x18
GameStateEx.body        // 0x1C
GameStateEx.Player      // 0x20
```

`UpdateState` 每次会把 Unity 场景里的活跃壶位置写回 `GameStateEx.body`。写入坐标使用 tee 偏移：

```text
body_x = teePosition.z - stone.position.z
body_y = teePosition.x - stone.position.x
```

如果壶不活跃，或写回后不在有效保留区域：

```text
-2.23 < body_x < 2.23
-2.015 < body_y < 5.645
```

Unity 会把对应 `body` 槽清零，把壶移动回初始/备用位置，并 `SetActive(false)`。
所以出界/无效壶不是只在最终计分时忽略，而是在 `UpdateState` 中被写回、清零、失活。

关键条件能读出：

```text
只在 ShotNum >= 2 后进入检查；
按 ShotNum % 2 的同色/同队 parity 扫描既有壶；
候选壶位置要求：
    0.145 < y < 5.645
   -2.23 < x < 2.23
    sqrt(x*x + y*y) >= 2.015
中心线接触判断：
    abs(x) <= 0.145
```

当检测到相关违规时：

```text
DCP/DCP_HumanVSAI 会调用 SetStonesByBody(...) 回滚/重设 body；
非人类选择路径会发送 "CENTERLINE_VIOLATION" 给对应 Client；
HumanVsAI 且人类是被违规方时，调用 HumanInputController.ShowCenterlineViolationPanel(...)
让人类选择 keep/reset。
```

这段规则对单壶 rollout 不影响，但对完整比赛状态 replay 和训练环境的规则层很重要。

`CENTERLINE_CHOICE` 的正式 socket 分支也已经确认：

```text
CENTERLINE_CHOICE RESET
  -> 清 waitingForCenterlineChoice 和 timeout
  -> 把 r7BackupBodyState 复制回 GameStateEx.body
  -> 保存 lastBodyState
  -> SetStonesByBody(r7BackupBodyState)
  -> SendGameState()
  -> Invoke(SendGoCommand, 16.0)

CENTERLINE_CHOICE KEEP
  -> 清 waitingForCenterlineChoice 和 timeout
  -> 保留当前 GameStateEx.body
  -> 清掉当前备份引用
  -> SendGameState()
  -> Invoke(SendGoCommand, 16.0)
```

`DCP/FastDCP/DCP_HumanVSAI` 的主行为一致；`FastDCP` 额外会在处理后把
`Time.timeScale` 设回 `1.0`。该消息只有在 `waitingForCenterlineChoice == true`
且消息玩家等于 `centerlineViolatedTeam` 时才会生效。超时未回复时，`Update` 路径默认按
`KEEP` 继续。

`DCP_HumanVSAI.GetScore` 对应 wasm `func60074`。它不是调用 Unity 物理，而是直接读取
`GameStateEx.body` 计分。恢复出的逻辑：

```text
blue/even slots: body index 0,2,4,...
red/odd slots:   body index 1,3,5,...

忽略 x 和 y 同时接近 0 的空槽；
只考虑 house 内壶：sqrt(x*x + y*y) <= 2.015；
先找偶数槽最近距离 f；
再找奇数槽最近距离 g；

if f < g:
    score = 偶数槽中 distance < g 的壶数
elif f > g:
    score = - 奇数槽中 distance < f 的壶数
else:
    score = 0

if firstShot == 1:
    score = -score
```

所以 Unity 的局分是标准“谁最近，数到对方最近壶为止”的冰壶计分；符号最后会按先后手/颜色视角翻转。

## 已恢复的每壶结束状态机

正式比赛的“这一壶什么时候结束、什么时候轮到下一方、什么时候计分”不在单壶物理
`FixedUpdate` 里，而在各 controller 的 `Update` 里完成：

```text
DCP.Update       -> wasm func61097
FastDCP.Update   -> wasm func60201
AutoDCP.Update   -> wasm func60908
```

`DCP_HumanVSAI` 的普通比赛路径与上面同源，但还混有人类 UI 和 trace replay 分支；训练环境优先模拟
`DCP/FastDCP/AutoDCP` 的正式 AI-vs-AI 主路径即可。

主状态流已经能读成下面的伪代码：

```text
if !gameOver:
    Dispatch queued socket messages

if waitingForCenterlineChoice:
    centerlineChoiceTimeout += Time.unscaledDeltaTime
    if timeout reached:
        default to KEEP
        waitingForCenterlineChoice = false
        centerlineChoiceTimeout = 0
        if !recordedGame:
            SendGameState()
            Invoke(SendGoCommand, delay)

if shot && movingCurling != null:
    current_stone = stone_list[floor(ShotNum * 0.5)]
    if distance(current_stone.position, release_origin) > 1.0
       and current_stone.velocity.sqrMagnitude < 0.000001:
        log "Curling stop"
        current_stone.collider.material.staticFriction = 0.6
        current_stone.collider.material.dynamicFriction = 0.6
        Sweep.isSweeping = false

        if IsAllCurlingStoped():
            shot = false
            ShotNum += 1
            if recordedGame:
                SetStonesByBody(record_body)

            if ShotNum == 16:
                UpdateState()
                score[End] = GetScore()
                SendGameState()
                choose first shot for next end from score sign
                ShotNum = 0
                End += 1
                UpdateScoreBoard()
                if End < totalGame:
                    ResetStones()
                    UpdateState()
                    SendGameState()
                    SendGoCommand/NewGame after delay
                else:
                    SendTotalScore()
                    deactivate all stones
                    gameOver = true
            else:
                WhiteToMove ^= 1
                UpdateState()
                if !waitingForCenterlineChoice && !recordedGame:
                    SendGameState()
                    Invoke(SendGoCommand, delay)
```

关键细节：

- 当前壶必须从释放点实际移动超过 `1m`，才会进入“停壶收尾”判断。这避免释放前或刚激活时的零速度误判。
- 单壶停止阈值和全场停止阈值都是 `velocity.sqrMagnitude < 1e-6` 这一量级。
- 停壶后会强制关闭 `Sweep.isSweeping`，并把当前壶 collider 摩擦改回 `0.6/0.6`。
- 非第 16 壶时只翻转 `WhiteToMove`、调用 `UpdateState`、广播局面、延迟发下一次 `GO`。
- 第 16 壶时先 `UpdateState`，再 `GetScore` 写入 `score[End]`，再根据本局得分决定下一局先后手。
- `FastDCP` 的中线选择超时约为 `1s`；`DCP` 路径约为 `5s`。正式训练环境可以把它抽象成
  “CENTERLINE_CHOICE 未回复时默认 KEEP”。

`SendGoCommand` 行为也已确认。它会先清空 `movingCurling`，然后按当前 `WhiteToMove/Player`
给当前方 client 发送 `GO`，最后清掉 `shot` 并打开出手超时计数。`DCP_HumanVSAI` 如果轮到人类，
不会发 socket `GO`，而是打开 `HumanInputController` 的输入面板；这属于 UI 分支。

`Dispatch` 只是在 `Update` 里从 socket message queue 取消息并调用对应 `HandleMessage`：

```text
queue.TryDequeue(out message) -> HandleMessage(message)
```

因此本地训练环境的最小规则层可以不复刻线程/队列，只需要按同样顺序处理：

```text
BESTSHOT/SWEEP/CENTERLINE_CHOICE messages
-> physics rollout
-> stop check
-> UpdateState
-> GetScore if ShotNum == 16
-> SendGameState-equivalent observation
-> next GO/action request
```

## 已恢复的 SendGameState 协议

`SendGameState` 是 Unity 每次广播局面给 AI 的主出口：

```text
DCP.SendGameState       -> wasm func61069
FastDCP.SendGameState   -> wasm func60177
AutoDCP.SendGameState   -> wasm func60866
DCP_HumanVSAI.SendGameState -> wasm func60063
```

它主要发三类文本消息：

```text
POSITION x1 y1 x2 y2 ... x16 y16
SCORE score
SETSTATE ShotNum End Player WhiteToMove
```

`POSITION` 使用 `GameStateEx.body` 的规则坐标再加回协议偏移：

```text
if body_x == 0 and body_y == 0:
    send "0 0"
else:
    send_x = body_x + 2.375
    send_y = body_y + 4.88
```

`SETSTATE` 的前三个整数来自 `GameStateEx.ShotNum`、`GameStateEx.End`、`GameStateEx.Player`，
最后一个布尔/整数来自 `GameStateEx.WhiteToMove`。在 `DCP` 的特殊总局数分支里，
当 `totalGame == 7` 时第三项会发送 `-1`，这是平台/赛制控制分支，不影响单壶物理。

`SCORE` 只在完成一局或需要同步比分时发送。`FastDCP/DCP` 会对两个 client 发送相反视角的 score：
一方收到 `score`，另一方收到 `-score`。这解释了为什么 Unity 内部 `GetScore` 的符号还会再经过
先后手/玩家视角处理，不能把 socket 里某一方收到的 `SCORE` 直接当作全局绝对分。

## AutoDCP 记录/回放格式

`AutoDCP` 是唯一明确支持记录和复现随机种子的 controller。它的相关字段为：

```text
recordedGame      // 是否回放已有记录
recordParser      // 当前写记录的 INIParser
recordLoader      // 回放读取的 INIParser
autoGameRecorder  // AutoGame 总记录/排名相关 INIParser
```

每壶使用一个 section，section 名由当前局和当前壶拼成：

```text
section = End.ToString("D2") + ShotNum.ToString("D2")
```

例如第 0 局第 3 壶是 `0003`。`SendGameState` 每次还会写：

```text
[LASTSTATE]
LASTSTATE = section
```

每个 section 中已经确认的 key：

```text
BESTSHOT = BESTSHOT velocity horizontal_offset rotation
RANDSEED = UnityEngine.Random.seed
SWEEP    = SWEEP distance
POSITION = POSITION ...
SCORE    = SCORE ...
SETSTATE = SETSTATE ShotNum End Player WhiteToMove
TRACE    = frame0_32floats frame1_32floats ...
```

`AutoDCP.HandleMessage` 的 wasm 证据已经对齐到字段偏移：`recordedGame` 在 `0x54`，
反编译里对应 `a[84]:ubyte`。因此 `BESTSHOT` 分支可以明确分成两边：

```text
recordedGame == false:
  recordParser.WriteValue(section, "BESTSHOT", "BESTSHOT v h w")
  释放刚体
  recordParser.WriteValue(section, "RANDSEED", UnityEngine.Random.seed)

recordedGame == true:
  释放刚体
  seed = recordLoader.ReadValue(section, "RANDSEED", "0")
  UnityEngine.Random.InitState(Convert.ToInt32(seed))
```

其中字符串/方法映射来自：

```text
d_[28651] -> "BESTSHOT"
d_[32223] -> "RANDSEED"
f_phbc    -> UnityEngine.Random.get_seed
f_lhbc    -> UnityEngine.Random.InitState
f_tclc/f_ddlc -> INIParser.WriteValue
f_sclc    -> INIParser.ReadValue
```

这里的顺序有个细节：`RANDSEED` 是在刚体释放代码之后写入/读取的，但在下一次
`FixedUpdate` 摩擦噪声之前完成，所以从 `BESTSHOT` 开始整段 replay 时，使用 record
里的 `RANDSEED` 且 `rng-skip=0` 是合理的。

换句话说，`BESTSHOT` 分支在 `recordedGame == false` 时，先把原始 `BESTSHOT v h w`
写入当前 section。释放刚体之后，它会立刻写：

```text
RANDSEED = UnityEngine.Random.seed
```

`recordedGame == true` 时，`BESTSHOT` 分支会从同一个 section 读取 `RANDSEED`，然后执行：

```text
UnityEngine.Random.InitState(Convert.ToInt32(RANDSEED))
```

因此 AutoGame 回放模式不是“重放每一帧轨迹”，而是用同样动作、同样 sweep、同样 Unity RNG seed
重新跑物理。

`AutoDCP.ReadMotionInfoFromRecord` 这个名字比较误导。它不是读取 `MOTIONINFO` 数值；实际逻辑是：

```text
section = End.ToString("D2") + ShotNum.ToString("D2")
sweep_message = recordLoader.ReadValue(section, "SWEEP", " ")
fake_player = "Player" + (pGameState.Player + 1)
HandleMessage((fake_player, sweep_message))
```

这个函数在 `CurlingStoneNew.OnTriggerEnter(Midline)` 的 AutoGame recorded 分支调用。
也就是说，壶过中线后，Unity 从记录文件取本壶的 `SWEEP` 命令，再走正式 `SWEEP` 协议入口。
这与普通比赛中 AI 在收到 `MOTIONINFO` 后自行发 `SWEEP` 的流程等价。

这给训练验证一个很好的方向：如果我们能生成或捕获 AutoGame 记录文件，就能得到
`BESTSHOT + RANDSEED + SWEEP` 的可复现实验，而不必依赖只含终点的数据盲猜摩擦噪声。

现在已经补了本地解析工具：

```powershell
D:\anaconda3\python.exe tools\reverse\parse_autodcp_record.py path\to\record.save
D:\anaconda3\python.exe tools\reverse\parse_autodcp_record.py path\to\record.save --jsonl --friction-preview 3
```

它会按四位 section（如 `0003`）抽出 `BESTSHOT`、`RANDSEED`、`SWEEP`、`POSITION`、
`SETSTATE`、`SCORE`、`TRACE`，并可用 `tools/reverse/recovered_unity_random.py` 同源的 RNG
预览该 seed 下的 Unity 摩擦噪声。当前工作区和单机版目录里没有发现现成 `.save`
录像；拿到 AutoDCP record 后，这个工具就是把记录转成 replay/golden-test 输入的入口。

AutoDCP 的历史读取函数也已经对上：

```text
ReadPosition -> 读取 section/POSITION，写回 body 坐标
ReadState    -> 读取 section/SETSTATE，写回 ShotNum/End/Player/WhiteToMove
ReadBestshot -> 读取 section/BESTSHOT，伪造成 Player 消息并调用 HandleMessage
ReadTrace    -> 读取 section/TRACE，填充 lTrace
ReadScore    -> 读取 section/SCORE，写回 score
```

`ReadTrace` 的格式也已经确认：它从同一 section 读取 `TRACE`，对空白做 normalize/split，
每 32 个 float 组成一帧，填充 `List<float[]> lTrace`。每帧 32 个数就是 16 个石壶的
`trace_x/trace_y`，坐标来自 `GetCurrentTrace`，即 `teePosition - worldPosition`，
没有协议层的 `+2.375/+4.88` 偏移。

`TRACE` 是历史播放/可视化用的轨迹列表，不是正式 AI 交互里必需的物理输入；但它是后续
做逐帧对齐验证的好材料。真正复现出手的核心仍然是 `BESTSHOT + RANDSEED + SWEEP`。

AutoDCP 还有一个会影响运行速度但不改变物理公式的静态设置：

```text
AutoDCP.timescale = 16.0
Awake -> Time.timeScale = AutoDCP.timescale
```

所以 AutoGame 自动赛程默认把 Unity 时间加速到 `16x`。这会影响真实等待时间和 `Invoke` 延迟，
但 `FixedUpdate` 中每个物理 tick 仍然调用同一个 `Newfrictionstep(..., 0.001)` 和同一个随机摩擦逻辑。
本地训练环境应复现固定 tick 的物理序列，不应把 `timescale=16` 当成新的摩擦或速度参数。

AutoDCP 的 UI 入口也已经从 wasm 函数映射确认。`AutoDCP.Start -> func60907` 会给等待面板按钮绑定：

```text
WaitingCanvas/Panel/StartGame    -> AutoDCP.NewGame
WaitingCanvas/Panel/StartHisGame -> AutoDCP.NewGameFromHistory
WaitingCanvas/Panel/SendIsReady  -> AutoDCP.SendIsReady
WaitingCanvas/Panel/ReadRecord   -> AutoDCP.ReadReacord
```

其中 `ReadReacord -> func60887` 和 `NewGameFromHistory -> func60895` 都走 `OpenFileName` 文件对话框，
初始目录是 `Directory.GetCurrentDirectory() + "/Records"`，过滤器是
`Record Files(*.save)\0*.save\0\0`。`NewGame -> func60894` 会新建比赛 `.save`，并打开
`autoGamePath + "\autoGame.save"` 作为自动赛程总记录。

当前单机 WebGL 包的限制是：BuildSettings 只有 `MenuScene`、`MotionTestScene`、`GameScene`、
`GameScene4Games`、`GameSceneNoLimit`、`GameSceneDebug`、`HumanVsAI`，没有 `AutoGame` 或
`FastGame` 场景；已打包 scene 里也没有挂着 `AutoDCP` 的 GameObject。因此 AutoDCP 记录/回放
代码是真的，但当前 UI 路径不能直接进入这个 controller。普通 DCP/HumanVsAI 场景里的
`ReadRecord` 和 `StartHisGame` GameObject 默认 inactive。

AutoDCP 的记录目录按 scene name 选择：

```text
GameScene       -> Records/8Games/
GameScene4Games -> Records/4Games/
FastGame        -> Records/4Games/
AutoGame        -> Records/4Games/
```

自动赛程结束时会更新 `AutoGame/rank.csv`，字段头为：

```text
团队名称,团队排名,小组积分,备注
```

这部分是赛程/排名外壳；目前没有证据显示它改写 `Newfrictionstep`、扫冰摩擦、碰撞材质或规则阈值。
