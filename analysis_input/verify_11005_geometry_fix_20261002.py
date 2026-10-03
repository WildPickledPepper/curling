"""Verify the formerly divergent 488th native setter using production changes."""
import hashlib
import argparse
import json
from pathlib import Path

from verify_pcm_internal_trace import events,rows_of,geometry_points

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path,default=ROOT/'analysis_input/c131_production_geometry_pose_fix_all_steps_20261002.json')
    parser.add_argument('--output',type=Path,default=ROOT/'analysis_input/11005_geometry_fix_verified_20261002.json')
    opts=parser.parse_args()
    source = opts.report
    report = json.loads(source.read_text(encoding='utf-8'))
    capture = ROOT/'analysis_input/unity_11005_step486_pcm_20261001'
    recorded,path = events(capture)
    pre = rows_of(recorded,'a12.dense_pre_angular_setter')
    post = rows_of(recorded,'a12.dense_post_angular_setter')
    pcm = rows_of(recorded,'a12.pcm_convex_mesh')
    boundary = next(r for r in report['releaseBoundary'] if r['sampleId']==11005)
    local = boundary['setters']
    assert len(pre)==len(post)==len(local)==1023
    for i,(u,v,l) in enumerate(zip(pre,post,local),1):
        assert u['ordinal']==v['ordinal']==i
        assert u['pose']['q']==l['rawQuaternion'],('q',i)
        assert u['pose']['p']==l['rawBefore']['physxPosition'],('p',i)
        assert v['bridge164']==l['result'],('angular setter',i)
    assert len(boundary['directContacts'])==3
    for query in boundary['directContacts']:
        truth = next(r for r in pcm if r['ordinal']==query['ordinal'])
        for index in (0,1):
            for field in ('p','q'):
                assert query['result']['input_transform'+str(index)][field] == truth['before']['transform'+str(index)][field]
        assert query['result']['points']==geometry_points(truth['after']['contactBuffer'])
        assert 'matchedInputGeometryProbe' not in query  # physical shape itself is corrected
    scale_events,_ = events(ROOT/'analysis_input/unity_pcm_geometry_scales_20261001')
    scales = [r for r in rows_of(scale_events,'a12.pcm_geometry_scale') if r['transform0']['p'][0]<-90]
    assert len(scales)==len(report['releaseBoundary'])==12
    for truth,local_release in zip(scales,report['releaseBoundary']):
        assert local_release['localGeometryScale']==truth['scale']
    cfg=report['diagnosticEffectiveConfiguration']
    assert cfg['transformScaleRefresh'] and cfg['bodyPoseWriteback']
    assert report['diagnosticDirectProbeScaleXz'] is None
    # Explicitly preserve the audit boundary: this is a fixed initial-state
    # replay, not evidence of end-to-end accuracy for arbitrary online states.
    getter_differences = []
    for u,l in zip(pre,local):
        if u['getterAngular'] is not None and u['getterAngular'] != l['rawBefore']['physxAngularVelocity']:
            getter_differences.append({'ordinal':u['ordinal'],'unity':u['getterAngular'],
                'localRaw':l['rawBefore']['physxAngularVelocity']})
    scripts = [ROOT/'local_simulator/unity_physx.py',
               ROOT/'local_simulator/runtime_support/tools/reverse/recovered_transform_scale.py']
    result = {'sampleId':11005,'oldFirstDivergentSetter':488,
        'rawPositionQuaternionAndSetterOutputsExactThroughOrdinal':1023,
        'contactQueriesExactOrdinals':[r['ordinal'] for r in boundary['directContacts']],
        'releaseScalesExact':12,'productionPoseWriteback':True,
        'postReleaseUnityInjection':False,
        'recordedInitialQuaternionOverride':report['diagnosticInitialQuaternionInjection'],
        'recordedResetYawAndFriction':True,
        'productionSourceSha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in scripts},
        'report':str(source),'reportSha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'unityEvents':str(path),'unityEventsSha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'remainingGetterAngularVsRawDifferences':getter_differences,
        'remainingEndpointErrorM':next(r['endpointErrorM'] for r in report['rows'] if r['sampleId']==11005),
        'limitation':'The 488th setter divergence is fixed. Setter capture ends at 1023; no later first-divergence ordinal is established. Collision-tail endpoint error and getter-vs-raw differences remain.'}
    output=opts.output
    output.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k in ('sampleId','rawPositionQuaternionAndSetterOutputsExactThroughOrdinal','contactQueriesExactOrdinals','releaseScalesExact','remainingEndpointErrorM')}))


if __name__=='__main__':
    main()
