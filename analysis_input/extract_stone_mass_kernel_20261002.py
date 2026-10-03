"""Extract the original convex-scale instruction segment and numeric helpers.

The wrapper supplies the three live pointer locals at the segment entrance;
the original instruction order, constants and helper bodies are unchanged.
wasmtime is a research compiler dependency, never a simulator dependency.
"""
import hashlib
import json
import re
from pathlib import Path

import wasmtime
from instrument_pcm_calls import Reader, sections

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'analysis_input/unity_20260930.wasm'
FUNCTIONS = ROOT / 'analysis_input/pcm_functions_20261001'
OUTPUT = ROOT / 'analysis_input/unity_mass_numeric_kernel_20261002.wasm'


def main():
    source = SOURCE.read_bytes()
    source_hash = hashlib.sha256(source).hexdigest()
    assert source_hash == 'cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81'
    text = (FUNCTIONS / 'f72776.wat').read_text()
    start = text.index('                  global.get $g0\n                  i32.const 96\n                  i32.sub')
    end = text.index('                  local.get $l4\n                  local.get $l4\n                  f32.load offset=264', start)
    segment = text[start:end]
    locals_ = re.sub(r'\(local \$(l4|l8|l9) i32\)', '', text.splitlines()[1])
    helpers = '\n'.join(re.sub(r'\(type \$t\d+\)', '',
        (FUNCTIONS / f'f{n}.wat').read_text(), count=1) for n in (72779, 69768, 72775))
    wat = ('(module (memory (export "memory") 8) '
           '(global $g0 (mut i32) (i32.const 500000)) ' + helpers +
           ' (export "diagonalize" (func $f69768)) '
           ' (func (export "scale") (param $l4 i32) (param $l8 i32) (param $l9 i32) ' +
           locals_ + ' ' + segment + '))')
    result = wasmtime.wat2wasm(wat)
    OUTPUT.write_bytes(result)
    OUTPUT.with_suffix('.wat').write_text(wat)
    sec = dict(sections(source))
    reader = Reader(sec[10])
    bodies = [reader.take(reader.uint()) for _ in range(reader.uint())]
    OUTPUT.with_suffix('.json').write_text(json.dumps({
        'source': str(SOURCE), 'sourceSha256': source_hash,
        'kernelSha256': hashlib.sha256(result).hexdigest(),
        'sourceFunctionBodySha256': {str(n): hashlib.sha256(bodies[n-476]).hexdigest()
                                    for n in (72776, 72779, 69768, 72775)},
        'numericSegmentWatSha256': hashlib.sha256(segment.encode()).hexdigest(),
        'wrapperInputs': {'l4': 'original stack frame with inertia at +48',
                          'l8': 'convex scale xyz', 'l9': 'scale rotation xyzw'},
        'sourceLines': {'functionIndex': 72776,
                        'start': text[:start].count('\n')+1,
                        'endExclusive': text[:end].count('\n')+1},
        'method': 'Verbatim numeric WAT segment and helpers; new pointer wrapper and exports.'
    }, indent=2), encoding='utf-8')
    print('extracted', len(result), 'bytes')


if __name__ == '__main__':
    main()
