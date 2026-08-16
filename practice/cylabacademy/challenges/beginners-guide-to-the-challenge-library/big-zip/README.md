# Big Zip

## Metadata

- Platform: CyLab Academy / picoCTF
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: General Skills
- Difficulty: Beginner
- Status: Solved
- Started: 2026-08-16
- Completed: 2026-08-16
- Files: `big-zip-files.zip` (extracts to `big-zip-files/`)
- Skills Learned: zip inspection, safe extraction, recursive text search, `rg`

## Problem Summary

The challenge provides a large zip archive with many text files. Find the
picoCTF flag hidden somewhere inside the extracted directory tree.

This is the same core lesson as [First Grep](../first-grep/README.md), but
with many files instead of one file.

## First Observations

Before extracting a zip from a challenge, inspect the archive paths:

```bash
unzip -Z1 big-zip-files.zip | head -40
unzip -Z1 big-zip-files.zip | grep -E '^/|(^|/)\.\.(/|$)'
unzip -Z1 big-zip-files.zip | wc -l
```

The archive contains 9,090 entries. The safety check produced no output,
which means there were no absolute paths and no `..` parent-directory paths.

After extraction:

```bash
unzip -q big-zip-files.zip
find big-zip-files -type f | wc -l
du -sh big-zip-files big-zip-files.zip
```

```text
8732
34M     big-zip-files
4.0M    big-zip-files.zip
```

That is too many files to inspect manually. The right move is to search.

## Key Idea

**Use recursive search when the data is too large to browse by hand.**

picoCTF flags usually have this shape:

```text
picoCTF{...}
```

So we can search every text file under the extracted directory for that
pattern.

## Solution Walkthrough

Extract the archive after checking that the paths are safe:

```bash
unzip -q big-zip-files.zip
```

Then recursively search the extracted folder:

```bash
rg -n "picoCTF\{[^}]*\}" big-zip-files
```

Output:

```text
big-zip-files/folder_pmbymkjcya/folder_cawigcwvgv/folder_ltdayfmktr/folder_fnpfclfyee/whzxrpivpqld.txt:1:information on the record will last a billion years. Genes and brains and books encode picoCTF{gr3p_15_m4g1c_ef8790dc}
```

Read that result as:

- file path:
  `big-zip-files/folder_pmbymkjcya/folder_cawigcwvgv/folder_ltdayfmktr/folder_fnpfclfyee/whzxrpivpqld.txt`
- line number: `1`
- matching line: the sentence containing the flag

## Commands Or Script

No script needed. The solve is archive extraction plus recursive search:

```bash
unzip -Z1 big-zip-files.zip | grep -E '^/|(^|/)\.\.(/|$)'
unzip -q big-zip-files.zip
rg -n "picoCTF\{[^}]*\}" big-zip-files
```

If `rg` is not installed, use `grep -R`:

```bash
grep -RnoE "picoCTF\{[^}]*\}" big-zip-files
```

Useful command details:

- `rg` is `ripgrep`, a fast recursive search tool.
- `-n` shows line numbers.
- `picoCTF\{` matches the literal flag prefix.
- `[^}]*` means "keep matching characters until the next closing brace."
- `\}` matches the literal closing brace.

## Flag

```text
picoCTF{gr3p_15_m4g1c_ef8790dc}
```

## Lessons Learned

- Check zip paths before extraction. Absolute paths or `..` entries can
  write files outside the folder you meant to use.
- Large file trees are search problems, not manual browsing problems.
- `rg` is useful because it recursively searches directories quickly and
  prints the file path and line number of each hit.
- The reusable picoCTF search pattern is `picoCTF\{[^}]*\}` when using
  regex tools that treat braces as special characters.

## Follow-Up

- Keep practicing the same search idea across one file, many files, and
  extracted archives. The tool changes less than the input shape.
