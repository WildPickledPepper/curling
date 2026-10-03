#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild and verify causal-transition and board-effect artifacts against SQLite."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

try:
    from .build_action_effect_audit_sample import _compact
    from .build_first_player_causal_transitions import build_rows
    from .derive_action_effects import SCORING_CONTROL_MARGIN_M, action_effect
except ImportError:  # pragma: no cover - direct script invocation
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.build_action_effect_audit_sample import _compact  # type: ignore
    from causal_state_machine.build_first_player_causal_transitions import build_rows  # type: ignore
    from causal_state_machine.derive_action_effects import SCORING_CONTROL_MARGIN_M, action_effect  # type: ignore


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle]


def key(row: dict[str, Any]) -> tuple[int, int]:
    return int(row["end_id"]), int(row["own_throw_number"])


def same(left: Any, right: Any) -> bool:
    return json.dumps(left, ensure_ascii=False, sort_keys=True, separators=(",", ":")) == json.dumps(right, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _independent_primary_violation(row: dict[str, Any]) -> str | None:
    """Check the minimal observable fact promised by the primary label.

    This intentionally does not call ``action_effect`` or ``board_facts``.
    It is a second, small implementation of only the label contracts, so a
    classifier regression cannot be hidden merely by recomputing with itself.
    """
    before = list(row["s_before_own"])
    after = list(row["u_after_own"])
    effect = str(row["observed_own_board_effect"]["primary_effect"])

    def house_count(board: list[dict[str, Any]], owner: str) -> int:
        return sum(
            1
            for stone in board
            if stone["owner"] == owner
            and float(stone["x_m"]) ** 2 + float(stone["y_m"]) ** 2 <= 1.8288 ** 2
        )

    def guard_count(board: list[dict[str, Any]], owner: str) -> int:
        return sum(
            1
            for stone in board
            if stone["owner"] == owner
            and 1.8288 < float(stone["y_m"]) <= 6.45
        )

    def scoring_owner(board: list[dict[str, Any]]) -> str | None:
        in_house = [
            (math.hypot(float(stone["x_m"]), float(stone["y_m"])), str(stone["owner"]))
            for stone in board
            if float(stone["x_m"]) ** 2 + float(stone["y_m"]) ** 2 <= 1.8288 ** 2
        ]
        if not in_house:
            return None
        nearest_by_owner = {
            owner: min(distance for distance, candidate in in_house if candidate == owner)
            for owner in ("first", "opponent")
            if any(candidate == owner for _, candidate in in_house)
        }
        if len(nearest_by_owner) == 2 and abs(nearest_by_owner["first"] - nearest_by_owner["opponent"]) <= SCORING_CONTROL_MARGIN_M:
            return None
        return min(in_house)[1]

    if effect == "GAIN_OWN_SCORING_CONTROL":
        return None if scoring_owner(before) == "opponent" and scoring_owner(after) == "first" else "scoring_control_not_gained"
    if effect == "REDUCE_OPPONENT_HOUSE_LAYER":
        return None if house_count(after, "opponent") < house_count(before, "opponent") else "opponent_house_not_reduced"
    if effect == "ADD_OWN_HOUSE_LAYER":
        return None if house_count(after, "first") > house_count(before, "first") else "own_house_not_added"
    if effect == "ADD_PRESSURE_GUARD":
        return None if guard_count(after, "first") > guard_count(before, "first") else "own_guard_not_added"
    if effect == "REDUCE_STONE_COUNT_WITHOUT_CONTROL":
        return None if len(after) < len(before) else "stone_count_not_reduced"
    if effect == "NO_CLASSIFIABLE_MACRO_EFFECT":
        return None
    return "unknown_primary_effect"


def verify(
    *,
    database: Path,
    match_types: tuple[str, ...],
    transitions_path: Path,
    effects_path: Path,
    audit_path: Path,
) -> dict[str, Any]:
    expected_rows, source_manifest, _ = build_rows(database, match_types)
    stored_rows = read_jsonl(transitions_path)
    expected_by_key = {key(row): row for row in expected_rows}
    stored_by_key = {key(row): row for row in stored_rows}
    transition_mismatches: list[dict[str, Any]] = []
    fields = (
        "offline_context", "source_frames", "s_before_own", "observed_own_delivery", "u_after_own",
        "observed_opponent_reply", "s_after_opponent_reply", "terminal_end_label",
    )
    for row_key, expected in expected_by_key.items():
        actual = stored_by_key.get(row_key)
        bad_fields = [] if actual is not None else ["missing_row"]
        if actual is not None:
            bad_fields = [field for field in fields if not same(expected[field], actual.get(field))]
        if bad_fields and len(transition_mismatches) < 10:
            transition_mismatches.append({"key": row_key, "fields": bad_fields})

    effect_rows = read_jsonl(effects_path)
    effect_by_key = {key(row): row for row in effect_rows}
    effect_mismatches: list[dict[str, Any]] = []
    effect_source_mismatches: list[dict[str, Any]] = []
    primary_contract_violations: list[dict[str, Any]] = []
    for row_key, row in effect_by_key.items():
        expected = action_effect(list(row["s_before_own"]), list(row["u_after_own"]))
        if not same(expected, row.get("observed_own_board_effect")) and len(effect_mismatches) < 10:
            effect_mismatches.append({"key": row_key, "expected": expected, "actual": row.get("observed_own_board_effect")})
        transition = stored_by_key.get(row_key)
        bad_fields = [] if transition is not None else ["missing_transition_row"]
        if transition is not None:
            bad_fields = [field for field in fields if not same(transition.get(field), row.get(field))]
        if bad_fields and len(effect_source_mismatches) < 10:
            effect_source_mismatches.append({"key": row_key, "fields": bad_fields})
        violation = _independent_primary_violation(row)
        if violation is not None and len(primary_contract_violations) < 10:
            primary_contract_violations.append({"key": row_key, "reason": violation})

    audit_rows = read_jsonl(audit_path)
    audit_keys = [str(row["audit_key"]) for row in audit_rows]
    audit_mismatches: list[dict[str, Any]] = []
    for audit_row in audit_rows:
        source_key = int(audit_row["end_id"]), (int(audit_row["own_throw_number"]))
        source = effect_by_key.get(source_key)
        if source is None or not same(_compact(source) if source is not None else None, audit_row):
            if len(audit_mismatches) < 10:
                audit_mismatches.append({"audit_key": audit_row["audit_key"], "reason": "missing_or_modified_source_row"})

    return {
        "schema": "nwnht_first_player_causal_artifact_verification_v2",
        "source_rebuild": {"ends_accepted": source_manifest["ends_accepted"], "rows": len(expected_rows)},
        "transition_export": {
            "stored_rows": len(stored_rows),
            "unique_keys": len(stored_by_key),
            "expected_unique_keys": len(expected_by_key),
            "missing_or_changed_count": sum(
                1 for row_key, expected in expected_by_key.items()
                if row_key not in stored_by_key or any(not same(expected[field], stored_by_key[row_key].get(field)) for field in fields)
            ),
            "extra_key_count": len(set(stored_by_key) - set(expected_by_key)),
            "examples": transition_mismatches,
        },
        "effect_export": {
            "stored_rows": len(effect_rows),
            "unique_keys": len(effect_by_key),
            "extra_key_count": len(set(effect_by_key) - set(stored_by_key)),
            "source_transition_mismatch_count": sum(
                1
                for row_key, row in effect_by_key.items()
                if row_key not in stored_by_key or any(not same(stored_by_key[row_key].get(field), row.get(field)) for field in fields)
            ),
            "recomputed_effect_mismatch_count": sum(
                1 for row in effect_by_key.values()
                if not same(action_effect(list(row["s_before_own"]), list(row["u_after_own"])), row.get("observed_own_board_effect"))
            ),
            "independent_primary_contract_violation_count": sum(
                1 for row in effect_by_key.values() if _independent_primary_violation(row) is not None
            ),
            "examples": effect_mismatches,
            "source_transition_examples": effect_source_mismatches,
            "independent_primary_contract_examples": primary_contract_violations,
        },
        "audit_sample": {
            "rows": len(audit_rows),
            "unique_audit_keys": len(set(audit_keys)),
            "per_primary_effect": dict(sorted(Counter(str(row["primary_effect"]) for row in audit_rows).items())),
            "source_match_mismatch_count": sum(
                1
                for audit_row in audit_rows
                if (source := effect_by_key.get((int(audit_row["end_id"]), int(audit_row["own_throw_number"])))) is None
                or not same(_compact(source), audit_row)
            ),
            "examples": audit_mismatches,
        },
        "scope": "Checks source-to-export identity and deterministic taxonomy consistency. It cannot verify whether upstream CV stone coordinates match original imagery.",
    }


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=Path(__file__).resolve().parents[3] / "external_research" / "NWNHT_curling" / "curling-main" / "src" / "world_curling_ss.db")
    parser.add_argument("--match-types", default="Mens_Teams,Womens_Teams,Mixed_Teams")
    parser.add_argument("--transitions", type=Path, default=root / "nwnht_first_player_causal_transitions_v0.jsonl")
    parser.add_argument("--effects", type=Path, default=root / "nwnht_first_player_board_effects_v2.jsonl")
    parser.add_argument("--audit", type=Path, default=root / "nwnht_first_player_board_effect_manual_audit_v2.jsonl")
    parser.add_argument("--report", type=Path, default=root / "nwnht_first_player_causal_artifact_verification_v2.json")
    args = parser.parse_args()
    if args.report.exists():
        raise SystemExit(f"Refusing to overwrite {args.report}; choose a new path deliberately.")
    report = verify(
        database=args.database,
        match_types=tuple(item.strip() for item in args.match_types.split(",") if item.strip()),
        transitions_path=args.transitions,
        effects_path=args.effects,
        audit_path=args.audit,
    )
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"report": str(args.report), "transition_mismatches": report["transition_export"]["missing_or_changed_count"], "effect_mismatches": report["effect_export"]["recomputed_effect_mismatch_count"], "audit_mismatches": report["audit_sample"]["source_match_mismatch_count"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
