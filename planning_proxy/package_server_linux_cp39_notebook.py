#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the direct-upload Linux CPython 3.9 course-Notebook package.

The native extension is produced by ``linux_cp39_physx_build`` in a Debian
bullseye (glibc 2.31) container.  This script deliberately emits a separate
archive and never replaces the Windows CP313 delivery artifacts.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROXY = ROOT / "planning_proxy"
SIMULATOR = ROOT / "local_simulator"
NATIVE_EXTENSION = Path(
    r"D:\DockerData\curling_physx_linux_build\pyphysx-build-private\lib"
    r"\_pyphysx.cpython-39-x86_64-linux-gnu.so"
)
NAME = "server_linux_cp39_physx_state_machine_20260721_direct"
OUT = PROXY / NAME
ARCHIVE = PROXY / f"{NAME}.zip"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def copy_into_payload(source: Path) -> None:
    target = OUT / source.relative_to(ROOT)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def payload_sources() -> list[Path]:
    planning = [
        PROXY / name
        for name in (
            "analytic_proxy.py",
            "competition_rules.py",
            "endgame_shapes.py",
            "evaluate_vs_teammate_ppo.py",
            "first_player_strategy.py",
            "strict_refine.py",
            "unity_planner_robot.py",
        )
    ]
    simulator: list[Path] = []
    for path in SIMULATOR.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(SIMULATOR)
        if rel.parts[:2] == ("runtime", "wheels"):
            continue
        if path.suffix == ".py" or rel.parts[0] in {"assets", "runtime_support"}:
            simulator.append(path)
    return planning + sorted(set(simulator))


def write_entrypoint() -> Path:
    source = (PROXY / "planner_submission_direct.py").read_text(encoding="utf-8")
    expected = '"--decision-budget-seconds": "90",'
    if expected not in source:
        raise RuntimeError("入口默认预算与预期不符，拒绝生成。")
    entry = OUT / "planner_submission_direct.py"
    entry.write_text(source.replace(expected, '"--decision-budget-seconds": "105",', 1), encoding="utf-8")
    return entry


def build() -> None:
    if OUT.exists() or ARCHIVE.exists():
        raise RuntimeError(f"输出已存在，拒绝覆盖：{OUT} 或 {ARCHIVE}")
    if not NATIVE_EXTENSION.is_file():
        raise RuntimeError(f"缺少已验证的 Linux CP39 扩展：{NATIVE_EXTENSION}")

    OUT.mkdir(parents=True)
    for source in payload_sources():
        copy_into_payload(source)

    native_dir = OUT / "local_simulator" / "runtime" / "pyphysx"
    native_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(NATIVE_EXTENSION, native_dir / NATIVE_EXTENSION.name)
    entry = write_entrypoint()

    manifest = {
        "package": NAME,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "target": {
            "platform": "Linux x86_64",
            "python": "3.9",
            "soabi": "cpython-39-x86_64-linux-gnu",
            "glibc_build_baseline": "2.31 (Debian bullseye)",
        },
        "entrypoint": entry.name,
        "decision_budget_seconds": 105,
        "native_extension": {
            "payload_path": f"local_simulator/runtime/pyphysx/{NATIVE_EXTENSION.name}",
            "bytes": NATIVE_EXTENSION.stat().st_size,
            "sha256": sha256(NATIVE_EXTENSION),
        },
    }
    (OUT / "MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT / "README_课程Notebook_Linux_CP39.md").write_text(
        "# 课程 Notebook 测试包（Linux x64 / CPython 3.9）\n\n"
        "解压到课程平台的 `/readme/` 文件夹后，先使用菜单 `Run -> Start Curling Server`，"
        "再在一个代码单元中以本次页面显示的 ConnectKey 运行：\n\n"
        "```python\n"
        "import runpy, sys\n"
        "sys.argv = [\n"
        "    'planner_submission_direct.py',\n"
        "    '-H', 'curling-server-7788.jupyterhub.svc.cluster.local',\n"
        "    '-p', '7788',\n"
        "    '-k', '在这里粘贴本次 ConnectionInfo 的 ConnectKey',\n"
        "    '--verbose',\n"
        "]\n"
        "runpy.run_path('planner_submission_direct.py', run_name='__main__')\n"
        "```\n\n"
        "本包是 Linux CP39 专用，不可用于 Windows CP313 比赛工作器；"
        "Windows 工作器请继续使用原有 CP313 `.pyd` 包。\n",
        encoding="utf-8",
    )
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(OUT.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(OUT).as_posix())
    print(json.dumps({"archive": str(ARCHIVE), "native_sha256": sha256(NATIVE_EXTENSION)}, ensure_ascii=False))


if __name__ == "__main__":
    build()
