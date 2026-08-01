# Obedient Cat

## Metadata

- Platform: CyLab Academy / picoCTF
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: General
- Difficulty: Beginner
- Status: Solved
- Started:
- Completed: 2026-08-01
- Files: `flag`
- Skills Learned: file inspection, `ls`, `cat`

## Problem Summary

The challenge provides a file named `flag`.

The goal is to read the file from the terminal. This is a warm-up challenge for basic Linux command-line navigation and file inspection.

## First Observations

- The challenge directory contains one file named `flag`.
- The filename strongly suggests the flag is stored directly in that file.

## What I Tried

The challenge hint points toward reading the file, so the first useful step is to list the directory and inspect the file content.

## Key Idea

`cat` prints a file's contents to the terminal. For beginner CTF challenges, this is often the first command to try when the challenge gives you a plain file.

## Solution Walkthrough

List the files in the challenge directory:

```bash
ls
```

The only file is:

```text
flag
```

Since the challenge hint is essentially telling us to read the file, use `cat`:

```bash
cat flag
```

Output:

```text
picoCTF{s4n1ty_v3r1f13d_9b8fa0bc}
```

## Flag

```text
picoCTF{s4n1ty_v3r1f13d_9b8fa0bc}
```

## Lessons Learned

- `cat` prints the contents of a file to the terminal.
- In beginner CTF challenges, sometimes the goal is simply to practice basic Linux commands and verify that you can inspect files from the command line.

## Follow-Up

- Keep practicing `ls`, `cat`, `file`, and `strings` because they are common first checks in many CTF categories.
