#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject *probe_answer(PyObject *self, PyObject *args) {
    (void)self;
    (void)args;
    return PyLong_FromLong(42);
}

static PyMethodDef ProbeMethods[] = {
    {"answer", probe_answer, METH_NOARGS, "Return a known value from native code."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef probemodule = {
    PyModuleDef_HEAD_INIT,
    "probeext",
    "Tiny native-extension compatibility probe.",
    -1,
    ProbeMethods
};

PyMODINIT_FUNC PyInit_probeext(void) {
    return PyModule_Create(&probemodule);
}
