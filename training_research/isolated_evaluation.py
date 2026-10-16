"""Restore observed activation/material inputs before counterfactual resets.

No physical calculations are changed. The template is obtained by executing
the ordinary complete-shot lifecycle, rather than inventing friction values.
"""
from __future__ import annotations

import time


def capture_context(env):
    return [{"index": s.index, "unity_constraints": int(s.unity_constraints),
             "static_friction": float(s.material.get_static_friction()),
             "dynamic_friction": float(s.material.get_dynamic_friction()),
             "restitution": float(s.material.get_restitution())} for s in env.scene.slots]


def restore_context(env, context):
    if [s["index"] for s in context] != list(range(len(env.scene.slots))):
        raise ValueError("activation context must cover all original slots")
    for saved, slot in zip(context, env.scene.slots):
        slot.unity_constraints = saved["unity_constraints"]
        slot.material.set_static_friction(saved["static_friction"])
        slot.material.set_dynamic_friction(saved["dynamic_friction"])
        slot.material.set_restitution(saved["restitution"])


def observed_mature_context():
    """Query-independent startup: run each slot through normal release/stop."""
    from training_research.inverse_dataset.cli import make_environment, reset_environment
    started = time.perf_counter()
    env = make_environment()
    for index in range(16):
        reset_environment(env, {"active_index": index, "stones": []}, 1000+index)
        result = env.play((3., 0., 0.))
        if not result["settled"]:
            raise RuntimeError("startup lifecycle did not complete")
    env.scene.reset_positions([0.]*32, yaw_overrides={i: 0. for i in range(16)})
    return {"slots": capture_context(env), "setup_seconds": time.perf_counter()-started,
            "provenance": "16 normal empty-board release/stop lifecycles at program startup; original simulator code and read-back native materials/component flags. Not an added benchmark test set."}
