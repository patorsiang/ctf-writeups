# PW Crack 2

## Metadata

- Platform: CyLab Academy
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: General Skills
- Difficulty: Beginner
- Status: Solved
- Started: 2026-08-14
- Completed: 2026-08-14
- Files: `level2.py`, `level2.flag.txt.enc`
- Skills Learned: reading Python expressions, converting hex character codes

## Problem Summary

The challenge gives a Python script and an encrypted flag file. The script asks for a password, then decrypts the flag if the input matches the expected password.

## First Observations

`level2.py` reads the encrypted flag using a relative path:

```python
flag_enc = open('level2.flag.txt.enc', 'rb').read()
```

So the script should be run from the same directory as `level2.flag.txt.enc`.

The password check is visible in the source:

```python
if( user_pw == chr(0x64) + chr(0x65) + chr(0x37) + chr(0x36) ):
```

## Key Idea

The password is still in the source, but this time each character is written as a hex number and converted with `chr()`.

Python's `chr()` converts a numeric code point into the matching character:

- `chr(0x64)` -> `d`
- `chr(0x65)` -> `e`
- `chr(0x37)` -> `7`
- `chr(0x36)` -> `6`

So the password is `de76`.

## Solution Walkthrough

1. Open `level2.py`.
2. Find the `level_2_pw_check()` function.
3. Read the password expression inside the `if` condition.
4. Convert each `chr(0x...)` value to its character.
5. Run the script from the challenge directory and enter `de76`.

## Commands Or Script

```sh
cd practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/pw-crack-2
python3 level2.py
```

Or non-interactively:

```sh
printf 'de76\n' | python3 level2.py
```

## Flag

`picoCTF{tr45h_51ng1ng_489dea9a}`

## Lessons Learned

- `chr()` turns an integer into a character.
- Hex values like `0x64` are just numbers written in base 16.
- When a password expression is visible, simplify the expression before guessing.

## Follow-Up

- Practice converting small hex values to ASCII by hand and with Python.
