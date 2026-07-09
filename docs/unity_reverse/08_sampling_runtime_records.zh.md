# 采样、记录文件与运行时探针

旧的重采样计划、记录文件路径、运行时注入探针长文档已合并到这里：

```text
docs/archive/unity_reverse_superseded_20260709/08_resampling_plan.zh.md
docs/archive/unity_reverse_superseded_20260709/09_record_file_storage.zh.md
docs/archive/unity_reverse_superseded_20260709/11_runtime_injection_probe.zh.md
```

## 当前结论

现在不需要继续普通 socket 采样。已有样本足够证明：

```text
1. 单壶 no-sweep 可做训练第一阶段。
2. 碰撞误差不是样本数量不够，而是缺首次碰撞帧 native state。
3. 普通四局或无限模式不会自动给出 AutoDCP `.save` / `RANDSEED`。
```

后续如果再打开 Unity，目标必须是抓运行时 native 字段，不是多收 endpoint。
运行一次碰撞只是为了触发 hook。

## `.save` 和 RANDSEED

Unity 代码里 AutoDCP 支持：

```text
BESTSHOT
RANDSEED
SWEEP
POSITION
SCORE
SETSTATE
TRACE
```

但是当前 WebGL build 没有打包可直接进入的 `AutoGame/FastGame` 主路径。普通 UI 的四局制和无限模式不会自然生成我们想要的 `.save` 文件。

WebGL 逻辑落盘位置通常在浏览器 IndexedDB / Emscripten FS 下，但当前包没有在普通模式暴露 AutoDCP record 入口，所以“找不到 `.save`”不是路径没扫全，而是模式没开。

## 运行时 probe 能抓什么

现有工具：

```text
tools/reverse/unity_webgl_runtime_probe.js
tools/calibration/launch_unity_probe_browser.py
tools/calibration/decode_runtime_probe_events.py
tools/reverse/export_cooked_hull_from_probe_events.py
```

已经能帮助抓：

```text
WebSocket 收发
console trajectory
Emscripten FS 行为
WASM memory/table 基础信息
部分 PhysX cooking hook 事件
PhysX native hook 事件：
  ContactBuffer 生成入口
  contact finalization task
  single-pair / 4-wide solver contact row 写出入口
```

当前等待页抓到的 cooked hull 已被尺寸判据排除为正式比赛石壶，不能直接接进训练。

## 当前主线：抓 native state

目标不是终点采样，而是抓 Unity 在碰撞帧喂给 PhysX 的中间态：

```text
ContactBuffer:
  normal / point / separation
  maxImpulse
  staticFriction / dynamicFriction / restitution
  targetVel
  internalFaceIndex1

friction cache / patch:
  old anchors
  correlation / grow patch 后的 anchors
  broken/writeback 状态

solver rows:
  SolverContactHeader
  SolverContactPoint
  SolverContactFriction
  4-wide batch row 的 normal / friction 写出缓冲
```

已经接入的 WebGL table hook：

```text
120118 func70576 PxcPCMContactConvexConvex        signature iiiiiiiii
120119 func70577 PxcPCMContactConvexMesh          signature iiiiiiiii
120204 func70739 PxsContext.contactManagerDiscreteUpdate signature vi
120587 func71272 PxsDynamics.createFinalizeContacts       signature vi
120379 func70963 createFinalizeSolverContacts4    signature iiiifffffi
120487 func71103 createFinalizeSolverContacts     signature iiiifffffii
```

`PxcPCMContactConvexConvex` 被调用时，probe 会自动把 native capture 武装一小段时间，
随后只抓这段时间内的 finalizer / solver row 入口，避免日志先被冰面支撑接触填满。

浏览器 console 最小流程：

```javascript
__curlingProbe.scanAndHookFS()
__curlingProbe.installPhysXNativeHooks({
  maxDumpsPerHook: 16,
  armMs: 2000,
  includeRawBytes: true,
  includeNestedRawBytes: false,
  argWindowBytes: 8192
})
```

然后只需要在页面里触发一次明确的石壶-石壶碰撞。结束后导出：

```javascript
__curlingProbe.downloadEvents("physx_native_state_events.json")
```

本地解码：

```powershell
python tools\calibration\decode_runtime_probe_events.py path\to\physx_native_state_events.json
```

重点看 summary 里的：

```text
physx_native_counts
physx_contact_candidates
```

原始 JSON 里的关键事件：

```text
physx.native.capture_armed
physx.native.before
physx.native.after
```

每个 `physx.native.before/after` 都会保存参数指针窗口、前若干 `u32/f32` 预览、完整 raw bytes
以及参数结构里的嵌套指针预览。若某个窗口正好是 `Gu::ContactBuffer`，会按已知布局直接给出
`contactBufferCandidate`。

## 如果以后必须再采样

采样必须服务于一个明确问题：

```text
单壶 RNG:
  需要 RANDSEED 或重复同一 BESTSHOT 的分布。

扫冰:
  需要记录 SWEEP 到达帧、Midline/Hogline2 状态和 sweep distance。

碰撞:
  需要 fresh scene / fresh page。
  需要 active/target 碰前碰后短时状态。
  重点抓 native ContactBuffer / solver rows。
```

不要再做只保存最终 `POSITION` 的碰撞采样；那会继续把 contact 和尾段滑行混在一起。

## 用户手动点页面时的最小流程

```text
1. 进入四局或无限模式。
2. 等脚本连接两个 player。
3. 点准备和开始。
4. 每发只跑一个明确 case。
5. 每发结束后清场或 fresh page。
6. 保存 socket log、browser console、probe events。
```

但当前阶段不建议继续做普通 endpoint 采样。主线是 native-state hook。
