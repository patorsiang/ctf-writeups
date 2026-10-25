# First Find

## Metadata

- Platform: CyLab Academy
- Learning Path: General Skills in CTF's
- Category: General Skills / File Search
- Difficulty: Easy
- Status: Solved
- Started: 2026-10-25
- Completed: 2026-10-25
- Re-solve: due 2026-11-01
- Files: `files.zip` and extracted `files/` tree (local-only challenge inputs)
- Skills Learned: `unzip`, recursive `find`, `cat`, hidden directories

## Problem Summary

The challenge provides a ZIP archive and asks me to find a file named
`uber-secret.txt`.

## First Observations

- The prompt gives the exact filename to find.
- The archive has 22 entries and nests the target several directories deep.
- The target is inside a dot-prefixed `.secret` directory.

## Solve Log

No intermediate hypothesis was recorded before tool use. This log records the
observed actions.

- **Tried:** Inspected the ZIP member names for `uber-secret.txt`.
  - **Result:** Found one regular file at
    `files/adequate_books/more_books/.secret/deeper_secrets/deepest_secrets/uber-secret.txt`.
- **Tried:** Extracted the archive into this challenge folder and read the found
  path with `cat`.
  - **Result:** The file printed the flag below.

## Key Idea

Search the extracted tree by filename instead of opening every book file.
`find` also searches dot-prefixed directories such as `.secret` by default.

## Solution Walkthrough

Download `files.zip` from the challenge page, then run these commands from this
challenge directory:

```sh
unzip -n files.zip -d .
find files -type f -name 'uber-secret.txt' -print
cat files/adequate_books/more_books/.secret/deeper_secrets/deepest_secrets/uber-secret.txt
```

The search finds the target under `files/adequate_books/`. Read that file to
recover the flag.

## Commands Or Script

The commands above reproduce the extraction, recursive filename search, and
read. The ZIP contains the original challenge files; no separate solve script
is needed.

## Flag

```text
academy{f1nd_15_f457_ab443fd1}
```

## Verification

`cat` printed the flag shown above. CyLab flag submission and learning-path
completion were not confirmed.

## Lessons Learned

- Search nested challenge files with `find` before opening files one by one.
- Dot-prefixed directories are still included in a normal `find` search.
- Recovering a flag does not confirm that the learning platform accepted it.

## Follow-Up

- Re-solve from the archive without notes or AI on 2026-11-01. Record the result
  in [the queue](../../../queue.md).

## References

- [CyLab Academy: First Find](https://learn.cylabacademy.org/learning-paths/14/103)
