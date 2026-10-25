# plumbing

## Metadata

- Platform: CyLab Academy / picoCTF 2019
- Learning Path: General Skills in CTF's
- Category: General Skills / Pipelines
- Difficulty: Medium
- Status: Solved
- Started: 2026-10-25
- Completed: 2026-10-25
- Re-solve: due 2026-11-01
- Files: Live service output in `output/plumbing-output.txt`
- Skills Learned: Netcat, pipelines, `tee`, `grep`

## Problem Summary

The challenge runs a program that prints many lines. It asks me to keep the
program's output and search it for the flag.

## First Observations

- The instance provides a host and port; those values can change after restart.
- A direct `nc` run printed 10,002 lines, and the terminal transcript was
  truncated.
- The output contains decoy lines, so filtering the stream is useful.

## Solve Log

- **Thought:** The raw output is too large to inspect in the terminal.
  - **Tried:** Connected with `nc` and let the output print directly.
  - **Result:** The command printed 10,002 lines; the terminal transcript was
    truncated before I could inspect the full output.
- **Thought:** Save the whole stream and search it as it arrives.
  - **Tried:** Ran `nc <host> <port> | tee plumbing-output.txt | grep -F '{'`.
  - **Result:** `tee` saved the stream, and `grep` printed
    `academy{digital_plumb3r_CB83CD6b}`. The captured output contained the same
    flag at line 2750.

## Key Idea

`tee` copies standard input to a file and standard output. That lets the pipe
save the complete stream while sending the same data to `grep`. `grep -F '{'`
searches for a literal opening brace, which isolates the brace-wrapped flag
from the decoy lines.

## Solution Walkthrough

Use the current host and port shown by the challenge instance. Run this from
the challenge directory:

```sh
nc <host> <port> | tee output/plumbing-output.txt | grep -F '{'
```

The command keeps the full response in `output/plumbing-output.txt` and prints
lines containing `{` to the terminal.

## Commands Or Script

No separate script is needed. The challenge uses standard shell pipes: `tee`
captures the output and forwards it, then `grep` filters the forwarded stream.

## Flag

```text
academy{digital_plumb3r_CB83CD6b}
```

## Verification

The successful command printed the flag, and the captured output contains it
at line 2750. CyLab flag submission and learning-path completion were not
confirmed.

## Lessons Learned

- A pipe sends one command's standard output to the next command's standard
  input.
- `tee` saves a copy without stopping the pipeline.
- Use `grep -F` when searching for literal characters such as `{`.
- Use the current instance host and port; they can change after restart.

## Follow-Up

- Re-solve from the live instance without notes or AI on 2026-11-01. Record the
  result in [the queue](../../../queue.md).

## References

- [CyLab Academy: plumbing](https://learn.cylabacademy.org/learning-paths/14/107)
