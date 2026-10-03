#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Filter NWNHT K1->K2 records for the local no-tick centre-guard rule.

This is deliberately a *conditional evidence* artifact, not a replacement for
the 95-state universal MDP.  K1 is fixed locally to the calibrated centre
guard.  We retain only historical opponent replies for which the original
first stone remains in the free guard zone and still touches the centre line.
Older real-world matches and outcomes in which the non-offending team chose to
leave a ticked guard are reported as excluded, because the local match runner
always restores that position.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping


HOUSE_R_M = 1.830
STONE_R_M = 0.145
FRONT_HOG_FROM_BUTTON_M = 10.525 - 4.880
ANCHOR_X_M = 0.0
ANCHOR_Y_M = 7.15 - 4.880


def _read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def _distance(stone: Mapping[str, Any]) -> float:
    return math.hypot(float(stone["x_m"]), float(stone["y_m"]))


def in_free_guard_zone(stone: Mapping[str, Any]) -> bool:
    return (
        0.0 <= float(stone["y_m"]) <= FRONT_HOG_FROM_BUTTON_M
        and _distance(stone) > HOUSE_R_M + STONE_R_M
    )


def touches_centre_line(stone: Mapping[str, Any]) -> bool:
    return abs(float(stone["x_m"])) <= STONE_R_M


def is_local_k1_anchor(stone: Mapping[str, Any]) -> bool:
    """Historical K1 centre guard usable as a local-anchor analogue.

    Its longitudinal position is retained as a similarity feature below, not
    as a hard inclusion gate.  Historical teams used several valid guard
    depths; deleting them before contextual retrieval made rare S2 branches
    appear much rarer than they are.
    """

    return (
        str(stone.get("owner")) == "first"
        and in_free_guard_zone(stone)
        and touches_centre_line(stone)
        and abs(float(stone["x_m"]) - ANCHOR_X_M) <= STONE_R_M
    )


def has_preserved_anchor(board: Iterable[Mapping[str, Any]]) -> bool:
    """The local rule invariant after the opponent's second global delivery."""

    return any(
        str(stone.get("owner")) == "first"
        and in_free_guard_zone(stone)
        and touches_centre_line(stone)
        for stone in board
    )


def reply_class(board: Iterable[Mapping[str, Any]]) -> str:
    """Small, interpretable S2 partition conditional on the preserved anchor."""

    opponents = [stone for stone in board if str(stone.get("owner")) == "opponent"]
    if not opponents:
        return "S2_LOCAL_ANCHOR_ONLY"
    # There is at most one opponent stone after the second global delivery,
    # but retain a conservative priority order for malformed historical rows.
    if any(_distance(stone) <= HOUSE_R_M + STONE_R_M for stone in opponents):
        return "S2_LOCAL_ANCHOR_OPPONENT_HOUSE"
    if any(in_free_guard_zone(stone) and touches_centre_line(stone) for stone in opponents):
        return "S2_LOCAL_ANCHOR_OPPONENT_CENTRE_GUARD"
    if any(in_free_guard_zone(stone) for stone in opponents):
        return "S2_LOCAL_ANCHOR_OPPONENT_SIDE_GUARD"
    return "S2_LOCAL_ANCHOR_OPPONENT_OTHER_IN_PLAY"


def build(
    transitions: Iterable[Mapping[str, Any]], *, old_state_by_panel: Mapping[str, str],
) -> dict[str, Any]:
    candidates = retained = excluded_no_tick = 0
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    old_state_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for row in transitions:
        if int(row.get("own_throw_number", -1)) != 1:
            continue
        after_own = list(row.get("u_after_own", []))
        if not any(is_local_k1_anchor(stone) for stone in after_own):
            continue
        candidates += 1
        after_reply = list(row.get("s_after_opponent_reply", []))
        if not has_preserved_anchor(after_reply):
            excluded_no_tick += 1
            continue
        retained += 1
        state = reply_class(after_reply)
        panel_key = f"{row['end_id']}:{row['own_global_shot_number']}"
        old_state = str(old_state_by_panel.get(panel_key, "UNMAPPED"))
        old_state_counts[state][old_state] += 1
        anchor_after_own = [dict(stone) for stone in after_own if is_local_k1_anchor(stone)][0]
        groups[state].append({
            "panel_key": panel_key,
            "match_id": int(row["match_id"]),
            "event_start_date": str(row.get("offline_context", {}).get("event_start_date", "")),
            "historical_s2_state": old_state,
            "opponent_reply_called_shot": str(row.get("observed_opponent_reply", {}).get("called_shot", "")),
            "anchor_after_own": anchor_after_own,
            "anchor_target_y_offset_m": round(float(anchor_after_own["y_m"]) - ANCHOR_Y_M, 6),
            "board_after_opponent_reply": after_reply,
        })
    state_rows = []
    for state, rows in sorted(groups.items()):
        rows.sort(key=lambda item: (item["match_id"], item["panel_key"]))
        offsets = sorted(abs(float(item["anchor_target_y_offset_m"])) for item in rows)
        def percentile(q: float) -> float:
            return round(offsets[round((len(offsets) - 1) * q)], 6)
        state_rows.append({
            "state_id": state,
            "K": 2,
            "direct_support": len(rows),
            "anchor_target_distance_y_m": {"p50": percentile(0.5), "p90": percentile(0.9), "max": percentile(1.0)},
            "historical_s2_state_distribution": [
                {"value": value, "count": count, "share": round(count / len(rows), 6)}
                for value, count in old_state_counts[state].most_common()
            ],
            "examples": rows[:10],
        })
    return {
        "manifest": {
            "schema": "nwnht_local_k1_anchor_k2_subset_v3",
            "purpose": "Historical K1->K2 reply evidence compatible with the local forced no-tick rollback rule.",
            "local_anchor": {
                "coordinate_frame": "NWNHT_BUTTON_CENTRED_METRES",
                "target_x_m": ANCHOR_X_M,
                "target_y_m": ANCHOR_Y_M,
                "historical_y_filter": "none; anchor y offset is retained per record for contextual nearest-neighbour weighting",
                "required_after_opponent_reply": "first anchor remains in FGZ and touches centre line",
            },
            "candidate_historical_k1_centre_guard_rows": candidates,
            "retained_local_legal_reply_rows": retained,
            "excluded_no_tick_conflict_rows": excluded_no_tick,
            "state_count": len(state_rows),
            "warning": "Excluded rows are not evidence that a local opponent would pass. They are rule-incompatible historical outcomes and must not be used as local S2 transition support.",
        },
        "states": state_rows,
    }


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--transitions", type=Path, default=root / "nwnht_first_player_causal_transitions_v0.jsonl")
    parser.add_argument("--templates", type=Path, default=root / "nwnht_v2_goal_templates_v0.jsonl")
    parser.add_argument("--output", type=Path, default=root / "nwnht_local_k1_anchor_k2_subset_v3.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new output path.")
    old_state_by_panel = {
        str(row["panel_key"]): str(row["after_opponent_reply_state"])
        for row in _read_jsonl(args.templates) if int(row["K"]) == 1
    }
    result = build(_read_jsonl(args.transitions), old_state_by_panel=old_state_by_panel)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), **result["manifest"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
