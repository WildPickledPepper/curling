from tools.reverse.recovered_extended_collider_mesh import generate_cylinder_mesh


def test_stone_cylinder_mesh_counts() -> None:
    mesh = generate_cylinder_mesh()

    assert len(mesh.vertices) == 512
    assert len(mesh.triangles) == 3060
    assert mesh.triangle_count == 1020


def test_stone_cylinder_mesh_dimensions() -> None:
    mesh = generate_cylinder_mesh()
    xs = [vertex[0] for vertex in mesh.vertices]
    ys = [vertex[1] for vertex in mesh.vertices]
    zs = [vertex[2] for vertex in mesh.vertices]

    assert min(xs) == -1.25
    assert max(xs) == 1.25
    assert min(ys) == -1.0
    assert max(ys) == 1.0
    assert min(zs) == -1.25
    assert max(zs) == 1.25


def test_stone_cylinder_flip_faces_matches_wasm_postpass() -> None:
    flipped = generate_cylinder_mesh(faces=4, flip_faces=True)
    unflipped = generate_cylinder_mesh(faces=4, flip_faces=False)

    assert unflipped.triangles[:6] == [0, 4, 1, 1, 4, 5]
    assert flipped.triangles[:6] == [4, 0, 1, 4, 1, 5]
