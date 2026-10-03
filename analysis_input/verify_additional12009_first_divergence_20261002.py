"""Record observed entry/exit bounds for the new step-313 divergence."""
import json
import struct

import validate_multiple_cases_20261002 as validation


def main():
    v=validation
    out=v.BASE/'additional_case_validation_20261002'
    events=v.event_path(out/'additional12009_unity')
    native_path=out/'additional12009_native_step313_trace.json'
    native=json.loads(native_path.read_text())
    trace=native['nativePhases'][0]
    core=next(v.rows(events,'a12.tail_phase_core'))['mainCorePtr']
    phases=[r for r in v.rows(events,'a12.tail_phase_core') if r['solverSerial']==313]
    entry=next(r for r in phases if r['phase']=='PxsDynamics.solverSetupSolve' and r['edge']=='enter')
    exit=next(r for r in phases if r['phase']=='PxsDynamics.solverSetupSolve' and r['edge']=='exit')
    def words(row):
        return v.pose_first(next(c for c in row['cores'] if c['corePtr']==core)['bits'])
    data=trace['solver_setup'][0]['body_data'][0]
    values=data['body2world']['p']+data['body2world']['q']+data['linear_velocity']+data['angular_velocity']
    local_entry=list(struct.unpack('<13I',struct.pack('<13f',*values)))
    report_path=out/'additional12009_comparison.json'
    report=json.loads(report_path.read_text())
    assert words(entry)==local_entry
    assert report['firstDifference']['physicsTick']==313
    assert report['firstDifference']['field']=='qy'
    assert report['observer']['unpatchedWasmControl']
    assert words(exit)!=trace['afterNativeBits'][0]
    assert all(words(r)==words(exit) for r in phases if r['phase']=='normalizeCandidate.121708')
    result=dict(physicsTick=313,setterOrdinal=314,
        unitySolverSetupSolveFunctionIndex=71259,unitySolverSetupSolveTableIndex=120569,
        unitySubsequentNormalizeFunctionIndex=72606,unitySubsequentNormalizeTableIndex=121708,
        earliestCompletedBoundaryDifference=report['firstDifference'],
        allCompletedStatesThroughStep312ByteIdentical=True,
        firstStoneContactTick=report['firstNativeContactTick'],
        solverEntryP_Q_v_wByteIdentical=True,
        unitySolverEntryBits=words(entry),nativeSolverEntryBits=local_entry,
        unitySolverExitBits=words(exit),nativeSimulateExitBits=trace['afterNativeBits'][0],
        nativeCompletedBits=native['states'][312][0],
        sampledUnityPhases=[dict(phase=r['phase'],edge=r['edge'],bits=words(r)) for r in phases],
        observedScope='Difference is present at solverSetupSolve exit, before subsequent normalizeCandidate.121708 calls. Only P/Q/v/w at the entry were compared here; full contact/constraint inputs and the responsible arithmetic instruction remain unverified.',
        observer=report['observer'],productionSourceSha256=native['sourceSha256'],
        nativeModuleSha256=native['moduleSha256'],
        evidence={str(f.relative_to(v.ROOT)):v.digest(f) for f in
                  (events,native_path,report_path,v.BASE/'unity_20260930.wat')})
    target=out/'case12009_step313_first_divergence.json'
    target.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8')
    print(json.dumps(dict(physicsTick=313,solverEntryP_Q_v_wByteIdentical=True,
        differingFields=[v.FIELDS[i] for i,(a,b) in enumerate(zip(words(exit),trace['afterNativeBits'][0])) if a!=b],
        unpatchedWasmControl=True,evidence=str(target.relative_to(v.ROOT)))))


if __name__=='__main__':main()
