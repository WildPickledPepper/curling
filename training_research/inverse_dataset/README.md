# 反推出手参数：造数据与编码

在仓库根目录运行 `python -m training_research.inverse_dataset.cli`。
`collect` 使用当前加速模拟器，已验证 Windows CP39；`encode` 和在线输入编码只需 NumPy，可在训练用 Anaconda 运行。
采样域为静止初始盘面、固定 BESTSHOT 释放、不扫冰；有限采样用于覆盖连续空间，不声称穷尽全部情况。

## 批量采集

约 64,000 次物理请求（重复盘面会合并），每个结果最多生成 8 条目标视图：

```powershell
& 'C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python39_64/python.exe' `
  -m training_research.inverse_dataset.cli collect `
  --output training_research/runs/inverse_dataset_batch1 `
  --scenes 1000 --shots-per-scene 32 --physics-seeds 2 --workers 2
```

局面族：空场、营内单壶、守壶遮挡、双壶、传击链、营内簇、多壶分散、8–15 壶密集盘面。
出手轮次、阵营、间距、坐标和朝向变化。已出手壶只使用当前编号之前的 slot，并拒绝重叠盘面。
mixed 候选包含列对齐初值、附近扰动和全域分层抽样，覆盖正反旋转。列对齐初值只是候选，不被当作物理反解。
默认速度 2.4–6.0；`--v-min 0.2` 可补充更低速度。试采中低速高旋请求可能明显更慢，但仍完整推演。

网格模式对每个局面遍历所有 v/h/w 组合；以下每局面 5×5×3=75 个候选：

```powershell
& 'C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python39_64/python.exe' `
  -m training_research.inverse_dataset.cli collect `
  --output training_research/runs/inverse_dataset_grid `
  --scenes 100 --sampling grid --physics-seeds 3 --workers 2 `
  --v-grid 2.7,3,3.4,4.2,6 --h-grid=-1.5,-0.5,0,0.5,1.5 --w-grid=-10,0,10
```

网格忽略 shots-per-scene；manifest 保存实际请求计划数。
`--families double_pair,guarded_target` 可定向增采某些族。
当前预测器的 BESTSHOT 实际限幅为 v≤6、|h|≤2.23、|w|≤15.7，不给被夹断前的无效参数建立不同标签。

## 导入局面和已有参数

`--scene-json 文件路径` 可重复；设置 `--scenes 0` 时只处理导入局面。输入示例：

```json
[
  {
    "scene_id": "game1-shot5", "group_id": "game1", "active_index": 4,
    "stones": [
      {"index": 1, "owner": "opponent", "x": 2.1, "y": 4.88, "yaw": 0},
      {"index": 3, "owner": "opponent", "x": 2.7, "y": 4.88, "yaw": 0}
    ],
    "candidate_shots": [[4.2, -0.275, 0], [6, 0.325, 0]]
  }
]
```

壶身份按 index 保留，阵营需符合交替出手编号；坏局面进入 rejected_scenes.json。
未知朝向在采集入口明确取零并标记 yaw_source=default_zero，不声称恢复历史朝向。
candidate_shots 优先作为候选重新模拟，旧终点不用于训练标签。
`--scene-log 日志路径` 读取本地 SERVER_TELEMETRY 的初始盘面和旧出手候选；同一日志目录按同源对局分组。
JSON 的 group_id 可把同一对局及其局面扰动归组；没有指定时使用初态的稳定哈希。

## 输出与续采

- manifest.json：计划/完成数量、场景族与具名战术覆盖、分组统计、配置、代码/内核/资产哈希及分片校验和。
- scenes.json、rejected_scenes.json：实际输入和拒绝原因。
- encoding.json：特征顺序、目标类型、归一化、战术编号。
- shards/*.raw.jsonl：初始完整状态、出手参数、16 壶完整终态、随机输入种子/消费/时钟、实际碰撞进入事件、规则检查和耗时。
- shards/*.samples.jsonl：每条样本实际达成的目标与原始请求编号。
- shards/*.npz：无需 pickle 的训练数组。
- shards/*.done.json：完整分片的校验收据。

每个进程拥有独立持久 PhysX Scene。候选之间通过原 reset_positions 恢复盘面及朝向，再完整运行原 FixedUpdate/Update 调度。
碰撞观察只读取驱动器已经返回的报告，不额外读取/清空 PhysX 报告。
原始记录保留失败、未停止、违规结果；这些结果不产生成功反推正样本。
rules_final 是仓库当前自由防守区/中线规则检查下的回滚视图，不冒充官方服务器完整裁判结果。

原命令加 `--resume` 可续采，可调整 workers。配置、输入、代码或运行时变化会拒绝混写。
完整分片先核对哈希；未完成分片重跑。原始记录逐条落盘，完整分片原子替换。
默认每分片 8 个场景，避免全部训练数组驻留内存。大批原始完整状态可能占用数 GB，请预留磁盘。

## 输入输出契约

训练与未来 PPO 调用使用相同编码器：

```python
from training_research.inverse_dataset.schema import encode_input, ACTION_SCALE
inputs = encode_input(initial_16_slot_states, {
    "stones": {
        "1": {"type": "OUT_OF_PLAY", "required": True},
        "3": {"type": "OUT_OF_PLAY", "required": True},
        "4": {"type": "IN_REGION", "x": 2.375, "y": 4.88,
              "radius": .3, "required": False}
    }
}, active_index=4, tactic="double_hit")
# future_network(inputs) -> normalized_shots [K,3]
# physical_shots = normalized_shots * ACTION_SCALE
```

initial_16_slot_states 为完整 16 slot，包含 index/enabled/x/y，可选 yaw。在线未知 yaw 用 known 掩码，不补造。

| 数组 | 形状 | 内容 |
| --- | --- | --- |
| stones | N×16×14 | 当前 x/y/enabled/own/shooter；五位目标类型；目标 x/y/radius；required |
| yaw | N×16×3 | 初始 sin(yaw)/cos(yaw)/known |
| tactic | N×42 | 原 PPO 41 战术，加 achieved_goal |
| context | N×2 | 当前出手编号/15、出手方编号奇偶 |
| actions | N×3 | 标签 v/6、h/2.23、w/15.7 |
| shots | N×3 | 原单位参数 |
| split | N | 0 训练、1 验证、2 测试 |
| record_id/sample_id/group_id | N | Unicode 溯源编号 |

x/y 以按钮中心平移，分别除以 2.375/10.525；目标 radius 除以 2.375。
目标类型为 ANY/IN_REGION/OUT_OF_PLAY/OUT_OF_HOUSE/SURVIVE；非坐标目标的坐标列填零，用类型掩码区分。
网络当前状态列不含终点、碰撞事件或摩擦种子；目标列只含请求希望达到的条件。

样本视图覆盖出手壶、被撞壶、组合终态、完整相关壶面、存活要求。
具名双飞标签需观察到：两枚原营内敌壶离营、单一首碰属于目标对、目标对碰撞成立。
离营与出界分开；无足够战术证据时使用 achieved_goal。采到双壶局面不等于采到成功双飞，也不等于旧 PPO 全合同验收。
多随机种子记录为独立结果；单次达成标签不冒充多种子稳健性认证。

所有候选、种子和派生目标按原始 group_id 作稳定 80/10/10 分组，不能再次按样本行随机切分。

重新编码原始分片，不运行物理：

```powershell
& 'D:/anaconda3/python.exe' -m training_research.inverse_dataset.cli encode `
  --raw-dir training_research/runs/inverse_dataset_batch1 `
  --output training_research/runs/inverse_dataset_batch1_reencoded
```

```python
import numpy as np
with np.load('000000.npz', allow_pickle=False) as batch:
    selected = batch['split'] == 0
    inputs = batch['stones'][selected]
    labels = batch['actions'][selected]
```

## 验证

### 扩大壶面与战术覆盖

`plan` 将手工设计的任务结构程序化，支持 12 类：进营、前四尺区、中央守壶、边守壶、营内清壶、
打定、打甩、清守壶、双飞、贴壶位置、借壶清壶、绕守壶进营。
每个基础壶面随机选择目标坐标、容许半径、投壶槽位、角度 yaw、间距、侧向偏移和 1–8 枚背景壶；
同一基础壶面的轻微平移变体使用相同 group_id，全部重新模拟，不复用平移前的结果。
精确相同壶面关联的数据分组会整体合并，防止跨分组泄漏。
贴壶在本数据合同中表示出手壶停在目标前方指定小区域，同时目标移动不超过 0.10 m；
这里只覆盖明确的几何终态条件，不宣称完成旧 PPO 的全部战术合同。

```powershell
& 'D:/anaconda3/python.exe' -m training_research.inverse_dataset.cli plan `
  --output training_research/runs/expanded_catalog_batch2.json `
  --layouts-per-family 100 --variants-per-layout 2 --max-background 8 --seed 20261005

& 'C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python39_64/python.exe' `
  -m training_research.inverse_dataset.cli collect `
  --output training_research/runs/expanded_batch2 --scenes 0 `
  --scene-json training_research/runs/expanded_catalog_batch2.json `
  --sampling uniform --shots-per-scene 48 --physics-seeds 3 `
  --workers 4 --scenes-per-shard 4

& 'D:/anaconda3/python.exe' -m training_research.inverse_dataset.cli select `
  --raw-dir training_research/runs/expanded_batch2 `
  --output training_research/runs/expanded_selected_batch2 --min-seeds 3 --min-success-rate 1

& 'D:/anaconda3/python.exe' -m training_research.inverse_dataset.cli audit `
  --dataset-dir training_research/runs/expanded_selected_batch2
```

上述规模为 2,400 壶面任务、115,200 组候选参数、345,600 次推演。
完成数量以 manifest 为准；候选不能算成功样本。中断后同参数加 `collect --resume` 续采，
续采要求实现/运行库和场景配置哈希一致。程序不自动启动后续批次。
JSON 的 family 会保留，用于统计每类任务。
同一壶面指定不同目标时任务不会被去重丢弃，记录编号使用 task_key；scene_key 仍单独标识物理初始场景。

采集数据保存全部合法已实现终态的几何目标视图，可用于通用逆向目标学习。
筛选数据另存仅满足明确战术条件的样本。两套数据含重叠记录，不能直接当作独立样本计数相加。
`audit` 核查原始数据/数组哈希，逐条重新构造输入、动作和元数据，比较 float32 数组的原始字节，
同时统计独立壶面、相邻壶面组、各战术成功记录、三种子全成功参数、训练/验证/测试覆盖。
没有成功样本的任务会在 `families_without_task_success` 中明确列出，不能凭任务目录存在宣称已覆盖。

生成器的参数范围是采样提案，不是物理机制或可达性结论；难任务需根据采样实际成功率追加覆盖。
12 类任务仍未覆盖全部 41 个 PPO 战术，模型准确性还需在独立壶面和新摩擦种子上验证。

### 固定手工壶面，连续采样，再筛选

`fixtures/manual_boards.json` 提供四个明确任务：进营、单壶打出界、双飞两壶出界、打定。
手工定义的是初始壶面和目标条件；成功与否由加速模拟器的真实终态决定。
双飞案例借用本地历史采样中两只目标壶的坐标，省略其他壶，重新模拟验收。

```powershell
& 'C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python39_64/python.exe' `
  -m training_research.inverse_dataset.cli collect `
  --output training_research/runs/manual_scan_batch1 --scenes 0 `
  --scene-json training_research/inverse_dataset/fixtures/manual_boards.json `
  --sampling uniform --shots-per-scene 1000 --physics-seeds 3 `
  --workers 2 --scenes-per-shard 1

& 'D:/anaconda3/python.exe' -m training_research.inverse_dataset.cli select `
  --raw-dir training_research/runs/manual_scan_batch1 `
  --output training_research/runs/manual_selected_batch1 `
  --min-seeds 3 --min-success-rate 1
```

每个壶面固定不变，`uniform` 独立连续抽取 `(v,h,w)`，按壶面内 `shot_bounds` 指定范围，抽样可复现。
未指定范围时使用全局 v-min/v-max 及 h∈[-2.23,2.23]、w∈[-15.7,15.7]。
`shot_bounds` 只作用于 uniform；mixed 与 grid 保持原行为。
若要按步长遍历则用 `--sampling grid --v-grid ... --h-grid=... --w-grid=...`。
这些范围是覆盖候选参数的提案，不表示已知这些参数会成功。

每个壶面可带 `selection`：

```json
{
  "tactic": "double_hit",
  "goal": {"stones": {"6": {"type": "OUT_OF_PLAY"}, "10": {"type": "OUT_OF_PLAY"}}},
  "first_contact_any": [6, 10],
  "require_single_first_contact": true,
  "required_collision_pairs": [[6, 10]]
}
```

筛选检查所有指定目标，包括 required=false 的软目标；未指定的壶不限制。
可指定 `require_no_contact`，或约束首碰目标及必须观察到的碰撞对。
双飞必须指定两枚敌方目标、单一首碰、两目标之间的碰撞，以及两目标离营或出界。
模拟错误、未停稳、规则违规均不能成为成功样本。
`min-seeds` 表示最低成功种子数；`min-success-rate` 的分母包含全部该参数的试验，包括失败和错误。
同一参数重复种子会报错，不能充当独立试验。有限种子达标只说明这些种子上的结果。

筛选输出：

- `selected_shots.jsonl`：达标参数、达标率、成功种子及来源记录编号。
- `shards/*.raw.jsonl`：被选中的实际推演记录，完整保留终态与碰撞证据。
- `shards/*.npz` 和 `*.samples.jsonl`：默认每条记录一个训练样本，输入目标使用手工定义的任务条件，输出是实际出手参数。
- `manifest.json`：统计、失败原因、源数据与筛选实现的哈希。

原始采集目录保留全部候选。用 `select --goal-json 新条件.json` 可以对已有结果重新筛选，无需重新运行物理；
该文件使用上述 selection 格式，覆盖所有源壶面的条件，因此应选择相应的源分片。
同一壶面的所有参数和种子使用同一 group_id，避免训练/验证之间泄漏。
大量训练时还需扩展不同壶面、间距、角度和遮挡；四个固定壶面用于验证采样筛选流程。

2026-10-04 试跑：`runs/inverse_manual_boards_20261004`，每局面 128 组连续参数，每组 3 种子，
共 512 组参数 / 1,536 次完整推演，无错误或规则违规。
`runs/inverse_manual_selected_20261004` 仅保留三种子全部成功的参数：
进营 22 组、单壶出界 128 组、双飞两壶出界 8 组、打定 36 组；合计 194 组 / 582 条指定目标训练样本。
`validation.json` 记录全部样本的编码逐位重建、目标及碰撞条件复核、源数据哈希未改变。
四个壶面的稳定分组恰好均属于 train；这批用于验证流程，不能据此评估模型泛化。

```powershell
& 'C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python39_64/python.exe' `
  -m unittest training_research.tests.test_inverse_dataset training_research.tests.test_inverse_dataset_selection training_research.tests.test_inverse_dataset_task_boards training_research.tests.test_inverse_dataset_physx -v
```

覆盖目标身份/掩码、离营与出界、双飞证据、违规/未完成过滤、采样复现、无终态泄漏、分组一致。
原生测试将被动观察路径与原预测入口对照，比较全部 16 壶状态、随机消费、时钟和首碰的完整序列化结果。
