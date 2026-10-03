"""Replay supplied commands and captured RNG draws using current production."""
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from local_simulator.runtime_loader import install_bundled_pyphysx, _resolve_bundled_extension
install_bundled_pyphysx()
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene

def words(scene,index):
    s=scene.raw_native_state(index);q=s['quaternionWxyz']
    values=s['physxPosition']+q[1:]+q[:1]+s['physxLinearVelocity']+s['physxAngularVelocity']
    return list(struct.unpack('<13I',struct.pack('<13f',*values)))

def main():
    source=Path(sys.argv[1]);output=Path(sys.argv[2]);inputs=json.loads(source.read_text())
    scene=PersistentPhysxFrontHalfScene(stone_count=16,ice_mesh_mode='unity-source-once')
    indices=[inputs['activeIndex']]+[i for i in range(16) if i!=inputs['activeIndex']
         and inputs['positions'][2*i:2*i+2]!=[0.,0.]]
    scene.reset_positions(inputs['positions'])
    scene.start_bestshot(inputs['activeIndex'],inputs['shot'])
    release=[words(scene,i) for i in indices]
    def live():return [scene.slots[i].in_scene and not scene.slots[i].body.get_actor_flag_value(
        scene.pyphysx.ActorFlag.DISABLE_SIMULATION) for i in indices]
    release_live=live();release_enabled=[scene.slots[i].enabled for i in indices]
    states=[];simulating=[];enabled=[]
    for noise in inputs['frictionNoises']:
        scene.step_custom_sliding(inputs['activeIndex'],noise)
        states.append([words(scene,i) for i in indices]);simulating.append(live())
        enabled.append([scene.slots[i].enabled for i in indices])
    result=dict(stoneIndices=indices,releaseBits=release,states=states,
        frictionNoises=inputs['frictionNoises'],simulating=simulating,enabled=enabled,
        releaseSimulating=release_live,releaseEnabled=release_enabled,
        sourceSha256=hashlib.sha256((ROOT/'local_simulator/unity_physx.py').read_bytes()).hexdigest(),
        moduleSha256=hashlib.sha256(_resolve_bundled_extension().read_bytes()).hexdigest(),
        inputsSha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        unityEventsSha256=inputs['unityEventsSha256'],
        scope='Only commands and recorded friction draws. No observed body state or solver result injected.')
    output.write_text(json.dumps(result),encoding='utf8')
    print(json.dumps(dict(steps=len(states),stoneIndices=indices)),flush=True)

if __name__=='__main__':main()
