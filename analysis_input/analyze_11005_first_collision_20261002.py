"""Locate the next observed divergence from actual PCM and solver traces."""
import hashlib
import json
import struct
from pathlib import Path

from verify_pcm_internal_trace import events,rows_of

ROOT=Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def core_values(core):
    return {k:v for k,v in core['decodedCandidate'].items() if k!='ptr'}


def main():
    baseline_dir=ROOT/'analysis_input/unity_11005_step486_pcm_20261001'
    capture_dir=ROOT/'analysis_input/unity_11005_first_dynamic_pcm_20261002'
    baseline,_=events(baseline_dir)
    captured,event_path=events(capture_dir)
    assert not [r for r in captured if 'failed' in r['type']]
    noise='sliding.random_range.friction'
    assert rows_of(captured,noise)==rows_of(baseline,noise)
    assert len(rows_of(captured,noise))==15580
    for kind in ('a12.dense_pre_angular_setter','a12.dense_post_angular_setter'):
        def stable(row):
            return {k:v for k,v in row.items() if k not in ('nativePtr','bridgePtr','tickSerial')}
        assert len(rows_of(captured,kind))==1023
        assert [stable(r) for r in rows_of(captured,kind)]==[stable(r) for r in rows_of(baseline,kind)]
    old_frames=rows_of(baseline,'c04.dynamic_solver_frame')
    frames=rows_of(captured,'c04.dynamic_solver_frame')
    assert len(frames)==len(old_frames)==40
    for a,b in zip(frames,old_frames):
        for edge in ('entryCores','exitCores'):
            assert [core_values(r) for r in a[edge]]==[core_values(r) for r in b[edge]]
    def samples(directory):
        return [json.loads(s) for s in next(directory.glob('collision*.jsonl')).read_text().splitlines()]
    physical=('sample_id','after_position','final_xy','target_moves','requested','collision_observed')
    assert [{k:r[k] for k in physical} for r in samples(capture_dir)]==[
        {k:r[k] for k in physical} for r in samples(baseline_dir)]
    local_path=ROOT/'analysis_input/c131_first_dynamic_solver_trace_v2_20261002.json'
    local=json.loads(local_path.read_text(encoding='utf-8'))
    old_local=json.loads((ROOT/'analysis_input/c131_production_geometry_pose_fix_all_steps_20261002.json').read_text(encoding='utf-8'))
    assert local['rows']==old_local['rows'] and local['aggregate']==old_local['aggregate']
    boundary=next(r for r in local['releaseBoundary'] if r['sampleId']==11005)
    assert len(boundary['postDenseFrames'])==8
    first=boundary['postDenseFrames'][0]
    assert first['ordinal']==1023
    pcm=rows_of(captured,'c05.persistent_pcm_call')
    assert len(pcm)==8
    unity=pcm[0]
    before=next(r for r in first['narrowphase'] if r['geom_type0']==r['geom_type1']==4 and not r['after'])
    after=next(r for r in first['narrowphase'] if r['geom_type0']==r['geom_type1']==4 and r['after'])
    # Active pose is bit-exact, but the actual argument order is reversed.
    for field in ('p','q'):
        assert unity['before']['transform0'][field]==before['transform1'][field]
    assert unity['before']['transform1']['p']==before['transform0']['p']
    cache_u=unity['before']['cache']['persistentManifoldCandidate']
    cache_l=before['cache']['manifold']
    assert cache_u['numContacts']==cache_l['num_contacts']==0
    assert cache_u['numWarmStartPoints']==cache_l['num_warm_start_points']==0
    assert unity['after']['contactBuffer']['count']==after['output_contacts']==2
    contacts_u=unity['after']['contactBuffer']['contactsPreview']
    contacts_l=first['finalizer'][0]['contacts']
    assert len(contacts_l)==len(contacts_u)==2
    # Canonicalize to the active->target ordering used by Unity.
    local_normals=[[-v for v in c['normal']] for c in contacts_l]
    assert contacts_u[0]['normal']!=local_normals[0]
    constraint=frames[0]['dynamicSolves'][0]['before']['descs'][0]['constraintWindow']['rawBytes']
    assert list(struct.unpack_from('<3f',bytes(constraint),32))==contacts_u[0]['normal']
    entry_data=next(r for r in first['solver_setup'] if not r['after_solve'])['body_data']
    active=entry_data[0]
    unity_active=frames[0]['entryCores'][0]['decodedCandidate']
    for key in ('p','q'):
        assert active['body2world'][key]==unity_active[key]
    assert active['linear_velocity']==unity_active['linearVelocity']
    assert active['angular_velocity']==unity_active['angularVelocity']
    stage_frames=[]
    for u,l in zip(frames,boundary['postDenseFrames']):
        stage_frames.append({'frameIndex':u['frameIndex'],
            'unityActiveExit':core_values(u['exitCores'][0]),
            'localActiveExit':l['afterNative']['1'],
            'unityTargetExit':core_values(u['exitCores'][1]),
            'localTargetExit':l['afterNative']['7']})
    result={'sampleId':11005,'physicalStep':1022,'lastDenseSetterOrdinal':1023,
        'pcmTableIndex':120118,'pcmFunctionIndex':70576,
        'solverSetupTableIndex':120569,'solverSetupFunctionIndex':71259,
        'observedFirstActiveCollisionDivergenceStage':'Convex-convex PCM output, before solver constraint construction',
        'activeSolverEntryPoseAndVelocitiesBitExact':True,
        'pairOrder':{'unity':['active','target'],'local':['target','active']},
        'targetInputQuaternion':{'unity':unity['before']['transform1']['q'],'local':before['transform0']['q']},
        'targetSolverEntryVelocity':{'unity':frames[0]['entryCores'][1]['decodedCandidate']['linearVelocity'],
                                    'local':entry_data[1]['linear_velocity']},
        'solverLockFlags':{'unityActive':unity_active['lockFlags'],'localActive':active['lock_flags']},
        'emptyManifoldInputBoth':True,'contactCountBoth':2,
        'unityContactsGeometry':[{k:c[k] for k in ('point','normal','separation')} for c in contacts_u],
        'localContactsGeometryCanonical':[{k:c[k] for k in ('point','separation')}|{'normal':normal}
            for c,normal in zip(contacts_l,local_normals)],
        'activeExitAngularY':{'unity':stage_frames[0]['unityActiveExit']['angularVelocity'][1],
                            'local':stage_frames[0]['localActiveExit']['physxAngularVelocity'][1]},
        'targetExitAngularY':{'unity':stage_frames[0]['unityTargetExit']['angularVelocity'][1],
                            'local':stage_frames[0]['localTargetExit']['physxAngularVelocity'][1]},
        'traceTransparency':{'frictionValues':15580,'denseSetterPairs':1023,'c04Frames':40,'endpoints':12,
                             'localTrajectoryUnchanged':True},
        'evidence':{'unityEvents':str(event_path),'unityEventsSha256':sha(event_path),
                    'localReport':str(local_path),'localReportSha256':sha(local_path),
                    'unityWasmSha256':'cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81'},
        'frames':stage_frames,
        'limitation':'This identifies actual input and PCM-output differences. It does not prove which input/branch causes the discrepancy; pair ordering and target history must be traced upstream. It is not an equal-input kernel failure claim.'}
    output=ROOT/'analysis_input/11005_first_collision_divergence_verified_20261002.json'
    output.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('physicalStep','lastDenseSetterOrdinal','observedFirstActiveCollisionDivergenceStage','activeExitAngularY','targetExitAngularY')}))


if __name__=='__main__':
    main()
