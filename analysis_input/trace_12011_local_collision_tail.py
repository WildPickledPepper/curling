"""Trace the native local Scene after sample 12011's first contact.

Uses the archived full-session audit without changing its physics inputs.
"""

from __future__ import annotations

import json
import math
import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from local_simulator.runtime_loader import install_bundled_pyphysx

install_bundled_pyphysx()

SOURCE = ROOT / "research_archive/unity_reverse/source/reverse/audit_hybrid_p6_endpoint_sixshot.py"
DATA = ROOT / "research_archive/unity_reverse/evidence/data/calibration/extended_collision_validation_20260715_ordered"
EVENTS = ROOT / "research_archive/unity_reverse/evidence/log/extended_collision_validation_20260715_ordered/collision_unique_targets_batch_r03/unity_runtime_probe_20260715_125420/events.jsonl"
OUTPUT = ROOT / "analysis_input/simulator_alignment_12011_local_tail_20260929.json"
AUDIT = ROOT / "analysis_input/simulator_alignment_12011_trace_audit_20260929.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inject-frame12", choices=("none", "position", "quaternion", "pose", "velocity", "all"), default="none")
    parser.add_argument("--a10-exact", action="store_true")
    parser.add_argument("--a10-all", action="store_true")
    parser.add_argument("--release-native-origin", action="store_true")
    parser.add_argument("--release-unity-height", action="store_true")
    parser.add_argument("--zero-setter-x", action="store_true")
    parser.add_argument("--direct-quat-rotate-setter", action="store_true")
    parser.add_argument("--projected-quat-setter", action="store_true")
    parser.add_argument("--zero-vertical-setter", action="store_true")
    parser.add_argument("--production-alignment", action="store_true")
    parser.add_argument("--exact-setter-only", action="store_true")
    parser.add_argument("--trace-sample-id", type=int, default=12011)
    parser.add_argument("--inject-precontact", choices=("none", "position", "pose", "all"), default="none")
    opts = parser.parse_args()
    trace_active = opts.trace_sample_id % 2
    trace_target = opts.trace_sample_id - 11998
    if opts.trace_sample_id not in range(12000, 12012):
        raise ValueError("trace sample must be one of the ordered batch 12000..12011")
    audit_output = AUDIT.with_name(
        AUDIT.stem + f"_frame12_{opts.inject_frame12}_pre_{opts.inject_precontact}"
        + ("_a10" if opts.a10_exact else "")
        + ("_a10_all" if opts.a10_all else "")
        + ("_release_native" if opts.release_native_origin else "")
        + ("_release_height" if opts.release_unity_height else "")
        + ("_zero_setter_x" if opts.zero_setter_x else "")
        + ("_direct_rotate" if opts.direct_quat_rotate_setter else "")
        + ("_projected_quat" if opts.projected_quat_setter else "") + AUDIT.suffix
    )
    if opts.zero_vertical_setter:
        audit_output = audit_output.with_name(audit_output.stem + "_zero_vertical" + audit_output.suffix)
    if opts.production_alignment:
        audit_output = audit_output.with_name(audit_output.stem + "_production_alignment" + audit_output.suffix)
    if opts.exact_setter_only:
        audit_output = audit_output.with_name(audit_output.stem + "_exact_setter_only" + audit_output.suffix)
    if opts.trace_sample_id != 12011:
        audit_output = audit_output.with_name(audit_output.stem + f"_sample_{opts.trace_sample_id}" + audit_output.suffix)
    unity_core = None
    pre_core = None
    if opts.inject_frame12 != "none" or opts.inject_precontact != "none":
        event_path = next((ROOT / "analysis_input/unity_12011_first_solver_poll_long_20260929/logs").glob("*/events.jsonl"))
        frames = [json.loads(line)["data"] for line in event_path.open(encoding="utf-8")
                  if '"type":"c04.dynamic_solver_frame"' in line or '"type": "c04.dynamic_solver_frame"' in line]
        assert len(frames) == 40
        unity_core = frames[12]["exitCores"][1]["decodedCandidate"]
        pre_core = frames[0]["exitCores"][1]["decodedCandidate"]
    code = SOURCE.read_text(encoding="utf-8")
    start = code.index("    if sys.version_info[:2] != (3, 8)")
    stop = code.index("    samples = _load_jsonl", start)
    code = code[:start] + (
        "    from tools.reverse.front_half_pcm_replay import event_shot_groups, load_jsonl\n"
        "    from local_simulator.unity_physx import NativePyphysxMotionStepper, PersistentPhysxFrontHalfScene\n"
    ) + code[stop:]
    original = (
        "            scene.scene.simulate(scene.dt)\n"
        "            scene.scene.get_contact_reports()\n"
        "            row[\"settle\"] = _settle(scene)"
    )
    replacement = (
        "            scene.scene.simulate(scene.dt)\n"
        "            scene.scene.get_contact_reports()\n"
        "            _record(scene, 'first_writeback')\n"
        "            row[\"settle\"] = _settle(scene)"
    )
    assert code.count(original) == 1
    code = code.replace(original, replacement)
    ns = {"__name__": "local_tail_trace", "__file__": str(SOURCE)}
    exec(compile(code, str(SOURCE), "exec"), ns)
    import local_simulator.unity_physx as up
    original_init = up.PersistentPhysxFrontHalfScene.__init__
    if opts.zero_vertical_setter or opts.production_alignment or opts.exact_setter_only:
        def init_zero_vertical(self, *args, **kwargs):
            if opts.zero_vertical_setter or opts.production_alignment:
                kwargs["custom_sliding_zero_vertical_setter"] = True
            if opts.production_alignment:
                kwargs["emulate_unity_native_angular_setter_rotation"] = True
                kwargs["emulate_unity_native_angular_setter_tilt_only"] = False
                kwargs["emulate_unity_bestshot_release_pose"] = True
            if opts.exact_setter_only:
                kwargs["emulate_unity_native_angular_setter_rotation"] = True
                kwargs["emulate_unity_native_angular_setter_tilt_only"] = False
            return original_init(self, *args, **kwargs)
        up.PersistentPhysxFrontHalfScene.__init__ = init_zero_vertical
    setter_inputs: list[float] = []
    original_tilt_setter = up.PersistentPhysxFrontHalfScene._unity_native_angular_setter_tilt_vector
    if opts.direct_quat_rotate_setter or opts.projected_quat_setter:
        def direct_rotate(self, slot, angular_y):
            if slot.index == trace_active and self.slots[trace_target].enabled:
                setter_inputs.append(float(angular_y))
            _p, quat = slot.body.get_global_pose()
            f = self.probe.np.float32
            x, y, z, w = (f(quat.x), f(quat.y), f(quat.z), f(quat.w))
            def rotate(q, v):
                qx, qy, qz, qw = q
                vx, vy, vz = (f(f(2.0) * a) for a in v)
                w2 = f(f(qw * qw) - f(0.5))
                dot2 = f(f(f(qx * vx) + f(qy * vy)) + f(qz * vz))
                return (
                    f(f(f(vx * w2) + f(f(qy * vz) - f(qz * vy)) * qw) + f(qx * dot2)),
                    f(f(f(vy * w2) + f(f(qz * vx) - f(qx * vz)) * qw) + f(qy * dot2)),
                    f(f(f(vz * w2) + f(f(qx * vy) - f(qy * vx)) * qw) + f(qz * dot2)),
                )
            q = (x, y, z, w)
            angular = f(angular_y)
            if opts.projected_quat_setter:
                inverse = rotate((f(-x), f(-y), f(-z), w), (f(0), angular, f(0)))
                vector = rotate(q, (f(0), inverse[1], f(0)))
            else:
                vector = rotate(q, (f(0), angular, f(0)))
            return [float(a) for a in vector]
        up.PersistentPhysxFrontHalfScene._unity_native_angular_setter_tilt_vector = direct_rotate
    elif opts.zero_setter_x:
        def zero_x(self, slot, angular_y):
            result = original_tilt_setter(self, slot, angular_y)
            result[0] = 0.0
            return result
        up.PersistentPhysxFrontHalfScene._unity_native_angular_setter_tilt_vector = zero_x
    original_sliding = up.PersistentPhysxFrontHalfScene.step_custom_sliding
    precontact: list[dict] = []
    pre_inputs: list[dict] = []
    pre_setters: list[dict] = []
    release_state: list[dict] = []

    def trace_sliding(self, active_index, noise, *args, **kwargs):
        if active_index == trace_active and self.slots[trace_target].enabled and not precontact:
            release_state.append(self.state(active_index))
        if active_index == trace_active and self.slots[trace_target].enabled:
            pre_inputs.append(self.state(active_index))
        result = original_sliding(self, active_index, noise, *args, **kwargs)
        if active_index == trace_active and self.slots[trace_target].enabled:
            precontact.append(result["afterScene"])
            pre_setters.append(result["beforeScene"])
            if len(precontact) == 899 and pre_core is not None and opts.inject_precontact != "none":
                body = self.slots[active_index].body
                state = self.state(active_index)
                quat = pre_core["q"] if opts.inject_precontact in ("pose", "all") else [state["quaternionWxyz"][i] for i in (1, 2, 3, 0)]
                body.set_global_pose((pre_core["p"], [quat[3], quat[0], quat[1], quat[2]]))
                if opts.inject_precontact == "all":
                    body.set_linear_velocity(pre_core["linearVelocity"])
                    body.set_angular_velocity(pre_core["angularVelocity"])
        return result

    up.PersistentPhysxFrontHalfScene.step_custom_sliding = trace_sliding
    if opts.a10_exact or opts.a10_all or opts.release_native_origin or opts.release_unity_height:
        original_start = up.PersistentPhysxFrontHalfScene.start_bestshot
        a10_quat = [-2.4462851300199873e-08, 0.9300537109375,
                    6.192122015136192e-08, -0.3674236834049225]
        all_a10 = json.loads((DATA / "collision_unique_targets_batch_r03_orientation.json").read_text(encoding="utf-8"))["samples"]

        def start_exact(self, active_index, shot, *args, **kwargs):
            result = original_start(self, active_index, shot, *args, **kwargs)
            if opts.release_native_origin or opts.release_unity_height:
                state = self.state(active_index)
                p = state["physxPosition"]
                if opts.release_native_origin:
                    p[0] = float(self.probe.np.float32(up.UNITY_NATIVE_ORIGIN_X - 32.4768))
                if opts.release_unity_height:
                    p[1] = 14.43239974975586
                self.slots[active_index].body.set_global_pose((p, state["quaternionWxyz"]))
            if opts.a10_all or (opts.a10_exact and active_index == 1 and self.slots[13].enabled):
                state = self.state(active_index)
                if opts.a10_all:
                    target_indices = [slot.index for slot in self.slots if slot.enabled and slot.index >= 2]
                    assert len(target_indices) == 1, target_indices
                    quat = all_a10[str(11998 + target_indices[0])]["a10"]["nativeQuaternion"]
                else:
                    quat = a10_quat
                x, y, z, w = quat
                self.slots[active_index].body.set_global_pose(
                    (state["physxPosition"], [w, x, y, z]))
                if opts.production_alignment or opts.projected_quat_setter:
                    # The diagnostic A10 injection changes the pose *after*
                    # BESTSHOT's reset setter. Re-run that setter using the
                    # injected pose. Replace the original reset call in the
                    # Transform-sync counter rather than counting both calls.
                    self._unity_angular_setter_calls[active_index] = 0
                    self.slots[active_index].body.set_angular_velocity(
                        self._unity_native_angular_setter_vector(
                            self.slots[active_index], float(shot[2])
                        )
                    )
            return result

        up.PersistentPhysxFrontHalfScene.start_bestshot = start_exact
    trace: list[dict] = []

    def record(scene, phase):
        if scene.slots[trace_active].enabled and scene.slots[trace_target].enabled and len(trace) < 300:
            if phase == "first_writeback" and unity_core is not None:
                body = scene.slots[trace_active].body
                if opts.inject_frame12 in ("position", "quaternion", "pose", "all"):
                    state = scene.state(trace_active)
                    quat = (unity_core["q"] if opts.inject_frame12 in ("pose", "all") else
                            [state["quaternionWxyz"][i] for i in (1, 2, 3, 0)])
                    if opts.inject_frame12 == "quaternion":
                        quat = unity_core["q"]
                    position = state["physxPosition"] if opts.inject_frame12 == "quaternion" else unity_core["p"]
                    body.set_global_pose((position, [quat[3], quat[0], quat[1], quat[2]]))
                if opts.inject_frame12 in ("velocity", "all"):
                    body.set_linear_velocity(unity_core["linearVelocity"])
                    body.set_angular_velocity(unity_core["angularVelocity"])
            trace.append({"phase": phase, "active": scene.state(trace_active), "target": scene.state(trace_target)})

    def settle(scene, *, max_steps=6000):
        quiet = 0
        moving = []
        for step in range(1, max_steps + 1):
            scene.scene.simulate(scene.dt)
            scene.scene.get_contact_reports()
            record(scene, step)
            moving = []
            for slot in scene.slots:
                if not slot.enabled:
                    continue
                state = scene.state(slot.index)
                linear = math.sqrt(state["vx"] ** 2 + state["vy"] ** 2 + state["vz"] ** 2)
                angular = math.sqrt(state["wx"] ** 2 + state["wy"] ** 2 + state["w"] ** 2)
                if linear > 0.01 or angular > 0.01:
                    moving.append(slot.index)
            quiet = quiet + 1 if not moving else 0
            if quiet >= 20:
                return {"settled": True, "steps": step, "movingIndices": []}
        return {"settled": False, "steps": max_steps, "movingIndices": moving}

    ns["_record"] = record
    ns["_settle"] = settle
    old_argv = sys.argv
    try:
        sys.argv = [str(SOURCE), "--samples", str(DATA / "collision_unique_targets_batch_r03.jsonl"),
                    "--events", str(EVENTS), "--orientation-manifest",
                    str(DATA / "collision_unique_targets_batch_r03_orientation.json"),
                    "--require-orientation-truth", "--motion-kernel", "native-pyphysx",
                    "--output", str(audit_output)]
        ns["main"]()
    finally:
        sys.argv = old_argv
        up.PersistentPhysxFrontHalfScene.step_custom_sliding = original_sliding
        up.PersistentPhysxFrontHalfScene.__init__ = original_init
        if opts.a10_exact or opts.a10_all or opts.release_native_origin or opts.release_unity_height:
            up.PersistentPhysxFrontHalfScene.start_bestshot = original_start
        up.PersistentPhysxFrontHalfScene._unity_native_angular_setter_tilt_vector = original_tilt_setter
    trace_output = OUTPUT if opts.inject_frame12 == "none" else OUTPUT.with_name(OUTPUT.stem + "_" + opts.inject_frame12 + OUTPUT.suffix)
    if opts.a10_exact:
        trace_output = trace_output.with_name(trace_output.stem + "_a10" + trace_output.suffix)
    if opts.a10_all:
        trace_output = trace_output.with_name(trace_output.stem + "_a10_all" + trace_output.suffix)
    if opts.release_native_origin:
        trace_output = trace_output.with_name(trace_output.stem + "_release_native" + trace_output.suffix)
    if opts.release_unity_height:
        trace_output = trace_output.with_name(trace_output.stem + "_release_height" + trace_output.suffix)
    if opts.zero_setter_x:
        trace_output = trace_output.with_name(trace_output.stem + "_zero_setter_x" + trace_output.suffix)
    if opts.direct_quat_rotate_setter:
        trace_output = trace_output.with_name(trace_output.stem + "_direct_rotate" + trace_output.suffix)
    if opts.projected_quat_setter:
        trace_output = trace_output.with_name(trace_output.stem + "_projected_quat" + trace_output.suffix)
    if opts.zero_vertical_setter:
        trace_output = trace_output.with_name(trace_output.stem + "_zero_vertical" + trace_output.suffix)
    if opts.production_alignment:
        trace_output = trace_output.with_name(trace_output.stem + "_production_alignment" + trace_output.suffix)
    if opts.exact_setter_only:
        trace_output = trace_output.with_name(trace_output.stem + "_exact_setter_only" + trace_output.suffix)
    if opts.trace_sample_id != 12011:
        trace_output = trace_output.with_name(trace_output.stem + f"_sample_{opts.trace_sample_id}" + trace_output.suffix)
    if opts.inject_precontact != "none":
        trace_output = trace_output.with_name(trace_output.stem + "_pre_" + opts.inject_precontact + trace_output.suffix)
    trace_output.write_text(json.dumps(trace, ensure_ascii=False) + "\n", encoding="utf-8")
    if opts.inject_frame12 == "none":
        pre_output = trace_output.with_name(trace_output.stem + "_precontact" + trace_output.suffix)
        pre_output.write_text(json.dumps(precontact, ensure_ascii=False) + "\n", encoding="utf-8")
        input_output = trace_output.with_name(trace_output.stem + "_inputs" + trace_output.suffix)
        input_output.write_text(json.dumps(pre_inputs, ensure_ascii=False) + "\n", encoding="utf-8")
        setter_output = trace_output.with_name(trace_output.stem + "_setters" + trace_output.suffix)
        setter_output.write_text(json.dumps(pre_setters, ensure_ascii=False) + "\n", encoding="utf-8")
        if opts.direct_quat_rotate_setter or opts.projected_quat_setter:
            scalar_output = trace_output.with_name(trace_output.stem + "_scalar_setters" + trace_output.suffix)
            scalar_output.write_text(json.dumps(setter_inputs, ensure_ascii=False) + "\n", encoding="utf-8")
        release_output = trace_output.with_name(trace_output.stem + "_release" + trace_output.suffix)
        release_output.write_text(json.dumps(release_state, ensure_ascii=False) + "\n", encoding="utf-8")
    row = next(item for item in json.loads(audit_output.read_text(encoding="utf-8"))["rows"] if item["sampleId"] == opts.trace_sample_id)
    print(json.dumps({"trace": str(trace_output), "frames": len(trace), "case": opts.inject_frame12,
                      "precontactCase": opts.inject_precontact,
                      "endpointErrorM": row["endpointErrorM"], "localEndpoint": row["localEndpoint"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
