"""Fast, deterministic regression tests for coordinate-extraction rules.

These are intentionally real source-chart fixtures, not hand-drawn mock
images.  They protect the two places where a blue mark over a *live* yellow
stone was previously mistaken for an out-of-play marker.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

from extract_stone_coordinates import extract_stone_candidates, mini_sheet_images


ROOT = Path(__file__).parent


def candidates_for(
    pdf_name: str, local_page: int, shot: int, red_team: str, yellow_team: str
) -> list[tuple[str, float, float]]:
    with tempfile.TemporaryDirectory(prefix="gushue_fixture_") as temporary:
        panels = mini_sheet_images(ROOT / "gushue_games" / pdf_name, Path(temporary))[local_page]
        stones, _, _ = extract_stone_candidates(panels[shot - 1], red_team, yellow_team)
    return [
        (str(stone["team"]), float(stone["x_m"]), float(stone["y_m"]), bool(stone["has_royal_blue_mark"]))
        for stone in stones
    ]


def assert_blue_candidate(label: str, actual: list[tuple[str, float, float, bool]], expected: tuple[str, float, float]) -> None:
    """Assert an independently known live stone survives candidate extraction.

    This test does not claim every blue candidate is live.  It proves that the
    raw extractor has not thrown away the known live candidates before the
    sequence-level rule gets a chance to decide.
    """
    team, x, y = expected
    if not any(
        candidate_team == team
        and marked
        and abs(candidate_x - x) < 0.02
        and abs(candidate_y - y) < 0.02
        for candidate_team, candidate_x, candidate_y, marked in actual
    ):
        raise AssertionError(f"{label}: missing blue-marked candidate {expected}; actual={actual}")


def main() -> None:
    # 2022 CAN–SUI, End 6: CAN's second shot is an active yellow front guard
    # carrying a blue mark.  The following Swiss guard makes the count 1→2→3.
    sui_pdf = "wmcc_2022_11_vs_SUI_pages_728-736.pdf"
    assert_blue_candidate(
        "2022 CAN-SUI E6 S2",
        candidates_for(sui_pdf, 6, 2, "SUI", "CAN"),
        ("CAN", 1.10, 1.97),
    )

    # 2023 CAN–SWE, End 3: SWE's first-shot live yellow guard is blue-marked.
    # CAN's reply makes the count 0→1→2.
    swe_pdf = "wmcc_2023_03_vs_SWE_pages_70-77.pdf"
    assert_blue_candidate(
        "2023 CAN-SWE E3 S1",
        candidates_for(swe_pdf, 3, 1, "CAN", "SWE"),
        ("SWE", 0.13, 2.53),
    )
    print("RULE_FIXTURES_OK: known blue-marked live stones remain available to the sequence-level selector")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"RULE_FIXTURES_FAILED: {error}", file=sys.stderr)
        raise
