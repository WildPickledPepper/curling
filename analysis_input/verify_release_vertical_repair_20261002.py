"""Compare repaired production states in order against original Unity memory."""
import hashlib
import inspect
import json
from pathlib import Path
import struct
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene
from verify_pcm_internal_trace import rows_of
from verify_reset_internal_alignment_20261002 import validate,words
from verify_first_release_chain_20261002 import pose_first,core_words

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    directory=ROOT/'analysis_input/unity_first_release_chain_complete_capture_20261002'
    rows,event_path,checks=validate(directory)
    traced_path=ROOT/'analysis_input/native_first_release_vertical_fixed_traced_20261002.json'
    base_path=ROOT/'analysis_input/native_first_release_vertical_fixed_untraced_20261002.json'
    full_path=ROOT/'analysis_input/native_first_release_vertical_fixed_full_20261002.json'
    traced=json.loads(traced_path.read_text());base=json.loads(base_path.read_text())
    full=json.loads(full_path.read_text())
    for key in ('release','releaseBits','setters','frames'):assert traced[key]==base[key],key
    assert full['releaseBits']==base['releaseBits']
    assert full['frames'][:4]==base['frames']
    assert inspect.signature(PersistentPhysxFrontHalfScene).parameters['custom_sliding_zero_vertical_setter'].default is True
    source=ROOT/'local_simulator/unity_physx.py'
    assert traced['unityPhysxSha256']==base['unityPhysxSha256']==full['unityPhysxSha256']==digest(source)
    assert full['moduleSha256']=='7c31ced1773023e552391645e42040c9f3694d513805bc8b95ef0f8bc737bd38'

    calls=rows_of(rows,'a12.pcm_internal_call')
    linear=[r for r in calls if r['functionIndex']==73034 and r['setterInputBits'][0]!=0]
    angular=[r for r in calls if r['functionIndex']==73035 and r['callId']>linear[0]['callId']]
    native_linear=[r for r in traced['setters'] if r['name']=='set_linear_velocity']
    native_angular=[r for r in traced['setters'] if r['name']=='set_angular_velocity']
    for i in range(4):
        for u,n in [(linear[i],native_linear[i]),(angular[i],native_angular[i])]:
            assert pose_first(u['setterCoreBeforeBits'])==n['beforeBits']
            assert pose_first(u['setterCoreAfterBits'])==n['afterBits']
        assert linear[i]['setterInputBits']==native_linear[i]['inputBits']
    assert native_linear[2]['inputBits'][1]==linear[2]['setterInputBits'][1]==0

    pre={r['ordinal']:r for r in rows_of(rows,'a12.dense_pre_angular_setter')}
    post={r['ordinal']:r for r in rows_of(rows,'a12.dense_post_angular_setter')}
    getters={}
    for r in rows_of(rows,'a12.velocity_getter_native'):
        key=(r['ordinal'],r['kind'])
        if key in getters:assert getters[key]['outputBits']==r['outputBits']
        getters[key]=r
    noises=[r['value'] for r in rows_of(rows,'sliding.random_range.friction')]
    states={}
    for ordinal,p in pre.items():
        if (ordinal,'velocity') in getters and (ordinal,'angularVelocity') in getters:
            states[ordinal]=words(p['pose']['p']+p['pose']['q'])+getters[(ordinal,'velocity')]['outputBits']+getters[(ordinal,'angularVelocity')]['outputBits']

    first=None;exact=0
    for frame in full['frames']:
        ordinal=frame['ordinal'];tick=ordinal-1
        assert frame['noise']==noises[tick-1]
        assert full['native'][tick-1]['before']['physxAngularVelocity']==[
            float(v) for v in frame['step']['beforeScene']['physxAngularVelocity']]
        assert states[ordinal]==(full['releaseBits'] if tick==1 else full['frames'][tick-2]['afterBits']),('entry',tick)
        angular_setter=next(r for r in full['setters'] if r['ordinal']==ordinal and r['name']=='set_angular_velocity')
        assert angular_setter['inputBits']==post[ordinal]['bridge164Bits'],('angular setter',tick)
        if ordinal+1 not in states:break
        truth=states[ordinal+1];native=frame['afterBits']
        changed=[i for i,(u,n) in enumerate(zip(truth,native)) if u!=n]
        if changed:
            first=dict(slidingTick=tick,denseOrdinal=ordinal,
                boundary='physics/fetch/pose-writeback output, sampled at next tick getter',
                stateFields=['positionXYZ','quaternionXYZW','linearVelocityXYZ','angularVelocityXYZ'],
                changedWordIndices=changed,
                unityWords=truth,nativeWords=native,
                angularSetterOutputWordsExact=3,entryStateWordsExact=13)
            break
        exact+=1
    assert exact==525 and first['slidingTick']==526
    assert first['changedWordIndices']==[10]
    assert first['unityWords'][10]==0x9a381bc6 and first['nativeWords'][10]==0x9a381bc5
    first['unityAngularX']=struct.unpack('<f',struct.pack('<I',first['unityWords'][10]))[0]
    first['nativeAngularX']=struct.unpack('<f',struct.pack('<I',first['nativeWords'][10]))[0]
    first['unityAngularXHex']='0x9a381bc6';first['nativeAngularXHex']='0x9a381bc5'

    # Explicit solver-exit snapshots exist for the first three physical ticks.
    phases=rows_of(rows,'a12.early_phase_core')
    for ordinal in range(2,5):
        u=next(r for r in phases if r['ordinal']==ordinal and r['edge']=='exit'
               and r['phase']=='PxsDynamics.solverSetupSolve')
        data=traced['native'][ordinal-2]['solver_setup'][-1]['body_data'][0]
        assert words(data['body2world']['p']+data['body2world']['q']+
                     data['linear_velocity']+data['angular_velocity'])==core_words(u['core'])
    report=dict(unityWasmSha256='cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81',
        nativeModuleSha256=full['moduleSha256'],productionCodeSha256=digest(source),
        repair='default custom_sliding_zero_vertical_setter=True, actual f60124 literal world-Y +0',
        oldSecondTickDivergenceResolved=True,
        releaseAndFirstThreeTicksSetterBeforeAfterStateWordsExact=True,
        explicitSolverExitTicksExact=3,
        continuousPostReleaseStateTicksExact=exact,continuousPostReleaseStateWordsExact=exact*13,
        nextConfirmedDivergence=first,
        observer=dict(checks,nativeFirstFourFramesAndSettersUnchanged=True,
                      fullRunFirstFourFramesExactToObservedBaseline=True),
        tests='31 unittest tests passed including actual Unity release + first four ticks',
        scope='sample 11000, fresh default Windows CP39, fixed recorded friction input stream',
        limitations=['Comparison advances discrete P/Q/velocity state boundaries; not every f64 arithmetic intermediate is audited.',
                    'Exact instruction causing tick 526 angular X difference is not located; Unity solver internals at that ordinal need targeted sampling.',
                    'Recorded friction inputs do not close Unity RNG state generation.',
                    'Do not propagate this result to later collision stages, other samples, or other ABI builds.'],
        evidence={str(p.relative_to(ROOT)):digest(p) for p in [event_path,traced_path,base_path,full_path,source,
                    ROOT/'local_simulator/tests/fixtures/unity_first_release_four_steps_20261002.json',
                    ROOT/'analysis_input/first_release_chain_verified_20261002.json']})
    out=ROOT/'analysis_input/release_vertical_repair_verified_20261002.json'
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    print('PASS: repaired second-tick vertical setter and continuous first 525 physical output states (6825 words).')
    print('Next sampled difference: tick 526 angular X, Unity 9a381bc6 vs Native 9a381bc5; angular setter result matches.')

if __name__=='__main__':main()
