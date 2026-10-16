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

2026-10-16 仅整理依赖路径、应用入口和文档，算法及数值资产没有重新调参；历史性能不是这次维护重新跑出的成绩。
