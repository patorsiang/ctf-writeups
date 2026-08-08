# strings it

## Metadata

- Platform: CyLab Academy / picoCTF
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: General Skills
- Difficulty: Beginner
- Status: Solved
- Started: 2026-08-09
- Completed: 2026-08-09
- Files: `strings` (ELF 64-bit x86-64, 768 KB), `solve.py`, `test_recon.py`
- Skills Learned: `strings`, printable-run scanning, static vs dynamic analysis, UTF-16 misses

## Problem Summary

A binary named `strings` is provided. Find the flag inside it.

The file name is the hint and the joke: the tool that solves this is also
called `strings`, so the command reads `strings strings`.

## First Observations

```bash
file strings
# ELF 64-bit LSB pie executable, x86-64, ... for GNU/Linux 3.2.0, not stripped

du -h strings          # 768K
strings strings | wc -l # 19243
```

19,243 printable runs is exactly the "really tedious to look through
manually" the challenge is pointing at. The answer is not to read them —
it is to filter them.

## Key Idea

**`strings` does not execute anything.** It opens the file, walks the
bytes, and reports runs of printable characters. Three rules, total:

1. scan for runs of printable characters
2. a run ends at the first non-printable byte — usually the `NUL` that
   terminates a C string
3. emit runs of at least `min_len` characters (default 4), discard the rest

That single fact answers the question this challenge quietly poses.
[Wave a Flag](../wave-a-flag/README.md) and
[Tab, Tab, Attack](../tab-tab-attack/README.md) both needed
`docker --platform linux/amd64`, because running a Linux x86-64 binary on
an arm64 Mac is impossible without emulation. **This one needs no Docker
at all** — nothing is being run. The bytes are just bytes, and the host's
OS and CPU are irrelevant to reading them.

That is the difference between **static** analysis (inspect the artifact)
and **dynamic** analysis (execute it and watch). Static is cheaper, safer,
and platform-independent. Reach for it first — especially with untrusted
binaries, where executing is the risky step.

### Why the flag is there to be found

The flag is a plain C string literal compiled into `.rodata`:

```python
data[0x1caa0:0x1caa0 + 28]   # b'picoCTF{5tRIng5_1T_1067EC4c}'
data[0x1caa0 - 1]            # 0   <- NUL before
data[0x1caa0 + 28]           # 0   <- NUL after
```

Compile-time constants are stored verbatim. Compilation is not encryption
and it is not obfuscation — a string in your source is a string in your
binary.

## Solution Walkthrough

```bash
strings strings | grep -i pico
```

```text
picoCTF{5tRIng5_1T_1067EC4c}
```

Useful variations:

| Command | Why |
| --- | --- |
| `strings -t x file` | prefix each hit with its **hex offset** — here `1caa0` |
| `strings -n 8 file` | raise the minimum length to cut noise |
| `strings -e l file` | scan **UTF-16LE** — essential for Windows binaries |
| `strings file \| grep -iE 'flag\|pass\|key\|http'` | broader first sweep than `pico` alone |

Note `./strings` would *execute* the file and fail with `exec format
error`. The file is an **argument** here, not a command.

## Commands Or Script

[`solve.py`](solve.py) reimplements the scan rather than shelling out,
because the three rules above are the whole lesson:

```bash
python3 solve.py              # scan the challenge file
python3 solve.py FILE --all   # dump every string with offsets
```

```text
FLAG @ 0x1caa0: picoCTF{5tRIng5_1T_1067EC4c}
```

[`test_recon.py`](test_recon.py) — 13 tests. The headline one is
**differential against the system tool over the real 768 KB binary**:

```text
mine: 19240 unique strings
strings -n 4: 19240 unique strings     # exact set equality
```

A reimplementation is only credible if it agrees with the real thing on
real input, not just on toy examples. The rest cover the scan rules on
inputs small enough to reason about — min-length boundary, non-printable
terminating a run, offsets pointing at the first character, and a run
that reaches end-of-file with no terminator (an off-by-one there silently
drops the last string of every file).

Tests needing the 768 KB binary **skip** rather than fail if it is absent,
so a fresh clone still runs 10 of 13:

```console
$ python3 test_recon.py
10 passed, 3 skipped
```

## Flag

```text
picoCTF{5tRIng5_1T_1067EC4c}
```

## Lessons Learned

- **Static beats dynamic as a first move.** Reading a file needs no
  matching OS or CPU and cannot be harmed by what the file does. Run it
  only once reading has stopped paying — and with untrusted binaries,
  ideally in a container.
- **Compilation is not obfuscation.** Hardcoded credentials, API keys,
  internal URLs and debug messages all survive into the binary in
  plaintext. `strings` is the first command anyone points at a mobile
  app, desktop binary, or firmware image, and it is routinely enough.
- **An empty `strings` result is not evidence of no strings.** Windows
  binaries store text as UTF-16LE, where every character is followed by a
  NUL — so an ASCII scan finds nothing and reports nothing, silently.
  `strings -e l` is the fix. The failure mode is a quiet empty list, not
  an error, which is what makes it dangerous.
- **`-t x` gives offsets**, which turns "the flag is in here somewhere"
  into a place to look in a hex editor or disassembler.
- **`not stripped` in `file` output was the tell.** Symbols and literals
  intact means static analysis will be productive.

## Follow-Up

- Expanded the `strings` entry in
  [../../../../../notes/general.md](../../../../../notes/general.md) with
  the scan rules, static-vs-dynamic framing, and the UTF-16 trap.
- Next step up from `strings` is a disassembler (`objdump -d`, Ghidra)
  when the interesting data is computed rather than stored — see
  [../../../../../notes/pwn.md](../../../../../notes/pwn.md).
