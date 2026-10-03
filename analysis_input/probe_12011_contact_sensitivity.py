"""Replay 12011 with tiny, explicit pose perturbations in the archived audit.

Each case runs the full 12-shot persistent scene with the same Unity friction
stream. Only the final shot changes. Outputs are diagnostic, not fitted physics.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.runtime_loader import install_bundled_pyphysx

install_bundled_pyphysx()
import local_simulator.unity_physx as up

ARCHIVE = ROOT / "research_archive/unity_reverse"
SOURCE = ARCHIVE / "source/reverse/audit_hybrid_p6_endpoint_sixshot.py"
DATA = ARCHIVE / "evidence/data/calibration/extended_collision_validation_20260715_ordered"
EVENTS = ARCHIVE / "evidence/log/extended_collision_validation_20260715_ordered/collision_unique_targets_batch_r03/unity_runtime_probe_20260715_125420/events.jsonl"
REPORT_DIR = ROOT / "analysis_input"

# Unity A10 native bridge quaternion at the start of shot 12011: x,y,z,w.
A10_QUAT_XYZW = [-2.4462851300199873e-08, 0.9300537109375, 6.192122015136192e-08, -0.3674236834049225]


def run_case(name: str, target_dx: float = 0.0, target_dy: float = 0.0,
             active_dx: float = 0.0, active_dy: float = 0.0,
             exact_a10_quat: bool = False, exact_a10_all: bool = False) -> dict:
    original_reset = up.PersistentPhysxFrontHalfScene.reset_positions
    original_start = up.PersistentPhysxFrontHalfScene.start_bestshot
    manifest = json.loads((DATA / "collision_unique_targets_batch_r03_orientation.json").read_text(encoding="utf-8"))
    shot_ordinal = 0

    def reset(self, positions, *args, **kwargs):
        values = list(positions)
        if values[26] != 0.0 or values[27] != 0.0:
            values[26] += target_dx
            values[27] += target_dy
        return original_reset(self, values, *args, **kwargs)

    def start(self, active_index, shot, *args, **kwargs):
        nonlocal shot_ordinal
        result = original_start(self, active_index, shot, *args, **kwargs)
        if exact_a10_all:
            sample_id = str(12000 + shot_ordinal)
            x, y, z, w = manifest["samples"][sample_id]["a10"]["nativeQuaternion"]
            state = self.state(active_index)
            self.slots[active_index].body.set_global_pose(
                (self._horizontal_position(state["x"], state["y"]), [w, x, y, z])
            )
        shot_ordinal += 1
        if active_index == 1 and self.slots[13].enabled:
            state = self.state(active_index)
            if exact_a10_quat:
                x, y, z, w = A10_QUAT_XYZW
                self.slots[active_index].body.set_global_pose(
                    (self._horizontal_position(state["x"], state["y"]), [w, x, y, z])
                )
            if active_dx or active_dy:
                self._set_position_preserve_orientation(
                    active_index, state["x"] + active_dx, state["y"] + active_dy
                )
        return result

    up.PersistentPhysxFrontHalfScene.reset_positions = reset
    up.PersistentPhysxFrontHalfScene.start_bestshot = start
    output = REPORT_DIR / f"simulator_alignment_12011_sensitivity_{name}.json"
    if output.exists():
        raise FileExistsError(output)

    code = SOURCE.read_text(encoding="utf-8")
    start_offset = code.index("    if sys.version_info[:2] != (3, 8)")
    end_offset = code.index("    samples = _load_jsonl", start_offset)
    code = code[:start_offset] + (
        "    from tools.reverse.front_half_pcm_replay import event_shot_groups, load_jsonl\n"
        "    from local_simulator.unity_physx import NativePyphysxMotionStepper, PersistentPhysxFrontHalfScene\n"
    ) + code[end_offset:]
    namespace = {"__name__": "sensitivity_audit", "__file__": str(SOURCE)}
    try:
        exec(compile(code, str(SOURCE), "exec"), namespace)
        sys.argv = [str(SOURCE), "--samples", str(DATA / "collision_unique_targets_batch_r03.jsonl"),
                    "--events", str(EVENTS), "--orientation-manifest",
                    str(DATA / "collision_unique_targets_batch_r03_orientation.json"),
                    "--require-orientation-truth", "--motion-kernel", "native-pyphysx",
                    "--output", str(output)]
        namespace["main"]()
    finally:
        up.PersistentPhysxFrontHalfScene.reset_positions = original_reset
        up.PersistentPhysxFrontHalfScene.start_bestshot = original_start

    report = json.loads(output.read_text(encoding="utf-8"))
    row = next(item for item in report["rows"] if item["sampleId"] == 12011)
    result = {"case": name, "firstContactStep": row["firstContactStep"],
              "contactCounts": row["firstContactCounts"],
              "activeErrorMm": 1000 * row["endpointErrorM"]["active"],
              "targetErrorMm": 1000 * row["endpointErrorM"]["target"],
              "activeEndpoint": row["localEndpoint"]["active"],
              "targetEndpoint": row["localEndpoint"]["target"]}
    print("CASE", json.dumps(result, ensure_ascii=False), flush=True)
    return result


def main() -> None:
    cases = [
        ("target_x_plus_0p1mm", {"target_dx": 0.0001}),
        ("target_x_minus_0p1mm", {"target_dx": -0.0001}),
        ("target_y_plus_0p1mm", {"target_dy": 0.0001}),
        ("target_y_minus_0p1mm", {"target_dy": -0.0001}),
        ("active_x_plus_0p1mm", {"active_dx": 0.0001}),
        ("active_x_minus_0p1mm", {"active_dx": -0.0001}),
        ("exact_a10_quaternion", {"exact_a10_quat": True}),
        ("exact_a10_all", {"exact_a10_all": True}),
    ]
    for name, options in cases:
        run_case(name, **options)


if __name__ == "__main__":
    main()
