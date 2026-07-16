"""Pixel-exact round-trip validation for extracted stone states.

It re-opens the official PDFs, re-extracts their embedded mini-sheets, and
compares every saved live-stone component's SHA-256 over its exact source
pixels.  This is intentionally separate from the original extraction run.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import tempfile
from collections import Counter, defaultdict
from pathlib import Path


def load_extractor(root: Path):
    path = root / "extract_stone_coordinates.py"
    spec = importlib.util.spec_from_file_location("gushue_extract_for_validation", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fingerprint(stones: list[dict[str, object]]) -> list[str]:
    return sorted(str(stone["source_component_sha256"]) for stone in stones)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).parent)
    args = parser.parse_args()
    root = args.root.resolve()
    rows = [json.loads(line) for line in (root / "coordinates" / "gushue_stone_states.jsonl").open(encoding="utf-8")]
    by_game_page: dict[tuple[str, int], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_game_page[(str(row["gushue_game_pdf"]), int(row["local_pdf_page"]))].append(row)

    extractor = load_extractor(root)
    audit = Counter()
    mismatches: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="gushue_pixel_validate_") as temporary:
        temporary_root = Path(temporary)
        image_cache: dict[str, dict[int, list[Path]]] = {}
        for (pdf_key, local_page), states in sorted(by_game_page.items()):
            if pdf_key not in image_cache:
                directory = temporary_root / Path(pdf_key).stem
                directory.mkdir()
                image_cache[pdf_key] = extractor.mini_sheet_images(root / pdf_key, directory)
            panels = image_cache[pdf_key][local_page]
            for state in states:
                panel = panels[int(state["shot_in_end"]) - 1]
                actual, _, _ = extractor.extract_stones(panel, str(state["red_team"]), str(state["yellow_team"]))
                audit["states_compared"] += 1
                audit["components_compared"] += len(actual)
                if fingerprint(actual) != fingerprint(state["stones"]):
                    audit["state_mismatches"] += 1
                    mismatches.append(
                        {
                            "gushue_game_pdf": state["gushue_game_pdf"],
                            "end_number": state["end_number"],
                            "shot_in_end": state["shot_in_end"],
                            "expected_component_hashes": fingerprint(state["stones"]),
                            "fresh_component_hashes": fingerprint(actual),
                        }
                    )

    report = {
        "validation": "fresh PDF extraction compared with saved exact connected-component pixel hashes",
        "states_compared": audit["states_compared"],
        "components_compared": audit["components_compared"],
        "state_mismatches": audit["state_mismatches"],
        "pixel_component_difference": 0 if not mismatches else "non-zero; see mismatches",
    }
    output = root / "coordinates" / "pixel_roundtrip_audit.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (root / "coordinates" / "pixel_roundtrip_mismatches.json").write_text(
        json.dumps(mismatches, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
