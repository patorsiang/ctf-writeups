# Extended

## Metadata

- Event: LA CTF 2025
- Category: Misc
- Difficulty: Unknown
- Status: Solved
- Files: [chall.txt](chall.txt), [gen.py](gen.py), [main.py](main.py)
- Skills Learned: Cross-platform text behavior

## Problem Summary

The challenge behavior differs between Mac and Windows.

## What I Tried

Inspect the provided text and generation script to understand why platform behavior changes the visible result.

## Key Idea

Cross-platform differences can affect how text, Unicode, or line endings are interpreted.

## Solution Walkthrough

Use the provided scripts and challenge text to reproduce the expected output.

## Flag

`lactf{Funnily_Enough_This_Looks_Different_On_Mac_And_Windows}`

## Lessons Learned

- Misc challenges often depend on environment-specific behavior.
