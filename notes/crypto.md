# Crypto Notes

## Beginner Checklist

- Identify whether data is encoded, encrypted, hashed, or compressed.
- Check common encodings first: hex, base64, URL encoding, ASCII, binary.
  Identify them by alphabet and length before opening a tool — see the
  table in [general.md](general.md#identifying-an-encoded-blob-by-alphabet-and-length).
  Encoding has no key and is not a finding; decode it and keep going.
- For RSA, record `n`, `e`, ciphertexts, and any relationship between exponents or moduli.
- For oracle challenges, write down exactly what the service reveals and what input you control.
- **Read the challenge description and title as a specification.** Authors hide
  the mechanism in wordplay — "a story about *autos*" meant autokey.

## Classical Ciphers: Triage Order

Work down this list; each step cheaply eliminates a family.

1. **Character set.** Digits or `+/=` → encoding problem, not a cipher.
2. **Structure preserved?** If word lengths, spaces and punctuation survive,
   letters map to letters in place. Rules out transposition and block ciphers —
   you are in the substitution family.
3. **Same word, same ciphertext?** If a repeated plaintext word enciphers
   identically, it is monoalphabetic (Caesar, keyed substitution) → frequency
   analysis. If it differs by position, it is polyalphabetic → frequency
   analysis is useless and will hand you a flat, uninformative histogram.
4. **Index of coincidence, split into `k` columns.** English ≈ 0.066,
   random ≈ 0.038. A peak at some `k` gives the repeating key length.

```python
def ic(s):
    n = len(s)
    return sum(v * (v - 1) for v in Counter(s).values()) / (n * (n - 1))

def avg_column_ic(s, k):        # peak here => key length k
    return sum(ic(s[i::k]) for i in range(k)) / k
```

5. **Flat IC at every `k`?** That is a *result*, not a failure: the key does not
   repeat. Go to running key / autokey. Note IC needs roughly 20+ letters per
   column to mean anything — with a 500-letter sample, `k > 25` is untestable,
   so "no period found" only covers the range you actually had power to test.

## Caesar / ROT13 — Read the Shift Off a Crib

The cheapest branch of step 3. If the cipher is monoalphabetic *and* the
challenge format hands you a known prefix (CTF flags almost always do —
`picoCTF{`, `flag{`), don't guess the key and don't reach for frequency
analysis on a 50-character string. Line the crib up and subtract:

```python
shift = (ord(ct[0]) - ord(crib[0])) % 26   # verify across the whole crib
```

Confirm the *same* offset holds for every crib character. If it doesn't,
that's the signal it isn't a Caesar at all — a real answer, arrived at in
one step. Brute-forcing all 26 keys works too and costs nothing; the point
is that "it's probably ROT13" is a guess, while the crib is a derivation.

**ROT13 is an involution.** `13 + 13 ≡ 0 (mod 26)`, so encode and decode
are the same operation and applying it twice returns the input untouched.
More generally, Caesar shifts compose additively — `shift(a)` then
`shift(b)` equals `shift(a+b mod 26)`. Composing a cipher with itself is
not automatically stronger, and for an involution it is exactly the
identity. Seen in
[Mod 26](../practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/mod-26/README.md),
whose flag jokes about "2 rounds of rot13".

Watch the alphabet boundary: only `A-Za-z` participate in mod-26
arithmetic. Braces, digits, underscores and punctuation must pass through
untouched, which is exactly why the flag's shape survives and gives you
the crib in the first place.

## Autokey — the one worth memorising

`key = PRIMER + plaintext`, so `ct[i] = pt[i] + pt[i - len(PRIMER)]`.

No period exists, so every classical periodicity attack fails by construction.
But it is *weaker* than Vigenère against a known primer: each recovered letter
becomes a key letter further along, so the whole message unravels from the
primer alone.

**The attack is: find the primer, not break the key.** A short primer is
brute-forceable (26^5 is large, but n-gram scoring on the first ~40 letters
prunes it instantly). Better, look for somewhere the plaintext is known — any
run of `A` in the plaintext contributes a zero shift, so the ciphertext there is
the raw key.

```python
def decrypt(ct, primer):
    pt = []
    for i, c in enumerate(ct):
        k = primer[i] if i < len(primer) else pt[i - len(primer)]
        pt.append(chr((ord(c) - ord(k)) % 26 + ord("a")))
    return "".join(pt)
```

## Crib Dragging

When you have known plaintext, subtract it from the ciphertext at the candidate
position: `key = ct - pt (mod 26)`. Slide the crib along and keep positions
where the result looks like language.

Two traps, both hit in [Too Loud To Yap](../events/2025/la-ctf/crypto/too-loud-to-yap/README.md):

- **Alignment.** Cribs spanning word boundaries need reordering to the reading
  order first. Fed in wrong, they produce junk that looks like a dead end.
- **Confirmation bias.** Five-letter fragments *will* look like English if you
  want them to. `overy` reads as "o very" and `hewas` as "he was", while
  `cubgle` and `sabhma` get quietly written off as misalignment. Score
  candidates with n-gram statistics, not by eye.

## Multiplicative Ciphers mod p — Counting Preimages Before Brute-Forcing

When a cipher raises characters to a power mod a prime `p` (or otherwise
applies a fixed exponent map on `(Z/pZ)*`, the group of nonzero residues,
which is cyclic of order `p-1`), check `gcd(exponent, p-1)` **before**
writing any search code:

- `gcd = 1` → the map is a bijection (injective), unique decryption.
- `gcd = d > 1` → the map is exactly `d`-to-1. Every output has precisely
  `d` valid preimages — not "some", not "up to `d`", exactly `d`. This is
  a group-theory fact, checkable by hand in one line, not something to
  discover by brute-forcing and being surprised at the count.

**Why this matters operationally:** ambiguity at *each* symbol is cheap
(`d` candidates, `d` small); ambiguity across a whole message is not, if
you combine per-symbol candidates with a Cartesian product. `d` candidates
at `n` independent positions is `d^n` combined guesses — solve each
position's ambiguity locally (a per-symbol disambiguator, a known
crib, a decoy the challenge hands you) and never materialize the full
product. Hit this exactly in
[Bigram Times](../events/2025/la-ctf/crypto/bigram-times/README.md): cubing
mod 67 is 3-to-1 since `gcd(3, 66) = 3`, and the naive Cartesian-product
solve (`3^24` candidates) exhausts memory instead of finishing.

**Practical move:** precompute a reverse lookup table over the whole
(small) input domain *once* — brute-forcing every possible input, grouping
by output — rather than re-deriving preimages per ciphertext symbol. The
domain is fixed and small; the reuse is free.

## Bit Commitment via PRG — When the Image Is Sparse

A commitment scheme built as `com = PRG(seed)` (open by revealing `seed`)
is only as binding as the PRG's image is *hard to hit twice*. If the PRG
stretches an `n`-bit seed to an `m`-bit output with `n < m`, the image has
only `2^n` points inside a `2^m` codomain — sparse, but not sparse enough
to stop a birthday attack once the attacker gets to combine **two**
independent evaluations (e.g. one XORed against a value the protocol
reveals to them, like `PRG(s0) == PRG(s1) XOR y`).

**Check the pair-count, not just "the domain is smaller than the
codomain":** the expected number of unordered pairs `(s0, s1)` from the
`2^n`-point image satisfying a fixed target relation is
`C(2^n, 2) / 2^m ≈ 2^(2n-1) / 2^m`. That is non-negligible exactly when
`2n` approaches `m` — here `n=16, m=32` gives an expected ~0.5 pairs per
target, i.e. a solution exists roughly `1 - e^-0.5 ≈ 39%` of the time.
Mind the ordered-vs-unordered trap: `(s0,s1)` and `(s1,s0)` are the same
discovery, so treating them as independent doubles the apparent rate.

**Why this breaks binding, not just secrecy:** if the protocol reveals
any value the attacker can fold into a second PRG evaluation *before*
they must commit (here, `y` — needed for one of two possible openings —
arrives before the commitment is requested), the attacker can search for
an equivocal commitment that opens as *either* answer, and was never
actually bound to one. Seen in
[Crypto Civilization](../events/2025/la-ctf/crypto/crypto-civilization/README.md).

**Practical move:** precompute the full `seed -> PRG(seed)` table once (the
seed space is the whole point of being small), then for each fresh
challenge value do an `O(2^n)` scan checking membership of `target XOR
candidate` in that table — no repeated hashing, and cheap enough to redo
per round of an interactive protocol.

## RSA: Cheap Checks Before Reaching for a Factoring Algorithm

Textbook RSA (no OAEP-style padding) breaks in ways that cost far less
than factoring `N`. Run these before anything heavier:

- **Is `N` odd?** A genuine modulus is a product of two large odd
  primes, so it must be odd. If it isn't, one "prime" is `2` — a buggy
  key generator, not a hard problem. Factor by parity, done. Seen in
  [EVEN RSA CAN BE BROKEN???](../practice/picogym/even-rsa-can-be-broken/README.md).
- **Is `e` small (3, 5, ...) and is there real padding?** With no
  padding, `c = M**e mod N` is just `M**e` once `M**e` stays under `N`
  — no modular reduction at all. Recovering `M` is then an integer
  `e`-th root, not a private-key operation. If `M**e` overflows `N` a
  *few* times, search small `k` for the first `c + k*N` that's a
  perfect `e`-th power — cheap, since `k` is small by construction
  whenever the message is only a little larger than `N**(1/e)`. Seen in
  [Mini RSA](../practice/picogym/mini-rsa/README.md), where the actual
  capture needed `k=0` despite the challenge text implying `k=1` —
  checked, not assumed.
- **Do two ciphertexts share a modulus, or share a prime factor with
  each other?** `gcd` of two moduli that shouldn't be related is free to
  compute and instantly fatal if it's not 1.
- **Is the public exponent even coprime to `phi(N)`?** If `gcd(e,
  phi(N)) != 1`, the "encryption" isn't invertible the intended way,
  which usually means a different door is open.

None of these require touching Pollard's rho, Fermat factorization, or
Coppersmith's method — they're all one-line checks against the public
key alone, and picoGym's "Easy" RSA challenges are almost always exactly
one of these, not a real factoring problem in disguise.

## Verifying a Break

- **Reconstruct, don't eyeball.** "The plaintext reads sensibly" is weak.
  Re-encrypting the recovered plaintext and getting the original ciphertext back
  byte-for-byte is proof, and it costs one assertion.
- **Test your oracle before trusting it.** A candidate-key check that filters
  wrong answers is not the same as one that confirms right ones — an oracle
  comparing two decryptions accepts any pair of keys shifted equally.
- **Pin the input file.** An editor normalising curly quotes shifts every offset
  and silently invalidates the analysis.

## Repo Examples

- [CyLab Mod 26](../practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/mod-26/README.md) — ROT13, shift recovered from a crib, involution property
- [LA CTF Too Loud To Yap](../events/2025/la-ctf/crypto/too-loud-to-yap/README.md) — Vigenère autokey, primer recovery
- [LA CTF Bigram Times](../events/2025/la-ctf/crypto/bigram-times/README.md) — multiplicative cipher mod 67, counting preimages via group theory
- [LA CTF Crypto Civilization](../events/2025/la-ctf/crypto/crypto-civilization/README.md) — Naor bit commitment, birthday attack on PRG image sparsity, equivocation
- [LA CTF big-e](../events/2025/la-ctf/crypto/big-e/README.md) — RSA common modulus
- [LA CTF Extremely Convenient Breaker](../events/2025/la-ctf/crypto/extremely-convenient-breaker/README.md) — oracle interaction
- [LA CTF RSAaaS](../events/2025/la-ctf/crypto/rsaaas/README.md) — RSA key validation
- [picoGym EVEN RSA CAN BE BROKEN???](../practice/picogym/even-rsa-can-be-broken/README.md) — modulus parity reveals p=2
- [picoGym Mini RSA](../practice/picogym/mini-rsa/README.md) — low-public-exponent attack, integer nth-root recovery
