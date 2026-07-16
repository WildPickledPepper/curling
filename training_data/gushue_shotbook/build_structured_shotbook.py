"""Build a PDF-free, per-shot curling state table from extracted CurlIT data.

The source PDFs are only needed once, when this script is run.  Consumers of
the strategy tree read the resulting JSONL tables instead of scraping or
opening a Results Book again.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


HOUSE_RADIUS_M = 1.8288
# A conceded end can finish after any throw, so its final header can have one,
# two, three, four, or the usual six columns.
SHOT_HEADER = re.compile(r"^\s*\d+(?:\s+\d+)*\s*$")
SHOT_NUMBER = re.compile(r"\d+")
TEAM_NAME = re.compile(r"(?P<team>[A-Z]{3}):\s*(?P<player>[A-Za-zÀ-ÖØ-öø-ÿ'\-]+\s+[A-Z])")
SCORE = re.compile(
    r"End\s+(?P<end>\d+)\s+"
    r"(?P<left_team>[A-Z]{3})\s+-\s+[^\d]+?"
    r"(?P<left_before>\d+|X)\s+\+\s+(?P<left_end>\d+|X)\s+\(this end\)\s+=\s+(?P<left_total>\d+|X)\s+"
    r"(?P<right_team>[A-Z]{3})\s+-\s+[^\d]+?"
    r"(?P<right_before>\d+|X)\s+\+\s+(?P<right_end>\d+|X)\s+\(this end\)\s+=\s+(?P<right_total>\d+|X)",
)
SUCCESS = re.compile(r"(?P<pct>\d+)%\s*$")


def source_page_text(book_text: str, page_number: int) -> str:
    pages = book_text.split("\f")
    if not 1 <= page_number <= len(pages):
        raise IndexError(f"Source page {page_number} is outside book with {len(pages)} pages")
    return pages[page_number - 1]


def columns(line: str, starts: list[int]) -> list[str]:
    return [line[start : starts[index + 1] if index + 1 < len(starts) else None].strip() for index, start in enumerate(starts)]


def parse_end_page(text: str) -> tuple[dict[str, object], dict[int, dict[str, object]]]:
    """Parse score and all call metadata on one official game-chart page."""
    score_match = SCORE.search(text)
    if not score_match:
        raise ValueError("Could not parse end score line")
    score = score_match.groupdict()
    def score_value(value: str) -> int | None:
        return int(value) if value.isdigit() else None

    summary: dict[str, object] = {
        "end_number": int(score["end"]),
        "teams": [score["left_team"], score["right_team"]],
        "score_before": {score["left_team"]: score_value(score["left_before"]), score["right_team"]: score_value(score["right_before"])},
        "points_this_end": {score["left_team"]: score_value(score["left_end"]), score["right_team"]: score_value(score["right_end"])},
        "score_after": {score["left_team"]: score_value(score["left_total"]), score["right_team"]: score_value(score["right_total"])},
        "official_end_unfinished": "X" in (
            score["left_before"], score["left_end"], score["left_total"], score["right_before"], score["right_end"], score["right_total"]
        ),
    }

    lines = text.splitlines()
    calls: dict[int, dict[str, object]] = {}
    for line_index, line in enumerate(lines):
        if not SHOT_HEADER.match(line):
            continue
        number_matches = list(SHOT_NUMBER.finditer(line))
        shot_numbers = [int(match.group()) for match in number_matches]
        if not shot_numbers or any(number < 1 or number > 16 for number in shot_numbers):
            continue
        starts = [match.start() for match in number_matches]
        # The next two non-blank lines respectively contain player/team and
        # official call/result.  Keeping this layout-based parsing means that
        # multi-word calls such as "Promotion Take-out" stay intact.
        following = [candidate for candidate in lines[line_index + 1 : line_index + 10] if candidate.strip()]
        name_line = next((candidate for candidate in following if TEAM_NAME.search(candidate)), None)
        if name_line is None:
            continue
        name_position = lines.index(name_line, line_index + 1)
        action_line = next((candidate for candidate in lines[name_position + 1 : name_position + 4] if "↺" in candidate or "↻" in candidate), None)
        if action_line is None:
            raise ValueError(f"Could not find action line for shots {shot_numbers}")

        for shot, name_cell, action_cell in zip(shot_numbers, columns(name_line, starts), columns(action_line, starts)):
            name_match = TEAM_NAME.search(name_cell)
            if not name_match:
                raise ValueError(f"Could not parse player for shot {shot}: {name_cell!r}")
            if "↺" in action_cell:
                call_name, direction = action_cell.split("↺", 1)
                rotation = "counterclockwise"
            elif "↻" in action_cell:
                call_name, direction = action_cell.split("↻", 1)
                rotation = "clockwise"
            else:
                # A few official records use only "-" (not considered) for
                # a shot, without printing a rotation glyph.  It is still a
                # valid call record; absence must not make the whole end
                # disappear from the training corpus.
                call_name, direction, rotation = action_cell.replace("-", " "), "", None
            success_match = SUCCESS.search(direction)
            calls[shot] = {
                "team": name_match["team"],
                "player": name_match["player"],
                "official_call": call_name.strip(),
                "rotation": rotation,
                "official_completion_percent": int(success_match["pct"]) if success_match else None,
                "official_completion_not_considered": bool(re.search(r"\s-\s*$", action_cell)),
            }
    if not calls or sorted(calls) != list(range(1, max(calls) + 1)):
        raise ValueError(f"Parsed non-contiguous official calls: {sorted(calls)}")
    return summary, calls


def stone_features(stones: list[dict[str, object]]) -> list[dict[str, object]]:
    featured: list[dict[str, object]] = []
    for stone in stones:
        x, y = float(stone["x_m"]), float(stone["y_m"])
        radius = (x * x + y * y) ** 0.5
        featured.append(
            {
                "team": stone["team"],
                "x_m": x,
                "y_m": y,
                "distance_to_button_m": round(radius, 4),
                "in_house": radius <= HOUSE_RADIUS_M,
                "side": "right" if x > 0.08 else "left" if x < -0.08 else "centre",
                "depth": "front" if y > 0.15 else "back" if y < -0.15 else "button_line",
            }
        )
    return featured


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).parent)
    args = parser.parse_args()
    root = args.root.resolve()
    coordinate_path = root / "coordinates" / "gushue_stone_states.jsonl"
    coordinates = [json.loads(line) for line in coordinate_path.open(encoding="utf-8")]
    by_page = {(row["source_book"], int(row["source_page"])): [] for row in coordinates}
    for row in coordinates:
        by_page[(row["source_book"], int(row["source_page"]))].append(row)

    parsed_pages: dict[tuple[str, int], tuple[dict[str, object], dict[int, dict[str, object]]]] = {}
    for source_book, source_page in by_page:
        text_file = root / "extracted_text" / (Path(source_book).stem + ".txt")
        parsed_pages[(source_book, source_page)] = parse_end_page(source_page_text(text_file.read_text(encoding="utf-8"), source_page))

    shot_rows: list[dict[str, object]] = []
    end_rows: list[dict[str, object]] = []
    for key, state_rows in by_page.items():
        summary, calls = parsed_pages[key]
        state_rows.sort(key=lambda row: int(row["shot_in_end"]))
        # A conceded end may stop before shot 16.  Hammer means the team that
        # *would* throw #16, not simply the team that happened to throw last.
        # Official ends alternate teams, therefore it is the other team from
        # shot #1 whenever a literal #16 record is absent.
        hammer_team = calls[16]["team"] if 16 in calls else next(team for team in summary["teams"] if team != calls[1]["team"])
        end_rows.append(
            {
                **summary,
                "event_year": state_rows[0]["event_year"],
                "game_sequence_in_book": state_rows[0]["game_sequence_in_book"],
                "opponent_code": state_rows[0]["opponent_code"],
                "phase": state_rows[0]["phase"],
                "gushue_game_pdf": state_rows[0]["gushue_game_pdf"],
                "hammer_team": hammer_team,
                "last_recorded_shot_in_end": int(state_rows[-1]["shot_in_end"]),
                "ended_before_sixteen_shots": int(state_rows[-1]["shot_in_end"]) < 16,
            }
        )
        previous_counts: Counter[str] = Counter()
        for state in state_rows:
            shot = int(state["shot_in_end"])
            if shot not in calls:
                raise ValueError(f"No official call parsed for source {key}, shot {shot}")
            call = calls[shot]
            stones = stone_features(state["stones"])
            current_counts = Counter(str(stone["team"]) for stone in stones)
            team = str(call["team"])
            other_team = next(candidate for candidate in summary["teams"] if candidate != team)
            shot_rows.append(
                {
                    "event_year": state["event_year"],
                    "game_sequence_in_book": state["game_sequence_in_book"],
                    "phase": state["phase"],
                    "opponent_code": state["opponent_code"],
                    "end_number": state["end_number"],
                    "shot_in_end": shot,
                    "throwing_team": team,
                    "throwing_player": call["player"],
                    "hammer_team": hammer_team,
                    "has_hammer": team == hammer_team,
                    "official_call": call["official_call"],
                    "rotation": call["rotation"],
                    "official_completion_percent": call["official_completion_percent"],
                    "official_completion_not_considered": call["official_completion_not_considered"],
                    "end_score_before": summary["score_before"],
                    "points_this_end": summary["points_this_end"],
                    "end_score_after": summary["score_after"],
                    "post_shot_stones": stones,
                    "post_shot_stone_count_by_team": {candidate: current_counts[candidate] for candidate in summary["teams"]},
                    "net_stone_count_change_by_team": {candidate: current_counts[candidate] - previous_counts[candidate] for candidate in summary["teams"]},
                    "coordinate_quality_status": state["quality_status"],
                    "source_id": {"book": state["source_book"], "page": state["source_page"], "game_pdf": state["gushue_game_pdf"]},
                }
            )
            previous_counts = current_counts

    # Link every end to the hammer actually observed in the next end.  This is
    # more useful for a state machine than re-deriving the rule from score each
    # time, and also handles blank/conceded ends explicitly.
    end_rows.sort(key=lambda row: (int(row["event_year"]), int(row["game_sequence_in_book"]), int(row["end_number"])))
    ends_by_game: dict[tuple[int, int], list[dict[str, object]]] = defaultdict(list)
    for row in end_rows:
        ends_by_game[(int(row["event_year"]), int(row["game_sequence_in_book"]))].append(row)
    game_rows: list[dict[str, object]] = []
    for (event_year, sequence), game_ends in ends_by_game.items():
        for index, end in enumerate(game_ends):
            end["actual_next_end_hammer_team"] = game_ends[index + 1]["hammer_team"] if index + 1 < len(game_ends) else None
        completed = [end for end in game_ends if not end["official_end_unfinished"]]
        final = completed[-1] if completed else game_ends[-1]
        final_score = final["score_after"]
        teams = final["teams"]
        left, right = str(teams[0]), str(teams[1])
        if final_score[left] is None or final_score[right] is None:
            winner = None
        elif final_score[left] == final_score[right]:
            winner = "tie"
        else:
            winner = left if final_score[left] > final_score[right] else right
        game_rows.append(
            {
                "event_year": event_year,
                "game_sequence_in_book": sequence,
                "phase": final["phase"],
                "opponent_code": final["opponent_code"],
                "gushue_game_pdf": final["gushue_game_pdf"],
                "teams": teams,
                "final_score": final_score,
                "winner": winner,
                "ends_recorded": len(game_ends),
                "ends": [
                    {
                        "end_number": end["end_number"],
                        "hammer_team": end["hammer_team"],
                        "points_this_end": end["points_this_end"],
                        "score_after": end["score_after"],
                        "ended_before_sixteen_shots": end["ended_before_sixteen_shots"],
                    }
                    for end in game_ends
                ],
            }
        )

    output_dir = root / "coordinates"
    output_dir.mkdir(exist_ok=True)
    shot_output = output_dir / "gushue_structured_shots.jsonl"
    end_output = output_dir / "gushue_structured_ends.jsonl"
    game_output = output_dir / "gushue_structured_games.jsonl"
    with shot_output.open("w", encoding="utf-8") as handle:
        for row in shot_rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    with end_output.open("w", encoding="utf-8") as handle:
        for row in end_rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    with game_output.open("w", encoding="utf-8") as handle:
        for row in game_rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "shots": len(shot_rows),
                "ends": len(end_rows),
                "games": len(game_rows),
                "shot_output": str(shot_output),
                "end_output": str(end_output),
                "game_output": str(game_output),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
