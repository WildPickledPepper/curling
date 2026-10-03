#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成面向比赛服务器 Windows x64 / CPython 3.13 的最小 PhysX 包。"""
from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROXY = ROOT / "planning_proxy"
NAME = "server_py313_physx_state_machine_20260721"
OUT = PROXY / NAME
ARCHIVE = PROXY / f"{NAME}.zip"
STAGE = OUT / ".stage"
PAYLOAD = OUT / "planner_payload.zip"
CP313_EXTENSION = ROOT / "local_simulator" / "runtime" / "pyphysx" / "_pyphysx.cp313-win_amd64.pyd"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def copy(source: Path) -> None:
    target = STAGE / source.relative_to(ROOT)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def source_files() -> list[Path]:
    core = [
        PROXY / name for name in (
            "analytic_proxy.py", "competition_rules.py", "endgame_shapes.py",
            "evaluate_vs_teammate_ppo.py", "first_player_strategy.py",
            "strict_refine.py", "unity_planner_robot.py",
        )
    ]
    simulator = ROOT / "local_simulator"
    files: list[Path] = []
    for path in simulator.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(simulator)
        if rel.parts[:2] == ("runtime", "wheels"):
            continue
        if path.suffix == ".py" or rel.parts[0] in {"assets", "runtime_support"}:
            files.append(path)
    # 不复制目录中同时存在的 CP38 扩展；服务器日志已确认其 ABI 是 CP313。
    files.extend([
        simulator / "runtime" / "pyphysx" / "__init__.py",
        simulator / "runtime" / "pyphysx" / "quaternion.py",
        CP313_EXTENSION,
    ])
    return core + sorted(set(files))


def write_entry() -> Path:
    text = (PROXY / "planner_submission.py").read_text(encoding="utf-8")
    needle = '"--decision-budget-seconds": "90",'
    if needle not in text:
        raise RuntimeError("入口默认预算与预期不符，拒绝生成。")
    path = OUT / "planner_submission.py"
    path.write_text(text.replace(needle, '"--decision-budget-seconds": "105",', 1), encoding="utf-8")
    return path


def build() -> None:
    if OUT.exists() or ARCHIVE.exists():
        raise RuntimeError(f"输出已存在，拒绝覆盖：{OUT} 或 {ARCHIVE}")
    if not CP313_EXTENSION.is_file():
        raise RuntimeError(f"缺少 CPython 3.13 扩展：{CP313_EXTENSION}")
    OUT.mkdir(parents=True)
    STAGE.mkdir()
    files = source_files()
    try:
        for path in files:
            copy(path)
        with zipfile.ZipFile(PAYLOAD, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in sorted(STAGE.rglob("*")):
                if path.is_file():
                    archive.write(path, path.relative_to(STAGE).as_posix())
        entry = write_entry()
        readme = OUT / "README_服务器_CP313.md"
        readme.write_text(
            "# 服务器部署包：Windows x64 / CPython 3.13\n\n"
            "依据平台回传：`runtime_soabi=cp313-win_amd64`。本包只包含 "
            "`_pyphysx.cp313-win_amd64.pyd`，不包含 CP38 原生扩展。\n\n"
            "上传或解压时必须把下列两个文件保持在同一目录：\n\n"
            "- `planner_submission.py`\n- `planner_payload.zip`\n\n"
            "选择 `planner_submission.py` 作为机器人入口。它会在运行目录创建 `.planner_runtime`，"
            "解压内层载荷后按当前 Python ABI 加载 PhysX 扩展。默认单手规划预算为 105 秒。\n\n"
            "注意：平台探针曾显示根目录 `.pyd` 未被保留；因此原生扩展放在内层 "
            "`planner_payload.zip`，由入口运行时解压。不要把 `.pyd` 单独放在上传根目录。\n",
            encoding="utf-8",
        )
        manifest = {
            "package": NAME,
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "target": {
                "platform": "win32 / Windows x64",
                "python": "3.13.5",
                "soabi": "cp313-win_amd64",
            },
            "decision_budget_seconds": 105,
            "entrypoint": entry.name,
            "cp313_extension": {
                "payload_path": "local_simulator/runtime/pyphysx/_pyphysx.cp313-win_amd64.pyd",
                "bytes": CP313_EXTENSION.stat().st_size,
                "sha256": sha256(CP313_EXTENSION),
            },
            "payload": {"name": PAYLOAD.name, "bytes": PAYLOAD.stat().st_size, "sha256": sha256(PAYLOAD)},
        }
        (OUT / "MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in sorted(OUT.rglob("*")):
                if path.is_file() and STAGE not in path.parents:
                    archive.write(path, (Path(NAME) / path.relative_to(OUT)).as_posix())
    finally:
        if STAGE.exists():
            shutil.rmtree(STAGE)
    print(json.dumps({"archive": str(ARCHIVE), "payload_mib": round(PAYLOAD.stat().st_size / 1024 / 1024, 2), "cp313_sha256": sha256(CP313_EXTENSION)}, ensure_ascii=False))


if __name__ == "__main__":
    build()
