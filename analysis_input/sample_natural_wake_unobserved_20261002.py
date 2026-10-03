"""Plain production replay: no body proxies, Scene wrappers or injected state."""
import hashlib
import argparse
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
    return list(struct.unpack('<13I', struct.pack('<13f', *(s['physxPosition'] + q[1:] + q[:1]
        + s['physxLinearVelocity'] + s['physxAngularVelocity']))))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=ROOT/'analysis_input/native_natural_wake_unobserved_20261002.json')
    opts=parser.parse_args()
    fixture = json.loads((ROOT / 'local_simulator/tests/fixtures/unity_target_activation_20261002.json').read_text())
    scene = PersistentPhysxFrontHalfScene(stone_count=16, ice_mesh_mode='unity-source-once')
    positions = [0.0] * 32
    positions[4:6] = [2.375, 5.2]
    scene.reset_positions(positions)
    scene.start_bestshot(0, [3.4, 0, 0])
    release = raw_words(scene, 0)
    states = []
    for noise in fixture['frictionNoises']:
        scene.step_custom_sliding(0, noise)
        states.append([raw_words(scene, k) for k in (0, 2)])
    for _ in range(1800):
        scene._simulate_unity_step()
        states.append([raw_words(scene, k) for k in (0, 2)])
    report = dict(releaseBits=release, states=states,
                  sourceSha256=hashlib.sha256((ROOT / 'local_simulator/unity_physx.py').read_bytes()).hexdigest(),
                  moduleSha256=hashlib.sha256(_resolve_bundled_extension().read_bytes()).hexdigest())
    output = opts.output
    output.write_text(json.dumps(report))
    print('plain production completed steps', len(states))


if __name__ == '__main__':
    main()
