# ASCII Numbers

## Metadata

- Platform: CyLab Academy
- Learning Path: Low Level Binary Intro
- Category: General Skills / ASCII
- Difficulty: Easy
- Status: Solved
- Started: 2026-10-28
- Completed: 2026-10-28
- Re-solve: due 2026-11-04
- Files: None; the challenge text is on the Academy page
- Skills Learned: hexadecimal byte decoding, ASCII, Python `bytes`

## Problem Summary

Decode a sequence of hexadecimal numbers into a readable string. The challenge
states that the `0x` prefix marks hexadecimal values.

Source: [CyLab Academy: ASCII Numbers](https://learn.cylabacademy.org/learning-paths/2/12).

## First Observations

- Each value starts with `0x`, so the values are hexadecimal, not decimal.
- Each two-digit value represents one byte.
- ASCII maps each byte value to a character. For example, `0x61` is decimal
  `97`, which maps to `a`; `0x7b` maps to `{`.

## Solve Log

- **Tried:** Parsed each `0x`-prefixed value as a hexadecimal byte and decoded
  the byte sequence as ASCII.
  - **Result:** The output matched the Academy flag format.

## Key Idea

Treat the sequence as bytes. Convert each hexadecimal value to its byte value,
keep the original order, then decode the bytes as ASCII.

## Solution Walkthrough

1. Split the input at spaces to get one hexadecimal value per byte.
2. Convert each value from hexadecimal to an integer.
3. Build a byte sequence from those integers.
4. Decode the sequence as ASCII.

## Commands Or Script

```python
values = """0x61 0x63 0x61 0x64 0x65 0x6d 0x79 0x7b 0x34 0x35 0x63 0x31 0x31 0x5f 0x6e 0x30 0x5f 0x71 0x75 0x33 0x35 0x37 0x31 0x30 0x6e 0x35 0x5f 0x31 0x6c 0x6c 0x5f 0x74 0x33 0x31 0x31 0x5f 0x79 0x33 0x5f 0x6e 0x30 0x5f 0x6c 0x31 0x33 0x35 0x5f 0x65 0x39 0x36 0x63 0x38 0x63 0x61 0x38 0x7d"""
flag = bytes(int(value, 16) for value in values.split()).decode("ascii")
print(flag)
```

## Flag

```text
academy{45c11_n0_qu35710n5_1ll_t311_y3_n0_l135_e96c8ca8}
```

## Verification

The Python conversion produced the flag above. CyLab submission and learning
path completion were not confirmed.

## Lessons Learned

- A `0x` prefix marks a hexadecimal value.
- A sequence of ASCII byte values becomes text when decoded in the same order.
- Python can parse prefixed hexadecimal values with `int(value, 16)` and build
  a byte sequence with `bytes(...)`.

## Follow-Up

- Re-solve without notes or AI on 2026-11-04. Record the result in
  [the queue](../../../queue.md).
