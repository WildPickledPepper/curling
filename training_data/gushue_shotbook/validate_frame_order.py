"""Verify that embedded mini-sheets map to the printed 1..16 shot order.

`pdfimages` exposes embedded objects in content-stream order, which happens to
look like reading order in many PDFs but is not a contractual guarantee.  This
validator reads the actual placement rectangles and the nearby printed shot
numbers from the PDF page.  It performs no coordinate extraction and writes no
data files.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import fitz


SHEET_SIZES = {(300, 600), (301, 601)}


def page_shot_labels(page: fitz.Page) -> list[int]:
    boards: list[fitz.Rect] = []
    for image in page.get_images(full=True):
        if (image[2], image[3]) in SHEET_SIZES:
            boards.extend(page.get_image_rects(image[0]))
    boards.sort(key=lambda rect: (round(rect.y0, 1), rect.x0))
    if not boards:
        return []
    words = page.get_text("words")
    labels: list[int] = []
    for rect in boards:
        candidates = []
        for x0, y0, x1, y1, text, *_ in words:
            if not text.isdigit():
                continue
            value = int(text)
            if not 1 <= value <= 16:
                continue
            # The number sits just above/left of its mini-sheet's upper edge.
            if rect.x0 - 12 <= x0 <= rect.x1 and abs(y0 - rect.y0) <= 7:
                candidates.append((abs(x0 - rect.x0), value))
        if len(candidates) != 1:
            raise ValueError(
                f"page {page.number + 1}: cannot uniquely associate a printed shot label "
                f"with mini-sheet at ({rect.x0:.1f}, {rect.y0:.1f}); candidates={candidates}"
            )
        labels.append(candidates[0][1])
    return labels


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).parent)
    parser.add_argument("--limit-games", type=int, default=0)
    args = parser.parse_args()
    root = args.root.resolve()
    games = list(csv.DictReader((root / "gushue_game_index.csv").open(encoding="utf-8")))
    if args.limit_games:
        games = games[: args.limit_games]
    checked_pages = 0
    checked_sheets = 0
    for game in games:
        document = fitz.open(root / game["gushue_game_pdf"])
        for page in document:
            labels = page_shot_labels(page)
            if not labels:
                continue
            expected = list(range(1, len(labels) + 1))
            if labels != expected:
                raise ValueError(
                    f"{game['gushue_game_pdf']} page {page.number + 1}: "
                    f"printed order {labels}, expected {expected}"
                )
            checked_pages += 1
            checked_sheets += len(labels)
    print(f"FRAME_ORDER_OK: games={len(games)} pages={checked_pages} mini_sheets={checked_sheets}")


if __name__ == "__main__":
    main()
