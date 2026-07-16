"""Build a compact Team Gushue shot-chart corpus from official Results Books.

The complete official books remain untouched.  This script extracts only the
``Game - Shot by Shot`` page ranges that contain ``CAN: GUSHUE B`` and writes
one lossless PDF per game plus a CSV index.  It deliberately does not infer
tactics: it creates a traceable evidence corpus for that later step.
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
import subprocess
from pathlib import Path

from pypdf import PdfReader, PdfWriter


GUSHUE_MARKER = re.compile(r"CAN:\s*GUSHUE B")
BOOK_NAME = re.compile(r"WMCC(?P<year>\d{4})_ResultsBook\.pdf$")
TEAM = re.compile(r"(?P<code>[A-Z]{3}) - (?P<name>[A-Za-z]+)")
PHASE = re.compile(r"Gold Medal Game|Bronze Medal Game|Semi-finals|Qualifications|Session \d+")


def grouped_pages(pages: list[int]) -> list[tuple[int, int]]:
    groups: list[tuple[int, int]] = []
    for page in pages:
        if not groups or page > groups[-1][1] + 1:
            groups.append((page, page))
        else:
            groups[-1] = (groups[-1][0], page)
    return groups


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).parent)
    args = parser.parse_args()
    root = args.root.resolve()
    source_dir = root / "source_results_books"
    text_dir = root / "extracted_text"
    game_dir = root / "gushue_games"
    text_dir.mkdir(parents=True, exist_ok=True)
    game_dir.mkdir(parents=True, exist_ok=True)

    books = sorted(source_dir.glob("WMCC*_ResultsBook.pdf"))
    if not books:
        raise SystemExit(f"No Results Book found under {source_dir}")

    rows: list[dict[str, object]] = []
    for book in books:
        match = BOOK_NAME.match(book.name)
        if not match:
            continue
        year = int(match["year"])
        text_path = text_dir / f"{book.stem}.txt"
        if not text_path.exists():
            if not shutil.which("pdftotext"):
                raise SystemExit("Missing pdftotext; install Poppler or provide extracted_text first.")
            subprocess.run(["pdftotext", "-layout", str(book), str(text_path)], check=True)

        # The leading blank chunk is retained by pdftotext, hence array index
        # plus one equals the physical PDF page number.
        text_pages = text_path.read_text(encoding="utf-8", errors="replace").split("\f")
        marked_pages = [number for number, text in enumerate(text_pages, start=1) if GUSHUE_MARKER.search(text)]
        reader = PdfReader(str(book))

        for sequence, (start, end) in enumerate(grouped_pages(marked_pages), start=1):
            header = re.sub(r"\s+", " ", text_pages[start - 1]).strip()
            opponent = next((item["code"] for item in TEAM.finditer(header) if item["code"] != "CAN"), "UNK")
            phase_match = PHASE.search(header)
            phase = phase_match.group(0) if phase_match else "Unclassified"
            slug = f"wmcc_{year}_{sequence:02d}_vs_{opponent}_pages_{start}-{end}"
            destination = game_dir / f"{slug}.pdf"

            if not destination.exists():
                writer = PdfWriter()
                for page_index in range(start - 1, end):
                    writer.add_page(reader.pages[page_index])
                with destination.open("wb") as stream:
                    writer.write(stream)

            rows.append(
                {
                    "event_year": year,
                    "game_sequence_in_book": sequence,
                    "phase": phase,
                    "opponent_code": opponent,
                    "source_book": f"source_results_books/{book.name}",
                    "source_page_start": start,
                    "source_page_end": end,
                    "shot_chart_pages": end - start + 1,
                    "gushue_game_pdf": f"gushue_games/{destination.name}",
                }
            )

    index_path = root / "gushue_game_index.csv"
    columns = [
        "event_year", "game_sequence_in_book", "phase", "opponent_code",
        "source_book", "source_page_start", "source_page_end", "shot_chart_pages",
        "gushue_game_pdf",
    ]
    with index_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    by_year: dict[int, int] = {}
    for row in rows:
        by_year[int(row["event_year"])] = by_year.get(int(row["event_year"]), 0) + 1
    print(f"Built {len(rows)} Team Gushue game records: {index_path}")
    for year, count in sorted(by_year.items()):
        print(f"WMCC {year}: {count} games")


if __name__ == "__main__":
    main()
