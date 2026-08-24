#!/usr/bin/env python3
"""Solve CyLab Academy Neuron Meet 0."""

from __future__ import annotations

import socket


HOST = "aureolin-pixie.cylabacademy.net"
PORT = 50261


def recv_until_prompt(sock: socket.socket) -> str:
    data = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
        text = data.decode("utf-8", "replace")
        lowered = text.lower()
        if "x>" in text or "flag" in lowered or "pattern matched" in lowered:
            break
    return data.decode("utf-8", "replace")


def classify(response: str) -> int:
    if "fires" in response:
        return 1
    if "stays quiet" in response:
        return 0
    raise ValueError(f"could not classify response: {response!r}")


def send_probe(sock: socket.socket, value: float) -> tuple[int, str]:
    sock.sendall(f"{value}\n".encode())
    response = recv_until_prompt(sock)
    bit = classify(response)
    print(f"x={value: .8f} -> {bit}")
    return bit, response


def send_command(sock: socket.socket, command: str) -> str:
    sock.sendall(f"{command}\n".encode())
    response = recv_until_prompt(sock)
    print(f">>> {command}")
    return response


def main() -> None:
    with socket.create_connection((HOST, PORT), timeout=10) as sock:
        sock.settimeout(5)
        print(recv_until_prompt(sock))

        low_value = -10.0
        high_value = 10.0
        low_bit, _ = send_probe(sock, low_value)
        high_bit, _ = send_probe(sock, high_value)

        if low_bit == high_bit:
            raise RuntimeError("extreme probes did not reveal opposite sides")

        zero_extreme = low_value if low_bit == 0 else high_value
        one_extreme = low_value if low_bit == 1 else high_value

        left_value, left_bit = low_value, low_bit
        right_value, right_bit = high_value, high_bit
        for _ in range(18):
            middle = (left_value + right_value) / 2
            middle_bit, _ = send_probe(sock, middle)
            if middle_bit == left_bit:
                left_value, left_bit = middle, middle_bit
            else:
                right_value, right_bit = middle, middle_bit

        print(
            "boundary between "
            f"{left_value:.8f} ({left_bit}) and {right_value:.8f} ({right_bit})"
        )

        print(send_command(sock, "RESET"))

        if zero_extreme < one_extreme:
            zero_values = [-10.0, -9.9, -9.8, -9.7, -9.6]
            one_values = [10.0, 9.9, 9.8, 9.7]
        else:
            zero_values = [10.0, 9.9, 9.8, 9.7, 9.6]
            one_values = [-10.0, -9.9, -9.8, -9.7]

        final_values = [
            zero_values[0],
            one_values[0],
            one_values[1],
            one_values[2],
            zero_values[1],
            zero_values[2],
            zero_values[3],
            zero_values[4],
        ]

        final_response = ""
        for value in final_values:
            _, final_response = send_probe(sock, value)

        print(final_response)


if __name__ == "__main__":
    main()
