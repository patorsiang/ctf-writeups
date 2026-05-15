# K

## Metadata

- Event: TCP1P 2024
- Category: Pwn
- Difficulty: Unknown
- Status: Solved
- Files: [K.tar.gz](K.tar.gz)
- Skills Learned: Archive inspection, remote service interaction

## Problem Summary

Author: rui

For yall who like K pwn

Connection: nc ctf.tcp1p.team 20024

## What I Tried

The challenge gives an archive and a remote service. The first useful step is to unpack the archive and inspect its folder structure before connecting.

## Key Idea

The archive structure is part of the puzzle. Inspecting it gives the clue needed to answer the remote service.

## Solution Walkthrough

unzip the find K.tar.gz to look the folders structure and connect to the server

<img width="313" alt="Screenshot 2567-10-13 at 19 10 02" src="https://github.com/user-attachments/assets/691b0ef8-aa50-4740-ae4c-f2d97985fa99">

## Flag

`TCP1P{https://youtu.be/L4sbDxR22z4?si=_IYkQ1yh_S3kDxQE}`

## Lessons Learned

- In pwn challenges, do not skip simple artifact inspection before exploit work.
