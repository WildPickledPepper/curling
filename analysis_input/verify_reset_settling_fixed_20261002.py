"""Audit the fresh reset outputs and stop at the first observed bit mismatch."""
import hashlib
import json
import struct
from pathlib import Path
from verify_pcm_internal_trace import events, rows_of

ROOT=Path(__file__).resolve().parents[1]


def bits(values):
    return list(struct.unpack('<%dI'%len(values),struct.pack('<%df'%len(values),*values)))


def main():
    directory=ROOT/'analysis_input/unity_reset_roster_first_case_20261002'
    captured,unity_path=events(directory)
    baseline_dir=ROOT/'analysis_input/unity_scene_chain_from_start_20261002'
    baseline,_=events(baseline_dir)
    assert not [x for x in captured if 'failed' in x['type']]
    friction=rows_of(captured,'sliding.random_range.friction')
    assert len(friction)==1562 and friction==rows_of(baseline,'sliding.random_range.friction')[:1562]
    sample=lambda d:json.loads(next(d.glob('*.jsonl')).read_text().splitlines()[0])
    a,b=sample(directory),sample(baseline_dir)
    for field in ('sample_id','after_position','final_xy','target_moves','requested','collision_observed'):
        assert a[field]==b[field],field
    native_path=ROOT/'analysis_input/native_reset_settling_fixed_20261002.json'
    native=json.loads(native_path.read_text())
    writes=rows_of(captured,'a10.release_reset_orientation')[0]['release']['reset']['positionWrites'][:16]
    for i,write in enumerate(writes):
        n=next(w for w in native['positionWrites'] if w['index']==i)
        assert bits(write['sourceVector'])==bits(n['state']['physxPosition']),i
    exits=[r['cores'][0] for r in rows_of(captured,'scene.reset_body_cores') if r['edge']=='exit']
    offsets={'P':[32,36,40],'Q':[16,20,24,28],'linearVelocity':[80,84,88],'angularVelocity':[96,100,104]}
    first=None
    for step,(u,n) in enumerate(zip(exits,native['frames']),1):
        truth=dict(zip(u['offsets'],u['bits']))
        s=n['after']; q=s['quaternionWxyz']
        state={'P':s['physxPosition'],'Q':q[1:]+q[:1],
               'linearVelocity':s['physxLinearVelocity'],'angularVelocity':s['physxAngularVelocity']}
        differences={key:{'unityBits':[truth[o] for o in off],'nativeBits':bits(state[key])}
                     for key,off in offsets.items() if [truth[o] for o in off]!=bits(state[key])}
        if differences:
            first={'resetPhysicsStep':step,'boundary':'Unity solverSetupSolve exit / native Scene output plus f72606 writeback',
                   'differences':differences}
            break
    assert first and first['resetPhysicsStep']==6,first
    result={'sampleId':11000,'oracleStateInjected':False,
            'programIdentity':{'unityOriginalWasmSha256':'cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81',
                               'nativeModuleSha256':json.loads((ROOT/'analysis_input/native_reset_settling_regression_20261002/calls.json').read_text())['moduleSha256']},
            'resetPositionWordsExact':48,'firstFiveStepsPQLinearAngularWordsExact':65,
            'firstObservedResetOutputDifference':first,'nativeReachedSleepAfterSteps':len(native['frames']),
            'observerVerification':{'frictionRecordsExact':1562,'endpointFieldsUnchanged':True},
            'wholeScenePrefixAligned':False,
            'limits':['This compares all P/Q/v/w output words of the target, not every internal contact/cache value.',
                      'Mass/cooking intermediates and every startup attribute write are not fully closed.',
                      'Sleep boundary and later reset frames are not yet bitwise aligned.'],
            'nextTrace':'Step 6 target/ice PCM cache, contact/friction constraints, solver inputs and first differing intermediate.',
            'evidenceSha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in (unity_path,native_path)},
            'sourceSha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in (ROOT/'local_simulator/unity_physx.py',)}}
    (ROOT/'analysis_input/reset_settling_verified_20261002.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('Reset: 48 position words and first 5 x 13 output words exact; first observed mismatch at physics step 6.')


if __name__=='__main__':
    main()
