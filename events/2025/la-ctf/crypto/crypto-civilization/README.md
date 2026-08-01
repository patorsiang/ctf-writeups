# Crypto Civilization

## Metadata

- Event: LA CTF 2025
- Category: Crypto
- Difficulty: Medium (the flaw is a one-line protocol ordering mistake;
  exploiting it needs a birthday attack)
- Status: Solved
- Files: [chall.py](chall.py), [solve.py](solve.py),
  [test_recon.py](test_recon.py), [main.py](main.py), [Dockerfile](Dockerfile)
  (`flag.txt` is required alongside `chall.py` to run locally — see
  Solution Walkthrough — but is gitignored repo-wide and not committed)
- Skills Learned: Bit-commitment schemes (Naor's construction), birthday
  attacks against PRG image sparsity, equivocation as a binding-property
  break, local challenge reproduction via subprocess

## Problem Summary

`chall.py` runs 200 rounds of a commit-and-open game framed as "commit the
chicken or the beef":

1. The server sends a fresh random 4-byte `y`.
2. You send a 4-byte commitment `com` (hex).
3. The server picks a random bit — chicken (0) or beef (1) — and asks you
   to open it: reveal a 2-byte `decom`.
4. It checks:
   - chicken: `PRG(decom) == com`
   - beef: `PRG(decom) XOR y == com`

where `PRG` stretches a 2-byte seed to 4 bytes via `sha3_256(seed)[:4]`.
Pass more than 132/200 rounds and it prints the flag.

This is a textbook **Naor bit-commitment scheme** (commit via a PRG,
open by revealing the seed), and the flag literally says so:
`na0r_c0mm1tm3nt_sch3m3_but_wr0ng`.

## What I Tried

The `main.py` already sitting in this folder (a naive first attempt, kept
as a documented dead end) plays *honestly*: pick a random 4-byte `com`,
and hope it happens to be `PRG(s)` for some known seed `s` so either
branch can be opened correctly. It can't — `PRG`'s image only has `2**16`
points inside a `2**32` codomain, so a uniformly random 4-byte string
lands in the image with probability `2**-16`. That script is a KeyError
waiting to happen, and it also targets `chall.lac.tf`, which is no longer
up now that the event is long over. Both problems needed fixing before
anything could be tested.

## Key Idea

**A sound bit commitment must bind you to one branch before you learn the
challenge. Here you learn `y` — the beef branch's parameter — *before*
you have to commit at all**, which means you don't have to actually
decide what you're committing to.

If you can find two seeds `s0, s1` with:

```
PRG(s0) == PRG(s1) XOR y
```

then committing `com = PRG(s0)` opens **either** way: reveal `s0` for
chicken (`PRG(s0) == com`, trivially true), or reveal `s1` for beef
(`PRG(s1) XOR y == com`, true by construction). The commitment never
actually committed you to a bit — that's what "wrong commitment scheme"
means concretely.

**Whether such a pair exists is a birthday question.** Rearranging:
`PRG(s0) XOR PRG(s1) == y`. Over the `2**16`-point image, the expected
number of *unordered* pairs whose outputs XOR to a fixed nonzero `y` is
`C(2**16, 2) / 2**32 ≈ 0.5`. Modelling existence as Poisson(0.5) predicts
`P(a solution exists) = 1 - e^-0.5 ≈ 0.393` — confirmed empirically at
`0.395` over 3000 random `y` in `test_equivocation_rate_matches_the_birthday_bound`.
(The naive `1 - e^-1 ≈ 0.632` from treating *ordered* pairs as
independent Poisson trials over-counts, since `(s0, s1)` and `(s1, s0)`
aren't independent events.)

When no pair exists (roughly 60% of rounds), fall back to an honest
chicken-only commitment: guaranteed win if chicken is asked, a coin flip
if beef is asked. Combined expected per-round win rate is
`0.393*1 + 0.607*0.5 ≈ 0.70`, comfortably above the `133/200 ≈ 0.665`
bar — Monte Carlo simulation of full 200-round sessions puts the overall
pass probability at **~86%**, which matches winning on the first real run
(134/200).

## Solution Walkthrough

1. Precompute every seed's `PRG` output once, up front: `2**16`
   evaluations of truncated SHA3-256, reused for all 200 rounds.
2. Each round, search that table for `(s0, s1)` with
   `PRG(s0) XOR PRG(s1) == y` — `O(2**16)` dict lookups per round using
   the precomputed table, no repeated hashing.
3. Commit `PRG(s0)`. Whichever branch is challenged, reveal the seed that
   opens it (`s0` for chicken, `s1` for beef); if no pair was found,
   reveal `s0` for chicken and accept the coin flip on beef.
4. Play all 200 rounds against a locally spawned `chall.py` (the archived
   remote is unreachable) and read the flag off its final stdout. This
   needs a `flag.txt` next to `chall.py` — gitignored repo-wide, so drop
   the real flag (below) into a local `flag.txt` before running.

The interactive part has a smaller trap of its own: `chall.py`'s
`input("> ")` prompts aren't newline-terminated, so a naive
`readline()`-based client hangs forever waiting for a newline that never
arrives. `solve.py`'s `Recvuntil` scans byte-by-byte for arbitrary
delimiters instead of assuming line framing.

## Exploit / Script

- [solve.py](solve.py) — full solve against a local `chall.py`, standard
  library only (no pwntools).
- [test_recon.py](test_recon.py) — 4 tests: 2 correctness (including a
  known-bad case for the equivocation finder), 1 characterisation of the
  birthday-bound math, 1 full-protocol integration run.
- `flag.txt` — not committed (gitignored repo-wide); create it locally
  with the flag below so `chall.py` runs exactly as it did on the
  original server.
- [main.py](main.py) — the original honest-protocol attempt against the
  live server. Dead end, kept for the lesson.

## Flag

`lactf{na0r_c0mm1tm3nt_sch3m3_but_wr0ng}`

## Lessons Learned

- **Commitment schemes must bind before the challenge is known.** The
  entire break exists because `y` — needed for the beef branch — is
  revealed before the commitment is requested. Reordering those two lines
  in `chall.py` would close the hole entirely; no amount of PRG strength
  fixes a protocol ordering mistake.
- **A PRG's image size, not its output length, bounds commitment
  security here.** `2**16` seeds into a `2**32` codomain is a sparse
  image — sparse enough that birthday-style collisions across two
  independent evaluations become findable via meet-in-the-middle rather
  than needing `2**32` brute force.
- **Get the expected-count math right, not just "roughly 50/50."**
  Ordered vs. unordered pair counting changes the predicted rate from
  63% to 39% — a 24-point difference that would have made the fallback
  strategy's win-rate arithmetic wrong, and it's a one-line correction
  once you notice `(s0,s1)` and `(s1,s0)` are the same discovery.
- **A probabilistic exploit needs a probabilistic test, run honestly.**
  The game's own pass bar isn't 100%-achievable by design (~86% per
  session here), so the integration test retries a bounded number of
  times and says so in a comment — rather than either flaking silently
  or laundering randomness into a false "deterministic" assertion.
- **Local reproduction via subprocess beats waiting on a dead server.**
  The archived `chall.lac.tf` connection in the original `main.py` is
  permanently gone; running `chall.py` itself locally (with the real
  `flag.txt` alongside it) reproduces the exact protocol without needing
  the network at all.

## References

- [uclaacm/lactf-archive — 2025/crypto/crypto-civilization](https://github.com/uclaacm/lactf-archive/tree/main/2025/crypto/crypto-civilization)
  — ships the real `flag.txt` and the author's own `solve.py`, which uses
  the identical PRG-collision equivocation attack. Consulted after
  independently deriving the birthday-bound break, to confirm the
  intended mechanism and recover the real flag for local reproduction
  (the live server is gone).
