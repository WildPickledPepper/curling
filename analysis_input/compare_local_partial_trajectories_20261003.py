"""Compare partial truth against current replay with identical recorded inputs."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis_input/local_partial_validation_20261003'
FIELDS=['px','py','pz','qx','qy','qz','qw','vx','vy','vz','wx','wy','wz']

def bits(values):
    return list(struct.unpack('<%dI'%len(values),struct.pack('<%df'%len(values),*values)))

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def setup(record):
    reset=None;shots=[]
    for row in record['commands']:
        if row['type']!='websocket.recv':continue
        for text in row['text'].splitlines():
            tokens=text.strip().split()
            if not tokens:continue
            if tokens[0]=='RESETPOSITION' and len(tokens)==33:reset=list(map(float,tokens[1:]))
            if tokens[0]=='BESTSHOT' and len(tokens)==4:
                shots.append((reset,list(map(float,tokens[1:]))))
    if len(shots)!=1 or shots[0][0] is None:return None
    return tuple(bits(shots[0][0]+shots[0][1]))

def selected(record):
    with gzip.open(ROOT/record['selectedPath'],'rt',encoding='utf8') as f:
        return [json.loads(line) for line in f]

def main():
    inventory=json.loads((OUT/'inventory.json').read_text(encoding='utf8'))
    by_path={r['path']:r for r in inventory['capturesInventory']}
    source_sha=sha(ROOT/'local_simulator/unity_physx.py')
    regression=json.loads((ROOT/'analysis_input/wall_repair_regression_20261003/report.json').read_text())
    references=[]
    for case in regression['cases']:
        evidence=case['evidence']
        event=next(p for p in evidence if p.endswith('events.jsonl'))
        native_path=next(p for p in evidence if p.endswith('_native.json'))
        native=json.loads((ROOT/native_path).read_text())
        assert native['sourceSha256']==source_sha
        assert sha(ROOT/native_path)==evidence[native_path]
        assert by_path[event]['sha256']==native['unityEventsSha256']==evidence[event]
        references.append((setup(by_path[event]),native,native_path))
    reports=[]
    skipped=[]
    for record in inventory['capturesInventory']:
        if not record['eventCounts'].get('a12.dense_pre_angular_setter'):continue
        key=setup(record)
        if key is None:
            skipped.append(dict(path=record['path'],reason='Persistent batch or incomplete Reset/shot command history. Needs a history replay adapter.'))
            continue
        events=selected(record)
        pre=[r for r in events if r['type']=='a12.dense_pre_angular_setter']
        sliding=[r for r in pre if r['data'].get('tickSerial') is not None and
                 r['data'].get('getterLinear') is not None and r['data'].get('getterAngular') is not None]
        if [r['data']['ordinal'] for r in sliding]!=list(range(2,len(sliding)+2)):
            skipped.append(dict(path=record['path'],reason='Sliding setter schedule is not a contiguous sampled prefix.'));continue
        noises=[r['data']['lastFrictionNoise'] for r in sliding]
        compatible=[r for r in references if r[0]==key and r[1]['frictionNoises'][:len(noises)]==noises]
        if not compatible:
            identifier=hashlib.sha256(json.dumps([key,noises]).encode()).hexdigest()[:16]
            input_path=OUT/('inputs_'+identifier+'.json')
            output_path=OUT/('native_'+identifier+'.json')
            values=list(struct.unpack('<35f',struct.pack('<35I',*key)))
            # These are fresh single-shot captures. The same first-shot
            # active index is verified by their release/dense state comparison.
            inputs=dict(positions=values[:32],shot=values[32:],activeIndex=0,
                        frictionNoises=noises,unityEventsSha256=record['sha256'])
            input_path.write_text(json.dumps(inputs),encoding='utf8')
            with (OUT/('native_'+identifier+'.log')).open('w',encoding='utf8') as log:
                subprocess.run([r'C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe',
                    str(ROOT/'analysis_input/replay_partial_inputs_cp39_20261003.py'),
                    str(input_path),str(output_path)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,
                    check=True,creationflags=subprocess.CREATE_NO_WINDOW)
            generated=(key,json.loads(output_path.read_text()),str(output_path.relative_to(ROOT)))
            references.append(generated);compatible=[generated]
        _,native,native_path=compatible[0]
        rows=[];first=None;counts=Counter();core_ids=None
        def compare(tick,stone,actual,expected,line,kind,fields=FIELDS):
            nonlocal first
            counts[kind+'.windows']+=1;counts[kind+'.bytesCompared']+=len(actual)*4
            if actual==expected:
                counts[kind+'.exactWindows']+=1
                return
            counts[kind+'.differentWindows']+=1
            word=next(i for i,(a,b) in enumerate(zip(actual,expected)) if a!=b)
            d=dict(physicsTick=tick,stoneIndex=stone,field=fields[word],line=line,
                   unityBits=hex(actual[word]),nativeBits=hex(expected[word]),kind=kind)
            rows.append(d)
            if first is None or tick<first['physicsTick']:first=d
        for row in pre:
            u=row['data'];ordinal=u['ordinal']
            if ordinal==1:
                compare(0,native['stoneIndices'][0],bits(u['pose']['p']+u['pose']['q']),
                        native['releaseBits'][0][:7],row['line'],'releasePose',FIELDS[:7])
        release_posts=[r for r in events if r['type']=='a12.dense_post_angular_setter'
                       and r['data']['ordinal']==1]
        release_stage=[]
        for row in release_posts:
            u=row['data']
            if u.get('bridge164') is not None:
                original=u.get('bridge164Bits') or bits(u['bridge164'])
                activated=native['releaseBits'][0][10:13]
                release_stage.append(dict(line=row['line'],unityCachedAngularBits=original,
                    nativeAfterActivationAngularBits=activated,valuesDiffer=original!=activated,
                    status='different_call_stages_not_a_trajectory_comparison',
                    reason='The sampled initial f73035 cache write precedes SetActive. f73018 recreates the actor and calls f73035 again directly. Native releaseBits is after that activation.'))
        for row in sliding:
            u=row['data'];tick=u['ordinal']-2
            expected=native['releaseBits'][0] if tick==0 else native['states'][tick-1][0]
            actual=bits(u['pose']['p']+u['pose']['q']+u['getterLinear']+u['getterAngular'])
            compare(tick,native['stoneIndices'][0],actual,expected,row['line'],'denseBeforeTick')
        # Tail/Reset events are intentionally parsed from source lines, not
        # reconstructed from an absent window. Main/target identities come
        # from the first observed boundary and the verified two-stone layout.
        with (ROOT/record['path']).open(encoding='utf8') as f:
            for line_no,line in enumerate(f,1):
                if 'a12.tail_phase_core' not in line:continue
                event=json.loads(line)
                if event['type']!='a12.tail_phase_core':continue
                u=event['data']
                if u.get('phase')!='DCP.FixedUpdate.boundary' or u.get('edge')!='enter':continue
                tick=u['solverSerial']
                if tick>len(native['states']):continue
                if core_ids is None:
                    if tick!=0:continue
                    main=u['mainCorePtr']
                    core_ids=[main]+[c['corePtr'] for c in u['cores'] if c['corePtr']!=main]
                    if len(core_ids)!=len(native['stoneIndices']):core_ids=None;continue
                mapping={c['corePtr']:c for c in u['cores']}
                enabled=native['releaseSimulating'] if tick==0 else native['simulating'][tick-1]
                counts['membership.windows']+=1
                if set(mapping)=={c for c,flag in zip(core_ids,enabled) if flag}:
                    counts['membership.exactWindows']+=1
                else:
                    counts['membership.differentWindows']+=1
                    d=dict(physicsTick=tick,line=line_no,kind='liveActorMembership',
                           unity=sorted(mapping),native=sorted(c for c,flag in zip(core_ids,enabled) if flag))
                    if first is None or tick<first['physicsTick']:first=d
                states=native['releaseBits'] if tick==0 else native['states'][tick-1]
                for i,ptr in enumerate(core_ids):
                    if ptr not in mapping or not enabled[i]:continue
                    words=mapping[ptr]['bits'];actual=words[4:7]+words[:4]+words[7:13]
                    compare(tick,native['stoneIndices'][i],actual,states[i],line_no,'tailBoundary')
        report=dict(path=record['path'],unityEventsSha256=record['sha256'],nativePath=native_path,
            nativeSha256=sha(ROOT/native_path),checks=dict(counts),firstDifference=first,
            differenceExamples=rows[:12],frictionPrefixExact=len(noises),
            releaseCacheStageRecords=release_stage,
            scope='Full replay consumes identical Reset/shot/friction inputs; only actually sampled release and pre-tick/tail states are compared.')
        reports.append(report)
        print(json.dumps(dict(path=report['path'],firstDifference=first,checks=dict(counts))),flush=True)
    totals=Counter()
    for r in reports:totals.update(r['checks'])
    result=dict(comparedCaptures=len(reports),capturesWithDifferences=sum(r['firstDifference'] is not None for r in reports),
                totals=dict(totals),captures=reports,pendingCaptures=skipped,
                productionSourceSha256=source_sha,scope='Fresh single-shot captures with exact available input-prefix match. Persistent batches are not replaced with fresh scenes.')
    (OUT/'partial_trajectories.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('captures','pendingCaptures')},indent=2),flush=True)

if __name__=='__main__':main()
