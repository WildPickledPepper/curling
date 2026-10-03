"""Actual island activation call chain and complete two-stone state replay."""
import hashlib
import json
from pathlib import Path
from compare_release_states_20261002 import compare
from verify_pcm_internal_trace import events, rows_of
from verify_reset_internal_alignment_20261002 import validate, code_bodies
from verify_release_ordinary_tail_20261002 import core_states, target_bits

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'analysis_input'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    directory = BASE / 'unity_release_both_complete_activation_v2_20261002'
    rows, event_path, checks = validate(directory)
    manifest = json.loads((directory / 'capture_manifest.json').read_text())
    original_path = BASE / 'unity_20260930.wasm'
    patched_path = Path(manifest['patched'])
    original, patched = code_bodies(original_path), code_bodies(patched_path)
    imports = manifest['importedFunctions']
    for entry in manifest['functions']:
        assert original[entry['functionIndex'] - imports] == patched[entry['rawFunctionIndex'] - imports]
    assert digest(original_path) == manifest['sourceSha256']
    assert digest(patched_path) == manifest['patchedSha256']
    baseline_rows, _ = events(BASE / 'unity_release_526_chain_capture_20261002')
    strip = lambda r: {k: v for k, v in r.items() if k not in ('nativePtr', 'bridgePtr', 'tickSerial')}
    for kind in ('a12.dense_pre_angular_setter', 'a12.dense_post_angular_setter'):
        assert [strip(r) for r in rows_of(rows, kind)] == [strip(r) for r in rows_of(baseline_rows, kind)]

    native_path = BASE / 'native_release_natural_target_wake_20261002.json'
    plain_path = BASE / 'native_natural_wake_unobserved_20261002.json'
    native, plain = json.loads(native_path.read_text()), json.loads(plain_path.read_text())
    source_path = ROOT / 'local_simulator/unity_physx.py'
    assert native['unityPhysxSha256'] == plain['sourceSha256'] == digest(source_path)
    assert native['moduleSha256'] == plain['moduleSha256']
    assert native['targetWakeCalls'] == []
    expected = [[f['afterBits'], target_bits(f['step']['targetsAfterScene']['2'])] for f in native['frames']]
    expected += [[f['afterBits'], f['targetAfterBits']] for f in native['tail']]
    assert expected == plain['states']
    assert native['releaseBits'] == plain['releaseBits']
    old = json.loads((BASE / 'native_first_release_bvh34_full_20261002.json').read_text())
    assert native['releaseBits'] == old['releaseBits']
    assert [f['afterBits'] for f in native['frames']] == [f['afterBits'] for f in old['frames']]
    prefix = compare(native_path, directory)
    assert prefix['continuousPostReleaseStateTicksExact'] == 1561 and prefix['nextConfirmedDivergence'] is None

    tails = rows_of(rows, 'a12.tail_phase_core')
    first_solver = next(r for r in tails if r['phase'] == 'PxsDynamics.solverSetupSolve' and r['edge'] == 'enter')
    assert first_solver['solverSerial'] == 1 and first_solver['ordinal'] == 2
    boundaries = {}
    for row in tails:
        if row['phase'] != 'DCP.FixedUpdate.boundary' or row['edge'] != 'enter' or row['solverSerial'] < 1:
            continue
        tick, states = row['solverSerial'], core_states(row)
        if tick in boundaries:
            assert boundaries[tick] == states
        boundaries[tick] = states
    last_tick = min(max(boundaries), len(expected))
    assert last_tick >= 1920
    first_difference = None
    for tick in range(1, last_tick + 1):
        assert tick in boundaries, ('missing completed boundary', tick)
        differences = [dict(stoneIndex=(0, 2)[k], wordIndex=j, unity=hex(a), native=hex(b))
                       for k in range(2) for j, (a, b) in enumerate(zip(boundaries[tick][k], expected[tick - 1][k])) if a != b]
        if differences:
            first_difference = dict(physicsTick=tick, differences=differences)
            break
    assert first_difference is None, first_difference

    main_ptr = first_solver['mainCorePtr']
    target_ptr = next(c['corePtr'] for c in first_solver['cores'] if c['corePtr'] != main_ptr)
    calls = [r for r in rows_of(rows, 'a12.pcm_internal_call') if r.get('stoneActivationBefore')]
    target_sim = next(c['rigidSimPtr'] for c in first_solver['cores'] if c['corePtr'] == target_ptr)
    target_call = next(r for r in calls if r['functionIndex'] == 71557 and r['args'] == [target_sim, 1])
    registration = next(r for r in calls if r['functionIndex'] == 71379 and r['args'][1] == target_sim)
    activation = next(r for r in calls if r['functionIndex'] == 71555 and r['args'][0] == target_sim)
    by_id = {r['callId']: r for r in calls}
    parent = by_id[target_call['parentCallId']]
    assert parent['functionIndex'] == 71529
    assert registration['parentCallId'] == activation['parentCallId'] == target_call['callId']
    assert target_call['ordinal'] == 1563 and target_call['tailSolverSerial'] == 1561
    field = lambda r, side, group, offset: next(x for x in r['stoneActivation' + side] if x['corePtr'] == target_ptr)[group + 'Words'][next(x for x in r['stoneActivation' + side] if x['corePtr'] == target_ptr)[group + 'Offsets'].index(offset)]
    assert field(target_call, 'Before', 'sim', 156) == 0xfffffffe
    assert field(target_call, 'After', 'sim', 156) == 2
    assert field(target_call, 'Before', 'core', 156) == field(target_call, 'After', 'core', 156) == 0
    assert not [r for r in calls if r['functionIndex'] in (71572, 71573) and r['args'][0] == target_sim]

    main_sleep = next(r['physicsTick'] for r in native['tail'] if r['sleeping'][0])
    target_sleep = next(r['physicsTick'] for r in native['tail'] if r['sleeping'][1])
    assert all(v == 0 for k in range(2) for v in boundaries[target_sleep][k][7:])
    evidence_paths = [event_path, native_path, plain_path, source_path, directory / 'capture_manifest.json',
                      directory / 'observer_source.js', ROOT / 'local_simulator/tests/fixtures/unity_target_activation_20261002.json']
    evidence_paths += [BASE / ('pcm_functions_20261001/f%d.wat' % i) for i in (71529, 71557, 71379, 71555, 71572, 71618)]
    report = dict(sampleId=11000, unityWasmSha256=digest(original_path), patchedWasmSha256=digest(patched_path),
                  nativeModuleSha256=native['moduleSha256'], productionCodeSha256=digest(source_path),
                  repair='Default target activation is owned by the PhysX island manager; remove forecast wake_up from both Python replay paths; old bulk loop restricted to explicit manual-wake diagnostic.',
                  actualTargetActivation=dict(physicsTick=1562, denseOrdinal=1563,
                      callChainFunctionIndices=[71529, 71557, 71379, 71555],
                      callIds=[parent['callId'], target_call['callId'], registration['callId'], activation['callId']],
                      activeArrayIndexBefore='0xfffffffe', activeArrayIndexAfter=2,
                      wakeCounterBitsBefore=0, wakeCounterBitsAfter=0, explicitTargetWakeUpCallsObserved=0),
                  observer=dict(checks, originalFunctionBodiesRetained=True, densePairsUnchanged=1563,
                                nativeWrappedAndPlainProductionStatesExact=3362),
                  continuousBothStoneCompletedStateTicksExact=last_tick,
                  continuousBothStoneCompletedStateWordsExact=last_tick * 26,
                  firstConfirmedCompletedStateDivergence=first_difference,
                  mainNativeSleepTick=main_sleep, targetNativeSleepTick=target_sleep,
                  tests='32 existing tests and 2 actual Unity target-activation regressions passed',
                  scope='sample 11000; Windows CP39; fresh Reset; actual BESTSHOT; same recorded friction inputs; two active stones completed-step P/Q/v/w from release through final rest',
                  limitations=['Every arithmetic intermediate and internal RNG state are not audited by boundary equality.',
                               'Protocol conversion/formatting and game-state transition internals are not yet compared.',
                               'Other samples, ABIs and the explicit manual-wake diagnostic mode are separate verification scopes.'],
                  evidence={str(p.relative_to(ROOT)): digest(p) for p in evidence_paths})
    (BASE / 'target_natural_wake_verified_20261002.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf8')
    print('PASS: actual island activation at tick 1562; both stones exact for %d completed steps (%d words), through final rest.' % (last_tick, last_tick * 26))


if __name__ == '__main__':
    main()
