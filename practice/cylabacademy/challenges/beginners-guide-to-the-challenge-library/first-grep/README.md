# First Grep

## Metadata

- Platform: CyLab Academy / picoCTF
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: General Skills
- Difficulty: Beginner
- Status: Solved
- Started: 2026-08-12
- Completed: 2026-08-12
- Files: `file` (ASCII text, 14 KB)
- Skills Learned: `grep`, regular expressions, shell quoting

## Problem Summary

The challenge provides a text file named `file`. Find the picoCTF flag hidden
inside the file.

This is a command-line filtering challenge: the file is small enough to read,
but noisy enough that searching for the flag pattern is the better habit.

## First Observations

```bash
file file
```

```text
file: ASCII text, with very long lines (14545)
```

The file is plain text, so there is no decoding, extraction, or binary analysis
needed. The goal is to search the text for the known picoCTF flag shape.

## What I Tried

At first I tried:

```bash
cat first-grep/file | grep picoCTF\{\*\}
```

That failed for two separate reasons:

- `first-grep/file` only works when the shell is already in the parent folder.
- In basic `grep` regex, `*` repeats the previous token. It does not mean
  "match anything" by itself.

## Key Idea

picoCTF flags usually look like:

```text
picoCTF{...}
```

So the reusable regex is:

```text
picoCTF{[^}]*}
```

`[^}]*` means "match zero or more characters that are not a closing brace."
That lets the search stop cleanly at the end of the flag.

## Solution Walkthrough

From the repository root, run:

```bash
grep -o 'picoCTF{[^}]*}' practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/first-grep/file
```

Output:

```text
picoCTF{grep_is_good_to_find_things_beD770f5}
```

The `-o` flag tells `grep` to print only the matching part instead of the full
line. That matters here because the file has very long lines.

## Commands Or Script

```bash
grep -o 'picoCTF{[^}]*}' file
```

If running from the repository root:

```bash
grep -o 'picoCTF{[^}]*}' practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/first-grep/file
```

## Flag

```text
picoCTF{grep_is_good_to_find_things_beD770f5}
```

## Lessons Learned

- `grep` searches text for matching patterns.
- Use `grep -o` when you only want the matching flag, not the whole line.
- In regex, `*` repeats the previous token; use `.*` for "anything" or
  `[^}]*` when you want "anything until the closing brace."
- Avoid unnecessary `cat file | grep ...`; `grep pattern file` is simpler.

## Follow-Up

- Practice reading regex as small pieces: literal prefix, character class,
  repetition, literal suffix.
