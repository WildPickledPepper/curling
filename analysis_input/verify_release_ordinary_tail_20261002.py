"""Compare matching completed-step boundaries, including the sleep transition."""
import hashlib
import json
from pathlib import Path

from compare_release_states_20261002 import compare
from verify_first_release_chain_20261002 import pose_first
from verify_pcm_internal_trace import events, rows_of
from verify_reset_internal_alignment_20261002 import validate, code_bodies, words

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'analysis_input'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def core_states(row):
    main = [c for c in row['cores'] if c['corePtr'] == row['mainCorePtr']]
    target = [c for c in row['cores'] if c['corePtr'] != row['mainCorePtr']]
    assert len(main) == len(target) == 1
    assert row['bits'] == main[0]['bits']
    return [pose_first(main[0]['bits']), pose_first(target[0]['bits'])]


def target_bits(state):
    q = state['quaternionWxyz']
    return words(state['physxPosition'] + q[1:] + q[:1]
                 + state['physxLinearVelocity'] + state['physxAngularVelocity'])


def main():
    directory = BASE / 'unity_release_tail_fixed_boundaries_20261002'
    rows, event_path, checks = validate(directory)
    native_path = BASE / 'native_release_ordinary_tail_1800_20261002.json'
    native = json.loads(native_path.read_text())
    assert native['baselineOutputsUnchanged']
    assert native['unityPhysxSha256'] == digest(ROOT / 'local_simulator/unity_physx.py')
    traced = json.loads((BASE / 'native_release_ordinary_tail_256_20261002.json').read_text())
    for a, b in zip(native['tail'], traced['tail']):
        assert a['afterBits'] == b['afterBits']
        assert a['targetAfterBits'] == b['targetAfterBits']

    manifest = json.loads((directory / 'capture_manifest.json').read_text())
    original_path = BASE / 'unity_20260930.wasm'
    original = code_bodies(original_path)
    patched_path = Path(manifest['patched'])
    patched = code_bodies(patched_path)
    imports = manifest['importedFunctions']
    for r in manifest['functions']:
        assert original[r['functionIndex'] - imports] == patched[r['rawFunctionIndex'] - imports]
    assert digest(original_path) == manifest['sourceSha256']
    assert digest(patched_path) == manifest['patchedSha256']
    baseline_rows, _ = events(BASE / 'unity_release_526_chain_capture_20261002')
    strip = lambda r: {k: v for k, v in r.items() if k not in ('nativePtr', 'bridgePtr', 'tickSerial')}
    for kind in ('a12.dense_pre_angular_setter', 'a12.dense_post_angular_setter'):
        assert [strip(r) for r in rows_of(rows, kind)] == [strip(r) for r in rows_of(baseline_rows, kind)]
    prefix = compare(native_path, directory)
    assert prefix['continuousPostReleaseStateTicksExact'] == 1561
    assert prefix['nextConfirmedDivergence'] is None

    tails = rows_of(rows, 'a12.tail_phase_core')
    solver_enters = [r for r in tails if r['phase'] == 'PxsDynamics.solverSetupSolve' and r['edge'] == 'enter']
    assert [r['solverSerial'] for r in solver_enters] == list(range(1, len(solver_enters) + 1))
    boundaries = {}
    for row in tails:
        if row['phase'] != 'DCP.FixedUpdate.boundary' or row['edge'] != 'enter' or row['solverSerial'] < 1:
            continue
        tick = 1560 + row['solverSerial']
        states = core_states(row)
        if tick in boundaries:
            assert boundaries[tick] == states, ('inconsistent boundary', tick)
        boundaries[tick] = states
    assert boundaries
    last_tick = min(max(boundaries), native['tail'][-1]['physicsTick'])
    differences = []
    main_differences = []
    for tick in range(1561, last_tick + 1):
        assert tick in boundaries, ('missing completed-step boundary', tick)
        if tick <= 1562:
            frame = native['frames'][tick - 1]
            expected = [frame['afterBits'], target_bits(frame['step']['targetsAfterScene']['2'])]
        else:
            frame = native['tail'][tick - 1563]
            expected = [frame['afterBits'], frame['targetAfterBits']]
        diff = [dict(stoneIndex=(0, 2)[k], wordIndex=j,
                     unity=hex(a), native=hex(b))
                for k in range(2) for j, (a, b) in enumerate(zip(boundaries[tick][k], expected[k])) if a != b]
        if diff:
            differences.append(dict(physicsTick=tick, differences=diff))
        if any(d['stoneIndex'] == 0 for d in diff):
            main_differences.append(dict(physicsTick=tick, differences=[d for d in diff if d['stoneIndex'] == 0]))
    assert not main_differences
    assert [d['physicsTick'] for d in differences] == [1561, 1562]

    wake_path = BASE / 'native_release_target_wake_calls_20261002.json'
    wake = json.loads(wake_path.read_text())
    assert wake['baselineOutputsUnchanged']
    assert [r['physicsTick'] for r in wake['targetWakeCalls']] == [1561, 1562]
    first_wake = wake['targetWakeCalls'][0]
    assert first_wake['sleepingBefore'] and not first_wake['sleepingAfter']
    assert first_wake['beforeBits'] == first_wake['afterBits'] == boundaries[1561][1]
    first_solver = next(r for r in tails if r['solverSerial'] == 1
                        and r['phase'] == 'PxsDynamics.solverSetupSolve' and r['edge'] == 'enter')
    assert core_states(first_solver)[1] == first_wake['beforeBits']
    assert wake['native'][1560]['targetAfterNativeBits'] != core_states(first_solver)[1]

    # A solver-exit observation precedes fetchResults/sleep finalization. It
    # must not be substituted for the completed-step state when no awake actor
    # invokes the subsequent Unity pose-normalization writer.
    sleep_tick = next(r['physicsTick'] for r in native['tail'] if all(r['sleeping']))
    sleep_solver = next(r for r in tails if r['solverSerial'] == sleep_tick - 1560
                        and r['phase'] == 'PxsDynamics.solverSetupSolve' and r['edge'] == 'exit')
    before_finalization = core_states(sleep_solver)
    sleeping = native['tail'][sleep_tick - 1563]
    assert before_finalization[1] != sleeping['targetAfterBits']
    assert boundaries[sleep_tick][1] == sleeping['targetAfterBits']

    report = dict(sampleId=11000, unityWasmSha256=digest(original_path),
                  nativeModuleSha256=native['moduleSha256'], productionCodeSha256=native['unityPhysxSha256'],
                  observer=dict(checks, densePairsUnchanged=1563, originalFunctionBodiesRetained=True,
                                nativeOutputsUnchanged=True, tracedFirst256TailOutputsUnchanged=True),
                  mainPrefixTicksExact=1561, completedBoundaryFirstTick=1561,
                  completedBoundaryLastTick=last_tick, mainContinuousStateTicksExact=last_tick,
                  mainContinuousStateWordsExact=last_tick * 13,
                  firstObservedTargetStateDifference=next(iter(differences), None),
                  observedTargetDifferenceTicks=[d['physicsTick'] for d in differences],
                  bothStonePhysicsOnlyTailTicksExact=last_tick - 1562,
                  bothStonePhysicsOnlyTailWordsExact=(last_tick - 1562) * 26,
                  targetWakeCalls=wake['targetWakeCalls'],
                  targetWakeCause='step_custom_sliding uses _reaches_pcm_shell_this_tick and explicitly calls target.body.wake_up before tick 1561; Unity sampled target core does not advance in that tick',
                  firstStoneContactTick=next(f['ordinal'] - 1 for f in native['frames'] if f['step']['stoneReports']),
                  mainNativeSleepTick=next(r['physicsTick'] for r in native['tail'] if r['sleeping'][0]),
                  targetNativeSleepTick=sleep_tick,
                  sleepTransition=dict(physicsTick=sleep_tick, unitySolverExitTargetBits=before_finalization[1],
                                       unityCompletedTargetBits=boundaries.get(sleep_tick, [None, None])[1],
                                       nativeCompletedTargetBits=sleeping['targetAfterBits']),
                  scope='sample 11000; Windows CP39; fresh Reset and actual BESTSHOT; recorded friction inputs; matching completed-step P/Q/v/w boundaries',
                  limitations=['Does not prove that every intermediate calculation or internal RNG state is identical.',
                               'The entire precontact target trajectory is not independently sampled in this report.',
                               'Protocol coordinate conversion/formatting and game-state transition internals remain separate checks.'],
                  evidence={str(p.relative_to(ROOT)): digest(p) for p in [event_path, native_path,
                      directory / 'capture_manifest.json', directory / 'observer_source.js',
                      wake_path, BASE / 'pcm_functions_20261001/f61107.wat', BASE / 'pcm_functions_20261001/f61030.wat']})
    out = BASE / 'release_ordinary_tail_verified_20261002.json'
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf8')
    print(json.dumps({k: report[k] for k in ('completedBoundaryLastTick', 'firstObservedTargetStateDifference',
                                           'firstStoneContactTick', 'mainNativeSleepTick', 'targetNativeSleepTick')}, indent=2))


if __name__ == '__main__':
    main()
