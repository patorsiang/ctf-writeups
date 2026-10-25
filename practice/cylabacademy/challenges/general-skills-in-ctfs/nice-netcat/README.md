# Nice netcat...

## Metadata

- Platform: CyLab Academy / picoCTF 2021
- Learning Path: General Skills in CTF's
- Category: General Skills / Networking
- Difficulty: Easy
- Status: Solved
- Started: 2026-10-24
- Completed: 2026-10-24
- Re-solve: due 2026-10-31
- Files: None
- Skills Learned: Netcat, TCP connections, decimal ASCII decoding

## Problem Summary

The challenge provides a shell command for connecting to a small TCP service. The service returns numbers instead of readable text. The goal is to decode its response and recover the flag.

## Prediction

- Guess: Not recorded before running the command.
- Score: n/a

## First Observations

- The challenge supplied a command in the form `nc <host> <port>`.
- The service returned one decimal number per line, ending with `125` and `10`.
- The values fit ASCII's decimal code points.

## Solve Log

- **Thought:** The host and port in the prompt identify a TCP service.
  - **Tried:** Ran the provided `nc <host> <port>` command.
  - **Result:** The service returned decimal numbers instead of readable text.
- **Thought:** Decode the numbers as ASCII, as requested.
  - **Tried:** Converted each decimal value to its matching ASCII character and joined the characters in order.
  - **Result:** The characters formed the flag. The final value, `10`, is a newline.

## Key Idea

Netcat opens a TCP connection and prints the service's response. Each returned number is a decimal ASCII code point: for example, `97` is `a`, `123` is `{`, and `10` is a line feed. Convert the values in order to reconstruct the text.

## Solution Walkthrough

1. Copy the host and port from the active challenge instance.
2. Connect with `nc <host> <port>`.
3. Convert each returned decimal value to its ASCII character.
4. Join the characters in order. Keep digits such as `0` and `1` exactly as returned.

## Commands Or Script

Use the instance's current host and port; they can change when the instance restarts:

```sh
nc <host> <port>
```

## Flag

```text
academy{g00d_k1tty!_n1c3_k1tty!_57380}
```

## Verification

The service response decoded to the flag above. Portal submission and learning-path completion were not confirmed.

## Lessons Learned

- Netcat can retrieve text or encoded data from a TCP service.
- Decimal ASCII values map directly to characters; preserve the original order and digits.
- A recovered flag does not confirm that the learning platform accepted it.

## Follow-Up

- Re-solve this challenge from the raw output without notes on 2026-10-31.
