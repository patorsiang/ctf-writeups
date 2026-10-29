# Bit-O-Asm-1

## Metadata

- Platform: CyLab Academy
- Learning Path: Low Level Binary Intro
- Category: Reverse Engineering / x86-64
- Difficulty: Easy
- Status: Solved; portal submission not confirmed
- Started: 2026-10-29
- Completed: 2026-10-29
- Re-solve: due 2026-11-05
- Files: [`disassembler-dump0_a.txt`](disassembler-dump0_a.txt)
- Skills Learned: x86-64 register tracking, Intel syntax, hexadecimal-to-decimal conversion

## Problem Summary

Read a short x86-64 assembly dump and report the final value of the `eax` register in decimal. The Academy asks for the answer in `academy{n}` format.

Source: [CyLab Academy: Bit-O-Asm-1](https://learn.cylabacademy.org/learning-paths/2/17).

## First Observations

- The dump uses Intel syntax, where `mov destination, source` copies the source into the destination.
- The instruction at offset `+15` is `mov eax,0x30`.
- The following `pop rbp` and `ret` instructions do not overwrite `eax`.

## Solve Log

- **Observed:** The function loads immediate value `0x30` into `eax` at offset `+15`.
- **Checked:** No later instruction changes `eax` before the function returns.
- **Converted:** `0x30` is hexadecimal for `3 × 16 + 0`, which equals decimal `48`.
- **Formatted:** Wrapped the decimal register value in the required Academy flag format.

## Key Idea

Track writes to the requested register. The `mov` instruction sets `eax` to `0x30`, and the remaining instructions leave that value unchanged. Convert the hexadecimal value to decimal before formatting the flag.

## Solution Walkthrough

1. Find the instruction that writes to `eax`: `mov eax,0x30`.
2. Read `mov` operands in Intel order: the first operand is the destination, and the second is the source.
3. Convert `0x30` to decimal: `3 × 16 + 0 = 48`.
4. Confirm later instructions do not change `eax`.
5. Format the answer as `academy{48}`.

## Flag

```text
academy{48}
```

## Verification

The disassembly sets `eax` to `0x30`, which is decimal `48`. CyLab portal submission and learning-path completion are not confirmed.

## Lessons Learned

- In Intel syntax, `mov destination, source` writes the second operand into the first.
- Check later instructions before assuming a register keeps its value.
- Convert hexadecimal values to the number base requested by the challenge.

## Follow-Up

- Re-solve without notes or AI on 2026-11-05. Record the result in [the queue](../../../queue.md).
