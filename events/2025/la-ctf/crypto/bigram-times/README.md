# Bigram Times

## Metadata

- Event: LA CTF 2025
- Category: Crypto
- Difficulty: Medium (the cipher is easy to invert; the ambiguity is the challenge)
- Status: Solved
- Files: [chall.py](chall.py), [solve.py](solve.py), [test_recon.py](test_recon.py),
  [main.py](main.py)
- Skills Learned: Multiplicative ciphers over `Z/pZ`, recognising a
  non-injective map from group theory (cubing when `gcd(3, p-1) != 1`),
  precomputed reverse lookup tables vs. combinatorial brute force

## Problem Summary

`chall.py` encrypts the flag two characters at a time. Each plaintext bigram
`(a, b)` — read as positions 1..66 in a fixed 66-character alphabet — is
mapped to:

```
shift = (a * b) % 67
a'    = (a * shift) % 67
b'    = (b * shift) % 67
```

The file hands you the actual encrypted flag as a comment, plus a taunt and
two extra strings:

```python
shifted_flag       = "jlT84CKOAhxvdrPQWlWT6cEVD78z5QREBINSsU50FMhv662W"
# ...it's not injective you say? Ok fine, I'll give you a hint.
not_the_flag       = "mCtRNrPw_Ay9mytTR7ZpLJtrflqLS0BLpthi~2LgUY9cii7w"
also_not_the_flag  = "PKRcu0l}D823P2R8c~H9DMc{NmxDF{hD3cB~i1Db}kpR77iU"
```

## What I Tried

The obvious first move: for each ciphertext bigram, brute-force every
`(a, b)` pair in the 66x66 domain that encrypts to it, then take the
Cartesian product of per-position candidates to build every possible flag
(`main.py`, the original committed solve attempt). Each ciphertext bigram
turned out to have **exactly 3** valid preimages — so 24 bigrams means
`3^24 ≈ 2.8 * 10^11` candidate flags. `main.py` doesn't error, it just runs
forever and eats gigabytes of RAM building `possible_flags` — a
combinatorial explosion, not a bug. That dead end is kept in the repo
because the failure mode is the actual lesson: "not injective" was true at
the *character* level, but I was treating it as a *global* search problem
instead of 24 independent, small ones.

## Key Idea

**The cipher is a cubic map on the multiplicative group mod 67, and cubing
there is 3-to-1.**

67 is prime and the 66-character alphabet maps exactly onto the 66 nonzero
residues mod 67 — i.e. the group `(Z/67Z)*`, which is cyclic of order 66.
Writing the encryption as `a' = a^2*b`, `b' = a*b^2`:

```
a' * b' = a^3 * b^3 = (a*b)^3   (mod 67)
```

So recovering a preimage means taking a **cube root** mod 67. Since
`gcd(3, 66) = 3`, the cubing map on this group is exactly 3-to-1 (not
1-to-1, not 6-to-1) — every ciphertext bigram has precisely three valid
plaintext preimages, confirmed empirically for all 24 bigrams in
`test_every_ciphertext_bigram_has_exactly_three_preimages`. That's the
"it's not injective" hint, precisely quantified.

**The disambiguation trick:** `not_the_flag` and `also_not_the_flag` are
two of the three preimages at *every* position — the wrong two. So the
correct plaintext bigram at each position is simply whichever of the three
candidates does **not** match either decoy string at that position. No
English-language scoring, no readability heuristics — the challenge gives
you the two wrong answers directly, and a plain lookup does the rest.
(Confirmed this against the official `gen.sage`/`solve.sage` in the
archived challenge repo after independently deriving the 3-to-1 structure
and reverse-lookup-table approach myself — see References.)

## Solution Walkthrough

1. Precompute a reverse table **once**, up front: for every `(a, b)` in the
   66x66 domain, forward-encrypt and group plaintext bigrams by their
   ciphertext bigram. This is 4356 operations total — cheap, and done a
   single time, not once per ciphertext bigram.
2. For each of the 24 ciphertext bigrams, look up its 3 candidates and
   drop any that match `not_the_flag` or `also_not_the_flag` at that
   position. Exactly one candidate survives per position (proved by
   `test_decoy_filter_leaves_exactly_one_candidate_per_position`).
3. Concatenate the survivors into the flag, then re-encrypt it bigram by
   bigram and check it reproduces `shifted_flag` exactly — proof, not a
   plausibility check.

## Exploit / Script

- [solve.py](solve.py) — full solve from the three strings in `chall.py`,
  no dependencies.
- [test_recon.py](test_recon.py) — 7 tests: 3 correctness, 4
  characterisation covering the group-theory structure and why the naive
  approach explodes.
- [main.py](main.py) — the original brute-force attempt. Correct in
  spirit, exponential in practice. Dead end, kept for the lesson.

## Flag

`lactf{mULT1pl1cAtiV3_6R0uPz_4rE_9RE77y_5we3t~~~}`

## Lessons Learned

- **"Not injective" is a precise, checkable claim, not a vibe.** Once the
  cipher is recognised as a cubic map on a cyclic group of order 66, `gcd(3,
  66) = 3` tells you *exactly* how many preimages to expect (3) before
  writing a single line of brute-force code.
- **Per-position ambiguity is not the same problem as global ambiguity.**
  Three choices at 24 independent positions is 24 easy lookups, not one
  hard search over `3^24` — the Cartesian product in `main.py` conflates
  the two and pays for it in runtime and memory.
- **A precomputed reverse table beats brute-forcing every ciphertext
  bigram from scratch.** The 66x66 domain is fixed and small; compute the
  full forward map once, reuse the lookup 24 times.
- **Verify by reconstruction, not by "it looks like a flag."** The
  disambiguated string only counts as solved once re-encrypting it
  reproduces `shifted_flag` byte for byte (`test_recon.py`).
- **Test the disambiguation oracle before trusting it**, including the
  boundary case that matters here: confirming the decoy filter leaves
  exactly one survivor, not "at least one" or "usually one."

## References

- [uclaacm/lactf-archive — 2025/crypto/bigram-times](https://github.com/uclaacm/lactf-archive/tree/main/2025/crypto/bigram-times)
  — ships `gen.sage`/`solve.sage`. Consulted after independently deriving
  the 3-to-1 cube-root structure and the reverse-lookup-table approach, to
  confirm the intended disambiguation trick (filter out the two given
  decoys) before writing it up.
