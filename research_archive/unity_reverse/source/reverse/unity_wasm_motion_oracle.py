"""Batch interface to the recovered Unity ``Newfrictionstep`` wasm function.

The wasm module is extracted from the shipped Unity WebGL build.  Calling it
for a whole sliding sequence preserves Unity's original f64 arithmetic without
using any captured Unity pose, velocity, or setter output as an input.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_WASM = Path(r"D:\esp\tmp\curling_reverse_il2cpp\newfrictionstep_oracle.wasm")
DEFAULT_RUNNER = ROOT / "tools" / "reverse" / "run_newfrictionstep_wasm_rollout.js"
DEFAULT_RPC_RUNNER = ROOT / "tools" / "reverse" / "run_newfrictionstep_wasm_rpc.js"


def rollout(
    *,
    vx: float,
    vy: float,
    angle: float,
    frictions: Sequence[float],
    wasm: Path = DEFAULT_WASM,
    runner: Path = DEFAULT_RUNNER,
) -> list[dict[str, float]]:
    """Return Unity-wasm motion states after each supplied friction update."""

    wasm = wasm.resolve()
    runner = runner.resolve()
    if not wasm.is_file():
        raise RuntimeError(f"Unity Newfrictionstep wasm oracle is missing: {wasm}")
    if not runner.is_file():
        raise RuntimeError(f"Unity Newfrictionstep wasm runner is missing: {runner}")
    payload = {
        "vx": float(vx),
        "vy": float(vy),
        "angle": float(angle),
        "steptime": 0.0010000000474974513,
        "frictions": [float(value) for value in frictions],
    }
    completed = subprocess.run(
        ["node", str(runner), str(wasm)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=True,
    )
    raw: Any = json.loads(completed.stdout)
    rows = raw.get("steps") if isinstance(raw, dict) else None
    if not isinstance(rows, list) or len(rows) != len(frictions):
        raise RuntimeError("Unity Newfrictionstep wasm oracle returned an incomplete rollout")
    result: list[dict[str, float]] = []
    for row in rows:
        if not isinstance(row, dict):
            raise RuntimeError("Unity Newfrictionstep wasm oracle returned a malformed step")
        result.append({key: float(row[key]) for key in ("vx", "vy", "angle")})
    return result


class WasmMotionStepper:
    """Persistent exact Unity-motion evaluator driven by the local getter state."""

    def __init__(self, wasm: Path = DEFAULT_WASM, runner: Path = DEFAULT_RPC_RUNNER) -> None:
        wasm = wasm.resolve()
        runner = runner.resolve()
        if not wasm.is_file() or not runner.is_file():
            raise RuntimeError("Unity Newfrictionstep wasm oracle or its RPC runner is missing")
        self._process = subprocess.Popen(
            ["node", str(runner), str(wasm)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        if self._process.stdin is None or self._process.stdout is None:
            self.close()
            raise RuntimeError("cannot open Unity Newfrictionstep wasm RPC pipes")

    def step(self, *, friction: float, vx: float, vy: float, angle: float) -> tuple[float, float, float]:
        if self._process.poll() is not None or self._process.stdin is None or self._process.stdout is None:
            detail = self._process.stderr.read() if self._process.stderr is not None else ""
            raise RuntimeError(f"Unity Newfrictionstep wasm RPC stopped unexpectedly: {detail}")
        self._process.stdin.write(json.dumps({
            "friction": float(friction), "vx": float(vx), "vy": float(vy), "angle": float(angle),
        }) + "\n")
        self._process.stdin.flush()
        line = self._process.stdout.readline()
        if not line:
            detail = self._process.stderr.read() if self._process.stderr is not None else ""
            raise RuntimeError(f"Unity Newfrictionstep wasm RPC produced no response: {detail}")
        row = json.loads(line)
        return float(row["vx"]), float(row["vy"]), float(row["angle"])

    def close(self) -> None:
        process = getattr(self, "_process", None)
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()

    def __enter__(self) -> "WasmMotionStepper":
        return self

    def __exit__(self, *_unused: object) -> None:
        self.close()
