import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
inventory=json.loads((ROOT/'analysis_input/local_unity_capture_inventory_20261002.json').read_text(encoding='utf8'))
wanted=['sliding.fixed_update.enter','sliding.fixed_update.exit','a12.dense_pre_angular_setter',
 'a12.dense_post_angular_setter','a12.early_phase_core','a10.release_reset_orientation',
 'scene.reset_body_cores','websocket.recv','c04.dynamic_solver_frame']
for kind in wanted:
    record=next(r for r in inventory['capturesInventory'] if kind in r['eventCounts'])
    for line in (ROOT/record['path']).open(encoding='utf8'):
        r=json.loads(line)
        if r.get('type')==kind:
            print(kind,record['path'])
            print(json.dumps(r,ensure_ascii=False)[:4500]);break
