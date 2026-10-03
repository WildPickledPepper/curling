"""Build the smallest self-contained course submission for the PhysX planner.

The generated ``planning_proxy/submission`` directory contains exactly two
files to copy into the course workspace root: ``planner_submission.py`` and
``planner_payload.zip``.  The native ``.pyd`` stays *inside* the payload zip
until the selected Python entrypoint extracts it at runtime.
"""

from __future__ import annotations

import shutil
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "planning_proxy"
OUT = SOURCE / "submission"
STAGE = OUT / ".stage"
PAYLOAD = OUT / "planner_payload.zip"
DIRECT_OUT = SOURCE / "submission_direct"


def copy_file(source: Path, target_root: Path) -> None:
    target = target_root / source.relative_to(ROOT)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def include_planning_proxy() -> list[Path]:
    keep = {
        "analytic_proxy.py", "competition_rules.py", "endgame_shapes.py",
        "evaluate_vs_teammate_ppo.py", "first_player_strategy.py",
        "strict_refine.py", "unity_planner_robot.py",
    }
    return [SOURCE / name for name in sorted(keep)]


def include_local_simulator() -> list[Path]:
    base = ROOT / "local_simulator"
    keep: list[Path] = []
    for path in base.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(base)
        if rel.parts[0] in {"tests", "runtime"} and rel.parts[:2] == ("runtime", "wheels"):
            continue
        if path.suffix == ".py" or rel.parts[0] in {"assets", "runtime_support"}:
            keep.append(path)
        elif rel.parts[:2] == ("runtime", "pyphysx") and (
            path.name in {"__init__.py", "quaternion.py"}
            or (path.name.startswith("_pyphysx.cp") and path.name.endswith("-win_amd64.pyd"))
        ):
            keep.append(path)
    return keep


def build() -> Path:
    if OUT.exists():
        shutil.rmtree(OUT)
    STAGE.mkdir(parents=True)
    for source in include_planning_proxy() + include_local_simulator():
        copy_file(source, STAGE)
    shutil.copy2(SOURCE / "planner_submission.py", OUT / "planner_submission.py")
    with zipfile.ZipFile(PAYLOAD, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(STAGE.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(STAGE).as_posix())
    shutil.rmtree(STAGE)
    return PAYLOAD


def build_direct() -> Path:
    if DIRECT_OUT.exists():
        shutil.rmtree(DIRECT_OUT)
    DIRECT_OUT.mkdir(parents=True)
    for source in include_planning_proxy() + include_local_simulator():
        copy_file(source, DIRECT_OUT)
    shutil.copy2(SOURCE / "planner_submission_direct.py", DIRECT_OUT / "planner_submission_direct.py")
    return DIRECT_OUT


if __name__ == "__main__":
    payload = build()
    direct = build_direct()
    print(f"submission_entry={OUT / 'planner_submission.py'}")
    print(f"submission_payload={payload} ({payload.stat().st_size / 1024 / 1024:.2f} MiB)")
    print(f"direct_submission={direct}")
