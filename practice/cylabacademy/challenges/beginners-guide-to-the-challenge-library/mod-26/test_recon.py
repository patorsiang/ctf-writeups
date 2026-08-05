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
import tempfile
from pathlib import Path

from solve import CIPHERTEXT, VALUES_FILE, caesar, find_shift, load_ciphertext, rot13

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
# values.txt is the single source of the ciphertext
# --------------------------------------------------------------------------


def test_ciphertext_comes_from_values_file():
    """CIPHERTEXT is read from disk, not duplicated as a literal here."""
    assert VALUES_FILE.exists(), f"{VALUES_FILE} is the input; it must be committed"
    assert load_ciphertext() == CIPHERTEXT


def test_values_file_drift_is_caught_by_the_flag_assertion():
    """The mechanism that makes a single source *stay* single: edit
    values.txt and test_rot13_recovers_the_flag fails. Proven here by
    feeding the loader a corrupted copy and checking it no longer
    decodes to the flag."""
    with tempfile.TemporaryDirectory() as tmp:
        corrupted = Path(tmp) / "values.txt"
        corrupted.write_text(CIPHERTEXT.replace("cvpb", "xxxx") + "\n")
        assert rot13(load_ciphertext(corrupted)) != FLAG


def test_loader_ignores_blank_lines_and_trailing_newline():
    """The real values.txt ends with a newline; that must not become a
    second entry or leave trailing whitespace on the ciphertext."""
    with tempfile.TemporaryDirectory() as tmp:
        padded = Path(tmp) / "values.txt"
        padded.write_text(f"\n  {CIPHERTEXT}  \n\n")
        assert load_ciphertext(padded) == CIPHERTEXT


def test_loader_rejects_a_file_with_two_entries():
    """Two lines means a different challenge input than this script was
    written for -- say so rather than silently taking the first."""
    with tempfile.TemporaryDirectory() as tmp:
        two = Path(tmp) / "values.txt"
        two.write_text(f"{CIPHERTEXT}\nsome_other_ciphertext\n")
        try:
            load_ciphertext(two)
            assert False, "expected ValueError for a two-entry file"
        except ValueError:
            pass


def test_loader_rejects_an_empty_file():
    with tempfile.TemporaryDirectory() as tmp:
        empty = Path(tmp) / "values.txt"
        empty.write_text("\n\n")
        try:
            load_ciphertext(empty)
            assert False, "expected ValueError for an empty file"
        except ValueError:
            pass


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
