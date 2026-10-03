import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
inventory=json.loads((ROOT/'analysis_input/local_partial_validation_20261003/inventory.json').read_text())
for r in inventory['capturesInventory']:
    if not r['eventCounts'].get('a0.angular_write.last_pre_pcm'):continue
    print(json.dumps(dict(path=r['path'],commands=r['commands'][:15]),ensure_ascii=False))
    for line in (ROOT/r['path']).open(encoding='utf8'):
        if 'a0.angular_write.last_pre_pcm' not in line:continue
        row=json.loads(line)
        if row['type']!='a0.angular_write.last_pre_pcm':continue
        data=row['data'];data.pop('phaseOrder',None);data.pop('phaseOrderByLastTwoAngularWrites',None)
        if data.get('a2StaticTrace'):data['a2StaticTrace']=data['a2StaticTrace'][:2]
        print(json.dumps(data,ensure_ascii=False));break
    break
