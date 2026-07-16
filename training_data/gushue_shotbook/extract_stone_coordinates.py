"""Extract in-play stone coordinates from World Curling Shot-by-Shot charts.

Each chart page contains one end and up to sixteen 301x601 indexed-colour
mini-sheet images.  The mini-sheets are embedded raster images, so extracting
them directly from the PDF is more reliable than cropping a rendered page.

The output is deliberately a *canonical diagram coordinate system*: every end
is rotated as needed so its house is at the top, with origin at the button,
+x to canonical chart right and +y toward the hog line / guards.  It is not
yet the local-simulator coordinate system; that conversion belongs at the
adapter boundary where the simulator's sheet origin is known.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import tempfile
from collections import Counter, deque
from pathlib import Path
from typing import Iterator

import numpy as np
from PIL import Image


# The outer 12-foot circle has radius 6 ft = 1.8288 m.  The official charts
# draw it at 40% of a mini-sheet's width.  The remaining error is under 1 cm
# for both 300x600 and 301x601 chart variants.
OUTER_HOUSE_RADIUS_M = 1.8288
MIN_FILLED_COMPONENT_PIXELS = 100
MIN_FILLED_BBOX_RATIO = 0.5
# Unplayed counters have centres around y=9. A live stone can legitimately sit
# on the back-line with its centre around y=39, so do not crop at the house
# border (y=40).
PLAY_Y_MIN = 25
PLAY_Y_MAX_MARGIN = 25
TEAM = re.compile(r"(?P<code>[A-Z]{3}) - (?P<name>[A-Za-z]+)")
END = re.compile(r"Game - Shot by Shot\s+End\s+(?P<end>\d+)")
LIST_LINE = re.compile(
    r"^\s*(?P<page>\d+)\s+(?P<num>\d+)\s+\w+\s+"
    r"(?P<width>\d+)\s+(?P<height>\d+)"
)


def connected_components(mask: np.ndarray) -> Iterator[np.ndarray]:
    """Yield 4-connected pixel components without requiring OpenCV/SciPy."""
    height, width = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    for y, x in zip(*np.nonzero(mask)):
        if seen[y, x]:
            continue
        queue: deque[tuple[int, int]] = deque([(int(y), int(x))])
        seen[y, x] = True
        points: list[tuple[int, int]] = []
        while queue:
            current_y, current_x = queue.popleft()
            points.append((current_y, current_x))
            for next_y, next_x in (
                (current_y - 1, current_x),
                (current_y + 1, current_x),
                (current_y, current_x - 1),
                (current_y, current_x + 1),
            ):
                if (
                    0 <= next_y < height
                    and 0 <= next_x < width
                    and mask[next_y, next_x]
                    and not seen[next_y, next_x]
                ):
                    seen[next_y, next_x] = True
                    queue.append((next_y, next_x))
        yield np.asarray(points, dtype=np.int16)


def button_centre(image: np.ndarray) -> tuple[float, float, float]:
    """Find the diagram's button from the fixed pale-blue 12-foot ring."""
    blue_ring = np.all(image == (200, 200, 255), axis=2)
    ys, xs = np.nonzero(blue_ring)
    if not len(xs):
        raise ValueError("Could not locate 12-foot ring in mini-sheet image")
    centre_x = float((xs.min() + xs.max()) / 2.0)
    centre_y = float((ys.min() + ys.max()) / 2.0)
    outer_radius_px = image.shape[1] * 0.4
    return centre_x, centre_y, outer_radius_px


def extract_stones(image_path: Path, red_team: str, yellow_team: str) -> tuple[list[dict[str, object]], str, int]:
    image = np.asarray(Image.open(image_path).convert("RGB"))
    height, _ = image.shape[:2]
    centre_x, centre_y, outer_radius_px = button_centre(image)
    metres_per_pixel = OUTER_HOUSE_RADIUS_M / outer_radius_px
    # The official scorebook alternates delivery direction by end: odd pages
    # have the house at the top, even pages have it at the bottom.  Normalize
    # bottom-house pages with a full 180-degree rotation, not merely a y flip;
    # otherwise left/right tactical layouts would be mirrored every other end.
    house_at_top = centre_y < height / 2.0
    sign = 1.0 if house_at_top else -1.0
    house_position = "top" if house_at_top else "bottom"
    rotation_degrees = 0 if house_at_top else 180

    # Solid stones use high-saturation fills. The yellow house is explicitly
    # excluded because its green channel is 255 rather than the stone's ~220.
    masks = {
        "red": (image[:, :, 0] >= 220) & (image[:, :, 1] <= 80) & (image[:, :, 2] <= 80),
        "yellow": (image[:, :, 0] >= 220)
        & (image[:, :, 1] >= 150)
        & (image[:, :, 1] <= 245)
        & (image[:, :, 2] <= 80),
    }
    teams = {"red": red_team, "yellow": yellow_team}
    stones: list[dict[str, object]] = []
    for colour, mask in masks.items():
        for component in connected_components(mask):
            area = len(component)
            pixel_y = float(component[:, 0].mean())
            pixel_x = float(component[:, 1].mean())
            min_y, min_x = component.min(axis=0)
            max_y, max_x = component.max(axis=0)
            bounding_area = int(max_y - min_y + 1) * int(max_x - min_x + 1)
            filled_bbox_ratio = area / bounding_area
            # CurlIT keeps a removed stone visible as a coloured circle with a
            # royal-blue X through it.  It is useful to humans but not a live
            # stone.  Looking for that saturated blue only inside the circle's
            # bounding box keeps it distinct from the pale-blue house ring.
            component_box = image[
                int(min_y) : int(max_y) + 1,
                int(min_x) : int(max_x) + 1,
            ]
            crossed_out = bool(
                np.any(
                    (component_box[:, :, 0] <= 80)
                    & (component_box[:, :, 1] <= 80)
                    & (component_box[:, :, 2] >= 200)
                )
            )
            # Reject outline-only "previous position" marks and unused-stone
            # counters at the upper/lower margins, plus blue-Xed removed rocks.
            if (
                area < MIN_FILLED_COMPONENT_PIXELS
                or filled_bbox_ratio < MIN_FILLED_BBOX_RATIO
                or pixel_y < PLAY_Y_MIN
                or pixel_y > height - PLAY_Y_MAX_MARGIN
                or crossed_out
            ):
                continue
            stones.append(
                {
                    "team": teams[colour],
                    "colour": colour,
                    "x_m": round(sign * (pixel_x - centre_x) * metres_per_pixel, 4),
                    "y_m": round(sign * (pixel_y - centre_y) * metres_per_pixel, 4),
                    "pixel_x": round(pixel_x, 2),
                    "pixel_y": round(pixel_y, 2),
                    "fill_pixels": area,
                    "filled_bbox_ratio": round(filled_bbox_ratio, 3),
                }
            )
    return (
        sorted(stones, key=lambda stone: (str(stone["team"]), float(stone["x_m"]), float(stone["y_m"]))),
        house_position,
        rotation_degrees,
    )


def mini_sheet_images(pdf: Path, temporary_dir: Path) -> dict[int, list[Path]]:
    """Return extracted mini-sheets grouped by PDF page, in shot order."""
    listing = subprocess.check_output(["pdfimages", "-list", str(pdf)], text=True, encoding="utf-8", errors="replace")
    board_refs: list[tuple[int, int]] = []
    for line in listing.splitlines():
        match = LIST_LINE.match(line)
        if not match:
            continue
        page = int(match["page"])
        number = int(match["num"])
        width = int(match["width"])
        height = int(match["height"])
        if width in (300, 301) and height in (600, 601):
            board_refs.append((page, number))

    prefix = temporary_dir / "image"
    subprocess.run(["pdfimages", "-png", str(pdf), str(prefix)], check=True)
    grouped: dict[int, list[Path]] = {}
    for page, number in board_refs:
        path = temporary_dir / f"image-{number:03d}.png"
        if not path.exists():
            raise FileNotFoundError(f"pdfimages listed {path.name}, but did not write it")
        grouped.setdefault(page, []).append(path)
    return grouped


def page_metadata(source_text: Path, source_page: int) -> tuple[int, str, str]:
    pages = source_text.read_text(encoding="utf-8", errors="replace").split("\f")
    text = pages[source_page - 1]
    end_match = END.search(text)
    if not end_match:
        raise ValueError(f"Cannot find End number on source page {source_page} in {source_text.name}")
    teams = [match["code"] for match in TEAM.finditer(text)]
    if len(teams) < 2:
        raise ValueError(f"Cannot identify red/yellow teams on source page {source_page} in {source_text.name}")
    return int(end_match["end"]), teams[0], teams[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).parent)
    parser.add_argument("--limit-games", type=int, default=0, help="For diagnosis: process only the first N indexed games.")
    args = parser.parse_args()
    if not shutil.which("pdfimages"):
        raise SystemExit("Missing pdfimages; install Poppler and add it to PATH.")

    root = args.root.resolve()
    coordinate_dir = root / "coordinates"
    coordinate_dir.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader((root / "gushue_game_index.csv").open(encoding="utf-8")))
    if args.limit_games:
        rows = rows[: args.limit_games]

    records: list[dict[str, object]] = []
    audit = Counter()
    review_states: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="gushue_charts_") as temporary:
        temporary_root = Path(temporary)
        for game in rows:
            game_pdf = root / game["gushue_game_pdf"]
            source_text = root / "extracted_text" / (Path(game["source_book"]).stem + ".txt")
            game_tmp = temporary_root / game_pdf.stem
            game_tmp.mkdir()
            panels_by_page = mini_sheet_images(game_pdf, game_tmp)
            audit["games"] += 1

            for local_page, panels in sorted(panels_by_page.items()):
                source_page = int(game["source_page_start"]) + local_page - 1
                end_number, red_team, yellow_team = page_metadata(source_text, source_page)
                audit["chart_pages"] += 1
                audit["mini_sheets"] += len(panels)
                if len(panels) > 16:
                    raise ValueError(f"{game_pdf.name} page {local_page} has {len(panels)} panels")
                previous_count = 0
                for shot_in_end, panel in enumerate(panels, start=1):
                    stones, house_position, rotation_degrees = extract_stones(panel, red_team, yellow_team)
                    count_delta_anomaly = len(stones) > previous_count + 1
                    if count_delta_anomaly:
                        audit["count_delta_anomalies"] += 1
                        review_states.append(
                            {
                                "gushue_game_pdf": game["gushue_game_pdf"],
                                "end_number": end_number,
                                "shot_in_end": shot_in_end,
                                "previous_detected_stone_count": previous_count,
                                "current_detected_stone_count": len(stones),
                                "reason": "detected count rose by more than one; review chart before strategy use",
                            }
                        )
                    previous_count = len(stones)
                    audit["states"] += 1
                    audit["stones"] += len(stones)
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
                            "quality_status": "needs_manual_review" if count_delta_anomaly else "auto_pass",
                            "stones": stones,
                        }
                    )

    output = coordinate_dir / "gushue_stone_states.jsonl"
    with output.open("w", encoding="utf-8") as stream:
        for record in records:
            stream.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    report = {
        "games": audit["games"],
        "chart_pages": audit["chart_pages"],
        "post_shot_states": audit["states"],
        "detected_in_play_stones_across_all_states": audit["stones"],
        "count_delta_anomalies": audit["count_delta_anomalies"],
        "coordinate_system": "button_origin_m; +x=canonical_chart_right; +y=toward_hog_line",
        "orientation_normalisation": "bottom-house source charts are rotated 180 degrees",
        "source": "World Curling / CurlIT embedded Shot-by-Shot mini-sheet images",
        "filters": {
            "solid_component_minimum_pixels": MIN_FILLED_COMPONENT_PIXELS,
            "solid_component_minimum_bbox_ratio": MIN_FILLED_BBOX_RATIO,
            "ignored": ["outline-only previous-position marks", "unused-stone counters", "out-of-play stones"],
        },
    }
    (coordinate_dir / "extraction_audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (coordinate_dir / "manual_review_states.json").write_text(
        json.dumps(review_states, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
