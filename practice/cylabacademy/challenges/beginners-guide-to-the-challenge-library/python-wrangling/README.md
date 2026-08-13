# Python Wrangling

## Metadata

- Platform: CyLab Academy / picoCTF
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: General Skills
- Difficulty: Beginner
- Status: Solved
- Started: 2026-08-13
- Completed: 2026-08-13
- Files: `ende.py`, `flag.txt.en`, `password.txt`
- Skills Learned: Python scripts, command arguments, virtual environments, file decryption

## Problem Summary

The challenge provides a Python helper script, an encrypted flag file, and a
password file. Use the script to decrypt `flag.txt.en` and recover the picoCTF
flag.

## First Observations

```bash
file ende.py flag.txt.en password.txt
```

```text
ende.py:      Python script text executable, ASCII text
flag.txt.en:  ASCII text, with no line terminators
password.txt: ASCII text
```

The script imports `cryptography.fernet.Fernet`, so it needs the `cryptography`
Python package before it can run.

## What I Tried

Trying to run the script name directly did not work:

```bash
ende.py -h
```

```text
zsh: command not found: ende.py
```

That happens because the current directory is not searched as a command path by
default. Running it through Python is the right habit:

```bash
python ende.py -h
```

At first, that failed because `cryptography` was missing. Since the system
Python environment is externally managed, I created a local virtual environment
for this challenge.

## Key Idea

Read the script's interface instead of guessing. The help text shows that
decryption uses:

```bash
python ende.py -d <file>
```

The password is provided separately in `password.txt`. The script can prompt for
it interactively, or it can receive the password as a third command-line
argument.

## Solution Walkthrough

From the challenge folder, create a local environment and install the required
dependency:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --no-cache-dir cryptography
```

Check the script help:

```bash
.venv/bin/python ende.py -h
```

```text
Usage: ende.py (-e/-d) [file]
Examples:
  To decrypt a file named 'pole.txt', do: '$ python ende.py -d pole.txt'
```

Decrypt the encrypted flag file:

```bash
.venv/bin/python ende.py -d flag.txt.en "$(cat password.txt)"
```

Output:

```text
picoCTF{4p0110_1n_7h3_h0us3_9c5f9bcf}
```

## Commands Or Script

```bash
cd practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/python-wrangling
python3 -m venv .venv
.venv/bin/python -m pip install --no-cache-dir cryptography
.venv/bin/python ende.py -d flag.txt.en "$(cat password.txt)"
```

## Flag

```text
picoCTF{4p0110_1n_7h3_h0us3_9c5f9bcf}
```

## Lessons Learned

- Use `python script.py ...` when a Python file is not installed as a shell
  command.
- `cd` only affects the current shell session; commands run from another working
  directory need full paths or a new `cd`.
- Use a virtual environment when a Python package is needed for one challenge.
- Read helper-script usage before solving; the intended decrypt mode was already
  exposed by `-h`.

## Follow-Up

- Practice passing command-line arguments and reading `sys.argv` in small Python
  scripts.
