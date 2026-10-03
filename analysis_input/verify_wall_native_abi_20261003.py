"""Verify all three known Windows ABI entry points against actual binaries."""
import ast
import hashlib
import json
from pathlib import Path

import pefile

ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'local_simulator/native_wall_contact.py'
module=ast.parse(source.read_text())
versions=next(ast.literal_eval(n.value) for n in module.body if isinstance(n,ast.Assign)
              and any(isinstance(t,ast.Name) and t.id=='_KERNELS' for t in n.targets))
files=list((ROOT/'local_simulator/runtime/pyphysx').glob('*.pyd'))
images={hashlib.sha256(p.read_bytes()).hexdigest():pefile.PE(str(p)) for p in files}
expected=bytes.fromhex('80e30f80fb01752a4080e50f403aeb7521b81c020000660906')
states=[]
for digest,(site,get_shapes,set_filter) in versions.items():
    pe=images[digest]
    assert pe.get_data(site,len(expected))==expected
    shape_stub=pe.get_data(get_shapes,9)
    setter=pe.get_data(set_filter,0xc0)
    getter=pe.get_data(set_filter+0x100,0x2e)
    states.append((shape_stub,setter,getter))
assert all(s==states[0] for s in states)
out=dict(versions=[dict(kernelSha256=d,filterSiteRva=hex(s),getShapesRva=hex(g),
    setSimulationFilterDataRva=hex(f),getSimulationFilterDataRva=hex(f+0x100))
    for d,(s,g,f) in versions.items()],
    originalFilterInstructionsExactAcrossABIs=True,
    nativeShapeAccessorAndSetterBodiesExactAcrossABIs=True,
    shapeAccessBodiesSha256=[hashlib.sha256(b).hexdigest() for b in states[0]],
    runtimeExecutedABI='Windows CPython3.9; CP38/CP313 inspected, not executed.',
    bridgeSha256=hashlib.sha256(source.read_bytes()).hexdigest())
(ROOT/'analysis_input/wall_native_abi_verified_20261003.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
