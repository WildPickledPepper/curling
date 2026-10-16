# 本地完整物理模拟器

应用入口与安装步骤见 [队友上手指南](../docs/TEAM_GUIDE.md)。目前使用场景是：给定静止起始壶面和 `BESTSHOT(v,h,w)`，推演完整终态，包含活动壶和其他壶的落点、失活、碰撞、随机消费与调度摘要；当前应用不扫冰。

## 安装与自检

推荐 Windows x64 / CPython 3.9，在仓库根目录执行：

```powershell
python -m pip install -r requirements-app.txt
python local_simulator/runtime/verify_native_runtime.py
```

CPython ABI 必须匹配随包 `.pyd`。Windows 随包包含 3.8、3.9、3.13；当前加速与求解成绩实际使用的是 Windows CP39。CP38 的历史环境依赖另见 `runtime/requirements-physx.txt`，不要把 CP38 的 wheel 安装到 CP39。Linux 加载器保留兼容分支，但当前 Git 交付未包含对应 `.so`，不能承诺克隆后在 Linux 直接运行。

## 在代码中使用

```python
from local_simulator.runtime_loader import install_bundled_pyphysx
install_bundled_pyphysx()
from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd

env = StrictCurlingEnd(seed=20261004)   # 长期复用实例
positions = [0.0] * 32                 # 16 个原始 slot，x/y 交替
positions[4:6] = [2.375, 5.2]         # 已有壶 index=2
before = env.scene.reset_positions(positions, yaw_overrides={i: 0.0 for i in range(16)})
env.shot_number = 3                   # 本次新壶 index=3
result = env.play((3.4, 0.0, 0.0))
assert result["settled"]
print(result["states"], result["contact"])
```

真实连续对局要保留旧壶 slot 和 yaw；本次新壶使用自己的投壶编号。每个实例串行使用。球场按钮中心坐标为 `(2.375, 4.88)` 米，战术库以按钮为原点的 `x_m/y_m` 不能直接混入这里。

反推出手请直接使用 [BudgetedShotSolver](../training_research/SOLVER_GUIDE.md)，该入口负责完整场景重置、规则和碰撞验收，不必自己拼接搜索回调。

## 默认运行路径

`training_fast=True` 使用已验证的精简分派和可用的原生辅助模块，同时保留完整物理推进和停止/碰撞规则。Windows CP39 随包加载随机、步进和受保护的内核优化资产。未知 ABI/内核按加载器的保护条件保留支持的基线路径；缺少必要 PhysX 扩展会报错。

完整请求实测随机器负载、CPU 核型和频率变化。历史较平稳的大核测量约 54–89 ms/手，属于当次五类正向场景；不能和包含多次模拟的反求耗时混为一谈，也不是跨机器承诺。`prediction_native_scene_steps` 仍默认关闭。

相同完整起始状态、逐次随机输入和真实调度是条件逐位对齐的前提。已有采样验证不构成未知输入下的全覆盖证明。逆向过程及大采样不属于本次应用交付的新增内容。

## 目录与验证

- `runtime_loader.py`、`runtime/pyphysx/`：按 ABI 加载随包扩展。
- `unity_physx.py`、`unity_prediction.py`：持久场景、调度与完整预测。
- `runtime_support/`、`assets/`：运行必需的公式辅助和几何资产。
- `native_*.py`、`runtime/*.dll`、`runtime/*.json`：加速所需的随包模块与保护清单。
- `examples/`、`tests/`：应用演示及本地小夹具回归。

在受支持的 Windows CP39 环境中运行：

```powershell
python -m unittest discover -s local_simulator/tests -p "test_*.py"
```

物理改动应遵循 [项目协作规则](../AGENTS.md)；应用维护不根据终点误差反推或补偿内部机制。
