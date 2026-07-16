# Unity WebGL 运行时注入探针

这页记录“在浏览器里旁路收集 Unity 运行时信息”的方案。目标不是 patch 游戏逻辑，而是在
Unity WebGL 正常运行时抓证据，补上 socket 采样看不到的虚拟文件、WASM table/memory 和关键
函数入口信息。

## 工具位置

```text
tools/reverse/unity_webgl_runtime_probe.js
```

脚本已通过 `node --check` 语法检查。它默认只安装 hook 和记录事件，不会主动调用 Unity 方法，
不会改 Rigidbody、Collider、PhysicMaterial 或任何比赛状态。

## 当前能抓什么

稳定可用的旁路记录：

```text
WebAssembly.instantiate / instantiateStreaming：
  捕获 instance、exports、memory、table。

createUnityInstance：
  记录 Unity loader config、dataUrl/frameworkUrl/codeUrl、返回的 unityInstance。

WebSocket：
  记录 send/recv 的数据预览，用来对齐 BESTSHOT/SWEEP/POSITION/GAMESTATE。

Emscripten FS：
  记录 writeFile/readFile/mkdir/unlink/syncfs。
  这条线用于确认 .save、RANDSEED、TRACE、rank.csv 是否真的进入虚拟文件系统。

WASM memory helper：
  提供 readCString/readF32/readU32，方便后续按指针读内存。

WASM importObject：
  记录 instantiate 时的 import namespace/key；
  对 WebSocket、socket、FileSystem、IDBFS、syncfs、SendMessage、JS_* 等相关 import
  做轻量调用记录。
```

探索性能力：

```text
installTableHook(index, name, options)
installKnownCurlingHooks()
```

这部分用于记录指定 wasm table 函数的入口参数。当前已预置的候选 index 包括：

```text
10894 CurlingStoneNew.Start
10896 CurlingStoneNew.OnCollisionEnter
12126 ExtendedColliders3D.Awake
10660 AutoDCP.HandleMessage
10932 DCP.HandleMessage
11172 FastDCP.CopyGameState
11203 FastDCP.Update
```

注意：函数级 hook 是否能直接成功，取决于浏览器 WASM table 对 JS wrapper 的接受方式，以及
该函数的真实签名。失败时脚本会记录 `table_hook.failed`，不应把它当成物理结论。

## 使用流程

在 Unity 页面打开后，进入浏览器 DevTools Console，粘贴整个脚本。推荐在页面刚打开、Unity
还没完全加载前粘贴，这样能抓到 `WebAssembly.instantiate` 和 `createUnityInstance`。

Unity 加载完成后运行：

```javascript
__curlingProbe.scanAndHookFS()
__curlingProbe.installKnownCurlingHooks()
```

正常进行一次采样或一局对战后导出事件：

```javascript
__curlingProbe.downloadEvents()
```

导出的 JSON 里主要看：

```text
probe.installed
unity.create.call / unity.create.result
wasm.instance
websocket.send / websocket.recv
fs.writeFile / fs.readFile / fs.syncfs
wasm.table.call
table_hook.failed
wasm.import.call
```

自动启动方式：

```powershell
python tools\calibration\launch_unity_probe_browser.py
```

它会打开可见 Chromium，预注入探针，并每 2 秒写：

```text
log/unity_runtime_probe_*/events.latest.json
log/unity_runtime_probe_*/console.log
```

`console.log` 是浏览器控制台旁路日志。这个文件很重要：Unity build 自己会打印
`b2Vec2 velocity: x=..., y=...` 和 `Curling stop`，可用于恢复单壶积分退出点，也就是
进入 PhysX 碰撞/边界路径前的线速度与位置。

解码 probe 结果：

```powershell
python tools\calibration\decode_runtime_probe_events.py `
  log\unity_runtime_probe_YYYYMMDD_HHMMSS\events.latest.json `
  --jsonl log\unity_runtime_probe_YYYYMMDD_HHMMSS\events.decoded.jsonl `
  --summary log\unity_runtime_probe_YYYYMMDD_HHMMSS\summary.json
```

## 能回答的问题

这条路线优先回答：

```text
1. 当前 WebGL build 有没有在运行时写 .save/RANDSEED/TRACE/rank.csv；
2. 如果写了，写入的虚拟路径是什么，何时 syncfs；
3. AutoDCP/DCP HandleMessage 是否真的经过预期 wasm 函数；
4. CurlingStoneNew.Start / OnCollisionEnter 的运行时调用次数和大致时刻；
5. 后续能否在指定函数入口按指针读取 Rigidbody/Collision/字符串参数。
```

## 不能直接解决的问题

它不会自动给出：

```text
1. Unity native PhysX 内部 contact manifold 的完整结构；
2. cooked convex hull 顶点/面，除非继续定位 PhysX 对象内存或 native 导出点；
3. Rigidbody 私有 native state，除非找到可读入口或对象布局；
4. bit-level 物理对齐，除非进一步拿到 RNG、接触 tick、初始姿态和 hull。
```

所以注入脚本是下一阶段证据入口，不是替代反编译和 PhysX 复现的捷径。它最有价值的地方是：
把“Unity 运行时到底有没有写/调用/读某个东西”从猜测变成可导出的事件日志。

## 2026-07-08 四局对战探针结果

本次启动：

```text
Unity URL: http://127.0.0.1:9007/?connectkey=localtest
probe log: log/unity_runtime_probe_20260708_171027
robots:
  ProbeBlue / ProbeRed
  tools/calibration/run_probe_robot.py
```

解码 summary：

```text
event_count = 723
wasm.instance = 1
memory_count = 1
table_count = 1
websocket.recv = 70
websocket.send = 424
fs.writeFile/readFile/syncfs/mkdir = 0

websocket.recv:
  BESTSHOT = 64
  CONNECTED/READYOK/NAME = 6

websocket.send:
  GO = 64
  MOTIONINFO = 64
  POSITION = 138
  SETSTATE = 138
  SCORE = 10
  TOTALSCORE = 2
  GAMEOVER = 2

keyword hits:
  RANDSEED = 0
  TRACE = 0
  SAVE/.save = 0
  Records = 0
  syncfs = 0
```

结论：

```text
1. 正常四局对战路径下，WebSocket 方向完整可见，可作为协议级旁路日志。
2. 本次没有看到任何 .save/RANDSEED/TRACE/Records 写入，也没有看到 syncfs。
3. 这进一步支持：当前 WebGL 普通四局/无限模式不会自动生成 AutoDCP record。
4. 首轮函数 table hook 失败原因是 hook 过早执行，table 尚未捕获；启动器已修为 table
   出现后再安装，下一轮可继续验证函数入口。
5. FS 未 hook 到全局 Module.FS；下一轮改从 wasm importObject/JSLIB 层记录 FileSystem/IDBFS
   相关 import 调用。
```

## 2026-07-08 增强探针结果

第二轮启动：

```text
probe log: log/unity_runtime_probe_20260708_172813
console log: log/unity_runtime_probe_launcher.out.log
```

新增结论：

```text
1. importObject hook 成功抓到 WebSocketSend、WebSocketAllocate、WebSocketConnect、
   JS_FileSystem_Initialize、JS_FileSystem_Sync 等 import 调用。
2. `JS_FileSystem_Sync` 在正常四局里会被 Unity WebGL runtime 调用，但没有看到
   .save/RANDSEED/TRACE/Records/IDBFS 相关路径或内容。
3. 早期 import 过滤把 JS_Sound/JS_SystemInfo/JS_Log_Dump 等每帧调用也记下来了，
   导致 12 万级事件噪声；脚本已收窄到 socket/FileSystem/WebRequest 等相关 import。
4. 直接 `WebAssembly.Table.set(index, ordinary JS function)` 失败，浏览器报：
   `function-typed object must be null ... or a Wasm function object`。
   这说明 table hook 不能简单塞普通 JS wrapper；需要 `WebAssembly.Function`、Emscripten
   `addFunction` 或改走 dynCall/import/native task 入口。当前 Chrome/Node 环境未稳定暴露
   可用的 `WebAssembly.Function`，Unity Module 也未导出 `addFunction`。
```

控制台速度解析工具：

```powershell
python tools\reverse\analyze_unity_console_trajectory.py `
  log\unity_runtime_probe_YYYYMMDD_HHMMSS\console.log `
  --output log\unity_runtime_probe_YYYYMMDD_HHMMSS\console_trajectory_summary.json
```

对 `log/unity_runtime_probe_launcher.out.log` 的四局日志解析得到：

```text
shot_count = 64
with MOTIONINFO = 64

纯滑行样本：
  丢掉第一条 b2Vec2 velocity 后按 dt=0.01 积分，
  可把最终 POSITION 对到约 1mm 级。

碰撞/边界样本：
  Curling stop 前最后一条速度仍有 0.26m/s - 1.52m/s，
  表明 `mCollision=true` 后 FixedUpdate 退出 Newfrictionstep，
  后续交给 PhysX/边界/多壶路径。
```

新增辅助工具：

```text
tools/reverse/analyze_unity_console_trajectory.py
tools/reverse/build_console_collision_samples.py
tools/reverse/merge_console_handoff_into_samples.py
```

其中 `merge_console_handoff_into_samples.py` 用于下一轮 controlled collision 采样：把
controlled sampler 的 JSONL 与同轮 runtime probe 的 `console_trajectory_summary.json`
按 BESTSHOT 校验后合并，给每条样本补上显式 `handoff_state`：

```text
x/y  = 控制台 b2Vec2 速度积分得到的 Newfrictionstep 退出位置
vx/vy = Curling stop 前最后一条 b2Vec2 velocity
w    = 可选 zero / MOTIONINFO / 从 MOTIONINFO 用 Newfrictionstep replay 到 exit 的估计值
```

这条证据不能替代 PhysX contact manifold，但可以消除“MOTIONINFO 到接触 tick 这段是否走错”
这一类误差来源。下一次应对 `collision_unique_roles_probe_r00.json` 同时采集 controlled JSONL
和 probe console，再用显式 handoff 重跑 PhysX 对齐。

### 四局制重连采样 2026-07-08 18:10

这轮先重启了 `curling_server.exe` 和两个 probe client；第一次 client 被拒是因为页面没有刷新，
WebGL 房间没有重新注册到 server。刷新并重新进入四局制后，页面收到：

```text
CONNECTED x2
READYOK x2
```

随后四局完整跑完，结果为 `TOTALSCORE 4 4 / GAMEOVER DRAW`。有效产物：

```text
log/unity_fourgame_20260708_1810/player1.out.log
log/unity_fourgame_20260708_1810/player2.out.log
log/unity_fourgame_20260708_1810/browser_console_slice.log
log/unity_fourgame_20260708_1810/console_trajectory_summary.json
```

解析命令：

```powershell
python tools\reverse\analyze_unity_console_trajectory.py `
  log\unity_fourgame_20260708_1810\browser_console_slice.log `
  --output log\unity_fourgame_20260708_1810\console_trajectory_summary.json `
  --release-x 2.3506 --release-y 32.4768 --dt 0.01
```

结果：

```text
shot_count = 64
handoff speed > 0.05m/s = 54
full-stop/no-collision = 10
full-stop 积分到 POSITION 的平均误差约 1mm
```

派生碰撞样本与当前 PhysX best 复跑：

```powershell
python tools\reverse\build_console_collision_samples.py `
  log\unity_fourgame_20260708_1810\console_trajectory_summary.json `
  --output data\calibration\unity_fourgame_1810_console_collision_samples_replay_w_20260708.jsonl `
  --angular-mode replay

D:\esp\tmp\curling_pyphysx_conda\python.exe tools\reverse\probe_physx_collision_alignment.py `
  --samples data\calibration\unity_fourgame_1810_console_collision_samples_replay_w_20260708.jsonl `
  --output data\calibration\unity_physx_fourgame_1810_console_replay_w_current_best_20260708.json `
  --radius 0.146 --height 0.23 --stone-faces 256 `
  --stone-friction 0.6 --stone-restitution 1.0 --combine-mode multiply `
  --contact-offset 0.005 --rest-offset 0.0 `
  --convex-quantized-count 255 --convex-vertex-limit 255 `
  --solver-position-iterations 6 --solver-velocity-iterations 1 `
  --max-depenetration-velocity 10.0 --use-unity-frame --dt 0.01 --max-time 20.0
```

复跑结果：

```text
sample_count = 36
active_rmse_m = 0.0387
target_in_play_rmse_m = 0.1553
combined_rmse_m = 0.0903
```

这轮的定位价值是确认：即使从 runtime console 恢复出显式 handoff，target 误差仍然保持
10cm 级，和受控 unique-role / unique-target 的方向一致。普通四局样本不能单独用于参数定标，
但可以作为多体/清壶路径的旁证。
