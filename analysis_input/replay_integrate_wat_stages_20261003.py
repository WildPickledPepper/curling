"""Execute the original integrateCore WAT and passively record f32 results."""
import json
from pathlib import Path
import re
import struct

import wasmtime

BASE=Path(__file__).resolve().parent


def bits(value):return struct.unpack('<I',struct.pack('<f',value))[0]


def replay(body_data,solver_body,motion_body,sin_value,cos_value,dt):
    source=(BASE/'pcm_functions_20261001/f71198.wat').read_text()
    plain=re.sub(r'\(type \$t\d+\)','',source,count=1)
    lines=plain.splitlines()
    augmented=[];stages=[]
    for number,line in enumerate(lines,1):
        augmented.append(line)
        if number==2:augmented.append('    (local $probe f32)')
        if re.match(r'\s*(f32\.(add|sub|mul|div|sqrt)|call \$f(18890|33062))\s*$',line):
            offset=16384+4*len(stages)
            stages.append(dict(originalWatLine=number,instruction=line.strip(),offset=offset))
            augmented.extend(['    local.tee $probe',f'    i32.const {offset}',
                              '    local.get $probe','    f32.store'])
    imports='(import "trig" "sin" (func $f18890 (param f32) (result f32))) (import "trig" "cos" (func $f33062 (param f32) (result f32)))'
    calls=[]
    def run(body):
        kernel=wasmtime.wat2wasm('(module '+imports+' (memory (export "memory") 2) '+body+' (export "integrate" (func $f71198)))')
        engine=wasmtime.Engine();store=wasmtime.Store(engine)
        def trig(name,value):
            def call(angle):calls.append(dict(name=name,inputBits=bits(angle),resultBits=bits(value)));return value
            return wasmtime.Func(store,wasmtime.FuncType([wasmtime.ValType.f32()],[wasmtime.ValType.f32()]),call)
        instance=wasmtime.Instance(store,wasmtime.Module(engine,kernel),[trig('sin',sin_value),trig('cos',cos_value)])
        memory=instance.exports(store)['memory']
        memory.write(store,solver_body,64);memory.write(store,motion_body,256);memory.write(store,body_data,1024)
        instance.exports(store)['integrate'](store,64,80,256,1024,dt)
        output=bytes(memory.read(store,1024,1136))
        trace=list(struct.unpack('<%dI'%len(stages),bytes(memory.read(store,16384,16384+4*len(stages)))))
        return output,trace,kernel
    original,_,original_kernel=run(plain)
    calls.clear()
    observed,trace,trace_kernel=run('\n'.join(augmented))
    assert observed==original,'Stage recording changed the original WAT calculation'
    return dict(outputHex=original.hex(),stages=[dict(row,resultBits=f'0x{word:08x}') for row,word in zip(stages,trace)],
                trigCalls=calls,originalBodyOutputUnchanged=True),original_kernel,trace_kernel


def main():
    path=BASE/'case12009_step313_native_registers_v2_20261003/calls.json'
    rows=json.loads(path.read_text())['calls']
    by={r['functionRva']:r for r in rows}
    def xmm(rva,n):return struct.unpack_from('<f',bytes.fromhex(by[rva]['xmmHex']),n*16)[0]
    first=by['0x2049c7']
    result,plain,traced=replay(bytes.fromhex(first['bodyDataHex']),bytes.fromhex(first['solverBodyHex']),
        bytes.fromhex(first['motionBodyHex']),xmm('0x204ccc',0),xmm('0x204d1b',0),xmm('0x2049c7',15))
    for label,kernel in [('original',plain),('traced',traced)]:
        (BASE/f'case12009_integrate_{label}_kernel_20261003.wasm').write_bytes(kernel)
    result['scope']='Original WAT with observed native input bytes and observed native sin/cos results. Compare to Unity runtime inputs before using this as a causal conclusion.'
    result['nativeFinalBodyDataHex']=by['0x204e02']['bodyDataHex']
    result['nativeTrigBits']=dict(sin=f"0x{bits(xmm('0x204ccc',0)):08x}",cos=f"0x{bits(xmm('0x204d1b',0)):08x}")
    (BASE/'case12009_integrate_wat_with_native_trig_20261003.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    print('WAT output Q', [hex(x) for x in struct.unpack_from('<4I',bytes.fromhex(result['outputHex']),80)])
    print('native final Q',[hex(x) for x in struct.unpack_from('<4I',bytes.fromhex(by['0x204e02']['bodyDataHex']),80)])
    print('trig',result['trigCalls'])


if __name__=='__main__':main()
