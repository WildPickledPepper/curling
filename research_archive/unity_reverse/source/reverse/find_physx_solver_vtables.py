#!/usr/bin/env python3
"""Find PhysX solver constraint vtables in Unity WebGL WAT data."""

from __future__ import annotations

import argparse
import heapq
import json
import re
import struct
from pathlib import Path

from extract_wat_data_string import _load_segments


TYPE_NAMES = (
    "NONE",
    "RB_CONTACT",
    "RB_1D",
    "EXT_CONTACT",
    "EXT_1D",
    "STATIC_CONTACT",
    "NOFRICTION_RB_CONTACT",
    "BLOCK_RB_CONTACT",
    "BLOCK_STATIC_RB_CONTACT",
    "BLOCK_1D",
)
FUNC_RE = re.compile(r"\$f(\d+)")


def _func_id(marker: str | None) -> int | None:
    if marker is None:
        return None
    match = FUNC_RE.fullmatch(marker)
    return int(match.group(1)) if match else None


def _fmt(word: int, table_map: dict[str, str]) -> str:
    if word == 0:
        return "0"
    marker = table_map.get(str(word))
    func_id = _func_id(marker)
    if func_id is None:
        return str(word)
    return f"{word} {marker} func{func_id}"


def _score(words: tuple[int, ...], table_map: dict[str, str], min_func: int, max_func: int) -> tuple[int, list[str]]:
    score = 0
    notes: list[str] = []

    expected_zero = {0, 3, 4}
    expected_func = {1, 2, 5, 6, 7, 8, 9}
    for index, word in enumerate(words):
        func_id = _func_id(table_map.get(str(word)))
        if index in expected_zero:
            if word == 0:
                score += 8
            else:
                notes.append(f"expected zero at {TYPE_NAMES[index]}, got {_fmt(word, table_map)}")
                score -= 10
        elif index in expected_func:
            if func_id is not None and min_func <= func_id <= max_func:
                score += 6
            else:
                notes.append(f"expected solver func at {TYPE_NAMES[index]}, got {_fmt(word, table_map)}")
                score -= 6

    if words[1] != 0 and words[1] == words[6]:
        score += 12
    else:
        notes.append("RB_CONTACT and NOFRICTION_RB_CONTACT entries differ")
        score -= 4

    return score, notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wat", type=Path)
    parser.add_argument("table_map", type=Path)
    parser.add_argument("--min-func", type=int, default=70000)
    parser.add_argument("--max-func", type=int, default=73000)
    parser.add_argument("--min-score", type=int, default=70)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--address-min", type=int)
    parser.add_argument("--address-max", type=int)
    args = parser.parse_args()

    segments = _load_segments(args.wat.read_text(encoding="utf-8", errors="replace"))
    table_map = json.loads(args.table_map.read_text(encoding="utf-8"))
    address_min = args.address_min if args.address_min is not None else min(start for start, _end, _data in segments)
    address_max = args.address_max if args.address_max is not None else max(end for _start, end, _data in segments)

    best: list[tuple[int, int, tuple[int, ...], list[str]]] = []
    matches: list[tuple[int, int, tuple[int, ...], list[str]]] = []
    heap_limit = max(args.limit, 1)
    window_size = len(TYPE_NAMES) * 4
    for seg_start, seg_end, data in segments:
        start = max(seg_start, address_min)
        end = min(seg_end, address_max)
        if end - start < window_size:
            continue
        offset_start = start - seg_start
        offset_end = end - seg_start - window_size
        for offset in range(offset_start + (-offset_start % 4), offset_end + 1, 4):
            address = seg_start + offset
            words = struct.unpack_from("<" + "I" * len(TYPE_NAMES), data, offset)
            score, notes = _score(words, table_map, args.min_func, args.max_func)
            item = (score, address, words, notes)
            if len(best) < heap_limit:
                heapq.heappush(best, item)
            elif score > best[0][0]:
                heapq.heapreplace(best, item)
            if score >= args.min_score:
                matches.append(item)

    candidates = matches if matches else best
    candidates.sort(reverse=True, key=lambda item: item[0])
    if not matches:
        print(f"no candidates reached min-score={args.min_score}; showing best {len(candidates)} windows")

    for score, address, words, notes in candidates[: args.limit]:
        print(f"candidate {address} ({address:#x}) score={score}")
        for index, name in enumerate(TYPE_NAMES):
            print(f"  [{index}] {name}: {_fmt(words[index], table_map)}")
        if notes:
            print("  notes:")
            for note in notes[:8]:
                print(f"    {note}")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
