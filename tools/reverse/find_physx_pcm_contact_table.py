#!/usr/bin/env python3
"""Find PhysX 7x7 PCM contact-method tables in Unity WebGL WAT data."""

from __future__ import annotations

import argparse
import heapq
import json
import re
from pathlib import Path

from extract_wat_data_string import _load_segments


GEOMETRIES = ("SPHERE", "PLANE", "CAPSULE", "BOX", "CONVEXMESH", "TRIANGLEMESH", "HEIGHTFIELD")
CONTACT_POSITIONS = {
    (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
    (1, 2), (1, 3), (1, 4),
    (2, 2), (2, 3), (2, 4), (2, 5),
    (3, 3), (3, 4), (3, 5),
    (4, 4), (4, 5),
}
INVALID_POSITIONS = {
    (0, 6),
    (1, 1), (1, 5), (1, 6),
    (2, 6),
    (3, 6),
    (4, 6),
    (5, 5), (5, 6),
    (6, 6),
}
ZERO_POSITIONS = {
    (1, 0),
    (2, 0), (2, 1),
    (3, 0), (3, 1), (3, 2),
    (4, 0), (4, 1), (4, 2), (4, 3),
    (5, 0), (5, 1), (5, 2), (5, 3), (5, 4),
    (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5),
}

FUNC_RE = re.compile(r"\$f(\d+)")


def _func_id(marker: str | None) -> int | None:
    if marker is None:
        return None
    match = FUNC_RE.fullmatch(marker)
    if not match:
        return None
    return int(match.group(1))


def _fmt(word: int, table_map: dict[str, str]) -> str:
    marker = table_map.get(str(word))
    func_id = _func_id(marker)
    if func_id is None:
        return str(word)
    return f"{word} {marker} func{func_id}"


def _score(words: tuple[int, ...], table_map: dict[str, str], min_func: int, max_func: int) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []

    for row in range(7):
        for col in range(7):
            word = words[row * 7 + col]
            marker = table_map.get(str(word))
            func_id = _func_id(marker)
            pos = (row, col)

            if pos in ZERO_POSITIONS:
                if word == 0:
                    score += 4
                else:
                    reasons.append(f"expected zero at {GEOMETRIES[row]}->{GEOMETRIES[col]}, got {word}")
                    score -= 8
            elif pos in CONTACT_POSITIONS:
                if func_id is not None and min_func <= func_id <= max_func:
                    score += 3
                else:
                    reasons.append(f"expected contact func at {GEOMETRIES[row]}->{GEOMETRIES[col]}, got {word}")
                    score -= 4
            elif pos in INVALID_POSITIONS:
                if func_id is not None:
                    score += 1
                else:
                    reasons.append(f"expected invalid-pair func at {GEOMETRIES[row]}->{GEOMETRIES[col]}, got {word}")
                    score -= 2

    invalid_values = {words[row * 7 + col] for row, col in INVALID_POSITIONS}
    if len(invalid_values) == 1:
        score += 12
    else:
        reasons.append(f"invalid entries differ: {sorted(invalid_values)}")
        score -= 6

    return score, reasons


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wat", type=Path)
    parser.add_argument("table_map", type=Path)
    parser.add_argument("--min-func", type=int, default=65000)
    parser.add_argument("--max-func", type=int, default=72500)
    parser.add_argument("--min-score", type=int, default=140)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--address-min", type=int)
    parser.add_argument("--address-max", type=int)
    args = parser.parse_args()

    segments = _load_segments(args.wat.read_text(encoding="utf-8", errors="replace"))
    table_map = json.loads(args.table_map.read_text(encoding="utf-8"))
    memory: dict[int, int] = {}
    for start, _end, data in segments:
        for index, byte in enumerate(data):
            memory[start + index] = byte

    address_min = args.address_min if args.address_min is not None else min(start for start, _end, _data in segments)
    address_max = args.address_max if args.address_max is not None else max(end for _start, end, _data in segments)

    def read_u32(address: int) -> int:
        return sum(memory.get(address + index, 0) << (index * 8) for index in range(4))

    best: list[tuple[int, int, tuple[int, ...], list[str]]] = []
    matched: list[tuple[int, int, tuple[int, ...], list[str]]] = []
    heap_limit = max(args.limit, 1)
    for address in range(address_min, address_max - 49 * 4 + 1, 4):
        words = tuple(read_u32(address + word_index * 4) for word_index in range(49))
        score, reasons = _score(words, table_map, args.min_func, args.max_func)
        item = (score, address, words, reasons)
        if len(best) < heap_limit:
            heapq.heappush(best, item)
        elif score > best[0][0]:
            heapq.heapreplace(best, item)
        if score >= args.min_score:
            matched.append(item)

    candidates = matched if matched else best
    candidates.sort(reverse=True, key=lambda item: item[0])

    if not matched:
        print(f"no candidates reached min-score={args.min_score}; showing best {len(candidates)} windows")

    for score, address, words, reasons in candidates[: args.limit]:
        print(f"candidate {address} ({address:#x}) score={score}")
        for row, row_name in enumerate(GEOMETRIES):
            print(f"  {row_name}:")
            for col, col_name in enumerate(GEOMETRIES):
                word = words[row * 7 + col]
                if word == 0:
                    mapped = "0"
                else:
                    mapped = _fmt(word, table_map)
                print(f"    {col_name}: {mapped}")
        if reasons:
            print("  notes:")
            for reason in reasons[:8]:
                print(f"    {reason}")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
