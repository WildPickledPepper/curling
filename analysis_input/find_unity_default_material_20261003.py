from pathlib import Path
import re
root=Path(__file__).resolve().parent
current=[]
def inspect():
    if not current: return
    body=''.join(current)
    if 'f32.const 0x1.333334p-1' in body:
        print(current[0].strip(), 'lines', len(current))
        number = int(re.search(r'\$f(\d+)',current[0])[1])
        if 70000 <= number <= 83000:
            path=root/'pcm_functions_20261001'/f'f{number}.wat'
            path.write_text(body)
for line in (root/'unity_20260930.wat').open():
    if line.startswith('  (func $f'):
        inspect();current=[]
    current.append(line)
inspect()
