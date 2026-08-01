"""Mini RSA — low-public-exponent attack, e = 3, no modular wraparound.

The challenge blurb: "we padded the plaintext so that (M ** e) is just
barely larger than N." With e = 3, a large N buys nothing if the message
M is small enough that M**3 doesn't wrap around N at all — then
`c = pow(M, e, N)` is just `M**3` with no modular reduction applied, and
recovering M is a plain integer cube root, no private key needed.

More generally, if M**e wraps around N a *small* number of times k, then
`c = M**e - k*N` for that k, so `M**e = c + k*N` — try k = 0, 1, 2, ...
until `c + k*N` is a perfect e-th power.

    python3 solve.py
"""

from pathlib import Path

VALUES_PATH = Path(__file__).parent / "values.txt"
E = 3


def parse_values(text: str) -> tuple[int, int]:
    values = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        values[key.strip().split()[0]] = int(val.strip())
    return values["N"], values["ciphertext"]


def integer_nth_root(n: int, e: int) -> int:
    """Largest x with x**e <= n, via binary search (no external deps)."""
    if n < 0:
        raise ValueError("no real root of a negative number for integer e")
    lo, hi = 0, 1 << (n.bit_length() // e + 2)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid**e <= n:
            lo = mid
        else:
            hi = mid - 1
    return lo


def recover_message(N: int, e: int, c: int, max_k: int = 10) -> bytes:
    """Search for the smallest k with `c + k*N` a perfect e-th power --
    the number of modular wraparounds M**e underwent."""
    for k in range(max_k):
        target = c + k * N
        m = integer_nth_root(target, e)
        if m**e == target:
            return m.to_bytes((m.bit_length() + 7) // 8, "big")
    raise ValueError(f"no perfect {e}-th power found for k in [0, {max_k})")


if __name__ == "__main__":
    N, c = parse_values(VALUES_PATH.read_text())
    message = recover_message(N, E, c)
    print("FLAG:", message.decode().strip())
