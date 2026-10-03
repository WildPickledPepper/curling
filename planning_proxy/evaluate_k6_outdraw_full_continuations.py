"""从真实 K1--K5 前缀批量重放当前 K6 outdraw 测试集到终局。

旧报告只提供前缀动作和 K6 输入。每条样本均在当前代码中连续 PhysX 重放前缀，
再让当前先手状态机与本地 PPO 完成 K6--K8；因此输出是当前版本的转移数据，而非
历史胜率。每局完成即写 JSON，便于长批次断点续跑。
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import install_bundled_pyphysx  # noqa: E402
from planning_proxy.evaluate_k7_continuation_variants import WorkerPPOOpponent, source_before  # noqa: E402
from planning_proxy.evaluate_vs_teammate_ppo import (  # noqa: E402
    Candidate,
    HOUSE_X,
    HOUSE_Y,
    ProxyMatchPlayer,
    append_log,
    canonical_board,
    evaluate_one,
    make_position,
    run_game,
)
from planning_proxy.first_player_strategy import plan_first_player_turn  # noqa: E402


OUTDRAW_BRANCHES = {
    "left": (3.080000162124634, -1.8699998903274535, 11.914285659790039),
    "right": (3.080000162124634, 1.7500000047683715, -10.714285850524902),
}


class ForcedOutdrawTopologyPlayer(ProxyMatchPlayer):
    """仅离线因果对照：提交已在当前壶面三种子复核的镜像 outdraw 分支。"""

    def __init__(self, *, branch: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.branch = str(branch)

    def choose(self, states: Any, *, proxy_team: int, shot_index: int, match_seed: int):
        if int(shot_index) != 10:
            return super().choose(states, proxy_team=proxy_team, shot_index=shot_index, match_seed=match_seed)
        strict_board, proxy_board = canonical_board(states, proxy_team)
        base = plan_first_player_turn(proxy_board, int(shot_index))
        outdraw_plan = replace(
            base,
            phase="sixth_outdraw_single_house_threat",
            target_points=((HOUSE_X, HOUSE_Y),),
            target_opponent_index=None,
            opponent_action="none",
            defence_shapes=(),
            landing_region_radius_m=0.22,
        )
        seeds = [
            int(match_seed) + int(shot_index) * 7919 + 104729 * offset
            for offset in range(self.physics_seeds)
        ]
        action = OUTDRAW_BRANCHES[self.branch]
        strict = evaluate_one(
            self.environment,
            Candidate(*action, parent_rank=1),
            strict_board,
            make_position(strict_board),
            seeds,
            int(shot_index),
            active_index=int(shot_index),
            tactical_plan=outdraw_plan,
        )
        if not (
            strict.rule_legal
            and all(strict.tactical_goal_met)
            and max(strict.own_cleared, default=99) == 0
        ):
            raise RuntimeError(f"{self.branch} outdraw branch is not a current three-seed strict solution")
        return action, {
            "mode": f"offline_forced_k6_{self.branch}_outdraw_strict",
            "candidateCount": 1,
            "eligibleCount": 1,
            "firstPlayerPlan": outdraw_plan.to_json(),
            "physicsSeeds": seeds,
            "strict": strict.to_json(),
        }


def save(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, required=True)
    parser.add_argument("--runs-dir", type=Path, default=Path(__file__).with_name("runs"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--torch-python", type=Path, default=Path(r"D:\anaconda3\python.exe"))
    parser.add_argument("--decision-budget-seconds", type=float, default=105.0)
    parser.add_argument("--physics-seeds", type=int, default=3)
    parser.add_argument("--parent-regions", type=int, default=3)
    parser.add_argument("--fixture-id", action="append", default=[])
    parser.add_argument(
        "--source",
        action="append",
        default=[],
        help="额外重放的历史完整报告文件名；用于同前缀当前续局核验，不修改状态机。",
    )
    parser.add_argument("--force-outdraw-branch", choices=("left", "right"), default=None)
    parser.add_argument(
        "--enable-k6-certified-clear-backup",
        action="store_true",
        help="仅离线：完整 K6 合同未解时使用已认证纯清保底；默认关闭。",
    )
    parser.add_argument("--limit", type=int)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    fixture_set = json.loads(args.fixtures.read_text(encoding="utf-8"))
    fixtures = list(fixture_set["fixtures"])
    requested = {str(value) for value in args.fixture_id}
    if requested:
        fixtures = [fixture for fixture in fixtures if str(fixture["fixtureId"]) in requested]
    elif args.source:
        # --source 是精确的历史前缀入口；不能在未指定 fixture-id 时顺带跑完整默认集。
        fixtures = []
    known_sources = {
        str(source)
        for fixture in fixtures
        for source in fixture.get("historicalSources", [])
    }
    for source in args.source:
        source_name = str(source)
        if source_name in known_sources:
            continue
        fixtures.append(
            {
                "fixtureId": f"historical_source_{Path(source_name).stem}",
                "historicalSources": [source_name],
                "historicalOutcomeCount": {},
                "historicalRecordCount": 1,
                "liveStoneSummary": [],
                "interpretation": "历史完整前缀的当前续局复验；旧终局不作为当前胜率。",
            }
        )
        known_sources.add(source_name)
    if args.limit is not None:
        fixtures = fixtures[: max(0, int(args.limit))]

    if args.resume and args.output.exists():
        payload = json.loads(args.output.read_text(encoding="utf-8"))
    else:
        payload = {
            "schema": "k6_current_full_continuation_evaluation_v1",
            "scope": "真实 K1--K5 前缀连续重放后的当前 K6--K8 对局；不是旧版本胜率。",
            "currentPlanner": {
                "decisionBudgetSeconds": float(args.decision_budget_seconds),
                "physicsSeeds": int(args.physics_seeds),
                "parentRegions": int(args.parent_regions),
                "enableK6CertifiedClearBackup": bool(args.enable_k6_certified_clear_backup),
            },
            "continuationOpponent": "ppo",
            "results": [],
        }
    completed = {str(item["fixtureId"]) for item in payload["results"] if "fixtureId" in item}
    progress = args.output.with_suffix(".jsonl")
    if not args.resume and progress.exists():
        progress.unlink()

    install_bundled_pyphysx()
    opponent = WorkerPPOOpponent(args.torch_python)
    try:
        for fixture in fixtures:
            fixture_id = str(fixture["fixtureId"])
            if fixture_id in completed:
                continue
            source_name = str(fixture["historicalSources"][0])
            source_path = args.runs_dir / source_name
            try:
                report, game, expected_state, prefix = source_before(source_path, 10)
                player_kwargs = {
                    "physics_seeds": int(args.physics_seeds),
                    "parent_regions": int(args.parent_regions),
                    "decision_budget_seconds": float(args.decision_budget_seconds),
                    "enable_k6_certified_clear_backup": bool(args.enable_k6_certified_clear_backup),
                }
                proxy = (
                    ForcedOutdrawTopologyPlayer(branch=str(args.force_outdraw_branch), **player_kwargs)
                    if args.force_outdraw_branch is not None
                    else ProxyMatchPlayer(**player_kwargs)
                )
                append_log(progress, {"type": "fixture_start", "fixtureId": fixture_id, "source": source_name})
                outcome = run_game(
                    game_index=len(payload["results"]) + 1,
                    proxy_team=0,
                    seed=int(game["seed"]),
                    proxy=proxy,
                    opponent=opponent,
                    opponent_label="ppo",
                    progress_path=progress,
                    start_shot=10,
                    prefix_trace=prefix,
                    expected_start_states=expected_state,
                )
                k6 = next(item for item in outcome["trace"] if int(item["shot"]) == 11)
                k7 = next(item for item in outcome["trace"] if int(item["shot"]) == 13)
                k8 = next(item for item in outcome["trace"] if int(item["shot"]) == 15)
                row: dict[str, Any] = {
                    "fixtureId": fixture_id,
                    "source": source_name,
                    "forcedOutdrawBranch": args.force_outdraw_branch,
                    "historicalOutcomeCount": fixture["historicalOutcomeCount"],
                    "historicalRecordCount": fixture["historicalRecordCount"],
                    "liveStoneSummary": fixture["liveStoneSummary"],
                    "finalScoreFirst": outcome["finalScoreProxy"],
                    "completedEnd": outcome["completedEnd"],
                    "replayStartMaxStateDelta": outcome["replayStartMaxStateDelta"],
                    "k6": {
                        "mode": k6.get("detail", {}).get("mode"),
                        "phase": k6.get("detail", {}).get("firstPlayerPlan", {}).get("phase"),
                        "action": k6.get("bestshot"),
                        "decisionSeconds": k6.get("decisionSeconds"),
                    },
                    "k7": {
                        "mode": k7.get("detail", {}).get("mode"),
                        "phase": k7.get("detail", {}).get("firstPlayerPlan", {}).get("phase"),
                        "action": k7.get("bestshot"),
                        "decisionSeconds": k7.get("decisionSeconds"),
                    },
                    "k8": {
                        "mode": k8.get("detail", {}).get("mode"),
                        "phase": k8.get("detail", {}).get("firstPlayerPlan", {}).get("phase"),
                        "action": k8.get("bestshot"),
                        "decisionSeconds": k8.get("decisionSeconds"),
                    },
                }
            except Exception as error:  # Keep batch evidence even when a source cannot replay.
                row = {"fixtureId": fixture_id, "source": source_name, "error": repr(error)}
            payload["results"].append(row)
            save(args.output, payload)
            append_log(progress, {"type": "fixture_end", "fixtureId": fixture_id, "result": row})
            print(
                f"{fixture_id} score={row.get('finalScoreFirst')} error={row.get('error')}",
                flush=True,
            )
    finally:
        opponent.close()
    save(args.output, payload)
    print(args.output)


if __name__ == "__main__":
    main()
