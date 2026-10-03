"""Capture the production reset path without any recorded state injection."""
import json
import struct
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from local_simulator.runtime_loader import install_bundled_pyphysx
install_bundled_pyphysx()
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene


def bits(values):
    return list(struct.unpack('<%dI'%len(values),struct.pack('<%df'%len(values),*values)))


def main():
    scene=PersistentPhysxFrontHalfScene(stone_count=16,ice_mesh_mode='unity-source-once')
    frames=[]
    writes=[]
    original_step=scene._simulate_unity_step
    original_position=scene._set_position_preserve_orientation
    def observed_step():
        before=scene.raw_native_state(2)
        result=original_step()
        frames.append({'step':len(frames)+1,'before':before,'after':scene.raw_native_state(2),
                       'sleeping':scene.slots[2].body.is_sleeping()})
        return result
    def observed_position(index,x,y,**kwargs):
        result=original_position(index,x,y,**kwargs)
        writes.append({'index':index,'state':scene.raw_native_state(index)})
        return result
    scene._simulate_unity_step=observed_step
    scene._set_position_preserve_orientation=observed_position
    position=[0.0]*32
    position[4:6]=[2.375,5.2]
    scene.reset_positions(position)
    result={'sampleId':11000,'scope':'Fresh production scene and first reset, no oracle yaw/quaternion/friction.',
            'positionWrites':writes,'frames':frames,'final':scene.raw_native_state(2)}
    path=ROOT/'analysis_input/native_reset_settling_fixed_20261002.json'
    path.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('physicsSteps',len(frames),'finalSleeping',frames[-1]['sleeping'])


if __name__=='__main__':
    main()
