# CP39 优化 `.pyd` 本地启用备份清单

- 启用日期：2026-07-25
- 候选来源：`D:\esp\tmp\curling_pyphysx_hybrid\build-cp39-optimized-20260722\lib\_pyphysx.cp39-win_amd64.pyd`
- 启用后 SHA-256：`2564ABEC4FA3F358E67259B105C4B88D49EAE28510611C8A0E2F11B7671888DF`
- 启用后大小：`5,107,712` 字节
- 启用目标：
  - `D:\Desktop\冰壶\DCCourse\local_simulator\runtime\pyphysx\_pyphysx.cp39-win_amd64.pyd`
  - `D:\Desktop\冰壶\DCCourse\ppo_stagec_physx_teammate_training_cp38_20260724\local_simulator\runtime\pyphysx\_pyphysx.cp39-win_amd64.pyd`

替换前文件的 SHA-256 均为 `D312EB021FDE9D5D4A8F0AAB84CBB35D54D6670C1749A0DD7A64E94F416662A3`，大小均为 `5,080,576` 字节：

- `main__pyphysx.cp39-win_amd64.pre_optimized_D312EB02.pyd`：主项目原件。
- `teammate__pyphysx.cp39-win_amd64.pre_optimized_D312EB02.pyd`：队友包原件。
- `teammate_server__pyphysx.cp39-win_amd64.pre_optimized_D312EB02.pyd`：队友 CP39 服务包原件。

回退时，仅将对应备份文件复制回同名目标，再核对 SHA-256 是否恢复为上面的 `D312...62A3`。不影响 Linux `.so`、课程平台包、对战平台或历史发布归档。

本地启用依据：`planning_proxy/runs/pyd_only_{tail,narrow,multistone,midspin,k5success,reverse_highspin}_{current,candidate,compare}_20260725.json`。这些报告仅证明已测物理输入的等价和速度，不代表整局胜率。

2026-07-25 已统一启用至所有当前 Windows CP39 运行时副本：主项目、队友训练包、队友 CP39 服务包。三份启用后文件均为本清单开头的优化哈希。
