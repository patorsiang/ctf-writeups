# Lucky Flag

## Metadata

- Event: LA CTF 2025
- Category: Web
- Difficulty: Beginner
- Status: Solved
- Files: [snapshot.png](snapshot.png)
- Skills Learned: JavaScript string decoding, XOR

## Problem Summary

The web challenge hides the flag behind a small client-side transformation.

## What I Tried

The page source contains an encoded string. Because the decoding logic is client-side JavaScript, it can be reproduced locally.

## Key Idea

Each character in the encoded string is XORed with `0x62`. Reversing XOR with the same key recovers the plaintext flag.

## Solution Walkthrough

Use JavaScript to convert each character to its char code, XOR it with `0x62`, then join the result back into a string.

## Flag

`lactf{w4s_i7_luck_0r_ski11}`

## Lessons Learned

- Client-side secrets should be treated as visible.
- XOR is reversible with the same key.
