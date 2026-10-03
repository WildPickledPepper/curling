import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
i=json.loads((ROOT/'analysis_input/local_partial_validation_20261003/inventory.json').read_text())
for name in ['unity_transform_scale_calc_trace_20261001','unity_11005_mass_properties_20261002']:
    r=next(r for r in i['capturesInventory'] if name+'\\' in r['path'])
    found=set()
    for line in (ROOT/r['path']).open(encoding='utf8'):
        if 'a12.pcm_internal_call' not in line:continue
        e=json.loads(line)
        if e['type']!='a12.pcm_internal_call':continue
        d=e['data'];n=d['functionIndex']
        if n not in (78119,78121,72778,72776,72779,72777,69768) or n in found:continue
        found.add(n)
        for edge in ('before','after'):
            for w in d.get(edge,[]):w['hex']=w['hex'][:180]
        print(json.dumps(dict(path=r['path'],call=d))[:7000])
        if len(found)>=5:break
