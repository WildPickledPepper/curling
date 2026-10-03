"""Replay C131 with explicit alignment profiles; record the release boundary."""
from __future__ import annotations

import argparse
import hashlib
import inspect
import json
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from local_simulator.runtime_loader import install_bundled_pyphysx, _resolve_bundled_extension


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", choices=("legacy", "exact", "launch", "vertical", "full", "full-q", "exact-q"))
    parser.add_argument("--trace", action="store_true")
    parser.add_argument("--cast-setter-pose", action="store_true")
    parser.add_argument("--sync-body-q", action="store_true")
    parser.add_argument("--sync-write-always", action="store_true")
    parser.add_argument("--solver-ordinal-min", type=int, default=2)
    parser.add_argument("--solver-ordinal-max", type=int, default=22)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--trace-constraints", action="store_true")
    parser.add_argument("--keep-multi-cache", action="store_true",
                        help="Diagnostic only: disable the existing Unity multi-cache lifecycle override.")
    parser.add_argument("--keep-pcm-task-cache", action="store_true")
    parser.add_argument("--float32-body-q", action="store_true",
                        help="Use f72606 reciprocal-multiply normalization instead of the legacy cast reader.")
    parser.add_argument("--direct-contact-probe", action="store_true")
    parser.add_argument("--post-dense-trace-frames", type=int, default=0,
                        help="Read-only trace starting at 11005's final dense setter, through the collision tail.")
    parser.add_argument("--native-trace-control", type=Path,
                        help="Bracket the first actual 11005 collision simulate for an external read-only observer.")
    parser.add_argument('--native-trace-ordinal',type=int,default=1023)
    parser.add_argument('--native-lifecycle-trace-control', type=Path)
    parser.add_argument("--native-trace-direct-pair", action="store_true",
                        help="Observe an isolated PCM query using the actual first-pair inputs/order, then simulate unchanged.")
    parser.add_argument("--direct-probe-scale-xz", type=float,
                        help="Isolated geometric query only: replay an observed Unity convex scale; never change the physical scene.")
    opts = parser.parse_args()
    install_bundled_pyphysx()
    import local_simulator.unity_physx as up
    source = ROOT / "research_archive/unity_reverse/source/reverse/audit_hybrid_p6_endpoint_sixshot.py"
    base = ROOT / "research_archive/unity_reverse/evidence"
    data = base / "data/calibration/c131_strict_yaw_r00_20260714"
    events = base / "log/c131_strict_yaw_r00_20260714/collision_unique_targets_batch_r00/unity_runtime_probe_20260714_173341/events.jsonl"
    manifest = json.loads((data / "orientation_manifest_r00.json").read_text(encoding="utf-8"))["samples"]
    samples = [json.loads(s) for s in (data / "collision_unique_targets_batch_r00.jsonl").read_text(encoding="utf-8").splitlines()]
    unity_releases = [json.loads(s)["data"] for s in events.read_text(encoding="utf-8").splitlines() if '"type": "a10.release_reset_orientation"' in s]
    assert len(samples) == len(unity_releases) == 12
    original_init = up.PersistentPhysxFrontHalfScene.__init__
    original_start = up.PersistentPhysxFrontHalfScene.start_bestshot
    original_run = up.PersistentPhysxFrontHalfScene.run_bestshot_to_first_contact
    releases = []
    current = {}
    effective_configuration = {}

    def init(self, *args, **kwargs):
        if opts.native_lifecycle_trace_control is not None:
            import ctypes, os, time
            control = opts.native_lifecycle_trace_control
            (control/'arm.json').write_text(json.dumps({'pid':os.getpid(),
                'threadId':ctypes.windll.kernel32.GetCurrentThreadId(),
                'module':str(_resolve_bundled_extension()),'scope':'startup-and-all-releases'}))
            deadline = time.monotonic()+90
            while not (control/'go').exists():
                if time.monotonic()>deadline: raise TimeoutError('lifecycle go')
                time.sleep(.05)
        kwargs["emulate_unity_native_angular_setter_rotation"] = opts.profile != "legacy"
        kwargs["emulate_unity_native_angular_setter_tilt_only"] = opts.profile == "legacy"
        kwargs["emulate_unity_bestshot_release_pose"] = opts.profile in ("launch", "full", "full-q")
        kwargs["custom_sliding_zero_vertical_setter"] = opts.profile in ("vertical", "full", "full-q")
        if opts.keep_multi_cache:
            kwargs["enable_unity_pcm_multi_cache_lifecycle"] = False
        if opts.keep_pcm_task_cache:
            kwargs["enable_unity_pcm_task_cache_lifecycle"] = False
        original_init(self, *args, **kwargs)
        if opts.direct_probe_scale_xz is not None:
            saved_scale = up.UNITY_STONE_SCALE_XZ
            try:
                up.UNITY_STONE_SCALE_XZ = opts.direct_probe_scale_xz
                query_scene = up.PersistentPhysxFrontHalfScene.__new__(up.PersistentPhysxFrontHalfScene)
                query_kwargs = dict(kwargs, stone_count=1)
                original_init(query_scene, *args, **query_kwargs)
                self._diagnostic_geometry_query_scene = query_scene
            finally:
                up.UNITY_STONE_SCALE_XZ = saved_scale
        effective_configuration.update(
            iceMesh=self.runtime_ice_mesh_meta,
            pcmTaskCacheLifecycle=self.enable_unity_pcm_task_cache_lifecycle,
            pcmMultiCacheLifecycle=self.enable_unity_pcm_multi_cache_lifecycle,
            releasePose=self.emulate_unity_bestshot_release_pose,
            zeroVerticalSetter=self.custom_sliding_zero_vertical_setter,
            transformScaleRefresh=self.emulate_unity_transform_scale_refresh,
            bodyPoseWriteback=self.emulate_unity_body_pose_writeback,
            setActiveNoSim=self.emulate_unity_setactive_no_sim,
        )
        if opts.sync_body_q:
            owner = self
            native_scene = self.scene
            class SyncScene:
                def __getattr__(self, name):
                    return getattr(native_scene, name)
                def simulate(self, dt):
                    index = current.get("activeIndex")
                    ordinal = owner._unity_angular_setter_calls.get(index, 0)
                    tail = None
                    if (opts.post_dense_trace_frames and current.get("sampleId") == 11005 and
                            ordinal >= opts.native_trace_ordinal and len(current.setdefault("postDenseFrames", [])) < opts.post_dense_trace_frames):
                        enabled = [slot.index for slot in owner.slots if slot.enabled]
                        tail = {"frameIndex":len(current["postDenseFrames"]),"ordinal":ordinal,
                            "before":{str(i):owner.raw_native_state(i) for i in enabled},
                            "activation":{str(i):owner.activation_audit_state(i) for i in enabled}}
                        for name in ("solver_setup", "solve_block", "solve_writeback", "narrowphase", "finalizer"):
                            getattr(owner.pyphysx,"clear_scene_"+name+"_trace")()
                            getattr(owner.pyphysx,"set_scene_"+name+"_trace_enabled")(True)
                    if (opts.direct_contact_probe and current.get("sampleId") == 11005 and
                            opts.solver_ordinal_min <= ordinal <= opts.solver_ordinal_max):
                        active = owner.slots[index]
                        query_row = {
                            "ordinal": ordinal,
                            "result": owner.pyphysx.generate_contacts_between(
                                active.body, active.shape, owner.ice, owner.ice.get_atached_shapes()[0],
                                0.02, 0.01, 1.0),
                        }
                        if opts.direct_probe_scale_xz is not None:
                            query_stone = owner._diagnostic_geometry_query_scene.slots[0]
                            query_stone.body.set_global_pose(active.body.get_global_pose())
                            query_row["observedUnityScaleXz"] = opts.direct_probe_scale_xz
                            query_row["matchedInputGeometryProbe"] = owner.pyphysx.generate_contacts_between(
                                query_stone.body, query_stone.shape, owner.ice, owner.ice.get_atached_shapes()[0],
                                0.02, 0.01, 1.0)
                        current.setdefault("directContacts", []).append(query_row)
                    control = opts.native_trace_control if (tail is not None and tail["frameIndex"] == 0) else None
                    if control is not None:
                        import ctypes, os, time
                        def await_observer(name):
                            deadline = time.monotonic() + 90
                            while not (control / name).exists():
                                if time.monotonic() > deadline:
                                    raise TimeoutError(name)
                                time.sleep(0.05)
                        request = {"pid":os.getpid(), "threadId":ctypes.windll.kernel32.GetCurrentThreadId(),
                            "sampleId":11005, "ordinal":ordinal, "module":str(_resolve_bundled_extension())}
                        (control / "arm.json").write_text(json.dumps(request),encoding="utf-8")
                        await_observer("go")
                    if control is not None and opts.native_trace_direct_pair:
                        # Match the actual native work-unit order (target,active).
                        target = owner.slots[7]
                        active = owner.slots[index]
                        tail["isolatedActualPair"] = owner.pyphysx.generate_contacts_between(
                            target.body,target.shape,active.body,active.shape,0.02,0.01,1.0)
                    else:
                        result = native_scene.simulate(dt)
                    if control is not None:
                        (control / "done").write_text("done",encoding="utf-8")
                        await_observer("resume")
                    if control is not None and opts.native_trace_direct_pair:
                        result = native_scene.simulate(dt)
                    if tail is not None:
                        tail["afterNative"] = {str(i):owner.raw_native_state(i) for i in enabled}
                        for name in ("solver_setup", "solve_block", "solve_writeback", "narrowphase", "finalizer"):
                            tail[name] = getattr(owner.pyphysx,"get_scene_"+name+"_trace")(False)
                            getattr(owner.pyphysx,"set_scene_"+name+"_trace_enabled")(False)
                        current["postDenseFrames"].append(tail)
                    if owner.emulate_unity_body_pose_writeback:
                        # The production step now performs the observed writeback
                        # after this diagnostic wrapper returns; do not do it twice.
                        return result
                    for slot in owner.slots:
                        if not slot.enabled or slot.body.is_sleeping():
                            continue
                        pose = slot.body.get_global_pose()
                        normalized = owner.pyphysx.cast_transformation(pose)
                        q, n = pose[1], normalized[1]
                        if opts.float32_body_q:
                            f = owner.probe.np.float32
                            x, y, z, w = (f(getattr(q, k)) for k in ("x", "y", "z", "w"))
                            norm2 = f(f(f(f(x*x) + f(y*y)) + f(z*z)) + f(w*w))
                            inv = f(f(1) / f(owner.probe.np.sqrt(norm2)))
                            import quaternion
                            n = quaternion.quaternion(*[float(f(v*inv)) for v in (w, x, y, z)])
                            normalized = (pose[0], n)
                        if opts.sync_write_always or any(getattr(q, k) != getattr(n, k) for k in ("x", "y", "z", "w")):
                            slot.body.set_global_pose(normalized)
                    return result
            self.scene = SyncScene()

    def start(self, active_index, shot, *args, **kwargs):
        i = len(releases)
        sample_id = samples[i]["sample_id"]
        current.clear()
        current.update(sampleId=sample_id, activeIndex=active_index, unity=unity_releases[i]["bridgePoseBeforeAngularSetter"]["transform"])
        current["ticks"] = []
        current["setters"] = []
        current["directContacts"] = []
        current["postDenseFrames"] = []
        original_yaw = self._yaw_quaternion
        q = manifest[str(sample_id)]["a10"]["nativeQuaternion"]
        if opts.profile in ("full-q", "exact-q"):
            self._yaw_quaternion = lambda yaw: [q[3], *q[:3]]
        try:
            result = original_start(self, active_index, shot, *args, **kwargs)
            current["localAfterRelease"] = self.state(active_index)
            current["localGeometryScale"] = self.slots[active_index].shape.get_convex_mesh_data()["scale"]
            releases.append(dict(current))
            return result
        finally:
            self._yaw_quaternion = original_yaw

    def run(self, *args, **kwargs):
        result = original_run(self, *args, **kwargs)
        releases[-1]['firstContactRoleOrder'] = [
            [r['stoneIndex0'], r['stoneIndex1']]
            for r in result.get('firstContactReports', [])]
        return result

    original_setter = up.PersistentPhysxFrontHalfScene._unity_native_angular_setter_vector
    original_projection = up.PersistentPhysxFrontHalfScene._unity_project_locked_angular_velocity
    last_projection = {}
    def projection(self, q, angular_y):
        last_projection.update(q=[float(v) for v in q], angularY=float(angular_y))
        return original_projection(self, q, angular_y)
    def setter(self, slot, angular_y):
        if self._unity_angular_setter_calls[slot.index] == 0:
            current["localBeforeAngularSetter"] = self.state(slot.index)
            current["scriptAngularY"] = angular_y
        before = self.state(slot.index) if opts.trace and current.get("sampleId") == 11005 else None
        count = self._unity_angular_setter_calls.get(slot.index)
        raw_q = slot.body.get_global_pose()[1]
        raw_q = [float(raw_q.x), float(raw_q.y), float(raw_q.z), float(raw_q.w)]
        setter_slot = slot
        if opts.cast_setter_pose:
            setter_slot = SimpleNamespace(index=slot.index, body=SimpleNamespace(
                get_global_pose=lambda: self.pyphysx.cast_transformation(slot.body.get_global_pose())))
        result = original_setter(self, setter_slot, angular_y)
        if before is not None:
            np = self.probe.np
            q = np.asarray([before["quaternionWxyz"][j] for j in (1, 2, 3, 0)], dtype=np.float32)
            norm = np.sqrt(np.sum(q*q, dtype=np.float32))
            current["setters"].append({"before": before, "rawBefore": self.raw_native_state(slot.index), "scriptY": angular_y, "result": result, "count": count, "norm": float(norm), "normalized": (q/norm).tolist(), "rawQuaternion": raw_q, "projection": dict(last_projection)})
        return result

    original_sliding = up.PersistentPhysxFrontHalfScene.step_custom_sliding
    def sliding(self, active_index, noise, *args, **kwargs):
        before = self.state(active_index) if opts.trace and current.get("sampleId") == 11005 else None
        ordinal = len(current["ticks"]) + 2
        early = before is not None and opts.solver_ordinal_min <= ordinal <= opts.solver_ordinal_max
        if early:
            self.pyphysx.clear_scene_solver_setup_trace()
            self.pyphysx.set_scene_solver_setup_trace_enabled(True)
            if opts.trace_constraints:
                self.pyphysx.clear_scene_solve_block_trace()
                self.pyphysx.set_scene_solve_block_trace_enabled(True)
                self.pyphysx.clear_scene_solve_writeback_trace()
                self.pyphysx.set_scene_solve_writeback_trace_enabled(True)
                self.pyphysx.clear_scene_narrowphase_trace()
                self.pyphysx.set_scene_narrowphase_trace_enabled(True)
                self.pyphysx.clear_scene_finalizer_trace()
                self.pyphysx.set_scene_finalizer_trace_enabled(True)
        result = original_sliding(self, active_index, noise, *args, **kwargs)
        if before is not None:
            q = self.slots[active_index].body.get_global_pose()[1]
            phases = self.pyphysx.get_scene_solver_setup_trace(True) if early else []
            if early:
                self.pyphysx.set_scene_solver_setup_trace_enabled(False)
            current["ticks"].append({"input": before, "beforeScene": result["beforeScene"], "afterScene": result["afterScene"], "rawAfterQ": [q.x, q.y, q.z, q.w], "solverPhases": phases})
            if early and opts.trace_constraints:
                current["ticks"][-1]["solveBlocks"] = self.pyphysx.get_scene_solve_block_trace(True)
                current["ticks"][-1]["solveWritebacks"] = self.pyphysx.get_scene_solve_writeback_trace(True)
                current["ticks"][-1]["narrowphase"] = self.pyphysx.get_scene_narrowphase_trace(True)
                current["ticks"][-1]["finalizer"] = self.pyphysx.get_scene_finalizer_trace(True)
                self.pyphysx.set_scene_solve_block_trace_enabled(False)
                self.pyphysx.set_scene_solve_writeback_trace_enabled(False)
                self.pyphysx.set_scene_narrowphase_trace_enabled(False)
                self.pyphysx.set_scene_finalizer_trace_enabled(False)
        return result

    up.PersistentPhysxFrontHalfScene.__init__ = init
    up.PersistentPhysxFrontHalfScene.start_bestshot = start
    up.PersistentPhysxFrontHalfScene.run_bestshot_to_first_contact = run
    up.PersistentPhysxFrontHalfScene._unity_native_angular_setter_vector = setter
    up.PersistentPhysxFrontHalfScene._unity_project_locked_angular_velocity = projection
    up.PersistentPhysxFrontHalfScene.step_custom_sliding = sliding
    code = source.read_text(encoding="utf-8")
    # The archived tail runner predates f72606 writeback. Route its reset,
    # collision-tail and settling steps through the current production step.
    code = code.replace("scene.scene.simulate(scene.dt)", "scene._simulate_unity_step()")
    # The historical runner never called UpdateState's out-of-play pass.
    # Actual Unity f71727/ID-pool captures show those retirements are already
    # reusable before the next RESETPOSITION (11001/11003/11010).
    code = code.replace('            row["settle"] = _settle(scene)',
        '            row["settle"] = _settle(scene)\n'
        '            row["clearedOutOfPlay"] = scene.clear_out_of_play_stones()\n'
        '            if row["clearedOutOfPlay"]:\n'
        '                scene._simulate_unity_step()\n'
        '                scene.scene.get_contact_reports()')
    begin = code.index("    if sys.version_info[:2] != (3, 8)")
    end = code.index("    samples = _load_jsonl", begin)
    code = code[:begin] + "    from tools.reverse.front_half_pcm_replay import event_shot_groups, load_jsonl\n    from local_simulator.unity_physx import NativePyphysxMotionStepper, PersistentPhysxFrontHalfScene\n" + code[end:]
    namespace = {"__name__": "c131_audit", "__file__": str(source)}
    exec(compile(code, str(source), "exec"), namespace)
    suffix = "_cast" if opts.cast_setter_pose else ""
    if opts.sync_body_q:
        suffix += "_sync"
    if opts.sync_write_always:
        suffix += "_always"
    output = opts.output or ROOT / f"analysis_input/c131_{opts.profile}{suffix}_20260930.json"
    if opts.output is not None and output.exists():
        raise FileExistsError(output)
    sys.argv = [str(source), "--samples", str(data / "collision_unique_targets_batch_r00.jsonl"), "--events", str(events), "--orientation-manifest", str(data / "orientation_manifest_r00.json"), "--require-orientation-truth", "--motion-kernel", "recovered-python", "--output", str(output)]
    # The archived parser explicitly passes False unless this flag is set.
    # Follow the current production default rather than its historical one.
    if inspect.signature(original_init).parameters['emulate_unity_setactive_no_sim'].default:
        sys.argv.append('--unity-setactive-no-sim')
    if opts.profile != "legacy":
        sys.argv.append("--unity-native-angular-setter-wrapper")
    namespace["main"]()
    if opts.native_lifecycle_trace_control is not None:
        import time
        control = opts.native_lifecycle_trace_control
        (control/'done').write_text('done')
        deadline = time.monotonic()+90
        while not (control/'resume').exists():
            if time.monotonic()>deadline: raise TimeoutError('lifecycle resume')
            time.sleep(.05)
    report = json.loads(output.read_text(encoding="utf-8"))
    extension = _resolve_bundled_extension()
    report["configuration"]["pyphysxExtension"] = str(extension)
    report["configuration"]["pyphysxExtensionSha256"] = hashlib.sha256(extension.read_bytes()).hexdigest()
    report["diagnosticEffectiveConfiguration"] = effective_configuration
    report["diagnosticProfile"] = opts.profile
    report["diagnosticKeepMultiCache"] = opts.keep_multi_cache
    report["diagnosticKeepPcmTaskCache"] = opts.keep_pcm_task_cache
    report["diagnosticFloat32BodyQuaternionNormalization"] = opts.float32_body_q
    report["diagnosticDirectProbeScaleXz"] = opts.direct_probe_scale_xz
    report["diagnosticInitialQuaternionInjection"] = opts.profile in ("full-q", "exact-q")
    if report["diagnosticInitialQuaternionInjection"]:
        report["policy"] = "Offline diagnostic: recorded A10 initial quaternion and recorded friction; no Unity post-release pose, velocity, contact or cache injection."
    report["releaseBoundary"] = releases
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    row = next(r for r in report["rows"] if r["sampleId"] == 11005)
    print(json.dumps({"profile": opts.profile, "11005": row["endpointErrorM"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
