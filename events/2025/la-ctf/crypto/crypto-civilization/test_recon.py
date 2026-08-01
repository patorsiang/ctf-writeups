"""Tests for Crypto Civilization.

Three kinds live here, deliberately:

  * Correctness of the equivocation finder itself — including a
    known-bad case, since an oracle that only ever returns "yes" is not
    the same as one that correctly says "no" when no answer exists.
  * Characterisation — the birthday-bound math behind "roughly a third
    of rounds are equivocable", measured empirically rather than just
    trusted from theory.
  * A full integration run against the real chall.py, which is the only
    way to prove the protocol-framing (recvuntil boundaries, prompt
    parsing) is actually right and not just plausible in isolation.

Run either way:
    python3 test_recon.py
    pytest test_recon.py
"""

from pathlib import Path

from solve import PASS_THRESHOLD, ROUNDS, build_prg_table, find_equivocation, play, prg, xor_bytes

FLAG = "lactf{na0r_c0mm1tm3nt_sch3m3_but_wr0ng}"
CHALL_DIR = Path(__file__).parent


# --------------------------------------------------------------------------
# Correctness of the equivocation finder
# --------------------------------------------------------------------------


def test_finds_a_planted_equivocation():
    """Craft y from two known seeds; the finder must recover *some* valid
    pair for it (not necessarily the same seeds — PRG collisions mean
    other pairs may also satisfy y, and any valid one is fine)."""
    table = build_prg_table()
    s0, s1 = (7).to_bytes(2, "big"), (99).to_bytes(2, "big")
    y = xor_bytes(prg(s0), prg(s1))

    result = find_equivocation(y, table)
    assert result is not None
    com, found_s0, found_s1 = result
    assert prg(found_s0) == com
    assert xor_bytes(prg(found_s1), y) == com


def test_returns_none_when_no_equivocation_exists():
    """The known-bad case: shrink the table to two seeds whose PRG outputs
    cannot possibly XOR to an arbitrary y, and confirm the finder reports
    failure instead of returning a bogus pair. Guards against an oracle
    that's only ever tested on cases where the answer is yes."""
    tiny_table = {prg(b"\x00\x00"): b"\x00\x00", prg(b"\x00\x01"): b"\x00\x01"}
    impossible_y = b"\xff\xff\xff\xff"
    assert find_equivocation(impossible_y, tiny_table) is None


# --------------------------------------------------------------------------
# Characterisation — the birthday bound
# --------------------------------------------------------------------------


def test_equivocation_rate_matches_the_birthday_bound():
    """PRG's image has 2**16 points in a 2**32 codomain. The expected
    number of *unordered* pairs (s0, s1) with PRG(s0) XOR PRG(s1) == y is
    (2**16 choose 2) / 2**32 ~= 0.5 for a uniform nonzero y, so treating
    solvability as Poisson(0.5) predicts P(a solution exists) =
    1 - e^-0.5 ~= 0.393. Assert the empirical rate over many random y
    lands near that, not near the naive (and wrong) 1 - e^-1 ~= 0.632
    that comes from double-counting ordered pairs."""
    import os

    table = build_prg_table()
    trials = 1500
    hits = sum(find_equivocation(os.urandom(4), table) is not None for _ in range(trials))
    rate = hits / trials
    assert 0.30 < rate < 0.48, rate


# --------------------------------------------------------------------------
# Integration — the real protocol
# --------------------------------------------------------------------------


def test_full_protocol_run_recovers_the_flag():
    """The actual proof: play the full 200-round protocol against the
    unmodified chall.py and recover the flag it prints. The game itself
    is probabilistic (~86% win rate per session per the birthday-bound
    math above, not 100%), so retry a few times rather than pretend a
    single run is deterministic -- failing 3 independent ~86%-likely
    rounds in a row is itself a ~0.3% event, which is an acceptable test
    flake rate, and nothing about the retry changes what's being proven."""
    for attempt in range(3):
        correct, equivocated, tail = play(rounds=ROUNDS, chall_dir=CHALL_DIR)
        if correct > PASS_THRESHOLD:
            break
    else:
        raise AssertionError(f"failed to clear {PASS_THRESHOLD}/200 in 3 attempts")

    assert correct > PASS_THRESHOLD
    assert FLAG in tail


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
