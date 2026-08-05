# General Skills Notes

Command-line fluency, number bases, file inspection — the substrate every
other category sits on.

## Beginner Checklist

- `ls -la` before anything else: hidden files (`.`-prefixed) are a
  standard hiding spot and invisible to a bare `ls`.
- `file <target>` before `cat <target>`. The extension is a claim, not
  evidence; `file` reads magic bytes.
- `strings <binary> | grep -i flag` is the cheapest first pass on anything
  non-text.
- When a service is involved, write down host **and** port. Non-default
  ports (`ssh -p`, `nc host port`) are the whole point of several
  beginner challenges.

## Number Bases

Positional notation: digit × base^position, counting right to left from
zero. Only the base changes between systems.

| Prefix | Base | Digits | Example | Decimal |
| --- | --- | --- | --- | --- |
| `0b` | 2 | `0-1` | `0b111101` | 61 |
| `0o` | 8 | `0-7` | `0o75` | 61 |
| (none) | 10 | `0-9` | `61` | 61 |
| `0x` | 16 | `0-9A-F` | `0x3D` | 61 |

The prefix is **not** part of the number. Converting all of `0x3D` instead
of just `3D` is the classic slip. In C, a bare leading zero also means
octal — `0755` is 493, not 755.

```bash
python3 -c 'print(0x3D, 0b111101, 0o75)'   # literals
python3 -c 'print(int("3D", 16))'          # parse a string in a given base
python3 -c 'print(hex(61), bin(61))'       # back the other way
printf '%d\n' 0x3D
echo 'ibase=16; 3D' | bc                   # bc needs uppercase hex digits
```

Seen in [Warmed Up](../practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/warmed-up/README.md).

### Out Of Decimal Is A Different Mechanic

Going *into* decimal is evaluation — multiply out the positions and add.
Going *out of* decimal is decomposition. Two methods:

- **Subtract the largest power that fits**, left to right. Fast for binary
  because the powers of two are memorable and each digit is just yes/no.
- **Repeated division by the base, remainders read bottom-up.** Works for
  any base. Reading the remainders top-down instead is *the* error here —
  42 gives `101010`, not `010101`.

```text
42 / 2 = 21 r 0  <- least significant        64 32 16  8  4  2  1
21 / 2 = 10 r 1                                  1  0  1  0  1  0
10 / 2 =  5 r 0                              32 + 8 + 2 = 42
 5 / 2 =  2 r 1
 2 / 2 =  1 r 0
 1 / 2 =  0 r 1  <- most significant
```

Seen in [2warm](../practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/2warm/README.md).

### Powers Of Two, Cold

`1 2 4 8 16 32 64 128 256 512 1024 2048 4096`

Recognising 255, 256, 1023, 1024, 65535, 65536 on sight is what turns
"weird number in the output" into "byte boundary", "off-by-one", or
"16-bit overflow" without stopping to compute.

### Regrouping Without Going Via Decimal

3 bits = 1 octal digit. 4 bits = 1 hex digit. So you can convert between
binary, octal and hex by regrouping the bits — decimal never enters it:

```text
101010  ->  101 010  ->  52  (octal)
101010  ->  10 1010  ->  2A  (hex)
```

This is exactly how Unix permissions work: `chmod 755` is `111 101 101` is
`rwx r-x r-x`. One octal digit per permission triple, by construction.

### Leading Zeros: No Value, But Width

`0b101010` and `0b00101010` are the same number and the same byte. The
zeros carry no numeric value — they carry *width*, and width is what
matters as soon as bytes, fields, or alignment are involved.

```python
bin(42)             # '0b101010'  -- prefixed, unpadded
format(42, "b")     # '101010'    -- bare digits
f"{42:08b}"         # '00101010'  -- padded to a byte
f"{42:#010b}"       # '0b00101010' -- prefix + padding
```

Reach for the padded form whenever the output will be compared,
concatenated, or read as a byte.

## Why Hex, Specifically

One hex digit is **exactly** 4 bits; one byte is **exactly** 2 hex digits.
That alignment never drifts, so byte boundaries stay visible by eye — which
is why memory dumps, hashes, colours and MAC addresses are all hex and
none of them are decimal. Decimal has no clean power-of-two relationship to
bit widths, so byte boundaries land mid-digit and become unreadable.

Practical consequence: when you see a hex string, count its length. An even
count is a byte sequence (candidate for hex-decode to ASCII); 32/40/64
characters are the fingerprints of MD5/SHA-1/SHA-256.

## Binary-To-Text Encodings Are Not Number Bases

"Base64" reuses the word but means something different from base 2 / 10 /
16. A number base is a radix for arithmetic on *one* number. Base64 is a
**transport encoding**: an arbitrary byte sequence re-expressed in 64
printable characters so it survives text-only channels — email, JSON, URLs,
HTTP headers, PEM keys. Nobody does arithmetic on a base64 string.

What they do share is the regrouping rule: `2^6 = 64`, so

```text
3 bits -> 1 octal digit
4 bits -> 1 hex digit
6 bits -> 1 base64 character
```

Decoding is map-to-6-bit-index, concatenate, re-slice into 8-bit bytes.
Seen in [Bases](../practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/bases/README.md).

**Encoding is not encryption.** No key, no secret. Spotting base64 in a
challenge is a transport observation, not a crypto finding — decode and
keep going; the actual challenge is usually underneath.

### The 4:3 Ratio And Why Padding Exists

`lcm(6, 8) = 24 bits = 3 bytes = 4 characters`. Hence:

- Base64 output is always a multiple of 4 characters.
- It inflates data by ~33%.
- `=` pads a short final group: payload ≡ 2 mod 3 bytes → one `=`,
  ≡ 1 mod 3 → two `=`. Three `=` is never valid.
- `=` is `0x3D` — the byte from
  [Warmed Up](../practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/warmed-up/README.md).
  One or two trailing `=` is the cheapest base64 tell there is.

### Identifying An Encoded Blob By Alphabet And Length

Check these before opening a tool:

| Alphabet | Length rule | Likely | Note |
| --- | --- | --- | --- |
| `0-9a-f` | even | hex | 32/40/64 chars = MD5/SHA-1/SHA-256 — a hash, decodes to nothing |
| `A-Za-z0-9+/=` | multiple of 4 | base64 | `=` only ever at the end |
| `A-Za-z0-9-_` | multiple of 4 | URL-safe base64 | `+/` swapped for `-_`, padding often dropped |
| `A-Z2-7=` | multiple of 8 | base32 | no lowercase, no `0 1 8 9` |
| `0-9` only | any | decimal / ASCII codes | try splitting into 2–3 digit groups |
| printable + `%` | any | URL encoding | `%20`, `%2F` |

If a standard decode yields garbage, suspect the **variant** before
suspecting the data.

## Never Type A Long Path

Two mechanisms, different moments, both worth fluency:

| Mechanism | Runs | Behaviour |
| --- | --- | --- |
| **Tab completion** | interactively, as you type | one Tab completes a unique match; two Tabs lists candidates when ambiguous |
| **Globbing** (`*`, `**`) | at execution, before the command | shell expands the pattern into real paths |

Tab is for exploring — you read each name as it appears. Globs are for
scripting and for skipping levels wholesale:

```bash
cd Addadshashanammu/*/*/*/*/*/*/   # six levels, one command
cd */                              # works whenever exactly one dir matches
```

Completion is **context-aware**, not just prefix matching: with a `foo`
directory and a `foo.zip` beside it, `cd foo`+Tab still completes to the
directory, because `cd` only accepts directories.

Seen in [Tab, Tab, Attack](../practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/tab-tab-attack/README.md).

**Absolute paths remove a class of error.** When `cd` reports "no such
file or directory" and the path looks right, check `pwd` before doubting
the file — a relative path is a claim about where you are standing.

## Inspect An Archive Before Extracting It

```bash
unzip -Z1 file.zip | grep -E '^/|\.\.'    # no output = safe
tar -tf file.tar.gz | grep -E '^/|\.\.'   # tarball equivalent
```

Listing writes nothing. An entry like `../../.ssh/authorized_keys` gets
written **outside** the directory you extracted from — this is
**zip-slip**, a real CVE class that has hit widely-used archive libraries
in many languages. One command, every untrusted archive, always.

## Running A Provided Binary

`file` first, always. One command answers the four things that decide how
the rest of the challenge goes:

```text
ELF 64-bit LSB pie executable, x86-64, dynamically linked,
interpreter /lib64/ld-linux-x86-64.so.2, with debug_info, not stripped
```

| Field | Decides |
| --- | --- |
| `ELF` / `Mach-O` / `PE` | which OS family can load it |
| `x86-64` / `aarch64` | which CPU can execute it |
| `pie` | load base is randomised (ASLR) — in pwn, whether a leak is needed first |
| `dynamically linked` + interpreter | needs glibc/musl present; picking the wrong libc image fails confusingly |
| `stripped` / `not stripped` | whether function names survived — reversing effort, and whether `strings` finds anything |

### Error Triage: Three Lookalikes

| Message | Actual meaning | Fix |
| --- | --- | --- |
| `no such file or directory` | wrong path or misspelled name | check `pwd` and spelling |
| `permission denied` | file present, execute bit off | `chmod +x` |
| `exec format error` | present and executable, wrong OS/CPU | run it somewhere matching |

Fourth case, Linux-only and genuinely confusing: `no such file or
directory` on a binary that plainly exists means the **dynamic loader**
named in the `interpreter` field is missing — the ENOENT is about
`ld-linux`, not about the binary.

Why `./` is required: the shell resolves bare names against `$PATH`, and
`.` is deliberately absent from it. Otherwise dropping a file named `ls`
into a directory would hijack the next `ls` run there.

### Running A Foreign Binary In Docker

The universal one-liner — an emulation fix *and* a disposable sandbox,
which is the right default for untrusted CTF binaries:

```bash
docker run --rm --platform linux/amd64 \
  -v "$PWD:/w" -w /w \
  debian:stable-slim ./binary --help
```

- `--platform linux/amd64` solves OS and architecture together. This is
  the same flag that fixes an Apple Silicon build crashing on an x86
  server — "works on my machine" has a precise mechanical cause.
- `-v` punches a hole in the container's isolation. Mount the narrowest
  directory that works; "just mount `$HOME`" is a real security finding.
- Emulation (Rosetta/QEMU) is a runtime tax. Prefer native
  `linux/arm64` images when the choice exists.
- Match the libc: glibc binaries need Debian/Ubuntu, not Alpine.

Seen in [Wave a Flag](../practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/wave-a-flag/README.md).

## CyberChef: Number Ops vs Byte Ops

[CyberChef](https://gchq.github.io/CyberChef/) is the browser tool the
beginner paths recommend. The one thing to get right is **which family an
operation belongs to**, because both families accept the same input and
both return plausible output — picking wrong fails silently.

| Family | Treats input as | Operations |
| --- | --- | --- |
| Number | one number, change its radix | `From Base`, `To Base` |
| Byte | a sequence of bytes | `From Hex`, `To Hex`, `From Decimal`, `To Decimal`, `From Binary`, `To Binary`, `From Base64` |

Same input, both families, different right answers:

```text
3D  --From Base(16)-->  61          (the number sixty-one)
3D  --From Hex------->  =           (one byte, 0x3D, as ASCII)

42  --To Base(2)----->  101010      (the number forty-two in binary)
42  --To Binary------>  00110100 00110010   (ASCII '4' and '2')
```

Decide which reading the challenge wants **before** dragging an operation
in. "Convert 42 to binary" wants the number; "what do these bytes say"
wants the byte family.

### Recipes Used So Far

| Goal | Operation | Settings | Challenge |
| --- | --- | --- | --- |
| hex → decimal | `From Base` | Radix 16 | [Warmed Up](../practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/warmed-up/README.md) |
| decimal → binary | `To Base` | Radix 2 | [2warm](../practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/2warm/README.md) |
| base64 → text | `From Base64` | Alphabet `A-Za-z0-9+/=` | [Bases](../practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/bases/README.md) |
| ROT13 / Caesar | `ROT13` | Amount 13; `ROT13 Brute Force` for unknown shift | [Mod 26](../practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/mod-26/README.md) |

### Habits

- **Magic** (the wand icon) auto-detects likely encodings — good for a
  first guess on an unknown blob, not a substitute for reading the
  alphabet and length yourself.
- Recipes chain: `From Base64` → `From Hex` → `Gunzip` in one column
  handles nested encodings without round-tripping through files.
- The URL encodes the whole recipe, so pasting it into a writeup preserves
  the exact steps.
- If output looks like garbage, suspect the **operation's settings**
  (radix, alphabet variant) before suspecting the input.

## Bytes Have Three Readings

Any byte can be read as a number, as an ASCII character, or as raw bits.
Beginner challenges ask for one and CTFs generally want another — check
which before answering.

| Hex | Decimal | ASCII | Why it matters |
| --- | --- | --- | --- |
| `0x3D` | 61 | `=` | base64 padding |
| `0x7F` | 127 | DEL | ASCII upper bound |
| `0x41` | 65 | `A` | `A-Z` is `0x41-0x5A` |
| `0x61` | 97 | `a` | lowercase = uppercase + `0x20` |

That last row is worth memorising: ASCII case differs by exactly one bit
(`0x20`), which is why case-flipping shows up as an XOR trick.

## Repo Examples

- [CyLab Warmed Up](../practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/warmed-up/README.md) — hex to decimal, positional notation
- [CyLab 2warm](../practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/2warm/README.md) — decimal to binary, powers of two, bit regrouping
- [CyLab Bases](../practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/bases/README.md) — base64 as 6-bit regrouping, encoding vs number base
- [CyLab Wave a Flag](../practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/wave-a-flag/README.md) — help flags, exec format error, Docker `--platform`
- [CyLab Tab, Tab, Attack](../practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/tab-tab-attack/README.md) — tab completion, globbing, zip-slip check
- [CyLab obedient-cat](../practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/obedient-cat/README.md) — reading a provided file
- [CyLab super-ssh](../practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/super-ssh/README.md) — `ssh -p` on a non-default port
- [CyLab whats-a-net-cat](../practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/whats-a-net-cat/README.md) — raw TCP with `nc`
