"""Inventory archived runtime evidence without treating rounded endpoints as raw state."""
import collections
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TYPE = re.compile(rb'"type"\s*:\s*"([^"\n]+)"')


def main():
    paths = list((ROOT/'analysis_input').glob('unity_*/logs/*/events.jsonl'))
    paths += list((ROOT/'research_archive/unity_reverse/evidence/log').rglob('events.jsonl'))
    result = []
    for path in sorted(paths):
        counts = collections.Counter()
        digest = hashlib.sha256()
        bad = 0
        for line in path.open('rb'):
            digest.update(line)
            m = TYPE.search(line)
            if m:
                counts[m[1].decode()] += 1
            else:
                bad += 1
        selected = {k:v for k,v in counts.items() if any(x in k for x in (
            'dense_', 'tail_phase_core', 'compact_core', 'release_orientation',
            'random_range.friction', 'fixed_update', 'early_phase_core', 'core_truth'))}
        row = dict(path=str(path.relative_to(ROOT)), sizeBytes=path.stat().st_size,
                   sha256=digest.hexdigest(), eventCounts=dict(counts),
                   rawTrajectoryCounts=selected, unparsedTypeLines=bad)
        result.append(row)
        if selected.get('a12.dense_pre_angular_setter', 0) or selected.get('a12.tail_phase_core', 0):
            print(json.dumps(dict(path=row['path'], counts=selected), ensure_ascii=False), flush=True)
    out = ROOT/'analysis_input/local_unity_capture_inventory_20261002.json'
    out.write_text(json.dumps(dict(captures=len(result), capturesInventory=result),
                              indent=2, ensure_ascii=False), encoding='utf8')
    print(json.dumps(dict(captures=len(result), totalBytes=sum(r['sizeBytes'] for r in result),
                         report=str(out)), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
