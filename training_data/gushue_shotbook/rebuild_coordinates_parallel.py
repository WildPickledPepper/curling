"""Safely rebuild shot-chart coordinates in parallel.

Unlike the original extractor, this recovery tool never overwrites the active
coordinate file unless an explicit --replace-active flag is passed *after* a
separate output has been inspected and validated.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import tempfile
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from build_structured_shotbook import parse_end_page, source_page_text
from extract_stone_coordinates import extract_stone_candidates, mini_sheet_images, page_metadata
from select_live_stones import select_end_live_stones


def process_game(args: tuple[str, dict[str, str]]) -> tuple[list[dict[str, object]], dict[str, int], list[dict[str, object]]]:
    root_text, game = args
    root = Path(root_text)
    game_pdf = root / game["gushue_game_pdf"]
    source_text = root / "extracted_text" / (Path(game["source_book"]).stem + ".txt")
    source_book_text = source_text.read_text(encoding="utf-8")
    records: list[dict[str, object]] = []
    audit: Counter[str] = Counter(games=1)
    review: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="gushue_parallel_") as temporary:
        panels_by_page = mini_sheet_images(game_pdf, Path(temporary))
        for local_page, panels in sorted(panels_by_page.items()):
            source_page = int(game["source_page_start"]) + local_page - 1
            end_number, red_team, yellow_team = page_metadata(source_text, source_page)
            _, calls = parse_end_page(source_page_text(source_book_text, source_page))
            candidate_states: list[list[dict[str, object]]] = []
            house_position = ""
            rotation_degrees = 0
            for panel in panels:
                candidates, house_position, rotation_degrees = extract_stone_candidates(panel, red_team, yellow_team)
                candidate_states.append(candidates)
            throwing_teams = [str(calls[shot]["team"]) for shot in range(1, len(panels) + 1)]
            try:
                selected_states = select_end_live_stones(candidate_states, throwing_teams, red_team, yellow_team)
            except ValueError as error:
                # Fail closed: do not write an ambiguous end as if it were
                # authoritative.  The report names it for targeted repair.
                audit["selection_errors"] += 1
                review.append(
                    {
                        "gushue_game_pdf": game["gushue_game_pdf"],
                        "end_number": end_number,
                        "reason": str(error),
                        "status": "not_exported",
                    }
                )
                continue
            audit["chart_pages"] += 1
            previous_by_team = {red_team: 0, yellow_team: 0}
            for shot_in_end, stones in enumerate(selected_states, start=1):
                throwing_team = throwing_teams[shot_in_end - 1]
                current_by_team = {
                    red_team: sum(stone["team"] == red_team for stone in stones),
                    yellow_team: sum(stone["team"] == yellow_team for stone in stones),
                }
                transition_invalid = any(
                    current_by_team[team] > previous_by_team[team] + int(team == throwing_team)
                    for team in (red_team, yellow_team)
                )
                if transition_invalid:
                    review.append(
                        {
                            "gushue_game_pdf": game["gushue_game_pdf"],
                            "end_number": end_number,
                            "shot_in_end": shot_in_end,
                            "previous_counts": previous_by_team,
                            "current_counts": current_by_team,
                            "throwing_team": throwing_team,
                            "reason": "selector emitted an illegal team-count transition",
                        }
                    )
                previous_by_team = current_by_team
                audit["states"] += 1
                audit["stones"] += len(stones)
                audit["selected_blue_candidates"] += sum(bool(stone["has_royal_blue_mark"]) for stone in stones)
                audit["count_delta_anomalies"] += int(transition_invalid)
                records.append(
                    {
                        "event_year": int(game["event_year"]),
                        "game_sequence_in_book": int(game["game_sequence_in_book"]),
                        "phase": game["phase"],
                        "opponent_code": game["opponent_code"],
                        "end_number": end_number,
                        "shot_in_end": shot_in_end,
                        "source_book": game["source_book"],
                        "source_page": source_page,
                        "gushue_game_pdf": game["gushue_game_pdf"],
                        "local_pdf_page": local_page,
                        "red_team": red_team,
                        "yellow_team": yellow_team,
                        "coordinate_system": "button_origin_m; +x=canonical_chart_right; +y=toward_hog_line",
                        "source_house_position": house_position,
                        "rotation_degrees_to_canonical": rotation_degrees,
                        "quality_status": "needs_manual_review" if transition_invalid else "auto_pass",
                        "stones": stones,
                    }
                )
    return records, dict(audit), review


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).parent)
    parser.add_argument("--workers", type=int, default=min(8, os.cpu_count() or 1))
    parser.add_argument("--limit-games", type=int, default=0)
    parser.add_argument("--output", type=Path, default=None, help="Defaults to coordinates/recovery_sequence_candidate.jsonl")
    args = parser.parse_args()
    root = args.root.resolve()
    rows = list(csv.DictReader((root / "gushue_game_index.csv").open(encoding="utf-8")))
    if args.limit_games:
        rows = rows[: args.limit_games]
    output = args.output or root / "coordinates" / "recovery_sequence_candidate.jsonl"
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    all_records: list[dict[str, object]] = []
    audit: Counter[str] = Counter()
    review: list[dict[str, object]] = []
    with ProcessPoolExecutor(max_workers=max(1, min(args.workers, len(rows)))) as pool:
        for records, game_audit, game_review in pool.map(process_game, [(str(root), row) for row in rows]):
            all_records.extend(records)
            audit.update(game_audit)
            review.extend(game_review)
    all_records.sort(key=lambda record: (int(record["event_year"]), int(record["game_sequence_in_book"]), int(record["end_number"]), int(record["shot_in_end"])))

    temporary_output = output.with_suffix(output.suffix + ".tmp")
    with temporary_output.open("w", encoding="utf-8") as handle:
        for record in all_records:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    temporary_output.replace(output)
    report = {
        "output": str(output),
        "games": audit["games"],
        "states": audit["states"],
        "stones": audit["stones"],
        "count_delta_anomalies": audit["count_delta_anomalies"],
        "selected_blue_candidates": audit["selected_blue_candidates"],
        "selection_errors": audit["selection_errors"],
        "workers": args.workers,
        "review_states": review,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
