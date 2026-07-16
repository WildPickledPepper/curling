"""Minimal curling AI used only to test native-extension submission packaging.

The module import is deliberately at top level: if the platform drops the .so
file, this process exits before it connects, making the failure unambiguous.
"""

import argparse
import importlib.machinery
import os
import socket
import sys
import sysconfig
import time

try:
    import probeext
except ModuleNotFoundError:
    # The battle worker can differ from the course Jupyter kernel.  This uses
    # standard library only, so its failure log identifies the correct ABI.
    print("NATIVE_PROBE_IMPORT_FAILED", flush=True)
    print(f"runtime_platform={sys.platform}", flush=True)
    print(f"runtime_python={sys.version}", flush=True)
    print(f"runtime_soabi={sysconfig.get_config_var('SOABI')}", flush=True)
    print(f"runtime_extension_suffixes={importlib.machinery.EXTENSION_SUFFIXES}", flush=True)
    print(f"runtime_cwd={os.getcwd()}", flush=True)
    try:
        print(f"runtime_files={sorted(os.listdir('.'))}", flush=True)
    except OSError as error:
        print(f"runtime_files_error={error!r}", flush=True)
    raise


print(f"NATIVE_PROBE_OK answer={probeext.answer()}", flush=True)


def receive_message(sock: socket.socket) -> tuple[str, list[str]]:
    buffer = bytearray()
    while True:
        data = sock.recv(1)
        if not data or data == b"\0":
            break
        buffer.extend(data)
    parts = buffer.decode(errors="replace").strip().split()
    return (parts[0], parts[1:]) if parts else ("", [])


def send_message(sock: socket.socket, message: str) -> None:
    print(f">>>> {message}", flush=True)
    sock.send(message.encode())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", required=True)
    parser.add_argument("-p", "--port", required=True, type=int)
    parser.add_argument("-k", "--key", default="")
    args = parser.parse_args()

    with socket.create_connection((args.host, args.port), timeout=20) as sock:
        send_message(sock, f"CONNECTKEY:{args.key}")
        empty_messages = 0
        while True:
            code, _ = receive_message(sock)
            print(f"<<<< {code}", flush=True)
            if not code:
                empty_messages += 1
                if empty_messages >= 5:
                    return 0
                continue
            empty_messages = 0
            if code == "ISREADY":
                send_message(sock, "READYOK")
                time.sleep(0.2)
                send_message(sock, "NAME NativeProbe")
            elif code == "GO":
                # This is intentionally a harmless fixed shot, not a strategy.
                send_message(sock, "BESTSHOT 3.0 0.0 0.0")
            elif code == "CENTERLINE_VIOLATION":
                send_message(sock, "CENTERLINE_CHOICE RESET")
            elif code == "GAMEOVER":
                return 0


if __name__ == "__main__":
    sys.exit(main())
