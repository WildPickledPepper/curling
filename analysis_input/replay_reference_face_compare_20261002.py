"""Replay f70077's observed arithmetic, using captured inputs and helper outputs.

This is a source-operation replay, not another physical/parameter experiment.
The two witness helper inputs must match their real runtime snapshots bitwise.
Execution stops at the observed generatedContacts call.
"""
import hashlib
import json
import re
import struct
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
f=np.float32
calls=json.loads((ROOT/'analysis_input/stone_pair_unity_deep_calls_20261002.json').read_text())
source=ROOT/'analysis_input/pcm_functions_20261001/f70077.wat'
main=next(c for c in calls if c['functionIndex']==70077)
helpers=sorted((c for c in calls if c['parentCallId']==main['callId']),key=lambda c:c['callId'])
assert [c['functionIndex'] for c in helpers]==[70080,70080,70076]
blobs=[(r['ptr'],bytes.fromhex(r['hex'])) for r in main['before']]
clip=helpers[-1]
blobs += [(r['ptr'],bytes.fromhex(r['hex'])) for r in clip['before'] if r['argument'] in (2,3)]
writes={}
def read(address,length):
    for begin,blob in blobs:
        if begin<=address and address+length<=begin+len(blob):
            return bytes(writes.get(address+i,blob[address-begin+i]) for i in range(length))
    if all(address+i in writes for i in range(length)):
        return bytes(writes[address+i] for i in range(length))
    raise KeyError((address,length))
def write(address,value):
    for i,b in enumerate(value): writes[address+i]=b

lines=source.read_text().splitlines()[2:]
lines=[line.strip().removesuffix(')') if line.strip().endswith(')') and not '(;' in line else line.strip() for line in lines]
def parse(index=0):
    nodes=[]
    while index<len(lines):
        line=lines[index]
        if line in ('else','end'): return nodes,index,line
        index+=1
        op=line.split()[0]
        if op in ('block','loop','if'):
            body,index,closing=parse(index)
            alternate=[]
            if closing=='else': alternate,index,closing=parse(index+1)
            assert closing=='end'
            nodes.append((op,line.split()[1],body,alternate))
            index+=1
        else: nodes.append(line)
    return nodes,index,None
nodes,_,_=parse()
locals_={name:0 for name in re.findall(r'\(local (\$\w+)',source.read_text().splitlines()[1])}
locals_.update({'$p'+str(i):v for i,v in enumerate(main['args'])})
globals_={'$g0':500000000}
stack=[]; comparisons=[]; helper_cursor=0
class Branch(Exception): pass
class Finished(Exception): pass
def execute(nodes):
    global helper_cursor
    for node in nodes:
        if isinstance(node,tuple):
            op,label,body,alternate=node
            selected=body if op!='if' or stack.pop() else alternate
            while True:
                try: execute(selected)
                except Branch as b:
                    if b.args[0]!=label: raise
                    if op=='loop': continue
                break
            continue
        words=node.split(); op=words[0]; arg=words[1] if len(words)>1 else None
        if op=='local.get': stack.append(locals_[arg])
        elif op=='local.set': locals_[arg]=stack.pop()
        elif op=='local.tee': locals_[arg]=stack[-1]
        elif op=='global.get': stack.append(globals_[arg])
        elif op=='global.set': globals_[arg]=stack.pop()
        elif op=='drop': stack.pop()
        elif op=='select':
            cond=stack.pop(); b=stack.pop(); a=stack.pop(); stack.append(a if cond else b)
        elif op=='br': raise Branch(arg)
        elif op=='br_if':
            if stack.pop(): raise Branch(arg)
        elif op.endswith('.const'):
            stack.append(f(float.fromhex(arg)) if op.startswith('f32') else int(arg))
        elif '.load' in op or '.store' in op:
            offset=int(next((v.split('=')[1] for v in words[1:] if v.startswith('offset=')),0))
            kind='f' if op.startswith('f32') else 'Q' if op.startswith('i64') else 'I'
            if '8_' in op or op.endswith('store8'): kind='B'
            if '16_' in op or op.endswith('store16'): kind='H'
            length=struct.calcsize('<'+kind)
            if '.load' in op: stack.append(struct.unpack('<'+kind,read(int(stack.pop())+offset,length))[0])
            else:
                value=stack.pop(); address=int(stack.pop())+offset
                if kind!='f': value=int(value)&((1<<(length*8))-1)
                write(address,struct.pack('<'+kind,value))
        elif op=='call':
            observed=helpers[helper_cursor]; helper_cursor+=1
            assert arg=='$f'+str(observed['functionIndex'])
            argc=len(observed['args']); actual=stack[-argc:]; del stack[-argc:]
            if observed['functionIndex']==70080:
                assert actual[:2]==observed['args'][:2] and actual[4]==observed['args'][4]
                for i in (2,3):
                    expected=bytes.fromhex(next(r['hex'] for r in observed['before'] if r['argument']==i))[:12]
                    assert read(actual[i],12)==expected,(i,struct.unpack('<3f',read(actual[i],12)),struct.unpack('<3f',expected))
                stack.append(observed['result'])
            else:
                assert actual[:6]==observed['args'][:6],(actual[:6],observed['args'][:6])
                raise Finished()
        else:
            prefix,action=op.split('.')
            if action in ('neg','abs','sqrt','eqz'):
                a=stack.pop()
                stack.append(f(-a) if action=='neg' else f(abs(a)) if action=='abs' else f(np.sqrt(f(a))) if action=='sqrt' else int(a==0))
                continue
            b=stack.pop(); a=stack.pop()
            if action in ('add','sub','mul','div'):
                a,b=(f(a),f(b)) if prefix=='f32' else (a,b)
                result={'add':lambda:a+b,'sub':lambda:a-b,'mul':lambda:a*b,'div':lambda:a/b}[action]()
                stack.append(f(result) if prefix=='f32' else result)
            elif action in ('lt','le','gt','ge','eq','ne'):
                result={'lt':lambda:a<b,'le':lambda:a<=b,'gt':lambda:a>b,'ge':lambda:a>=b,'eq':lambda:a==b,'ne':lambda:a!=b}[action]()
                if prefix=='f32' and action=='ge': comparisons.append({'lhs':float(a),'rhs':float(b),'taken':bool(result)})
                stack.append(int(result))
            elif action=='and': stack.append(int(a)&int(b))
            else: raise NotImplementedError(node)
try: execute(nodes)
except Finished: pass
assert helper_cursor==3 and len(comparisons)==1
result={'functionIndex':70077,'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),
    'method':'Observed-path source operation replay; original f32 ordering; both witness inputs bit-exact',
    'comparison':comparisons[0],'witnessFaces':[helpers[0]['result'],helpers[1]['result']],
    'generatedContactsReferencePlanePointer':clip['args'][2],'referenceRole':'target'}
(ROOT/'analysis_input/reference_face_compare_replay_20261002.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result))
