"""Render deterministic source-image overlays for manual coordinate QA."""

from __future__ import annotations

import argparse
import importlib.util
import json
import tempfile
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def load_extractor(root: Path):
    path = root / "extract_stone_coordinates.py"
    spec = importlib.util.spec_from_file_location("gushue_extract", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def choose_samples(rows: list[dict[str, object]], count: int) -> list[dict[str, object]]:
    """Cover years, both source orientations, sparse and dense layouts."""
    buckets: dict[tuple[int, int, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        density = "dense" if len(row["stones"]) >= 6 else "sparse"
        buckets[(int(row["event_year"]), int(row["rotation_degrees_to_canonical"]), density)].append(row)
    selected: list[dict[str, object]] = []
    for key in sorted(buckets):
        values = buckets[key]
        selected.append(values[len(values) // 2])
    # Fill the remaining slots evenly through the already deterministic corpus.
    step = max(1, len(rows) // max(1, count - len(selected)))
    for row in rows[::step]:
        if len(selected) >= count:
            break
        if row not in selected:
            selected.append(row)
    return selected[:count]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).parent)
    parser.add_argument("--count", type=int, default=24)
    args = parser.parse_args()
    root = args.root.resolve()
    rows = [json.loads(line) for line in (root / "coordinates" / "gushue_stone_states.jsonl").open(encoding="utf-8")]
    selected = choose_samples(rows, args.count)
    extractor = load_extractor(root)

    tiles: list[Image.Image] = []
    with tempfile.TemporaryDirectory(prefix="gushue_qa_") as temporary:
        temporary_root = Path(temporary)
        image_cache: dict[str, dict[int, list[Path]]] = {}
        for record in selected:
            pdf_key = str(record["gushue_game_pdf"])
            if pdf_key not in image_cache:
                directory = temporary_root / Path(pdf_key).stem
                directory.mkdir()
                image_cache[pdf_key] = extractor.mini_sheet_images(root / pdf_key, directory)
            panel = image_cache[pdf_key][int(record["local_pdf_page"])][int(record["shot_in_end"]) - 1]
            tile = Image.open(panel).convert("RGB").resize((241, 481), Image.Resampling.NEAREST)
            draw = ImageDraw.Draw(tile)
            for stone in record["stones"]:
                x = float(stone["pixel_x"]) * 241 / Image.open(panel).width
                y = float(stone["pixel_y"]) * 481 / Image.open(panel).height
                draw.ellipse((x - 8, y - 8, x + 8, y + 8), outline=(0, 255, 0), width=2)
                draw.line((x - 10, y, x + 10, y), fill=(0, 255, 0), width=1)
                draw.line((x, y - 10, x, y + 10), fill=(0, 255, 0), width=1)
            label = f"{record['event_year']} {record['opponent_code']} E{record['end_number']} S{record['shot_in_end']}\n{record['source_house_position']}→{record['rotation_degrees_to_canonical']}° / {len(record['stones'])} stones"
            labeled = Image.new("RGB", (241, 521), "white")
            labeled.paste(tile, (0, 0))
            ImageDraw.Draw(labeled).text((4, 485), label, fill="black")
            tiles.append(labeled)

    columns = 6
    rows_count = (len(tiles) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * 241, rows_count * 521), "white")
    for index, tile in enumerate(tiles):
        sheet.paste(tile, ((index % columns) * 241, (index // columns) * 521))
    output = root / "diagnostics" / "coordinate_overlay_qa.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)
    print(output)


if __name__ == "__main__":
    main()
