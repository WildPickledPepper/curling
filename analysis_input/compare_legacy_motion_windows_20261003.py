"""Compare original A0/A2 measured calls; preserve missing inputs and branch evidence."""
from collections import Counter,defaultdict
from datetime import datetime,timedelta,timezone
import hashlib,json,re,struct
from itertools import chain
from pathlib import Path
from compare_local_motion_windows_20261003 import controls,bits,newfrictionstep,unity_friction,B2Vec2,STEP
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis_input/local_partial_validation_20261003'
TYPES={'a0.angular_write.last_pre_pcm','a0.angular_write.before_first_stone_task'}

def sample_key(shot,positions):return tuple(bits(shot+positions))
def sample_index():
    index=defaultdict(list)
    for path in (ROOT/'research_archive/unity_reverse/evidence/data').rglob('*.jsonl'):
        if path.name=='events.jsonl':continue
        with path.open('rb') as f:
            first=f.readline()
            if b'"requested"' not in first:continue
            for n,line in enumerate(chain([first],f),1):
                try:s=json.loads(line)
                except (ValueError,UnicodeError):continue
                q=s.get('requested') or {};p=s.get('reset_position')
                if not p or any(k not in q for k in ('v0','h0','w0')) or not s.get('issued_at_utc'):continue
                key=sample_key([q['v0'],q['h0'],q['w0']],p)
                index[key].append(dict(path=str(path.relative_to(ROOT)),line=n,
                    issuedAt=datetime.fromisoformat(s['issued_at_utc'].replace('Z','+00:00')).timestamp(),
                    sentSweep=s.get('sent_sweep'),requestedSweep=q.get('sweep')))
    return index

def branch_evidence(record,index):
    known=controls(record)
    if known:return known
    meta=(ROOT/record['path']).parent/'meta.json'
    if not meta.exists():return None
    started=json.loads(meta.read_text(encoding='utf8')).get('started_at')
    if not started:return None
    start=datetime.fromisoformat(started).replace(tzinfo=timezone(timedelta(hours=8))).timestamp()
    end=start+max((c.get('t') or 0)/1000 for c in record['commands'])+60
    positions=None;matches=[]
    for c in record['commands']:
        if c['type']!='websocket.recv':continue
        tokens=c['text'].split()
        if tokens[0]=='SWEEP':return None
        if tokens[0]=='RESETPOSITION':positions=list(map(float,tokens[1:]))
        if tokens[0]=='BESTSHOT':
            if positions is None:return None
            candidates=[s for s in index.get(sample_key(list(map(float,tokens[1:])),positions),[])
                if start-15<=s['issuedAt']<=end]
            if not candidates or any(s['sentSweep'] is not False or s['requestedSweep']!=0 for s in candidates):return None
            matches.append(dict(commandLine=c['line'],samples=candidates))
    return dict(metaPath=str(meta.relative_to(ROOT)),matchedProtocolSamples=matches,
        scope='Every received BESTSHOT/layout has nonsweep sample records within this capture session; no received SWEEP.') if matches else None

def main():
    inventory=json.loads((OUT/'inventory.json').read_text(encoding='utf8'))
    index=sample_index();reports=[];total=Counter();control_hashes={}
    for r in inventory['capturesInventory']:
        if not any(r['eventCounts'].get(k) for k in TYPES):continue
        evidence=branch_evidence(r,index);checks=[];skips=Counter();seen=set();digest=hashlib.sha256()
        if evidence:
            for match in evidence.get('matchedProtocolSamples',[]):
                for sample in match['samples']:
                    p=sample['path']
                    if p not in control_hashes:control_hashes[p]=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
                    sample['sha256']=control_hashes[p]
        with (ROOT/r['path']).open('rb') as f:
            for line_no,line in enumerate(f,1):
                digest.update(line)
                if not any(k.encode() in line for k in TYPES):continue
                event=json.loads(line)
                if event['type'] not in TYPES:continue
                d=event['data'];noises={n['tickSerial']:n for n in d.get('lastTwoFrictionNoises',[]) if n.get('tickSerial') is not None}
                calls=[]
                for w in d.get('lastTwoAngularWrites',[]) or [d.get('lastAngularWrite')]:
                    if not w:continue
                    n=noises.get(w.get('tickSerial'));g=w.get('scriptInputs') or {}
                    calls.append(dict(tick=w.get('tickSerial'),body=w.get('bodyManagedPtr'),
                        getter=g,noise=n.get('value') if n else None,angular=w.get('vector'),linear=None,
                        stage='A0.scriptSetter.beforeAngularCall',writeSerial=w.get('writeSerial')))
                for w in d.get('a2StaticTrace') or []:
                    calls.append(dict(tick=w.get('tickSerial'),body=((w.get('scriptGetter') or {}).get('linearVelocity') or {}).get('bodyManagedPtr'),
                        getter=w.get('scriptGetter') or {},noise=w.get('frictionNoise'),angular=[0.,w['setterWy'],0.],
                        linear=w.get('linearSetter'),stage='A2.capturedScriptSetters.atStaticSolve',writeSerial=w.get('angularWriteSerial')))
                for call in calls:
                    v=(call['getter'].get('linearVelocity') or {}).get('vector')
                    w=(call['getter'].get('angularVelocity') or {}).get('vector')
                    if call['tick'] is None or v is None or w is None or call['noise'] is None or call['angular'] is None:
                        skips['missingActualGetterOrSameTickNoise']+=1;continue
                    if evidence is None:skips['unresolvedSweepBranch']+=1;continue
                    key=(call['tick'],call['body'],call['writeSerial'],call['stage'])
                    if key in seen:continue
                    seen.add(key)
                    result=newfrictionstep(unity_friction(False,noise=call['noise']),B2Vec2(-v[2],-v[0]),w[1],STEP)
                    actual=bits([0.,result.angle,0.]);expected=bits(call['angular'])
                    check=dict(line=line_no,tickSerial=call['tick'],writeSerial=call['writeSerial'],stage=call['stage'],
                        localAngularBits=actual,unityAngularBits=expected,exact=actual==expected,
                        measuredLinear=v,measuredAngular=w,measuredNoise=call['noise'])
                    if call['linear'] is not None:
                        linear_actual=bits([-result.v.y,0.,-result.v.x]);linear_expected=bits(call['linear'])
                        check.update(localLinearBits=linear_actual,unityLinearBits=linear_expected,
                            linearExact=linear_actual==linear_expected)
                        if not check['linearExact']:check['exact']=False
                    checks.append(check)
        assert digest.hexdigest()==r['sha256'],r['path']+' changed since inventory'
        counts=dict(compared=len(checks),exact=sum(c['exact'] for c in checks),different=sum(not c['exact'] for c in checks))
        counts['withLinearOutput']=sum('linearExact' in c for c in checks)
        total.update(counts)
        reports.append(dict(path=r['path'],unityEventsSha256=r['sha256'],control=evidence,checks=counts,
            comparedWindows=checks,excluded=dict(skips),firstDifference=next((c for c in checks if not c['exact']),None)))
    output=dict(captures=len(reports),capturesWithComparedCalls=sum(bool(r['checks']['compared']) for r in reports),
        capturesWithDifferences=sum(bool(r['checks']['different']) for r in reports),totals=dict(total),capturesInventory=reports,
        sourceSha256=hashlib.sha256((ROOT/'local_simulator/runtime_support/tools/reverse/recovered_curling_motion.py').read_bytes()).hexdigest(),
        scope='Measured input -> current production sliding kernel -> sampled script angular output only; no unseen scene history claim.',
        mappingEvidence='Original f60124/f59956 and unity_webgl_runtime_probe.js A0 angular beforeCall / same-tick friction noise / A2 appendA2StaticTrace.')
    (OUT/'legacy_motion_windows.json').write_text(json.dumps(output,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in output.items() if k not in ('capturesInventory',)},indent=2))
if __name__=='__main__':main()
