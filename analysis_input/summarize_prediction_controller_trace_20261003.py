"""Retain observed controller gates with exact event line numbers."""
import hashlib,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'analysis_input/prediction_schedule_unity_v4_20261003/logs/unity_runtime_probe_20261003_201831/events.jsonl'
counts=Counter();updates=[];scales=[]
for n,line in enumerate(p.open(encoding='utf8'),1):
    e=json.loads(line);counts[e['type']]+=1;d=e.get('data',{})
    if e['type']=='controller.update.direct' and d['controllerRaw'][105]:
        updates.append(dict(line=n,t=e['t'],edge=d['edge'],fixedCount=d['fixedCount'],
                            frictionCount=d['earlyFrictionCount'],shotInProgress=d['controllerRaw'][236],
                            controllerPtr=d['controllerPtr']))
    if e['type']=='controller.time_scale.direct':scales.append(dict(line=n,t=e['t'],**d))
r=dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
       timeScaleCalls=scales,activeControllerUpdates=updates,eventCounts=counts,
       sourceManifest='analysis_input/prediction_schedule_unity_v4_20261003/observer_manifest.json',
       timingPassivityVerified=False)
(ROOT/'analysis_input/prediction_controller_trace_20261003.json').write_text(json.dumps(r,indent=2))
print(json.dumps(dict(updates=updates,timeScaleCalls=scales)))
