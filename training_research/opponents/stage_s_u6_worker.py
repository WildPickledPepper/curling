"""JSON-lines worker for the supplied Stage-S U6 PPO in the Torch environment.

This is intentionally tiny: the parent process owns strict PhysX; this worker
only runs the teammate-supplied PyTorch inference stack.  It keeps stdout
machine-readable so the CPython 3.13 simulator can call it once per turn.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from training_research.opponents.stage_s_u6_adapter import StageSU6Opponent


def decision_json(decision) -> dict:
    return {
        "ok": True,
        "bestshot": list(decision.bestshot),
        "tactic": decision.tactic,
        "action_id": decision.action_id,
        "policy_probability": decision.policy_probability,
        "value": decision.value,
        "fallback": decision.fallback,
        "legal_tactics": list(decision.legal_tactics),
        "stage_s_p1_peel_guard": decision.stage_s_p1_peel_guard,
        "stage_s_p2_blocked_draw": decision.stage_s_p2_blocked_draw,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True, type=Path)
    parser.add_argument("--deterministic", action="store_true")
    parser.add_argument("--stochastic", action="store_true")
    args = parser.parse_args()
    deterministic = bool(args.deterministic and not args.stochastic)
    # force_local prevents recursively launching another worker.
    bot = StageSU6Opponent(args.checkpoint, deterministic=deterministic, force_local=True)
    for line in sys.stdin:
        try:
            request = json.loads(line)
            if request.get("close"):
                return 0
            # The archive's get_bestshot prints diagnostics.  Hide those so
            # every stdout line remains a single parent-readable JSON object.
            with contextlib.redirect_stdout(io.StringIO()):
                decision = bot.choose(
                    request["position"],
                    player_is_init=bool(request["player_is_init"]),
                    shot_num=int(request["shot_num"]),
                    end_score=int(request.get("end_score", 0)),
                    total_ends=int(request.get("total_ends", 1)),
                    current_player=int(request.get("current_player", 0)),
                )
            response = decision_json(decision)
        except Exception as exc:  # Parent reports the real message and stops safely.
            response = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
        print(json.dumps(response, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
