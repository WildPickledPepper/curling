"""Protocol Reset inputs to sampled Unity Transform position setter arguments."""
from collections import Counter
import ast,hashlib,json,struct,sys
from pathlib import Path
from types import SimpleNamespace,MethodType
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'analysis_input/local_partial_validation_20261003'
sys.path.insert(0,str(ROOT))
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene as Scene
PROBE_SOURCE=ROOT/'local_simulator/runtime_support/tools/reverse/probe_physx_collision_alignment.py'
HEIGHT=next(ast.literal_eval(n.value) for n in ast.parse(PROBE_SOURCE.read_text(encoding='utf8')).body
    if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='HEIGHT' for t in n.targets))
def bits(v):return list(struct.unpack('<%dI'%len(v),struct.pack('<%df'%len(v),*v)))
def local_inputs(position):
    writes={}
    # Retain the actual production Reset branch and coordinate arithmetic.
    # Observe downstream pose input only; no scene history/physics is replayed.
    model=SimpleNamespace(slots=list(range(16)),coordinate_mode='unity-native-yup',emulate_unity_setactive_no_sim=True,center_height=HEIGHT/2.)
    model._horizontal_position=MethodType(Scene._horizontal_position,model)
    def record(index,*args,native_position_override=None):writes[index]=bits(native_position_override)
    model.activate_stationary=record;model.deactivate=record
    Scene.reset_positions(model,position,settle_steps=0,force_sleep_after_reset=False)
    return writes
def main():
    inventory=json.loads((OUT/'inventory.json').read_text());reports=[];totals=Counter()
    for r in inventory['capturesInventory']:
        if not r['eventCounts'].get('a10.release_reset_orientation'):continue
        checks=[];excluded=Counter();seen=set();h=hashlib.sha256()
        for n,line in enumerate((ROOT/r['path']).open('rb'),1):
            h.update(line)
            if b'a10.release_reset_orientation' not in line:continue
            e=json.loads(line)
            if e['type']!='a10.release_reset_orientation':continue
            reset=(e['data'].get('release') or {}).get('reset')
            if not reset or not reset.get('text') or not reset.get('positionWrites'):
                excluded['missingActualResetCommandOrWrites']+=1;continue
            reset_key=(reset['serial'],reset.get('receivedAtMs'),reset['text'])
            if reset_key in seen:continue
            seen.add(reset_key)
            position=list(map(float,reset['text'].split()[1:]))
            if len(position)!=32:excluded['unsupportedProtocolLength']+=1;continue
            writes=reset['positionWrites'][:16]
            if len(writes)!=16 or [w['writeOrdinal'] for w in writes]!=list(range(16)) or len({w['transformManagedPtr'] for w in writes})!=16:
                excluded['unresolvedStoneWriteMapping']+=1;continue
            actual=local_inputs(position)
            for w in writes:
                if w.get('sourceVector') is None:excluded['missingActualSourceVector']+=1;continue
                index=w['writeOrdinal'];expected=bits(w['sourceVector'])
                checks.append(dict(line=n,resetSerial=reset['serial'],stoneIndex=index,localBits=actual[index],unityBits=expected,
                    exact=actual[index]==expected,protocolPosition=position[index*2:index*2+2]))
        assert h.hexdigest()==r['sha256']
        counts=dict(compared=len(checks),exact=sum(c['exact'] for c in checks),different=sum(not c['exact'] for c in checks))
        totals.update(counts);reports.append(dict(path=r['path'],unityEventsSha256=r['sha256'],checks=counts,
            comparedWindows=checks,excluded=dict(excluded),firstDifference=next((c for c in checks if not c['exact']),None)))
    result=dict(captures=len(reports),capturesWithComparedInputs=sum(bool(r['checks']['compared']) for r in reports),
        capturesWithDifferences=sum(bool(r['checks']['different']) for r in reports),totals=dict(totals),capturesInventory=reports,
        sourceSha256=hashlib.sha256((ROOT/'local_simulator/unity_physx.py').read_bytes()).hexdigest(),
        scope='Protocol -> actual production Reset placement branch -> sampled Unity Transform position setter input, three f32 words. This excludes setter internals, rotations, integration and previous scene history.',
        evidence='Original f61066; probe f32531 Reset initial positionWrites hooks; verified 16-stone first-write mapping.')
    (OUT/'reset_position_inputs.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in result.items() if k!='capturesInventory'},indent=2))
if __name__=='__main__':main()
