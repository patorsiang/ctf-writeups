"""Bases — base64 decode, implemented as bit regrouping.

`base64.b64decode` solves this in one line. This file implements the
decode by hand instead, because the *mechanism* is the lesson: base64 is
the same "regroup the bitstream" trick as octal and hex, just with a
different group size.

    3 bits -> 1 octal digit
    4 bits -> 1 hex digit
    6 bits -> 1 base64 character

Decoding is therefore: map each character to its 6-bit index, concatenate
into one bitstream, re-slice into 8-bit bytes.

    python3 solve.py            # decode the challenge string
    python3 solve.py <text>     # decode anything else
"""

import string
import sys

# Index in this string *is* the 6-bit value of the character. This exact
# order (A-Z, a-z, 0-9, +, /) is what makes it "standard" base64; the
# URL-safe variant differs only in the last two.
ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits + "+/"
PAD = "="


def b64_decode(text: str) -> bytes:
    """Decode standard base64 by regrouping 6-bit units into 8-bit bytes.

    Rejects malformed input rather than silently returning partial output:
    a decoder that always produces *something* can't tell you that a blob
    wasn't base64 in the first place.
    """
    stripped = text.rstrip(PAD)
    padding = len(text) - len(stripped)

    if len(text) % 4 != 0:
        raise ValueError(f"length {len(text)} is not a multiple of 4")
    if padding > 2:
        raise ValueError(f"{padding} padding chars; standard base64 allows at most 2")
    for ch in stripped:
        if ch not in ALPHABET:
            raise ValueError(f"{ch!r} is not in the base64 alphabet")

    bits = "".join(f"{ALPHABET.index(ch):06b}" for ch in stripped)
    # Each padding char stood in for 6 bits that carry no data; the
    # leftover bits at the tail are zero-fill, not part of any byte.
    usable = len(bits) - (len(bits) % 8)
    return bytes(int(bits[i : i + 8], 2) for i in range(0, usable, 8))


CIPHERTEXT = "bDNhcm5fdGgzX3IwcDM1"


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else CIPHERTEXT
    decoded = b64_decode(text).decode()
    print(f"{len(text)} chars -> {len(decoded)} bytes")
    print("FLAG:", f"picoCTF{{{decoded}}}")
