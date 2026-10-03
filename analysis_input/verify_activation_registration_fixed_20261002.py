"""Compare every observed stone registration, with exact field semantics."""
import hashlib
import json
import struct
from pathlib import Path
from verify_pcm_internal_trace import events, rows_of

ROOT = Path(__file__).resolve().parents[1]


def raw(call):
    return bytes.fromhex(next(b['hex'] for b in call['before'] if b['argument'] == 2))


def main():
    rows, unity_path = events(ROOT/'analysis_input/unity_scene_chain_from_start_20261002')
    constructors = sorted((c for c in rows_of(rows,'a12.pcm_internal_call')
                           if c['functionIndex']==71726),key=lambda c:c['callId'])
    u = [c for c in constructors if struct.unpack_from('<I',raw(c),140)[0]==0x3d567344]
    native_path = ROOT/'analysis_input/native_reset_settling_regression_20261002/calls.json'
    native = json.loads(native_path.read_text())
    assert native['callStackReliable'] and not native['dropped'] and not native['unfinished']
    n = [c for c in native['calls'] if c['functionRva']=='0x214bd0'
         and struct.unpack_from('<I',raw(c),140)[0]==0x3d567344]
    offsets=list(range(16,44,4))+list(range(48,160,4))
    assert len(u)==len(n)==40
    checks=[]
    for ordinal,(a,b) in enumerate(zip(u,n)):
        for offset in offsets:
            assert struct.unpack_from('<I',raw(a),offset)[0]==struct.unpack_from('<I',raw(b),offset)[0], (ordinal,offset)
        checks.append({'stoneRegistrationOrdinal':ordinal,'unityCallId':a['callId'],'nativeCallId':b['callId']})
    actual=json.loads((native_path.parent/'alignment.json').read_text())
    baseline=json.loads((ROOT/'analysis_input/c131_getter_gap_closed_20261002.json').read_text())
    assert actual['aggregate']==baseline['aggregate']
    target_state_changes=[]
    for x,y in zip(actual['rows'],baseline['rows']):
        for field in x.keys() | y.keys():
            if field != 'firstContactEntrance':
                assert x.get(field)==y.get(field),(x['sampleId'],field)
        for field in ('active','afterScene'):
            assert x['firstContactEntrance'][field]==y['firstContactEntrance'][field]
        if x['firstContactEntrance']!=y['firstContactEntrance']:
            target_state_changes.append(x['sampleId'])
    a=next(r for r in actual['releaseBoundary'] if r['sampleId']==11005)
    b=next(r for r in baseline['releaseBoundary'] if r['sampleId']==11005)
    assert len(a['setters'])==1023 and a['setters']==b['setters']
    for x,y in zip(a['ticks'],b['ticks']):
        for field in ('input','beforeScene','afterScene','rawAfterQ'):
            assert x[field]==y[field], field
    result={'boundary':'Sc::RigidSim registration numerical input',
            'unityFunctionIndex':71726,'nativeFunctionRva':'0x214bd0',
            'nativeModuleSha256':native['moduleSha256'],
            'initialRegistrationsExact':16,'reactivationsExact':24,
            'wordsPerRegistration':35,'totalExactWords':1400,'checks':checks,
            'floatComparison':'raw binary32 words including signed zeros',
            'regression':{'shots':12,'endpointOutcomesAndAggregatesUnchanged':True,
                          'activeFirstContactInputsOutputsUnchanged':True,
                          'targetStateChangedByRestoredResetFall':target_state_changes,
                          '11005SettersExact':1023},
            'wholeScenePrefixAligned':False,
            'remaining':'Attribute synchronization and Reset placement/integration/sleep. Factory/cooking internals are not fully closed.',
            'evidenceSha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in (unity_path,native_path,native_path.parent/'alignment.json')},
            'sourceSha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in (ROOT/'local_simulator/unity_physx.py',ROOT/'local_simulator/assets/unity_startup_body_roster.json')}}
    (ROOT/'analysis_input/activation_registration_fixed_20261002.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('40 x 35 = 1400 registration words exact; 12 endpoint outcomes and active 11005 unchanged; target reset states changed.')


if __name__=='__main__':
    main()
