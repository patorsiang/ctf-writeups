# Too Loud To Yap

## Metadata

- Event: LA CTF 2025
- Category: Crypto
- Difficulty: Easy (once the cipher is identified)
- Status: Solved
- Files: [ct.txt](ct.txt), [solve.py](solve.py), [test_recon.py](test_recon.py),
  [solve_helper.py](solve_helper.py), [main.py](main.py)
- Skills Learned: Vigenère autokey, index of coincidence, crib dragging,
  recognising confirmation bias in cipher analysis

## Problem Summary

One file, `ct.txt`: five paragraphs of English-looking prose where most words
are garbled, a few are readable, and ten words are ALL CAPS. The flag is sitting
in the text already, enciphered, on line 9:

```
N sjsmbwk "OUTED lactf{ooyg_blhd_pea_ubu}!"
```

Braces and underscores survive untouched, so only the letters are enciphered and
the flag body is 14 letters.

The author's description is the specification, once you can read it:

> i love AAAAA telling and posting stories! [...] when i AAAAA tried telling
> this story about "autos", some guy kept YELLING "AAAAA" in the background
> which AAAAA kept messing up my new take on the vigenere cipher! he actually
> started yelling right AAAAA when i started my story

"autos" → **autokey**. The yelling is the leak.

## Key Idea

**Vigenère autokey with a five-letter primer.** The key is the primer followed
by the plaintext itself:

```
key   = PRIMER + plaintext
ct[i] = pt[i] + pt[i-5]        (pt[i-5] replaced by PRIMER[i] while i < 5)
```

Each plaintext letter becomes the key letter five positions later. There is no
repeating key, which is why every classical periodicity attack fails — but an
autokey needs only the primer to unravel completely, because each letter you
recover immediately keys the next one.

**The primer is `LACTF`, printed on line 1 of the ciphertext.** The plaintext
opens with a yelled `AAAAA`, and `A` contributes a zero shift, so the first five
ciphertext letters *are* the raw key. The challenge hands you the whole thing on
line 1.

The same applies at every yell: each ALL-CAPS word is the ciphertext of an
`AAAAA`, so it exposes the key at that point — which is the plaintext delayed by
five. That is why `QUITE` sits immediately after the ciphertext of "quite", and
why the caps words read as English fragments.

## Solution Walkthrough

```python
PRIMER = "lactf"

def decrypt(ct, primer=PRIMER):
    pt = []
    for i, c in enumerate(ct):
        k = primer[i] if i < len(primer) else pt[i - len(primer)]
        pt.append(chr((ord(c) - ord(k)) % 26 + ord("a")))
    return "".join(pt)
```

Strip everything but letters, run it, and the story falls out:

```
aaaaaheresaaaaaathingaaaaathathappenedtooneofmyfriendsiwastherea...
```

The `aaaaa` runs are the yells. The flag region decrypts to `downwithcisbus`,
which the ciphertext's own underscores split as `4_4_3_3`.

Proof the model is right, rather than merely plausible: re-encrypting the
recovered plaintext reproduces `ct.txt` byte for byte
(`test_model_reproduces_the_ciphertext_exactly`).

## Exploit / Script

- [solve.py](solve.py) — full solve from `ct.txt` alone, no dependencies.
- [test_recon.py](test_recon.py) — 7 tests: 4 correctness, 3 characterisation
  covering the recon phase.
- [solve_helper.py](solve_helper.py) — the crib-dragging tools built during the
  wrong-turn phase. Superseded, kept because the technique transfers.
- [main.py](main.py) — the original frequency-analysis attempt. Dead end.

## Flag

`lactf{down_with_cis_bus}`

## Lessons Learned

- **Read the challenge description as a specification.** "a story about *autos*"
  is the word *autokey*, and the AAAAA prompt describes the exact leak. The
  entire statistical detour was avoidable by reading the text on the page.
- **An autokey is a running key whose key text is the message itself.** The IC
  analysis correctly identified "running key, no period" and then stalled,
  because the search assumed the key was some *external* prose. Getting the
  family right is not the same as getting the mechanism right.
- **A flat index of coincidence is information.** It means the key does not
  repeat, which points at autokey or running key rather than Vigenère.
- **Autokey ciphers unravel from the primer alone**, since every recovered
  letter keys a later one. Recovering five letters recovers everything — so the
  attack is: find the primer, not break the key.
- **Watch for confirmation bias when scoring "English".** Mid-investigation,
  fragments like `overy`, `hewas` and `owitha` were read as "o very", "he was",
  "with a" and taken as confirmation of an external prose key. They were real
  key material, but the readings that felt convincing (`cubgle`, `sabhma`,
  `esish` sitting alongside them) were quietly discounted as misalignment. Short
  fragments will look like English if you want them to; score with n-gram
  statistics rather than by eye.
- **Verify by reconstruction.** "The plaintext reads sensibly" is weak evidence.
  "Re-encrypting reproduces the ciphertext exactly" is proof, and it is one
  extra assertion.
- **Test the verifier before trusting it.** The candidate-key oracle used
  mid-solve accepted false positives — shifting both keys equally made two
  segments agree on the wrong plaintext.

## References

- [uclaacm/lactf-archive — 2025/crypto/too-loud-to-yap](https://github.com/uclaacm/lactf-archive/tree/main/2025/crypto/too-loud-to-yap)
  — ships `pt.txt` and `challenge.yaml` alongside the ciphertext. Consulted
  after the independent attempt stalled; the mechanism above was then derived
  and verified against `ct.txt` directly.
