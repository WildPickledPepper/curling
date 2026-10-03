"""Bitwise equivalence of the optional native float32 arithmetic kernel."""
import random
import struct
from types import SimpleNamespace
import unittest
import numpy as np
from local_simulator.native_angular_projection import load_angular_projection
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene

class NativeAngularProjectionTest(unittest.TestCase):
    def test_normalized_and_raw_projection_match_reference_float_words(self):
        native=load_angular_projection()
        if native is None:
            self.skipTest('optional Windows native helper is unavailable')
        scene=SimpleNamespace(probe=SimpleNamespace(np=np))
        rng=random.Random(20261003)
        samples=[(0.,0.,0.,1.),(0.,0.,1.,0.),
                 (5.197146535351749e-08,-.6250340938568115,-4.161447719752687e-08,.7805975079536438)]
        samples += [tuple(np.float32(rng.uniform(-1.,1.)) for _ in range(4)) for _ in range(5000)]
        for q in samples:
            for normalize in (False,True):
                reference_q=q
                if normalize:
                    a=np.asarray(q,dtype=np.float32)
                    reference_q=tuple(a/np.sqrt(np.sum(a*a,dtype=np.float32)))
                for angle in (0.,-.0,15.7,-9.42,1e-8):
                    expected=PersistentPhysxFrontHalfScene._unity_project_locked_angular_velocity(scene,reference_q,angle)
                    actual=native(q,angle,normalize=normalize)
                    self.assertEqual(struct.pack('<3f',*actual),struct.pack('<3f',*expected),(q,angle,normalize))

if __name__=='__main__':unittest.main()
