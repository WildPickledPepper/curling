"""Use existing internal PCM snapshots at matched measured function inputs."""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,struct,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'analysis_input/local_partial_validation_20261003'
CP39=r'C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe'
def scan(r):
    events={};h=hashlib.sha256()
    for n,line in enumerate((ROOT/r['path']).open('rb'),1):
        h.update(line)
        if b'func70576' not in line or b'physx.native.' not in line:continue
        e=json.loads(line)
        if e['type'] not in ('physx.native.before','physx.native.after') or e['data']['hook']['wasm']!='func70576':continue
        d=e['data'];pcm=next((x for x in d.get('extraDumps',[]) if x.get('label','').endswith('.pcmInputs')),None)
        key=d['dumpId'];events.setdefault(key,{})[d['phase']]=dict(line=n,pcm=pcm)
    assert h.hexdigest()==r['sha256']
    return dict(path=r['path'],sha256=r['sha256'],events=events)
def contact_words(p):
    return list(struct.unpack('<7I',struct.pack('<7f',*(p['normal']+[p['separation']]+p['point']))))+[p['internal_face_index1']]
def main():
    inventory=json.loads((OUT/'inventory.json').read_text());records=[r for r in inventory['capturesInventory'] if any(k.startswith('func70576:') for k in r['nativeHooks'])]
    with ThreadPoolExecutor(max_workers=4) as pool:captures=list(pool.map(scan,records))
    requests=[];pending=[]
    for c in captures:
        for key,edges in c['events'].items():
            if not all(e in edges and edges[e]['pcm'] for e in ('before','after')):
                pending.append(dict(path=c['path'],dumpId=key,reason='Missing paired actual PCM input/output snapshots.'));continue
            before=edges['before']['pcm'];required=('shape0','shape1','transform0','transform1','narrowPhaseParams','cache','contactBuffer')
            if any(k not in before for k in required):pending.append(dict(path=c['path'],dumpId=key,reason='Missing sampled PCM geometry/transform/cache/params input.'));continue
            requests.append(dict(key=c['path']+'|'+key,path=c['path'],dumpId=key,beforeLine=edges['before']['line'],afterLine=edges['after']['line'],
                before=before,after=edges['after']['pcm']))
    inputs=OUT/'pcm_requests.json';outputs=OUT/'pcm_native_replies.json';inputs.write_text(json.dumps(requests),encoding='utf8')
    subprocess.run([CP39,str(ROOT/'analysis_input/replay_partial_pcm_inputs_cp39_20261003.py'),str(inputs),str(outputs)],cwd=ROOT,check=True)
    native=json.loads(outputs.read_text());by_key={r['key']:r for r in native['replies']};report=[];total=Counter()
    for c in captures:
        windows=[];skipped=[]
        for req in requests:
            if req['path']!=c['path']:continue
            reply=by_key[req['key']]
            if 'pendingReason' in reply:skipped.append(dict(dumpId=req['dumpId'],line=req['beforeLine'],reason=reply['pendingReason']));continue
            actual=reply['actual'];cb=req['after'].get('contactBuffer') or {};raw=bytes((cb.get('window') or {}).get('rawBytes') or [])
            expected=[]
            if len(raw)<4100:skipped.append(dict(dumpId=req['dumpId'],reason='Incomplete actual contact output buffer.'));continue
            count=struct.unpack_from('<I',raw,4096)[0]
            if count>64:skipped.append(dict(dumpId=req['dumpId'],reason='Invalid sampled contact count.'));continue
            for i in range(count):expected.append(list(struct.unpack_from('<7I',raw,i*64))+[struct.unpack_from('<I',raw,i*64+52)[0]])
            observed=[contact_words(p) for p in actual['points']]
            windows.append(dict(dumpId=req['dumpId'],beforeLine=req['beforeLine'],afterLine=req['afterLine'],
                unityContactCount=count,localContactCount=actual['contact_count'],unityContactWords=expected,localContactWords=observed,
                exact=count==actual['contact_count'] and expected==observed,measuredPoseInputsUnchanged=reply['measuredPoseInputsUnchanged']))
        checks=dict(compared=len(windows),exact=sum(w['exact'] for w in windows),different=sum(not w['exact'] for w in windows),
            geometricWordsCompared=sum(1+8*w['unityContactCount'] for w in windows))
        total.update(checks);report.append(dict(path=c['path'],unityEventsSha256=c['sha256'],checks=checks,comparedWindows=windows,pending=skipped,
            firstDifference=next((w for w in windows if not w['exact']),None)))
    result=dict(captures=len(report),capturesWithComparedCalls=sum(bool(c['checks']['compared']) for c in report),
        capturesWithDifferences=sum(bool(c['checks']['different']) for c in report),totals=dict(total),capturesInventory=report,
        pendingUnpairedWindows=pending,nativeModuleSha256=native['nativeModuleSha256'],productionSourceSha256=native['productionSourceSha256'],
        nativeRepliesSha256=hashlib.sha256(outputs.read_bytes()).hexdigest(),
        scope='Measured complete convex/convex function input including persistent cache -> current native PCM output. Contact count, seven geometric f32 words and face index; exclude uninitialized/material scratch fields and unseen scene history.',
        unityFunctionIndex=70576,contactOutputLayout='Gu::ContactBuffer count@4096, stride64, normal/separation/point@0..24, internalFaceIndex1@52.')
    (OUT/'pcm_windows.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('capturesInventory','pendingUnpairedWindows')},indent=2))
if __name__=='__main__':main()
