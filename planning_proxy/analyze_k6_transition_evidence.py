"""离线复盘 K6→对手 K6→K7 的状态转移证据。

这个工具不修改状态机，也不加载 PPO 的未来动作来给线上出手排序。它只读取已经
完成的完整对局记录，在同一真实 K6 入局上并列记录：

* 当前 K6 直接 outdraw 的三种子严格结果；
* 原 K6“清当前威胁并进入防御形”合同的无粗代理全局严格搜索；
* 有限的、对手无关的下一手反击筛查（它只能发现反例，不能证明安全）；
* 实际对局里对手 K6 和我方 K7 的后继状态。

它的目的，是防止把“某一手命中合同”“某次 K7 回退”或“某一条有限反击”单独
误读为整局胜负原因。输出 JSON 可作为状态机改动前后的固定回归证据。
"""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import replace
from pathlib import Path
from typing import Any

from evaluate_vs_teammate_ppo import (
    HOUSE_X,
    HOUSE_Y,
    ProxyMatchPlayer,
    canonical_board,
    make_position,
)
from first_player_strategy import plan_first_player_turn


CASES: tuple[tuple[str, str, int, bool], ...] = (
    ("ppo_failure_21027182", "current_budgettail_ppo_seed21027182.json", 21027182, True),
    ("ppo_failure_21457792", "benchmark_current_ppo_seed21457792.json", 21457792, True),
    ("aggressive_positive_21457791", "benchmark_current_aggressive_seed21457791.json", 21457791, False),
)


def _trace_row(game: dict[str, Any], shot: int) -> dict[str, Any]:
    return next(row for row in game["trace"] if int(row["shot"]) == int(shot))


def _live_board(states: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """按固定出手顺序恢复阵营标签，输出紧凑且可读的 K7 壶面。"""

    return [
        {
            "index": int(index),
            "owner": "self" if index % 2 == 0 else "opponent",
            "x": round(float(stone["x"]), 6),
            "y": round(float(stone["y"]), 6),
            "yaw": round(float(stone.get("yaw", 0.0)), 6),
        }
        for index, stone in enumerate(states)
        if bool(stone.get("enabled", True))
    ]


def _strict_summary(item: Any) -> dict[str, Any]:
    return {
        "action": [float(item.candidate.v0), float(item.candidate.h0), float(item.candidate.w0)],
        "goalMetByPhysicsSeed": [bool(value) for value in item.tactical_goal_met],
        "enemyClearedByPhysicsSeed": [int(value) for value in item.enemy_cleared],
        "ownClearedByPhysicsSeed": [int(value) for value in item.own_cleared],
        "activeFinalPositions": item.active_final_positions,
    }


def _run_case(
    report_path: Path,
    match_seed: int,
    *,
    run_strict_clear: bool,
    clear_deadline_seconds: float,
) -> dict[str, Any]:
    game = json.loads(report_path.read_text(encoding="utf-8"))["games"][0]
    k6 = _trace_row(game, 11)
    opponent_k6 = _trace_row(game, 12)
    k7 = _trace_row(game, 13)
    strict_board, proxy_board = canonical_board(k6["stateBefore"], 0)
    base_plan = plan_first_player_turn(proxy_board, 10)
    outdraw_plan = replace(
        base_plan,
        phase="sixth_outdraw_single_house_threat",
        target_points=((HOUSE_X, HOUSE_Y),),
        target_opponent_index=None,
        opponent_action="none",
        defence_shapes=(),
        landing_region_radius_m=0.22,
    )
    seeds = [int(match_seed) + 10 * 7919 + 104729 * offset for offset in range(3)]
    player = ProxyMatchPlayer(physics_seeds=3, parent_regions=3, decision_budget_seconds=105)
    result: dict[str, Any] = {
        "recordedFinalScoreFirst": game.get("finalScoreFirst"),
        "recordedWinner": game.get("winner"),
        "baseClearContract": base_plan.to_json(),
        "recordedK6": {
            "action": k6.get("bestshot"),
            "mode": k6.get("detail", {}).get("mode"),
            "decisionSeconds": k6.get("decisionSeconds"),
        },
        "recordedOpponentK6": {
            "action": opponent_k6.get("bestshot"),
            "activeAnchorAfter": (
                bool(opponent_k6["stateAfter"][10].get("enabled", True))
                if len(opponent_k6["stateAfter"]) > 10
                else None
            ),
        },
        "recordedK7": {
            "mode": k7.get("detail", {}).get("mode"),
            "action": k7.get("bestshot"),
            "decisionSeconds": k7.get("decisionSeconds"),
            "temporaryScoreFirst": k7.get("temporaryScoreFirst"),
            "stateBefore": _live_board(k7["stateBefore"]),
        },
    }

    draw_started = time.perf_counter()
    outdraw = player._try_fast_targeted_draw(
        strict_board=strict_board,
        proxy_board=proxy_board,
        position=make_position(strict_board),
        tactical_plan=outdraw_plan,
        shot_index=10,
        seeds=seeds,
        deadline=draw_started + 35.0,
    )
    if outdraw is None:
        result["strictOutdraw"] = {"found": False, "elapsedSeconds": time.perf_counter() - draw_started}
    else:
        candidate, detail = outdraw
        pressure = player._anchor_reply_pressure(
            candidate,
            match_seed=int(match_seed),
            deadline=time.perf_counter() + 30.0,
        )
        result["strictOutdraw"] = {
            "found": True,
            "elapsedSeconds": time.perf_counter() - draw_started,
            "solver": detail.get("solver"),
            "physicsCalls": detail.get("physicsCalls"),
            "strict": _strict_summary(candidate),
            "finiteGenericReplyScreen": pressure,
            "screenLimitation": "仅四条候选回复；零反例不等于安全。",
        }

    if run_strict_clear:
        clear_started = time.perf_counter()
        clear, detail = player._try_strict_global_contract_search(
            strict_board=strict_board,
            position=make_position(strict_board),
            tactical_plan=base_plan,
            shot_index=10,
            seeds=seeds,
            deadline=clear_started + float(clear_deadline_seconds),
        )
        result["strictBaseClear"] = {
            "found": clear is not None,
            "elapsedSeconds": time.perf_counter() - clear_started,
            "search": detail,
            "strict": _strict_summary(clear) if clear is not None else None,
            "limitation": "有限时间严格全局采样；零候选不是数学无解证明。",
        }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs-dir", type=Path, default=Path(__file__).with_name("runs"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--skip-strict-clear", action="store_true")
    parser.add_argument("--clear-deadline-seconds", type=float, default=70.0)
    args = parser.parse_args()
    output: dict[str, Any] = {
        "scope": "offline K6 transition evidence; does not change production strategy",
        "cases": {},
    }
    for name, filename, seed, run_clear in CASES:
        output["cases"][name] = _run_case(
            args.runs_dir / filename,
            seed,
            run_strict_clear=bool(run_clear and not args.skip_strict_clear),
            clear_deadline_seconds=float(args.clear_deadline_seconds),
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
