"""Match actual initial stone constructor numeric core inputs, excluding ABI data."""
from collections import Counter
import hashlib,json,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'analysis_input/local_partial_validation_20261003'
OFFSETS=list(range(16,44,4))+list(range(48,160,4))
def raw(c,edge):return bytes.fromhex(next(w['hex'] for w in c[edge] if w['argument']==2))
def words(c,edge):return [struct.unpack_from('<I',raw(c,edge),n)[0] for n in OFFSETS]
def main():
    native_path=ROOT/'analysis_input/native_startup_numeric_partial_20261003/calls.json'
    native=json.loads(native_path.read_text());observed=json.loads(native_path.with_name('alignment.json').read_text())
    assert native['callStackReliable'] and not native['dropped'] and not native['unfinished']
    assert observed['observerStartupStatesUnchanged']
    assert observed['productionSourceSha256']==hashlib.sha256((ROOT/'local_simulator/unity_physx.py').read_bytes()).hexdigest()
    assert native['moduleSha256']==hashlib.sha256((ROOT/'local_simulator/runtime/pyphysx/_pyphysx.cp39-win_amd64.pyd').read_bytes()).hexdigest()
    nc=[c for c in native['calls'] if c['functionRva']=='0x214bd0' and struct.unpack_from('<I',raw(c,'before'),140)[0]==0x3d567344]
    assert len(nc)==16
    inventory=json.loads((OUT/'inventory.json').read_text());reports=[];totals=Counter()
    for r in inventory['capturesInventory']:
        if not r['eventCounts'].get('a12.pcm_internal_call'):continue
        first_reset=min((c['line'] for c in r['commands'] if c['type']=='websocket.recv' and c['text'].startswith(('RESETPOSITION','BESTSHOT'))),default=10**12)
        uc=[];hashes=hashlib.sha256()
        for n,line in enumerate((ROOT/r['path']).open('rb'),1):
            hashes.update(line)
            if n>=first_reset or b'a12.pcm_internal_call' not in line:continue
            e=json.loads(line)
            if e['type']!='a12.pcm_internal_call' or e['data']['functionIndex']!=71726:continue
            c=e['data'];c['_line']=n
            try:mass=struct.unpack_from('<I',raw(c,'before'),140)[0]
            except (KeyError,StopIteration,struct.error):continue
            if mass==0x3d567344:uc.append(c)
        assert hashes.hexdigest()==r['sha256']
        if not uc:continue
        comparisons=[]
        for i,(u,n) in enumerate(zip(uc,nc)):
            for edge in ('before','after'):
                try:expected=words(u,edge);actual=words(n,edge)
                except (KeyError,StopIteration,struct.error):continue
                comparisons.append(dict(stoneCreationIndex=i,unityCallId=u['callId'],line=u['_line'],edge=edge,nativeCallId=n['callId'],
                    localWords=actual,unityWords=expected,exact=actual==expected))
        counts=dict(compared=len(comparisons),exact=sum(c['exact'] for c in comparisons),different=sum(not c['exact'] for c in comparisons),wordsCompared=len(comparisons)*len(OFFSETS))
        totals.update(counts)
        reports.append(dict(path=r['path'],unityEventsSha256=r['sha256'],checks=counts,observedStartupStoneCalls=len(uc),
            comparedWindows=comparisons,firstDifference=next((c for c in comparisons if not c['exact']),None),
            excludedExtraInitialStoneCalls=max(0,len(uc)-16)))
    result=dict(captures=len(reports),totals=dict(totals),capturesWithDifferences=sum(bool(r['checks']['different']) for r in reports),
        capturesInventory=reports,sourceSha256=observed['productionSourceSha256'],nativeModuleSha256=native['moduleSha256'],
        numericCoreOffsets=OFFSETS,unityFunctionIndex=71726,nativeFunctionRva='0x214bd0',
        nativeCaptureSha256=hashlib.sha256(native_path.read_bytes()).hexdigest(),observerStartupStatesUnchanged=True,
        scope='Actual initial formal-stone ScRigidCore constructor input/output numeric words. Pointers, padding, reserved transform flags, other actors and earlier factory/cooking stages are excluded; not complete serial-prefix proof.')
    (OUT/'startup_windows.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in result.items() if k!='capturesInventory'},indent=2))
if __name__=='__main__':main()
