#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prepare a grouped-fold causal-estimation panel; does not estimate effects."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

try:
    from .build_causal_state_abstraction import _opponent_reply_effect, read_jsonl, state_key
except ImportError:  # pragma: no cover
    import sys
    ROOT = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(ROOT))
    from causal_state_machine.build_causal_state_abstraction import _opponent_reply_effect, read_jsonl, state_key  # type: ignore


FOLDS = 5
MIN_ACTION_SUPPORT = 100


def fold_for_match(match_id: int) -> int:
    return hashlib.sha256(f"nwnht-causal-fold:{match_id}".encode("ascii")).digest()[0] % FOLDS


def build(rows: Iterable[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    panel: list[dict[str, Any]] = []
    state_actions: dict[str, Counter[str]] = defaultdict(Counter)
    k_actions: dict[int, Counter[str]] = defaultdict(Counter)
    z_cells: Counter[tuple[str, str, str]] = Counter()
    for row in rows:
        k = int(row["own_throw_number"])
        core = state_key(k, list(row["s_before_own"]))
        fine = state_key(k, list(row["s_before_own"]), fine=True)
        action = str(row["observed_own_board_effect"]["primary_effect"])
        event = str(row["offline_context"]["event_name"])
        z = {"first_team": str(row["first_team"]), "opponent_team": str(row["opponent_team"]), "event_name": event}
        panel.append({
            "panel_key": f"{row['end_id']}:{row['own_global_shot_number']}",
            "match_id": int(row["match_id"]), "fold": fold_for_match(int(row["match_id"])), "K": k,
            "runtime_core_state": core, "runtime_fine_state": fine,
            "observed_own_effect": action,
            "observed_opponent_reply_effect": _opponent_reply_effect(list(row["u_after_own"]), list(row["s_after_opponent_reply"])),
            "terminal_first_end_margin": int(row["terminal_end_label"]["first_end_margin"]),
            "offline_confounders": z,
        })
        state_actions[core][action] += 1
        k_actions[k][action] += 1
        z_cells[(z["first_team"], z["opponent_team"], event)] += 1
    eligible = {
        state: dict(sorted(actions.items()))
        for state, actions in state_actions.items()
        if sum(actions.values()) >= MIN_ACTION_SUPPORT and any(count >= MIN_ACTION_SUPPORT for count in actions.values())
    }
    manifest = {
        "schema": "nwnht_first_player_causal_estimation_panel_v0",
        "purpose": "Cross-fitted causal-estimation input only; no causal values or policy recommendations are present.",
        "runtime_contract": "Only K and runtime_core_state/runtime_fine_state may enter a deployed policy. All remaining identifiers are offline-only.",
        "treatment_caveat": "observed_own_effect is a post-shot board-effect label. It is an estimand proxy for achieving an effect, not an independently randomized human intention.",
        "folding": {"kind": "deterministic SHA-256 grouped by match_id", "folds": FOLDS},
        "summary": {
            "rows": len(panel), "matches": len({row['match_id'] for row in panel}),
            "runtime_core_states": len(state_actions), "offline_team_pair_event_cells": len(z_cells),
            "states_with_any_action_support_at_least_100": len(eligible),
            "actions_by_K": {str(k): dict(sorted(v.items())) for k, v in sorted(k_actions.items())},
        },
        "overlap_screen": {
            "minimum_observed_action_support": MIN_ACTION_SUPPORT,
            "eligible_state_action_counts": eligible,
            "warning": "This is raw action support, not propensity overlap. DR/AIPW must still reject low estimated propensity and unstable folds.",
        },
    }
    return panel, manifest


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=root / "nwnht_first_player_board_effects_v2.jsonl")
    parser.add_argument("--output", type=Path, default=root / "nwnht_first_player_causal_estimation_panel_v0.jsonl")
    parser.add_argument("--manifest", type=Path, default=root / "nwnht_first_player_causal_estimation_panel_v0_manifest.json")
    args = parser.parse_args()
    if args.output.exists() or args.manifest.exists():
        raise SystemExit("Refusing to overwrite existing panel output; choose new paths deliberately.")
    panel, manifest = build(read_jsonl(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for row in panel:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "manifest": str(args.manifest), **manifest["summary"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
