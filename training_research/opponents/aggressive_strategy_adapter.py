"""将仓库根目录的 ``aggresive_ai.py`` 接成纯本地对局对手。

不改动原 Socket 机器人，也不复制它的战术优先级；本适配器仅绕开网络连接，
把本地 PhysX 的棋盘写入原类实例后直接调用 ``get_bestshot()``。因此本地评测
使用的正是交付脚本里的激进策略顺序和 strategy_library 参数。
"""

from __future__ import annotations

import contextlib
import io
import sys
import types
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ROBOT_PATH = PROJECT_ROOT / "aggresive_ai.py"
TACTICSLIB_ROOT = PROJECT_ROOT / "tacticslib"


@dataclass(frozen=True)
class AggressiveOpponentDecision:
    bestshot: Tuple[float, float, float]
    tactic: str
    command: str
    fallback: bool
    # 与 PPO 评测日志保持同一字段形状；激进规则策略没有策略网络概率/价值。
    action_id: int = -1
    policy_probability: float = 1.0
    value: float = 0.0


class AggressiveStrategyOpponent:
    """调用原 ``AggressiveRobot.get_bestshot`` 的无 Socket 对手。"""

    label = "aggressive"

    def __init__(self) -> None:
        if not ROBOT_PATH.is_file():
            raise FileNotFoundError(f"aggressive robot not found: {ROBOT_PATH}")
        if str(TACTICSLIB_ROOT) not in sys.path:
            sys.path.insert(0, str(TACTICSLIB_ROOT))
        # 原脚本在 Python 3.9 中会在函数内部的 ``str | None`` 注解处失败，
        # 但文件为只读，不能为了本地评测改队友交付物。以内存方式补 future
        # import 后执行，运行逻辑保持逐字相同。
        module = types.ModuleType("_local_aggressive_robot")
        module.__file__ = str(ROBOT_PATH)
        source = "from __future__ import annotations\n" + ROBOT_PATH.read_text(encoding="utf-8")
        exec(compile(source, str(ROBOT_PATH), "exec"), module.__dict__)
        # 原文件的相对路径写法会漏掉 tacticslib；本地评测显式补齐后强制启用。
        import strategy_library

        module.sl = strategy_library
        module._HAS_TACTICSLIB = True
        self._robot_class = module.AggressiveRobot

    @staticmethod
    def _parse(command: str) -> Tuple[float, float, float]:
        parts = command.split()
        if len(parts) != 4 or parts[0] != "BESTSHOT":
            raise ValueError(f"invalid aggressive BESTSHOT: {command!r}")
        return float(parts[1]), float(parts[2]), float(parts[3])

    def choose(
        self,
        position: Sequence[float],
        *,
        player_is_init: bool,
        shot_num: int,
        **_: object,
    ) -> AggressiveOpponentDecision:
        # 绕过 __init__，它唯一的副作用是建立 Socket；其余字段均在此完整赋值。
        robot = self._robot_class.__new__(self._robot_class)
        robot.show_msg = False
        robot.position = [float(value) for value in position[:32]]
        robot.position.extend([0.0] * (32 - len(robot.position)))
        robot.motioninfo = [0.0] * 5
        robot.round_num = 0
        robot.shot_num = int(shot_num)
        robot.round_total = 1
        robot.player_is_init = bool(player_is_init)
        robot.score = 0
        with contextlib.redirect_stdout(io.StringIO()):
            command = robot.get_bestshot()
        tactic = "aggressive_strategy_library"
        return AggressiveOpponentDecision(
            bestshot=self._parse(command), command=command, tactic=tactic,
            fallback=command == "BESTSHOT 3.0 0 0",
        )
