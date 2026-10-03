"""Load the bundled strict ``pyphysx`` extension for local-simulator clients.

The extension is intentionally shipped beside the simulator instead of relying
on a developer-specific Conda installation.  Call
``install_bundled_pyphysx()`` before importing code that imports ``pyphysx``.
"""

from __future__ import annotations

import importlib.util
import platform
import sys
import types
from pathlib import Path
from typing import Any


RUNTIME_ROOT = Path(__file__).resolve().parent / "runtime"
RUNTIME_PYPHYSX_DIR = RUNTIME_ROOT / "pyphysx"
WINDOWS_BUNDLED_EXTENSIONS = {
    (3, 8): RUNTIME_PYPHYSX_DIR / "_pyphysx.cp38-win_amd64.pyd",
    (3, 9): RUNTIME_PYPHYSX_DIR / "_pyphysx.cp39-win_amd64.pyd",
    (3, 13): RUNTIME_PYPHYSX_DIR / "_pyphysx.cp313-win_amd64.pyd",
}
LINUX_BUNDLED_EXTENSIONS = {
    (3, 9): RUNTIME_PYPHYSX_DIR / "_pyphysx.cpython-39-x86_64-linux-gnu.so",
}
# Preserve the historical name for callers that inspect Windows payloads.
BUNDLED_EXTENSIONS = WINDOWS_BUNDLED_EXTENSIONS
# Kept as a compatibility alias for callers that inspect the original 3.8
# delivery path.  ``install_bundled_pyphysx`` resolves the active ABI itself.
BUNDLED_EXTENSION = WINDOWS_BUNDLED_EXTENSIONS[(3, 8)]


def _resolve_bundled_extension() -> Path:
    # Older callers (notably the benchmark) override ``BUNDLED_EXTENSION``
    # directly.  Honour that explicit non-default path while selecting the
    # appropriate ABI automatically in ordinary use.
    legacy_override = BUNDLED_EXTENSION
    if legacy_override != WINDOWS_BUNDLED_EXTENSIONS[(3, 8)]:
        extension = legacy_override
    else:
        system = platform.system()
        if system == "Windows":
            extensions = WINDOWS_BUNDLED_EXTENSIONS
        elif system == "Linux":
            extensions = LINUX_BUNDLED_EXTENSIONS
        else:
            extensions = {}
        extension = extensions.get(sys.version_info[:2])
    if extension is None or sys.maxsize <= 2**32:
        windows = ", ".join(f"Windows CPython {major}.{minor}" for major, minor in WINDOWS_BUNDLED_EXTENSIONS)
        linux = ", ".join(f"Linux CPython {major}.{minor}" for major, minor in LINUX_BUNDLED_EXTENSIONS)
        raise RuntimeError(f"严格模拟器需要受支持的 64 位 ABI（支持：{windows}；{linux}）。")
    if not extension.is_file():
        raise RuntimeError(f"缺少当前 Python 对应的随包 pyphysx 扩展：{extension}")
    return extension


def install_bundled_pyphysx() -> Any:
    """Install and return the bundled native binding for this Python ABI.

    This installs only into the current Python process; it neither modifies
    site-packages nor reads a pyphysx extension from another machine path.
    """

    extension_path = _resolve_bundled_extension()

    existing = sys.modules.get("pyphysx")
    if existing is not None:
        module_file = str(getattr(existing, "__file__", ""))
        if str(extension_path.parent) not in module_file:
            raise RuntimeError(
                "当前进程已加载其他 pyphysx；请在新的 Python 进程中先调用 "
                "install_bundled_pyphysx()。"
            )
        return existing

    package = types.ModuleType("pyphysx")
    package.__path__ = []
    package.__file__ = str(extension_path)
    sys.modules["pyphysx"] = package
    # CPython 3.13 Windows and CPython 3.9 Linux payloads ship a tiny
    # pure-Python ``quaternion`` shim beside the extension.  The binding
    # imports it while defining pose defaults.
    if str(extension_path.parent) not in sys.path:
        sys.path.insert(0, str(extension_path.parent))
    spec = importlib.util.spec_from_file_location("pyphysx._pyphysx", extension_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("无法创建 bundled pyphysx extension loader。")
    extension = importlib.util.module_from_spec(spec)
    sys.modules["pyphysx._pyphysx"] = extension
    spec.loader.exec_module(extension)
    for name in dir(extension):
        if not name.startswith("_"):
            setattr(package, name, getattr(extension, name))
    return package
