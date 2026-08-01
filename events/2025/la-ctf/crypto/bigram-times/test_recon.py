"""Tests for Bigram Times.

Two kinds live here, deliberately:

  * Correctness — the model reproduces the challenge's ciphertext exactly
    and recovers the flag.
  * Characterisation — the cipher's non-injectivity, which is the entire
    reason the naive brute force (main.py) blows up and why the decoy
    strings in chall.py exist at all.

Run either way:
    python3 test_recon.py
    pytest test_recon.py
"""

from solve import (
    ALSO_NOT_THE_FLAG,
    CHARACTERS,
    NOT_THE_FLAG,
    SHIFTED_FLAG,
    build_reverse_table,
    encrypt_bigram,
    solve,
)

FLAG = "lactf{mULT1pl1cAtiV3_6R0uPz_4rE_9RE77y_5we3t~~~}"


# --------------------------------------------------------------------------
# Correctness
# --------------------------------------------------------------------------


def test_solve_recovers_the_flag():
    assert solve(SHIFTED_FLAG, NOT_THE_FLAG, ALSO_NOT_THE_FLAG) == FLAG


def test_model_reproduces_the_ciphertext_exactly():
    """The real proof. A flag-shaped string is suggestive; re-encrypting to
    the byte-identical ciphertext chall.py printed is conclusive."""
    reconstructed = "".join(
        encrypt_bigram(FLAG[i : i + 2]) for i in range(0, len(FLAG), 2)
    )
    assert reconstructed == SHIFTED_FLAG


def test_decoys_are_not_the_flag():
    """Guards against a solve that accidentally reproduces a decoy instead
    of filtering it out."""
    assert NOT_THE_FLAG != FLAG
    assert ALSO_NOT_THE_FLAG != FLAG


# --------------------------------------------------------------------------
# Characterisation — why disambiguation is needed at all
# --------------------------------------------------------------------------


def test_every_ciphertext_bigram_has_exactly_three_preimages():
    """The cipher maps (a, b) -> (a^2*b, a*b^2) mod 67, and
    a'*b' = (a*b)^3. Since gcd(3, 66) = 3, cubing on the group of nonzero
    residues mod 67 is exactly 3-to-1 — not "at least 2", not "up to 6".
    This is the mechanism the challenge title/hint ("it's not injective")
    is pointing at, and it is why a per-position lookup, not a global
    search, is the right tool."""
    table = build_reverse_table()
    for i in range(0, len(SHIFTED_FLAG), 2):
        candidates = table[SHIFTED_FLAG[i : i + 2]]
        assert len(candidates) == 3, (i, candidates)


def test_decoy_filter_leaves_exactly_one_candidate_per_position():
    """The oracle this solve depends on: removing the two known-decoy
    bigrams from the 3 candidates must leave exactly one survivor, at
    every position, or the "pick the one that isn't a decoy" trick
    doesn't actually determine the flag."""
    table = build_reverse_table()
    decoys = (NOT_THE_FLAG, ALSO_NOT_THE_FLAG)
    for i in range(0, len(SHIFTED_FLAG), 2):
        candidates = table[SHIFTED_FLAG[i : i + 2]]
        remaining = [c for c in candidates if c not in (d[i : i + 2] for d in decoys)]
        assert len(remaining) == 1, (i, candidates, remaining)


def test_brute_force_cartesian_product_would_be_astronomical():
    """Documents why main.py (itertools.product over all per-bigram
    candidates) never finishes: 3 candidates at each of 24 positions is
    3^24 combinations, not a number you enumerate your way out of."""
    assert 3 ** (len(SHIFTED_FLAG) // 2) > 2 * 10**11


def test_reverse_table_covers_the_full_alphabet():
    """Sanity check on the precomputed table itself: every character in
    the 66-symbol alphabet must appear as a valid first (or second) slot
    of some plaintext bigram, or the table was built over the wrong
    domain."""
    table = build_reverse_table()
    seen = {c for bigrams in table.values() for bigram in bigrams for c in bigram}
    assert seen == set(CHARACTERS)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
