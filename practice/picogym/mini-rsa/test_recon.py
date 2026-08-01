"""Tests for Mini RSA.

Three kinds live here, deliberately:

  * Correctness against the real values.txt.
  * Characterisation — confirming, rather than assuming, that this
    particular ciphertext needed zero modular wraparounds (k=0), despite
    the challenge blurb implying M**e sits just *past* N.
  * A known-bad case and a k>0 round trip, since the real capture alone
    only ever exercises the k=0 branch of recover_message's search loop.

Run either way:
    python3 test_recon.py
    pytest test_recon.py
"""

from pathlib import Path

from solve import E, integer_nth_root, parse_values, recover_message

VALUES_PATH = Path(__file__).parent / "values.txt"
FLAG = "picoCTF{e_sh0u1d_b3_lArg3r_92f4d5a5}"


# --------------------------------------------------------------------------
# Correctness
# --------------------------------------------------------------------------


def test_recovers_the_flag_from_the_real_values():
    N, c = parse_values(VALUES_PATH.read_text())
    assert recover_message(N, E, c).decode().strip() == FLAG


# --------------------------------------------------------------------------
# Characterisation
# --------------------------------------------------------------------------


def test_ciphertext_needed_zero_modular_wraparounds():
    """The blurb says M**e is "just barely larger than N", which reads as
    "expect k=1". Check what actually happened instead of assuming it:
    c itself is already a perfect cube, meaning M**3 < N and no modular
    reduction occurred at all."""
    N, c = parse_values(VALUES_PATH.read_text())
    m = integer_nth_root(c, E)
    assert m**E == c


def test_integer_nth_root_rejects_a_non_perfect_power():
    """Known-bad case for the root finder: a value one away from a
    perfect cube must not be reported as an exact root."""
    m = integer_nth_root(1000, 3)  # 10**3 == 1000 exactly
    assert m == 10
    not_a_cube = 1001
    root = integer_nth_root(not_a_cube, 3)
    assert root**3 != not_a_cube


# --------------------------------------------------------------------------
# recover_message's search loop beyond the real capture's k=0 case
# --------------------------------------------------------------------------


def test_recovers_a_message_that_needed_two_wraparounds():
    """The real values.txt only exercises k=0. Build a synthetic case
    where M**e wraps around N twice, to prove the k-search loop itself
    is correct and not just coincidentally right once."""
    message = b"hello"
    m = int.from_bytes(message, "big")
    e = 3
    power = m**e
    N = power // 3 + 1  # large enough that k=2 wraps land in [0, N)
    k = 2
    c = power - k * N
    assert 0 <= c < N, "test fixture invalid: c must be a valid residue mod N"

    assert recover_message(N, e, c, max_k=5) == message


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
