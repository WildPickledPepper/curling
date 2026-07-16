#!/usr/bin/env python3
"""Parse AutoDCP record files into reproducible shot records.

AutoDCP records are INI-like files. The useful physics replay tuple is:

    section, BESTSHOT, RANDSEED, SWEEP

With those fields Unity can replay the same shot with the same Random seed.
TRACE is also parsed when present; it is a history/visualization stream made of
32-float frames in the trace coordinate system.
"""

from __future__ import annotations

import argparse
import configparser
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.reverse.recovered_curling_motion import RecoveredUnityRandom, unity_friction  # noqa: E402


SECTION_RE = re.compile(r"^\d{4}$")


@dataclass(frozen=True)
class AutoDcpShotRecord:
    path: str
    section: str
    end: int
    shot: int
    bestshot_velocity: float | None
    bestshot_offset: float | None
    bestshot_rotation: float | None
    randseed: int | None
    sweep_distance: float | None
    position: list[float] | None
    setstate: list[int] | None
    score: list[int] | None
    trace: list[list[float]] | None

    @property
    def has_replay_seed(self) -> bool:
        return self.bestshot_velocity is not None and self.randseed is not None

    @property
    def trace_frames(self) -> int:
        return 0 if self.trace is None else len(self.trace)


@dataclass(frozen=True)
class AutoDcpRecordFile:
    path: str
    last_state: str | None
    shots: list[AutoDcpShotRecord]


def _split_message(value: str | None) -> list[str]:
    if value is None:
        return []
    return value.strip().split()


def _parse_prefixed_floats(value: str | None, prefix: str, count: int) -> list[float] | None:
    parts = _split_message(value)
    if not parts:
        return None
    if parts[0].upper() != prefix:
        raise ValueError(f"expected {prefix}, got {parts[0]!r}")
    if len(parts) < count + 1:
        raise ValueError(f"{prefix} expects {count} numeric values, got {len(parts) - 1}")
    return [float(part) for part in parts[1 : count + 1]]


def _parse_prefixed_numbers(value: str | None, prefix: str, numeric_type: type[int] | type[float]) -> list[int] | list[float] | None:
    parts = _split_message(value)
    if not parts:
        return None
    if parts[0].upper() != prefix:
        raise ValueError(f"expected {prefix}, got {parts[0]!r}")
    return [numeric_type(part) for part in parts[1:]]


def _parse_trace(value: str | None) -> list[list[float]] | None:
    parts = _split_message(value)
    if not parts:
        return None
    if len(parts) % 32 != 0:
        raise ValueError(f"TRACE expects 32 floats per frame, got {len(parts)} values")
    values = [float(part) for part in parts]
    return [values[index : index + 32] for index in range(0, len(values), 32)]


def parse_record(path: Path) -> AutoDcpRecordFile:
    parser = configparser.ConfigParser(strict=False)
    parser.optionxform = str
    with path.open("r", encoding="utf-8-sig", errors="replace") as handle:
        parser.read_file(handle)

    last_state = None
    if parser.has_section("LASTSTATE"):
        last_state = parser.get("LASTSTATE", "LASTSTATE", fallback=None)

    shots: list[AutoDcpShotRecord] = []
    for section in sorted(parser.sections()):
        if not SECTION_RE.match(section):
            continue
        end = int(section[:2])
        shot = int(section[2:])
        bestshot = _parse_prefixed_floats(parser.get(section, "BESTSHOT", fallback=None), "BESTSHOT", 3)
        sweep = _parse_prefixed_floats(parser.get(section, "SWEEP", fallback=None), "SWEEP", 1)
        position = _parse_prefixed_numbers(parser.get(section, "POSITION", fallback=None), "POSITION", float)
        setstate = _parse_prefixed_numbers(parser.get(section, "SETSTATE", fallback=None), "SETSTATE", int)
        score = _parse_prefixed_numbers(parser.get(section, "SCORE", fallback=None), "SCORE", int)
        trace = _parse_trace(parser.get(section, "TRACE", fallback=None))
        seed_text = parser.get(section, "RANDSEED", fallback=None)
        shots.append(
            AutoDcpShotRecord(
                path=str(path),
                section=section,
                end=end,
                shot=shot,
                bestshot_velocity=bestshot[0] if bestshot else None,
                bestshot_offset=bestshot[1] if bestshot else None,
                bestshot_rotation=bestshot[2] if bestshot else None,
                randseed=int(seed_text) if seed_text not in (None, "") else None,
                sweep_distance=sweep[0] if sweep else None,
                position=position,
                setstate=setstate,
                score=score,
                trace=trace,
            )
        )
    return AutoDcpRecordFile(path=str(path), last_state=last_state, shots=shots)


def _with_friction_preview(record: AutoDcpShotRecord, count: int, sweeping: bool) -> dict:
    data = asdict(record)
    if record.randseed is None or count <= 0:
        return data
    rng = RecoveredUnityRandom.from_seed(record.randseed)
    data["friction_preview"] = [unity_friction(sweeping, rng=rng, noise=None) for _ in range(count)]
    data["friction_preview_sweeping"] = sweeping
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", nargs="+", type=Path)
    parser.add_argument("--jsonl", action="store_true", help="emit one JSON object per shot")
    parser.add_argument("--friction-preview", type=int, default=0, help="include first N recovered Unity friction values")
    parser.add_argument("--sweeping", action="store_true", help="friction preview uses sweep friction instead of dry friction")
    args = parser.parse_args()

    for path in args.records:
        record_file = parse_record(path)
        if args.jsonl:
            for shot in record_file.shots:
                print(json.dumps(_with_friction_preview(shot, args.friction_preview, args.sweeping), ensure_ascii=False))
            continue

        seeded = sum(1 for shot in record_file.shots if shot.has_replay_seed)
        sweep_count = sum(1 for shot in record_file.shots if shot.sweep_distance is not None)
        trace_count = sum(1 for shot in record_file.shots if shot.trace is not None)
        print(
            f"{record_file.path}: shots={len(record_file.shots)} seeded={seeded} "
            f"sweep={sweep_count} trace={trace_count} last_state={record_file.last_state}"
        )
        for shot in record_file.shots:
            seed = "seed=missing" if shot.randseed is None else f"seed={shot.randseed}"
            bestshot = (
                "bestshot=missing"
                if shot.bestshot_velocity is None
                else f"bestshot=({shot.bestshot_velocity:g},{shot.bestshot_offset:g},{shot.bestshot_rotation:g})"
            )
            sweep = "sweep=missing" if shot.sweep_distance is None else f"sweep={shot.sweep_distance:g}"
            trace = "trace=missing" if shot.trace is None else f"trace_frames={shot.trace_frames}"
            print(f"  [{shot.section}] {bestshot} {seed} {sweep} {trace}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
