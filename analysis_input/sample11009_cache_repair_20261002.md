# 第 1383 步缓存分叉已修复

新样例 11009 的出手状态与第 1–3000 个完成物理步，两只冰壶的 P/Q/v/w 共 78,000 个状态字全部逐位一致。修复前仅第 1383 步的七个字不同，现在已消除；在已采样的完成状态中没有发现下一处分叉。结论限于这些样例和采样窗口，不代表所有未采样内部计算或所有局面都已对齐。

## 修改依据与实现

[修复前内部定位](sample11009_step1383_internals_20261002.md)通过 Frida 实测和原始 Unity 函数重放证明：本地 C19/C20 清空函数 `0x330f0` 把目标冰面的 304 字节缓存清成 0，而 Unity `f70030` 保留它，并调用 `f69978` 更新旧接触点。两者走了不同分支，随后 separation、法向修正项和目标静态求解输出分歧。

生产修改在 `local_simulator/unity_physx.py`：将 `enable_unity_pcm_multi_cache_lifecycle` 默认设为 False，停用这段每次窄相入口强行清空 multi-cache 的历史逻辑。这个开关保留用于显式历史诊断。

缓存失效继续走现有真实姿态写回：`f73070 → f72606(autowake=0) → f71596 → f71729` 的对应原生路径。睡眠目标此前没有姿态写回，缓存得以保留；开始参与求解后，原有写回流程正常更新交互。没有更改接触间距、求解冲量、最终状态或原生二进制。

这次修改依据实际观察到的缓存输入、失效写入及调用分支，不以开关实验的终点改善推断机制。

## 修复后内部验证

第 1383 步再次以 Frida 只读采样：`0x330f0` 调用前后缓存大小都是 304，指针和全部已有 payload 未变。本地实际调用 `0x29cbe0`，与 Unity 的 `f69978` 更新分支对应。

逐位核对结果：

- 更新函数前后五个活动接触记录的 65 个有效字相同，变换矩阵的 15 个字和阈值相同。记录末尾未被函数读取的填充字不属于计算字段。
- 五个 PCM 输出接触点的法向、间距、位置共 35 个字相同。
- 目标冰面五轮静态求解：每轮 60 个法向约束字、40 个摩擦约束有效字，以及输入/输出 solver body 的线速度与角状态全部逐位一致。
- 修复后跟踪运行和正常回放的 3000 个完成状态完全相同，插桩没有改变轨迹。

## 回归验证

新样例 11009：出手 26 字、第 1–3000 步两壶全部状态字连续逐位一致。相比修复前，只有第 1383 步改变，并精确变成 Unity 对应值。

旧样例 11000：3362 个原生完成步与修复前完全相同；已捕获的第 1–2000 个 Unity 完成步两壶仍逐位一致。

新增 `test_unity_preserved_ice_cache.py` 使用独立 Unity 采样 fixture，自 Reset/出手正常推进，不注入状态。修复前在 `cachedSize: 0 != 304` 处失败；修复后校验缓存、五条法向约束及 1381–1386 步两壶状态通过。39 项完整测试全部通过。

```powershell
& 'C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python39_64/python.exe' -m unittest discover -s local_simulator/tests -p 'test_*.py'
python analysis_input/verify_sample11009_cache_repair_20261002.py
```

## 可复查证据

- [验证脚本](verify_sample11009_cache_repair_20261002.py)
- [机器报告及版本/证据 SHA256](sample11009_cache_repair_verified_20261002.json)
- 新样例真实回放：`native_sample11009_cache_fixed_3000_20261002.json`
- 修复后函数输入输出：`native_sample11009_step1383_cache_fixed_calls_20261002/calls.json`
- 旧样例真实回放：`native_sample11000_cache_fixed_3362_20261002.json`
- Unity 原始 Wasm SHA256：`cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81`
- 原生 CP39 模块 SHA256：`7c31ced1773023e552391645e42040c9f3694d513805bc8b95ef0f8bc737bd38`，本次未修改。

历史修复前报告保持原样，避免把先前未对齐结果混写成当前结果。
