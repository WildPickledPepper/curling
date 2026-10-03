"""Trace real native Reset solver inputs/outputs; verify observer passivity."""
import hashlib
import json
from pathlib import Path
import struct
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from local_simulator.runtime_loader import install_bundled_pyphysx,_resolve_bundled_extension
install_bundled_pyphysx()
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene

def bits(values):return list(struct.unpack('<%dI'%len(values),struct.pack('<%df'%len(values),*values)))
def state(scene,index):
    s=scene.raw_native_state(index);q=s['quaternionWxyz']
    return bits(s['physxPosition']+q[1:]+q[:1]+s['physxLinearVelocity']+s['physxAngularVelocity'])

def run(positions,index,traced):
    scene=PersistentPhysxFrontHalfScene(stone_count=16,ice_mesh_mode='unity-source-once')
    frames=[];real=scene.scene;step=scene._simulate_unity_step;current={}
    class Observer:
        def __getattr__(self,name):return getattr(real,name)
        def simulate(self,dt):
            if traced:
                scene.pyphysx.clear_scene_solver_setup_trace()
                scene.pyphysx.set_scene_solver_setup_trace_enabled(True)
            result=real.simulate(dt)
            if traced:
                phases=scene.pyphysx.get_scene_solver_setup_trace(False)
                scene.pyphysx.set_scene_solver_setup_trace_enabled(False)
                current['solverPhases']=[]
                for p in phases:
                    if len(p['body_data'])!=1:raise ValueError('Expected a one-body Reset solver island')
                    d=p['body_data'][0]
                    current['solverPhases'].append(dict(afterSolve=p['after_solve'],
                        bits=bits(d['body2world']['p']+d['body2world']['q']+
                                  d['linear_velocity']+d['angular_velocity'])))
            return result
    scene.scene=Observer()
    def observed_step():
        current.clear();current['before']=state(scene,index)
        result=step();current['after']=state(scene,index)
        frames.append(dict(current));return result
    scene._simulate_unity_step=observed_step
    scene.reset_positions(positions)
    return frames

def main():
    inputs=json.loads(Path(sys.argv[1]).read_text());index=inputs['targetIndex']
    baseline=run(inputs['positions'],index,False);observed=run(inputs['positions'],index,True)
    assert len(baseline)==len(observed) and all(
        b['before']==o['before'] and b['after']==o['after'] for b,o in zip(baseline,observed))
    result=dict(targetIndex=index,frames=observed,observerOutputsUnchanged=True,
        sourceSha256=hashlib.sha256((ROOT/'local_simulator/unity_physx.py').read_bytes()).hexdigest(),
        moduleSha256=hashlib.sha256(_resolve_bundled_extension().read_bytes()).hexdigest())
    Path(sys.argv[2]).write_text(json.dumps(result),encoding='utf8')
    print(json.dumps(dict(steps=len(observed),observerOutputsUnchanged=True)))
if __name__=='__main__':main()
