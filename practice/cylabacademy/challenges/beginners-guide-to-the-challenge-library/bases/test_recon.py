"""Tests for Bases.

The hand-rolled decoder is only worth having if it agrees with the real
one, so the stdlib is the oracle throughout:

  * Correctness against the challenge string.
  * Differential test vs base64.b64decode over every payload length
    0..64 -- this is where padding bugs live, and a decoder tested only
    on one unpadded 20-char string would never see them.
  * Known-bad cases -- a decoder that always returns bytes can't tell
    you that a blob wasn't base64.
  * The 4:3 ratio the whole encoding rests on.

Run either way:
    python3 test_recon.py
    pytest test_recon.py
"""

import base64
import os

from solve import ALPHABET, CIPHERTEXT, b64_decode

PLAINTEXT = b"l3arn_th3_r0p35"
FLAG = "picoCTF{l3arn_th3_r0p35}"


# --------------------------------------------------------------------------
# Correctness against the real challenge string
# --------------------------------------------------------------------------


def test_decodes_the_challenge_string():
    assert b64_decode(CIPHERTEXT) == PLAINTEXT


def test_flag_is_the_decoded_text_in_the_wrapper():
    assert f"picoCTF{{{b64_decode(CIPHERTEXT).decode()}}}" == FLAG


def test_challenge_string_needs_no_padding():
    """20 chars is a multiple of 4, so the encoder had a whole number of
    3-byte groups -- which is why there is no trailing '='."""
    assert len(CIPHERTEXT) % 4 == 0
    assert "=" not in CIPHERTEXT


# --------------------------------------------------------------------------
# Differential test against the stdlib
# --------------------------------------------------------------------------


def test_matches_stdlib_across_every_padding_case():
    """Lengths 0..64 cover each residue mod 3 many times over, so every
    padding case ('', '=', '==') is exercised repeatedly on random data."""
    for n in range(65):
        payload = os.urandom(n)
        encoded = base64.b64encode(payload).decode()
        assert b64_decode(encoded) == payload, f"mismatch at length {n}"


def test_matches_stdlib_on_the_padding_boundaries_explicitly():
    """The three residues, named, so a failure says which case broke."""
    for payload, expected_pad in ((b"abc", 0), (b"ab", 1), (b"a", 2)):
        encoded = base64.b64encode(payload).decode()
        assert encoded.count("=") == expected_pad
        assert b64_decode(encoded) == payload


# --------------------------------------------------------------------------
# Known-bad cases
# --------------------------------------------------------------------------


def _rejects(text, why):
    try:
        b64_decode(text)
        assert False, f"expected ValueError: {why}"
    except ValueError:
        pass


def test_rejects_bad_input():
    _rejects("abcde", "length not a multiple of 4")
    _rejects("ab!d", "'!' is outside the base64 alphabet")
    _rejects("a===", "three padding chars is never valid")


# --------------------------------------------------------------------------
# The property the encoding rests on
# --------------------------------------------------------------------------


def test_four_characters_carry_exactly_three_bytes():
    """lcm(6, 8) = 24 bits = 3 bytes = 4 characters. That ratio is the
    reason padding exists at all, and it fixes the ~33% size overhead."""
    for n_groups in range(1, 20):
        payload = os.urandom(3 * n_groups)
        encoded = base64.b64encode(payload).decode()
        assert len(encoded) == 4 * n_groups
        assert "=" not in encoded


def test_alphabet_is_64_distinct_characters():
    assert len(ALPHABET) == 64 == len(set(ALPHABET))


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
