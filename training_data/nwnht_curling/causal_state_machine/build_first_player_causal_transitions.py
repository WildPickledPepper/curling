#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Export auditable first-player causal transition panels from NWNHT.

Each accepted end supplies eight rows with the actual sequence of board
snapshots, always from the first thrower's perspective:

    S_k (frame 2k-2) -> own action -> U_k (frame 2k-1)
        -> opponent reply -> S_(k+1) (frame 2k)

This is a data-quality and causal-data preparation step only.  It does not
cluster actions, estimate effects, generate target regions, or run PhysX.
The source SQLite database is opened read-only and existing outputs are never
overwritten.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from collections import Counter, defaultdict
from dataclasses import asdict
from pathlib import Path
from typing import Any, Iterable

try:
    from ..discover_state_graph import (
        DEFAULT_DB,
        DEFAULT_MATCH_TYPES,
        EndRecord,
        Frame,
        _iter_end_records,
        infer_colour_owners,
        normalize_action,
    )
except ImportError:  # pragma: no cover - direct script invocation
    NWNHT_ROOT = Path(__file__).resolve().parents[1]
    if str(NWNHT_ROOT) not in sys.path:
        sys.path.insert(0, str(NWNHT_ROOT))
    from discover_state_graph import (  # type: ignore
        DEFAULT_DB,
        DEFAULT_MATCH_TYPES,
        EndRecord,
        Frame,
        _iter_end_records,
        infer_colour_owners,
        normalize_action,
    )


SCHEMA = "nwnht_first_player_causal_transition_row_v0"


def _board(frame: Frame, owners: dict[str, str], first_team: str) -> list[dict[str, str | float]]:
    """Return one detected board in stable order, preserving upstream colour."""

    rows = [
        {
            "owner": "first" if owners[colour] == first_team else "opponent",
            "colour": colour,
            "x_m": float(x),
            "y_m": float(y),
        }
        for colour, x, y in frame.stones
        if colour in owners
    ]
    return sorted(rows, key=lambda row: (str(row["owner"]), str(row["colour"]), float(row["x_m"]), float(row["y_m"])))


def _end_labels(record: EndRecord, first_team: str, opponent_team: str) -> dict[str, Any]:
    first_points = int(record.score_after[first_team]) - int(record.score_before[first_team])
    opponent_points = int(record.score_after[opponent_team]) - int(record.score_before[opponent_team])
    margin = first_points - opponent_points
    return {
        "first_end_points": first_points,
        "opponent_end_points": opponent_points,
        "first_end_margin": margin,
        "end_result": "FIRST_SCORES" if margin > 0 else "OPPONENT_SCORES" if margin < 0 else "BLANK",
    }


def validate_record(record: EndRecord) -> tuple[str | None, str | None, str | None, dict[str, str] | None]:
    """Validate one end without silently repairing missing/ambiguous evidence."""

    if set(record.frames) != set(range(17)):
        return "missing_frame_0_to_16", None, None, None
    if any(record.frames[shot].throwing_team is None for shot in range(1, 17)):
        return "missing_throwing_team", None, None, None
    first_team = record.frames[1].throwing_team
    opponent_team = record.frames[2].throwing_team
    if first_team is None or opponent_team is None or first_team == opponent_team:
        return "invalid_first_opponent_identity", None, None, None
    if any(record.frames[shot].throwing_team != (first_team if shot % 2 else opponent_team) for shot in range(1, 17)):
        return "non_alternating_throw_order", None, None, None
    owners = infer_colour_owners(record.frames, record.teams)
    if owners is None:
        return "ambiguous_colour_owner_mapping", None, None, None
    return None, first_team, opponent_team, owners


def rows_from_record(record: EndRecord, context: MappingLike | None = None) -> tuple[list[dict[str, Any]] | None, str | None]:
    """Create exactly eight rows for one validated end, or return a reject reason."""

    reason, first_team, opponent_team, owners = validate_record(record)
    if reason is not None:
        return None, reason
    assert first_team is not None and opponent_team is not None and owners is not None
    labels = _end_labels(record, first_team, opponent_team)
    context = context or {}
    rows: list[dict[str, Any]] = []
    for own_throw_number in range(1, 9):
        own_shot = own_throw_number * 2 - 1
        reply_shot = own_shot + 1
        before = _board(record.frames[own_shot - 1], owners, first_team)
        after_own = _board(record.frames[own_shot], owners, first_team)
        after_reply = _board(record.frames[reply_shot], owners, first_team)
        rows.append(
            {
                "schema": SCHEMA,
                "match_id": record.match_id,
                "end_id": record.end_id,
                "end_number": record.end_number,
                "match_type": record.match_type,
                "first_team": first_team,
                "opponent_team": opponent_team,
                # Context is intentionally unavailable to runtime policy.  It is
                # retained only for later propensity/sensitivity analyses.
                "offline_context": dict(context),
                "own_throw_number": own_throw_number,
                "own_global_shot_number": own_shot,
                "opponent_global_shot_number": reply_shot,
                "source_frames": {
                    "before_own": own_shot - 1,
                    "after_own": own_shot,
                    "after_opponent_reply": reply_shot,
                },
                "s_before_own": before,
                "observed_own_delivery": {
                    "called_shot": normalize_action(record.frames[own_shot].call),
                    "upstream_called_shot": record.frames[own_shot].call,
                    "rating": record.frames[own_shot].rating,
                },
                "u_after_own": after_own,
                "observed_opponent_reply": {
                    "called_shot": normalize_action(record.frames[reply_shot].call),
                    "upstream_called_shot": record.frames[reply_shot].call,
                    "rating": record.frames[reply_shot].rating,
                },
                "s_after_opponent_reply": after_reply,
                # End labels are never state features.  Game score/result is
                # deliberately excluded from this causal panel.
                "terminal_end_label": labels,
            }
        )
    return rows, None


# Kept as an alias rather than importing typing.Mapping at runtime in every
# row construction; dict-like metadata is sufficient for this exporter.
MappingLike = dict[str, Any]


def _match_context(connection: sqlite3.Connection, match_types: tuple[str, ...]) -> dict[int, dict[str, str | None]]:
    placeholders = ",".join("?" for _ in match_types)
    rows = connection.execute(
        f"""
        SELECT m.match_id,ev.name,ev.start_date
        FROM Match m LEFT JOIN Event ev ON ev.event_id=m.event_id
        WHERE m.type IN ({placeholders})
        """,
        match_types,
    )
    return {
        int(match_id): {"event_name": None if name is None else str(name), "event_start_date": None if date is None else str(date)}
        for match_id, name, date in rows
    }


def build_rows(database: Path, match_types: tuple[str, ...]) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    connection = sqlite3.connect(f"file:{database.resolve().as_posix()}?mode=ro", uri=True)
    accepted = examined = 0
    rejected: Counter[str] = Counter()
    rows: list[dict[str, Any]] = []
    per_k: dict[int, Counter[str]] = defaultdict(Counter)
    audit_end_ids: list[int] = []
    try:
        contexts = _match_context(connection, match_types)
        for record in _iter_end_records(connection, match_types):
            examined += 1
            end_rows, reason = rows_from_record(record, contexts.get(record.match_id))
            if end_rows is None:
                rejected[str(reason)] += 1
                continue
            accepted += 1
            rows.extend(end_rows)
            audit_end_ids.append(record.end_id)
            for row in end_rows:
                k = int(row["own_throw_number"])
                per_k[k]["rows"] += 1
                if row["observed_own_delivery"]["upstream_called_shot"] is None:
                    per_k[k]["missing_own_call"] += 1
                if row["observed_opponent_reply"]["upstream_called_shot"] is None:
                    per_k[k]["missing_reply_call"] += 1
    finally:
        connection.close()

    # Deterministic evenly-spaced IDs form the manual review set.  They are
    # recorded rather than copied, keeping this export compact and traceable.
    sample_count = min(50, len(audit_end_ids))
    audit_sample_end_ids = [] if sample_count == 0 else [
        audit_end_ids[round(index * (len(audit_end_ids) - 1) / max(sample_count - 1, 1))]
        for index in range(sample_count)
    ]
    manifest = {
        "schema": "nwnht_first_player_causal_transition_manifest_v0",
        "source": {"database": str(database), "match_types": list(match_types)},
        "definition": "One accepted end emits K1..K8 rows: S(frame 2K-2) -> own U(frame 2K-1) -> opponent-reply S'(frame 2K).",
        "runtime_state_boundary": "Only own_throw_number and board snapshots may become runtime state. Offline context and terminal labels are not runtime features.",
        "ends_examined": examined,
        "ends_accepted": accepted,
        "ends_rejected": int(sum(rejected.values())),
        "row_count": len(rows),
        "rejection_reasons": dict(sorted(rejected.items())),
        "manual_audit_end_ids": audit_sample_end_ids,
        "no_overwrite_policy": "Exporter refuses to overwrite any output path.",
    }
    quality = {
        "schema": "nwnht_first_player_causal_transition_quality_v0",
        "accepted_chain_checks": {
            "eight_rows_per_accepted_end": len(rows) == accepted * 8,
            "source_frame_pattern": "Each row records consecutive source frames (2K-2, 2K-1, 2K); U is the same physical snapshot observed before the opponent delivery.",
            "strict_acceptance": ["frames 0..16 present", "alternating throw teams", "unambiguous colour-owner mapping"],
        },
        "per_own_throw": {str(k): dict(counts) for k, counts in sorted(per_k.items())},
        "warning": "Detected stone positions are upstream computer-vision observations. This report establishes snapshot continuity, not stone-tracking accuracy or causal validity.",
    }
    return rows, manifest, quality


def _write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parent / "artifacts"
    parser.add_argument("--database", type=Path, default=DEFAULT_DB)
    parser.add_argument("--match-types", default=",".join(DEFAULT_MATCH_TYPES))
    parser.add_argument("--output", type=Path, default=root / "nwnht_first_player_causal_transitions_v0.jsonl")
    parser.add_argument("--manifest", type=Path, default=root / "nwnht_first_player_causal_transitions_v0_manifest.json")
    parser.add_argument("--quality-report", type=Path, default=root / "nwnht_first_player_causal_transitions_v0_quality.json")
    args = parser.parse_args()
    for path in (args.output, args.manifest, args.quality_report):
        if path.exists():
            raise SystemExit(f"Refusing to overwrite {path}; choose a new path deliberately.")
    match_types = tuple(item.strip() for item in args.match_types.split(",") if item.strip())
    rows, manifest, quality = build_rows(args.database, match_types)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    _write_jsonl(args.output, rows)
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    args.quality_report.write_text(json.dumps(quality, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "manifest": str(args.manifest), "quality_report": str(args.quality_report), "rows": len(rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
