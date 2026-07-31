# Crypto Notes

## Beginner Checklist

- Identify whether data is encoded, encrypted, hashed, or compressed.
- Check common encodings first: hex, base64, URL encoding, ASCII, binary.
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

- [LA CTF Too Loud To Yap](../events/2025/la-ctf/crypto/too-loud-to-yap/README.md) — Vigenère autokey, primer recovery
- [LA CTF big-e](../events/2025/la-ctf/crypto/big-e/README.md) — RSA common modulus
- [LA CTF Extremely Convenient Breaker](../events/2025/la-ctf/crypto/extremely-convenient-breaker/README.md) — oracle interaction
- [LA CTF RSAaaS](../events/2025/la-ctf/crypto/rsaaas/README.md) — RSA key validation
