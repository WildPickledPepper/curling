"""Fail on any getter/setter gap; state the remaining scene boundary honestly."""
import hashlib
import json
import struct
from pathlib import Path

from verify_pcm_internal_trace import events, rows_of, geometry_points

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bits(values):
    return list(struct.unpack('<' + str(len(values)) + 'I',
                              struct.pack('<' + str(len(values)) + 'f', *values)))


def samples(folder):
    fields = ('sample_id', 'after_position', 'final_xy', 'target_moves', 'requested', 'collision_observed')
    return [{k:r[k] for k in fields} for r in
            (json.loads(s) for s in next(folder.glob('collision*.jsonl')).read_text().splitlines())]


def unchanged(captured, directory, baseline, baseline_directory):
    assert not [r for r in captured if 'failed' in r['type']]
    assert rows_of(captured, 'sliding.random_range.friction') == rows_of(baseline, 'sliding.random_range.friction')
    for kind in ('a12.dense_pre_angular_setter', 'a12.dense_post_angular_setter'):
        def stable(row):
            return {k:v for k,v in row.items() if k not in
                    ('nativePtr','bridgePtr','tickSerial','bridge164Bits','bridge300Bits')}
        actual, expected = rows_of(captured, kind), rows_of(baseline, kind)
        assert len(actual) == len(expected) == 1023
        assert list(map(stable, actual)) == list(map(stable, expected))
    def core(row):
        return {k:v for k,v in row['decodedCandidate'].items() if k != 'ptr'}
    actual, expected = rows_of(captured, 'c04.dynamic_solver_frame'), rows_of(baseline, 'c04.dynamic_solver_frame')
    assert len(actual) == len(expected) == 40
    for a,b in zip(actual, expected):
        for edge in ('entryCores','exitCores'):
            assert list(map(core,a[edge])) == list(map(core,b[edge]))
    assert samples(directory) == samples(baseline_directory)


def main():
    directory = ROOT/'analysis_input/unity_11005_getter_setter_bits_20261002'
    captured, event_path = events(directory)
    base_dir = ROOT/'analysis_input/unity_11005_step486_pcm_20261001'
    baseline, _ = events(base_dir)
    unchanged(captured, directory, baseline, base_dir)
    mass_dir = ROOT/'analysis_input/unity_11005_mass_properties_v2_20261002'
    mass_capture, mass_event_path = events(mass_dir)
    unchanged(mass_capture, mass_dir, baseline, base_dir)
    report_path = ROOT/'analysis_input/c131_getter_gap_closed_20261002.json'
    report = json.loads(report_path.read_text())
    active = next(r for r in report['releaseBoundary'] if r['sampleId'] == 11005)
    pre, post = (rows_of(captured, kind) for kind in
                 ('a12.dense_pre_angular_setter','a12.dense_post_angular_setter'))
    assert len(pre) == len(post) == len(active['setters']) == 1023
    for ordinal,(u,v,l) in enumerate(zip(pre,post,active['setters']), 1):
        assert u['ordinal'] == v['ordinal'] == ordinal
        assert bits(u['pose']['p']) == bits(l['rawBefore']['physxPosition']), ('P',ordinal)
        assert bits(u['pose']['q']) == bits(l['rawQuaternion']), ('Q',ordinal)
        assert v['bridge164Bits'] == v['bridge300Bits'] == bits(l['result']), ('angular setter',ordinal)
    getters = rows_of(captured, 'a12.velocity_getter_native')
    counts = {}
    for kind,field,count,slot in [('velocity','physxLinearVelocity',2044,121727),
                                  ('angularVelocity','physxAngularVelocity',1022,121729)]:
        selected = [r for r in getters if r['kind'] == kind]
        assert len(selected) == count
        for g in selected:
            assert g['bridgeGetterTableIndex'] == slot
            assert g['coreBeforeBits'] == g['bufferBeforeBits'] == g['outputBits'] == g['coreAfterBits'] == g['bufferAfterBits']
            expected = active['ticks'][g['ordinal']-2]['input'][field]
            assert g['outputBits'] == bits(expected), (kind, g['ordinal'], g['outputBits'], bits(expected))
        counts[kind] = count
    # The numerical solver input and deltas at the original fork also close.
    native_path = ROOT/'analysis_input/native_getter_mass_fixed_465_20261002/calls.json'
    native = json.loads(native_path.read_text())
    assert native['callStackReliable'] and not native['dropped'] and not native['unfinished']
    assert len(native['calls']) == 1 and native['calls'][0]['functionRva'] == '0x2049c7'
    sample = native['calls'][0]
    unity = next(r for r in rows_of(mass_capture,'a12.static_writeback') if r['ordinal'] == 465)
    u = bytes(unity['before']['solverBodyData'][0]['bodyA']['rawBytes'])
    n = bytes(sample['bodyDataBytes'])
    # Offset 72 is the roster index (Unity 15/local 14), not a physical value.
    assert u[:72] == n[:72] and u[76:] == n[76:]
    assert bytes(sample['motionBodyBytes']) == bytes(unity['after']['descs'][0]['bodyAWindow']['rawBytes'][:32])
    # Preserve the uncovered scene fork rather than treating one body's prefix
    # as proof that the entire scene is aligned.
    manager = rows_of(captured,'c03.first_dynamic_writeback')[0]['manager']
    target_truth = manager['coresBeforeSolve'][1]['decodedCandidate']['q']
    frame = active['postDenseFrames'][0]
    local_pair = next(r for r in frame['narrowphase'] if not r['after'] and r['geom_type0'] == r['geom_type1'] == 4)
    target_local = local_pair['transform1']['q']
    assert bits(target_truth) != bits(target_local)
    source_files = [ROOT/'local_simulator/unity_physx.py',
                    ROOT/'local_simulator/runtime_support/tools/reverse/recovered_stone_mass.py',
                    ROOT/'research_archive/unity_reverse/source/reverse/unity_webgl_runtime_probe.js']
    result = {'sampleId':11005, 'closedAngularGetterOrdinals':[466,482],
              'closedSignedZeroLinearGetterOrdinal':2,
              'verifiedActiveBody':{'poseAndAngularSetterOrdinals':[1,1023],
                                   'getterOrdinals':[2,1023], 'getterCounts':counts,
                                   'comparison':'raw IEEE754 binary32 bits, including signed zeros'},
              'solverInputAndDeltaExactOrdinal':465,
              'massRebuildCallsExact':98, 'massRebuildReleaseCount':12,
              'observerPreservesFrictionSettersDynamicCoreFramesAndEndpoints':True,
              'remainingSceneDifference':{'location':'target body pose before first stone-pair PCM',
                  'firstObservedOrdinal':1023, 'unityQuaternionBits':bits(target_truth),
                  'localQuaternionBits':bits(target_local), 'earliestOccurrenceKnown':False,
                  'nextRequiredTrace':'Target activation/reset settling, followed through native P/Q/v/w and sleep boundaries.'},
              'fullSceneAlignedThrough1023':False,
              'replayConditions':'Recorded initial/reset rotations and friction; no post-release state injection.',
              'sourceSha256':{str(p.relative_to(ROOT)):sha(p) for p in source_files},
              'evidenceSha256':{str(p.relative_to(ROOT)):sha(p) for p in
                               (report_path,event_path,mass_event_path,native_path)}}
    output = ROOT/'analysis_input/11005_angular_gap_verified_20261002.json'
    output.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k in
                     ('closedAngularGetterOrdinals','closedSignedZeroLinearGetterOrdinal','verifiedActiveBody','fullSceneAlignedThrough1023')}))


if __name__ == '__main__':
    main()
