"""Actual captured hierarchy/mass calls against current production arithmetic."""
from collections import Counter,defaultdict
import hashlib,json,struct,subprocess,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'analysis_input/local_partial_validation_20261003'
sys.path.insert(0,str(ROOT))
import local_simulator.unity_physx
from tools.reverse.recovered_transform_scale import recovered_stone_world_matrix,recovered_stone_scale_matrix
from tools.reverse.recovered_stone_mass import recovered_stone_inertia
def raw(row,edge,arg):return bytes.fromhex(next(w['hex'] for w in row[edge] if w['argument']==arg))
def bits(v):return np.asarray(v,dtype=np.float32).view(np.uint32).tolist()
def main():
    inventory=json.loads((OUT/'inventory.json').read_text())
    fixture=json.loads((ROOT/'local_simulator/tests/fixtures/unity_stone_mass_20261002.json').read_text())
    mass_info=fixture['massInformation']
    reports=[];totals=Counter()
    for r in inventory['capturesInventory']:
        if not r['eventCounts'].get('a12.pcm_internal_call'):continue
        calls=[];counts=Counter();digest=hashlib.sha256()
        for n,line in enumerate((ROOT/r['path']).open('rb'),1):
            digest.update(line)
            if b'a12.pcm_internal_call' not in line:continue
            event=json.loads(line)
            if event['type']!='a12.pcm_internal_call':continue
            row=event['data'];counts[row['functionIndex']]+=1
            if row['functionIndex'] in (78119,78120,78121,72776,72778,72779,72777,69768):
                row['_line']=n;calls.append(row)
        assert digest.hexdigest()==r['sha256']
        by_id={c['callId']:c for c in calls};children=defaultdict(list)
        for c in calls:children[c['parentCallId']].append(c)
        compared=[];pending=[]
        for c in calls:
            fn=c['functionIndex']
            if fn in (78119,78120,78121):
                chain=(c.get('transformHierarchy') or {}).get('chain')
                if not chain or len(chain)!=2 or chain[1]['parent']!=-1 or chain[1]['values'][3:7]!=[0,0,0,1]:
                    pending.append(dict(line=c['_line'],callId=c['callId'],functionIndex=fn,reason='Missing captured supported two-node hierarchy.'));continue
                local,parent=chain[0]['values'],chain[1]['values']
                method=recovered_stone_world_matrix if fn==78121 else recovered_stone_scale_matrix
                actual=bits(method(local[3:7],local[7:10],parent[7:10]))
                try:expected=list(struct.unpack_from('<9I',raw(c,'after',0)))
                except (KeyError,StopIteration,struct.error):
                    pending.append(dict(line=c['_line'],callId=c['callId'],functionIndex=fn,reason='Missing nine-word captured matrix output.'));continue
                compared.append(dict(scope='Transform matrix arithmetic',line=c['_line'],callId=c['callId'],functionIndex=fn,
                    localBits=actual,unityBits=expected,exact=actual==expected,measuredHierarchy=chain))
            elif fn==72776:
                scales=sorted((s for s in children[c['callId']] if s['functionIndex']==72779),key=lambda s:s['callId'])
                outer=by_id.get(c['parentCallId'])
                finals=[s for s in children[c['parentCallId']] if s['functionIndex']==72777]
                reason=None
                if len(scales)!=2 or not outer or outer['functionIndex']!=72778 or len(finals)!=1:
                    reason='Missing captured parent mass and two scale calls / final inertia output.'
                else:
                    try:
                        source=raw(scales[0],'before',1)
                        inertia=list(struct.unpack_from('<9f',source));scaled_mass=struct.unpack_from('<f',source,36)[0]
                        scale=list(struct.unpack_from('<3f',source,44));rotation=list(struct.unpack_from('<4f',source,56))
                        diagonal=[s for s in children[finals[0]['callId']] if s['functionIndex']==69768]
                        volume=(np.float32(scale[0])*np.float32(scale[1]))*np.float32(scale[2])
                        if rotation!=[0,0,0,1] or len(diagonal)!=1 or raw(diagonal[0],'after',2)[:16]!=struct.pack('<4f',0,0,0,1):
                            reason='Scale/inertia rotation outside directly observed production identity path.'
                        elif bits(inertia[::4])!=bits([mass_info['local_inertia_rows'][i][i] for i in range(3)]) or bits([np.float32(mass_info['unit_density_mass'])*volume])!=bits([scaled_mass]):
                            reason='Captured mass inputs are not the formal production stone hull.'
                        elif raw(finals[0],'before',4)[:12]!=struct.pack('<3f',0,0,0):
                            reason='Captured COM shift input is not the supported zero COM.'
                        else:
                            actual=bits(recovered_stone_inertia(mass_info,scale,outer['args'][1]))
                            expected=list(struct.unpack_from('<3I',raw(finals[0],'after',1)))
                            compared.append(dict(scope='Stone inertia arithmetic',line=c['_line'],callId=c['callId'],functionIndex=fn,
                                outputLine=finals[0]['_line'],localBits=actual,unityBits=expected,exact=actual==expected,
                                measuredScale=scale,measuredRequestedMass=outer['args'][1]))
                    except (KeyError,StopIteration,struct.error):reason='Incomplete captured mass input/output buffers.'
                if reason:pending.append(dict(line=c['_line'],callId=c['callId'],functionIndex=fn,reason=reason))
        check=dict(compared=len(compared),exact=sum(c['exact'] for c in compared),different=sum(not c['exact'] for c in compared))
        totals.update(check)
        reports.append(dict(path=r['path'],unityEventsSha256=r['sha256'],checks=check,comparedWindows=compared,
            unsupportedNumericWindows=pending,actualCapturedFunctionCounts=dict(counts),
            firstDifference=next((c for c in compared if not c['exact']),None)))
    result=dict(captures=len(reports),totals=dict(totals),capturesWithComparedCalls=sum(bool(r['checks']['compared']) for r in reports),
        capturesWithDifferences=sum(bool(r['checks']['different']) for r in reports),capturesInventory=reports,
        scope='Actual measured function inputs to production matrix/inertia output only; no scene history or capture passivity assertion.',
        massInputFixtureSha256=hashlib.sha256((ROOT/'local_simulator/tests/fixtures/unity_stone_mass_20261002.json').read_bytes()).hexdigest())
    (OUT/'geometry_numeric_windows.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in result.items() if k!='capturesInventory'},indent=2))
if __name__=='__main__':main()
