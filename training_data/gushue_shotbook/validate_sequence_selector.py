"""Small, non-destructive proof suite for the end-level blue-mark selector."""

from __future__ import annotations

import argparse
import csv
import tempfile
from pathlib import Path

from build_structured_shotbook import parse_end_page, source_page_text
from extract_stone_coordinates import extract_stone_candidates, mini_sheet_images, page_metadata
from select_live_stones import select_end_live_stones


ROOT = Path(__file__).parent


def select_page(pdf_name: str, local_page: int, source_book: str, source_page: int) -> tuple[list[list[dict[str, object]]], list[str], str, str]:
    with tempfile.TemporaryDirectory(prefix="gushue_selector_") as temporary:
        panels = mini_sheet_images(ROOT / "gushue_games" / pdf_name, Path(temporary))[local_page]
        end_number, red_team, yellow_team = page_metadata(ROOT / "extracted_text" / source_book, source_page)
        source_text = (ROOT / "extracted_text" / source_book).read_text(encoding="utf-8")
        _, calls = parse_end_page(source_page_text(source_text, source_page))
        candidates = [extract_stone_candidates(panel, red_team, yellow_team)[0] for panel in panels]
        throwing = [str(calls[index]["team"]) for index in range(1, len(panels) + 1)]
    return select_end_live_stones(candidates, throwing, red_team, yellow_team), throwing, red_team, yellow_team


def has_stone(state: list[dict[str, object]], team: str, x: float, y: float) -> bool:
    return any(
        stone["team"] == team and abs(float(stone["x_m"]) - x) < 0.02 and abs(float(stone["y_m"]) - y) < 0.02
        for stone in state
    )


def assert_transitions(states: list[list[dict[str, object]]], throwing: list[str], red_team: str, yellow_team: str) -> None:
    previous = {red_team: 0, yellow_team: 0}
    for shot, (state, team) in enumerate(zip(states, throwing), start=1):
        current = {red_team: sum(stone["team"] == red_team for stone in state), yellow_team: sum(stone["team"] == yellow_team for stone in state)}
        for colour_team in (red_team, yellow_team):
            if current[colour_team] > previous[colour_team] + int(colour_team == team):
                raise AssertionError(f"shot {shot}: {colour_team} rises {previous[colour_team]}→{current[colour_team]} while {team} throws")
        previous = current


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Read four varied games only; never writes coordinates.",
    )
    args = parser.parse_args()
    # Two independent real pages which broke the per-image blue rule.
    sui_states, sui_throwing, sui_red, sui_yellow = select_page(
        "wmcc_2022_11_vs_SUI_pages_728-736.pdf", 6, "WMCC2022_ResultsBook.txt", 733
    )
    assert_transitions(sui_states, sui_throwing, sui_red, sui_yellow)
    if not has_stone(sui_states[1], "CAN", 1.10, 1.97):
        raise AssertionError("CAN-SUI E6 S2 did not retain the known live blue-marked guard")

    swe_states, swe_throwing, swe_red, swe_yellow = select_page(
        "wmcc_2023_03_vs_SWE_pages_70-77.pdf", 3, "WMCC2023_ResultsBook.txt", 72
    )
    assert_transitions(swe_states, swe_throwing, swe_red, swe_yellow)
    if not has_stone(swe_states[0], "SWE", 0.13, 2.53):
        raise AssertionError("CAN-SWE E3 S1 did not retain the known live blue-marked guard")

    print("SEQUENCE_SELECTOR_FIXTURES_OK: two known live blue marks retained; every transition is legal")

    if not args.benchmark:
        return

    # A deliberately small but varied blind benchmark: normal early/mid/late
    # games across all three years, plus the two games containing the known
    # blue-mark fixtures.  This is a rule check only; no coordinate file is
    # created or touched.
    wanted = {
        (2022, 1), (2022, 2), (2022, 7), (2022, 11),
        (2023, 3), (2023, 14),
        (2024, 1), (2024, 7), (2024, 14),
    }
    game_rows = [
        row
        for row in csv.DictReader((ROOT / "gushue_game_index.csv").open(encoding="utf-8"))
        if (int(row["event_year"]), int(row["game_sequence_in_book"])) in wanted
    ]
    audited_pages = 0
    audited_states = 0
    selected_blue = 0
    for game in game_rows:
        source_book = Path(game["source_book"]).stem + ".txt"
        source_start = int(game["source_page_start"])
        with tempfile.TemporaryDirectory(prefix="gushue_selector_benchmark_") as temporary:
            panels_by_page = mini_sheet_images(ROOT / game["gushue_game_pdf"], Path(temporary))
            for local_page, panels in sorted(panels_by_page.items()):
                source_page = source_start + local_page - 1
                end_number, red_team, yellow_team = page_metadata(ROOT / "extracted_text" / source_book, source_page)
                source_text = (ROOT / "extracted_text" / source_book).read_text(encoding="utf-8")
                _, calls = parse_end_page(source_page_text(source_text, source_page))
                candidates = [extract_stone_candidates(panel, red_team, yellow_team)[0] for panel in panels]
                throwing = [str(calls[index]["team"]) for index in range(1, len(panels) + 1)]
                states = select_end_live_stones(candidates, throwing, red_team, yellow_team)
                assert_transitions(states, throwing, red_team, yellow_team)
                audited_pages += 1
                audited_states += len(states)
                selected_blue += sum(
                    bool(stone["has_royal_blue_mark"])
                    for state in states
                    for stone in state
                )
    print(
        f"SEQUENCE_SELECTOR_BENCHMARK_OK: games={len(game_rows)} pages={audited_pages} "
        f"states={audited_states} selected_blue_candidates={selected_blue}"
    )


if __name__ == "__main__":
    main()
