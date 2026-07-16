#!/usr/bin/env python3
"""Keep two curling protocol slots connected without issuing any throws."""

from __future__ import annotations

import argparse
import select
import socket


def recv_message(sock: socket.socket) -> tuple[str, list[str]]:
    data = bytearray()
    while True:
        chunk = sock.recv(1)
        if not chunk or chunk == b"\0":
            break
        data.extend(chunk)
    text = data.decode(errors="replace").strip()
    parts = text.split()
    if not parts:
        raise ConnectionError("server closed the protocol socket")
    return parts[0], parts[1:]


def send(sock: socket.socket, message: str) -> None:
    sock.send(message.encode())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7788)
    parser.add_argument("--key", default="localtest")
    parser.add_argument("--name", default="ice_mesh_probe")
    parser.add_argument(
        "--bestshot-on-go",
        default="",
        help="Optional one-shot BESTSHOT payload sent to the first GO only.",
    )
    args = parser.parse_args()
    clients: list[socket.socket] = []
    shot_sent = False
    try:
        for index in range(2):
            client = socket.socket()
            client.connect((args.host, args.port))
            send(client, "CONNECTKEY:" + args.key)
            clients.append(client)
        print(f"connected_slots=2 host={args.host} port={args.port}", flush=True)
        while True:
            ready, _, _ = select.select(clients, [], [], 0.25)
            for client in ready:
                code, values = recv_message(client)
                if code == "ISREADY":
                    send(client, "READYOK")
                    send(client, f"NAME {args.name}")
                elif code == "GO" and args.bestshot_on_go and not shot_sent:
                    send(client, "BESTSHOT " + args.bestshot_on_go)
                    shot_sent = True
                elif code == "CENTERLINE_VIOLATION":
                    send(client, "CENTERLINE_CHOICE RESET")
                elif code.startswith("Error"):
                    raise ConnectionError("server rejected the protocol key")
                print(f"{code} {' '.join(values)}", flush=True)
    finally:
        for client in clients:
            client.close()


if __name__ == "__main__":
    raise SystemExit(main())
