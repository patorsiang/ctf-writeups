# Bases

## Metadata

- Platform: CyLab Academy / picoCTF
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: General Skills
- Difficulty: Beginner
- Status: Solved
- Started: 2026-08-04
- Completed: 2026-08-04
- Files: `solve.py`, `test_recon.py`
- Skills Learned: base64 decoding, binary-to-text encoding vs number bases, 6-bit regrouping

## Problem Summary

> What does this `bDNhcm5fdGgzX3IwcDM1` mean? I think it has something to
> do with bases.

Decode the string and wrap it in the flag format.

## First Observations

- Mixed case letters and digits, no `+`, `/` or `=`, length 20.
- Length is a multiple of 4 — the tell for base64, and it explains the
  absent `=`: the input was a whole number of 3-byte groups, so no padding
  was needed.
- The alphabet is too wide for hex (`g`, `h`, `m`, `n`, `w`, `z` all appear
  and none are hex digits), and case is significant, which rules out the
  case-insensitive bases.

## Key Idea

**"Bases" is a pun, and it is the point of the challenge.** The two
previous challenges in this path were positional number bases — [Warmed
Up](../warmed-up/README.md) (base 16 → 10) and [2warm](../2warm/README.md)
(base 10 → 2), where "base" means the radix in digit × base^position.

Base64 is *not* that. It is a **binary-to-text encoding**: it takes an
arbitrary byte sequence and re-expresses it using only 64 printable,
transport-safe characters. Nobody is doing arithmetic on `bDNhcm5f` — it
isn't a number.

What the two ideas genuinely share is the regrouping rule from 2warm:

```text
3 bits -> 1 octal digit
4 bits -> 1 hex digit
6 bits -> 1 base64 character     <- 2^6 = 64
```

So decoding is: map each character to its 6-bit index, concatenate into one
bitstream, re-slice into 8-bit bytes. Working the first group by hand:

```text
char   index    6 bits
  b      27     011011
  D       3     000011
  N      13     001101
  h      33     100001

bitstream:  011011 000011 001101 100001
re-sliced:  01101100 00110011 01100001
                0x6C     0x33     0x61
                 'l'      '3'      'a'
```

`bDNh` → `l3a`. Repeat across the string for `l3arn_th3_r0p35`.

## Solution Walkthrough

### CyberChef Recipe

| Step | Operation | Settings |
| --- | --- | --- |
| 1 | **From Base64** | Alphabet: `A-Za-z0-9+/=` (the default) |

Input `bDNhcm5fdGgzX3IwcDM1`. Output: `l3arn_th3_r0p35`.

Two notes:

- **`From Base64`, not `From Base`.** Despite the challenge hint saying
  "bases", the number-base operation is the wrong family here — base64 is a
  byte encoding, which is the whole point of the pun. This is the same
  number-op vs byte-op fork as [Warmed Up](../warmed-up/README.md) and
  [2warm](../2warm/README.md), and here the byte side is the right one.
- **If the output is garbage, change the Alphabet dropdown before doubting
  the data.** URL-safe (`A-Za-z0-9-_`) and the other presets live in that
  one setting. Ticking *Remove non-alphabet chars* also rescues input
  that picked up stray whitespace or newlines on the way in.

Terminal:

```bash
echo 'bDNhcm5fdGgzX3IwcDM1' | base64 -d    # l3arn_th3_r0p35
python3 -c 'import base64; print(base64.b64decode("bDNhcm5fdGgzX3IwcDM1"))'
```

Note `echo` adds a trailing newline that `base64 -d` tolerates here; use
`printf` or `echo -n` if a decoder ever complains about input length.

## Commands Or Script

[`solve.py`](solve.py) does *not* call `base64.b64decode` — it implements
the decode as explicit bit regrouping, because the mechanism is the lesson:

```bash
python3 solve.py
# 20 chars -> 15 bytes
# FLAG: picoCTF{l3arn_th3_r0p35}
```

[`test_recon.py`](test_recon.py) uses the stdlib as the oracle — a
hand-rolled decoder is only worth having if it agrees with the real one.
Eight tests: the challenge string, a differential test against
`base64.b64decode` over random payloads of every length 0–64 (which is
where padding bugs live), the three padding residues named explicitly,
rejection of malformed input, and the 4:3 ratio:

```bash
python3 test_recon.py    # or: pytest test_recon.py
```

## Flag

```text
picoCTF{l3arn_th3_r0p35}
```

## Lessons Learned

- **Encoding is not encryption.** Base64 has no key and hides nothing; it
  exists so binary survives text-only channels (email, JSON, URLs, HTTP
  headers). Finding base64 in a challenge is a *transport* observation, not
  a crypto one — decode it and keep going, the real challenge is usually
  underneath.
- **4 characters carry exactly 3 bytes.** `lcm(6, 8) = 24 bits`. Two
  consequences worth memorising: base64 inflates data by ~33%, and the
  length is always a multiple of 4 — which is what padding exists to
  guarantee. `=` fills a group when the payload wasn't a multiple of 3
  bytes: 2 bytes left over → one `=`, 1 byte left over → two `=`.
- **`=` is `0x3D`, which is exactly the byte from
  [Warmed Up](../warmed-up/README.md).** Seeing one or two `=` at the end
  of a blob is the single cheapest base64 tell there is.
- **Read the length before reaching for a tool.** Multiple of 4 plus a
  64-character alphabet identified this as base64 before any decoding.
  Contrast: an even-length string over `0-9a-f` is hex; 32/40/64 hex chars
  is a hash, which does *not* decode to anything.
- **Watch the variant.** URL-safe base64 swaps `+/` for `-_` and often
  drops padding; base32 uses `A-Z2-7`. If a standard decode produces
  garbage, check the alphabet before assuming the data is wrong.

## Follow-Up

- Added the binary-to-text encoding section (identification table,
  encoding-vs-encryption, the 4:3 ratio) to
  [../../../../../notes/general.md](../../../../../notes/general.md).
- Cross-referenced from the encoding triage in
  [../../../../../notes/crypto.md](../../../../../notes/crypto.md), since
  "is this encoded or encrypted" is step one there.
