"""Check the earliest observed full-input replay divergence and phase boundaries."""
import hashlib
import json
from pathlib import Path
import struct

from validate_multiple_cases_20261002 import rows, event_path
from verify_first_release_chain_20261002 import pose_first

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'analysis_input/multi_case_validation_20261002'


def bits(values):
    return list(struct.unpack('<%dI'%len(values),struct.pack('<%df'%len(values),*values)))


def main():
    capture=BASE/'full12004_run1_unity'
    event=event_path(capture)
    native_path=BASE/'full12004_run1_native.json'
    traced_path=BASE/'full12004_run1_native_step3169_trace.json'
    n=json.loads(native_path.read_text())
    t=json.loads(traced_path.read_text())
    assert n['states']==t['states'] and n['releaseBits']==t['releaseBits']
    pre=list(rows(event,'a12.dense_pre_angular_setter'))
    post=list(rows(event,'a12.dense_post_angular_setter'))
    assert len(pre)==len(post)==3169
    assert [r['ordinal'] for r in pre]==[r['ordinal'] for r in post]==list(range(1,3170))
    assert [r['lastFrictionNoise'] for r in pre[1:]]==n['frictionNoises']
    boundaries={r['solverSerial']:pose_first(r['bits']) for r in rows(event,'a12.tail_phase_core')
                if r['phase']=='DCP.FixedUpdate.boundary' and r['edge']=='enter'}
    assert n['releaseBits'][0]==boundaries[0]
    divergent=[step for step in range(1,4001) if n['states'][step-1][0]!=boundaries[step]]
    assert divergent==list(range(3169,3209))
    phase=next(r for r in t['nativePhases'] if r['physicsTick']==3169)
    assert phase['beforeNativeBits'][0]==boundaries[3168]
    uenter=next(r for r in rows(event,'a12.tail_phase_core') if r['solverSerial']==3169
                and r['phase']=='PxsDynamics.solverSetupSolve' and r['edge']=='enter')
    uexit=next(r for r in rows(event,'a12.tail_phase_core') if r['solverSerial']==3169
                and r['phase']=='PxsDynamics.solverSetupSolve' and r['edge']=='exit')
    setup=phase['solver_setup'][0]['body_data'][0]
    b=bits(setup['body2world']['p']+setup['body2world']['q']+setup['linear_velocity']+setup['angular_velocity'])
    assert b==pose_first(uenter['bits'])
    fields=['px','py','pz','qx','qy','qz','qw','vx','vy','vz','wx','wy','wz']
    diff=[dict(field=fields[i],unityBits=f'0x{a:08x}',nativeBits=f'0x{b:08x}',
               unityFloat=struct.unpack('<f',struct.pack('<I',a))[0],
               nativeFloat=struct.unpack('<f',struct.pack('<I',b))[0])
          for i,(a,b) in enumerate(zip(boundaries[3169],n['states'][3168][0])) if a!=b]
    assert pose_first(uexit['bits'])==boundaries[3169]
    proof_path=BASE/'full12004_run1_comparison.json'
    proof=json.loads(proof_path.read_text(encoding='utf8'))
    assert proof['observer']['unpatchedWasmControl']
    result=dict(sampleId=12004,completedStepsCompared=4000,firstCompletedStateDifferenceTick=3169,
        continuousBothStoneExactPrefixSteps=3168, differingCompletedSteps=divergent,
        rawMainPoseVelocityAtSolverSetupEnterWordsExact=13, firstObservedDifferingPhase='PxsDynamics.solverSetupSolve exit',
        firstDifference=diff, nativeReadOnlyTraceDoesNotChangeAnyCompletedState=True,
        completeInputPairs=3169, originalWasmControl=proof['observer'],
        known='The custom sliding window has ended. The next solver setup has identical observed P/Q/v/w, and the solver exit has different velocity words.',
        unknown='This capture does not contain the complete narrowphase/cache/constraint inputs of tick 3169. The differing internal calculation is not yet established.',
        nextRequiredCapture='At completed steps 3168-3170, record actual PCM cache/refresh/contact output, friction preparation and all static solve inputs/outputs, then compare in true call order.',
        excludedInvalidReplay='fresh12004_run1: dense pre-setter capture truncated at 2000; never a confirmed simulator divergence.',
        evidenceSha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in (event,native_path,traced_path,proof_path)})
    out=BASE/'case12004_first_divergence_verified.json'
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8')
    print(json.dumps({k:result[k] for k in ('firstCompletedStateDifferenceTick','rawMainPoseVelocityAtSolverSetupEnterWordsExact','firstDifference')},indent=2))


if __name__=='__main__': main()
