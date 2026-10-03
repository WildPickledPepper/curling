"""Replay a fresh captured case with actual friction inputs, never state overrides."""
import argparse
import hashlib
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from local_simulator.runtime_loader import install_bundled_pyphysx, _resolve_bundled_extension
install_bundled_pyphysx()
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene


def raw_words(scene, index):
    s = scene.raw_native_state(index)
    q = s['quaternionWxyz']
    return list(struct.unpack('<13I', struct.pack('<13f', *(s['physxPosition']
        + q[1:] + q[:1] + s['physxLinearVelocity'] + s['physxAngularVelocity']))))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--capture', type=Path, required=True)
    p.add_argument('--plan', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--steps', type=int, default=3000)
    p.add_argument('--exclude-non-sliding-setters', action='store_true',
                   help='Record cleanup setters separately; do not misread their stale noise as a friction draw.')
    p.add_argument('--trace-from-step',type=int)
    p.add_argument('--trace-through-step',type=int)
    p.add_argument('--native-trace-control',type=Path)
    args = p.parse_args()
    plan = json.loads(args.plan.read_text())[0]
    event_path = next(args.capture.glob('logs/*/events.jsonl'))
    rows = [json.loads(l) for l in event_path.open(encoding='utf8')]
    setters = [r['data'] for r in rows if r['type'] == 'a12.dense_pre_angular_setter']
    post = [r['data'] for r in rows if r['type'] == 'a12.dense_post_angular_setter']
    assert len(post) == len(setters), 'Incomplete dense input capture: setter recording limit was reached'
    assert [r['ordinal'] for r in post] == list(range(1, len(post) + 1)), 'Dense setter ordinals froze at the recording limit'
    assert [r['ordinal'] for r in setters] == list(range(1, len(setters) + 1))
    sliding = setters[1:]
    excluded = []
    if args.exclude_non_sliding_setters:
        excluded = [r for r in sliding if r['tickSerial'] is None or
                    r['getterLinear'] is None or r['getterAngular'] is None]
        sliding = [r for r in sliding if r not in excluded]
        assert [r['ordinal'] for r in sliding] == list(range(2, len(sliding)+2)), \
            'Interleaved non-sliding setters need an explicit call schedule, not a dense friction replay'
    noises = [r['lastFrictionNoise'] for r in sliding]
    assert all(n is not None for n in noises)
    active = plan['active_index']
    indices = [active] + [s['index'] for s in plan['stones']]
    scene = PersistentPhysxFrontHalfScene(stone_count=16, ice_mesh_mode='unity-source-once')
    positions = [0.] * 32
    for s in plan['stones']:
        positions[s['index']*2:s['index']*2+2] = [s['x'], s['y']]
    scene.reset_positions(positions)
    reset = [raw_words(scene, k) for k in indices]
    scene.start_bestshot(active, [plan['v0'], plan['h0'], plan['w0']])
    release = [raw_words(scene, k) for k in indices]
    def live_flags():
        return [scene.slots[k].in_scene and not scene.slots[k].body.get_actor_flag_value(
            scene.pyphysx.ActorFlag.DISABLE_SIMULATION) for k in indices]
    release_enabled = [scene.slots[k].enabled for k in indices]
    release_live = live_flags()
    states, sleeping, contacts, enabled, simulating, wall_contacts = [], [], [], [], [], []
    native_phases=[]
    phase_step=[0]
    trace_names=('solver_setup','solve_block','solve_writeback','narrowphase','finalizer')
    if args.trace_from_step is not None:
        real_scene=scene.scene
        class ObservedScene:
            def __getattr__(self,name):return getattr(real_scene,name)
            def simulate(self,dt):
                traced=args.trace_from_step<=phase_step[0]<=(args.trace_through_step or args.trace_from_step)
                if traced:
                    for name in trace_names:
                        getattr(scene.pyphysx,'clear_scene_'+name+'_trace')()
                        getattr(scene.pyphysx,'set_scene_'+name+'_trace_enabled')(True)
                    before=[raw_words(scene,k) for k in indices]
                control=args.native_trace_control if traced else None
                if control:
                    import ctypes,os,time
                    (control/'arm.json').write_text(json.dumps(dict(pid=os.getpid(),
                        threadId=ctypes.windll.kernel32.GetCurrentThreadId(),
                        module=str(_resolve_bundled_extension()),physicsTick=phase_step[0])))
                    deadline=time.monotonic()+90
                    while not (control/'go').exists():
                        if time.monotonic()>deadline:raise TimeoutError('go')
                        time.sleep(.05)
                result=real_scene.simulate(dt)
                if control:
                    (control/'done').write_text('done')
                    deadline=time.monotonic()+90
                    while not (control/'resume').exists():
                        if time.monotonic()>deadline:raise TimeoutError('resume')
                        time.sleep(.05)
                if traced:
                    row=dict(physicsTick=phase_step[0],beforeNativeBits=before,
                        afterNativeBits=[raw_words(scene,k) for k in indices])
                    for name in trace_names:
                        row[name]=getattr(scene.pyphysx,'get_scene_'+name+'_trace')(False)
                        getattr(scene.pyphysx,'set_scene_'+name+'_trace_enabled')(False)
                    native_phases.append(row)
                return result
        scene.scene=ObservedScene()
    for step in range(1, args.steps + 1):
        phase_step[0]=step
        if step <= len(noises):
            result = scene.step_custom_sliding(active, noises[step-1])
            if result['stoneReports']:
                contacts.append(step)
        else:
            scene._simulate_unity_step()
        states.append([raw_words(scene, k) for k in indices])
        sleeping.append([scene.slots[k].body.is_sleeping() for k in indices])
        enabled.append([scene.slots[k].enabled for k in indices])
        simulating.append(live_flags())
        if scene._last_wall_reports:
            wall_contacts.append(dict(physicsTick=step, reports=scene._last_wall_reports))
    report = dict(plan=plan, stoneIndices=indices, resetBits=reset, releaseBits=release,
        frictionNoises=noises, states=states, sleeping=sleeping, stoneContactTicks=contacts,
        enabled=enabled, simulating=simulating, releaseEnabled=release_enabled, releaseSimulating=release_live,
        wallContacts=wall_contacts, wallContactMetadata=scene.wall_contact_metadata,
        sourceSha256=hashlib.sha256((ROOT/'local_simulator/unity_physx.py').read_bytes()).hexdigest(),
        moduleSha256=hashlib.sha256(_resolve_bundled_extension().read_bytes()).hexdigest(),
        integrationCosine=scene.integration_cosine_metadata,
        unityEventsSha256=hashlib.sha256(event_path.read_bytes()).hexdigest())
    if args.trace_from_step is not None:
        report['nativePhases']=native_phases
    if args.exclude_non_sliding_setters:
        report['excludedNonSlidingSetters']=excluded
        report['slidingSetterOrdinals']=[r['ordinal'] for r in sliding]
        report['replayScope']='Layout, release and recorded friction inputs only. Wall callbacks originate from native contact reports; observed cleanup calls are not injected.'
    args.output.write_text(json.dumps(report))
    print(json.dumps(dict(steps=len(states), frictionDraws=len(noises), contactTicks=contacts,
        firstSleepTicks=[next((i+1 for i,s in enumerate(sleeping) if s[k]), None)
            for k in range(len(indices))])))


if __name__ == '__main__': main()
