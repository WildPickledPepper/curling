"""Verify the actual creation/sorting and reference-face divergence chain."""
import hashlib
import json
import struct
from pathlib import Path
from verify_pcm_internal_trace import events,rows_of

ROOT=Path(__file__).resolve().parents[1]
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def read(row,address,length,edge='before'):
    for item in row[edge]:
        begin=item['ptr']; blob=bytes.fromhex(item['hex'])
        if begin<=address and address+length<=begin+len(blob):
            return blob[address-begin:address-begin+length]
    raise KeyError((address,length))
def uint(row,address): return struct.unpack('<I',read(row,address,4))[0]
def main():
    baseline,_=events(ROOT/'analysis_input/unity_11005_step486_pcm_20261001')
    validations=[]
    captured=None; event_path=None
    for name in ('unity_11005_stone_internal_calls_20261002','unity_11005_stone_deep_calls_20261002','unity_11005_pair_registration_20261002'):
        directory=ROOT/'analysis_input'/name
        captured,event_path=events(directory)
        assert not [r for r in captured if 'failed' in r['type']]
        assert rows_of(captured,'sliding.random_range.friction')==rows_of(baseline,'sliding.random_range.friction')
        for kind in ('a12.dense_pre_angular_setter','a12.dense_post_angular_setter'):
            def stable(row): return {k:v for k,v in row.items() if k not in ('nativePtr','bridgePtr','tickSerial')}
            assert len(rows_of(captured,kind))==1023
            assert [stable(r) for r in rows_of(captured,kind)]==[stable(r) for r in rows_of(baseline,kind)]
        frames=rows_of(captured,'c04.dynamic_solver_frame')
        assert len(frames)==40
        for a,b in zip(frames,rows_of(baseline,'c04.dynamic_solver_frame')):
            for edge in ('entryCores','exitCores'):
                def core(c): return {k:v for k,v in c['decodedCandidate'].items() if k!='ptr'}
                assert [core(c) for c in a[edge]]==[core(c) for c in b[edge]]
        def samples(d): return [json.loads(s) for s in next(d.glob('collision*.jsonl')).read_text().splitlines()]
        physical=('sample_id','after_position','final_xy','target_moves','requested','collision_observed')
        assert [{k:r[k] for k in physical} for r in samples(directory)]==[
            {k:r[k] for k in physical} for r in samples(ROOT/'analysis_input/unity_11005_step486_pcm_20261001')]
        validations.append({'events':str(event_path),'sha256':sha(event_path),
            'frictionValues':15580,'setterPairs':1023,'solverFrames':40,'endpoints':12})
    calls=rows_of(captured,'a12.pcm_internal_call')
    sort=next(c for c in calls if c['functionIndex']==71700 and c['ordinal']==1023)
    ctor=next(c for c in calls if c['functionIndex']==71680 and c['parentCallId']==sort['callId'])
    # ShapeSim +4 -> ActorSim; ActorSim +48 is the RigidID used by f71700.
    incoming_sim=[uint(sort,p+4) for p in sort['args'][1:3]]
    ids=[uint(ctor,p+48) for p in incoming_sim]
    assert ids==[16,1]
    assert ctor['args'][1:3]==incoming_sim
    target_ice=next(c for c in calls if c['functionIndex']==71700 and c['ordinal']==0)
    active_ice=next(c for c in calls if c['functionIndex']==71700 and c['ordinal']==2)
    assert target_ice['args'][1]==sort['args'][2]
    assert active_ice['args'][1]==sort['args'][1]
    native_path=ROOT/'analysis_input/native_stone_pair_sort_interceptor_20261002/calls.json'
    native=json.loads(native_path.read_text())
    assert native['callStackReliable'] and not native['unfinished'] and native['dropped']==0
    ns=next(c for c in native['calls'] if c['functionRva']=='0x236ed0')
    ni=ns['pairSortInput']
    assert [c['actorType'] for c in ni]==[1,1]
    assert [c['rigidId'] for c in ni]==[3,9]
    poses=[list(struct.unpack_from('<3f',bytes(c['bodyCoreBytes']),16)) for c in ni]
    pcm=rows_of(captured,'c05.persistent_pcm_call')[0]
    assert poses[0]==pcm['before']['transform0']['p']
    assert poses[1]==pcm['before']['transform1']['p']
    nc=next(c for c in native['calls'] if c['functionRva']=='0x27c630' and c['parentCallId']!=None)
    assert nc['args'][1:3]==[ni[1]['actorSim'],ni[0]['actorSim']]
    reference=json.loads((ROOT/'analysis_input/reference_face_compare_replay_20261002.json').read_text())
    assert reference['comparison']['lhs']==reference['comparison']['rhs']==0.9997755289077759
    assert reference['comparison']['taken']
    full=next(c for c in calls if c['functionIndex']==70077)
    clip=next(c for c in calls if c['functionIndex']==70076)
    assert clip['args'][0:2]==[full['args'][1],full['args'][0]]
    def uplane(argument): return list(struct.unpack('<4f',read(clip,clip['args'][argument],16)))
    nfull=next(c for c in native['calls'] if c['functionRva']=='0x3c5a90')
    nclip=next(c for c in native['calls'] if c['functionRva']=='0x3cab40')
    assert nclip['args'][:2]==[nfull['args'][1],nfull['args'][0]]
    assert nclip['returnAddressRva']=='0x3c868f' # >= branch's actual generatedContacts call.
    def nplane(argument):
        return list(struct.unpack('<4f',bytes.fromhex(next(r['hex'] for r in nclip['before'] if r['argument']==argument))[:16]))
    assert nplane(2)==uplane(3) and nplane(3)==uplane(2)
    # The true scene GJK status is the same as the observed Unity GJK status.
    assert next(c for c in calls if c['functionIndex']==70533)['result']==4
    assert next(c for c in native['calls'] if c['functionRva']=='0x320e40')['resultRax']=='0x4'
    production=json.loads((ROOT/'analysis_input/c131_production_geometry_pose_fix_all_steps_20261002.json').read_text())
    local_paths=[]
    for name in ('native_stone_pair_interceptor_20261002','native_stone_scene_interceptor_20261002','native_stone_pair_sort_interceptor_20261002'):
        path=ROOT/'analysis_input'/name/'alignment.json'
        local=json.loads(path.read_text())
        assert local['rows']==production['rows'] and local['aggregate']==production['aggregate']
        local_paths.append({'path':str(path),'sha256':sha(path)})
    result={'sampleId':11005,'physicalStep':1022,'setterOrdinal':1023,
        'firstConfirmedPairCreationInputDifference':'RigidID role ordering',
        'unity':{'sortFunctionIndex':71700,'constructorFunctionIndex':71680,
                 'activeRigidId':16,'targetRigidId':1,'order':['active','target'],'referenceRole':'target'},
        'local':{'sortRva':'0x236ed0','sortCompareRva':'0x236f65','constructorRva':'0x27c630',
                 'activeRigidId':3,'targetRigidId':9,'order':['target','active'],'referenceRole':'active',
                 'fullManifoldRva':'0x3c5a90','compareRva':'0x3c861e','generatedContactsRva':'0x3cab40',
                 'generatedContactsReturnRva':nclip['returnAddressRva']},
        'gjkStatusBoth':4,'unitySourceReplayComparison':reference['comparison'],
        'samePhysicalFacePlanes':{'target':uplane(2),'active':uplane(3)},
        'unityValidations':validations,'localValidations':local_paths,
        'nativeCallsPath':str(native_path),'nativeCallsSha256':sha(native_path),
        'unityWasmSha256':'cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81',
        'nativeModuleSha256':native['moduleSha256'],
        'sourceHashes':{str(p):sha(p) for p in [ROOT/'analysis_input/pcm_functions_20261001/f71700.wat',
            ROOT/'analysis_input/pcm_functions_20261001/f70077.wat',ROOT/'analysis_input/native_full_manifold_20261002.asm']},
        'limits':['Native reference comparison scores are not sampled; its >= branch is observed via the actual call site.',
            'Target quaternion/velocity history and solver lock flags remain separate known input differences.',
            'This locates sorting input and the immediate reference-face divergence; no production repair or whole trajectory alignment claim.']}
    out=ROOT/'analysis_input/collision_pair_sort_verified_20261002.json'
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('firstConfirmedPairCreationInputDifference','unity','local','unitySourceReplayComparison')}))
if __name__=='__main__': main()
