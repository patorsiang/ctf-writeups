# Extremely Convenient Breaker

## Metadata

- Event: LA CTF 2025
- Category: Crypto
- Difficulty: Unknown
- Status: Solved
- Files: [chall.py](chall.py), [main.py](main.py)
- Skills Learned: Oracle interaction, block handling, socket scripting

## Problem Summary

The service prints an encrypted flag and accepts ciphertext queries.

## What I Tried

Connect to the service, capture the encrypted flag, split it into 16-byte blocks, and test how the oracle responds to repeated blocks.

## Key Idea

The oracle leaks useful decrypted output when a target block is repeated enough times. Querying each encrypted block separately recovers the plaintext block by block.

## Solution Walkthrough

The solve script in [main.py](main.py) connects to the challenge, extracts the encrypted flag, splits it into 16-byte blocks, sends each block repeated four times, and joins the returned plaintext.

## Flag

`lactf{seems_it_was_extremely_convenient_to_get_the_flag_too_heh}`

## Lessons Learned

- When a service decrypts chosen ciphertext, test block-level behavior carefully.
- Automate oracle queries once the pattern is known.
