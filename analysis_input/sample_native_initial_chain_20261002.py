"""Read production startup and ResetPosition inputs without recorded state injection."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from local_simulator.runtime_loader import install_bundled_pyphysx

install_bundled_pyphysx()
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene


def main():
    # The wrappers below call the original methods unchanged and only read state.
    writes = []
    original = PersistentPhysxFrontHalfScene._set_position_preserve_orientation

    def observed(self, index, x, y):
        result = original(self, index, x, y)
        writes.append({'index': index, 'protocolPosition': [x, y],
                       'nativeAfterWrite': self.raw_native_state(index)})
        return result

    PersistentPhysxFrontHalfScene._set_position_preserve_orientation = observed
    scene = PersistentPhysxFrontHalfScene(stone_count=16, ice_mesh_mode='unity-source-once')
    startup = [scene.raw_native_state(i) for i in range(16)]
    shape = scene.slots[0].shape
    hull = shape.get_convex_mesh_runtime_hull_data()
    mass = shape.get_convex_mesh_data()['mass_information']
    source = ROOT/'analysis_input/unity_scene_chain_from_start_20261002'
    events = next((source/'logs').glob('*/events.jsonl'))
    resets = [json.loads(s)['data']['release']['reset'] for s in events.read_text().splitlines()
              if json.loads(s)['type'] == 'a10.release_reset_orientation']
    outputs = []
    for reset in resets:
        writes.clear()
        position = [float(x) for x in reset['text'].split()[1:]]
        scene.reset_positions(position)
        outputs.append({'resetSerial': reset['serial'], 'text': reset['text'],
                        'positionWrites': list(writes),
                        'afterReset': [scene.raw_native_state(i) for i in range(16)]})
    result = {'scope': 'Production startup and isolated reset input writes; no shots, recorded yaw, release quaternion, or friction injected.',
              'startup': startup, 'hull': hull, 'massInformation': mass, 'resets': outputs}
    output = ROOT/'analysis_input/native_initial_chain_readonly_20261002.json'
    output.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print('startup stones', len(startup), 'resets', len(outputs), 'output', output)


if __name__ == '__main__':
    main()
