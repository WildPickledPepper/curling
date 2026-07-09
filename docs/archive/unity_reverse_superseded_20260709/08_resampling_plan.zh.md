# 重采样计划

本轮重采样的目的不是重新拟合 Unity 公式，而是获取能验证剩余未知项的硬证据：

> 2026-07-08 当前状态：unique-target 与 unique-role 两组关键样本已经采到。
> 后续先不再主动拉起 Unity 采样，优先用已有样本继续逆向 convex cooking、contact
> manifold、rotation/yaw 与 RNG 摩擦序列。managed material timing 已在 2026-07-09
> 通过离线小网格弱化为非主因。

```text
1. AutoDCP .save：BESTSHOT + RANDSEED + SWEEP + TRACE
2. socket JSONL：BESTSHOT -> MOTIONINFO -> POSITION
3. sweep window：不同 SWEEP distance 的开始/结束帧影响
4. repeat shots：同一动作重复多次，用来区分随机摩擦和公式偏差
5. 少量边界/碰撞样本：验证 clamp、出界、碰撞路径是否触发预期分支
```

## 先开记录归档

在让 Unity 页面开始比赛前，先启动 record watcher：

```powershell
D:\anaconda3\python.exe tools\calibration\collect_autodcp_records.py `
  --archive-dir data/calibration/autodcp_records_20260707 `
  --jsonl data/calibration/autodcp_records_20260707.jsonl `
  --poll-seconds 1
```

它会扫描工程目录和单机版目录下常见的 `Records/`、`Records/4Games/`、`Records/8Games/`
与 `AutoGame/` 输出目录，发现含 shot section 与 `BESTSHOT/RANDSEED/TRACE`
等字段的文件就复制到：

```text
data/calibration/autodcp_records_20260707/
```

同时解析成：

```text
data/calibration/autodcp_records_20260707.jsonl
```

如果 Unity 先写临时文件再重命名，watcher 可能会遇到一次 parse failed；这不致命，下一轮轮询会再抓。

## 推荐：开可控场景 socket 采样

这轮如果要“一壶一清场”、同时覆盖碰撞和擦冰，优先用新的可控场景采样器：

```powershell
D:\anaconda3\python.exe tools\calibration\build_controlled_sampling_plan.py `
  --output config\unity_controlled_sampling_plan_20260707.json
```

当前计划共 98 条，覆盖：

```text
repeat                  同一动作重复，检查 Unity 随机摩擦/回放散布
no_collision            清场单壶，校准 BESTSHOT -> MOTIONINFO -> POSITION
sweep_window            sweep=0/1/2/4/6/8/10/12，验证扫冰窗口和 socket 延迟
collision_headon        直线正碰
collision_glancing      斜碰/擦碰
collision_double        双目标连锁碰撞
collision_with_sweep    扫冰与碰撞叠加
boundary                高速、出界、输入 clamp、墙边界
```

启动命令：

```powershell
D:\anaconda3\python.exe tools\calibration\controlled_scene_sampler.py `
  --key localtest `
  -H 127.0.0.1 `
  -p 7788 `
  --plan-file config\unity_controlled_sampling_plan_20260707.json `
  --output-file data/calibration/unity_controlled_samples_20260707.jsonl `
  --use-reset `
  --collision-tolerance 0.02
```

这个工具会连接两个玩家，并自动使用 `localtest:0` debug key。每次收到 `GO` 后：

```text
1. RESETPOSITION：清场，必要时摆目标壶；
2. RESETSTATE：把当前可投壶固定成 Player1/Player2 对应的调试壶；
3. BESTSHOT：发送计划中的 v0/h0/w0；
4. MOTIONINFO：记录中线状态，必要时发送 SWEEP；
5. POSITION：记录最终全场 16 壶位置、目标壶位移、是否发生碰撞。
```

这比旧的自然对局采样更适合验证剩余物理未知项，因为每条样本都有明确二维初始场面。
但 2026-07-08 的碰撞对齐报告显示：连续跑同一个 Unity 页面时，目标壶二维位置会被清零，
但 rotation/contact history 等隐藏状态未必被重置。因此这套 98 条计划适合找问题，
不再作为最终碰撞 2cm 验收金标准。

## 碰撞金标准：fresh page 一发一采

不扫冰碰撞要重新采样时，用一发一个 plan 文件。生成命令：

```powershell
python tools\calibration\build_fresh_collision_plans.py --repeats 3
```

输出：

```text
config/unity_fresh_collision_manifest_20260708.json
config/unity_fresh_collision_plans_20260708/*.json
```

当前默认生成 36 个 one-shot plan：`collision_headon` 和 `collision_glancing`
各保留原目标位置/速度组合，每个重复 3 次。每个 plan 只含一发，跑法是：

```powershell
python tools\calibration\controlled_scene_sampler.py `
  --key localtest `
  -H 127.0.0.1 `
  -p 7788 `
  --plan-file config\unity_fresh_collision_plans_20260708\000_collision_headon_y5p2_v3p4_r00.json `
  --output-file data/calibration/unity_fresh_collision_samples_20260708.jsonl `
  --use-reset `
  --collision-tolerance 0.02
```

每跑完一个 one-shot plan 后，刷新或重开 Unity 页面，再跑 manifest 里的下一个 plan。
这一步的目的不是方便，而是强制目标壶回到 prefab 初始姿态，避免样本 78/80/82/83
那种“二维位置干净但隐藏状态污染”的情况。采样完成后先对 fresh 样本重新跑 PhysX baseline probe：

```powershell
D:\esp\tmp\curling_pyphysx_conda\python.exe tools\reverse\probe_physx_collision_alignment.py `
  --samples data\calibration\unity_fresh_collision_samples_20260708.jsonl `
  --output data\calibration\unity_physx_collision_probe_fresh_collision_dt0010.json `
  --combine-mode multiply `
  --use-unity-frame `
  --dt 0.01
```

然后做隐藏状态复用检查：

```powershell
python tools\reverse\analyze_collision_sample_carryover.py `
  --samples data\calibration\unity_fresh_collision_samples_20260708.jsonl `
  --baseline-probe data\calibration\unity_physx_collision_probe_fresh_collision_dt0010.json `
  --scan-probe data\calibration\unity_physx_collision_probe_fresh_collision_dt0010.json `
  --output data\calibration\unity_fresh_collision_state_report_20260708.json
```

## 省力碰撞验证：同页唯一目标壶 batch

如果一发一刷新太慢，可以先跑唯一目标壶 batch。生成命令：

```powershell
python tools\calibration\build_fresh_collision_plans.py --mode unique-target-batch --repeats 3
```

输出：

```text
config/unity_unique_target_collision_batch_manifest_20260708.json
config/unity_unique_target_collision_batches_20260708/collision_unique_targets_batch_r00.json
config/unity_unique_target_collision_batches_20260708/collision_unique_targets_batch_r01.json
config/unity_unique_target_collision_batches_20260708/collision_unique_targets_batch_r02.json
```

每个 batch 文件含 12 个 no-sweep collision case，并显式把目标壶分配为
`2..13`，同一页内不复用目标壶。跑法：

```powershell
python tools\calibration\controlled_scene_sampler.py `
  --key localtest `
  -H 127.0.0.1 `
  -p 7788 `
  --plan-file config\unity_unique_target_collision_batches_20260708\collision_unique_targets_batch_r00.json `
  --output-file data/calibration/unity_unique_target_collision_samples_20260708.jsonl `
  --use-reset `
  --collision-tolerance 0.02
```

跑完一个 batch 文件后刷新或重开 Unity 页面，再跑下一个 batch 文件。这个方案不能完全替代
fresh one-shot，因为 active 壶 0/1 仍会复用；但它能优先验证“target hidden state
复用是主误差源”这个假设，人工刷新次数从 36 次降到 3 次。

`controlled_scene_sampler.py` 会把计划里的额外字段保存在输出 JSONL 的
`plan_metadata` 里，例如 `source_sample_id`、`batch_repeat_index`、
`assigned_target_index`。后续做 probe/报告时优先用这些字段对应旧样本和 batch。

unique-target batch 采完后固定跑三步验收：

```powershell
D:\esp\tmp\curling_pyphysx_conda\python.exe tools\reverse\probe_physx_collision_alignment.py `
  --samples data\calibration\unity_unique_target_collision_samples_20260708.jsonl `
  --output data\calibration\unity_physx_collision_probe_unique_target_dt0010.json `
  --combine-mode multiply `
  --use-unity-frame `
  --dt 0.01
```

```powershell
python tools\reverse\summarize_collision_alignment.py `
  --samples data\calibration\unity_unique_target_collision_samples_20260708.jsonl `
  --probe data\calibration\unity_physx_collision_probe_unique_target_dt0010.json `
  --output data\calibration\unity_collision_alignment_summary_unique_target_20260708.json
```

```powershell
python tools\reverse\analyze_collision_sample_carryover.py `
  --samples data\calibration\unity_unique_target_collision_samples_20260708.jsonl `
  --baseline-probe data\calibration\unity_physx_collision_probe_unique_target_dt0010.json `
  --scan-probe data\calibration\unity_physx_collision_probe_unique_target_dt0010.json `
  --output data\calibration\unity_collision_state_carryover_unique_target_20260708.json
```

第一份 probe 是原始仿真对齐结果；第二份 summary 直接给出 `full_in_play_pass_count`、
`failed_in_play_sample_ids` 和 `all_in_play_targets_within_threshold`；第三份 carryover
检查 `same_session_target_reuse_detected` 是否已经降为 false。

## 备选：旧 38 条 socket 采样

使用本轮核心计划：

```text
config/unity_resampling_plan_20260707.json
```

计划里有 38 条 shot，覆盖：

```text
repeat_seed_probe_*       同一 shot 重复，检查随机摩擦差异
sweep_window_*            sweep=0/1/2/4/6/8/10/12 阶梯
geometry_*                无扫冰几何基准
moderate/heavy_sweep_*    中高扫冰
boundary_*                边界、速度、clamp 分支
```

旧方案启动两个 socket 采样客户端：

```powershell
D:\anaconda3\python.exe tools\calibration\unity_sampling_supervisor.py `
  --key localtest `
  -H 127.0.0.1 `
  -p 7788 `
  --plan-file config\unity_resampling_plan_20260707.json `
  --output data/calibration/unity_resample_20260707_{player}.jsonl `
  --max-samples-per-client 19 `
  --target-total-samples 38 `
  --log-dir log/unity_resampling_20260707
```

如果想把计划跑两遍，把 `--max-samples-per-client` 改成 `38`，`--target-total-samples`
改成 `76`。

## 你需要操作页面的部分

等上面两个命令都已经运行后，再在 Unity 页面点：

```text
准备 / Ready
开始 / Start
```

如果页面弹出玩家名、确认、继续之类按钮，只点让比赛继续进入正式投壶的按钮。不要中途手动发 shot；
shot 会由两个 socket 采样客户端发。

## 采样结束后的验收

采样完成后至少应出现：

```text
data/calibration/unity_controlled_samples_20260707.jsonl
data/calibration/unity_resample_20260707_Player1.jsonl
data/calibration/unity_resample_20260707_Player2.jsonl
data/calibration/autodcp_records_20260707.jsonl
data/calibration/autodcp_records_20260707/*.save 或同类归档文件
```

如果使用推荐的可控场景采样器，`unity_resample_20260707_Player*.jsonl` 可以没有；
它们只属于旧 38 条 socket 采样。

验收重点：

```text
1. controlled JSONL 是否每条都有 motioninfo、final_xy、after_position；
2. collision 样本的 target_moves/max_target_move 是否记录到目标壶位移；
3. sweep 样本是否覆盖 0/1/2/4/6/8/10/12；
4. .save JSONL 是否每条都有 bestshot_* 和 randseed；
5. TRACE 是否至少有若干帧，可用于逐帧对齐；
6. repeat 样本的相同 shot 是否出现合理的随机散布。
```

如果 `.save` 没有出现，说明当前打开的不是会写 AutoDCP record 的场景，或者 record 目录在未覆盖的路径。
这时先不要继续大量采样，应该回头定位 Unity 实际写文件目录，再用 `--watch-root`
把该目录显式加入 watcher。
