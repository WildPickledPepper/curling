#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把当前工作树的先手状态机封装成可交给队友的独立对手包。

故意不复用 ``submission/`` 或 ``submission_direct/``，避免覆盖其他会话已生成的
交付物。该脚本拒绝覆盖同名输出目录；需要重建时应先人工确认并改包名。
"""
from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "planning_proxy"
PACKAGE_NAME = "teammate_state_machine_package_20260721"
OUT = SOURCE / PACKAGE_NAME
ARCHIVE = SOURCE / f"{PACKAGE_NAME}.zip"
STAGE = OUT / ".payload_stage"
PAYLOAD = OUT / "planner_payload.zip"


def copy_file(source: Path, target_root: Path) -> Path:
    target = target_root / source.relative_to(ROOT)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return target


def planner_files() -> list[Path]:
    names = (
        "analytic_proxy.py", "competition_rules.py", "endgame_shapes.py",
        "evaluate_vs_teammate_ppo.py", "first_player_strategy.py",
        "strict_refine.py", "unity_planner_robot.py",
    )
    return [SOURCE / name for name in names]


def simulator_files() -> list[Path]:
    base = ROOT / "local_simulator"
    files: list[Path] = []
    for path in base.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(base)
        if relative.parts[:2] == ("runtime", "wheels"):
            continue
        if path.suffix == ".py" or relative.parts[0] in {"assets", "runtime_support"}:
            files.append(path)
        elif relative.parts[:2] == ("runtime", "pyphysx") and (
            path.name in {"__init__.py", "quaternion.py"}
            or (path.name.startswith("_pyphysx.cp") and path.name.endswith("-win_amd64.pyd"))
        ):
            files.append(path)
    return files


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_entrypoint() -> Path:
    text = (SOURCE / "planner_submission.py").read_text(encoding="utf-8")
    old = '"--decision-budget-seconds": "90",'
    new = '"--decision-budget-seconds": "105",'
    if old not in text:
        raise RuntimeError("未找到预期的 90 秒默认预算，拒绝生成不明入口。")
    text = text.replace(old, new, 1)
    entry = OUT / "planner_submission.py"
    entry.write_text(text, encoding="utf-8")
    return entry


def write_readme() -> Path:
    readme = OUT / "README_队友运行说明.md"
    readme.write_text(
        "# 当前先手状态机对手包\n\n"
        "这是当前工作树的 PhysX 先手状态机快照，可作为本地模拟器或 Unity 模拟器的对手。"
        "它不包含 PPO 权重，也不会读取历史动作或测试 witness。\n\n"
        "解压后保持 `planner_submission.py` 与 `planner_payload.zip` 同一目录，运行：\n\n"
        "```powershell\n"
        "python planner_submission.py --host 127.0.0.1 --port 7788 --key <比赛密钥> --name PhysXStateMachine\n"
        "```\n\n"
        "入口默认每手规划预算为 105 秒；规划器内部仍保留返回余量，目标是在平台 120 秒限制内返回。"
        "首次启动会在当前目录解压 `.planner_runtime`。仅支持 Windows x64，且比赛端须使用包内提供原生扩展对应的 CPython 版本。\n\n"
        "`MANIFEST.json` 记录本包来自哪些当前源文件及其 SHA-256。此包是当前代码快照，不表示对任何对手或所有物理种子的必胜承诺。\n",
        encoding="utf-8",
    )
    return readme


def build() -> None:
    if OUT.exists() or ARCHIVE.exists():
        raise RuntimeError(f"输出已存在，拒绝覆盖：{OUT} 或 {ARCHIVE}")
    OUT.mkdir(parents=True)
    STAGE.mkdir()
    source_files = planner_files() + simulator_files()
    copied: list[Path] = []
    try:
        for source in source_files:
            copied.append(copy_file(source, STAGE))
        with zipfile.ZipFile(PAYLOAD, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in sorted(STAGE.rglob("*")):
                if path.is_file():
                    archive.write(path, path.relative_to(STAGE).as_posix())
        entry = write_entrypoint()
        readme = write_readme()
        manifest = {
            "package": PACKAGE_NAME,
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "purpose": "当前先手状态机的队友本地/Unity 对手包。",
            "decision_budget_seconds": 105,
            "entrypoint": entry.name,
            "payload": {"name": PAYLOAD.name, "sha256": sha256(PAYLOAD), "bytes": PAYLOAD.stat().st_size},
            "source_files": [
                {"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path)}
                for path in sorted(source_files)
            ],
        }
        manifest_path = OUT / "MANIFEST.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in sorted(OUT.rglob("*")):
                if path.is_file() and STAGE not in path.parents:
                    archive.write(path, (Path(PACKAGE_NAME) / path.relative_to(OUT)).as_posix())
    finally:
        if STAGE.exists():
            shutil.rmtree(STAGE)
    print(json.dumps({
        "package_dir": str(OUT), "archive": str(ARCHIVE),
        "payload_mib": round(PAYLOAD.stat().st_size / 1024 / 1024, 2),
        "payload_sha256": sha256(PAYLOAD),
    }, ensure_ascii=False))


if __name__ == "__main__":
    build()
