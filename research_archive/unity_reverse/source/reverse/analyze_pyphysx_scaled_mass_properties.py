#!/usr/bin/env python3
"""Compute Unity-scale PhysX mass properties for the formal cooked stone hull.

The raw pyphysx dump stores PxConvexMesh::getMassInformation() in mesh-local
space. Unity/PhysX then applies PxConvexMeshGeometry.scale and, when a single
Rigidbody mass is requested, scales the density so the actor mass is 19.1 kg.
This script mirrors the PhysX 4.1 PxMassProperties::scaleInertia path for the
scale candidates we can prove from the recovered Unity assets.
"""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RAW = (
    PROJECT_ROOT
    / "data"
    / "calibration"
    / "pyphysx_cooked_stone_hull_probe_unity_flags_rebuilt_raw_20260708.json"
)
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "pyphysx_scaled_mass_properties_20260709.json"

RIGIDBODY_MASS = 19.1
LOCAL_UNIFORM_SCALE = (0.115, 0.115, 0.115)
WORLD_LOSSY_SCALE = (0.112700008, 0.115, 0.112700008)

Vector = tuple[float, float, float]
Matrix = list[list[float]]


def _load_raw(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    report = json.loads(path.read_text(encoding="utf-8"))
    raw = (report.get("detail") or {}).get("raw_convex_mesh_data")
    if not isinstance(raw, dict):
        raise SystemExit(
            f"{path} has no detail.raw_convex_mesh_data. Re-run "
            "dump_pyphysx_cooked_convex_hull.py with --include-raw-convex-data."
        )
    return report, raw


def _vec(values: Any) -> Vector:
    return (float(values[0]), float(values[1]), float(values[2]))


def _matrix(values: Any) -> Matrix:
    return [[float(values[row][col]) for col in range(3)] for row in range(3)]


def _round_float(value: float, digits: int = 12) -> float:
    if abs(value) < 10 ** (-(digits - 2)):
        return 0.0
    return round(value, digits)


def _round_vec(value: Vector, digits: int = 12) -> list[float]:
    return [_round_float(part, digits) for part in value]


def _round_matrix(value: Matrix, digits: int = 12) -> list[list[float]]:
    return [[_round_float(part, digits) for part in row] for row in value]


def _mul_matrix_scalar(matrix: Matrix, scalar: float) -> Matrix:
    return [[matrix[row][col] * scalar for col in range(3)] for row in range(3)]


def _max_abs_offdiag(matrix: Matrix) -> float:
    return max(abs(matrix[row][col]) for row in range(3) for col in range(3) if row != col)


def _diag(matrix: Matrix) -> Vector:
    return (matrix[0][0], matrix[1][1], matrix[2][2])


def _scaled_bounds(bounds: dict[str, Any], scale: Vector) -> dict[str, Any]:
    minimum = _vec(bounds["minimum"])
    maximum = _vec(bounds["maximum"])
    scaled_min = tuple(minimum[index] * scale[index] for index in range(3))
    scaled_max = tuple(maximum[index] * scale[index] for index in range(3))
    extents = tuple(scaled_max[index] - scaled_min[index] for index in range(3))
    radius_x = max(abs(scaled_min[0]), abs(scaled_max[0]))
    radius_z = max(abs(scaled_min[2]), abs(scaled_max[2]))
    return {
        "minimum": _round_vec(scaled_min),
        "maximum": _round_vec(scaled_max),
        "extents": _round_vec(extents),
        "radius_x_m": _round_float(radius_x),
        "radius_z_m": _round_float(radius_z),
        "mean_radius_m": _round_float((radius_x + radius_z) * 0.5),
        "height_y_m": _round_float(extents[1]),
    }


def _shift_noncom_to_com(inertia_noncom: Matrix, mass: float, com: Vector) -> Matrix:
    """Mirror PxMassProperties convex branch.

    PxConvexMesh::getMassInformation() stores inertia in mesh local space. The
    PxMassProperties constructor converts it to COM-relative inertia before
    applying non-uniform scale. COM is near zero for this hull, but preserving
    the step keeps the report tied to PhysX.
    """

    result = [[inertia_noncom[row][col] for col in range(3)] for row in range(3)]
    x, y, z = com
    result[0][0] -= mass * (y * y + z * z)
    result[1][1] -= mass * (z * z + x * x)
    result[2][2] -= mass * (x * x + y * y)
    result[0][1] = result[1][0] = inertia_noncom[0][1] + mass * x * y
    result[1][2] = result[2][1] = inertia_noncom[1][2] + mass * y * z
    result[0][2] = result[2][0] = inertia_noncom[0][2] + mass * z * x
    return result


def _scale_inertia_identity_rotation(inertia_com: Matrix, scale: Vector) -> Matrix:
    """PhysX 4.1 PxMassProperties::scaleInertia for identity scaleRotation."""

    sx, sy, sz = scale
    diagonal = _diag(inertia_com)
    half_trace = 0.5 * sum(diagonal)
    xyz2 = tuple(half_trace - diagonal[index] for index in range(3))
    scaledxyz2 = (xyz2[0] * sx * sx, xyz2[1] * sy * sy, xyz2[2] * sz * sz)

    xx = scaledxyz2[1] + scaledxyz2[2]
    yy = scaledxyz2[2] + scaledxyz2[0]
    zz = scaledxyz2[0] + scaledxyz2[1]
    xy = inertia_com[0][1] * sx * sy
    xz = inertia_com[0][2] * sx * sz
    yz = inertia_com[1][2] * sy * sz

    scaled = [
        [xx, xy, xz],
        [xy, yy, yz],
        [xz, yz, zz],
    ]
    return _mul_matrix_scalar(scaled, sx * sy * sz)


def _solid_cylinder_inertia(mass: float, radius: float, height: float) -> Vector:
    radial = mass * (3.0 * radius * radius + height * height) / 12.0
    vertical = 0.5 * mass * radius * radius
    return (radial, vertical, radial)


def _thin_shell_cylinder_inertia(mass: float, radius: float, height: float) -> Vector:
    radial = mass * (6.0 * radius * radius + height * height) / 12.0
    vertical = mass * radius * radius
    return (radial, vertical, radial)


def _candidate_report(
    *,
    name: str,
    role: str,
    scale: Vector,
    local_bounds: dict[str, Any],
    unit_mass: float,
    local_com: Vector,
    local_inertia_com: Matrix,
) -> dict[str, Any]:
    scale_product = scale[0] * scale[1] * scale[2]
    scaled_unit_mass = unit_mass * scale_product
    density_scale = RIGIDBODY_MASS / scaled_unit_mass
    scaled_com = tuple(local_com[index] * scale[index] for index in range(3))
    scaled_unit_inertia = _scale_inertia_identity_rotation(local_inertia_com, scale)
    final_inertia = _mul_matrix_scalar(scaled_unit_inertia, density_scale)
    final_diag = _diag(final_inertia)
    bounds = _scaled_bounds(local_bounds, scale)
    radius = bounds["mean_radius_m"]
    height = bounds["height_y_m"]
    solid = _solid_cylinder_inertia(RIGIDBODY_MASS, radius, height)
    thin = _thin_shell_cylinder_inertia(RIGIDBODY_MASS, radius, height)

    radial_mean = (final_diag[0] + final_diag[2]) * 0.5
    vertical = final_diag[1]
    return {
        "name": name,
        "role": role,
        "scale": _round_vec(scale),
        "scale_product": _round_float(scale_product, 15),
        "scaled_bounds": bounds,
        "unit_density_scaled_mass": _round_float(scaled_unit_mass, 15),
        "density_scale_to_rigidbody_mass_19p1": _round_float(density_scale, 9),
        "center_of_mass_after_scale_before_csharp_override": _round_vec(scaled_com, 15),
        "center_of_mass_runtime_after_csharp": [0.0, 0.0, 0.0],
        "unit_density_scaled_inertia_rows": _round_matrix(scaled_unit_inertia, 15),
        "rigidbody_mass_scaled_inertia_rows": _round_matrix(final_inertia, 12),
        "rigidbody_mass_scaled_inertia_diag_xyz": _round_vec(final_diag, 12),
        "max_abs_offdiag": _round_float(_max_abs_offdiag(final_inertia), 15),
        "axis_convention": {
            "mesh_x": "horizontal/radial",
            "mesh_y": "vertical",
            "mesh_z": "horizontal/radial",
            "probe_custom_inertia_note": (
                "probe_physx_collision_alignment.py builds z-up stones, so pass "
                "inertia_radial=(diag_x+diag_z)/2 and inertia_vertical=diag_y."
            ),
        },
        "probe_z_up_custom_args": {
            "inertia_radial": _round_float(radial_mean, 12),
            "inertia_vertical": _round_float(vertical, 12),
        },
        "comparison": {
            "solid_cylinder_diag_xyz_same_radius_height": _round_vec(solid, 12),
            "thin_shell_cylinder_diag_xyz_same_radius_height": _round_vec(thin, 12),
            "ratio_to_solid_cylinder_diag_xyz": _round_vec(
                tuple(final_diag[index] / solid[index] for index in range(3)), 9
            ),
            "ratio_to_thin_shell_cylinder_diag_xyz": _round_vec(
                tuple(final_diag[index] / thin[index] for index in range(3)), 9
            ),
        },
    }


def analyze(raw_path: Path) -> dict[str, Any]:
    _report, raw = _load_raw(raw_path)
    mass_info = raw.get("mass_information") or {}
    unit_mass = float(mass_info["unit_density_mass"])
    local_com = _vec(mass_info["local_center_of_mass"])
    local_inertia_noncom = _matrix(mass_info["local_inertia_rows"])
    local_inertia_com = _shift_noncom_to_com(local_inertia_noncom, unit_mass, local_com)
    local_bounds = raw["local_bounds"]

    candidates = [
        _candidate_report(
            name="mesh_local_identity",
            role="Control only: raw PxConvexMesh mass information without Unity object scale.",
            scale=(1.0, 1.0, 1.0),
            local_bounds=local_bounds,
            unit_mass=unit_mass,
            local_com=local_com,
            local_inertia_com=local_inertia_com,
        ),
        _candidate_report(
            name="unity_local_uniform_scale_0p115",
            role="Stone localScale without parent/non-uniform world scale.",
            scale=LOCAL_UNIFORM_SCALE,
            local_bounds=local_bounds,
            unit_mass=unit_mass,
            local_com=local_com,
            local_inertia_com=local_inertia_com,
        ),
        _candidate_report(
            name="unity_world_lossy_scale_0p112700008_0p115",
            role="Formal scene world scale recovered from assets; current best runtime geometry candidate.",
            scale=WORLD_LOSSY_SCALE,
            local_bounds=local_bounds,
            unit_mass=unit_mass,
            local_com=local_com,
            local_inertia_com=local_inertia_com,
        ),
    ]

    best = candidates[-1]
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_raw": str(raw_path),
        "physx_source_reference": {
            "mass_constructor": "PxMassProperties(const PxGeometry&), eCONVEXMESH branch",
            "inertia_scaling": "PxMassProperties::scaleInertia(identity scaleRotation)",
            "rigidbody_mass_scaling": (
                "PxRigidBodyExt::setMassAndUpdateInertia(single mass) scales density "
                "by targetMass / computedShapeMass"
            ),
        },
        "raw_mass_information": {
            "unit_density_mass": _round_float(unit_mass, 15),
            "local_center_of_mass": _round_vec(local_com, 15),
            "local_inertia_rows_noncom": _round_matrix(local_inertia_noncom, 15),
            "local_inertia_rows_com": _round_matrix(local_inertia_com, 15),
            "local_bounds": local_bounds,
            "raw_mesh_axes": "x/z radial, y vertical",
        },
        "rigidbody_mass": RIGIDBODY_MASS,
        "candidates": candidates,
        "recommended_for_collision_probe": {
            "candidate": best["name"],
            "reason": (
                "It uses the formal stone world radius 1.25*0.112700008=0.14087501m "
                "and world height 2*0.115=0.23m recovered from the Unity assets."
            ),
            "command_fragment": (
                "--radius 0.14087501 --height 0.23 --inertia-model custom "
                f"--inertia-radial {best['probe_z_up_custom_args']['inertia_radial']:.12g} "
                f"--inertia-vertical {best['probe_z_up_custom_args']['inertia_vertical']:.12g}"
            ),
        },
        "conclusion": (
            "The cooked hull inertia is now a derived PhysX value, not a fitted parameter. "
            "The remaining collision-error suspects are shape wrapper/local pose/contact handoff "
            "and solver/contact state, not the convex hull mass-property formula itself."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", type=Path, default=DEFAULT_RAW)
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    result = analyze(args.raw)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"output: {args.output}")
    for candidate in result["candidates"]:
        args_for_probe = candidate["probe_z_up_custom_args"]
        print(
            f"{candidate['name']}: radial={args_for_probe['inertia_radial']:.12g}, "
            f"vertical={args_for_probe['inertia_vertical']:.12g}, "
            f"massScale={candidate['density_scale_to_rigidbody_mass_19p1']:.6g}"
        )
    print(result["recommended_for_collision_probe"]["command_fragment"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
