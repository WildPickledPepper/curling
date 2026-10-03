from setuptools import Extension, setup

setup(
    name="curling-native-probe",
    version="0.1.0",
    ext_modules=[Extension("probeext", ["probeext.c"])],
)
