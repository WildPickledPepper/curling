"""Observe the unchanged default production Reset -> BESTSHOT -> first ticks."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from local_simulator.runtime_loader import install_bundled_pyphysx, _resolve_bundled_extension
install_bundled_pyphysx()
import local_simulator.unity_physx as up

def bits(values):
    return list(struct.unpack('<%dI'%len(values),struct.pack('<%df'%len(values),*values)))

def state_bits(s):
    q=s['quaternionWxyz']
    return bits(s['physxPosition']+q[1:]+q[:1]+s['physxLinearVelocity']+s['physxAngularVelocity'])

def physical_output(value):
    """Allocation addresses vary across processes; retain every physical field."""
    if isinstance(value,dict):
        return {k:physical_output(v) for k,v in value.items()
                if k not in ('actor0','actor1','shape0','shape1')}
    if isinstance(value,list):
        return [physical_output(v) for v in value]
    return value

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--trace',action='store_true')
    parser.add_argument('--steps',type=int,default=4)
    parser.add_argument('--tail-steps',type=int,default=0)
    parser.add_argument('--trace-at-step',type=int)
    parser.add_argument('--native-trace-control',type=Path)
    parser.add_argument('--baseline',type=Path)
    parser.add_argument('--fast-midphase',action='store_true')
    parser.add_argument('--output',type=Path,required=True)
    opts=parser.parse_args()
    scene=up.PersistentPhysxFrontHalfScene(stone_count=16,ice_mesh_mode='unity-source-once',
        **({'ice_use_fast_midphase':True} if opts.fast_midphase else {}))
    position=[0.]*32;position[4:6]=[2.375,5.2]
    scene.reset_positions(position)
    setters=[];phase='release';ordinal=1
    real_recreate=scene._recreate_unity_activation_body
    class Body:
        def __init__(self,body): self.body=body
        def __getattr__(self,name):
            function=getattr(self.body,name)
            if name not in ('set_linear_velocity','set_angular_velocity','set_global_pose'):
                return function
            def call(value):
                before=scene.raw_native_state(0)
                result=function(value)
                after=scene.raw_native_state(0)
                row=dict(phase=phase,ordinal=ordinal,name=name,before=before,after=after,
                         beforeBits=state_bits(before),afterBits=state_bits(after))
                if name!='set_global_pose':
                    row.update(input=list(value),inputBits=bits(list(value)))
                setters.append(row)
                return result
            return call
    def recreate(slot):
        real_recreate(slot)
        if slot.index==0:slot.body=Body(slot.body)
    scene._recreate_unity_activation_body=recreate
    target_wakes=[]
    class TargetBody:
        def __init__(self,body): self.body=body
        def __getattr__(self,name):
            function=getattr(self.body,name)
            if name!='wake_up':return function
            def call(*args,**kwargs):
                before=state_bits(scene.raw_native_state(2))
                sleeping_before=self.body.is_sleeping()
                result=function(*args,**kwargs)
                target_wakes.append(dict(physicsTick=ordinal-1,stoneIndex=2,
                    beforeBits=before,afterBits=state_bits(scene.raw_native_state(2)),
                    sleepingBefore=sleeping_before,sleepingAfter=self.body.is_sleeping()))
                return result
            return call
    scene.slots[2].body=TargetBody(scene.slots[2].body)
    scene.start_bestshot(0,[3.4,0,0])
    release=scene.raw_native_state(0)
    real_scene=scene.scene
    native_rows=[]
    trace_names=('solver_setup','solve_block','solve_writeback','narrowphase','finalizer')
    class Scene:
        def __getattr__(self,name):return getattr(real_scene,name)
        def simulate(self,dt):
            before=scene.raw_native_state(0)
            traced=opts.trace and (opts.trace_at_step is None or ordinal-1==opts.trace_at_step)
            control=opts.native_trace_control if ordinal-1==opts.trace_at_step else None
            if control:
                import ctypes,os,time
                (control/'arm.json').write_text(json.dumps(dict(pid=os.getpid(),
                    threadId=ctypes.windll.kernel32.GetCurrentThreadId(),
                    module=str(_resolve_bundled_extension()),slidingTick=ordinal-1,denseOrdinal=ordinal)))
                deadline=time.monotonic()+90
                while not (control/'go').exists():
                    if time.monotonic()>deadline:raise TimeoutError('go')
                    time.sleep(.05)
            if traced:
                for name in trace_names:
                    getattr(scene.pyphysx,'clear_scene_'+name+'_trace')()
                    getattr(scene.pyphysx,'set_scene_'+name+'_trace_enabled')(True)
            result=real_scene.simulate(dt)
            if control:
                (control/'done').write_text('done')
                deadline=time.monotonic()+90
                while not (control/'resume').exists():
                    if time.monotonic()>deadline:raise TimeoutError('resume')
                    time.sleep(.05)
            row=dict(ordinal=ordinal,before=before,afterNative=scene.raw_native_state(0),
                     targetAfterNativeBits=state_bits(scene.raw_native_state(2)),
                     targetSleepingAfterNative=scene.slots[2].body.is_sleeping())
            if traced:
                for name in trace_names:
                    row[name]=getattr(scene.pyphysx,'get_scene_'+name+'_trace')(False)
                    getattr(scene.pyphysx,'set_scene_'+name+'_trace_enabled')(False)
            native_rows.append(row)
            return result
    scene.scene=Scene()
    source=ROOT/'analysis_input/unity_reset_cache_lifecycle_steps1_8_delayed_first_case_20261002/logs/unity_runtime_probe_20261002_155746/events.jsonl'
    noises=[json.loads(line)['data']['value'] for line in source.open(encoding='utf-8')
            if '"type": "sliding.random_range.friction"' in line][:opts.steps]
    frames=[]
    phase='sliding'
    for i,noise in enumerate(noises,2):
        ordinal=i
        step=scene.step_custom_sliding(0,noise)
        frames.append(dict(ordinal=i,noise=noise,step=step,
                           after=scene.raw_native_state(0),afterBits=state_bits(scene.raw_native_state(0))))
    tail=[]
    phase='physics-only-tail'
    for j in range(opts.tail_steps):
        ordinal=len(frames)+j+2
        before=scene.raw_native_state(0)
        scene._simulate_unity_step()
        target=scene.raw_native_state(2)
        tail.append(dict(physicsTick=ordinal-1,beforeBits=state_bits(before),
            afterBits=state_bits(scene.raw_native_state(0)),targetAfterBits=state_bits(target),
            sleeping=[scene.slots[k].body.is_sleeping() for k in [0,2]],
            reports=scene._stone_reports(scene.scene.get_contact_reports())))
    report=dict(moduleSha256=hashlib.sha256(_resolve_bundled_extension().read_bytes()).hexdigest(),
        unityPhysxSha256=hashlib.sha256(Path(up.__file__).read_bytes()).hexdigest(),
        scope='default production scene; no release pose/quaternion or motion override injection',
        release=release,releaseBits=state_bits(release),setters=setters,targetWakeCalls=target_wakes,
        frames=frames,tail=tail,native=native_rows)
    if opts.baseline:
        old=json.loads(opts.baseline.read_text())
        report['baselineComparisonExcludedFields']=['actor0','actor1','shape0','shape1']
        report['baselineOutputsUnchanged']=old['releaseBits']==report['releaseBits'] and physical_output(old['frames'][:len(frames)])==physical_output(frames)
        assert report['baselineOutputsUnchanged'],'observer changed production output'
    opts.output.write_text(json.dumps(report,indent=2))
    print('releaseBits',report['releaseBits'])
    for frame in frames[:4]:print('ordinal',frame['ordinal'],frame['afterBits'])
    print('sampledFrames',len(frames))

if __name__=='__main__':main()
