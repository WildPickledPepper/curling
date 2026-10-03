"""Check final production hashes, raw-state reports and complete test result."""
import hashlib
import json
from pathlib import Path

import validate_multiple_cases_20261002 as v

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'analysis_input'
work=BASE/'wall_repair_regression_20261003'
report=json.loads((work/'report.json').read_text())
assert report['fullTrajectoryRuns']==10 and report['completedStepsCompared']==37000
assert report['fullTrajectoryStateBytesCompared']==3738696
assert report['allFullTrajectoryBytesExact'] and report['allFirstDifferencesNull']
for name,digest in report['productionEvidence'].items():
    assert v.digest(ROOT/name)==digest,name
for case in report['cases']:
    assert case['productionSourceSha256']==v.digest(ROOT/'local_simulator/unity_physx.py')
    assert case['firstDifference'] is None and case['stateBytesCompared']==case['stateBytesExact']
    for name,digest in case['evidence'].items():
        assert v.digest(ROOT/name)==digest,name
wall=next(r for r in report['cases'] if r['label']=='additional12000')
assert wall['actorMembershipBoundariesCompared']==4001
assert wall['nativeMembershipFromActualDisableSimulationFlags']
assert wall['preCallbackSolverExitBothActorsByteExact'] and wall['wallCallbackPoseAndZeroVelocitiesExact']
assert wall['nativeWallContactTicks']==[1879] and wall['lastEnabled']==[False,True]
assert v.digest(ROOT/'local_simulator/runtime/pyphysx/_pyphysx.cp39-win_amd64.pyd')==\
    '7c31ced1773023e552391645e42040c9f3694d513805bc8b95ef0f8bc737bd38'
log=BASE/'wall_full_tests_20261003.log'
text=log.read_text(encoding='utf8')
assert 'Ran 44 tests' in text and '\nOK' in text
files=[work/'report.json',work/'additional12000_comparison.json',
    ROOT/'local_simulator/native_wall_contact.py',ROOT/'local_simulator/assets/unity_wall_colliders.json',
    ROOT/'local_simulator/tests/test_unity_wall_collision.py',
    ROOT/'local_simulator/tests/fixtures/unity_wall_collision_12000_20261003.json',
    BASE/'wall_native_abi_verified_20261003.json',BASE/'pcm_functions_20261001/f73733.wat',
    BASE/'unity_data_20261002.unity3d',log,Path(__file__)]
proof=dict(fullTrajectoryRuns=10,completedSteps=37000,comparedStateBytes=3738696,
    allComparedBytesExact=True,firstDifference=None,wallRemovalStep=1879,
    actualNativeSimulationFlagsMatchUnityActorSets=True,testCount=44,allTestsPassed=True,
    nativeBindingOnDiskUnchanged=True,evidence={str(p.relative_to(ROOT)):v.digest(p) for p in files})
(BASE/'wall_repair_verified_20261003.json').write_text(json.dumps(proof,indent=2))
print('PASS 10 complete trajectories, 37000 steps, 3738696 exact state bytes, 44 tests')
