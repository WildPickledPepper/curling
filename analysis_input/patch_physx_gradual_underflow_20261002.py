"""Replace observed PhysX FPU-guard FTZ/DAZ policy with wasm gradual underflow.

Only decoded immediate writes between stmxcsr/ldmxcsr are changed, 0x9fc0
to 0x1f80. All original instruction bytes and the complete kernel are saved.
The actual step-7 matrix operands reproduce Unity's 0x8001b2e2; native MXCSR
entry sampling observes the conflicting FTZ/DAZ bits. No physical values or
contact data are substituted.
"""
import hashlib
import json
from pathlib import Path
import struct

import capstone
import pefile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'local_simulator/runtime/pyphysx/_pyphysx.cp39-win_amd64.pyd'
BEFORE = '2564abec4fa3f358e67259b105c4b88d49eae28510611c8a0e2f11b7671888df'


def main():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == BEFORE, 'Unexpected kernel version'
    pe = pefile.PE(data=raw)
    decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    decoder.detail = True
    patches = {}
    for section in pe.sections:
        if not section.Characteristics & 0x20000000:
            continue
        data = section.get_data()
        offset = 0
        while True:
            offset = data.find(b'\x0f\xae', offset)
            if offset < 0:
                break
            address = section.VirtualAddress + offset
            instructions = list(decoder.disasm(data[offset:offset+100], address))
            if instructions and instructions[0].mnemonic == 'stmxcsr':
                for instruction in instructions[1:]:
                    if instruction.mnemonic == 'ldmxcsr':
                        break
                    if (instruction.mnemonic == 'mov' and instruction.imm_size == 4
                            and instruction.operands[-1].type == capstone.x86.X86_OP_IMM
                            and instruction.operands[-1].imm == 0x9fc0):
                        immediate_rva = instruction.address + instruction.imm_offset
                        file_offset = pe.get_offset_from_rva(immediate_rva)
                        assert raw[file_offset:file_offset+4] == struct.pack('<I', 0x9fc0)
                        patches[file_offset] = dict(instructionRva=hex(instruction.address),
                            immediateRva=hex(immediate_rva), fileOffset=file_offset,
                            oldInstructionBytes=bytes(instruction.bytes).hex(),
                            mnemonic=instruction.mnemonic, operands=instruction.op_str)
            offset += 2
    assert patches, 'No verified FPU guard instructions found'
    output = bytearray(raw)
    for offset in patches:
        output[offset:offset+4] = struct.pack('<I', 0x1f80)
    backup = ROOT / 'analysis_input/native_kernel_before_gradual_underflow_20261002.pyd'
    assert not backup.exists(), 'Refusing to overwrite the original kernel backup'
    backup.write_bytes(raw)
    after = hashlib.sha256(output).hexdigest()
    report = dict(source=str(SOURCE), originalBackup=str(backup), originalSha256=BEFORE,
                  patchedSha256=after, oldMxcsr=hex(0x9fc0), newMxcsr=hex(0x1f80),
                  patches=list(patches.values()),
                  basis='Actual entry MXCSR plus exact captured matrix operands, step 7 angular X 0x8001b2e2')
    (ROOT / 'analysis_input/native_gradual_underflow_patch_20261002.json').write_text(json.dumps(report, indent=2))
    SOURCE.write_bytes(output)
    print('patched guards', len(patches), 'sha256', after)


if __name__ == '__main__':
    main()
