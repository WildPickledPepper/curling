import json
from pathlib import Path
from collections import Counter
from compare_local_motion_windows_20261003 import controls
ROOT=Path(__file__).resolve().parents[1]
i=json.loads((ROOT/'analysis_input/local_partial_validation_20261003/inventory.json').read_text())
c=Counter()
for r in i['capturesInventory']:
    if not any(r['eventCounts'].get(k) for k in ['a0.angular_write.last_pre_pcm','a0.angular_write.before_first_stone_task']):continue
    result=controls(r)
    c['matched' if result else 'unmatched']+=1
    if result is None:print(r['path'],[x['text'] for x in r['commands'][:5]])
print(c)
