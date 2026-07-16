#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""基准：连续数学粗代理一次可筛多少候选。"""

from __future__ import annotations

import time

import numpy as np

from analytic_proxy import (
    ProxyStone, attack_score, calibrate_force_lookup, calibrate_from_recovered_formula, make_initial_candidates,
    refine_candidates, simulate_batch,
)


def main() -> None:
    board = (
        ProxyStone(2, "self", 2.05, 7.25),
        ProxyStone(1, "opponent", 2.55, 5.45),
        ProxyStone(3, "opponent", 2.75, 4.72),
    )
    started = time.perf_counter()
    params = calibrate_from_recovered_formula()
    force_lookup = calibrate_force_lookup()
    calibration_seconds = time.perf_counter() - started
    initial = make_initial_candidates()
    started = time.perf_counter()
    first = simulate_batch(initial, board, params, force_lookup=force_lookup, dt=0.02)
    first_seconds = time.perf_counter() - started
    parent = first.shots[np.argsort(-attack_score(first))[:24]]
    refined_shots = refine_candidates(parent)
    started = time.perf_counter()
    refined = simulate_batch(refined_shots, board, params, force_lookup=force_lookup, dt=0.02)
    refined_seconds = time.perf_counter() - started
    print("calibration=%.6fs" % calibration_seconds)
    print("initial=%d candidates %.6fs" % (len(initial), first_seconds))
    print("refined=%d candidates %.6fs" % (len(refined_shots), refined_seconds))
    print("total=%d candidates %.6fs" % (len(initial) + len(refined_shots), calibration_seconds + first_seconds + refined_seconds))
    print("params drag_floor=%.6f drag_quadratic=%.6f spin_decay=%.6f curl=%.8f" % (
        params.drag_floor_mps2, params.drag_quadratic_per_m, params.spin_decay_per_s, params.curl_turn_per_m_per_spin
    ))
    print("force_lookup=%s" % force_lookup.metadata())
    print("top_first_hit=%s" % list(refined.first_hit_owner[np.argsort(-attack_score(refined))[:10]]))


if __name__ == "__main__":
    main()
