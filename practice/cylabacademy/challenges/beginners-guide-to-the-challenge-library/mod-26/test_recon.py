"""Tests for Mod 26.

Three kinds live here:

  * Correctness against the real challenge string.
  * A known-bad case for find_shift -- a shift finder that only ever
    succeeds isn't proof it would notice a non-Caesar ciphertext.
  * The structural property the flag text jokes about: ROT13 is an
    involution, so "2 rounds of rot13" is the identity map.

Run either way:
    python3 test_recon.py
    pytest test_recon.py
"""

import string

from solve import CIPHERTEXT, caesar, find_shift, rot13

FLAG = "picoCTF{next_time_I'll_try_2_rounds_of_rot13_45559abd}"


# --------------------------------------------------------------------------
# Correctness against the real challenge string
# --------------------------------------------------------------------------


def test_rot13_recovers_the_flag():
    assert rot13(CIPHERTEXT) == FLAG


def test_recovered_shift_is_13():
    """Derived from the `picoCTF{` crib, not assumed."""
    assert find_shift(CIPHERTEXT) == 13


def test_non_letters_pass_through():
    """Braces, digits, the apostrophe and underscores are outside the
    mod-26 alphabet, so they must survive the shift unchanged."""
    assert rot13("{_'2_45559}") == "{_'2_45559}"


# --------------------------------------------------------------------------
# Known-bad case for the shift finder
# --------------------------------------------------------------------------


def test_find_shift_rejects_text_no_shift_can_fix():
    """A ciphertext no rotation maps to the crib must raise, not return a
    plausible-looking wrong shift."""
    try:
        find_shift("9999999999")
        assert False, "expected ValueError for a non-Caesar ciphertext"
    except ValueError:
        pass


# --------------------------------------------------------------------------
# The property the flag is joking about
# --------------------------------------------------------------------------


def test_rot13_is_an_involution():
    """13 + 13 = 26 = 0 mod 26. Two rounds of ROT13 is the identity, so
    the flag's "next time I'll try 2 rounds of rot13" would encrypt
    nothing at all."""
    for sample in (CIPHERTEXT, FLAG, string.ascii_letters):
        assert rot13(rot13(sample)) == sample


def test_caesar_shifts_compose_mod_26():
    """The general claim behind the involution: shifting by a then b is
    the same as shifting once by (a + b) mod 26."""
    sample = string.ascii_letters
    for a in range(26):
        for b in range(26):
            assert caesar(caesar(sample, a), b) == caesar(sample, (a + b) % 26)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
