# Warmed Up

## Metadata

- Platform: CyLab Academy / picoCTF
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: General Skills
- Difficulty: Beginner
- Status: Solved
- Started: 2026-08-04
- Completed: 2026-08-04
- Files: none
- Skills Learned: hex to decimal conversion, positional number bases

## Problem Summary

> What is `0x3D` (base 16) in decimal (base 10)?

Convert a two-digit hexadecimal value to decimal and wrap the answer in the
flag format.

## First Observations

- The `0x` prefix is C-style notation for "the following digits are base
  16" — it is not part of the number. The value is the two digits `3D`.
- Hex digits run `0-9` then `A-F`, where `A=10 ... F=15`. So `D = 13`.

## Key Idea

Positional notation: each digit is worth its face value times the base
raised to its position index, counting right to left from zero.

```text
0x3D = 3 * 16^1  +  13 * 16^0
     = 48        +  13
     = 61
```

The same rule is what makes decimal work (`61 = 6*10^1 + 1*10^0`) — only
the base changes.

## Solution Walkthrough

By hand, as above: `3 * 16 = 48`, plus `D` = 13, gives 61.

### CyberChef Recipe

| Step | Operation | Settings |
| --- | --- | --- |
| 1 | **From Base** | Radix: `16` |

Input `3D` (no `0x` prefix — CyberChef wants the digits only). Output: `61`.

**The trap worth doing on purpose once:** swap `From Base` for **From Hex**
and the same input gives `=`, not `61`. Both are "hex to something", but

- `From Base` / `To Base` treat the input as **one number** and change its
  radix → `61`.
- `From Hex` / `To Decimal` treat the input as a **byte sequence** →
  `0x3D` is one byte, whose ASCII character is `=`.

Picking the wrong family is the most common CyberChef mistake in this
category, and it is silent — both produce plausible output. Decide which
reading you want *before* dragging an operation in.

Any of these confirm it:

```bash
python3 -c 'print(0x3D)'          # literal -- Python parses 0x natively
python3 -c 'print(int("3D", 16))' # parse a string in an explicit base
printf '%d\n' 0x3D                # shell
echo 'ibase=16; 3D' | bc          # bc, note: uppercase digits required
```

All print `61`.

## Commands Or Script

No `solve.py` here — the whole solve is `int("3D", 16)`, and there is no
property worth asserting that the language's own parser doesn't already
guarantee. A test file would be testing Python, not the solve.

## Flag

```text
picoCTF{61}
```

## Lessons Learned

- **`0x` is a prefix, not a digit.** Same family: `0b` for binary, `0o`
  for octal, and a bare leading `0` for octal in C. Reading `0x3D` as
  "zero-ex-three-dee" and converting all four characters is the classic
  beginner slip.
- **One hex digit is exactly 4 bits, one byte is exactly 2 hex digits.**
  That fixed alignment is why hex — not decimal — is the default for
  memory dumps, colours, and hashes: byte boundaries stay visible.
  `0x3D` is one byte, `0011 1101`.
- **Watch for the base you are *not* in.** `0x3D` as an ASCII byte is
  `=`, which is base64's padding character. In a forensics or crypto
  challenge, the interesting question about a byte is usually "what does
  it mean as ASCII", not "what is it in decimal" — this challenge just
  happens to want the decimal.

## Follow-Up

- Seeded [../../../../../notes/general.md](../../../../../notes/general.md) with the number-base
  reference table and the hex/byte alignment rule.
- The hex-to-ASCII direction shows up immediately in encoding challenges —
  see the encoding triage in [../../../../../notes/crypto.md](../../../../../notes/crypto.md).
