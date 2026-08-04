"""Mod 26 — ROT13 on the provided ciphertext.

The challenge title is the whole hint: everything happens modulo 26, i.e.
a Caesar shift over the alphabet. The given string starts `cvpbPGS{`,
which maps to `picoCTF{` under a shift of 13 — ROT13.

Implemented as a general Caesar so the shift is an argument rather than a
magic constant: a shift-13 special case can't be sanity-checked against
the shift that actually recovers the known `picoCTF{` prefix.

    python3 solve.py            # decode the pinned ciphertext
    python3 solve.py <text>     # decode anything else
"""

import string
import sys

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


CIPHERTEXT = "cvpbPGS{arkg_gvzr_V'yy_gel_2_ebhaqf_bs_ebg13_45559noq}"


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else CIPHERTEXT
    shift = find_shift(text)
    print(f"shift: {shift}")
    print("FLAG:", caesar(text, shift))
