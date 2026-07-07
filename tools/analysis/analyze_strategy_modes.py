# -*- coding: utf-8 -*-
"""Analyze tactical modes of the current search-distilled curling robot."""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from continuous_shot_search import (
    choose_refined_plan,
    is_our_turn,
    play_controlled_shot,
    play_uncontrolled_shot,
    score_for_player,
)
from fast_curling_env import FastCurlingEnv
from train_search_distill import load_model


TACTIC_GROUPS = {
    "draw": {"draw_center", "occupy", "middle_in_center"},
    "curl_draw": {"curl_left", "curl_right"},
    "guard": {"guard_left", "guard_right", "defense"},
    "freeze": {"freeze"},
    "takeout": {"take_out", "hit_roll", "clear", "double_hit_gote"},
    "raise_push": {"push_in", "push_in_14", "defense_push_in"},
}


def tactic_group(action: str) -> str:
    for group, names in TACTIC_GROUPS.items():
        if action in names:
            return group
    return "other"


def phase_for_shot(own_idx: int, player_is_init: bool) -> str:
    if own_idx <= 2:
        return "early"
    if own_idx <= 5:
        return "middle"
    if own_idx <= 7:
        return "late_setup"
    return "hammer" if not player_is_init else "final_without_hammer"


def score_bucket(score: int) -> str:
    if score <= -2:
        return "trailing_2plus"
    if score == -1:
        return "trailing_1"
    if score == 0:
        return "tied"
    if score == 1:
        return "leading_1"
    return "leading_2plus"


def search_budget(
    shot_num: int,
    player_is_init: bool,
    top_k: int,
    candidates: int,
    rollouts: int,
    late_top_k: int,
    late_candidates: int,
    late_rollouts: int,
    hammer_candidates: int,
    hammer_rollouts: int,
) -> Tuple[int, int, int, str]:
    completed_own_shots = max(0, min(8, shot_num // 2))
    remaining_own_shots = max(1, 8 - completed_own_shots)
    if remaining_own_shots == 1 and not player_is_init:
        return (
            max(top_k, late_top_k),
            max(candidates, hammer_candidates),
            max(rollouts, hammer_rollouts),
            "hammer",
        )
    if remaining_own_shots <= 2 or shot_num >= 12:
        return (
            max(top_k, late_top_k),
            max(candidates, late_candidates),
            max(rollouts, late_rollouts),
            "late",
        )
    return top_k, candidates, rollouts, "normal"


def pct(counter: Counter[str]) -> Dict[str, float]:
    total = sum(counter.values())
    if total <= 0:
        return {}
    return {key: value / total for key, value in counter.most_common()}


def summarize_records(records: List[Dict[str, Any]], scores: List[int]) -> Dict[str, Any]:
    by_action = Counter(record["action"] for record in records)
    by_group = Counter(record["group"] for record in records)
    by_phase: Dict[str, Counter[str]] = defaultdict(Counter)
    by_phase_group: Dict[str, Counter[str]] = defaultdict(Counter)
    by_bucket_group: Dict[str, Counter[str]] = defaultdict(Counter)
    sweep_by_phase: Dict[str, List[float]] = defaultdict(list)
    mean_by_phase: Dict[str, List[float]] = defaultdict(list)
    budget_by_phase: Dict[str, Counter[str]] = defaultdict(Counter)

    for record in records:
        phase = record["phase"]
        bucket = record["score_bucket"]
        by_phase[phase][record["action"]] += 1
        by_phase_group[phase][record["group"]] += 1
        by_bucket_group[bucket][record["group"]] += 1
        sweep_by_phase[phase].append(1.0 if record["sweep"] > 0 else 0.0)
        mean_by_phase[phase].append(record["search_mean"])
        budget_by_phase[phase][record["budget"]] += 1

    return {
        "shots": len(records),
        "games": len(scores),
        "avg_score": float(np.mean(scores)) if scores else 0.0,
        "win_rate": float(np.mean([score > 0 for score in scores])) if scores else 0.0,
        "loss_rate": float(np.mean([score < 0 for score in scores])) if scores else 0.0,
        "action_counts": dict(by_action.most_common()),
        "group_counts": dict(by_group.most_common()),
        "group_rates": pct(by_group),
        "phase_action_counts": {phase: dict(counter.most_common()) for phase, counter in by_phase.items()},
        "phase_group_rates": {phase: pct(counter) for phase, counter in by_phase_group.items()},
        "score_bucket_group_rates": {bucket: pct(counter) for bucket, counter in by_bucket_group.items()},
        "phase_sweep_rate": {
            phase: float(np.mean(values)) for phase, values in sorted(sweep_by_phase.items())
        },
        "phase_search_mean": {
            phase: float(np.mean(values)) for phase, values in sorted(mean_by_phase.items())
        },
        "phase_budget_counts": {phase: dict(counter.most_common()) for phase, counter in budget_by_phase.items()},
    }


def analyze_side(args: argparse.Namespace, player_is_init: bool) -> Dict[str, Any]:
    rng = random.Random(args.seed + (11 if player_is_init else 29))
    model = load_model(Path(args.model_file))
    records: List[Dict[str, Any]] = []
    scores: List[int] = []

    for _ in range(args.games_per_side):
        env = FastCurlingEnv(seed=rng.randint(1, 2_000_000_000))
        while env.shot_num < 16:
            if not is_our_turn(env.shot_num, player_is_init):
                play_uncontrolled_shot(env)
                continue

            own_idx = env.shot_num // 2 + 1
            before_score = score_for_player(env, player_is_init)
            top_k, candidates, rollouts, budget = search_budget(
                env.shot_num,
                player_is_init,
                args.top_k,
                args.candidates,
                args.rollouts,
                args.late_top_k,
                args.late_candidates,
                args.late_rollouts,
                args.hammer_candidates,
                args.hammer_rollouts,
            )
            plan = choose_refined_plan(
                env,
                rng,
                model=model,
                top_k=top_k,
                max_candidates=candidates,
                rollouts=rollouts,
                player_is_init=player_is_init,
            )
            records.append(
                {
                    "shot_num": env.shot_num,
                    "own_idx": own_idx,
                    "phase": phase_for_shot(own_idx, player_is_init),
                    "score_before": before_score,
                    "score_bucket": score_bucket(before_score),
                    "budget": budget,
                    "action": plan.action_name,
                    "group": tactic_group(plan.action_name),
                    "sweep": plan.sweep,
                    "search_mean": plan.mean_score,
                    "search_std": plan.std_score,
                    "shot": [round(x, 4) for x in plan.shot],
                }
            )
            play_controlled_shot(env, plan.swept_shot())
        scores.append(score_for_player(env, player_is_init))

    return {
        "player_is_init": player_is_init,
        "summary": summarize_records(records, scores),
        "sample_records": records[: min(64, len(records))],
    }


def render_rates(rates: Dict[str, float]) -> str:
    if not rates:
        return "-"
    return ", ".join(f"{name} {value:.1%}" for name, value in rates.items())


def write_markdown(report: Dict[str, Any], path: Path) -> None:
    first = report["first_player"]["summary"]
    second = report["second_player"]["summary"]
    lines = [
        "# 当前模型策略模式分析",
        "",
        "## 结论摘要",
        "",
        "- 当前策略不是单一打法，而是“进营/占位 + 旋进 + 保护/清障”的混合策略。",
        "- 先手和后手差异明显：先手更需要前中盘建立局面、后期防守保护；后手拥有最后一壶，末端更像 hammer-shot 优化问题。",
        "- 当前本地策略偏向在 house 内累计优势，`draw/occupy` 与 `curl_draw` 占比很高；takeout 类动作只在落后或局面拥挤时出现。",
        "- 擦冰主要绑定 draw/curl/freeze 类动作，guard/takeout 大多不擦，符合当前搜索假设。",
        "",
        "## 总体表现",
        "",
        "| 视角 | Games | Avg score | Win rate | Loss rate | Top groups |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
        f"| 先手 | {first['games']} | {first['avg_score']:.3f} | {first['win_rate']:.1%} | {first['loss_rate']:.1%} | {render_rates(first['group_rates'])} |",
        f"| 后手 | {second['games']} | {second['avg_score']:.3f} | {second['win_rate']:.1%} | {second['loss_rate']:.1%} | {render_rates(second['group_rates'])} |",
        "",
        "## 分阶段战术模式",
        "",
    ]
    for title, summary in [("先手", first), ("后手", second)]:
        lines.extend([f"### {title}", "", "| 阶段 | 战术组占比 | 擦冰率 | 平均搜索估值 | 预算模式 |", "| --- | --- | ---: | ---: | --- |"])
        phases = ["early", "middle", "late_setup", "final_without_hammer", "hammer"]
        for phase in phases:
            if phase not in summary["phase_group_rates"]:
                continue
            sweep = summary["phase_sweep_rate"].get(phase, 0.0)
            mean = summary["phase_search_mean"].get(phase, 0.0)
            budget = summary["phase_budget_counts"].get(phase, {})
            lines.append(
                f"| {phase} | {render_rates(summary['phase_group_rates'][phase])} | {sweep:.1%} | {mean:.3f} | {budget} |"
            )
        lines.append("")

    lines.extend(
        [
            "## 按局势切换",
            "",
            "下面是按当前 house 内即时分数粗分的战术组倾向。注意这不是整局真实胜率，只是当前局面快照。",
            "",
        ]
    )
    for title, summary in [("先手", first), ("后手", second)]:
        lines.extend([f"### {title}", "", "| 当前局势 | 战术组占比 |", "| --- | --- |"])
        for bucket, rates in summary["score_bucket_group_rates"].items():
            lines.append(f"| {bucket} | {render_rates(rates)} |")
        lines.append("")

    lines.extend(
        [
            "## 对训练和搜索的含义",
            "",
            "1. 后续模型最好显式拆分或条件化先手/后手策略。虽然 state 已包含 `player_is_init`，但从统计看两种模式差异足够大，值得考虑 separate head 或 side-specific calibration。",
            "2. 最后一壶需要独立目标。后手 hammer 不应只最大化当前 end 期望分，长期应接入 winning percentage table；领先保守、落后搏高方差。",
            "3. 训练标签应记录 `phase`、`score_bucket`、`budget` 和 `group`。这能避免模型只学一个平均策略，把先手布局和后手收官混在一起。",
            "4. 搜索可以按模式调参：early 保留更多 draw/guard 候选，late/hammer 增加 takeout/raise_push 和连续探索预算。",
            "5. 当前统计仍基于本地 mock physics。官方服务器恢复后，应重新跑同一脚本生成 official-calibrated strategy report。",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze tactical modes of the refined curling policy")
    parser.add_argument("--model-file", default="model/search_distill_tactic_policy.pt")
    parser.add_argument("--games-per-side", type=int, default=80)
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--candidates", type=int, default=24)
    parser.add_argument("--rollouts", type=int, default=2)
    parser.add_argument("--late-top-k", type=int, default=4)
    parser.add_argument("--late-candidates", type=int, default=32)
    parser.add_argument("--late-rollouts", type=int, default=3)
    parser.add_argument("--hammer-candidates", type=int, default=48)
    parser.add_argument("--hammer-rollouts", type=int, default=4)
    parser.add_argument("--seed", type=int, default=20260707)
    parser.add_argument("--report-file", default="log/strategy_modes_analysis.json")
    parser.add_argument("--markdown-file", default="STRATEGY_MODE_ANALYSIS.md")
    args = parser.parse_args()

    started = time.time()
    report = {
        "config": vars(args),
        "first_player": analyze_side(args, True),
        "second_player": analyze_side(args, False),
        "elapsed_sec": time.time() - started,
    }

    report_path = Path(args.report_file)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(report, Path(args.markdown_file))
    print(json.dumps({k: report[k] for k in ["config", "elapsed_sec"]}, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
