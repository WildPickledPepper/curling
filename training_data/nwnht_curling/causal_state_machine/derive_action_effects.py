#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Derive auditable *board-effect* labels for first-player causal panels.

The label describes observable change from S (before own delivery) to U
(immediately after own delivery).  It never treats the upstream call text as
the action definition.  Labels are deliberately conservative and may include
multiple facts; ``primary_effect`` is only a deterministic indexing key for
the next causal-analysis stage.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


HOUSE_RADIUS_M = 1.8288
CENTER_LANE_M = 0.38
FRONT_GUARD_Y_MAX = 6.45
# NWNHT positions are upstream CV-derived coordinates, not a certified
# measurement.  At or within this gap between the closest opposing stones, we
# abstain from asserting either side has scoring control.  This is a cautious
# data-label convention (not a claim about the physical measuring rule).
SCORING_CONTROL_MARGIN_M = 0.005


def board_facts(board: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = list(board)
    result: dict[str, Any] = {"visible": len(rows)}
    in_house: dict[str, list[float]] = {"first": [], "opponent": []}
    for owner in ("first", "opponent"):
        owned = [row for row in rows if row["owner"] == owner]
        house = [row for row in owned if math.hypot(float(row["x_m"]), float(row["y_m"])) <= HOUSE_RADIUS_M]
        guards = [row for row in owned if HOUSE_RADIUS_M < float(row["y_m"]) <= FRONT_GUARD_Y_MAX]
        result[f"{owner}_visible"] = len(owned)
        result[f"{owner}_in_house"] = len(house)
        result[f"{owner}_guards"] = len(guards)
        result[f"{owner}_centre_guards"] = sum(abs(float(row["x_m"])) <= CENTER_LANE_M for row in guards)
        in_house[owner] = sorted(math.hypot(float(row["x_m"]), float(row["y_m"])) for row in house)

    first_nearest = in_house["first"][0] if in_house["first"] else None
    opponent_nearest = in_house["opponent"][0] if in_house["opponent"] else None
    result["scoring_control_margin_m"] = None if first_nearest is None or opponent_nearest is None else abs(first_nearest - opponent_nearest)
    if first_nearest is None and opponent_nearest is None:
        result["scoring_owner"] = None
        result["scoring_count"] = 0
        result["scoring_control_certain"] = False
    elif opponent_nearest is None:
        result["scoring_owner"] = "first"
        result["scoring_count"] = len(in_house["first"])
        result["scoring_control_certain"] = True
    elif first_nearest is None:
        result["scoring_owner"] = "opponent"
        result["scoring_count"] = len(in_house["opponent"])
        result["scoring_control_certain"] = True
    elif abs(first_nearest - opponent_nearest) <= SCORING_CONTROL_MARGIN_M:
        result["scoring_owner"] = None
        result["scoring_count"] = 0
        result["scoring_control_certain"] = False
    elif first_nearest < opponent_nearest:
        result["scoring_owner"] = "first"
        result["scoring_count"] = sum(distance < opponent_nearest for distance in in_house["first"])
        result["scoring_control_certain"] = True
    else:
        result["scoring_owner"] = "opponent"
        result["scoring_count"] = sum(distance < first_nearest for distance in in_house["opponent"])
        result["scoring_control_certain"] = True
    return result


def action_effect(before_board: list[dict[str, Any]], after_board: list[dict[str, Any]]) -> dict[str, Any]:
    before, after = board_facts(before_board), board_facts(after_board)
    delta = {key: int(after[key]) - int(before[key]) for key in after if key.endswith(("visible", "in_house", "guards", "centre_guards"))}
    tags: list[str] = []
    if delta["opponent_in_house"] < 0:
        tags.append("OPPONENT_HOUSE_LAYER_REDUCED")
    if delta["first_in_house"] > 0:
        tags.append("FIRST_HOUSE_LAYER_ADDED")
    if delta["first_guards"] > 0:
        tags.append("FIRST_PRESSURE_GUARD_ADDED")
    if before["scoring_owner"] == "opponent" and after["scoring_owner"] == "first":
        tags.append("FIRST_TAKES_SCORING_CONTROL")
    if delta["visible"] < 0:
        tags.append("STONE_COUNT_REDUCED")
    if before["scoring_owner"] == after["scoring_owner"] and before["scoring_count"] == after["scoring_count"] and not tags:
        tags.append("NO_OBSERVABLE_MACRO_CHANGE")

    # Priority intentionally favours observable strategic result over a
    # guessed shot mechanism.  For example, a hit-and-roll and an outdraw can
    # both honestly map to FIRST_TAKES_SCORING_CONTROL at this stage.
    if "FIRST_TAKES_SCORING_CONTROL" in tags:
        primary = "GAIN_OWN_SCORING_CONTROL"
    elif "OPPONENT_HOUSE_LAYER_REDUCED" in tags:
        primary = "REDUCE_OPPONENT_HOUSE_LAYER"
    elif "FIRST_HOUSE_LAYER_ADDED" in tags:
        primary = "ADD_OWN_HOUSE_LAYER"
    elif "FIRST_PRESSURE_GUARD_ADDED" in tags:
        primary = "ADD_PRESSURE_GUARD"
    elif "STONE_COUNT_REDUCED" in tags:
        # A lower total can mean an opponent stone was cleared, a self stone
        # was lost, or a mixed collision.  Without stone identities across
        # CV snapshots, calling it a "clear" would overstate what we know.
        primary = "REDUCE_STONE_COUNT_WITHOUT_CONTROL"
    else:
        primary = "NO_CLASSIFIABLE_MACRO_EFFECT"
    return {"primary_effect": primary, "effect_tags": tags, "before": before, "after": after, "delta": delta}


def derive(rows: Iterable[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    output: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    by_k: dict[str, Counter[str]] = {}
    for row in rows:
        updated = dict(row)
        effect = action_effect(list(row["s_before_own"]), list(row["u_after_own"]))
        updated["observed_own_board_effect"] = effect
        output.append(updated)
        counts[effect["primary_effect"]] += 1
        by_k.setdefault(str(row["own_throw_number"]), Counter())[effect["primary_effect"]] += 1
    return output, {
        "schema": "nwnht_first_player_board_effect_taxonomy_manifest_v2",
        "definition": "Observable S->U board-effect labels; not causal treatment effects and not a PhysX action library.",
        "scoring_control_margin_m": SCORING_CONTROL_MARGIN_M,
        "scoring_control_note": "Within this CV-coordinate margin, scoring control is deliberately marked uncertain rather than assigned by a floating-point tie-break.",
        "row_count": len(output),
        "primary_effect_counts": dict(sorted(counts.items())),
        "primary_effect_counts_by_K": {key: dict(sorted(value.items())) for key, value in sorted(by_k.items())},
        "manual_validation_required": "Randomly inspect at least 30 rows per primary effect before using labels as causal treatments.",
    }


def read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            yield json.loads(line)


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=root / "nwnht_first_player_causal_transitions_v0.jsonl")
    parser.add_argument("--output", type=Path, default=root / "nwnht_first_player_board_effects_v2.jsonl")
    parser.add_argument("--manifest", type=Path, default=root / "nwnht_first_player_board_effects_v2_manifest.json")
    args = parser.parse_args()
    for path in (args.output, args.manifest):
        if path.exists():
            raise SystemExit(f"Refusing to overwrite {path}; choose a new path deliberately.")
    rows, manifest = derive(read_jsonl(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "manifest": str(args.manifest), "rows": len(rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
