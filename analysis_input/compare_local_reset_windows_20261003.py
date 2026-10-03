"""Compare first-Reset partial core windows, with original phase boundaries."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct
import subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'analysis_input/local_partial_validation_20261003'
PY39=r'C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe'
def main():
    inventory=json.loads((OUT/'inventory.json').read_text());cache={};reports=[];pending=[];totals=Counter()
    for record in inventory['capturesInventory']:
        if not record['eventCounts'].get('scene.reset_body_cores'):continue
        command=next((c for c in record['commands'] if c['type']=='websocket.recv'
                      and c['text'].startswith('RESETPOSITION ')),None)
        if not command:pending.append(dict(path=record['path'],reason='First Reset input command absent.'));continue
        positions=list(map(float,command['text'].split()[1:]))
        targets=[i for i in range(16) if positions[2*i:2*i+2]!=[0.,0.]]
        if len(targets)!=1:
            pending.append(dict(path=record['path'],reason='Multi-body Reset needs an explicit roster mapping adapter.'));continue
        key=hashlib.sha256(json.dumps(positions).encode()).hexdigest()[:16]
        input_path=OUT/('reset_inputs_'+key+'.json');output_path=OUT/('reset_native_'+key+'.json')
        if key not in cache:
            input_path.write_text(json.dumps(dict(positions=positions,targetIndex=targets[0])),encoding='utf8')
            with (OUT/('reset_native_'+key+'.log')).open('w',encoding='utf8') as log:
                subprocess.run([PY39,str(ROOT/'analysis_input/replay_partial_reset_cp39_20261003.py'),
                    str(input_path),str(output_path)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,
                    check=True,creationflags=subprocess.CREATE_NO_WINDOW)
            cache[key]=json.loads(output_path.read_text())
        native=cache[key];counts=Counter();first=None;step=0;entered=False
        with (ROOT/record['path']).open(encoding='utf8') as f:
            for line_no,line in enumerate(f,1):
                if 'scene.reset_body_cores' not in line:continue
                event=json.loads(line)
                if event['type']!='scene.reset_body_cores':continue
                u=event['data']
                if u.get('resetSerial')!=1:continue
                if u['edge']=='enter':step+=1;entered=True
                elif not entered:continue
                if not u['cores']:
                    counts['emptyCapturedCoreWindows']+=1;continue
                if len(u['cores'])!=1:
                    counts['unsupportedRoster']+=1;continue
                core=u['cores'][0];words=core['bits'];actual=words[4:7]+words[:4]+words[7:13]
                if step<=len(native['frames']):
                    frame=native['frames'][step-1]
                    phases=[p for p in frame['solverPhases'] if p['afterSolve']==(u['edge']=='exit')]
                    expected=phases[0]['bits'] if len(phases)==1 else frame['before' if u['edge']=='enter' else 'after']
                else:expected=native['frames'][-1]['after']
                counts['compared']+=1;counts['bytesCompared']+=52
                if actual==expected:counts['exact']+=1
                else:
                    counts['different']+=1
                    if first is None:
                        word=next(i for i,(a,b) in enumerate(zip(actual,expected)) if a!=b)
                        first=dict(line=line_no,resolvedPhysicsStep=step,reportedStep=u.get('step'),
                            reportedFrame=u.get('frame'),edge=u['edge'],word=word,
                            unityBits=hex(actual[word]),nativeBits=hex(expected[word]))
        report=dict(path=record['path'],unityEventsSha256=record['sha256'],checks=dict(counts),
            firstDifference=first,nativePath=str(output_path.relative_to(ROOT)),
            nativeSha256=hashlib.sha256(output_path.read_bytes()).hexdigest(),
            observerOutputsUnchanged=native['observerOutputsUnchanged'],
            targetIndex=targets[0],nativeNaturalSleepStep=len(native['frames']))
        reports.append(report);totals.update(counts)
        if not counts['compared']:
            pending.append(dict(path=record['path'],reason='Reset core window exists but contains no usable core payload.'))
        print(json.dumps(dict(path=record['path'],checks=dict(counts),firstDifference=first)),flush=True)
    result=dict(captures=len(reports),totals=dict(totals),capturesInventory=reports,pendingCaptures=pending,
        scope='First Reset solver core enter/exit sampled raw P/Q/v/w; native natural sleep and passive trace. Old constant-zero step labels resolved by actual ordered enter/exit calls.')
    (OUT/'reset_windows.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps(dict(captures=len(reports),totals=dict(totals),pending=len(pending)),indent=2))
if __name__=='__main__':main()
