"""Mod 26 — ROT13 on the provided ciphertext.

The challenge title is the whole hint: everything happens modulo 26, i.e.
a Caesar shift over the alphabet. The given string starts `cvpbPGS{`,
which maps to `picoCTF{` under a shift of 13 — ROT13.

Implemented as a general Caesar so the shift is an argument rather than a
magic constant: a shift-13 special case can't be sanity-checked against
the shift that actually recovers the known `picoCTF{` prefix.

    python3 solve.py            # decode the ciphertext in values.txt
    python3 solve.py <text>     # decode anything else
"""

import string
import sys
from pathlib import Path

LOWER = string.ascii_lowercase
UPPER = string.ascii_uppercase


def caesar(text: str, shift: int) -> str:
    """Shift letters by `shift` mod 26. Non-letters pass through untouched,
    which is why the flag's braces, digits and underscores survive."""
    out = []
    for ch in text:
        if ch in LOWER:
            out.append(LOWER[(LOWER.index(ch) + shift) % 26])
        elif ch in UPPER:
            out.append(UPPER[(UPPER.index(ch) + shift) % 26])
        else:
            out.append(ch)
    return "".join(out)


def rot13(text: str) -> str:
    return caesar(text, 13)


def find_shift(ciphertext: str, crib: str = "picoCTF{") -> int:
    """Recover the shift from a known plaintext prefix instead of assuming
    13. Raises if no shift produces the crib -- a Caesar that doesn't fit
    the crib is a different cipher, not a Caesar with an unlucky key."""
    for shift in range(26):
        if caesar(ciphertext, shift).startswith(crib):
            return shift
    raise ValueError(f"no shift in 0..25 maps this ciphertext to {crib!r}")


VALUES_FILE = Path(__file__).parent / "values.txt"


def load_ciphertext(path: Path = VALUES_FILE) -> str:
    """Read the challenge input from values.txt.

    values.txt is the single source of truth for the ciphertext. Holding a
    copy here as a literal too would mean two things that must agree with
    nothing enforcing it -- the point of a single source isn't saving
    space, it's that there is no second copy to drift.

    Validates rather than silently coercing: a file with two entries is a
    different challenge input than the one this script was written for,
    and should say so instead of quietly using the first line.
    """
    lines = [line.strip() for line in path.read_text().splitlines()]
    entries = [line for line in lines if line]
    if len(entries) != 1:
        raise ValueError(f"{path.name}: expected 1 non-empty line, found {len(entries)}")
    return entries[0]


CIPHERTEXT = load_ciphertext()


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else CIPHERTEXT
    shift = find_shift(text)
    print(f"shift: {shift}")
    print("FLAG:", caesar(text, shift))
