# Mod 26

## Metadata

- Platform: CyLab Academy / picoCTF
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: Crypto
- Difficulty: Beginner
- Status: Solved
- Started: 2026-08-04
- Completed: 2026-08-04
- Files: `solve.py`, `test_recon.py`
- Skills Learned: ROT13 / Caesar shift, CyberChef, recovering a shift from a crib instead of guessing

## Problem Summary

The challenge hands over a single string and says it can be solved in the
browser with CyberChef:

```text
cvpbPGS{arkg_gvzr_V'yy_gel_2_ebhaqf_bs_ebg13_45559noq}
```

The goal is to decode it into the flag.

## First Observations

- The string has the exact shape of a picoCTF flag: `XXXXXXX{...}` with
  underscores, digits and an apostrophe inside the braces.
- The braces, digits and punctuation are already in the right places, so
  **structure is preserved** — letters map to letters in place. That rules
  out transposition and anything block-based; this is the substitution
  family.
- `cvpbPGS` is 7 characters, same as `picoCTF`, and the case pattern
  matches (`lower lower lower lower UPPER UPPER UPPER`).

## Key Idea

The title is the hint. "Mod 26" means arithmetic on the 26-letter alphabet
— a Caesar shift. Line up the known prefix:

```text
c -> p   is +13
v -> i   is +13
p -> c   is +13
b -> o   is +13
```

A shift of 13 is ROT13, the special case everyone memorises.

The nice part: 13 + 13 = 26 ≡ 0 (mod 26), so **ROT13 is its own inverse**.
Encoding and decoding are the same operation, which is why CyberChef only
gives you one ROT13 button rather than an encode/decode pair.

## Solution Walkthrough

### CyberChef Recipe

| Step | Operation | Settings |
| --- | --- | --- |
| 1 | **ROT13** | Amount: `13` (the default); rotate lower + upper both ticked |

Paste the ciphertext into Input; the flag appears in Output.

Two notes:

- **There is no "decode" button, and that is the lesson.** ROT13 is an
  involution, so the same operation encodes and decodes. Compare
  `From Base64`, which needs a separate `To Base64` — a real inverse pair.
- **If the shift weren't 13**, the same operation covers it: set Amount to
  the shift, or use **ROT13 Brute Force** to dump all 26 candidates at once
  and eyeball the readable one. That is the general Caesar tool.

Terminal route, no tooling needed:

```bash
echo "cvpbPGS{arkg_gvzr_V'yy_gel_2_ebhaqf_bs_ebg13_45559noq}" | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

`tr` maps `A-Za-z` onto the alphabet rotated by 13 and leaves everything
outside that set alone — so the braces, digits and apostrophe survive.

## Commands Or Script

[`solve.py`](solve.py) implements a general Caesar rather than hardcoding
13, and **recovers the shift from the `picoCTF{` crib** instead of assuming
it:

```bash
python3 solve.py
# shift: 13
# FLAG: picoCTF{next_time_I'll_try_2_rounds_of_rot13_45559abd}
```

[`test_recon.py`](test_recon.py) covers the flag, the crib-derived shift,
non-letter pass-through, a ciphertext no shift can fix (so the finder is
proven to say "no", not just "yes"), and the involution property below:

```bash
python3 test_recon.py    # or: pytest test_recon.py
```

## Flag

```text
picoCTF{next_time_I'll_try_2_rounds_of_rot13_45559abd}
```

## Lessons Learned

- **The flag is a joke, and the joke is the lesson.** "next time I'll try
  2 rounds of rot13" would encrypt nothing: `rot13(rot13(x)) == x`, because
  shifts compose additively mod 26. Composing a cipher with itself is not
  automatically stronger — for an involution it is exactly the identity.
- **Derive the key, don't guess it.** ROT13 is the famous shift, but the
  general move is to line a known crib (`picoCTF{`) up against the
  ciphertext and read the offset off. That same step solves shift-7 or
  shift-19 without a second thought, and tells you immediately when the
  cipher *isn't* a Caesar.
- Structure surviving intact (spaces, braces, punctuation in place) is the
  cheap tell that separates substitution from transposition — worth
  checking before touching any tooling.
- Brute force is trivially cheap here anyway: 26 keys, eyeball the one that
  reads as English.

## Follow-Up

- Added the Caesar/ROT13 triage step to [../../../../../notes/crypto.md](../../../../../notes/crypto.md).
- Next classical-cipher step up: a keyed substitution or Vigenère, where
  frequency analysis and index of coincidence start to matter — see
  [Too Loud To Yap](../../../../../events/2025/la-ctf/crypto/too-loud-to-yap/README.md).
