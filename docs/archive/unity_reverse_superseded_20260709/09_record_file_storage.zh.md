# Unity 记录文件存放位置

本页专门记录 `.save`、`RANDSEED`、`TRACE`、`AutoGame/rank.csv` 这类中间记录到底会写到哪里。

## 先说结论

我们要找的不是三个独立文件：

- `.save` 是 AutoDCP/AutoGame 的 INI 风格录像文件。
- `RANDSEED`、`BESTSHOT`、`SWEEP`、`TRACE` 是同一个 `.save` 里每壶 section 的 key。
- “出手到中线前已经消耗的 RNG 次数”不是 Unity 写出的字段；这是我们拿到 `RANDSEED` 后，为了从中线后的 `MOTIONINFO` 接着 replay 而推导出来的量。

如果从 AutoDCP `.save` 的 `BESTSHOT` 开始整段 replay，`RANDSEED` 写入/读取发生在释放刚体之后、下一次
`FixedUpdate` 之前，所以初始 `rng-skip` 应按 `0` 处理。只有从中线 `MOTIONINFO` 半路接入时，才需要估计或搜索
已经消耗了多少次 `Random.Range(-0.0002, 0.0002)`。

当前这版 WebGL 包还有一个更关键的入口事实：`BuildSettings` 只打包了
`MenuScene`、`MotionTestScene`、`GameScene`、`GameScene4Games`、`GameSceneNoLimit`、
`GameSceneDebug`、`HumanVsAI`，没有 `AutoGame`，也没有 `FastGame`。代码里有
`AutoDCP` 和 AutoGame 记录分支，不等于当前包的 UI 能加载 AutoGame 场景。

## Unity 代码里的逻辑路径

二进制字符串池和已恢复的 AutoDCP 分支共同给出的逻辑目录是：

```text
GameScene       -> Records/8Games/
GameScene4Games -> Records/4Games/
FastGame        -> Records/4Games/
AutoGame        -> Records/4Games/
AutoGame rank   -> AutoGame/rank.csv
```

字符串池还能看到这些文件相关字符串：

```text
autoGame.save
Record Files(*.save)
*.save
AutoGame\rank.csv
```

因此 `.save` 的目录已经明确；具体文件名可能来自 AutoGame 默认名 `autoGame.save` 或 UI/代码选择的记录名。
实际采集时应监控整个 `Records/4Games/`、`Records/8Games/`，不要只盯一个固定文件名。

但当前 BuildSettings 里不存在 `AutoGame`/`FastGame` 场景，所以这些目录是“代码逻辑路径”，
不是当前 UI 路径必然会写出的文件。

## 当前包的记录入口状态

静态资源和 IL2CPP 方法映射已经对上：

```text
AutoDCP.Start                -> func60907
AutoDCP.NewGame              -> func60894
AutoDCP.NewGameFromHistory   -> func60895
AutoDCP.ReadReacord          -> func60887
AutoDCP.<Start>b__138_0      -> NewGame
AutoDCP.<Start>b__138_1      -> NewGameFromHistory
AutoDCP.<Start>b__138_2      -> SendIsReady
AutoDCP.<Start>b__138_3      -> ReadReacord
ScenesController.mLoadScence -> SceneManager.LoadScene(sceneName)
```

`AutoDCP.Start()` 会绑定这些按钮路径：

```text
WaitingCanvas/Panel/StartGame    -> NewGame
WaitingCanvas/Panel/StartHisGame -> NewGameFromHistory
WaitingCanvas/Panel/SendIsReady  -> SendIsReady
WaitingCanvas/Panel/ReadRecord   -> ReadReacord
```

`ReadReacord()` 和 `NewGameFromHistory()` 都会构造 `OpenFileName`，默认初始目录为：

```text
Directory.GetCurrentDirectory() + "/Records"
```

过滤器是：

```text
Record Files(*.save)\0*.save\0\0
```

读取成功后才会把 `recordedGame` 置为 true，并用 `INIParser.Open(path)` 打开 `.save`。
`NewGame()` 则会新建当前比赛 record，并额外打开：

```text
autoGamePath + "\autoGame.save"
```

这些入口说明 `.save` 读写逻辑是真实存在的；问题不是代码里没有 record 功能，而是当前 WebGL
BuildSettings 没有 `AutoGame` scene，普通 DCP/HumanVsAI 场景里的 `ReadRecord`/`StartHisGame`
GameObject 还是 inactive。

## WebGL 实际落盘位置

这个单机版跑的是 Unity WebGL，不是普通 Windows standalone 文件系统。Unity runtime 把
`Application.persistentDataPath` 挂到 Emscripten IDBFS：

```text
/idbfs/<origin-hash>/...
```

本机 Edge 的实际持久化目录是：

```text
C:\Users\PickledPepper\AppData\Local\Microsoft\Edge\User Data\Default\IndexedDB\http_127.0.0.1_9007.indexeddb.leveldb
```

如果访问的是远程比赛地址，也会有对应 origin，例如：

```text
C:\Users\PickledPepper\AppData\Local\Microsoft\Edge\User Data\Default\IndexedDB\http_182.92.113.197_9007.indexeddb.leveldb
```

本次在 `http_127.0.0.1_9007` 的 LevelDB 里确认能看到 `/idbfs` 和 Unity 自己的
`Unity/local/.../Analytics/ArchivedEvents` 记录，但没有 `Records`、`BESTSHOT`、`RANDSEED`、`TRACE`、
`autoGame.save`。这和 socket 采样结果一致：普通无限模式和普通四局对战没有进入会写 AutoDCP `.save`
的分支。现在进一步确认，这不是采样脚本漏路径，而是当前包缺 AutoGame/FastGame 场景入口。

还有一个 WebGL 模板细节：`web/index.html` 里这行仍是注释状态：

```javascript
// config.autoSyncPersistentDataPath = true;
```

所以即便 Unity 某个分支写了 `Application.persistentDataPath`，也要确认是否发生了 `FS.syncfs` 持久化；
否则可能只存在于当次浏览器内存文件系统中。当前已落盘的 IndexedDB 里没有 AutoDCP record 字段。

## 当前采样事实

已经做过两类采样：

- 无限模式控制采样：96 条有效 socket JSONL，没有 `.save`，没有 `RANDSEED`。
- 普通四局对战：Player1/Player2 各 32 条 socket JSONL，没有 `.save`，没有 `RANDSEED`。
- 2026-07-08 运行时注入探针完整跑完一场四局对战：
  `log/unity_runtime_probe_20260708_171027`。解码后有 `BESTSHOT=64`、`MOTIONINFO=64`、
  `POSITION=138`、`SETSTATE=138`、`GAMEOVER=2`；但 `fs.writeFile/readFile/syncfs/mkdir=0`，
  `RANDSEED/TRACE/.save/Records/syncfs` 关键字命中均为 0。

同时检查过：

- 工程目录和单机版目录下的 `Records/`、`Records/4Games/`、`Records/8Games/`、`AutoGame/`。
- Edge IndexedDB 的 `http_127.0.0.1_9007.indexeddb.leveldb`。
- Edge IndexedDB 的 `http_182.92.113.197_9007.indexeddb.leveldb`。
- WebGL BuildSettings：没有 `AutoGame` 和 `FastGame` scene。

结论是：当前 UI 入口没有生成 AutoDCP `.save`；不是 watcher 路径漏了普通工程目录。
要拿真实 AutoDCP `.save`，需要另一份包含 `Assets/Scenes/AutoGame.unity` 的 build，
或者修改/注入当前 build 让某个已打包场景挂上 `AutoDCP` 并激活 record UI。

## 检查工具

现在有一个只读检查脚本：

```powershell
D:\anaconda3\python.exe tools\reverse\inspect_unity_record_storage.py --origin-filter 9007
```

它会扫描：

- Unity build 里的路径/字段字符串；
- 工程和单机版下的 `Records/`、`AutoGame/`；
- Edge/Chrome profile 里的 IndexedDB origin；
- `BESTSHOT/RANDSEED/TRACE/Records/AutoGame/rank.csv` 等关键字。

需要机器可读报告时：

```powershell
D:\anaconda3\python.exe tools\reverse\inspect_unity_record_storage.py --origin-filter 9007 --json
```

场景入口和 controller/UI inventory 用：

```powershell
D:\anaconda3\python.exe tools\reverse\inspect_unity_assets.py $env:TEMP\curling_reverse_il2cpp\data.unity3d
```

它会在开头输出 BuildSettings 场景列表，并明确标出：

```text
AutoGame: not present in BuildSettings
FastGame: not present in BuildSettings
```

如果之后我们真的进入 AutoGame/AutoDCP 记录分支，优先预期它出现在：

```text
Unity 逻辑路径: /idbfs/<origin-hash>/Records/4Games/*.save
Edge 落盘路径: C:\Users\PickledPepper\AppData\Local\Microsoft\Edge\User Data\Default\IndexedDB\http_127.0.0.1_9007.indexeddb.leveldb
```

也可能同步成普通目录形式：

```text
D:\Desktop\冰壶\DCCourse\Records\4Games\*.save
D:\Desktop\冰壶\DCCourse\数字冰壶单机版_win\数字冰壶单机版\Records\4Games\*.save
```

但本次运行没有出现这些普通目录输出。
