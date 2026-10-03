"""Export the bundled NWNHT/CURLIT public SQLite database as JSONL states.

This is intentionally a *source adapter*, not a conversion to the local
simulator coordinate system.  NWNHT's 2016--2019 database is an independent,
automatically parsed historical corpus.  Keeping its native axes, physical
stone colours, and parser-quality label prevents it being silently mixed with
the separately extracted Gushue 2022--2024 corpus.

The source archive is expected at::

    DCCourse/external_research/NWNHT_curling/curling-main/src/world_curling_ss.db

It contains match metadata, every end, every frame, the reported call/rating,
and all detected stones.  It never writes to that SQLite file.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterator


ROOT = Path(__file__).resolve().parent
DEFAULT_DATABASE = (
    ROOT.parents[1]
    / "external_research"
    / "NWNHT_curling"
    / "curling-main"
    / "src"
    / "world_curling_ss.db"
)


def database_connection(path: Path) -> sqlite3.Connection:
    """Open the third-party database in SQLite's read-only mode."""
    if not path.is_file():
        raise FileNotFoundError(
            f"NWNHT database not found: {path}. Extract "
            "DCCourse/archive/third_party_and_model_snapshots/curling-main.zip under "
            "DCCourse/external_research/NWNHT_curling first."
        )
    connection = sqlite3.connect(f"file:{path.resolve().as_posix()}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def position_rows(
    connection: sqlite3.Connection,
    limit_matches: int,
    match_type: str | None,
    team: str | None,
    include_initial_frame: bool,
) -> Iterator[sqlite3.Row]:
    """Yield one Position row per recorded post-throw state, in game order."""
    match_conditions: list[str] = []
    params: list[object] = []
    if match_type:
        match_conditions.append("type = ?")
        params.append(match_type)
    if team:
        match_conditions.append("(team_1 = ? OR team_2 = ?)")
        params.extend((team, team))
    selected_matches = "SELECT match_id FROM Match"
    if match_conditions:
        selected_matches += " WHERE " + " AND ".join(match_conditions)
    selected_matches += " ORDER BY match_id"
    if limit_matches:
        selected_matches += " LIMIT ?"
        params.append(limit_matches)
    frame_filter = "p.frame_num BETWEEN 1 AND 16" if not include_initial_frame else "p.frame_num BETWEEN 0 AND 16"
    query = f"""
        SELECT
            m.match_id, m.start_time, m.type AS match_type, m.sheet,
            m.team_1, m.team_1_final_score, m.team_2, m.team_2_final_score,
            ev.event_id, ev.name AS event_name, ev.abbrev AS event_code,
            ev.start_date AS event_start_date, ev.end_date AS event_end_date,
            e.end_id, e.num AS end_number, e.hammer_colour, e.direction,
            p.position_id, p.frame_num,
            t.colour AS throw_colour, t.type AS called_shot, t.rating AS shot_rating,
            pl.name AS player_name, pl.team AS player_team,
            s.colour AS stone_colour, s.x AS stone_x_m, s.y AS stone_y_m,
            s.size AS source_contour_size
        FROM Position p
        JOIN End e ON e.end_id = p.end_id
        JOIN Match m ON m.match_id = e.match_id
        JOIN Event ev ON ev.event_id = m.event_id
        LEFT JOIN Throw t ON t.end_id = e.end_id AND t.throw_num = p.frame_num
        LEFT JOIN Player pl ON pl.player_id = t.player_id
        LEFT JOIN Stone s ON s.position_id = p.position_id
        WHERE m.match_id IN ({selected_matches})
          AND {frame_filter}
        ORDER BY m.match_id, e.num, p.frame_num, s.stone_id
    """
    yield from connection.execute(query, tuple(params))


def records(
    connection: sqlite3.Connection,
    limit_matches: int,
    match_type: str | None,
    team: str | None,
    include_initial_frame: bool,
) -> Iterator[dict[str, object]]:
    """Group one-to-many SQL rows into one JSON object per end/frame."""
    current_id: int | None = None
    current: dict[str, object] | None = None
    stones: list[dict[str, object]] = []
    for row in position_rows(connection, limit_matches, match_type, team, include_initial_frame):
        position_id = int(row["position_id"])
        if position_id != current_id:
            if current is not None:
                current["stones"] = stones
                yield current
            current_id = position_id
            stones = []
            current = {
                "source": "NWNHT/curling public SQLite database",
                "source_quality": "upstream_auto_parsed_not_ground_truth",
                "coordinate_system": "nwnht_native_normalized_m; button_origin; axis convention retained from upstream",
                "match_id": int(row["match_id"]),
                "event": {
                    "id": int(row["event_id"]),
                    "name": row["event_name"],
                    "code": row["event_code"],
                    "start_date": row["event_start_date"],
                    "end_date": row["event_end_date"],
                },
                "match": {
                    "start_time": row["start_time"],
                    "type": row["match_type"],
                    "sheet": row["sheet"],
                    "team_1": row["team_1"],
                    "team_2": row["team_2"],
                    "final_score": {row["team_1"]: row["team_1_final_score"], row["team_2"]: row["team_2_final_score"]},
                },
                "end_number": int(row["end_number"]),
                "shot_in_end": int(row["frame_num"]),
                "hammer_colour": row["hammer_colour"],
                "upstream_direction": row["direction"],
                "throw": {
                    "physical_colour": row["throw_colour"],
                    "team": row["player_team"],
                    "called_shot": row["called_shot"],
                    "rating": row["shot_rating"],
                    "player": row["player_name"],
                },
                # The throwing player's team lets consumers build the colour
                # map within an end.  Do not infer a missing mapping from
                # score order, because physical colours can switch by end.
                "stone_team_mapping": "derive per end from throw.physical_colour and throw.team",
            }
        if row["stone_colour"] is not None:
            stones.append(
                {
                    "physical_colour": row["stone_colour"],
                    "x_m": round(float(row["stone_x_m"]), 6),
                    "y_m": round(float(row["stone_y_m"]), 6),
                    "source_contour_size": int(row["source_contour_size"]),
                }
            )
    if current is not None:
        current["stones"] = stones
        yield current


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "coordinates" / "nwnht_public_states.jsonl",
    )
    parser.add_argument("--limit-matches", type=int, default=0, help="For a fast smoke test; 0 exports every match.")
    parser.add_argument("--match-type", help="Exact upstream match type, e.g. Mens_Teams.")
    parser.add_argument("--team", help="Three-letter upstream team code, e.g. CAN.")
    parser.add_argument(
        "--include-initial-frame",
        action="store_true",
        help="Also export upstream frame 0; default is only post-shot frames 1..16.",
    )
    parser.add_argument("--overwrite", action="store_true", help="Required when --output already exists.")
    args = parser.parse_args()
    if args.limit_matches < 0:
        raise SystemExit("--limit-matches must be zero or positive")
    if args.output.exists() and not args.overwrite:
        raise SystemExit(f"Refusing to overwrite {args.output}; pass --overwrite explicitly.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    audit: Counter[str] = Counter()
    match_ids: set[int] = set()
    with database_connection(args.database) as connection, args.output.open("w", encoding="utf-8") as stream:
        for record in records(
            connection,
            args.limit_matches,
            args.match_type,
            args.team,
            args.include_initial_frame,
        ):
            stream.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
            audit["states"] += 1
            audit["stones"] += len(record["stones"])
            match_ids.add(int(record["match_id"]))
    print(
        json.dumps(
            {
                "output": str(args.output),
                "states": audit["states"],
                "stones": audit["stones"],
                "matches": len(match_ids),
                "source_database": str(args.database),
                "note": "Coordinates retain NWNHT native normalization; this is an independent auto-parsed historical corpus.",
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
