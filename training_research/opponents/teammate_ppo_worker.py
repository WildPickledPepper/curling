"""给严格 PhysX 父进程调用的队友 PPO JSON-lines 推理子进程。"""

from __future__ import annotations

import contextlib
import io
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from training_research.opponents.teammate_ppo_adapter import TeammatePPOOpponent


def main() -> int:
    bot = TeammatePPOOpponent(deterministic=True)
    for line in sys.stdin:
        try:
            request = json.loads(line)
            if request.get("close"):
                return 0
            with contextlib.redirect_stdout(io.StringIO()):
                decision = bot.choose(
                    request["position"],
                    player_is_init=bool(request["player_is_init"]),
                    shot_num=int(request["shot_num"]),
                    end_score=int(request.get("end_score", 0)),
                    total_ends=int(request.get("total_ends", 1)),
                    current_player=int(request.get("current_player", 0)),
                )
            response = {
                "ok": True, "bestshot": list(decision.bestshot), "tactic": decision.tactic,
                "action_id": decision.action_id, "policy_probability": decision.policy_probability,
                "value": decision.value, "fallback": decision.fallback,
            }
        except Exception as exc:
            response = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
        print(json.dumps(response, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
