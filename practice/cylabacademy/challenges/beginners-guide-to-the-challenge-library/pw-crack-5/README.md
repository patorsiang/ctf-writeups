# PW Crack 5

## Metadata

- Platform: CyLab Academy
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: General Skills
- Difficulty: Beginner
- Status: Solved
- Started: 2026-08-15
- Completed: 2026-08-15
- Files: `level5.py`, `level5.flag.txt.enc`, `level5.hash.bin`, `dictionary.txt`
- Skills Learned: dictionary attacks, reading files line by line, comparing MD5 digests

## Problem Summary

The challenge gives a Python script, an encrypted flag file, a hash file, and a dictionary of possible passwords. The script asks for a password, hashes the input with MD5, and decrypts the flag only when the input hash matches the stored hash.

## First Observations

`level5.py` reads both challenge files using relative paths:

```python
flag_enc = open('level5.flag.txt.enc', 'rb').read()
correct_pw_hash = open('level5.hash.bin', 'rb').read()
```

So the script should be run from the same directory as those files.

The password check still compares raw MD5 digest bytes:

```python
user_pw_hash = hash_pw(user_pw)

if( user_pw_hash == correct_pw_hash ):
```

Unlike PW Crack 3 and 4, the possible passwords are not embedded in `level5.py`. They are stored in `dictionary.txt`, which contains every four-hex-digit value from `0000` through `ffff`.

## Key Idea

This is a dictionary attack. We do not need to reverse MD5; we hash each candidate from `dictionary.txt` using the same logic as the checker and compare each digest to `level5.hash.bin`.

The matching candidate is `9581`.

## Solution Walkthrough

1. Open `level5.py`.
2. Confirm `hash_pw()` uses `hashlib.md5()` and returns raw `digest()` bytes.
3. Read candidates from `dictionary.txt`, one line at a time.
4. Strip the newline from each candidate.
5. Hash each candidate with MD5.
6. Compare each digest to the contents of `level5.hash.bin`.
7. Run the script from the challenge directory and enter `9581`.

## Commands Or Script

```sh
cd practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/pw-crack-5
printf '9581\n' | python3 level5.py
```

To find the matching dictionary entry:

```sh
python3 - <<'PY'
import hashlib
from pathlib import Path

correct = Path("level5.hash.bin").read_bytes()

for line_no, raw in enumerate(Path("dictionary.txt").read_text().splitlines(), 1):
    pw = raw.strip()
    digest = hashlib.md5(pw.encode()).digest()
    if digest == correct:
        print(f"line={line_no} password={pw} md5={digest.hex()}")
        break
PY
```

Output:

```text
line=38274 password=9581 md5=123650dd0560587918b3d771cf0c0171
```

## Flag

`picoCTF{h45h_sl1ng1ng_36e992a6}`

## Lessons Learned

- A dictionary attack hashes known candidates and compares the resulting digests.
- Newlines from dictionary files should not be part of the password unless the checker includes them.
- `splitlines()` is a clean way to read candidate words without trailing newline characters.

## Follow-Up

- Practice streaming large dictionaries line by line instead of loading the whole file when the list becomes much larger.
