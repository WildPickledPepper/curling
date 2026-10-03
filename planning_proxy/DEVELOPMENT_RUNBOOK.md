# 冰壶规划器工作手册

> 用途：记录不会随某一局对战变化的开发前提，避免反复寻找源码、Python 解释器、原生扩展和 PowerShell 调用方式。
> 状态机假设、失败局面、实验结论放在 `STATE_MACHINE_ITERATION_LOG.md`，不要混在本文件。

## 1. 工作区与关键目录

| 用途 | 路径 |
|---|---|
| 项目根目录 | `D:\Desktop\冰壶\DCCourse` |
| 状态机/对局主入口 | `D:\Desktop\冰壶\DCCourse\planning_proxy\evaluate_vs_teammate_ppo.py` |
| 严格候选验收 | `D:\Desktop\冰壶\DCCourse\planning_proxy\strict_refine.py` |
| 粗代理 | `D:\Desktop\冰壶\DCCourse\planning_proxy\analytic_proxy.py` |
| 严格物理 Python 桥 | `D:\Desktop\冰壶\DCCourse\local_simulator\unity_physx.py` |
| 严格一手回放环境 | `D:\Desktop\冰壶\DCCourse\local_simulator\examples\train_policy_tree_selfplay.py` |
| 原生 PhysX/运动积分 C++ 源码 | `D:\esp\tmp\curling_pyphysx_hybrid\src\pyphysx.cpp` |
| 原生工程构建配置 | `D:\esp\tmp\curling_pyphysx_hybrid\CMakeLists.txt` |
| 运行时 CP39 扩展 | `D:\Desktop\冰壶\DCCourse\local_simulator\runtime\pyphysx\_pyphysx.cp39-win_amd64.pyd` |
| 运行时 CP313 扩展 | `D:\Desktop\冰壶\DCCourse\local_simulator\runtime\pyphysx\_pyphysx.cp313-win_amd64.pyd` |
| Linux CP39 扩展 | `D:\Desktop\冰壶\DCCourse\local_simulator\runtime\pyphysx\_pyphysx.cpython-39-x86_64-linux-gnu.so` |
| 原生扩展加载器 | `D:\Desktop\冰壶\DCCourse\local_simulator\runtime_loader.py` |
| 原生工程 CP39 优化构建（不等于已部署版本） | `D:\esp\tmp\curling_pyphysx_hybrid\build-cp39-optimized-20260722\lib\_pyphysx.cp39-win_amd64.pyd` |
| 原生工程 CP39 链接期优化试验构建（已止损，不用于验证） | `D:\esp\tmp\curling_pyphysx_hybrid\build-cp39-ltcg-20260724\lib\_pyphysx.cp39-win_amd64.pyd` |
| 首碰撞循环计时诊断构建（仅测量，绝不部署） | `D:\esp\tmp\curling_pyphysx_hybrid\build-cp39-firstcontact-timing-20260724\lib\_pyphysx.cp39-win_amd64.pyd` |

### 源码与部署副本的边界

**当前本地 Windows CP39 正式扩展：** 2026-07-25 已启用优化构建，主项目运行时的 SHA-256 是
`2564ABEC4FA3F358E67259B105C4B88D49EAE28510611C8A0E2F11B7671888DF`（`5,107,712` 字节），与
`D:\esp\tmp\curling_pyphysx_hybrid\build-cp39-optimized-20260722\lib\_pyphysx.cp39-win_amd64.pyd` 完全相同。
替换前运行时为 `D312EB021FDE9D5D4A8F0AAB84CBB35D54D6670C1749A0DD7A64E94F416662A3`（`5,080,576` 字节），其可恢复副本位于
`D:\Desktop\冰壶\DCCourse\archive\pyd_backups\cp39_optimized_activation_20260725`。本次仅替换主项目和队友包的本地 Windows CP39 副本；Linux `.so`、课程平台与发布归档未改。

现有 `curling_pyphysx_hybrid\src\pyphysx.cpp` 已继续演进，直接重新编译不能自动视为正式运行时源码。用下面命令核对，不凭文件名判断：

```powershell
Get-FileHash .\local_simulator\runtime\pyphysx\_pyphysx.cp39-win_amd64.pyd -Algorithm SHA256
Get-FileHash D:\esp\tmp\curling_pyphysx_hybrid\build-cp39-optimized-20260722\lib\_pyphysx.cp39-win_amd64.pyd -Algorithm SHA256
```

历史构建目录还保留 `build-cp39-msvc\lib\_pyphysx.pdb` 和 `Release\_pyphysx.tlog\CL.command.1.tlog`。它们确认
当时使用 CP39、`/O2 /Ob2 /GL /fp:precise`，也记录源码路径；**PDB 不含 C++ 源码快照**，不能把它当作恢复正式源码的
手段。以后每次正式 pyd 构建必须另存“源码压缩包 + CMakeCache + pyd 的 SHA-256”，三者缺一不可。

日常开发只改项目根目录下的 `planning_proxy`、`local_simulator`。下列目录是历史打包副本，除非明确在做该平台的重新打包，否则不要把它们误当成主源码：

| 目录 | 用途 |
|---|---|
| `planning_proxy\submission_direct` | 对战平台直连提交副本 |
| `planning_proxy\archive\deployment_directories\server_py313_physx_state_machine_20260721` | Windows CP313 服务端历史打包副本 |
| `planning_proxy\server_linux_cp39_physx_state_machine_20260721_direct` | 课程平台 Linux CP39 直连包 |
| `planning_proxy\archive\deployment_directories\server_linux_cp39_physx_state_machine_20260721_backhand_draw` | 课程平台 Linux CP39 的旧变体 |
| `planning_proxy\archive\deployment_directories\teammate_state_machine_package_20260721` | 发给队友的历史独立包 |

对战日志主文件是项目根目录的 `unity_planner.jsonl`；离线评测与诊断报告写到 `planning_proxy\runs\`。先用只读命令确认来源与日期，再基于它做结论：

```powershell
Get-Item .\unity_planner.jsonl | Select-Object FullName,Length,LastWriteTime
Get-ChildItem .\planning_proxy\runs\*.json | Sort-Object LastWriteTime -Descending | Select-Object -First 10 Name,LastWriteTime,Length
```

## 2. Python 环境

| 用途 | 解释器 | 备注 |
|---|---|---|
| Windows 严格模拟、CP39 `.pyd`、路径求解诊断 | `C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe` | 当前严格 CP39 的标准解释器 |
| Windows CP313 提交/打包兼容检查 | `C:\Users\PickledPepper\scoop\apps\python313\current\python.exe` | 必须搭配 CP313 `.pyd` |
| PPO 对手及历史评测 | `D:\anaconda3\python.exe` | 不要拿它加载 CP39 `.pyd` |
| 课程平台 | Linux CPython 3.9 | 必须使用 Linux `.so`，不能使用 Windows `.pyd` |

严禁跨 ABI 加载：CP39 只能加载 CP39 扩展；CP313 只能加载 CP313 扩展；Linux 不能加载 Windows `.pyd`。

## 3. 现有诊断工具

| 工具 | 用途 | 产物 |
|---|---|---|
| `diagnostics/profile_k6_search.py` | 从真实 `game.trace` 恢复某手，拆分粗代理、严格候选、首次碰撞、静止结算耗时 | `planning_proxy/runs/*.json` |
| `diagnostics/probe_strict_candidate.py` | 重放单一严格候选，记录首次碰撞循环步数、接触结果和耗时 | `planning_proxy/runs/*.json` |
| `diagnostics/run_evaluator_with_extension.py` | 仅在当前 CP39 子进程临时指向指定 pyd，再运行完整本地对局；绝不覆盖运行时文件 | 显式指定的完整对局报告 |
| `diagnostics/run_tests_with_extension.py` | 临时指向候选 `.pyd` 运行 unittest；Windows 子进程会继承扩展路径 | 控制台测试结果 |
| `diagnostics/summarize_extension_probe_benchmark.py` | 只读汇总成对的当前/候选严格单候选探针，输出平均、P95、最大耗时与加速比；不执行物理 | 显式指定的 JSON 报告 |
| `diagnostics/evaluate_k6_fixed_candidate_contracts.py` | 合同无关固定候选批次，对照完整/修复/仅清/交换的严格可行性 | `planning_proxy/runs/*.json` |
| `evaluate_k7_continuation_variants.py` | 离线比较同一 K7 前缀下不同后继状态边 | `planning_proxy/runs/*.json` |
| `diagnostics/build_representative_failure_corpus.py` | 从真实完整对局中提取 fallback、超时和预算越界壶面，并按状态语义聚类 | `planning_proxy/diagnostics/*.json` |
| `diagnostics/evaluate_representative_failure_corpus.py` | 串行复现难例集中的真实壶面；默认只跑 1 个，须显式 `--all` 才跑全体；逐样本独立 CP39 进程 | 显式指定的索引 JSON 与逐样本 profile JSON |
| `evaluate_k7_continuation_variants.py` | 从保存的 K3/K5/K6/K7/K8 前缀只替换一条离线状态边并续局到终局；会沿 `sourceReport` 递归拼接同种子上游 BESTSHOT 前缀 | 显式指定的完整续局 JSON |
| `diagnostics/audit_strict_global_tail.py` | 只读汇总严格全局搜索的最慢候选与提交动作分带；不判断有无解 | 显式指定的 JSON 报告 |
| `diagnostics/probe_strict_global_contract.py` | 从真实壶面隔离执行严格全局层；用于比较候选顺序，不代表整手选择 | 显式指定的 JSON 报告 |
| `diagnostics/compare_strict_probe_reports.py` | 比较两份严格候选探针的接触、规则、合同与逐壶终局壶面 | 显式指定的 JSON 报告 |
| `diagnostics/analyze_strict_contract_outcomes.py` | 汇总完整选择器中每条严格候选的合同失败分布与最近落点 | 显式指定的 JSON 报告 |
| `diagnostics/search_multiseed_neighborhood.py` | 已知单种子 witness 附近的三种子严格局部盒搜索；不能证明无解 | 显式指定的 JSON 报告 |
| `diagnostics/analyze_k7_control_geometry.py` | 从真实 K7 壶面提取目标壶、控制槽与其余壶的静态几何关系；不模拟、不判有无解 | 显式指定的 JSON 报告 |
| `search_k8_reply_grid.py` | 从 fixture 或真实报告的 K8 出手前壶面，严格执行候选后接确定性 PPO 最后一手，按多个物理种子终局分数排序 | 显式指定的 JSON 报告 |
| `diagnostics/probe_k16_generic_counterplay.py` | 从真实 trace 的出手前/后壶面生成有限的物理首撞线；默认 `--diversity spin` 复现历史压缩。其余模式仅用于覆盖诊断；`spin_lateral_envelope` 已有挤掉旧候选的反例，`spin_lateral_envelope_preserve_base_low_spin` 先完整保留 `spin` 再以低旋优先补高速横向边界。均不调用 PPO，也不证明反击空间已穷尽 | 显式指定的 JSON 报告 |

所有诊断都必须显式指定输出文件，不能覆盖已有报告。

`probe_k16_generic_counterplay.py --strict-lateral-refine` 默认关闭。它只对初轮最危险的有限父路线做严格横移微细化，
用于暴露毫米级窄碰撞通道；命中可作为“存在反击”的物理见证，未命中绝不表示壶面安全或没有反击。

`search_k8_reply_grid.py` 必须用 CP39 运行严格 PhysX；PPO 会自动通过 `D:\anaconda3\python.exe` 的子进程推理。
不能在 CP39 里直接导入 Torch，也不能在 Anaconda CP311 中加载 CP39 `.pyd`。当要复核真实壶面时优先使用
`--source-report <完整续局报告> --source-shot 15`，不要把别的分支的手工 fixture 当作同一物理前缀。

## 4. PowerShell 调用约定

在项目根目录执行：

```powershell
Set-Location 'D:\Desktop\冰壶\DCCourse'
$cp39 = 'C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe'
& $cp39 -m py_compile planning_proxy\diagnostics\profile_k6_search.py
```

运行带空格路径的解释器必须使用 `& $cp39`；不要省略 `&`。PowerShell 多行临时 Python 诊断使用 here-string 管道：

```powershell
@'
print("temporary diagnostic")
'@ | & $cp39 -
```

查找文件和文本优先使用 `rg`：

```powershell
rg -n "simulate_curling_until_first_contact" D:\esp\tmp\curling_pyphysx_hybrid\src\pyphysx.cpp
rg --files planning_proxy | rg "profile|diagnostic|test"
```

PowerShell 的三个易错点：

1. 路径含空格时，解释器路径存入变量后用 `& $cp39` 执行；普通文件路径统一加单引号。
2. 使用反引号 `` ` `` 换行时，反引号必须是该行最后一个字符，后面不能有空格；不确定时宁可写成一行。
3. PowerShell 的变量是 `$name`，数组是 `@(...)`，不能把 Bash 的 `$()`、`export`、`&&` 原样复制进来。

确认当前实际环境，而不是凭记忆：

```powershell
Get-Location
& $cp39 -c "import sys, platform; print(sys.executable); print(sys.version); print(platform.platform())"
& $cp39 -c "import local_simulator.runtime_loader as r; print(r._resolve_bundled_extension())"
```

用 `Test-Path` 先确认目标；用 `Copy-Item`、`Remove-Item` 前先把目标绝对路径打印出来。不得用通配符对项目根目录、`planning_proxy` 或 `local_simulator` 做删除、覆盖或移动。

## 4.1 平台与运行入口

本地 Windows、对战平台、课程 Notebook 是三个不同运行面，不能互相替代：

| 运行面 | 当前入口/约束 |
|---|---|
| 本地 Windows 严格验证 | 项目根目录，CP39 或 CP313 与对应 `.pyd` 配对 |
| 对战平台 | 保持根目录既有提交布局；不把课程平台目录混进根目录 |
| 课程 Notebook | 使用 Linux CP39 包；在 Notebook 根目录的 `readme` 目录展开；通过 `planner_submission_direct.py` 连接 Unity 服务 |

课程平台连接前，先在界面执行 **Run → Start Curling Server**，再复制本次页面显示的 `ConnectKey`。连接脚本中的主机为 `curling-server-7788.jupyterhub.svc.cluster.local`，端口 `7788`；`Player2` 使用内置模型时，按课程 Notebook 约定在连接键后加后缀 `:0`。每次新开服务都必须重新读取 ConnectKey，旧键不可复用。

课程平台运行日志由提交程序的标准输出与 Notebook 目录内的日志文件共同提供；不要把 Windows 的 `unity_planner.jsonl` 当作课程平台本局日志。

## 5. 原生扩展操作安全规则

1. 默认不直接覆盖 `local_simulator/runtime/pyphysx` 下正在使用的 `.pyd`；已完成等价/性能验证并保留原件时，才按明确授权替换。
2. 新构建先放在独立 build 目录；在新的 Python 进程中通过 `runtime_loader.BUNDLED_EXTENSION` 临时指向它进行对照。
3. 对照必须记录：逐步运动输出、首次接触结果、最终壶面、规则判定、合同判定、平均/P95/最大耗时。
4. 只有等价性和性能都通过后，才复制到运行时目录；复制前保留原文件和哈希。
5. 不得把 Windows `.pyd` 作为课程平台 Linux 的部署产物。

候选扩展测试示例：

```powershell
& $cp39 planning_proxy\diagnostics\run_tests_with_extension.py `
  --extension D:\esp\tmp\curling_pyphysx_hybrid\build-cp39-optimized-20260722\lib\_pyphysx.cp39-win_amd64.pyd `
  planning_proxy.tests.test_first_player_strategy `
  planning_proxy.tests.test_competition_rules `
  planning_proxy.tactical_library_strategy.tests.test_semantic_match_player `
  planning_proxy.tactical_library_strategy.tests.test_semantic_contract_physx_bridge
```

不要用 `python -` 执行包含多进程的 unittest：Windows 子进程会尝试重开 `<stdin>` 并失败。

`profile_k6_search.py` 与 `probe_strict_candidate.py` 都支持 `--extension <候选.pyd>`；该参数只对当前进程
生效，并把实际加载的扩展路径写进 JSON 报告。优先使用该参数，不再手写 `runpy` 临时覆盖。

历史上短暂接入过 `baseline_plus_low_spin_boundary` 的正式求解器实验，已因两条独立完整合同反例撤回；不要通过环境变量、
构造参数或临时补丁复活它。`profile_k6_search.py` 保留对既有 `_adaptive_target_hit_candidates` 的调用记录，以确认某个
回放究竟是否经过该入口；横向边界覆盖研究只保留在 `probe_k16_generic_counterplay.py` 的诊断模式中。

`probe_strict_candidate.py --native-timing` 只能与“首碰撞循环计时诊断构建”搭配。它额外记录摩擦积分、场景
推进、接触扫描和积分细分次数；此构建带计时开销，仅用于定位瓶颈，不能作为性能数据的部署候选。

`diagnostics/compare_k8_state_edges.py` 只比较两份**同一严格前缀**的 K8 完整续局及可选反击报告。它输出 K8 后壶面、
有限反击集和指定对手终局，目的是避免把“有限集合内没找到双清”误当成状态边安全证明。该脚本不能生成提交候选，也不得接入
`ProxyMatchPlayer`。示例：

```powershell
& $cp39 planning_proxy\diagnostics\compare_k8_state_edges.py `
  --baseline planning_proxy\runs\continuation_case003_k8_baseline_20260724.json `
  --candidate planning_proxy\runs\continuation_case003_k8_pure_clear_20260724.json `
  --baseline-counterplay planning_proxy\runs\counterplay_case003_k8_baseline_lateral_refine_k16_seeds_20260724.json `
  --candidate-counterplay planning_proxy\runs\counterplay_case003_k8_pure_clear_lateral_refine_k16_seeds_20260724.json `
  --output planning_proxy\runs\k8_state_edge_case003_20260724.json
```

`diagnostics/probe_k8_terminal_reply_lattice.py` 是 K8 后的离线有限末手反击格。它不读 PPO/aggressive：反击入口来自
当前壶面上的首撞、高速直击和直达按钮三族，并逐条在给定物理种子严格执行。输出负的 `R内最坏分` 或“三种子必败见证”可用于
证明该有限集合中存在风险；没有见证不能证明安全，不能作为状态机的放行条件。它与 `compare_k8_state_edges.py` 的
`--*-reply-lattice` 参数配套使用，默认始终离线。

`diagnostics/probe_strict_global_contract.py --override-clear-roll-target X Y` 只用于审计一个命令行显式给出的清壶滚位合同；
报告会写明搜索边界、已完成严格样本数、多种子候选数、最慢候选和实际耗时。未找到时只能写“当前覆盖/预算内未找到”。它跳过
完整 `choose`，不能用来声称比赛整手的性能或策略效果。

历史上做过“低速高旋候选延后”顺序实验，报告和反例仍保留在 `runs/k7_global_only_*.json`；因未通过当前合同
正例、完整续局和多对手验证，它已从正式求解器撤回。不要通过环境变量或临时改动在提交包中复活该实验。

## 6. 当前已定位的性能事实（2026-07-24）

- 低速高旋输入会触发 `pyphysx.cpp` 中 `speed in [1.0, 1.5)` 的 20 路自适应 Simpson 积分分支。
- 同一输入 `(1.0390625, -0.4680246913580248, 12.4344)` 连续调用 `curling_new_friction_step` 100 次：旧运行时 CP39 扩展约 `7.78s`；优化构建约 `2.10s`。该旧微基准本身不作为等价结论；2026-07-25 已由六类严格终局对照补足本地启用证据，详见 `STATE_MACHINE_ITERATION_LOG.md`。
- 此事实属于求解器性能层，不得直接改写为状态机策略结论。
- 优化构建曾与旧运行时 `.pyd` 哈希不同；完成第 5 节的临时加载对照、保留旧文件后，已于 2026-07-25 启用于两份本地 Windows CP39 运行时。
- 严格全局 Halton 搜索的低速高旋尾部已被独立复现：`(1.0390625,-0.4680246914,12.4344)` 会无首次碰撞地跑满 5000 步，
  旧 CP39 约 27 秒。优化构建在同一输入上约 10.7 秒且单例最终壶面相同；其本地启用依据是后续六类严格物理等价对照，
  不把这条单例或本地启用解释为整局胜率结论。

## 7. 提交前最小检查

```powershell
& $cp39 -m py_compile planning_proxy\evaluate_vs_teammate_ppo.py planning_proxy\strict_refine.py
& $cp39 -m unittest planning_proxy.tests.test_first_player_strategy planning_proxy.tests.test_competition_rules
git diff --check
```

工作树可能同时存在其他会话的修改。不得使用 `git reset --hard`、`git checkout --`、批量覆盖或清理未跟踪文件。
