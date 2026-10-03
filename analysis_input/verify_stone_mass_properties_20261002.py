"""Verify the recovered mass calculation against runtime calls and source code."""
import hashlib
import json
import struct
import subprocess
from pathlib import Path

import numpy as np
import wasmtime
from verify_pcm_internal_trace import events, rows_of
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import local_simulator.unity_physx
from tools.reverse.recovered_stone_mass import recovered_stone_inertia


def memory(row, edge, argument):
    return bytes.fromhex(next(a['hex'] for a in row[edge] if a['argument'] == argument))


def bits(values):
    return np.asarray(values, dtype=np.float32).view(np.uint32).tolist()


def main():
    captured, event_path = events(ROOT/'analysis_input/unity_11005_mass_properties_v2_20261002')
    calls = rows_of(captured, 'a12.pcm_internal_call')
    mass_calls = [r for r in calls if r['functionIndex'] == 72776]
    by_id = {r['callId']: r for r in calls}
    # Read the actual formal hull's mass information through its native API.
    result = subprocess.run([
        r'C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe',
        '-c', 'import json; from local_simulator.runtime_loader import install_bundled_pyphysx; '
        'install_bundled_pyphysx(); from local_simulator.unity_physx import PersistentPhysxFrontHalfScene; '
        's=PersistentPhysxFrontHalfScene(stone_count=1); '
        'print("MASS_INFORMATION="+json.dumps(s.slots[0].shape.get_convex_mesh_data()["mass_information"]))'
    ], cwd=ROOT, capture_output=True, text=True, check=True)
    mass_info = json.loads(next(s.partition('=')[2] for s in result.stdout.splitlines()
                               if s.startswith('MASS_INFORMATION=')))
    store = wasmtime.Store()
    kernel = ROOT/'analysis_input/unity_mass_numeric_kernel_20261002.wasm'
    instance = wasmtime.Instance(store, wasmtime.Module(store.engine, kernel.read_bytes()), [])
    mem = instance.exports(store)['memory']
    cases = []
    for row in mass_calls:
        scale_calls = sorted((r for r in calls if r['functionIndex'] == 72779 and
                              r['parentCallId'] == row['callId']), key=lambda r:r['callId'])
        assert len(scale_calls) == 2
        first, last = scale_calls
        source = memory(first, 'before', 1)
        inertia = list(struct.unpack_from('<9f', source))
        scaled_mass = struct.unpack_from('<f', source, 36)[0]
        scale = list(struct.unpack_from('<3f', source, 44))
        rotation = list(struct.unpack_from('<4f', source, 56))
        assert rotation == [0,0,0,1]
        assert bits(inertia[::4]) == bits([mass_info['local_inertia_rows'][i][i] for i in range(3)])
        volume = (np.float32(scale[0])*np.float32(scale[1]))*np.float32(scale[2])
        assert bits([np.float32(mass_info['unit_density_mass'])*volume]) == bits([scaled_mass])
        mem.write(store, struct.pack('<9f', *inertia), 1048)
        mem.write(store, struct.pack('<3f', *scale), 2000)
        mem.write(store, struct.pack('<4f', *rotation), 3000)
        instance.exports(store)['scale'](store, 1000, 2000, 3000)
        original_result = bytes(mem.read(store, 1264, 1300))
        assert original_result == memory(last, 'after', 0)[:36], ('source scale', row['callId'])
        outer = by_id[row['parentCallId']]
        assert outer['functionIndex'] == 72778
        requested_mass = outer['args'][1]
        final = next(r for r in calls if r['functionIndex'] == 72777 and r['parentCallId'] == outer['callId'])
        diagonal = next(r for r in calls if r['functionIndex'] == 69768 and r['parentCallId'] == final['callId'])
        assert memory(diagonal, 'after', 2)[:16] == struct.pack('<4f', 0,0,0,1)
        expected = list(struct.unpack('<3I', memory(final, 'after', 1)[:12]))
        recovered = recovered_stone_inertia(mass_info, scale, requested_mass)
        assert bits(recovered) == expected, ('production mass', row['callId'])
        cases.append({'callId':row['callId'], 'releaseSerial':row.get('releaseSerial'),
                      'scale':scale, 'mass':requested_mass,
                      'expectedInertiaBits':expected,
                      'expectedInverseYawInertiaBits':bits([np.float32(1)/np.float32(recovered[1])]),
                      'scaledUnitMassBits':bits([scaled_mass])})
    assert len(cases) == 98
    assert set(c['releaseSerial'] for c in cases) == set(range(2,25,2))
    fixture = {'sourceSha256':'cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81',
               'events':str(event_path), 'eventsSha256':hashlib.sha256(event_path.read_bytes()).hexdigest(),
               'kernelSha256':hashlib.sha256(kernel.read_bytes()).hexdigest(),
               'massInformation':mass_info, 'cases':cases,
               'scope':'Observed formal stone hull, identity shape and scale rotation, forced zero COM.'}
    output = ROOT/'local_simulator/tests/fixtures/unity_stone_mass_20261002.json'
    output.write_text(json.dumps(fixture, indent=2), encoding='utf-8')
    print('original scale and production inertia exact:', len(cases), 'runtime calls')


if __name__ == '__main__':
    main()
