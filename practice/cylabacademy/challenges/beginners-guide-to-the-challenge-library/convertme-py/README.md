# convertme.py

## Metadata

- Platform: CyLab Academy / picoCTF
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: General Skills
- Difficulty: Beginner
- Status: Solved
- Started: 2026-10-23
- Completed: 2026-10-23
- Re-solve: n/a
- Files: `convertme.py`
- Skills Learned: Decimal-to-binary conversion by repeated division, interactive Python input

## Problem Summary

The script asks for a random decimal number converted to binary. A correct answer prints the flag. Source: [CyLab Academy](https://learn.cylabacademy.org/learning-paths/14/96).

## Prediction

- Guess: Not recorded before source inspection.
- Score: n/a

## First Observations

- The script first displayed `35` and then raised `EOFError` at `input()` because the command runner had no interactive input.
- Adding `35` after the script name did not answer the prompt. The script reads from standard input and chooses its own random number.
- A later run displayed `56`.

## Solve Log

- **Thought:** Convert `56` from base 10 to base 2.
  - **Tried:** Repeatedly divide by 2 and keep each remainder.
  - **Result:** `56 / 2 = 28 r0`, `28 / 2 = 14 r0`, `14 / 2 = 7 r0`, `7 / 2 = 3 r1`, `3 / 2 = 1 r1`, and `1 / 2 = 0 r1`.
- **Thought:** Read the remainders from bottom to top.
  - **Tried:** Entered `110000` first.
  - **Result:** One `1` was missing. Reading all six remainders in reverse gives `111000`.

## Key Idea

The remainder list runs from least significant bit to most significant bit. Reverse it to form the binary number.

## Solution Walkthrough

1. Divide the decimal number by 2.
2. Record the remainder and repeat with the quotient until the quotient is 0.
3. Read the remainders from bottom to top.
4. Check the result by converting it back to decimal. For `56`, `111000` is `32 + 16 + 8`.

## Commands Or Script

Run the script in an interactive terminal so `input()` can read the answer:

```sh
python3 convertme.py
```

For the prompt value `56`, enter `111000`.

## Flag

```text
academy{4ll_y0ur_b4535_5dbc7d96}
```

## Lessons Learned

- Reverse the remainders from repeated division; reading them in the original order reverses the bit significance.
- Programs using `input()` need an interactive terminal or supplied standard input. A command-line argument does not answer an `input()` prompt.

## Follow-Up

- Practice the same decimal-to-binary conversion from [2warm](../2warm/README.md).
