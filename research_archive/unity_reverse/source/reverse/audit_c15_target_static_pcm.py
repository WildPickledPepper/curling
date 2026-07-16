"""Compare target-ice PCM geometry against an existing Unity native capture.

This is an offline discriminator. It consumes a historical Unity trace only to
select an already captured target-on-ice call whose transform exactly matches
the C14 target static support state. No Unity process is launched and no scene
state is fed back into the production front-half path.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.reverse.audit_hybrid_p6_endpoint_sixshot import install_pyphysx_extension  # noqa: E402


UNITY = ROOT / "data/calibration/unity_physx_native_solver_state_pcm_20260709_164101.json"
C14 = ROOT / "data/calibration/c14_static_intercall_14000_20260712.json"
EXTENSION = Path(r"D:\esp\tmp\curling_pyphysx_hybrid_build\lib\_pyphysx.cp38-win_amd64.pyd")
OUTPUT = ROOT / "data/calibration/c15_target_static_pcm_14000_20260712.json"


def delta(left: list[float], right: list[float]) -> dict[str, Any]:
    values = [float(a) - float(b) for a, b in zip(left, right)]
    return {"components": values, "maxAbs": max(abs(value) for value in values)}


def exact_target_capture() -> dict[str, Any]:
    c14 = json.loads(C14.read_text(encoding="utf-8"))
    local = next(
        row
        for row in c14["hybrid"]["solveBlockTrace"]
        if row["sequence"] == 18 and row["constraint_type"] == 5 and row["body_a_data_index"] == 1
    )
    p = local["data_a_before"]["body2world"]["p"]
    q = local["data_a_before"]["body2world"]["q"]
    unity = json.loads(UNITY.read_text(encoding="utf-8"))
    for row in unity["pcmContactRows"]:
        if row["hook"] != "PxcPCMContactConvexMesh" or row["phase"] != "after":
            continue
        inputs = row["pcmInputs"]
        transform = inputs["transform0"]
        contacts = inputs["contactBuffer"]["candidate"].get("contactsPreview") or []
        if len(contacts) != 5:
            continue
        if max(abs(a - b) for a, b in zip(transform["p"], p)) != 0.0:
            continue
        if max(abs(a - b) for a, b in zip(transform["q"], q)) != 0.0:
            continue
        return {"unity": row, "c14": local}
    raise RuntimeError("no historical Unity target-ice PCM call matches C14 target transform exactly")


def main() -> int:
    match = exact_target_capture()
    unity_row = match["unity"]
    unity_inputs = unity_row["pcmInputs"]
    unity_contacts = unity_inputs["contactBuffer"]["candidate"]["contactsPreview"]

    install_pyphysx_extension(EXTENSION)
    from unity_front_half_physx import PersistentPhysxFrontHalfScene

    scene = PersistentPhysxFrontHalfScene(
        stone_count=16,
        ice_mesh_mode="unity-source-once",
        ice_use_fast_midphase=True,
        emulate_unity_native_angular_setter_rotation=True,
        emulate_unity_setactive_no_sim=True,
        restore_active_friction_at_pcm_shell=True,
    )
    scene.reset_positions([0.0] * 32, settle_steps=0)
    target = scene.slots[8]
    p = unity_inputs["transform0"]["p"]
    qx, qy, qz, qw = unity_inputs["transform0"]["q"]
    target.body.set_global_pose((p, [qw, qx, qy, qz]))
    target.body.set_linear_velocity([0.0, -0.09809999912977219, 0.0])
    target.body.set_angular_velocity([0.0, 0.0, 0.0])
    ice_shape = scene.ice.get_atached_shapes()[0]
    local = scene.pyphysx.generate_contacts_between(
        target.body,
        target.shape,
        scene.ice,
        ice_shape,
        float(unity_inputs["narrowPhaseParams"]["contactDistance"]),
        float(unity_inputs["narrowPhaseParams"]["meshContactMargin"]),
        float(unity_inputs["narrowPhaseParams"]["toleranceLength"]),
    )
    local_contacts = local["points"]
    rows = []
    for index, (unity_contact, local_contact) in enumerate(zip(unity_contacts, local_contacts)):
        rows.append(
            {
                "index": index,
                "point": delta(local_contact["point"], unity_contact["point"]),
                "normal": delta(local_contact["normal"], unity_contact["normal"]),
                "separation": float(local_contact["separation"]) - float(unity_contact["separation"]),
                "face": [local_contact["internal_face_index1"], unity_contact["internalFaceIndex1"]],
            }
        )
    result = {
        "schema": "c15-target-static-pcm-v1",
        "boundary": "historical Unity target-ice convex-mesh PCM matched exactly to C14 target transform",
        "singleVariable": "local immediate contact generation at the same target/ice transform and narrowphase parameters",
        "scope": "offline diagnostic only; historical Unity capture is not a same-run C11 replacement and cannot authorize a production correction",
        "unityCall": {"callIndex": unity_row["callIndex"], "dumpId": unity_row["dumpId"]},
        "inputTransformExact": True,
        "unityCount": len(unity_contacts),
        "localCount": len(local_contacts),
        "rows": rows,
        "local": local,
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "counts": [len(unity_contacts), len(local_contacts)],
                "maxPoint": max((row["point"]["maxAbs"] for row in rows), default=None),
                "maxNormal": max((row["normal"]["maxAbs"] for row in rows), default=None),
                "maxSeparation": max((abs(row["separation"]) for row in rows), default=None),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
