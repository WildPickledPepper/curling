import base64
import hashlib
import json
from pathlib import Path
import struct
import zlib

import validate_multiple_cases_20261002 as v

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'analysis_input'
capture = BASE/'additional_case_validation_20261002/additional12000_unity'
native = json.loads((BASE/'wall_repair_regression_20261003/additional12000_native.json').read_text())
path = v.event_path(capture)
rows = [r for r in v.rows(path, 'a12.tail_phase_core')
        if r['phase'] == 'DCP.FixedUpdate.boundary' and r['edge'] == 'enter']
assert [r['solverSerial'] for r in rows] == list(range(4001))
main = rows[0]['mainCorePtr']
cores = [main] + [c['corePtr'] for c in rows[0]['cores'] if c['corePtr'] != main]
bits = bytearray()
members = []
for row in rows:
    mapping = {c['corePtr']: c for c in row['cores']}
    alive = [core in mapping for core in cores]
    members.append(alive)
    for core in cores:
        if core in mapping:
            bits.extend(struct.pack('<13I', *v.pose_first(mapping[core]['bits'])))
result = dict(plan=native['plan'], completedSteps=4000, stoneIndices=native['stoneIndices'],
    frictionNoises=native['frictionNoises'], actorMembership=members,
    liveActorStateBytesZlibBase64=base64.b64encode(zlib.compress(bits, 9)).decode(),
    stateBytesSha256=hashlib.sha256(bits).hexdigest(),
    wallCallback=json.loads((BASE/'case12000_callback_pose_20261003.json').read_text()),
    unityEventsSha256=v.digest(path), originalUnityWasmSha256=v.digest(BASE/'unity_20260930.wasm'),
    scope='Independent Unity completed boundaries, compare only genuinely live actors. Retained inactive pose comes from actual f72606 in the Wall callback, not fallback core zeros.')
(ROOT/'local_simulator/tests/fixtures/unity_wall_collision_12000_20261003.json').write_text(json.dumps(result))
print('live actor bytes', len(bits), 'boundaries', len(rows))
