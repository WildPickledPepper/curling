"""Compare the Python and native settle loops on the exact same 16-shot end.

Run this file twice in fresh CPython 3.8 processes: once normally, then once
with ``--native-extension <built pyd>``.  The report contains only the stable
game outputs plus elapsed wall time, so the two reports can be compared without
depending on forensic per-tick payloads.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import types
from pathlib import Path
from typing import Any, Sequence


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# This sequence deliberately includes straight and offset takeouts.  It is
# deterministic and leaves the Scene alive across all 16 shots, just like
# self-play training.
SHOTS: Sequence[Sequence[float]] = (
    (3.00, 0.00, 0.00),
    (4.20, 0.00, 0.00),
    (3.00, 0.22, 0.00),
    (4.20, 0.22, 0.00),
) * 4


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--native-extension", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def compact_states(states: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep all simulation state, excluding only diagnostic-only fields."""

    keys = ("enabled", "x", "y", "yaw", "vx", "vy", "w")
    return [{key: state[key] for key in keys} for state in states]


def install_extension(path: Path | None) -> bool:
    from local_simulator import runtime_loader

    if path is not None:
        runtime_loader.BUNDLED_EXTENSION = path.resolve()
    pyphysx = runtime_loader.install_bundled_pyphysx()
    return hasattr(pyphysx.Scene, "simulate_until_quiet")


def install_native_settle(environment: Any) -> None:
    def native_settle(self: Any, *, max_steps: int = 6000) -> bool:
        bodies = [slot.body for slot in self.scene.slots if slot.enabled]
        settled, _steps = self.scene.scene.simulate_until_quiet(
            bodies,
            self.scene.dt,
            max_steps,
            0.01,
            0.01,
            20,
        )
        return bool(settled)

    environment._settle = types.MethodType(native_settle, environment)


def main() -> int:
    args = parse_args()
    native = install_extension(args.native_extension)
    from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd

    environment = StrictCurlingEnd(seed=20260715, training_fast=True)
    if native:
        install_native_settle(environment)
    environment.reset()
    trace: list[dict[str, Any]] = []
    started = time.perf_counter()
    for shot_number, shot in enumerate(SHOTS, start=1):
        result = environment.play(shot)
        trace.append(
            {
                "shot": shot_number,
                "contact": result["contact"],
                "settled": result["settled"],
                "cleared": result["cleared"],
                "states": compact_states(result["states"]),
            }
        )
    elapsed_seconds = time.perf_counter() - started
    report = {
        "schema": "native_settle_equivalence_v1",
        "nativeSettle": native,
        "nativeFrontHalf": hasattr(environment.scene.scene, "simulate_curling_until_first_contact"),
        "elapsedSeconds": elapsed_seconds,
        "trace": trace,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                "nativeSettle": native,
                "nativeFrontHalf": report["nativeFrontHalf"],
                "elapsedSeconds": elapsed_seconds,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
