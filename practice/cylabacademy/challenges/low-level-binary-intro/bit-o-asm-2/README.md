# Bit-O-Asm-2

## Metadata

- Platform: CyLab Academy
- Learning Path: Low Level Binary Intro
- Category: Reverse Engineering / x86-64
- Difficulty: Easy
- Status: Solved; portal submission not confirmed
- Started: 2026-10-29
- Completed: 2026-10-29
- Re-solve: due 2026-11-05
- Files: [`disassembler-dump0_b.txt`](disassembler-dump0_b.txt)
- Skills Learned: x86-64 register tracking, stack-local data flow, hexadecimal-to-decimal conversion

## Problem Summary

Read an x86-64 assembly dump and report the final value of the `eax` register in decimal. The Academy asks for the answer in `academy{n}` format.

Source: [CyLab Academy: Bit-O-Asm-2](https://learn.cylabacademy.org/learning-paths/2/19).

## First Observations

- The dump uses Intel syntax, where `mov destination, source` copies the source into the destination.
- At offset `+15`, the code stores `0x9fe1a` in a stack-local slot at `[rbp-0x4]`.
- At offset `+22`, the code loads that slot into `eax`.
- The later `pop rbp` and `ret` instructions do not overwrite `eax`.

## Solve Log

- **Observed:** `mov DWORD PTR [rbp-0x4],0x9fe1a` stores the hexadecimal value in a local stack slot.
- **Traced:** `mov eax,DWORD PTR [rbp-0x4]` copies the stored value into `eax`.
- **Converted:** `0x9fe1a` equals decimal `654874`.
- **Formatted:** Wrapped the decimal register value in the required Academy flag format.

## Key Idea

Follow the value through memory. The immediate constant first goes into `[rbp-0x4]`, then the next `mov` loads it into `eax`. Convert the hexadecimal value to decimal because the challenge requests decimal output.

## Solution Walkthrough

1. Find the immediate value stored by `mov DWORD PTR [rbp-0x4],0x9fe1a`.
2. Follow the next instruction, `mov eax,DWORD PTR [rbp-0x4]`, to see that the value reaches `eax`.
3. Convert `0x9fe1a` to decimal: `9 × 16^4 + 15 × 16^3 + 14 × 16^2 + 1 × 16 + 10 = 654874`.
4. Confirm the function returns without another instruction changing `eax`.
5. Format the answer as `academy{654874}`.

## Flag

```text
academy{654874}
```

## Verification

The disassembly stores `0x9fe1a` and loads it into `eax`; decimal conversion gives `654874`. CyLab portal submission and learning-path completion are not confirmed.

## Lessons Learned

- Track register values through stack-local memory when instructions store and reload them.
- Read Intel syntax with the destination first and source second.
- Convert hexadecimal values to the number base requested by the challenge.

## Follow-Up

- Re-solve without notes or AI on 2026-11-05. Record the result in [the queue](../../../queue.md).
