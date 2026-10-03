"""Check actual native cooker output before the existing hull asset import."""
import json
from pathlib import Path
import struct
import unittest
from unittest.mock import patch

from local_simulator.runtime_loader import install_bundled_pyphysx
import local_simulator.unity_physx as up


def words(values):
    return list(struct.unpack('<%dI'%len(values),struct.pack('<%df'%len(values),*values)))


class UnityStoneCookingTest(unittest.TestCase):
    def test_default_cooker_produces_observed_geometry_without_output_import(self):
        install_bundled_pyphysx()
        from tools.reverse import probe_physx_collision_alignment as probe
        fixture=json.loads((Path(__file__).parent/'fixtures/unity_stone_cooking_output_20261002.json').read_text())
        original=probe._patch_runtime_stone_shape
        seen=[]

        def observe(shape,**kwargs):
            actual=shape.get_convex_mesh_runtime_hull_data()
            # Observe before forwarding: output replacement cannot make this pass.
            for name,expected in fixture['byteLayout'].items():
                native=actual['byte_layout'][name]
                self.assertEqual(native['bytes'],expected['bytes'],name)
                self.assertEqual(actual['raw_bytes'][native['offset']:native['offset']+native['bytes']],
                    fixture['rawBytes'][expected['offset']:expected['offset']+expected['bytes']],name)
            for name,offset in [('aabb_center',0),('aabb_extents',12),('center_of_mass',24),('internal',48)]:
                value=words(actual[name])
                self.assertEqual(value,fixture['headerBits'][offset//4:offset//4+len(value)],name)
            for name,expected in fixture['bigConvexArrays'].items():
                self.assertEqual(actual['big_convex_raw_data'][name],expected,name)
            seen.append(actual)
            return original(shape,**kwargs)

        with patch.object(probe,'_patch_runtime_stone_shape',observe):
            up.PersistentPhysxFrontHalfScene(stone_count=16)
        self.assertEqual(len(seen),1)


if __name__=='__main__':unittest.main()
