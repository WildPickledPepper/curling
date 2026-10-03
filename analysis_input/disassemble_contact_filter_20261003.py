from pathlib import Path
import re
import pefile
import capstone

p = Path('local_simulator/runtime/pyphysx/_pyphysx.cp39-win_amd64.pyd')
pe = pefile.PE(str(p))
data = pe.get_memory_mapped_image()
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
for s in re.findall(rb'[ -~]{6,}', p.read_bytes()):
    if any(w in s for w in (b'FilterShader', b'contact_report', b'Scene.cpp')):
        print(s.decode(errors='replace'))
for f in pe.DIRECTORY_ENTRY_EXCEPTION:
    a, b = f.struct.BeginAddress, f.struct.EndAddress
    if b-a > 420:
        continue
    ins = list(md.disasm(data[a:b], a))
    # Small filters write a PxPairFlags word, test trigger bit 0x20 and
    # separate static/dynamic attribute classes. This only selects candidates.
    if any(i.mnemonic == 'test' and i.op_str.endswith(', 0x20') for i in ins) and any(
        i.mnemonic == 'mov' and 'word ptr' in i.op_str for i in ins):
        print('\nFUNCTION', hex(a), hex(b))
        for i in ins: print(hex(i.address), i.mnemonic, i.op_str)
