#!/usr/bin/env python3
"""Solve CyLab Academy Neuron Express 0."""

from __future__ import annotations

import socket


HOST = "aureolin-pixie.cylabacademy.net"
PORT = 51643


def recv_until_prompt(sock: socket.socket) -> str:
    data = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
        text = data.decode("utf-8", "replace")
        if "x>" in text or "academy{" in text:
            break
    return data.decode("utf-8", "replace")


def send_line(sock: socket.socket, line: str) -> str:
    sock.sendall(f"{line}\n".encode())
    response = recv_until_prompt(sock)
    print(f">>> {line}\n{response}", end="")
    return response


def main() -> None:
    with socket.create_connection((HOST, PORT), timeout=10) as sock:
        sock.settimeout(5)
        print(recv_until_prompt(sock), end="")

        for value in (10, -10, 0, 4, 2, 1):
            send_line(sock, str(value))

        send_line(sock, "TEST 1 -2")


if __name__ == "__main__":
    main()
