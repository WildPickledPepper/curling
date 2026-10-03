"""Read actual GameSceneNoLimit Wall colliders, retaining binary32 values."""
import hashlib
import importlib.util
import json
from pathlib import Path

import UnityPy

ROOT = Path(__file__).resolve().parents[1]
source = ROOT/'analysis_input/unity_data_20261002.unity3d'
inspector = ROOT/'research_archive/unity_reverse/source/reverse/inspect_unity_assets.py'
spec = importlib.util.spec_from_file_location('unity_asset_reader', inspector)
module = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = module
spec.loader.exec_module(module)
env = UnityPy.load(str(source))
walls = []
settings = None
for reader in env.objects:
    if reader.type.name == 'PhysicsManager':
        p = reader.read()
        settings = dict(contactOffset=p.m_DefaultContactOffset,
                        defaultMaterialPathId=p.m_DefaultMaterial.m_PathID)
    if reader.type.name != 'GameObject' or reader.assets_file.name != 'level4':
        continue
    obj = reader.read()
    if obj.m_Name not in ('bound1', 'bound2', 'bound3', 'bound4'):
        continue
    t = obj.m_Transform.read()
    assert t.m_Father.m_PathID == 0
    collider = next(c for c in module.component_readers(obj) if c.type.name == 'BoxCollider')
    c = collider.read()
    def vec(v): return [v.x, v.y, v.z]
    assert vec(c.m_Center) == [0, 0, 0]
    assert vec(c.m_Size) == [1, 1, 1]
    assert c.m_Material.m_PathID == 0 and obj.m_Tag == 20000
    assert c.m_Enabled and not c.m_IsTrigger and obj.m_IsActive
    walls.append(dict(name=obj.m_Name, gameObjectPathId=reader.path_id,
        colliderPathId=collider.path_id, position=vec(t.m_LocalPosition),
        quaternionWxyz=[t.m_LocalRotation.w, t.m_LocalRotation.x,
                         t.m_LocalRotation.y, t.m_LocalRotation.z],
        size=vec(t.m_LocalScale), layer=obj.m_Layer, tag='Wall',
        materialPathId=c.m_Material.m_PathID))
assert len(walls) == 4 and settings
out = dict(schema='unity-gamescene-wall-colliders-v1', scene='level4 / GameSceneNoLimit',
           walls=walls, physics=settings, source=dict(path=str(source.relative_to(ROOT)),
           sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
           extractor=str(Path(__file__).relative_to(ROOT))))
(ROOT/'local_simulator/assets/unity_wall_colliders.json').write_text(
    json.dumps(out, indent=2), encoding='utf8')
print(json.dumps(out, indent=2))
