# `planning_proxy/runs/` 报告索引

`runs/` 当前约有 1,927 个文件。它是实验和回放的证据库，不是源码目录；同名或相近 seed 的报告可能来自不同代码版本，不能直接横向比较。

## 先看哪些报告

| 目的 | 首选报告/索引 | 说明 |
|---|---|---|
| 当前版本的完整基线 | `benchmark_current_*.json` | 当前状态机与 PPO/aggressive 的整局基线。 |
| 真实 Unity 失败来源 | 项目根目录 `unity_planner.jsonl` | `runs/` 内回放应注明其来源和物理前缀。 |
| 真实 fallback 结构集合 | `diagnostics/representative_failure_corpus_v4_20260724.json` | 440 局扫描、522 事件、185 结构簇。 |
| K8 单外场己壶的合同对照 | `case21457791_k8_one_outer_reclaim_ppo_20260724.json`、`case21457792_k8_one_outer_reclaim_ppo_20260724.json`、`case21891642_k8_one_outer_reclaim_ppo_20260724.json` | 一个平局改善、两个失败；候选已撤回。 |
| 分层入口严格校准 | `case21891642_k8_stratified_topology_audit_v2_20260724.json`、`case21891642_k8_stratified_topology_audit_v3_one_start_20260724.json` | 已知成功局用于检查诊断是否漏解。 |
| 两个困难壶面的覆盖证据 | `case21457791_k8_stratified_topology_audit_v2_20260724.json`、`case21457792_k8_stratified_topology_audit_v2_20260724.json` | 当前覆盖内未找到完整合同，不能解释成无解。 |
| 严格耗时分解 | `case21457791_k8_stratified_topology_audit_v3_timing_20260724.json` | 确认瓶颈是严格候选数量，不是单候选物理长尾。 |

完整解释、代码版本、正反例和撤回决定都以 `../STATE_MACHINE_ITERATION_LOG.md` 为准。

## 文件名前缀分类

| 前缀/模式 | 含义 | 是否可直接当当前结论 |
|---|---|---|
| `benchmark_current_*` | 当前代码版本完整基线 | 可以，但需确认对手、种子与时间戳。 |
| `case*` | 某个明确问题的离线对照 | 只能用于该报告写明的假设。 |
| `k3_*` 至 `k8_*` | 分手/局部合同或续局实验 | 默认不能代表整局胜率。 |
| `ppo_*` | PPO 对手回放 | 不能推到其他对手。 |
| `unity_*` | Unity/平台日志或重放 | 优先用于发现真实失败结构。 |
| `strict_*`、`analytic_*`、`proxy_*` | 求解器或粗代理诊断 | 只能说明物理候选和性能，不能判断状态机价值。 |
| `full_*`、`first_player_*` | 整局或状态机专题审计 | 仍需核对来源版本。 |

## 不完整或不可引用的运行

若脚本在中断、超时或异常前没有写出 JSON 报告，该运行不属于证据。例如 K8 的
`case21457791_k8_stratified_topology_audit_v3_budget32_20260724.json` 未成功写出，不能被当作“32 起点方案通过/失败”的完整统计；已知事实仅是该运行超过比赛时限而未完成。

## 新报告登记规则

新报告文件名应包含：`来源/局面`、`K 手或范围`、`对手或物理条件`、日期。每次新增以下任一类报告时，同时更新
`STATE_MACHINE_ITERATION_LOG.md`：

- 生产状态机改动的完整对局；
- 新的真实 fallback 构型；
- PhysX 等价性或性能对照；
- 已撤回的候选策略。

不要覆盖已有报告；同一实验重跑请使用新日期或版本后缀。
