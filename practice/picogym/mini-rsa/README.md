# Mini RSA

## Metadata

- Platform: picoGym (picoCTF 2021)
- Category: Cryptography
- Difficulty: Medium
- Status: Solved
- Files: [values.txt](values.txt), [solve.py](solve.py), [test_recon.py](test_recon.py)
- Skills Learned: Low-public-exponent RSA attack (e=3), integer nth-root
  recovery, checking a stated assumption instead of trusting the blurb

## Problem Summary

> What happens if you have a small exponent? There is a twist though, we
> padded the plaintext so that `(M ** e)` is just barely larger than N.
> Let's decrypt this.

`values.txt` provides a ~3000-bit `N`, `e = 3`, and a ciphertext `c`.
No private key, no server — just those three numbers.

## What I Tried

`e = 3` is the classic low-public-exponent red flag: with no OAEP-style
padding, `c = M**e mod N`. If the message `M` is small enough that
`M**e` never reaches `N`, there's no modular reduction at all — `c` is
literally `M**e` over the integers, and recovering `M` is just an
integer cube root. The blurb's "padded so that `M**e` is just barely
larger than N" reads like it's daring you to expect exactly one
wraparound (`c = M**e - N`), so the natural move was to check that
first, then generalize instead of assuming.

## Key Idea

**With a small `e`, the only thing standing between "trivial cube root"
and "needs the private key" is whether `M**e` overflows the modulus at
all.** If it overflows `k` times, `M**e = c + k*N` for that `k`, so
searching `k = 0, 1, 2, ...` for the first value where `c + k*N` is a
perfect `e`-th power finds `M` directly — no factoring, no `d`.

**What actually happened here surprised me relative to the blurb:**
`c` itself is already a perfect cube (`k = 0`), meaning `M**3 < N` with
*zero* wraparounds — not the "just barely larger than N" the challenge
text suggests. `test_ciphertext_needed_zero_modular_wraparounds` checks
this directly rather than assuming the blurb's framing was the literal
mechanism. The lesson generalizes better than the specific number would:
write the attack as a search over `k`, not a hardcoded `c + N`, so it
doesn't silently depend on which case you happened to get.

## Solution Walkthrough

1. Parse `N` and `c` out of `values.txt`; `e = 3` is given directly.
2. Try `k = 0, 1, 2, ...`: for each, compute `target = c + k*N` and take
   its integer cube root via binary search (no external big-int math
   library needed — Python's arbitrary-precision `int` is enough).
3. Stop at the first `k` where `root**3 == target` exactly — that root
   is `M`. Here that's `k = 0`.
4. Convert `M` back to bytes; the decoded plaintext is left-padded with
   literal space characters (`0x20`), not null bytes — strip and read
   off the flag.

## Exploit / Script

- [solve.py](solve.py) — `python3 solve.py`, standard library only.
- [test_recon.py](test_recon.py) — 4 tests: 1 correctness against the
  real `values.txt`, 1 characterisation (confirms `k=0` rather than
  assuming the blurb's `k=1` framing), 1 known-bad case for the root
  finder, 1 synthetic round-trip that forces `k=2` — since the real
  capture only ever exercises the `k=0` branch, this is the only thing
  that actually tests the search loop.

## Flag

`picoCTF{e_sh0u1d_b3_lArg3r_92f4d5a5}`

## Lessons Learned

- **A small `e` is the entire vulnerability once there's no padding
  scheme.** `e = 3` and an unpadded message turns RSA decryption into an
  integer root-finding problem — the "hard" direction of RSA (factoring
  `N`, computing `d`) never has to be touched.
- **Verify the challenge's own framing instead of coding to it
  literally.** The blurb suggested one wraparound; the actual ciphertext
  needed zero. Writing `recover_message` as a bounded search over `k`
  rather than hardcoding `c + N` meant the "surprise" cost nothing to
  handle — and the characterisation test now documents what's actually
  true about this capture instead of what the prompt implied.
- **Watch for padding that isn't null bytes.** The recovered plaintext
  was left-padded with literal spaces (`0x20`), not zero bytes — a
  `.decode().strip()` away from the flag, but worth noticing rather than
  being confused by leading whitespace in the output.
- **Test the part of the algorithm the real data doesn't exercise.** The
  actual capture only exercises `k=0` in the search loop; without a
  synthetic `k=2` case, the loop's upper branches would be unverified
  code, not verified-and-unused code.
