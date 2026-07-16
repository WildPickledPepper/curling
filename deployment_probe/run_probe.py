"""Run this after compiling probeext in the target-compatible Codespace."""

import platform
import sys

import probeext

print("native_extension_import=OK")
print(f"probe_answer={probeext.answer()}")
print(f"python={sys.version.split()[0]}")
print(f"platform={platform.platform()}")
