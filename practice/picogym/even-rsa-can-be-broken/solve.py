"""EVEN RSA CAN BE BROKEN??? — parity attack on a buggy prime generator.

encrypt.py builds a "1024-bit" RSA key as `p, q = get_primes(k // 2)`,
`N = p * q` — standard textbook RSA, e = 65537, no padding. `get_primes`
(from an undisclosed `setup.py`) is buggy: one of the two primes it
returns is always 2. That makes N even, which is visible from the public
key alone: no factoring algorithm needed, just `N % 2`. Once one factor
is known, decryption is textbook: `phi = (p-1)*(q-1)`, `d = e^-1 mod phi`.

Decrypt the pinned capture from the instance this was solved against:
    python3 solve.py

Or connect to a fresh instance and decrypt whatever it hands you:
    python3 solve.py HOST PORT
"""

import socket
import sys


def factor_even_modulus(N: int) -> tuple[int, int]:
    """N's only known weakness is that it's even. Guard the assumption
    instead of silently mis-factoring an N this attack doesn't apply to."""
    if N % 2 != 0:
        raise ValueError("N is odd -- this modulus isn't the broken kind")
    return 2, N // 2


def decrypt(N: int, e: int, c: int) -> bytes:
    p, q = factor_even_modulus(N)
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    m = pow(c, d, N)
    return m.to_bytes((m.bit_length() + 7) // 8, "big")


def fetch_from_service(host: str, port: int) -> tuple[int, int, int]:
    with socket.create_connection((host, port), timeout=10) as s:
        data = s.recv(65536).decode()
    values = {}
    for line in data.splitlines():
        key, _, val = line.partition(":")
        values[key.strip()] = val.strip()
    return int(values["N"]), int(values["e"]), int(values["cyphertext"])


# Captured live via `nc verbal-sleep.picoctf.net 51977` while solving this.
# The random half of the key (q) differs on every connection, but the bug
# -- p always coming out as 2 -- doesn't; test_recon.py exercises the
# attack against a freshly, independently generated vulnerable key rather
# than relying solely on this one capture.
CAPTURED_N = 21633626737269615521951039144702251856228273557790311610823320576692637632787053852817547102650838958629568629728177764942082801438515481978557887242862578
CAPTURED_E = 65537
CAPTURED_C = 14199031501331299946574426394086541776318261200568907273343531853704473146121518433141531851128851636629077412296241554941489648851999973942131698168991625


if __name__ == "__main__":
    if len(sys.argv) == 3:
        N, e, c = fetch_from_service(sys.argv[1], int(sys.argv[2]))
    else:
        N, e, c = CAPTURED_N, CAPTURED_E, CAPTURED_C

    print("FLAG:", decrypt(N, e, c).decode())
