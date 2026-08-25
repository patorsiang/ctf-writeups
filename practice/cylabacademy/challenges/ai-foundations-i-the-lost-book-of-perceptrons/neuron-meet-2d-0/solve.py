#!/usr/bin/env python3
"""Solve CyLab Academy Neuron Meet 2D-0."""

from __future__ import annotations

import socket
import sys


HOST = "aureolin-pixie.cylabacademy.net"
DEFAULT_PORT = 56279


def recv_until_prompt(sock: socket.socket) -> str:
    data = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
        text = data.decode("utf-8", "replace")
        lowered = text.lower()
        if "(x,y)>" in text or "flag" in lowered or "pattern matched" in lowered:
            break
    return data.decode("utf-8", "replace")


def send_pair(sock: socket.socket, x_value: int, y_value: int) -> str:
    sock.sendall(f"{x_value},{y_value}\n".encode())
    response = recv_until_prompt(sock)
    if "fires" in response:
        bit = 1
    elif "stays quiet" in response:
        bit = 0
    else:
        bit = "?"
    print(f"{x_value},{y_value} -> {bit}")
    return response


def main() -> None:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    final_pairs = [
        (-10, -10),
        (10, 10),
        (9, 9),
        (8, 8),
        (-9, -9),
        (-8, -8),
        (-7, -7),
        (-6, -6),
    ]

    with socket.create_connection((HOST, port), timeout=10) as sock:
        sock.settimeout(5)
        print(recv_until_prompt(sock))

        final_response = ""
        for x_value, y_value in final_pairs:
            final_response = send_pair(sock, x_value, y_value)

        print(final_response)


if __name__ == "__main__":
    main()
