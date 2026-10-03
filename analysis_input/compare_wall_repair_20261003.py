"""Compare every live actor's raw state and actor membership through cleanup."""
import hashlib
import json
from pathlib import Path
import struct

import validate_multiple_cases_20261002 as v

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'analysis_input'


def compare(capture, native_path, label):
    path = v.event_path(capture)
    native = json.loads(native_path.read_text())
    assert native['sourceSha256'] == v.digest(ROOT/'local_simulator/unity_physx.py')
    assert native['unityEventsSha256'] == v.digest(path)
    tail = list(v.rows(path, 'a12.tail_phase_core'))
    boundaries = [r for r in tail if r['phase'] == 'DCP.FixedUpdate.boundary' and r['edge'] == 'enter']
    assert [r['solverSerial'] for r in boundaries] == list(range(len(native['states'])+1))
    main = boundaries[0]['mainCorePtr']
    cores = [main] + [c['corePtr'] for c in boundaries[0]['cores'] if c['corePtr'] != main]
    assert len(cores) == len(native['stoneIndices']) == 2
    exact = total = 0
    first = None
    for row in boundaries:
        tick = row['solverSerial']
        mapping = {c['corePtr']: c for c in row['cores']}
        enabled = native['releaseSimulating'] if tick == 0 else native['simulating'][tick-1]
        assert enabled == (native['releaseEnabled'] if tick == 0 else native['enabled'][tick-1])
        expected_cores = {c for c, alive in zip(cores, enabled) if alive}
        if set(mapping) != expected_cores and first is None:
            first = dict(physicsTick=tick, kind='live_actor_membership',
                unity=sorted(mapping), native=sorted(expected_cores))
        states = native['releaseBits'] if tick == 0 else native['states'][tick-1]
        for index, core in enumerate(cores):
            if core not in mapping or not enabled[index]:
                continue
            unity = v.pose_first(mapping[core]['bits'])
            a, b = (struct.pack('<13I', *words) for words in (unity, states[index]))
            exact += sum(x == y for x, y in zip(a, b))
            total += len(a)
            if a != b and first is None:
                word = next(i for i, (x, y) in enumerate(zip(unity, states[index])) if x != y)
                first = dict(physicsTick=tick, kind='raw_state', stoneIndex=native['stoneIndices'][index],
                    field=v.FIELDS[word], unityBits=hex(unity[word]), nativeBits=hex(states[index][word]))
    report = dict(label=label, firstDifference=first, completedStepsCompared=len(boundaries)-1,
        stateBytesCompared=total, stateBytesExact=exact, actorMembershipBoundariesCompared=len(boundaries),
        nativeMembershipFromActualDisableSimulationFlags=True,
        nativeWallContactTicks=[r['physicsTick'] for r in native['wallContacts']],
        lastEnabled=native['enabled'][-1], fullTrajectoryExact=first is None and total == exact,
        nativeBothSleepingAtLastComparedStep=all(native['sleeping'][-1]),
        productionSourceSha256=native['sourceSha256'], nativeModuleSha256=native['moduleSha256'],
        evidence={str(p.relative_to(ROOT)): v.digest(p) for p in (path, native_path)})
    if label.endswith('12000'):
        assert len(native['wallContacts']) == 1 and native['wallContacts'][0]['physicsTick'] == 1879
        r = native['wallContacts'][0]['reports']
        assert len(r) == 1 and r[0]['wall'] == 'bound1' and r[0]['stoneIndex'] == 0
        assert all(native['enabled'][t-1] == [True, True] for t in range(1, 1879))
        assert all(native['enabled'][t-1] == [False, True] for t in range(1879, 4001))
        solver = next(r for r in tail if r['solverSerial'] == 1879 and
            r['phase'] == 'PxsDynamics.solverSetupSolve' and r['edge'] == 'exit')
        by_core = {c['corePtr']: c for c in solver['cores']}
        solver_bits = [v.pose_first(by_core[c]['bits']) for c in cores]
        if native.get('nativePhases'):
            phase = next(r for r in native['nativePhases'] if r['physicsTick'] == 1879)
            assert phase['afterNativeBits'] == solver_bits
            report['preCallbackSolverExitBothActorsByteExact'] = True
        # The actual callback's f72606 argument was sampled separately. Check
        # retained P/Q against that sample; absent core states are never zeros.
        callback = json.loads((BASE/'case12000_callback_pose_20261003.json').read_text())
        assert native['states'][1878][0][:7] == callback['poseWords']
        assert native['states'][1878][0][7:] == [0]*6
        assert all(native['states'][t-1][0] == native['states'][1878][0] for t in range(1879, 4001))
        report['wallCallbackPoseAndZeroVelocitiesExact'] = True
        report['nativeWallContact'] = r[0]
    return report


if __name__ == '__main__':
    r = compare(BASE/'additional_case_validation_20261002/additional12000_unity',
        BASE/'wall_repair_regression_20261003/additional12000_native.json', 'wall_fixed_12000')
    (BASE/'case12000_wall_fixed_comparison_20261003.json').write_text(json.dumps(r, indent=2))
    print(json.dumps(r, indent=2))
