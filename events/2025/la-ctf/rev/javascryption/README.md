# Javascryption

## Metadata

- Event: LA CTF 2025
- Category: Rev
- Difficulty: Unknown
- Status: Solved
- Files: None
- Skills Learned: Reversing JavaScript transformations

## Problem Summary

The challenge validates a flag after applying several JavaScript string transformations.

## What I Tried

Read the validation function and list each transformation in order: base64 encode, reverse, replace `Z`, URL encode, and base64 encode again.

## Key Idea

Reverse the transformations in the opposite order.

## Solution Walkthrough

Decode the stored base64 string, URL-decode it, replace `[OLD_DATA]` back to `Z`, reverse the string, then base64-decode the result.

## Flag

`lactf{no_grizzly_walls_here}`

## Lessons Learned

- Reversing code is often just careful bookkeeping of transformations and order.
