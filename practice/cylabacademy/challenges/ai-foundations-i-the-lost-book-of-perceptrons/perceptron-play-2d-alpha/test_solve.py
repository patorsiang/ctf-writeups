"""Tests for the Perceptron Play 2D Alpha helper."""

import unittest

from solve import run_session


class ScriptedSocket:
    """Small TCP-service double with banner and command responses."""

    def __init__(self) -> None:
        self.sent: list[bytes] = []
        self.responses = [
            b"Welcome to Perceptron Play 2D!\n> ",
            b"Current weights -> w1: 1, w2: 1, b: 0\n> ",
            b"Perfect! All points are classified correctly.\n"
            b"academy{test_flag}\n",
        ]

    def recv(self, _size: int) -> bytes:
        return self.responses.pop(0)

    def sendall(self, data: bytes) -> None:
        self.sent.append(data)


class RunSessionTests(unittest.TestCase):
    def test_submits_working_parameters_then_checks(self) -> None:
        sock = ScriptedSocket()

        transcript = run_session(sock)

        self.assertEqual(sock.sent, [b"SET 1 1 0\n", b"CHECK\n"])
        self.assertIn("academy{test_flag}", transcript)


if __name__ == "__main__":
    unittest.main()
