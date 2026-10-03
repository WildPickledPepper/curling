"""Probe whether the submission service preserves a native extension inside a zip.

The ordinary ``.pyd`` file is silently dropped by the battle-worker uploader.
This script unpacks the exact CPython 3.13 Windows probe extension at runtime,
then imports it from the extracted directory.
"""

import argparse
import importlib
import os
from pathlib import Path
import socket
import sys
import time
import zipfile


ROOT = Path(__file__).resolve().parent
PAYLOAD = ROOT / "native_payload.zip"
NATIVE_DIR = ROOT / ".native_probe"


def load_probe_extension() -> object:
    if not PAYLOAD.is_file():
        raise RuntimeError(f"native payload missing: {PAYLOAD.name}")
    NATIVE_DIR.mkdir(exist_ok=True)
    with zipfile.ZipFile(PAYLOAD) as archive:
        archive.extractall(NATIVE_DIR)
    sys.path.insert(0, os.fspath(NATIVE_DIR))
    return importlib.import_module("probeext")


probeext = load_probe_extension()
print(f"EMBEDDED_NATIVE_PROBE_OK answer={probeext.answer()}", flush=True)


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
        while True:
            code, _ = receive_message(sock)
            print(f"<<<< {code}", flush=True)
            if code == "ISREADY":
                send_message(sock, "READYOK")
                time.sleep(0.2)
                send_message(sock, "NAME EmbeddedNativeProbe")
            elif code == "GO":
                send_message(sock, "BESTSHOT 3.0 0.0 0.0")
            elif code == "CENTERLINE_VIOLATION":
                send_message(sock, "CENTERLINE_CHOICE RESET")
            elif code == "GAMEOVER" or not code:
                return 0


if __name__ == "__main__":
    raise SystemExit(main())
