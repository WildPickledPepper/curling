from collections import Counter
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'analysis_input/local_partial_validation_20261003'
review=json.loads((OUT/'remaining_capture_payload_review.json').read_text())
inv=json.loads((OUT/'inventory.json').read_text())
paths={r['path'] for r in review['capturesInventory']}
hooks=Counter()
for r in inv['capturesInventory']:
    if r['path'] in paths:hooks.update(r['nativeHooks'])
print('NATIVE_HOOKS',json.dumps(hooks,indent=2))
geom=json.loads((OUT/'geometry_numeric_windows.json').read_text())
for r in geom['capturesInventory']:
    if r['path'] in paths:print('PCM',r['path'],r['actualCapturedFunctionCounts'])
for kind in ('a10.release_reset_orientation','wasm.table.call.after','a0.tick.enter','a0.tick.exit',
    'reset.rotation_restored','game_object.set_active.before','mesh_collider.activation.before'):
    print('SCHEMA',kind)
    r=next((r for r in review['capturesInventory'] if kind in r['actualEventCounts']),None)
    if r:print(json.dumps(r['firstActualPayloadPerType'][kind],indent=2)[:6500])
