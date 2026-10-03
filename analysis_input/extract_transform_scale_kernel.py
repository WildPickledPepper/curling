"""Extract observed Unity Transform functions without changing arithmetic.

Only function call indices are relocated. Hierarchy synchronization helpers
trap: offline inputs must already be synchronized (header bytes zero).
"""
import hashlib
import json
from pathlib import Path

from instrument_pcm_calls import Reader, sections, uleb, sleb
from instrument_geometry_writes import instruction

SOURCE = Path('analysis_input/unity_20260930.wasm')
OUTPUT = Path('analysis_input/unity_transform_scale_kernel_20261001.wasm')
IDS = [78119, 78120, 78121, 79911, 79912]


def main():
    source = SOURCE.read_bytes()
    assert hashlib.sha256(source).hexdigest() == 'cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81'
    sec = dict(sections(source))
    ir = Reader(sec[2]); imports = ir.uint()
    fr = Reader(sec[3]); types = [fr.uint() for _ in range(fr.uint())]
    cr = Reader(sec[10]); bodies = [cr.take(cr.uint()) for _ in range(cr.uint())]
    mapping = {old: new for new, old in enumerate(IDS)}
    new_bodies, records = [], []
    for fid in IDS:
        original = bodies[fid - imports]
        if fid in (79911, 79912):
            body = b'\0\0\x0b'  # unreachable, never silently skip synchronization
        else:
            r = Reader(original)
            for _ in range(r.uint()):
                r.uint(); r.byte()
            out = bytearray(original[:r.pos])
            while r.pos < len(original):
                begin = r.pos
                op, _ = instruction(r)
                if op == 0x10:
                    target = Reader(original[begin + 1:r.pos]).uint()
                    out += b'\x10' + uleb(mapping[target])
                else:
                    out += original[begin:r.pos]
            body = bytes(out)
        new_bodies.append(body)
        records.append({'functionIndex': fid, 'typeIndex': types[fid-imports],
                        'sourceBodySha256': hashlib.sha256(original).hexdigest(),
                        'relocatedBodySha256': hashlib.sha256(body).hexdigest()})
    exports = []
    for name, kind, index in [('memory', 2, 0)] + [('f'+str(fid), 0, mapping[fid]) for fid in IDS[:3]]:
        encoded = name.encode()
        exports.append(uleb(len(encoded)) + encoded + bytes([kind]) + uleb(index))
    payloads = {
        1: sec[1], 3: uleb(len(IDS)) + b''.join(uleb(types[fid-imports]) for fid in IDS),
        5: b'\x01\x00' + uleb(8192),  # 512 MiB, accommodates captured Unity addresses
        6: b'\x01\x7f\x01\x41' + sleb(536800000) + b'\x0b',
        7: uleb(len(exports)) + b''.join(exports),
        10: uleb(len(new_bodies)) + b''.join(uleb(len(b)) + b for b in new_bodies),
    }
    result = source[:8] + b''.join(bytes([kind])+uleb(len(data))+data for kind,data in payloads.items())
    if OUTPUT.exists():
        raise FileExistsError(OUTPUT)
    OUTPUT.write_bytes(result)
    OUTPUT.with_suffix('.json').write_text(json.dumps({
        'sourceSha256': hashlib.sha256(source).hexdigest(),
        'kernelSha256': hashlib.sha256(result).hexdigest(), 'functions': records,
        'method': 'Original numeric instructions; direct calls relocated; synchronization traps.'
    }, indent=2), encoding='utf-8')
    print('extracted',len(result),'bytes')


if __name__ == '__main__':
    main()
