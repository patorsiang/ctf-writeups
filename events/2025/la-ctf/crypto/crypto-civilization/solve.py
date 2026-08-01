"""Crypto Civilization — equivocal-commitment attack.

chall.py implements a bit-commitment "coin flip" 200 times: it hands you a
fresh 32-bit `y`, you commit to a 4-byte value `com` *before* it tells you
which branch it will challenge, then it asks you to open either:

    chicken (choice 0): reveal s0 with PRG(s0)          == com
    beef    (choice 1): reveal s1 with PRG(s1) XOR y     == com

where PRG stretches a 2-byte seed to 4 bytes via truncated SHA3-256. A
sound commitment scheme would bind you to one branch before you learn the
challenge. This one doesn't, because `y` is sent to you *before* you have
to commit: if you can find seeds s0, s1 with

    PRG(s0) == PRG(s1) XOR y       (equivalently PRG(s0) XOR PRG(s1) == y)

you commit `com = PRG(s0)`, and now *either* challenge opens correctly:
s0 for chicken, s1 for beef. You never had to decide which coin you were
committing to.

Whether such a pair exists for a given `y` is a birthday question: PRG's
image has exactly 2**16 points inside a 2**32 codomain, so the expected
number of (s0, s1) pairs with PRG(s0) XOR PRG(s1) == y is
2**16 * 2**16 / 2**32 == 1 for uniform y — meaning a solution exists for
most, not all, of the 200 rounds (see test_recon.py for the measured
rate). When no pair exists, fall back to an honest chicken commitment:
that still wins half the time by chance, which is enough to clear the
scoreboard's 133/200 bar in expectation.

Runs the local chall.py directly (the archived chall.lac.tf server is no
longer reachable):

    python3 solve.py
"""

import hashlib
import subprocess
import sys
from pathlib import Path

CHALL_DIR = Path(__file__).parent
ROUNDS = 200
PASS_THRESHOLD = 132  # chall.py: number_correct > 132


def prg(seed: bytes) -> bytes:
    assert len(seed) == 2
    return hashlib.sha3_256(seed).digest()[:4]


def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def build_prg_table():
    """Every seed's PRG output, computed once and reused for all 200
    rounds — the fixed 65536-seed domain never changes between rounds."""
    return {prg(i.to_bytes(2, "big")): i.to_bytes(2, "big") for i in range(2**16)}


def find_equivocation(y: bytes, table: dict):
    """A commitment that opens as either branch, or None if none exists
    for this y (expected for roughly a third of rounds)."""
    for out, s0 in table.items():
        target = xor_bytes(out, y)
        s1 = table.get(target)
        if s1 is not None:
            return out, s0, s1
    return None


class Recvuntil:
    """chall.py's input() prompts aren't newline-terminated, so a
    line-based reader would block forever waiting for one. Scan
    byte-by-byte for an arbitrary delimiter instead."""

    def __init__(self, stream):
        self.stream = stream

    def until(self, delim: bytes) -> bytes:
        buf = b""
        while not buf.endswith(delim):
            c = self.stream.read(1)
            if not c:
                break
            buf += c
        return buf


def play(rounds=ROUNDS, chall_dir=CHALL_DIR):
    proc = subprocess.Popen(
        [sys.executable, "-u", "chall.py"],
        cwd=chall_dir,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    out = Recvuntil(proc.stdout)

    def send(data: bytes):
        proc.stdin.write(data + b"\n")
        proc.stdin.flush()

    table = build_prg_table()
    correct = 0
    equivocated = 0

    out.until(b"Can you level up to a Crypto Pro?\n")

    for _ in range(rounds):
        out.until(b"Here's y: ")
        y = bytes.fromhex(out.until(b"\n").strip().decode())

        result = find_equivocation(y, table)
        if result:
            com, s0, s1 = result
            equivocated += 1
        else:
            s0 = s1 = b"\x00\x00"
            com = prg(s0)

        out.until(b"> ")
        send(com.hex().encode())

        prompt = out.until(b"(hex).\n")
        out.until(b"> ")
        send((s0 if b"chicken" in prompt else s1).hex().encode())

        if b"Good work" in out.until(b"\n"):
            correct += 1

    tail = out.until(b"trials passed\n") + proc.stdout.read()
    proc.stdin.close()
    proc.wait(timeout=10)

    return correct, equivocated, tail.decode(errors="replace")


if __name__ == "__main__":
    correct, equivocated, tail = play()
    print(f"Equivocated {equivocated}/{ROUNDS} rounds")
    print(f"Passed {correct}/{ROUNDS} (need > {PASS_THRESHOLD})")
    print(tail)
