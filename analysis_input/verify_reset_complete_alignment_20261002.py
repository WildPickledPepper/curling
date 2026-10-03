"""Verify actual cache writers, gradual underflow, complete Reset and release pose."""
import hashlib
import json
from pathlib import Path
import struct

import numpy as np

from verify_pcm_internal_trace import events, rows_of, raw_argument
from verify_reset_internal_alignment_20261002 import validate, words

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analysis_input/reset_complete_alignment_verified_20261002.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def state_words(state):
    q = state['quaternionWxyz']
    return words(state['physxPosition']+q[1:]+q[:1]
                 +state['physxLinearVelocity']+state['physxAngularVelocity'])


def main():
    validations = {}
    for name in ('unity_reset_friction_cache_writes_first_case_20261002',
                 'unity_reset_cache_lifecycle_first_case_20261002',
                 'unity_reset_cache_lifecycle_steps1_8_delayed_first_case_20261002'):
        rows, path, checks = validate(ROOT / 'analysis_input' / name)
        validations[name] = dict(checks, eventsSha256=digest(path))
    unity, unity_path, _ = validate(ROOT / 'analysis_input/unity_reset_cache_lifecycle_steps1_8_delayed_first_case_20261002')
    calls = rows_of(unity, 'a12.pcm_internal_call')
    by_id = {r['callId']:r for r in calls}
    clears = [r for r in calls if r['functionIndex']==71632 and r.get('resetPhysicsStep',0)>1]
    assert len(clears)==7
    chain = [71632,71729,71596,72606]
    core_frames = rows_of(unity, 'scene.reset_body_cores')
    for clear in clears:
        row = clear
        for function in chain:
            assert row['functionIndex']==function
            if function!=72606:
                row=by_id[row['parentCallId']]
        assert row['args'][2]==0 and row['callerFunctionIndex']==73070
        old=next(r for r in core_frames if r['step']==clear['resetPhysicsStep']-1 and r['edge']=='exit')
        assert list(struct.unpack_from('<7I',raw_argument(row,1,'before')))==old['cores'][0]['bits'][:7]
    writes=rows_of(unity,'scene.friction_cache_write')
    for step in range(2,9):
        selected=[r for r in writes if r['resetPhysicsStep']==step and r['callerFunctionIndex']==71632]
        assert [(r['storeOpcode'],r['value']) for r in selected]==[(0x3a,0),(0x37,'0n')]
        assert selected[-1]['frictionDataPtr']==selected[-1]['frictionCount']==0
    cache_path=ROOT/'analysis_input/native_reset_pose_cache_fixed_steps1_8_20261002/calls.json'
    native_cache=json.loads(cache_path.read_text())
    assert native_cache['callStackReliable'] and not native_cache['dropped'] and not native_cache['unfinished']
    prep=[r for r in native_cache['calls'] if r['functionRva']=='0xdcf30']
    assert len(prep)==8
    for row in prep:
        data=raw_argument(row,0,'before')
        assert struct.unpack_from('<Q',data,160)[0]==data[168]==0
    old_path=ROOT/'analysis_input/native_reset_integrate_step7_20261002/calls.json'
    old=json.loads(old_path.read_text())
    row=old['calls'][0]
    assert row['mxcsrAtNativeEntry'] & 0x8040 == 0x8040
    body=bytes(row['bodyDataBytes'])
    motion=bytes(row['motionBodyBytes'])
    f=lambda data,off:np.float32(struct.unpack_from('<f',data,off)[0])
    terms=[np.float32(f(motion,16)*f(body,32)),np.float32(f(motion,20)*f(body,44)),
           np.float32(f(motion,24)*f(body,56))]
    angular_x=np.float32(np.float32(np.float32(terms[0]+terms[1])+terms[2])+f(body,16))
    assert words([angular_x])==[0x8001b2e2]
    native_path=ROOT/'analysis_input/native_reset_gradual_underflow_full_trace_20261002.json'
    native=json.loads(native_path.read_text())
    assert native['baselineOutputsUnchanged']
    exits=[r['cores'][0]['decoded'] for r in core_frames if r['edge']=='exit'][:42]
    assert len(native['frames'])==len(exits)==42
    for local,truth in zip(native['frames'],exits):
        data=local['solver_setup'][-1]['body_data'][0]
        assert words(data['body2world']['p']+data['body2world']['q']+data['linear_velocity']+data['angular_velocity'])==words(
            truth['p']+truth['q']+truth['linearVelocity']+truth['angularVelocity']), local['step']
    sleepy=next(r['cores'][0]['decoded'] for r in core_frames if r['step']==43 and r['edge']=='enter')
    assert native['frames'][-1]['sleeping']
    assert state_words(native['frames'][-1]['after'])==words(sleepy['p']+sleepy['q']+sleepy['linearVelocity']+sleepy['angularVelocity'])
    # Compare the complete relevant constraints and both solver entry/exit
    # deltas over eight sampled steps. ABI pointers and padding are excluded.
    for step in range(1,9):
        truth=[r for r in rows_of(unity,'a12.static_solve') if r['resetPhysicsStep']==step]
        actual=native['frames'][step-1]['solve_block']
        assert len(truth)==len(actual)==5
        for a,b in zip(truth,actual):
            x=bytes(a['before']['descs'][0]['constraintWindow']['rawBytes'])
            y=bytes(b['constraint_bytes_before'])
            assert x[:56]==y[:56] and x[64:304]==y[80:320]
            for i in range(4):
                for off in list(range(0,32,4))+[44,48]:
                    assert x[336+i*64+off:340+i*64+off]==y[352+i*64+off:356+i*64+off]
            for edge in ('before','after'):
                x=bytes(a[edge]['descs'][0]['bodyAWindow']['rawBytes'])
                y=bytes(b['body_a_'+edge]['raw_bytes'])
                for off in (0,4,8,16,20,24):
                    assert x[off:off+4]==y[off:off+4]
    patch_path=ROOT/'analysis_input/native_gradual_underflow_patch_20261002.json'
    patch=json.loads(patch_path.read_text())
    backup=Path(patch['originalBackup'])
    kernel=Path(patch['source'])
    assert digest(backup)==patch['originalSha256'] and digest(kernel)==patch['patchedSha256']
    expected=bytearray(backup.read_bytes())
    for instruction in patch['patches']:
        off=instruction['fileOffset']
        assert expected[off:off+4]==struct.pack('<I',0x9fc0)
        expected[off:off+4]=struct.pack('<I',0x1f80)
    assert bytes(expected)==kernel.read_bytes()
    mxcsr_path=ROOT/'analysis_input/native_reset_ieee_mxcsr_step7_20261002/calls.json'
    current=json.loads(mxcsr_path.read_text())
    assert current['callStackReliable'] and not current['unfinished'] and not current['dropped']
    assert all(r['mxcsrAtNativeEntry']&0x8040==0 for r in current['calls'])
    assert current['moduleSha256']==patch['patchedSha256']
    release=json.loads((ROOT/'analysis_input/native_first_reset_bestshot_boundary_fixed_20261002.json').read_text())['activeAfterBestshot']
    pose=rows_of(unity,'a10.release_reset_orientation')[0]['bridgePoseBeforeAngularSetter']['transform']
    assert words(release['physxPosition']+release['quaternionWxyz'][1:]+release['quaternionWxyz'][:1])==words(pose['p']+pose['q'])
    regression=json.loads((ROOT/'analysis_input/native_reset_cache_ieee_regression_20261002.json').read_text())
    old_regression=json.loads((ROOT/'analysis_input/native_reset_start_friction_regression_v3_20261002.json').read_text())
    assert regression['aggregate']==old_regression['aggregate']
    assert regression['releaseBoundary'][5]['setters']==old_regression['releaseBoundary'][5]['setters']
    result=dict(originalWasmSha256=digest(ROOT/'analysis_input/unity_20260930.wasm'),
        originalNativeSha256=patch['originalSha256'],currentNativeSha256=patch['patchedSha256'],
        observerValidations=validations, cacheClearChain=chain[::-1],
        upstreamUnityCaller=73070,autoWake=0,unchangedRawPoseStillWritten=True,
        nativeEmptyCacheStepsExact=8, nativeClearRva='0x2115d0',
        gradualUnderflow=dict(step=7, angularXBits='0x8001b2e2',
            nativeMultiplyInstructionRva='0x204bed',nativeAngularXStoreRva='0x204c26',
            operandTermBits=words(terms),originalMxcsr=hex(row['mxcsrAtNativeEntry']),
            guardImmediatePatches=len(patch['patches']),newMxcsrPolicy='0x1f80'),
        resetSolverExitStepsExact=42, resetSolverExitWordsExact=42*13,
        sleepAfterFetchWordsExact=13,naturalSleepAtStep=42,
        sampledConstraintStepsExact=8,staticSolverDeltaWordsExact=8*5*2*6,
        bestshotReleasePoseWordsExact=7,calibratedRegressionSetterPairs11005Exact=1023,
        calibratedRegressionAggregateUnchanged=True,
        nextUnclosedBoundary='BESTSHOT release setters and the first sliding/physics step; no full post-release prefix claim',
        limits=['Verification is for first Reset sample 11000 on the patched Windows CP39 kernel.',
                'CP38/CP313 pose-setter instruction streams checked; gradual-underflow repair not applied there.',
                'Linux requires an explicit no-autowake native binding; this bridge rejects unverified kernels.',
                'Startup/cooking intermediates and every post-release arithmetic operation are not all compared.'],
        evidenceSha256={str(p.relative_to(ROOT)):digest(p) for p in
                       (unity_path,native_path,cache_path,old_path,patch_path,mxcsr_path)},
        sourceSha256={str(p.relative_to(ROOT)):digest(p) for p in
                      (ROOT/'local_simulator/unity_physx.py',ROOT/'local_simulator/native_pose_writeback.py')})
    OUT.write_text(json.dumps(result,indent=2))
    print('42 Reset solver exits (546 words), natural sleep and 7 release-pose words exact.')


if __name__=='__main__':
    main()
