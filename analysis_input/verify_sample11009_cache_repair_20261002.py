"""Verify the repaired cache branch, arithmetic and completed trajectories."""
import hashlib
import json
import struct
from pathlib import Path

from verify_pcm_internal_trace import events, rows_of, raw_argument
from verify_release_ordinary_tail_20261002 import core_states

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'analysis_input'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def bits(v): return struct.pack('<%df'%len(v),*v)

def main():
    investigation=BASE/'sample11009_step1383_internals_verified_20261002.json'
    established=json.loads(investigation.read_text())
    unity,path=events(BASE/'unity_sample11009_step1383_capture_v2_20261002')
    assert digest(path)==established['evidenceSha256'][str(path.relative_to(ROOT))]
    truth,truth_path=events(BASE/'unity_new_sample_11009_capture_20261002')
    assert digest(truth_path)==established['evidenceSha256'][str(truth_path.relative_to(ROOT))]
    native_path=BASE/'native_sample11009_cache_fixed_3000_20261002.json'
    native=json.loads(native_path.read_text())
    code=ROOT/'local_simulator/unity_physx.py'
    assert digest(code)==native['sourceSha256']
    assert native['moduleSha256']==established['hashes']['nativeModule']
    bounds={r['solverSerial']:core_states(r) for r in rows_of(truth,'a12.tail_phase_core')
        if r['phase']=='DCP.FixedUpdate.boundary'}
    assert len(native['states'])==3000
    assert native['releaseBits']==bounds[0]
    assert all(native['states'][i-1]==bounds[i] for i in range(1,3001))
    before=json.loads((BASE/'native_bestshot_offset_fixed_11009_20261002.json').read_text())
    assert [i+1 for i,(a,b) in enumerate(zip(before['states'],native['states'])) if a!=b]==[1383]
    calls_path=BASE/'native_sample11009_step1383_cache_fixed_calls_20261002/calls.json'
    calls=json.loads(calls_path.read_text())
    assert calls['moduleSha256']==native['moduleSha256']
    assert calls['callStackReliable'] and not calls['unfinished'] and not calls['dropped']
    observed=json.loads(calls_path.with_name('alignment.json').read_text())
    assert observed['states']==native['states'] and observed['releaseBits']==native['releaseBits']
    clear=calls['calls'][0]
    assert clear['functionRva']=='0x330f0'
    assert clear['multiCacheBefore']==clear['multiCacheAfter']
    assert clear['multiCacheBefore']['cachedSize']==304
    ur=next(r for r in rows_of(unity,'a12.pcm_internal_call') if r['functionIndex']==69978)
    nr=next(r for r in calls['calls'] if r['functionRva']=='0x29cbe0')
    for edge in ('before','after'):
        a,b=raw_argument(ur,1,edge),raw_argument(nr,0,edge)
        # Active five 64-byte records: 12 arithmetic words and the face ID.
        # The next three words per record are padding, never read by f69978.
        for i in range(5): assert a[i*64:i*64+52]==b[i*64:i*64+52]
        assert a[384:388]==b[384:388] # active contact count
    for arg,size in ((2,60),(3,4)):
        assert raw_argument(ur,arg,'before')[:size]==raw_argument(nr,arg,'before')[:size]
    pcm=next(r for r in rows_of(unity,'a12.pcm_convex_mesh') if r['ordinal']==1384
        and r['before']['transform0']['p'][0]==-71.17739868164062)
    npcm=next(r for r in calls['calls'] if r['functionRva']=='0x2e2880')
    raw=raw_argument(npcm,8,'after')
    for i,p in enumerate(pcm['after']['contactBuffer']['contactsPreview']):
        assert bits(p['normal']+[p['separation']]+p['point'])==raw[i*64:i*64+28]
    static=[]; serial=0
    for r in unity:
        d=r['data']
        if r['type']=='a12.tail_phase_core' and d['phase']=='PxsDynamics.solverSetupSolve' and d['edge']=='enter':
            serial=d['solverSerial']
        if serial==2 and r['type']=='a12.static_solve': static.append(d)
    n=native['nativePhases'][1]
    assert n['physicsTick']==1383
    target_x=-71.17739868164062
    index=next(i for i,r in enumerate(static[0]['before']['solverBodyData']) if r['bodyA']['body2World']['p'][0]==target_x)
    solves=[r for r in n['solve_block'] if r['constraint_type']==5 and r['data_a_before']['body2world']['p'][0]==target_x]
    assert len(static)==len(solves)==5
    for a,b in zip(static,solves):
        ua=bytes(a['before']['descs'][index]['constraintWindow']['rawBytes'])
        nb=bytes(b['constraint_bytes_before'])
        assert ua[:56]==nb[:56]
        assert ua[64:304]==nb[80:320] # five normal constraints
        for i in range(4):
            for off in list(range(0,32,4))+[44,48]:
                assert ua[336+i*64+off:340+i*64+off]==nb[352+i*64+off:356+i*64+off]
        for side in ('before','after'):
            ua=bytes(a[side]['descs'][index]['bodyAWindow']['rawBytes'])
            bbody=b['body_a_'+side]
            assert ua[:12]==bits(bbody['linear_velocity'])
            assert ua[16:28]==bits(bbody['angular_state'])
    old_path=BASE/'native_sample11000_cache_fixed_3362_20261002.json'
    old=json.loads(old_path.read_text())
    old_before_path=BASE/'native_bestshot_offset_fixed_11000_20261002.json'
    old_before=json.loads(old_before_path.read_text())
    assert old['sourceSha256']==native['sourceSha256'] and old['moduleSha256']==native['moduleSha256']
    assert len(old['states'])==3362 and old['states']==old_before['states']
    assert old['releaseBits'][0]==old_before['releaseBits']
    old_truth,old_truth_path=events(BASE/'unity_release_both_complete_activation_v2_20261002')
    old_bounds={r['solverSerial']:core_states(r) for r in rows_of(old_truth,'a12.tail_phase_core')
        if r['phase']=='DCP.FixedUpdate.boundary' and r['solverSerial']>=1}
    assert all(old_bounds[i]==old['states'][i-1] for i in range(1,2001))
    evidence=[investigation,path,truth_path,native_path,calls_path,calls_path.with_name('alignment.json'),
        old_path,old_before_path,old_truth_path,code,Path(__file__),
        ROOT/'local_simulator/tests/test_unity_preserved_ice_cache.py',
        ROOT/'local_simulator/tests/fixtures/unity_preserved_ice_cache_11009_20261002.json']
    result=dict(sampleId=11009,productionCodeSha256=native['sourceSha256'],nativeModuleSha256=native['moduleSha256'],
        unityWasmSha256=established['hashes']['unityWasm'],
        repair='Disable unconditional multi-cache clearing by default. Preserve standard PhysX invalidation through the existing actual no-autowake pose-writeback path.',
        internalVerification=dict(physicsTick=1383,nativeClearHookRva='0x330f0',cachedSizeBeforeAndAfter=304,
            entireCachedPayloadUnchanged=True,unityRefreshFunction=69978,nativeRefreshFunctionRva='0x29cbe0',
            activeContactRecordWordsExactBeforeAndAfter=65,refreshMatrixWordsExact=15,refreshThresholdExact=True,
            pcmContactOutputWordsExact=35,normalConstraintWordsExactPerIteration=60,frictionArithmeticWordsExactPerIteration=40,
            targetStaticSolverIterationsExact=5,solverBodyNumericWordsExactPerInputAndOutput=6),
        sample11009=dict(releaseStateWordsExact=26,completedStepsExact=3000,completedStateWordsExact=78000,
            changedCompletedStepsVersusBeforeRepair=[1383],firstObservedRemainingCompletedStateDifference=None,
            observedNativeOutputsUnchanged=3000),
        sample11000=dict(nativeRegressionStepsUnchanged=3362,unityCompletedStepsExact=2000),
        limits=['Boundary state equality is limited to these samples and captured steps; it does not establish all unsampled internal calculations or all possible scenarios.'],
        evidenceSha256={str(p.relative_to(ROOT)):digest(p) for p in evidence})
    out=BASE/'sample11009_cache_repair_verified_20261002.json'
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8')
    print(json.dumps({k:result[k] for k in ('internalVerification','sample11009','sample11000')},indent=2))

if __name__=='__main__': main()
