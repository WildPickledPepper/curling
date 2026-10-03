#!/usr/bin/env python3
"""从严格多种子已验证解构造非平凡的局部收敛初值集。

用途是隔离“已有正确碰撞盆地附近的初值后，局部算法能否收敛”。每个初值
是对历史三种子通过解施加固定扰动后的球，而不是把验证解直接作为输入。
它不适合衡量粗代理覆盖率；入口覆盖仍应使用分层审计集。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PERTURBATIONS = ((0.072, -0.060, 0.80), (-0.084, 0.048, -1.00))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument(
        "--perturbation-scale", type=float, default=1.0,
        help="固定扰动的缩放系数；必须大于 0，且应小于等于 1 以保持局部测试性质。",
    )
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else (ROOT / path).resolve()


def verified(row: dict[str, Any]) -> bool:
    return all(bool(row.get(name, False)) for name in (
        "ruleLegal", "targetNeutralized", "innerAnchor", "lossBudgetOk", "allSeedContractMet",
    ))


def clamp(values: tuple[float, float, float]) -> list[float]:
    v, h, w = values
    return [min(6.0, max(1.0, v)), min(2.23, max(-2.23, h)), min(15.7, max(-15.7, w))]


def main() -> int:
    args = parse_args()
    if args.perturbation_scale <= 0 or args.perturbation_scale > 1.0:
        raise SystemExit("--perturbation-scale 必须在 (0, 1] 内")
    audit_path = resolve(args.audit)
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    roots = [row for row in audit.get("multiSeedRows", ()) if verified(row)]
    if not roots:
        raise SystemExit("审计中没有三种子严格通过的根解")

    rows: list[dict[str, Any]] = []
    for root in roots:
        solution = tuple(float(value) for value in root["bestshot"])
        for perturbation_index, delta in enumerate(PERTURBATIONS, 1):
            scaled_delta = tuple(float(value) * float(args.perturbation_scale) for value in delta)
            start = clamp(tuple(solution[index] + scaled_delta[index] for index in range(3)))
            rows.append({
                "rank": len(rows) + 1,
                "rootPrimaryRank": int(root["primaryRank"]),
                "verifiedRootShot": list(solution),
                "perturbation": list(scaled_delta),
                "rawBestshot": start,
            })

    output: dict[str, Any] = {
        "schema": "verified_basin_local_convergence_initials_v1",
        "scope": (
            "局部收敛质量测试：每条输入来自同一合同下三物理种子已验证根解的固定扰动；"
            "不用于声明粗代理覆盖能力，也不接入生产。"
        ),
        "sourceAudit": str(audit_path),
        "sourceReport": audit["sourceReport"],
        "shot": int(audit["shot"]),
        "physicsSeeds": [int(value) for value in audit["physicsSeeds"]],
        "plan": audit["plan"],
        "rootCount": len(roots),
        "perturbationScale": float(args.perturbation_scale),
        "perturbations": [[float(value) * float(args.perturbation_scale) for value in values] for values in PERTURBATIONS],
        "primaryRows": rows,
    }
    output_path = resolve(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"roots": len(roots), "initials": len(rows), "output": str(output_path)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
