"""Require all observed numerical registration words to match Unity."""
import hashlib
import json
from pathlib import Path
import struct

from verify_pcm_internal_trace import events, rows_of

ROOT = Path(__file__).resolve().parents[1]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def raw(call):
    return bytes.fromhex(next(b['hex'] for b in call['before'] if b['argument'] == 2))


def main():
    u, event_path = events(ROOT/'analysis_input/unity_scene_chain_from_start_20261002')
    u = sorted((c for c in rows_of(u,'a12.pcm_internal_call') if c['functionIndex']==71726), key=lambda c:c['callId'])[:26]
    u = [c for c in u if struct.unpack_from('<I',raw(c),140)[0]==0x3d567344]
    native_path = ROOT/'analysis_input/native_startup_registration_fixed_v2_20261002/calls.json'
    native = json.loads(native_path.read_text())
    assert native['callStackReliable'] and not native['dropped'] and not native['unfinished']
    n = [c for c in native['calls'] if c['functionRva']=='0x214bd0']
    n = [c for c in n[:18] if struct.unpack_from('<I',raw(c),140)[0]==0x3d567344]
    fixture = json.loads((ROOT/'local_simulator/tests/fixtures/unity_stone_registration_20261002.json').read_text())
    assert len(u)==len(n)==16
    verified = []
    for index,(a,b) in enumerate(zip(u,n)):
        aw = [struct.unpack_from('<I',raw(a),off)[0] for off in fixture['offsets']]
        bw = [struct.unpack_from('<I',raw(b),off)[0] for off in fixture['offsets']]
        assert aw==bw==fixture['bits'], (index,aw,bw)
        verified.append({'stoneCreationIndex':index,'unityCallId':a['callId'],'nativeCallId':b['callId']})
    directory = native_path.parent
    actual = json.loads((directory/'alignment.json').read_text())
    baseline = json.loads((ROOT/'analysis_input/c131_getter_gap_closed_20261002.json').read_text())
    assert actual['rows']==baseline['rows'] and actual['aggregate']==baseline['aggregate']
    # Different ABI capture sizes in other report parts are not compared as bytes.
    a = next(c for c in actual['releaseBoundary'] if c['sampleId']==11005)
    b = next(c for c in baseline['releaseBoundary'] if c['sampleId']==11005)
    assert a['setters']==b['setters']
    assert len(a['ticks'])==len(b['ticks'])==1022
    for actual_tick, baseline_tick in zip(a['ticks'], b['ticks']):
        # Lifecycle captures have extra solver observations at ordinals 2-22;
        # compare the body inputs/outputs at every tick, not trace scheduling.
        for field in ('input','beforeScene','afterScene','rawAfterQ'):
            assert actual_tick[field] == baseline_tick[field]
    report = {'closedBoundary':'Initial Sc::RigidSim registration numerical input for 16 stones',
        'unityFunctionIndex':71726,'nativeFunctionRva':'0x214bd0',
        'numericWordsPerStone':len(fixture['offsets']),'verifiedWordCount':16*len(fixture['offsets']),
        'calls':verified,'rawIEEE754BitsExactIncludingSignedZeros':True,
        'postStartupAngularSpeedLimit':20,'postStartupLimitEvidence':'Subsequent Unity f71726 inputs and solver cores: maxAngularVelocitySq = 0x43c80000.',
        'initialRegistrationWholeAbiEqualClaimed':False,
        'completeScenePrefixAligned':False,
        'scopeLimits':['Pointers and ABI padding excluded; internal reserved identity-transform flag encodings differ between PhysX versions.',
                       'Factory/cooking internals, complete roster and attribute-sync order have not all been traced.',
                       'Reactivation constructor inputs, Reset settling and sleep are not yet closed.'],
        'regression':{'shots':12,'rowsAndAggregatesUnchanged':True,'active11005SettersAndTicksUnchanged':True},
        'evidenceSha256':{str(p.relative_to(ROOT)):sha(p) for p in [event_path,native_path,directory/'alignment.json']},
        'sourceSha256':{str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'local_simulator/unity_physx.py',ROOT/'local_simulator/runtime_support/tools/reverse/probe_physx_collision_alignment.py']}}
    output=ROOT/'analysis_input/stone_registration_fixed_20261002.json'
    output.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    print('16 stones x 35 words = 560 exact; 12 shot regressions and 11005 recorded ticks/setters unchanged')


if __name__=='__main__':
    main()
