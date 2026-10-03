"""Compare the production native cosine to the original Unity WAT arithmetic."""
import ctypes
import hashlib
import json
from pathlib import Path
import random
import re
import struct
import wasmtime
import validate_multiple_cases_20261002 as validation
from verify_pcm_internal_trace import raw_argument

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'analysis_input'

def bits(x): return struct.unpack('<I', struct.pack('<f', x))[0]
def value(x): return struct.unpack('<f', struct.pack('<I', x))[0]
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    # The unreachable large reducer makes domain overruns fail, not fabricate
    # an expected result. All original calculation bodies remain verbatim.
    files = [BASE/f'pcm_functions_20261001/f{n}.wat' for n in (33062,18889,18888,18176)]
    bodies = [re.sub(r'\(type \$t\d+\)', '', p.read_text(), count=1) for p in files]
    wat = ('(module (memory 2) (global $g0 (mut i32) (i32.const 65536)) '
        '(func $f5976 (param i32 i32 i32 i32 i32) (result i32) unreachable) '
        + '\n'.join(bodies) + '(export "cos" (func $f33062)))')
    kernel = wasmtime.wat2wasm(wat)
    (BASE/'case12009_cos_repair_reference_20261003.wasm').write_bytes(kernel)
    engine=wasmtime.Engine();store=wasmtime.Store(engine)
    reference=wasmtime.Instance(store,wasmtime.Module(engine,kernel),[]).exports(store)['cos']
    dll_path=ROOT/'local_simulator/runtime/unity_integrate_cos.dll'
    dll=ctypes.CDLL(str(dll_path));native=dll.unity_integrate_cosf
    native.argtypes=[ctypes.c_float];native.restype=ctypes.c_float
    inputs={0,0x80000000,0x3bd59dea}
    for edge in (964689920,1061752794,1075235812,1081824209,1085271520,1088565717,1305022426):
        inputs.update((word|sign) for word in range(edge-8,edge+9) for sign in (0,0x80000000))
    rng=random.Random(1200920261003)
    inputs.update(bits(rng.uniform(-50000,50000)) for _ in range(50000))
    inputs.update(rng.randrange(1305022427)|rng.choice((0,0x80000000)) for _ in range(50000))
    inputs={word for word in inputs if (word&0x7fffffff)<=1305022426}
    for word in sorted(inputs):
        x=value(word);a=bits(reference(store,x));b=bits(native(x))
        assert a==b,(hex(word),hex(a),hex(b))
    assert bits(native(value(0x3bd59dea)))==0x3f7ffe9c
    trace_dir=BASE/'case12009_cos_fixed_registers_20261003'
    observed=json.loads((trace_dir/'calls.json').read_text())
    assert len(observed['calls'])==13 and not observed['dropped'] and not observed['unfinished']
    by={r['functionRva']:r for r in observed['calls']}
    assert struct.unpack_from('<I',bytes.fromhex(by['0x204d1b']['xmmHex']))[0]==0x3f7ffe9c
    unity_events=validation.event_path(BASE/'case12009_step313_unity_integrate_20261003')
    integral=next(r for r in validation.rows(unity_events,'a12.pcm_internal_call') if r['callId']==87)
    assert integral['functionIndex']==71198 and integral['ordinal']==314
    a=raw_argument(integral,3,'after')[:112]
    b=bytes.fromhex(by['0x204e02']['bodyDataHex'])
    assert a[:72]+a[76:]==b[:72]+b[76:]
    plain=json.loads((BASE/'cos_repair_regression_20261003/additional12009_native.json').read_text())
    traced=json.loads((trace_dir/'alignment.json').read_text())
    assert traced['states']==plain['states'][:3000] and traced['releaseBits']==plain['releaseBits']
    report=dict(comparedFiniteInputs=len(inputs),allResultsBitIdentical=True,
        failingAngleBits='0x3bd59dea',repairedCosBits='0x3f7ffe9c',
        repairedNativeReturnObserved=True,integrateOutputBytesExactExcludingRosterInteger=108,
        passiveRegisterSnapshots=13,observerCompletedStatesUnchanged=3000,
        scope='Verbatim Unity WAT moderate reduction; samples across all branches, signs and integration domain. Large finite f5976 is outside the integration contract.',
        evidence={str(p.relative_to(ROOT)):digest(p) for p in files+[dll_path,
            ROOT/'local_simulator/runtime/unity_integrate_cos.c',Path(__file__),
            trace_dir/'calls.json',trace_dir/'alignment.json',unity_events]})
    (BASE/'case12009_cos_arithmetic_verified_20261003.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report))

if __name__=='__main__':main()
