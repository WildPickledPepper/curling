"""Locate the observed shape-interaction sorting body in the pinned PE."""
import json
from pathlib import Path
import pefile
import capstone

root=Path(__file__).resolve().parents[1]
d=json.loads((root/'analysis_input/native_stone_scene_kernel_discovery_20261002/calls.json').read_text())
pe=pefile.PE(d['request']['module'])
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
rows=[]
for rva in sorted({int(c['functionRva'],16) for c in d['calls'] if c.get('functionRva')}):
    ops=list(md.disasm(pe.get_data(rva,1200),rva))
    lines=[f'{i.address:#x} {i.mnemonic} {i.op_str}' for i in ops]
    if any(i.mnemonic=='cmp' and '+ 0x58]' in i.op_str for i in ops):
        rows.append({'rva':hex(rva),'disassembly':lines})
        print(hex(rva),'\n'+'\n'.join(lines[:75]))
(root/'analysis_input/native_pair_sort_candidates_20261002.json').write_text(json.dumps(rows,indent=2))
