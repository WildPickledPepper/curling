"""Windows SDK-backed read-only CPU topology/performance counters."""
import ctypes as C
import struct


class CpuTelemetry:
    def __init__(self):
        self.k = C.WinDLL('kernel32', use_last_error=True)
        get = self.k.GetSystemCpuSetInformation
        get.argtypes = (C.c_void_p, C.c_uint32, C.POINTER(C.c_uint32), C.c_void_p, C.c_uint32)
        size = C.c_uint32()
        get(None, 0, C.byref(size), None, 0)
        data = C.create_string_buffer(size.value)
        if not get(data, size, C.byref(size), None, 0):
            raise C.WinError(C.get_last_error())
        self.topology = []
        offset = 0
        while offset < size.value:
            length, kind = struct.unpack_from('<II', data.raw, offset)
            if length < 8:
                raise RuntimeError('Invalid CPU topology record')
            if kind == 0:
                # SYSTEM_CPU_SET_INFORMATION from local Windows SDK winnt.h.
                ident, group, logical, core, cache, numa, efficiency, flags, scheduling = \
                    struct.unpack_from('<IHBBBBBBI', data.raw, offset+8)
                self.topology.append(dict(id=ident, group=group, logical=logical, core=core,
                    cache=cache, numa=numa, efficiency=efficiency, flags=flags, scheduling=scheduling & 255))
            offset += length
        self.pdh = C.WinDLL('pdh')
        self.query = C.c_void_p()
        self.pdh.PdhOpenQueryW.argtypes = (C.c_wchar_p, C.c_size_t, C.POINTER(C.c_void_p))
        self.pdh.PdhAddEnglishCounterW.argtypes = (C.c_void_p, C.c_wchar_p, C.c_size_t, C.POINTER(C.c_void_p))
        self.pdh.PdhCollectQueryData.argtypes = (C.c_void_p,)
        self.pdh.PdhCloseQuery.argtypes = (C.c_void_p,)
        self.pdh.PdhGetFormattedCounterValue.argtypes = (C.c_void_p, C.c_uint32, C.c_void_p, C.c_void_p)
        self.counters = []
        self.error = self.pdh.PdhOpenQueryW(None, 0, C.byref(self.query))
        if not self.error:
            for cpu in self.topology:
                for label in ('% Processor Performance', '% Processor Utility', 'Processor Frequency'):
                    handle = C.c_void_p()
                    path = '\\Processor Information(%s,%s)\\%s' % (cpu['group'], cpu['logical'], label)
                    status = self.pdh.PdhAddEnglishCounterW(self.query, path, 0, C.byref(handle))
                    self.counters.append((cpu['logical'], label, handle, status))
            self.pdh.PdhCollectQueryData(self.query)

    def snapshot(self):
        if self.error:
            return dict(error=self.error)
        status = self.pdh.PdhCollectQueryData(self.query)
        rows = {}
        class Value(C.Structure):
            _fields_ = [('status', C.c_uint32), ('value', C.c_double)]
        for cpu, label, handle, added in self.counters:
            value = Value()
            formatted = added or self.pdh.PdhGetFormattedCounterValue(handle, 0x200 | 0x8000, None, C.byref(value))
            rows.setdefault(str(cpu), {})[label] = dict(status=formatted or value.status,
                value=value.value if not formatted and value.status in (0, 1) else None)
        return dict(status=status, processors=rows)

    def close(self):
        if self.query:
            self.pdh.PdhCloseQuery(self.query)
