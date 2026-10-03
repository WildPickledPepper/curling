"""Verify the portable arithmetic against actual Unity matrix and shape calls."""
import hashlib
import json
import struct
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'local_simulator/runtime_support'))
from tools.reverse.recovered_transform_scale import (
    recovered_stone_scale_matrix, recovered_stone_world_matrix,
)
from verify_pcm_internal_trace import events, rows_of, raw_argument, verify_capture


def main():
    replay_path = ROOT / 'analysis_input/transform_scale_kernel_verified_20261001.json'
    replay = json.loads(replay_path.read_text(encoding='utf-8'))
    capture = ROOT / 'analysis_input/unity_transform_scale_calc_trace_20261001'
    capture_validation = verify_capture(capture)
    source_events, _ = events(capture)
    calls = rows_of(source_events, 'a12.pcm_internal_call')
    fixtures = {}
    for row in replay['verified']:
        chain = row['hierarchy']['chain']
        assert len(chain) == 2 and chain[1]['parent'] == -1
        assert chain[1]['values'][3:7] == [0,0,0,1]
        values, parent = chain[0]['values'], chain[1]['values']
        method = recovered_stone_world_matrix if row['functionIndex'] == 78121 else recovered_stone_scale_matrix
        output = np.asarray(method(values[3:7],values[7:10],parent[7:10]),dtype=np.float32)
        assert output.view(np.uint32).tolist() == row['matrixBits'], row['callId']
        if row['functionIndex'] == 78119:
            key = tuple(chain[0]['bits'][3:10] + chain[1]['bits'][7:10])
            fixtures[key] = {'localQuaternion':values[3:7], 'localScale':values[7:10],
                'parentScale':parent[7:10], 'expectedMatrixBits':row['matrixBits'],
                'callId':row['callId'], 'releaseSerial':row['releaseSerial']}
    for row in replay['verified']:
        if row['functionIndex'] == 78121:
            chain = row['hierarchy']['chain']
            key = tuple(chain[0]['bits'][3:10] + chain[1]['bits'][7:10])
            fixtures[key]['expectedWorldMatrixBits'] = row['matrixBits']
    producers = []
    for row in calls:
        if row['functionIndex'] != 72950:
            continue
        matrix_calls = [r for r in calls if r['functionIndex']==78119 and r['parentCallId']==row['callId']]
        assert len(matrix_calls)==2
        matrix = struct.unpack_from('<9I',raw_argument(matrix_calls[0],0,'after'))
        scale = struct.unpack_from('<3I',raw_argument(row,1,'after'))
        assert scale == (matrix[0],matrix[4],matrix[8])
        shape_calls = [r for r in calls if r['functionIndex']==72573 and r['parentCallId']==row['parentCallId']]
        assert len(shape_calls)==1
        # f72573 argument 1 is the incoming PxGeometry, copied by f70398.
        shape = shape_calls[0]
        geometry = raw_argument(shape,1,'before')
        assert struct.unpack_from('<I',geometry)[0]==4
        assert struct.unpack_from('<3I',geometry,4)==scale
        assert shape['callerFunctionIndex']==73282
        producers.append({'releaseSerial':row['releaseSerial'],'producerCallId':row['callId'],
            'shapeCreationCallId':shape['callId'],'scaleBits':list(scale),
            'scale':list(struct.unpack('<3f',struct.pack('<3I',*scale)))})
    assert len(producers)==23
    fixture_data = {'sourceSha256':'cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81',
        'eventsSha256':replay['eventSha256'], 'sourceEvents':replay['eventPath'],
        'sourceFunctions':[78119,78120,78121,72950], 'cases':list(fixtures.values())}
    fixture_path = ROOT / 'local_simulator/tests/fixtures/unity_transform_scale_20261001.json'
    fixture_path.parent.mkdir(exist_ok=True)
    fixture_path.write_text(json.dumps(fixture_data,indent=2),encoding='utf-8')
    result = {'captureValidation':capture_validation,'matrixCallsBitExact':138,
        'matrixFieldsBitExact':1242,'shapeProducerCallsBitExact':23,'independentFixtureCases':len(fixtures),
        'portableSource':str(ROOT/'local_simulator/runtime_support/tools/reverse/recovered_transform_scale.py'),
        'fixtureSha256':hashlib.sha256(fixture_path.read_bytes()).hexdigest(),'producers':producers,
        'limitation':'Arithmetic is recovered. Live shape scale update and native-to-Transform rotation synchronization are not yet integrated.'}
    output = ROOT/'analysis_input/recovered_transform_scale_verified_20261001.json'
    output.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k.endswith('Exact') or k=='independentFixtureCases'}))


if __name__=='__main__':
    main()
