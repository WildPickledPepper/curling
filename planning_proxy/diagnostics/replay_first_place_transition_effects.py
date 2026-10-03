#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reconstruct the observable effect of an opponent move from match telemetry.

The platform log contains our input board and our actual release, but it does
not contain the opponent's release.  For each of our non-final strict turns,
this tool replays our release under its three recorded friction seeds.  It
then compares that simulated post-shot board with the next logged board
(which is after the opponent's intervening turn).  The difference is an
*observable effect* -- e.g. opponent removed/pushed an existing stone and
where its newly thrown stone settled -- not a claim about the opponent's
hidden tactic label or exact v/h/w.

Yaw and the server's execution seed are not present in the source logs.  The
report therefore keeps the three-seed agreement rate and never presents a
release reconstruction as exact.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


HOUSE_X = 2.375
HOUSE_Y = 4.880
HOUSE_R = 1.830
FRONT_HOG_Y = 10.525
MOVE_THRESHOLD_M = 0.25


def _load_decisions(path: Path) -> list[dict[str, Any]]:
    decisions: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith("SERVER_TELEMETRY "):
            continue
        event = json.loads(line[len("SERVER_TELEMETRY "):])
        if event.get("event") == "PHYSX_TOPK":
            decisions.append(event)
    return decisions


def _position_map(position: list[float]) -> dict[int, tuple[float, float]]:
    return {
        index: (float(position[index * 2]), float(position[index * 2 + 1]))
        for index in range(16)
        if float(position[index * 2]) != 0.0 or float(position[index * 2 + 1]) != 0.0
    }


def _zone(point: tuple[float, float] | None) -> str:
    if point is None:
        return "out_of_play"
    x_value, y_value = point
    if math.hypot(x_value - HOUSE_X, y_value - HOUSE_Y) <= HOUSE_R:
        return "house"
    if HOUSE_Y + HOUSE_R < y_value <= FRONT_HOG_Y:
        return "guard_zone"
    return "outside_house"


def _effect(simulated: dict[int, tuple[float, float]], observed: dict[int, tuple[float, float]], opponent_slot: int) -> dict[str, Any]:
    removed = sorted(index for index in simulated if index != opponent_slot and index not in observed)
    moved: list[dict[str, Any]] = []
    for index in sorted(set(simulated) & set(observed)):
        if index == opponent_slot:
            continue
        before, after = simulated[index], observed[index]
        distance = math.hypot(before[0] - after[0], before[1] - after[1])
        if distance >= MOVE_THRESHOLD_M:
            moved.append({
                "slot": index,
                "distance_m": round(distance, 4),
                "simulated_after_our_shot": [round(before[0], 4), round(before[1], 4)],
                "observed_after_opponent_shot": [round(after[0], 4), round(after[1], 4)],
            })
    if removed and moved:
        label = "clear_and_move"
    elif removed:
        label = "clear"
    elif moved:
        label = "hit_or_push"
    else:
        label = "placement_only"
    opponent_final = observed.get(opponent_slot)
    return {
        "effect": label,
        "removed_slots": removed,
        "moved": moved,
        "opponent_new_slot": opponent_slot,
        "opponent_final_position": None if opponent_final is None else [round(opponent_final[0], 4), round(opponent_final[1], 4)],
        "opponent_final_zone": _zone(opponent_final),
    }


def _replay_one(environment: Any, record: dict[str, Any], seed: int) -> dict[int, tuple[float, float]]:
    active_slot = int(record["shot_num"])
    # The telemetry seed is seed + active_slot * 7919.  Restore that exact
    # per-shot sequence, then reset all visible x/y with conservative yaw=0
    # because platform telemetry did not expose historical yaws.
    environment.seed = int(seed) - active_slot * 7919
    environment.scene.reset_positions(record["position"], yaw_overrides={index: 0.0 for index in range(16)})
    environment.shot_number = active_slot
    result = environment.play(record["executed_bestshot"])
    return {
        index: (float(state["x"]), float(state["y"]))
        for index, state in enumerate(result["states"])
        if bool(state["enabled"])
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--logs-root",
        type=Path,
        default=PROJECT_ROOT / "analysis_input" / "first_place_draws_20260726",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "analysis_input" / "first_place_draws_20260726" / "first_place_transition_replay_20260726.json",
    )
    args = parser.parse_args()

    # Must precede import of StrictCurlingEnd, which imports the native module.
    from local_simulator.runtime_loader import install_bundled_pyphysx
    install_bundled_pyphysx()
    from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd

    report_rows: list[dict[str, Any]] = []
    environment = StrictCurlingEnd(seed=1, training_fast=True)
    for log_path in sorted(args.logs_root.rglob("*-1.log")):
        decisions = _load_decisions(log_path)
        for index, record in enumerate(decisions):
            # A final stone is followed by a new end, not the opponent's reply.
            if index % 8 == 7:
                continue
            candidates = record.get("candidates", [])
            seeds = list(candidates[0].get("physics_seeds", [])) if candidates else []
            if not seeds:
                continue  # Template-only turns have no recorded physics seed.
            next_record = decisions[index + 1]
            active_slot = int(record["shot_num"])
            opponent_slot = active_slot + 1
            observed = _position_map(next_record["position"])
            variants = [_effect(_replay_one(environment, record, int(seed)), observed, opponent_slot) for seed in seeds]
            labels = Counter(variant["effect"] for variant in variants)
            zones = Counter(variant["opponent_final_zone"] for variant in variants)
            selected_effect, selected_count = labels.most_common(1)[0]
            report_rows.append({
                "source_log": str(log_path),
                "end_number": index // 8 + 1,
                "our_role": record["role"],
                "our_shot_number": active_slot,
                "our_selected_action": record["selected_action"],
                "our_executed_bestshot": record["executed_bestshot"],
                "recorded_physics_seeds": [int(seed) for seed in seeds],
                "opponent_slot": opponent_slot,
                "effect_mode": selected_effect,
                "effect_seed_agreement": round(selected_count / len(variants), 4),
                "opponent_final_zone": zones.most_common(1)[0][0],
                "variants": variants,
            })

    effect_counts = Counter(row["effect_mode"] for row in report_rows)
    zone_counts = Counter(row["opponent_final_zone"] for row in report_rows)
    report = {
        "scope": "Observable opponent-move effects inferred from our recorded strict turns only.",
        "limitations": [
            "Opponent v/h/w and hidden tactic labels are absent.",
            "Historical yaw and the actual platform execution seed are absent; replay uses yaw=0 and the three recorded validation seeds.",
            "A label describes board change, not the opponent model's internal intent.",
        ],
        "move_threshold_m": MOVE_THRESHOLD_M,
        "replayable_transitions": len(report_rows),
        "effect_counts": dict(sorted(effect_counts.items())),
        "opponent_final_zone_counts": dict(sorted(zone_counts.items())),
        "rows": report_rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "rows"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
