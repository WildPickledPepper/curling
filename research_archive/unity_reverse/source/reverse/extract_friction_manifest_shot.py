#!/usr/bin/env python3
"""Extract one BESTSHOT's friction events for diagnostic Unity manifest replay."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.reverse.front_half_pcm_replay import BESTSHOT_RE, text_preview


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--shot-index", type=int, required=True, help="Zero-based BESTSHOT ordinal.")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    current = -1
    kept: list[dict] = []
    for line in args.events.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        if BESTSHOT_RE.search(text_preview(event)):
            current += 1
            continue
        if current == args.shot_index and event.get("type") == "sliding.random_range.friction":
            kept.append(event)
    if not kept:
        raise SystemExit(f"No friction events for shot {args.shot_index}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in kept), encoding="utf-8")
    print(json.dumps({"shotIndex": args.shot_index, "frictionCount": len(kept), "output": str(args.output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
