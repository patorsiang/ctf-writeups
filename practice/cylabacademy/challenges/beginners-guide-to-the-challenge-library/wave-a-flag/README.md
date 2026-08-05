# Wave a Flag

## Metadata

- Platform: CyLab Academy / picoCTF
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: General Skills
- Difficulty: Beginner
- Status: Solved
- Started: 2026-08-05
- Completed: 2026-08-05
- Files: `warm` (ELF 64-bit x86-64, not committed — see Follow-Up)
- Skills Learned: `file`, executable permission bit, `./` vs `$PATH`, exec format error, running foreign binaries in Docker

## Problem Summary

> Can you invoke help flags for a tool or binary? This program has
> extraordinarily helpful information...

The challenge provides a binary named `warm`. Run it in a way that makes it
print the flag.

## First Observations

```bash
file warm
```

```text
warm: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV),
dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2,
BuildID[sha1]=9e46ec87..., for GNU/Linux 3.2.0, with debug_info, not stripped
```

Every field earns attention:

| Field | Meaning | Why it matters |
| --- | --- | --- |
| `ELF` | Linux/Unix executable format | Names the OS family immediately |
| `64-bit LSB` | 64-bit, little-endian | Byte order matters in pwn/forensics |
| `pie executable` | Position-Independent, random load base | ASLR — in pwn, decides whether a leak is needed before any address is usable |
| `x86-64` | CPU architecture | Must match the host |
| `dynamically linked` + `interpreter` | needs glibc, loaded by `ld-linux` | A musl image (Alpine) would fail with a different, confusing error |
| `with debug_info`, `not stripped` | symbols and debug data intact | Reversing would be easy; also why `strings` finds the flag |

**The host is macOS on arm64. The binary is Linux on x86-64. Both axes
mismatch.**

## What I Tried

The solve was three failures in a row, and the failures are the lesson.

**1. `no such file or directory`**

```console
$ ./warm
(eval):1: no such file or directory: ./warm
```

Not a platform problem — the shell was still in the repo root, so the
relative path pointed at nothing. A typo (`./warn`) produced the identical
message, which shows how little this error narrows things down.

Also worth knowing why `./` is required at all: the shell resolves bare
command names against `$PATH`, and `.` is deliberately **not** on `$PATH`.
If it were, dropping a file named `ls` into a directory would hijack the
next `ls` anyone ran there. So a program in the current directory must be
named by path.

**2. Permission — already fine here**

```console
$ ls -l warm
-rwxr-xr-x@ 1 ... warm
```

The `x` bit was already set. Had it not been (the usual state for a fresh
download), the error would have been `permission denied` and the fix
`chmod +x warm`. The execute bit is not a property of the contents — a
perfectly valid program refuses to run without it.

**3. `exec format error` — the real obstacle**

```console
$ cd .../wave-a-flag && ./warm
(eval):1: exec format error: ./warm
```

Nothing is wrong with the file or the path. macOS has no idea how to load
an ELF, and even if it did, the instructions inside target a different CPU.
No amount of `chmod` or path-fixing helps.

## Key Idea

Two separate ideas, and only one of them is the stated puzzle.

**The stated puzzle:** essentially every command-line program accepts a
conventional flag that prints usage instead of doing its job. Running the
binary bare says so outright:

```text
Hello user! Pass me a -h to learn what I can do!
```

**The actual work:** getting to the point where you can run it at all. A
compiled binary carries an OS and an architecture baked in; being *valid*
and being *runnable here* are different properties.

### Error Triage

Three lookalike messages, three unrelated causes. Worth memorising:

| Message | Actual meaning | Fix |
| --- | --- | --- |
| `no such file or directory` | wrong path, or name misspelled | check `pwd`, check spelling |
| `permission denied` | file present, execute bit off | `chmod +x` |
| `exec format error` | file present and executable, built for another OS/CPU | run it somewhere that matches |

(On Linux, `no such file or directory` on a binary that clearly exists is a
fourth case: the *dynamic loader* named in the `interpreter` field is
missing. Same message, different subject.)

## Solution Walkthrough

### Route taken: Docker with an emulated x86-64 Linux

```bash
docker run --rm --platform linux/amd64 \
  -v "$PWD:/w" -w /w \
  debian:stable-slim ./warm -h
```

| Flag | Purpose |
| --- | --- |
| `--rm` | delete the container on exit; avoids accumulating dead containers |
| `--platform linux/amd64` | **the fix** — requests the x86-64 image and emulates that CPU, solving OS and arch at once |
| `-v "$PWD:/w"` | bind-mount the current directory in; a container cannot otherwise see `warm` |
| `-w /w` | set working directory so `./warm` resolves |
| `debian:stable-slim` | any glibc Linux; Alpine (musl) would fail differently |

Output:

```text
Hello user! Pass me a -h to learn what I can do!          # no arguments
Oh, help? I actually don't do much, but I do have this flag here: picoCTF{...}
```

### Route not taken: the picoCTF webshell

The intended environment. The challenge page provides a browser-based
x86-64 Linux host where `./warm -h` runs natively with no setup. Faster,
but it teaches nothing about why the binary would not run locally.

### Route not taken: don't execute at all

```bash
strings warm | grep -i pico
```

Works because the binary is `not stripped` and the flag is a plain literal
in the data section. A legitimate CTF technique, and the right call when a
binary is untrusted — but it bypasses the entire lesson of this challenge.

## Commands Or Script

No `solve.py`. The solve is a single `docker run` invocation, recorded
above; there is no derivation to pin down or property to assert.

## Flag

```text
picoCTF{b1scu1ts_4nd_gr4vy_ac5832c}
```

## Lessons Learned

- **"Works on my machine" has a precise mechanical cause.** A compiled
  artifact carries OS and architecture in its header. Both must match the
  host. This is why CI builds on the same platform as prod, why images are
  tagged by architecture, and why Apple Silicon caused an industry-wide
  scramble. `--platform linux/amd64` is the same flag people reach for when
  an M-series Mac builds an image that crashes on an x86 server.
- **Run unknown binaries in a container, not on your host.** CTF binaries
  are untrusted code. The Docker one-liner above is not just an emulation
  workaround — it is a disposable sandbox, and the right default instinct.
- **Emulation is a tax.** Rosetta/QEMU translate x86-64 to arm64 at
  runtime. Invisible for this binary; significant when building real
  images. Prefer native `linux/arm64` where available.
- **Every `-v` is a hole in the isolation.** Bind-mounting is the container
  reaching into the host filesystem. "Just mount the home directory" is a
  genuine finding in a security review.
- **`file` first, always.** One command answers OS, architecture, PIE,
  linkage, and whether symbols survived — the four things that decide how
  the rest of a binary challenge goes.

## Follow-Up

- Added the binary-execution triage (error table, `file` field decode, the
  Docker one-liner) to [../../../../../notes/general.md](../../../../../notes/general.md).
- `pie` and `not stripped` are the two fields that carry straight into
  binary exploitation — see [../../../../../notes/pwn.md](../../../../../notes/pwn.md).
- The `warm` binary is not committed. It is a 19 KB redistributable
  challenge file; commit it if reproducibility matters more than repo
  weight, and add a `.gitattributes` entry if binaries start accumulating.
