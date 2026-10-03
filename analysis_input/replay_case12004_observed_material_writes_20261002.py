"""Causal verification only: replay the two observed Unity material writes.

This driver does not modify production or override any body/contact/cache state.
The write ordinal and values come directly from the recorded setter calls.
"""
import json
from pathlib import Path

import sample_new_case_20261002 as replay

BASE = Path(__file__).resolve().parent / 'multi_case_validation_20261002'
CAPTURE = BASE / 'case12004_stop_material_unity'
EVENT = next(CAPTURE.glob('logs/*/events.jsonl'))
WRITES = []
for line in EVENT.open(encoding='utf8'):
    if 'a12.pcm_internal_call' not in line:
        continue
    row = json.loads(line)['data']
    if row['functionIndex'] in (32511, 32512):
        # Ordinal 1 is release; ordinal 3169 is custom update 3168.
        WRITES.append(dict(afterCompletedStep=row['ordinal']-1,
                           functionIndex=row['functionIndex'], value=row['args'][1]))
assert WRITES == [dict(afterCompletedStep=3168,functionIndex=f,value=0.6000000238418579)
                  for f in (32511,32512)]


class ObservedMaterialReplay(replay.PersistentPhysxFrontHalfScene):
    def start_bestshot(self, *args, **kwargs):
        result = super().start_bestshot(*args, **kwargs)
        self._verification_active_index = args[0]
        self._verification_completed_steps = 0
        return result

    def _simulate_unity_step(self):
        if hasattr(self, '_verification_completed_steps'):
            for write in WRITES:
                if write['afterCompletedStep'] == self._verification_completed_steps:
                    material = self.slots[self._verification_active_index].material
                    setter = (material.set_dynamic_friction if write['functionIndex']==32511
                              else material.set_static_friction)
                    setter(write['value'])
            self._verification_completed_steps += 1
        return super()._simulate_unity_step()


if __name__ == '__main__':
    replay.PersistentPhysxFrontHalfScene = ObservedMaterialReplay
    replay.main()
