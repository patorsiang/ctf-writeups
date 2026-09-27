#!/usr/bin/env python3
"""Solve CyLab Academy Perceptron Play Naught."""

from __future__ import annotations

import socket
import sys
from typing import Protocol


HOST = "xebec.cylabacademy.net"
DEFAULT_PORT = 18281
COMMANDS = ("SET 0 1 0", "CHECK")


class SocketLike(Protocol):
    def recv(self, size: int) -> bytes: ...

    def sendall(self, data: bytes) -> None: ...


def recv_until_prompt(sock: SocketLike) -> str:
    data = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
        text = data.decode("utf-8", "replace")
        if text.endswith("> ") or "academy{" in text:
            break
    return data.decode("utf-8", "replace")


def run_session(sock: SocketLike) -> str:
    transcript = [recv_until_prompt(sock)]
    for command in COMMANDS:
        sock.sendall(f"{command}\n".encode())
        transcript.append(recv_until_prompt(sock))

    result = "".join(transcript)
    print(result, end="")
    return result


def main() -> None:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    with socket.create_connection((HOST, port), timeout=10) as sock:
        sock.settimeout(5)
        run_session(sock)


if __name__ == "__main__":
    main()
