# Static Ain't Always Noise

## Metadata

- Platform: CyLab Academy / picoCTF 2021
- Learning Path: General Skills in CTF's
- Category: General Skills / Static Analysis
- Difficulty: Easy
- Status: Solved
- Started: 2026-10-25
- Completed: 2026-10-25
- Re-solve: due 2026-11-01
- Files: `static`, `ltdis.sh`, `static.ltdis.x86_64.txt`, `static.ltdis.strings.txt`
- Skills Learned: Bash scripts, `objdump`, `strings`, static analysis

## Problem Summary

The challenge provides a binary named `static` and a Bash helper named
`ltdis.sh`. The prompt asks me to inspect the binary and says the script might
help.

## First Observations

- `ltdis.sh` takes a program filename as its first argument.
- The script runs `objdump` on the binary's `.text` section and runs `strings`
  across the file.
- The downloaded script had mode `644`, so I invoked it through Bash.

## Solve Log

- **Thought:** The helper could reveal readable text as well as disassembly, so
  inspect the script before running it.
  - **Tried:** Read `ltdis.sh` as text.
  - **Result:** It writes `static.ltdis.x86_64.txt` and
    `static.ltdis.strings.txt` for the supplied binary.
- **Thought:** Run the helper with the provided binary as its argument.
  - **Tried:** Ran the script from the repository root, passing the challenge
    binary path as its argument.
  - **Result:** The script succeeded and generated both reports.
- **Thought:** Check the strings report for the flag text.
  - **Tried:** Searched `static.ltdis.strings.txt`.
  - **Result:** Found the flag at file offset `0x3020`.

## Key Idea

The `strings` report exposes printable text embedded in a binary. The script
uses `strings -a -t x`, so it scans the whole file and shows each string's
hexadecimal file offset. The disassembly report was available, but the strings
report contained the flag directly.

## Solution Walkthrough

Run these commands from this challenge directory:

```sh
bash ltdis.sh static
rg -n 'academy\{' static.ltdis.strings.txt
```

Read the matching string from the report. The `0x3020` offset helps locate the
same bytes in the original binary.

## Commands Or Script

`ltdis.sh` is the challenge-provided helper. Its output files separate the
disassembly from printable strings, so search the strings report first when
looking for readable data.

## Flag

```text
academy{d15a5m_t34s3r_fac3431a}
```

## Verification

The flag appeared in `static.ltdis.strings.txt` at offset `0x3020`. CyLab flag
submission and learning-path completion were not confirmed.

## Lessons Learned

- Read a helper script before running it; its arguments and output files were
  clear from the source.
- Use `bash script-name binary-name` when a downloaded script lacks its
  executable bit.
- Search printable strings before studying a full disassembly when the goal is
  to locate readable text.
- `strings -t x` reports offsets in hexadecimal.

## Follow-Up

- Re-solve from the binary without notes or AI on 2026-11-01. Record the result
  in [the queue](../../../queue.md).

## References

- [CyLab Academy: Static Ain't Always Noise](https://learn.cylabacademy.org/learning-paths/14/105)
