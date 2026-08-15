# PW Crack 3

## Metadata

- Platform: CyLab Academy
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: General Skills
- Difficulty: Beginner
- Status: Solved
- Started: 2026-08-15
- Completed: 2026-08-15
- Files: `level3.py`, `level3.flag.txt.enc`, `level3.hash.bin`
- Skills Learned: reading Python lists, comparing MD5 digests, testing candidate passwords

## Problem Summary

The challenge gives a Python script, an encrypted flag file, and a hash file. The script asks for a password, hashes the input, and decrypts the flag only when the input hash matches the stored hash.

## First Observations

`level3.py` reads both challenge files using relative paths:

```python
flag_enc = open('level3.flag.txt.enc', 'rb').read()
correct_pw_hash = open('level3.hash.bin', 'rb').read()
```

So the script should be run from the same directory as those files.

The password check compares MD5 digest bytes:

```python
user_pw_hash = hash_pw(user_pw)

if( user_pw_hash == correct_pw_hash ):
```

The script also gives seven possible passwords:

```python
pos_pw_list = ["6997", "3ac8", "f0ac", "4b17", "ec27", "4e66", "865e"]
```

## Key Idea

We do not need to reverse MD5. Because the candidate list is small, we can hash each candidate using the same `hash_pw()` logic and compare the resulting bytes to `level3.hash.bin`.

The matching candidate is `865e`.

## Solution Walkthrough

1. Open `level3.py`.
2. Find `hash_pw()` and confirm it uses `hashlib.md5()`.
3. Read the candidate password list at the bottom of the file.
4. Hash each candidate with MD5.
5. Compare each digest to the contents of `level3.hash.bin`.
6. Run the script from the challenge directory and enter `865e`.

## Commands Or Script

```sh
cd practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/pw-crack-3
printf '865e\n' | python3 level3.py
```

To check the candidates:

```sh
python3 - <<'PY'
import hashlib
from pathlib import Path

correct = Path("level3.hash.bin").read_bytes()
for pw in ["6997", "3ac8", "f0ac", "4b17", "ec27", "4e66", "865e"]:
    digest = hashlib.md5(pw.encode()).digest()
    print(f"{pw}: {digest.hex()} match={digest == correct}")
PY
```

Output:

```text
6997: c9049d2a46feb0ae2de6b0636f32ea0d match=False
3ac8: 9648ae234bd327d686f9d684342070cd match=False
f0ac: ee7751a05dead01a36378729fd0c204e match=False
4b17: 03078179ea3e83075620b5ed18f95894 match=False
ec27: f41719388902e51c111a5778b4669fcb match=False
4e66: cd6925a9d53245b106a97e303f5e2ef7 match=False
865e: 1b18e1316f9218cc5b053e1cea28e02e match=True
```

## Flag

`picoCTF{m45h_fl1ng1ng_2b072a90}`

## Lessons Learned

- A hash check usually stores only the digest, not the original password.
- If the candidate list is small, hash each candidate and compare digests.
- Match the program's exact encoding and digest format; here it uses `pw_str.encode()` and raw `digest()` bytes.

## Follow-Up

- Practice reading `hashlib` code and identifying whether a program compares hex strings or raw digest bytes.
