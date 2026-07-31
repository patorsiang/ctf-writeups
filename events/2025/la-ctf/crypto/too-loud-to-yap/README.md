# Too Loud To Yap

## Metadata

- Event: LA CTF 2025
- Category: Crypto
- Difficulty: Unknown
- Status: In progress — cipher family identified, key not yet recovered
- Files: [ct.txt](ct.txt), [test_recon.py](test_recon.py), [main.py](main.py)
- Skills Learned: Index of coincidence, crib dragging, running-key ciphers

## Problem Summary

A single file, `ct.txt` (781 bytes): five paragraphs of English-looking prose
where most words are garbled, a handful are readable, and ten words are written
in ALL CAPS. The flag sits in the text already, encrypted, on line 9:

```
N sjsmbwk "OUTED lactf{ooyg_blhd_pea_ubu}!"
```

Note that the wrapper `lactf{`, the underscores and the braces survive
untouched — only the letters inside are enciphered, and the flag body is 14
letters of recoverable plaintext. **The whole message does not need to be
decrypted.**

## What I Tried

### Recon: what the character set rules out

No digits, no `+/=`, nothing base64- or hex-shaped, so this is not an encoding
problem. More usefully, **word lengths, spaces, apostrophes and quotation marks
are all preserved** — `htwpxues` is eight letters sitting where an eight-letter
word belongs. A transposition would scramble word boundaries; a block cipher
would destroy them. Letters map to letters, in place: the substitution family.

`dlhd` (line 7) and `blhd` (line 9) are the same underlying word and differ.
Same plaintext, different ciphertext, depending on position — so not a simple
substitution and not a Caesar. Polyalphabetic.

### Dead end 1: frequency analysis

`main.py` (written before the break) counts letter frequencies with pandas and
plots them with matplotlib. On a polyalphabetic cipher the histogram flattens
out and tells you nothing. Correct first reflex, wrong cipher class — kept in
the folder as a record of the false start.

### Dead end 2: a repeating Vigenère key

Standard probe — split the letter stream into `k` columns and average the index
of coincidence of each. If the key repeats with period `k`, every column is a
single Caesar shift and its IC climbs toward English (0.066).

Important detail: **strip the ALL-CAPS words before running any statistic.**
They are plaintext (see below), and leaving them in pollutes the stream with
real English.

Every key length from 1 to 15 came back in the 0.038–0.046 band — random-text
level. No short repeating key exists. Pinned by
`test_no_repeating_key_up_to_length_15`.

### Dead end 3: per-word Caesar

Rotated every garbled word through all 26 shifts against `/usr/share/dict/words`.
Only chance hits (`hppa`→`weep`, `awis`→`soak`) — noise, not a consistent shift.
Pinned by `test_word_level_caesar_is_ruled_out`.

### The pivot: the ALL-CAPS words are cribs

The challenge title is the hint. "Too loud" = the shouted words:

```
HERES  THING  THERE  MOVIEA  STOPS  THCISA  OUTED  WHATS  QUITE  ATTHE
```

Each one is **known plaintext for the ciphertext immediately preceding it**,
ignoring word boundaries (`MOVIEA` spans "movie" + "a", `ATTHE` spans "at" +
"the"):

```
oo  xyc   ATTHE   hospiaod    ->  "at the hospital"
o   iwope MOVIEA              ->  "a movie"
xyetw     QUITE  injurmq      ->  "quite injured"
```

Subtracting, `key = ct - pt (mod 26)`:

```
oo    - at    -> ov      | concatenated: "ov" + "ery" = overy
xyc   - the   -> ery     |
iwope - movie -> witha  ->  "with a"
xyetw - quite -> hewas  ->  "he was"
```

## Key Idea

The key is English prose, as long as the message and never repeating — a
**running-key cipher**. That is exactly why the index of coincidence came back
flat: with a non-repeating key there is no column to align, so every classical
periodicity attack fails by construction.

The author then undermines their own key by leaking known plaintext at ten
scattered positions. Each crib exposes a window of the key, and because the key
is *prose*, those windows can be extended by guessing forward the way you would
finish anyone's sentence — recovering key material well beyond the crib itself.

## Solution Walkthrough

Remaining steps, not yet done:

- [ ] Decode `N sjsmbwk` on line 9 (1 + 7 letters) using `OUTED` as the crib for
      its tail. This is the key window running directly into the flag.
- [ ] Extend that key fragment forward across the 14 flag letters
      (`ooygblhdpeaubu`) by guessing the prose continuation one letter at a
      time, keeping candidates that leave the plaintext readable.
- [ ] Cross-check: `dlhd pea` (line 7, on the shirt) and `blhd_pea` (line 9, in
      the flag) are the same two words at different key offsets. When both
      decrypt identically, the key is right.
- [ ] Recover the full flag and confirm it starts with `lactf{`.
- [ ] Add the correctness test — `decrypt(ct, key).startswith("lactf{")` — to
      `test_recon.py`, alongside the existing characterisation tests.
- [ ] Write the recovered key text into this file; a running key is usually a
      quote or a song lyric and is worth recording.
- [ ] Flip `Status` to `Solved` and push the technique into
      [notes/crypto.md](../../../../../notes/crypto.md).

## Exploit / Script

- [test_recon.py](test_recon.py) — characterisation tests pinning the recon
  findings. Runs bare (`python3 test_recon.py`) or under pytest, no dependencies.
  Contains the reusable helpers: `index_of_coincidence`, `average_column_ic`,
  and `subtract` (the `ct - pt` key-recovery step).
- [main.py](main.py) — the abandoned frequency-analysis approach. Needs pandas
  and matplotlib and opens a GUI window; kept only as a record of the dead end.

## Flag

Not recovered yet. Ciphertext form: `lactf{ooyg_blhd_pea_ubu}`.

## Lessons Learned

- **Read the challenge title as a hint.** "Too Loud To Yap" points straight at
  the ALL-CAPS words; the statistical work was a detour around something the
  author had already labelled.
- **A flat index of coincidence is information, not failure.** It does not mean
  "the cipher is too strong" — it means the key does not repeat, which points at
  running-key or one-time-pad rather than Vigenère.
- **Scope the work to the goal.** The flag body is 14 letters. Decrypting all
  542 letters of the message was never required.
- **Assert the property, not the observation.** The Caesar test asserts "hits
  are noise" (< 10%) rather than an exact count, which would be brittle against
  a different platform's wordlist.
- **Pin the input file.** An editor silently normalising the curly `'` quotes in
  `ct.txt` would shift every offset and invalidate the analysis with no visible
  change to the text.
- Structured known-plaintext at attacker-chosen positions is the finding — in a
  CTF and in a real crypto review — before any of the maths starts.

## References

- Challenge title, which is the actual hint.
