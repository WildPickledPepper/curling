# 精简求解测试数据

从六批本地原始正向采样提取，37,061 条合法、停稳的实际采样记录、306 个不同起始构型。没有加入逆向搜索得到的成功记录，没有重新造局面。所有原始记录均合法且停稳，因此本次未排除任何记录；目标按实际达成终态构造，不表示原先每个具名战术都成功。

原始 104 个分片合计 880.12 MiB。精简数据不压缩约 75.47 MiB，12 个 gzip 文件合计 **4.03 MiB**。起始坐标、朝向、目标坐标及参照参数均未四舍五入。

## 求解器需要什么

输入文件 `*.inputs.jsonl.gz` 每行是一份可直接传入 `BudgetedShotSolver.solve()` 的请求：

| 字段 | 用途 |
| --- | --- |
| `active_index` | 本次新投壶的实际投壶编号。 |
| `stones` | 起始在场壶，每颗只保留 `index/x/y/yaw`。 |
| `selection` | 实际终态构造的目标圆区/出界要求，以及首碰、碰撞对等验收条件。 |
| `record_id`、`scene_key` | 来源关联和物理构型标识，不是参照出手。 |

起始壶面沿用采样时传入的原始 reset 坐标和 yaw，以保持原构型身份；目标由实际 `physical_final` 构造。落点圆半径为 0.15 米，双飞沿用已有目标定义与实际碰撞要求。

对应的 `*.references.jsonl.gz` 与输入逐行对应，通过 `record_id` 关联，只供搜索之后复验：

- `shot`：采样时的已知成功出手，不能作为在线初值。
- `physics_seed`：采样时种子，只用于诊断；未知比赛世界的种子仍未知。
- `physical_final`：出手壶与原在场壶的实际终态，只保留 `index/enabled/x/y/yaw`。
- `source_shard/source_line`：原始数据来源行号。

无需 PhysX 的位置、四元数、速度重复表示或时钟/RNG 内部状态即可使用此测试接口。这份数据用于出手搜索测试，不能替代 Unity 逐位物理对齐采样。

## 直接运行

```python
import gzip
import json
from pathlib import Path
from training_research.shot_solver import BudgetedShotSolver

root = Path("training_research/datasets/forward_samples_20261004")
with gzip.open(root / "inverse_dataset_smoke_20261004.inputs.jsonl.gz", "rt", encoding="utf-8") as f:
    request = json.loads(next(f))

solver = BudgetedShotSolver()
result = solver.solve(request, budget_seconds=10)
print(result["success"], result["shot"])
```

一次有实际成功即可纳入已知可解数据；其他种子是否稳定是另一项指标。37,061 条是目标任务记录数，不能当作 37,061 个独立起始构型或新的成功率结果。

## 来源与复查

`manifest.json` 记录各源分片和压缩输出的 SHA-256、条数与字节数；`validation.json` 记录逐条与原始数据核对的结果，及旧 306 局输入的一致性。完整 raw 文件仍留在本地，不随精简包重复保存。

提取脚本：`training_research/export_solver_samples.py`。已有输出目录不会被覆盖；要重新提取请另选新目录：

```powershell
python -m training_research.export_solver_samples --output training_research/runs/compact_samples_rebuild
```
