# What's A Net Cat?

## Metadata

- Platform: CyLab Academy / picoCTF
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: Networking
- Difficulty: Beginner
- Status: Solved
- Started:
- Completed: 2026-08-01
- Files:
- Skills Learned: Netcat, TCP service connections, host and port syntax

## Problem Summary

Connect to the remote picoCTF service with `nc` and read the flag returned by
the server.

## First Observations

- Host: `fickle-tempest.picoctf.net`
- Port: `64689`

The challenge is about connecting to a raw TCP service, not logging in through a browser or SSH.

## What I Tried

The challenge gives a hostname and port, so the direct test is to connect with Netcat.

## Key Idea

Netcat opens a TCP connection to a host and port. It is useful in CTFs because many beginner services print a message or wait for simple text input.

## Solution Walkthrough

The challenge provides a hostname and port. Use `nc`, also known as Netcat, to
open a TCP connection to that service:

```bash
nc fickle-tempest.picoctf.net 64689
```

The server responds with a short message and the flag:

```text
You're on your way to becoming the net cat master
picoCTF{nEtCat_Mast3ry_95035DAa}
```

## Flag

```text
picoCTF{nEtCat_Mast3ry_95035DAa}
```

## Lessons Learned

- `nc` is useful in CTFs because it lets you connect directly to services running on specific ports.
- The basic syntax is:

```bash
nc <host> <port>
```

## Follow-Up

- For future service challenges, first identify whether the connection should use `nc`, `ssh`, `curl`, or a browser.
