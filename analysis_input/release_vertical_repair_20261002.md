# 释放滑行竖直速度修复与新状态边界（2026-10-02）

此处第 526 帧边界是历史记录，已由 [BVH34 修复](release_bvh34_repair_20261002.md) 消除；最新连续状态比较已通过第 1561 帧。

已按原始 `f60124 FixedUpdate` 的实际指令，把生产场景默认 `custom_sliding_zero_vertical_setter` 改为 `True`。每帧滑行构造线速度时向竖直分量写入正零，然后交给同一个 PhysX 场景；不再沿用上一帧重力产生的竖直速度。现有审计路径、训练循环和原生循环参数均读取这个场景配置。

实现依据和修复前记录见 [第二帧分叉检查](first_release_chain_alignment_20261002.md)：`f60124` 正文 byte offset=837 明确执行 `i32.const 0; i32.store offset=124`，随后经 `f32521 → f82501 → f73034` 写入线速度。修复没有修改滑行公式、摩擦输入或二进制内核。

## 串行状态比较结果

同一新建生产场景，样本 11000，`Reset → BESTSHOT 3.4 0 0`，不注入任何 Unity 释放 P/Q、速度或滑行结果。使用与 Unity 同一组记录的摩擦输入，按顺序比较：

`Reset 42 步/自然休眠 → 释放 P/Q、线速度与角速度 → 第1帧 → …… → 第525帧物理推进后状态`

这段连续的已采样状态边界逐位通过。释放后的 525 帧，每帧 Pxyz/Qxyzw/线速度xyz/角速度xyz 共 13 个原始浮点字，累计 **6,825 个字全部一致**。第二帧线速度 setter 的竖直输入已由 `0xbdc8e8a7` 修正为 Unity 的 `0x00000000`，该分叉消失。释放与前 3 帧的实际两个 setter 入口/出口也逐位相同；前 3 帧另外有 solverSetupSolve.exit 对齐证据。

后续长序列的物理推进输出由下一帧 getter 入口采到的原始速度位值与 bridge 位姿确定。getter 在新的 setter 之前读取，因此不会混入下一帧速度写入。多次 getter 对同一 ordinal 返回的原始位值也一致。该验证针对连续状态边界，不等同于所有 f64 算术中间值逐指令对照，也不证明摩擦 RNG 的内部状态生成已闭合。

## 新的首个已采样差异

**第 526 帧物理推进后的角速度 X**（密集 ordinal=527）：

- 帧入口 13 个状态字与 Unity 一致。
- 该帧角速度 setter 的 3 个实际写入字与 Unity 一致。
- 推进后的状态只差角速度 X 一个字：Unity `0x9a381bc6`，Native `0x9a381bc5`，相邻 1 ULP。
- 其余 12 个状态字相同。

这把此前第二帧的分叉后移到了第 526 帧的物理/fetch/位姿写回输出区间。当前 Unity 定点 solver 内部窗口只覆盖前几帧，因此**尚未定位第 526 帧的具体内部指令**。下一步应将 Unity solver/积分/写回采样窗口移到 ordinal=527，和 Native 同帧实际输入与中间结果逐位比较，不根据这一位差异猜测机制。

## 验证、版本和范围

- 31 项 unittest 测试通过，包括新增的真实 Unity 释放及前四帧状态 fixture；第二帧非零重力输入必须被脚本清零才能通过。
- 修复后的 Native 前四帧开启/关闭内部 trace 时，所有 setter 与输出一致。长序列的前四帧与上述基线一致。
- 原有 Reset 完整复查仍通过：42 个 solver 出口 546 个字、自然休眠、释放 P/Q。
- 复用的 Unity 被动观察器已经验证：256 个 Reset 状态帧、1,562 次摩擦输入及终局物理字段与原始基线一致。
- Unity wasm SHA256：`cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81`。
- Native CP39 SHA256：`7c31ced1773023e552391645e42040c9f3694d513805bc8b95ef0f8bc737bd38`。
- 结果限于本次样本、默认配置、Windows CP39 和相同摩擦输入。未推广到其他出手、ABI 或后续碰撞全轨迹。

复查：`python analysis_input/verify_release_vertical_repair_20261002.py`。逐项原始字、当前源码哈希和全部采样证据哈希见 [修复结果](release_vertical_repair_verified_20261002.json)。长序列原始记录见 [本地完整采样](native_first_release_vertical_fixed_full_20261002.json)，Unity 记录沿用 [实际运行采样](unity_first_release_chain_complete_capture_20261002/logs/unity_runtime_probe_20261002_162622/events.jsonl)。
