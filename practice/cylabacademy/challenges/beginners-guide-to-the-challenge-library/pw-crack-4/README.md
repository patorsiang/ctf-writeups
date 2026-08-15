# PW Crack 4

## Metadata

- Platform: CyLab Academy
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: General Skills
- Difficulty: Beginner
- Status: Solved
- Started: 2026-08-15
- Completed: 2026-08-15
- Files: `level4.py`, `level4.flag.txt.enc`, `level4.hash.bin`
- Skills Learned: parsing Python literals, checking many password candidates, comparing MD5 digests

## Problem Summary

The challenge gives a Python script, an encrypted flag file, and a hash file. The script asks for a password, hashes the input with MD5, and decrypts the flag only when the input hash matches the stored hash.

## First Observations

`level4.py` reads both challenge files using relative paths:

```python
flag_enc = open('level4.flag.txt.enc', 'rb').read()
correct_pw_hash = open('level4.hash.bin', 'rb').read()
```

So the script should be run from the same directory as those files.

The password check compares raw MD5 digest bytes:

```python
user_pw_hash = hash_pw(user_pw)

if( user_pw_hash == correct_pw_hash ):
```

The script also includes `pos_pw_list`, which contains 100 possible passwords.

## Key Idea

This is the same hash-check idea as PW Crack 3, but the candidate list is longer. Instead of copying 100 strings by hand, parse `pos_pw_list` from the Python source and hash each candidate the same way the checker does.

The matching candidate is `8b95`.

## Solution Walkthrough

1. Open `level4.py`.
2. Confirm `hash_pw()` uses `hashlib.md5()` and returns raw `digest()` bytes.
3. Extract the `pos_pw_list` candidates from the script.
4. Hash each candidate with MD5.
5. Compare each digest to the contents of `level4.hash.bin`.
6. Run the script from the challenge directory and enter `8b95`.

## Commands Or Script

```sh
cd practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/pw-crack-4
printf '8b95\n' | python3 level4.py
```

To check all candidates without manually copying the list:

```sh
python3 - <<'PY'
import ast
import hashlib
from pathlib import Path

source = Path("level4.py").read_text()
module = ast.parse(source)
candidates = []

for node in module.body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "pos_pw_list":
                candidates = ast.literal_eval(node.value)

correct = Path("level4.hash.bin").read_bytes()
for pw in candidates:
    digest = hashlib.md5(pw.encode()).digest()
    if digest == correct:
        print(f"{pw}: {digest.hex()}")
PY
```

Output:

```text
8b95: d3d58c4786a6a229427351500ac7abd7
```

## Flag

`picoCTF{fl45h_5pr1ng1ng_cf341ff1}`

## Lessons Learned

- A longer candidate list should be automated instead of checked manually.
- `ast.literal_eval()` can safely read a Python literal list from source code.
- Compare the same digest format as the checker; this script compares raw `digest()` bytes, not hex strings.

## Follow-Up

- Practice extracting structured values from source code before reaching for brittle text parsing.
