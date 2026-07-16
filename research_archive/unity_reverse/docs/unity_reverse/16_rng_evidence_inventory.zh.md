# 历史 Unity 采样的 RNG 证据清单

更新时间：2026-07-13

## 结论先行

历史数据**不作废**，但从本日起不得再把所有 `sampleId=14000` 的数值视为同一个可横向相减的真值。
`BESTSHOT 3.4 0 0`、target 位置和 sweep 参数相同，只说明协议请求相同；每个 `FixedUpdate` 的
`Random.Range(-0.0002, 0.0002)` 都会改变实际摩擦、碰前 `P/Q/v/w` 和随后碰撞分支。

严格的单次毫米级验收只接受：

```text
同一 Unity run + 完整逐 tick friction RNG 流
或
同一 Unity run + 在 BESTSHOT 前固定并记录的 RANDSEED/draw 起点
```

其他证据仍按其原有边界有效，但不得外推为跨 run 的单次 endpoint 误差。

## 证据等级

| 等级 | 必要条件 | 允许的结论 | 禁止的结论 |
|---|---|---|---|
| `R0_replay_grade` | 原始 event log 中有完整逐 tick friction stream，且能绑定 shot/run。 | 同次 deterministic local replay、碰前到 endpoint 验收。 | 不自动证明另一次未固定 RNG run。 |
| `R1_same_run_boundary` | 同一 event log 内的 core/PCM/solver checkpoint；可以没有完整 friction stream。 | 该 run 的同一 native boundary 字段对照、oracle 因果和 source 定位。 | 跨 run endpoint 数值相减或把结果拼成连续真值。 |
| `R2_input_conditioned` | Unity 已给定/注入该边界输入，例如 raw ContactBuffer、P/Q/v/w、constraint row。 | PCM、finalizer、solver consume 的条件等价。 | 推出未观测的 release/RNG/lifecycle 历史。 |
| `R3_statistical_only` | endpoint 或摘要存在，但无完整 RNG 流/seed，也无可绑定的同次 core。 | 历史残差规模、回归趋势、分布估计。 | 单次毫米级验收或根因量化。 |

## 当前历史资产分类

| 资产/记录 | 等级 | 现有证据 | 后续用途 |
|---|---|---|---|
| `log/unity_runtime_probe_20260710_012403/events.jsonl` 与 `front_half_pcm_replay_compare_20260710.json` | `R0_replay_grade` | event log 实际保留 `8,111` 条 `sliding.random_range.friction`；报告明确引用该 log。 | 作为有完整摩擦流的前半段/碰前复现基线；可重新按 shot 切片。 |
| A5/A11--A19 的 release、setter、bridge、locked-axis 结论 | `R1_same_run_boundary` | 报告明确使用 captured Unity friction noises；A5 audit 摘要只保留关键 noise，而非可独立重放的完整 stream。 | 保留 script setter、bridge、solver-body 边界结论；重跑 endpoint 时需回到原始 event log 或新固定 seed capture。 |
| B20--B24 direct PCM、ContactBuffer、finalizer 和 solver-row 审计 | `R2_input_conditioned` | Unity 已捕获 PCM transform/contact/constraint 输入，局部调用或同次 pair 边界比对。 | 保留几何、PCM、solver 公式和 pair lifecycle 的闭合结论。 |
| C03/C11/C22/C23 连续 writeback window | `R1_same_run_boundary` | 同次 `c03.first_dynamic_writeback`、`c04.dynamic_solver_frame`、solver descriptors/rows 存在；C11 有 4 frame、C31 有 1024 frame。 | 用于第一个字段差、静态 solver 与缓存边界定位；不得将不同 log 的 frame 编号直接对齐。 |
| C31 first run | `R1_same_run_boundary` | `1024` C04 core frames、同 run C03 输入和 endpoint。 | 原 C31 waterfall 内部有效；只能解释该 run。 |
| C31 retry | `R1_same_run_boundary` | `16` C04 frames、frame-1 static descriptors、同 run endpoint。 | retry waterfall 内部有效；与 first run 不可数值合并。 |
| B25/C21/C22 P6 six-shot endpoint 汇总 | `R3_statistical_only`（待追溯） | artifact 自身没有 `RANDSEED`、完整 `friction_noise[]` 或绑定 raw event-log 路径。 | 保留历史 endpoint 残差规模；只有找到完整原始 RNG 流后才可升为 `R0`。 |
| C25 active0 history PCM capture | `R1_same_run_boundary` | Unity PCM history 及 reused active0 transform 已捕获；本地 replay 因无完整 noise 流在 step 0 耗尽。 | 保留 Unity history/PCM 事实；不得使用其 local endpoint。 |

## 已知跨 run 分叉的实测例子

两个 C31 run 的协议请求相同，但最后 pre-PCM script state 已不同：

| 字段 | first C31 | retry C31 |
|---|---:|---:|
| last friction draw | `+0.0000834421` | `+0.0001134852` |
| last setter `wy` | `0.1651429683` | `0.1793442070` |
| pre-PCM `vx` | `0.8005638123` | `0.7915377617` |
| C03 pre-solve active `w.y` 差（first - retry） | `-0.0142012984rad/s` | — |
| Unity target final XY 差的范数 | `50.9mm` | — |

target 在 C03 pre-solve 仍相同，故这不是 collision/PCM/solver 首次随机分叉；它在 active 单壶的
`FixedUpdate -> Random.Range -> Newfrictionstep -> Rigidbody setter` 链已发生。

## 之后的采样与验收协议

1. 每次 runtime capture 生成不可复用的 `run_id`；所有 core/PCM/endpoint 行均写入它。
2. 在 `BESTSHOT` 前记录 `rng_seed`、`rng_draw_start`。优先使用 AutoDCP `RANDSEED`；诊断 harness 可在同一
   边界显式调用 Unity `Random.InitState(seed)`，但必须标注为 runtime diagnostic mutation。
3. 无法得到 seed 时，保存从 release 到 quiet 的所有 friction draws；本地严格按原序列消费。
4. 每个 endpoint 验收行必须写明 `rngEvidenceLevel`。不是 `R0_replay_grade` 的行不得参与“毫米级通过率”。
5. 旧 P6 endpoint 在找到对应原始 event log 前保留 `R3_statistical_only`；不删除、不改写历史数字。

## 当前下一步

先把新的 Unity runtime harness 扩展为“shot-bound seed/draw manifest”，并用相同 seed 连续重复两次同一
shot。只有碰前 core 与 endpoint 自身复现，才重新开启跨 run 的毫米级生产验收；否则先修 RNG 设定时机。

### C33 seed gate 实测（2026-07-13）

已新增 launcher `--rng-seed-on-first-friction <int32>`。它是明确标记的 runtime diagnostic mutation：在 fresh
browser 的受控 single shot 中，A0 friction hook 看到首个 `Range(-0.0002,0.0002)` **之前**才调用
`UnityEngine.Random.InitState(seed)`，避免 UI/startup 的随机消费污染物理输入。首轮 `seed=20260713` 的实际
事件顺序为：`rng.random_init_state`（event `217`）→ `sliding.random_init_state`（`218`）→
`rng.seed_applied`（`219`）→ 第一条 friction draw（`220`）；首 draw 为
`-0.00014820003707427531`，全 shot 记录 `1562` 条 friction draws。

随后成功的同 seed fresh-browser repeat（C35）证明 protocol 恢复已有效，却同时否定了 seed gate 的充分性：两轮
都在第一个 friction draw 前设定 `20260713`，两者均有 `1562` draws，但第 `22` 个 draw 起已不同。原因不是 DCP
friction hook 的设定时机，而是 Unity 的 **process-global RNG 仍可被其他 runtime 路径消费**。故 C33 的正确状态是
`seed_gate_timing_verified_but_not_replay_grade`；不得把 `InitState` 当作 R0 的输入固定方式。

```text
data/calibration/c33_rng_seed_gate_a_14000_20260713.json
```

### C36 DCP friction manifest replay（2026-07-13，R0 fixture 已闭合）

为排除全局 RNG 的非 DCP 消费，runtime harness 新增 `--rng-friction-manifest-events <events.jsonl>`：它只在已恢复的
`Random.Range(-0.0002,0.0002)` DCP friction 调用处按 capture manifest 返回值，不改其它 `Random` 调用。manifest
耗尽会发出 `rng.friction_manifest_exhausted`，该 run 自动失去严格 fixture 资格，不能静默回退。

两次 fresh-browser C36 都实际 `applied=1`、完整消费 `1562` 项、`exhausted=0`；服务器 active/target 最终坐标分别
逐字相同：`(2.3412,5.4872)/(2.4841,3.8930)`。C04 frame `0..3` 的 decoded `P/Q/v/w` 也逐值相同。C26 frame-1 的
solver-body 物理字段相同；constraint raw block 中只保留 allocator pointer / 未初始化 tail 的差异报告，绝不将其误判
为物理首差。

以其中一轮 Unity C04 truth 输入本地 replay 后，frame-1 起最大 `P/Q/v/w` 差为
`1.847743988e-6 rad/s`，仍是 float ULP 量级。因此旧 C31 的 `0.022045rad/s` angular “首差”已撤回为跨 run RNG
分叉伪像，不再是 static solver hidden-state 缺失的证据。

```text
data/calibration/c36_manifest_replay_audit_14000_20260713.json
data/calibration/c37_manifest_local_static_phase_map_14000_20260713.json
log/c36_manifest_replay_fixed_a_20260713/unity_runtime_probe_20260713_115243/events.jsonl
log/c36_manifest_replay_fixed_b_20260713/unity_runtime_probe_20260713_115347/events.jsonl
```

C39 将同一 R0 fixture 直接跑完整 `BESTSHOT -> C03` production handoff 后确认：最终仍有 active/target
`0.630/4.226mm`，但累计 C03 truth-fill 显示仅 active position `45.776μm` residual 已解释 target 的
`4.203mm` 改善；full C03 truth 为 `0.036/0.022mm`。因此 manifest 已把“可重现输入”闭合，下一项严格误差是
last DCP setter/pre-sim pose handoff，而不是 RNG 或 post-contact static solver。

同一 R0 fixture 的 C42 release-height ablation 进一步限定了该结论：release native `Y` 加
`12.615203857mm` 后，C03 entry 的 `P/v` 不变，仅 `q.y/w.y` 分别变 `5.2154e-8/1.0431e-7rad/s`，且 endpoint
没有改善。这是碰撞入口分支敏感性证据，不得把 release height 或单字段 waterfall 的局部改善解释成 production 根因。
