# 出手求解器应用

给实际起始场景和完整目标，返回合法且经模拟验收的 `BESTSHOT(v,h,w)`，或当前预算内未找到。默认不扫冰。它是连续参数搜索器，不是已训练的反推神经网络。

## 运行

在仓库根目录使用 Windows x64 / CPython 3.9：

```powershell
python -m training_research.shot_solver --scene training_research/fixtures/sampled_goal_draw.json
python -m training_research.shot_solver --scene training_research/fixtures/sampled_goal_collision.json --budget-seconds 10 --max-calls 256
python -m training_research.shot_solver --scene training_research/fixtures/sampled_goal_double.json --output training_research/runs/my_double.json
```

输出文件必须新建，不会覆盖已有报告。增加 `--include-records` 可保留实际搜索的完整物理记录。机器速度会影响同一预算下的搜索覆盖。

长期运行时复用实例，各请求串行调用：

```python
import json
from pathlib import Path
from training_research.shot_solver import BudgetedShotSolver

scene = json.loads(Path("training_research/fixtures/sampled_goal_draw.json").read_text(encoding="utf-8"))
solver = BudgetedShotSolver()  # 模块和原生场景启动在单次搜索计时之外
result = solver.solve(scene, budget_seconds=10, max_calls=256)
if result["success"]:
    v, h, w = result["shot"]
```

## 输入

`active_index` 为本次投壶的零基编号；已有壶的原始编号必须更小。每颗旧壶提供米制本地 `x/y` 和朝向 `yaw`，角度为弧度。未提供 yaw 时默认零，并在标准化输入中记录该假设。

`selection` 必须包含 `tactic` 和 `goal.stones`。目标字典的 key 是当前物理 slot 的字符串，而不是同色壶重新排序后的序号：

| 目标类型 | 含义 |
| --- | --- |
| `IN_REGION` | 壶仍启用，终点进入指定 `x/y/radius` 圆；半径单位米。 |
| `OUT_OF_PLAY` | 最终停用。 |
| `OUT_OF_HOUSE` | 离开大本营范围，或已停用。 |
| `SURVIVE` | 最终仍启用。 |
| `ANY` | 不限制该壶。 |

首碰和实际碰撞链约束还可包含 `first_contact_any`、`require_single_first_contact`、`required_collision_pairs`；无碰撞落点可包含 `require_no_contact`。全部目标同时验收，规则违规、未停稳或缺少必需碰撞不能作为成功。

`tactic=double_hit` 使用现有双飞搜索分支，要求两颗对方目标、单一首碰及目标间实际碰撞。其他已支持战术名走通用终态搜索。只给“想双飞”文字还不足以定义具体当前目标，调用方应先完成角色绑定。

## 输出与随机性

可选搜索方案正在做固定性能核对照，默认仍为 `baseline`。例如 `BudgetedShotSolver(search_profile="safe_stream")` 会先验证一个廉价候选，失败后沿用原初值池；`search_profile="wide_dfols"` 测试更广的入口与较长的 DFO-LS 局部拟合，需先安装根目录 `requirements-solver-research.txt`。CLI 可传 `--search-profile`。不同实例独立选择方案，不修改全局求解器。阶段性数据和限制见 [10 秒求解研究](solver_strategy_research_20261016.md)，实验方案还不能宣称达到近乎全覆盖。

成功输出 `success=true, shot=[v,h,w]`；失败输出 `shot=null`。`diagnostics.best_effort_shot` 是诊断，不是可提交动作。`NOT_FOUND_WITHIN_BUDGET` 不证明无解。

默认只要求一个导航种子成功。`required_seed_successes=3` 要求三个搜索种子都通过，所有模拟仍计入同一个预算。未知比赛世界的摩擦种子不由此变成已知；额外种子稳定性应单独衡量。

十秒是开始新调用前检查的同步预算，正在执行的一次模拟允许结束；不是硬实时中断。启动、日志序列化和写盘不计入返回的搜索时间。

## 随包依赖与历史成绩

- [精简采样测试数据](datasets/forward_samples_20261004/README.md)：37,061 条原始正向采样的可直接调用请求，压缩约 4.03 MiB，参照答案单独保存。
- `legacy_support/`：原样保留的旧数学提案代码和标定表，有逐文件哈希；不再依赖本机旧交接目录。
- `assets/inverse_contact_atlas_v6_20261004.npz`：小型经验初值库。查询前排除当前 `scene_key` 的所有采样，不使用当前局的参照出手作为初值。NPZ 字节与 2026-10-04 测试版本相同。
- `inverse_dataset/`：输入检查、规则/终态验收、批量正向采集与训练编码。
- `local_simulator/`：实际完整物理推演；物理依赖和可用加速模块随应用保留。

历史完整测试为 292/306，双飞 14/14；成功搜索中位数 2.806 秒，额外五种子全通过为 237/292，仍剩 14 个未解任务。详见 [范围与优化记录](inverse_solver_optimization_20261004.md)、[剩余任务](inverse_remaining_14_diagnosis_20261004.md)。完整原始采样和逐次搜索日志仍在本地 `runs/`；Git 保存 [可移植结果摘要](results/inverse_solver_20261004_summary.json)。三个随包应用输入只用于安装和链路检查，不当作新的独立成功率测量。

2026-10-16 的依赖整理最初没有改算法；之后开展了独立的 10 秒搜索研究。历史性能仍只对应旧版和旧目录，本次新实验按独立目录统计，见上文研究记录。公开默认保持 `baseline`，可选实验方案不改变物理计算或验收合同。

研究用法示例：

```powershell
python -m training_research.shot_solver --scene training_research/fixtures/sampled_goal_collision.json --search-profile wide_dfols --budget-seconds 10
python -m training_research.benchmark_compact_solver --profile contact_de --cpu 4 --output training_research/runs/new_contact_de
```

研究依赖安装命令为 `python -m pip install -r requirements-solver-research.txt`。固定 704/1024 题目录的解压、计时边界、核选择和成功证据检查见 [基准说明](benchmarks/README.md)。`wide_dfols` 的已审计成绩是 681/704（680 项严格不超过 10 秒），不代表默认 `baseline` 的成绩。

`contact_de` 使用几何初值、短局部拟合和接触坐标差分进化，全部共用单个预算。`learned_dfols` / `impact_learned` 还依赖本地离线模型；先安装 `requirements-solver-learning.txt`，再分别运行 `python -m training_research.contact_seed_forest` 或 `python -m training_research.contact_seed_forest --coordinate-mode impact --output training_research/runs/contact_seed_forest_impact_v2_paired_20261016`。模型按构型整折排除，不能用当前任务的参照动作当在线初值。

精简数据的 `record_id` 会跨文件重复；输入与真值必须按同名 gzip 文件的行配对，外部任务目录用完整请求指纹查回配对位置。`compact_pairs.py` 实现此规则。学习初值默认路径均已切换到 `_paired_20261016`，旧路径模型保留作实验档案，不再由当前默认配置加载。分布初值 `distribution_dfols` 在修正的接触模型建立后运行 `python -m training_research.contact_distribution_prior`；完整壶面版本 `full_distribution` 再运行 `python -m training_research.full_contact_prior` 构建。所有模型输出目录必须新建。

`full_augmented` 先按原顺序验证最多 24 个 `wide_dfols` 候选，再按需加入最多 6 个完整壶面模型提案；依赖与 `full_distribution` 相同。`region_feasible` / `region_routes` 测试区域不等式拟合与不同已观测碰撞模式的入口。这些方案都仍是实验，不能把各自成功项取并集作为一套算法成绩。学习模型权重留在本地 `runs/`，克隆后需用随包原始数据按上述命令重建；它们不是运行默认应用或 `wide_dfols` 的前置条件。

`full_augmented` 最新完整 704 题批次为 684 个合格解，全部严格不超过 10 秒，成功中位数约 0.205 秒。尚有 20 项漏解，额外 1024 题对照仍在运行；该研究方案没有升为公开默认。
