"""Package the fixed collider's actual Unity cooker input, preserving binary32."""
import hashlib
import json
from pathlib import Path
import struct

ROOT=Path(__file__).resolve().parents[1]


def main():
    directory=ROOT/'analysis_input/unity_startup_geometry_audit_capture_20261002_inputs_v2'
    path=next((directory/'logs').glob('*/events.jsonl'))
    manifest=json.loads((directory/'capture_manifest.json').read_text())
    calls=[]
    runtime=None
    for line in path.open(encoding='utf8'):
        row=json.loads(line)
        if row['type']=='a12.startup_convex_runtime':runtime=row['data']
        if row['type']=='a12.pcm_internal_call':
            data=row['data']
            if data.get('convexCookerInput',{}).get('count')==512:calls.append(data)
    assert len(calls)==16
    source=calls[0]['convexCookerInput']
    assert all(r['convexCookerInput']['pointBits']==source['pointBits'] for r in calls)
    assert {k:source[k] for k in ('stride','count','flags','vertexLimit','quantizedCount')}==dict(stride=12,count=512,flags=2,vertexLimit=255,quantizedCount=255)
    raw=b''.join(struct.pack('<3I',*p) for p in source['pointBits'])
    vertices=[list(struct.unpack('<3f',struct.pack('<3I',*p))) for p in source['pointBits']]
    result=dict(schema='unity-fixed-stone-convex-cooking-input-v1',vertices=vertices,
        pointBits=source['pointBits'],pointBufferSha256=hashlib.sha256(raw).hexdigest(),
        descriptor={k:source[k] for k in ('stride','count','flags','vertexLimit','quantizedCount')},
        source=dict(unityWasmSha256=manifest['sourceSha256'],functionIndex=72908,
            callIds=[r['callId'] for r in calls],events=str(path.relative_to(ROOT)),
            eventsSha256=hashlib.sha256(path.read_bytes()).hexdigest()),
        scope='Fixed gameplay collider mesh in native Unity XYZ; actual input asset, not a cooked output or trajectory state.')
    destination=ROOT/'local_simulator/assets/unity_stone_convex_input_512.json'
    destination.write_text(json.dumps(result,indent=2),encoding='utf8')
    assert runtime is not None
    fixture=dict(source=result['source'],headerBits=runtime['headerBits'],hull=runtime['hull'],
        byteLayout=runtime['runtime']['byteLayout'],rawBytes=runtime['runtime']['runtimeBufferWindow']['rawBytes'],
        bigConvexArrays={nk:runtime['runtime']['bigConvexRawDataArrays'][uk]['rawBytes']
            for uk,nk in [('samplesWindow','samples_raw_bytes'),('valenciesWindow','valencies_raw_bytes'),
                          ('adjacentVertsWindow','adjacent_vertices_raw_bytes')]})
    # Numeric output is an independent Unity observation, not the repaired input.
    (ROOT/'local_simulator/tests/fixtures/unity_stone_cooking_output_20261002.json').write_text(json.dumps(fixture,indent=2),encoding='utf8')
    print('actual Unity fixed collider input:',len(vertices),'vertices',result['pointBufferSha256'])


if __name__=='__main__':main()
