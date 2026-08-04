# 2warm

## Metadata

- Platform: CyLab Academy / picoCTF
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: General Skills
- Difficulty: Beginner
- Status: Solved
- Started: 2026-08-04
- Completed: 2026-08-04
- Files: none
- Skills Learned: decimal to binary conversion, powers of two, repeated division

## Problem Summary

> Can you convert the number 42 (base 10) to binary (base 2)?

The reverse direction of [Warmed Up](../warmed-up/README.md): that one went
base 16 → base 10, this one goes base 10 → base 2.

## First Observations

- Going *into* decimal is evaluation (multiply out the positions and add).
  Going *out of* decimal is decomposition — a different mechanic, which is
  why this is its own challenge rather than a repeat.
- Binary digits are only `0` and `1`, so each position is a yes/no question:
  "does this power of two fit?"

## Key Idea

Two methods, same answer. Both are worth being able to do without a tool.

**Subtract the largest power of two that fits.** Write the powers down
first, then walk left to right:

```text
     64  32  16   8   4   2   1
          1   0   1   0   1   0

42 - 32 = 10   ->  1   (64 doesn't fit, 32 does)
10 - 16 = no   ->  0
10 -  8 =  2   ->  1
 2 -  4 = no   ->  0
 2 -  2 =  0   ->  1
 0 -  1 = no   ->  0
```

Result: `101010`. Check by evaluating back: `32 + 8 + 2 = 42`.

**Repeated division by 2, remainders read bottom-up.** Mechanical, works
for any target base:

```text
42 / 2 = 21 r 0     <- least significant bit
21 / 2 = 10 r 1
10 / 2 =  5 r 0
 5 / 2 =  2 r 1
 2 / 2 =  1 r 0
 1 / 2 =  0 r 1     <- most significant bit
```

Read the remainders **upward**: `101010`. Reading them downward gives
`010101`, which is the classic error in this method.

## Solution Walkthrough

By hand, as above.

### CyberChef Recipe

| Step | Operation | Settings |
| --- | --- | --- |
| 1 | **To Base** | Radix: `2` |

Input `42`. Output: `101010`.

**Same trap as [Warmed Up](../warmed-up/README.md), mirrored.** Using
**To Binary** instead gives `00110100 00110010` — that is the binary of the
*characters* `'4'` and `'2'` (bytes `0x34 0x32`), not the number 42.

- `To Base` (radix 2) → the number 42 rewritten in base 2 → `101010`.
- `To Binary` → each input byte spelled out in bits → two bytes of ASCII.

The flag wants the number, so `To Base`. Again: decide number-op or
byte-op before choosing the operation, because both return something that
looks like an answer.

Confirm:

```bash
python3 -c 'print(bin(42))'          # 0b101010
python3 -c 'print(format(42, "b"))'  # 101010  -- no prefix
python3 -c 'print(f"{42:08b}")'      # 00101010 -- zero-padded to a byte
```

The flag wants the bare digits, so strip the `0b`.

## Commands Or Script

No `solve.py` — same reasoning as [Warmed Up](../warmed-up/README.md). The
solve is `format(42, "b")`; there is no derivation to pin down that the
language's own formatter doesn't already guarantee.

## Flag

```text
picoCTF{101010}
```

## Lessons Learned

- **The flag wants `101010`, but the *byte* is `00101010`.** Leading zeros
  carry no numeric value, yet they carry width — and width is what matters
  the moment bytes are involved. `0b101010` and `0b00101010` are the same
  number and the same byte; `f"{42:08b}"` is the formatting to reach for
  when alignment matters, `bin()` when it doesn't.
- **Know the powers of two up to 1024 cold.** `1 2 4 8 16 32 64 128 256
  512 1024`. Recognising 255, 256, 1023, 1024, 4096, 65535 on sight is what
  turns "weird number" into "that's a byte boundary / off-by-one /
  16-bit overflow" in a pwn or web challenge.
- **Three bits = one octal digit, four bits = one hex digit.** So `42` is
  `101010` binary, `52` octal, `2A` hex, and you can regroup between them
  without going via decimal at all: `101 010` → `52`, `10 1010` → `2A`.
  That regrouping is exactly how `chmod 755` works — `111 101 101`, i.e.
  `rwx r-x r-x`.

## Follow-Up

- Added the decimal → base decomposition methods, powers-of-two table, and
  the binary/octal/hex regrouping rule to
  [../../../../../notes/general.md](../../../../../notes/general.md).
- Bit-width awareness (padding, overflow, byte boundaries) is the thread
  that leads into [../../../../../notes/pwn.md](../../../../../notes/pwn.md).
