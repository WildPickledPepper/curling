"""Start a tiny local curling server and verify probe_submission.py end to end.

Run this inside the Linux Codespaces build directory after `build_ext --inplace`.
It deliberately uses the same NUL-terminated server messages as the course
protocol, and checks the AI's CONNECTKEY / READYOK / NAME / BESTSHOT flow.
"""

from __future__ import annotations

import socket
import subprocess
import sys
import threading
import time
from pathlib import Path


HOST = "127.0.0.1"
PORT = 18080
HERE = Path(__file__).resolve().parent


def send(sock: socket.socket, message: str) -> None:
    sock.sendall((message + "\0").encode())


def receive(sock: socket.socket, label: str) -> str:
    data = sock.recv(1024)
    if not data:
        raise RuntimeError(f"{label}: client disconnected")
    text = data.decode().strip()
    print(f"server received {label}: {text}")
    return text


def server(errors: list[BaseException]) -> None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind((HOST, PORT))
            listener.listen(1)
            listener.settimeout(10)
            client, _ = listener.accept()
            with client:
                client.settimeout(5)
                assert receive(client, "connect").startswith("CONNECTKEY:"), "missing CONNECTKEY"
                send(client, "CONNECTNAME Player1")
                send(client, "ISREADY")
                assert receive(client, "ready") == "READYOK", "missing READYOK"
                time.sleep(0.3)
                assert receive(client, "name").startswith("NAME "), "missing NAME"

                send(client, "SETSTATE 0 0 -1 0")
                send(client, "POSITION " + " ".join(["0"] * 32))
                send(client, "GO")
                assert receive(client, "shot") == "BESTSHOT 3.0 0.0 0.0", "unexpected BESTSHOT"
                send(client, "GAMEOVER DRAW")
    except BaseException as error:  # surfaced in the main thread with context
        errors.append(error)


def main() -> int:
    errors: list[BaseException] = []
    thread = threading.Thread(target=server, args=(errors,), daemon=True)
    thread.start()
    time.sleep(0.1)
    process = subprocess.run(
        [sys.executable, "probe_submission.py", "-H", HOST, "-p", str(PORT), "-k", "local-probe"],
        cwd=HERE,
        text=True,
        capture_output=True,
        timeout=15,
    )
    thread.join(timeout=10)

    print("--- AI stdout ---")
    print(process.stdout, end="")
    if process.stderr:
        print("--- AI stderr ---")
        print(process.stderr, end="")
    if errors:
        raise errors[0]
    if thread.is_alive():
        raise RuntimeError("server did not finish")
    if process.returncode != 0:
        raise RuntimeError(f"AI exited with {process.returncode}")
    if "NATIVE_PROBE_OK answer=42" not in process.stdout:
        raise RuntimeError("native extension import marker missing")
    print("LOCAL_PROTOCOL_SMOKE_TEST=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
