"""Verify the read-only activation trace and retain exact runtime evidence."""
import hashlib
import json
import struct
from pathlib import Path

from verify_pcm_internal_trace import events, rows_of

ROOT = Path(__file__).resolve().parents[1]


def main():
    directory = ROOT / 'analysis_input/unity_reset_lifecycle_first_case_20261002'
    captured, path = events(directory)
    baseline_dir = ROOT / 'analysis_input/unity_scene_chain_from_start_20261002'
    baseline, baseline_path = events(baseline_dir)
    assert not [r for r in captured if 'failed' in r['type']]
    friction = rows_of(captured, 'sliding.random_range.friction')
    assert len(friction) == 1562
    assert friction == rows_of(baseline, 'sliding.random_range.friction')[:1562]
    sample = json.loads(next(directory.glob('*.jsonl')).read_text().splitlines()[0])
    reference = json.loads(next(baseline_dir.glob('*.jsonl')).read_text().splitlines()[0])
    for key in ('sample_id', 'after_position', 'final_xy', 'target_moves', 'requested', 'collision_observed'):
        assert sample[key] == reference[key], key
    calls = rows_of(captured, 'a12.pcm_internal_call')
    by_id = {r['callId']: r for r in calls}
    constructors = sorted((r for r in calls if r['functionIndex'] == 71726), key=lambda r:r['callId'])
    assert len(constructors) == 28
    activations = []
    offsets = list(range(16,44,4)) + list(range(48,160,4))
    for constructor in constructors[26:]:
        parent = by_id[constructor['parentCallId']]
        assert parent['functionIndex'] == 73018 and parent['args'][1] == 1
        assert parent['rigidbodyActorBefore'] != parent['rigidbodyActorAfter']
        assert constructor['args'][2] == parent['rigidbodyActorAfter'] + 64
        component = bytes.fromhex(next(b['hex'] for b in parent['before'] if b['argument'] == 0))
        core = bytes.fromhex(next(b['hex'] for b in constructor['before'] if b['argument'] == 2))
        activations.append({
            'componentPtr':parent['args'][0], 'creationCallId':parent['callId'],
            'constructorCallId':constructor['callId'], 'releaseSerial':constructor.get('releaseSerial'),
            'actorBefore':parent['rigidbodyActorBefore'], 'actorAfter':parent['rigidbodyActorAfter'],
            'componentConstraints':struct.unpack_from('<I',component,136)[0],
            'componentInertiaTensorBits':list(struct.unpack_from('<3I',component,104)),
            'coreOffsets':offsets, 'coreBits':[struct.unpack_from('<I',core,o)[0] for o in offsets],
        })
    assert [r['componentConstraints'] for r in activations] == [80,0]
    result = {
        'sampleId':11000, 'runtimeFactoryFunction':73018,
        'observedActorReplacementAtBothActivationCalls':True,
        'observerVerification':{'frictionWordsExact':1562,'endpointFieldsUnchanged':True},
        'activations':activations,
        'completeScenePrefixAligned':False,
        'remaining':'Native actor replacement, managed component lifecycle, Transform/mass synchronization and reset integration/sleep must be closed.',
        'evidenceSha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (path,baseline_path)},
    }
    (ROOT/'analysis_input/reset_lifecycle_observed_20261002.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('Factory/registration: two actual actor replacements; 1562 friction records and endpoint fields unchanged.')


if __name__ == '__main__':
    main()
