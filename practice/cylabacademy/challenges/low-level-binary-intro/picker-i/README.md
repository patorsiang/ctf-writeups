# Picker I

## Metadata

- Platform: CyLab Academy
- Learning Path: Low Level Binary Intro
- Category: Reverse Engineering
- Difficulty: Easy
- Status: Solved; flag recovered, portal submission not confirmed
- Started: 2026-10-29
- Completed: 2026-10-29
- Re-solve: due 2026-11-05
- Files: [`picker-I.py`](picker-I.py)
- Skills Learned: Python function dispatch, source-code triage, hexadecimal ASCII decoding

## Problem Summary

The service accepts a function name and calls it. The provided Python source contains a harmless-looking `getRandomNumber()` function and a `win()` function that reads the flag and prints its characters as hexadecimal code points.

Source: [CyLab Academy: Picker I](https://learn.cylabacademy.org/learning-paths/2/14).

## First Observations

- The service suggests `getRandomNumber`; entering it prints `4` and returns to the prompt.
- The source contains large embedded C snippets, but the input loop and Python function definitions are the useful parts.
- The loop runs `eval(user_input + '()')`, so it appends call syntax to the supplied function name.

## Solve Log

- **Tried:** Entered `getRandomNumber` at the service prompt.
  - **Result:** The service printed `4`; this confirmed the function call worked.
- **Inspected:** Read `picker-I.py` and found `win()` plus the loop that evaluates the supplied name as a function call.
- **Tried:** Entered `win` without parentheses.
  - **Result:** The service printed the flag as hexadecimal values.
- **Decoded:** Parsed each `0x`-prefixed byte and decoded the ordered bytes as ASCII. Two adjacent values had no separating space in the output, so the parser matched each `0xNN` value directly.

## Key Idea

Read the input loop before guessing. The service calls any function name accepted by its `eval()` expression. `win()` exposes the flag, but encodes each character as a hexadecimal code point.

## Solution Walkthrough

1. Connect to the instance:

   ```sh
   nc chatelaine.cylabacademy.net 43198
   ```

2. Enter `getRandomNumber` at the `==>` prompt. The service prints `4` and asks for another name.
3. Inspect `picker-I.py`. The loop uses `eval(user_input + '()')`, and `win()` prints the flag as hexadecimal values.
4. Enter `win` without parentheses. The service adds `()` and calls the function.
5. Decode the hexadecimal values as ASCII. This parser handles adjacent values such as `0x300x6e`:

   ```python
   import re

   output = """0x61 0x63 0x61 0x64 0x65 0x6d 0x79 0x7b 0x34 0x5f 0x64 0x31 0x34 0x6d 0x300x6e 0x64 0x5f 0x31 0x6e 0x5f 0x37 0x68 0x33 0x5f 0x72 0x30 0x75 0x67 0x680x5f 0x33 0x33 0x39 0x38 0x34 0x31 0x38 0x38 0x7d"""
   values = re.findall(r"0x[0-9a-fA-F]{2}", output)
   flag = bytes(int(value, 16) for value in values).decode("ascii")
   print(flag)
   ```

## Flag

```text
academy{4_d14m0nd_1n_7h3_r0ugh_33984188}
```

## Verification

The `win` function returned the flag bytes, and ASCII decoding produced the flag above. CyLab portal submission and learning-path completion are not confirmed.

## Lessons Learned

- Follow the input path into the program. Here, `eval(user_input + '()')` turns input into a Python function call.
- Skip large unrelated embedded code when the challenge's Python control flow answers the question.
- Hexadecimal character values can be decoded as an ordered ASCII byte sequence.

## Follow-Up

- Re-solve without notes or AI on 2026-11-05. Record the result in [the queue](../../../queue.md).
