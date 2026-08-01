# EVEN RSA CAN BE BROKEN???

## Metadata

- Platform: picoGym (picoCTF 2025)
- Category: Cryptography
- Difficulty: Easy
- Status: Solved
- Files: [encrypt.py](encrypt.py), [solve.py](solve.py), [test_recon.py](test_recon.py)
- Skills Learned: RSA internals (modulus parity as a factoring shortcut),
  distinguishing a real vulnerability from a decoy title, testing an
  exploit against a freshly generated instance of the bug, not just one
  capture

## Problem Summary

The service prints textbook RSA output — no padding, `e = 65537` — and
challenges you to decrypt it "with just N & e":

```python
e = 65537

def gen_key(k):
    p, q = get_primes(k // 2)
    N = p * q
    d = inverse(e, (p - 1) * (q - 1))
    return ((N, e), d)

def encrypt(pubkey, m):
    N, e = pubkey
    return pow(bytes_to_long(m.encode('utf-8')), e, N)
```

`get_primes` lives in an undisclosed `setup.py` — not provided. A live
instance (`nc verbal-sleep.picoctf.net 51977`) hands you:

```
N: 21633626737269615521951039144702251856228273557790311610823320576692637632787053852817547102650838958629568629728177764942082801438515481978557887242862578
e: 65537
cyphertext: 14199031501331299946574426394086541776318261200568907273343531853704473146121518433141531851128851636629077412296241554941489648851999973942131698168991625
```

## What I Tried

`e = 65537` rules out the usual "Easy" RSA traps immediately: it's much
too large for a low-public-exponent cube-root attack (that needs `e`
small, like 3), and the 513-bit `N` is far too big to brute-force or
Fermat-factor on the assumption `p ≈ q`. With `get_primes` hidden, the
next move was just to look *at* the numbers instead of assuming a
standard attack family — starting with the cheapest possible check.

## Key Idea

**`N` is even.** Checking `N % 2` costs nothing and it's the whole
challenge: a genuine RSA modulus is a product of two large *odd* primes
and is therefore always odd. This one isn't, which means one of
`get_primes`'s two "primes" is literally `2` — the pun in the title
("EVEN RSA") is the vulnerability, not flavor text.

Once one factor is public knowledge from parity alone, the rest is
textbook RSA decryption, no factoring algorithm required:

```
p = 2,  q = N // 2
phi = (p - 1) * (q - 1) = q - 1
d = e^-1 mod phi
m = c^d mod N
```

## Solution Walkthrough

1. Connect to the live instance and capture `N`, `e`, `cyphertext`.
2. Check `N % 2 == 0` — true, confirming the modulus is exploitable this
   way (`factor_even_modulus` raises instead of guessing if it isn't).
3. Factor trivially: `p = 2`, `q = N // 2`.
4. Compute `phi = q - 1`, `d = pow(e, -1, phi)` (Python's built-in
   modular inverse, no external crypto library needed), decrypt with
   `pow(c, d, N)`, convert the resulting integer back to bytes.

## Exploit / Script

- [solve.py](solve.py) — `python3 solve.py` decrypts the pinned capture
  below; `python3 solve.py HOST PORT` connects to a fresh instance and
  decrypts whatever it returns. Standard library only.
- [test_recon.py](test_recon.py) — 4 tests: 2 correctness against the
  real capture, 1 known-bad case (rejects a modulus that isn't actually
  even), 1 full attack round-trip against an independently generated
  vulnerable key (own from-scratch Miller-Rabin prime generator, not the
  pinned capture) — proof the *attack* generalizes, not just this one N.

## Flag

`picoCTF{tw0_1$_pr!m31c9046c4}`

("two is prime" — `p = 2` is in fact prime; the bug is that it's always
the *same* prime, not that it's an invalid one.)

## Lessons Learned

- **Check the cheapest thing first.** Parity is a one-character check
  and it broke the entire scheme; no need to reach for Fermat
  factorization or a cube-root attack before ruling out something that
  costs nothing to test.
- **A large, standard-looking `e` is not proof the scheme is sound.**
  `e = 65537` defeats the classic *low-exponent* attacks, which is
  exactly why this challenge doesn't hide the bug there — the flaw moved
  to key generation instead. Don't let one closed door imply the house
  is secure.
- **Read the title as a specification, again.** "EVEN RSA CAN BE
  BROKEN???" isn't just tone — "even" is the literal, checkable property
  of the modulus that breaks it. (Same lesson as `autos` → autokey in
  [Too Loud To Yap](../../../events/2025/la-ctf/crypto/too-loud-to-yap/README.md).)
- **Test the exploit against a fresh instance of the bug, not just the
  one capture you happened to get.** `test_recon.py` builds its own
  vulnerable key from scratch (own Miller-Rabin primality test, no
  external dependency) to prove the *attack* is correct, since a test
  that only replays one pinned `(N, e, c)` can't distinguish "the attack
  works" from "I got the arithmetic right once."
