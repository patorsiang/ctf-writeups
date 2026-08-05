# Tab, Tab, Attack

## Metadata

- Platform: CyLab Academy / picoCTF
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: General Skills
- Difficulty: Beginner
- Status: Solved
- Started: 2026-08-05
- Completed: 2026-08-05
- Files: `Addadshashanammu.zip`
- Skills Learned: tab completion, shell globbing, zip-slip check before extracting, absolute vs relative paths

## Problem Summary

> Using tabcomplete in the Terminal will add years to your life, esp. when
> dealing with long rambling directory structures and filenames.

The challenge provides `Addadshashanammu.zip`. Extract it, navigate to the
bottom of a deeply nested directory tree, and run the binary there.

## First Observations

Before extracting anything, list the archive rather than trusting it:

```bash
unzip -Z1 Addadshashanammu.zip | grep -E '^/|\.\.'    # no output = clean
```

Nine entries, no absolute paths, no `..` — safe to extract. See the
zip-slip note under Lessons Learned for why this is worth doing every time.

After extraction:

- **7 levels** of directories, each with exactly one child
- At the bottom, two files: `fang-of-haynekhtnamet` and its `.c` source

```text
Addadshashanammu/Almurbalarammi/Ashalmimilkala/Assurnabitashpi/
  Maelkashishi/Onnissiralis/Ularradallaku/
    fang-of-haynekhtnamet
    fang-of-haynekhtnamet.c
```

The names are unpronounceable Mesopotamian deities on purpose — typing
them by hand is exactly the misery the challenge wants you to avoid.

```bash
file fang-of-haynekhtnamet
# ELF 64-bit LSB pie executable, x86-64, ... for GNU/Linux 3.2.0, not stripped
```

Same platform mismatch as [Wave a Flag](../wave-a-flag/README.md): Linux
x86-64 binary, arm64 macOS host.

## Key Idea

**Never type a long path by hand.** The shell offers two separate
mechanisms, and knowing both is the lesson:

| Mechanism | When it runs | How it works |
| --- | --- | --- |
| **Tab completion** | interactively, as you type | shell fills in the unique match; two Tabs lists candidates when ambiguous |
| **Globbing** (`*`) | when the command executes | shell expands the pattern into matching paths before running anything |

Tab is for exploring — you see each name as it appears. Globbing is for
scripting and for skipping levels wholesale:

```bash
cd Addadshashanammu/*/*/*/*/*/*/    # six levels in one command
```

Each `*/` matches the single subdirectory at that level, so the whole
descent takes one line and zero typed deity names.

A detail worth noticing: at the top level, `Addadshashanammu` and
`Addadshashanammu.zip` share a prefix, yet `cd Add`+Tab still completes
cleanly. Zsh knows `cd` only accepts directories, so the zip was never a
candidate. Completion is context-aware, not just prefix matching.

## What I Tried

The descent itself was uneventful; the friction was elsewhere.

**Shell working directory drifted.** Several `cd` commands did not persist
as expected between steps, producing:

```console
$ cd practice/cylabacademy/
(eval):cd:1: no such file or directory: practice/cylabacademy/
```

That is error case #1 from the triage table in
[../wave-a-flag/README.md](../wave-a-flag/README.md) — the path is wrong
because the shell is not where it is assumed to be, not because anything
is missing. `pwd` first, or use an absolute path and make the question
irrelevant. Relative paths are only as good as your belief about `$PWD`.

## Solution Walkthrough

```bash
# 1. Inspect before extracting
unzip -Z1 Addadshashanammu.zip | grep -E '^/|\.\.'   # expect no output
unzip -q Addadshashanammu.zip

# 2. Descend -- Tab completion interactively, or one glob
cd Addadshashanammu/*/*/*/*/*/*/
pwd     # .../Onnissiralis/Ularradallaku

# 3. Run it: Linux x86-64 binary on an arm64 macOS host
docker run --rm --platform linux/amd64 \
  -v "$PWD:/w" -w /w \
  debian:stable-slim ./fang-of-haynekhtnamet
```

```text
*ZAP!* picoCTF{l3v3l_up!_t4k3_4_r35t!_fc588427}
```

The Docker one-liner came straight from
[../../../../../notes/general.md](../../../../../notes/general.md), written
up after Wave a Flag, and worked first try — which is the entire argument
for keeping notes.

### Route not taken: read the source

`fang-of-haynekhtnamet.c` ships alongside the binary, so the flag is
readable without executing anything. Same trade-off as `strings` in Wave a
Flag: faster, but skips the exercise. Reading provided source *is* the
right move when a binary is untrusted or when the challenge is genuinely
about the logic.

## Commands Or Script

No `solve.py`. The solve is `cd` plus one `docker run`; there is no
derivation to pin down.

## Flag

```text
picoCTF{l3v3l_up!_t4k3_4_r35t!_fc588427}
```

## Lessons Learned

- **Check an archive before extracting it.** `unzip -Z1 file.zip` lists
  entries without writing anything. An entry like `../../.ssh/authorized_keys`
  will be written *outside* the directory you are standing in — this is
  **zip-slip**, a real CVE class that has hit widely-used libraries. The
  check costs one command and applies to any untrusted archive, not just
  CTF files. `tar -tf` is the equivalent for tarballs.
- **Tab and `*` solve the same problem at different times.** Tab completes
  interactively while you type; globs expand at execution. Reach for Tab
  when exploring, globs when scripting or skipping known-shape structures.
- **Absolute paths remove a whole class of error.** When `cd` fails with
  "no such file or directory" and the path looks right, check `pwd` before
  doubting the file. A relative path is a claim about where you are.
- **Notes compound.** The platform fix here was zero effort because it was
  already written down after the previous challenge. The second time a
  problem appears is when the writeup pays for itself.

## Follow-Up

- Added tab completion, globbing, and the archive-inspection habit to
  [../../../../../notes/general.md](../../../../../notes/general.md).
- Binary execution and the error triage table live in
  [../wave-a-flag/README.md](../wave-a-flag/README.md).
