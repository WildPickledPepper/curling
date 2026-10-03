"""Read actual schemas from previously unhandled local captures."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'analysis_input/local_partial_validation_20261003'
inventory=json.loads((BASE/'inventory.json').read_text())
report=json.loads((BASE/'report.json').read_text())
todo={r['path'] for r in report['coverage'] if not r['passedScopes']}
kinds=['physx.native.before','c04.dynamic_solver_frame','a12.pcm_internal_call',
       'a10.release_reset_orientation','a0.tick.enter','wasm.table.call.after','a9.angular_setter_native_delta']
for kind in kinds:
    match=next(r for r in inventory['capturesInventory'] if r['path'] in todo and kind in r['eventCounts'])
    with (ROOT/match['path']).open(encoding='utf8') as f:
        for line_no,line in enumerate(f,1):
            if kind not in line:continue
            row=json.loads(line)
            if row['type']!=kind:continue
            print(json.dumps(dict(path=match['path'],line=line_no,event=row))[:8000]);break
