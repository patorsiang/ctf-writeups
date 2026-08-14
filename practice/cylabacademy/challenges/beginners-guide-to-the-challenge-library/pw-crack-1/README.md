# PW Crack 1

## Metadata

- Platform: CyLab Academy
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: General Skills
- Difficulty: Beginner
- Status: Solved
- Started: 2026-08-14
- Completed: 2026-08-14
- Files: `level1.py`, `level1.flag.txt.enc`
- Skills Learned: reading Python conditionals, running scripts from the right working directory

## Problem Summary

The challenge gives a Python script and an encrypted flag file. The script asks for a password, then decrypts the flag if the password is correct.

## First Observations

`level1.py` reads `level1.flag.txt.enc` using a relative path:

```python
flag_enc = open('level1.flag.txt.enc', 'rb').read()
```

That means the script should be run from the same directory as the encrypted file.

The password check is also directly visible in the source:

```python
if( user_pw == "1e1a"):
```

## Key Idea

This is not a password cracking problem yet. The correct password is hard-coded in the Python source, so reading the condition gives the answer.

## Solution Walkthrough

1. Open `level1.py`.
2. Find the `level_1_pw_check()` function.
3. Read the `if` condition that compares `user_pw` to the expected password.
4. Run the script from the challenge directory and enter `1e1a`.

## Commands Or Script

```sh
cd practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/pw-crack-1
python3 level1.py
```

Or non-interactively:

```sh
printf '1e1a\n' | python3 level1.py
```

## Flag

`picoCTF{545h_r1ng1ng_fa343060}`

## Lessons Learned

- Read the source before guessing passwords.
- A hard-coded comparison like `user_pw == "1e1a"` reveals the expected input.
- Relative file paths depend on the current working directory.

## Follow-Up

- Keep watching how later password challenges make the password less obvious.
