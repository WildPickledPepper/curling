# 固定目录与可移植验收证据

这里保存 2026-10-16 出手搜索研究的小型工件。原始前向样本及其真值仍在 [datasets/forward_samples_20261004](../datasets/forward_samples_20261004/README.md)；`certificates/` 中的动作是后来逆向搜索得到的结果，不能混入原始前向真值。

## 固定任务目录

`catalogs/` 的 gzip 解压后都是可以直接传给 `--catalog` 的 JSON 数组，不含参照动作或源种子。

| 文件 | 任务 | 用途 |
| --- | ---: | --- |
| `development306_20261016.json.gz` | 306 | 每个物理构型一题，旧基线和候选的共同目录。 |
| `additional398_20261016.json.gz` | 398 | 补齐每个构型与战术类别的组合；与前 306 题不重叠。 |
| `development704_20261016.json.gz` | 704 | 上述任务的完整目录，306 个构型、17 个标签；顺序与两个分区的拼接顺序不同。 |
| `hard23_20261016.json.gz` | 23 | 旧主候选的正常漏解，21 个物理构型；只用于开发诊断。 |
| `validation1024_20261016.json.gz` | 1024 | 候选固定前选定的额外目标，294 个构型；仍来自同一布局范围，不能称为未见布局家族。 |

[目录清单](catalogs/manifest_20261016.json) 保存压缩与解压后的 SHA-256。所有请求均来自真实前向样本；1024 题按完整目标去重并排除 704 个开发目标，即使普通分支的战术标签不同也不重复计入。

在仓库根目录解压需要的目录：

```python
import gzip
from pathlib import Path

root = Path("training_research")
target = root / "runs/reproduce704_catalog.json"
target.parent.mkdir(parents=True, exist_ok=True)
with target.open("xb") as output:
    output.write(gzip.decompress((root / "benchmarks/catalogs/development704_20261016.json.gz").read_bytes()))
```

Windows x64 / CPython 3.9 下运行新的完整批次：

```powershell
python -m pip install -r requirements-solver-research.txt
python -m training_research.benchmark_compact_solver --profile wide_dfols --cpu 4 --catalog training_research/runs/reproduce704_catalog.json --output training_research/runs/reproduce704_wide --replay-references
```

`--cpu` 必须选择本机的性能核；CPU 4 是研究机器 i7-14700 的选择，不是通用拓扑保证。运行目录必须新建。基准在所有计时搜索结束后才打开参照复验。物理环境与模块预热在单次计时外，输入验证和候选生成在内；正在执行的末次同步调用可以略超预算。历史 681/704 来自两个预热进程分区和一次有事件证据的中断重跑；上面的完整目录命令是一个新进程批次，不能承诺逐项、逐位复现旧成绩。物理历史与随机输入的限制见 [研究记录](../solver_strategy_research_20261016.md)。

## 已保存的 704 题结果

| 方案 | 找到解 | 严格不超过 10 秒 | 成功中位数 |
| --- | ---: | ---: | ---: |
| `wide_dfols` | 681/704 | 680 | 224.753 毫秒 |
| `full_augmented` | 684/704 | 684 | 205.415 毫秒 |

[结果证据](certificates/wide_dfols704_20261016.jsonl.gz) 依完整 704 题目录顺序逐行保存：完整请求、请求指纹、来源运行及索引、成功状态、返回动作、计时，以及每个成功动作在实际调用中记录的终态、碰撞和规则证据。失败行没有可执行动作。它不包含用于生成候选的原始参照出手。

681 项记录满足原始全部验收条件，680 项严格不超过 10 秒，成功耗时中位数约 224.753 毫秒。修正前原始分区为 680 个成功；只替换了一个已证实系统睡眠中断的任务，没有替换普通漏解。原报告哈希与替换请求记录在 [证据清单](certificates/wide_dfols704_20261016_manifest.json)，系统事件摘要见 [中断证据](../results/sleep_interruption_evidence_20261016.json)。

新的 [完整壶面模型结果证据](certificates/full_augmented704_20261016.jsonl.gz) 按相同目录格式保存，684 个成功全部满足原验收合同，严格不超过 10 秒。[清单](certificates/full_augmented704_20261016_manifest.json) 与 [摘要](../results/compact_search_full_augmented704_paired_20261016_summary.json) 保存哈希和逐项改善/退步。它是一个完整预热批次，没有中断替换；与旧方案匹配请求后新增成功 6 项、退步 3 项，但运行顺序、进程分区与物理历史不同，不能作为只改变优化器的受控比较。额外 1024 题对照未完成，默认方案未切换。

无需重新调用原生物理即可检查所存证据与目录、摘要的一致性：

```powershell
python -m unittest training_research.tests.test_published_solver_results
```

这是对已记录结果的重新验收，不能代替在另一个完整物理历史或其他随机种子下重新模拟。原始逐次调用、源码快照和离线学习权重继续保留在本地 `runs/`；Git 保存源码、目录、摘要与上述最小成功证据。学习模型需按 [求解器指南](../SOLVER_GUIDE.md) 重建，`wide_dfols` 无此依赖。
