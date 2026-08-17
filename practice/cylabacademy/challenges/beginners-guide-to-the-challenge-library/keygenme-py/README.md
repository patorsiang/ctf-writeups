# Keygenme Py

## Metadata

- Platform: CyLab Academy / picoCTF
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: Reverse Engineering
- Difficulty: Beginner
- Status: Solved
- Started: 2026-08-17
- Completed: 2026-08-17
- Files: `keygenme-trial.py`, `keygenme.py`
- Skills Learned: Python source review, key validation logic, SHA-256 indexing, interactive program execution

## Problem Summary

The challenge gives a trial Python program for an "Arcane Calculator."
The goal is to generate a valid license key that unlocks the full version.

This is reverse engineering from source code. The important part is not the
calculator menu. The important part is the license validation function.

## First Observations

Running the trial with the system `python` failed because the global
interpreter did not have `cryptography` installed:

```text
ModuleNotFoundError: No module named 'cryptography'
```

The repo virtualenv already had the dependency, so the working command was:

```sh
.venv/bin/python practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/keygenme-py/keygenme-trial.py
```

When running an interactive program, stdin must stay open. A non-interactive
run can fail at `input()` with:

```text
EOFError: EOF when reading a line
```

## Key Idea

**Read the key checker instead of guessing license keys.**

The program defines the fixed parts of the key near the top:

```python
key_part_static1_trial = "picoCTF{1n_7h3_kk3y_of_"
key_part_dynamic1_trial = "xxxxxxxx"
key_part_static2_trial = "}"
```

That means the license key must have this shape:

```text
picoCTF{1n_7h3_kk3y_of_????????}
```

The dynamic 8-character part comes from selected characters in:

```python
hashlib.sha256(b"BENNETT").hexdigest()
```

## Solution Walkthrough

The trial username appears in two forms:

```python
username_trial = "BENNETT"
bUsername_trial = b"BENNETT"
```

When the user enters a license key, the program passes the byte-string username
into `check_key()`:

```python
if check_key(user_key, bUsername_trial):
```

Inside `check_key()`, the static prefix is checked first. Then the program
compares each dynamic character against selected positions from the SHA-256
hex digest:

```python
if key[i] != hashlib.sha256(username_trial).hexdigest()[4]:
if key[i] != hashlib.sha256(username_trial).hexdigest()[5]:
if key[i] != hashlib.sha256(username_trial).hexdigest()[3]:
if key[i] != hashlib.sha256(username_trial).hexdigest()[6]:
if key[i] != hashlib.sha256(username_trial).hexdigest()[2]:
if key[i] != hashlib.sha256(username_trial).hexdigest()[7]:
if key[i] != hashlib.sha256(username_trial).hexdigest()[1]:
if key[i] != hashlib.sha256(username_trial).hexdigest()[8]:
```

So the dynamic characters use these hash indexes:

```text
4, 5, 3, 6, 2, 7, 1, 8
```

Compute the hash and select those positions:

```sh
.venv/bin/python -c "import hashlib; h=hashlib.sha256(b'BENNETT').hexdigest(); print(h); print(''.join(h[i] for i in [4,5,3,6,2,7,1,8]))"
```

Output:

```text
ba6c084a4d888e1f7c3b0fc71d61c4625708bd915b5e0e60eb73e1667251b567
08c46aa4
```

Build the full license key:

```text
picoCTF{1n_7h3_kk3y_of_08c46aa4}
```

After entering that key, the trial decrypts the full version:

```text
Full version written to 'keygenme.py'.
```

## Commands Or Script

Run from the repo root to derive the dynamic part:

```sh
.venv/bin/python -c "import hashlib; h=hashlib.sha256(b'BENNETT').hexdigest(); print(''.join(h[i] for i in [4,5,3,6,2,7,1,8]))"
```

Run the challenge from its directory so the generated full version stays with
the challenge files:

```sh
cd practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/keygenme-py
../../../../../.venv/bin/python keygenme-trial.py
```

Then choose `c` and enter:

```text
picoCTF{1n_7h3_kk3y_of_08c46aa4}
```

## Flag

```text
picoCTF{1n_7h3_kk3y_of_08c46aa4}
```

## Lessons Learned

- In source-based reverse engineering, start from the validation function.
- A hash does not need to be reversed if the program tells you exactly which
  derived characters it expects.
- Python byte strings like `b"BENNETT"` matter because hashes operate on bytes.
- Run interactive programs in a terminal session, or pipe input deliberately.

## Follow-Up

- For later keygen challenges, look for the same pattern: fixed prefix, dynamic
  generated characters, and a final unlock or decrypt step.
