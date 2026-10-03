from collections import Counter
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'analysis_input/local_partial_validation_20261003'
report=json.loads((OUT/'report.json').read_text());inv=json.loads((OUT/'inventory.json').read_text());review=json.loads((OUT/'remaining_capture_payload_review.json').read_text())
done={r['path'] for r in report['coverage'] if r['passedScopes']}
for fn in ('startup_windows.json','reset_position_inputs.json'):
    done.update(r['path'] for r in json.loads((OUT/fn).read_text())['capturesInventory'] if r['checks']['compared'])
paths={r['path'] for r in inv['capturesInventory']} - done
by_path={r['path']:r for r in review['capturesInventory']}
for r in inv['capturesInventory']:
    if r['path'] not in paths:continue
    out=dict(path=r['path'],size=r['sizeBytes'],commands=[c['text'] for c in r['commands']],
        nativeHooks=r['nativeHooks'],eventCounts=r['eventCounts'])
    print(json.dumps(out))
print('TABLE_SCHEMA')
for r in inv['capturesInventory']:
    if r['path'] not in paths or not r['eventCounts'].get('wasm.table.call.after'):continue
    kinds=Counter();examples={}
    for n,line in enumerate((ROOT/r['path']).open('rb'),1):
        if b'wasm.table.call' not in line:continue
        e=json.loads(line)
        if not e['type'].startswith('wasm.table.call'):continue
        d=e['data'];kind=d.get('name','?');kinds[(e['type'],kind)]+=1
        if kind not in examples:examples[kind]=dict(line=n,data={k:v for k,v in d.items() if 'window' not in k.lower()})
    print(json.dumps(dict(path=r['path'],counts={str(k):v for k,v in kinds.items()},examples=examples))[:12000])
