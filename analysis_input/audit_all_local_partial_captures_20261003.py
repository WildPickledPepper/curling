"""Inventory every local Unity events.jsonl and check measured function windows.

No missing state is filled, no truth pose is installed in a running scene.
Function replay uses measured inputs, so passing it is not a trajectory claim.
"""
import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import gzip
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analysis_input/local_partial_validation_20261003'
TYPE = re.compile(rb'"type"\s*:\s*"([^"\n]+)"')
SELECT = {'a12.dense_pre_angular_setter', 'a12.dense_post_angular_setter',
          'a12.angular_setter_two_pose_inputs', 'a12.velocity_getter_native'}


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(4 * 1024 * 1024), b''): h.update(block)
    return h.hexdigest()


def scan(path):
    relative = str(path.relative_to(ROOT))
    key = hashlib.sha256(relative.encode()).hexdigest()[:16]
    selected = OUT / 'selected' / (key + '.jsonl.gz')
    h = hashlib.sha256()
    counts = Counter()
    bad = []
    hooks = Counter()
    phases = Counter()
    commands = []
    manifests = []
    selected_count = 0
    with path.open('rb') as f, gzip.open(selected, 'wt', encoding='utf8') as g:
        for line_no, line in enumerate(f, 1):
            h.update(line)
            m = TYPE.search(line)
            if not m:
                if line.strip(): bad.append(line_no)
                continue
            kind = m[1].decode('utf8')
            counts[kind] += 1
            wanted = (kind in SELECT or kind.startswith('websocket.') or
                      kind.startswith('rng.') or kind in ('a12.early_phase_core',
                      'physx.native.before', 'probe.installed', 'wasm.instance'))
            if not wanted: continue
            try: row = json.loads(line)
            except (ValueError, UnicodeDecodeError):
                bad.append(line_no)
                continue
            data = row.get('data') or {}
            if kind in SELECT:
                g.write(json.dumps({'line':line_no,'type':kind,'data':data}, separators=(',',':'))+'\n')
                selected_count += 1
            elif kind == 'a12.early_phase_core':
                phases[data.get('phase','?')] += 1
                if str(data.get('phase','')).startswith('normalizeCandidate.'):
                    g.write(json.dumps({'line':line_no,'type':kind,'data':data}, separators=(',',':'))+'\n')
                    selected_count += 1
            elif kind == 'physx.native.before':
                hook = data.get('hook') or {}
                hooks[str(hook.get('wasm'))+':'+str(hook.get('name'))] += 1
            elif kind.startswith('websocket.'):
                message = data.get('textPreview', '')
                if re.search(r'BESTSHOT|RESETPOSITION|SWEEP|SHOTNUM|GO\b', message):
                    commands.append({'line':line_no,'type':kind,'text':message,'t':row.get('t')})
            elif kind in ('probe.installed', 'wasm.instance') or kind.startswith('rng.'):
                if len(manifests) < 20: manifests.append({'line':line_no,'type':kind,'data':data})
    return dict(path=relative,sizeBytes=path.stat().st_size,sha256=h.hexdigest(),
                eventCounts=dict(counts),malformedSelectedLines=bad[:30],
                nativeHooks=dict(hooks),phases=dict(phases),commands=commands,
                provenanceEvents=manifests,selectedPath=str(selected.relative_to(ROOT)),
                selectedEvents=selected_count)


def bits(values):
    return list(struct.unpack('<%dI'%len(values), struct.pack('<%df'%len(values), *values)))


def check(record, Scene, np):
    rows = []
    with gzip.open(ROOT/record['selectedPath'],'rt',encoding='utf8') as f:
        rows = [json.loads(line) for line in f]
    grouped = defaultdict(lambda: defaultdict(list))
    for event in rows:
        d=event['data']
        grouped[(d.get('releaseSerial'),d.get('ordinal'))][event['type']].append(event)
    dummy=SimpleNamespace(probe=SimpleNamespace(np=np))
    counters=Counter()
    skipped=Counter()
    differences=[]
    first_by_check={}
    def compare(name, actual, expected, line, context):
        counters[name+'.compared'] += 1
        counters[name+'.bytesCompared'] += len(actual)*4
        if actual == expected:
            counters[name+'.exact'] += 1
            return
        counters[name+'.different'] += 1
        word=next((i for i,(a,b) in enumerate(zip(actual,expected)) if a!=b),None)
        detail=dict(check=name,line=line,context=context,word=word,
                    localBits=actual,unityBits=expected)
        first_by_check.setdefault(name,detail)
        if len(differences)<16: differences.append(detail)
    for key, group in grouped.items():
        pre=group.get('a12.dense_pre_angular_setter',[])
        post=group.get('a12.dense_post_angular_setter',[])
        poses=group.get('a12.angular_setter_two_pose_inputs',[])
        if pre or post:
            # The pose getter is also invoked outside an angular setter;
            # its result-48 window is meaningful only inside this call.
            # Recording-limit tails repeat a post ordinal; retain the first
            # completed call whose pre input was actually recorded.
            if len(pre)==1:
                candidates=[p for p in post if p['line']>pre[0]['line']]
                if candidates:
                    post=[candidates[0]]
                    poses=[p for p in poses if pre[0]['line']<p['line']<post[0]['line']]
            if len(pre)==len(post)==1 and (key[1]>=2 or poses):
                u,v=pre[0]['data'],post[0]['data']
                if u['setterAngular'][0]==0 and u['setterAngular'][2]==0:
                    q=u['pose']['q']
                    body=SimpleNamespace(get_global_pose=lambda:(None,
                        SimpleNamespace(x=q[0],y=q[1],z=q[2],w=q[3])))
                    slot=SimpleNamespace(index=0,body=body)
                    model=SimpleNamespace(probe=SimpleNamespace(np=np),
                        _unity_angular_setter_calls={0:key[1]-1})
                    actual=bits(Scene._unity_native_angular_setter_vector(model,slot,u['setterAngular'][1]))
                    for field in ('bridge164','bridge300'):
                        if field in v:
                            compare('angularSetterFromBodyPose.'+field,actual,
                                v.get(field+'Bits') or bits(v[field]),post[0]['line'],
                                dict(releaseSerial=key[0],ordinal=key[1],inputLine=pre[0]['line'],
                                     measuredTransformAvailable=bool(poses)))
            elif len(pre)==len(post)==1:
                # f73035 checks native component byte136 & 112 before any
                # rotation. Fresh release can precede Start's constraints.
                # Missing Transform getter is not a license to force the
                # locked-axis helper into that different caller branch.
                skipped['angularSetterFromBodyPose.releaseConstraintBranchUnobserved']+=1
            if len(pre)!=1 or len(post)!=1:
                skipped['angularProjection.ambiguousOrMissingPair'] += max(len(pre),len(post))
            elif not poses:
                skipped['angularProjection.missingMeasuredTransform'] += 1
            elif len({tuple(p['data']['transformPose']['q']) for p in poses})!=1:
                skipped['angularProjection.ambiguousTransform'] += 1
            elif any(bits(p['data']['bridgePose']['q'])!=bits([0.,0.,0.,1.]) for p in poses):
                skipped['angularProjection.nonidentityRelativeQuaternion'] += 1
            else:
                u,v=pre[0]['data'],post[0]['data']
                arg=u['setterAngular']
                if arg[0]!=0 or arg[2]!=0:
                    skipped['angularProjection.nonWorldYInput']+=1
                else:
                    actual=bits(Scene._unity_project_locked_angular_velocity(dummy,
                        tuple(poses[0]['data']['transformPose']['q']),arg[1]))
                    for field in ('bridge164','bridge300'):
                        if field not in v:
                            skipped['angularProjection.missing.'+field]+=1
                            continue
                        expected=v.get(field+'Bits') or bits(v[field])
                        compare('angularProjection.'+field, actual, expected, post[0]['line'],
                                dict(releaseSerial=key[0],ordinal=key[1],
                                     inputLine=pre[0]['line'],transformLine=poses[0]['line']))
        for event in group.get('a12.velocity_getter_native',[]):
            d=event['data']; kind=d.get('kind')
            required=['coreBeforeBits','outputBits','coreAfterBits']
            if not all(name in d for name in required):
                skipped['velocityGetter.missingRawBits']+=1;continue
            # Native getters copy their measured core input into the output;
            # signed-zero restoration is part of the current simulator path.
            actual=d['coreBeforeBits']
            for field in ('outputBits','coreAfterBits','bufferAfterBits'):
                if field in d:
                    compare('velocityGetter.'+str(kind)+'.'+field,actual,d[field],
                        event['line'],dict(releaseSerial=key[0],ordinal=key[1],
                                          tableIndex=d.get('bridgeGetterTableIndex')))
        phase_pairs=defaultdict(lambda:defaultdict(list))
        for event in group.get('a12.early_phase_core',[]):
            phase_pairs[event['data'].get('phase')][event['data'].get('edge')].append(event)
        for phase,edges in phase_pairs.items():
            if len(edges['enter'])!=1 or len(edges['exit'])!=1:
                skipped['poseNormalization.ambiguousOrMissingPair']+=1;continue
            a,b=edges['enter'][0],edges['exit'][0]
            if not a['data'].get('core') or not b['data'].get('core'):
                skipped['poseNormalization.missingCore']+=1;continue
            f=np.float32
            q=list(map(f,a['data']['core']['q']))
            x,y,z,w=q
            norm2=f(f(f(f(x*x)+f(y*y))+f(z*z))+f(w*w))
            inverse=f(f(1)/f(np.sqrt(norm2)))
            actual=bits([float(f(v*inverse)) for v in q])
            compare('poseNormalization',actual,bits(b['data']['core']['q']),b['line'],
                    dict(releaseSerial=key[0],ordinal=key[1],function=phase,inputLine=a['line']))
    return dict(path=record['path'],sha256=record['sha256'],checks=dict(counters),
                skipped=dict(skipped),firstDifferences=first_by_check,differenceExamples=differences,
                scope='Measured-input function windows. No full-scene or serial-prefix claim.')


def main():
    p=argparse.ArgumentParser();p.add_argument('--reuse-inventory',action='store_true');args=p.parse_args()
    OUT.mkdir(exist_ok=True);(OUT/'selected').mkdir(exist_ok=True)
    inventory_file=OUT/'inventory.json'
    if args.reuse_inventory:
        inventory=json.loads(inventory_file.read_text(encoding='utf8'))
    else:
        found=subprocess.check_output(['rg','--files','-uuu','-g','events.jsonl'],cwd=ROOT).decode('utf8').splitlines()
        paths=[ROOT/path for path in found]
        records=[];size=0
        with ThreadPoolExecutor(max_workers=4) as pool:
            for future in as_completed([pool.submit(scan,path) for path in paths]):
                r=future.result();records.append(r);size+=r['sizeBytes']
                print(json.dumps(dict(scanned=len(records),total=len(paths),bytes=size,path=r['path'])),flush=True)
        inventory=dict(captures=len(records),bytes=sum(r['sizeBytes'] for r in records),
                       capturesInventory=sorted(records,key=lambda r:r['path']))
        inventory_file.write_text(json.dumps(inventory,indent=2),encoding='utf8')
    sys.path.insert(0,str(ROOT))
    import numpy as np
    from local_simulator.unity_physx import PersistentPhysxFrontHalfScene as Scene
    reports=[check(r,Scene,np) for r in inventory['capturesInventory']]
    totals=Counter();skips=Counter();types=Counter()
    for r in reports:totals.update(r['checks']);skips.update(r['skipped'])
    for r in inventory['capturesInventory']:types.update(r['eventCounts'])
    report=dict(captures=inventory['captures'],bytes=inventory['bytes'],
        capturesWithComparedWindows=sum(bool(r['checks']) for r in reports),
        capturesWithDifferences=sum(bool(r['firstDifferences']) for r in reports),
        totals=dict(totals),skipped=dict(skips),eventTotals=dict(types),capturesInventory=reports,
        productionSourceSha256=digest(ROOT/'local_simulator/unity_physx.py'),
        unityWasmSha256=digest(ROOT/'analysis_input/unity_20260930.wasm'),
        scope='All local event files inventoried; measured angular setter/getter/normalization windows checked. Remaining event types require their specific replay adapters.')
    (OUT/'function_windows.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('capturesInventory','eventTotals')},indent=2),flush=True)


if __name__=='__main__':main()
