#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""量化一条对方末手反击是否只是针尖参数，还是有足够大的成功盆地。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd  # noqa: E402
from local_simulator.runtime_loader import install_bundled_pyphysx  # noqa: E402
from planning_proxy.strict_refine import Candidate, evaluate_one, make_position  # noqa: E402
from planning_proxy.validate_final_defence import ACTIVE_INDEX, DEFENCE_FIXTURES, _seed_is_safe  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", required=True, choices=[item.name for item in DEFENCE_FIXTURES])
    parser.add_argument("--shot", required=True, type=float, nargs=3, metavar=("V0", "H0", "W0"))
    parser.add_argument("--dv", type=float, default=0.06)
    parser.add_argument("--dh", type=float, default=0.06)
    parser.add_argument("--dw", type=float, default=0.75)
    parser.add_argument("--physics-seeds", type=int, default=9)
    parser.add_argument("--seed", type=int, default=20260716)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if min(args.dv, args.dh, args.dw, args.physics_seeds) <= 0:
        raise SystemExit("扰动半径和摩擦序列数必须为正")
    fixture = next(item for item in DEFENCE_FIXTURES if item.name == args.fixture)
    seeds = [args.seed + index * 7919 for index in range(args.physics_seeds)]
    install_bundled_pyphysx()
    environment = StrictCurlingEnd(seed=args.seed, training_fast=True)
    position = make_position(fixture.stones)
    own_indices = {stone.index for stone in fixture.stones}
    v0, h0, w0 = args.shot
    rows = []
    total_breaches = 0
    stable_breach_candidates = 0
    for dv in (-args.dv, 0.0, args.dv):
        for dh in (-args.dh, 0.0, args.dh):
            for dw in (-args.dw, 0.0, args.dw):
                candidate = Candidate(v0 + dv, h0 + dh, w0 + dw, parent_rank=0)
                result = evaluate_one(
                    environment, candidate, fixture.stones, position, seeds,
                    shot_index=15, active_index=ACTIVE_INDEX,
                )
                seed_checks = [_seed_is_safe(item, own_indices) for item in result.final_center_distance_by_index]
                breach_count = sum(not item[0] for item in seed_checks)
                total_breaches += breach_count
                stable_breach_candidates += int(breach_count == len(seeds))
                centre_distances = [item[2] for item in seed_checks if item[2] is not None]
                centre_advantages = [
                    item[3] - item[2] for item in seed_checks
                    if item[2] is not None and item[3] is not None
                ]
                rows.append({
                    "bestshot": [candidate.v0, candidate.h0, candidate.w0],
                    "breachSeedCount": breach_count,
                    "seedCount": len(seeds),
                    "worstOpponentDistanceM": None if not centre_distances else min(centre_distances),
                    "largestOpponentCentreAdvantageM": None if not centre_advantages else max(centre_advantages),
                })
    total_outcomes = len(rows) * len(seeds)
    payload = {
        "fixture": args.fixture,
        "centreShot": [v0, h0, w0],
        "perturbation": {"dv": args.dv, "dh": args.dh, "dw": args.dw},
        "candidateCount": len(rows),
        "physicsSeedsPerCandidate": len(seeds),
        "breachOutcomeCount": total_breaches,
        "breachOutcomeRate": total_breaches / total_outcomes,
        "breachCandidateCount": sum(item["breachSeedCount"] > 0 for item in rows),
        "stableBreachCandidateCount": stable_breach_candidates,
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"{args.fixture}: {total_breaches}/{total_outcomes} 个扰动-摩擦组合反超；"
        f"稳定反超输入 {stable_breach_candidates}/{len(rows)}；report={args.output}"
    )


if __name__ == "__main__":
    main()
