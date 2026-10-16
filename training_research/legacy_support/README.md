# 求解器的数学提案依赖

这些文件从旧交接目录原样复制，供当前出手求解器生成自由轨迹和接触几何候选。
`manifest.json` 记录原目录、相对路径及逐文件 SHA-256；本次没有改写其中算法。

当前物理推进仍使用仓库主目录的 `local_simulator/`；这里不含旧 PhysX 实现、PPO 权重或 Unity 逆向采样。原路径布局保留，是因为旧代码通过相对路径加载标定数据。日常修改求解逻辑请从 `training_research/shot_solver.py`、`inverse_initials.py`、`inverse_goal_search.py` 开始。
