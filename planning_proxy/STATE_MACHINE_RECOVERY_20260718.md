# 先手状态机恢复说明（2026-07-18）

## 当前目标

固定 K1 为中线守壶；用本地确定性 PPO 作对手，逐步完善 K2--K8 的 `S_k -> G_k` 状态机。验收不是“代码可跑”，而是多个严格 PhysX 物理种子下的完整 K1--K8 回放均赢或不输。

## 已确认的事实

- K1 使用固定中线守壶 `OPENING_CENTRE_GUARD_SHOT`。
- K6 曾有合同错误：右侧威胁的 G6 需要 `physical_clear`，旧代码仍保留 `physical_displace`，导致可行候选被拒绝。已修正。
- 固定 K5 跨侧落位 `[3.064, 1.702, -9.541]` 后，K6 明确候选 `[5.5, 1.45, -10.5]` 可实现“清右侧敌壶、保留两颗营内得分壶”。
- 该 K5--K8 固定轨迹对 PPO 的严格回放最终为先手 `+2`：
  `runs/ppo_k5_cross_layer_fixed_g6_to_k8_seed20260718_v3.json`。
- K8 进一步抽取到 raise 候选 `[3.0, 0.0, 0.0]`；在 fixture `ppo_k8_guard_raise_stack_seed20260718_before.json` 上，经三个物理种子和 PPO 最后一壶检验，最差 `+1`。

## 已落地修改

- `first_player_strategy.py`
  - G6 的 `sixth_clear_right_threat_keep_two_layers` 以“至少两颗营内壶”验收，不能错误要求两颗最内圈壶。
  - 新增 K8 phase `eighth_raise_centre_guard_into_scoring_stack`：要求至少三颗己方营内壶、出手壶进入前方目标区。
- `evaluate_vs_teammate_ppo.py`
  - K6 右侧威胁动态 G6 明确设为 `opponent_action="physical_clear"`。
  - K8 窄状态（己方 index 0/10/12，敌方 index 13）直接严格复验 raise 候选，再提交；模式名为 `first_player_k8_centre_guard_raise_scoring_stack`。
- 新 fixture：
  - `fixtures/ppo_k6_after_cross_layer_seed20260718_before.json`
  - `fixtures/ppo_k8_guard_raise_stack_seed20260718_before.json`

## 已通过检查

```powershell
python -m py_compile planning_proxy\first_player_strategy.py planning_proxy\evaluate_vs_teammate_ppo.py
python -m unittest planning_proxy.tests.test_first_player_strategy planning_proxy.tests.test_competition_rules planning_proxy.tactical_library_strategy.tests.test_semantic_match_player planning_proxy.tactical_library_strategy.tests.test_semantic_contract_physx_bridge
```

最近完整执行时 45 个测试通过；K8 接入后仅重跑了 `test_first_player_strategy`，34 个通过。新会话应先重跑完整套测试。

## 尚未完成（不能宣称达标）

1. 用**已接入 K8**的版本重跑完整 K5--K8 固定轨迹，确认不再出现 `safe_fallback_after_mads`。
2. 从 K1 开始跑完整对 PPO 回放，而非只从 K5 fixture 继续。
3. 至少三个独立物理种子验收完整 K1--K8；每局最终分数必须 `>= 0`。
4. 若有任一败局，定位最早第一次偏离显式 G 的 K 手，只修该 `S_k -> G_k` 边，不做泛化攻击脚本。

## 注意

- 不要把单条 `+2` 轨迹称为稳定获胜。
- K8 raise 分支目前按壶 slot 身份识别，是已验证窄状态，不是泛化终局战术。
- 工作区可能有其他会话的未提交修改；不要重置或覆盖无关文件。

## 2026-07-19：连续 PhysX 重放与泛化恢复进展

### 已修复的泛化瓶颈

- **规则回滚不能只存动作。** PPO 的早期自由防守区犯规会触发壶面 RESET；
  仅以 `x/y/yaw` 恢复后再前瞻会丢失 PhysX 隐状态，K7 的“有解”会在真实 K8
  失效。评测器现在同时记录每一手动作和回滚壶面，K7/K8 前瞻从 K1 连续重放
  两者。
- **K7/K8 不再只枚举固定 draw。** 当前壶面先经廉价粗代理提取“首撞当前
  目标壶”的不同旋转拓扑，随后每条仍由严格 PhysX 与 PPO K16 终局筛选；该
  初值不是 fixture 动作，也不直接提交。
- **完整防御合同无解不等于物理清壶无解。** 主 MADS 合同失败后，状态机对最多
  三条自适应首撞初值做三物理 seed 严格纯清复核；只有规则合法、清壶目标满足且
  己方交换未超限才可取代默认 `(3,0,0)` 降级。
- **预算保护。** 内部候选搜索截至外部 105 秒前 5 秒，避免不可抢占的一次 PhysX
  结算导致平台超时；报告仍以完整 105 秒合同记录。

### 当前本地证据（先手、完整 K1--K16、PPO 对手）

下列报告均以最终分 `>= 0` 且 `decisionWithinBudget=true` 为验收。它们是独立
物理 seed，不是从 fixture 中盘恢复：

| seed | 最终先手分 | 报告 |
|---:|---:|---|
| 20713579 | 0 | `runs/ppo_k1k8_unseen_validation_seed20713579_adaptive_pure_clear.json` |
| 20824680 | 0 | `runs/ppo_k1k8_unseen_validation_seed20824680_adaptive_pure_clear.json` |
| 20931415 | +1 | `runs/ppo_k1k8_unseen_validation_seed20931415_adaptive_pure_clear.json` |
| 21027182 | +2 | `runs/ppo_k1k8_unseen_validation_seed21027182_budget_margin5.json` |
| 21116180 | +1 | `runs/ppo_k1k8_unseen_validation_seed21116180_budget_margin5.json` |
| 21235813 | 0 | `runs/ppo_k1k8_unseen_validation_seed21235813_budget_margin5.json` |
| 21346729 | 0 | `runs/ppo_k1k8_unseen_validation_seed21346729_budget_margin5.json` |
| 21457791 | +4 | `runs/ppo_k1k8_unseen_validation_seed21457791_budget_margin5.json` |
| 21568347 | +2 | `runs/ppo_k1k8_unseen_validation_seed21568347_budget_margin5.json` |
| 21679458 | +1 | `runs/ppo_k1k8_unseen_validation_seed21679458_budget_margin5.json` |

固定十局独立集统一审计结果：全部完成、最低最终分为 `0`、无预算超时、最大
单手决策为 `102.635s`。当前完整回归为 49 项通过。该本地验收门已经通过；以上
样本仍不足以声称对所有 PhysX 轨迹“稳定必胜”，继续按“发现负例 -> 定位最早
不可恢复状态 -> 扩展严格认证状态边 -> 重跑未见 seed”闭环推进。

额外压力样本 `runs/ppo_k1k8_stress5physics_seed21027182_budget_margin5.json`
把规划器内部严格复核从 3 条提高到 5 条物理 seed；完整终局为 `+1`、无超时、
最大单手 `101.874s`。这是更强覆盖的单一样本，不替代独立 seed 集验收。

## 2026-07-19：去除对手预测后的反例审计（仍未达标）

此前表格中的 PPO 结果不能被视作“对任意对手的稳定胜局”证据：部分本地验收曾
注入 PPO 末手前瞻。比赛默认路径现在已关闭该能力；它只能离线暴露反例，不能决定
线上出手。

### 已确认可内化的部分

- K7 的密集壶群不应把“完整双门防线无解”误当成“没有可击打路线”。对 PPO
  `21457791` 的 K7，至少 12 条首撞拓扑可在三种子下清掉当前威胁、零己方损失、
  保留两颗营内壶。
- `evaluate_vs_teammate_ppo.py` 现在把这类 K7 清壶解保存为**严格 PhysX 保底**，
  继续搜索完整防线、repair 和镜像形，最后才使用保底；不会再提交固定
  `(3,0,0)`，也不会在找到不输本手的候选后提前停止搜索。
- K6 的“侧向威胁清除后保两层”已改为按当前威胁侧镜像，而非仅右侧分支。该改动
  是相对按钮的状态角色，不匹配历史 slot 或坐标。

49 项单元/规则/语义桥回归在上述搜索调度改动后通过。

### 已证伪、不能直接上线的补丁

- 在该反例的 K8，旧 PPO 反事实能给出 `[3,-0.73,-5]` 并报告 `+4`，但原因是
  PPO 最后一壶清掉了自己的壶。通用末壶反击搜索能立即找到击破该壶面的路线，
  所以不能把这条动作或 PPO 的未来回应内化成状态机边。
- 同一 K8 壶面中，12 条“清当前威胁”的严格物理解和 8 条不强制清壶的绕行/占位
  解，都被 `validate_final_defence.py` 的对手无关直线/旋进/撞击反击族击破。
  这说明此 K8 子状态本身没有当前搜索预算内的可守解；应继续向前定位，而不是
  给 K8 加坐标补丁。
- 反例的 K4“补第二错层营内锚”经 46,965 条宽粗筛、1,927 条净空路径、80 条
  三种子严格复核未找到解；K4 的 100 条 raise 候选也未能把中线守壶推进为中心锚。
  K3 清中心威胁后的局部 567 条严格细化，三种子下同样未进入旧的狭窄锚区。
  因此当前早盘目标区域/可达角色需要重建，不能靠延长搜索时间解决。

### 当前最早结构性失效

PPO `21457791` 的 K3 单锚会被 K4 拆除，而 K4 在当时实际几何下不能恢复两层营内
结构；K5--K8 的连续清壶只是后果。后续应把 K3/K4 从“命中固定锚区”改为：

1. 当前威胁已清；
2. 出手后形成在有限、对手无关末壶反击族下压力最小的可达锚/屏风角色；
3. 该角色以镜像拓扑和严格 PhysX 合同表达，并用扰动壶面及 PPO、aggressive
   完整回放验证。

在此完成前，不能宣称稳定胜局或构建最终提交包。

## 2026-07-19：历史语义候选库的独立对照（仅作候选生成）

以 `--semantic-tactical-library` 运行时，历史数据只提供与当前壶面相近的**角色
区域**，每个区域仍由严格 PhysX、多物理 seed 和规则合同反解；没有调用 PPO
未来动作，也没有命中历史坐标 fixture。

- PPO `21457791`：语义候选库整局为 `+1`，K3 选择了一个左前侧单清/落区合同，
  K6/K7 选择放置型角色，而不是主状态机的“见上一壶即清”。这证明历史语义可
  扩展当前候选空间。
- PPO `20713579`：同一模式整局为 `-1`。K8 原先错误地清了一颗 `x=0.18` 的
  边缘壶；修复为“该壶不作为敌方主威胁、改补右低门”后仍为 `-1`，因为 PPO
  最后一壶直接清掉补门壶并占分。

因此语义库目前只能作为 `S_k` 下的候选角色生成器，不能直接替代主状态机的
价值/排序。所有 K8 repair draw、guard 和 clearing 都必须进入同一个对手无关
末壶反击筛查；不能仅因本手 `tacticalGoalMet=true` 就接受。

## 2026-07-19：把历史补丁内化为 K6 的盘面门，而非坐标分支

历史语义 K6 并非应当删除的“无用补丁”，而是两类当前盘面下的反例对：

- PPO `20713579` / `21457791`：K6 前营内己方壶不超过一颗，历史低位锚经过
  严格 PhysX 认证后可保留；前者的实时完整日志已走到第 16 手并以 `+3` 结束，
  后者已有完整 `+1` 报告。
- PPO `21568347`：K6 前已有两颗己方营内壶；继续追加历史落区会形成一次双清
  目标，旧语义 K6 路线的完整结果为 `-1`。

状态机现在不读取历史 state id、对手名、未来动作或精确 x/y fixture，而是在
`SemanticTacticalMatchPlayer` 的 K6 计算通用角色谓词：`ownInHouse >= 2` 时把
K6 交回当前完整壶面的清壶/repair 状态机；否则历史低位锚只作为严格 PhysX
候选。新的完整 PPO `21568347` 回放以 `+1` 获胜。该门是“从补丁提炼反例条件”
的第一条可验证实例，不构成稳定胜局的最终声明。

回归：相关单元/规则/语义桥共 52 项通过；`git diff --check` 通过。
