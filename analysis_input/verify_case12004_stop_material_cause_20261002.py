"""Direct evidence and causal replay for sample 12004's first divergence."""
import hashlib
import json
from pathlib import Path
import struct

from validate_multiple_cases_20261002 import rows, event_path, observer_check, compare
from verify_first_release_chain_20261002 import pose_first
from verify_pcm_internal_trace import raw_argument

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'analysis_input/multi_case_validation_20261002'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def words(values):
    return list(struct.unpack('<%dI'%len(values),struct.pack('<%df'%len(values),*values)))


def check_capture(cap, baseline, native):
    path = event_path(cap)
    manifest = json.loads((cap/'capture_manifest.json').read_text())
    control = BASE/'full12004_run1_original_control'
    result = observer_check(cap,control,manifest,native)
    assert not list(rows(path,'rng.friction_manifest_exhausted'))
    assert len(list(rows(path,'sliding.random_range.friction')))==3168
    # Compare every captured completed tail state, both bodies, against the
    # earlier full capture. Relative serial 1 is completed physics step 3167.
    expected = {r['solverSerial']: [pose_first(c['bits']) for c in r['cores']]
                for r in rows(baseline,'a12.tail_phase_core')
                if r['phase']=='DCP.FixedUpdate.boundary' and r['edge']=='enter'}
    actual = [r for r in rows(path,'a12.tail_phase_core')
              if r['phase']=='DCP.FixedUpdate.boundary' and r['edge']=='enter']
    assert [r['solverSerial'] for r in actual]==[1,2,3,4,5]
    for r in actual:
        assert [pose_first(c['bits']) for c in r['cores']]==expected[3166+r['solverSerial']]
    reset = lambda p: [(r['step'],r['phase'],r['edge'],[c['bits'] for c in r['cores']])
                       for r in rows(p,'scene.reset_body_cores')]
    assert reset(path)==reset(baseline) and len(reset(path))==256
    result.update(resetSnapshotsUnchanged=256,completedBothStoneTailStatesUnchanged=5)
    return result


def main():
    old_path = BASE/'full12004_run1_native.json'
    baseline = event_path(BASE/'full12004_run1_unity')
    cap = BASE/'case12004_stop_material_unity'
    event = event_path(cap)
    capture_checks = {name:check_capture(BASE/name,baseline,old_path)
                      for name in ('case12004_stop_internal_unity','case12004_stop_material_unity')}
    old = json.loads(old_path.read_text())
    traced_path = BASE/'case12004_step3169_native_calls/alignment.json'
    traced = json.loads(traced_path.read_text())
    assert traced['states']==old['states'][:len(traced['states'])]
    assert traced['releaseBits']==old['releaseBits']
    calls_path = traced_path.with_name('calls.json')
    native_calls = json.loads(calls_path.read_text())
    assert native_calls['callStackReliable'] and not native_calls['unfinished'] and not native_calls['dropped']

    solver_serial = 0
    writes, solves = [], []
    for line_number,line in enumerate(event.open(encoding='utf8'),1):
        row = json.loads(line)
        d = row['data']
        if row['type']=='a12.tail_phase_core' and d['phase']=='PxsDynamics.solverSetupSolve' and d['edge']=='enter':
            solver_serial = d['solverSerial']
        if row['type']=='a12.pcm_internal_call' and d['functionIndex'] in (32511,32512):
            assert solver_serial==2 and d['ordinal']==3169
            assert d['args'][1]==0.6000000238418579
            writes.append(dict(line=line_number,afterCompletedStep=3168,beforeCompletedStep=3169,
                               functionIndex=d['functionIndex'],tableIndex=d['tableIndex'],
                               value=d['args'][1],valueBits=f'0x{words([d["args"][1]])[0]:08x}'))
        if row['type']=='a12.static_solve' and solver_serial==3:
            solves.append(d)
    assert [r['functionIndex'] for r in writes]==[32511,32512]
    assert len(solves)==5

    # PCM output was observed in the preceding narrowphase, before solve serial3.
    pcm = list(rows(event,'a12.pcm_convex_mesh'))[2]
    assert pcm['before']['cache']['cachedSize']==pcm['after']['cache']['cachedSize']==0
    local_pcm = next(c for c in native_calls['calls'] if c['functionRva']=='0x2e2880')
    for index,key in ((5,'transform0'),(6,'transform1')):
        assert words(pcm['before'][key]['q']+pcm['before'][key]['p'])==list(
            struct.unpack_from('<7I',raw_argument(local_pcm,index,'before')))
    geometry = pcm['after']['contactBuffer']['contactsPreview']
    assert len(geometry)==5
    raw_contacts = raw_argument(local_pcm,8,'after')
    for i,c in enumerate(geometry):
        assert words(c['normal']+[c['separation']]+c['point'])==list(
            struct.unpack_from('<7I',raw_contacts,i*64))

    phase = next(r for r in traced['nativePhases'] if r['physicsTick']==3169)
    first = phase['solve_block'][0]
    u = bytes(solves[0]['before']['descs'][0]['constraintWindow']['rawBytes'])
    n = bytes(first['constraint_bytes_before'])
    header_difference = [i for i in range(0,56,4) if u[i:i+4]!=n[i:i+4]]
    assert header_difference==[16,20]
    for offset in header_difference:
        assert struct.unpack_from('<I',u,offset)[0]==0x3c449ba6
        assert struct.unpack_from('<I',n,offset)[0]==0
    for i in range(5):
        assert u[64+i*48:112+i*48]==n[80+i*48:128+i*48]
    # Only arithmetic fields are compared; pointer/layout/padding are distinct
    # between the 32-bit WebGL and 64-bit native builds.
    friction_offsets = list(range(0,32,4))+[44,48]
    for i in range(4):
        for off in friction_offsets:
            assert u[336+i*64+off:340+i*64+off]==n[352+i*64+off:356+i*64+off]
    assert bytes(solves[0]['before']['descs'][0]['bodyAWindow']['rawBytes'][:32])==bytes(first['body_a_before']['raw_bytes'])

    verification_path = BASE/'case12004_observed_material_writes_native.json'
    verified = json.loads(verification_path.read_text())
    assert verified['states'][:3168]==old['states'][:3168]
    # These are the archived investigation runs, before the production repair.
    # Their source hashes must match each other, not today's production file.
    assert verified['sourceSha256']==old['sourceSha256']
    assert not verified['stoneContactTicks']
    full_report = json.loads((BASE/'case12004_observed_material_writes_comparison.json').read_text())
    assert full_report['evidence'][str(verification_path.relative_to(ROOT))]==digest(verification_path)
    for r in rows(baseline,'a12.tail_phase_core'):
        if r['phase']!='DCP.FixedUpdate.boundary' or r['edge']!='enter':continue
        expected=[pose_first(c['bits']) for c in r['cores']]
        actual=verified['releaseBits'] if r['solverSerial']==0 else verified['states'][r['solverSerial']-1]
        assert expected==actual
    assert full_report['firstDifference'] is None and full_report['completedStepsCompared']==4000
    corrected_solves = verified['nativePhases'][0]['solve_block']
    for a,b in zip(solves,corrected_solves):
        x=bytes(a['before']['descs'][0]['constraintWindow']['rawBytes'])
        y=bytes(b['constraint_bytes_before'])
        assert x[:56]==y[:56]
        for i in range(5):assert x[64+i*48:112+i*48]==y[80+i*48:128+i*48]
        for i in range(4):
            for off in friction_offsets:assert x[336+i*64+off:340+i*64+off]==y[352+i*64+off:356+i*64+off]
        for edge in ('before','after'):
            assert bytes(a[edge]['descs'][0]['bodyAWindow']['rawBytes'][:32])==bytes(b['body_a_'+edge]['raw_bytes'])

    wat = ROOT/'analysis_input/pcm_functions_20261001/f61097.wat'
    text = wat.read_text()
    assert 'f32.const 0x1.0c6f7ap-20 (;=1e-06;)' in text
    assert 'call $f32511' in text and 'call $f32512' in text
    paths = (event,baseline,old_path,traced_path,calls_path,verification_path,wat,
             ROOT/'analysis_input/replay_case12004_observed_material_writes_20261002.py')
    result = dict(sampleId=12004,earliestConfirmedMissingOperation='Natural-stop material restoration between completed steps3168 and3169',
        staticSourceFunction='DCP.Update / Wasm f61097',
        stopConditionFromOriginalWasm='shot active, displacement > 1.0, float32 velocity squared sum < 1e-6',
        observedRuntimeWrites=writes, firstContactFrictionHeaderDifference=dict(
            physicsTick=3169,unity=[0.012000000104308128]*2,native=[0.0]*2,
            unityBits=['0x3c449ba6']*2,nativeBits=['0x00000000']*2),
        pcmTransformsAndFiveContactsExact=True, fiveNormalRowsExact=True,
        fourFrictionRowsArithmeticFieldsExact=True,initialSolverBodyExact=True,
        productionMissingBranch='Only OnCollisionEnter participant material restoration is emulated; DCP.Update natural-stop restoration is omitted.',
        whyOtherCasesPassed='Other validated conditions had stone-stone collisions, so their existing collision callback restored material friction before the tail.',
        causalVerification=dict(replayObservedMaterialWritesOnly=True,productionSourceUnchanged=True,
            correctedSolverIterationsInputsAndOutputsExact=5,releaseAndCompletedBothStoneStatesExact=4001,
            completedStepsCompared=4000,stateBytesCompared=full_report['stateBytesCompared'],firstDifference=None),
        observerChecks=capture_checks,nativeObservedStatesUnchanged=len(traced['states']),
        scope='Root cause established and verified by a diagnostic driver. Production has not been repaired in this investigation.',
        unityOriginalSha256='cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81',
        productionSourceSha256=old['sourceSha256'],nativeModuleSha256=old['moduleSha256'],
        evidenceSha256={str(p.relative_to(ROOT)):digest(p) for p in paths})
    out=BASE/'case12004_stop_material_cause_verified.json'
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8')
    print('PASS: actual writes after3168; matching PCM and constraint arithmetic inputs; observed material writes recover all4000steps. Production unchanged.')


if __name__=='__main__':main()
